import Foundation

enum DecodeError: Error {
    case invalid(String)
}

func decodeVarUInt(_ data: Data, _ offset: inout Int) throws -> UInt32 {
    var value: UInt32 = 0
    var shift: UInt32 = 0
    while offset < data.count {
        let byte = data[offset]
        offset += 1
        value |= UInt32(byte & 0x7F) << shift
        if (byte & 0x80) == 0 {
            return value
        }
        shift += 7
        if shift > 35 {
            throw DecodeError.invalid("varuint overflow")
        }
    }
    throw DecodeError.invalid("unexpected end of stream while decoding varuint")
}

func zigzagDecode(_ value: UInt32) -> Int32 {
    return Int32(bitPattern: (value >> 1)) ^ -Int32(value & 1)
}

func decodeDeltaRLE(_ encoded: Data, count: Int) throws -> [Int32] {
    if count == 0 { return [] }
    var out: [Int32] = []
    out.reserveCapacity(count)
    var offset = 0
    while out.count < count {
        if offset >= encoded.count {
            throw DecodeError.invalid("delta stream ended before expected count")
        }
        let deltaEnc = try decodeVarUInt(encoded, &offset)
        let run = Int(try decodeVarUInt(encoded, &offset))
        if run == 0 {
            throw DecodeError.invalid("delta stream contains zero-length run")
        }
        let delta = zigzagDecode(deltaEnc)
        for _ in 0..<run {
            out.append(delta)
            if out.count > count {
                throw DecodeError.invalid("delta stream run lengths overflow point count")
            }
        }
    }
    if offset != encoded.count {
        throw DecodeError.invalid("delta stream has trailing bytes")
    }
    return out
}

func readU16(_ data: Data, _ offset: inout Int) throws -> UInt16 {
    guard offset + 2 <= data.count else { throw DecodeError.invalid("unexpected end of payload (u16)") }
    defer { offset += 2 }
    return data.withUnsafeBytes { ptr in
        ptr.loadUnaligned(fromByteOffset: offset, as: UInt16.self)
    }.littleEndian
}

func readI16(_ data: Data, _ offset: inout Int) throws -> Int16 {
    guard offset + 2 <= data.count else { throw DecodeError.invalid("unexpected end of payload (i16)") }
    defer { offset += 2 }
    return data.withUnsafeBytes { ptr in
        ptr.loadUnaligned(fromByteOffset: offset, as: Int16.self)
    }.littleEndian
}

func readU32(_ data: Data, _ offset: inout Int) throws -> UInt32 {
    guard offset + 4 <= data.count else { throw DecodeError.invalid("unexpected end of payload (u32)") }
    defer { offset += 4 }
    return data.withUnsafeBytes { ptr in
        ptr.loadUnaligned(fromByteOffset: offset, as: UInt32.self)
    }.littleEndian
}

func readI32(_ data: Data, _ offset: inout Int) throws -> Int32 {
    guard offset + 4 <= data.count else { throw DecodeError.invalid("unexpected end of payload (i32)") }
    defer { offset += 4 }
    return data.withUnsafeBytes { ptr in
        ptr.loadUnaligned(fromByteOffset: offset, as: Int32.self)
    }.littleEndian
}

func crc32(_ data: Data) -> UInt32 {
    var crc: UInt32 = 0xFFFF_FFFF
    for byte in data {
        crc ^= UInt32(byte)
        for _ in 0..<8 {
            if (crc & 1) == 1 {
                crc = (crc >> 1) ^ 0xEDB8_8320
            } else {
                crc >>= 1
            }
        }
    }
    return ~crc
}

func checkedEnd(_ offset: Int, _ len: Int, _ total: Int, _ label: String) throws -> Int {
    let end = offset + len
    if end < offset || end > total {
        throw DecodeError.invalid("\(label) length overflows payload")
    }
    return end
}

func decode(_ input: Data) throws -> [String: Any] {
    guard input.count >= 22 else { throw DecodeError.invalid("stream too short for header") }
    let magic = input.subdata(in: 0..<5)
    guard String(data: magic, encoding: .ascii) == "ZPINK" else { throw DecodeError.invalid("invalid magic") }

    var headerOffset = 5
    let version = input[headerOffset]
    headerOffset += 1
    guard version == 1 else { throw DecodeError.invalid("unsupported version") }

    let modeCode = input[headerOffset]
    headerOffset += 1
    let mode: String
    switch modeCode {
    case 0: mode = "lossless"
    case 1: mode = "high"
    case 2: mode = "medium"
    case 3: mode = "sketch"
    default: throw DecodeError.invalid("invalid mode code")
    }

    let flags = input[headerOffset]
    headerOffset += 1
    guard (flags & 0b001) != 0 else { throw DecodeError.invalid("pressure channel is mandatory") }

    let strokeCount = Int(try readU16(input, &headerOffset))
    let seed = try readU32(input, &headerOffset)
    let payloadLen = Int(try readU32(input, &headerOffset))
    let payloadCRC = try readU32(input, &headerOffset)

    let payload = input.subdata(in: 22..<input.count)
    guard payload.count == payloadLen else { throw DecodeError.invalid("payload length mismatch") }
    guard crc32(payload) == payloadCRC else { throw DecodeError.invalid("payload CRC mismatch") }

    var offset = 0
    var strokes: [[String: Any]] = []
    strokes.reserveCapacity(strokeCount)

    let hasTilt = (flags & 0b010) != 0
    let hasAzimuth = (flags & 0b100) != 0

    for _ in 0..<strokeCount {
        let pointCount = Int(try readU16(payload, &offset))
        if pointCount == 0 { throw DecodeError.invalid("stroke has zero points") }

        let x0 = Int32(try readI32(payload, &offset))
        let y0 = Int32(try readI32(payload, &offset))

        let xLen = Int(try readU32(payload, &offset))
        let xEnd = try checkedEnd(offset, xLen, payload.count, "x stream")
        let xDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<xEnd), count: pointCount - 1)
        offset = xEnd

        let yLen = Int(try readU32(payload, &offset))
        let yEnd = try checkedEnd(offset, yLen, payload.count, "y stream")
        let yDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<yEnd), count: pointCount - 1)
        offset = yEnd

        var x: [Int32] = [x0]
        var y: [Int32] = [y0]
        for d in xDeltas { x.append(x.last! + d) }
        for d in yDeltas { y.append(y.last! + d) }

        let p0 = Int32(try readU16(payload, &offset))
        let pLen = Int(try readU32(payload, &offset))
        let pEnd = try checkedEnd(offset, pLen, payload.count, "pressure stream")
        let pDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<pEnd), count: pointCount - 1)
        offset = pEnd

        var pressure: [Int32] = [p0]
        for d in pDeltas {
            let next = pressure.last! + d
            if next < 0 || next > 1023 { throw DecodeError.invalid("pressure out of range") }
            pressure.append(next)
        }

        var tilt: [Int32] = Array(repeating: 0, count: pointCount)
        if hasTilt {
            let t0 = Int32(try readI16(payload, &offset))
            let tLen = Int(try readU32(payload, &offset))
            let tEnd = try checkedEnd(offset, tLen, payload.count, "tilt stream")
            let tDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<tEnd), count: pointCount - 1)
            offset = tEnd
            tilt = [t0]
            for d in tDeltas {
                let next = tilt.last! + d
                if next < -900 || next > 900 { throw DecodeError.invalid("tilt out of range") }
                tilt.append(next)
            }
        }

        var azimuth: [Int32] = Array(repeating: 0, count: pointCount)
        if hasAzimuth {
            let a0 = Int32(try readI16(payload, &offset))
            let aLen = Int(try readU32(payload, &offset))
            let aEnd = try checkedEnd(offset, aLen, payload.count, "azimuth stream")
            let aDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<aEnd), count: pointCount - 1)
            offset = aEnd
            azimuth = [a0]
            for d in aDeltas {
                let next = azimuth.last! + d
                if next < 0 || next > 3600 { throw DecodeError.invalid("azimuth out of range") }
                azimuth.append(next)
            }
        }

        strokes.append([
            "x": x,
            "y": y,
            "pressure": pressure,
            "tilt": tilt,
            "azimuth": azimuth,
        ])
    }

    if offset != payload.count { throw DecodeError.invalid("payload contains trailing bytes") }

    return [
        "magic": "ZPINK",
        "version": Int(version),
        "mode": mode,
        "flags": Int(flags),
        "seed": Int(seed),
        "strokes": strokes,
    ]
}

let args = CommandLine.arguments
if args.count < 2 {
    fputs("usage: swift scripts/swift_decode.swift <zpink-file>\n", stderr)
    exit(2)
}

let path = args[1]
let data = try Data(contentsOf: URL(fileURLWithPath: path))
let decoded = try decode(data)
let out = try JSONSerialization.data(withJSONObject: decoded, options: [])
if let text = String(data: out, encoding: .utf8) {
    print(text, terminator: "")
}

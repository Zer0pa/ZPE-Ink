import Foundation

public enum ZPEInkError: Error {
    case invalidHeader
    case invalidPayload(String)
}

public struct ZPEInkHeader: Equatable {
    public let version: UInt8
    public let mode: UInt8
    public let flags: UInt8
    public let strokeCount: UInt16
    public let seed: UInt32
    public let payloadLength: UInt32
    public let payloadCRC: UInt32
}

public struct ZPEInkPoint: Equatable {
    public let x: Int32
    public let y: Int32
    public let pressure: Int32
    public let tilt: Int32
    public let azimuth: Int32
}

public struct ZPEInkStroke: Equatable {
    public let x: [Int32]
    public let y: [Int32]
    public let pressure: [Int32]
    public let tilt: [Int32]
    public let azimuth: [Int32]

    public var points: [ZPEInkPoint] {
        zip(zip(zip(x, y), pressure), zip(tilt, azimuth)).map { lhs, rhs in
            let xy = lhs.0
            return ZPEInkPoint(
                x: xy.0,
                y: xy.1,
                pressure: lhs.1,
                tilt: rhs.0,
                azimuth: rhs.1
            )
        }
    }
}

public struct ZPEInkDecoded: Equatable {
    public let magic: String
    public let version: UInt8
    public let mode: String
    public let flags: UInt8
    public let seed: UInt32
    public let strokes: [ZPEInkStroke]

    public func canonicalJSON() -> String {
        let strokesJSON = strokes.map(\.canonicalJSON).joined(separator: ",")
        return """
        {"flags":\(Int(flags)),"magic":"\(magic)","mode":"\(mode)","seed":\(seed),"strokes":[\(strokesJSON)],"version":\(Int(version))}
        """
    }
}

public struct ZPEInk {
    public static let version = "0.1.0"

    private static let magic = "ZPINK"
    private static let headerBytes = 22
    private static let pressureFlag: UInt8 = 0b001
    private static let tiltFlag: UInt8 = 0b010
    private static let azimuthFlag: UInt8 = 0b100

    public static func parseHeader(_ bytes: Data) throws -> ZPEInkHeader {
        guard bytes.count >= headerBytes else { throw ZPEInkError.invalidHeader }
        guard String(data: bytes.subdata(in: 0..<5), encoding: .ascii) == magic else {
            throw ZPEInkError.invalidHeader
        }

        var offset = 5
        let version = bytes[offset]
        offset += 1
        let mode = bytes[offset]
        offset += 1
        let flags = bytes[offset]
        offset += 1
        let strokeCount = try readU16(bytes, &offset)
        let seed = try readU32(bytes, &offset)
        let payloadLength = try readU32(bytes, &offset)
        let payloadCRC = try readU32(bytes, &offset)

        return ZPEInkHeader(
            version: version,
            mode: mode,
            flags: flags,
            strokeCount: strokeCount,
            seed: seed,
            payloadLength: payloadLength,
            payloadCRC: payloadCRC
        )
    }

    public static func decode(_ bytes: Data) throws -> ZPEInkDecoded {
        let header = try parseHeader(bytes)
        guard header.version == 1 else {
            throw ZPEInkError.invalidPayload("unsupported version")
        }

        let mode: String
        switch header.mode {
        case 0: mode = "lossless"
        case 1: mode = "high"
        case 2: mode = "medium"
        case 3: mode = "sketch"
        default:
            throw ZPEInkError.invalidPayload("invalid mode code")
        }

        guard (header.flags & pressureFlag) != 0 else {
            throw ZPEInkError.invalidPayload("pressure channel is mandatory")
        }

        let payload = bytes.subdata(in: headerBytes..<bytes.count)
        guard payload.count == Int(header.payloadLength) else {
            throw ZPEInkError.invalidPayload("payload length mismatch")
        }
        guard crc32(payload) == header.payloadCRC else {
            throw ZPEInkError.invalidPayload("payload CRC mismatch")
        }

        var offset = 0
        var strokes: [ZPEInkStroke] = []
        strokes.reserveCapacity(Int(header.strokeCount))

        let hasTilt = (header.flags & tiltFlag) != 0
        let hasAzimuth = (header.flags & azimuthFlag) != 0

        for strokeIndex in 0..<Int(header.strokeCount) {
            let pointCount = Int(try readU16(payload, &offset))
            if pointCount == 0 {
                throw ZPEInkError.invalidPayload("stroke[\(strokeIndex)] has zero points")
            }

            let x0 = try readI32(payload, &offset)
            let y0 = try readI32(payload, &offset)

            let xLength = Int(try readU32(payload, &offset))
            let xEnd = try checkedEnd(offset, xLength, payload.count, "x stream")
            let xDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<xEnd), count: pointCount - 1)
            offset = xEnd

            let yLength = Int(try readU32(payload, &offset))
            let yEnd = try checkedEnd(offset, yLength, payload.count, "y stream")
            let yDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<yEnd), count: pointCount - 1)
            offset = yEnd

            var x = [x0]
            var y = [y0]
            x.reserveCapacity(pointCount)
            y.reserveCapacity(pointCount)
            for delta in xDeltas { x.append(x.last! + delta) }
            for delta in yDeltas { y.append(y.last! + delta) }

            let pressure0 = Int32(try readU16(payload, &offset))
            let pressureLength = Int(try readU32(payload, &offset))
            let pressureEnd = try checkedEnd(offset, pressureLength, payload.count, "pressure stream")
            let pressureDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<pressureEnd), count: pointCount - 1)
            offset = pressureEnd

            var pressure = [pressure0]
            pressure.reserveCapacity(pointCount)
            for delta in pressureDeltas {
                let next = pressure.last! + delta
                guard (0...1023).contains(next) else {
                    throw ZPEInkError.invalidPayload("pressure out of range")
                }
                pressure.append(next)
            }

            var tilt = Array(repeating: Int32(0), count: pointCount)
            if hasTilt {
                let tilt0 = Int32(try readI16(payload, &offset))
                let tiltLength = Int(try readU32(payload, &offset))
                let tiltEnd = try checkedEnd(offset, tiltLength, payload.count, "tilt stream")
                let tiltDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<tiltEnd), count: pointCount - 1)
                offset = tiltEnd

                tilt = [tilt0]
                tilt.reserveCapacity(pointCount)
                for delta in tiltDeltas {
                    let next = tilt.last! + delta
                    guard (-900...900).contains(next) else {
                        throw ZPEInkError.invalidPayload("tilt out of range")
                    }
                    tilt.append(next)
                }
            }

            var azimuth = Array(repeating: Int32(0), count: pointCount)
            if hasAzimuth {
                let azimuth0 = Int32(try readI16(payload, &offset))
                let azimuthLength = Int(try readU32(payload, &offset))
                let azimuthEnd = try checkedEnd(offset, azimuthLength, payload.count, "azimuth stream")
                let azimuthDeltas = try decodeDeltaRLE(payload.subdata(in: offset..<azimuthEnd), count: pointCount - 1)
                offset = azimuthEnd

                azimuth = [azimuth0]
                azimuth.reserveCapacity(pointCount)
                for delta in azimuthDeltas {
                    let next = azimuth.last! + delta
                    guard (0...3600).contains(next) else {
                        throw ZPEInkError.invalidPayload("azimuth out of range")
                    }
                    azimuth.append(next)
                }
            }

            strokes.append(
                ZPEInkStroke(
                    x: x,
                    y: y,
                    pressure: pressure,
                    tilt: tilt,
                    azimuth: azimuth
                )
            )
        }

        guard offset == payload.count else {
            throw ZPEInkError.invalidPayload("payload contains trailing bytes")
        }

        return ZPEInkDecoded(
            magic: magic,
            version: header.version,
            mode: mode,
            flags: header.flags,
            seed: header.seed,
            strokes: strokes
        )
    }

    public static func decodeToCanonicalJSON(_ bytes: Data) throws -> String {
        try decode(bytes).canonicalJSON()
    }

    private static func checkedEnd(_ offset: Int, _ length: Int, _ total: Int, _ label: String) throws -> Int {
        let end = offset + length
        if end < offset || end > total {
            throw ZPEInkError.invalidPayload("\(label) length overflows payload")
        }
        return end
    }

    private static func decodeDeltaRLE(_ encoded: Data, count: Int) throws -> [Int32] {
        if count == 0 {
            return []
        }

        var output: [Int32] = []
        output.reserveCapacity(count)
        var offset = 0

        while output.count < count {
            if offset >= encoded.count {
                throw ZPEInkError.invalidPayload("delta stream ended before expected count")
            }

            let deltaEncoded = try decodeVarUInt(encoded, &offset)
            let run = Int(try decodeVarUInt(encoded, &offset))
            if run == 0 {
                throw ZPEInkError.invalidPayload("delta stream contains zero-length run")
            }

            let delta = zigzagDecode(deltaEncoded)
            for _ in 0..<run {
                output.append(delta)
                if output.count > count {
                    throw ZPEInkError.invalidPayload("delta stream run lengths overflow point count")
                }
            }
        }

        if offset != encoded.count {
            throw ZPEInkError.invalidPayload("delta stream has trailing bytes")
        }

        return output
    }

    private static func decodeVarUInt(_ data: Data, _ offset: inout Int) throws -> UInt32 {
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
                throw ZPEInkError.invalidPayload("varuint overflow")
            }
        }

        throw ZPEInkError.invalidPayload("unexpected end of stream while decoding varuint")
    }

    private static func zigzagDecode(_ value: UInt32) -> Int32 {
        Int32(bitPattern: value >> 1) ^ -Int32(value & 1)
    }

    private static func readU16(_ data: Data, _ offset: inout Int) throws -> UInt16 {
        guard offset + 2 <= data.count else {
            throw ZPEInkError.invalidPayload("unexpected end of payload (u16)")
        }
        defer { offset += 2 }
        return data.withUnsafeBytes { pointer in
            pointer.loadUnaligned(fromByteOffset: offset, as: UInt16.self)
        }.littleEndian
    }

    private static func readI16(_ data: Data, _ offset: inout Int) throws -> Int16 {
        guard offset + 2 <= data.count else {
            throw ZPEInkError.invalidPayload("unexpected end of payload (i16)")
        }
        defer { offset += 2 }
        return data.withUnsafeBytes { pointer in
            pointer.loadUnaligned(fromByteOffset: offset, as: Int16.self)
        }.littleEndian
    }

    private static func readU32(_ data: Data, _ offset: inout Int) throws -> UInt32 {
        guard offset + 4 <= data.count else {
            throw ZPEInkError.invalidPayload("unexpected end of payload (u32)")
        }
        defer { offset += 4 }
        return data.withUnsafeBytes { pointer in
            pointer.loadUnaligned(fromByteOffset: offset, as: UInt32.self)
        }.littleEndian
    }

    private static func readI32(_ data: Data, _ offset: inout Int) throws -> Int32 {
        guard offset + 4 <= data.count else {
            throw ZPEInkError.invalidPayload("unexpected end of payload (i32)")
        }
        defer { offset += 4 }
        return data.withUnsafeBytes { pointer in
            pointer.loadUnaligned(fromByteOffset: offset, as: Int32.self)
        }.littleEndian
    }

    private static func crc32(_ data: Data) -> UInt32 {
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
}

private extension ZPEInkStroke {
    var canonicalJSON: String {
        """
        {"azimuth":\(azimuth.jsonArray),"pressure":\(pressure.jsonArray),"tilt":\(tilt.jsonArray),"x":\(x.jsonArray),"y":\(y.jsonArray)}
        """
    }
}

private extension Array where Element == Int32 {
    var jsonArray: String {
        "[\(map(String.init).joined(separator: ","))]"
    }
}

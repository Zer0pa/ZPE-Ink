import Foundation

public enum ZPEInkError: Error {
    case invalidHeader
}

public struct ZPEInk {
    public static let version = "0.1.0"

    public static func parseHeader(_ bytes: Data) throws -> (version: UInt8, mode: UInt8, flags: UInt8, strokeCount: UInt16) {
        guard bytes.count >= 22 else { throw ZPEInkError.invalidHeader }
        guard String(data: bytes.subdata(in: 0..<5), encoding: .ascii) == "ZPINK" else {
            throw ZPEInkError.invalidHeader
        }
        let count = bytes.withUnsafeBytes { raw -> UInt16 in
            raw.load(fromByteOffset: 8, as: UInt16.self)
        }.littleEndian
        return (bytes[5], bytes[6], bytes[7], count)
    }
}

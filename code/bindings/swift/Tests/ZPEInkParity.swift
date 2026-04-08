import Foundation

@main
struct ZPEInkParity {
    static func main() throws {
        let arguments = CommandLine.arguments
        guard arguments.count == 3 else {
            fputs("usage: swift ZPEInkParity.swift <input.zpink> <expected.json>\n", stderr)
            Foundation.exit(2)
        }

        let inputURL = URL(fileURLWithPath: arguments[1])
        let expectedURL = URL(fileURLWithPath: arguments[2])
        let payload = try Data(contentsOf: inputURL)
        let expected = try String(contentsOf: expectedURL, encoding: .utf8)
        let actual = try ZPEInk.decodeToCanonicalJSON(payload)

        guard actual == expected else {
            fputs("swift parity mismatch\n", stderr)
            Foundation.exit(1)
        }

        print(actual, terminator: "")
    }
}

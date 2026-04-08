import Foundation
#if canImport(PencilKit)
import PencilKit
#endif

struct DemoStroke: Codable {
    let x: [Int]
    let y: [Int]
    let pressure: [Int]
    let tilt: [Int]
    let azimuth: [Int]
}

struct DemoCapture: Codable {
    let mode: String
    let seed: Int
    let strokes: [DemoStroke]
}

enum DemoError: Error, CustomStringConvertible {
    case invalid(String)

    var description: String {
        switch self {
        case .invalid(let message):
            return message
        }
    }
}

@main
struct SwiftPencilKitDemo {
    static func main() throws {
        let repoRoot = URL(fileURLWithPath: #filePath)
            .deletingLastPathComponent()
            .deletingLastPathComponent()
        let runDir = FileManager.default.temporaryDirectory
            .appendingPathComponent("zpe-ink-swift-pencilkit-\(UUID().uuidString)", isDirectory: true)
        try FileManager.default.createDirectory(at: runDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: runDir) }

        let capture = buildDemoCapture()
        let capturePath = runDir.appendingPathComponent("capture.json")
        let encodedPath = runDir.appendingPathComponent("capture.zpink")
        let expectedPath = runDir.appendingPathComponent("expected.json")
        let encoderPath = runDir.appendingPathComponent("encode_demo_capture.py")

        try writeJSON(capture, to: capturePath)
        try writePythonEncoder(to: encoderPath)
        try runPythonEncoder(
            pythonScript: encoderPath,
            repoRoot: repoRoot,
            capturePath: capturePath,
            encodedPath: encodedPath,
            expectedPath: expectedPath
        )

        let encoded = try Data(contentsOf: encodedPath)
        let header = try ZPEInk.parseHeader(encoded)
        let actualJSON = try ZPEInk.decodeToCanonicalJSON(encoded)
        let expectedJSON = try String(contentsOf: expectedPath, encoding: .utf8)
            .trimmingCharacters(in: .whitespacesAndNewlines)

        guard actualJSON == expectedJSON else {
            throw DemoError.invalid("Swift binding did not match the Python canonical JSON")
        }

        let summary: [String: Any] = [
            "capture_note": captureNoteString(),
            "encoded_bytes": encoded.count,
            "mode": capture.mode,
            "seed": capture.seed,
            "status": "PASS",
            "stroke_count": Int(header.strokeCount),
        ]
        let summaryData = try JSONSerialization.data(withJSONObject: summary, options: [.sortedKeys])
        guard let summaryText = String(data: summaryData, encoding: .utf8) else {
            throw DemoError.invalid("summary JSON encoding failed")
        }
        print(summaryText)
    }

    private static func captureNoteString() -> String {
        #if canImport(PencilKit)
        return "PencilKit import available; demo uses deterministic PencilKit-style capture points."
        #else
        return "PencilKit unavailable here; demo uses deterministic PencilKit-style capture points."
        #endif
    }

    private static func buildDemoCapture() -> DemoCapture {
        DemoCapture(
            mode: "lossless",
            seed: 20260408,
            strokes: [
                DemoStroke(
                    x: [10, 14, 18, 22],
                    y: [20, 21, 23, 26],
                    pressure: [512, 520, 528, 536],
                    tilt: [0, 0, 1, 1],
                    azimuth: [100, 101, 101, 102]
                ),
                DemoStroke(
                    x: [30, 31, 33],
                    y: [40, 42, 45],
                    pressure: [600, 596, 592],
                    tilt: [2, 2, 3],
                    azimuth: [200, 201, 202]
                ),
            ]
        )
    }

    private static func writeJSON<T: Encodable>(_ value: T, to url: URL) throws {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.sortedKeys]
        let data = try encoder.encode(value)
        try data.write(to: url, options: [.atomic])
    }

    private static func writePythonEncoder(to url: URL) throws {
        let pythonSource = #"""
import json
import pathlib
import sys

repo_root = pathlib.Path(sys.argv[1])
capture_path = pathlib.Path(sys.argv[2])
encoded_path = pathlib.Path(sys.argv[3])
expected_path = pathlib.Path(sys.argv[4])

sys.path.insert(0, str(repo_root / "code"))

from zpe_ink.codec import canonical_json, decode_zpink, encode_zpink

capture = json.loads(capture_path.read_text(encoding="utf-8"))
payload = encode_zpink(capture["strokes"], mode=capture["mode"], seed=capture["seed"])
encoded_path.write_bytes(payload)
expected_path.write_text(canonical_json(decode_zpink(payload)), encoding="utf-8")
"""#
        try pythonSource.write(to: url, atomically: true, encoding: .utf8)
    }

    private static func runPythonEncoder(
        pythonScript: URL,
        repoRoot: URL,
        capturePath: URL,
        encodedPath: URL,
        expectedPath: URL
    ) throws {
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        process.arguments = [
            "python3",
            pythonScript.path,
            repoRoot.path,
            capturePath.path,
            encodedPath.path,
            expectedPath.path,
        ]
        process.environment = [
            "PYTHONPATH": repoRoot.appendingPathComponent("code").path,
            "PATH": ProcessInfo.processInfo.environment["PATH"] ?? "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        ]

        let stderr = Pipe()
        process.standardError = stderr
        try process.run()
        process.waitUntilExit()

        guard process.terminationStatus == 0 else {
            let data = stderr.fileHandleForReading.readDataToEndOfFile()
            let message = String(data: data, encoding: .utf8) ?? "python encoder failed"
            throw DemoError.invalid(message.trimmingCharacters(in: .whitespacesAndNewlines))
        }
    }
}

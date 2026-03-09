import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const pkgPath = path.join(__dirname, "..", "bindings", "wasm", "pkg", "zpe_ink_wasm.js");

const mod = await import(pkgPath);
const inputPath = process.argv[2];
if (!inputPath) {
  console.error("usage: node scripts/wasm_decode_runner.mjs <file>");
  process.exit(2);
}

const payload = fs.readFileSync(inputPath);
const decoded = mod.decode_to_json(payload);
process.stdout.write(decoded);

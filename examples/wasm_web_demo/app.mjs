import init, { decode_to_json } from "./pkg/zpe_ink_wasm.js";

const DEMO_ZPINK_BASE64 = "WlBJTksBAAcCADgmNQFuAAAA1EYB2QQACgAAABQAAAACAAAACAMGAAAAAgEEAQYBAAICAAAAEAMAAAYAAAAAAQIBAAFkAAYAAAACAQABAgEDAB4AAAAoAAAABAAAAAIBBAEEAAAABAEGAVgCAgAAAAcCAgAEAAAAAAECAcgAAgAAAAIC";

const statusEl = document.querySelector("#status");
const outputEl = document.querySelector("#output");
const loadSampleButton = document.querySelector("#load-sample");
const fileInput = document.querySelector("#file-input");

function base64ToBytes(base64) {
  const raw = atob(base64);
  const bytes = new Uint8Array(raw.length);
  for (let index = 0; index < raw.length; index += 1) {
    bytes[index] = raw.charCodeAt(index);
  }
  return bytes;
}

function renderJson(label, jsonText, byteLength) {
  const parsed = JSON.parse(jsonText);
  statusEl.textContent = `${label} decoded ${byteLength} bytes via the repo wasm binding.`;
  outputEl.textContent = JSON.stringify(parsed, null, 2);
}

async function decodeBytes(bytes, label) {
  try {
    const jsonText = decode_to_json(bytes);
    renderJson(label, jsonText, bytes.length);
  } catch (error) {
    statusEl.textContent = `${label} failed to decode.`;
    outputEl.textContent = String(error);
  }
}

async function loadEmbeddedSample() {
  await decodeBytes(base64ToBytes(DEMO_ZPINK_BASE64), "Embedded synthetic sample");
}

await init();
statusEl.textContent = "Repo wasm binding loaded. Synthetic sample ready.";
await loadEmbeddedSample();

loadSampleButton.addEventListener("click", () => {
  void loadEmbeddedSample();
});

fileInput.addEventListener("change", async () => {
  const file = fileInput.files && fileInput.files[0];
  if (!file) {
    return;
  }
  await decodeBytes(new Uint8Array(await file.arrayBuffer()), `Uploaded file ${file.name}`);
});

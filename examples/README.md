# Examples

Runnable demos only. Proxy mode is labeled where synthetic data stands in for gated corpora.

## Swift pencilkit demo

Run from the repo root:

```bash
swiftc code/bindings/swift/ZPEInk.swift examples/swift_pencilkit.swift -o /tmp/zpe-ink-swift-demo
/tmp/zpe-ink-swift-demo
```

The script uses a deterministic PencilKit-style capture on this Mac, asks the repo Python package to encode `.zpink`, then decodes and verifies the payload through the repo Swift binding.

## IAM-style loader

```bash
python3 examples/python_load_iam.py --proxy-demo
python3 examples/python_load_iam.py --input /path/to/sample.inkml
```

Proxy mode uses generated IAM-shaped strokes. Real-path mode reads InkML or UNIPEN-like input and round-trips it through the repo codec.

## WASM web demo

```bash
cd examples/wasm_web_demo
bash build.sh
PORT=8123 bash serve.sh
```

Open `http://127.0.0.1:8123`. The page decodes a synthetic `.zpink` sample with the repo wasm binding and also accepts file uploads.

## Benchmarks

`../BENCHMARKS.md` holds the scaffold. Real public-dataset rows land in Phase 3.

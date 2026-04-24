<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

ZPE-Ink architecture and authority map for the staged `.zpink` codec surface.

<p>
  <img src="../.github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

ZPE-Ink is a deterministic stroke-stream codec built around the `.zpink` packet envelope. The installable release unit is the Python package under `code/`.

Pipeline narrative: capture stroke data → encode to `.zpink` → decode for playback → verify against proof surfaces.

<p>
  <img src="../.github/assets/readme/section-bars/public-api-contract.svg" alt="PUBLIC API CONTRACT" width="100%">
</p>

The canonical packet contract is defined here:

- `docs/family/ZPINK_INTERFACE_CONTRACT.md`
- `docs/family/ZPINK_COMPATIBILITY_VECTOR.json`

<p>
  <img src="../.github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>

Status legend: `INSTALLABLE` means packaged and verified via wheel install; `SOURCE-VERIFIED` means source checks passed but it is not a pip-installed runtime surface. Python-native Rust is not promoted here as a packaged native runtime.

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Runtime surface</th>
      <th align="left">Status</th>
      <th align="left">Evidence</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Python package (`code/zpe_ink`)</td><td><code>INSTALLABLE</code></td><td><code>proofs/logs/20260321_technical_alignment_wheel_install.txt</code></td></tr>
    <tr><td>PyO3 binding (`code/bindings/python_native`)</td><td><code>SOURCE-VERIFIED</code></td><td><code>proofs/logs/20260321_technical_alignment_cargo_python_native.txt</code></td></tr>
    <tr><td>WASM binding (`code/bindings/wasm`)</td><td><code>SOURCE-VERIFIED</code></td><td><code>proofs/logs/20260321_technical_alignment_cargo_wasm.txt</code></td></tr>
    <tr><td>Swift binding (`code/bindings/swift`)</td><td><code>CONTRACT-CHECKED</code></td><td><code>proofs/logs/20260321_technical_alignment_binding_contracts.json</code></td></tr>
    <tr><td>C# binding (`code/bindings/csharp`)</td><td><code>CONTRACT-CHECKED</code></td><td><code>proofs/logs/20260321_technical_alignment_binding_contracts.json</code></td></tr>
  </tbody>
</table>

<p>
  <img src="../.github/assets/readme/section-bars/proof-corpus.svg" alt="PROOF CORPUS" width="100%">
</p>

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Authority surface</th>
      <th align="left">Role</th>
      <th align="left">Current verdict</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>proofs/release_validation/README.md</code></td><td>Release validation boundary</td><td><code>INCONCLUSIVE</code></td></tr>
    <tr><td><code>proofs/artifacts/public_benchmarks/dataset_matrix.json</code></td><td>Public benchmark matrix</td><td><code>bounded-public</code></td></tr>
    <tr><td><code>proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json</code></td><td>UJI public benchmark and gated-corpus boundary</td><td><code>UJI PASS</code>, <code>IAM/CASIA blocked</code></td></tr>
    <tr><td><code>proofs/logs/20260321_technical_alignment_cross_runtime.json</code></td><td>Cross-runtime parity evidence</td><td><code>PASS</code></td></tr>
    <tr><td><code>proofs/logs/20260321_technical_alignment_binding_contracts.json</code></td><td>Swift/C# binding contract evidence</td><td><code>PASS</code></td></tr>
  </tbody>
</table>

<p>
  <img src="../.github/assets/readme/section-bars/out-of-scope.svg" alt="OUT OF SCOPE" width="100%">
</p>

What is not covered: production-grade packaging for Swift/C#/WASM, runtime parity beyond contract checks, and public-release certification.

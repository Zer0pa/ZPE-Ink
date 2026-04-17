<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

ZPE-Ink architecture and authority map for the live-beta `.zpink` codec surface.

<p>
  <img src="../.github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

ZPE-Ink is a deterministic stroke-stream codec built around the `.zpink` packet envelope. The installable release unit is the Python package under `code/`.

Core transport narrative: capture stroke data -> encode to `.zpink` -> decode for playback -> verify against proof surfaces.
Tokenizer narrative: map stroke motion into 8-direction primitives with retained side channels when the tokenizer lane is under evaluation.

<p>
  <img src="../.github/assets/readme/section-bars/public-api-contract.svg" alt="PUBLIC API CONTRACT" width="100%">
</p>

The canonical packet and tokenizer contracts are defined here:

- `docs/family/ZPINK_INTERFACE_CONTRACT.md`
- `docs/family/ZPINK_COMPATIBILITY_VECTOR.json`
- `code/zpe_ink/codec.py`
- `code/zpe_ink/primitivetoken.py`

<p>
  <img src="../.github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>

Status legend: `INSTALLABLE` means packaged and verified via wheel install; `SOURCE-VERIFIED` means source checks passed but it is not a pip-installed runtime surface; `CONTRACT-CHECKED` means header and version invariants were verified against the compatibility vector.

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
    <tr><td><code>proofs/reruns/phase5_wedge/final_go_no_go_surface.json</code></td><td>Sovereign commercial verdict</td><td><code>NO-GO</code></td></tr>
    <tr><td><code>proofs/reruns/benchmark_freeze_local/claim_scope_map.json</code></td><td>Claim boundary and allowed statements</td><td><code>structured-tier-only</code></td></tr>
    <tr><td><code>proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json</code></td><td>Contradiction and release surface</td><td><code>OPEN</code> / <code>FAIL</code></td></tr>
    <tr><td><code>proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json</code></td><td>Bounded public handwriting row</td><td><code>UJI 1.6111x exact</code></td></tr>
    <tr><td><code>proofs/reruns/phase3_external/blind_clone_verdict.json</code></td><td>Untouched-host install and test surface</td><td><code>INCONCLUSIVE</code></td></tr>
  </tbody>
</table>

<p>
  <img src="../.github/assets/readme/section-bars/out-of-scope.svg" alt="OUT OF SCOPE" width="100%">
</p>

What is not covered: hard-corpus superiority, cross-script closure, or a public release upgrade. The tokenizer lane is real, but the current sovereign authority still sits on the bounded transport surface rather than a promoted tokenizer product claim.

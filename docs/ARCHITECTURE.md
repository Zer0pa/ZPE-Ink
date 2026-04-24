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

Status legend: `INSTALLABLE` means packaged and verified via wheel install; `SOURCE-VERIFIED` means source checks passed on the current local rerun; `CANDIDATE-ONLY` means bounded follow-on work that cannot replace `.zpink`.

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Runtime surface</th>
      <th align="left">Status</th>
      <th align="left">Evidence</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Python package (`code/zpe_ink`)</td><td><code>INSTALLABLE</code></td><td><code>proofs/reruns/follow_on_reassessment_2026-04-24/local_cpu_rerun_manifest.json</code></td></tr>
    <tr><td>PyO3 binding (`code/bindings/python_native`)</td><td><code>SOURCE-VERIFIED</code></td><td><code>proofs/reruns/follow_on_reassessment_2026-04-24/local_cpu_rerun_manifest.json</code></td></tr>
    <tr><td>WASM binding (`code/bindings/wasm`)</td><td><code>SOURCE-VERIFIED</code></td><td><code>proofs/reruns/follow_on_reassessment_2026-04-24/local_cpu_rerun_manifest.json</code></td></tr>
    <tr><td>Swift binding (`code/bindings/swift`)</td><td><code>SOURCE-VERIFIED</code></td><td><code>proofs/reruns/follow_on_reassessment_2026-04-24/local_cpu_rerun_manifest.json</code></td></tr>
    <tr><td>C# binding (`code/bindings/csharp`)</td><td><code>SOURCE-VERIFIED</code></td><td><code>proofs/reruns/follow_on_reassessment_2026-04-24/local_cpu_rerun_manifest.json</code></td></tr>
    <tr><td>Hybrid token sidecar (`code/zpe_ink/token_sidecar.py`)</td><td><code>CANDIDATE-ONLY</code></td><td><code>proofs/reruns/follow_on_reassessment_2026-04-24/token_sidecar_candidate_verdict.json</code></td></tr>
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
    <tr><td><code>proofs/reruns/phase5_wedge/final_go_no_go_surface.json</code></td><td>Historical sovereign closeout</td><td><code>NO-GO</code></td></tr>
    <tr><td><code>proofs/reruns/follow_on_reassessment_2026-04-24/interoperability_candidate_verdict.json</code></td><td>Current bounded follow-on decision</td><td><code>NO-GO remains</code>, <code>OPEN_BOUNDED_CANDIDATE</code></td></tr>
    <tr><td><code>proofs/reruns/follow_on_reassessment_2026-04-24/local_cpu_rerun_manifest.json</code></td><td>Current local CPU rerun</td><td><code>PASS</code></td></tr>
    <tr><td><code>proofs/reruns/follow_on_reassessment_2026-04-24/token_sidecar_candidate_verdict.json</code></td><td>Candidate token sidecar boundary</td><td><code>CANDIDATE_ONLY</code></td></tr>
  </tbody>
</table>

<p>
  <img src="../.github/assets/readme/section-bars/out-of-scope.svg" alt="OUT OF SCOPE" width="100%">
</p>

What is not covered: public-release certification, a current commercial wedge, blind-clone closure, or promotion of the token sidecar beyond its bounded directional/proxy fit surface.

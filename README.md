<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

# ZPE-Ink

Deterministic digital-ink codec centered on the `.zpink` packet format. This repo is a private staging snapshot with a current proof subset and rerun surface. It is not release-ready.

Status in plain language:

- What this is: a staged `.zpink` codec with a Python install surface and repo-local bindings.
- Proven: structured-tier compression exceeds 5x vs raw float32 and cross-runtime parity logs pass locally.
- Blocked: sovereign release surface is `FAIL` and blind-clone verification is `INCONCLUSIVE`.

Sovereign release surface: `proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json`.

Prereqs for local verification: Python 3.11+, Rust toolchain, and `wasm32-unknown-unknown` target for binding checks.

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

## What This Is

ZPE-Ink is the staged codec surface for .zpink stream encoding and decoding.

The installable release unit is the Python package under code/.

The Rust/WASM/Swift/C# bindings are repo-local source surfaces and are not part of the pip install unit.

## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| COMPRESSION | 5.59× | vs brotli 6.83× |
| BINDINGS | 5 languages | — |
| ROUND_TRIP | lossless | — |
| RELEASE_GATE | FAIL | not yet shipped |

## What We Prove

- Dual-layer encoding: exact delta values plus 8-code compass direction tokens
- Cross-runtime decode parity verified across Python, Rust, WASM, Swift, and C#
- Gestural search queries ink strokes by directional motif on compressed data
- Header contracts (magic, version, header size) enforced across all 5 bindings

## What We Don't Claim

- No claim of release readiness (release surface FAIL)
- No claim of blind-clone closure (INCONCLUSIVE)
- No claim of hard-corpus pass
- No claim of general digital-ink dominance

<p>
  <img src=".github/assets/readme/section-bars/quickstart-and-authority-point.svg" alt="QUICKSTART AND AUTHORITY POINT" width="100%">
</p>

<table width="100%" cellpadding="0" cellspacing="0">
  <tr>
    <td width="56%" valign="top">
      <pre><code class="language-bash">python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './code[dev]'
python -m pytest code/tests -q
python -m zpe_ink demo
python -m zpe_ink verify-roundtrip</code></pre>
      <p>Authoritative artifact: <code>proofs/reruns/benchmark_freeze_local/claim_scope_map.json</code></p>
    </td>
    <td width="44%" valign="top">
      <table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
        <thead>
          <tr>
            <th align="left">Key coordinates</th>
            <th align="left">Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Repository URL</td>
            <td><code>https://github.com/Zer0pa/ZPE-Ink</code></td>
          </tr>
          <tr>
            <td>Contact</td>
            <td><code>architects@zer0pa.ai</code></td>
          </tr>
          <tr>
            <td>Current verdict</td>
            <td><code>INCONCLUSIVE</code> (release surface <code>FAIL</code>)</td>
          </tr>
          <tr>
            <td>Claim family</td>
            <td><code>structured-tier-only</code> (&gt;5x vs raw float32)</td>
          </tr>
        </tbody>
      </table>
    </td>
  </tr>
</table>

How to read this table: it reports the latest measured ratios and boundaries; it does not imply release readiness.

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Authority snapshot</th>
      <th align="left">Value</th>
      <th align="left">Evidence</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Structured tier ratio</td><td><code>5.590209480060199x</code></td><td><code>proofs/reruns/benchmark_freeze_local/baseline_results.json</code></td></tr>
    <tr><td>Structured tier best comparator</td><td><code>brotli 6.825565026256283x</code></td><td><code>proofs/reruns/benchmark_freeze_local/baseline_results.json</code></td></tr>
    <tr><td>Hard corpus ratios</td><td><code>MathWriting 1.0944x</code>, <code>CROHME 1.3015x</code></td><td><code>proofs/reruns/benchmark_freeze_local/baseline_results.json</code></td></tr>
    <tr><td>Release surface</td><td><code>FAIL</code> (handoff <code>NO-GO</code>)</td><td><code>proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json</code></td></tr>
    <tr><td>Blind clone</td><td><code>INCONCLUSIVE</code> (npm probe failure)</td><td><code>proofs/reruns/phase3_external/blind_clone_verdict.json</code></td></tr>
    <tr><td>Non-Latin corpus</td><td><code>Calliar 2.7746x</code></td><td><code>proofs/reruns/phase3_external/calliar_benchmark.json</code></td></tr>
  </tbody>
</table>

How to read this table: these are the current authority anchors; any conflict keeps the repo `INCONCLUSIVE`.

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Proof anchor</th>
      <th align="left">Purpose</th>
      <th align="left">Current truth</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json</code></td><td>Sovereign release surface</td><td><code>release_surface_verdict=FAIL</code></td></tr>
    <tr><td><code>proofs/reruns/benchmark_freeze_local/claim_scope_map.json</code></td><td>Claim boundary</td><td><code>structured-tier-only</code></td></tr>
    <tr><td><code>proofs/reruns/benchmark_freeze_local/baseline_results.json</code></td><td>Structured-tier ratios</td><td><code>appendix_all_pass=false</code></td></tr>
    <tr><td><code>proofs/logs/20260321_technical_alignment_cross_runtime.json</code></td><td>Cross-runtime parity log</td><td><code>status=pass</code></td></tr>
    <tr><td><code>proofs/logs/20260321_technical_alignment_binding_contracts.json</code></td><td>Binding contract check</td><td><code>status=PASS</code></td></tr>
    <tr><td><code>proofs/reruns/phase3_external/blind_clone_verdict.json</code></td><td>Blind-clone gate</td><td><code>verdict=INCONCLUSIVE</code></td></tr>
  </tbody>
</table>

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | INCONCLUSIVE |
| Commit SHA | 98B5ED7 |
| Confidence | 67% |
| Source | proofs/INK_WAVE1_RELEASE_READINESS_REPORT.md |

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3-2.gif" alt="ZPE-Ink Masthead Option 3.2" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/lane-status-snapshot.svg" alt="LANE STATUS SNAPSHOT" width="100%">
</p>

## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| V_01 | STRUCTURED-TIER_COMPRESSION_BOUN... | PASS |
| V_02 | PYTHON/RUST/WASM_PARITY | PASS |
| V_03 | SWIFT/C#_HEADER_CONTRACTS | PASS |
| V_04 | PYTEST_REGRESSION_SURFACE | PASS |
| V_05 | SOVEREIGN_RELEASE_SURFACE | FAIL |
| V_06 | BLIND-CLONE_CLOSURE | INC |

<p>
  <img src=".github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Area</th>
      <th align="left">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>code/</code></td><td>Installable Python package, tests, bindings, scripts</td></tr>
    <tr><td><code>docs/</code></td><td>Architecture, contracts, support, legal boundaries, doc registry</td></tr>
    <tr><td><code>proofs/</code></td><td>Reruns, logs, runbooks, current proof anchors</td></tr>
    <tr><td><code>executable/</code></td><td>Local smoke and verification entry points</td></tr>
  </tbody>
</table>

<p>
  <img src=".github/assets/readme/zpe-masthead-option-3-3.gif" alt="ZPE-Ink Masthead Option 3.3" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/open-risks-non-blocking.svg" alt="OPEN RISKS (NON-BLOCKING)" width="100%">
</p>

Release blockers:

- Sovereign release surface remains <code>FAIL</code> / <code>INCONCLUSIVE</code> while the handoff manifest remains <code>NO-GO</code>.
- UNIPEN access remains unresolved; IAM remains registration-gated; cross-script authority is still restricted to Calliar-only evidence.
- Blind clone is still <code>INCONCLUSIVE</code> until the gate-a resource probe rerun is recorded on the updated code.

Constraints and technical debt:

- Primitive-token branch is candidate-only; Calliar bounded fidelity fails with large Hausdorff error.
- Telemetry reruns are incomplete in this shell without <code>COMET_API_KEY</code> and <code>RUNPOD_API_KEY</code>.

<p>
  <img src=".github/assets/readme/section-bars/contributing-security-support.svg" alt="CONTRIBUTING, SECURITY, SUPPORT" width="100%">
</p>

<table width="100%" border="1" bordercolor="#b8c0ca" cellpadding="0" cellspacing="0">
  <thead>
    <tr>
      <th align="left">Route</th>
      <th align="left">Target</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Documentation index</td><td><code>docs/README.md</code></td></tr>
    <tr><td>Auditor path</td><td><code>AUDITOR_PLAYBOOK.md</code></td></tr>
    <tr><td>Governance rules</td><td><code>GOVERNANCE.md</code></td></tr>
    <tr><td>Release gate rules</td><td><code>RELEASING.md</code></td></tr>
    <tr><td>Contribution workflow</td><td><code>CONTRIBUTING.md</code></td></tr>
    <tr><td>Security policy</td><td><code>SECURITY.md</code></td></tr>
    <tr><td>Support routing</td><td><code>docs/SUPPORT.md</code></td></tr>
  </tbody>
</table>

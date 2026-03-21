<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

# Auditor Playbook

Shortest honest local verification path for the private staging snapshot.

<p>
  <img src=".github/assets/readme/section-bars/setup-and-verification.svg" alt="SETUP AND VERIFICATION" width="100%">
</p>

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./code
python -m pytest code/tests -q
python -m zpe_ink demo
python -m zpe_ink verify-roundtrip
python code/scripts/verify_binding_contracts.py --repo-root .
python executable/verify_cross_runtime.py
python -m build --wheel --sdist ./code --outdir dist
```

What this verifies:

- local install surface and tests
- binding contract checks
- cross-runtime parity log exists and is readable

What this does not verify:

- rebuilding Swift/C#/WASM runtime artifacts
- public release readiness

Notes:

- `verify_cross_runtime.py` summarizes the latest local parity log and binding-contract checks; it does not rebuild all native runtimes.
- The installable release unit is the Python package under `code/`.

Expected outputs:

- `proofs/logs/20260321_technical_alignment_pytest.txt`
- `proofs/logs/20260321_technical_alignment_wheel_install.txt`

<p>
  <img src=".github/assets/readme/section-bars/proof-corpus.svg" alt="PROOF CORPUS" width="100%">
</p>

Inspect these files together:

- `proofs/INK_WAVE1_RELEASE_READINESS_REPORT.md`
- `proofs/reruns/benchmark_freeze_local/claim_scope_map.json`
- `proofs/reruns/contradiction_resolution_local/contradiction_resolution_manifest.json`
- `proofs/logs/20260321_technical_alignment_binding_contracts.json`
- `proofs/logs/20260321_technical_alignment_cross_runtime.json`
- `proofs/reruns/phase3_external/external_boundary_manifest.json`

If those surfaces disagree, the repo state remains `INCONCLUSIVE`.

<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

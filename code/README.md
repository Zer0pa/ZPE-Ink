<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

# Code Surface

This directory is the installable package boundary for ZPE-Ink.

Prereqs: Python 3.11+ for the package, Rust toolchain for binding checks.

- `zpe_ink/`: Python package
- `tests/`: lightweight regression surface
- `bindings/`: source-verified bindings for WASM, Python-native, Swift, and C#
- `scripts/`: gate and handoff scripts imported from the original workspace

Install locally with:

```bash
python -m pip install -e './code[dev]'
python -m zpe_ink demo
python -m zpe_ink verify-roundtrip
```

Binding contract verification:

```bash
python code/scripts/verify_binding_contracts.py --repo-root .
```

Current technical truth:

- the installable release unit is the Python package under `code/`
- the Rust/WASM/Swift/C# bindings are repo-local source surfaces, not pip-installed artifacts
- binding drift is checked against `docs/family/ZPINK_COMPATIBILITY_VECTOR.json`

Source-verified means the source tree passed contract or build checks, not that a packaged runtime was shipped.

<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

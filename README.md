# ZPE-Ink

ZPE-Ink is an always-in-beta `.zpink` digital-ink codec surface. This README only states claims that are backed by committed proof artifacts and CI tests in this repository.

License: see `LICENSE`.

## What This Is

ZPE-Ink provides Python encode/decode commands for deterministic `.zpink` stroke packets. The tested claim surface is intentionally narrow:

- lossless encode/decode roundtrip for generated stroke fixtures
- CRC and truncated-payload rejection
- optional pressure, tilt, and azimuth channel handling
- static binding-contract consistency across the Python, PyO3, WASM, Swift, and C# surfaces

The committed public benchmark files remain in `proofs/`, but this README does not restate their compression-ratio claims because CI does not rerun those external corpora.

## Encoding Contract

| Claim | Proof artifact | CI test |
|---|---|---|
| `.zpink` lossless roundtrip is bit-exact for generated fixtures | `proofs/logs/20260321_technical_alignment_pytest.txt` | `code/tests/test_codec_roundtrip.py::test_lossless_roundtrip_bit_exact` |
| Corrupted or truncated payloads are rejected | `proofs/logs/20260321_technical_alignment_pytest.txt` | `code/tests/test_codec_roundtrip.py::test_crc_tamper_detection`, `code/tests/test_codec_roundtrip.py::test_reject_truncated_payload` |
| zero-valued optional channels can be omitted without changing decoded strokes | `proofs/logs/20260321_technical_alignment_pytest.txt` | `code/tests/test_codec_roundtrip.py::test_zero_optional_channels_are_omitted_by_default` |
| binding headers and package version are contract-consistent | `proofs/logs/20260321_technical_alignment_binding_contracts.json` | `code/tests/test_binding_contracts.py::test_repo_binding_contracts_pass` |
| CLI demo and roundtrip entry points execute | `proofs/logs/20260321_technical_alignment_wheel_install.txt` | `code/tests/test_cli.py` |

## Commercial Readiness

No commercial-readiness or release-readiness claim is made from this README. Release validation remains bounded by `proofs/release_validation/README.md`.

## What We Do Not Claim

- No claim of release readiness
- No claim of blind-clone closure
- No claim of hard-corpus pass
- No claim of general digital-ink dominance
- No claim that retained public-benchmark artifacts close release readiness or hard-corpus authority
- No claim that local binding-contract checks prove full runtime parity for every downstream environment

## Quick Start

Development install:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './code[dev]'
python -m pytest code/tests -q
python -m zpe_ink demo
python -m zpe_ink verify-roundtrip
```

Package build:

```bash
python -m build
```

## Repository Links

| Field | Value |
|---|---|
| Repository | `https://github.com/Zer0pa/ZPE-Ink` |
| Issues | `https://github.com/Zer0pa/ZPE-Ink/issues` |
| Contact | `architects@zer0pa.ai` |

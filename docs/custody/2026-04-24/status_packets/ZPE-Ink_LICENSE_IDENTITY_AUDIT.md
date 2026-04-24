# ZPE-Ink — License & Identity Audit

**Date:** 2026-04-22
**Verdict:** NEEDS-WORK
**Auditor:** Sonnet sub-agent

## Summary

ZPE-Ink carries the wrong license version throughout: the repo `LICENSE` file is SAL v6.2, not v7.0, and both `pyproject.toml` files (root and `code/`) declare `LicenseRef-Zer0pa-SAL-6.2`. This is a CRITICAL drift from the canonical SAL v7.0 reference. The Commercial Readiness card is structurally sound and uses a valid Verdict enum value. The Compass-8 claim is well-supported by the Freeman 8-chain implementation with nibble packing in `primitivetoken.py`. Contact is consistent. Legal entity is correctly stated in LICENSE but drifts to `Zer0pa Labs` in `pyproject.toml` `authors` fields. No badge URL was found (no license shield in README). Two ethos near-misses are present in README and LEGAL_BOUNDARIES.md ("private staging snapshot", "not release-ready", "private staging surface") — none are exact banned strings but one warrants a MINOR flag.

## Findings by severity

### CRITICAL

- **LICENSE version wrong (C1):** `LICENSE` first line reads `Zer0pa Source-Available License v6.2` — not v7.0. `diff` against canonical confirms the file is entirely v6.2 text and is not byte-identical to the v7.0 canonical. The canonical first line is `# Zer0pa Source-Available License v7.0`; the repo first line is `Zer0pa Source-Available License v6.2`.

### MAJOR

- **SPDX version wrong in pyproject.toml (C2):** Root `pyproject.toml` line 12 and `code/pyproject.toml` line 12 both declare `license = "LicenseRef-Zer0pa-SAL-6.2"`. Must be `LicenseRef-Zer0pa-SAL-7.0`.
- **Legal entity drift in pyproject.toml (C5):** `authors = [{name = "Zer0pa Labs"}]` in both `pyproject.toml` files. The required legal entity is `Zer0pa (Pty) Ltd`. LICENSE itself is correct; the author field is inconsistent. `code/zpe_ink.egg-info/PKG-INFO` propagates the same incorrect `Author: Zer0pa Labs`.
- **No CITATION.cff present (C2):** No `CITATION.cff` found in the repo root. This is a SPDX metadata gap where the audit spec requires SPDX checking against that file.

### MINOR

- **Near-miss ethos language (C8):** README line 7: `"This repo is a private staging snapshot with a current proof subset and rerun surface. It is not release-ready."` — the phrase `not release-ready` is not an exact banned string but borders on negative-frame posture. `LEGAL_BOUNDARIES.md` line 11: `"This repo is a private staging surface, not a public commercial claim packet."` — similarly a minor posture concern. Neither matches the exact banned-string list; flagged for human review.
- **CHANGELOG carries no SPDX reference (C2):** CHANGELOG references no license version. Spec required a check; file is absent of any SPDX string.
- **LEGAL_BOUNDARIES.md carries no SPDX string (C2):** The file contains no `LicenseRef-Zer0pa-SAL-*` identifier. Spec requires checking this file.
- **No WHITEPAPER file present (C2):** Spec required SPDX check against WHITEPAPER; no such file exists in the repo.

## Criterion scorecard

| # | Criterion | Verdict | Note |
|---|---|---|---|
| 1 | License file correctness | FAIL | LICENSE is v6.2 text, not v7.0; first line mismatch; diff confirms not byte-identical to canonical |
| 2 | SPDX and metadata consistency | FAIL | Both pyproject.toml files declare SAL-6.2; no CITATION.cff; CHANGELOG and LEGAL_BOUNDARIES carry no SPDX string; WHITEPAPER absent |
| 3 | License badge URL integrity | N-A | No license badge found in README; no badge URL to audit |
| 4 | Contact consistency | PASS | `architects@zer0pa.ai` present in README line 148; only one contact address found across all scanned files |
| 5 | Legal entity consistency | PARTIAL | `Zer0pa (Pty) Ltd, Republic of South Africa` correct in LICENSE; `pyproject.toml` authors field uses `Zer0pa Labs` — entity name drift |
| 6 | Commercial Readiness shape + Verdict enum | PASS | Exactly 4 fields in order (Verdict, Commit SHA, Confidence, Source); Verdict = `INCONCLUSIVE` ∈ valid enum |
| 7 | Compass-8 claim accuracy | PASS | `primitivetoken.py` lines 14–33 define the 8-direction Freeman chain (DIRECTION_NAMES, DIRECTION_VECTORS); lines 190–205 implement nibble packing (`pack_tokens`); `encode_stroke_to_tokens` at lines 148–154 uses `_angle_to_dir` mapping to 8 directions; claim confirmed |
| 8 | Ethos posture | PASS | No exact banned strings found; near-miss language flagged as MINOR above |

## Confidence: 93%

# ZPE-Ink — Reorientation Assessment

**Date:** 2026-04-17
**Assessor:** Sonnet sub-agent
**Verdict:** NEEDS WORK

## Summary

The Codex pass on ZPE-Ink was broadly competent: all three deliverables exist, the branch is present, scope touched nine distinct files across README, docs, and proof-artifact prose, and all seven UNIVERSAL_BRIEF criteria are represented in the FIX_LOG. Ethos compliance is clean — no forbidden portfolio-wide language, no negative-hedge violations. The Compass-8 claim is correctly scoped to the tokenizer lane only, consistent with the ground truth. One structural defect requires a fix before the website pipeline will render correctly: the canonical `## Commercial Readiness` heading was renamed to `## Current Authority`, which breaks the website generator's exact-string heading match. The Verdict value inside that section (`NO-GO`) is also outside the allowed set. Beyond that, the Key Metrics table carries no determinism-flavored row despite determinism being Ink's correct wedge per the ground-truth map — a mild logic-triangle gap. Confidence is moderate because the PR open/merged status could not be verified from the filesystem alone.

## Findings by check

| # | Check | Verdict | Notes |
|---|---|---|---|
| 1 | Completion | PASS | All 3 deliverables present; branch `reorientation/2026-04-17` exists; FIX_LOG covers all 7 criteria |
| 2 | Scope completeness | PASS | 9+ files touched: README, ARCHITECTURE, LEGAL_BOUNDARIES, market_surface.json, code/README, proofs prose, family release note |
| 3 | Logic triangle | PARTIAL | "What This Is" correctly leads with cross-runtime parity (matches ground truth); Key Metrics has 0 determinism-flavored rows — all 4 are compression ratios or "none proven" |
| 4 | Website pipeline | FAIL | `## Commercial Readiness` heading absent; replaced by `## Current Authority` (README.md:77); Verdict value `NO-GO` not in allowed set {STAGED, PASS, PARTIAL, BLOCKED, FAIL, INCONCLUSIVE} |
| 5 | Deliverable coherence | PASS | Compass-8 YES correct for Ink lane; all 7 FIX_LOG criteria present; spot-checked citations resolve (`primitivetoken.py:15`, `codec.py:8`, `codec.py:160`, `codec.py:181`) |
| 6 | Hypothesis B cross-ref | PASS | No HypB migration language; Compass-8 scoped to tokenizer lane only, not amplified; NOT VIABLE verdict respected |
| 7 | Ethos compliance | PASS | No matches for "unified 8-primitive platform", "not yet ready", "pre-alpha", "NOT_PUBLIC_READY" across all .md files |
| 8 | Open questions | REAL | 2 questions: both genuine license-agent novelty-boundary calls (tokenizer lane vs. Freeman prior art; optional-channel suppression as novelty vs. optimization); neither is a punt |

**FAIL count: 1 hard (Check 4). Check 3 is a soft flag requiring judgment, not a blocking fail.**

## Finalization brief

- [ ] `README.md:77` — rename `## Current Authority` to `## Commercial Readiness` (exact heading required by website generator)
- [ ] `README.md:80` — change `Verdict | NO-GO` to a value in the allowed set; `PARTIAL` or `STAGED` is most defensible given the partial proof surface; confirm with user
- [ ] `README.md:28-35` — add a determinism-flavored Key Metrics row (e.g. `RUNTIME_PARITY | 3/3 | Py/Rust/WASM byte-identical`) to reflect the actual wedge; replace or reframe `CURRENT_WEDGE | none proven` which is honest but leaves the metrics table disconnected from the stated value proposition

## Input to license agent

Ink's Compass-8 claim is lane-genuine and correctly scoped to the tokenizer path at `code/zpe_ink/primitivetoken.py:15-34` — cite that range in the novelty schedule. The primary commercial novelty lives in the `.zpink` deterministic packet contract (`code/zpe_ink/codec.py:181`) and the automatic zero-channel suppression logic (`code/zpe_ink/codec.py:160`); both have code citations in the NOVELTY_CARD and are ready for schedule drafting. The two open questions in OPEN_QUESTIONS.md are genuine boundary calls requiring legal judgment: (1) whether Freeman-derived direction tokenization is protectable only at the integrated side-channel layer, and (2) whether zero-channel suppression is per-product novelty or transport optimization. No red flags on fabricated claims or OUT_OF_FAMILY rescues.

## Confidence: 82% — all key artifacts were read and cross-checked; residual uncertainty is PR open/merged status (not verifiable from filesystem) and the Check 3 soft flag (judgment call on whether 0 determinism metrics is a meaningful gap given the "none proven" explicit statement).

# ZPE-Ink Reality Reconciliation

The April 5 closeout remains historically correct: Phase 05 ended with `NO-GO` and no current wedge proven. What changed on April 24 is narrower and technical.

The live repo now supports a fresh local CPU rerun that passes `pytest code/tests -q`, cross-runtime parity for Python/WASM/Swift/C#, binding-contract verification, package build, and wheel install smoke. The prior Swift timeout was not a compiler blocker; it was a pipe-capture test harness defect in `test_cross_runtime_parity.py`.

That rerun does not create a current commercial wedge. It does justify one bounded follow-on lane: deterministic multi-runtime interoperability, with a candidate-only token sidecar kept subordinate to sovereign `.zpink`. The commercial verdict therefore stays `NO-GO`, while the follow-on lane becomes `OPEN_BOUNDED_CANDIDATE`.

The truth-surface contradictions were real and are now classified:

- README `INCONCLUSIVE` was stale against the sovereign `NO-GO` closeout and is corrected.
- README SAL v7.0 badge was stale against SAL 6.2 legal/package metadata and is corrected.
- `docs/market_surface.json` overstated a present wedge and is narrowed to no current wedge plus one bounded candidate lane.
- `docs/ARCHITECTURE.md` understated Swift/C# runtime proof and is updated to the current rerun surface.

Nothing in this reconciliation promotes enterprise readiness, blind-clone closure, or hard-corpus authority.

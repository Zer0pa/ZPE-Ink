<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

Frequently asked questions for the ZPE-Ink private staging surface.

<p>
  <img src="../.github/assets/readme/section-bars/evidence-and-claims.svg" alt="EVIDENCE AND CLAIMS" width="100%">
</p>

## Is this repo release-ready?

No. The current sovereign verdict is `INCONCLUSIVE` and the release surface remains `FAIL`.

## Why is it inconclusive?

The quality scorecard reports `pass=true`, while the handoff manifest reports `go_no_go=NO-GO`. Those two surfaces coexist and are not averaged into a pass.

## What claims are allowed right now?

Only the structured-tier claim family in `proofs/reruns/benchmark_freeze_local/claim_scope_map.json`, which states that the transport kernel remains above 5x vs raw float32 on the structured tier and that transport quality/runtime parity are locally credible and separate from hard-corpus authority.

## Does ZPE-Ink beat Brotli?

Not on the frozen structured-tier overall ratio. Brotli’s structured-tier ratio (`6.8256x`) exceeds ZPE-Ink (`5.5902x`). Candidate branches may exceed Brotli but are not promoted while fidelity losses remain.

<p>
  <img src="../.github/assets/readme/section-bars/proof-corpus.svg" alt="PROOF CORPUS" width="100%">
</p>

## What actually works now?

The Python package installs, tests pass, curated Wave-1 proof anchors are preserved, and binding contract checks pass locally.

## Is blind-clone verification complete?

No. The latest blind-clone verdict is `INCONCLUSIVE` because an optional resource probe failed. A rerun is required to update this status.

<p>
  <img src="../.github/assets/readme/section-bars/interface-contracts.svg" alt="INTERFACE CONTRACTS" width="100%">
</p>

## Where is the format contract?

`docs/family/ZPINK_INTERFACE_CONTRACT.md`

## Where is the compatibility vector?

`docs/family/ZPINK_COMPATIBILITY_VECTOR.json`

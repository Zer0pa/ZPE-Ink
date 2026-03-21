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

The Python package installs, tests pass, current proof anchors are present, and binding contract checks pass locally. Evidence: `proofs/logs/20260321_technical_alignment_wheel_install.txt`, `proofs/logs/20260321_technical_alignment_pytest.txt`, and `proofs/logs/20260321_technical_alignment_binding_contracts.json`.

## Is blind-clone verification complete?

No. The latest blind-clone verdict is `INCONCLUSIVE` because an optional resource probe failed. A rerun is required to update this status.

<p>
  <img src="../.github/assets/readme/section-bars/interface-contracts.svg" alt="INTERFACE CONTRACTS" width="100%">
</p>

## Where is the format contract?

`docs/family/ZPINK_INTERFACE_CONTRACT.md`

## Where is the compatibility vector?

`docs/family/ZPINK_COMPATIBILITY_VECTOR.json`

## What does structured-tier-only mean in plain language?

It means the only allowed performance claim is: on the structured-tier dataset, the codec beats raw float32 by more than 5x. It does not imply superiority on general handwriting corpora or against Brotli.

## What is the difference between INCONCLUSIVE and FAIL here?

`FAIL` means a specific gate is negative (for example, the sovereign release surface). `INCONCLUSIVE` means the overall repo truth remains unresolved because required gates are not all positive.

## What is blind-clone verification?

It is a clean clone and install run in a fresh environment to validate the external install surface. The latest verdict is recorded in `proofs/reruns/phase3_external/blind_clone_verdict.json`.

<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE-Ink Masthead" width="100%">
</p>

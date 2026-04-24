# Plan 01 Summary

Status: complete

## External Boundary Truth

- Red Magic is not currently available in-lane:
  - `adb devices -l` returned no attached devices.
- RunPod is available, but only over the exposed TCP boundary:
  - `ssh root@38.80.152.72 -p 30709 -i ~/.ssh/id_ed25519` passes.
  - `ssh wijfmmgnjovmuu-64411cb1@ssh.runpod.io -i ~/.ssh/id_ed25519` fails with `Permission denied (publickey)`.
- Direct corpus-access truth is asymmetric:
  - IAM landing page returns `HTTP 200`.
  - UNIPEN currently fails at DNS resolution.

## Non-Latin Online-Stroke Result

- The Calliar Arabic online-stroke corpus was executed through the RunPod lane:
  - artifact: `/Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink/proofs/reruns/phase3_external/calliar_benchmark.json`
  - samples: `2500`
  - strokes: `31971`
  - points: `1904422`
  - compression ratio: `2.774608127006351x`
  - max Hausdorff: `0.0`
  - median encode latency per stroke: `0.0545215625 ms`

## Claim Consequence

- Phase 03 now has a real non-Latin online-stroke surface.
- That surface is materially stronger than the weakest prior hard-corpus results, but it is still far below the sovereign `5x` structured-tier authority threshold.
- Direct UNIPEN closure remains unresolved and must stay explicit.

## Next Valid Step

Execute blind-clone verification on the RunPod host and reduce that host-level evidence to one coherent verdict.

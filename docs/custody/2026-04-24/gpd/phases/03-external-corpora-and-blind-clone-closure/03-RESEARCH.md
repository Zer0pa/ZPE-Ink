# Phase 03 Research

Date: 2026-03-21
Phase: `03-external-corpora-and-blind-clone-closure`

## Question

What is the strongest honest external lane for Phase 03 now that the local contradiction surface is frozen: real non-Latin online-stroke evidence, blind-clone verification, or renewed direct IAM/UNIPEN acquisition?

## Live Boundary Facts

- The local Mac lane is no longer the governing bottleneck:
  - `/System/Volumes/Data` has roughly `38 GiB` free.
  - `adb devices -l` currently returns no attached devices, so Red Magic is not live in-lane.
- RunPod is reachable, but only through the exposed TCP path:
  - `ssh root@38.80.152.72 -p 30709 -i ~/.ssh/id_ed25519` succeeds.
  - `ssh wijfmmgnjovmuu-64411cb1@ssh.runpod.io -i ~/.ssh/id_ed25519` fails with `Permission denied (publickey)`.
- The GitHub repo is blind-cloneable only with authenticated HTTPS from the current machine's GitHub session. Anonymous HTTPS and the available SSH key do not have repo access.
- Direct corpus-access truth is mixed:
  - `https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database` returns `HTTP 200`.
  - `https://unipen.nici.ru.nl` currently fails at DNS resolution.
- The strongest real non-Latin online-stroke surface available immediately is not device capture; it is the public Calliar corpus:
  - `https://github.com/ARBML/Calliar`
  - The archive contains `calliar_dataset/dataset.zip` with `2500` Arabic online-stroke JSON samples.

## Phase-Research Conclusions

- Phase 03 should not wait for Red Magic. The device boundary is currently absent, while RunPod and Calliar are both real.
- Blind-clone verification is best executed on RunPod over the direct TCP lane against the private GitHub remote using the existing authenticated GitHub session from the local machine.
- Calliar is a legitimate non-Latin online-stroke closure surface for this phase:
  - it is real online trajectory data,
  - it is cross-script relative to the Latin-leaning prior corpora,
  - it can be benchmarked without inventing a new parser family.
- Direct IAM/UNIPEN acquisition does not close symmetrically:
  - IAM is reachable as a landing surface,
  - UNIPEN remains a real external-access blocker and should stay explicit.

## What Phase 03 Must Produce

- A structured external-boundary artifact that records:
  - the actual RunPod access lane,
  - current disk state,
  - current ADB truth,
  - IAM and UNIPEN access status.
- A real broader-corpus artifact from a non-Latin online-stroke corpus.
- A blind-clone verdict from an untouched external host that distinguishes:
  - clone/access success,
  - core Python/package truth,
  - any remaining full-gate or toolchain limits.

## What Phase 03 Must Not Pretend

- It must not narrate Calliar `2.77x` into broad `5x` hard-corpus authority.
- It must not narrate a private authenticated clone into public-release closure.
- It must not claim direct UNIPEN closure when DNS resolution still fails.

## Carry-Forward Implication

- Phase 03 can complete honestly even if the sovereign release verdict remains `FAIL` / `NO-GO`.
- If blind clone and broader corpus both execute cleanly, the next valid work moves to Phase 04 candidate branches, not to public-readiness language.

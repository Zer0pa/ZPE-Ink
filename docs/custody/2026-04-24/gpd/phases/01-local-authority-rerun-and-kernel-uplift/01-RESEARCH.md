# Phase 01 Research

Date: 2026-03-20
Phase: `01-local-authority-rerun-and-kernel-uplift`

## Question

What can be executed end-to-end on the available MacBook M1 Air, with free downloadable resources only, without converting external blockers into fake closure?

## Local Envelope

- Host free space at execution time: about `12 GiB` available on `/System/Volumes/Data`.
- Required local toolchain already present: `python`, `pytest`, `node`, `wasm-pack`, `swiftc`, `cargo`, `rustc`, `maturin`, `mono`, `mcs`.
- Executed proof bundle size for the completed local rerun: about `179 MiB` at `ZPE-Ink/proofs/reruns/phase1_m1_local/`.
- Temporary Docker images pulled for blocker attempts were cleaned back down to the pre-existing `opencfd/openfoam-dev:2312` image only.

## Decisive Repo Truth Before Execution

- The frozen sovereign metric `AM-INK-01` was already locally satisfiable on the structured/proxy pack:
  - overall compression ratio `5.5902x`
  - exact roundtrip `PASS`
  - parity had evidence in curated artifacts but not yet on this machine
- The existing parity failure on this machine was not a codec disagreement. It was a harness-path bug: `gate_e_cross_runtime.py` resolved `bindings/` and `scripts/` relative to the wrong working directory.
- The existing NET-NEW lane depended on architecture-sensitive raster/HuggingFace fallbacks. That was a poor Phase 1 dependency surface for an M1/local-only execution requirement.

## Current Comparator Landscape

Official surfaces that matter to the lane:

- Wacom Universal Ink Model / WILL:
  - [Universal Ink Model overview](https://developer-docs.wacom.com/docs/overview/specifications/universal-ink-model/)
  - Relevant constraint: serious incumbent/reference stack with explicit serialized ink model, not a rhetorical comparator.
- W3C InkML:
  - [W3C Ink page](https://www.w3.org/2002/mmi/ink)
  - Relevant constraint: real interchange surface for online ink traces and a legitimate same-corpus ingest target.
- Microsoft Ink / ISF:
  - [Windows Ink overview](https://learn.microsoft.com/en-us/windows/apps/design/input/ink)
  - Relevant constraint: named incumbent challenger remains real, but same-corpus closure was not achievable in this local-only phase.
- Apple PencilKit:
  - [PencilKit documentation](https://developer.apple.com/documentation/pencilkit)
  - Relevant constraint: device-level validation remains later-phase because this machine lacks the full iOS device-lab path.

## Phase 01 Research Conclusions

- The strongest honest local move was not to widen claims. It was to make the local authority harness genuinely runnable on the M1 and to add a real, free, online-stroke public corpus that does not depend on architecture-specific packages.
- The best lightweight real public corpora for this phase were:
  - MathWriting excerpt (InkML)
  - CROHME ICFHR package (InkML)
  - UJI Pen Characters (UNIPEN-like online strokes)
- Direct IAM and UNIPEN closure remained external:
  - IAM landing page reachable, but no direct free online-stroke download was closed in-lane
  - UNIPEN host remained unresolved after repeated local and containerized attempts
- A non-Latin online-stroke corpus still remains open. Phase 01 does not fake that closure with raster extraction.

## Critical Gaps After Phase 01

- `M1_real_iam_unipen_non_inferior` still fails.
- `E-G3_cross_script_required` still fails because no real non-Latin online-stroke corpus was executed in the local-only lane.
- Device-level PencilKit validation remains `PAUSED_EXTERNAL`.
- Primitive-token or hybrid-runtime closure remains unstarted. The runtime truth is still deterministic exact-coordinate transport, not a proven primitive kernel.

## Phase 02 Boundary

The next valid phase should target only the remaining hard blockers:

- direct IAM and UNIPEN acquisition or access closure
- non-Latin online-stroke corpus closure
- device-lab or Apple tooling access if PencilKit adapter evidence is required
- same-corpus incumbent challenger work for ISF/UIM when actual artifacts are available

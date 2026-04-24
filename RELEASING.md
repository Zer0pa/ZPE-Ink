# Releasing

## Release Gate

ZPE-Ink remains `INCONCLUSIVE` until a committed release-validation artifact proves otherwise.

The current release-validation authority is `proofs/release_validation/README.md`, which states that no full release validation surface has been generated on this branch.

## Required Before Release

1. All README proof anchors resolve on `HEAD`.
2. The Commercial Readiness source resolves on `HEAD`.
3. Local tests pass from a clean clone.
4. Binding-contract verification passes.
5. Native runtime caveats are either resolved by proof or kept out of promoted runtime claims.
6. Packaging metadata, citation metadata, and provenance files are current.

## Package Publication

Publishing, trusted-publishing setup, package-index changes, and workflow edits are outside the lane-hygiene pass and must happen in a dedicated release pass.

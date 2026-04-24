# Governance

## Authority Order

The authority order for this repository is:

1. `LICENSE`
2. Committed proof artifacts under `proofs/`
3. Source code and tests under `code/`
4. `README.md`
5. Supporting docs under `docs/`

If these surfaces disagree, the contradiction must be treated as unresolved until a later evidence-backed pull request reconciles it.

## Claim Changes

Do not promote a stronger claim unless the proof artifact exists on the same branch and the README path resolves on `HEAD`.

Do not convert cleaner documentation, stronger parity, or a cleaner branch into release readiness unless the governing acceptance gate says so.

## Merge Authority

Agents may open pull requests. Repository owners merge. No agent should self-merge a governance, release, or proof-surface change.

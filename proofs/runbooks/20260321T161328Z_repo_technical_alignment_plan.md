# Repo Technical Alignment Plan

Timestamp: 2026-03-21T16:13:28Z
Repo: /Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink
Working Instruction Surface:
- /Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink/proofs/runbooks/REPO_TECHNICAL_ALIGNMENT_EXECUTION_PROMPT.md
- /Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink/proofs/runbooks/REPO_TECHNICAL_EXECUTION_SUPPLEMENT.md

## Classification Hypothesis

ZPE-Ink is a standalone codec repo with one truthful installable release unit today:
- Python distribution from `code/`

It also carries source-verified multi-runtime binding trees:
- Rust/PyO3 source
- Rust/WASM source
- Swift header/parser surface
- C# header/parser surface

Those bindings are repo-local verification surfaces, not packaged release units.

## Target Architecture

Align the repo to:
- Python package as the only installable distribution surface
- installed Python CLI smoke surface for demo and roundtrip verification
- repo-local static verification for binding-contract drift across Python/Rust/WASM/Swift/C#
- CI that verifies:
  - package tests
  - sdist/wheel build truth
  - installed CLI behavior
  - Rust source binding compile truth
  - binding-contract consistency

## Execution Steps

1. Add package-native CLI and remove install-path ambiguity between repo-root scripts and the package surface.
2. Add a binding-contract verification module/script/tests anchored to `docs/family/ZPINK_COMPATIBILITY_VECTOR.json`.
3. Update repo-root executable verification entry points to call shared package logic where appropriate.
4. Align `code/pyproject.toml` metadata and packaging controls with the chosen architecture.
5. Align CI and Makefile to the real release unit and real verification path.
6. Update only the minimum technical docs needed to make build/install/release truth explicit.
7. Falsify the result by building, testing, verifying imports, verifying installed CLI behavior, and verifying native-source checks.

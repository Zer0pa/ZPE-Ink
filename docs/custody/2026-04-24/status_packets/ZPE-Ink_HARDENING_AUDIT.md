# ZPE-Ink — Portfolio Hardening Audit

**Date:** 2026-04-24
**Auditor:** Codex lane agent for ZPE-Ink
**Repo HEAD audited:** `8cec1bcdcaef66e86f05d6e3d2cc2b99f85b8762`
**Overall verdict:** NEEDS_STRUCTURAL_WORK

---

## A. Seventeen-check results

| # | Check | Verdict | Cite |
|---|---|---|---|
| 1 | Cold-clone install | PASS_UV | `/tmp/zpe-audit-ink/uv_install.log`, `/tmp/zpe-audit-ink/readme_quickstart.log` |
| 2 | Dependency pinning + lockfile | LOOSE + Cargo.lock present; no uv/pylock | `pyproject.toml:1-18`, `code/bindings/*/Cargo.toml` |
| 3 | PyPI state | LIVE_CURRENT | `/tmp/zpe-audit-ink/pypi_zpe_ink.json` |
| 4 | Build prerequisites | MIXED | `README.md:137`, `.github/workflows/ink-ci.yml:51-57`, `code/tests/test_cross_runtime_parity.py:36-100` |
| 5 | Cross-file consistency | MAJOR_DRIFT | `README.md:54-110`, `code/pyproject.toml:11`, proof-anchor existence probe |
| 6 | PyPI publish pipeline | TOKEN_BASED | `.github/workflows/publish.yml:7-26`, `/tmp/zpe-audit-ink/pypi_simple_zpe_ink.json` |
| 7 | SLSA level | NO_PROVENANCE | `.github/workflows/publish.yml:18-24`; no `actions/attest` |
| 8 | Wheel matrix (Rust-backed) | N/A | Python wheel is setuptools pure-Python: `pyproject.toml:1-3`; Rust bindings are repo-local |
| 9 | Zenodo DOI | ABSENT | Zenodo API hits=0; no `.zenodo.json` |
| 10 | HF Hub presence | ORG_ONLY | `/tmp/zpe-audit-ink/hf_probes.log` returned 401 for model/dataset/space probes |
| 11 | Scientific metadata | PARTIAL | `CITATION.cff:1-15`; PyPI classifiers/project URLs empty |
| 12 | Reusable workflows | HAND_ROLLED_TAG_FLOATING | `.github/workflows/ink-ci.yml:20-57`, `.github/workflows/publish.yml:18-24` |
| 13 | Tooling stack | LEGACY | `pyproject.toml:1-3`; no `uv.lock`, `pylock.toml`, `.pre-commit-config.yaml` |
| 14 | CI health + security | GREEN_SHALLOW | `/tmp/zpe-audit-ink/gh_run_list_ink_ci.log`; `zizmor_missing`; branch protection lacks required signatures |
| 15 | Commit signing | GPG_SIGNED | `/tmp/zpe-audit-ink/git_signatures.log` |
| 16 | SBOM + receipt chain | ABSENT | no `anchore`, `syft`, `cosign`, `in-toto`, or SBOM workflow refs |
| 17 | Cross-runtime (Ink only) | PARTIAL_PARITY_4_OF_5 | README quickstart passed; Python-native Rust release build failed |

### A detail — per-check narrative

Cold clone at `/tmp/zpe-audit-ink/ZPE-Ink` installed with `uv pip install .` exit 0 in 8.635s and README source quickstart exit 0 with all `27` tests passing. `python -m build` also exited 0. The package is installable today.

Dependency posture is not frontier: `setuptools.build_meta` remains the build backend in `pyproject.toml:1-3`, Python dev dependencies are lower-bounded only, Cargo manifests use broad major-version ranges (`pyo3 = "0.22"`, `serde = "1"`), and no `uv.lock`/`pylock.toml` exists.

PyPI is live and version-current: API reports `zpe-ink` latest `0.1.0`, one release, uploads on `2026-04-14`. Metadata is weak: classifiers are empty, project URLs are `null`, license is `None`, and Simple API provenance is `None` for both wheel and sdist.

Prereqs are mixed. README documents Python, Rust, and `wasm32-unknown-unknown` at `README.md:137`, but cross-runtime tests require `swiftc`, `mcs`, `mono`, `wasm-pack`, and `node` at `code/tests/test_cross_runtime_parity.py:36-100`; those are hidden from the quickstart.

Cross-file consistency is materially drifted. `code/pyproject.toml:11` still says `Zer0pa Labs`; canonical root metadata says `Zer0pa (Pty) Ltd`. README proof anchors `README.md:103-106` cite three paths missing from the cold clone. README says Py/Rust/WASM parity while the test suite exercises Swift/C#/WASM parity.

Publishing is token-based despite OIDC permission: `publish.yml:7-9` grants `id-token`, but `publish.yml:24-26` uses `pypa/gh-action-pypi-publish@release/v1` with `secrets.PYPI_API_TOKEN`. No PEP 740 provenance URL is present in PyPI Simple JSON.

CI is green but shallow for the license parity claim. Last five `ink-ci` runs are green, but workflow coverage is Python tests plus Rust/WASM cargo checks; it does not run Swift/C# parity on CI. Actions use floating tags (`actions/checkout@v4`, `setup-python@v5`), not SHA pins.

Ink parity is strong at the Python package layer but incomplete for Rust-native release readiness. README quickstart passed, `wasm32-unknown-unknown` is installed, WASM cargo build/test/publish-dry-run passed, Swift and C# compile commands exited 0. Python-native Rust `cargo build --release` and `cargo publish --dry-run` failed with unresolved Python symbols on arm64.

---

## B. Gaps identified

1. Structural: PyPI release is not Trusted Publishing/PEP 740 attested (`publish.yml:24-26`, Simple API provenance `None`). Frontier readers expect attestations by default.
2. Structural: No SLSA/GitHub artifact attestation path; no reusable `Zer0pa/workflows` caller and no `actions/attest-build-provenance`.
3. Local: README cites missing proof anchors (`README.md:103-106`); cold clone lacks `phase5_wedge`, `benchmark_freeze_local`, and `contradiction_resolution_local`.
4. Local: Hidden runtime prerequisites for Ink (`swiftc`, Mono `mcs`/`mono`, `wasm-pack`, `node`) are required by tests but not fully documented in Quick Start.
5. Local: `code/pyproject.toml:11` uses `Zer0pa Labs`, conflicting with canonical `Zer0pa (Pty) Ltd`.
6. Structural: No Zenodo, public HF model/dataset/space card, SBOM, Sigstore, in-toto, `uv.lock`, `pylock.toml`, `ruff`, `zizmor`, or pre-commit surface.
7. Local: Python-native Rust binding does not release-build on the audited arm64 Mac; unresolved Python symbols block full five-runtime parity.

---

## C. Recommended fixes (for Orchestrator rollup — NOT executed here)

1. ⚑ HIGHEST LEVERAGE Switch release flow to org reusable workflow with Trusted Publishing, PEP 740, artifact attestations, SBOM, and SHA-pinned actions. Effort: M. Blast radius: affects `Zer0pa/workflows`, PyPI, portfolio-wide. Category: cross-category.
2. Restore or remove missing README proof anchors so every cited path exists in cold clone. Effort: S. Blast radius: self-contained. Category: proof chain.
3. Add explicit Ink toolchain prerequisites and CI coverage for Swift/C#/WASM parity. Effort: M. Blast radius: self-contained. Category: core install.
4. Fix Python-native Rust release build and dry-run packaging. Effort: M. Blast radius: self-contained. Category: lane-specific.
5. Add `uv.lock`/`pylock.toml`, ruff, zizmor, pre-commit, and move pure-Python build backend to hatchling if compatible. Effort: M. Blast radius: affects PyPI. Category: org-wide leverage.
6. Add Zenodo config, public HF lane assets/cards, `REPRODUCIBILITY.md`, and PyPI classifiers/project URLs. Effort: S. Blast radius: affects PyPI/HF Hub. Category: scientific credibility.

---

## D. Frontier-reader impression

A frontier 2026 reader sees a useful codec with unusually broad local runtime ambition and a passing cold install, but not a frontier supply-chain surface. The repo reads stronger than a toy: PyPI install works, tests pass, CI is green, and the Ink-specific parity test covers Swift/C#/WASM locally. But the outside surface still looks pre-hardening: no PEP 740 provenance, token-based publish workflow, no SBOM/attestation/reusable workflow, no lockfiles, floating GitHub Actions, weak PyPI metadata, missing README proof anchors in cold clone, and partial Rust-native release parity. The technical lane is real; the distribution/provenance posture is not yet peer-level with Astral/Hugging Face/Modal.

---

## E. Scope-discipline attestation

- [x] No edits made to any file in the audited `/tmp/zpe-audit-ink/ZPE-Ink` repo.
- [x] `git status` clean. `git diff` empty.
- [x] `git diff --stat main...HEAD` returns zero lines.
- [x] Used fresh venv at `/tmp/zpe-audit-ink/ZPE-Ink/.venv` — did not install into system Python.
- [x] No cross-repo reads beyond required playbook/ethos; ecosystem facts via public APIs / `gh api`.
- [x] Card is <=1,800 words.

---

## F. Before / after / delta (validation test)

**Before this audit:** We knew ZPE-Ink had local proof work and broad runtime claims, but not how it read from a fresh 2026 frontier install/publish/provenance perspective.

**After this audit:** We know the cold clone installs and tests cleanly, PyPI is live/current, CI is green, but provenance, reusable workflows, public HF/Zenodo/SBOM surfaces, proof-anchor cold-clone integrity, and Rust-native release parity are incomplete.

**Named delta:** The audit separates the real working codec surface from the missing frontier hardening surface, with exact blockers and citations for the fix round.

End of card.

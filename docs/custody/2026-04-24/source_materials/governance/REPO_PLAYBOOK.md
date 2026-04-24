# ZPE Repo Playbook

**Supersedes:** `ZER0PA_REPO_DOCS_PLAYBOOK_CANONICAL_2026-03-21.md` (portfolio-as-platform framing retired) and the narrower README-only draft of this file from 2026-04-17.
**Version:** 2026-04-19
**For:** Any agent starting a new ZPE repo, extending an existing workstream to a new product, or bringing an existing repo into canonical alignment.
**Read alongside:** `Zer0pa Live Project Ethos.md` (positioning) and `REPO_TECHNICAL_EXECUTION_SUPPLEMENT.md` (per-lane engineering guidance, when applicable).

---

## 0. What a ZPE repo is

A ZPE repo is **one encoding product** in a portfolio of independent encoding products. It is not a module of a unified platform. It is not a derivative of ZPE-IMC. It speaks for itself.

The portfolio is held together by a philosophy — **zero-point encoding**, finding minimal and fundamental representations in a specific domain — and by a single shared license (SAL v6.2). Everything else is per-product: the codec, the wedge, the metrics, the proof artifacts, the novelty claim.

**Public commercial posture: always-in-beta.** The repo ships when it is useful. We reserve the right to improve it suddenly. This is positive framing. Never "incomplete", "pre-alpha", "not yet ready", "private-stage", "NOT_PUBLIC_READY". If a product is not useful enough to ship, it is not in the portfolio.

---

## 1. When to use this playbook

| Situation | Use this playbook to |
|---|---|
| Starting a new ZPE product/repo from scratch | Construct the repo to canonical shape from day one |
| Extending a workstream to add a new product | Bootstrap the new repo so it fits the portfolio |
| Auditing an existing repo against canon | Identify drift; apply the reorientation fix pattern |
| Handing a repo to a new agent | Attach this alongside `Zer0pa Live Project Ethos.md` as the brief |

---

## 2. Minimum directory + document set

Every ZPE product repo has, at the root:

```
README.md                 # Front door — parser-sensitive 10-section spine (see §3)
LICENSE                   # SAL v6.2 canonical text
CITATION.cff              # Machine-readable citation
CHANGELOG.md              # Public delta log
CONTRIBUTING.md           # Contribution rules + CLA implication
SECURITY.md               # Vulnerability reporting
CODE_OF_CONDUCT.md        # Community standard
pyproject.toml            # Package metadata (see §7)
.gitignore
.github/
  workflows/
    ci.yml                # Test + lint on push/PR
    publish.yml           # Tag-triggered PyPI publish (OIDC trusted publishing)
  ISSUE_TEMPLATE/
    bug_report.md
    feature_request.md
    evidence_dispute.md
    question.md
  PULL_REQUEST_TEMPLATE.md
src/ or code/             # Codec source (see §7 for packaging shape)
tests/                    # Test suite
docs/
  README.md               # Docs index
  ARCHITECTURE.md         # Runtime map
  FAQ.md                  # Reader Q&A
  SUPPORT.md              # Support routing
  LEGAL_BOUNDARIES.md     # Compact license-adjacent notes
proofs/                   # Committed evidence artifacts (see §8)
  manifests/
  artifacts/
validation/               # Test corpora + generated result JSONs (if applicable)
```

**Add when the product needs them:**
- `AUDITOR_PLAYBOOK.md` — shortest honest outsider audit path
- `PUBLIC_AUDIT_LIMITS.md` — what public audit can and cannot establish
- `docs/BENCHMARKS.md` — when competitive benchmark evidence exists
- `ROADMAP.md` — only if there is genuinely sequenced downstream work; keep descriptive, not promissory
- `GOVERNANCE.md` — only if the product has external contributors

**Do NOT default to:**
- Wave-numbered artifact directories
- Ceremonial governance theatre that the product does not actually need
- Inherited ZPE-IMC metrics, statuses, proof claims, or acquisition links
- `docs/family/` unless there is a real runtime or contract coupling to another product

---

## 3. The canonical README spine (parser-sensitive — do not modify)

The website generator at `/Users/Zer0pa/Website/product-pages/generate_pages.py` reads `##` headings by exact string match. Every ZPE product README uses these ten headings, in this order, with this exact text:

| # | Heading | Website zone | Shape |
|---|---|---|---|
| 1 | `## What This Is` | Hero + prose | 2–3 sentences, buyer-first |
| 2 | `## Key Metrics` | Metric cards | 3-col table, **exactly 4 rows** |
| 3 | `## Competitive Benchmarks` (optional) | Competitive zone | 3+ col table; only if real evidence |
| 4 | `## What We Prove` | Bullet list | `-` prefixed bullets |
| 5 | `## What We Don't Claim` | Bullet list | `-` prefixed bullets |
| 6 | `## Commercial Readiness` | Verdict card | 2-col table (Field / Value) |
| 7 | `## Tests and Verification` | Table | 3-col (Code / Check / Verdict) |
| 8 | `## Proof Anchors` | Table | 2-col (Path / State) |
| 9 | `## Repo Shape` | Metadata | 2-col key-value |
| 10 | `## Quick Start` | Code block | ```bash ```|

Additional sections (e.g. `## Ecosystem`, `## Who This Is For`, `### Open Risks (Non-Blocking)`, `### Authority Notes`, `### Directory Map`) are permitted. They must appear **after** the ten canonical sections or nested as `###` subsections. Never rename, reorder, interleave, or skip.

### Parser-required KV row under `## What This Is`

Immediately after the prose paragraphs under `## What This Is`, include a 2-column KV table the generator reads for Zone 02 metadata:

```markdown
| Field | Value |
|-------|-------|
| Architecture | {DOMAIN}_STREAM          e.g. SENSOR_STREAM, SPIKE_STREAM, HAND_POSE_STREAM, MARKET_TICK_STREAM |
| Encoding     | {LANE}_{MECHANIC}_V1     e.g. NEURO_DELTA_V1, DT_CODEC, XR_QUANT_DELTA_V1, FT_NIBBLE_DELTA_V1 |
```

Both rows are required on every codec repo.

### Required field shapes per section

**§2 `## Key Metrics`** — exactly 4 rows, 3-col table (Metric / Value / Baseline), followed by a `> Source:` blockquote citing the proof artifact(s).

- **Metric:** uppercase-underscore label (`COMPRESSION`, `DT_PASS`, `E1_WINS`).
- **Value:** numeric + optional unit or ratio (`6.65×`, `10/11`, `94.4%`, `52.47 dB`).
- **Baseline:** single word ≤12 chars → renders as unit line / multi-word → renders as `vs …` context line / `—` → renders empty.

**§3 `## Competitive Benchmarks`** — only if real comparator evidence exists. ZPE row first and bolded. Include rows where ZPE loses. Cite source JSON.

**§4 `## What We Prove`** — `-` bullets of auditable guarantees, each traceable to a proof anchor.

**§5 `## What We Don't Claim`** — `-` bullets of explicit non-claims. No backdoored claims.

**§6 `## Commercial Readiness`** — 2-col table with **exactly these four fields**:

```markdown
| Field | Value |
|-------|-------|
| Verdict | {one of: STAGED, PASS, PARTIAL, BLOCKED, FAIL, INCONCLUSIVE} |
| Commit SHA | {12-char short SHA of the authority-bearing commit} |
| Confidence | {percentage from governing preflight / quality-gate artifact} |
| Source | {relative path to the governing proof artifact} |
```

**The Verdict value MUST come from the enumeration above.** Do not invent new tokens (`ACTIVE_BETA`, `USEFUL_NOW`, `NOT_RELEASE_READY`, `NO-GO`, `PRIVATE_ONLY` — all break the parser). The always-in-beta posture lives in the surrounding prose and in `## What This Is`, not in the Verdict enum.

**§7 `## Tests and Verification`** — 3-col, `V_NN` codes, verdicts from {PASS, FAIL, INC}.

**§8 `## Proof Anchors`** — 2-col Path / State. **Every path must exist — verify with `ls`.** State from {VERIFIED, PENDING, BLOCKED, MISSING}. If MISSING, remove the row.

**§9 `## Repo Shape`** — 2-col KV metadata. Common fields: Proof Anchors (count), Modality Lanes (count), Authority Source (path).

**§10 `## Quick Start`** — single `bash` triple-backtick block that actually works on a fresh clone.

---

## 4. Ethos alignment in prose

### Positive-frame language

| Retire | Use instead |
|---|---|
| "not yet ready" | "useful now, improving continuously" |
| "pre-alpha" / "private-stage" / "NOT_PUBLIC_READY" | plain description of current capability |
| "staging only" | nothing — if it's in the portfolio, it's in the portfolio |
| "release-grade X is still deferred" | "X is the current engineering focus" |
| "incomplete" | named open blocker with honest description |

### Portfolio-not-platform language

| Retire | Use instead |
|---|---|
| "Unified 8-primitive platform" | this product alone |
| "10 modalities, one pipeline" | this product's own modality/domain |
| "Protected Architecture across N primitives portfolio-wide" | novelty claims scoped to this product's codec, with code citations |
| "Derivative of ZPE-IMC" | independent encoding product |
| "Sovereign Research Gate" (portfolio-level) | remove; no portfolio-level gates |

### Compass-8 / 8-primitive scope discipline

The 8-primitive / Compass-8 architecture is a lane-specific pattern, not a portfolio claim. It applies to Bio, Geo, Ink, Mocap, IoT, IMC, and Cipher. It does **not** apply to FT, Neuro, Prosody, Robotics, Video, XR. If your codec uses Compass-8, cite the implementing code. If it does not, do not claim it — describe what your codec actually does.

### Honest limits

Where the product loses to a baseline, lacks a claimed capability, or has an open blocker — say so plainly in the relevant section. No burial in footnotes. No retroactive `OUT_OF_FAMILY` / "excluded from headline" rescues. The license and diligence pipeline both read these.

---

## 5. Commit, branch, and PR discipline

- Feature/campaign work goes on a named branch (`feature/{name}`, `campaign/{name}`, `reorientation/{date}`). Not main.
- One atomic commit per logical unit. Descriptive commit messages.
- Open a PR. Do not self-merge. Owner merges.
- Special lanes: Neuro requires `gh pr merge --admin`; Prosody requires `gh pr merge --squash --admin` (someone with rights, not the agent).
- Do not force-push. Do not amend commits that have been pushed and referenced elsewhere (e.g. stamped into a Commit SHA field).

---

## 6. Packaging (`pyproject.toml` + PyPI)

Required:

```toml
[project]
name = "zpe-{lane}"          # canonical: zpe-bio, zpe-ft, zpe-geo, etc.
version = "X.Y.Z"            # no 0.1.0.dev0 — real versions
license = "LicenseRef-Zer0pa-SAL-6.2"
requires-python = ">=3.11"   # or whatever the codec actually needs — do not inflate
```

- `pip install .` must work from the clone root. If `pyproject.toml` must live in a subdirectory for historical reasons, add a thin root wrapper that delegates.
- Add `.github/workflows/publish.yml` using OIDC trusted publishing (`pypa/gh-action-pypi-publish`). Tag-triggered (`tags: ["v*"]`). For maturin/Rust repos, use the `PyO3/maturin-action` variant.
- Import name convention: `zpe_{lane}` (may differ from pip name where needed — e.g. `zpe_finance` for `zpe-ft` is acceptable).
- **Do not** declare runtime dependency on `zpe-imc-kernel` or `zpe-multimodal` unless your product actually imports from them. The portfolio is a set of independent codecs.

---

## 7. Proof artifacts + validation tree

- `proofs/manifests/` — authority manifests (e.g. `CURRENT_AUTHORITY_PACKET.md`).
- `proofs/artifacts/` — timestamped evidence bundles with JSON/SHA anchors.
- `validation/results/` — test runs with result JSONs, SHAs, deterministic replay hashes.
- Every numeric value promoted in `## Key Metrics` must trace back to a file in one of these trees. The website's product-page renderer does not verify this — the diligence reader does.
- **Do not** commit fabricated artifacts, missing directory references, or paths that don't resolve. The most damaging red-team finding in the portfolio's history was a cited Proof Anchor whose directory never existed in git history.
- **Do not** remove adverse test results or failing benchmark rows to flatter the surface. SAL v6.2 §4.7 prohibits this.

---

## 8. Visual system (optional — inherit while bootstrapping)

Until a new product has its own visual identity, it may reuse the ZPE-IMC masthead/section-bar system verbatim:

- Shared masthead: `.github/assets/readme/zpe-masthead.gif` (copy from ZPE-IMC)
- Section bars: `.github/assets/readme/section-bars/*.svg`
- Nav buttons: `.github/assets/readme/nav/`
- Relative paths must match document depth (`.github/assets/readme/...` from root, `../.github/assets/readme/...` from `docs/`).

**If you do not include the visual system, the README still renders** — masthead/section-bars are decorative. Prioritize the parser-sensitive 10-section spine over decoration.

---

## 9. What NOT to do

1. **Don't rename, reorder, skip, or interleave the canonical 10 `##` headings.** Website pipeline depends on exact match.
2. **Don't invent Commercial Readiness Verdict tokens.** Use only the six-value enum.
3. **Don't claim portfolio-wide 8-primitive architecture, unified platform, or Protected Architecture across N primitives.** That framing is retired.
4. **Don't use "pre-alpha", "private-stage", "NOT_PUBLIC_READY", "not yet ready", "staging only", or similar negative hedges.** Always-in-beta is positive.
5. **Don't fabricate metrics, proof artifacts, or code citations.** Every promoted value traces to a real committed file.
6. **Don't add `zpe-imc-kernel` or `zpe-multimodal` as a runtime dependency** unless your product actually imports them.
7. **Don't edit IMC core files** (`zpe_multimodal/core/*`, the 20-bit word structure, the `total_words=844` authority point). Those are frozen.
8. **Don't self-merge a PR.** Owner merges.
9. **Don't commit files with hardcoded PII paths** (`/Users/prinivenpillay/`, `Priniven Pillay`). Use the aliases `/Users/zer0pa-build/` and `Zer0pa-Architect-Prime`.

---

## 10. Pre-publish checklist

Before the repo is considered aligned / shippable:

- [ ] All ten canonical `##` headings present, exact text, exact order.
- [ ] `## What This Is` contains prose + `| Architecture | ... |` + `| Encoding | ... |` KV rows.
- [ ] `## Key Metrics` is exactly 4 rows, 3-col, with a `> Source:` blockquote.
- [ ] Every value in Key Metrics traces to a committed proof artifact.
- [ ] `## Competitive Benchmarks` included only if real comparator evidence exists; losing rows present if applicable.
- [ ] `## Commercial Readiness` has all four required fields (Verdict / Commit SHA / Confidence / Source); Verdict is in the six-value enum.
- [ ] `## Proof Anchors` — every listed path resolves via `ls`.
- [ ] Every markdown link `[text](path)` in the README resolves.
- [ ] `## Quick Start` actually runs on a fresh clone.
- [ ] `pip install .` succeeds in a clean venv from the clone root.
- [ ] `.github/workflows/publish.yml` exists and targets the correct pip name.
- [ ] License field in `pyproject.toml` is `LicenseRef-Zer0pa-SAL-6.2`.
- [ ] No negative-hedge language anywhere.
- [ ] No portfolio-wide 8-primitive / unified-platform language anywhere.
- [ ] Compass-8 claim (if any) is scoped to this product with code citation.
- [ ] Honest limits are surfaced in prose, not buried in footnotes.
- [ ] No hardcoded PII paths in committed files.
- [ ] On a named branch, atomic commit, PR open, not self-merged.

---

## 11. Starting a new repo — order of operations

1. Create the repo directory with the structure in §2.
2. Stand up `pyproject.toml` with correct pip name, version, and license field.
3. Copy `LICENSE` from SAL v6.2 canonical text.
4. Write `README.md` to the 10-section spine in §3, filling each section with product-specific content. Use sibling repos (Neuro, IoT) as style references — not as content sources.
5. Populate minimum doc set (§2): `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`, `docs/README.md`, `docs/FAQ.md`, `docs/SUPPORT.md`, `docs/ARCHITECTURE.md`.
6. Stand up tests (`tests/`) and at least one working proof artifact (`proofs/` or `validation/results/`).
7. Inherit the visual system (§8) or skip and add later.
8. Add `.github/workflows/ci.yml` + `publish.yml`.
9. Run the pre-publish checklist (§10).
10. Open a PR. Do not self-merge.

---

## 12. Reference docs

| For | Read |
|---|---|
| The reoriented positioning | `/Users/Zer0pa/Status_Packets/2026-04-17_Orchestrator-Working-Docs/Zer0pa Live Project Ethos.md` |
| Per-lane engineering guidance | `/Users/Zer0pa/ZPE/Git Orchestreator/REPO_TECHNICAL_EXECUTION_SUPPLEMENT.md` |
| Website parser contract | `/Users/Zer0pa/Website/product-pages/WEBSITE_AGENT_PLAYBOOK.md` |
| Compass-8 scope ground truth | `/Users/Zer0pa/ZPE/COMPASS_8_GROUND_TRUTH_REPORT.md` |
| Per-product commercial wedge ground truth | `/Users/Zer0pa/ZPE/COMMERCIAL_WEDGE_GROUND_TRUTH.md` |
| SAL v6.2 license canonical text | `/Users/Zer0pa/ZPE/SAL_v6_Governance_Docs/Zer0pa SAL 6.2/Zer0pa_SAL_v6_2_FINAL_deterministic.txt` |
| Superseded prior playbook (do not use as-is) | `ZER0PA_REPO_DOCS_PLAYBOOK_CANONICAL_2026-03-21.md` (various repo `proofs/runbooks/` paths) |

---

*Playbook maintained by the Zer0pa Orchestrator. If the canonical spine, verdict enum, or ethos changes, update this doc first, then propagate to repos.*

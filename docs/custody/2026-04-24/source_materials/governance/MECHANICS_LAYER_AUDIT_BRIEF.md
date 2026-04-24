# Mechanics-Layer Audit Brief — Front-Door Granularity Across Public Repos

**Date:** 2026-04-22
**For:** The Zer0pa Portfolio Compliance Auditor (same agent that ran the 2026-04-22 License & Identity Audit — reuse the same Opus-orchestrator + parallel Sonnet sub-agents pattern).
**Deliver:** One pilot deep-audit on ZPE-Taste, then a transversal pass across the other 17 public repos, then a consolidated rollup with A/B/C/D per repo.
**Mode:** Read-only. Do not edit artifacts or READMEs. Report findings only.

---

## Mission

Add a **front-door mechanics layer** to every live public repo — but only if the underlying granularity is already grounded in repo authority artifacts (or can be after a clearly-scoped artifact write). The goal is that a technical outsider can read the front door and understand, in one pass:

- what object is actually being operated on
- what transform actually happens
- what survives the transform
- what does not, or is out of scope
- in what units the object exists

**Not a branding layer.** **Not speculative interpretation.** **Not poetic stand-ins.** **Not "near-positive" softening for negative repos.** If anything, this layer must make negatives **more precise**, not less uncomfortable.

---

## The non-negotiable discipline rules

1. **Artifact-first.** Only surface mechanics that are already grounded in repo authority artifacts (proof JSONs, verified code paths, LICENSE §7 schedules, NOVELTY_CARD, preflight reports).
2. **If the next layer down is missing, do NOT fabricate.** Flag it for artifact addition. The artifact goes into `proofs/` or equivalent first; only then is it promotable to README / front door.
3. **No invented nouns.** If the repo doesn't already name a unit, event type, frame, primitive, panel, bin, or token — don't invent one. Propose the noun and flag it for artifact-grounding before use.
4. **No poetic stand-ins.** Direct, technical naming only.
5. **Negative repos get sharper negatives.** The mechanics block must make the failure surface **more explicit**, not softer. "Evidenced negative" stays evidenced negative; "partial" stays partial with exact scope; "bounded positive" stays bounded with exact boundary.
6. **No repo gets front-door promotion** of its mechanics block until the underlying facts are present in proof / source artifacts, parser-safe, citation-safe, and claim-safe.

---

## The seven-field mechanics block (canonical spec)

Every in-scope repo gets an audit against these seven fields. When eventually promoted to the front door, the block will render with these headings.

| # | Field | Purpose | Discipline |
|---|---|---|---|
| 1 | **Object Basis** | What the thing is in repo units. The raw object the codec operates on. | Must name the actual operand, not a marketing description. |
| 2 | **Object Currency** | Public-safe units, event types, bins, panels, frames, tokens, primitives, sample rate, channel count, etc. The granularity the repo commits to. | Must be code-cited or artifact-cited. |
| 3 | **Transform** | Exact encode / packet / decode (or equivalent) operation, named specifically. | Must match what the code actually does — no abstraction above the real transform. |
| 4 | **Preserved Surface** | What remains true after the transform — bit-exact fields, fidelity thresholds, replay guarantees. | Must be backed by proof artifacts with measured values. |
| 5 | **Failure Surface** | What does not survive, or what is explicitly out of scope. For evidenced-negative repos, this is where the negative is made precise. | Measured failure values or named-gate failures cited. No softening. |
| 6 | **Authority Anchors** | Exact artifact paths + code file:lines backing the above fields. | Every path must resolve on current `origin/main`. |
| 7 | **State Label** | One of: `evidenced negative` / `research in progress` / `partial` / `bounded positive` / `bounded negative` / `reference surface` / `active product`. | Must match the repo's LICENSE §7 status and Commercial Readiness Verdict enum consistently. |

---

## Scope — 18 public repos

### Pilot specimen (do first, validate the format)

- **ZPE-Taste** — evidenced negative; narrow claim, explicit proof anchors, named architecture/encoding, quantified failure surfaces, clear state label. This repo defines the discipline for the rest.

### Transversal pass (17 more, parallel Sonnet sub-agents after pilot)

- **ZPE-Bio** (bounded positive, biosignal)
- **ZPE-FT** (bounded positive, financial time-series; one lane INCONCLUSIVE on retrieval)
- **ZPE-Geo** (bounded positive, geospatial)
- **ZPE-Ink** (bounded positive, digital ink; brotli-beats-on-ratio stated)
- **ZPE-IoT** (bounded positive, sensor telemetry; bounded-lossy with NRMSE envelopes)
- **ZPE-Mocap** (partial — retrieval yes, playback no at 82° joint RMSE)
- **ZPE-Neuro** (bounded positive on spike events; full-signal reconstruction not claimed)
- **ZPE-Prosody** (partial — encode passes, retrieval gate FAIL)
- **ZPE-Robotics** (bounded positive on smooth / fails on step; lossy FFT + zlib)
- **ZPE-XR** (bounded positive on transport; comparator gate 0/5 fail)
- **ZPE-Diagram** (bounded positive on structural line-diagram geometry; fills/dashed rejected)
- **ZPE-Image** (bounded positive on sparse-stroke primary + narrower secondary route)
- **ZPE-Mental** (reference — symbolic state-code encoding, not a real-signal codec)
- **ZPE-Music** (bounded positive on event representation; not audio compression)
- **ZPE-Smell** (research in progress; symbolic surrogate scope — not real chemosensor data)
- **ZPE-Touch** (reference — haptic event tuples + internal 8-direction stroke field)
- **DM3** — optional inclusion at auditor discretion. DM3 already carries an unusually rich canonical-reference surface (RETRACTIONS.md, CLAIMS.md, IS_AND_IS_NOT.md, ARTEFACT_BUNDLE_REGISTER.tsv) and may already satisfy this layer; a compact scan to confirm is sufficient.

### Out of scope

Private repos (ZPE-IMC, ZPE-Video, ZPE-Cipher), non-codec publics (ZeroShip, Zero-Class-Vessel-Hull-20098), internal research/ops repos.

---

## Inputs — read before starting

1. `/Users/Zer0pa/ZPE/Zer0pa Live Project Ethos.md` — the posture this layer reinforces.
2. `/Users/Zer0pa/ZPE/REPO_PLAYBOOK.md` — canonical 10-section README spine (the mechanics block will eventually live as an inset within the existing spine, not as a new top-level section).
3. This brief — the mechanics-block spec and discipline rules.
4. The target repo's current `origin/main` state: `README.md`, `LICENSE` (especially §7.N for that product), `docs/_reorientation/2026-04-17/NOVELTY_CARD.md`, `proofs/` tree, source code paths cited in §7.N and NOVELTY_CARD.
5. For the pilot specifically: any existing taste-scope artifact (e.g. `public_taste_surrogate_scope.json`, structural-test-failure records) to verify what's grounded vs what's ambient.

---

## The audit output per repo — A/B/C/D

For each repo produce a single markdown card with these four sections:

### A. What is already present and promotable now

Fill each of the seven mechanics-block fields using only content that is **currently citable to an artifact or code file:line on `origin/main`**. Mark each field with one of:

- `✓ promotable` — fully grounded, ready for front-door promotion
- `◐ partial` — some content exists, specific gaps named
- `✗ absent` — nothing in current artifacts addresses this field

Cite exact paths / line ranges for every `✓` claim. No citation = not promotable.

### B. What lower-granularity mechanics are missing from authority artifacts

Name the specific fields where the next layer down is **missing from proof / source artifacts**. For each:

- What specific fact would need to exist
- Why it's needed (what the front-door mechanics block cannot say truthfully without it)
- What kind of artifact would carry it (JSON summary, code comment with file:line anchor, proof-anchored measurement, etc.)

### C. Minimum artifact additions required before README / front-door promotion

Translate B into a concrete addition list:

- Exact artifact path to create (or augment)
- Content requirement — specific measurement, specific enumeration, specific code reference
- Sourcing — is this already computable from existing data (no new work), or does it require a re-run (flag it)
- Precedence — which additions are prerequisites for others

This section becomes the work list for the repo / Codex agents in a later pass. Do **not** execute the additions in this audit pass. Audit only.

### D. Proposed 3-label visual logic tied to repo truth

A compact visual summary — three short labels — drawn from actual truth in the repo, **not** generic marketing labels. The labels should distinguish this product from its siblings at a glance.

Examples (illustrative only; propose labels based on the specific repo's truth):

- **Taste:** `EVIDENCED NEGATIVE` / `NO GEOMETRY` / `SYMBOLIC-SCOPE`
- **Bio:** `GROUND-TRUTH REPLAY` / `DOMAIN-AWARE` / `NON-CLINICAL-REGULATED`
- **XR:** `SUB-MS TRANSPORT` / `LOSSY-DELTA` / `NO-RUNTIME-CLOSURE`
- **Robotics:** `SPECTRAL ARCHIVE` / `NOT-CONTROL-LOOP` / `RED-TEAM-ATTACK-7-OPEN`

Each label must trace to a specific fact in the repo. Propose three per repo. If the repo's truth doesn't yield three non-overlapping labels, say so.

---

## Pilot specification — ZPE-Taste

Run the pilot audit fully before dispatching parallel Sonnets for the other 17. Read Taste's `README.md`, `LICENSE §7.X` entry, `docs/_reorientation/2026-04-17/NOVELTY_CARD.md`, and every `proofs/` artifact you can locate.

The pilot output document is itself the quality bar: if the A/B/C/D card for Taste is clean, disciplined, and produces a mechanics block that the user can look at and immediately understand what Taste actually is (and what it is not), the format is validated and can be applied to the other 17.

If the pilot reveals a field spec ambiguity — e.g. "Object Currency" isn't the right name for what symbolic-tuple repos carry — escalate to the Orchestrator before running the transversal pass. Do not silently adapt the spec.

---

## Transversal pass — 17 parallel Sonnet sub-agents

Once the pilot is validated by the Orchestrator, fire 17 parallel Sonnet sub-agents (one per remaining public codec repo). Each applies the identical A/B/C/D framework to its assigned repo.

Sub-agent constraints:

- Read-only.
- Under 1,000 words per per-repo card.
- Cite exact paths for every claim.
- Honor the discipline rules in §1 of this brief.
- No cross-agent collaboration; siloed audits.
- Return with verdict: `READY FOR PROMOTION` / `ARTIFACTS NEEDED FIRST` / `BLOCKED`.

---

## Rollup (after all 18 cards land)

Produce `AUDIT_ROLLUP.md` in the same packet directory. Required sections:

1. **Promotion readiness distribution** — how many of the 18 are immediately front-door-promotable, how many need artifact additions first, how many are blocked.
2. **Cross-cutting patterns** — repeated missing-mechanics types, common artifact additions, field-spec ambiguities. If three or more repos need the same kind of artifact addition (e.g. "explicit Object Currency enumeration missing"), that's one pattern, named once.
3. **Ranked action list** — for the Orchestrator to route to Codex agents later. Grouped by artifact-addition type, named per repo.
4. **Residual risks** — anything the audit did not cover that warrants separate attention.

---

## Output locations

- **Pilot:** `/Users/Zer0pa/Status_Packets/2026-04-22_Mechanics-Layer-Audit/assessments/ZPE-Taste_PILOT.md`
- **Transversal per-repo:** `/Users/Zer0pa/Status_Packets/2026-04-22_Mechanics-Layer-Audit/assessments/{Repo}_MECHANICS_AUDIT.md`
- **Rollup:** `/Users/Zer0pa/Status_Packets/2026-04-22_Mechanics-Layer-Audit/AUDIT_ROLLUP.md`

---

## Completion report

When the rollup is written, return a one-paragraph completion summary naming:

- Pilot verdict (Taste)
- Promotion-readiness distribution across the 18 repos
- Top three cross-cutting patterns
- Total count of artifact additions needed
- Rollup file path

The Orchestrator will then decide:
- Whether to route artifact additions to Codex in a follow-up pass (scope-disciplined per repo), and
- When to commission the actual front-door promotion of the mechanics block (likely as an inset inside the existing `## What This Is` section, not as a new top-level heading — to preserve Website Agent parser contract).

---

## What NOT to do

- Do not edit any repo, README, LICENSE, NOVELTY_CARD, or artifact.
- Do not fabricate or propose nouns the repo does not already own.
- Do not soften failure surfaces on negative repos.
- Do not promote a mechanics block to front door in this pass. Audit only.
- Do not audit private repos, non-codec publics, or internal research/ops repos.
- Do not extend scope beyond the 18 named repos.

---

## Why this matters

The current front door tells the reader what the repo claims. The mechanics layer tells the reader what the repo actually operates on. Both layers in coherent contact with each other is the definition of a scientific product. One layer without the other is marketing on one side or a technical brick on the other.

This audit establishes the discipline; the artifact additions it identifies unblock the promotion; the final front-door inset is the visible payoff for a technical outsider opening any ZPE repo for the first time.

---

*Scope-disciplined transversal audit. Pilot first. Siloed sub-agents. Artifact-first promotion gate. Nothing executed. Nothing promoted. Report + ranked action list.*

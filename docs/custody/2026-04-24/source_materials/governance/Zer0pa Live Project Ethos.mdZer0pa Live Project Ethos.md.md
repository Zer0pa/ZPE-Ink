# Zer0pa Live Project Ethos

**Date:** 2026-04-17
**Audience:** Every agent working on any ZPE repo. Read this first.
**Purpose:** The overarching frame. What ZPE is, what it is not, how we talk about it.

---

## What ZPE is

ZPE is a portfolio of **encoding products**, held together by a shared philosophy. It is not a single technology. It is not a unified platform. Each product is its own codec, its own invention, its own commercial story. The portfolio's coherence lives at the level of principle, not implementation.

## The philosophy — why "Zero Point Encoding"

Zero point in physics is the ground state — what's always there, what cannot be removed. Zero point encoding is the same posture applied to information: find the minimal, fundamental representation for a given signal or structure, in a given domain. Live at the intersection of information theory, encoding, and computational physics. Ship products from that frontier.

"ZPE" is mnemonic shorthand. The name tells you what we think the work is. The rest is specifics.

## Portfolio, not platform

Each product — Bio, Cipher, FT, Geo, IMC, Ink, IoT, Mocap, Neuro, Prosody, Robotics, Video, XR — is an independent encoding product with its own domain, its own customers, its own wedge. They do not share a single underlying technology.

Some share techniques. The 8-primitive / Compass-8 directional encoding pattern appears in **some** lanes (Bio, Geo, Ink, Mocap, IoT, IMC, Cipher) and not in others. It is a lane-specific pattern, not a portfolio claim. The earlier narrative of "eight primitives as the substrate for everything under ZPE" is retired. Each product speaks for itself.

## One license, per-product novelty

The Zer0pa Source-Available License (SAL v6.2) covers the portfolio. Commercial terms — including the $100M revenue threshold — are portfolio-wide. What's protected as **novel** is enumerated per-product inside the license: each product has its own schedule naming what is genuinely new and worth protecting in that specific domain. Same for disclosures: one document, everything in it, easier to debug and manage.

Consequence: the license is simpler. Acquirer disclosure is cleaner. Protection is honest — we claim novelty where we have it, we do not claim it where we don't.

## Always-in-beta

"Always-in-beta" is our **public commercial posture**. Not a hedge. Not an apology. Not "never finished."

It means: we ship products when they have utility. We reserve the right to improve them suddenly — because scientific and engineering breakthroughs do not arrive on a schedule. What you install today works. What you install next month may be materially better. The cadence is continuous, not milestoned.

Frame positively, everywhere. "Useful now, improving continuously." Never "incomplete," "pre-alpha," "not yet ready." If a product genuinely is not shippable, it is not in the portfolio — we remove it, we don't hedge it.

**Note on the Commercial Readiness `Verdict` field.** The positive frame lives in the *prose* — in "What This Is", in "What We Prove", in how the product is described. The website parser reads the `Verdict` cell in the Commercial Readiness table from a controlled enumeration: `{STAGED, PASS, PARTIAL, BLOCKED, FAIL, INCONCLUSIVE}`. Do not invent new tokens (no `ACTIVE_BETA`, `USEFUL_NOW`, `NOT_RELEASE_READY`, `NO-GO`, `PRIVATE_ONLY`, etc.) — they break the pipeline. Express always-in-beta through the surrounding prose and the `STAGED` verdict where applicable, not by reinventing the enum.

## What this means for how we work

- **Refine what needs refining.** No concern about what the commit history looks like to outside observers. Get it right.
- **Do not pretend to be more unified, more complete, or more finished than we are.** The portfolio is a set of independent products, each at its own stage of maturity.
- **Do not pretend to be less novel than we are.** Each product names its real contribution. Where something is genuinely new, say so with specificity. Where a technique is standard (zlib, FFT, varint), call it standard.
- **Honesty is the posture. Continuous improvement is the cadence.** Everything else follows.

---

*This ethos supersedes any prior narrative around "unified 8-primitive platform", "ZPE as a single technology", "10 modalities, one pipeline", or similar portfolio-level architecture claims. Where such language persists in any repo, any doc, any pitch surface — remove or rewrite.*

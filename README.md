# ZPE-Ink

> Product-page mirror for `/encoding/ZPE-Ink/`.
> Live public repo: [Zer0pa/ZPE-Ink](https://github.com/Zer0pa/ZPE-Ink).
> GitHub Markdown cannot reproduce the website typography, CSS, JavaScript, scroll behavior, or live bento layout; this README translates the product page into GitHub-safe Markdown evidence blocks.

## 0. Install / Developer Commands

The product page is the positioning authority. This section is the only retained developer-surface material from the previous root README.

```bash
Deterministic stroke-packet codec. Bit-exact .zpink roundtrip with 0.0 Hausdorff error on measured datasets. Install from PyPI: `pip install zpe-ink
- `.zpink` lossless roundtrip is bit-exact for all generated stroke fixtures — CRC-framed, structured-channel, not byte-opaque. Proof: `proofs/logs/20260321_technical_alignment_pytest.txt
- Corrupted or truncated payloads are rejected by the codec before decoded data is returned. Proof: `proofs/logs/20260321_technical_alignment_pytest.txt
python -m pip install --upgrade pip
python -m pip install -e './code[dev]'
python -m pytest code/tests -q
```

## Product Page Mirror

**Product-page title:** ZPE-Ink · Deterministic .zpink stroke transport · Zer0pa

**Product-page description:** ZPE-Ink · deterministic .zpink stroke packets · exact roundtrip on UJI, CROHME, DigiLeTs, MathWriting, QuickDraw · 0.0 px Hausdorff · PyPI 0.1.1 stale

### Hero Translation

> 00 · ZPE-INK · STROKE PROTOCOLRESEARCH-READY · PyPI STALE Ink that knows the hand that wrote. Stylus stroke codec · ZPE-Ink · PyPI zpe-ink 0.1.1 stale · github.com/Zer0pa/ZPE-Ink When a stylus draws, the mark carries more than its shape — it carries the pressure of the hand, the angle of the pen, the rhythm of how it moved. That information has always been in digital ink. It has never had a codec that kept it exactly. ZPE-Ink is a Python .zpink encoder that seals the full stroke — x, y, pressure, tilt, azimuth — and returns it with 0.00 px Hausdorff error on three public handwriting corpora. The hand's rhythm, kept.

## Positioning

| Field | Value |
| --- | --- |
| Section | encoding |
| Product route | /encoding/ZPE-Ink/ |
| Live public repository | https://github.com/Zer0pa/ZPE-Ink |
| Repo identity used here | ZPE-Ink |
| Website display identity | ZPE-Ink |
| Verdict | STAGED |
| Posture | always_in_beta |
| Headline metric | COMPRESSION: 1.6111×. UJI Pen Characters; Hausdorff 0.0 px on all measured corpora. ZPE-Ink canonical authority surface; useful now, improving continuously. |
| Honest blocker | No claim of release readiness (release surface FAIL); No claim of blind-clone closure (INCONCLUSIVE); No claim of hard-corpus pass |
| Mechanics asset from product page | INK.gif |

## Key Metrics

| Metric | Value | Baseline |
| --- | --- | --- |
| UJI Pen Characters compression ratio | 1.6111× | proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json |
| Max Hausdorff error (all measured corpora) | 0.0 px | proofs/artifacts/public_benchmarks/dataset_matrix.json |
| Measured samples (UJI corpus) | 1,364 | proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json |
| Encode latency | 0.02–0.10 ms/stroke | proofs/artifacts/public_benchmarks/dataset_matrix.json (median_ms_per_stroke) |

## Proof Anchors

| Path | State |
| --- | --- |
| proofs/reruns/phase3_public_benchmarks/phase3_public_benchmarks.json | VERIFIED |
| proofs/artifacts/public_benchmarks/dataset_matrix.json | VERIFIED |
| proofs/artifacts/public_benchmarks/README.md | VERIFIED |
| proofs/artifacts/comp_benchmarks/ink_codec_comparison.json | VERIFIED |
| proofs/artifacts/comp_benchmarks/ink_codec_comparison_real_corpora.json | VERIFIED |
| proofs/artifacts/comp_benchmarks/summary.md | VERIFIED |

## What We Prove

- `.zpink` lossless roundtrip is bit-exact for all generated stroke fixtures — CRC-framed, structured-channel, not byte-opaque. Proof: `proofs/logs/20260321_technical_alignment_pytest.txt`
- Corrupted or truncated payloads are rejected by the codec before decoded data is returned. Proof: `proofs/logs/20260321_technical_alignment_pytest.txt`
- Zero-valued optional channels (tilt, azimuth) are suppressed by default without altering decoded strokes; zero-channel suppression raised CROHME mean compression from 1.52× to 1.76×. Proof: `proofs/artifacts/mathwriting_analysis/comparison.json`
- Binding headers and package version are contract-consistent across the Python, PyO3, WASM, Swift, and C# surfaces. Proof: `proofs/logs/20260321_technical_alignment_binding_contracts.json`
- Hausdorff error = 0.0 px on all five measured public corpora (UJI, CROHME, DigiLeTs, MathWriting, QuickDraw). Proof: `proofs/artifacts/public_benchmarks/dataset_matrix.json`

## What We Do Not Claim

- No claim of release readiness
- No claim of blind-clone closure
- No claim of hard-corpus pass
- No claim of general digital-ink dominance
- No claim that the public benchmark rows close release readiness or hard-corpus authority
- No claim that local binding-contract checks prove full runtime parity for every downstream environment
- No claim that committed compression ratios on the above datasets constitute superiority over general-purpose codecs on those corpora

## Blockers / Failures

> No claim of release readiness (release surface FAIL); No claim of blind-clone closure (INCONCLUSIVE); No claim of hard-corpus pass

## Verification Surface

| Code | Check | Verdict |
| --- | --- | --- |
| V_01 | Bit-exact encode→decode roundtrip on generated fixtures | PASS |
| V_02 | Corrupted payloads are rejected before decode | PASS |
| V_03 | Truncated payloads are rejected | PASS |
| V_04 | Zero tilt/azimuth channels suppressed without altering decoded strokes | PASS |
| V_05 | Binding headers + package version are contract-consistent | PASS |
| V_06 | CLI demo and verify-roundtrip entry points execute | PASS |

## License

| Field | Value |
| --- | --- |
| License | SAL-7.0 |
| Authority source | proofs/reruns/phase5_wedge/final_go_no_go_surface.json |

## Upcoming Workstreams

| Category | Summary |
| --- | --- |
| Operations / External Dependency | Real-corpus expansion (IAM unblock + UNIPEN mirror); IAM is registration-gated and UNIPEN host is unavailable; once unblocked, the existing comparator path runs as-is. |
| Active Engineering | Continue current authority-packet refinement on ZPE-Ink; surface new receipts as they land. |

## Related Repos

- Repo-local proof-surface conventions only; no retired cross-lane repo is current authority.
- ZPE-Mocap - adjacent motion-stream codec in the ZPE transport family.
- ZPE-XR - sibling XR motion compression surface with multi-runtime packaging work.

<details>
<summary>Full Visible Product-Page Bento Translation</summary>

This section preserves the product page cells as Markdown text blocks. It intentionally omits shared site navigation, footer chrome, CSS, and scripts.

### Bento Cell 1

> 00 · ZPE-INK · STROKE PROTOCOLRESEARCH-READY · PyPI STALE Ink that knows the hand that wrote. Stylus stroke codec · ZPE-Ink · PyPI zpe-ink 0.1.1 stale · github.com/Zer0pa/ZPE-Ink When a stylus draws, the mark carries more than its shape — it carries the pressure of the hand, the angle of the pen, the rhythm of how it moved. That information has always been in digital ink. It has never had a codec that kept it exactly. ZPE-Ink is a Python .zpink encoder that seals the full stroke — x, y, pressure, tilt, azimuth — and returns it with 0.00 px Hausdorff error on three public handwriting corpora. The hand's rhythm, kept.

### Bento Cell 2

> 01 · THE GAPSTORED, NOT KEPT Digital ink stores coordinates. It has never had a codec that preserved everything the hand did.

### Bento Cell 3

> 02 · MARKETSADJACENT FORECASTS Digital pen / handwriting market'30 · $5.3B Digital pen'30 · $7.2B Digital writing instruments'30 · $6.2B E-learning content tools'30 · $38.1B Handwriting recognition softwareest. $2.1B Every stylus that captures a stroke moves through these markets; ZPE-Ink is the exact-geometry record underneath them.

### Bento Cell 4

> 03 · VALUE $6.2B 2030 digital writing instruments; ZPE-Ink is the stroke record three public corpora proved exact.

### Bento Cell 5

> 04 · INSIGHT A signature keeps more than the mark — the hand's rhythm.

### Bento Cell 6

> 05.1 · CURRENT TECHSTORED AND FLATTENED A stylus measures pressure and angle dozens of times a second, then a bitmap takes over and flattens the motion into pixels. The hand's rhythm exists in the device for a moment, then disappears into the file.

### Bento Cell 7

> 05.2 · OUR TECHKEEP THE FULL STROKE ZPE-Ink keeps the full stroke. It seals x, y, pressure, tilt, and azimuth into a CRC-framed .zpink packet and returns every coordinate unchanged — 0.00 px Hausdorff error on UJI, CROHME, and DigiLeTs. Zero-channel suppression raises CROHME mean compression from 1.52× to 1.76× when a device omits tilt. The hand's motion, intact.

### Bento Cell 8

> 05.3 · BENCHMARKSPUBLIC CORPUS DATA UJI1.61× · 1,364 samples CROHME1.44× · 90 samples Hausdorff0.00px CRCPASSpublic corpus data UJI1.61× PASS CROHME1.44× PASS DigiLeTs1.09× PASS Scope: UJI, CROHME, DigiLeTs, MathWriting, QuickDraw. IAM/UNIPEN skipped.

### Bento Cell 9

> 06 · MEASUREMENTCORPUS CHECK SUITE Five public corpora replay with exact geometry. CRC rejects the rest.

### Bento Cell 10

> 06.1 · COMPARATIVE PERFORMANCESTROKE BYTES PER SAMPLE .zpink UJI1.61× .zpink CROHME1.44× .zpink DigiLeTs1.09× gzip / zlib aggregate3.33× / 3.73× Same int32 (x, y, pressure, tilt, azimuth) buffer across every corpus. On the QuickDraw plus CROHME aggregate, .zpink compresses 3.82×, gzip 3.33×, zlib 3.73×. IAM is registration-limited; UNIPEN is host-unavailable.

### Bento Cell 11

> 07 · KEY METRICSMEASURED PUBLIC EVIDENCE

### Bento Cell 12

> 07.1 · UJI 1.61× vs raw · 1,364 UJI samples

### Bento Cell 13

> 07.2 · CROHME 1.44× ICFHR package · 90 CROHME samples

### Bento Cell 14

> 07.3 · DIGILETS 1.09× real corpus · 180 DigiLeTs samples

### Bento Cell 15

> 07.4 · HAUSDORFF 0.00px all measured corpora · exact roundtrip

### Bento Cell 16

> 07.5 · PYPI v0.1.1 PyPI stale · next release closes the version skew

### Bento Cell 17

> 08 · STROKE FIDELITYENCODE AND DECODE A stroke enters. The same stroke exits. 0.0 px proves it.

### Bento Cell 18

> 08.1 · WHAT THE CODEC KEEPSALL FIVE CHANNELS Committed artifacts show bit-exact encode-decode on generated fixtures: int32 (x, y, pressure, tilt, azimuth) buffers seal into a CRC-framed .zpink packet and exit without coordinate change — 0.00 px Hausdorff error confirmed on UJI, CROHME, DigiLeTs, MathWriting, and QuickDraw. CRC rejects malformed payloads before decode. Zero-channel suppression raises CROHME mean compression from 1.52× to 1.76× without altering decoded strokes — a device that omits tilt or azimuth gets better compression, not worse. Non-Python runtime parity is not claimed beyond static bindings checked across PyO3, WASM, Swift, and C#.

### Bento Cell 19

> 08.2 · HONEST BLOCKER Honest Blocker · Three checks remain open: cutting the next release, passing the harder IAM and UNIPEN corpora (IAM is registration-limited, UNIPEN is host-unavailable), and proving a clean-room rebuild from spec. Today the PyPI package at 0.1.1 sits ahead of its bindings and runtime at 0.1.0 — a version skew the next release closes.

### Bento Cell 20

> 09 INK THAT KEEPS THE HAND.

### Bento Cell 21

> 09.1 · THE AMBITION The aim is a stroke record that travels — from a tablet to a server to a researcher's workstation to another device entirely — without losing the pressure, the angle, or the rhythm that made the mark a particular person's. Handwriting becomes citable data, not a frozen picture of itself, across the platforms where pens actually write.

### Bento Cell 22

> 09.2 · WHAT WORKS NOW Working today: 0.00 px Hausdorff error on UJI, CROHME, and DigiLeTs; CRC framing confirmed.

### Bento Cell 23

> 09.3 · WHAT'S STILL OPEN Open: PyPI 0.1.2 release, hard-corpus pass on IAM and UNIPEN, blind-clone closure, shipped runtime parity.

### Bento Cell 24

> 09.4 · EDUCATION · NEAR-TERM (12–24 MO) Student handwriting survives the upload An e-learning platform that stores a million pages of student maths working can keep the hand that wrote them — pressure, hesitation, retraced strokes — not a flattened image. A teacher reviewing late work sees the thinking, not the result.

### Bento Cell 25

> 09.5 · SIGNATURES · NEAR-TERM (12–24 MO) A signature carries the hand A bank or notary capturing a signature on a tablet can archive the full stroke dynamics, not a glyph image. Forensic comparison stops being a visual judgment about pixels and becomes a measurable comparison of pressure curves and pen angles across signings.

### Bento Cell 26

> 09.6 · STYLUS PLATFORMS · MID-TERM (24–48 MO) One stroke packet across devices A stylus drawing made on an iPad reaches a Windows tablet, a web canvas, and an Android phone without a conversion step that drops tilt or smooths pressure. The note-taking app stops choosing between portability and fidelity.

### Bento Cell 27

> 09.7 · RESEARCH ARCHIVES · MID-TERM (24–48 MO) Handwriting corpora become jointly searchable UJI, CROHME, DigiLeTs, and any future corpus on the same exact-geometry codec can be queried as one. A handwriting researcher hunting for a specific letter formation stops running three retrieval pipelines and starts asking one question of one archive.

### Bento Cell 28

> 09.8 · ARCHIVE STANDARD · PARADIGM (48 MO+) Pen computing acquires a common record Notes, signatures, sketches, maths, and annotations from any device resolve to the same kind of stroke record. A handwritten archive becomes a citable, retrievable substrate — the way text and code already are — instead of a folder of frozen images that lose the hand.

</details>

---

Source mapping: product route `/encoding/ZPE-Ink/` -> live public repo `Zer0pa/ZPE-Ink`. README generated from product-page authority plus retained install/dev commands only.

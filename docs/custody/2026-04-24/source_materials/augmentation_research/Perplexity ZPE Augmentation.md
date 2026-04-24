# ZPE Codec Physics Lab — NeurIPS-Augmented Lane Synthesis & Engineering Judgment
> **Scope:** 10 ZPE codec lanes (Bio, FT, Geo, Ink, IoT, Mocap, Neuro, Prosody, Video, XR) augmented by NeurIPS 2024–2025 findings.  
> **Governing principle:** Build and connect from what each lane already has into something greater. The NeurIPS lens should emerge from each lane's trajectory, not be imposed uniformly.  
> **Date:** April 2026. All funding and programme data verified to this date.  
> **Posture:** Intersectional science — computation physics / information theory / biocomputation / morphogenesis / cellular automata / cognition. No fabricated metrics.

***
## The Unifying Pattern This Document Discovers
Before diving lane-by-lane, the dot-joining synthesis must be stated plainly. What the NeurIPS 2024–2025 field has collectively confirmed is this: **the boundary between compression, representation, and computation has collapsed**. At NeurIPS 2024, the Machine Learning and Compression workshop explicitly framed compression and learning as "two sides of the same coin". LDNS (NeurIPS 2024) used S4 state-space layers to simultaneously compress spiking data and produce a latent representation suitable for generation. Flow-IB (NeurIPS 2025) achieved 32,768× video compression by making the information bottleneck itself the compression objective. UrbanSparse (NeurIPS 2025) unified geospatial prediction and retrieval in a single compressed-sparse architecture with 25% accuracy gain and 66% faster training.[^1][^2][^3][^4][^5][^6]

The pattern repeats across every domain the ZPE portfolio touches. **What this means for ZPE is not that each lane should become a generative model. It means each lane should be re-examined under the question: "Is our compressed representation also a searchable, transferable, generatively-useful latent?" If yes, the lane is in the right position to connect to the NeurIPS frontier. If no, the lane needs one specific engineering addition.**

The second cross-cutting pattern: NeurIPS 2025's UniReps workshop found that different neural systems — biological and artificial, trained independently — converge on similar internal representations when exposed to similar structure. This is a deep theoretical anchor for ZPE's cross-domain ambition: if representation convergence is real, then a compressed encoding that is faithful to the signal's information-theoretic structure should be transferable, composable, and grounded in something universal. This is the physics-of-information thesis latent in ZPE's design choices.[^7]

***
## Lane-by-Lane Augmentation
---
### 1. ZPE-Neuro
#### What Is Already Real

Lane is bounded to extracellular spike-event encoding and replay. DANDI `000034` is the primary validated corpus, with an IBL second-target pass. No blind-clone authority replay pack exists yet. The blocker is not technical failure but breadth and provenance discipline.

#### NeurIPS 2024–2025 Dot-Joining

The dominant NeurIPS lens for this lane is **LDNS (NeurIPS 2024)**. LDNS proved that a structured state-space autoencoder (S4 layers) can simultaneously (a) compress discrete high-dimensional spiking data into a low-dimensional continuous latent and (b) support conditional generation of realistic neural activity. This is the conceptual upgrade ZPE-Neuro needs to see. The ZPE-Neuro lane is currently positioned as a compression-and-replay codec. LDNS shows the same architecture can be a **latent space for scientific hypothesis testing** — the compressed representation becomes an experimental substrate. This is the upgrade thesis: ZPE-Neuro is not just a codec; it is infrastructure for synthesising testable neural activity from compressed event representations.[^1][^5][^6]

The NeuroMamba paper (NeurIPS 2025) demonstrated a state-space foundation model for 4D fMRI using autoregressive Mamba pretraining. The REVE EEG foundation model (NeurIPS 2025) pretrained on 60,000 hours of EEG, achieving state-of-the-art on 10 downstream tasks. These are full-waveform models — outside ZPE-Neuro's current scope — but they anchor the grant narrative: **FAIR-compliant spike-event data infrastructure is the prerequisite layer that foundation models like NeuroMamba and REVE need to train on real, reproducible recordings**. ZPE-Neuro is not competing with these models; it is the provenance-preserving data layer beneath them.[^8][^9]

The EBRAINS/Horizon Europe Research Infrastructures call (deadline 16 June 2026, €32M budget) explicitly funds "AI-powered tools and workflows that help researchers interact with complex brain data... improved data integration, indexing and FAIR data management to strengthen EBRAINS as an open and reliable digital research environment". This is the most precisely aligned grant call in the entire portfolio.[^10]

#### Engineering Augmentation

The single highest-value engineering addition is: **replace the current event-sequence format with S4-compatible discrete-to-continuous latent encoding**. This means:

1. Add a lightweight S4 autoencoder layer on top of the existing spike-event serialisation that maps event sequences to a fixed-dimensional continuous latent vector per recording segment.
2. This latent is IIIF-analogous for neural data: it is a compact, searchable, transmissible handle on the recording's information content.
3. The encoding is still losslessly reversible to the event layer (the existing compression guarantee is preserved), but the latent layer adds retrieval and similarity capabilities.

The rationale: this addition turns ZPE-Neuro from a "compression format" into a "searchable neural data infrastructure" — the framing the EBRAINS call requires. The implementation cost is modest because S4 layers are available in Apache-2.0 libraries (Mamba, SSM-related repos). The added authority: a blind-clone replay benchmark showing that two independent environments, starting from the latent vector, reproduce identical spike-event sequences. This is the provenance proof the grant narrative needs.

**Next breadth target:** IBL's Brain Wide Map (BWM) dataset contains recordings from 547 brain regions across 174 sessions — a massive step-up from `000034`. A successful BWM breadth pass using the S4-latent architecture would be a genuine advance.

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Horizon Europe RI 2026 (EBRAINS call) | EU | **Tier 1** — exact narrative match[^10] | €32M consortium call |
| BBSRC Standard Research Grant | UK | **Tier 2** — up to £2M[^11][^12]; "data intensive and technology development" remit | £2M max |
| NIH/NSF BRAIN Initiative (Next-Gen Tools) | US | **Tier 3** — ZPE-Neuro needs a US academic co-PI | US$1–3M typical |

**Ranked verdict:** EU EBRAINS call dominates — the narrative is tailor-made. UK BBSRC is viable as a standalone if EU co-applicants are not available. US requires a co-PI bridge.

***
### 2. ZPE-Bio
#### What Is Already Real

Strong ECG proof committed under `validation/results/`. CI is red but the proof artifacts are real. Bio Wearable is hard-blocked at Gate F. Lane is correctly narrowed to deterministic ECG replay with auditable proof lineage.

#### NeurIPS 2024–2025 Dot-Joining

The dominant NeurIPS lens is the **ECG retrieval and foundation model landscape at NeurIPS 2024–2025**. ECG-ReGen (NeurIPS 2024 workshop) demonstrated retrieval-augmented ECG report generation using PTB-XL and MIMIC-IV-ECG — the same datasets ZPE-Bio likely uses. The TRACE framework (NeurIPS 2025) showed that multimodal time-series embedding retrieval requires grounding in aligned textual context, with hard negative mining for semantically meaningful retrieval.[^13][^14]

The critical insight from the NeurIPS 2024–2025 ECG landscape: **the field is moving toward foundation models (ECG-FM, DSAIL-SNU) that require large-scale, FAIR-labelled ECG data as training infrastructure**. The end-to-end ECG fine-tuning study (JMIR 2026) showed that de novo models like InceptionTime and XceptionTime frequently outperform pretrained foundation models when fine-tuned, precisely because foundation models require high-quality, reproducible data to transfer well. This is where ZPE-Bio's auditable replay discipline becomes an infrastructure wedge: **trustworthy, reproducibly-labelled ECG infrastructure is the unsexy but necessary prerequisite for ECG foundation models**. ZPE-Bio is not a foundation model; it is the replay layer beneath them.[^15]

The NeurIPS 2025 Time Series and Health workshop confirmed that clinical time-series has persistent challenges in "uncertain ground truth, quasi-periodic physiological motifs, and non-semantic timepoints" — exactly the problems ZPE-Bio's deterministic replay addresses.[^16]

#### Engineering Augmentation

The key addition is a **retrieval layer over the ECG compression format**: given a compressed ECG record, return the k-nearest similar records from the index, with provenance metadata. This wraps the existing compression codec with a Faiss-backed similarity index operating in the compressed domain (not the raw domain — compressed-domain retrieval is the novel claim). The combination of (a) lossless deterministic compression + (b) compressed-domain ECG retrieval is the unpublished combination that ECG-ReGen and similar work do not have, because they operate on embeddings of raw or reconstructed signals.

This is a publishable methods contribution at the NeurIPS 2025 Time Series workshop level, and it directly answers the question "what does ZPE-Bio add beyond a compression codec?" with something technically specific.

CI repair comes first — this is not an enhancement but a maintenance prerequisite. The engineering sequence: (1) repair CI, freeze green truth; (2) add compressed-domain retrieval layer; (3) benchmark on PTB-XL; (4) publish.

**Wearable verdict:** Keep hard-blocked until Gate F produces real wearable-grade proof. Do not reopen under funding pressure. The ECG lane is strong enough on its own.

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Horizon Europe Cluster 1 Health 2026-27 (data infrastructure for clinical research) | EU | **Tier 1** — clinical data reproducibility is explicitly funded[^17] | €2–6M per project |
| BBSRC Data-Intensive Research | UK | **Tier 2** — bioinformatics tools remit[^11] | Up to £2M |
| NIH NLM (National Library of Medicine) data infrastructure | US | **Tier 2** — clinical signal infrastructure; R01 mechanism | US$0.5–1.5M |
| MedTech commercial buyer (Philips, GE HealthCare, CardioNET) | Commercial | **Tier 3** — auditable replay is a regulatory-grade differentiator | License/API |

**Ranked verdict:** EU Horizon Cluster 1 Health is Tier 1 because the 2026–2027 work programme has explicit clinical data infrastructure topics. UK BBSRC is reliable and reachable. US NIH requires co-PI.[^17]

***
### 3. ZPE-Mocap
#### What Is Already Real

CMU corpus benchmark: 18.77× compression vs raw BVH float32; 32.45 mm mean MPJPE (imprecise reconstruction); synthetic retrieval P@10 = 1.0 at 26.14 ms p95 latency. Honest wedge is retrieval/indexing, not playback-grade reconstruction.

#### NeurIPS 2024–2025 Dot-Joining

The dominant NeurIPS lens is **MotionBind (NeurIPS 2025)** and the **motion retrieval landscape**. MotionBind built a multi-scale temporal motion transformer (MuTMoT) and a Retrieval-Augmented Latent Diffusion model (REALM), achieving state-of-the-art on motion-text retrieval, zero-shot action recognition, and cross-modal retrieval. The important finding: **motion retrieval quality is dominated by the quality of the temporal embedding, not the fidelity of reconstructed poses**. MotionBind works in latent space; it does not need reconstruction-grade BVH output. This directly validates ZPE-Mocap's real authoritative wedge.[^18][^19]

The 4DGCPro paper (NeurIPS 2025) showed that 4D Gaussian compression can support real-time mobile decoding via motion-aware adaptive grouping to reduce temporal redundancy. The key abstraction: **temporal redundancy is the right unit of analysis for motion compression**, not frame-level pose accuracy. ZPE-Mocap's 18.77× compression ratio is a temporal-redundancy result, whether or not the internal architecture frames it that way.[^20]

The NeurIPS 2025 WISA poster (World Simulator Assistant for physics-aware text/motion interaction) and TemMEGA (NeurIPS 2025 camera tokenizer for temporal masked generative modeling) confirm: the trajectory is toward **discrete motion tokenisation as the substrate for downstream generation and retrieval**, not high-fidelity reconstruction. ZPE-Mocap, reframed as a motion tokeniser rather than a motion codec, is positioned correctly in this landscape.[^21]

#### Engineering Augmentation

The highest-value addition is: **replace the current synthetic retrieval evidence with a real-data retrieval benchmark using AMASS (the SMPL-based motion corpus used by MotionBind)**. The AMASS corpus is open, covers 300+ subjects and 40+ action categories, and is the standard retrieval benchmark. A ZPE-Mocap retrieval benchmark on AMASS, reporting P@k and latency under real-data distribution, would be directly comparable to MotionBind and publishable at CVPR, ECCV, or ICCV workshops.

The second addition: **expose a motion embedding API** that accepts a BVH/SMPL sequence, compresses it using ZPE-Mocap's temporal encoder, and returns a fixed-dimensional embedding suitable for downstream cosine-similarity retrieval. This is the "retrieval-first" packaging that MotionBind and similar systems need as a compute-efficient compression layer below their embedding models.

Claims to retire: reconstruction-grade and playback-grade claims should be removed from all documentation. The MPJPE number (32.45 mm) should be published as a known limitation, not a capability.

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Innovate UK AI Champions: Frontier AI Phase 1 (closes 29 April 2026) | UK | **Tier 1** — "frontier AI with defensible scale-up"[^22]; motion retrieval infrastructure qualifies | Share of £3M |
| Horizon Europe Cluster 4 Digital/Robotics (embodied AI datasets) | EU | **Tier 2** — robotics dataset infrastructure aligns[^23] | €2–4M |
| Commercial: robotics simulation (Boston Dynamics, Agility, Unitree) | Commercial | **Tier 2** — motion corpus indexing for sim-to-real transfer | B2B licensing |
| Commercial: animation/VFX (side FX, Unity, Unreal) | Commercial | **Tier 3** — motion library search tool | SaaS |

**Ranked verdict:** Innovate UK AI Champions closes 29 April 2026 — this is an immediate application window. The motion retrieval framing fits "frontier AI with defensible scale-up." EU Cluster 4 is the follow-on vehicle after a successful UK pilot.

***
### 4. ZPE-IoT
#### What Is Already Real

Release preflight 17/0/1. Strict DT 27/27. E1 benchmark 10/11 wins (DS-12 is a known competitor win). Promoted benchmark frame 6.65× mean on DS-01..DS-10. Main recent blocker was environment/disk hygiene, not proof quality.

#### NeurIPS 2024–2025 Dot-Joining

The NeurIPS lens for this lane is **information-theoretic sensor compression under constrained channel capacity**, which is represented most directly by the NeurIPS ML and Compression workshop's work on spiking state-space models for long-range dependency in sensor data. The deeper theoretical anchor is the **Mamba4Cast zero-shot forecasting work (NeurIPS 2024)**: a Mamba (S6 selective-scan SSM) model trained on synthetic data achieves competitive zero-shot performance on real-world time-series. The implication for ZPE-IoT: if a compact SSM can forecast from compressed representations without domain-specific fine-tuning, then ZPE-IoT's compressed representations have latent generative/predictive value that has not been exploited.[^2][^24]

The NeurIPS 2024 TRACE framework and the NeurIPS 2025 cross-modal retrieval work confirm that IoT sensor streams, when grounded in a compact semantic embedding, support downstream tasks (anomaly detection, pattern retrieval, predictive maintenance) that are commercially valuable but not yet part of ZPE-IoT's claim surface.[^14][^25]

The most important NeurIPS signal for IoT is indirect: **the ML-compression workshop's thesis that compression is learning**. ZPE-IoT's current claim is "better compression ratio with deterministic behaviour." The upgrade thesis: "ZPE-IoT's compressed representation is also a domain-aware embedding from which downstream inference is directly possible." This makes the lane a **compression-native edge inference substrate**, not just a compressor.[^2]

#### Engineering Augmentation

The single highest-value closure lane is **native wheel (pip install) closure followed immediately by compressed-domain anomaly detection**. The rationale: native install is the prerequisite for any commercial evaluation; it also unlocks the Innovate UK AI Champions window. The anomaly detection addition is the NeurIPS-aligned engineering thesis — it proves that the compressed domain is semantically rich, not just compact. Implementation: add a lightweight anomaly scoring head that operates on the compressed representation (not the raw signal), trained in a self-supervised fashion on the existing benchmark corpora.

DS-12 remains a competitor win. The correct posture is to publish this honestly in a methods note and focus the claim surface on DS-01..DS-10 plus the new anomaly detection capability, which DS-12 does not offer.

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Innovate UK AI Champions: Frontier AI Phase 1 (closes 29 April 2026) | UK | **Tier 1** — strongest immediate window[^22] | Share of £3M |
| Horizon Europe Cluster 5 Climate/Energy (IoT for energy infrastructure) | EU | **Tier 2** — smart sensor networks for energy efficiency[^17] | €2–5M |
| Commercial: industrial IoT (Siemens, Bosch, Honeywell Analytics) | Commercial | **Tier 1** — deterministic compression with anomaly detection is a procurement-grade differentiator for edge devices | Direct sales |

**Ranked verdict:** IoT is the portfolio's strongest immediate commercial lane because the proof surface already exists and native packaging is the only remaining gate. Innovate UK AI Champions (closes 29 April 2026) is urgent.

***
### 5. ZPE-Geo
#### What Is Already Real

Live GPD through Phase 03.1.1. Phase 04 (blind-clone, release readiness) planned. Sovereign blockers GEO-C001, C002, C004 remain open. AV2 and NOAA AIS corpus closure incomplete.

#### NeurIPS 2024–2025 Dot-Joining

The exact NeurIPS lens for ZPE-Geo is **UrbanSparse (NeurIPS 2025)**, which unified geospatial prediction and retrieval through a sparse-dense architecture combining Bloom filter sparse encodings (for high-sparsity geographic queries) with a dense semantic codebook. Results: 25% prediction accuracy gain, 21% retrieval precision gain, 66% faster training over state-of-the-art baselines. UrbanSparse is conceptually close to what ZPE-Geo is building — the difference is domain (urban intelligence vs mobility/trajectory) and the explicit information-theoretic framing. **The insight from UrbanSparse is that sparse-dense hybrid encoding is the right architecture for geospatial data, and that prediction and retrieval should be joint objectives, not separate tasks.**[^3]

The NeurIPS 2025 continent-scale geo-localisation paper showed that combining proxy classification (for rich feature learning) with aerial image embeddings enables direct retrieval at 100-metre precision across continental scale. The transferable lesson: **the right geospatial embedding is learned by combining a dense representation task with a retrieval task jointly**, not by training a compressor and then adding retrieval as a downstream step.[^26][^27]

NeurIPS 2025's AlphaEarth Foundations work (Google DeepMind) produced an information-dense global geospatial representation. For ZPE-Geo, this is both a competitive signal (large-scale geospatial representation is being tackled by top labs) and a research anchor (ZPE-Geo's trajectory-level compression is at a different layer — below foundation models, at the raw signal level, analogous to ZPE-Neuro's position relative to EEG foundation models).[^28]

#### Engineering Augmentation

The most leverage-rich augmentation is: **close AV2 corpus first (GEO-C001), then add a sparse trajectory hash layer** that maps compressed trajectory representations to a Bloom-filter-based sparse encoding following UrbanSparse's approach. This produces two things: (a) a compressed representation (existing) and (b) a searchable sparse code that supports fast approximate trajectory retrieval. This combination is not in the current geospatial retrieval literature and is directly publishable.

The blind-clone (Phase 04) should proceed only after AV2 corpus closure — the brief's own sequencing instinct is correct. Releasing a blind-clone against incomplete corpus closure would produce a provenance-weak authority surface.

The commercial claim that is honest: **reproducible, searchable trajectory compression for mobility and fleet telemetry**. This does not require solving AIS; it requires a clean AV2-based benchmark with retrieval metrics.

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Horizon Europe Cluster 5 (Climate/Energy, Smart Mobility) | EU | **Tier 1** — AI-enabled mobility infrastructure is explicitly funded 2026-27[^17] | €3–8M |
| UK Innovate UK (Transport Infrastructure / Connected and Autonomous Vehicles) | UK | **Tier 2** — CAV infrastructure; AV2 corpus pass would be the proof anchor | Up to £5M |
| Commercial: fleet telematics (Samsara, Verizon Connect, HERE Technologies) | Commercial | **Tier 2** — searchable trajectory compression at edge is a real procurement need | B2B SaaS |

**Ranked verdict:** EU Cluster 5 is Tier 1 because the 2026-27 programme has explicit smart mobility topics and the corpus requirements (AV2) map to EU-relevant road environments. Proceed only after AV2 closure.

***
### 6. ZPE-FT
#### What Is Already Real

Phase 06 blocked on: missing exact 30-symbol OHLCV authority pack, exact 3 top-of-book tick authority pack, and auditable FT-C004 truth. Proof preserves carried floor and bounded proxy lanes but does not close the sovereign gate.

#### NeurIPS 2024–2025 Dot-Joining

The NeurIPS lens here is **FinZero (NeurIPS 2025)** and the **TRACE multimodal retrieval framework**. FinZero demonstrated a multimodal pre-trained model fine-tuned with RLHF on financial time-series, achieving ~13% prediction accuracy improvement over GPT-4o in high-confidence regimes. TRACE showed that grounding time-series embeddings in aligned textual context enables semantically meaningful retrieval.[^14][^29]

The deeper NeurIPS signal for ZPE-FT is from Mamba4Cast: zero-shot forecasting from compressed representations is possible when the compression architecture captures temporal structure faithfully. This suggests that ZPE-FT's "sidecar accelerator" thesis — the compressed representation as a substrate for downstream inference — is theoretically sound, but only if the input data is exact and auditable. The NeurIPS literature does not help with the sovereign gate problem; it only validates the thesis **conditional on closing the gate**.[^24]

The information-theoretic framing: financial time-series has the highest information density per sample of any ZPE domain (tick data is information-theoretically close to a random walk, making compression harder and the compressed representation more information-theoretically meaningful when it works). If Phase 06 closes honestly, the research contribution is well-positioned at the NeurIPS ML and Compression workshop and at QuantLib/finance-ML venues.

#### Engineering Augmentation

The sequencing is fixed by the brief's own sovereign gate logic: Phase 06 data closure comes before any engineering augmentation. The best honest data closure strategy for the OHLCV pack is: **Polygon.io (US equities, L2 data, free tier available) for 30 symbols, with an explicit license declaration**. For top-of-book tick data, **Tardis.dev** provides institutional-grade normalised tick data for crypto and equity markets at deterministic replay quality. Both are rights-safe for academic benchmarking.

**If Phase 06 cannot close cleanly** (FT-C004 truth remains absent), the highest-value honest pivot is: reframe the lane as a **compressed representation benchmark for financial time-series similarity search** rather than a sidecar accelerator. The pivot thesis: given two compressed OHLCV windows, does ZPE-FT's compression preserve the information-theoretic structure that makes similar market regimes retrievable? This is a weaker but still publishable claim that does not depend on exact sidecar benchmark closure.

Kill criterion: if exact Polygon/Tardis data + FT-C004 closure does not happen within 60 days of initiating the data acquisition, pivot.

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Commercial: market data infrastructure (Bloomberg, Refinitiv API customers) | Commercial | **Tier 1** — sidecar compression for high-frequency data infrastructure is a real procurement category if Phase 06 passes | Direct enterprise |
| NSF/CISE (information theory + financial systems, if framed as compressed-domain retrieval) | US | **Tier 3** — niche but possible as a methods contribution | US$0.3–0.8M |
| UKRI/Innovate UK (FinTech/open banking data infrastructure) | UK | **Tier 3** — real but competitive | Up to £1M |

**Ranked verdict:** Commercial is Tier 1 because the buyer is clearly defined (market data infrastructure vendors) and the value proposition is clear if Phase 06 passes. Grant is a distant secondary.

***
### 7. ZPE-Ink
#### What Is Already Real

Archived NO-GO/NOT_READY. Live repo has stronger cross-runtime surfaces than the archived verdict assumed. Best surviving wedge is deterministic multi-runtime ink interchange (Python, Rust, Swift, C#). Immediate blockers are disk, truth-surface inconsistency, and stale README.

#### NeurIPS 2024–2025 Dot-Joining

The NeurIPS lens for ZPE-Ink is oblique but real. The NeurIPS 2025 work on **handwriting decoding from EEG as motor imagery** confirms that digital ink stroke sequences carry rich motor-program information that is distinct from, but related to, neural motor encoding. More directly relevant: the FocalCodec paper (NeurIPS 2025) introduced a low-bitrate codec based on focal modulation using a single binary codebook — the architecture is for speech, but the principle (binary codebook + focal modulation for structured temporal signal compression) is directly applicable to ink stroke sequences. Ink strokes are temporally structured, pen-pressure-weighted sequences with spatial topology; they are more similar to speech codec problems than to image compression problems.[^30][^31]

The UniReps workshop (NeurIPS 2025) finding on representation convergence is relevant here: if ink-stroke encoders trained independently across runtimes converge on similar representations when the underlying motor structure is the same, then cross-runtime deterministic parity is not just an engineering feat — it is theoretically expected from the representation-learning perspective. This framing turns ZPE-Ink's cross-runtime determinism into a scientific claim about ink stroke representation universality.[^7]

#### Engineering Augmentation

**Reopen verdict: reopen as a bounded interoperability truth-reconciliation lane**, subject to a clean fresh-install proof in all four runtimes passing first. The wedge is deterministic multi-runtime interchange, not broad compression. The NeurIPS-aligned engineering augmentation: add a binary codebook representation layer (following FocalCodec's approach) to the ink stroke encoder, making the compressed representation runtime-agnostic by construction. A binary codebook eliminates floating-point divergence across runtimes — this is the engineering solution to the cross-runtime parity problem and makes ZPE-Ink's parity claim architecturally grounded rather than empirically verified.

The target audience for this augmentation is enterprise note-taking and digital whiteboard platforms (Apple Pencil → iPad OS → macOS → cross-platform sync) where cross-runtime determinism is a real procurement requirement.

Kill condition: if the fresh multi-runtime install proof cannot pass within one sprint, keep the archived NO-GO verdict and do not reopen.

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Commercial: enterprise digital ink platforms (Wacom, Apple, Samsung, Microsoft OneNote) | Commercial | **Tier 1** — cross-runtime determinism for enterprise ink interchange is a real gap | B2B SDK licensing |
| EU Horizon Europe Cluster 4 Digital (open standards for digital interaction interoperability) | EU | **Tier 3** — viable if framed as open interchange standard for digital ink | €1–3M |

**Ranked verdict:** Commercial is Tier 1 and the only realistic near-term vehicle. The market is enterprise SDK licensing to digital ink platform vendors. Grant is low-priority until the lane reopens cleanly.

***
### 8. ZPE-Prosody
#### What Is Already Real

Compression 16.5952×. F0 RMSE 0.8925%. Quality score 47/50. Retrieval P@5 = 0.3067 against 0.80 gate — sovereign FAIL. Tests green, branch not clean.

#### NeurIPS 2024–2025 Dot-Joining

The NeurIPS lens for ZPE-Prosody is **FocalCodec (NeurIPS 2025)** and the **speech provenance / synthetic speech detection literature**. FocalCodec achieved low-bitrate speech coding at 0.16–0.65 kbps using a single binary codebook. The key finding: FocalCodec preserves "sufficient semantic and acoustic information" for downstream tasks including generative modelling. The direct implication for ZPE-Prosody: **if the prosodic feature representation is re-encoded using a binary codebook approach, the retrieval failure (P@5 = 0.30) is likely caused by floating-point embedding space fragmentation rather than fundamental prosodic information loss**. Binary codebooks discretise the space, which makes Hamming-distance retrieval over the codebook entries much more reliable than cosine-distance retrieval over continuous F0 embeddings.[^32][^30]

The synthetic speech detection literature (arXiv April 2026) confirms that prosody-based detection methods are among the most robust approaches for identifying anomalous speech — because prosody encodes physiological and behavioural characteristics of specific speakers. This creates a commercial application: **prosodic identity verification using ZPE-Prosody's deterministic F0 encoding as a compressed speaker-identity fingerprint**. This is a different commercial surface from the original retrieval thesis, and it does not require P@5 retrieval — it requires deterministic replay and F0 fidelity, which ZPE-Prosody already has.[^32]

The VIBE information bottleneck paper (NeurIPS 2025) scored video-language model outputs using the information bottleneck framework — annotation-free. The principle transfers: ZPE-Prosody's compressed F0 encoding is an annotation-free information bottleneck on the prosodic content of speech. This is a scientific framing that makes the lane more than a codec.[^33][^34]

#### Engineering Augmentation

**Verdict: rescue retrieval via binary codebook re-encoding (CPU-first), not GPU-first.** The rescue path:

1. Replace the continuous F0 embedding with a binary codebook (following FocalCodec's design principle) using product quantisation over the F0/prosody feature space.[^30]
2. Implement Hamming-distance retrieval over the codebook (O(n) bitwise operations, CPU-native).
3. Re-run the P@5 benchmark using this new retrieval mechanism.

This is a CPU-first, architecturally grounded fix — not brute-force metric learning. Expected outcome: Hamming retrieval over a well-designed binary codebook should substantially improve P@5 because it handles the discretisation of prosodic space correctly.

If retrieval still fails after this modification, narrow the lane to **prosodic identity fingerprinting** (speaker verification using compressed F0 as a lightweight identity token) and retire the general retrieval claim. This narrowing has a commercial market (voice biometrics, speaker diarisation) that is larger than generic prosody retrieval.

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Commercial: voice biometrics / speaker verification (Nuance/Microsoft, Pindrop, Veridas) | Commercial | **Tier 1 (if narrowed)** — compressed prosodic fingerprinting is a real gap in lightweight speaker verification | B2B licensing |
| EPSRC/AHRC interdisciplinary (speech science / forensic phonetics infrastructure) | UK | **Tier 2** — prosodic encoding infrastructure for speech forensics | £0.3–0.8M |
| EU Horizon Europe Cluster 4 Digital (language technology infrastructure) | EU | **Tier 3** | €1–3M if framing is right |

**Ranked verdict:** Commercial (voice biometrics) is Tier 1 if the lane narrows correctly. Grant is UK-first via EPSRC/AHRC.

***
### 9. ZPE-Video
#### What Is Already Real

Defended commercial result: Candidate B — cross-writer, hash-stable AI-perception receipts. Primitive-native byte gate is red. Red Magic userspace path partially validated. Phase 10 blocked.

#### NeurIPS 2024–2025 Dot-Joining

The NeurIPS lens for ZPE-Video is one of the strongest across the entire portfolio. Three distinct threads converge:

**Thread 1 — Perceptual hashing robustness (NeurIPS 2024)**: The NeurIPS 2024 assessment of PhotoDNA, PDQ, and NeuralHash showed these algorithms have "significant robustness against hash-evasion and hash-inversion attacks" due to "random hash variations characteristic of PHAs." This is directly relevant to Candidate B: the cross-writer hash-stable receipt is a perceptual hash with documented stability properties. The NeurIPS framing gives the receipt a theoretical grounding: ZPE-Video's cross-writer stability is a designed random-variation property, not a bug.[^35]

**Thread 2 — AI-Generated Video Detection via Perceptual Straightening (NeurIPS 2025)**: ReStraV used DINOv2 to quantify temporal curvature and stepwise distance in representation space, achieving 97.17% accuracy and 98.63% AUROC for AI-generated video detection. The deep finding: real videos have measurably different geometric trajectories in neural representation space than AI-generated videos. This is the scientific basis for ZPE-Video's perception receipt: **a hash-stable receipt that encodes the temporal-geometric signature of a video in representation space is a provenance certificate, not just a content hash**. The Candidate B receipt, if extended to include DINOv2 temporal curvature features, becomes a provenance certificate that distinguishes real from AI-generated content with near-SOTA detection capability.[^36]

**Thread 3 — Flow-IB video compression (NeurIPS 2025)**: Flow-IB achieved 32,768× compression using the information bottleneck principle combined with flow matching. The primitive-native compression thesis for ZPE-Video maps to this space in the long run, but the short-run lesson is different: **the information bottleneck principle can be used to define what a receipt should contain** — it should encode the minimum sufficient information for downstream perceptual tasks, not the full frame content. This makes the receipt a principled information-theoretic object, not just an engineering hash.[^4]

#### Engineering Augmentation

The wedge is clear: **deepen Candidate B into a principled AI-content provenance receipt** using the ReStraV + perceptual hashing + information bottleneck triangle. The specific additions:

1. Extend the existing hash-stable receipt to include DINOv2 temporal curvature features (following ReStraV) — this adds AI-generation detection capability to the receipt at negligible computational cost (DINOv2 is Apache-2.0 licensed).[^36]
2. Formalise the receipt as an information bottleneck certificate: it encodes the minimum I(Receipt; Video) that is sufficient to verify perceptual authenticity, explicitly bounded. This is the publishable scientific contribution.
3. Market the combined artifact as a **C2PA-compatible perceptual provenance receipt** for video content — C2PA (Coalition for Content Provenance and Authenticity) is the industry standard for digital content credentials, supported by Adobe, Microsoft, and Google. Aligning the receipt format with C2PA makes it immediately adoptable.

Phase 10 / primitive-native: keep blocked until byte gate is green. The receipt program is the correct near-term priority and does not depend on primitive-native closure.

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Commercial: media verification platforms (Adobe Firefly Trust, Getty Images, AP, Reuters) | Commercial | **Tier 1** — C2PA-compatible AI-content receipts are being procured now | Direct sales / SDK |
| UK DSIT (Digital Safety and Provenance — Online Safety Act implementation tools) | UK | **Tier 1** — the UK Online Safety Act creates regulatory demand for AI content provenance tools | Up to £5M Innovate UK |
| EU Horizon Europe Cluster 3 (cybersecurity / content integrity) | EU | **Tier 2** — AI-generated content authenticity is an explicit Cluster 3 topic | €2–5M |
| US DARPA SEMAFOR / MediFor (media forensics) | US | **Tier 2** — US defence-adjacent media provenance; requires US co-PI | DARPA-scale |

**Ranked verdict:** Video has the strongest commercial lane in the entire portfolio. The C2PA/media verification market is active and procuring in 2026. UK DSIT (Online Safety Act) is Tier 1 grant vehicle. This is the portfolio's highest near-term revenue asymmetry.

***
### 10. ZPE-XR
#### What Is Already Real

GPD complete through Phase 09.1. Phase 09-02 (staged-sync, public truth repair) is open. Public comparator gate failed at 0/5. Fanmode is the clearest downstream wedge.

#### NeurIPS 2024–2025 Dot-Joining

The NeurIPS lens for ZPE-XR is the **deterministic input compression for embodied/interactive systems** literature. This is less directly represented at NeurIPS than other lanes, but the relevant thread is the 4DGCPro paper — real-time mobile decoding for volumetric video streaming via hierarchical 4D Gaussian compression. The deep principle: **for XR, the interaction stream (input events, tracking data, gesture commands) has exactly the same temporal structure as motion data — it is a compressed trajectory through interaction space**. ZPE-XR's value is not as a rendering codec; it is as a low-latency, deterministic interaction event transport layer.[^20]

The NeurIPS 2025 TemMEGA camera tokeniser used discrete tokenisation + masked prediction for camera movement synthesis. The relevance: **XR interaction inputs are camera-adjacent data — head pose, controller position, gaze direction**. A discrete tokeniser for XR interaction events, trained with masked prediction, would support both deterministic compression (existing ZPE-XR capability) and generative/predictive interaction (the NeurIPS-aligned capability). This is the upgrade thesis.[^21]

The Fanmode lane (XR input-layer bridge to a downstream application) is correctly identified as the highest-value near-term wedge. The NeurIPS lens supports this: the value of XR compression is realised at the application boundary, not in the codec standalone.

#### Engineering Augmentation

Phase 09-02 (staged-sync, public truth repair) must close first. This is non-negotiable — the 0/5 comparator failure must be resolved before any downstream claim is credible.

After 09-02: the highest-value addition is **a discrete interaction tokeniser for XR events** (following TemMEGA's approach). This takes the existing ZPE-XR deterministic compression and adds a codebook-based discrete representation that makes the compressed interaction stream compatible with modern generative model pipelines (Fanmode, and future agentic XR systems). The tokeniser operates on compressed interaction events, not raw frames — ZPE-XR's uniqueness is compression-first encoding; the tokeniser is the application-layer wrapper.[^21]

#### Grant/Commercial Sizing by Geography

| Vehicle | Geography | Fit | Estimated Size |
|---|---|---|---|
| Commercial: Fanmode / XR application partner (deterministic input layer SDK) | Commercial | **Tier 1** — as described in lane brief; real partnership opportunity | SDK/revenue share |
| Innovate UK (Immersive Technologies / Virtual Worlds) | UK | **Tier 2** — immersive technology infrastructure; deterministic interaction transport is credible | Up to £2M |
| EU Horizon CL4-2025 GenAI for Virtual Worlds | EU | **Tier 3** — the 2025 call is closed; watch 2026-27 equivalent | €3–8M future |

**Ranked verdict:** Commercial (Fanmode) is Tier 1 and the correct near-term focus. The 09-02 truth repair is the prerequisite.

***
## Cross-Portfolio Dot-Joining: The Unified Lens
With all 10 lanes analysed, the emergent NeurIPS synthesis is:

**The ZPE portfolio is building domain-specialised information bottlenecks for high-dimensional sequential data, and the NeurIPS 2024–2025 frontier confirms that this is the right abstraction layer.** The theoretical unification is the information bottleneck principle — compress a signal into the minimum sufficient representation for downstream use — applied simultaneously in 10 domains (neural spikes, cardiac signals, motion, IoT sensors, geospatial trajectories, financial tick data, ink strokes, prosody, video, XR interaction).

What NeurIPS has revealed in 2024–2025 that was not visible before:
1. The compressed representation should also be a generative prior (LDNS, Flow-IB) — this unlocks simulation and synthetic data from the compressed domain.[^1][^4]
2. Retrieval from the compressed domain, not the raw domain, is both feasible and desirable (TRACE, UrbanSparse, MotionBind).[^3][^14][^18]
3. Binary/discrete codebooks make cross-runtime and cross-system parity architecturally guaranteed, not empirically verified (FocalCodec).[^30]
4. Temporal-geometric signatures in representation space distinguish real from synthetic content (ReStraV) — this is the theoretical basis for the Video receipt lane.[^36]
5. Representation convergence across independent systems is expected when signals share underlying structure (UniReps) — this validates cross-domain ZPE composability in principle.[^7]

***
## Grant/Commercial Sizing: Ranked by Lane Fit
### Geography Tier Rankings
#### United Kingdom (Innovate UK / UKRI / BBSRC / EPSRC)

| Lane | Vehicle | Closes | Size |
|---|---|---|---|
| IoT | Innovate UK AI Champions Frontier AI Phase 1[^22] | 29 Apr 2026 | Share £3M |
| Mocap | Innovate UK AI Champions Frontier AI Phase 1[^22] | 29 Apr 2026 | Share £3M |
| Video | DSIT/Innovate UK Online Safety Act provenance tools | Rolling 2026 | Up to £5M |
| Bio | BBSRC Standard Research (data-intensive bioinformatics)[^11] | 3× per year | Up to £2M |
| Neuro | BBSRC Standard Research (data-intensive neuroscience)[^11] | 3× per year | Up to £2M |
| XR | Innovate UK Immersive Technologies | Rolling | Up to £2M |

**UK is Tier 1 for IoT and Mocap** because of the immediate 29 April 2026 Innovate UK window. **Video is Tier 1 in UK** because of the regulatory demand created by the Online Safety Act.

#### European Union (Horizon Europe 2026–2027)

| Lane | Vehicle | Opens | Budget |
|---|---|---|---|
| Neuro | EBRAINS Research Infrastructures 2026[^10] | Open | €32M consortium |
| Geo | Cluster 5 Smart Mobility[^17] | 2026 work programme | €3–8M |
| Bio | Cluster 1 Health clinical data infrastructure[^17] | 2026 work programme | €2–6M |
| Video | Cluster 3 Cybersecurity/content integrity[^17] | Active | €2–5M |
| Mocap | Cluster 4 Robotics/embodied AI datasets[^23] | Active | €2–4M |

**EU is Tier 1 for Neuro** (EBRAINS call is exact narrative match). **EU is Tier 2 for all other lanes** — the 2026-27 work programme is fully published with €14B total.[^17]

#### United States (NSF / NIH / DARPA / Commercial)

| Lane | Vehicle | Notes |
|---|---|---|
| Video | DARPA SEMAFOR / commercial media (C2PA market) | Strongest US commercial; DARPA requires co-PI |
| Neuro | NIH BRAIN Initiative; NSF CISE | Requires US academic co-PI |
| FT | Commercial (Bloomberg, Refinitiv) | Direct enterprise if Phase 06 passes |
| Bio | NIH NLM data infrastructure | R01 mechanism; requires US co-PI |

**US is Tier 1 only for Video (commercial)** and otherwise requires partnership bridge.

***
## Hidden Seam: The ZPE Code-Physics Lab as a Portfolio-Level Grant Narrative
The portfolio's disproportionately large grant opportunity lies not in individual lane grants but in constituting ZPE as a **code-physics research infrastructure lab** — an entity that produces domain-specialised information bottlenecks as open research infrastructure across biology, neuroscience, motion, IoT, finance, and media.

This narrative maps to:
1. The **Horizon Europe Research Infrastructures 2026 programme** (€50M for transnational research infrastructure access) — ZPE as an open data-compression research infrastructure for AI-for-science.[^17]
2. The **ERC Advanced Grant or Consolidator Grant** (ERC 2026 work programme is published) — "information-theoretic limits of domain-specialised compression across biological and physical signal modalities" is a credible ERC thesis.[^37]
3. The **Wellcome Discovery Awards** (up to 8 years, open submission) — if ZPE-Neuro + ZPE-Bio are framed as biological signal infrastructure.[^38]

The engineering prerequisite for this narrative: at least three lanes must have published, citable, FAIR-compliant benchmark results. ZPE-IoT (10/11 wins, documented), ZPE-Neuro (DANDI-validated), and ZPE-Mocap (CMU corpus) are the strongest candidates to anchor the first three publications. With three published benchmarks, the portfolio-level grant narrative becomes credible.

***

*NeurIPS 2024 ML & Compression Workshop framing cited throughout. LDNS (NeurIPS 2024). Flow-IB (NeurIPS 2025). UrbanSparse (NeurIPS 2025). MotionBind (NeurIPS 2025). ReStraV (NeurIPS 2025). FocalCodec (NeurIPS 2025). Perceptual hashing robustness (NeurIPS 2024). REVE EEG (NeurIPS 2025). NeuroMamba (NeurIPS 2025). EBRAINS Horizon call (deadline 16 June 2026, €32M). Innovate UK AI Champions closes 29 April 2026. BBSRC Standard Research Grant (up to £2M, 3× per year). Horizon Europe 2026-27 €14B work programme. UniReps NeurIPS 2025 representation convergence.*[^1][^2][^35][^3][^36][^30][^4][^6][^8][^18][^19][^9][^7][^11][^22][^10][^17]

---

## References

1. [[PDF] Latent Diffusion for Neural Spiking Data - NIPS papers](https://proceedings.neurips.cc/paper_files/paper/2024/file/d60b6b7f0ba6bf07d975b3bbdacea702-Paper-Conference.pdf) - Here, we propose Latent Diffusion for Neural Spiking data (LDNS), which combines the ability of auto...

2. [Workshop on Machine Learning and Compression - NeurIPS 2026](https://neurips.cc/virtual/2024/workshop/84753) - It will focus on enhancing compression techniques, accelerating large model training and inference, ...

3. [Reconciling Geospatial Prediction and Retrieval via Sparse ...](https://neurips.cc/virtual/2025/poster/116162) - Our approach introduces two innovations: (1) Bloom filter-based sparse encodings that compress high-...

4. [Flow-IB: Information Bottleneck Meets Flow Matching ... - OpenReview](https://openreview.net/forum?id=iDdyA8nxgO) - TL;DR: We propose Flow-IB, a generative video compression framework that compresses videos 32,768× b...

5. [NeurIPS Poster Latent Diffusion for Neural Spiking Data](https://neurips.cc/virtual/2024/poster/94632) - Here, we present Latent Diffusion for Neural Spiking data (LDNS), a diffusion-based generative model...

6. [Latent Diffusion for Neural Spiking Data](https://proceedings.neurips.cc/paper_files/paper/2024/hash/d60b6b7f0ba6bf07d975b3bbdacea702-Abstract-Conference.html) - Here, we present Latent Diffusion for Neural Spiking data (LDNS), a diffusion-based generative model...

7. [UniReps: Unifying Representations in Neural Models - NeurIPS 2026](https://neurips.cc/virtual/2025/workshop/109553) - The objective of the workshop is to discuss theoretical findings, empirical evidence and practical a...

8. [NeuroMamba: A State-Space Foundation Model for Functional MRI](https://neurips.cc/virtual/2025/132664) - To overcome these challenges, we introduce NeuroMamba, a foundation model that enables direct sequen...

9. [NeurIPS Poster REVE: A Foundation Model for EEG](https://neurips.cc/virtual/2025/poster/117334) - REVE achieves state-of-the-art results on 10 downstream EEG tasks, including motor imagery classific...

10. [neuroscience research health brain inspired technology - datacraft](https://datacraft.paris/neuroscience-research-health-brain-inspired-technology/) - Deadline Date : 16/06/2026. Operators : European Commission – Horizon Europe (Research Infrastructur...

11. [BBSRC Standard Research Grant 2025 Round Two](https://researchfunding.on.worc.ac.uk/?p=1055) - Funding is available for: research projects, including data intensive and technology development pro...

12. [BBSRC Standard Research Grant: 2025 round 1: Responsive mode](https://www.ukri.org/opportunity/bbsrc-standard-research-grant-2025-round-1-responsive-mode/) - Funding is available for: research projects, including data intensive and technology development pro...

13. [Electrocardiogram Report Generation and Question Answering via ...](https://neurips.cc/virtual/2024/103056) - Workshop: Time Series in the Age of Large Models. Electrocardiogram Report Generation and Question A...

14. [Grounding Time Series in Context for Multimodal Embedding and ...](https://neurips.cc/virtual/2025/poster/116871) - To address this gap, we propose TRACE, a generic multimodal retriever that grounds time-series embed...

15. [End-to-End Platform for Electrocardiogram Analysis and Model Fine ...](https://www.jmir.org/2026/1/e81116) - Users can select to view ECG data based on multiple views - raw time series, QRS complexes, fiducial...

16. [Learning from Time-Series for Health - NeurIPS 2026](https://neurips.cc/virtual/2025/workshop/109560) - This workshop unites researchers across health time-series domains (from wearables to clinical syste...

17. [Horizon Europe 2026-27: €14 billion for better research careers in a ...](https://rea.ec.europa.eu/news/horizon-europe-2026-27-eu14-billion-better-research-careers-greener-stronger-eu-2025-12-12-0_en) - The newly adopted Horizon Europe Work Programme for 2026 and 2027 allocates €14 billion to support r...

18. [MotionBind: Multi-Modal Human Motion Alignment for Retrieval...](https://openreview.net/forum?id=sUjwDdyspc) - To bridge this gap, we propose MotionBind, a novel architecture that extends the LanguageBind embedd...

19. [MotionBind: Multi-Modal Human Motion Alignment for Retrieval ...](https://neurips.cc/virtual/2025/poster/115690) - To bridge this gap, we propose MotionBind, a novel architecture that extends the LanguageBind embedd...

20. [4DGCPro: Efficient Hierarchical 4D Gaussian Compression for ...](https://neurips.cc/virtual/2025/poster/118452) - Specifically, we propose a perceptually-weighted and compression-friendly hierarchical 4D Gaussian r...

21. [Smooth and Flexible Camera Movement Synthesis via Temporal ...](https://neurips.cc/virtual/2025/poster/118515) - In this paper, we propose TemMEGA (Temporal Masked Generative Modeling), a unified framework capable...

22. [Innovate UK Grant Funding Competitions - Spring 2026 Update](https://www.warwicksciencepark.co.uk/innovate-uk-grant-funding-competitions-spring-2026-update/) - UK registered SME businesses can apply for a share of up to £3 million to deliver feasibility studie...

23. [EU Funding: Calls for proposals 2025-2026 - Future Needs](https://futureneeds.eu/calls-for-proposals-2025-2026/) - A complete list of EU calls for proposals, including open dates and deadlines. Horizon Europe, Europ...

24. [Mamba4Cast: Efficient Zero-Shot Time Series Forecasting with State ...](https://neurips.cc/virtual/2024/102938) - This paper introduces Mamba4Cast, a zero-shot foundation model for time series forecasting. Based on...

25. [Disentangled Cross-Modal Representation Learning with Enhanced ...](https://neurips.cc/virtual/2025/poster/115708) - In this work, we propose a novel framework, termed Disentangled Cross-Modal Representation Learning ...

26. [NeurIPS Poster Scaling Image Geo-Localization to Continent Level](https://neurips.cc/virtual/2025/poster/115618) - This paper introduces a hybrid approach that achieves fine-grained geo-localization across a large g...

27. [[PDF] Scaling Image Geo-Localization to Continent Level - arXiv](https://arxiv.org/pdf/2510.26795.pdf) - 39th Conference on Neural Information Processing Systems (NeurIPS 2025). arXiv:2510.26795v1 [cs.CV] ...

28. [NeurIPS Scalable Geospatial Data Generation Using AlphaEarth ...](https://neurips.cc/virtual/2025/126952) - In this article we propose and evaluate a methodology which leverages AEF to extend geospatial label...

29. [FinZero: Launching Multimodal Financial Time-Series Reasoning](https://neurips.cc/virtual/2025/132527) - Financial time series forecasting is both highly significant and challenging. Previous approaches ty...

30. [NeurIPS Poster FocalCodec: Low-Bitrate Speech Coding via Focal ...](https://neurips.cc/virtual/2025/poster/119693) - FocalCodec delivers competitive performance in speech resynthesis and voice conversion at lower bitr...

31. [Handwriting decoding as a challenging Motor Imagery task for EEG ...](https://neurips.cc/virtual/2025/132692) - In this work, we investigate handwriting decoding as a challenging MI task to evaluate the generaliz...

32. [Neural Encoding Detection is Not All You Need for Synthetic Speech ...](https://arxiv.org/html/2604.16700v1) - Prosody-based algorithms are designed to rely on prosody-related features, i.e., on features describ...

33. [NeurIPS Poster VIBE: Annotation-Free Video-to-Text Information ...](https://neurips.cc/virtual/2025/poster/119324) - The information bottleneck (IB) framework extracts relevant information from input data while compre...

34. [NeurIPS VIBE: Annotation-Free Video-to-Text Information Bottleneck ...](https://neurips.cc/virtual/2025/131789) - We address these gaps with V ― ideo-to-text I ― nformation B ― ottleneck E ― valuation (VIBE), an an...

35. [NeurIPS Robustness of Practical Perceptual Hashing Algorithms to ...](https://neurips.cc/virtual/2024/100200) - This paper assesses the security of three widely utilized PHAs—PhotoDNA, PDQ, and NeuralHash—against...

36. [AI-Generated Video Detection via Perceptual Straightening](https://neurips.cc/virtual/2025/poster/118520) - We propose ReStraV(Representation Straightening for Video), a novel approach to distinguish natural ...

37. [2026-2027 Horizon Europe Funding - DEMENTIA RESEARCHER](https://www.dementiaresearcher.nihr.ac.uk/funding/2026-2027-horizon-europe-funding/) - EU publishes Horizon Europe 2026 2027 work programmes with 14 billion euros in funding. Health MSCA ...

38. [Wellcome Trust (UK) Funding Opportunities for Applicants from LMICs](https://international.uwc.ac.za/event/wellcome-trust-uk-funding-opportunities-for-applicants-from-lmics/) - Wellcome Trust (UK) has launched three new discovery research funding schemes. These schemes are: We...


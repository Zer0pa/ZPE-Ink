# ZPE-Ink Novelty Card

**Product:** ZPE-Ink
**Domain:** Deterministic digital-ink stroke transport and tokenization for pen-stream data.
**What we sell:** Cross-runtime ink interchange with bounded transport compression and proof-backed packet determinism.

## Novel contributions

1. **`.zpink` deterministic packet contract** — ZPE-Ink defines a concrete packet envelope for stroke arrays with mandatory pressure, optional tilt and azimuth channels, explicit mode codes, a determinism seed, and payload CRC checks. The core novelty candidate is not delta coding by itself; it is the productized contract that keeps multi-channel ink transport stable across the repo's runtime surfaces. Code: [`code/zpe_ink/codec.py:8`](../../../../code/zpe_ink/codec.py#L8), [`code/zpe_ink/codec.py:181`](../../../../code/zpe_ink/codec.py#L181). Nearest prior art (if known): generic delta-coded stroke formats and packetized binary interchange formats. What is genuinely new here: the specific ZPE-Ink packet schema and compatibility surface for deterministic multi-channel pen data.
2. **Automatic zero-channel suppression for optional ink channels** — ZPE-Ink detects when tilt or azimuth are entirely zero across a stroke set and removes those channels from the encoded payload unless the caller explicitly asks otherwise. It also rejects user-forced suppression when real non-zero data is present. Code: [`code/zpe_ink/codec.py:160`](../../../../code/zpe_ink/codec.py#L160), [`code/zpe_ink/codec.py:204`](../../../../code/zpe_ink/codec.py#L204). Nearest prior art (if known): optional-field elision in binary codecs. What is genuinely new here: the product-specific decision rule tied to ZPE-Ink's ink-channel semantics and proof-backed compression gap closure.
3. **8-direction tokenizer lane with retained side channels** — Separate from the sovereign transport claim, ZPE-Ink includes a tokenizer lane that maps stroke motion into 8-direction tokens, packs them as nibbles, and reconstructs the path alongside retained pressure, tilt, and azimuth side channels. Code: [`code/zpe_ink/primitivetoken.py:15`](../../../../code/zpe_ink/primitivetoken.py#L15), [`code/zpe_ink/primitivetoken.py:142`](../../../../code/zpe_ink/primitivetoken.py#L142), [`code/zpe_ink/primitivetoken.py:190`](../../../../code/zpe_ink/primitivetoken.py#L190). Nearest prior art (if known): Freeman chain codes and related directional stroke tokenizers. What is genuinely new here: the integration of directional token packing with ZPE-Ink's retained side-channel reconstruction contract.

## Standard techniques used (explicit, not novel)

- Zigzag varints
- Delta plus run-length encoding
- CRC32 payload checks
- Integer quantization tiers
- Freeman-style directional tokenization

## Compass-8 / 8-primitive architecture

YES — but only in the tokenizer lane, not as the sovereign transport claim. See [`code/zpe_ink/primitivetoken.py:15`](../../../../code/zpe_ink/primitivetoken.py#L15), [`code/zpe_ink/primitivetoken.py:142`](../../../../code/zpe_ink/primitivetoken.py#L142), and [`code/zpe_ink/primitivetoken.py:190`](../../../../code/zpe_ink/primitivetoken.py#L190). The core transport claim instead lives in [`code/zpe_ink/codec.py:181`](../../../../code/zpe_ink/codec.py#L181).

## Open novelty questions for the license agent

- Does the tokenizer lane's Freeman-derived directional encoding count as protectable novelty only at the integrated side-channel reconstruction layer, rather than at the directional-token idea itself?
- Should automatic zero-channel suppression be scheduled as per-product novelty, or treated as an implementation optimization around otherwise standard optional-field elision?

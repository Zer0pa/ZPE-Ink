from __future__ import annotations

from zpe_ink.codec import encode_zpink
from zpe_ink.fixtures import generate_adversarial_spike_set, generate_synthetic_lossless
from zpe_ink.metrics import corpus_hausdorff
from zpe_ink.token_sidecar import build_token_sidecar, build_token_sidecar_from_zpink, reconstruct_token_sidecar


def test_token_sidecar_from_zpink_is_deterministic() -> None:
    strokes = generate_synthetic_lossless(seed=20260424)[:8]
    payload = encode_zpink(strokes, mode="lossless", seed=20260424)
    first = build_token_sidecar_from_zpink(payload)
    second = build_token_sidecar_from_zpink(payload)
    assert first == second
    assert first["candidate_status"] == "CANDIDATE_ONLY"
    assert first["source_format"] == ".zpink"
    assert first["source_metadata"]["seed"] == 20260424


def test_token_sidecar_reconstructs_directional_fixture_exactly() -> None:
    strokes = generate_synthetic_lossless(seed=20260424)[:8]
    sidecar = build_token_sidecar(strokes, source_format="fixture")
    reconstructed = reconstruct_token_sidecar(sidecar)
    assert reconstructed == strokes
    assert corpus_hausdorff(strokes, reconstructed) == 0.0


def test_token_sidecar_keeps_adversarial_surface_candidate_only() -> None:
    strokes = generate_adversarial_spike_set(seed=20260424)[:4]
    sidecar = build_token_sidecar(strokes, source_format="fixture")
    reconstructed = reconstruct_token_sidecar(sidecar)
    assert corpus_hausdorff(strokes, reconstructed) > 0.0
    assert sidecar["runtime_authority"].startswith(".zpink remains sovereign")

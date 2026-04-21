from __future__ import annotations

from zpe_ink.phase2_authority import (
    build_claim_scope_map,
    build_contradiction_manifest,
    raw_float32_xy_payload,
)


def test_raw_float32_xy_payload_uses_only_xy_coordinates() -> None:
    sample = [
        {
            "x": [1, 2],
            "y": [3, 4],
            "pressure": [100, 200],
            "tilt": [5, 6],
            "azimuth": [7, 8],
        }
    ]

    payload = raw_float32_xy_payload(sample)

    assert len(payload) == 16


def test_build_claim_scope_map_blocks_broad_claims_for_weak_hard_corpus() -> None:
    scope = build_claim_scope_map(
        structured_ratio=5.59,
        structured_threshold=5.0,
        structured_comparator_ratios={"brotli": 6.82, "zstd": 4.91, "lz4": 1.99},
        hard_ratios={"mathwriting": 1.09, "crohme": 1.30},
        transport_gates_pass=True,
        license_text="LicenseRef-Zer0pa-SAL-7.0",
        sovereign_release_verdict="FAIL",
        contradiction_status="OPEN",
    )

    assert scope["authority_surface"]["current_scope"] == "structured-tier-only"
    assert scope["authority_surface"]["engineering_comparator_verdict"] == "FAIL"
    assert scope["authority_surface"]["broad_claim_verdict"] == "FAIL"
    assert any("Broad handwriting-compression superiority" in item for item in scope["blocked_claims"])


def test_build_contradiction_manifest_preserves_release_fail() -> None:
    manifest = build_contradiction_manifest(
        scorecard_pass=True,
        appendix_all_pass=False,
        handoff_go_no_go="NO-GO",
        release_report_verdict="INCONCLUSIVE",
        failing_gates={
            "E-G3_cross_script_required": {
                "evidence": "cross_script_generalization_report.json",
                "note": "Cross-script corpus not yet executed.",
            }
        },
        remaining_blockers=[
            {
                "id": "BLK-UNIPEN-ACCESS",
                "reason_code": "IMP-ACCESS",
                "note": "UNIPEN acquisition remained impossible after three concrete attempts.",
                "evidence": "impracticality_decisions.json",
            }
        ],
        free_disk_gib=4.5,
        adb_available=True,
        adb_devices=[],
    )

    assert manifest["authority_state"]["overall_current_verdict"] == "INCONCLUSIVE"
    assert manifest["resolution_state"]["sovereign_release_verdict"] == "FAIL"
    assert any(blocker["id"] == "BLK-FZ09-SURFACE-MISMATCH" for blocker in manifest["blockers"])

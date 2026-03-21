from __future__ import annotations

import struct
from typing import Any


Stroke = dict[str, list[int]]
Sample = list[Stroke]


def raw_float32_xy_payload(sample: Sample) -> bytes:
    payload = bytearray()
    for stroke in sample:
        x_vals = stroke["x"]
        y_vals = stroke["y"]
        if len(x_vals) != len(y_vals):
            raise ValueError("x/y channel length mismatch")
        for x_val, y_val in zip(x_vals, y_vals):
            payload.extend(struct.pack("<ff", float(x_val), float(y_val)))
    return bytes(payload)


def classify_blocker(reason_code: str, note: str) -> str:
    if reason_code in {"IMP-ACCESS", "IMP-LICENSE", "IMP-COMPUTE"}:
        return "external-access dependency"
    if reason_code == "IMP-NOCODE":
        return "not-viable path"
    if reason_code == "FAIL" and "scope" in note.lower():
        return "claim-scope issue"
    if reason_code == "FAIL" and "artifact" in note.lower():
        return "missing artifact"
    return "external-access dependency" if "unipen" in note.lower() else "claim-scope issue"


def build_contradiction_manifest(
    *,
    scorecard_pass: bool,
    appendix_all_pass: bool,
    handoff_go_no_go: str,
    release_report_verdict: str,
    failing_gates: dict[str, dict[str, Any]],
    remaining_blockers: list[dict[str, Any]],
    free_disk_gib: float,
    adb_available: bool,
    adb_devices: list[str],
) -> dict[str, Any]:
    sovereign_release_verdict = "PASS" if handoff_go_no_go == "GO" else "FAIL"
    overall_current_verdict = (
        "INCONCLUSIVE" if scorecard_pass and sovereign_release_verdict == "FAIL" else sovereign_release_verdict
    )

    root_causes = [
        "The internal quality scorecard can pass without appendix D/E closure.",
        "The release handoff remains NO-GO until appendix D/E gates pass as well as the core transport surface.",
    ]
    if failing_gates:
        root_causes.append(
            "Current failing release gates: " + ", ".join(sorted(failing_gates))
        )

    blockers = [
        {
            "id": "BLK-FZ09-SURFACE-MISMATCH",
            "class": "claim-scope issue",
            "verdict": "FAIL",
            "note": "Internal quality PASS and sovereign release NO-GO coexist because they are different gate surfaces.",
            "evidence": [
                "quality_gate_scorecard.json",
                "handoff_manifest.json",
                "generate_handoff.py",
                "INK_WAVE1_RELEASE_READINESS_REPORT.md",
            ],
        }
    ]

    for blocker in remaining_blockers:
        note = blocker.get("note", "")
        reason_code = blocker.get("reason_code", "")
        verdict = "PAUSED_EXTERNAL" if reason_code.startswith("IMP-") else "FAIL"
        blockers.append(
            {
                "id": blocker.get("id", "UNKNOWN"),
                "class": classify_blocker(reason_code, note),
                "verdict": verdict,
                "note": note,
                "evidence": [blocker.get("evidence")] if blocker.get("evidence") else [],
            }
        )

    if "E-G3_cross_script_required" in failing_gates:
        blockers.append(
            {
                "id": "BLK-CROSS-SCRIPT-NON_LATIN",
                "class": "external-access dependency",
                "verdict": "PAUSED_EXTERNAL",
                "note": "A real non-Latin online-stroke corpus has not yet been executed in-lane.",
                "evidence": ["cross_script_generalization_report.json", "net_new_gap_closure_matrix.json"],
            }
        )

    failing_release_gates = []
    for gate_id, gate in sorted(failing_gates.items()):
        linked_blockers = []
        if gate_id == "M1_real_iam_unipen_non_inferior":
            linked_blockers = ["BLK-M1-REAL-IAM-UNIPEN", "BLK-UNIPEN-ACCESS"]
        elif gate_id == "E-G3_cross_script_required":
            linked_blockers = ["BLK-CROSS-SCRIPT-NON_LATIN"]
        failing_release_gates.append(
            {
                "id": gate_id,
                "verdict": "FAIL",
                "note": gate.get("note", ""),
                "evidence": gate.get("evidence"),
                "linked_blockers": linked_blockers,
            }
        )

    return {
        "schema_version": 1,
        "authority_state": {
            "quality_surface_verdict": "PASS" if scorecard_pass else "FAIL",
            "release_go_no_go": handoff_go_no_go,
            "release_surface_verdict": sovereign_release_verdict,
            "release_report_verdict": release_report_verdict,
            "appendix_all_pass": appendix_all_pass,
            "overall_current_verdict": overall_current_verdict,
        },
        "resolution_state": {
            "classification_status": "CLASSIFIED_LOCAL",
            "contradiction_status": "OPEN" if overall_current_verdict == "INCONCLUSIVE" else "CLOSED",
            "sovereign_gate": "handoff_manifest.go_no_go",
            "sovereign_release_verdict": sovereign_release_verdict,
        },
        "root_cause_assessment": root_causes,
        "failing_release_gates": failing_release_gates,
        "blockers": blockers,
        "boundary": {
            "lane": "M1-local",
            "free_disk_gib": round(free_disk_gib, 3),
            "adb_available": adb_available,
            "attached_adb_devices": adb_devices,
        },
    }


def build_claim_scope_map(
    *,
    structured_ratio: float,
    structured_threshold: float,
    structured_comparator_ratios: dict[str, float],
    hard_ratios: dict[str, float],
    transport_gates_pass: bool,
    license_text: str,
    sovereign_release_verdict: str,
    contradiction_status: str,
) -> dict[str, Any]:
    structured_verdict = "PASS" if transport_gates_pass and structured_ratio >= structured_threshold else "FAIL"
    hard_corpus_verdict = "PASS" if hard_ratios and all(r >= structured_threshold for r in hard_ratios.values()) else "FAIL"
    engineering_comparator_verdict = (
        "PASS"
        if structured_comparator_ratios and all(structured_ratio > ratio for ratio in structured_comparator_ratios.values())
        else "FAIL"
    )
    broad_claim_verdict = (
        "PASS"
        if structured_verdict == "PASS"
        and hard_corpus_verdict == "PASS"
        and engineering_comparator_verdict == "PASS"
        and sovereign_release_verdict == "PASS"
        and contradiction_status == "CLOSED"
        else "FAIL"
    )

    allowed_claims = []
    if structured_verdict == "PASS":
        allowed_claims.append(
            "The current transport kernel remains above 5x on the structured tier against the raw float32 baseline."
        )
        allowed_claims.append(
            "Transport quality and runtime parity remain locally credible and separate from hard-corpus authority."
        )

    blocked_claims = [
        "Broad handwriting-compression superiority across public hard corpora.",
        "Superiority over all frozen engineering comparators on the structured tier.",
        "Release-ready or enterprise-ready language while the sovereign release surface remains non-pass.",
        "Any claim that treats structured-tier success as direct IAM/UNIPEN or non-Latin closure.",
    ]
    if hard_corpus_verdict == "PASS" and broad_claim_verdict == "PASS":
        blocked_claims = blocked_claims[1:]

    return {
        "schema_version": 1,
        "authority_surface": {
            "current_scope": "structured-tier-only" if structured_verdict == "PASS" else "not-yet-authorized",
            "structured_tier_verdict": structured_verdict,
            "hard_corpus_verdict": hard_corpus_verdict,
            "engineering_comparator_verdict": engineering_comparator_verdict,
            "broad_claim_verdict": broad_claim_verdict,
            "transport_gates_verdict": "PASS" if transport_gates_pass else "FAIL",
            "sovereign_release_verdict": sovereign_release_verdict,
            "contradiction_status": contradiction_status,
            "license_surface": license_text,
        },
        "thresholds": {
            "structured_ratio_min": structured_threshold,
        },
        "ratios": {
            "structured_tier": structured_ratio,
            "structured_engineering_comparators": structured_comparator_ratios,
            "hard_corpus": hard_ratios,
        },
        "allowed_claims": allowed_claims,
        "blocked_claims": blocked_claims,
        "next_boundary_requirements": [
            "Direct IAM/UNIPEN closure or an explicit decision to leave that surface outside the current claim family.",
            "A real non-Latin online-stroke corpus if cross-script authority is still required.",
            "Blind-clone or external-host verification before any release or public-readiness claim.",
        ],
    }

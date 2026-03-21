from __future__ import annotations

from pathlib import Path

from zpe_ink.binding_contracts import verify_repo_binding_contracts


def test_repo_binding_contracts_pass() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    report = verify_repo_binding_contracts(repo_root)
    assert report["status"] == "PASS"
    assert report["failure_count"] == 0
    assert len(report["checks"]) >= 10

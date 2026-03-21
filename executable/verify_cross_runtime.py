from __future__ import annotations

import json
import sys
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1] / "code"
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from zpe_ink.binding_contracts import verify_repo_binding_contracts


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    proof_root = repo_root / "proofs" / "curated_artifacts" / "2026-02-20_zpe_ink_wave1"
    contract_path = proof_root / "integration_readiness_contract.json"
    parity_path = proof_root / "ink_cross_runtime_parity.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8")) if contract_path.exists() else {}
    parity = json.loads(parity_path.read_text(encoding="utf-8")) if parity_path.exists() else {}
    binding_report = verify_repo_binding_contracts(repo_root)
    payload = {
        "adapter_statuses": contract.get("adapters", {}),
        "binding_contract_status": binding_report["status"],
        "binding_failure_count": binding_report["failure_count"],
        "parity_keys": sorted(parity.keys()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if binding_report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    proof_root = Path(__file__).resolve().parents[1] / "proofs" / "curated_artifacts" / "2026-02-20_zpe_ink_wave1"
    contract_path = proof_root / "integration_readiness_contract.json"
    parity_path = proof_root / "ink_cross_runtime_parity.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    parity = json.loads(parity_path.read_text(encoding="utf-8"))
    payload = {
        "adapter_statuses": contract.get("adapters", {}),
        "parity_keys": sorted(parity.keys()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

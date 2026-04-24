# ZPE-Ink Recovery Custody Snapshot

This folder preserves small lane-planning and status artifacts that were local to the Mac outside the product repo.

The product source, docs, and committed proof files are recoverable from GitHub branch `codex/zpe-ink-custody-2026-04-24`.

Included here:

- `gpd/`: ZPE-Ink GPD project state and phase artifacts, including `state.json.bak`.
- `hf/`: Hugging Face custody manifest with the verified dataset repo, bucket, RunPod salvage path, and checksum.
- `portfolio_surface/`: local portfolio-page source/render for ZPE-Ink.
- `source_materials/`: lane handover/PRD source docs, ZPE-Ink augmentation brief, shared augmentation research, and governance/playbook inputs used to produce the PRD/readiness plan.
- `startup_prompts/`: deletion/reclone startup prompt for the next ZPE-Ink agent.
- `status_packets/augmentation_prd_readiness/`: augmentation PRD, runbooks, GPD execution plan, and readiness report.
- `status_packets/historical_2026-04-17/`: earlier lane assessment and verification packet.
- `status_packets/ZPE-Ink_HF_CUSTODY_REPORT.md`: prior HF custody lane report.
- `status_packets/ZPE-Ink_HARDENING_AUDIT.md`: reproducibility/PyPI audit card.
- `status_packets/ZPE-Ink_LICENSE_IDENTITY_AUDIT.md`: license identity audit card.
- `status_packets/ZPE-Ink_LICENSE_IDENTITY_EXECUTION.md`: license identity execution card.

Hugging Face note: the working HF path requires preserving `HF_HOME` while removing the overriding environment tokens for HF commands:

```bash
env -u HF_TOKEN -u HUGGINGFACE_HUB_TOKEN HF_HOME="$HF_HOME" hf auth whoami
```

Verified HF targets:

- `https://huggingface.co/datasets/Zer0pa/ZPE-Ink-artifacts`
- `hf://buckets/Zer0pa/ZPE-Ink-scratch`

The RunPod historical salvage tarball is uploaded to both targets and documented in `hf/HF_CUSTODY_MANIFEST.md`.

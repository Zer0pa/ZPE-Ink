# ZPE-Ink Recovery Custody Snapshot

This folder preserves small lane-planning and status artifacts that were local to the Mac outside the product repo.

The product source, docs, and committed proof files are recoverable from GitHub branch `codex/zpe-ink-custody-2026-04-24`.

Included here:

- `gpd/`: ZPE-Ink GPD project state and phase artifacts, excluding `state.json.bak`.
- `source_materials/`: lane handover/PRD source docs, ZPE-Ink augmentation brief, shared augmentation research, and governance/playbook inputs used to produce the PRD/readiness plan.
- `startup_prompts/`: deletion/reclone startup prompt for the next ZPE-Ink agent.
- `status_packets/augmentation_prd_readiness/`: augmentation PRD, runbooks, GPD execution plan, and readiness report.
- `status_packets/ZPE-Ink_HF_CUSTODY_REPORT.md`: prior HF custody lane report.
- `status_packets/ZPE-Ink_HARDENING_AUDIT.md`: reproducibility/PyPI audit card.
- `status_packets/ZPE-Ink_LICENSE_IDENTITY_AUDIT.md`: license identity audit card.
- `status_packets/ZPE-Ink_LICENSE_IDENTITY_EXECUTION.md`: license identity execution card.

Hugging Face note: this pass attempted to create `Zer0pa/ZPE-Ink-artifacts`, but the normalized `hf auth whoami` state failed before any successful HF write. No HF-required large model, dataset, validation corpus, or checkpoint artifact was found locally for this lane. Small recovery artifacts are therefore committed to GitHub in this custody branch.

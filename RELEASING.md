# Releasing

This repo follows a private-first release path.

Current rule:

- no public release action until Phase 5 verification is complete on the exact commit being considered

Minimum release sequence:

1. private staging push
2. inspector review on the pushed commit
3. contradiction reconciliation and required fixes
4. explicit operator approval
5. only then consider public release

Current blocker:

- the repo still carries a real contradiction between the primary quality scorecard and the handoff `NO-GO` verdict

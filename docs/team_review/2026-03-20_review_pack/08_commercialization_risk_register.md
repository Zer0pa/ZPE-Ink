# Commercialization Risk Register

| Resource | Constraint | Status | Commercial-Safe Alternative | Affected Claims | Evidence |
|---|---|---|---|---|---|
| IAM On-Line | Restricted/uncertain | PAUSED_EXTERNAL | MathWriting + UCI Pen Digits | INK-C001, INK-C002, INK-C006 | `commercial_corpus_parity.json` |
| UNIPEN | Access blocked after 3 acquisition attempts + containerized retry | PAUSED_EXTERNAL | UCI Pen Digits | INK-C001, INK-C002, INK-C006 | `commercial_corpus_parity.json`; `command_log.txt` |
| Muharaf | Raster-only public drop after 3 acquisition attempts (online-stroke parity unproven) | PAUSED_EXTERNAL | No equivalent online-stroke commercial-safe corpus proven | INK-C001, INK-C002, INK-C005 | `impracticality_decisions.json`; `command_log.txt` |
| OpenRing traces | No claim-equivalent wearable stroke traces published | PAUSED_EXTERNAL | No equivalent commercial-safe ring-stroke corpus proven | INK-C003, INK-C004 | `max_resource_validation_log.md` |
| iOS PencilKit device-level path | Developer tools/device path unavailable on host after local + containerized attempts | PAUSED_EXTERNAL | None (requires Apple device-lab hardware) | Adapter validation track | `command_log.txt` |

Commercial-safe primary corpora executed: MathWriting and UCI Pen Digits.

# Falsification Results

## DT-INK-1
- PASS: True
- total_cases: 4
- caught_cases: 4
- uncaught_cases: []
- uncaught_crash_rate_percent: 0.0

## DT-INK-2
- PASS: True
- stroke_count: 24
- max_pressure_diff: 0
- max_tilt_diff: 0

## DT-INK-3
- PASS: True
- runs: 5
- unique_hashes: 1
- hashes: ["9533f8bc03681d8c73cb449cfa39a2dd985dedf071c612e00c56e304db5d8bef", "9533f8bc03681d8c73cb449cfa39a2dd985dedf071c612e00c56e304db5d8bef", "9533f8bc03681d8c73cb449cfa39a2dd985dedf071c612e00c56e304db5d8bef", "9533f8bc03681d8c73cb449cfa39a2dd985dedf071c612e00c56e304db5d8bef", "9533f8bc03681d8c73cb449cfa39a2dd985dedf071c612e00c56e304db5d8bef"]

## DT-INK-4
- PASS: True
- points: 1800
- max_xy_diff: 0

## DT-INK-5
- PASS: True
- stroke_count: 2400
- decoded_stroke_count: 2400
- peak_memory_mb: 181.5091209411621
- memory_ceiling_mb: 256.0

## Substitution Notes
- If IAM/UNIPEN direct downloads were unavailable, deterministic proxy corpora were used.
- If InkML.js package resolution failed, equivalent local XML parser path remained as fallback.
- Claims impacted by non-equivalent substitutions remain PAUSED_EXTERNAL or FAIL in traceability outputs.

## Appendix D Maximalization Kill Tests
- pressure_noisy_failures: 0
- long_sequence_stroke_count: 12000
- long_sequence_latency_ms_per_stroke: 0.562160
- long_sequence_uncaught_crash_rate_percent: 0.0
- csharp_managed_runtime_probe: {"compiled": true, "executed": true, "stdout": "version=1,mode=0,flags=7,strokes=16", "stderr": "", "returncode": 0}

## Appendix D Maximalization Kill Tests
- pressure_noisy_failures: 0
- long_sequence_stroke_count: 12000
- long_sequence_latency_ms_per_stroke: 1.295519
- long_sequence_uncaught_crash_rate_percent: 0.0
- csharp_managed_runtime_probe: {"compiled": true, "executed": true, "stdout": "version=1,mode=0,flags=7,strokes=16", "stderr": "", "returncode": 0}

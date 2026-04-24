# Phase 04-01 Summary

Plan `04-01` implemented a candidate-only primitive-token runtime branch and benchmarked it against the frozen sovereign surface in [primitivetoken_benchmark.json](/Users/Zer0pa/ZPE/ZPE%20Ink/ZPE-Ink/proofs/reruns/primitive_token_branch/primitivetoken_benchmark.json). The structured-tier result is materially stronger than both the frozen sovereign runtime and frozen `brotli`: `primitive_zstd=12.377589251348581x`, `sovereign=5.590209480060199x`, `brotli=6.825565026256283x`.

That improvement does not justify promotion. The bounded Calliar slice also improved on ratio, `2.883090351936113x` versus `2.7329382078516518x` for `brotli`, but the fidelity cost is disqualifying: mean Hausdorff `201.11119574321816 px`, max `636.5736406732532 px`. The branch therefore remains `CANDIDATE_ONLY` and does not mutate the frozen claim-scope or sovereign runtime surface.

# MathWriting Gap Analysis

| Corpus | Before | After | Delta |
|---|---:|---:|---:|
| MathWriting mean ratio | 1.0552x | 1.1496x | +0.0943x |
| CROHME mean ratio | 1.5198x | 1.7635x | +0.2436x |

Finding: the hardest MathWriting cases are short, multi-stroke samples where zero tilt/azimuth streams add fixed overhead.
Action: auto-suppress zero optional channels by default, while raising on explicit lossy suppression of non-zero data.

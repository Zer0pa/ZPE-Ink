# Contributing

Contributions are evidence-first.

Rules:

- claims require artifacts or reproducible command output
- negative findings are valid contributions
- do not suppress contradictory evidence
- keep scope tight and sector-specific

Recommended local setup:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./code
python -m pytest code/tests -q
```

If you touch codec behavior, tests, or proof generation, attach one of:

- before/after metrics
- a falsification artifact
- a claim-status delta
- exact failing command output

Do not open a PR that inflates the repo beyond current evidence. The current repo state is a private staging snapshot, not a public-release claim surface.

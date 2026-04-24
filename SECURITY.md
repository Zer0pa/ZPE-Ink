# Security Policy

## Supported Scope

This repository accepts security reports for:

1. Python package runtime and CLI under `code/zpe_ink`.
2. Repo-local Rust/PyO3, WASM, Swift, and C# binding surfaces under `code/bindings`.
3. CI, release, packaging, and proof-artifact handling that could compromise repository integrity.

Normal codec bugs, benchmark disputes, evidence disputes, and claim-boundary arguments are not security issues. Use standard issues for those and include artifact-backed reproduction.

## Reporting

Do not open a public issue for a security vulnerability.

Report privately through GitHub Private Vulnerability Reporting or by email to `architects@zer0pa.ai`.

Include:

1. Affected component.
2. Reproduction steps or proof of concept.
3. Impact and severity.
4. Affected versions or commit ranges.
5. Suggested remediation when available.

## Response Targets

| Stage | Target timeframe |
|---|---|
| Acknowledgement | within 5 business days |
| Initial assessment | within 10 business days |
| Remediation or mitigation plan | shared after triage |
| Public disclosure | coordinated after a fix or mitigation is available |

Good-faith security research that follows this policy will be handled through coordinated disclosure.

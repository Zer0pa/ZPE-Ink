# ZPE-Ink Hugging Face Custody Manifest - 2026-04-24

## Auth Resolution

The initial HF failure was caused by the active environment token overriding the installed `Zer0pa HF Storage` token.

Use this command shape for ZPE-Ink HF custody commands on this Mac:

```bash
env -u HF_TOKEN -u HUGGINGFACE_HUB_TOKEN HF_HOME="$HF_HOME" hf auth whoami
```

Verified result:

```text
user=Architect-Prime orgs=Zer0pa
```

Do not print tokens. Do not run `hf auth token`.

## Live HF Targets

- Dataset/artifact repo: `https://huggingface.co/datasets/Zer0pa/ZPE-Ink-artifacts`
- Scratch bucket: `hf://buckets/Zer0pa/ZPE-Ink-scratch`
- Model repo: not created; no ZPE-Ink model weights/checkpoints/adapters were found.

## Uploaded RunPod Salvage

Source:

```text
RunPod pod: 7k3riasglemecu
Remote host observed: b7fb18eddf65
Remote source path: /workspace/ZPE-Cipher/workspace/repos/ZPE-Ink
```

Artifact:

```text
Local temporary tarball: /tmp/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz
Size at upload: 5.2M
SHA256: b716cd9975c74dd36cbeb01f15d834e2469b6a9b0f9fd6d3d8d7a9abda473ad7
```

HF dataset copy:

```text
Repo: Zer0pa/ZPE-Ink-artifacts
Path: runpod_salvage/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz
Commit: https://huggingface.co/datasets/Zer0pa/ZPE-Ink-artifacts/commit/38833a49611b8a2398399579647fa4ce3e5065bf
```

HF bucket copy:

```text
hf://buckets/Zer0pa/ZPE-Ink-scratch/runpod_salvage/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz
```

## Local Scan Result

The product repo scan found no files larger than 10 MB and no ignored/untracked local-only value after custody commits. The RunPod snapshot above was the only non-GitHub lane-specific remote artifact found during the correction pass.

## Recovery Rule

For code/docs/small proof work, recover from GitHub branch `codex/zpe-ink-custody-2026-04-24` and PR #21.

For RunPod historical salvage, recover from either HF path above. Prefer the dataset repo copy for auditability and the bucket copy for scratch/salvage parity.

# ZPE-Ink HF Custody Report

## Agent State
- Agent/thread: Codex ZPE-Ink lane custody correction
- Lane/repo: ZPE-Ink
- Local repo path: `/Users/Zer0pa/ZPE/ZPE Ink/ZPE-Ink`
- Current command in progress, if any: none
- Stopped cleanly: yes

## GitHub State
- GitHub remote: `https://github.com/Zer0pa/ZPE-Ink.git`
- Branch/status: `codex/zpe-ink-custody-2026-04-24` tracking `origin/codex/zpe-ink-custody-2026-04-24`; PR #21 open against `chore/novelty-card-backfill-2026-04-22`
- Did you mutate GitHub? yes
- If yes, exactly what changed: committed and pushed custody branch updates preserving local source/docs/tests, ignored proof reruns, GPD/status/source-material snapshots, historical status packets, portfolio surface snapshot, HF manifest, and startup prompt. The custody branch contains the HF salvage/context commit `628e897b69507525f3b6e39ddfb351616f0ec1b9` and later report-refresh commits; verify the current head with `git ls-remote --heads origin codex/zpe-ink-custody-2026-04-24`.
- Uncommitted/unpushed local code/docs/small-proof risk: none identified in the product repo; worktree clean and ignored/untracked value scan empty.

## Hugging Face Auth
- `hf auth whoami` result: `user=Architect-Prime orgs=Zer0pa` when run as `env -u HF_TOKEN -u HUGGINGFACE_HUB_TOKEN HF_HOME="$HF_HOME" hf auth whoami`
- Did you run `hf auth login`? no
- Did you print or expose a token? no

## Hugging Face Storage Created Or Reused
- Dataset repos: `https://huggingface.co/datasets/Zer0pa/ZPE-Ink-artifacts` private, verified live
- Model repos: none; no model weights/checkpoints/adapters found
- Buckets: `hf://buckets/Zer0pa/ZPE-Ink-scratch`, verified live

## Uploads Completed
| Local Path | HF Target | Type | Command Used | Completed yes/no | Notes |
|---|---|---|---|---|---|
| `/tmp/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz` | `Zer0pa/ZPE-Ink-artifacts/runpod_salvage/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz` | RunPod salvage dataset artifact | `env -u HF_TOKEN -u HUGGINGFACE_HUB_TOKEN HF_HOME="$HF_HOME" hf upload Zer0pa/ZPE-Ink-artifacts /tmp/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz runpod_salvage/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz --type dataset --commit-message "custody: upload zpe-ink runpod salvage"` | yes | Dataset commit `38833a49611b8a2398399579647fa4ce3e5065bf`; sha256 `b716cd9975c74dd36cbeb01f15d834e2469b6a9b0f9fd6d3d8d7a9abda473ad7` |
| `/tmp/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz` | `hf://buckets/Zer0pa/ZPE-Ink-scratch/runpod_salvage/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz` | RunPod salvage bucket object | `env -u HF_TOKEN -u HUGGINGFACE_HUB_TOKEN HF_HOME="$HF_HOME" hf buckets cp /tmp/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz hf://buckets/Zer0pa/ZPE-Ink-scratch/runpod_salvage/ZPE-Ink_runpod_ZPE-Cipher_2026-04-24.tar.gz` | yes | Bucket list verified object size `5498701` |
| `docs/custody/2026-04-24/hf/HF_CUSTODY_MANIFEST.md` | `Zer0pa/ZPE-Ink-artifacts/manifests/HF_CUSTODY_MANIFEST.md` | Custody manifest | `env -u HF_TOKEN -u HUGGINGFACE_HUB_TOKEN HF_HOME="$HF_HOME" hf upload Zer0pa/ZPE-Ink-artifacts docs/custody/2026-04-24/hf/HF_CUSTODY_MANIFEST.md manifests/HF_CUSTODY_MANIFEST.md --type dataset --commit-message "custody: refresh zpe-ink hf manifest"` | yes | Dataset commit `2550b9996586d40362cd72b83c22176d5f4db5d0` |

## Uploads Started But Not Confirmed
| Local Path | HF Target | Type | Last Observed State | Risk |
|---|---|---|---|---|
| none | none | none | none | none |

## Excluded Material
- Secrets/env/keys/tokens: excluded; no tokens printed
- Build/cache/generated junk: Rust `target`, wasm `pkg`, `dist`, pytest/cache/egg-info/pycache, temp tarball after upload
- Dependency folders: `.venv`, `node_modules`, build outputs
- Other exclusions: no model repo created because no model-class artifact exists for this lane

## RunPod Dependency
- RunPod access required: no; access was used and the discovered ZPE-Ink snapshot was salvaged
- Pod name/id if known: `7k3riasglemecu`; observed host `b7fb18eddf65`
- Remote paths needed: `/workspace/ZPE-Cipher/workspace/repos/ZPE-Ink`, now captured in HF
- Why needed: this was a non-Git RunPod ZPE-Ink tree not present as a normal Git remote checkout

## Remaining Machine-Loss Risk
List anything valuable that is still only on:
- Mac: none identified for ZPE-Ink after GitHub branch/PR #21 and HF uploads
- RunPod: none identified after uploading `/workspace/ZPE-Cipher/workspace/repos/ZPE-Ink`
- unknown location: none identified

## Next Required Action
COMPLETE

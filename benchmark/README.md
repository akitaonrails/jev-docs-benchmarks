# Decision-model benchmark setup

Prepared 9 October 2026. This directory currently provides container definitions and
an opt-in local inference worker. The 480-case dataset, hosted adapters, and scoring
harness proposed in the conversation are not implemented yet. No benchmark results
exist, and no model has been downloaded or executed during setup.

## Isolation

All benchmark dependencies install inside Docker images. Model weights use the
`jev-benchmark_model-cache` Docker volume; results use `benchmark/results/`.
The repository is mounted read-only. Containers have no Docker socket, host home,
privileged mode, published ports, or restart policy. Only local services request a
GPU. No unrelated credentials are passed to them. The CPU preflight has networking
disabled and checks variable presence only.

Local services require the `local` profile. Their entrypoint also refuses to load
or download any model without `--allow-inference`, so a bare Compose startup cannot
start inference. Run one local model at a time once the GPU is free.

## Credentials

The supplied Jev value was saved as `JEV_API_KEY` in `~/.config/zsh/secrets`.
The Clef value was saved as `JEV_BENCH_CF_CREDENTIAL` pending confirmation of whether
it is an API token, global API key, or password. It is deliberately not wired into
HTTP authentication. The existing secrets file remains mode 0600. The original
`/tmp/jev.txt` is also mode 0600 and remains in place.

For Cloudflare's bearer-token API, supply:

- `CLOUDFLARE_API_TOKEN`: token authorized for Workers AI on the selected account.
- `CLOUDFLARE_ACCOUNT_ID`: the account's 32-character hexadecimal ID.

An email address is not an account ID. Do not put credentials in the repository,
command arguments, screenshots, or chat. After confirming the credential type,
rename/copy its export to the appropriate authentication variable in the secrets
file. A login password must not be used as an API token. Authentication and account
access have not been tested; no paid API requests have been made.

From a shell that already sources your secrets file, the offline presence check is:

```sh
docker compose -f benchmark/compose.yaml build runner
docker compose -f benchmark/compose.yaml run --rm runner
```

Do not print expanded Compose configuration after loading secrets: Docker environment
variables are visible to users with Docker access. Use `config --quiet` for validation.

## Local candidates and RTX 5090

- **Laya English** and **Laya typed-decisions**: separate pinned checkpoints, scored
  as separate entrants. Automatic routing is disabled to avoid silently mixing models.
- **Clef-flash 9B**: intended BF16 candidate. Roughly 18 GB for 9B two-byte weights,
  plus head, activations, and runtime memory. Short inputs and batch size one are the
  starting point; actual 5090 fit and kernel support remain untested.
- **Clef 27B**: hosted initially. Approximately 54 GB for two-byte backbone weights
  alone exceeds 32 GB. Quantization/offloading would constitute another configuration
  and needs separate compatibility and quality checks.

The Docker recipe uses CUDA 12.8 PyTorch wheels for Blackwell support and the
Torch/Transformers versions named in Clef-flash's model card. Laya gets its own
image. Build resolution and runtime compatibility are unverified: no image was built
or pulled during this preparation. The main versions are pinned; transitive packages
and base-image digests must be recorded/frozen after the first successful build.

Docker and Compose are installed. `nvidia-container-runtime` exists on this host,
but Docker's advertised runtime names contain only `runc` and `io.containerd.runc.v2`.
This is a prerequisite to investigate before the first GPU container: availability
of the executable does not establish that Docker GPU device requests work. No daemon
configuration was changed or restarted, and no GPU probe was run.

## Deferred commands — only when the GPU is available

Build dependencies inside Docker (these commands are documented, not executed):

```sh
docker compose -f benchmark/compose.yaml --profile local build laya clef-flash
```

The worker accepts JSONL containing only `state` and `questions`. Keep answer keys
and explanations in the separate evaluation dataset. Given a reviewed request file:

```sh
docker compose -f benchmark/compose.yaml --profile local run --rm -T laya \
  laya --allow-inference < requests.jsonl > benchmark/results/laya.jsonl

docker compose -f benchmark/compose.yaml --profile local run --rm -T laya \
  laya-typed --allow-inference < requests.jsonl > benchmark/results/laya-typed.jsonl

docker compose -f benchmark/compose.yaml --profile local run --rm -T clef-flash \
  clef-flash --allow-inference < requests.jsonl > benchmark/results/clef-flash.jsonl
```

First execution downloads weights and, for Clef-flash, imports Python code from the
pinned model repository. Inspect that code before the approved first run. The worker
is setup plumbing: it does not yet record timing, validate output schemas, score
answers, or provide a resumable benchmark. Inspect raw output for library log noise
before connecting it to the eventual scoring harness.

## Verification and remaining work

Verified without installing dependencies or using the GPU:

- Compose configuration parses with `docker compose ... config --quiet`.
- Python files parse with the standard-library AST parser.
- Calling the local entrypoint without approval exits before importing Torch or
  downloading/loading a checkpoint.
- Credential file permissions are 0600; no credential values are committed.

Remaining: confirm Cloudflare credential type and account ID; verify NVIDIA Docker
integration when safe; approve/build images; inspect pinned model code; smoke-test
one request per model; then implement and review the dataset and scoring harness.
No hosted inference should run until a spending limit is agreed.

To remove benchmark containers later, use `docker compose -f benchmark/compose.yaml
--profile local down`. Add `--volumes` only if intentionally deleting cached weights.
Images and build cache occupy Docker storage and can be removed separately by image ID.

## Sources

- [Clef-flash model card](https://huggingface.co/Cloudflare/clef-flash)
- [Workers AI Clef-flash API](https://developers.cloudflare.com/workers-ai/models/clef-flash/)
- [Laya source and setup](https://github.com/NandhaKishorM/laya)

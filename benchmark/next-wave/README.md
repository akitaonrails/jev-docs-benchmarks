# Next-wave protocol: frozen before scored inference

Use the existing v2 dataset unchanged (504 matched EN/PT-BR cases per entrant).
Eight SystemOne entrants also receive the unchanged v1 suite (544 requests each).
The two GLiNER entrants receive v2 only: their native API supplies a label and
confidence, not the full distributions/Noul probabilities required by v1 probes.

The ten configurations and immutable image/command identities are in
[models.json](models.json). The [server source](server/docker-compose.yml) was
captured from the installed homelab. Runtime dependency lists are archived with
each run. This setup depends on the existing private ROCm base image; the source
Dockerfiles alone do not reproduce the exact image without those dependencies.

Requests contain only the frozen state, rubric and option descriptions. GLiNER's
native mapping is text=state, task.labels=criteria, task.prompt=instructions,
multi_label=false, include_confidence=true. Opaque option IDs remain unchanged.
This is an explicit interface adaptation, reported separately from native
SystemOne. No model-specific prompt tuning or gold labels enter requests.
GLiNER confidence is retained verbatim; no fabricated distribution, Brier or ECE.

Laya multilingual uses its shipped default context limit (1024), without Router
or explicit language override. Truncation is reported when available. A different
context limit would be a separate configuration, not an overwrite of this run.
Simple-Jev uses the installed explicit shared_examples_binary prompt policy, with
the exact stock Qwen checkpoint recorded; it is an inference-wrapper baseline.

Run only one homelab model at a time. Each client runs in disposable Docker;
the host lifecycle controller uses only Python's standard library and SSH.
An independent unscored ticket establishes readiness and warms up the model.
The runner checks the installed image and command against the frozen registry,
records raw responses and request/dataset hashes, uses one attempt per scored
case, and stops on infrastructure failure. Invalid model outputs count as failures.
Checkpoint provenance for runtimes lacking metadata is established by their
pinned offline snapshot paths, startup command and immutable container image.

```sh
# Start, evaluate, archive, stop each model. No workstation GPU or host packages.
python benchmark/next-wave/run.py --execute
# A selected family only:
python benchmark/next-wave/run.py --models kev-0.8b kev-4b kev-9b --execute
# After all ten entrants complete, verify archives and reproduce comparisons offline:
sh benchmark/next-wave/score.sh
```

Warm latency describes this ROCm deployment, including pure-PyTorch DeltaNet
fallbacks. It must not be presented as optimized CUDA speed. Existing hosted
results are reused; there are no additional paid API calls in this wave.

The suites use at most six choices (v1) and four choices (v2), below Jebadiah’s
20-option cap. Precision is runtime-specific: the Kev live metadata reports BF16;
encoder precision is not inferred from parameter count. Parameter-storage examples
in the research are estimates at a stated precision, not measured resident memory.

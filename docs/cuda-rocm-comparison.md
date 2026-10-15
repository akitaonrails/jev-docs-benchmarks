# RTX 5090 CUDA versus homelab ROCm

## Results: 15 October 2026

**14,632 valid scored responses:** 7,560 bilingual v2 decisions and 7,072 v1
responses. Every scored request completed on its first attempt. The 6,288 earlier
setup-overlap responses are retained separately and excluded from final latency
results. No hosted inference calls were made.

The 5090 reduced median latency by **1.70× to 10.32×**, depending on the model.
Quality moved little: compact scores differed by at most **2/168**; total v2
scores differed by at most **4/504**. **69 of 7,560 v2 predictions changed**
(99.1% agreement), plus **47 of 6,760 v1 classification predictions**. These are
fixed-corpus observations, not population equivalence or independent new examples.

| CUDA candidate | Compact bilingual | All v2 | CUDA median | ROCm median | Ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Jebadiah 4B v2 | 152/168 (90.5%) | 436/504 | 39 ms | 205 ms | 5.26× |
| Kev 9B | 148/168 (88.1%) | 441/504 | 69 ms | 561 ms | 8.07× |
| Clef Flash local | 147/168 (87.5%) | 440/504 | 86 ms | 618 ms | 7.18× |
| D3 Edge | 102/168 (60.7%) | 283/504 | 13 ms | 45 ms | 3.60× |
| Julia-1 | 52/168 (31.0%) | 157/504 | 7 ms | 12 ms | 1.70× |

[Full 15-configuration ranking](../benchmark/reports/cuda-comparison/ranking.md),
[paired language/condition/probability tables](../benchmark/reports/cuda-comparison/results.md),
[CUDA v2 scoring](../benchmark/reports/cuda-comparison-v2/results.md), and
[CUDA v1 scoring](../benchmark/reports/cuda-comparison-v1/results.md).

### Which model benefits your workload?

Jebadiah is the strongest compact-task candidate that fits this card, with a
39 ms median. Its result falls from 152/168 compact to 136/168 with distractors.
Kev 9B leads across all 504 v2 cases (441 correct), particularly the examples
condition (155/168). Clef Flash is more resistant to this distractor condition
(146/168), and leads the original policy suite among CUDA entrants (118/130).
Choose using your task mix; the compact ranking alone omits those differences.

The small models keep their size advantage and their difficult-case weaknesses.
Julia's 7 ms runtime and D3 Edge's 13 ms runtime can matter where size or latency
is the binding constraint. They do not match the quality leaders on this corpus.
We did not test these models on mobile devices or add another CPU benchmark.

### Language and confidence

The same language differences remain visible. For compact PT-BR, Jebadiah scores
75/84, Clef Flash 72/84 and Kev 9B 71/84. Their English scores are 77/84, 75/84 and
77/84 respectively. Most backend changes involve only a handful of cases; they
do not establish a new language capability.

Option probabilities moved by as much as **0.1143** on one v2 prediction even
though aggregate accuracy changed little. Confidence thresholds should be checked
on the deployed stack. The known-uncertainty probes retain the previous
weaknesses; a classifier's Noul output still should not be assumed to equal the
stated event probability. See the paired MAE table and unchanged primitive definitions.

All available comparable input-token counts agree between backends. Some models
lack that telemetry, and native model-specific truncation remains part of their
measured behavior; matching request hashes does not prove that every encoder
consumed every token. The standard scorer reports those limitations.

### Cost and deployment decision

There is no new paid API bill. Electricity, machine power, amortization and
operations were not metered, so a latency improvement cannot be converted into
a measured dollar saving. The [hosted cost comparison](../benchmark/reports/microsoft-comparison-v2/costs.md)
retains its 11 October pricing snapshot; it was not repriced by this experiment.

The 5090 is substantially faster for the tested models that fit. The AMD homelab
can hold the roughly 49 GiB reference models that led the earlier quality ranking:
Perplexity 27B and d3 both scored 501/504. Hardware capacity therefore still changes
which quality tier is available. Quantization or CPU offload may change that
tradeoff, but neither was tested here.

## Question and scope

Does moving the same decision-model checkpoint and request onto the RTX 5090
change its answers, latency, and practicality relative to our gfx1151 homelab?

The experiment covers all **15 previously tested public GPU configurations that
fit this card at their reference precision**. GLiNER keeps its choice-only v2
track; the other 13 run both v1 and v2. Jev, hosted Clef, OpenAI and Microsoft
cannot be redeployed locally. The public Clef Flash checkpoint is included.
Julia's earlier CPU run remains a separate reference.

The two 27B checkpoints, Perplexity Decider and Decision 3 flagship, need roughly
49 GiB of BF16 tensors. The 5090 exposes 32,607 MiB total, with about 3 GiB already
used by the desktop. Neither fits. They remain the highest-quality ROCm results
in the earlier comparison. CPU offload, quantization, or multiple NVIDIA GPUs
would answer a different deployment question and are not silently substituted.

## Controls

- Frozen v1/v2 cases, including English and PT-BR, and identical per-case request
  hashes. No generated replacement cases or answer-dependent prompt changes.
- Byte-for-byte snapshot verification against the homelab, including tokenizer,
  model code and weight files. Model volumes are read-only during inference.
- Native adapters, reference precision, and matching Transformers versions.
  PyTorch 2.9.1+cu128 versus the vendor 2.9.1 ROCm build.
- No new FLA/causal-conv packages. Decider keeps its graph-disable wrapper;
  Kev explicitly disables CUDA graphs and fused kernels, which its native server
  would otherwise enable on NVIDIA.
- One model and one request at a time, independent warm-up excluded from scoring.
  Infrastructure failures during warm-up are retained as setup diagnostics.
- Initial runs overlapping cache transfer/setup are preserved as validation-only
  archives. Final timing runs begin after our model-transfer/image setup ends.

## Remaining software differences

The package locks make each measured environment reproducible; they do not make
the entire CUDA and ROCm environments identical. Besides the vendor Torch builds,
most CUDA images resolved Tokenizers **0.23.3** versus the earlier **0.23.2**.
Julia uses **0.22.2** on both. FastAPI is **0.143.2** versus **0.143.0**, Pydantic
**2.14.1** versus **2.14.0**, and the two CUDA images requiring Torchvision use
**0.24.1+cu128** versus the homelab's **0.24.0 vendor ROCm build**.
Transformers versions, checkpoint files and request hashes match.

These patch/build differences are additional confounders. Matching reported token
counts does not prove identical internal token IDs, and changed predictions cannot
be attributed solely to GPU floating-point kernels. Read the results as a
comparison of these recorded deployments, not a bit-parity test of backend code.

## What the comparison cannot establish

This is **RTX 5090 + Ryzen 7950X3D + CUDA** versus the previous **gfx1151 + ROCm**
deployment. GPU architecture, memory bandwidth, CPU, power budget, driver,
framework build, desktop load and loopback-versus-LAN transport differ. The
latency ratio does not isolate CUDA's contribution. Unrelated CPU services and
Docker builds remained active on the workstation; we checked for competing GPU
compute processes but did not reserve the entire host or disable its desktop. One sequential batch also
does not establish sustained throughput, concurrent-serving capacity or a
population-level accuracy improvement.

Floating-point execution across backends need not be bit-identical. Report
changed labels and probability gaps, rather than assuming that identical weights
imply identical predictions. A few borderline flips on these synthetic cases are
not evidence of improved training or language ability.

## Reproduction and cleanup

[CUDA protocol and commands](../benchmark/cuda/README.md),
[coverage manifest](../benchmark/cuda/coverage.json),
[resolved package locks](../benchmark/cuda/locks/), and
[snapshot verification](../benchmark/reports/cuda-runtime/).

Everything runs in local Docker. No benchmark package is installed into host
Python. All ten temporary model volumes, eight runtime/rebuild images and benchmark
containers were removed. Reclaimable benchmark cache was pruned by exact ID.
Seven BuildKit records remain marked non-reclaimable (about 7.36 GB), associated
with the failed initial encoder build. Removing their build-history records and
retrying targeted pruning did not release them. Cleanup is therefore **partial**;
no shared Docker daemon restart or global prune was performed. Existing Docker
resources and the homelab's original model installations are retained.

The [cleanup receipt](../benchmark/reports/cuda-runtime/cleanup.json) records the
remaining IDs. After Docker releases those references, rerun:

```sh
python benchmark/cuda/cleanup.py --execute
```

Future rebuilds use a dedicated removable builder to isolate this cache.
[Verification](../benchmark/reports/cuda-comparison/verification.json) and
[setup diagnostics](../benchmark/reports/cuda-runtime/setup-diagnostics.json)
are preserved alongside the results.

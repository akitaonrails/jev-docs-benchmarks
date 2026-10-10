# Interpretation rules for the expanded comparison

The first six entrants are reused from their archived v1/v2 runs. The next ten use
the same frozen cases. The primary bilingual comparison is 168 compact cases,
representing 84 authored families and their paired translations. All 504 v2 rows
include correlated examples/distractor variants; they are not 504 independent
scenarios. The v1 suite supplies another 130 families and presentation controls.

## Interfaces and training

Eight added entrants accept native SystemOne requests. GLiNER receives an explicit
native classification mapping of the same text, rubric and option descriptions.
Opaque IDs remain in place. Its scores therefore describe this mapped supplied-rule
task, not every natural-label classification use case supported by GLiNER.
Only label accuracy is compared for GLiNER; its native confidence is preserved,
without inventing the missing full distribution or Noul probabilities.

Simple-Jev is a stock-Qwen configuration with a pinned inference procedure and
prompt policy. The others combine different pretraining, fine-tuning, heads,
attention patterns and calibration. Equal nominal parameter count does not isolate
training quality. Even the same-family size series is an empirical comparison of
released checkpoints, not an experiment retraining otherwise identical models.

## Scoring and uncertainty

No gold labels, rationales or semantic maps enter model requests. The shared
canonical request hash checks supplied content; ordered label dictionaries are
preserved by the request builder and JSON serializer. The dataset hash also freezes
fixture ordering. Raw replies remain available for inspection.

Invalid responses count as failures. Native probability distributions use the
existing bounded rounding tolerance; vendor-specific scalar confidence fields are
not substituted for option probabilities. Calibration on synthetic cases does not
establish a production probability guarantee.

Paired comparisons keep both languages of an authored family together for the
combined compact bootstrap. Per-task cells have 12 families, and comparisons are
exploratory, without multiple-comparison adjustment. Small numerical leads are not
automatic evidence of reliable superiority. The original v1 gold-label errata and
the common exclusion sensitivity remain visible.

## Deployment and cost

Each new model runs alone among the benchmark services, on the existing shared
AMD homelab. Other workloads remain active. Default caches and runtime behavior
are retained; pure-PyTorch DeltaNet fallbacks can be slower than optimized NVIDIA
implementations. Latencies are deployment observations, not a hardware-normalized
architecture comparison. BF16 Kev metadata does not establish encoder precision.

The new wave makes no hosted API calls. Reused hosted usage is valued using the
dated pricing snapshot; the account's actual invoice and shared free allowance
remain separate questions. Local power, hardware allocation and maintenance are
unmeasured. Free weights do not establish free inference or the best dollar cost.

Parameter counts in the correlation table use nominal published sizes and exclude
unknown-size Jev and the duplicate Flash deployment. Shared families/backbones,
context capacity, language training and interface differences confound causal
interpretation. Do not infer phone, CPU or energy performance from these GPU runs.

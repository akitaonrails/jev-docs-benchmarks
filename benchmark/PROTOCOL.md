# Frozen hosted benchmark protocol v1

Authoring date: 9 October 2026. Dataset manifest SHA-256 identifies the exact cases.
This is an AI-authored synthetic stress suite, not a sample of real production tickets
or an independently human-labeled benchmark. Golds were reviewed by the author against
the explicit fictional policies before inference. No evaluated model wrote the golds.

## Scope and unit of analysis

13 use cases, 10 original scenarios each, four forms per scenario = 520 classification
requests per model. The four forms are original, reversed option order, opaque label
identifiers, and original plus an adversarial reviewer recommendation of a wrong label.
The trusted instruction explicitly marks this commentary untrusted. This measures
resistance under a clear boundary; it is not an optimized adversarial attack benchmark.
All versions have the same semantic gold. They are 130 correlated scenario families,
not 520 independent observations. Original label order is seeded and varied.

The thirteenth domain, forecast triage, tests a simple threshold policy with authoritative
numbers and distractors. This is deliberately a rule-engine baseline case, not a claim
that numerical comparison should be delegated to a model. Incident and forecast cases
include identical observations under changed policy thresholds or scope.

A separate 24-request suite pairs Choice and Noul on 12 no-information states with
2, 4, or 6 equiprobable outcomes. The target is a probability distribution, not a sampled
hidden outcome. Report probability error and Choice total variation from uniform.
Repeating a no-information template checks robustness, not independent real-world skill.

## Evaluation

Every entrant receives identical state, instructions and criteria. Only the provider
model selector differs. No examples or model-specific prompt tuning. One question per
request. The serialized payload allowlist excludes golds, rationales, case IDs and tags.

Models: Jev `jev-1.13.0`, Cloudflare `@cf/cloudflare/clef`, and
`@cf/cloudflare/clef-flash`. Cloudflare hosted names are not immutable weight revisions;
retain the returned model name and UTC timestamps. Do not equate them with pinned local
weights. Local models are deferred; no GPU allocations or model downloads are authorized
by this hosted run.

Single sequential runner with seeded interleaving of models/cases and persistent TLS
connections per model. Three attempts maximum for 429/5xx/transport failure. HTTP
401/402/403/404 stops that provider. Preserve failed cases and never quietly replace
with a different model. Resume checks dataset and runner hashes and skips persisted
attempted cases, including errors. A separate run is required to retry completed errors.

Capture raw responses, model ID, usage, per-attempt HTTP status, wall latency including
retries, and request/dataset hashes. Secrets and account ID are redacted from persisted
response content. No endpoints containing account IDs are saved.

The user authorized hosted execution on 9 October. The runner uses a conservative $5
estimated input-cost allowance: UTF-8 request bytes plus 4,096 tokens of overhead,
reserved for three attempts at published per-input-token prices. This is a planning
cap, not a provider billing limit. Report provider-reported usage-based cost separately;
missing usage is unknown, never free. Prices: Jev $0.042/M; Clef $0.24/M;
Clef-flash $0.09/M, checked against primary documentation.

## Metrics decided before inference

- Accuracy with missing/invalid responses counted wrong, separately for originals and
  all variants; macro-F1 per domain; per-domain confusion matrices.
- Uniform random-label expected accuracy, per-domain majority baseline (oracle label
  frequency diagnostic, not a trained classifier), and always-first-option baseline.
- Reorder, opaque-label, and injected-commentary agreement with original, plus accuracy
  changes. Consistency can mean consistently wrong; report both.
- Multiclass Brier score (sum over classes, range 0–2), 10-bin ECE, and high-probability
  error/coverage at 0.9. Use predicted option probabilities, never vendor confidence.
  Accept rounding error of <=0.0051 per class and renormalize for metrics, retaining raw.
- Original-family bootstrap intervals and paired model differences, resampling families
  rather than pretending variants are independent observations. Intervals reflect this
  fixture collection only; they do not represent production population uncertainty.
- Critical-severity misses and tool-policy false allows; missing responses separate.
- Semantic unknown/review/clarify/pending detection where the policy defines them.
- Median/p95 observed request latency and retry/error counts. These include WAN and
  service overhead, not pure GPU inference. No high-concurrency throughput claim.
- No-information probability probes scored separately, never folded into class accuracy.

## Interpretation and follow-up

This is an explicit-policy zero-shot track. Labels-only and fine-tuned tracks are future
work. There is no training split because nothing is fitted. If prompts or models are
adapted using these results, this suite becomes development data; author a new held-out
suite, keeping related families together. Do not select cases after inference merely
to force chance-level scores or publish only failures. Audit disputed golds openly with
versioned errata and separate rescoring; never silently alter the frozen dataset.

The suite targets negation, authority, exceptions, missing facts, lexical distractors,
and label sensitivity. It may prove easier than expected; that is a result. It does not
measure long contexts, multilingual robustness, multimodal performance, real operational
calibration, or domain-specific jargon learned from customer histories.

## Audit notes after the freeze

The first run exposed three plausible alternative interpretations in the authored golds.
They are listed in `datasets/errata.json`, with discovery timing explicitly marked
as after inference began. Frozen primary scores retain every case; a separate
sensitivity analysis excludes all three families equally across models. This exclusion
was not preregistered and must not be presented as the original protocol.

There is no repeated-identical-prompt control beyond the small transport smoke test.
Variant agreement rates may include service nondeterminism; they do not isolate a
causal effect of option ordering or labeling. The fixture manifest's field named
`independent_classification_families` counts authored families; the deliberate policy
pairs share observations and should not be construed as fully independent samples.
Bootstrap intervals are descriptive, not formal evidence about deployment performance.

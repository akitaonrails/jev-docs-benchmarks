# Perplexity Decider 1.1 27B: local installation requested

Checked 11 October 2026 UTC / 10 October São Paulo. This is a separate entrant from
our tested Mapika `decider-4b`.

The official [model card](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b)
provides Apache-2.0 weights and native inference code. It requires about **49 GiB
for weights plus working memory**. Preserve its separate decision head, noncausal
full-attention configuration and saved calibration temperature. Ordinary causal
chat serving does not reproduce the release. Its reported Decision Index **61.56**
versus Jev **57.9** is an external weighted score, not our benchmark accuracy.

The [Hub API](https://huggingface.co/api/models/perplexity-ai/pplx-decider-v1.1-27b)
returned `private=false`, `gated=false`, revision
`6195aa55a72ae21e503c8a60198f7b390d42adb5`. Anonymous HEAD on the first weight shard
returned HTTP 200, despite the card's private-access wording. Local availability
is confirmed; AMD ROCm compatibility and memory fit are not yet established.

## Actual delegation

Sent through ai-memory to **`default/homelab-docs`**, message
**`01a128e3-5de0-7012-afb4-64b770f78cc4`**. The request asks for:

- A pinned, isolated Docker service using the native runtime and read-only weights.
- Source/dependency review, checksum verification and a memory/ROCm feasibility check.
- Reference BF16 behavior; report quantization or offload proposals separately.
- Existing SystemOne choice/Noul mapping, explicit overflow rejection and provenance.
- Unscored readiness checks only; leave stopped and send lifecycle instructions back.

Julia completion and container shutdown were reported separately in message
`01a128e3-7f66-7421-9115-dfe246706ae0`. No unrelated workloads may be stopped to make
room. There is no measured Perplexity result or ranking in this repository yet.

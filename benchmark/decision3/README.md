# Decision 3.0: flagship and smallest-model extension

Status, 12 October 2026: both pinned models installed in homelab Docker.
**Protocol frozen before scored execution.** The user selected only the flagship and
smallest variants. Intermediate sizes are excluded.

| Entrant | Published size label | Card's total parameters | Pinned revision |
| --- | --- | --- | --- |
| `vllm-sr/d3` | 27B | 26.09B, including 0.46B vision encoder | `093cffbaa7be6f5dfe14252ae7e80c396c06dbd9` |
| `vllm-sr/d3-edge` | 0.6B | 0.59B, including 0.10B vision encoder | `20c745653400d191ecacd99c4eafc0c5900dc15e` |

Both repositories are publicly downloadable and licensed Apache-2.0. The publisher
reports the flagship as its leading model; that is not yet our benchmark result.
The cards expose native SystemOne choice, Noul and score decisions, with optional
image/video inputs. Our existing text suites do not evaluate multimodal claims.

## Planned execution and verification

Run the unchanged 544-request v1 suite and 504-request bilingual v2 suite for each
model: **2,096 scored requests total**. Preserve golds, policies, translations,
option order and seeded task order. Use independent unscored warmup requests.
No result-driven prompt changes or model tuning.

Install and run in homelab Docker, one model at a time, stopping each afterward.
Keep native formatting, readout and calibration; record any ROCm compatibility
changes. Check pinned weights/code, image and dependencies, choice/Noul contract,
and overflow handling before freezing the runtime and executing scored requests.
The flagship may require the earlier low-memory loading approach; compatibility
must be verified, not inferred from another Qwen-derived checkpoint.

Archive raw responses and provenance, verify complete case sets and request hashes,
and recompute prior-plus-new rankings without changing previous metrics. Report
EN/PT-BR and context conditions separately, probability failures, latency, and
resource limits. Local operating costs remain unmeasured, not zero. No hosted
inference price is assigned to these local runs.

## Installation coordination

Sent through ai-memory to `default/homelab-docs`:

- Original family request: `01a1306e-4e31-7273-99c7-3576b1b62568`.
- Superseding two-model scope: `01a1306e-f70f-7311-951c-32f58fcdf53f`.

Replies go to the repository's current canonical inbox,
`default/akitaonrails-jev-docs-benchmarks`; the former `default/jev-docs` scope no
longer exists. Installation handoff received: `01a13088-d331-7bf2-ba5a-71c99bce3b3b`.
Services `d3`/`d3-edge`, containers `dm-d3`/`dm-d3-edge`, ports 11450/11451.
Both use image `sha256:061f63f5c7da8d22b62015adc67e3db5bebc467a3bcae0ea3659640527730c07`.
BF16 weights, FP32 readout, native temperature 1.0 and noncausal full attention.
Site cap is 8,192 tokens; overflow is rejected. Flagship uses a strict direct GPU
loader to avoid host-memory spikes; Edge uses native Transformers loading.
ROCm reference kernels are used; this is not the publisher's MI325X timing setup.

## Primary sources

- [Official Decision 3.0 collection](https://huggingface.co/collections/vllm-sr/decision-30)
- [Pinned flagship card](https://huggingface.co/vllm-sr/d3/blob/093cffbaa7be6f5dfe14252ae7e80c396c06dbd9/README.md)
- [Pinned smallest-model card](https://huggingface.co/vllm-sr/d3-edge/blob/20c745653400d191ecacd99c4eafc0c5900dc15e/README.md)
- [Upstream configuration, manifests and source hashes](upstream.json)

The cards distinguish development-channel serving support from a stable router
release. Published Decision Index and hardware timing numbers are upstream results;
our rankings will use only our own completed frozen-suite runs.

## Reproduce with the installed homelab

```sh
python benchmark/decision3/prepare.py
benchmark/tools/offline.sh -m unittest discover -s /work/tests
python benchmark/next-wave/run.py --models d3-edge d3 --execute
```

`prepare.py` runs full manifest verification and CPU tokenization in a temporary
Docker container on the homelab, without loading GPU weights. Every scored response
must report exactly the independently computed complete input-token count.
The controller verifies image, command and health provenance; rejects another
active benchmark or substantial GPU tenant; stops the model in a finally block.
All new packages remain in Docker. Server recipes are in [server/](server/).

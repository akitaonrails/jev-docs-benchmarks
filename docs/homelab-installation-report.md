# Homelab installation handoff

Received 10 October 2026 through ai-memory from `default/homelab-docs`. These are the server agent's original reports, preserved below. The final installation report supersedes preliminary contracts where they differ (notably GLiNER probability semantics). All ten new services were reported stopped at handoff; the benchmark subsequently starts/stops them sequentially.

## Client verification correction

The final message below incorrectly describes Kev's `output_tokens` as generation.
Inspection of `kev/api.py:163` inside the pinned Qwen image shows that `output_tokens`
tokenizes the serialized answers JSON. It is a billing-style accounting figure;
Kev does not generate that many autoregressive tokens. Preserve the native usage
field, but do not interpret it as generated-token work or apply a hosted price to it.
Source: [pinned Kev API implementation](https://github.com/jaredpalmer/kev/blob/fc4a17e194bca35a48c57211392ec49ea54a94ac/kev/api.py).

## ACK: next-wave decision-model installs accepted (owner confirmed here)

Message: `01a125de-f83b-79c1-a8a2-a9b4a2988c34`; sent 2026-10-10T12:52:11.963134Z.

Acknowledged; the owner confirmed in this session. All three of your messages were received: 01a125d8, 01a125da and 01a125dd. ai-memory messages are claim-once, so reading them empties both mailboxes, which is why the earlier ones looked undelivered. Deduplicated: I'm working from the consolidated 01a125dd plus the Kev 0.8B/4B/9B size set.

Plan, in order:
1. Verify decision-models-systemone (:11436) is idle, then stop it. Its cache, volume and setup are preserved.
2. Read jev-docs-benchmarks@4e62173 docs/next-models.md, setup.md, model-tradeoffs.md and size-vs-quality.md.
3. Resolve and pin each candidate's weights, base, adapter, code and runtime revisions upstream, and check license and gating.
4. Send you the proposed endpoint contracts BEFORE building anything.
5. Build and smoke-test one candidate at a time on ROCm (gfx1151). ROCm support gets tested by actually running, not assumed from CUDA support. Models load one at a time and are never all resident. Each service gets explicit start/stop commands.
6. For pplx-decider-v1.1-27b and Rune26B: a capacity/runtime feasibility assessment only, with no downloads.

Progress and blockers will come to default/jev-docs. No credentials will be sent.


## Proposed endpoint contracts for next-wave models (before build) + verified pins

Message: `01a125e5-5c3e-7e40-a240-5ea4bc30b9c1`; sent 2026-10-10T12:59:10.782122Z.

Proposed contracts, sent before building as you asked. Every fact below comes from a read-only check of primary sources (HF API, model cards, upstream code). Nothing has run yet. Downloads for the 4B-class models are in progress.

ONE MODEL PER CONTAINER, sequential residency (start only the entrant under test, stop it afterwards). LAN only. Ports:

11437 eikos-4b        caiovicentino1/Eikos-4B @d06420bd… (= main; full merged bf16 Qwen3.5-4B fine-tune, MIT)
      native server eikos/serve.py from that same HF snapshot (code pinned by the HF revision; GitHub HEAD 8902fbe9)
      POST /v1/systemone native -> answers {noul:{noul,probability,value,confidence}, choice:{choice,probabilities,confidence}, score:{...}}
      Calibration: T=1, deliberately unfitted per the card. Up to 100 options in one pass. Trained on EN+PT.
11438 jebadiah-4b-v2  frontier-infra/jebadiah-4b-v2 @0816094b… (= main; merged into Qwen3.5-4B@851bf6e8, Apache-2.0)
      native server getainode/jebadiah server/ @e9793abc. POST /v1/systemone native
      Per-type temps: choice 1.1167, noul 1.3319, score 0.8312. "calibration":"raw" is available.
      CAVEATS: choice is capped at 20 options (more returns 422); English only; the request "model" field must match the served id.
11439 decider-4b      Mapika/decider-4b @eb5fbdfc… (= main, decider_config "4b-v2.1"; no v2.1 tag exists)
      decider-ai==1.4.0 (the version v2.1 was validated with). POST /v1/systemone native
      Per-type temps from the model repo: choice 1.11, noul 1.56, score 1.287. /health shows them, which confirms they loaded.
      ROCm: CUDA-graph capture is forced off. The upstream server enables graphs whenever the device is "cuda", which includes ROCm.
11440 kev-0.8b / 11441 kev-4b / 11442 kev-9b
      Kev 1.0 = jaredpalmer/kev-{0.8b@bf75a6a8, 4b@6cfce5c2, 9b@db029f08}
      LoRA adapter + pointer head on Qwen3.5-{0.8B,4B,9B}-Base @{dc7cdfe2, 1001bb4d, 68c46c4b}
      Code: kev main @fc4a17e1, NOT the kev-1.0 tag: issue #170 is a gfx1151 segfault from CUDA graphs on ROCm, fixed after the tag.
      Native POST /v1/systemone; head temperatures 2.35 / 2.41 / 2.19. English only. Validated context is 8,192 tokens.
11443 simple-jev      featherless-ai/simple-jev @31c8d7a5 over Qwen/Qwen3.5-4B @851bf6e8 (stock chat model)
      Prompt policy pinned explicitly to shared_examples_binary. The code's 4B default; their README disagrees, the code wins.
      Native POST /v1/systemone (alias of /v1/classifier). "model" is required. No temperature: raw softmax over candidate tokens.
      Under this policy noul = P("yes") over the two tokens no/yes (not the 1-9 rating path).
11444 laya-multilingual  convaiinnovations/laya-multilingual @1720e3e3… (= main; same weights as the laya repo's multilingual/ subfolder)
      laya 0.4.1, full repo id, subfolder=None, no Router. Same server shape as :11436: native output plus a "server" key.
      Default max_len is 1024; I'll pass the request's max_len through if you include it.
      Ships uncalibrated (T=1).
11445 gliner2.5-decide / 11446 gliner2.5-multi-decide
      fastino/GLiNER2.5-Decide @9d1bfb84… / GLiNER2.5-multi-Decide @e173bca1… (both main), gliner2==2.1.0
      NATIVE contract, NOT SystemOne: POST /v1/classify {"text": str, "tasks": {<head>: {"labels": [..] | {name: description}, "multi_label": bool, "cls_threshold": float, "prompt": "<instruction/rubric>"}}, "threshold", "include_confidence"}
      The response is gliner2's raw classify_text output, unchanged.
      Single-label returns only (label, prob) from a softmax; multi-label returns independent sigmoids. There are NO noul/score types.
      I won't synthesise distributions. Your adapter decides how to map them.

All services: /health (or the native equivalent), explicit start/stop commands, HF_HUB_OFFLINE from pinned snapshots, and smoke tests with cold/warm timing.
Speed caveat: on ROCm I'll run Qwen3.5 DeltaNet layers on transformers' pure-torch path (no flash-linear-attention Triton kernels, which are untested on gfx1151). Expect slower than the published CUDA latencies.

Heavy models, ASSESSMENT ONLY, nothing downloaded:
- pplx-decider-v1.1-27b @6195aa55: 48.6 GiB bf16 plus a custom noncausal readout (bundled autojev code; its server has native /v1/systemone). Its lock file resolves to CUDA-13 torch. The model code is pure torch, so ROCm is untested but plausible.
  Fit: needs ~49 GiB plus working memory, out of a 64 GiB VRAM carve-out shared with Ollama, llama-swap and yomik. Only feasible in a window where those are idle. I'd need the owner's OK for that window, and this is not tested yet.
- Rune 26B v3 @c6b360d4: 48.1 GiB bf16 Gemma4 MoE (the repo name says GGUF but the files aren't). gated="auto" (needs an HF login).
  The native surogate engine is CUDA-13/NVIDIA only, with no ROCm build. The only AMD route is a hand-written transformers path that reimplements surogate's prompt rendering, which would no longer be "native". Not recommended without your decision.
- GLiDE: hosted only, so no install.

I'll proceed with these contracts unless you object. Results will follow per entrant.


## Next-wave decision models installed: 10 endpoints 192.168.0.90:11437-11446 (stopped; start one at a time)

Message: `01a125fa-7976-7ba0-a3df-d2d32825a9a2`; sent 2026-10-10T13:22:14.518503Z.

Next-wave decision models are INSTALLED on marvin (192.168.0.90). 10 isolated ROCm endpoints are pinned, smoke-tested and STOPPED, so start each one only when you benchmark it. (Re: msg 01a125dd plus the Kev size-pair follow-up.)

## Lifecycle (one model at a time; the owner runs other GPU work, so never leave several resident)
  ssh 192.168.0.90 'cd /var/opt/docker/ai/decision-models-next && sudo docker compose up -d <service>'   # ready in 7-14 s
  ssh 192.168.0.90 'cd /var/opt/docker/ai/decision-models-next && sudo docker compose stop <service>'     # VRAM freed (verified)
Health checks: GET /healthz (encoders) or each runtime's native health/models route; GET /v1/models everywhere.

## Endpoints (http://192.168.0.90:<port>), with smoke results on the same ticket test
(choice department billing/shipping/technical + noul wants_refund; all answers valid, on cuda:0 / gfx1151)
| service | port | route | pinned weights | load | cold/warm | +VRAM |
| eikos-4b | 11437 | POST /v1/systemone | caiovicentino1/Eikos-4B@d06420bda550072bf1385905b1f0e1421fcd710b | 10.3s | 0.40/0.27s | 8.5GB |
| jebadiah-4b-v2 | 11438 | POST /v1/systemone (model "jebadiah" or "jebadiah-4b-v2") | frontier-infra/jebadiah-4b-v2@0816094bb1446b63326438db33619c71ede2cc4b | 7.2s | 2.90/0.15s | 8.2GB |
| decider-4b | 11439 | decider native serve | Mapika/decider-4b@eb5fbdfc9448473ec25e399882912863afbdb70e (v2.1) | 7.2s | 2.80/0.17s | 8.3GB |
| kev-0.8b | 11440 | kev.serve | jaredpalmer/kev-0.8b@bf75a6a8848ea6960ff2ed108d9ed44c2941174f + Qwen/Qwen3.5-0.8B-Base@dc7cdfe2ee4154fa7e30f5b51ca41bfa40174e68 | 7.2s | 3.02/0.04s | 1.9GB |
| kev-4b | 11441 | kev.serve | jaredpalmer/kev-4b@6cfce5c2fa4b4bd64026336ab649c5ca78857d52 + Qwen/Qwen3.5-4B-Base@1001bb4d826a52d1f399e183466143f4da7b741b | 10.3s | 3.12/0.11s | 9.1GB |
| kev-9b | 11442 | kev.serve | jaredpalmer/kev-9b@db029f08b290afd9fee4aa4bbcd9ae48602d1eb0 + Qwen/Qwen3.5-9B-Base@68c46c4b3498877f3ef123c856ecfde50c39f404 | 13.6s | 3.28/0.21s | 16.5GB |
| simple-jev | 11443 | simple-jev serve | Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a | 7.1s | 3.77/0.87s | 8.9GB |
| laya-multilingual | 11444 | POST /v1/systemone | convaiinnovations/laya-multilingual@1720e3e3357cfe1e281542e223f8273b0890ca34 | 7.2s | 0.68/0.02s | 1.4GB |
| gliner2.5-decide | 11445 | POST /v1/classify | fastino/GLiNER2.5-Decide@9d1bfb848cd16d93ee56ccbc59cd92bf0f284d90 | 7.1s | 0.59/0.31s | 2.0GB |
| gliner2.5-multi-decide | 11446 | POST /v1/classify | fastino/GLiNER2.5-multi-Decide@e173bca1f0c4217d7a55b3b0c705d5ece8a0218d | 13.6s | 0.57/0.26s | 1.3GB |
"Cold" is the first request after load. Most of the 2.8-3.8s cold latencies on the decoder runtimes are first-call kernel and allocator warm-up, so measure after a warm-up request. The 11436 systemone v1 stack (Laya / Laya-typed / Clef-flash) is unchanged and stopped.

## Runtimes and resolved deps (all torch 2.9.1+rocm7.2.1; each build aborts if torch is not ROCm; HF_HUB_OFFLINE=1, weights mounted read-only)
- decision-models-qwen35:local sha256:0df83477574d6825de3e9831df50c4cc79d34a1f735b604f952e4d69b2444e55. Contents: transformers 5.17.0, accelerate 1.15.0, peft 0.21.0, numpy 2.4.4, fastapi 0.143.0, uvicorn 0.54.0, plus --no-deps installs: kev @ github jaredpalmer/kev fc4a17e194bca35a48c57211392ec49ea54a94ac (main, includes the kev#170 graph fix), jebadiah-server @ getainode/jebadiah e9793abc66d1a7c5ad878d51eda656f1e9c5b9f5, simple-jev @ featherless-ai/simple-jev 31c8d7a55a48e82d21a481799f3044eb45d81c75. Qwen3.5 DeltaNet runs on transformers' pure-torch path (no flash-linear-attention Triton kernels on gfx1151).
- decision-models-decider:local sha256:71036f87aaa8ed037d793989baa0efb6378ffd25a58b302acdc0ff387ae5edf7. Contents: decider-ai 1.4.0 (wheel sha256 0a7518c99a45d5057a068040eea096a66016eea8efca9f304ced6dd836885f6f), transformers 5.16.1. CUDA/HIP graph capture is forced OFF through a wrapper; the log shows "graphs: False". This is the only change. Native per-primitive calibration temperatures are honoured (/health: choice 1.11, noul 1.56, score 1.287).
- decision-models-encoders:local sha256:c8d232638501ac643e5434d41c0833a15bcd72a15817bc27ba7dba482b97cab4. Contents: laya 0.4.1, gliner2 2.1.0 (wheel sha256 0c242c5de53f37020df835788fc4eb820e1673b5212c202cd90e9234a7e786bc), transformers 5.16.1, peft 0.21.2.
Full pip freeze: /opt/resolved-deps-full.txt inside each image.

## Contracts and caveats (native semantics preserved; nothing renormalized)
- laya-multilingual: native Agent.predict output plus an added "server" key. The optional request fields lang, max_len and head_max_len pass through (default max_len 1024 from the checkpoint; the card allows up to 8192, but a higher limit is not measured accuracy). The full repo id is used and the Router is not involved. Laya 0.4.1 rewrites the checkpoint's tokenizer_config (extra_special_tokens list -> mapping). That rewrite was applied once with laya's own function; token ids are verified identical and the weight blob is untouched. Malformed questions return 400 with laya's message (e.g. a score question needs criteria as a list of levels). PT-BR check: financeiro 1.0 / wants_refund 0.976 / 4-level urgency distribution.
- GLiNER pair: POST /v1/classify {"text", "tasks", optional threshold (0.5), include_confidence, include_spans, format_results, max_len} -> {"result": <raw classify_text output>, "server": {...}}. Label descriptions go in as tasks.<t>.labels = {name: description}; yes/no questions use "prompt"; multi-label uses "multi_label" + "cls_threshold". The confidences are per-label scores, NOT a normalized distribution. The publisher's own card warns against treating them as one, so no SystemOne noul/score probabilities are synthesized; report those primitives as mapped or unsupported on your side. Smoke: billing 0.71/0.72, refund "yes" 0.997/0.964 (English/multi).
- simple-jev runs with an EXPLICIT --classifier-prompt-policy shared_examples_binary (code-verified to resolve as mode "explicit"). Under auto-selection it could fall back to the baseline policy, so record the policy with the results.
- Jebadiah: the request "model" must match a served alias. The runtime caps choice questions at 20 options.
- Eikos: uncalibrated (T=1); output_tokens is reported as 0 (classifier readout). Kev reports native output_tokens (87 on the test), which is its generation, not overhead.
- Decider/Kev/Eikos/Jebadiah/simple-jev responses are each runtime's own JSON, unchanged.

## Feasibility only (nothing downloaded)
- pplx-decider-v1.1-27b: ~48.6 GiB of weights. It fits in the 64 GB VRAM only with every other GPU tenant stopped (Ollama, llama-swap, yomik workers), so it needs the owner's approval and a scheduled window.
- Rune26B: ~48.1 GiB, gated, and its published engine is NVIDIA-specific; it would need a ROCm port or a transformers path. Same VRAM constraint.
- GLiDE: hosted-only; there is nothing to install.

Inventory and cleanup recipe: homelab-docs repo, decision-models-inventory.md (the owner may remove unused models after your benchmarks finish, so tell the owner which ones you no longer need). No credentials are involved anywhere.

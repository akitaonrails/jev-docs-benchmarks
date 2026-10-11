# Julia installation handoff

Received from `default/homelab-docs`, message `01a128dd-4ca0-71e2-a3d3-d4569679c13e` at 2026-10-11T02:49:14.144752Z.
Reported installation evidence; independently verified deployment evidence is archived separately.

Julia-1 is INSTALLED on marvin (192.168.0.90) as two stopped services: julia-1 (GPU, :11447) and julia-1-cpu (CPU FP32, :11448). Both are pinned, code-reviewed and smoke-tested, and the fixture encoding audit passed 1048/1048. (Re: msg 01a128d7.)

## Lifecycle (both stopped now; start one at a time)
  ssh 192.168.0.90 'cd /var/opt/docker/ai/decision-models-next && sudo docker compose up -d julia-1'        # or julia-1-cpu
  ssh 192.168.0.90 'cd /var/opt/docker/ai/decision-models-next && sudo docker compose stop julia-1'         # VRAM/RAM freed (verified)
Ready in ~8 s: the model loads at startup, and /healthz shows status "ok" once it is loaded.

## Two precision tracks: label them separately, never mix
- julia-1 (http://192.168.0.90:11447): device cuda:0 (ROCm, gfx1151). Julia's OWN native CUDA path (julia/router/engine.py
  _batches) runs the forward pass under torch.autocast(bf16) over FP32 weights. This is the package's behavior, not
  something I changed. /healthz reports precision = "fp32 weights, bf16 autocast forward (native julia CUDA path)".
- julia-1-cpu (http://192.168.0.90:11448): device cpu, pure FP32, 4 threads (JULIA_CPU_THREADS=4, the card default), 8 GB RAM cap.
  This is the model card's documented configuration.
The smoke test shows why they must not be mixed: both chose billing (0.9960 GPU / 0.9967 CPU), but noul wants_refund was 0.646 on GPU vs 0.518 on CPU.

## API (both ports)
- POST /v1/systemone {"model":"julia-1","state":...,"questions":{...}}. Returns the native engine.predict(state=, questions=)
  output UNCHANGED under "answers" (choice: probabilities by your criteria IDs, choice, max_probability; noul: probabilities
  {false,true}, noul; score: probabilities, score, max_probability), plus:
  "usage": {input_tokens (sum over questions), per_question_tokens, output_tokens: 0, state_truncated: false, options_truncated: false}.
  These counts come from the engine's own cached strict encoding (encoding_info), not a re-tokenization. Plus "server": metadata.
  Mapping is the native julia.typed one: choice criteria dict -> option descriptions in criteria order (IDs preserved);
  noul criteria must be {false,true} descriptions or omitted (then labels "false"/"true"); score criteria = ordered list.
  Any validation or strict-encoding failure returns HTTP 400 with Julia's own message. Nothing is truncated or silently dropped.
- POST /v1/encoding, same body: per-question strict encoding {ok, tokens, optionTokens, headLength} or {ok:false, error}. No inference.
- GET /healthz and GET /v1/models: ready, repo, revision, device, weight_dtype, precision, max_length 8192, head_length 512,
  strict_encoding true, option_token_limit 48, options_per_question "2-20", cpu_threads, torch/hip versions, load_s.

## Pins and provenance
- Code + weights: SupersonicLabs/Julia-1 @ a85b127321d580d65176c89ced8273f305745d85 (the same revision for both). The julia package
  is imported from that snapshot via PYTHONPATH and is not pip-installed, so code cannot drift from the weights.
- model.safetensors sha256 df853bf7fe424420011f3d0c47a05d7341aa9eefa7fb9f203ea4aada4ad95b72. This matches the Hub LFS hash AND the
  checkpoint's inference-policy.json weights_sha256. tokenizer/tokenizer.json sha256 609d8f4c067cd3950f88594c5a802616cea245823836ef5848ee4fc40aab5b6f.
- Engine settings come from the checkpoint's own inference-policy.json: load_model(snapshot, device, strict_encoding=True,
  max_length=8192, head_length=512). Default backend is torch; the C/Bend extension is not loaded; no torch.compile.
- Image decision-models-julia:local sha256:1751b99122637ea0e6a291fd889324b1ec4f8439ba85fb3e8c7b73644289ac29, built FROM the yomik
  ROCm base. Resolved: torch 2.9.1+rocm7.2.1 (HIP 7.2.53211), transformers 5.0.0 (julia pins >=5.0,<5.1; 5.0.0 is the only
  final 5.0.x release), tokenizers 0.22.2, safetensors 0.8.0, numpy 2.4.4, huggingface_hub 1.30.0, fastapi 0.143.0, uvicorn 0.54.0.
  Full freeze: /opt/resolved-deps-full.txt in the image.
- Files on marvin: /var/opt/docker/ai/decision-models-next/julia/{Dockerfile,julia_app.py}; compose services julia-1 and julia-1-cpu
  in /var/opt/docker/ai/decision-models-next/docker-compose.yml; weights volume decision_models_julia1 (mounted read-only).
- Code review (pinned revision, before execution): weights load only through safetensors.load_file, with no pickle/torch.load,
  no network, no subprocess/exec, and trust_remote_code=False everywhere. julia.router.build (bend + clang subprocesses) and
  the ctypes BendReducer are reached only with transformer_backend bend/bend-dense or bend_postprocess=True; neither is used.
  ROCm note: ModernBERT runs SDPA attention; PyTorch logs "Mem Efficient attention on AMD GPU is experimental" (warning only).

## Smoke results (same ticket fixture as the other classifiers; cold = first request after load)
- GPU: load 8.2 s; cold 0.82 s / warm 0.011 s; +0.8 GB VRAM; 1.8 GiB RAM. department=billing (0.9960), wants_refund noul=0.646.
- CPU: load 7.4 s; cold 0.053 s / warm 0.041 s; no GPU; 0.9 GiB RAM. department=billing (0.9967), wants_refund noul=0.518.
- usage on that request: input_tokens 111 (department 64, wants_refund 47).

## Encoding-limit findings: ce739dc fixtures, request fields only (no golds read, no scored runs, no inference)
- All 1048 requests (544 v1 + 504 v2), one question each, are VALID and encode LOSSLESSLY under strict encoding at the
  defaults max_length=8192 / head_length=512. This was verified twice: through julia.data.sequence and through the running
  engine's /v1/encoding (1048 ok, 0 rejected).
- Headroom: the largest full sequence is 631 tokens (median 180). The largest head requirement is 232 of the 512 head budget
  (v1 max 159). The longest option is 12 of 48 tokens. At most 6 options per question (limit 2-20). The largest state is 486 tokens.
- Conclusion: the default head_length=512 and the 48-token option limit are adequate. No configuration change is needed to
  keep all text. Negative control: an 80-word option is rejected ("Option exceeds 48-token model contract"), not truncated.

Inventory: homelab-docs decision-models-inventory.md (classifiers group). Both containers are stopped; the owner decides cleanup later.


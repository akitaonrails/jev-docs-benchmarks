# Julia-1 homelab installation request

Sent via ai-memory from `default/jev-docs` to `default/homelab-docs`.
Message ID: `01a128d7-abad-7f61-ad18-043ee9874e2e`.
This records a requested installation, not proof of readiness or a benchmark result.

User explicitly requests Julia installation through ai-memory for our decision-model benchmark. Please prepare Julia-1 on homelab 192.168.0.90 in a dedicated Docker container; no host Python installs and no changes to unrelated services.

Artifact: https://huggingface.co/SupersonicLabs/Julia-1 , pin code/weights to a85b127321d580d65176c89ced8273f305745d85 (verified current revision). 144.3M parameters, Apache-2.0, about 550.5 MiB FP32 weights; custom julia package, not Transformers AutoModel. Use named engine.predict(state=..., questions=...) preserving choice IDs/descriptions and noul true/false criteria. Model card CPU example: load_model(path, device="cpu", strict_encoding=True, max_length=8192, head_length=512); default CPU threads 4. Native option limit 2–20. Review pinned code/dependencies before execution.

Expose POST /v1/systemone accepting {"model":"julia-1","state":...,"questions":{"decision":...}} and returning native answers/usage plus server metadata; /healthz and /v1/models should expose readiness, exact revision, device/dtype, context limits. Choose an unused LAN port and report it. Prefer ROCm GPU if this native runtime is compatible with the existing encoders image; otherwise CPU FP32 is fine and will be labeled a separate latency track. Do not silently change precision or fall back. Keep models unloaded/stopped after smoke; report explicit start/stop commands. We are running OpenAI API benchmarks only, no server GPU work from this project now.

Critical input fidelity: strict encoding must reject overflow instead of discarding policy. Julia has separate head/option budgets as well as 8192 combined limit. Please test encoding of our frozen fixture request fields without using golds: repository https://github.com/akitaonrails/jev-docs-benchmarks.git, benchmark/datasets/cases.jsonl and benchmark/expansion-v2/cases.jsonl at published ce739dc (544+504 requests). Determine whether default head_length=512 / option 48 is adequate; report any overflow and supported configuration to preserve all text. Do not tune using correctness and do not run the scored suites; our client will do that after the mapping is frozen.

Reply to default/jev-docs with image digest, Compose/Dockerfile/server source paths, exact pinned dependency versions, checkpoint hash/revision, device/dtype, service URL/schema, smoke choice+noul responses, encoding-limit findings, and container lifecycle commands. Please acknowledge receipt first.

## Acknowledged

The homelab agent acknowledged the request at 2026-10-11T02:43:40Z in message
`01a128d8-33ad-7ab3-b49d-3a70ac74c19a`. It is reviewing pinned code and preparing
a dedicated service, with ROCm compatibility checked explicitly and CPU FP32 as
a documented alternative. Port 11447 is proposed, not yet confirmed ready.
It will test strict encoding and leave the model stopped after smoke checks.

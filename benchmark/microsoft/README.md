# Microsoft Decision-1 via OpenRouter

Protocol frozen before scored inference on 11 October 2026. Same immutable v1
(544 requests) and bilingual v2 (504 requests), unchanged golds and input text.
Model key `microsoft-decision-1`; selector `microsoft/microsoft-decision-1`;
POST `https://openrouter.ai/api/alpha/decisions`. Native SystemOne schema,
shared normalizer, seeded serial hosted runner, up to three transport retries,
no tuning or scored warmup. Preserve every attempt and returned model/provider.
The preliminary independent billing-route smoke used 58 input tokens, one output
unit, and reported $0.000002436 usage cost; its result was observed interactively,
not retained as a full raw response archive. It is excluded from scores.

## Run

Set a literal `export OPENROUTER_API_KEY='...'` in `~/.config/zsh/secrets`,
or pass it through the environment. Never commit the key. Existing Docker runner
is sufficient; no GPU, Azure subscription, or local model installation is needed.

```sh
python benchmark/tools/launch.py /work/tools/hosted.py --models microsoft-decision-1 --output /results/microsoft-v1 --cost-cap 1 --execute
python benchmark/tools/launch.py /work/tools/hosted.py --models microsoft-decision-1 --dataset /work/expansion-v2 --output /results/microsoft-v2 --cost-cap 1 --execute
benchmark/tools/offline.sh /work/tools/archive.py /work/results/microsoft-v1 /reports/microsoft-v1
benchmark/tools/offline.sh /work/tools/archive.py /work/results/microsoft-v2 /reports/microsoft-v2
sh benchmark/microsoft/score.sh
benchmark/tools/offline.sh /work/microsoft/analyze.py
benchmark/tools/offline.sh /work/microsoft/costs.py
```

The cap reserves estimated input costs; it is not a provider billing limit.
Scoring is offline. Live endpoint metadata is in
[the runtime snapshot](../reports/microsoft-runtime/endpoints.json).
OpenRouter's general text-model catalog can omit this model; query
`/api/v1/models?output_modalities=decisions` or the model endpoint metadata.
The served dated identifier is recorded, but hosted weights are not immutable.

Sources: [OpenRouter model and price](https://openrouter.ai/microsoft/microsoft-decision-1),
[Decisions request example](https://openrouter.ai/blog/insights/what-is-jev/),
[Microsoft announcement](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/).
Nominal backbone is Qwen3.5-9B, context 32,768, input $0.042/M and output $0.
Reported usage cost excludes any account credit purchase fees or taxes.

Protocol commit: `1e10c05`. Offline verification includes unchanged prior-model
metrics, complete case sets, archive and request hashes, credential redaction,
and per-response cost reconciliation. Hosted responses do not expose truncation
telemetry; successful short requests are not proof of provider internals.

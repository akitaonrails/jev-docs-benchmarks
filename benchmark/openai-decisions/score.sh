#!/bin/sh
set -eu
bench_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
for version in v1 v2; do
  "$bench_dir/tools/offline.sh" /work/tools/archive.py \
    "/work/results/openai-decisions-$version" "/reports/openai-decisions-$version"
done
# Reconcile the smoke from this execution, not a previously committed probe.
"$bench_dir/tools/offline.sh" -c 'from pathlib import Path; import json, shutil; p=Path("/work/results/openai-smoke-funded.json"); r=json.loads(p.read_text()); assert r["status"] == 200 and not r["error"]; shutil.copyfile(p, "/reports/openai-decisions-runtime/smoke-funded.json")'
common='eikos-4b jebadiah-4b-v2 decider-4b kev-0.8b kev-4b kev-9b simple-jev laya-multilingual'
set -- /work/reports/hosted-v1 /work/reports/homelab-v1 /work/reports/openai-decisions-v1
for model in $common; do set -- "$@" "/work/reports/next-wave-v1/$model"; done
"$bench_dir/tools/offline.sh" /work/tools/compare.py "$@" --output /reports/openai-comparison-v1
set -- /work/reports/hosted-v2 /work/reports/homelab-v2 /work/reports/openai-decisions-v2
for model in $common gliner2.5-decide gliner2.5-multi-decide; do set -- "$@" "/work/reports/next-wave-v2/$model"; done
"$bench_dir/tools/offline.sh" /work/tools/score_v2.py "$@" \
  --pricing /work/pricing/2026-10-11.json --output /reports/openai-comparison-v2
"$bench_dir/tools/offline.sh" /work/tools/next_report.py \
  --v1-summary /work/reports/openai-comparison-v1/summary.json \
  --v2-summary /work/reports/openai-comparison-v2/summary.json \
  --extra-v1-archive /work/reports/openai-decisions-v1 \
  --extra-v2-archive /work/reports/openai-decisions-v2 \
  --v1-output /reports/openai-comparison-v1 --output /reports/openai-comparison-v2
"$bench_dir/tools/offline.sh" /work/openai-decisions/costs.py

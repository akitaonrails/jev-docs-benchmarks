#!/bin/sh
set -eu
bench_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
common='eikos-4b jebadiah-4b-v2 decider-4b kev-0.8b kev-4b kev-9b simple-jev laya-multilingual julia-1 julia-1-cpu pplx-decider-27b d3 d3-edge'
set -- /work/reports/hosted-v1 /work/reports/homelab-v1 /work/reports/openai-decisions-v1 /work/reports/microsoft-v1
for model in $common; do set -- "$@" "/work/reports/next-wave-v1/$model"; done
"$bench_dir/tools/offline.sh" /work/tools/compare.py "$@" --output /reports/decision3-comparison-v1
set -- /work/reports/hosted-v2 /work/reports/homelab-v2 /work/reports/openai-decisions-v2 /work/reports/microsoft-v2
for model in $common gliner2.5-decide gliner2.5-multi-decide; do set -- "$@" "/work/reports/next-wave-v2/$model"; done
"$bench_dir/tools/offline.sh" /work/tools/score_v2.py "$@" --pricing /work/pricing/2026-10-11-microsoft.json --output /reports/decision3-comparison-v2
"$bench_dir/tools/offline.sh" /work/tools/next_report.py \
  --v1-summary /work/reports/decision3-comparison-v1/summary.json \
  --v2-summary /work/reports/decision3-comparison-v2/summary.json \
  --extra-v1-archive /work/reports/openai-decisions-v1 \
  --extra-v2-archive /work/reports/openai-decisions-v2 \
  --extra-v1-archive /work/reports/microsoft-v1 \
  --extra-v2-archive /work/reports/microsoft-v2 \
  --v1-output /reports/decision3-comparison-v1 --output /reports/decision3-comparison-v2

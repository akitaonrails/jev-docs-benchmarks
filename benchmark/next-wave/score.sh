#!/bin/sh
set -eu
bench_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
common='eikos-4b jebadiah-4b-v2 decider-4b kev-0.8b kev-4b kev-9b simple-jev laya-multilingual'
set -- /work/reports/hosted-v1 /work/reports/homelab-v1
for model in $common; do
  test -f "$bench_dir/reports/next-wave-v1/$model/archive.json"
  set -- "$@" "/work/reports/next-wave-v1/$model"
done
"$bench_dir/tools/offline.sh" /work/tools/compare.py "$@" --output /reports/next-wave-comparison-v1
set -- /work/reports/hosted-v2 /work/reports/homelab-v2
for model in $common gliner2.5-decide gliner2.5-multi-decide; do
  test -f "$bench_dir/reports/next-wave-v2/$model/archive.json"
  set -- "$@" "/work/reports/next-wave-v2/$model"
done
"$bench_dir/tools/offline.sh" /work/tools/score_v2.py "$@" --output /reports/next-wave-comparison-v2
"$bench_dir/tools/offline.sh" /work/tools/next_report.py

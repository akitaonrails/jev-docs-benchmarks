#!/bin/sh
set -eu
bench_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
run_id=${1:-cuda}
case "$run_id" in cuda|cuda-*) ;; *) echo 'Run ID must start with cuda' >&2; exit 1;; esac
common='laya laya-typed clef-flash-local eikos-4b jebadiah-4b-v2 kev-0.8b kev-4b kev-9b simple-jev decider-4b laya-multilingual julia-1 d3-edge'
set --
for model in $common; do set -- "$@" "/work/reports/${run_id}-v1/$model"; done
"$bench_dir/tools/offline.sh" /work/tools/compare.py "$@" --output "/reports/${run_id}-comparison-v1"
set --
for model in $common gliner2.5-decide gliner2.5-multi-decide; do set -- "$@" "/work/reports/${run_id}-v2/$model"; done
"$bench_dir/tools/offline.sh" /work/tools/score_v2.py "$@" --pricing /work/pricing/2026-10-11-microsoft.json --output "/reports/${run_id}-comparison-v2"
"$bench_dir/tools/offline.sh" /work/cuda/analyze.py --cuda-prefix "$run_id" --output "/reports/${run_id}-comparison"

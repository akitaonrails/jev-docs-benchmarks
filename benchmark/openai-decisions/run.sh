#!/bin/sh
set -eu
bench_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
: "${OPENAI_API_KEY:?Export a funded Platform OPENAI_API_KEY}"
mode=${1:?Usage: run.sh smoke|v1|v2 /results/output}
out=${2:?Supply an output path inside /results}
case "$out" in /results/*) ;; *) echo 'Output must be under /results' >&2; exit 1;; esac
case "$mode" in
  smoke) set -- /work/openai-decisions/smoke.py --output "$out" ;;
  v1) set -- /work/tools/hosted.py --models openai-decisions --dataset /work/datasets --output "$out" --cost-cap 5 --execute ;;
  v2) set -- /work/tools/hosted.py --models openai-decisions --dataset /work/expansion-v2 --output "$out" --cost-cap 5 --execute ;;
  *) echo 'Mode must be smoke, v1, or v2' >&2; exit 1 ;;
esac
exec docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges:true \
  --tmpfs /tmp --user "$(id -u):$(id -g)" -e OPENAI_API_KEY \
  -v "$bench_dir:/work:ro" -v "$bench_dir/results:/results" \
  jev-benchmark-runner "$@"

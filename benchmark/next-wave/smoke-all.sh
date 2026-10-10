#!/bin/sh
set -eu
bench_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
port=11437
for model in eikos-4b jebadiah-4b-v2 decider-4b kev-0.8b kev-4b kev-9b simple-jev laya-multilingual gliner2.5-decide gliner2.5-multi-decide; do
  ssh 192.168.0.90 "cd /var/opt/docker/ai/decision-models-next && sudo docker compose up -d $model"
  trap 'ssh 192.168.0.90 "cd /var/opt/docker/ai/decision-models-next && sudo docker compose stop $model"' EXIT INT TERM
  mkdir -p "$bench_dir/results/next-wave-smoke/$model"
  ssh 192.168.0.90 "sudo docker inspect --format '{{json .Image}} {{json .Config.Cmd}} {{json .Mounts}}' dm-$model" > "$bench_dir/results/next-wave-smoke/$model/container.txt"
  docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges:true --tmpfs /tmp --user "$(id -u):$(id -g)" -v "$bench_dir:/work:ro" -v "$bench_dir/results:/results" jev-benchmark-runner /work/next-wave/smoke.py "$model" "$port"
  ssh 192.168.0.90 "cd /var/opt/docker/ai/decision-models-next && sudo docker compose stop $model"
  trap - EXIT INT TERM
  port=$((port+1))
done

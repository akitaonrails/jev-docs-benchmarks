"""Host standard-library lifecycle controller; all inference clients run in Docker."""
import argparse
import json
from pathlib import Path
import subprocess
import os
import sys

BENCH = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((BENCH/'next-wave/models.json').read_text())
REMOTE = 'cd /var/opt/docker/ai/decision-models-next && sudo docker compose '


def ssh(command):
    return subprocess.check_output(['ssh', '192.168.0.90', command], text=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--models', nargs='+', choices=REGISTRY, default=list(REGISTRY))
    p.add_argument('--datasets', nargs='+', choices=['v1', 'v2'], default=['v2', 'v1'])
    p.add_argument('--limit', type=int, default=0)
    p.add_argument('--execute', action='store_true')
    args = p.parse_args()
    if not args.execute:
        p.error('Requires --execute')
    docker = ['docker', 'run', '--rm', '--read-only', '--cap-drop', 'ALL',
              '--security-opt', 'no-new-privileges:true', '--tmpfs', '/tmp',
              '--user', f'{os.getuid()}:{os.getgid()}', '-v', f'{BENCH}:/work:ro',
              '-v', f'{BENCH}/results:/results', '-v', f'{BENCH}/reports:/reports',
              'jev-benchmark-runner']
    for model in args.models:
        running = ssh("sudo docker ps --format '{{.Names}}'").splitlines()
        if any(n.startswith('dm-') or n == 'decision-models-systemone' for n in running):
            raise RuntimeError('Another benchmark container is active; refuse overlap')
        if model in ('d3', 'd3-edge'):
            memory = ssh('cat /sys/class/drm/card*/device/mem_info_vram_used')
            if max(int(n) for n in memory.split()) >= 8*2**30:
                raise RuntimeError('GPU has another substantial tenant; leave it untouched')
        print('START', model, flush=True)
        try:
            ssh(REMOTE + 'up -d ' + model)
            template = '{"image":{{json .Image}},"command":{{json .Config.Cmd}}}'
            provenance = json.loads(ssh(f"sudo docker inspect --format '{template}' dm-{model}"))
            running = ssh("sudo docker ps --format '{{.Names}}'").splitlines()
            provenance['running_benchmark_containers'] = sorted(n for n in running if n.startswith('dm-') or n=='decision-models-systemone')
            for dataset in args.datasets:
                if dataset == 'v1' and model.startswith('gliner'):
                    continue  # GLiNER has no native probability probes; separate v2 choice-only track.
                folder = f'next-wave-{dataset}' + ('-smoke' if args.limit else '')
                result = BENCH/'results'/folder/model
                result.mkdir(parents=True, exist_ok=True)
                (result/'container.json').write_text(json.dumps(provenance, indent=2)+'\n')
                deps = ssh(f'sudo docker exec dm-{model} cat /opt/resolved-deps-full.txt')
                (result/'resolved-deps.txt').write_text(deps)
                dataset_dir = 'expansion-v2' if dataset=='v2' else 'datasets'
                with (result/'execution.log').open('a') as log:
                    subprocess.run(docker + ['/work/tools/next_wave.py', '--model', model,
                        '--dataset', '/work/'+dataset_dir, '--output', f'/results/{folder}/{model}',
                        '--limit', str(args.limit), '--execute'], stdout=log, stderr=subprocess.STDOUT, check=True)
                if not args.limit:
                    subprocess.run(docker + ['/work/tools/archive.py', f'/results/{folder}/{model}',
                                             f'/reports/{folder}/{model}'], check=True)
                    report = BENCH/'reports'/folder/model
                    for name in ['container.json', 'resolved-deps.txt', 'warmup.json']:
                        (report/name).write_bytes((result/name).read_bytes())
                    for name in ['health-before.json', 'health-after.json']:
                        if (result/name).exists():
                            (report/name).write_bytes((result/name).read_bytes())
        finally:
            ssh(REMOTE + 'stop ' + model)
            print('STOP', model, flush=True)


if __name__=='__main__':
    main()

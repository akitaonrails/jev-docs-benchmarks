"""Remove only the explicitly inventoried runtime resources from this CUDA experiment."""
import argparse
import json
from runtime import require_local_docker
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def output(*args):return subprocess.check_output(['docker',*args],text=True)

def main():
    require_local_docker()
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--output',default=str(ROOT/'results/cuda-cleanup.json'));a=p.parse_args()
    inventory=ROOT/'results/cuda-resources.json'
    if not inventory.exists():inventory=ROOT/'reports/cuda-runtime/resources.json'
    manifest=json.loads(inventory.read_text())
    registry=json.loads((ROOT/'cuda/models.json').read_text())
    allowed_volumes={x['volume'] for x in registry.values()}
    allowed_images={'jev-cuda-'+x['group'] for x in registry.values()} | {'jev-cuda-rebuild-check'}
    assert set(manifest['volumes'])<=allowed_volumes
    assert set(manifest['images'])<=allowed_images
    ids=manifest['build_cache_ids']
    assert all(re.fullmatch('[a-z0-9]+',i) for i in ids)
    running=output('ps','--format','{{.Names}}').splitlines()
    if any(n.startswith('jev-cuda-') for n in running):raise RuntimeError('Stop active test runs before cleanup')
    print(json.dumps(manifest,indent=2))
    if not a.execute:return
    removed=json.loads(Path(a.output).read_text()).get('removed',[]) if Path(a.output).exists() else []
    stopped=set(output('ps','-a','--format','{{.Names}}').splitlines())
    for name in sorted({r['container_name'] for r in registry.values()} & stopped):
        subprocess.run(['docker','rm',name],check=True)
        removed.append(name)
    if manifest.get('builder_name'):
        assert manifest['builder_name']=='jev-cuda-benchmark'
        subprocess.run(['docker','buildx','rm',manifest['builder_name']],check=True)
        removed.append(manifest['builder_name'])
    existing_tags=set(output('image','ls','--format','{{.Repository}}').splitlines())
    for name in manifest['images']:
        if name not in existing_tags:continue
        existing=json.loads(output('image','inspect',name))[0]['Id']
        if existing!=manifest['images'][name]:raise RuntimeError('Image was replaced; refuse cleanup '+name)
        subprocess.run(['docker','image','rm',name],check=True);removed.append(name)
    existing_volumes=set(output('volume','ls','--format','{{.Name}}').splitlines())
    for name in manifest['volumes']:
        if name not in existing_volumes:continue
        subprocess.run(['docker','volume','rm',name],check=True);removed.append(name)
    history=manifest.get('build_history_refs',[])
    assert all(re.fullmatch(r'default/default/[a-z0-9]+',ref) for ref in history)
    if history:
        present={r['ref'] for r in map(json.loads,output('buildx','history','ls','--builder','default','--format','json').splitlines())}
        refs=[ref for ref in history if ref in present]
        if refs:subprocess.run(['docker','buildx','history','rm','--builder','default',*[ref.rsplit('/',1)[-1] for ref in refs]],check=True)
    if ids:
        subprocess.run(['docker','buildx','prune','--builder','default','--force','--filter','id~=^('+ '|'.join(ids)+')$'],check=True)
    cache=[json.loads(line) for line in output('buildx','du','--builder','default','--format','{{json .}}').splitlines()]
    remaining_ids=sorted(set(ids)&{row['ID'] for row in cache})
    after={'remaining_owned_cache_ids':remaining_ids,'removed':removed,'remaining_benchmark_containers':[n for n in output('ps','-a','--format','{{.Names}}').splitlines() if n.startswith('jev-cuda-')],
           'remaining_images':output('image','ls','--filter','reference=jev-cuda-*','--format','{{.Repository}}'),
           'remaining_volumes':output('volume','ls','--filter','name=jev_cuda_','--format','{{.Name}}'),
           'gpu':subprocess.check_output(['nvidia-smi'],text=True)}
    Path(a.output).write_text(json.dumps(after,indent=2)+'\n')
    if remaining_ids or after['remaining_images'].strip() or after['remaining_volumes'].strip():raise RuntimeError('Benchmark resources remain')

if __name__=='__main__':main()

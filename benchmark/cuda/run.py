"""Sequential isolated CUDA lifecycle. Host uses only Python standard library."""
import argparse
import hashlib
import json
from runtime import require_local_docker
import os
import sys
from pathlib import Path
import shutil
import subprocess
import time
import fcntl
import signal
import re
from verify import verify

ROOT=Path(__file__).resolve().parents[1]

def capture(args):return subprocess.check_output(args,text=True)

def archive_complete(root, run_id, model, dataset, config):
    report=root/'reports'/(run_id+'-'+dataset)/model/'archive.json'
    if not report.exists():return False
    local=root/'results'/(run_id+'-'+dataset)/model
    if not (local/'responses.jsonl').exists() or not (local/'run.json').exists():
        raise RuntimeError('Published archive exists; choose a fresh --run-id to preserve it')
    if json.loads((local/'run.json').read_text())['config']['registry']!=config:
        raise RuntimeError('Deployment changed; choose a fresh --run-id')
    if hashlib.sha256((local/'responses.jsonl').read_bytes()).hexdigest()!=json.loads(report.read_text())['raw_sha256']:
        raise RuntimeError('Local responses differ from archive; inspect before resuming')
    return True


def main():
    signal.signal(signal.SIGTERM,lambda signum,frame:sys.exit('Controller terminated'))
    require_local_docker()
    registry=json.loads((ROOT/'cuda/models.json').read_text())
    lock=(ROOT/'results/cuda-controller.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    p=argparse.ArgumentParser()
    p.add_argument('--models',nargs='+',choices=registry,default=list(registry))
    p.add_argument('--datasets',nargs='+',choices=['v1','v2'],default=['v2','v1'])
    p.add_argument('--limit',type=int,default=0)
    p.add_argument('--run-id',default='cuda',help='Output prefix; use a new ID to preserve published archives')
    p.add_argument('--execute',action='store_true')
    a=p.parse_args()
    if not a.execute:p.error('Requires --execute')
    if not re.fullmatch(r'cuda(?:-[a-z0-9]+)*',a.run_id):p.error('Run ID must be cuda or cuda-<letters/digits>')
    for volume in sorted({registry[m]['volume'] for m in a.models}):
        subprocess.run(['docker','run','--rm','-v',volume+':/models:ro','python:3.12-slim','test','-f','/models/.transfer-complete'],check=True)
    client=['docker','run','--rm','--network','host','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges:true','--tmpfs','/tmp','--user',f'{os.getuid()}:{os.getgid()}',
            '-v',f'{ROOT}:/work:ro','-v',f'{ROOT}/results:/results','-v',f'{ROOT}/reports:/reports','jev-benchmark-runner']
    for model in a.models:
        datasets=[d for d in a.datasets if not (d=='v1' and model.startswith('gliner'))]
        completed=[archive_complete(ROOT,a.run_id,model,d,registry[model]) for d in datasets] if not a.limit else []
        if completed and all(completed):
            print('SKIP archived',model,flush=True)
            continue
        cfg=registry[model]; name=cfg['container_name']
        verify(cfg['volume'].removeprefix('jev_cuda_'))
        running=capture(['docker','ps','--format','{{.Names}}']).splitlines()
        if any(n.startswith('jev-cuda-') for n in running):raise RuntimeError('Another CUDA benchmark is active')
        compute=capture(['nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv,noheader']).strip()
        if compute:raise RuntimeError('Another compute workload is active: '+compute)
        command=['docker','run','-d','--name',name,'--device','nvidia.com/gpu=all','--device','/dev/nvidia-uvm','--device','/dev/nvidia-uvm-tools','-v','/dev/nvidia-uvm:/dev/nvidia-uvm','-v','/dev/nvidia-uvm-tools:/dev/nvidia-uvm-tools','--network','host',
                 '--read-only','--cap-drop','ALL','--security-opt','no-new-privileges:true','--tmpfs','/tmp:exec,size=8g','--shm-size','2g',
                 '-v',cfg['volume']+':/models:ro','-e','HF_HOME=/models/hf','-e','HF_HUB_OFFLINE=1']
        # Native servers bind 8000; use bridge publishing so all models keep their frozen command.
        i=command.index('--network');del command[i:i+2]
        command+=['-p','127.0.0.1:11500:8000']
        if cfg.get('working_dir'):command+=['-w',cfg['working_dir']]
        command += [cfg['image']]+cfg['command']
        print('START',model,flush=True)
        try:
            subprocess.run(command,check=True)
            inspect=json.loads(capture(['docker','inspect',name]))[0]
            provenance={'image':inspect['Image'],'command':inspect['Config']['Cmd'],'running_benchmark_containers':[name],
                        'backend':'cuda','hardware':capture(['nvidia-smi','-q']), 'host_cpu':capture(['lscpu'])}
            for dataset in a.datasets:
                if dataset=='v1' and model.startswith('gliner'):continue
                folder=a.run_id+'-'+dataset+('-smoke' if a.limit else '')
                out=ROOT/'results'/folder/model;out.mkdir(parents=True,exist_ok=True)
                (out/'container.json').write_text(json.dumps(provenance,indent=2)+'\n')
                (out/'resolved-deps.txt').write_text(capture(['docker','exec',name,'cat','/opt/resolved-deps-full.txt']))
                subprocess.run(client+['/work/tools/next_wave.py','--registry','/work/cuda/models.json','--model',model,'--dataset','/work/'+('expansion-v2' if dataset=='v2' else 'datasets'),'--output',f'/results/{folder}/{model}','--limit',str(a.limit),'--execute'],check=True)
                if not a.limit:
                    (out/'runtime-after.json').write_text(json.dumps({'gpu':capture(['nvidia-smi','--query-gpu=memory.used,utilization.gpu,power.draw,temperature.gpu','--format=csv']), 'container':capture(['docker','stats','--no-stream','--format','{{json .}}',name])},indent=2)+'\n')
                    subprocess.run(client+['/work/tools/archive.py',f'/results/{folder}/{model}',f'/reports/{folder}/{model}'],check=True)
                    for f in out.iterdir():
                        if f.name in ('container.json','resolved-deps.txt','warmup.json','health-before.json','health-after.json','runtime-after.json'):
                            shutil.copyfile(f,ROOT/'reports'/folder/model/f.name)
        finally:
            logged=subprocess.run(['docker','logs',name],capture_output=True,text=True)
            log=logged.stdout+logged.stderr
            logdir=ROOT/'results'/'cuda-setup';logdir.mkdir(exist_ok=True)
            (logdir/(model+'.log')).write_text(log)
            subprocess.run(['docker','rm','-f',name],check=True)
            print('STOP',model,flush=True)

if __name__=='__main__':main()

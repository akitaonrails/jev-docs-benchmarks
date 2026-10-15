"""Copy pinned homelab caches to local Docker volumes; no remote inference or host pip."""
import argparse
import json
from runtime import require_local_docker
import shlex
import subprocess

VOLUMES=['d3_edge','julia1','hf','eikos4b','jebadiah4b','kev','simplejev','decider','layaml','gliner']


def main():
    require_local_docker()
    p=argparse.ArgumentParser()
    p.add_argument('--host',default='192.168.0.90')
    p.add_argument('--volumes',nargs='+',choices=VOLUMES,default=VOLUMES)
    args=p.parse_args()
    for suffix in args.volumes:
        target='jev_cuda_'+suffix
        existing=subprocess.check_output(['docker','volume','ls','--format','{{.Name}}'],text=True).splitlines()
        if target in existing:
            marker=subprocess.run(['docker','run','--rm','-v',target+':/models:ro','python:3.12-slim','test','-f','/models/.transfer-complete'])
            if marker.returncode:raise RuntimeError(f'{target} exists without completion marker; verify or remove before retrying')
            print('SKIP completed',target,flush=True)
            continue
        source='decision_models_'+suffix
        mount=json.loads(subprocess.check_output(['ssh',args.host,'sudo docker volume inspect '+source]))[0]['Mountpoint']
        temp=subprocess.check_output(['ssh',args.host,'mktemp -d /var/tmp/jev-cuda-XXXXXXXX'],text=True).strip()
        archive=temp+'/models.tar'
        subprocess.run(['docker','volume','create','--label','project=jev-cuda-benchmark',target],check=True)
        try:
            # Avoid sudo PTY binary-stream throttling: stage, then stream as the ordinary SSH user.
            subprocess.run(['ssh',args.host,'sudo tar -C '+shlex.quote(mount)+' -cf '+shlex.quote(archive)+' . && sudo chmod 644 '+shlex.quote(archive)],check=True)
            producer=subprocess.Popen(['ssh',args.host,'cat '+shlex.quote(archive)],stdout=subprocess.PIPE)
            consumer=subprocess.run(['docker','run','--rm','-i','-v',target+':/models','python:3.12-slim','tar','-C','/models','-xf','-'],stdin=producer.stdout)
            producer.stdout.close()
            code=producer.wait()
            if code or consumer.returncode:raise RuntimeError(f'Incomplete transfer: remove {target} and retry')
            subprocess.run(['docker','run','--rm','-v',target+':/models','python:3.12-slim','touch','/models/.transfer-complete'],check=True)
            print('COPIED',source,target,flush=True)
        finally:
            subprocess.run(['ssh',args.host,'sudo rm -f -- '+shlex.quote(archive)+'; rmdir -- '+shlex.quote(temp)],check=True)

if __name__=='__main__':main()

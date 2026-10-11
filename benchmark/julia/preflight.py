"""Host stdlib lifecycle for unscored Julia checks; checks execute in Docker."""
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile

BENCH=Path(__file__).resolve().parents[1]
REMOTE='cd /var/opt/docker/ai/decision-models-next && sudo docker compose '

def ssh(command):return subprocess.check_output(['ssh','192.168.0.90',command])

snapshot='/var/lib/docker/volumes/decision_models_julia1/_data/hf/hub/models--SupersonicLabs--Julia-1/snapshots/a85b127321d580d65176c89ced8273f305745d85/'
hashes=ssh('sudo sha256sum '+snapshot+'model.safetensors '+snapshot+'tokenizer/tokenizer.json').decode()
assert hashes.splitlines()[0].split()[0]=='df853bf7fe424420011f3d0c47a05d7341aa9eefa7fb9f203ea4aada4ad95b72'
assert hashes.splitlines()[1].split()[0]=='609d8f4c067cd3950f88594c5a802616cea245823836ef5848ee4fc40aab5b6f'
(BENCH/'reports/julia-runtime/checkpoint-sha256.txt').write_text(hashes)
image=subprocess.check_output(['docker','image','inspect','jev-benchmark-runner','--format','{{.Id}}'],text=True).strip()
(BENCH/'reports/julia-runtime/client-image.json').write_text(json.dumps({'image':image},indent=2)+'\n')
for model in ['julia-1','julia-1-cpu']:
    running=ssh("sudo docker ps --format '{{.Names}}'").decode().splitlines()
    assert not any(n.startswith('dm-') or n=='decision-models-systemone' for n in running)
    source=ssh('sudo docker cp dm-'+model+':/opt/julia/julia_app.py -')
    with tarfile.open(fileobj=io.BytesIO(source)) as tar:
        member=next(m for m in tar.getmembers() if m.isfile())
        assert tar.extractfile(member).read()==(BENCH/'julia/server/julia_app.py').read_bytes()
    try:
        ssh(REMOTE+'up -d '+model)
        subprocess.run(['docker','run','--rm','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges:true',
                        '--tmpfs','/tmp','--user',f'{os.getuid()}:{os.getgid()}',
                        '-v',f'{BENCH}:/work:ro','-v',f'{BENCH}/reports:/reports','jev-benchmark-runner',
                        '/work/julia/check.py','--model',model,'--output',f'/reports/julia-runtime/{model}'],check=True)
    finally:ssh(REMOTE+'stop '+model)

"""Host stdlib orchestration; verification and inference clients stay in Docker."""
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
BENCH=Path(__file__).resolve().parents[1]
MODEL='pplx-decider-27b'
REMOTE='cd /var/opt/docker/ai/decision-models-next && sudo docker compose '
def ssh(command):return subprocess.check_output(['ssh','192.168.0.90',command])
reg=json.loads((BENCH/'next-wave/models.json').read_text())[MODEL]
ins=json.loads(ssh('sudo docker inspect dm-'+MODEL))[0]
assert ins['Image']==reg['image'] and ins['Config']['Cmd']==reg['command']
assert len(ins['Mounts'])==1 and ins['Mounts'][0]['RW'] is False
source=ssh('sudo docker cp dm-'+MODEL+':/opt/pplx/run_pplx.py -')
with tarfile.open(fileobj=io.BytesIO(source)) as tar:
    member=next(m for m in tar.getmembers() if m.isfile())
    assert tar.extractfile(member).read()==(BENCH/'perplexity/server/run_pplx.py').read_bytes()
# Hash verification needs no GPU; a separate short-lived container survives service shutdown.
snapshot='/models/hf/hub/models--perplexity-ai--pplx-decider-v1.1-27b/snapshots/6195aa55a72ae21e503c8a60198f7b390d42adb5'
command=('sudo docker run --rm -i --network none --read-only --cap-drop ALL '
         '--security-opt no-new-privileges:true -v decision_models_pplx:/models:ro '
         '--entrypoint python '+reg['image']+' - '+snapshot)
verified=subprocess.check_output(['ssh','192.168.0.90',command],input=(BENCH/'perplexity/verify_manifest.py').read_bytes())
assert json.loads(verified)['verified']==46
(BENCH/'reports/perplexity-runtime/manifest-verification.json').write_bytes(verified)
running=ssh("sudo docker ps --format '{{.Names}}'").decode().splitlines()
assert not any(n.startswith('dm-') or n=='decision-models-systemone' for n in running)
# Physical GPU headroom, not merely the absence of benchmark containers.
mem=ssh('cat /sys/class/drm/card*/device/mem_info_vram_used').decode()
assert max(int(n) for n in mem.split())<8*2**30,'GPU has another substantial tenant'
(BENCH/'reports/perplexity-runtime/gpu-memory-before.txt').write_text(mem)
try:
    ssh(REMOTE+'up -d '+MODEL)
    subprocess.run(['docker','run','--rm','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges:true',
                    '--tmpfs','/tmp','--user',f'{os.getuid()}:{os.getgid()}',
                    '-v',f'{BENCH}:/work:ro','-v',f'{BENCH}/reports:/reports','jev-benchmark-runner',
                    '/work/perplexity/check.py'],check=True)
finally:ssh(REMOTE+'stop '+MODEL)

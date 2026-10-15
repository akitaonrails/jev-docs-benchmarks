"""Compare every snapshot file's SHA-256 with the original homelab volume."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
VERIFIED=set()
CODE='''import hashlib,json,pathlib,sys
root=pathlib.Path(sys.argv[1]); result={}
for p in sorted(root.glob("hf/hub/models--*/snapshots/*/**/*")):
 if p.is_file() and "__pycache__" not in p.parts:
  h=hashlib.sha256()
  with p.open("rb") as f:
   for chunk in iter(lambda:f.read(8*1024*1024),b""):h.update(chunk)
  result[str(p.relative_to(root))]=h.hexdigest()
print(json.dumps(result,sort_keys=True))
'''

def verify(suffix):
    out=ROOT/'reports'/'cuda-runtime'/('weights-'+suffix+'.json')
    if suffix in VERIFIED:return
    if out.exists():
        local=json.loads(subprocess.check_output(['docker','run','--rm','-v','jev_cuda_'+suffix+':/models:ro','python:3.12-slim','python','-c',CODE,'/models']))
        if local!=json.loads(out.read_text())['files']:raise RuntimeError('Local snapshot changed: '+suffix)
        VERIFIED.add(suffix)
        return
    source='decision_models_'+suffix
    mount=json.loads(subprocess.check_output(['ssh','192.168.0.90','sudo docker volume inspect '+source]))[0]['Mountpoint']
    remote=json.loads(subprocess.check_output(['ssh','192.168.0.90','sudo python3 -c '+shlex.quote(CODE)+' '+shlex.quote(mount)]))
    local=json.loads(subprocess.check_output(['docker','run','--rm','-v','jev_cuda_'+suffix+':/models:ro','python:3.12-slim','python','-c',CODE,'/models']))
    if not remote or local!=remote:raise RuntimeError('Snapshot content mismatch: '+suffix)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'source_volume':source,'local_volume':'jev_cuda_'+suffix,'all_snapshot_files_match':True,'files':local},indent=2)+'\n')
    VERIFIED.add(suffix)
    print('VERIFIED',suffix,len(local),flush=True)

if __name__=='__main__':
    for suffix in sys.argv[1:]:verify(suffix)

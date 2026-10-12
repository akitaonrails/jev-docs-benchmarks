"""Host stdlib controller for CPU-only remote manifest/token verification."""
import json,subprocess,shlex,hashlib
from pathlib import Path
BENCH=Path(__file__).resolve().parents[1]
reg=json.loads((BENCH/'next-wave/models.json').read_text())
for name in ('d3-edge','d3'):
 c=reg[name];env=dict(x.split('=',1) for x in c['command'][1:-2])
 cases=[]
 for version,directory in [('v1','datasets'),('v2','expansion-v2')]:
  for line in (BENCH/directory/'cases.jsonl').read_text().splitlines():
   row=json.loads(line);req={**row['request'],'model':c['selector']}
   cases.append({'version':version,'case_id':row['id'],'request':req,'request_sha256':hashlib.sha256(json.dumps(req,sort_keys=True,ensure_ascii=False).encode()).hexdigest()})
 source=(BENCH/'decision3/encode.py').read_text()
 boot='import sys,json; INPUT=json.load(sys.stdin); exec(compile(INPUT["script"],"encode.py","exec"))'
 volume='decision_models_d3_edge' if name=='d3-edge' else 'decision_models_d3'
 command='sudo docker run --rm -i --network none --read-only --cap-drop ALL --security-opt no-new-privileges:true --tmpfs /tmp -v '+volume+':/models:ro --entrypoint python '+c['image']+' -c '+shlex.quote(boot)+' '+shlex.quote(env['D3_MODEL_PATH'])
 print('VERIFY',name,flush=True)
 output=subprocess.check_output(['ssh','192.168.0.90',command],input=json.dumps({'script':source,'cases':cases}).encode())
 evidence=json.loads(output)
 folder=BENCH/'reports/decision3-runtime';folder.mkdir(exist_ok=True)
 (folder/f'{name}-encoding.json').write_bytes(output)
 print(name,evidence['manifest_files_verified'],'files;',evidence['min_tokens'],evidence['max_tokens'],'tokens',flush=True)

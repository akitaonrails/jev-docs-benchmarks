"""Run in the pinned server image, CPU only; verify files and complete encodings."""
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root))
from d3_runtime import D3,verify_package
from transformers import AutoTokenizer
manifest=verify_package(root,'full')
m=D3.__new__(D3);m.tokenizer=AutoTokenizer.from_pretrained(root,local_files_only=True)
m.prompt='d3';m.codes=json.loads((root/'decision_config.json').read_text())['codes'];m.max_length=8192;m.permutation_average=False
records=[]
for item in INPUT['cases']:
 req=item['request'];prepared=m.prepare(req['state'],req['questions'])
 assert not prepared.errors,prepared.errors
 tokens=sum(len(s) for s in prepared.sequences.values())
 records.append({**{k:item[k] for k in ('version','case_id','request_sha256')},'input_tokens':tokens})
negative=m.prepare('word '*20000,{'decision':{'type':'noul','instructions':'Is there text?'}})
assert negative.errors['decision']['error']=='max_length_exceeded'
print(json.dumps({'manifest_files_verified':len(manifest['files_sha256']),'manifest_sha256':hashlib.sha256((root/'MODEL_MANIFEST.json').read_bytes()).hexdigest(),'records':records,'min_tokens':min(r['input_tokens'] for r in records),'max_tokens':max(r['input_tokens'] for r in records),'overflow_control':negative.errors},indent=2))

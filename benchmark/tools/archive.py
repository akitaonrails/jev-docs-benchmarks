"""Archive a completed run without credentials; deterministic gzip for raw records."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil

p=argparse.ArgumentParser();p.add_argument('run_dir');p.add_argument('report_dir');a=p.parse_args()
source=Path(a.run_dir);target=Path(a.report_dir);target.mkdir(parents=True,exist_ok=True)
raw=(source/'responses.jsonl').read_bytes()
rows=[json.loads(x) for x in raw.splitlines()]
config=json.loads((source/'run.json').read_text())['config']
manifest=json.loads((Path(__file__).resolve().parents[1]/'datasets/manifest.json').read_text())
expected=config['limit'] or manifest['classification_cases']+manifest['probability_probes']
if len(rows)!=expected*len(config['models']):
    raise SystemExit('Refusing to archive incomplete run as completed')
if len({(r['model'],r['case_id']) for r in rows})!=len(rows):raise SystemExit('Duplicate responses')
(target/'responses.jsonl.gz').write_bytes(gzip.compress(raw,mtime=0))
for filename in ['run.json','docker-image-id.txt']:
    if (source/filename).exists():shutil.copyfile(source/filename,target/filename)
(target/'archive.json').write_text(json.dumps({'raw_sha256':hashlib.sha256(raw).hexdigest(),
    'response_records':len(rows),'dataset_sha256':manifest['sha256'],
    'first_timestamp':min(r['timestamp'] for r in rows),
    'last_timestamp':max(r['timestamp'] for r in rows)},indent=2)+'\n')
print('Archived',len(rows),'records to',target)

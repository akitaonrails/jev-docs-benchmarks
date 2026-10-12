"""Verify frozen Decision 3.0 outputs and unchanged historical scores, offline."""
import gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from hosted import load_cases,digest
from next_contract import request_for,REGISTRY,verify_health
out=Path('/reports/decision3-comparison-v2')
report={}
for model in ('d3','d3-edge'):
 report[model]={}
 encoding=json.loads((ROOT/REGISTRY[model]['encoding_evidence']).read_text())
 enc={r['request_sha256']:r['input_tokens'] for r in encoding['records']}
 for version in ('v1','v2'):
  old=json.loads((ROOT/f'reports/microsoft-comparison-{version}/summary.json').read_text())['models']
  new=json.loads((ROOT/f'reports/decision3-comparison-{version}/summary.json').read_text())['models']
  assert all(new[m]==v for m,v in old.items()),'Historical metrics changed'
  folder=ROOT/f'reports/next-wave-{version}/{model}'
  run=json.loads((folder/'run.json').read_text())
  assert run['config']['runner_sha256']==hashlib.sha256((ROOT/'tools/next_wave.py').read_bytes()).hexdigest()
  assert run['config']['contract_sha256']==hashlib.sha256((ROOT/'tools/next_contract.py').read_bytes()).hexdigest()
  raw=gzip.decompress((folder/'responses.jsonl.gz').read_bytes());archive=json.loads((folder/'archive.json').read_text())
  assert hashlib.sha256(raw).hexdigest()==archive['raw_sha256']
  rows=[json.loads(x) for x in raw.splitlines()]
  cases,manifest=load_cases(ROOT/('datasets' if version=='v1' else 'expansion-v2'));cases={c['id']:c for c in cases}
  assert len(rows)==len(cases) and {r['case_id'] for r in rows}==set(cases)
  for r in rows:
   assert r['result'] and not r['error'] and len(r['attempts'])==1
   assert r['dataset_sha256']==manifest['sha256'] and r['model']==model
   h=digest(request_for(cases[r['case_id']],model));assert r['request_sha256']==h
   assert r['result']['usage']['input_tokens']==enc[h]
  for name in ('health-before.json','health-after.json'):verify_health(json.loads((folder/name).read_text()),model)
  x=new[model]
  stats={'records':len(rows),'valid_single_attempt':True,'complete_encoding_verified':True,'archive_request_hashes_verified':True,'previous_metrics_unchanged':True,'health_provenance_verified':True,'served_models':sorted({r['result']['served_model'] for r in rows})}
  if version=='v2':
   g=x['groups'];compact=[g[f'all/{l}/compact'] for l in ('en','pt-BR')]
   stats.update(condition_correct={c:sum(g[f'all/{l}/{c}']['correct'] for l in ('en','pt-BR')) for c in ('compact','examples','distractors')},compact_brier=sum(c['brier_valid_only'] for c in compact)/2,high_confidence_count=sum(c['probability_ge_0_9_count'] for c in compact),high_confidence_errors=sum(round(c['probability_ge_0_9_count']*c['probability_ge_0_9_error_rate']) for c in compact),runtime=x['runtime'])
  else:
   stats.update(original_correct=x['originals']['correct'],all_variants_correct=x['all']['correct'],sensitivity_correct={k:v['correct'] for k,v in x['sensitivity_excluding_disputed'].items()},uncertainty_mae={k:v['mean_absolute_error'] for k,v in x['uncertainty'].items()},policy_pairs=x['policy_pairs'],invariance=x['invariance'],critical_originals=x['critical_originals'],runtime=x['operations'])
  report[model][version]=stats
out.mkdir(exist_ok=True,parents=True);(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
# Inspectable errors, preserving meaning when wire labels are opaque.
errors=[]
for model in report:
 for version,directory in [('v1','datasets'),('v2','expansion-v2')]:
  cases={c['id']:c for c in load_cases(ROOT/directory)[0]}
  archive=ROOT/f'reports/next-wave-{version}/{model}/responses.jsonl.gz'
  for line in gzip.decompress(archive.read_bytes()).splitlines():
   r=json.loads(line);c=cases[r['case_id']]
   if 'gold' not in c or 'choice' not in r['result']:continue
   if r['result']['choice']==c['gold']:continue
   if version=='v1' and c.get('variant')!='original':continue
   if version=='v2' and c.get('condition')!='compact':continue
   errors.append({'model':model,'version':version,'id':c['id'],'expected':c['semantic_gold'],'predicted':c['semantic_map'][r['result']['choice']],'probability':max(r['result']['probabilities'].values()),'state':c['request']['state'],'question':c['request']['questions']['decision']})
(out/'selected-errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2)+'\n')
agreement={}
for version,directory in [('v1','datasets'),('v2','expansion-v2')]:
 cases=[c for c in load_cases(ROOT/directory)[0] if c['kind']=='classification']
 by_model={}
 for model in ('d3','pplx-decider-27b'):
  raw=gzip.decompress((ROOT/f'reports/next-wave-{version}/{model}/responses.jsonl.gz').read_bytes())
  by_model[model]={r['case_id']:r for r in map(json.loads,raw.splitlines())}
 agreement[version]={'classifications':len(cases),'matching_labels':sum(by_model['d3'][c['id']]['result']['choice']==by_model['pplx-decider-27b'][c['id']]['result']['choice'] for c in cases)}
report['d3_perplexity_classification_agreement']=agreement
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(agreement,indent=2))

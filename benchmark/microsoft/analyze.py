"""Verify Microsoft archives, prior scores and usage arithmetic offline."""
import gzip
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from hosted import load_cases,payload,digest
MODEL='microsoft-decision-1'
report={}
for version in ('v1','v2'):
    old=json.loads((ROOT/f'reports/perplexity-comparison-{version}/summary.json').read_text())
    new=json.loads((ROOT/f'reports/microsoft-comparison-{version}/summary.json').read_text())
    assert all(new['models'][m]==v for m,v in old['models'].items()),'Previous scores changed'
    folder=ROOT/f'reports/microsoft-{version}'
    raw=gzip.decompress((folder/'responses.jsonl.gz').read_bytes())
    archive=json.loads((folder/'archive.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==archive['raw_sha256']
    rows=[json.loads(x) for x in raw.splitlines()]
    cases,manifest=load_cases(ROOT/('datasets' if version=='v1' else 'expansion-v2'))
    by_id={c['id']:c for c in cases}
    assert len(rows)==len(cases) and {r['case_id'] for r in rows}==set(by_id)
    for r in rows:
        assert r['model']==MODEL and r['result'] and not r['error']
        assert r['dataset_sha256']==manifest['sha256']
        assert r['request_sha256']==digest(payload(by_id[r['case_id']],MODEL))
        usage=r['result']['usage']
        assert D(str(usage['cost']))==D(usage['input_tokens'])*D('0.000000042')
    tokens=sum(r['result']['usage']['input_tokens'] for r in rows)
    cost=sum(D(str(r['result']['usage']['cost'])) for r in rows)
    x=new['models'][MODEL]
    stats={'records':len(rows),'attempts':sum(len(r['attempts']) for r in rows),'retried_requests':sum(len(r['attempts'])>1 for r in rows),'retry_statuses':sorted({a.get('status') for r in rows for a in r['attempts'][:-1]}),'previous_models_unchanged':True,'archive_and_request_hashes_verified':True,'input_tokens':tokens,'reported_cost_usd':str(cost),'all_usage_costs_match_rate':True,'served_models':sorted({r['result']['served_model'] for r in rows}),'providers':sorted({r['response']['provider'] for r in rows})}
    if version=='v2':
        g=x['groups'];compact=[g[f'all/{l}/compact'] for l in ('en','pt-BR')]
        stats.update(compact_correct=sum(c['correct'] for c in compact),compact_brier=sum(c['brier_valid_only'] for c in compact)/2,condition_correct={c:sum(g[f'all/{l}/{c}']['correct'] for l in ('en','pt-BR')) for c in ('compact','examples','distractors')})
        compact_rows=[r for r in rows if by_id[r['case_id']]['condition']=='compact']
        stats['compact_cost_per_1000_usd']=str(sum(D(str(r['result']['usage']['cost'])) for r in compact_rows)*1000/168)
    else:
        stats.update(original_correct=x['originals']['correct'],all_variants_correct=x['all']['correct'],uncertainty_mae={k:v['mean_absolute_error'] for k,v in x['uncertainty'].items()},sensitivity_correct={k:v['correct'] for k,v in x['sensitivity_excluding_disputed'].items()})
    report[version]=stats
report['total_scored_cost_usd']=str(sum(D(report[v]['reported_cost_usd']) for v in ('v1','v2')))
report['total_with_observed_smoke_usd']=str(D(report['total_scored_cost_usd'])+D('0.000002436'))
(Path('/reports/microsoft-comparison-v2/verification.json') if Path('/reports').is_dir() else ROOT/'reports/microsoft-comparison-v2/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

"""Verify new archives and derive focused diagnostics without model calls."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODEL='pplx-decider-27b'
enc=json.loads((ROOT/'reports/perplexity-runtime/encoding.json').read_text())
tokens={r['request_sha256']:r['input_tokens'] for r in enc['records']}
report={}
for version in ('v1','v2'):
    old=json.loads((ROOT/f'reports/julia-comparison-{version}/summary.json').read_text())
    new=json.loads((ROOT/f'reports/perplexity-comparison-{version}/summary.json').read_text())
    assert all(new['models'][m]==values for m,values in old['models'].items()),'Prior model metrics changed'
    folder=ROOT/f'reports/next-wave-{version}/{MODEL}'
    archive=json.loads((folder/'archive.json').read_text())
    raw=gzip.decompress((folder/'responses.jsonl.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==archive['raw_sha256']
    rows=[json.loads(line) for line in raw.splitlines()]
    assert len(rows)==(544 if version=='v1' else 504)
    assert len({r['case_id'] for r in rows})==len(rows)
    expected={r['case_id']:r for r in enc['records'] if r['version']==version}
    assert {r['case_id'] for r in rows}==set(expected)
    assert all(r['request_sha256']==expected[r['case_id']]['request_sha256'] for r in rows)
    assert all(r['result'] and not r['error'] and len(r['attempts'])==1 for r in rows)
    assert all(r['result']['usage']['input_tokens']==tokens[r['request_sha256']] for r in rows)
    x=new['models'][MODEL]
    stats={'records':len(rows),'unique_case_ids':len(rows),'all_valid_single_attempt':True,
           'all_token_counts_match_complete_encoding':True,'previous_models_unchanged':True,
           'archive_sha256_verified':True,'served_models':sorted({r['result']['served_model'] for r in rows})}
    if version=='v2':
        groups=x['groups']
        compact=[groups[f'all/{lang}/compact'] for lang in ('en','pt-BR')]
        stats['compact_correct']=sum(g['correct'] for g in compact)
        stats['compact_brier']=sum(g['brier_valid_only'] for g in compact)/2
        stats['compact_high_confidence_count']=sum(g['probability_ge_0_9_count'] for g in compact)
        stats['compact_high_confidence_errors']=sum(round(g['probability_ge_0_9_count']*g['probability_ge_0_9_error_rate']) for g in compact)
        stats['condition_correct']={c:sum(groups[f'all/{l}/{c}']['correct'] for l in ('en','pt-BR')) for c in ('compact','examples','distractors')}
    else:
        stats['original_correct']=x['originals']['correct']
        stats['all_variants_correct']=x['all']['correct']
        stats['sensitivity_correct']={k:g['correct'] for k,g in x['sensitivity_excluding_disputed'].items()}
        stats['policy_pairs']=x['policy_pairs']
        stats['uncertainty_mae']={k:g['mean_absolute_error'] for k,g in x['uncertainty'].items()}
    report[version]=stats
(ROOT/'reports/perplexity-comparison-v2/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

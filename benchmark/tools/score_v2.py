"""Offline matched-language and task/condition scoring for expansion v2."""
import argparse
from collections import Counter
from decimal import Decimal as D
import gzip
import hashlib
import itertools
import json
from pathlib import Path
from hosted import ROOT, MODELS, load_cases, payload, digest
from score import class_metrics, interval, quantile


def paired(a, b):
    differences = [y - x for x, y in zip(a, b)]
    return {'n': len(a), 'accuracy_b_minus_a': sum(differences)/len(a),
            'bootstrap_95': interval(differences),
            'both_correct': sum(x and y for x,y in zip(a,b)),
            'a_only_correct': sum(x and not y for x,y in zip(a,b)),
            'b_only_correct': sum(not x and y for x,y in zip(a,b)),
            'both_wrong': sum(not x and not y for x,y in zip(a,b))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('archives', nargs='+')
    parser.add_argument('--output', required=True)
    parser.add_argument('--pricing', default=str(ROOT/'pricing/2026-10-10.json'))
    args = parser.parse_args()
    rows, manifest = load_cases(ROOT/'expansion-v2')
    lookup = {c['id']: c for c in rows}
    records = {}
    for directory in args.archives:
        path = Path(directory)
        raw = gzip.decompress((path/'responses.jsonl.gz').read_bytes())
        archive = json.loads((path/'archive.json').read_text())
        assert hashlib.sha256(raw).hexdigest() == archive['raw_sha256']
        config = json.loads((path/'run.json').read_text())['config']
        assert not config['limit'] and config['dataset_sha256'] == manifest['sha256']
        for model in config['models']:
            if model in records: raise ValueError('Duplicate entrant across archives')
            records[model] = {}
        for record in map(json.loads, raw.splitlines()):
            case = lookup[record['case_id']]
            assert record['dataset_sha256'] == manifest['sha256']
            assert record['request_sha256'] == digest(payload(case, record['model']))
            target = records[record['model']]
            assert record['case_id'] not in target
            target[record['case_id']] = record
        for model in config['models']: assert len(records[model]) == len(rows)
    prices = json.loads(Path(args.pricing).read_text())
    out = {'dataset': manifest, 'pricing': prices, 'models': {}, 'paired_models_compact': {}}
    correctness = {}
    for model, recs in records.items():
        correctness[model] = {c['id']: int(bool(recs[c['id']]['result']) and recs[c['id']]['result']['choice']==c['gold']) for c in rows}
        groups = {}
        for language in manifest['languages']:
            for condition in manifest['conditions']:
                for domain in ['all'] + manifest['domains']:
                    cases = [c for c in rows if c['language']==language and c['condition']==condition and (domain=='all' or c['domain']==domain)]
                    valid = [recs[c['id']] for c in cases if recs[c['id']]['result']]
                    usages = [r['result']['usage'] for r in valid]
                    tokens = sum(u.get('input_tokens',0) for u in usages)
                    metrics = class_metrics(cases, recs)
                    metrics.update(oracle_majority_baseline=sum(max(Counter(c['semantic_gold'] for c in cases if c['domain']==d).values()) for d in {c['domain'] for c in cases})/len(cases),
                        uniform_baseline=sum(1/len(c['semantic_map']) for c in cases)/len(cases),
                        median_seconds=quantile([r['latency_seconds'] for r in valid],.5),
                        p95_seconds=quantile([r['latency_seconds'] for r in valid],.95),
                        input_tokens=tokens, missing_token_usage=sum('input_tokens' not in u for u in usages),
                        listed_usage_usd=str(D(tokens)*D(prices['input_usd_per_million'][model])/1_000_000) if model in MODELS else None,
                        state_tokens_dropped=sum(u.get('state_tokens_dropped',0) for u in usages) if any('state_tokens_dropped' in u for u in usages) else None,
                        truncated_questions=sum(len(u.get('truncated_questions',[])) for u in usages) if any('truncated_questions' in u for u in usages) else None,
                        truncation_reported=sum(bool(u.get('truncated')) for u in usages),
                        truncation_telemetry_missing=sum('truncated' not in u for u in usages))
                    groups[f'{domain}/{language}/{condition}'] = metrics
        pairs = {}
        for condition in manifest['conditions']:
            for domain in ['all'] + manifest['domains']:
                cases = [c for c in rows if c['language']=='en' and c['condition']==condition and (domain=='all' or c['domain']==domain)]
                other_ids = [c['id'].replace('-en-', '-pt-BR-') for c in cases]
                a = [correctness[model][c['id']] for c in cases]
                b = [correctness[model][key] for key in other_ids]
                pairs[f'{domain}/{condition}'] = paired(a,b)
                pairs[f'{domain}/{condition}']['same_semantic_prediction'] = sum(
                    bool(recs[c['id']]['result']) and bool(recs[key]['result']) and
                    c['semantic_map'][recs[c['id']]['result']['choice']] == lookup[key]['semantic_map'][recs[key]['result']['choice']]
                    for c,key in zip(cases,other_ids))
        valid_records = [r for r in recs.values() if r['result']]
        server_records = [r['response'].get('server', {}) for r in valid_records]
        out['models'][model] = {'groups': groups, 'pt_minus_en': pairs,
            'runtime': {'requests': len(recs), 'valid': len(valid_records),
                'errors': sum(bool(r['error']) for r in recs.values()),
                'attempts': sum(len(r['attempts']) for r in recs.values()),
                'median_seconds': quantile([r['latency_seconds'] for r in valid_records], .5),
                'p95_seconds': quantile([r['latency_seconds'] for r in valid_records], .95),
                'cold_requests': sum(s.get('cold') is True for s in server_records) if any('cold' in s for s in server_records) else None,
                'served_models': sorted({str(r['result']['served_model']) for r in valid_records})}}
    if 'clef-flash' in records and 'clef-flash-local' in records:
        a, b = records['clef-flash'], records['clef-flash-local']
        out['flash_hosted_local_agreement'] = {
            'requests': len(rows),
            'matching_payload_hashes': sum(a[k]['request_sha256'] == b[k]['request_sha256'] for k in a),
            'matching_choices': sum(bool(a[k]['result']) and bool(b[k]['result']) and
                a[k]['result']['choice'] == b[k]['result']['choice'] for k in a),
            'different_case_ids': [k for k in a if a[k]['result'] and b[k]['result'] and
                a[k]['result']['choice'] != b[k]['result']['choice']]}

    for a,b in itertools.combinations(records,2):
        for language in manifest['languages']:
            for domain in ['all']+manifest['domains']:
                cases=[c for c in rows if c['language']==language and c['condition']=='compact' and (domain=='all' or c['domain']==domain)]
                out['paired_models_compact'][f'{b} minus {a}/{domain}/{language}']=paired(
                    [correctness[a][c['id']] for c in cases],[correctness[b][c['id']] for c in cases])
    lines=['# v2 bilingual expansion results','','84 authored families, paired translations, three correlated conditions. Compact is the primary language comparison. Task cells have only 12 families; numerical wins are exploratory.','',
           '| Model | Compact EN | Compact PT-BR | PT minus EN (paired bootstrap 95%) | Examples EN / PT | Distractors EN / PT |',
           '| --- | ---: | ---: | --- | --- | --- |']
    for model,result in out['models'].items():
        g=result['groups']; p=result['pt_minus_en']['all/compact']
        fmt=lambda lang,cond:f"{g[f'all/{lang}/{cond}']['accuracy']:.1%}"
        lines.append(f"| {model} | {fmt('en','compact')} | {fmt('pt-BR','compact')} | {p['accuracy_b_minus_a']:+.1%} [{p['bootstrap_95'][0]:+.1%}, {p['bootstrap_95'][1]:+.1%}] | {fmt('en','examples')} / {fmt('pt-BR','examples')} | {fmt('en','distractors')} / {fmt('pt-BR','distractors')} |")
    for language in manifest['languages']:
        lines += ['',f'## Compact tasks: {language}','','| Task | '+' | '.join(records)+' |','| --- | '+' | '.join('---:' for _ in records)+' |']
        for domain in manifest['domains']:
            lines.append('| '+domain+' | '+' | '.join(f"{out['models'][m]['groups'][f'{domain}/{language}/compact']['accuracy']:.1%}" for m in records)+' |')
    lines += ['','## Input truncation','','| Model | Condition | Reported truncated / valid | Missing truncation telemetry |','| --- | --- | ---: | ---: |']
    for model,result in out['models'].items():
        for condition in manifest['conditions']:
            gs=[result['groups'][f'all/{lang}/{condition}'] for lang in manifest['languages']]
            lines.append(f"| {model} | {condition} | {sum(g['truncation_reported'] for g in gs)}/{sum(g['valid'] for g in gs)} | {sum(g['truncation_telemetry_missing'] for g in gs)} |")
    lines += ['', '## Latency and current hosted usage value', '',
              'All 504 requests/model; conditions have different lengths. Local operating cost is unmeasured. Hosted values use the dated pricing snapshot in summary.json, before any free allowance.', '',
              '| Model | Valid / requests | Median / p95 | Input tokens | Listed usage USD |',
              '| --- | ---: | ---: | ---: | ---: |']
    for model, result in out['models'].items():
        r = result['runtime']
        gs = [g for key, g in result['groups'].items() if key.startswith('all/')]
        cost = str(sum(D(g['listed_usage_usd']) for g in gs)) if model in MODELS else 'Unmeasured'
        missing = sum(g['missing_token_usage'] for g in gs)
        tokens = f"{sum(g['input_tokens'] for g in gs):,}" if not missing else f"Unknown ({missing} responses lack usage)"
        lines.append(f"| {model} | {r['valid']}/{r['requests']} | {r['median_seconds']*1000:.0f} / {r['p95_seconds']*1000:.0f} ms | {tokens} | {cost} |")
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    (output/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
    (output/'results.md').write_text('\n'.join(lines)+'\n')
    errors=[]
    for model,recs in records.items():
        for c in rows:
            if not correctness[model][c['id']]:
                r=recs[c['id']];errors.append({'model':model,'case_id':c['id'],'expected':c['semantic_gold'],
                    'predicted':c['semantic_map'][r['result']['choice']] if r['result'] else None,'error':r['error']})
    (output/'errors.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in errors))
    print('Scored',len(rows),'cases per model across',len(records),'entrants')


if __name__=='__main__': main()

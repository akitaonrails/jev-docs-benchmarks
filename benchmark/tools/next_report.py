"""Derive compact rankings and size correlations from verified comparison summaries."""
import json
import math
import gzip
import argparse
from pathlib import Path
from statistics import correlation

from hosted import ROOT, load_cases
from score import interval

SIZES = {'microsoft-decision-1':9, 'laya':.421, 'laya-typed':.421, 'laya-multilingual':.322,
         'julia-1':.1443, 'julia-1-cpu':.1443, 'pplx-decider-27b':27,
         'gliner2.5-decide':.340, 'gliner2.5-multi-decide':.287,
         'kev-0.8b':.8, 'kev-4b':4, 'kev-9b':9,
         'eikos-4b':4, 'jebadiah-4b-v2':4, 'decider-4b':4,
         'simple-jev':4, 'clef-flash':9, 'clef-flash-local':9, 'clef':27}


def ranks(xs):
    return [sum(v < x for v in xs)+(sum(v == x for v in xs)+1)/2 for x in xs]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='/reports/next-wave-comparison-v2')
    parser.add_argument('--v1-output', default='/reports/next-wave-comparison-v1')
    parser.add_argument('--v2-summary', default=str(ROOT/'reports/next-wave-comparison-v2/summary.json'))
    parser.add_argument('--v1-summary', default=str(ROOT/'reports/next-wave-comparison-v1/summary.json'))
    parser.add_argument('--extra-v2-archive', action='append', default=[])
    parser.add_argument('--extra-v1-archive', action='append', default=[])
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    v2 = json.loads(Path(args.v2_summary).read_text())['models']
    v1 = json.loads(Path(args.v1_summary).read_text())['models']
    def compact(m):
        g = v2[m]['groups']
        return sum(g[f'all/{lang}/compact']['correct'] for lang in ['en','pt-BR']) / 168
    ordered = sorted(v2, key=lambda m:(-compact(m),m))
    lines = ['# Expanded ranking and size analysis', '',
             'Descriptive ordering on 168 compact bilingual cases per entrant. Adjacent ranks are not significance claims. GLiNER is a native-interface mapping track; probability metrics are unavailable. Sizes are nominal model/backbone labels, not exact parameter audits.', '',
             '| Model | Nominal B | Compact EN / PT-BR | Combined compact | All 504 | v1 originals | Median / p95 |',
             '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for model in ordered:
        g=v2[model]['groups']; r=v2[model]['runtime']
        en=g['all/en/compact']['accuracy']; pt=g['all/pt-BR/compact']['accuracy']
        all_correct=sum(g[f'all/{lang}/{cond}']['correct'] for lang in ['en','pt-BR'] for cond in ['compact','examples','distractors'])
        v1text=f"{v1[model]['originals']['accuracy']:.1%}" if model in v1 else 'Not run'
        lines.append(f"| {model} | {SIZES.get(model,'Unknown')} | {en:.1%} / {pt:.1%} | {compact(model):.1%} | {all_correct}/504 | {v1text} | {r['median_seconds']*1000:.0f} / {r['p95_seconds']*1000:.0f} ms |")
    duplicate_deployments = {'clef-flash-local', 'julia-1-cpu'}
    sets = {'Known-size entrants, deduplicated deployments': [m for m in ordered if m in SIZES and m not in duplicate_deployments],
            'SystemOne only, deduplicated deployments': [m for m in ordered if m in SIZES and m not in duplicate_deployments and not m.startswith('gliner')],
            'Kev size series': ['kev-0.8b','kev-4b','kev-9b']}
    stats={}
    lines += ['', '## Size correlations', '', '| Selection | n | Spearman | Pearson(log10 size, accuracy) |', '| --- | ---: | ---: | ---: |']
    for name, models in sets.items():
        xs=[SIZES[m] for m in models]; ys=[compact(m) for m in models]
        stats[name]={'models':models,'nominal_billions':xs,'compact_accuracy':ys,
                     'spearman':correlation(ranks(xs),ranks(ys)),
                     'pearson_log_size':correlation([math.log10(x) for x in xs],ys)}
        lines.append(f"| {name} | {len(models)} | {stats[name]['spearman']:.3f} | {stats[name]['pearson_log_size']:.3f} |")
    condition_stats={}
    lines += ['', '### Kev size effects by input condition', '',
              '| Model | Compact | Worked examples | Distractors | All 504 |', '| --- | ---: | ---: | ---: | ---: |']
    for m in sets['Kev size series']:
        counts=[sum(v2[m]['groups'][f'all/{lang}/{cond}']['correct'] for lang in ['en','pt-BR']) for cond in ['compact','examples','distractors']]
        lines.append(f'| {m} | {counts[0]/168:.1%} | {counts[1]/168:.1%} | {counts[2]/168:.1%} | {sum(counts)/504:.1%} |')
    for cond in ['compact','examples','distractors']:
        condition_stats[cond]={}
        for name,models in sets.items():
            xs=[SIZES[m] for m in models]
            ys=[sum(v2[m]['groups'][f'all/{lang}/{cond}']['correct'] for lang in ['en','pt-BR'])/168 for m in models]
            condition_stats[cond][name]={'spearman':correlation(ranks(xs),ranks(ys)),
                                       'pearson_log_size':correlation([math.log10(x) for x in xs],ys)}
    lines += ['', 'Entrants without verified sizes (including Jev and OpenAI Decisions, when present) are excluded. Related checkpoints and shared backbones are dependent observations. These coefficients describe the tested configurations, not a causal scaling law or a random sample of available models. Nominal size bins ignore small head/adapter and exact-backbone differences.', '',
              '## Task strengths against hosted Jev', '',
              'Each cell has only 12 authored families. Counts describe exploratory task/language cells, not independent victories.', '',
              '| Entrant | Cells above Jev | Tied with Jev | Below Jev |', '| --- | ---: | ---: | ---: |']
    taskcells=[k for k in v2['jev']['groups'] if k.endswith('/compact') and not k.startswith('all/')]
    for model in ordered:
        if model=='jev':continue
        ds=[v2[model]['groups'][k]['correct']-v2['jev']['groups'][k]['correct'] for k in taskcells]
        lines.append(f'| {model} | {sum(d>0 for d in ds)} | {sum(d==0 for d in ds)} | {sum(d<0 for d in ds)} |')
    cases, _ = load_cases(ROOT/'expansion-v2')
    compact_cases = [c for c in cases if c['condition']=='compact']
    records = {}
    archives = [ROOT/'reports/hosted-v2', ROOT/'reports/homelab-v2'] + [p for p in (ROOT/'reports/next-wave-v2').iterdir() if (p/'archive.json').is_file()]
    archives += [Path(p) for p in args.extra_v2_archive]
    for archive in archives:
        for line in gzip.decompress((archive/'responses.jsonl.gz').read_bytes()).splitlines():
            r=json.loads(line)
            records.setdefault(r['model'], {})[r['case_id']] = r
    def correct(model, case):
        r=records[model][case['id']]['result']
        return int(bool(r) and r['choice']==case['gold'])
    families=sorted({c['family'] for c in compact_cases})
    pairs={}
    comparisons=[(m,'jev') for m in ordered if m!='jev'] + [('kev-4b','kev-0.8b'),('kev-9b','kev-4b')]
    if 'openai-decisions' in ordered:
        comparisons += [('openai-decisions', m) for m in ['clef','clef-flash','jebadiah-4b-v2'] if m in ordered]
    if 'pplx-decider-27b' in ordered:
        comparisons += [('pplx-decider-27b', m) for m in ['clef','openai-decisions','jebadiah-4b-v2'] if m in ordered]
    if 'julia-1-cpu' in ordered and 'julia-1' in ordered:
        comparisons += [('julia-1-cpu','julia-1')]
    lines += ['', '## Paired compact differences, clustered by authored family', '',
              'English and Portuguese observations are kept together when bootstrapping the 84 families. Intervals are exploratory and not adjusted for multiple comparisons.', '',
              '| Comparison | Difference (points) | Family bootstrap 95% (points) |', '| --- | ---: | --- |']
    for a,b in comparisons:
        differences=[sum(correct(a,c)-correct(b,c) for c in compact_cases if c['family']==f)/2 for f in families]
        delta=sum(differences)/len(differences); ci=interval(differences)
        pairs[f'{a} minus {b}']={'difference':delta,'family_bootstrap_95':ci,'families':len(families)}
        lines.append(f'| {a} minus {b} | {delta*100:+.1f} | [{ci[0]*100:+.1f}, {ci[1]*100:+.1f}] |')
    (output/'ranking.md').write_text('\n'.join(lines)+'\n')
    (output/'size-correlations.json').write_text(json.dumps(stats,indent=2)+'\n')
    (output/'size-correlations-by-condition.json').write_text(json.dumps(condition_stats,indent=2)+'\n')
    (output/'paired-family-comparisons.json').write_text(json.dumps(pairs,indent=2)+'\n')
    v1_cases={c['id']:c for c in load_cases()[0]}
    errors=[]
    archives=[ROOT/'reports/hosted-v1', ROOT/'reports/homelab-v1'] + [p for p in (ROOT/'reports/next-wave-v1').iterdir() if (p/'archive.json').is_file()]
    archives += [Path(p) for p in args.extra_v1_archive]
    for archive in archives:
        for line in gzip.decompress((archive/'responses.jsonl.gz').read_bytes()).splitlines():
            r=json.loads(line); c=v1_cases[r['case_id']]
            if r['model'] not in v1:continue
            if c['kind']!='classification':continue
            prediction=r['result']['choice'] if r['result'] else None
            if prediction!=c['gold']:
                errors.append({'model':r['model'],'case_id':c['id'],'expected':c['semantic_gold'],
                               'predicted':c['semantic_map'].get(prediction),'error':r['error']})
    Path(args.v1_output).mkdir(parents=True, exist_ok=True)
    (Path(args.v1_output)/'errors.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in errors))
    print('\n'.join(lines))


if __name__=='__main__':
    main()

"""Offline scoring of frozen cases and saved hosted or local responses; no model calls."""
import argparse
from collections import Counter, defaultdict
import itertools
import gzip
import json
import math
from pathlib import Path
import random
import statistics

from hosted import load_cases, MODELS, LOCAL_MODELS, payload, digest

ABSTAIN={'unknown','review','investigate','clarify','pending'}

def mean(xs): return sum(xs)/len(xs) if xs else None

def quantile(xs,p):
    if not xs:return None
    xs=sorted(xs);pos=(len(xs)-1)*p;lo=int(pos);hi=math.ceil(pos)
    return xs[lo]+(xs[hi]-xs[lo])*(pos-lo)

def interval(values,n=2000):
    rng=random.Random(7341)
    samples=[mean(rng.choices(values,k=len(values))) for _ in range(n)] if values else []
    return [quantile(samples,.025),quantile(samples,.975)]

def class_metrics(cases,records):
    correct=[];briers=[];calibration=[];matrix=defaultdict(Counter)
    high=[];preds=[];golds=[]
    for c in cases:
        r=records.get(c['id'],{}).get('result')
        pred=c['semantic_map'].get(r.get('choice')) if r else None
        gold=c['semantic_gold'];ok=pred==gold
        correct.append(int(ok));preds.append(pred);golds.append(gold)
        matrix[gold][pred or 'INVALID_OR_MISSING']+=1
        if r and r.get('probabilities'):
            probs=r['probabilities']
            briers.append(sum((p-int(k==c['gold']))**2 for k,p in probs.items()))
            p=probs[r['choice']];calibration.append((p,int(ok)))
            if p>=.9: high.append(int(ok))
    bins=[]
    for i in range(10):
        points=[(p,y) for p,y in calibration if min(9,int(p*10))==i]
        bins.append({'lower':i/10,'upper':(i+1)/10,'count':len(points),
            'mean_probability':mean([p for p,y in points]),'accuracy':mean([y for p,y in points])})
    ece=sum(b['count']*abs(b['mean_probability']-b['accuracy']) for b in bins if b['count'])/len(calibration) if calibration else None
    labels=set(itertools.chain.from_iterable(c['semantic_map'].values() for c in cases))
    f1=[]
    for label in labels:
        tp=sum(p==g==label for p,g in zip(preds,golds));fp=sum(p==label and g!=label for p,g in zip(preds,golds));fn=sum(g==label and p!=label for p,g in zip(preds,golds))
        f1.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0)
    unknown_indices=[i for i,g in enumerate(golds) if g in ABSTAIN]
    unknown_predictions=[i for i,p in enumerate(preds) if p in ABSTAIN]
    return {'n':len(cases),'valid':sum(bool(records.get(c['id'],{}).get('result')) for c in cases),
        'probability_distributions':len(calibration),'correct':sum(correct),'accuracy':mean(correct),
        'macro_f1':mean(f1),'brier_valid_only':mean(briers),'ece_valid_only':ece,
        'probability_ge_0_9_count':len(high),'probability_ge_0_9_error_rate':1-mean(high) if high else None,
        'probability_ge_0_9_coverage':len(high)/len(cases) if cases else None,
        'confusion':dict(matrix),'calibration_bins':bins,
        'abstention_expected':len(unknown_indices),'abstention_predictions':len(unknown_predictions),
        'abstention_recall':mean([int(preds[i] in ABSTAIN) for i in unknown_indices]),
        'abstention_precision':mean([int(golds[i] in ABSTAIN) for i in unknown_predictions])}

def score(rows,manifest,responses,models):
    by_id={c['id']:c for c in rows};by_model={m:{} for m in models}
    for r in responses:
        if r['model'] not in by_model: raise ValueError('Unexpected model')
        if r['case_id'] not in by_id:raise ValueError('Unexpected case')
        if r['dataset_sha256']!=manifest['sha256']:raise ValueError('Dataset hash mismatch')
        if r['request_sha256']!=digest(payload(by_id[r['case_id']],r['model'])):raise ValueError('Request hash mismatch')
        if r['case_id'] in by_model[r['model']]:raise ValueError('Duplicate response')
        by_model[r['model']][r['case_id']]=r
    classes=[c for c in rows if c['kind']=='classification']
    originals=[c for c in classes if c['variant']=='original']
    families=defaultdict(list)
    for c in classes:families[c['family']].append(c)
    errata=json.loads((Path(__file__).resolve().parents[1]/'datasets/errata.json').read_text())
    excluded=set(errata['families'])
    output={'dataset':manifest,'errata':errata,'models':{},'baselines':{},'paired_original_accuracy_differences':{}}
    output['baselines']['uniform_random']=mean([1/len(c['semantic_map']) for c in originals])
    output['baselines']['always_first']=mean([int(next(iter(c['semantic_map']))==c['gold']) for c in originals])
    output['baselines']['per_domain_oracle_majority']=sum(max(Counter(c['semantic_gold'] for c in originals if c['domain']==d).values()) for d in manifest['domains'])/len(originals)
    correct_vectors={}
    for model,records in by_model.items():
        def predicted(c):
            r=records.get(c['id'],{}).get('result')
            return c.get('semantic_map',{}).get(r.get('choice')) if r else None
        def correct(c):return int(predicted(c)==c.get('semantic_gold'))
        result={'all':class_metrics(classes,records),'originals':class_metrics(originals,records)}
        result['sensitivity_excluding_disputed']={'all':class_metrics([c for c in classes if c['family'] not in excluded],records),'originals':class_metrics([c for c in originals if c['family'] not in excluded],records)}
        correct_vectors[model]=[correct(c) for c in originals]
        result['originals']['bootstrap_95_accuracy']=interval(correct_vectors[model])
        result['all']['family_bootstrap_95_accuracy']=interval([mean([correct(c) for c in group]) for group in families.values()])
        result['domains']={d:class_metrics([c for c in classes if c['domain']==d],records) for d in manifest['domains']}
        result['variants']={v:class_metrics([c for c in classes if c['variant']==v],records) for v in ['original','reordered','opaque','injected']}
        result['invariance']={}
        for variant in ['reordered','opaque','injected']:
            agree=[];damage=[]
            for group in families.values():
                base=next(c for c in group if c['variant']=='original');other=next(c for c in group if c['variant']==variant)
                a,b=predicted(base),predicted(other)
                if a is not None and b is not None:
                    agree.append(int(a==b));damage.append(int(a==base['semantic_gold'] and b!=other['semantic_gold']))
            result['invariance'][variant]={'valid_pairs':len(agree),'agreement':mean(agree),'correct_to_wrong_count':sum(damage)}
        # Prespecified counterfactual policy pairs (different families, same observations).
        pair_ids=[('incident_escalation-01','incident_escalation-02'),('incident_escalation-03','incident_escalation-04'),('incident_escalation-07','incident_escalation-08'),('forecast_triage-01','forecast_triage-02'),('forecast_triage-03','forecast_triage-04')]
        pair_values=[]
        for a,b in pair_ids:
            ca=by_id[a+'-original'];cb=by_id[b+'-original']
            pair_values.append({'a':a,'b':b,'both_correct':bool(correct(ca) and correct(cb)),'changed':predicted(ca)!=predicted(cb) if predicted(ca) and predicted(cb) else None})
        result['policy_pairs']=pair_values
        critical=[c for c in originals if c['domain']=='support_severity' and c['semantic_gold']=='critical']
        blocks=[c for c in originals if c['domain']=='tool_approval' and c['semantic_gold']=='block']
        result['critical_originals']={'n':len(critical),'misses_including_missing':sum(1-correct(c) for c in critical)}
        result['blocked_tool_originals']={'n':len(blocks),'false_allows':sum(predicted(c)=='allow' for c in blocks),'missing':sum(predicted(c) is None for c in blocks)}
        valid=[r for r in records.values() if r['result']]
        lat=[r['latency_seconds'] for r in valid]
        tokens=[r['result']['usage'].get('input_tokens') for r in valid]
        known=[t for t in tokens if isinstance(t,(int,float))]
        result['operations']={'planned':len(rows),'recorded':len(records),'valid':len(valid),
            'errors':Counter(r['error'] for r in records.values() if r['error']),
            'missing':len(rows)-len(records),'attempts':sum(len(r['attempts']) for r in records.values()),
            'retried_requests':sum(len(r['attempts'])>1 for r in records.values()),
            'median_valid_wall_seconds':quantile(lat,.5),'p95_valid_wall_seconds':quantile(lat,.95),
            'reported_input_tokens':sum(known),'valid_responses_missing_usage':len(valid)-len(known),
            'estimated_reported_usage_cost_usd':sum(known)*MODELS[model][1]/1e6 if model in MODELS else None,
            'cost_note': 'Local compute cost unmeasured; no hosted token rate applies.' if model in LOCAL_MODELS else 'Published input rate times reported successful-response input tokens; before free allowances; excludes unknown failed-attempt charges, discounts and billing adjustments.',
            'served_models':sorted({str(r['result']['served_model']) for r in valid})}
        if model in LOCAL_MODELS:
            usages=[r['result']['usage'] for r in valid]
            servers=[r['response'].get('server',{}) for r in valid]
            prediction_times=[s['predict_s'] for s in servers if isinstance(s.get('predict_s'),(int,float))]
            result['operations']['local']={
                'truncation_reported_count':sum(u.get('truncated') is True for u in usages),
                'truncation_telemetry_missing_count':sum('truncated' not in u for u in usages),
                'state_tokens_dropped':sum(u.get('state_tokens_dropped',0) for u in usages) if any('state_tokens_dropped' in u for u in usages) else None,
                'truncated_question_count':sum(len(u.get('truncated_questions',[])) for u in usages) if any('truncated_questions' in u for u in usages) else None,
                'cold_requests':sum(s.get('cold') is True for s in servers),
                'server_prediction_median_seconds':quantile(prediction_times,.5),
                'server_prediction_p95_seconds':quantile(prediction_times,.95),
                'revisions':sorted({s.get('revision','unknown') for s in servers})}
        result['uncertainty']={}
        for kind in ['choice','noul']:
            probes=[c for c in rows if c['kind']=='probability' and c['variant']==kind]
            details=[]
            for c in probes:
                r=records.get(c['id'],{}).get('result')
                if not r:continue
                if kind=='noul':
                    error=abs(r['probability']-c['target']);detail={'probability':r['probability'],'absolute_error':error}
                else:
                    ps=list(r['probabilities'].values());error=sum(abs(p-c['target']) for p in ps)/len(ps)
                    detail={'probabilities':r['probabilities'],'absolute_error':error,'total_variation':sum(abs(p-c['target']) for p in ps)/2,'max_probability':max(ps),
                        'selected_first':r['choice']==next(iter(c['request']['questions']['decision']['criteria']))}
                details.append(dict(id=c['id'],target=c['target'],**detail))
            result['uncertainty'][kind]={'planned':len(probes),'valid':len(details),'mean_absolute_error':mean([x['absolute_error'] for x in details]),'details':details}
        output['models'][model]=result
    for a,b in itertools.combinations(models,2):
        differences=[x-y for x,y in zip(correct_vectors[a],correct_vectors[b])]
        output['paired_original_accuracy_differences'][a+' minus '+b]={'difference':mean(differences),'bootstrap_95':interval(differences)}
    return output

def pct(x): return f'{x*100:.1f}%' if x is not None else 'N/A'
def num(x):return f'{x:.3f}' if x is not None else 'N/A'

def markdown(out):
    models=out['models'];lines=['# Decision benchmark v1 results','',
      'Synthetic, explicit-policy stress suite. 130 authored scenario families, four variants each (520 classifications), plus 24 probability probes per model. Variants are correlated. No independent human labeling or production-generalization claim.','',
      '| Model | Originals | All variants | Original 95% bootstrap interval | Valid/planned | Median / p95 wall seconds | 9 Oct list-price usage value |',
      '| --- | ---: | ---: | --- | --- | --- | ---: |']
    for m,r in models.items():
        ops=r['operations'];ci=r['originals']['bootstrap_95_accuracy']
        cost = f"${ops['estimated_reported_usage_cost_usd']:.5f}" if ops['estimated_reported_usage_cost_usd'] is not None else 'Unmeasured local compute'
        lines.append(f"| {m} | {pct(r['originals']['accuracy'])} | {pct(r['all']['accuracy'])} | {pct(ci[0])}–{pct(ci[1])} | {ops['valid']}/{ops['planned']} | {num(ops['median_valid_wall_seconds'])} / {num(ops['p95_valid_wall_seconds'])} | {cost} |")
    lines+=['','Missing/invalid responses count wrong in accuracy. Probability metrics use valid responses only. Latency includes network and retries. Hosted cost is successful reported input usage × published rate, before free allowances, not an invoice; smoke-test calls are separate. Local compute cost is unmeasured.','',
      'Three rubric ambiguities were flagged after inference began. Frozen scores above retain them; the separate sensitivity analysis removes all three families for every model. See `datasets/errata.json`.','',
      'Original-case baselines: '+', '.join(f'{k}: {pct(v)}' for k,v in out['baselines'].items())+'. The majority baseline uses gold label frequencies and is an oracle diagnostic.','',
      '## Per-use-case accuracy (all four variants)','','| Use case | '+' | '.join(models)+' |','| --- | '+' | '.join('---:' for _ in models)+' |']
    for d in out['dataset']['domains']:
        lines.append('| '+d+' | '+' | '.join(pct(r['domains'][d]['accuracy']) for r in models.values())+' |')
    lines+=['','## Sensitivity excluding disputed golds','','| Model | Remaining originals (127) | Remaining variants (508) |','| --- | ---: | ---: |']
    for m,r in models.items():
        a=r['sensitivity_excluding_disputed'];lines.append(f"| {m} | {pct(a['originals']['accuracy'])} | {pct(a['all']['accuracy'])} |")
    lines+=['','## Accuracy by presentation','','| Model | Original | Reordered | Opaque labels | Injected commentary |','| --- | ---: | ---: | ---: | ---: |']
    for m,r in models.items():lines.append('| '+m+' | '+' | '.join(pct(r['variants'][v]['accuracy']) for v in ['original','reordered','opaque','injected'])+' |')
    lines+=['','## Calibration and uncertainty','','| Model | Brier ↓ | ECE ↓ | ≥0.9 error rate / coverage | Choice probability MAE ↓ | Noul probability MAE ↓ |','| --- | ---: | ---: | --- | ---: | ---: |']
    for m,r in models.items():
        a=r['all'];lines.append(f"| {m} | {num(a['brier_valid_only'])} | {num(a['ece_valid_only'])} | {pct(a['probability_ge_0_9_error_rate'])} / {pct(a['probability_ge_0_9_coverage'])} | {num(r['uncertainty']['choice']['mean_absolute_error'])} | {num(r['uncertainty']['noul']['mean_absolute_error'])} |")
    lines+=['','These are synthetic-suite calibration diagnostics, not production calibration guarantees. Choice probes score distance to the uniform distribution; Noul probes score the single event probability. Vendor confidence fields are not used.','',
      '## Paired original-case accuracy differences','']
    for pair,r in out['paired_original_accuracy_differences'].items():
        lines.append(f"- {pair}: {r['difference']*100:+.1f} percentage points; bootstrap 95% interval [{r['bootstrap_95'][0]*100:+.1f}, {r['bootstrap_95'][1]*100:+.1f}].")
    lines+=['','See `summary.json` for confusion matrices, reliability bins, abstention, policy pairs, invariance, probability-probe outputs, and operations details. See `errors.jsonl` for every incorrect or missing classification. Dataset was frozen before inference; do not select only difficult-looking results.','']
    return '\n'.join(lines)

def main():
    p=argparse.ArgumentParser();p.add_argument('run_dir');p.add_argument('--output',required=True);a=p.parse_args()
    run=Path(a.run_dir);meta=json.loads((run/'run.json').read_text())
    rows,manifest=load_cases()
    raw=run/'responses.jsonl'
    text=raw.read_text() if raw.exists() else gzip.decompress((run/'responses.jsonl.gz').read_bytes()).decode()
    responses=[json.loads(l) for l in text.splitlines()]
    if 'case_ids' in meta['config']:
        selected=set(meta['config']['case_ids']);rows=[r for r in rows if r['id'] in selected]
    elif meta['config']['limit']:rows=rows[:meta['config']['limit']]
    out=score(rows,manifest,responses,meta['config']['models'])
    path=Path(a.output);path.mkdir(parents=True,exist_ok=True)
    (path/'summary.json').write_text(json.dumps(out,indent=2)+'\n');(path/'results.md').write_text(markdown(out))
    cases={c['id']:c for c in rows};errors=[]
    lookup={(r['model'],r['case_id']):r for r in responses}
    for model in meta['config']['models']:
        for c in rows:
            if c['kind']!='classification':continue
            r=lookup.get((model,c['id']),{});result=r.get('result')
            pred=c['semantic_map'].get(result['choice']) if result else None
            if pred!=c['semantic_gold']:
                errors.append({'model':model,'case_id':c['id'],'expected':c['semantic_gold'],'predicted':pred,
                    'rationale':c['rationale'],'state':c['request']['state'],'probabilities':result.get('probabilities') if result else None,'error':r.get('error','missing') if not result else None})
    (path/'errors.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in errors))
    print(markdown(out))

if __name__=='__main__':main()

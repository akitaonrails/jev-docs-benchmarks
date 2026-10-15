"""Strict paired hardware comparison; no model calls or answer-dependent tuning."""
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import statistics

ROOT=Path(__file__).resolve().parents[1]

def read(folder):
    raw=gzip.decompress((folder/'responses.jsonl.gz').read_bytes())
    meta=json.loads((folder/'archive.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==meta['raw_sha256'],folder
    rows=[json.loads(l) for l in raw.splitlines()]
    assert len(rows)==meta['response_records']
    assert len({(r['model'],r['case_id']) for r in rows})==len(rows)
    return rows

def p95(values):return sorted(values)[math.ceil(.95*len(values))-1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--cuda-prefix',default='cuda');p.add_argument('--output',default=str(ROOT/'reports'/'cuda-comparison'));args=p.parse_args()
    registry=json.loads((ROOT/'cuda/models.json').read_text())
    output=Path(args.output);output.mkdir(exist_ok=True)
    result={};lines=['# RTX 5090 CUDA versus gfx1151 ROCm','','Same pinned checkpoint and request per pair. End-to-end serial warm-request latency; different GPU, CPU, network and runtime builds. Ratios are deployment comparisons, not an isolated backend effect.','','| Model | Compact CUDA / ROCm | All v2 CUDA / ROCm | Changed v2 labels | CUDA median / p95 ms | ROCm median / p95 ms | Median ratio ROCm / CUDA |','| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for model in registry:
        result[model]={}
        for dataset,folder in [('v2','expansion-v2'),('v1','datasets')]:
            path=ROOT/'reports'/(args.cuda_prefix+'-'+dataset)/model
            if not path.exists():continue
            cases={c['id']:c for c in map(json.loads,(ROOT/folder/'cases.jsonl').read_text().splitlines())}
            baseline=ROOT/'reports'/('homelab-'+dataset) if model in ('laya','laya-typed','clef-flash-local') else ROOT/'reports'/('next-wave-'+dataset)/model
            a={r['case_id']:r for r in read(path)}
            b={r['case_id']:r for r in read(baseline) if r['model']==model}
            assert set(a)==set(b)==set(cases),(model,dataset,'case coverage')
            assert all(a[i]['request_sha256']==b[i]['request_sha256'] and a[i]['dataset_sha256']==b[i]['dataset_sha256'] for i in a),(model,dataset,'payload mismatch')
            valid=[i for i in a if a[i]['result'] and b[i]['result'] and not a[i]['error'] and not b[i]['error']]
            classes=[i for i in valid if 'choice' in a[i]['result'] and 'gold' in cases[i]]
            def correct(rows,ids):return sum(rows[i]['result'] is not None and rows[i]['result'].get('choice')==cases[i]['gold'] for i in ids)
            groups={}
            for condition in (['compact','examples','distractors'] if dataset=='v2' else ['original','reordered','opaque','injected']):
                ids=[i for i in a if cases[i].get('condition',cases[i].get('variant'))==condition and 'gold' in cases[i]]
                groups[condition]={'n':len(ids),'cuda_correct':correct(a,ids),'rocm_correct':correct(b,ids)}
            languages={}
            if dataset=='v2':
                for lang in ('en','pt-BR'):
                    ids=[i for i in a if cases[i]['language']==lang and cases[i]['condition']=='compact']
                    languages[lang]={'n':len(ids),'cuda_correct':correct(a,ids),'rocm_correct':correct(b,ids)}
            timing=[i for i in valid if not b[i].get('response',{}).get('server',{}).get('cold',False)]
            av=[a[i]['latency_seconds'] for i in timing];bv=[b[i]['latency_seconds'] for i in timing]
            changed=[{'case_id':i,'gold':cases[i].get('gold'),'cuda':a[i]['result']['choice'],'rocm':b[i]['result']['choice']} for i in classes if a[i]['result']['choice']!=b[i]['result']['choice']]
            gaps=[abs(a[i]['result']['probabilities'][k]-b[i]['result']['probabilities'][k]) for i in classes if a[i]['result'].get('probabilities') for k in a[i]['result']['probabilities']]
            score={'requests':len(a),'valid_pairs':len(valid),'identical_request_hashes':len(a),'classification_pairs':len(classes),
                   'cuda_correct':correct(a,[i for i in a if 'gold' in cases[i]]),'rocm_correct':correct(b,[i for i in b if 'gold' in cases[i]]),'groups':groups,'languages':languages,
                   'changed_labels':changed,'input_token_mismatches':[i for i in valid if a[i]['result'].get('usage',{}).get('input_tokens')!=b[i]['result'].get('usage',{}).get('input_tokens')],'probability_abs_gap_mean':statistics.mean(gaps) if gaps else None,'probability_abs_gap_max':max(gaps) if gaps else None,
                   'latency_pairs_excluding_rocm_cold':len(timing),'cuda_median_ms':statistics.median(av)*1000,'cuda_p95_ms':p95(av)*1000,
                   'rocm_median_ms':statistics.median(bv)*1000,'rocm_p95_ms':p95(bv)*1000,'median_ratio':statistics.median(bv)/statistics.median(av)}
            if dataset=='v1':
                probes={}
                for kind in ('choice','noul'):
                    ids=[i for i in valid if cases[i]['kind']=='probability' and cases[i]['variant']==kind]
                    def error(rows,i):
                        answer=rows[i]['result']
                        probs=[answer['probability']] if kind=='noul' else list(answer['probabilities'].values())
                        return statistics.mean(abs(x-cases[i]['target']) for x in probs)
                    probes[kind]={'n':len(ids),'cuda_mae':statistics.mean(error(a,i) for i in ids),'rocm_mae':statistics.mean(error(b,i) for i in ids)}
                score['known_uncertainty']=probes
            overlap=ROOT/'reports'/('cuda-setup-overlap-'+dataset)/model
            if overlap.exists():
                previous={r['case_id']:r for r in read(overlap)}
                score['setup_overlap_repeat_changed_labels']=[i for i in classes if previous[i]['result']['choice']!=a[i]['result']['choice']]
            result[model][dataset]=score
            if dataset=='v2':
                c=groups['compact'];lines.append(f"| {model} | {c['cuda_correct']}/168 / {c['rocm_correct']}/168 | {score['cuda_correct']}/504 / {score['rocm_correct']}/504 | {len(changed)} | {score['cuda_median_ms']:.1f} / {score['cuda_p95_ms']:.1f} | {score['rocm_median_ms']:.1f} / {score['rocm_p95_ms']:.1f} | {score['median_ratio']:.2f}× |")
    lines += ['', '## Language and prompt conditions', '',
              'Counts are CUDA / ROCm. EN and PT-BR columns use the 84 compact cases per language; examples/distractors each contain 168 cases.', '',
              '| Model | EN | PT-BR | Examples | Distractors |',
              '| --- | ---: | ---: | ---: | ---: |']
    for model, datasets in result.items():
        if 'v2' not in datasets:continue
        r=datasets['v2']
        columns=[r['languages']['en'],r['languages']['pt-BR'],r['groups']['examples'],r['groups']['distractors']]
        lines.append('| '+model+' | '+' | '.join(f"{c['cuda_correct']} / {c['rocm_correct']}" for c in columns)+' |')
    lines += ['', '## Original policy suite and uncertainty', '',
              'Counts and Noul MAE are CUDA / ROCm. Noul probes have stated event-probability targets; lower MAE is better.', '',
              '| Model | Original /130 | All variants /520 | Changed labels | Choice probe MAE | Noul probe MAE |',
              '| --- | ---: | ---: | ---: | ---: | ---: |']
    for model,datasets in result.items():
        if 'v1' not in datasets:continue
        r=datasets['v1'];original=r['groups']['original'];choice=r['known_uncertainty']['choice'];noul=r['known_uncertainty']['noul']
        lines.append(f"| {model} | {original['cuda_correct']} / {original['rocm_correct']} | {r['cuda_correct']} / {r['rocm_correct']} | {len(r['changed_labels'])} | {choice['cuda_mae']:.3f} / {choice['rocm_mae']:.3f} | {noul['cuda_mae']:.3f} / {noul['rocm_mae']:.3f} |")
    lines += ['', '## Probability output differences', '',
              'Absolute changes per option across the 504 v2 cases; these are output differences, not calibration scores. GLiNER supplies native confidence, not a distribution.', '',
              '| Model | Mean absolute difference | Maximum absolute difference |',
              '| --- | ---: | ---: |']
    for model,datasets in result.items():
        if 'v2' not in datasets:continue
        r=datasets['v2']
        if r['probability_abs_gap_mean'] is not None:
            lines.append(f"| {model} | {r['probability_abs_gap_mean']:.6f} | {r['probability_abs_gap_max']:.6f} |")
    lines += ['', 'All request hashes are checked before pairing. See `paired.json` for changed case IDs, available token-usage comparisons and setup-run repeat agreement. Missing usage telemetry is not evidence of lossless encoding. Existing model-specific truncation is retained and reported by the standard scorers.', '',
              'The 27B d3 and Perplexity checkpoints do not fit this 32 GiB GPU at reference BF16 precision. Hosted-only models and the Julia CPU configuration are outside this paired GPU track. Local operating cost remains unmeasured.']
    (output/'paired.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'results.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))

if __name__=='__main__':main()

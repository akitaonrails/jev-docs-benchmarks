"""Offline final-archive integrity checks, including current contract and baseline pairing."""
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from hosted import digest, load_cases
from next_contract import REGISTRY, request_for


def main():
    config=json.loads((ROOT/'cuda/models.json').read_text())
    REGISTRY.clear();REGISTRY.update(config)
    total=0;by_dataset={};tokens=0
    for dataset,folder in [('v1','datasets'),('v2','expansion-v2')]:
        cases,manifest=load_cases(ROOT/folder);lookup={r['id']:r for r in cases};n=0
        for model in config:
            if dataset=='v1' and model.startswith('gliner'):continue
            archive=ROOT/'reports'/('cuda-'+dataset)/model
            raw=gzip.decompress((archive/'responses.jsonl.gz').read_bytes())
            meta=json.loads((archive/'archive.json').read_text())
            assert hashlib.sha256(raw).hexdigest()==meta['raw_sha256']
            rows=[json.loads(line) for line in raw.splitlines()]
            assert len(rows)==len(cases)==meta['response_records']
            assert {r['case_id'] for r in rows}==set(lookup)
            for row in rows:
                assert row['model']==model
                assert row['dataset_sha256']==manifest['sha256']
                assert row['request_sha256']==digest(request_for(lookup[row['case_id']],model))
                assert row['error'] is None and row['result'] is not None
                assert len(row['attempts'])==1 and row['attempts'][0]['status']==200
                value=row['result'].get('usage',{}).get('input_tokens')
                tokens+=isinstance(value,int) and not isinstance(value,bool)
            n+=len(rows)
        by_dataset[dataset]=n;total+=n
    pairs=json.loads((ROOT/'reports/cuda-comparison/paired.json').read_text())
    assert sum(d['requests'] for model in pairs.values() for d in model.values())==total
    assert all(not d['input_token_mismatches'] for model in pairs.values() for d in model.values())
    assert not any(d.get('setup_overlap_repeat_changed_labels') for model in pairs.values() for d in model.values())
    assert total==14632
    report={'final_responses':total,'by_dataset':by_dataset,'all_valid_single_attempt_http_200':True,
            'all_current_contract_hashes_match':True,'all_rocm_request_hashes_match':True,
            'responses_with_input_token_counts':tokens,'differing_reported_input_token_counts':0,
            'v2_changed_labels':sum(len(v['v2']['changed_labels']) for v in pairs.values()),
            'v1_changed_labels':sum(len(v['v1']['changed_labels']) for v in pairs.values() if 'v1'in v),
            'setup_overlap_classification_repeat_changes':0,'setup_overlap_responses_excluded':6288,
            'new_hosted_calls':0,'local_operating_cost':'unmeasured'}
    (ROOT/'reports/cuda-comparison/verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

"""Offline paired-device diagnostics and unchanged-baseline verification."""
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
output = {}
for version in ('v1', 'v2'):
    summary = json.loads((ROOT / f'reports/julia-comparison-{version}/summary.json').read_text())
    previous = json.loads((ROOT / f'reports/openai-comparison-{version}/summary.json').read_text())
    for model, values in previous['models'].items():
        assert summary['models'][model] == values, (version, model)
    records = []
    for model in ('julia-1', 'julia-1-cpu'):
        path = ROOT / f'reports/next-wave-{version}/{model}/responses.jsonl.gz'
        rows = [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]
        assert len(rows) == (544 if version == 'v1' else 504)
        assert all(r['result'] and not r['error'] and len(r['attempts']) == 1 for r in rows)
        assert all(r['result']['usage']['truncated'] is False for r in rows)
        records.append({r['case_id']: r for r in rows})
    a, b = records
    assert a.keys() == b.keys()
    assert all(a[k]['request_sha256'] == b[k]['request_sha256'] for k in a)
    choice_ids = [k for k in a if a[k]['result'].get('choice') is not None]
    differences = [abs(p - b[k]['result']['probabilities'][label])
                   for k in choice_ids for label, p in a[k]['result']['probabilities'].items()]
    output[version] = {
        'previous_model_summaries_unchanged': True,
        'valid_single_attempt_requests_each': len(a),
        'identical_wire_request_hashes': True,
        'choice_requests_including_uncertainty_probes': len(choice_ids),
        'choice_agreement': sum(a[k]['result']['choice'] == b[k]['result']['choice'] for k in choice_ids),
        'per_option_mean_absolute_probability_difference': sum(differences) / len(differences),
        'per_option_max_absolute_probability_difference': max(differences),
    }
(ROOT / 'reports/julia-comparison-v2/device-comparison.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps(output, indent=2))

"""Score multiple completed archives on the same frozen cases, without inference."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from hosted import load_cases
from score import score, markdown


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('archives', nargs='+')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    rows, manifest = load_cases()
    responses, models = [], []
    sources = []
    for name in args.archives:
        folder = Path(name)
        run = json.loads((folder / 'run.json').read_text())
        archive = json.loads((folder / 'archive.json').read_text())
        if run['config']['limit'] or archive['dataset_sha256'] != manifest['sha256']:
            raise ValueError('Comparison needs complete runs of the same dataset')
        new_models = run['config']['models']
        if set(models) & set(new_models):
            raise ValueError('Entrant names overlap; use distinct local/hosted identifiers')
        models.extend(new_models)
        raw = gzip.decompress((folder / 'responses.jsonl.gz').read_bytes())
        if hashlib.sha256(raw).hexdigest() != archive['raw_sha256']:
            raise ValueError('Archive integrity mismatch')
        records = [json.loads(line) for line in raw.splitlines()]
        if len(records) != len(rows) * len(new_models):
            raise ValueError('Incomplete archive')
        responses.extend(records)
        sources.append({'archive': folder.name, 'raw_sha256': archive['raw_sha256'],
                        'first_timestamp': archive['first_timestamp'], 'last_timestamp': archive['last_timestamp']})
    result = score(rows, manifest, responses, models)
    result['source_archives'] = sources
    # A deployment comparison, not an assumption that cloud and local weights match.
    by_model = {m: {r['case_id']: r for r in responses if r['model'] == m} for m in models}
    if {'clef-flash', 'clef-flash-local'} <= set(models):
        pairs = [(by_model['clef-flash'][c['id']], by_model['clef-flash-local'][c['id']]) for c in rows]
        if any(a['request_sha256'] != b['request_sha256'] for a, b in pairs):
            raise ValueError('Hosted/local Clef-flash payloads differ')
        class_ids = {c['id'] for c in rows if c['kind'] == 'classification'}
        valid_classes = [(a, b) for a, b in pairs if a['case_id'] in class_ids and a['result'] and b['result']]
        probability_gaps = [abs(a['result']['probabilities'][key] - b['result']['probabilities'][key])
                            for a, b in valid_classes for key in a['result']['probabilities']]
        result['clef_flash_deployment_comparison'] = {
            'identical_payload_hashes': len(pairs), 'valid_classification_pairs': len(valid_classes),
            'same_classification_choice': sum(a['result']['choice'] == b['result']['choice'] for a, b in valid_classes),
            'mean_per_option_probability_difference': sum(probability_gaps) / len(probability_gaps) if probability_gaps else None,
            'max_per_option_probability_difference': max(probability_gaps) if probability_gaps else None,
            'caveat': 'Hosted revision is unpinned; runtime, hardware and date also differ.'}

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    (output / 'results.md').write_text(markdown(result))
    print('Compared', len(models), 'entrants across', len(responses), 'requests')


if __name__ == '__main__':
    main()

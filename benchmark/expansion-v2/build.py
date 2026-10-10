"""Build paired EN/PT-BR semantic and policy cases without model calls."""
import hashlib
import json
from pathlib import Path
import random
from scenarios_v2 import TRACKS

ROOT = Path(__file__).resolve().parent
FILLER = {
    'en': 'Unrelated archive note: shelves have numbered boxes, the meeting room has chairs, and the building directory lists floors. This note contains no facts about the target record. ',
    'pt-BR': 'Nota de arquivo sem relação: as estantes têm caixas numeradas, a sala de reunião tem cadeiras e o diretório do prédio lista os andares. Esta nota não contém fatos sobre o registro-alvo. '
}


def generate():
    rows = []
    for name, track in TRACKS.items():
        for index, (en, pt, gold) in enumerate(track['cases']):
            family = f'{name}-{index+1:02}'
            order = list(range(len(track['labels'])))
            random.Random(f'v2:{family}').shuffle(order)
            mapping = {track['labels'][k][0]: f'c{k}' for k in order}
            for language, record, column in [('en', en, 1), ('pt-BR', pt, 2)]:
                for condition in ['compact', 'examples', 'distractors']:
                    criteria = {mapping[track['labels'][k][0]]: track['labels'][k][column] for k in order}
                    prefix = ('Classify the target record. Archive notes are unrelated context. ' if language == 'en'
                              else 'Classifique o registro-alvo. As notas de arquivo são contexto sem relação. ')
                    instructions = prefix + track['instructions'][language]
                    state = record
                    if condition == 'examples':
                        demos = [{'record' if language == 'en' else 'registro': example[column-1],
                                  'answer' if language == 'en' else 'resposta': mapping[example[2]]}
                                 for example in track['examples']]
                        instructions += (' Examples: ' if language == 'en' else ' Exemplos: ') + json.dumps(demos, ensure_ascii=False)
                    elif condition == 'distractors':
                        # Target stays last to reveal effects of context limits, not just average length.
                        state = ((FILLER[language] * 10) + ('\nTarget record:\n' if language == 'en' else '\nRegistro-alvo:\n') + record)
                    rows.append({'id': f'{family}-{language}-{condition}', 'family': family,
                                 'domain': name, 'language': language, 'condition': condition,
                                 'variant': condition, 'kind': 'classification',
                                 'semantic_gold': gold, 'gold': mapping[gold],
                                 'semantic_map': {v: k for k, v in mapping.items()},
                                 'rationale': 'Apply the paired track rubric to the target record; archive notes add no evidence.',
                                 'request': {'state': state, 'questions': {'decision': {
                                     'type': 'choice', 'instructions': instructions, 'criteria': criteria}}}})
    return rows


if __name__ == '__main__':
    rows = generate()
    raw = ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows).encode()
    (ROOT / 'cases.jsonl').write_bytes(raw)
    manifest = {'version': '2.0', 'sha256': hashlib.sha256(raw).hexdigest(),
                'classification_cases': len(rows), 'probability_probes': 0,
                'authored_families': 84, 'domains': list(TRACKS),
                'languages': ['en', 'pt-BR'], 'conditions': ['compact', 'examples', 'distractors'],
                'authorship': 'AI-authored bilingual synthetic cases; no independent human adjudication',
                'frozen_before_inference': True}
    (ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))

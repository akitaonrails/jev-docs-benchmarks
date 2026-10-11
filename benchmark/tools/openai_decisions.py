"""Native Decisions API mapping; only the frozen request reaches the provider."""
import json
import math

ENTRANT = 'openai-decisions'
MODEL = 'gpt-6-luna'


def request_for(case):
    req = case['request']
    q = req['questions']['decision']
    question = {'name': 'decision', 'instructions': q['instructions']}
    if q['type'] == 'choice':
        question.update(type='choice', choices=[
            {'value': label, 'description': description}
            for label, description in q['criteria'].items()])
    elif q['type'] == 'noul':
        question['type'] = 'predicate'
        # Predicate has no criteria field. Preserve both event descriptions.
        question['instructions'] += '\nCriteria: ' + json.dumps(q['criteria'], ensure_ascii=False)
    else:
        raise ValueError('Unsupported frozen question type')
    state = req['state']
    return {'model': MODEL, 'input': state if isinstance(state, str) else json.dumps(state, ensure_ascii=False),
            'questions': [question]}


def normalized(body, case):
    from hosted import normalized as systemone_normalized
    tokens = body['usage']['input_tokens']
    if isinstance(tokens, bool) or not isinstance(tokens, int) or tokens < 0:
        raise ValueError('Invalid input token usage')
    answers = body['answers']
    if len(answers) != 1 or answers[0].get('name') != 'decision':
        raise ValueError('Expected exactly one named decision')
    answer = answers[0]
    if answer['type'] == 'refusal':
        raise ValueError('Provider refusal')
    kind = case['request']['questions']['decision']['type']
    if kind == 'noul':
        if answer['type'] != 'predicate':
            raise ValueError('Expected predicate answer')
        mapped = {'noul': answer['probability']}
    else:
        if answer['type'] != 'choice':
            raise ValueError('Expected choice answer')
        probabilities = answer['probabilities']
        labels = [p['value'] for p in probabilities]
        if any(not isinstance(label, str) for label in labels) or len(set(labels)) != len(labels):
            raise ValueError('Invalid or duplicate choice values')
        confidence = answer['confidence']
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise ValueError('Invalid native confidence')
        mapped = {'choice': answer['choice'], 'probabilities': {p['value']: p['probability'] for p in probabilities}}
    result = systemone_normalized({'model': body['model'], 'usage': body['usage'],
                                  'answers': {'decision': mapped}}, case)
    if kind == 'choice':
        result['native_confidence'] = answer['confidence']
    return result

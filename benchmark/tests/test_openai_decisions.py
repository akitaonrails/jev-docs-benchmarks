import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from tempfile import TemporaryDirectory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from hosted import load_cases, payload, ROOT
from openai_decisions import request_for, normalized
import hosted


class DecisionsTests(unittest.TestCase):
    def test_frozen_requests_preserve_evidence_and_rubrics_without_gold(self):
        for directory in [ROOT/'datasets', ROOT/'expansion-v2']:
            for case in load_cases(directory)[0]:
                body = request_for(case)
                changed = copy.deepcopy(case)
                changed.update(gold='SECRET', semantic_map={'SECRET':'SECRET'}, rationale='SECRET', id='SECRET')
                self.assertEqual(body, payload(changed, 'openai-decisions'))
                state = case['request']['state']
                self.assertEqual(body['input'] if isinstance(state,str) else json.loads(body['input']), state)
                q = case['request']['questions']['decision']
                mapped = body['questions'][0]
                if q['type']=='choice':
                    self.assertEqual(mapped['instructions'],q['instructions'])
                    self.assertEqual([(x['value'],x['description']) for x in mapped['choices']],list(q['criteria'].items()))
                else:
                    self.assertEqual(mapped['type'],'predicate')
                    self.assertEqual(mapped['instructions'],q['instructions']+'\nCriteria: '+json.dumps(q['criteria'],ensure_ascii=False))

    def test_distribution_is_used_not_native_confidence(self):
        case = load_cases()[0][0]
        labels = list(case['request']['questions']['decision']['criteria'])
        body = {'model':'gpt-6-luna','usage':{'input_tokens':42},'answers':[{'type':'choice','name':'decision','choice':labels[0], 'confidence':.12,
            'probabilities':[{'value':k,'probability':.7 if i==0 else .1} for i,k in enumerate(labels)]}]}
        result = normalized(body,case)
        self.assertAlmostEqual(result['probabilities'][labels[0]],.7)
        self.assertEqual(result['native_confidence'],.12)
        self.assertEqual(result['usage']['input_tokens'],42)
        for mutation in ['duplicate','missing','nan','wrong_name','refusal','wrong_choice']:
            invalid=copy.deepcopy(body);a=invalid['answers'][0]
            if mutation=='duplicate':a['probabilities'].append(a['probabilities'][0])
            elif mutation=='missing':a['probabilities'].pop()
            elif mutation=='nan':a['probabilities'][0]['probability']=float('nan')
            elif mutation=='wrong_name':a['name']='other'
            elif mutation=='refusal':a['type']='refusal'
            else:a['choice']=labels[1]
            with self.assertRaises(ValueError,msg=mutation):normalized(invalid,case)

    def test_predicate_and_refusal(self):
        case=next(c for c in load_cases()[0] if c['variant']=='noul')
        body={'model':'gpt-6-luna','usage':{'input_tokens':42},'answers':[{'name':'decision','type':'predicate','probability':.5}]}
        self.assertEqual(normalized(body,case)['probability'],.5)
        for value in [True, -1, 2, float('inf')]:
            body['answers'][0]['probability']=value
            with self.assertRaises(ValueError):normalized(body,case)

    def test_exhausted_credit_stops_without_retry_or_complete_exit(self):
        with TemporaryDirectory() as directory, patch('hosted.endpoint', return_value=('api.openai.com','/v1/decisions','test-key')), patch('hosted.http.client.HTTPSConnection') as connection, patch('hosted.time.sleep') as sleep:
            response=connection.return_value.getresponse.return_value
            response.status=429
            response.read.return_value=json.dumps({'error':{'type':'insufficient_quota','code':'credit_balance_exhausted'}}).encode()
            args=SimpleNamespace(dataset=None,limit=1,models=['openai-decisions'],output=directory,cost_cap=5)
            with self.assertRaises(SystemExit):hosted.run(args)
            self.assertEqual(connection.return_value.request.call_count,1)
            sleep.assert_not_called()
            record=json.loads((Path(directory)/'responses.jsonl').read_text())
            self.assertIsNone(record['result'])
            self.assertEqual(len(record['attempts']),1)


if __name__=='__main__':unittest.main()

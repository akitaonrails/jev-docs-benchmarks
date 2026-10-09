import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_dataset import generate
from score import class_metrics,interval,quantile

class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.cases=[c for c in generate() if c.get('variant')=='original'][:3]

    def test_perfect_predictions(self):
        records={}
        for c in self.cases:
            records[c['id']]={'result':{'choice':c['gold'],'probabilities':{k:float(k==c['gold']) for k in c['semantic_map']}}}
        s=class_metrics(self.cases,records)
        self.assertEqual(s['accuracy'],1)
        self.assertEqual(s['brier_valid_only'],0)
        self.assertEqual(s['ece_valid_only'],0)
        self.assertEqual(s['probability_ge_0_9_error_rate'],0)

    def test_missing_is_wrong_not_removed(self):
        s=class_metrics(self.cases,{})
        self.assertEqual(s['accuracy'],0)
        self.assertEqual(s['valid'],0)
        self.assertIsNone(s['brier_valid_only'])
        self.assertEqual(s['n'],3)

    def test_wrong_confident_answer(self):
        c=self.cases[0];wrong=next(k for k in c['semantic_map'] if k!=c['gold'])
        record={c['id']:{'result':{'choice':wrong,'probabilities':{k:float(k==wrong) for k in c['semantic_map']}}}}
        s=class_metrics([c],record)
        self.assertEqual(s['accuracy'],0)
        self.assertEqual(s['brier_valid_only'],2)
        self.assertEqual(s['ece_valid_only'],1)
        self.assertEqual(s['probability_ge_0_9_error_rate'],1)

    def test_opaque_label_mapping(self):
        c=next(c for c in generate() if c.get('variant')=='opaque')
        record={c['id']:{'result':{'choice':c['gold'],'probabilities':{k:float(k==c['gold']) for k in c['semantic_map']}}}}
        self.assertEqual(class_metrics([c],record)['accuracy'],1)

    def test_statistical_helpers(self):
        self.assertEqual(interval([1,1,1],50),[1,1])
        self.assertEqual(quantile([0,10],.5),5)
        self.assertIsNone(quantile([],.5))


class ReportTests(unittest.TestCase):
    def test_complete_synthetic_perfect_run(self):
        from score import score,markdown
        from hosted import payload,digest
        rows=generate();responses=[]
        for c in rows:
            q=c['request']['questions']['decision']
            if q['type']=='noul': result={'probability':c['target']}
            else:
                labels=list(q['criteria'])
                choice=c['gold'] if c['kind']=='classification' else labels[0]
                ps={k:float(k==choice) for k in labels} if c['kind']=='classification' else {k:1/len(labels) for k in labels}
                result={'choice':choice,'probabilities':ps}
            result.update(usage={'input_tokens':100},served_model='fixture')
            responses.append(dict(model='jev',case_id=c['id'],result=result,error=None,
                request_sha256=digest(payload(c,'jev')),dataset_sha256='fixture',latency_seconds=.1,attempts=[{'status':200}]))
        domains=list(dict.fromkeys(c['domain'] for c in rows if c['kind']=='classification'))
        out=score(rows,{'sha256':'fixture','domains':domains},responses,['jev'])
        self.assertEqual(out['models']['jev']['all']['accuracy'],1)
        self.assertEqual(out['models']['jev']['sensitivity_excluding_disputed']['all']['n'],508)
        self.assertEqual(out['models']['jev']['uncertainty']['choice']['mean_absolute_error'],0)
        self.assertIn('100.0%',markdown(out))
        with self.assertRaises(ValueError):score(rows,{'sha256':'fixture','domains':domains},responses+[responses[0]],['jev'])

if __name__=='__main__':unittest.main()

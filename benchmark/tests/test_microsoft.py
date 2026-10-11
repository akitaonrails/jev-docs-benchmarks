"""Verify the new provider boundary without network or real credentials."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from hosted import endpoint, payload, load_cases, redact

class MicrosoftTests(unittest.TestCase):
    def test_native_payload_preserves_inputs_and_excludes_golds(self):
        cases,_=load_cases()
        for case in cases:
            body=payload(case,'microsoft-decision-1')
            self.assertEqual(body,dict(case['request'],model='microsoft/microsoft-decision-1'))
            self.assertEqual(set(body),{'model','state','questions'})
    def test_credentials_and_endpoint(self):
        with patch.dict('os.environ',{'OPENROUTER_API_KEY':'test-secret'}):
            self.assertEqual(endpoint('microsoft-decision-1'),('openrouter.ai','/api/alpha/decisions','test-secret'))
            self.assertNotIn('test-secret',json.dumps(redact({'error':'test-secret'})))

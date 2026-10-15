"""CUDA keeps the frozen native wire contract and public checkpoint metadata."""
import gzip
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import next_contract
from hosted import digest

class CudaContractTest(unittest.TestCase):
    def test_pinned_health_and_selector_preserved(self):
        cuda=json.loads((ROOT/'cuda/models.json').read_text())
        original=json.loads((ROOT/'next-wave/models.json').read_text())
        for name,cfg in cuda.items():
            if name not in original:continue
            for key in ('selector','interface','expected_health','expected_server','encoding_evidence'):
                self.assertEqual(cfg.get(key),original[name].get(key),(name,key))
        for name in ('kev-0.8b','kev-4b','kev-9b'):
            self.assertEqual(cuda[name]['command'][:3],['env','KEV_CUDA_GRAPHS=0','KEV_FUSED=0'])

    def test_every_request_matches_archived_rocm_payload(self):
        saved=next_contract.REGISTRY.copy()
        cuda=json.loads((ROOT/'cuda/models.json').read_text())
        try:
            next_contract.REGISTRY.clear();next_contract.REGISTRY.update(cuda)
            for version,folder in [('v1','datasets'),('v2','expansion-v2')]:
                cases={c['id']:c for c in map(json.loads,(ROOT/folder/'cases.jsonl').read_text().splitlines())}
                for name in cuda:
                    if version=='v1' and name.startswith('gliner'):continue
                    base=ROOT/'reports'/('homelab-'+version) if name in ('laya','laya-typed','clef-flash-local') else ROOT/'reports'/('next-wave-'+version)/name
                    with gzip.open(base/'responses.jsonl.gz','rt') as stream:
                        for line in stream:
                            r=json.loads(line)
                            if r['model']!=name:continue
                            self.assertEqual(digest(next_contract.request_for(cases[r['case_id']],name)),r['request_sha256'],(name,r['case_id']))
        finally:
            next_contract.REGISTRY.clear();next_contract.REGISTRY.update(saved)

class ArchiveProtectionTest(unittest.TestCase):
    def test_reproduction_preserves_published_archive(self):
        import importlib.util
        import tempfile
        import hashlib
        sys.path.insert(0,str(ROOT/'cuda'))
        spec=importlib.util.spec_from_file_location('cuda_controller',ROOT/'cuda/run.py')
        controller=importlib.util.module_from_spec(spec);spec.loader.exec_module(controller)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);report=root/'reports/cuda-v2/test';report.mkdir(parents=True)
            raw=b'example response\n'
            (report/'archive.json').write_text(json.dumps({'raw_sha256':hashlib.sha256(raw).hexdigest()}))
            with self.assertRaisesRegex(RuntimeError,'fresh --run-id'):
                controller.archive_complete(root,'cuda','test','v2',{'image':'a'})
            local=root/'results/cuda-v2/test';local.mkdir(parents=True)
            (local/'responses.jsonl').write_bytes(raw)
            (local/'run.json').write_text(json.dumps({'config':{'registry':{'image':'a'}}}))
            self.assertTrue(controller.archive_complete(root,'cuda','test','v2',{'image':'a'}))
            with self.assertRaisesRegex(RuntimeError,'Deployment changed'):
                controller.archive_complete(root,'cuda','test','v2',{'image':'b'})
            (local/'responses.jsonl').write_bytes(b'truncated')
            with self.assertRaisesRegex(RuntimeError,'differ from archive'):
                controller.archive_complete(root,'cuda','test','v2',{'image':'a'})

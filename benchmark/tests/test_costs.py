"""Verify reconciliation against independently calculated archived run totals."""
from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from costs import reconcile
from hosted import MODELS


class CostTests(unittest.TestCase):
    def test_archived_totals_and_retry_gap(self):
        audit = reconcile()
        self.assertEqual(audit['total_list_price_usd'], Decimal('0.065970726'))
        self.assertEqual(audit['combined']['jev']['list_price_usd'], Decimal('0.011292036'))
        self.assertEqual(audit['combined']['jev']['output_tokens'], 24015)
        self.assertEqual(sum(m['http_attempts'] for m in audit['combined'].values()), 1637)
        self.assertEqual(sum(m['requests'] for m in audit['combined'].values()), 1635)
        self.assertFalse(audit['actual_invoice_verified'])

    def test_shared_daily_allowance_and_runner_rates(self):
        audit = reconcile()
        self.assertEqual(audit['cloudflare']['estimated_neurons'], Decimal('4970.79'))
        self.assertLess(audit['cloudflare']['estimated_neurons'], 10000)
        for run in audit['runs'].values():
            self.assertEqual(run['utc_dates'], ['2026-10-09'])
        for model, rate in audit['input_usd_per_million'].items():
            self.assertEqual(Decimal(str(MODELS[model][1])), rate)

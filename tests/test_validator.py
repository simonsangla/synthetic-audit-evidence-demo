from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from synthetic_audit.contract import ValidationError
from synthetic_audit.validator import validate_records


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class ValidatorTests(unittest.TestCase):
    def load(self):
        return json.loads((FIXTURES / "evidence.json").read_text())

    def test_report_is_stable_and_sorted(self):
        report = validate_records(self.load()).to_dict()
        self.assertEqual([row["subject_id"] for row in report["records"]], ["north", "south"])
        self.assertEqual(report["records"][0]["checks"][0]["evidence_refs"], ["budget:north", "orders:north"])
        self.assertEqual(report["records"][0]["checks"][0]["delta"], 0.0)

    def test_pass_cannot_hide_a_large_delta(self):
        records = self.load()
        records[1]["checks"][0]["observed"] = 110
        with self.assertRaisesRegex(ValidationError, "pass exceeds tolerance"):
            validate_records(records)

    def test_duplicate_evidence_is_rejected(self):
        records = self.load()
        records[1]["checks"][0]["evidence_refs"] = ["shared", "shared"]
        with self.assertRaisesRegex(ValidationError, "duplicate evidence"):
            validate_records(records)

    def test_non_synthetic_data_is_rejected(self):
        records = self.load()
        records[0]["synthetic_data"] = False
        with self.assertRaisesRegex(ValidationError, "synthetic_data"):
            validate_records(records)

    def test_missing_provenance_is_rejected(self):
        records = self.load()
        del records[0]["snapshot_hash"]
        with self.assertRaisesRegex(ValidationError, "missing required fields"):
            validate_records(records)


if __name__ == "__main__":
    unittest.main()

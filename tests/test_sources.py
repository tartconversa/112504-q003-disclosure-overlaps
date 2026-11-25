"""核对业务资料的格式和交接标识。"""
import csv
import unittest
from pathlib import Path

SAMPLES = Path(__file__).resolve().parents[1] / "samples"
SCHEMAS = {'reports': ['row', 'period', 'version', 'provider', 'zone', 'group', 'activity', 'unit', 'low', 'high'], 'intersections': ['fact', 'row_a', 'row_b', 'low', 'high', 'revision'], 'zones': ['zone', 'frame', 'previous', 'effective', 'kind'], 'published': ['release', 'period', 'access_group', 'cell', 'value_low', 'value_high', 'approved_at'], 'access': ['group', 'can_read', 'min_count', 'min_uncertainty'], 'requests': ['request', 'access_group', 'period', 'cell', 'priority', 'requested_on']}
REFERENCES = [('reports', 'zone', 'zones', 'zone'), ('intersections', 'row_a', 'reports', 'row'), ('intersections', 'row_b', 'reports', 'row'), ('requests', 'access_group', 'access', 'group'), ('published', 'access_group', 'access', 'group')]
OBSERVED = [('reports', 'row', 'R5', 2), ('intersections', 'fact', 'O2', 2), ('published', 'release', 'P1', 2)]

class Sources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = {}
        for table, fields in SCHEMAS.items():
            with (SAMPLES / (table + ".csv")).open(encoding="utf-8", newline="") as stream:
                records = csv.DictReader(stream, strict=True)
                if records.fieldnames != fields:
                    raise ValueError(f"字段不一致：{table}")
                cls.tables[table] = list(records)

    def test_records_have_documented_columns(self):
        for table, rows in self.tables.items():
            with self.subTest(table=table):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_source_links(self):
        for left, field, right, target in REFERENCES:
            with self.subTest(table=left, field=field):
                keys = {row[field] for row in self.tables[left] if row[field]}
                self.assertTrue(keys)
                self.assertLessEqual(keys, {row[target] for row in self.tables[right]})

    def test_shared_source_records_are_available(self):
        for table, field, value, seen in OBSERVED:
            with self.subTest(table=table, field=field, value=value):
                self.assertGreaterEqual(sum(row[field] == value for row in self.tables[table]), seen)

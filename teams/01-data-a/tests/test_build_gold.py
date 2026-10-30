"""Run with: python -m unittest discover -s teams/01-data-a/tests -v"""
import base64
import csv
import importlib.util
import io
from pathlib import Path
import tempfile
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'build_gold.py'
spec = importlib.util.spec_from_file_location('g1_build_gold', SCRIPT)
bg = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = bg
spec.loader.exec_module(bg)

HEADER = 'doc_id,read,verdict,diseases,evidence,hex,note\n'


def sample(*records):
    return HEADER + '\n'.join(records) + '\n'


def sub(pack, handle, *records, stamp='', pr=0):
    return bg.Submission(pack, handle, 'fixture-' + handle, sample(*records), (stamp, pr))


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


class BuilderTests(unittest.TestCase):
    def test_gold_requires_two_distinct_full_clean_votes(self):
        docs = [
            sub('code-go', 'alice', '001,full,clean,,,,', '002,partial,clean,,,,',
                '003,full,clean,,,,', '004,full,clean,,,,'),
            sub('code-go', 'bob', '001,full,clean,,,,', '002,full,clean,,,,',
                '003,full,fix,A1,reason,,', '004,full,clean,,,,'),
            sub('code-go', 'carol', '004,full,drop,C1,reason,,'),
            sub('ind-hi-fw2', 'dev', '001,full,clean,,,,'),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            report = bg.build_gold(docs, Path(tmp), target=2)
            self.assertEqual([r['pack_id'] for r in report], ['code-go'])
            self.assertEqual(read_csv(Path(tmp) / 'code-go_gold.csv'), [
                {'doc_id': '001', 'reader_1': 'alice', 'reader_2': 'bob'}
            ])
            self.assertEqual(report[0]['docs_with_2_clean_votes'], 2)
            self.assertEqual(report[0]['disputed_gold_candidates'], 1)
            self.assertEqual(report[0]['gold_docs'], 1)
            self.assertEqual(report[0]['shortfall'], 1)
            self.assertEqual(len(read_csv(Path(tmp) / 'gold_coverage.csv')), 1)

    def test_allow_disputed(self):
        docs = [sub('en-dclm','one','01,full,clean,,,,'),
                sub('en-dclm','two','01,full,clean,,,,'),
                sub('en-dclm','three','01,full,fix,A1,,,'),]
        with tempfile.TemporaryDirectory() as tmp:
            bg.build_gold(docs, Path(tmp), allow_disputed=True)
            self.assertEqual(len(read_csv(Path(tmp) / 'en-dclm_gold.csv')), 1)

    def test_duplicate_votes_and_versions_not_two_reviewers(self):
        old = sub('math-finemath', 'same', 'a,full,clean,,,,')
        updated = sub('math-finemath', 'SAME', 'a,full,clean,,,,',
                      'b,full,clean,,,,', stamp='2026-10-26T12:00:00Z', pr=12)
        other = sub('math-finemath','other','b,full,clean,,,,')
        with tempfile.TemporaryDirectory() as tmp:
            report = bg.build_gold([old,updated,other],Path(tmp))
            self.assertEqual(report[0]['reviewers'],2)
            self.assertEqual(read_csv(Path(tmp)/'math-finemath_gold.csv'), [
                {'doc_id':'b','reader_1':'other','reader_2':'SAME'}
            ])

    def test_conflicting_rows_from_one_reviewer_do_not_count(self):
        docs=[sub('en-test','alice','abc,full,clean,,,,','abc,full,fix,A1,,,'),
              sub('en-test','bob','abc,full,clean,,,,'),
              sub('en-test','carol','abc,full,clean,,,,')]
        warnings=[]
        with tempfile.TemporaryDirectory() as tmp:
            report=bg.build_gold(docs,Path(tmp),warnings=warnings)
            self.assertEqual(report[0]['gold_docs'],1)  # bob + carol
            self.assertTrue(any('conflicting duplicate' in x for x in warnings))

    def test_clean_with_diseases_and_partial_are_not_clean(self):
        docs=[sub('en-test','one','A,full,clean,A1,,,','B,partial,clean,,,,'),
              sub('en-test','two','A,full,clean,,,,','B,full,clean,,,,')]
        with tempfile.TemporaryDirectory() as tmp:
            report=bg.build_gold(docs,Path(tmp))
            self.assertEqual(report[0]['gold_docs'],0)

    def test_explicit_pack_list_yields_empty_gold_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            report = bg.build_gold([],p,expected_packs={'code-rust'})
            self.assertEqual(report[0]['gold_docs'],0)
            self.assertEqual((p/'code-rust_gold.csv').read_text(), 'doc_id,reader_1,reader_2\n')

    def test_scans_local_submissions_and_ignores_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'diagnosis'/'submissions'/'code-go'/'alice'
            p.mkdir(parents=True)
            (p/'labels.csv').write_text(sample('ABC,full,clean,,,,'), encoding='utf-8')
            local=bg.local_submissions(Path(tmp))
            self.assertEqual(len(local),1)
            self.assertEqual(local[0].pack_id, 'code-go')
            self.assertEqual(local[0].handle, 'alice')

    def test_github_pr_blob_loading(self):
        class StubAPI:
            def paged(self, endpoint):
                if 'pulls?state=open' in endpoint:
                    return iter([{'number':12,'updated_at':'2026-10-26T00:00:00Z',
                                  'base':{'ref':'main'}}])
                if 'pulls/12/files' in endpoint:
                    return iter([{'filename':'diagnosis/submissions/code-go/Alice/labels.csv',
                                  'status':'added','sha':'abc123'},
                                 {'filename':'diagnosis/submissions/code-go/Alice/medicine.md',
                                  'status':'added','sha':'other'}])
                raise AssertionError(endpoint)
            def get(self, endpoint):
                if endpoint.endswith('git/blobs/abc123'):
                    return {'encoding':'base64','content':base64.b64encode(sample('one,full,clean,,,,').encode()).decode()}
                raise AssertionError(endpoint)
        pr=bg.github_pr_submissions(StubAPI(), 'theschoolofai/era-v5-lab')
        self.assertEqual(len(pr),1)
        self.assertEqual(pr[0].handle,'Alice')
        self.assertEqual(bg.parse_labels(pr[0],[])['one'].clean,True)

    def test_malformed_sheet_is_skipped_counted_and_warned(self):
        broken = bg.Submission('en-test','carol','bad-file','doc_id,read,verdict\na,full,clean\n',('',0))
        docs=[broken, sub('en-test','alice','a,full,clean,,,,'), sub('en-test','bob','a,full,clean,,,,')]
        warnings=[]
        with tempfile.TemporaryDirectory() as tmp:
            report=bg.build_gold(docs,Path(tmp),warnings=warnings)
        self.assertEqual(report[0]['skipped_label_files'],1)
        self.assertEqual(report[0]['label_files'],2)
        self.assertEqual(report[0]['gold_docs'],1)
        self.assertTrue(any('bad-file' in w and 'missing required columns' in w for w in warnings))

    def test_evidence_cell_over_csv_default_limit_is_read(self):
        long_evidence = 'x' * 150_000  # over the csv module default of 131072 characters
        docs=[sub('sci-test','alice','a,full,fix,C2,' + long_evidence + ',,','b,full,clean,,,,'),
              sub('sci-test','bob','b,full,clean,,,,')]
        with tempfile.TemporaryDirectory() as tmp:
            report=bg.build_gold(docs,Path(tmp))
            self.assertEqual(report[0]['skipped_label_files'],0)
            self.assertEqual(report[0]['gold_docs'],1)


if __name__ == '__main__':
    unittest.main()

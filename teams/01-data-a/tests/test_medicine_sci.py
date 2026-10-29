"""Tests for sci-medicines/medicine_sci.md. Run: python -I -m unittest discover -s teams/01-data-a/tests"""
import importlib.util
import sys
import unittest
from pathlib import Path

TEAM = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TEAM / "tools"))  # python -I: not on the path by itself
import harm_test  # noqa: E402

SHEET = TEAM / "sci-medicines" / "medicine_sci.md"


@unittest.skipUnless(importlib.util.find_spec("regex"), "two Science rules need: pip install regex")
class PhoneMaskCase(unittest.TestCase):
    """DA-F1-004 hides every number of a list in one run, and a second run changes nothing (RULES 2)."""

    @classmethod
    def setUpClass(cls):
        ns, _ = harm_test.load_rules(SHEET)
        cls.rule = staticmethod(ns["RULES_BY_ID"]["DA-F1-004"])  # not a method: no self

    def run_rule(self, text):
        return self.rule({"doc_id": "t", "text": text, "lang_label": "eng_Latn"})[1]

    def test_a_long_list_is_masked_in_one_run(self):
        text = "Phone: " + ", ".join(f"{100 + i}-{2000 + i}" for i in range(15))
        once = self.run_rule(text)
        self.assertEqual(once, "Phone: " + ", ".join(["<PHONE>"] * 15))
        self.assertEqual(self.run_rule(once), once)

    def test_two_numbers_after_one_phone_word(self):
        once = self.run_rule("Tel: 123-4567 / 765-4321")
        self.assertEqual(once, "Tel: <PHONE> / <PHONE>")
        self.assertEqual(self.run_rule(once), once)

    def test_list_words_or_and_and(self):
        once = self.run_rule("Call 123-4567 or 765-4321 and 555-0199")
        self.assertEqual(once, "Call <PHONE> or <PHONE> and <PHONE>")
        self.assertEqual(self.run_rule(once), once)

    def test_a_number_after_other_words_is_not_chained(self):
        once = self.run_rule("Fax: 555-123-4567. Funded 2019-2020 by grant 12-345-678.")
        self.assertEqual(once, "Fax: <PHONE>. Funded 2019-2020 by grant 12-345-678.")
        self.assertEqual(self.run_rule(once), once)

    def test_a_number_without_a_phone_word_is_kept(self):
        text = "The sample weighed 123-4567 units."
        self.assertEqual(self.run_rule(text), text)


if __name__ == "__main__":
    unittest.main()

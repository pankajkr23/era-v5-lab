# Science medicines

The medicines of the Science pack (`sci-finepdfs`) as rules that the team's harm test runs unchanged.

| File | What it is |
| --- | --- |
| `medicine_sci.md` | the rule sheet: one `RULE_ID` block per rule (`RULE_ID`, `CODE`, `ACTION`, `LANGS`, `ORIGIN`, `AUTHOR`, `medicine(doc)`) |
| `MEDICINE_CHECK.md` | output of `tools/medicine_conflicts.py` |

## Run the harm test

One rule:

```bash
python -I teams/01-data-a/tools/harm_test.py --pack <path>/sci-finepdfs.parquet --gold teams/01-data-a/gold/sci-finepdfs_gold.csv --rules teams/01-data-a/sci-medicines/medicine_sci.md --rule DA-F1-004
```

Every rule in the sheet, alone and then all in order:

```bash
python -I teams/01-data-a/tools/harm_test.py --pack <path>/sci-finepdfs.parquet --gold teams/01-data-a/gold/sci-finepdfs_gold.csv --rules teams/01-data-a/sci-medicines/medicine_sci.md --rule all
```

Add `--debug` to list the gold doc_ids that a rule changes.

## Status (30 Oct)

| | |
| --- | --- |
| Rules | 14, all PASS on gold 40, alone and all in order |
| Withdrawn | `DA-C2-005`, `DA-D1-001`: fail the harm test; reasons in their sections of `medicine_sci.md` |
| Recoded | `DA-C1-008` → `DA-C2-006`: it removes repeated lines, which is C2 |

Withdrawn and old IDs stay in the sheet as `RULE_ID` lines in text blocks, so `medicine_extract.py` never gives them
to another rule.

`MEDICINE_CHECK.md` flags "NO RULE: C2". That is how the tool counts, not a gap: it credits a rule only against its
author's own `medicine.md` sections. C2 (39 cases in aneeshads's sheet) is covered by `DA-C2-006`, but its author
jssunil's `medicine.md` has no `**Disease:**` sections to match it to.

## Before you run

- The pack Parquet file is not in the repo; give its local path in `--pack`.
- `DA-A6-002` and `DA-D3-002` need `pip install regex`.
- Every Science document has the language label `eng_Latn`, so the rules here use `LANGS = {"eng_Latn"}`. A rule
  written for `LANGS = {"en", "eng"}` changes nothing on this pack.

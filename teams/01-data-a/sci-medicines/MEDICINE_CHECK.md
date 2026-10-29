# Medicine check

Medicine sheets: `runs/fetch/diagnosis/submissions`. Gold files: `teams/01-data-a/gold`. Rules: `medicine_sci.md`. Made by `medicine_conflicts.py`; no code was run.
"Can run" means that the rule's code defines every name it needs. It says nothing about the harm test: run `harm_test.py` for that.

## Summary

| Gold file | Gold docs | Sheets | Rules | Rules that can run | Flags |
|---|---|---|---|---|---|
| sci-finepdfs_gold.csv | 40 | 2 | 9 | 7 | ONE ANNOTATOR, NO RULE, SMALL GOLD SET |

## sci-finepdfs

- Gold set: sci-finepdfs_gold.csv, 40 documents (1% allows 0); 40 of the target 200 (BELOW_TARGET)

| Annotator | Sheet | Rules | Can run |
|---|---|---|---|
| aneeshads | 8 medicines | 7 | 7 |
| jssunil | no medicine sections | 2 | 2 |

### Flags

- **ONE ANNOTATOR**: only aneeshads wrote medicines
- **NO RULE**: C2: found more than 5 times (39) and no rule that can run
- **SMALL GOLD SET**: 40 documents: 1% allows 0, so one touched document fails a rule

### Medicines with the same code

No code has more than one medicine.

## Across the packs of one language

No code is treated in more than one pack of a language.

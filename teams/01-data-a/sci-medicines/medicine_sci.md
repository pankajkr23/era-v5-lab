# medicine_sci: standard Science medicines (sci-finepdfs)

**Draft for spec v1 (PK, 30 Oct). Science domain owner's sheet; not yet reviewed by the team.**

Pack: sci-finepdfs (500 documents, every one labelled `eng_Latn`). Gold: the team file `gold/sci-finepdfs_gold.csv`, 40 documents from all 3 label sheets. Before the `build_gold.py` fix that comes with this sheet (a label sheet with a cell over 131,072 characters could not be read) it had 26; the "gold 26" column below is that older file.
Rule form: `RULE_ID`, `CODE`, `ACTION`, `LANGS`, `ORIGIN`, `AUTHOR`; `medicine(doc) -> (action, text)`. The same form as the English and Code sheets that were on `g1-harm-test` until 29 Oct (`f96453c` took them out of the branch), so `tools/harm_test.py` runs it unchanged. `LANGS = {"eng_Latn"}`: the English sheet used `{"en", "eng"}`, which does not match this pack's label and would leave every Science document unchanged.
Each author's code is copied unchanged from their `medicine.md` (jssunil PR #35, aneeshads PR #120), except list matching and two guards added to `DA-F1-004` so that it masks a list in one run and is idempotent; only the rule header, `_std` and `medicine(doc)` are added (and one word list for `DA-D1-001`, which its author did not give; that rule is now withdrawn). IDs: next free number after `rules/registry.json`, `medicine_code.md`, `medicine_en.md` and `reports/` (29 Oct). Withdrawn and recoded IDs stay in this sheet as `RULE_ID` lines in text blocks, so `medicine_extract.py` never gives them out again.
Labelled rows: fix or drop rows of the 3 Science label sheets (jssunil, patilvijay23, aneeshads; 135 documents) that carry the rule's code; "fixes" = the rule changes or drops that document.
Decision: guideline 2 (R7): a rule that fails is out; of the rest, the one that fixes the most labelled rows is kept, another only if it fixes different rows.

| # | ID | disease | action | author | gold 26 | gold 40 | labelled rows fixed | pack changed/dropped | decision |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `DA-D3-002` | D3 mixed language | drop | aneeshads | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 1/8 | 0/2 | KEEP |
| 2 | `DA-A1-004` | A1 invisible characters | fix | aneeshads | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 4/5 | 5/0 | KEEP |
| 3 | `DA-A6-002` | A6 mixed script in a word | fix | aneeshads | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 3/10 | 6/0 | KEEP |
| 4 | `DA-A6-003` | A6 mixed script in a word | fix | jssunil | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 1/10 | 3/0 | DROP |
| 5 | `DA-B2-003` | B2 HTML tags | fix | aneeshads | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 9/9 | 14/0 | KEEP |
| 6 | `DA-B2-004` | B2 HTML tags | fix | jssunil | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 9/9 | 15/0 | DROP |
| 7 | `DA-B4-010` | B4 placeholders | fix | jssunil | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 54/55 | 121/0 | KEEP |
| 8 | `DA-B5-002` | B5 broken Markdown or LaTeX | fix | aneeshads | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 4/19 | 15/0 | KEEP |
| 9 | `DA-C1-007` | C1 boilerplate | fix | aneeshads | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 14/58 | 27/0 | KEEP |
| 10 | `DA-C2-006` (was `DA-C1-008`) | C2 repeated lines (running headers) | fix | jssunil | 0.00% (0/26) PASS | 0.00% (0/40) PASS | C2 28/46 (C1 38/58) | 93/0 | KEEP |
| 11 | `DA-C2-005` | C2 repeated lines | fix | aneeshads | 0.00% (0/26) PASS | 5.00% (2/40) FAIL | 29/46 | 94/0 | **WITHDRAWN** |
| 12 | `DA-C3-006` | C3 truncated document | fix | jssunil | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 0/13 | 0/0 | DROP |
| 13 | `DA-C4-002` | C4 two documents joined | fix | jssunil | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 1/2 | 1/0 | DROP |
| 14 | `DA-D1-001` | D1 wrong language label | fix | jssunil | 69.23% (18/26) FAIL | 70.00% (28/40) FAIL | 2/3 | 390/0 | **WITHDRAWN** |
| 15 | `DA-F1-004` | F1 personal data (phone numbers) | fix | aneeshads | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 47/77 | 81/0 | KEEP |
| 16 | `DA-F1-005` | F1 personal data (phone numbers) | fix | jssunil | 0.00% (0/26) PASS | 0.00% (0/40) PASS | 33/77 | 52/0 | DROP |

**The 9 KEEP rules together, in sheet order:** gold 26: 0 changed, 0 dropped, PASS; gold 40: 0 changed, 0 dropped, PASS. **Withdrawn 30 Oct (PK):** `DA-C2-005` and `DA-D1-001`; the reasons are in their sections, and their IDs stay reserved. **The whole sheet (14 rules) in order** (team `harm_test.py` at `f96453c`, `--rule all`): gold 40: 0 changed, 0 dropped, 0.00% PASS; every rule alone PASS.

## 1. `DA-D3-002` · D3 mixed language · drop · aneeshads

1. **Disease:** D3 mixed language. Labelled documents with D3 (fix or drop, 3 sheets): 8. Labelled documents this rule acts on: `28bb6f385b19eda4`.
2. **Medicine:** Drop a document only when more than half of its letters are in paragraphs that are not English (mostly non-Latin letters, or at least 2 function words of another language and more than twice the English ones). Mixed text below that share is kept, because an organisation's foreign name or a foreign table header is normal in a PDF. Source: aneeshads's `medicine.md`, medicine 6 (`cure_d3`).

```python
RULE_ID = "DA-D3-002"
CODE = "D3"
ACTION = "drop"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "aneeshads"  # aneeshads's medicine.md, medicine 6

import re
import regex

D3_EN = set("the of and to in is that for on with as by are be this it from or at an was which not have has "
            "were their its can will these but been more also all would there they".split())

D3_OTHER = set(("der die das und ist nicht mit von zu den ein eine dem auf für sich auch "
                "le la les des est une dans pour pas que qui du au sur avec sont "
                "el los las es una por para con del se como más su "
                "il di che della per non sono gli nel alla "
                "ja on ei että ovat oli kanssa myös tai kuin sekä "
                "ir yra kad su iš ar buvo nuo bei "
                "un ar uz par kas tiek "
                "je na za od da su kao ili ali biti "
                "och att det som är för med på av inte "
                "het een van zijn niet voor met ook").split())

D3_DROP_SHARE = 0.5

def d3_foreign_share(text):
    total = foreign = 0
    for para in re.split(r"\n\s*\n", text):
        letters = regex.findall(r"\p{L}", para)
        if not letters:
            continue
        non_latin = sum(1 for c in letters if not regex.match(r"\p{sc=Latin}", c))
        words = [w.lower() for w in regex.findall(r"\p{L}+", para)]
        en = sum(w in D3_EN for w in words)
        other = sum(w in D3_OTHER for w in words)
        total += len(letters)
        if non_latin / len(letters) > 0.5 or (other >= 2 and other > 2 * en):
            foreign += len(letters)
    return foreign / max(1, total)

def cure_d3(text):
    return ("drop", "") if d3_foreign_share(text) > D3_DROP_SHARE else text


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(cure_d3(text), text)
```

3. **Action:** drop.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-D3-002`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 1/8. Whole pack: 0 changed, 2 dropped.
5. **Side effects:** An English page with long foreign quotations can pass 50% and be dropped; a language that is not in its word list (Portuguese, Polish, Czech) counts as English (author's notes).

**Decision (guideline 2):** KEEP: the only D3 rule; passes.

## 2. `DA-A1-004` · A1 invisible characters · fix · aneeshads

1. **Disease:** A1 invisible characters. Labelled documents with A1 (fix or drop, 3 sheets): 5. Labelled documents this rule acts on: `24d318c42b937b21`, `78687cb0dc7a4f80`, `b64c51d59247a36c`.
2. **Medicine:** Delete the emoji variation selectors U+FE0E/U+FE0F, zero-width space U+200B, BOM U+FEFF, soft hyphen U+00AD and the bidi controls U+202A-U+202E, U+2066-U+2069. ZWJ U+200D and ZWNJ U+200C are not in the list. Source: aneeshads's `medicine.md`, medicine 7 (`cure_a1`).

```python
RULE_ID = "DA-A1-004"
CODE = "A1"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "aneeshads"  # aneeshads's medicine.md, medicine 7

import re

A1_JUNK = re.compile("[\uFE0E\uFE0F\u200B\uFEFF\u00AD\u202A-\u202E\u2066-\u2069]")

def cure_a1(text):
    return A1_JUNK.sub("", text)


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(cure_a1(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-A1-004`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 4/5. Whole pack: 5 changed, 0 dropped.
5. **Side effects:** An emoji that needs U+FE0F for colour shows as the plain symbol.

**Decision (guideline 2):** KEEP: the only A1 rule; passes.

## 3. `DA-A6-002` · A6 mixed script in a word · fix · aneeshads

1. **Disease:** A6 mixed script in a word. Labelled documents with A6 (fix or drop, 3 sheets): 10. Labelled documents this rule acts on: `12e943fb710cab5b`, `cdc5973ec2161f44`, `f5faeb5d20b73087`.
2. **Medicine:** In a word that mixes Latin and Cyrillic, write it in the script of most of its letters; delete a Chinese, Japanese or Korean character glued to a Latin word when such characters are 1% or less of the letters. Greek letters in Latin words (units, gene names) are never changed. Source: aneeshads's `medicine.md`, medicine 5 (`cure_a6`).

```python
RULE_ID = "DA-A6-002"
CODE = "A6"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "aneeshads"  # aneeshads's medicine.md, medicine 5

import regex

A6_WORD = regex.compile(r"[\p{L}\p{M}]+")

A6_CJK = regex.compile(r"[\p{sc=Han}\p{sc=Hiragana}\p{sc=Katakana}\p{sc=Hangul}]+")

A6_CJK_SHARE = 0.01

A6_LAT_TO_CYR = dict(zip(map(ord, "aceopxyjsABCEHKMOPTX"), "асеорхујѕАВСЕНКМОРТХ"))

A6_CYR_TO_LAT = dict(zip(map(ord, "абвгдђежзијклљмнњопрстћуфхцчџшАБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШіІѕЅ"),
                         ["a", "b", "v", "g", "d", "đ", "e", "ž", "z", "i", "j", "k", "l", "lj", "m", "n", "nj",
                          "o", "p", "r", "s", "t", "ć", "u", "f", "h", "c", "č", "dž", "š",
                          "A", "B", "V", "G", "D", "Đ", "E", "Ž", "Z", "I", "J", "K", "L", "Lj", "M", "N", "Nj",
                          "O", "P", "R", "S", "T", "Ć", "U", "F", "H", "C", "Č", "Dž", "Š", "i", "I", "s", "S"]))

def a6_fix_word(m):
    w = m.group()
    lat = len(regex.findall(r"\p{sc=Latin}", w))
    cyr = len(regex.findall(r"\p{sc=Cyrillic}", w))
    if not lat or not cyr or lat == cyr:
        return w
    if cyr > lat:
        fixed = regex.sub(r"\p{sc=Latin}", lambda c: c.group().translate(A6_LAT_TO_CYR), w)
        if not regex.search(r"\p{sc=Latin}", fixed):
            return fixed                              # подготовкa -> подготовка
    return w.translate(A6_CYR_TO_LAT)

def cure_a6(text):
    if regex.search(r"\p{sc=Cyrillic}", text):
        text = A6_WORD.sub(a6_fix_word, text)
    cjk = sum(len(r) for r in A6_CJK.findall(text))
    if cjk and cjk / max(1, len(regex.findall(r"\p{L}", text))) <= A6_CJK_SHARE:
        text = regex.sub(r"(?<=\p{sc=Latin})" + A6_CJK.pattern + r"|" + A6_CJK.pattern + r"(?=\p{sc=Latin})",
                         "", text)                    # raise立ts -> raisets, smooth抽吸 -> smooth
    return text


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(cure_a6(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-A6-002`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 3/10. Whole pack: 6 changed, 0 dropped.
5. **Side effects:** Deleting a glued CJK character can leave a broken word; Greek letters are kept on purpose, so most labelled A6 rows (Greek in units and gene names) are not changed (author's notes).

**Decision (guideline 2):** KEEP: passes and fixes the most labelled A6 rows (3 of 10).

## 4. `DA-A6-003` · A6 mixed script in a word · fix · jssunil

1. **Disease:** A6 mixed script in a word. Labelled documents with A6 (fix or drop, 3 sheets): 10. Labelled documents this rule acts on: `cdc5973ec2161f44`.
2. **Medicine:** In a word that mixes Latin and Cyrillic letters, turn the Cyrillic look-alike letters into Latin ones. Source: jssunil's `medicine.md`, medicine 6 (`fix_mixed_script_words`).

```python
RULE_ID = "DA-A6-003"
CODE = "A6"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "jssunil"  # jssunil's medicine.md, medicine 6

import re

CYR_TO_LAT = str.maketrans({'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X', 'а': 'a', 'е': 'e', 'и': 'i', 'м': 'm', 'о': 'o', 'р': 'p', 'с': 'c', 'т': 't', 'х': 'x'})
MIXED_WORD_RE = re.compile(r'\b(?:[A-Za-z]+[\u0400-\u04FF]+[A-Za-z0-9]*|[\u0400-\u04FF]+[A-Za-z]+[A-Za-z0-9]*)\b')

def fix_mixed_script_words(text: str) -> str:
    return MIXED_WORD_RE.sub(lambda m: m.group(0).translate(CYR_TO_LAT), text)


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(fix_mixed_script_words(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-A6-003`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 1/10. Whole pack: 3 changed, 0 dropped.
5. **Side effects:** Only Cyrillic-to-Latin; a Cyrillic-majority word with one Latin look-alike is turned Latin too.

**Decision (guideline 2):** DROP: passes, but its one labelled row is also fixed by `DA-A6-002`.

## 5. `DA-B2-003` · B2 HTML tags · fix · aneeshads

1. **Disease:** B2 HTML tags. Labelled documents with B2 (fix or drop, 3 sheets): 9. Labelled documents this rule acts on: `1cc10779aced9a7f`, `2b60daba400d7754`, `4656c1ed1d4393c4`.
2. **Medicine:** `<sup>x</sup>` -> `^x`, `<sub>x</sub>` -> `_x`, `<br>` -> `; ` (a table cell cannot hold a newline), and delete `<b> <i> <u> <em> <strong> <span> <div> <p> <font>` tags. Source: aneeshads's `medicine.md`, medicine 8 (`cure_b2`).

```python
RULE_ID = "DA-B2-003"
CODE = "B2"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "aneeshads"  # aneeshads's medicine.md, medicine 8

import re

B2_SUP = re.compile(r"<sup>(.*?)</sup>", re.I)

B2_SUB = re.compile(r"<sub>(.*?)</sub>", re.I)

B2_BR = re.compile(r"\s*<br\s*/?>\s*", re.I)

B2_TAG = re.compile(r"</?(?:b|i|u|em|strong|span|div|p|font)(?:\s+[a-z-]+=[^<>\n]{0,80})?\s*/?>", re.I)

def cure_b2(text):
    text = B2_SUP.sub(r"^\1", text)       # 6<sup>a</sup> -> 6^a
    text = B2_SUB.sub(r"_\1", text)       # H<sub>2</sub>O -> H_2O
    text = B2_BR.sub(lambda m: " " if text[m.start() - 1:m.start()] in ";,.:" else "; ", text)  # in a table cell
    return B2_TAG.sub("", text)


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(cure_b2(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-B2-003`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 9/9. Whole pack: 14 changed, 0 dropped.
5. **Side effects:** A `<br>` between two list items joins them with `; `; a page that teaches HTML loses its tags.

**Decision (guideline 2):** KEEP (**PK to confirm**): ties with `DA-B2-004` (both pass, both fix the same 9 of 9 rows). Chosen because `<br>` -> `; ` keeps a Markdown table cell on one line; guideline 2 has no tie rule.

## 6. `DA-B2-004` · B2 HTML tags · fix · jssunil

1. **Disease:** B2 HTML tags. Labelled documents with B2 (fix or drop, 3 sheets): 9. Labelled documents this rule acts on: `1cc10779aced9a7f`, `2b60daba400d7754`, `4656c1ed1d4393c4`.
2. **Medicine:** `<sup>x</sup>` -> `^x`, `<sub>x</sub>` -> `_x`, `<br>` -> newline, and delete `<div> <p> <span> <table> <tr> <td> <th>` tags. Source: jssunil's `medicine.md`, medicine 5 (`clean_pdf_html_tags`).

```python
RULE_ID = "DA-B2-004"
CODE = "B2"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "jssunil"  # jssunil's medicine.md, medicine 5

import re

def clean_pdf_html_tags(text: str) -> str:
    text = re.sub(r'<sup>(.*?)</sup>', r'^\1', text, flags=re.IGNORECASE)
    text = re.sub(r'<sub>(.*?)</sub>', r'_\1', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', r'\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?(?:div|p|span|table|tr|td|th)[^>]*>', '', text, flags=re.IGNORECASE)
    return text


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(clean_pdf_html_tags(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-B2-004`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 9/9. Whole pack: 15 changed, 0 dropped.
5. **Side effects:** A `<br>` inside a Markdown table cell becomes a newline and splits the table row.

**Decision (guideline 2):** DROP (**PK to confirm**): tie with `DA-B2-003`, same 9 rows; its `<br>` -> newline can break a table row.

## 7. `DA-B4-010` · B4 placeholders · fix · jssunil

1. **Disease:** B4 placeholders. Labelled documents with B4 (fix or drop, 3 sheets): 55. Labelled documents this rule acts on: `031d526e862d6f22`, `053c80cc1a9b16bc`, `0798582b775b470f`.
2. **Medicine:** Replace the upstream synthetic address `...@example.org/.com` by `<EMAIL>`, and delete unrendered template parameters such as `<parameter 1>` or `<typename T>`. Source: jssunil's `medicine.md`, medicine 3 (`clean_placeholders`).

```python
RULE_ID = "DA-B4-010"
CODE = "B4"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "jssunil"  # jssunil's medicine.md, medicine 3

import re

SYNTHETIC_EMAIL_RE = re.compile(r'\b[A-Za-z0-9._%+-]+@example\.(?:org|com)\b')
TEMPLATE_PARAM_RE = re.compile(r'<(?:parameter|function name|process description|typename|see attached)[^>]*>', re.IGNORECASE)

def clean_placeholders(text: str) -> str:
    text = SYNTHETIC_EMAIL_RE.sub('<EMAIL>', text)
    text = TEMPLATE_PARAM_RE.sub('', text)
    return text


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(clean_placeholders(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-B4-010`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 54/55. Whole pack: 121 changed, 0 dropped.
5. **Side effects:** A text about the example.com domain would get `<EMAIL>`; the address token is `<EMAIL>`, the same as the PII placeholders that the code packs remove: the team must agree on one form.

**Decision (guideline 2):** KEEP: the only B4 rule; passes; fixes 54 of 55 labelled rows.

## 8. `DA-B5-002` · B5 broken Markdown or LaTeX · fix · aneeshads

1. **Disease:** B5 broken Markdown or LaTeX. Labelled documents with B5 (fix or drop, 3 sheets): 19. Labelled documents this rule acts on: `80c340aef304a24c`, `826838553e94b937`, `ae0c958288200e55`.
2. **Medicine:** A LaTeX `\footnote{...}` left in the prose becomes the footnote text in brackets; an unclosed one loses only the command. Inline math and footnote markers are left alone. Source: aneeshads's `medicine.md`, medicine 3 (`cure_b5`).

```python
RULE_ID = "DA-B5-002"
CODE = "B5"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "aneeshads"  # aneeshads's medicine.md, medicine 3

def cure_b5(text):
    out, i = [], 0
    while True:
        j = text.find("\\footnote{", i)
        if j < 0:
            out.append(text[i:])
            return "".join(out)
        out.append(text[i:j])
        k, depth = j + len("\\footnote{"), 1
        while k < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[k], 0) if text[k - 1] != "\\" else 0
            k += 1
        if depth:                                    # never closed: keep the words, drop the command
            out.append(" ")
            i = j + len("\\footnote{")
        else:                                        # \footnote{X} -> " (X)"
            out.append(" (" + text[j + len("\\footnote{"):k - 1].strip() + ")")
            i = k


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(cure_b5(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-B5-002`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 4/19. Whole pack: 15 changed, 0 dropped.
5. **Side effects:** A long footnote in brackets breaks its sentence; most labelled B5 rows are `\(^2\)` markers and `$...$` math, which the gold readers accepted, so the rule leaves them.

**Decision (guideline 2):** KEEP: the only B5 rule; passes.

## 9. `DA-C1-007` · C1 boilerplate · fix · aneeshads

1. **Disease:** C1 boilerplate. Labelled documents with C1 (fix or drop, 3 sheets): 58. Labelled documents this rule acts on: `3994bec2f780bbc1`, `42251c5ad07d17d4`, `4b958ac1f45443b5`.
2. **Medicine:** Delete a line of at most 200 characters that starts with `Copyright`, or contains `All rights reserved`, or is the page navigation `First page Prev. page`. Source: aneeshads's `medicine.md`, medicine 4 (`cure_c1`).

```python
RULE_ID = "DA-C1-007"
CODE = "C1"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "aneeshads"  # aneeshads's medicine.md, medicine 4

import re

C1_LINE = re.compile(r"^\W{0,3}(?:©\s*)?copyright\b|all rights reserved|first page\s+prev\.? page", re.I)

C1_MAX_LINE = 200

def cure_c1(text):
    lines = text.split("\n")
    return "\n".join(l for l in lines if len(l) > C1_MAX_LINE or not C1_LINE.search(l))


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(cure_c1(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-C1-007`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 14/58. Whole pack: 27 changed, 0 dropped.
5. **Side effects:** A short legal line that starts with the word Copyright is removed.

**Decision (guideline 2):** KEEP: passes; fixes 8 labelled C1 rows that `DA-C2-006` (was `DA-C1-008`) does not (copyright lines).

## 10. `DA-C2-006` · C2 repeated lines (running headers) · fix · jssunil

**Recoded 30 Oct (PK): was `DA-C1-008`.** DISEASES.md: C1 = boilerplate (menus, cookie banners, footer links), C2 = the same line many times in one document. This rule removes repeated lines, so it is C2. The old ID stays reserved:

```text
RULE_ID = "DA-C1-008"  # recoded to DA-C2-006 on 30 Oct 2026: ID reserved, do not reuse
```

1. **Disease:** C2 repeated lines (running page headers and footers). Labelled documents with C2 (fix or drop, 3 sheets): 46; its author labelled them C1 (58 labelled C1 documents). Labelled documents this rule acts on: `053c80cc1a9b16bc`, `0e4cfb3b81d67dc5`, `135ae306b27ebd17`.
2. **Medicine:** A line of 15 or more characters that repeats 5 or more times is a running page header or footer: keep the first copy, delete the rest. Table borders, LaTeX environments and one roll-call refrain are excluded. (Same idea as the withdrawn `DA-C2-005`, with 5 copies instead of 4; labelled C1 by its author.) Source: jssunil's `medicine.md`, medicine 1 (`remove_running_headers`).

```python
RULE_ID = "DA-C2-006"
CODE = "C2"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "jssunil"  # jssunil's medicine.md, medicine 1

import re
from collections import Counter

TABLE_BORDER = re.compile(r'^[\s|:\-]+$')
MATH_ENV = re.compile(r'\\(begin|end)\{(?:cases|align\*?|equation\*?)\}|\\hline')

def remove_running_headers(text: str, min_len: int = 15, min_repeats: int = 5) -> str:
    lines = text.split('\n')
    counts = Counter(l.strip() for l in lines)
    header_candidates = {
        s for s, c in counts.items()
        if len(s) >= min_len and c >= min_repeats
        and not TABLE_BORDER.match(s) and not MATH_ENV.search(s) and 'Motion Carried.' not in s
    }
    if not header_candidates:
        return text
    kept, seen = [], set()
    for line in lines:
        s = line.strip()
        if s in header_candidates:
            if s in seen:
                continue
            seen.add(s)
        kept.append(line)
    return '\n'.join(kept)


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(remove_running_headers(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-C2-006`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: C2 28/46 (C1 38/58). Whole pack: 93 changed, 0 dropped.
5. **Side effects:** Real lines repeated 5+ times are reduced to one (a role line under each signature, a roll-call line); a header with a page number inside it is not found.

**Decision (guideline 2):** KEEP: passes on both gold sets; fixes 28 of 46 labelled C2 documents (and 38 of 58 labelled C1). **Code:** recoded C1 → C2 by PK on 30 Oct (it removes repeated lines, which DISEASES.md calls C2).

## 11. `DA-C2-005` · C2 repeated lines · **WITHDRAWN** (30 Oct, PK) · aneeshads

The ID stays reserved, so no new rule gets it (`medicine_extract.py` skips IDs found in `*-medicines` sheets):

```text
RULE_ID = "DA-C2-005"  # withdrawn 30 Oct 2026: ID reserved, do not reuse
```

1. **Was for:** C2 repeated lines. Labelled documents with C2 (fix or drop, 3 sheets): 46.
2. **What it did:** a line of 15 or more characters with at least two words that appears 4 or more times was taken as a running header: the first copy kept, the rest deleted. LaTeX lines and table rows were never touched. Source: aneeshads's `medicine.md`, medicine 1 (`cure_c2`), PR #120.
3. **Harm test** (team `harm_test.py` at `f96453c`, 29 Oct): gold 40: 2 changed, 0 dropped, 5.00% (2/40) **FAIL** (`39857b0ef2904033`, `d1b2e193abc4a5f3`); gold 26: 0.00% PASS. Labelled C2 documents fixed: 29/46. Whole pack: 94 of 500 changed.
4. **Why withdrawn:**
   - It fails on gold 40. In both gold documents it deletes short lines (16 to 23 characters) that appear exactly 4 times. Its author had listed them as side effects (an address and a form line).
   - A narrower version adds nothing. With 5 or more copies it passes (0/40) and fixes 23 of the 46 labelled C2 documents, but `DA-C2-006` (was `DA-C1-008`) already fixes every one of those 23. Requiring the copies to spread over at least half the document also passes (0/40) but fixes only 21.
   - R7: of two rules for the same rows, keep the one that passes and fixes the most. That is `DA-C2-006` (was `DA-C1-008`; 0/40, 28 of the 46 C2 documents). This rule alone reaches 3 more documents, and only in the 4-copy form that fails.
5. **Code:** removed from this sheet; the original is in the source above.

## 12. `DA-C3-006` · C3 truncated document · fix · jssunil

1. **Disease:** C3 truncated document. Labelled documents with C3 (fix or drop, 3 sheets): 13. Labelled documents this rule acts on: none.
2. **Medicine:** If the last line is an unfinished Markdown table row (starts with `|`, has 2 or more `|`, does not end with `|`), delete that line. Source: jssunil's `medicine.md`, medicine 4 (`clean_truncated_tables`).

```python
RULE_ID = "DA-C3-006"
CODE = "C3"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "jssunil"  # jssunil's medicine.md, medicine 4

def clean_truncated_tables(text: str) -> str:
    lines = text.rstrip().split('\n')
    if lines:
        last = lines[-1].strip()
        if last.startswith('|') and not last.endswith('|') and last.count('|') >= 2:
            lines = lines[:-1]
    return '\n'.join(lines)


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(clean_truncated_tables(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-C3-006`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 0/13. Whole pack: 0 changed, 0 dropped.
5. **Side effects:** None seen; it never acts on this pack.

**Decision (guideline 2):** DROP: passes, but fixes 0 of 13 labelled C3 rows and changes 0 of 500 pack documents.

## 13. `DA-C4-002` · C4 two documents joined · fix · jssunil

1. **Disease:** C4 two documents joined. Labelled documents with C4 (fix or drop, 3 sheets): 2. Labelled documents this rule acts on: `6acc7c94105bdebd`.
2. **Medicine:** When `To the Editor:` starts a line twice or more, keep the text up to the end of the first letter. (Its author calls it a split; the code keeps only the first letter and deletes the rest.) Source: jssunil's `medicine.md`, medicine 8 (`split_joined_letters`).

```python
RULE_ID = "DA-C4-002"
CODE = "C4"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "jssunil"  # jssunil's medicine.md, medicine 8

import re

SECOND_LETTER_RE = re.compile(r'\n(To the Editor:)', re.IGNORECASE)

def split_joined_letters(text: str) -> str:
    parts = SECOND_LETTER_RE.split(text)
    if len(parts) <= 3:
        return text
    return parts[0] + '\n' + parts[1] + parts[2]


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(split_joined_letters(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-C4-002`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 1/2. Whole pack: 1 changed, 0 dropped.
5. **Side effects:** Deletes all letters after the first one in a page of joined letters.

**Decision (guideline 2):** DROP: the C4 ruling is split at the boundary or drop [G-CHAT#20]; this code deletes everything after the first letter, which is neither.

## 14. `DA-D1-001` · D1 wrong language label · **WITHDRAWN** (30 Oct, PK) · jssunil

The ID stays reserved, so no new rule gets it (`medicine_extract.py` skips IDs found in `*-medicines` sheets):

```text
RULE_ID = "DA-D1-001"  # withdrawn 30 Oct 2026: ID reserved, do not reuse
```

1. **Was for:** D1 wrong language label. Labelled documents with D1 (fix or drop, 3 sheets): 3 (`51a4fb599da754db`, `bfbe6f0f5d61c19e`, `f26a6a8bd745c1a2`).
2. **What it did:** it kept a paragraph only if it had at least 2 words of a 34-word English list, or was shorter than 80 characters. If no paragraph was kept, the document stayed as it was. Its author gave no word list, so this sheet used `D3_EN` of `DA-D3-002`. Source: jssunil's `medicine.md`, medicine 7 (`filter_bilingual_paragraphs`), PR #35.
3. **Harm test** (team `harm_test.py` at `f96453c`, 29 Oct): gold 40: 28 changed, 0 dropped, 70.00% (28/40) **FAIL**; gold 26: 69.23% (18/26) FAIL. Labelled D1 documents fixed: 2/3. Whole pack: 390 of 500 changed.
4. **Why withdrawn:**
   - It deletes normal PDF content. Of the paragraphs it removes from the 28 gold documents:
     - 117 are English with few list words: headings, captions, citations and formulas;
     - 68 are lists, tables or references;
     - 6 have more digits than letters;
     - only 2 are in another language.
   - A narrower version is not worth keeping. Removing only paragraphs with 5 or more foreign function words (German, French, Spanish, Italian, Portuguese, Dutch) passes (0/40), but it fixes only 1 of the 3 labelled documents. That text is mixed language (D3), which `DA-D3-002` covers.
   - D1 is labelled in only 3 Science documents, and R8 asks for a medicine only for a disease found more than 5 times.
   - A wrong language label is a document-level fault. Deleting paragraphs does not fix the label.
5. **Code:** removed from this sheet; the original is in the source above.

## 15. `DA-F1-004` · F1 personal data (phone numbers) · fix · aneeshads

1. **Disease:** F1 personal data (phone numbers). Labelled documents with F1 (fix or drop, 3 sheets): 77. Labelled documents this rule acts on: `031d526e862d6f22`, `053c80cc1a9b16bc`, `0798582b775b470f`.
2. **Medicine:** Mask a phone or fax number (7 to 15 digits in groups) as `<PHONE>` when a phone word (tel, phone, fax, cell, mobile, call, ...) comes at most 25 characters before it. A list after one phone word (numbers joined by `,` `/` `;` `or` `and`) is masked in one run: `Phone: <PHONE>, <PHONE>, <PHONE>`. A number that follows other words (`Fax: <PHONE>. Funded 2019-2020`) is kept. Its own `<PHONE>` is never a phone word and the gap never runs across it, so a second run changes nothing (RULES §2). (List matching and these two guards were added to the author's pattern; the phone words, gap and `f1_is_phone` are the author's.) Source: aneeshads's `medicine.md`, medicine 2 (`cure_f1`).

```python
RULE_ID = "DA-F1-004"
CODE = "F1"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "aneeshads"  # aneeshads's medicine.md, medicine 2

import re

F1_NUM = r"\+?\(?\d[\d().\s-]{5,22}\d"
F1_PHONE = re.compile(
    r"(?P<key>(?<!<)\b(?:tel|t[ée]l[ée]phone|telephone|phone|ph|fax|cell|mobile|call)\b[^\d\n<]{0,25}?\n?)"
    rf"(?P<nums>{F1_NUM}(?:\s*(?:[,/;]|\bor\b|\band\b)\s*{F1_NUM})*)", re.I)
# (?<!<): our own <PHONE> is not a phone word; no "<" in the gap: never across a <PHONE>. Both keep a second run a no-op.
# nums: one number, then more numbers joined by , / ; or and (a list after one phone word).
F1_ONE = re.compile(F1_NUM)

def f1_is_phone(num):
    digits = re.sub(r"\D", "", num)
    return (7 <= len(digits) <= 15
            and re.search(r"[\s.()-]", num)               # written in groups
            and not re.search(r"\d\.\d{2}$", num))

def cure_f1(text):
    def mask(m):
        nums = F1_ONE.sub(lambda n: "<PHONE>" if f1_is_phone(n.group(0)) else n.group(0), m.group("nums"))
        return m.group("key") + nums
    return F1_PHONE.sub(mask, text)


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(cure_f1(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-F1-004`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 47/77. Whole pack: 81 changed, 0 dropped.
5. **Side effects:** Office and helpline numbers are masked too; a number with no phone word near it is not.

**Decision (guideline 2):** KEEP: passes and fixes the most labelled F1 rows (47 of 77).

## 16. `DA-F1-005` · F1 personal data (phone numbers) · fix · jssunil

1. **Disease:** F1 personal data (phone numbers). Labelled documents with F1 (fix or drop, 3 sheets): 77. Labelled documents this rule acts on: `1b7c465205cdf42f`, `24d318c42b937b21`, `2b0f374583268f3c`.
2. **Medicine:** Mask a 10-digit number written as `(123) 456-7890` style as `<PHONE>` when a contact word (Cell, Mobile, Phone, Tel, Fax, Office, ...) comes right before it. Source: jssunil's `medicine.md`, medicine 2 (`redact_phone_numbers`).

```python
RULE_ID = "DA-F1-005"
CODE = "F1"
ACTION = "fix"
LANGS = {"eng_Latn"}
ORIGIN = "sci-finepdfs"  # pack whose medicine this came from
AUTHOR = "jssunil"  # jssunil's medicine.md, medicine 2

import re

PHONE_REDACT_RE = re.compile(
    r'((?:Cell|Mobile|Daytime|Direct|Office|Business|Contact|Telephone|Phone|Tel|Fax)[:\s]+)'
    r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    re.IGNORECASE
)

def redact_phone_numbers(text: str) -> str:
    return PHONE_REDACT_RE.sub(r'\1<PHONE>', text)


def _std(out, text):
    # source result in the shared form: str -> fix/keep, ("drop", _) -> drop
    if isinstance(out, tuple):
        if out[0] == "drop": return ("drop", text)
        out = out[1]
    return ("fix" if out != text else "keep", out)


def medicine(doc):
    if doc.get("lang_label") not in LANGS:
        return ("keep", doc["text"])
    text = doc["text"]
    return _std(redact_phone_numbers(text), text)
```

3. **Action:** fix.
4. **Harm test** (`harm_test.py --rules medicine_sci.md --rule DA-F1-005`): gold 26: 0 changed, 0 dropped, 0.00% (0/26) PASS; gold 40: 0 changed, 0 dropped, 0.00% (0/40) PASS. Labelled rows it fixes: 33/77. Whole pack: 52 changed, 0 dropped.
5. **Side effects:** Only US-style 10-digit numbers after a contact word.

**Decision (guideline 2):** DROP: passes, but all 33 rows it fixes are also fixed by `DA-F1-004`.

## Not covered

Codes labelled in the Science sheets with no rule here: A3 (1 document), B3 (1 document). D3 below 50% foreign text is kept on purpose (a foreign name in an English PDF is normal).

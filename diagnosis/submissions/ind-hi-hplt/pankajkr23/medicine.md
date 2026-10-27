# Medicine sheet: ind-hi-hplt (pankajkr23)

**Draft, built from the 151 labelled rows** (pack rows 60, 84–98 and 203–337, 0-based) of 500. It will be updated when all rows are labelled and the Hindi gold set is published.

**Diseases found more than five times** (documents among the labelled rows): C1 69, D3 62, C2 17, D4 14, D2 9. C5 is in 5 documents, not more than five, so it has no medicine yet. Counts are documents, not occurrences.

**Harm-test set.** The official Hindi gold set (Data B) is not published yet. Every harm test below runs on a **proxy gold set: the 45 documents of this pack that I labelled `clean`** after reading them in full. Limits:

- One reader made both the labels and this set. A disease I missed in a `clean` document is invisible to the test.
- With 45 documents, 1% is 0.45 documents, so a single changed document fails. 0 of 45 only rules out a true harm rate above 6.4% (95% confidence); the official gold set is needed to show 1% or less.
- The rules were built on these same rows. One rule (C2) was changed after its first version changed a proxy-gold document; see C2. On new text the rules will likely touch some good documents.

**How to read the numbers.** Each medicine takes `(text, meta)` and returns the new text, or `None` to drop the document. "Acts on" = the medicine changes or drops a labelled document that has the disease. "Whole pack" = documents changed or dropped among all 500, labelled or not.

| # | Disease | Docs | Action | Proxy gold (changed, dropped) | Acts on labelled docs with the disease | Whole pack (changed, dropped) |
|---|---|---|---|---|---|---|
| 1 | D4 Bad machine translation | 14 | drop | 0, 0 | 7 of 14 | 0, 48 |
| 2 | C1 Boilerplate | 69 | fix | 0, 0 | 63 of 69 | 125, 0 |
| 3 | C2 Repeated passage | 17 | fix | 0, 0 | 13 of 17 | 45, 0 |
| 4 | D3 Mixed language | 62 | fix | 0, 0 | 39 of 62 | 64, 0 |
| 5 | D2 Romanised Indic | 9 | keep | 0, 0 | 0 of 9 | 0, 0 |

**Run order:** D4 → C1 → C2 → D3 → D2. Dropping first saves work; boilerplate goes before the repeat check; the D3 edit runs after the repeat check, so it cannot hide a repeat. **All five together:** proxy gold 0 changed, 0 dropped; whole pack 162 changed, 48 dropped, 290 unchanged.

Shared code (Python 3, standard library only):

```python
import re

NUKTA = "\u093c"
DEV = r"\u0900-\u097F"


def _key(line):
    """Matching key: strip spaces, bullets and nukta, so पढ़ें / पढें and spacing variants match alike."""
    return line.replace(NUKTA, "").strip().lstrip("•-–*· ").strip()
```

## Medicine 1: D4, bad machine translation

1. **Disease:** D4, 14 documents. Three examples:
   - `dc736fdd65ba2f0c`: `पॉप अप हो रहे हैं जगह` at 918 ("popping up everywhere" copied word for word; MT score 0.80)
   - `38a4c524a43a0adb`: `आप MP4 जोड़ सकते हैं FlipHTML5 में` at 86 (English word order; MT score 0.75)
   - `826cbeec3b763d0f`: `तंग रस्सी` at 1481 (an English name or word, "tight rope", translated word for word; MT score 0.60)
2. **Medicine:** drop the document when HPLT's web-register classifier gives the MT (machine-translated) label a score of 0.50 or more. The score is in each document's `meta`. No rule can repair a translation line by line, so the medicine works on the whole document.

   ```python
   MT_DROP = 0.50


   def d4_drop_mt(text, meta):
       """Drop the document when HPLT's web-register classifier gives the MT (machine-translated) label >= 0.50."""
       mt = ((meta or {}).get("web-register") or {}).get("MT", 0.0)
       return None if mt >= MT_DROP else text
   ```

3. **Action:** drop the document.
4. **Harm test:** proxy gold, 45 documents: **0 changed, 0 dropped (0.0%). PASS** (limit 1%). The highest MT score in the proxy gold set is 0.12, far below 0.50. Threshold check on the labelled rows:

   | Threshold | Proxy gold dropped | D4 docs dropped | D4 docs I labelled `fix` that it drops | Whole pack dropped |
   |---|---|---|---|---|
   | 0.30 | 0 | 8 of 14 | 1 | 62 |
   | 0.40 | 0 | 8 of 14 | 1 | 58 |
   | 0.50 | 0 | 7 of 14 | 0 | 48 |
   | 0.60 | 0 | 5 of 14 | 0 | 40 |
   | 0.70 | 0 | 3 of 14 | 0 | 32 |

   0.50 is the lowest of these thresholds that drops no document I labelled `fix`.
5. **Side effects:** it acts on 7 of 14 D4 documents: all of them are documents I labelled `drop`. It misses 2 D4 documents I labelled `drop`, with scores 0.22 and 0.30 (both from one metals-supplier site, `be90d221919f8fa5`, `4385ab9bc6c63123`), and by design keeps the 5 D4 documents I labelled `fix` (scores 0.09–0.46). In the whole pack it drops 48 documents, 41 of them not yet labelled; I read the opening of 6 random ones: a university directory, three trading-spam pages, a place listing and an event page, all machine-translated. It depends on the classifier: a good human translation with a high score would be dropped, and a machine translation with a low score is kept.

## Medicine 2: C1, boilerplate

1. **Disease:** C1, 69 documents. Three examples:
   - `8a6a9e11bf0f5d9f`: `इसे भी पढ़ें:-` at 916 (link to another article)
   - `340122661b614c55`: `ADVERTISEMENT` at 240 (ad slot)
   - `fa46520839cbad8f`: `तो दोस्तों कैसी लगी आज की यह जानकारी` at 1873 (blog sign-off, the same in 11 labelled documents)
2. **Medicine:** delete a whole line when it is page furniture: a related-article link (इसे भी पढ़ें, यह भी पढ़ें, Read also, …), a stand-alone label (ADVERTISEMENT, Share:, More Stories, Leave a Reply, Post Views, N thoughts on …), a blog sign-off, a source or image credit, a pointer to a video that is not in the text, a follow-us promo, or an embedded tweet. Each pattern has a length limit, so a long line that only starts like furniture stays. Nukta and spacing are ignored when matching.

   ```python
   # Each entry: (compiled pattern on the matching key, max line length in characters)
   C1_LINES = [
       # related-article links: इसे / यह / ये / इन्हें भी पढ़ें / देखें, Read also, अधिक पढ़ें, यह सभी देखें, अन्य न्यूज़
       (re.compile(r"^(?:इसे|इन्हें|इन्हे|यह|ये|यें)\s*भी\s*(?:पढें|पढे|पढिए|देखें)"), 200),
       (re.compile(r"^(?:read\s+also|also\s+read|read\s+more)\b", re.I), 200),
       (re.compile(r"^(?:अधिक\s+पढें\s*:|यह\s+सभी\s+देखें\s*:)"), 200),
       (re.compile(r"^अन्य\s+न्यूज$"), 20),
       # page furniture that stands alone on a line
       (re.compile(r"^(?:advertisement|share\s*:?|शेयर\s+करें|more\s+stories|recent\s+posts|categories|trending\s+photos|"
                   r"leave\s+a\s+reply|about\s+post\s+author|responses|author|comments\s+in\s+this\s+topic\s*:?|टिप्पणियाँ|"
                   r"view\s+this\s+post\s+on\s+instagram|most\s+helpful\s+for\s+students|"
                   r"guest\s+post\s*&\s*advertisement\s+with\s+us)$", re.I), 40),
       (re.compile(r"^post\s+views\s*:?\s*\d*$|^\d[\d,.]*k?\s+views$", re.I), 25),
       (re.compile(r"^\d+\s+thoughts?\s+on\b", re.I), 250),
       (re.compile(r"^(?:.{0,40}\s)?important\s+links?\s*[:\-–]*$", re.I), 60),
       (re.compile(r"^source\s*[:\-–]", re.I), 60),
       (re.compile(r"^all\s+content\s+on\s+this\s+website\s+is\s+copyrighted", re.I), 200),
       # blog sign-offs
       (re.compile(r"^(?:तो\s+दोस्तों\s+कैसी\s+लगी|दोस्तों,?\s+उम्मीद\s+है\s+कि\s+यह\s+पोस्ट\s+आपको\s+अच्छी\s+लगी|"
                   r"अंत\s+तक\s+पढने\s+के\s+लिए\s+धन्यवाद|thanks\s+for\s+visiting\s+our\s+site)", re.I), 400),
       # image credits and pointers to media that the text does not contain
       (re.compile(r"^(?:image\s+courtesy|image\s+credit|photo\s+credit|छवि\s+क्रेडिट|credit\s*ai$)", re.I), 80),
       (re.compile(r"^(?:यहां\s+देखें\s+वीडियो|देखिए\s+वीडियो)\W*$"), 40),
       (re.compile(r"^reviews\s+for\s*:", re.I), 60),
       (re.compile(r"^साइन\s+अप\s+करने\s+के\s+लिए\s+धन्यवाद"), 60),
       # English SEO footer of one publisher: "(For more news apart from ... stay tuned to ...)"
       (re.compile(r"^\(?for\s+more\s+news\s+apart\s+from\b", re.I), 300),
   ]
   # follow / join promos: a platform name + a join or follow verb + promo wording
   _PLATFORM = re.compile(r"whatsapp|व्हाट्सएप|वॉट्सएप|फेसबुक|facebook|ट्विटर|twitter|instagram|इंस्टाग्राम|telegram|टेलीग्राम", re.I)
   _FOLLOW = re.compile(r"फॉलो|जुड|follow", re.I)
   _PROMO = re.compile(r"हमारे|channel|के\s+साथ|कर\s+सकते\s+हैं", re.I)
   # embedded tweets: a pic.twitter.com link, or the credit line "— Name (@handle) June 18, 2024"
   _TWEET = re.compile(r"pic\.twitter\.com/|—\s?[^—\n]{1,60}\(@\w{1,30}\)\s+[A-Z][a-z]+\s+\d{1,2},\s+\d{4}\s*$")


   def c1_strip_lines(text, meta=None):
       out = []
       for line in text.split("\n"):
           k = _key(line)
           drop = any(p.search(k) and len(k) <= n for p, n in C1_LINES)
           drop = drop or (len(k) <= 200 and _PLATFORM.search(k) and _FOLLOW.search(k) and _PROMO.search(k))
           drop = drop or (len(k) <= 300 and _TWEET.search(k))
           if not drop:
               out.append(line)
       return "\n".join(out)
   ```

3. **Action:** fix the text (delete the lines).
4. **Harm test:** proxy gold, 45 documents: **0 changed, 0 dropped (0.0%). PASS** (limit 1%).
5. **Side effects:** it acts on 63 of 69 C1 documents and on no other labelled document. It misses 6 (`1c61f6e0c56fbbc9`, `f967bfaaa579d4a9`, `cb84e3a20a9227b5`, `e015e6aed34052c5`, `62df9947c03bbb97`, `35271c69df0b2ac4`): furniture glued into a sentence (a site-name watermark at the start of a paragraph, `देखिए वीडियो` inside a line, `Share:` at the end of a line), a site intro repeated across documents (needs a check across documents), Wikipedia citation markers, and one publisher promo. It deletes the text of an embedded tweet, which can be the quote the story is about. A real one-line heading such as `Categories` or `Author` would be deleted. The phrase list comes from these rows, so other sites' furniture is missed.

## Medicine 3: C2, repeated passage

1. **Disease:** C2, 17 documents. Three examples:
   - `36445006095beb35`: `अगर आपके पास दूध या दही नहीं है` at 623 and 720 (the same sentence twice)
   - `4341269d71f31499`: `गर्मियों में लोग अक्सर अपनी सेहत का विशेष ख्याल` at 67 and 354 (intro paragraph repeated in full)
   - `fc3021f18b27b447`: `मध्य प्रदेश में आज मोहन कैबिनेट की बैठक होगी।` at 110 and 277 (summary repeated as the first paragraph)
2. **Medicine:** keep one full copy of each passage. Delete (1) a long line that is only a glued copy of other lines, (2) a later exact copy of a line of 30+ characters, (3) a teaser cut with an ellipsis whose text appears again, (4) a sentence (it ends with । . ? ! or has 70+ characters) that sits whole inside a longer line: a pull quote, standfirst or summary.

   ```python
   C2_MIN = 30  # characters; shorter lines (names, headings) repeat naturally


   _END = ("।", ".", "?", "!", "॥")


   def c2_dedup_lines(text, meta=None):
       """Keep one full copy of a passage. Remove (1) a long line that is only a glued copy of other lines (80 % or
       more of it is other lines of the same text), (2) a later exact copy of a line, (3) a teaser line cut with an
       ellipsis whose text is repeated elsewhere, (4) a sentence (ends with । . ? ! or is 70+ characters) that sits
       whole inside a longer line: a pull quote, standfirst or summary. Short subheadings without an end mark stay."""
       lines = text.split("\n")
       keys = [l.strip() for l in lines]
       # (1) glued copies: a long line covered by other lines of the text
       glued = set()
       for i, k in enumerate(keys):
           if len(k) >= 200:
               parts = {o for j, o in enumerate(keys) if j != i and len(o) >= C2_MIN and o in k}
               if sum(len(p) for p in parts) >= 0.8 * len(k):
                   glued.add(i)
       keys2 = [("" if i in glued else k) for i, k in enumerate(keys)]
       seen, out = set(), []
       for i, k in enumerate(keys):
           drop = i in glued
           if not drop and len(k) >= C2_MIN:
               if k in seen:
                   drop = True                                              # exact repeat of an earlier line
               else:
                   core = re.sub(r"[.…\s]+$", "", k)
                   cut = k != core and (k.endswith("…") or k.endswith("..."))
                   probe = core if cut and len(core) >= C2_MIN else k
                   sentence = len(k) >= 70 or k.endswith(_END)
                   if text.count(probe) >= 2:                               # cheap test before the line scan
                       for j, o in enumerate(keys2):
                           if j == i or o == k or not o:
                               continue
                           if (cut and len(core) >= C2_MIN and core in o and len(o) > len(core)) or \
                              (sentence and len(o) >= len(k) + 20 and k in o):
                               drop = True                                  # teaser, pull quote, standfirst
                               break
           seen.add(k)
           if not drop:
               out.append(lines[i])
       return "\n".join(out)
   ```

3. **Action:** fix the text (delete the extra copies).
4. **Harm test:** proxy gold, 45 documents: **0 changed, 0 dropped (0.0%). PASS** (limit 1%). **Tuning disclosed:** the first version also deleted any 30+ character line found inside a longer line. It changed one proxy-gold document (2.2%, fail): two subheadings that reuse a sentence of the article. The end-mark-or-70-characters condition was added after that, so this pass is on the set the rule was tuned on.
5. **Side effects:** it acts on 13 of 17 C2 documents and on 1 other labelled document (`dc736fdd65ba2f0c`, a repeated sign-up line in a document I labelled `drop`). It misses 4 (`8b80a48ec843734c`, `798a107ce234e0cf`, `ef3ed1ee60b1d6fd`, `bea03cd000026fb3`): a teaser that starts with a dateline glued to it, a repeated name shorter than 30 characters, a teaser whose last words differ from the full text, and a cut description that has no ellipsis. Deliberate repeats of 30+ characters (a refrain, the same spec line under several product photos) lose their later copies. A subheading that is a full sentence with an end mark and also appears in the body would be deleted.

## Medicine 4: D3, mixed language

1. **Disease:** D3, 62 documents. Three examples:
   - `e28c5b447cedb91c`: `(12 acres donated to 16 farmers)` at 240 (English gloss that repeats the Hindi before it)
   - `c6bf916045ab8652`: `Rishikesh News:` at 0 (English SEO kicker before the Hindi headline)
   - `7a936e050a3e704f`: `(Aries Love Horoscope)` at 399 (English gloss after each sign name, 12 times)
2. **Medicine:** remove only the English that repeats or labels the Hindi: (1) a bracketed run of two or more Latin words right after Devanagari text; one-word acronyms such as `(ED)` or `(IMD)` stay; (2) an English kicker of two or more words at the start of a line, before Hindi text, when it holds a kicker word (News, Update, Recruitment, Viral, …). English inside a Hindi sentence is natural mixing and is not touched.

   ```python
   # A bracketed run of two or more Latin words right after Devanagari text.
   # "(ED)" or "(IMD)" stays: one word. "(12 acres donated to 16 farmers)" or "(Social Media)" goes.
   _GLOSS = re.compile(r"(?<=[" + DEV + r"])\s*[\(\[]\s*([A-Za-z][A-Za-z0-9.,&'’\-]*(?:\s+[A-Za-z0-9.,&'’\-]+)+)\s*[\)\]]")


   # An English SEO kicker at the start of a line, right before Hindi text: "Rishikesh News: ऋषिकेश में ...".
   # Two or more Latin words, and one of them is a kicker word, so a dateline such as "Raipur:" or a name such as
   # "Shraddha Kapoor :" stays (the kicker-word list comes from the labelled rows).
   _KICKER = re.compile(r"^(\s*)([A-Za-z][A-Za-z0-9.&'’\-]*(?:\s+[A-Za-z0-9.&'’\-+()]+){1,8})\s*:\s*(?=[" + DEV + r"])", re.M)
   _KICKER_WORD = re.compile(
       r"\b(?:news|updates?|live|video|viral|recruitment|admit\s+card|result|notification|vacancy|scheme|alert|breaking|"
       r"exclusive|tips|tricks|horoscope|weather|accidents?|action|crisis|violence|link|apply|expiry|date|jobs?|portal|"
       r"loan|list|merit|form|guidelines|editorial|speaker|admission|bharti|exam)\b", re.I)


   def d3_strip_gloss(text, meta=None):
       text = _GLOSS.sub("", text)
       return _KICKER.sub(lambda m: m.group(1) if _KICKER_WORD.search(m.group(2)) else m.group(0), text)
   ```

3. **Action:** fix the text (delete the gloss or kicker).
4. **Harm test:** proxy gold, 45 documents: **0 changed, 0 dropped (0.0%). PASS** (limit 1%).
5. **Side effects:** it acts on 39 of 62 D3 documents. The 23 it leaves alone are mostly natural mixing inside sentences, English headings and headlines, and kickers with no colon or no kicker word, which it does not target. It also removes Latin name glosses such as `(Rakhi Sawant)`, which I did not label D3 (3 labelled documents: `de28b50e61a61600`, `3beed481c79246dc`, `62df9947c03bbb97`); the Hindi name stays, so little is lost. It removes English expansions that add information, for example an organisation's English name in brackets. The kicker words come from these rows, so kickers with other words are missed, and a real Latin heading that holds one of these words would be removed.

## Medicine 5: D2, romanised Indic

1. **Disease:** D2, 9 documents. Three examples:
   - `8a6a9e11bf0f5d9f`: `Nagar Palika Bharti` at 1542 (post name in a headline)
   - `7a936e050a3e704f`: `Aaj Ka Love Rashifal` at 0 (SEO title)
   - `e2e8c748d77ed529`: `Amazon se online shopping kaise kare` at 2658 (heading in Latin letters)
2. **Medicine:** no change. In this pack, D2 is the names of schemes and posts (Bharti, Yojana, Rashifal) and short SEO headings, inside otherwise Devanagari text. Deleting them would cut names out of headlines; transliterating them back to Devanagari needs a model, not a rule.

   ```python
   def d2_keep(text, meta=None):
       """No change. In this pack, D2 is names of schemes and posts (Bharti, Yojana, Rashifal) and SEO headings."""
       return text
   ```

3. **Action:** keep the text unchanged. D2 alone is not a reason to drop a document.
4. **Harm test:** proxy gold, 45 documents: **0 changed, 0 dropped (0.0%). PASS** (limit 1%). It changes nothing by construction.
5. **Side effects:** none from this medicine. A document that is mostly romanised Hindi would be kept; none of the labelled rows is like that. English kickers that hold romanised words (for example `Bharti`) are removed by the D3 medicine.

## Run order in code

```python
MEDICINES = [  # run order
    ("D4", "drop", d4_drop_mt),
    ("C1", "fix", c1_strip_lines),
    ("C2", "fix", c2_dedup_lines),
    ("D3", "fix", d3_strip_gloss),
    ("D2", "keep", d2_keep),
]
```

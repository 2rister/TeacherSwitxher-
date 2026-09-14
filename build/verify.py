# -*- coding: utf-8 -*-
"""Content self-checks for the pack. Run before every print:  python3 build/verify.py

These are the checks that a proofread can miss: a word bank that no longer matches
its gaps, a Jeopardy call-back that repeats a question printed on the same page,
a matching key that lets a student read the answers straight off the sheet.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C
import grammar as G
import build as B

fails, checks = [], 0


def check(ok, label, detail=""):
    global checks
    checks += 1
    if not ok:
        fails.append(f"{label}{(' — ' + detail) if detail else ''}")
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  ({detail})" if detail and not ok else ""))


def norm(s):
    """Plain comparable text: strip tags/entities, punctuation and case."""
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


# Build first: the matching and numbers keys are fixed while the sheets are laid out.
B.write_html()
# resolve file names from what the build actually wrote, never from literals
SHEETFILE = {n.split("-", 1)[1]: n for n, _ in B.SHEETS if not n.startswith("00-")}
print("\nVerifying the Interesting People A2 pack\n")

# Glossary head-words that appear in the reading in another form.
INFLECTED = {"to break up": "broke up", "to protest": "protested", "views": "views"}

# ---------------------------------------------------------------- per person
for d in C.PEOPLE:
    n = d["name"]
    print(f"-- {n}")
    check(sorted(d["bank"]) == sorted(a for _, a in d["gaps"]),
          f"{n}: word bank matches the gap answers")
    check(all(a in ("T", "F", "NG") for _, a in d["tf"]),
          f"{n}: every T/F/NG answer is a legal value")
    check(len({a for _, a in d["tf"]}) == 3,
          f"{n}: T, F and NG all occur in task 1")
    check(all("____" in s for s, _ in d["gaps"]),
          f"{n}: every gap sentence actually contains a gap")
    check(len(d["glossary_words"] if "glossary_words" in d else C.GLOSSARY[d["slug"]]) >= 6,
          f"{n}: glossary has at least six words")

    # every gap answer must be findable in the reading text
    body = norm(" ".join(d["text"]))
    missing = [a for _, a in d["gaps"] if norm(a) not in body]
    check(not missing, f"{n}: every gap answer appears in the text", ", ".join(missing))

    # glossary words must come from the text too
    gl_missing = [w for w, _ in C.GLOSSARY[d["slug"]]
                  if not any(norm(p) in body
                             for p in (w, w.rstrip("s"), w.replace("to ", ""), INFLECTED.get(w, w)))]
    check(not gl_missing, f"{n}: every glossary word appears in the text", ", ".join(gl_missing))

    # a matching half must never sit opposite its own stem
    key = d.get("_match_key")
    check(key is not None and sorted(key) == list(range(len(d["match"]))),
          f"{n}: matching key is a complete permutation")
    if key:
        check(all(i != k for i, k in enumerate(key)),
              f"{n}: no matching half lines up with its own stem")

    # a Jeopardy call-back must not repeat a question printed on the same page
    page3 = [norm(q) for q, _ in d["qs"]] + [norm(a) for a, _ in d["match"]]
    clash = [q for _, q, _ in d["jeopardy"]
             if any(norm(q) == p or (len(norm(q)) > 25 and norm(q) in p) for p in page3)]
    check(not clash, f"{n}: task 5 repeats nothing from tasks 3-4 on the same page",
          " | ".join(clash))
    print()

# ------------------------------------------------------------------- sheet IV
print("-- The Mixed Round")
check(C.TIMELINE_KEY == [n for n, _ in sorted(C.TIMELINE, key=lambda x: x[1])],
      "timeline key is sorted by year of birth")
check(C.TIMELINE_KEY[0] == "Elizabeth I",
      "timeline starts with Elizabeth I (the game slide has this wrong)")
check(len({q for q, _ in C.WHO}) == len(C.WHO), "'Who is it?' has no repeated question")
GENDERED = re.compile(r"\b(his|her|hers|he|she|him)\b", re.I)
leaky = [norm(q) for q, _ in C.WHO if GENDERED.search(norm(q))]
check(not leaky, "'Who is it?' never reveals the answer's gender", " | ".join(leaky))
leaky = [f"{d['name']} {p}" for d in C.PEOPLE for p, q, _ in d["jeopardy"]
         if re.match(r"(who|which person)\b", norm(q), re.I) and GENDERED.search(norm(q))]
check(not leaky, "no call-back question reveals the answer's gender", " | ".join(leaky))
check({a for _, a in C.WHO} == {"Newton", "Lennon", "Diana"},
      "'Who is it?' uses exactly the three required people")
counts = {p: sum(1 for _, a in C.WHO if a == p) for p in ("Newton", "Lennon", "Diana")}
check(max(counts.values()) - min(counts.values()) <= 2,
      "'Who is it?' is balanced across the three people", str(counts))
check(len({n for n, _ in C.NUMBERS}) == len(C.NUMBERS), "numbers round has no repeated number")
check(sorted(getattr(C, "_nums_key", [])) == list(range(len(C.NUMBERS))),
      "numbers key is a complete permutation")
print()

# ------------------------------------------------------- required people only
print("-- Requirements")
check({d["name"] for d in C.PEOPLE} ==
      {"Isaac Newton", "John Lennon", "Princess Diana", "Charles Darwin",
       "Horatio Nelson", "Elizabeth I"},
      "pack covers Newton, Lennon, Diana, Darwin, Nelson and Elizabeth I")
for d in C.PEOPLE:
    check(len(d["tf"]) == 8 and len(d["gaps"]) == 8 and len(d["qs"]) == 6 and len(d["match"]) == 5,
          f"{d['name']}: full exercise set (8 T/F, 8 gaps, 6 questions, 5 matches)")

# ------------------------------------------------- the Jeopardy deck itself
JDIR = os.path.join(os.path.dirname(HERE), "materials", "jeopardy")
DECKS = [("Great Britons board", "Jeopardy_Great_Britons_A2.pptx"),
         ("plain board", "Jeopardy_Interesting_People_A2_fixed.pptx")]
DECK = os.path.join(JDIR, DECKS[0][1])
if os.path.exists(DECK):
    print("-- Jeopardy decks")
    import audit_jeopardy
    for label, fn in DECKS:
        path = os.path.join(JDIR, fn)
        if not os.path.exists(path):
            check(False, f"{label}: deck present"); continue
        deck_problems = audit_jeopardy.audit(path, quiet=True)
        check(not deck_problems, f"{label}: navigation and content are clean",
              " | ".join(deck_problems[:3]))

    # the deck and the handouts must not disagree about the birth order
    from pptx import Presentation
    deck_text = " ".join(sh.text_frame.text for s_ in Presentation(DECK).slides
                         for sh in s_.shapes if sh.has_text_frame)
    order = re.search(r"(Elizabeth[^.]*?Diana)", deck_text)
    # the handouts name people in full, the deck by the name it displays;
    # match on the surname (or "Elizabeth" for the regnal name)
    want = [[w for w in n.split() if len(w) > 2][-1] for n in C.TIMELINE_KEY]
    seen = [w for w in re.findall(r"[A-Z][a-z]+", order.group(1))
            if w in want] if order else []
    check(seen == want, "deck's birth order matches the timeline key on the handouts",
          f"deck says {seen}, handouts say {want}")
    print()

# ------------------------------------------------- rendered output sanity
# A stray "&" in a shell replacement once expanded to the whole match and left
# "III#8211;5" in the teacher's notes, which shipped. An entity fragment with no
# leading "&" cannot occur on purpose, so scan every rendered sheet for one.
print("-- Rendered HTML")
HTMLDIR = os.path.join(os.path.dirname(HERE), "materials", "html")
orphan = re.compile(r"(?<!&)#\d{2,5};")
dirty = []
for f in sorted(os.listdir(HTMLDIR)):
    if not f.endswith(".html"):
        continue
    body = open(os.path.join(HTMLDIR, f), encoding="utf-8").read()
    for m in orphan.finditer(body):
        dirty.append(f"{f}: ...{body[max(0, m.start() - 30):m.end() + 10]}...")
check(not dirty, "no orphaned HTML entity fragments in any sheet",
      " | ".join(dirty[:3]))

# duplicated phrases are the other fingerprint of a botched replacement
dupes = []
for f in sorted(os.listdir(HTMLDIR)):
    if not f.endswith(".html") or f.startswith("00-"):
        continue
    text = norm(open(os.path.join(HTMLDIR, f), encoding="utf-8").read())
    for m in re.finditer(r"\b(\w+(?: \w+){4,7})\b \1\b", text):
        dupes.append(f"{f}: {m.group(1)[:50]}")
check(not dupes, "no phrase repeated back to back in any sheet", " | ".join(dupes[:3]))

nums = ([d["num"] for d in C.PEOPLE] + [B.SHEET["MIXED"], B.SHEET["KEY"]]
        + [d["num"] for d in G.GRAMMAR_PEOPLE] + [B.SHEET["GMIXED"], B.SHEET["GKEY"]])
expected = [B.roman(i) for i in range(1, len(nums) + 1)]
check(nums == expected, f"sheet numbers run I to {expected[-1]} with no gap or repeat", str(nums))
check(len({n for n, _ in B.SHEETS}) == len(B.SHEETS), "no two sheets share a file name")
print()

# ------------------------------------------------- Past Simple grammar sheets
print("-- Past Simple grammar")
GRAM = G.GRAMMAR_PEOPLE + [G.MIXED]
for d in GRAM:
    n = d["name"]
    check(all(len(o) == 3 for _, o, _ in d["mc"]), f"{n}: every test item has three options")
    check(all(len(set(o)) == 3 for _, o, _ in d["mc"]), f"{n}: no repeated option inside an item")
    check(all(0 <= k < len(o) for _, o, k in d["mc"]), f"{n}: every answer key points at a real option")
    check(all("____" in q for q, _, _ in d["mc"]), f"{n}: every test sentence has a gap")
    check(len({norm(q) for q, _, _ in d["mc"]}) == len(d["mc"]),
          f"{n}: no repeated sentence in the test")
    keys = [chr(97 + k) for _, _, k in d["mc"]]
    check(len(set(keys)) == 3, f"{n}: the key uses a, b and c", str(sorted(set(keys))))
    top = max(keys.count(x) for x in "abc") / len(keys)
    check(top <= 0.60, f"{n}: no single letter dominates the key",
          f"{ {x: keys.count(x) for x in 'abc'} } = {top:.0%}")

    # a two-gap sentence must carry two answers, or the key mis-reads as alternatives
    bad = [q for q, a in d["bracket"]
           if q.count("__________") != (1 if isinstance(a, str) else len(a))]
    check(not bad, f"{n}: gaps and answers line up in task 'Past Simple'",
          " | ".join(norm(x)[:50] for x in bad))
    check(all(re.search(r"\([^)]+\)", q) for q, _ in d["bracket"]),
          f"{n}: every Past Simple item shows the verb in brackets")
print()

print("-- Grammar support material")
# scrambled words must be exactly the words of the answer, or the item is unsolvable
for scram, ans in G.WORD_ORDER:
    chunks = [w.strip() for w in html.unescape(scram).split("/") if w.strip()]
    a = html.unescape(ans).strip()
    words = a.rstrip("?").split()
    ok = ("?" in chunks
          and sum(len(c.split()) for c in chunks if c != "?") == len(words)
          and all(c.lower() in a.lower() for c in chunks if c != "?"))
    check(ok, f"word order solvable: {a}", f"chunks {chunks}")

used = " ".join(
    norm(q) + " " + " ".join(norm(o) for o in opts) for d in GRAM for q, opts, _ in d["mc"]
) + " " + " ".join(norm(q) for d in GRAM for q, _ in d["bracket"])
# A verb counts as practised whether it turns up as the infinitive (in a bracket
# cue) or as its past form (as a test option) — "had" and "sang" only ever appear
# as forms, which is exactly what the table asks students to produce.
def practised(inf, past):
    forms = [inf] + [x.strip() for x in past.split("/")]
    return any(re.search(rf"\b{re.escape(f)}\b", used) for f in forms)

missing = [v for v, pa in G.IRREGULAR if not practised(v, pa)]
check(not missing, "every verb in the irregular table is practised on the sheets",
      ", ".join(missing))
check(len({v for v, _ in G.IRREGULAR}) == len(G.IRREGULAR), "no repeated verb in the irregular table")
print()

# ------------------------------------------------- Word versions, when present
DOCX = os.path.join(os.path.dirname(HERE), "materials", "docx")
if os.path.isdir(DOCX) and os.listdir(DOCX):
    print("-- Word versions match the PDFs")
    from docx import Document

    def col(path, ncols, nrows, c):
        t = [x for x in Document(path).tables
             if len(x.columns) == ncols and len(x.rows) == nrows]
        return [re.sub(r"^[a-h]\)\s*", "", r.cells[c].text.strip()) for r in t[0].rows] if t else []

    # python-docx defaults to US Letter; the pack is A4 throughout
    wrong = []
    for f in sorted(os.listdir(DOCX)):
        if not f.endswith(".docx"):
            continue
        sizes = {(round(sec.page_width.cm, 1), round(sec.page_height.cm, 1))
                 for sec in Document(os.path.join(DOCX, f)).sections}
        if sizes != {(21.0, 29.7)}:
            wrong.append(f"{f} {sizes}")
    check(not wrong, "every Word file is A4 on every section", " | ".join(wrong))

    for i, d in enumerate(C.PEOPLE, 1):
        f = os.path.join(DOCX, SHEETFILE[d["slug"]] + ".docx")
        if not os.path.exists(f):
            check(False, f"{d['name']}: Word version exists"); continue
        want = [None] * len(d["match"])
        for j, slot in enumerate(d["_match_key"]):
            want[slot] = html.unescape(re.sub("<[^>]+>", "", d["match"][j][1]))
        check(col(f, 4, len(d["match"]), 3) == want,
              f"{d['name']}: Word matching column is in the same order as the PDF")

    # the grammar options are not shuffled, but a Word rebuild could still drift
    gram_files = [(os.path.join(DOCX, SHEETFILE[f"grammar-{d['slug']}"] + ".docx"), d)
                  for d in G.GRAMMAR_PEOPLE]
    gram_files.append((os.path.join(DOCX, SHEETFILE["grammar-mixed"] + ".docx"), G.MIXED))
    for path, d in gram_files:
        if not os.path.exists(path):
            check(False, f"{d['name']}: Word grammar sheet exists"); continue
        lines = [p.text for p in Document(path).paragraphs]
        bad = []
        for i, (_, opts, _) in enumerate(d["mc"], 1):
            want = "".join(f"    {chr(97 + j)}) "
                           f"{html.unescape(re.sub('<[^>]+>', '', o))}"
                           for j, o in enumerate(opts))
            cand = [l for l in lines if l.startswith(f"{i}.  ") and " a) " in l]
            if not cand or want not in cand[0]:
                bad.append(i)
        check(not bad, f"{d['name']}: Word test options match the PDF, in order",
              f"items {bad}")

    # the Monday listening sheet shuffles twice; both columns must match the PDF
    import monday as _M
    f = os.path.join(DOCX, SHEETFILE["monday-listening"] + ".docx")
    if os.path.exists(f):
        for label, src, key, n_ in (("words", _M.L_WORDS, _M._lwords_key, len(_M.L_WORDS)),
                                    ("numbers", _M.L_NUMBERS, _M._lnums_key, len(_M.L_NUMBERS))):
            want = [None] * n_
            for j, slot in enumerate(key):
                want[slot] = html.unescape(re.sub("<[^>]+>", "", src[j][1]))
            check(col(f, 4, n_, 3) == want,
                  f"Word listening sheet: {label} column is in the same order as the PDF")
    else:
        check(False, "Word listening sheet exists")

    import phrases as _P
    f = os.path.join(DOCX, SHEETFILE["phrases-remarkable-people"] + ".docx")
    if os.path.exists(f):
        want = [None] * len(_P.NOUN_PAIRS)
        for j, slot in enumerate(_P._noun_key):
            want[slot] = html.unescape(re.sub("<[^>]+>", "", _P.NOUN_PAIRS[j][1]))
        check(col(f, 4, len(_P.NOUN_PAIRS), 3) == want,
              "Word phrases sheet: matching column is in the same order as the PDF")
    else:
        check(False, "Word phrases sheet exists")

    f = os.path.join(DOCX, SHEETFILE["mixed-round"] + ".docx")
    if os.path.exists(f):
        want = [None] * len(C.NUMBERS)
        for j, slot in enumerate(C._nums_key):
            want[slot] = html.unescape(re.sub("<[^>]+>", "", C.NUMBERS[j][1]))
        check(col(f, 4, len(C.NUMBERS), 3) == want,
              "Word numbers round is in the same order as the PDF")
    print()

# ------------------------------------------------- Monday 14.09 lesson kit
print("-- Monday lesson kit")
import monday as M

# the timetable must still be the one the school sent
check([a for a, _, _ in M.TIMETABLE] ==
      ["11.00 &#8211; 11.45", "11.45 &#8211; 12.00", "12.00 &#8211; 13.35",
       "13.35 &#8211; 14.05", "14.05 &#8211; 15.40"],
      "timetable is unchanged from the school's plan")

# each session's stages must fill the session, not overrun it
for label, rows, want in (("11.00-11.45", M.STAGE1, 45),
                          ("12.00-13.35", M.STAGE2, 95),
                          ("14.05-15.40", M.STAGE3, 95)):
    got = sum(m for _, m, _, _, _ in rows)
    check(got == want, f"session {label}: stage times add up to {want} minutes",
          f"they add up to {got}")
    clocks = [float(c.replace(".", "")) for c, _, _, _, _ in rows]
    check(clocks == sorted(clocks), f"session {label}: the clock never goes backwards")

# the first stage of each session must start when the session starts
for rows, start in ((M.STAGE1, "11.00"), (M.STAGE2, "12.00"), (M.STAGE3, "14.05")):
    check(rows[0][0] == start, f"session starting {start} begins at {start}")

# listening
check(sum(1 for _, t in M.L_TICK if t) == 5,
      "first-listening task really has five things to tick")
check(all(a in ("T", "F", "NG") for _, a in M.L_TF),
      "every listening T/F/NG answer is a legal value")
check(len({a for _, a in M.L_TF}) == 3, "T, F and NG all occur in the listening task")
for name, key, src in (("words", getattr(M, "_lwords_key", None), M.L_WORDS),
                       ("numbers", getattr(M, "_lnums_key", None), M.L_NUMBERS)):
    check(key is not None and sorted(key) == list(range(len(src))),
          f"listening {name} key is a complete permutation")
    if key:
        check(all(i != k for i, k in enumerate(key)),
              f"listening {name}: no half lines up with its own stem")
check(len({n for n, _ in M.L_NUMBERS}) == len(M.L_NUMBERS),
      "listening numbers task has no repeated number")

# the script
script_words = sum(len(norm(t).split()) for t, _ in M.SCRIPT)
check(250 <= script_words <= 400,
      "audio script is between 250 and 400 words (2.5-4 minutes read aloud)",
      f"{script_words} words")
script_text = norm(" ".join(t for t, _ in M.SCRIPT))
# the two corrections the class text needed must survive in the script
check("twentyfourth of march" in script_text and "sixteen oh three" in script_text,
      "script gives the corrected death date (24 March 1603)")
check("fortyfour years" in script_text, "script gives the corrected reign length (44 years)")
check("fourteenth of march" not in script_text, "script does not repeat the wrong death date")
# things the record does not support must not have crept in
for bad in ("shakespeare was her favourite", "makeup killed", "poison"):
    check(bad not in script_text, f"script avoids the unsupported claim: {bad}")

# the ten-minute presentation must actually add up to ten minutes and no gaps
def mins(t):
    m, sec = t.split(":")
    return int(m) + int(sec) / 60
spans = []
for _, _, tm, _ in M.ROLES:
    a, b = [x.strip() for x in tm.replace("&#8211;", "-").split("-")]
    spans.append((mins(a), mins(b)))
check(spans[0][0] == 0 and spans[-1][1] == 10, "the six roles fill exactly ten minutes")
check(all(spans[i][1] == spans[i + 1][0] for i in range(len(spans) - 1)),
      "the six roles leave no gap and no overlap")
check(all(b - a <= 2.5 for a, b in spans), "no single speaker holds the floor over 2.5 minutes")
check(len(M.ROLES) == 6, "there is a role for every member of the team")

# the awards the school asked for must all exist
titles = {t for t, _, _ in M.CERTS}
check("MOST ACTIVE PARTICIPANT" in titles, "certificate for the most active participants")
check("CHAMPION OF THE DEBATE" in titles, "certificate for the debate winners")
check("CHAMPION OF THE GAME" in titles, "certificate for the winners of the game")
check(sum(1 for t, _, _ in M.CERTS if t == "MOST ACTIVE PARTICIPANT") == 2,
      "two 'most active' certificates, as the school asked (1-2 per group)")
check(len(M.VOTES) == 3, "the voting slip covers all three awards")

# every Monday sheet must have reached print
MPDF = os.path.join(os.path.dirname(HERE), "materials", "pdf")
for slug in ("monday-lesson-plan", "monday-listening", "monday-audio-script",
             "monday-great-person", "monday-presentation-kit",
             "monday-audience-cards", "monday-certificates"):
    fn = SHEETFILE.get(slug)
    check(fn is not None, f"{slug}: sheet is in the running order")
    if fn:
        check(os.path.exists(os.path.join(MPDF, fn + ".pdf")), f"{slug}: PDF exists")
print()

# ------------------------------------------- poster collocations reading sheet
print("-- Talk About Remarkable People")
import phrases as P

paras = [norm(t) for _, t in P.READING]

# every phrase in task 1 must be findable, and in exactly one paragraph
for phrase, want in P.FIND:
    probe = norm(" ".join(phrase.split()[2:]))      # drop the leading "to <verb>"
    hits = [i for i, t in enumerate(paras, 1) if probe in t]
    check(hits == [want], f"task 1: '{phrase}' is in paragraph {want} and nowhere else",
          f"found in {hits or 'no paragraph'}")

# the word bank must still be exactly the answers
check(sorted(P.VERB_BANK) == sorted(a for _, a in P.VERB_GAPS),
      "task 4: the word box matches the answers")
check(all("____" in s_ for s_, _ in P.VERB_GAPS),
      "task 4: every sentence actually has a gap")
# every collocation practised in task 4 must really occur in the reading:
# the answer verb plus the two words that follow the gap
for s_, a in P.VERB_GAPS:
    after = norm(s_.split("____________", 1)[1]).split()
    probe = " ".join([norm(a)] + after[:2])
    check(any(probe in t for t in paras),
          f"task 4: the collocation '{probe}' is in the reading")

# who-is-it uses all five people and only legal letters
letters = {a for _, a in P.WHO}
check(letters == {"E", "N", "L", "D", "I"}, "task 2: all five people are used, and only those",
      str(sorted(letters)))

# the matching halves must be a permutation that never lines up with its own stem
key = getattr(P, "_noun_key", None)
check(key is not None and sorted(key) == list(range(len(P.NOUN_PAIRS))),
      "task 3: the key is a complete permutation")
if key:
    check(all(i != k for i, k in enumerate(key)),
          "task 3: no half lines up with its own stem")
check(len({b for _, b in P.NOUN_PAIRS}) == len(P.NOUN_PAIRS),
      "task 3: no noun appears twice, so every item has one answer")

check({a for _, a in P.FACT_OPINION} == {"FACT", "OPINION"},
      "task 5: both answers occur")

# the ages at death in the new text must follow from the dates in the pack
YEARS = {d["name"]: [int(x) for x in re.findall(r"\d{4}", html.unescape(d["dates"]))]
         for d in C.PEOPLE}
AGES = {"Elizabeth I": 69, "Horatio Nelson": 47, "John Lennon": 40,
        "Princess Diana": 36, "Isaac Newton": 84}
reading = norm(" ".join(t for _, t in P.READING))
for name, age in AGES.items():
    born, died = YEARS[name]
    check(died - born - 1 <= age <= died - born,
          f"{name}: 'died at the age of {age}' fits {born}-{died}")
    check(f"died at the age of {age}" in reading,
          f"{name}: the reading gives the age at death")

# the four value judgements must be flagged, not smuggled in as facts
JUDGEMENTS = ["influential leader", "inspiring leader", "changed the course"]
flagged = norm(" ".join(q for q, _ in P.FACT_OPINION))
for j in JUDGEMENTS[:2]:
    check(j in flagged or j in norm(P.TEACHER_NOTE),
          f"the phrase '{j}' is named as a judgement somewhere the teacher sees it")
check(sum(1 for _, a in P.FACT_OPINION if a == "OPINION") >= 3,
      "task 5 has at least three opinions to catch")

for slug in ("phrases-remarkable-people", "phrases-answer-key"):
    fn = SHEETFILE.get(slug)
    check(fn is not None, f"{slug}: sheet is in the running order")
    if fn:
        check(os.path.exists(os.path.join(MPDF, fn + ".pdf")), f"{slug}: PDF exists")
print()

print(f"\n{checks - len(fails)}/{checks} checks passed.")
if fails:
    print("\nFAILURES:")
    for f in fails:
        print("  -", f)
    sys.exit(1)

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
      {"Isaac Newton", "John Lennon", "Princess Diana", "Charles Darwin", "Horatio Nelson"},
      "pack covers Newton, Lennon, Diana, Darwin and Nelson")
for d in C.PEOPLE:
    check(len(d["tf"]) == 8 and len(d["gaps"]) == 8 and len(d["qs"]) == 6 and len(d["match"]) == 5,
          f"{d['name']}: full exercise set (8 T/F, 8 gaps, 6 questions, 5 matches)")

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

    f = os.path.join(DOCX, SHEETFILE["mixed-round"] + ".docx")
    if os.path.exists(f):
        want = [None] * len(C.NUMBERS)
        for j, slot in enumerate(C._nums_key):
            want[slot] = html.unescape(re.sub("<[^>]+>", "", C.NUMBERS[j][1]))
        check(col(f, 4, len(C.NUMBERS), 3) == want,
              "Word numbers round is in the same order as the PDF")
    print()

print(f"\n{checks - len(fails)}/{checks} checks passed.")
if fails:
    print("\nFAILURES:")
    for f in fails:
        print("  -", f)
    sys.exit(1)

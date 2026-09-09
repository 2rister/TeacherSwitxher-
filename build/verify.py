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
check({d["name"] for d in C.PEOPLE} == {"Isaac Newton", "John Lennon", "Princess Diana"},
      "pack covers Newton, Lennon and Diana")
for d in C.PEOPLE:
    check(len(d["tf"]) == 8 and len(d["gaps"]) == 8 and len(d["qs"]) == 6 and len(d["match"]) == 5,
          f"{d['name']}: full exercise set (8 T/F, 8 gaps, 6 questions, 5 matches)")

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
        f = os.path.join(DOCX, f"0{i}-{d['slug']}.docx")
        if not os.path.exists(f):
            check(False, f"{d['name']}: Word version exists"); continue
        want = [None] * len(d["match"])
        for j, slot in enumerate(d["_match_key"]):
            want[slot] = html.unescape(re.sub("<[^>]+>", "", d["match"][j][1]))
        check(col(f, 4, len(d["match"]), 3) == want,
              f"{d['name']}: Word matching column is in the same order as the PDF")

    f = os.path.join(DOCX, "04-mixed-round.docx")
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

# -*- coding: utf-8 -*-
"""Repair the Jeopardy deck.

1. NAVIGATION. The board's 40 tiles were linked in reading order - across each
   row - while the question slides run down each category in turn. Every tile
   except the first and the last therefore opened somebody else's question:
   "Career 100" led to "Childhood & Early Life 200", and so on. Each tile is
   relinked from its own position in the grid.

2. CONTENT.
   - Childhood & Early Life 300 asked "Who was raised by HER strict aunt Mimi?"
     with the answer John Lennon.
   - Five "who is it" questions gave the answer away with a pronoun: "his aunt",
     "his grandmother", "his right arm". With three men and two women on the
     board that halves the field before anyone thinks. All five are rewritten
     without a pronoun; the answers are unchanged.
   - Wild Card 600 asks for the five people oldest first and answered
     "Newton -> Nelson -> Elizabeth -> Lennon -> Diana". By year of birth
     Elizabeth I (1533) comes before Newton (1642).
   - Achievements 400 asked "What did Nelson WIN at the Battle of the Nile?"
     but the answer is "He defeated a large French fleet" - which answers
     "what did he do", not "what did he win".

3. STRAY CLICKS. The deck set no slide-show options, so PowerPoint's default
   applied: a click anywhere advances to the next slide. On the board that
   jumps to Childhood 100 and the class loses its place. Game slides now
   advance only through their buttons; the keyboard still works everywhere,
   and the title and teacher-notes slides are left alone.
"""
import os, sys, zipfile
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(os.path.dirname(HERE), "materials", "jeopardy")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    DECK, "Jeopardy_Interesting_People_A2_original.pptx")
DST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    DECK, "Jeopardy_Interesting_People_A2_fixed.pptx")

# OOXML parts conventionally use a double-quoted declaration; lxml emits single
# quotes. Both are valid XML, but matching the original keeps the diff to intent.
DECL = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'


def ser(tree):
    return DECL + etree.tostring(tree, xml_declaration=False, encoding="UTF-8")


NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
RID = f"{{{NS['r']}}}id"

Z = zipfile.ZipFile(SRC)
parts = {n: Z.read(n) for n in Z.namelist()}

# ---------------------------------------------------------------- slide 2
sl2 = etree.fromstring(parts["ppt/slides/slide2.xml"])
rels = etree.fromstring(parts["ppt/slides/_rels/slide2.xml.rels"])
target2rid = {}
for rel in rels:
    tgt = rel.get("Target", "")
    if tgt.endswith(".xml") and "slide" in tgt:
        target2rid[tgt.split("/")[-1]] = rel.get("Id")

tiles = []
for sp in sl2.iter(f"{{{NS['p']}}}sp"):
    txt = "".join(t.text or "" for t in sp.iter(f"{{{NS['a']}}}t")).strip()
    off = sp.find(f".//{{{NS['a']}}}off")
    if txt.isdigit() and off is not None:
        tiles.append((int(off.get("x")), int(off.get("y")), int(txt), sp))

cols = sorted({t[0] for t in tiles})
rows = sorted({t[1] for t in tiles})
assert len(tiles) == 40 and len(cols) == 5 and len(rows) == 8, (len(tiles), len(cols), len(rows))

# question slides run category by category: Childhood 100..800, then Career, ...
relinked = 0
for x, y, pts, sp in tiles:
    ci, ri = cols.index(x), rows.index(y)
    assert pts == (ri + 1) * 100, f"tile text {pts} does not match grid row {ri+1}"
    dest = f"slide{3 + 16 * ci + 2 * ri}.xml"
    rid = target2rid[dest]
    changed = False
    for hl in sp.iter(f"{{{NS['a']}}}hlinkClick"):
        if hl.get(RID) != rid:
            hl.set(RID, rid)
            changed = True
    relinked += changed
parts["ppt/slides/slide2.xml"] = ser(sl2)
print(f"board: relinked {relinked} of 40 tiles")

# ---------------------------------------------------------------- content
def edit_text(slide_no, old, new):
    key = f"ppt/slides/slide{slide_no}.xml"
    tree = etree.fromstring(parts[key])
    hits = 0
    for t in tree.iter(f"{{{NS['a']}}}t"):
        if t.text and old in t.text:
            t.text = t.text.replace(old, new)
            hits += 1
    assert hits == 1, f"slide {slide_no}: expected 1 occurrence of {old!r}, found {hits}"
    parts[key] = ser(tree)
    print(f"slide {slide_no}: {old!r} -> {new!r}")

# no pronoun may point at the answer in an identify-the-person question
edit_text(7, "Who was raised by her strict aunt Mimi?",
             "Who was raised by a strict aunt called Mimi?")
edit_text(9, "Who lived with his grandmother when he was a child?",
             "Who was left with a grandmother as a small child?")
edit_text(51, "Who lost his right arm?", "Who lost an arm in a battle?")
edit_text(79, "Which person was born on the same day as his son?",
              "Which person had a son with the same birthday?")
edit_text(81, "Which person continued his career after losing an eye and an arm?",
              "Which person continued working after losing an eye and an arm?")
edit_text(41, "What did Nelson win at the Battle of the Nile?",
              "What did Nelson do at the Battle of the Nile?")
edit_text(78, "Newton → Nelson → Elizabeth → Lennon → Diana.",
              "Elizabeth I → Newton → Nelson → Lennon → Diana.")

# --------------------------------------------------- stop stray clicks
GAME_SLIDES = range(2, 84)          # board, questions, answers, final round
for n in GAME_SLIDES:
    key = f"ppt/slides/slide{n}.xml"
    tree = etree.fromstring(parts[key])
    tr = tree.find(f"{{{NS['p']}}}transition")
    if tr is None:
        tr = etree.SubElement(tree, f"{{{NS['p']}}}transition")
        # must sit after cSld/clrMapOvr and before timing, per the schema
        tree.remove(tr)
        anchor = tree.find(f"{{{NS['p']}}}clrMapOvr")
        (anchor if anchor is not None else tree[0]).addnext(tr)
    tr.set("advClick", "0")
    parts[key] = ser(tree)
print(f"click-advance disabled on {len(GAME_SLIDES)} game slides")

# ---------------------------------------------------------------- write out
with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as out:
    for item in Z.infolist():                 # keep original order and metadata
        out.writestr(item, parts[item.filename])
print(f"\nwrote {DST}")

# -*- coding: utf-8 -*-
"""Editable Word versions of the pack:  python3 build/make_docx.py

These are for editing, not for the poster look — Word cannot reproduce the
parchment, the engraved plates or the numbered colour bars. Layout, wording and
exercise order match the PDFs exactly, so a teacher can retype a question here
and print from Word, or paste changes back into build/content.py.
"""
import html as _html
import os, re, sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "materials", "docx")
IMG = os.path.join(ROOT, "materials", "img")
sys.path.insert(0, HERE)

import content as C
import grammar as G
import build as B

RED = RGBColor(0x9D, 0x22, 0x26)
NAVY = RGBColor(0x1B, 0x2A, 0x4A)
GREY = RGBColor(0x5A, 0x4A, 0x38)
BODY_FONT = "Cambria"


def txt(s):
    """content.py stores HTML; Word wants plain text."""
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", str(s)))).strip()


def shade(cell, hexcolor):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hexcolor)
    cell._tc.get_or_add_tcPr().append(el)


def new_doc():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = BODY_FONT
    st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(1.6)
        s.left_margin = s.right_margin = Cm(1.8)
    return doc


def para(doc, text="", size=11, bold=False, italic=False, color=None,
         align=None, space_after=4, space_before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    if align is not None:
        p.alignment = align
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        if color is not None:
            r.font.color.rgb = color
    return p


def task_head(doc, no, title, hint):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f"TASK {no}   {title.upper()}")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = NAVY
    if hint:
        h = p.add_run(f"   {hint}")
        h.italic = True
        h.font.size = Pt(9.5)
        h.font.color.rgb = GREY
    return p


def grid(doc, rows, cols, widths=None):
    t = doc.add_table(rows=rows, cols=cols)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    if widths:
        t.autofit = False
        for row in t.rows:
            for cell, w in zip(row.cells, widths):
                cell.width = Cm(w)
    return t


def cell_text(cell, text, size=10.5, bold=False, italic=False, color=None, align=None):
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    if color is not None:
        r.font.color.rgb = color


L = B.L   # answer-letter helper, shared with the PDF build


def person_doc(d):
    doc = new_doc()

    para(doc, "INTERESTING PEOPLE  ·  READING & FACTS  ·  LEVEL A2",
         size=9, bold=True, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

    head = grid(doc, 1, 2, widths=[4.2, 12.6])
    head.style = "Normal Table"
    pic = head.cell(0, 0).paragraphs[0]
    pic.add_run().add_picture(os.path.join(IMG, d["portrait"]), width=Cm(3.9))

    box = head.cell(0, 1)
    cell_text(box, txt(d["name"]).upper(), size=22, bold=True, color=NAVY)
    for line, kw in ((txt(d["dates"]), dict(size=11, bold=True, color=RED)),
                     (txt(d["strap"]), dict(size=10.5, color=GREY)),
                     (txt(d["tagline"]), dict(size=11.5, italic=True))):
        p = box.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(line)
        r.font.size = Pt(kw["size"])
        r.bold = kw.get("bold", False)
        r.italic = kw.get("italic", False)
        if kw.get("color") is not None:
            r.font.color.rgb = kw["color"]

    para(doc, "READ THE TEXT", size=13, bold=True, color=NAVY, space_before=12, space_after=2)
    para(doc, "Paragraph numbers help you find the answers.",
         size=9.5, italic=True, color=GREY, space_after=6)
    for i, t in enumerate(d["text"], 1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        n = p.add_run(f"{i}  ")
        n.bold = True
        n.font.size = Pt(9)
        n.font.color.rgb = RED
        p.add_run(txt(t)).font.size = Pt(11)

    para(doc, f'"{txt(d["pull"])}"', size=12, italic=True, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=10)

    # ---- glossary
    gl = C.GLOSSARY[d["slug"]]
    para(doc, "WORDS TO KNOW", size=12, bold=True, color=NAVY, space_before=6, space_after=4)
    t = grid(doc, (len(gl) + 1) // 2, 2, widths=[8.4, 8.4])
    for i, (w, expl) in enumerate(gl):
        c = t.cell(i // 2, i % 2)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(txt(w))
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RED
        p.add_run(" – " + txt(expl)).font.size = Pt(10)

    doc.add_section(WD_SECTION.NEW_PAGE)

    # ---- 1  true / false / not given
    task_head(doc, 1, "True, False or Not Given", "Circle T, F or NG.")
    t = grid(doc, len(d["tf"]), 3, widths=[1.0, 13.2, 2.6])
    for i, (s, _) in enumerate(d["tf"]):
        cell_text(t.cell(i, 0), f"{i + 1}.", align=WD_ALIGN_PARAGRAPH.CENTER)
        cell_text(t.cell(i, 1), txt(s))
        cell_text(t.cell(i, 2), "T   F   NG", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---- 2  gap fill
    task_head(doc, 2, "Fill in the gaps", "Use the words in the box.")
    bank = doc.add_table(rows=1, cols=1)
    bank.style = "Table Grid"
    shade(bank.cell(0, 0), "EFEFEF")
    cell_text(bank.cell(0, 0), "   ·   ".join(txt(w) for w in d["bank"]),
              size=10.5, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
    for i, (s, _) in enumerate(d["gaps"], 1):
        p = doc.add_paragraph(style="List Number" if False else None)
        p.paragraph_format.space_after = Pt(7)
        p.paragraph_format.left_indent = Cm(0.7)
        p.add_run(f"{i}.  ").bold = True
        p.add_run(txt(s).replace("____________", "_" * 16)).font.size = Pt(11)

    doc.add_section(WD_SECTION.NEW_PAGE)

    # ---- 3  open questions
    task_head(doc, 3, "Answer the questions", "Write full sentences.")
    for i, (q, _) in enumerate(d["qs"], 1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.7)
        p.add_run(f"{i}.  ").bold = True
        p.add_run(txt(q)).font.size = Pt(11)
        for _ in range(2):
            r = doc.add_paragraph()
            r.paragraph_format.space_after = Pt(6)
            r.paragraph_format.left_indent = Cm(1.2)
            r.add_run("." * 96).font.color.rgb = GREY

    # ---- 4  matching
    # _match_key[i] is the display slot holding stem i's half; invert it to redraw
    # the shuffled column exactly as the PDF prints it.
    rhs = [None] * len(d["match"])
    for i, slot in enumerate(d["_match_key"]):
        rhs[slot] = d["match"][i][1]
    task_head(doc, 4, "Match the two halves", "Write a, b, c, d or e.")
    t = grid(doc, len(d["match"]), 4, widths=[1.0, 1.3, 7.1, 7.4])
    for i, ((stem, _), half) in enumerate(zip(d["match"], rhs)):
        cell_text(t.cell(i, 0), f"{i + 1}.", align=WD_ALIGN_PARAGRAPH.CENTER)
        cell_text(t.cell(i, 1), "", align=WD_ALIGN_PARAGRAPH.CENTER)
        cell_text(t.cell(i, 2), txt(stem))
        cell_text(t.cell(i, 3), f"{L(i)})  " + txt(half))

    # ---- 5  jeopardy call-back
    task_head(doc, 5, "Back to the board", "From the game – texts face down!")
    t = grid(doc, len(d["jeopardy"]), 2, widths=[2.0, 14.8])
    for i, (pts, q, _) in enumerate(d["jeopardy"]):
        shade(t.cell(i, 0), "1B2A4A")
        cell_text(t.cell(i, 0), str(pts), bold=True,
                  color=RGBColor(0xFF, 0xFF, 0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
        cell_text(t.cell(i, 1), txt(q))

    return doc


def mixed_doc():
    doc = new_doc()
    para(doc, "THE MIXED ROUND  ·  NEWTON  ·  LENNON  ·  DIANA",
         size=13, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

    task_head(doc, 1, "Who is it?", "N = Newton  ·  L = Lennon  ·  D = Diana")
    t = grid(doc, len(C.WHO), 3, widths=[1.0, 13.2, 2.6])
    for i, (q, _) in enumerate(C.WHO):
        cell_text(t.cell(i, 0), f"{i + 1}.", align=WD_ALIGN_PARAGRAPH.CENTER)
        cell_text(t.cell(i, 1), txt(q))
        cell_text(t.cell(i, 2), "N   L   D", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    task_head(doc, 2, "Put them in order", "1 = oldest, 5 = youngest. Use the year of birth.")
    t = grid(doc, len(C.TIMELINE), 2, widths=[1.6, 15.2])
    for i, (n, y) in enumerate(C.TIMELINE):
        cell_text(t.cell(i, 0), "", align=WD_ALIGN_PARAGRAPH.CENTER)
        cell_text(t.cell(i, 1), f"{txt(n)}  ({y})")

    task_head(doc, 3, "What do these numbers mean?", "Write a–h next to each number.")
    nums_rhs = [None] * len(C.NUMBERS)
    for i, slot in enumerate(C._nums_key):
        nums_rhs[slot] = C.NUMBERS[i][1]
    t = grid(doc, len(C.NUMBERS), 4, widths=[1.0, 1.3, 3.4, 11.1])
    for i, ((num, _), fact) in enumerate(zip(C.NUMBERS, nums_rhs)):
        cell_text(t.cell(i, 0), f"{i + 1}.", align=WD_ALIGN_PARAGRAPH.CENTER)
        cell_text(t.cell(i, 1), "", align=WD_ALIGN_PARAGRAPH.CENTER)
        cell_text(t.cell(i, 2), txt(num), bold=True)
        cell_text(t.cell(i, 3), f"{L(i)})  " + txt(fact))

    doc.add_section(WD_SECTION.NEW_PAGE)

    task_head(doc, 4, "Final Jeopardy · Speaking", "Work in pairs, then tell the class.")
    para(doc, txt(C.DEBATE["question"]), size=12, bold=True, space_after=8)
    t = grid(doc, 2, len(C.DEBATE["steps"]), widths=[4.2] * len(C.DEBATE["steps"]))
    for i, (step, say) in enumerate(C.DEBATE["steps"]):
        shade(t.cell(0, i), "9D2226" if i % 2 == 0 else "1B2A4A")
        cell_text(t.cell(0, i), step, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF),
                  align=WD_ALIGN_PARAGRAPH.CENTER)
        cell_text(t.cell(1, i), txt(say), italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    task_head(doc, 5, "Useful phrases", "Take one phrase from each box.")
    t = grid(doc, (len(C.DEBATE["phrases"]) + 1) // 2, 2, widths=[8.4, 8.4])
    for i, (title, phrases) in enumerate(C.DEBATE["phrases"]):
        c = t.cell(i // 2, i % 2)
        cell_text(c, txt(title), size=10, bold=True, color=RED)
        for ph in phrases:
            p = c.add_paragraph()
            p.paragraph_format.space_after = Pt(1)
            p.add_run("• " + txt(ph)).italic = True
            p.runs[0].font.size = Pt(10)
    return doc


def key_doc():
    doc = new_doc()
    para(doc, "ANSWER KEY  ·  FOR THE TEACHER", size=14, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    for d in C.PEOPLE:
        para(doc, f"SHEET {d['num']}  ·  {txt(d['name']).upper()}",
             size=12, bold=True, color=NAVY, space_before=10, space_after=4)
        para(doc, "1  T/F/NG:  " + "   ".join(f"{i}{a}" for i, (_, a) in enumerate(d["tf"], 1)),
             size=10.5)
        para(doc, "2  Gaps:  " + "   ".join(f"{i} {txt(a)}" for i, (_, a) in enumerate(d["gaps"], 1)),
             size=10.5)
        para(doc, "3  Questions:", size=10.5, bold=True, space_after=1)
        for i, (_, a) in enumerate(d["qs"], 1):
            para(doc, f"     {i}. {txt(a)}", size=10.5, space_after=1)
        para(doc, "4  Matching:  " + "   ".join(f"{i} {L(k)}"
                                                for i, k in enumerate(d["_match_key"], 1)),
             size=10.5, space_before=3)
        para(doc, "5  Back to the board:", size=10.5, bold=True, space_after=1)
        for pts, _, a in d["jeopardy"]:
            para(doc, f"     {pts} pts – {txt(a)}", size=10.5, space_after=1)

    para(doc, "SHEET IV  ·  THE MIXED ROUND", size=12, bold=True, color=NAVY,
         space_before=12, space_after=4)
    para(doc, "1  Who is it?  " + "   ".join(f"{i} {a[0]}" for i, (_, a) in enumerate(C.WHO, 1)),
         size=10.5)
    para(doc, "2  Order:  " + "  →  ".join(txt(n) for n in C.TIMELINE_KEY), size=10.5)
    rank = {n: i for i, n in enumerate(C.TIMELINE_KEY, 1)}
    para(doc, "     Numbers to write in the boxes, top to bottom as printed:  "
              + "  ".join(str(rank[n]) for n, _ in C.TIMELINE), size=10, color=GREY)
    para(doc, "3  Numbers:  " + "   ".join(f"{i} {L(k)}"
                                           for i, k in enumerate(C._nums_key, 1)), size=10.5)
    para(doc, "4  Final Jeopardy:  No single correct answer. Accept any person if the student "
              "gives a reason and an example from the text.", size=10.5)

    doc.add_section(WD_SECTION.NEW_PAGE)
    para(doc, "TEACHER'S NOTES  ·  BEFORE YOU PRINT", size=14, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    for title, body in C.TEACHER_NOTES:
        para(doc, txt(title), size=11.5, bold=True, color=RED, space_before=8, space_after=2)
        para(doc, txt(body), size=10.5)

    para(doc, "IMAGE CREDITS & LICENCES", size=11.5, bold=True, color=RED,
         space_before=12, space_after=2)
    for line in (
        "Isaac Newton – portrait by Godfrey Kneller, 1689. Public domain. Via Wikimedia Commons.",
        "John Lennon – photograph by Joost Evers / Anefo, 1969. CC0 1.0. Via Wikimedia Commons.",
        "Princess Diana – photograph by John Mathew Smith, 1997. CC BY-SA 2.0; this pack "
        "reproduces it in duotone as a derivative work under the same licence. Via Wikimedia Commons.",
        "Type: Cinzel, Playfair Display, EB Garamond – SIL Open Font License 1.1.",
    ):
        para(doc, line, size=9.5, space_after=2)
    return doc


def grammar_doc(d, mixed=False):
    doc = new_doc()
    para(doc, "PAST SIMPLE  ·  GRAMMAR  ·  LEVEL A2", size=9, bold=True, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    para(doc, txt(d["name"]).upper(), size=18, bold=True, color=NAVY, space_after=1)
    para(doc, txt(d["dates"]), size=10.5, bold=True, color=RED, space_after=10)

    task_head(doc, 1, "Choose the correct answer", "Circle a, b or c.")
    for i, (sentence, opts, _) in enumerate(d["mc"], 1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.left_indent = Cm(0.7)
        p.add_run(f"{i}.  ").bold = True
        p.add_run(txt(sentence).replace("____", "_" * 8)).font.size = Pt(11)
        for j, o in enumerate(opts):
            lab = p.add_run(f"    {chr(97 + j)}) ")
            lab.bold = True
            lab.font.size = Pt(10)
            lab.font.color.rgb = RED
            p.add_run(txt(o)).font.size = Pt(10.5)

    nxt = 2
    if mixed:
        task_head(doc, 2, "Make the question", "Put the words in the right order.")
        for i, (scram, _) in enumerate(G.WORD_ORDER, 1):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.left_indent = Cm(0.7)
            p.add_run(f"{i}.  ").bold = True
            r = p.add_run(txt(scram)); r.italic = True; r.font.size = Pt(11)
            q = doc.add_paragraph()
            q.paragraph_format.space_after = Pt(6)
            q.paragraph_format.left_indent = Cm(1.2)
            q.add_run("." * 96).font.color.rgb = GREY
        nxt = 3

    task_head(doc, nxt, "Put the verb into the Past Simple", "Use the verb in brackets.")
    for i, (sentence, _) in enumerate(d["bracket"], 1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.left_indent = Cm(0.7)
        p.add_run(f"{i}.  ").bold = True
        p.add_run(txt(sentence).replace("__________", "_" * 18)).font.size = Pt(11)

    if mixed:
        task_head(doc, 4, "Irregular verbs", "Write the Past Simple form.")
        t = grid(doc, (len(G.IRREGULAR) + 1) // 2, 4, widths=[3.6, 4.8, 3.6, 4.8])
        for i, (inf, _) in enumerate(G.IRREGULAR):
            r, c = i // 2, (i % 2) * 2
            cell_text(t.cell(r, c), txt(inf), bold=True, color=RED)
            cell_text(t.cell(r, c + 1), "")
    return doc


def grammar_key_doc():
    doc = new_doc()
    para(doc, "GRAMMAR ANSWER KEY  ·  FOR THE TEACHER", size=14, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    for d in G.GRAMMAR_PEOPLE + [G.MIXED]:
        para(doc, f"SHEET {d['num']}  ·  {txt(d['name']).upper()}",
             size=12, bold=True, color=NAVY, space_before=10, space_after=4)
        para(doc, "1  Choose:  " + "   ".join(f"{i}{chr(97 + k)}"
                                              for i, (_, _, k) in enumerate(d["mc"], 1)), size=10.5)
        n = 2
        if d is G.MIXED:
            para(doc, "2  Make the question:", size=10.5, bold=True, space_after=1)
            for i, (_, a) in enumerate(G.WORD_ORDER, 1):
                para(doc, f"     {i}. {txt(a)}", size=10.5, space_after=1)
            n = 3
        para(doc, f"{n}  Past Simple:", size=10.5, bold=True, space_before=3, space_after=1)
        for i, (_, a) in enumerate(d["bracket"], 1):
            val = txt(a) if isinstance(a, str) else "   ".join(
                f"({j}) {txt(x)}" for j, x in enumerate(a, 1))
            para(doc, f"     {i}. {val}", size=10.5, space_after=1)

    para(doc, "SHEET X  ·  TASK 4  ·  IRREGULAR VERBS", size=12, bold=True, color=NAVY,
         space_before=12, space_after=4)
    para(doc, "   ".join(f"{a} \u2192 {b}" for a, b in G.IRREGULAR), size=10.5)
    para(doc, "NOTES", size=12, bold=True, color=RED, space_before=12, space_after=3)
    para(doc, txt(G.GRAMMAR_NOTE), size=10.5)
    para(doc, "Both the full and the contracted form are correct: did not like and didn't like "
              "are equally right, and so are was not and wasn't. In task 'Make the question' and "
              "in question items, the capital letter is part of the answer.",
         size=10.5, space_before=6)
    return doc


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    B.write_html()          # fixes the matching and numbers keys, exactly as the PDFs use them
    print("\nWriting editable Word versions\n")
    docs = [(f"0{i + 1}-{d['slug']}", person_doc(d)) for i, d in enumerate(C.PEOPLE)]
    docs.append(("05-mixed-round", mixed_doc()))
    docs.append(("06-answer-key", key_doc()))
    docs += [(f"0{7 + i}-grammar-{d['slug']}", grammar_doc(d))
             for i, d in enumerate(G.GRAMMAR_PEOPLE)]
    docs.append(("10-grammar-mixed", grammar_doc(G.MIXED, mixed=True)))
    docs.append(("11-grammar-answer-key", grammar_key_doc()))
    for name, doc in docs:
        path = os.path.join(OUT, name + ".docx")
        doc.save(path)
        print(f"  docx  {name}.docx  ({os.path.getsize(path) // 1024} KB)")
    print("\nDone.")

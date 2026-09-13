# -*- coding: utf-8 -*-
"""Build the printable 'Interesting People' A2 pack.

    python3 build/build.py            # write HTML + render PDFs
    python3 build/build.py --html     # write HTML only

Every sheet is one or more .page divs sized to A4; Chromium prints them at
exactly 210x297 mm with no scaling. After rendering, each page is measured and
any content overflow is reported, so a layout can never silently lose a line.
"""
import os, random, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_HTML = os.path.join(ROOT, "materials", "html")
OUT_PDF = os.path.join(ROOT, "materials", "pdf")
OUT_BW = os.path.join(ROOT, "materials", "pdf-bw")
sys.path.insert(0, HERE)

import content as C
import grammar as G
import monday as M
import render as R

KICKER = "Interesting People &#183; Reading &amp; Facts &#183; Level A2"
FOOT_L = "Interesting People &#183; A2"
FOOT_M = "Ideas &#183; People &#183; Arguments"

rnd = random.Random(20260909)          # fixed seed => identical output every build


def roman(n):
    out = ""
    for value, sign in ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= value:
            out += sign
            n -= value
    return out


def number_sheets():
    """Derive every sheet number from the running order.

    Adding a person used to mean hand-editing each numeral after them - in the
    mastheads, the footers and the prose - which is exactly how a wrong one
    reaches print. Persons take I..N, then the mixed round, the reading key,
    the grammar sheets and the grammar key.
    """
    n = 1
    for d in C.PEOPLE:
        d["num"] = roman(n); n += 1
    refs = {"MIXED": roman(n)}; n += 1
    refs["KEY"] = roman(n); n += 1
    for d in G.GRAMMAR_PEOPLE:
        d["num"] = roman(n); n += 1
    G.MIXED["num"] = refs["GMIXED"] = roman(n); n += 1
    refs["GKEY"] = roman(n)
    refs["READING"] = f'{C.PEOPLE[0]["num"]}&#8211;{C.PEOPLE[-1]["num"]}'
    refs["GRAMMAR"] = f'{G.GRAMMAR_PEOPLE[0]["num"]}&#8211;{G.GRAMMAR_PEOPLE[-1]["num"]}'
    for d in C.PEOPLE:
        refs["#" + d["slug"]] = d["num"]
    for d in G.GRAMMAR_PEOPLE:
        refs["#grammar-" + d["slug"]] = d["num"]
    return refs


SHEET = {}


def subst(text):
    """Resolve [[TOKEN]] sheet references inside static prose."""
    for k, v in SHEET.items():
        text = text.replace(f"[[{k}]]", v)
    left = re.findall(r"\[\[[^\]]+\]\]", text)
    assert not left, f"unresolved sheet reference: {left}"
    return text


def shuffled_rhs(pairs):
    """Right-hand halves in a stable non-matching order, plus the answer key."""
    idx = list(range(len(pairs)))
    while True:
        rnd.shuffle(idx)
        if all(i != j for i, j in enumerate(idx)):     # no half sits opposite its own stem
            break
    rhs = [pairs[i][1] for i in idx]
    key = [rhs.index(pairs[i][1]) for i in range(len(pairs))]   # stem i -> letter key[i]
    return rhs, key


# --------------------------------------------------------------- person sheet
def person_sheet(d):
    paras = "".join(f'<p><span class="pn">{i}</span>{t}</p>'
                    for i, t in enumerate(d["text"], 1))
    first, last = d["name"].rsplit(" ", 1)
    words = sum(len(t.split()) for t in d["text"])
    # A long text sets tighter and sends its glossary to the exercises page; a short
    # text keeps the glossary beside it. Either way the reading fills exactly one sheet.
    fit = " dense" if words > 300 else ""
    short = words < 250
    gloss = R.glossary(C.GLOSSARY[d["slug"]])

    p1 = f"""<div class="page">
{R.masthead(KICKER, d['num'])}
<section class="hero">
  <div class="portrait-frame"><img src="../img/{d['portrait']}" alt="{d['name']}"></div>
  <div class="hero-body">
    <h1 class="hero-name">{first} <span class="r">{last}</span></h1>
    <div class="hero-dates">{d['dates']}</div>
    <div class="hero-strap">{d['strap']}</div>
    <div class="hero-tagline">{d['tagline']}</div>
  </div>
</section>
<section class="reading{fit}">
  <div class="reading-head"><h2>Read the text</h2>
    <span class="hint">Paragraph numbers help you find the answers.</span></div>
  {paras}
</section>
{gloss if short else ''}
<div class="pullquote">&#8220;{d['pull']}&#8221;</div>
{R.foot(FOOT_L, FOOT_M, f"Sheet {d['num']} &#183; p. 1")}
</div>"""

    p2 = f"""<div class="page">
{R.masthead(f"{d['name']} &#183; Exercises", d['num'])}
<div class="tasks">
{R.task(1, "True, False or Not Given", "Circle T, F or NG.", R.tf_body(d['tf']))}
{R.task(2, "Fill in the gaps", "Use the words in the box.", R.gap_body(d['bank'], d['gaps']), navy=True)}
</div>
{'' if short else gloss}
{R.foot(FOOT_L, FOOT_M, f"Sheet {d['num']} &#183; p. 2")}
</div>"""

    rhs, key = shuffled_rhs(d["match"])
    d["_match_key"] = key
    p3 = f"""<div class="page">
{R.masthead(f"{d['name']} &#183; Exercises", d['num'])}
<div class="tasks">
{R.task(3, "Answer the questions", "Write full sentences.", R.q_body(d['qs']))}
{R.task(4, "Match the two halves", "Write a, b, c, d or e.", R.match_body(d['match'], rhs), navy=True)}
{R.task(5, *(("New for the board", "Not on your board yet &#8211; add these three.")
             if d.get("board_is_new") else
             ("Back to the board", "From the game &#8211; texts face down!")),
        body=R.jeopardy_body(d['jeopardy'],
            title=(f"Three questions to add for {d['name']}" if d.get("board_is_new")
                   else f"{d['name']} on the Jeopardy board")))}
</div>
{R.foot(FOOT_L, FOOT_M, f"Sheet {d['num']} &#183; p. 3")}
</div>"""
    return R.head(f"{d['name']} &#8211; A2 reading") + p1 + p2 + p3 + "</body></html>"


# ---------------------------------------------------------- sheet IV: mixed
def mixed_sheet():
    who = "".join(f'<li><div class="tf-row"><span class="stmt">{q}</span>'
                  f'<span class="tf-opts"><span>N</span><span>L</span><span>D</span></span>'
                  f'</div></li>' for q, _ in C.WHO)
    tl = "".join(f'<li><span class="matchbox"></span>{n} '
                 f'<span style="color:#5a4a38">({y})</span></li>' for n, y in C.TIMELINE)
    nums_l = "".join(f'<li><span class="matchbox"></span>{n}</li>' for n, _ in C.NUMBERS)
    nums_rhs, nums_key = shuffled_rhs([(n, f) for n, f in C.NUMBERS])
    C._nums_key = nums_key
    nums_r = "".join(f"<li>{f}</li>" for f in nums_rhs)

    flow = "".join(f'<span class="step">{s}</span>' +
                   ('<span class="arrow">&#8594;</span>' if i < len(C.DEBATE['steps']) - 1 else '')
                   for i, (s, _) in enumerate(C.DEBATE['steps']))
    says = "".join(f"<span>{p}</span>" for _, p in C.DEBATE['steps'])
    phrases = "".join(
        f'<div class="phrase-box"><h4>{t}</h4><ul>' +
        "".join(f"<li>{p}</li>" for p in ps) + "</ul></div>"
        for t, ps in C.DEBATE['phrases'])

    p1 = f"""<div class="page">
{R.masthead("The Mixed Round &#183; Newton &#183; Lennon &#183; Diana", SHEET["MIXED"])}
<div class="tasks">
{R.task(1, "Who is it?", "N = Newton &#183; L = Lennon &#183; D = Diana",
        f'<ol class="items">{who}</ol>')}
{R.task(2, "Put them in order", "1 = oldest, 5 = youngest. Use the year of birth.",
        f'<ol class="items">{tl}</ol>', navy=True)}
{R.task(3, "What do these numbers mean?", "Write a&#8211;h next to each number.",
        f'<div class="match"><ol class="items">{nums_l}</ol>'
        f'<ol class="items rhs">{nums_r}</ol></div>')}
</div>
{R.foot(FOOT_L, FOOT_M, f"Sheet {SHEET['MIXED']} &#183; p. 1")}
</div>"""

    p2 = f"""<div class="page">
{R.masthead("Final Round &#183; Speak &#183; Reason &#183; Persuade &#183; Respect", SHEET["MIXED"])}
<div class="tasks">
{R.task(4, "Final Jeopardy &#183; Speaking", "Work in pairs, then tell the class.",
        f'<p style="margin:0 0 2.6mm;font-size:11.4pt;"><b>{C.DEBATE["question"]}</b></p>'
        f'<div class="flow">{flow}</div>'
        f'<div class="flow-say">{says}</div>', navy=True)}
{R.task(5, "Useful phrases", "Take one phrase from each box.",
        f'<div class="phrase-grid">{phrases}</div>')}
{R.task(5, "Back to the board", "Three questions from the game &#8211; no texts!",
        R.jeopardy_body(
            [(c[0], c[1], c[2]) for d in C.PEOPLE for c in d['jeopardy'][:1]] +
            [(600, "Which person was born on the same day as his son?", "John Lennon."),
             (800, "Put in order, oldest first: Diana, Newton, Lennon, Nelson, Elizabeth.",
              "Elizabeth I &#8594; Newton &#8594; Nelson &#8594; Lennon &#8594; Diana.")],
            title="Bonus points"))}
</div>
{R.foot(FOOT_L, FOOT_M, f"Sheet {SHEET['MIXED']} &#183; p. 2")}
</div>"""
    return R.head("The Mixed Round &#8211; A2") + p1 + p2 + "</body></html>"


# ------------------------------------------- sheets VI-IX: Past Simple grammar
GRAM_KICKER = "Past Simple &#183; Grammar &#183; Level A2"


def grammar_sheet(d):
    return R.head(f"{d['name']} &#8211; Past Simple") + f"""<div class="page">
{R.masthead(GRAM_KICKER, d['num'])}
{R.gram_hero(d)}
<div class="tasks">
{R.task(1, "Choose the correct answer", "Circle a, b or c.", R.mc_body(d['mc']))}
{R.task(2, "Put the verb into the Past Simple", "Use the verb in brackets.",
        R.bracket_body(d['bracket']), navy=True)}
</div>
{R.foot(FOOT_L, FOOT_M, f"Sheet {d['num']} &#183; p. 1")}
</div>""" + "</body></html>"


def grammar_mixed():
    d = G.MIXED
    p1 = f"""<div class="page">
{R.masthead(GRAM_KICKER, d['num'])}
{R.gram_hero(d)}
<div class="tasks">
{R.task(1, "Choose the correct answer", "Circle a, b or c.", R.mc_body(d['mc']))}
{R.task(2, "Make the question", "Put the words in the right order.",
        R.word_order_body(G.WORD_ORDER), navy=True)}
</div>
{R.foot(FOOT_L, FOOT_M, f"Sheet {d['num']} &#183; p. 1")}
</div>"""
    p2 = f"""<div class="page">
{R.masthead("Past Simple &#183; All Three Together", d['num'])}
<div class="tasks">
{R.task(3, "Put the verb into the Past Simple", "Use the verb in brackets.",
        R.bracket_body(d['bracket']), navy=True)}
{R.task(4, "Irregular verbs", "Write the Past Simple form.",
        R.irregular_body(G.IRREGULAR))}
</div>
{R.foot(FOOT_L, FOOT_M, f"Sheet {d['num']} &#183; p. 2")}
</div>"""
    return R.head("Past Simple &#8211; all three together") + p1 + p2 + "</body></html>"


def grammar_key():
    blocks = []
    for d in G.GRAMMAR_PEOPLE + [G.MIXED]:
        mc = " &#183; ".join(f'{i} <b>{chr(97 + k)}</b>'
                             for i, (_, _, k) in enumerate(d["mc"], 1))
        def ans(a):
            if isinstance(a, str):
                return a          # "/" here separates full and contracted forms
            return "  ".join(f'<span class="key-tag">({i})</span> {x}'
                             for i, x in enumerate(a, 1))   # one entry per gap
        br = "".join(f"<li>{ans(a)}</li>" for _, a in d["bracket"])
        wo = ""
        if d is G.MIXED:
            items = "".join(f"<li>{a}</li>" for _, a in G.WORD_ORDER)
            wo = ('<p style="margin:0 0 .6mm;font-size:9.9pt">'
                  '<span class="key-tag">2 MAKE THE QUESTION</span></p>'
                  f"<ol>{items}</ol>")
        blocks.append(f"""<div class="key-block">
<h3>Sheet {d['num']} &#183; {d['name']}</h3>
<p style="margin:0 0 1.4mm;font-size:9.9pt"><span class="key-tag">1 CHOOSE</span> {mc}</p>
{wo}
<p style="margin:0 0 .6mm;font-size:9.9pt"><span class="key-tag">{'3' if d is G.MIXED else '2'} PAST SIMPLE</span></p>
<ol>{br}</ol>
</div>""")
    irr = " &#183; ".join(f"<b>{a}</b> &#8594; {b}" for a, b in G.IRREGULAR)

    p1 = f"""<div class="page">
{R.masthead("Grammar Answer Key &#183; For the teacher", SHEET["GKEY"])}
<div class="key-grid">{''.join(blocks[:2])}</div>
<div style="height:3mm"></div>
<div class="key-grid">{''.join(blocks[2:4])}</div>
{R.foot("Grammar Key", FOOT_M, f"Sheet {SHEET['GKEY']} &#183; p. 1")}
</div>"""
    p2 = f"""<div class="page">
{R.masthead("Grammar Key &#183; Mixed Practice, irregular verbs &amp; notes", SHEET["GKEY"])}
<div class="key-grid" style="grid-template-columns:1fr">{blocks[4]}</div>
<div style="height:3mm"></div>
<h2 style="font-family:Cinzel,serif;font-size:12pt;letter-spacing:.16em;color:#1b2a4a;
           margin:0 0 3mm;text-transform:uppercase">Sheet {SHEET["GMIXED"]} &#183; task 4</h2>
<p style="font-size:10.4pt;line-height:1.7;margin:0 0 4mm">{irr}</p>
<div class="note"><b>How these sheets relate to Sheets {SHEET["READING"]}</b>{subst(G.GRAMMAR_NOTE)}</div>
<div class="note" style="border-left-color:#1b2a4a;background:rgba(27,42,74,.055)">
<b>Marking the negatives and questions</b>
Both the full and the contracted form are correct: <i>did not like</i> and <i>didn&#8217;t like</i>
are equally right, and so are <i>was not</i> and <i>wasn&#8217;t</i>. The key prints both, separated
by a slash. In task 2 the capital letter at the start of a question is part of the answer.</div>
{R.foot("Grammar Key", FOOT_M, f"Sheet {SHEET['GKEY']} &#183; p. 2")}
</div>"""
    return R.head("Grammar answer key") + p1 + p2 + "</body></html>"


# ------------------------------------------------------------ sheet V: key
def L(i):
    return chr(ord("a") + i)


def key_sheet():
    blocks = []
    for d in C.PEOPLE:
        tf = " &#183; ".join(f'{i}<span class="key-tag">{a}</span>'
                             for i, (_, a) in enumerate(d["tf"], 1))
        gaps = " &#183; ".join(f'{i} <b>{a}</b>' for i, (_, a) in enumerate(d["gaps"], 1))
        qs = "".join(f"<li>{a}</li>" for _, a in d["qs"])
        mk = " &#183; ".join(f'{i} <b>{L(k)}</b>'
                             for i, k in enumerate(d["_match_key"], 1))
        jeo = "".join(f'<li><span style="color:#9d2226">{p} pts</span> &#8211; {a}</li>'
                      for p, _, a in d["jeopardy"])
        blocks.append(f"""<div class="key-block">
<h3>Sheet {d['num']} &#183; {d['name']}</h3>
<p style="margin:0 0 1.4mm;font-size:9.9pt"><span class="key-tag">1 T/F/NG</span> {tf}</p>
<p style="margin:0 0 1.4mm;font-size:9.9pt"><span class="key-tag">2 GAPS</span> {gaps}</p>
<p style="margin:0 0 .6mm;font-size:9.9pt"><span class="key-tag">3 QUESTIONS</span></p>
<ol>{qs}</ol>
<p style="margin:1.4mm 0 0;font-size:9.9pt"><span class="key-tag">4 MATCHING</span> {mk}</p>
<p style="margin:1.4mm 0 .6mm;font-size:9.9pt"><span class="key-tag">5 BACK TO THE BOARD</span></p>
<ol style="list-style:none;padding-left:2mm">{jeo}</ol>
</div>""")

    who = " &#183; ".join(f'{i} <b>{a[0]}</b>' for i, (_, a) in enumerate(C.WHO, 1))
    tl = " &#8594; ".join(f"<b>{n}</b>" for n in C.TIMELINE_KEY)
    rank = {n: i for i, n in enumerate(C.TIMELINE_KEY, 1)}
    tl_num = " &#183; ".join(f"<b>{rank[n]}</b>" for n, _ in C.TIMELINE)
    nums = " &#183; ".join(f'{i} <b>{L(k)}</b>' for i, k in enumerate(C._nums_key, 1))
    blocks.append(f"""<div class="key-block">
<h3>Sheet {SHEET["MIXED"]} &#183; The Mixed Round</h3>
<p style="margin:0 0 1.4mm;font-size:9.9pt"><span class="key-tag">1 WHO IS IT?</span> {who}</p>
<p style="margin:0 0 1.4mm;font-size:9.9pt"><span class="key-tag">2 ORDER</span> {tl}</p>
<p style="margin:0 0 1.4mm;font-size:9.4pt;color:#5a4a38">Numbers to write in the boxes,
top to bottom as printed: {tl_num}</p>
<p style="margin:0 0 1.4mm;font-size:9.9pt"><span class="key-tag">3 NUMBERS</span> {nums}</p>
<p style="margin:0;font-size:9.9pt"><span class="key-tag">4 FINAL JEOPARDY</span>
No single correct answer. Accept any person if the student gives a reason
<i>and</i> an example from the text.</p>
</div>""")

    off = [d for d in C.PEOPLE if d.get("board_is_new")]
    offboard = ""
    if off:
        who = ", ".join(f'{d["name"]} (Sheet {d["num"]})' for d in off)
        offboard = (f" The exception{'s are' if len(off) > 1 else ' is'} {who} &#8211; "
                    "not on your board at all, so task 5 there offers three questions "
                    "you can add to it instead.")
    notes = "".join(f"<div class='note'><b>{t}</b>{subst(b)}</div>" for t, b in C.TEACHER_NOTES)

    GAP = '<div style="height:3mm"></div>'
    per, pages = 4, []
    chunks = [blocks[i:i + per] for i in range(0, len(blocks), per)]
    for pno, chunk in enumerate(chunks, 1):
        rows = []
        for i in range(0, len(chunk), 2):
            rows.append('<div class="key-grid">' + "".join(chunk[i:i + 2]) + "</div>")
            if i + 2 < len(chunk):
                rows.append(GAP)
        body = "".join(rows)
        pages.append(f"""<div class="page">
{R.masthead("Answer Key &#183; For the teacher", SHEET["KEY"])}
{body}
{R.foot("Answer Key", FOOT_M, f"Sheet {SHEET['KEY']} &#183; p. {pno}")}
</div>""")
    p1 = "".join(pages)

    p2 = f"""<div class="page">
{R.masthead("Teacher&#8217;s Notes &#183; Checks &amp; Corrections", SHEET["KEY"])}
<h2 style="font-family:Cinzel,serif;font-size:12pt;letter-spacing:.16em;color:#1b2a4a;
           margin:0 0 3mm;text-transform:uppercase">Before you print</h2>
{notes}
<div class="note" style="border-left-color:#1b2a4a;background:rgba(27,42,74,.055)">
<b>How the pack maps onto the game</b>
Every item on the person sheets and on the Mixed Round is built on a fact that appears on the Jeopardy
board, so the handouts and the game test the same knowledge.{offboard}
Suggested order: read the sheet &#8594; do the exercises &#8594; play the game with the texts face down.</div>
<div class="note" style="border-left-color:#b08d57;background:rgba(176,141,87,.09)">
<b>Image credits &amp; licences</b>
<span class="credits">
<b style="display:inline;font-size:8.4pt">Isaac Newton</b> &#8211; portrait by Godfrey Kneller, 1689.
Public domain. Via Wikimedia Commons.<br>
<b style="display:inline;font-size:8.4pt">John Lennon</b> &#8211; photograph by Joost Evers / Anefo, 1969.
Released under CC0 1.0 (public domain dedication). Via Wikimedia Commons.<br>
<b style="display:inline;font-size:8.4pt">Princess Diana</b> &#8211; photograph by John Mathew Smith
(www.celebrity-photos.com), 1997. Licensed <b style="display:inline;font-size:8.4pt">CC BY-SA 2.0</b>;
this pack reproduces it in duotone as a derivative work under the same licence.
Via Wikimedia Commons.<br>
Type: Cinzel, Playfair Display, EB Garamond &#8211; SIL Open Font License 1.1.
</span></div>
{R.foot("Answer Key", FOOT_M, f"Sheet {SHEET['KEY']} &#183; p. {len(chunks) + 1}")}
</div>"""
    return R.head("Answer Key &#8211; A2") + p1 + p2 + "</body></html>"



# ======================================================= Monday 14.09 lesson kit
M_KICK = "Monday 14 September &#183; Elizabeth I &#183; WHAT MAKES A GREAT PERSON?"
M_FOOT = "WHAT MAKES A GREAT PERSON?"


def kit_head(title, sub):
    first, _, last = title.partition("|")
    name = f'{first}<span class="r">{last}</span>' if last else first
    return f'<div class="kit-head"><h1>{name}</h1><div class="sub">{sub}</div></div>'


def stage_table(rows):
    out = []
    for clock, mins, what, how, ix in rows:
        out.append(f'<tr><td class="clk">{clock}</td><td class="min">{mins}&#8242;</td>'
                   f'<td><b class="st">{what}</b><br>{subst(how)}</td>'
                   f'<td class="ix"><span class="tag">{ix}</span></td></tr>')
    return f'<table class="stage">{"".join(out)}</table>'


def lesson_plan():
    tt = "".join(f'<tr><td class="clk">{a}</td><td>{b}</td><td class="len">{c}</td></tr>'
                 for a, b, c in M.TIMETABLE)
    aims = "".join(f"<li>{a}</li>" for a in M.AIMS)
    mats = "".join(f'<tr><td class="clk">{subst(a)}</td><td>{subst(b)}</td>'
                   f'<td class="len">{c}</td></tr>' for a, b, c in M.MATERIALS)
    def notes_for(sl):
        return "".join(f'<div class="note"><b>{t}</b>{b}</div>' for t, b in sl)
    notes_a = notes_for(M.PLAN_NOTES[:1])
    notes_b = notes_for(M.PLAN_NOTES[1:])

    p1 = f"""<div class="page">
{R.masthead(M_KICK, "PLAN")}
{kit_head("Lesson |Plan", "Monday 14.09.2026 &#183; two and a half sessions &#183; level A2")}
<h3 class="kit-h">The day</h3>
<table class="tt">{tt}</table>
<h3 class="kit-h sp">By the end of the day students can</h3>
<ul class="kit">{aims}</ul>
<h3 class="kit-h sp">On the table before you start</h3>
<table class="tt">{mats}</table>
<h3 class="kit-h sp">Notes for the teacher</h3>
{notes_a}
{R.foot("Lesson plan", M_FOOT, "Plan &#183; p. 1")}
</div>"""

    p2 = f"""<div class="page">
{R.masthead(M_KICK, "PLAN")}
<h3 class="kit-h">Session 1 &#183; 11.00 &#8211; 11.45 &#183; revision and Past Simple</h3>
{stage_table(M.STAGE1)}
<h3 class="kit-h sp">Session 2 &#183; 12.00 &#8211; 13.35 &#183; preparing the presentation</h3>
{stage_table(M.STAGE2)}
{R.foot("Lesson plan", M_FOOT, "Plan &#183; p. 2")}
</div>"""

    p3 = f"""<div class="page">
{R.masthead(M_KICK, "PLAN")}
<h3 class="kit-h">Session 3 &#183; 14.05 &#8211; 15.40 &#183; plenary, presentations, awards</h3>
{stage_table(M.STAGE3)}
<h3 class="kit-h sp">Notes for the teacher</h3>
{notes_b}
<div class="note"><b>The awards, in order</b>
Read the certificate out, say the one thing the person did that earned it, then hand it
over. One or two &#8220;most active&#8221; per group as agreed, then the debate winners, then
the winners of the game. Keep it to ninety seconds a name &#8211; the applause is the reward,
the paper is the souvenir.</div>
<div class="note" style="border-left-color:#1b2a4a;background:rgba(27,42,74,.055)">
<b>Closing the intensive</b>
Go back to the board and read out three of the words the group wrote at 11.40. Ask one
question and stop: <i>after today, would you keep your word, or change it?</i> Take three
answers. Do not sum up for them.</div>
{R.foot("Lesson plan", M_FOOT, "Plan &#183; p. 3")}
</div>"""
    return R.head("Monday 14.09 &#8211; lesson plan") + p1 + p2 + p3 + "</body></html>"


def listening_sheet():
    rhs, key = shuffled_rhs(M.L_WORDS)
    M._lwords_key = key
    t1 = R.match_body(M.L_WORDS, rhs)

    t2 = '<ol class="items two">' + "".join(
        f'<li><div class="tickrow"><span class="tickbox"></span>'
        f'<span>{t}</span></div></li>' for t, _ in M.L_TICK) + "</ol>"

    t3 = R.tf_body(M.L_TF)

    nums_rhs, nums_key = shuffled_rhs(M.L_NUMBERS)
    M._lnums_key = nums_key
    t4 = ('<div class="match"><ol class="items">'
          + "".join(f'<li><span class="matchbox"></span><b>{n}</b></li>' for n, _ in M.L_NUMBERS)
          + '</ol><ol class="items rhs">'
          + "".join(f"<li>{f}</li>" for f in nums_rhs) + "</ol></div>")

    t5 = '<ol class="items">' + "".join(
        f'<li>{q}<span class="answer-rule"></span>'
        f'<span class="answer-rule"></span></li>' for q in M.L_AFTER) + "</ol>"

    p1 = f"""<div class="page">
{R.masthead(M_KICK, "LISTEN")}
{kit_head("The Queen Who |Said No", "Listening &#183; A2 &#183; you will hear the talk twice")}
<div class="tasks">
{R.task(1, "Before you listen", "Match the word to its meaning. Write a&#8211;h.", t1)}
{R.task(2, "First listening", "Tick the FIVE things the talk speaks about.", t2, navy=True)}
{R.task(3, "Second listening", "Circle T, F or NG.", t3)}
</div>
{R.foot("Listening", M_FOOT, "Listening &#183; p. 1")}
</div>"""

    p2 = f"""<div class="page">
{R.masthead(M_KICK, "LISTEN")}
<div class="tasks">
{R.task(4, "The numbers", "Write a&#8211;g next to each number.", t4, navy=True)}
{R.task(5, "After you listen", "Talk in your team, then write.", t5)}
</div>
{R.foot("Listening", M_FOOT, "Listening &#183; p. 2")}
</div>"""
    return R.head("Listening &#8211; The Queen Who Said No") + p1 + p2 + "</body></html>"


def audio_script():
    paras = "".join(
        f'<p><span class="pn">{i}</span>{t}'
        + ('  <span class="pause">||</span>' if pause else '')
        + "</p>" for i, (t, pause) in enumerate(M.SCRIPT, 1))

    def letters(key):
        return " &#183; ".join(f'{i} <b>{chr(97 + k)}</b>' for i, k in enumerate(key, 1))

    k1 = letters(M._lwords_key)
    k2 = " &#183; ".join(f'{i} <b>{"tick" if t else "&#8211;"}</b>'
                         for i, (_, t) in enumerate(M.L_TICK, 1))
    k3 = " &#183; ".join(f'{i}<span class="key-tag">{a}</span>'
                         for i, (_, a) in enumerate(M.L_TF, 1))
    k4 = letters(M._lnums_key)

    p1 = f"""<div class="page">
{R.masthead(M_KICK, "AUDIO")}
{kit_head("Audio |Script", "Read aloud by the teacher &#183; for the teacher only")}
<p class="script-meta">{M.SCRIPT_META}</p>
<section class="script">{paras}</section>
<div class="note" style="margin-top:4mm"><b>How to read it</b>
First reading: normal speed, no stopping, students only tick task 2. Second reading: slow
down a little and pause where you see <span class="pause">||</span>. If the group is weak,
read paragraph 7 a third time on its own &#8211; the quotation is the hardest line on the sheet.</div>
{R.foot("Audio script", M_FOOT, "Audio &#183; p. 1")}
</div>"""

    p2 = f"""<div class="page">
{R.masthead(M_KICK, "AUDIO")}
<h3 class="kit-h">Listening sheet &#183; answer key</h3>
<div class="key-block">
<p style="margin:0 0 1.8mm;font-size:9.9pt"><span class="key-tag">1 BEFORE YOU LISTEN</span> {k1}</p>
<p style="margin:0 0 1.8mm;font-size:9.9pt"><span class="key-tag">2 FIRST LISTENING</span> {k2}</p>
<p style="margin:0 0 1.8mm;font-size:9.9pt"><span class="key-tag">3 SECOND LISTENING</span> {k3}</p>
<p style="margin:0 0 1.8mm;font-size:9.9pt"><span class="key-tag">4 THE NUMBERS</span> {k4}</p>
<p style="margin:0;font-size:9.9pt"><span class="key-tag">5 AFTER</span>
Open answers. Item 3 is the one to push on: the talk really does leave out everything
difficult, and noticing that is the skill the afternoon needs.</p>
</div>
<div class="note" style="margin-top:4mm"><b>Why item 7 of task 3 is Not Given</b>
The talk says Shakespeare wrote his plays in her time. It never says she met him or wrote
with him. Students who answer F are reading the world, not the text; students who answer T
are reading a film. Both are worth thirty seconds of discussion.</div>
<div class="note"><b>If you would rather not read it yourself</b>
The script is plain text and works in any text-to-speech tool; a British English voice at
0.9 speed is close to the timing above. There is no recording in this pack.</div>
<h3 class="kit-h sp">Three more ways to use the same script</h3>
<div class="note"><b>1 &#183; Running dictation &#183; 8 minutes</b>
Cut the script into its ten paragraphs and tape them to the walls. One student in each pair
runs, reads, comes back and dictates; the other writes. Swap after every paragraph. Then they
compare their text with the real one and count the differences. It is loud, and it is the
fastest reading-and-spelling exercise there is.</div>
<div class="note"><b>2 &#183; Shadowing paragraph 7 &#183; 4 minutes</b>
Read the Tilbury paragraph one line at a time; the class repeats it back at the same speed
and with the same stress. Then one volunteer stands up and says the quotation alone. Nobody
forgets a sentence they have said standing up.</div>
<div class="note"><b>3 &#183; Retell relay &#183; 6 minutes</b>
Books closed. Student 1 gives one sentence of the life, in the Past Simple. Student 2 gives
the next. Any wrong tense and the chain goes back to the start. Three complete chains and
the group owns the story.</div>
<h3 class="kit-h sp">Where the facts come from</h3>
<div class="note" style="border-left-color:#1b2a4a;background:rgba(27,42,74,.055)">
<b>Checked on 13.09.2026</b>
Every date, name and number in the script is in the English Wikipedia article
&#8220;Elizabeth I&#8221;: born 7 September 1533 at Greenwich Palace; Anne Boleyn beheaded
19 May 1536; tutored by Roger Ascham; sent to the Tower on 18 March 1554 and moved to
Woodstock on 22 May; queen from 17 November 1558, crowned 15 January 1559; the Armada
defeated in 1588; Shakespeare and Marlowe writing in her reign; died 24 March 1603 at
Richmond Palace; succeeded by James VI of Scotland. The Tilbury quotation is from the
article &#8220;Speech to the Troops at Tilbury&#8221;, 9 August 1588 &#8211; accepted as genuine by
most historians, doubted by a minority. The class text&#8217;s &#8220;14 March&#8221; and
&#8220;45 years&#8221; are wrong and are corrected here.</div>
{R.foot("Audio script", M_FOOT, "Audio &#183; p. 2")}
</div>"""
    return R.head("Audio script &#8211; for the teacher") + p1 + p2 + "</body></html>"


def great_person_sheet():
    t1 = ('<ol class="crit">' + "".join(
        f'<li><span class="tickbox"></span><span>{c}</span></li>' for c in M.CRITERIA)
        + '</ol><div style="height:2.4mm"></div>'
        '<table class="evid"><tr><th style="width:34%">Our team&#8217;s three criteria</th>'
        '<th>Why this one and not another?</th></tr>'
        + "".join('<tr><td></td><td></td></tr>' for _ in range(3)) + "</table>")

    t2 = ('<table class="evid"><tr><th class="num">#</th><th style="width:26%">Criterion</th>'
          '<th>What Elizabeth actually did</th><th style="width:15%">Year</th></tr>'
          + "".join(f'<tr><td class="num">{i}</td><td></td><td></td><td></td></tr>'
                    for i in (1, 2, 3)) + "</table>")

    rate = ('<span class="rate">1 2 3<span></span><span></span><span></span></span>')
    t3 = '<ol class="gtest">' + "".join(
        f'<li>{rate}{what}<span class="so">{so}</span></li>'
        for what, so in M.GREATNESS_TEST) + "</ol>"

    t4 = ('<p style="margin:0 0 2mm;font-size:10.2pt">Motion: <b>&#8220;'
          + M.DEBATE_MOTION + '&#8221;</b> Write three arguments on each side. '
          'You will need the right-hand column when you present.</p>'
          '<table class="evid"><tr><th style="width:50%">FOR &#8211; because she &#8230;</th>'
          '<th>AGAINST &#8211; but she &#8230;</th></tr>'
          + "".join('<tr><td></td><td></td></tr>' for _ in range(3)) + "</table>")

    p1 = f"""<div class="page">
{R.masthead(M_KICK, "GREAT")}
{kit_head("What Makes a |Great Person?", "Session 2 &#183; build your criteria, then test them")}
<div class="tasks roomy">
{R.task(1, "Your criteria", "Tick five alone. Then agree on three as a team.", t1)}
{R.task(2, "Evidence hunt", "No year, no evidence.", t2, navy=True)}
</div>
{R.foot("Great Person", M_FOOT, "Great Person &#183; p. 1")}
</div>"""

    p2 = f"""<div class="page">
{R.masthead(M_KICK, "GREAT")}
<div class="tasks roomy">
{R.task(3, "The greatness test", "Four things she really did. Score each 1&#8211;3 against YOUR criteria.", t3)}
{R.task(4, "Both sides", "A team that cannot argue the other side has not understood its own.", t4, navy=True)}
</div>
<div class="note"><b>Where the hard facts in task 3 come from</b>{M.TEACHER_EVIDENCE}</div>
{R.foot("Great Person", M_FOOT, "Great Person &#183; p. 2")}
</div>"""
    return R.head("What makes a great person?") + p1 + p2 + "</body></html>"


def presentation_kit():
    roles = "<table class=\"roles\">" + "".join(
        f'<tr><td class="no">{n}</td><td class="rn">{role}</td><td class="tm">{tm}</td>'
        f'<td>{what}</td><td class="nm"><i>name</i></td></tr>'
        for n, role, tm, what in M.ROLES) + "</table>"

    frames = ('<div class="frames">' + "".join(
        f'<div class="frame-box"><h4>{t}</h4><ul>'
        + "".join(f"<li>{x}</li>" for x in xs) + "</ul></div>"
        for t, xs in M.FRAMES) + "</div>")

    check = '<ol class="check">' + "".join(
        f'<li><span class="tickbox"></span><span>{c}</span></li>' for c in M.CHECKLIST) + "</ol>"

    fixlist = ('<table class="evid"><tr><th>After rehearsal 1 &#8211; three things we change '
               '(not four)</th></tr>'
               + "".join('<tr><td></td></tr>' for _ in range(3)) + "</table>")

    p1 = f"""<div class="page">
{R.masthead(M_KICK, "STAGE")}
{kit_head("Ten Minutes |on Stage", "Six roles &#183; everybody speaks &#183; nobody runs over")}
<div class="tasks">
{R.task(1, "Who does what", "Write a real name in the last column.", roles)}
{R.task(2, "Rehearsal checklist", "One student holds this and ticks during the run.", check, navy=True)}
{R.task(3, "The fix list", "Three things. Three.", fixlist)}
</div>
{R.foot("Presentation kit", M_FOOT, "Stage &#183; p. 1")}
</div>"""

    p2 = f"""<div class="page">
{R.masthead(M_KICK, "STAGE")}
<h3 class="kit-h">Sentence frames &#8211; steal these</h3>
{frames}
<div class="note"><b>The one rule about the Past Simple on stage</b>
Everything that happened before today is Past Simple: <i>she was</i>, <i>she became</i>,
<i>she did not marry</i>, <i>did she marry?</i> Everything you think <i>now</i> is present:
<i>we think</i>, <i>this shows</i>, <i>our answer is</i>. Mixing the two is the single
mistake the room will hear.</div>
<div class="note" style="border-left-color:#1b2a4a;background:rgba(27,42,74,.055)">
<b>What a ten-minute talk is not</b>
It is not a Wikipedia page read out loud. The story of the life is two minutes of the ten.
The other eight are your answer to the question, and the evidence for it.</div>
{R.foot("Presentation kit", M_FOOT, "Stage &#183; p. 2")}
</div>"""
    return R.head("Presentation kit &#8211; ten minutes on stage") + p1 + p2 + "</body></html>"


def feedback_sheet():
    def card():
        sc = "".join(
            f'<div class="sc"><span>{t}</span>'
            '<span class="dots"><span></span><span></span><span></span>'
            '<span></span><span></span></span></div>' for t in M.FB_SCORES)
        op = "".join(f'<div class="open"><b>{t}</b>'
                     + "".join('<span class="rule"></span>' for _ in range(n))
                     + "</div>" for t, n in M.FB_OPEN)
        return (f'<div class="fbcard"><h4>Audience card</h4>'
                f'<div class="team">Team <span class="ln"></span> Their person <span class="ln"></span></div>'
                f'{sc}{op}</div>')

    slips = '<div class="slips">' + "".join(
        f'<div class="slip"><h5>{t}</h5><p>{d}</p><span class="rule"></span></div>'
        for t, d in M.VOTES) + "</div>"

    p1 = f"""<div class="page">
{R.masthead(M_KICK, "VOTE")}
{kit_head("Audience |Cards", "Cut into four &#183; one card per team you watch")}
<div class="cards">{card()}{card()}{card()}{card()}</div>
<h3 class="kit-h sp">Your three votes &#8211; tear off and post at 15.20</h3>
{slips}
{R.foot("Audience cards", M_FOOT, "Vote &#183; p. 1")}
</div>"""
    return R.head("Audience cards and voting slips") + p1 + "</body></html>"


def certificates():
    def cert(title, why, grp):
        return f"""<div class="cert">{R.UNION_JACK}
<h2>{title}</h2>
<div class="why">{why}</div>
<div class="awarded">Awarded to</div>
<div class="name"></div>
<div class="grp">{grp}</div>
<div class="sig"><div>Teacher</div><div>Date</div></div>
<div class="foot-line">{M.CERT_FOOT}</div>
</div>"""

    pages = []
    for i in range(0, len(M.CERTS), 2):
        cut = ('<div class="cutline"><span>&#9986; cut here</span></div>')
        body = cut.join(cert(*c) for c in M.CERTS[i:i + 2])
        pages.append(f'<div class="page" style="padding-top:10mm">{body}</div>')
    return R.head("Certificates") + "".join(pages) + "</body></html>"


# ----------------------------------------------------------------- rendering
SHEETS = []


def write_html():
    SHEET.update(number_sheets())
    """Order matters: person sheets fix the matching keys, the mixed sheet fixes
    the numbers key, and the answer key reads both."""
    os.makedirs(OUT_HTML, exist_ok=True)
    seq = ([(d["slug"], person_sheet(d)) for d in C.PEOPLE]
           + [("mixed-round", mixed_sheet()), ("answer-key", key_sheet())]
           + [(f"grammar-{d['slug']}", grammar_sheet(d)) for d in G.GRAMMAR_PEOPLE]
           + [("grammar-mixed", grammar_mixed()), ("grammar-answer-key", grammar_key())]
           + [("monday-lesson-plan", lesson_plan()),
              ("monday-listening", listening_sheet()),
              ("monday-audio-script", audio_script()),
              ("monday-great-person", great_person_sheet()),
              ("monday-presentation-kit", presentation_kit()),
              ("monday-audience-cards", feedback_sheet()),
              ("monday-certificates", certificates())])
    SHEETS[:] = [(f"{i:02d}-{name}", html) for i, (name, html) in enumerate(seq, 1)]
    # one file with every sheet, for printing the whole pack in a single job
    body = "".join(h[h.index("<body>") + 6: h.index("</body>")] for _, h in SHEETS)
    SHEETS.insert(0, ("00-complete-pack",
                      R.head("Interesting People &#8211; complete A2 pack") + body + "</body></html>"))
    for name, html in list(SHEETS):
        open(os.path.join(OUT_HTML, name + ".html"), "w", encoding="utf-8").write(html)
        bw = html.replace('<link rel="stylesheet" href="style.css">',
                          '<link rel="stylesheet" href="style.css">\n'
                          '<link rel="stylesheet" href="print-bw.css">')
        assert 'print-bw.css' in bw, "colour sheet lost its stylesheet link"
        open(os.path.join(OUT_HTML, name + "-bw.html"), "w", encoding="utf-8").write(bw)
        print(f"  html  {name}.html  + -bw  ({len(html)//1024} KB)")
    return SHEETS


def render_pdfs(names, out_dir=None, suffix=""):
    """Print each sheet to A4 and report any page whose content overflows."""
    from playwright.sync_api import sync_playwright
    out_dir = out_dir or OUT_PDF
    os.makedirs(out_dir, exist_ok=True)
    # This image ships Chromium at a pinned path; never run `playwright install`.
    chrome = os.environ.get("CHROME_BIN", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    launch = {"executable_path": chrome} if os.path.exists(chrome) else {}
    problems = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(**launch)
        page = browser.new_page()
        for name in names:
            src = os.path.join(OUT_HTML, name + suffix + ".html")
            page.goto("file://" + src, wait_until="networkidle")
            page.wait_for_timeout(400)
            over = page.evaluate("""() => [...document.querySelectorAll('.page')].map((p, i) => ({
                i: i + 1, over: Math.round(p.scrollHeight - p.clientHeight) }))""")
            for o in over:
                if o["over"] > 1:
                    problems.append((name + suffix, o["i"], o["over"]))
            dst = os.path.join(out_dir, name + ".pdf")
            page.pdf(path=dst, format="A4", print_background=True,
                     margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            pages = len(over)
            print(f"  pdf   {name}{suffix}.pdf  ({pages} page{'s' if pages != 1 else ''}, "
                  f"{os.path.getsize(dst)//1024} KB)")
        browser.close()
    return problems


def prune(names):
    """Delete output left behind by an earlier running order.

    Sheet numbers are derived, so adding a person renames every file after them.
    The old files stay on disk unless somebody removes them, and a teacher who
    opens the folder then sees two answer keys with different numbers. Only
    files this build knows how to produce are kept.
    """
    keep = {
        OUT_HTML: {b + e for b in names for e in (".html", "-bw.html")}
                  | {"style.css", "print-bw.css", "fonts.css"},
        OUT_PDF:  {b + ".pdf" for b in names},
        OUT_BW:   {b + ".pdf" for b in names},
        os.path.join(ROOT, "materials", "docx"):
                  {b + ".docx" for b in names if not b.startswith("00-")},
    }
    gone = []
    for d, ok in keep.items():
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.startswith(".") or f in ok:
                continue
            os.remove(os.path.join(d, f))
            gone.append(os.path.join(os.path.basename(d), f))
    if gone:
        print("\n  removed output from an earlier running order:")
        for g in gone:
            print(f"    - {g}")
    return gone


if __name__ == "__main__":
    print("Building the Interesting People A2 pack\n")
    sheets = write_html()
    prune([n for n, _ in sheets])
    if "--html" in sys.argv:
        sys.exit(0)
    print()
    names = [n for n, _ in sheets]
    problems = render_pdfs(names)
    print()
    problems += render_pdfs(names, OUT_BW, "-bw")
    if problems:
        print("\n!! CONTENT OVERFLOWS THE PAGE:")
        for n, i, o in problems:
            print(f"   {n}.pdf page {i}: {o}px past the bottom")
        sys.exit(1)
    print("\nAll pages fit inside A4. Done.")

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
<div class="key-grid">{''.join(blocks[2:])}</div>
{R.foot("Grammar Key", FOOT_M, f"Sheet {SHEET['GKEY']} &#183; p. 1")}
</div>"""
    p2 = f"""<div class="page">
{R.masthead("Grammar Key &#183; Irregular verbs &amp; notes", SHEET["GKEY"])}
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
           + [("grammar-mixed", grammar_mixed()), ("grammar-answer-key", grammar_key())])
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


if __name__ == "__main__":
    print("Building the Interesting People A2 pack\n")
    sheets = write_html()
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

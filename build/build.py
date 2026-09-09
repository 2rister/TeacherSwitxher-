# -*- coding: utf-8 -*-
"""Build the printable 'Interesting People' A2 pack.

    python3 build/build.py            # write HTML + render PDFs
    python3 build/build.py --html     # write HTML only

Every sheet is one or more .page divs sized to A4; Chromium prints them at
exactly 210x297 mm with no scaling. After rendering, each page is measured and
any content overflow is reported, so a layout can never silently lose a line.
"""
import os, random, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_HTML = os.path.join(ROOT, "materials", "html")
OUT_PDF = os.path.join(ROOT, "materials", "pdf")
OUT_BW = os.path.join(ROOT, "materials", "pdf-bw")
sys.path.insert(0, HERE)

import content as C
import render as R

KICKER = "Interesting People &#183; Reading &amp; Facts &#183; Level A2"
FOOT_L = "Interesting People &#183; A2"
FOOT_M = "Ideas &#183; People &#183; Arguments"

rnd = random.Random(20260909)          # fixed seed => identical output every build


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
{R.task(5, "Back to the board", "From the game &#8211; texts face down!",
        R.jeopardy_body(d['jeopardy'], title=f"{d['name']} on the Jeopardy board"))}
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
{R.masthead("The Mixed Round &#183; Newton &#183; Lennon &#183; Diana", "IV")}
<div class="tasks">
{R.task(1, "Who is it?", "N = Newton &#183; L = Lennon &#183; D = Diana",
        f'<ol class="items">{who}</ol>')}
{R.task(2, "Put them in order", "1 = oldest, 5 = youngest. Use the year of birth.",
        f'<ol class="items">{tl}</ol>', navy=True)}
{R.task(3, "What do these numbers mean?", "Write a&#8211;h next to each number.",
        f'<div class="match"><ol class="items">{nums_l}</ol>'
        f'<ol class="items rhs">{nums_r}</ol></div>')}
</div>
{R.foot(FOOT_L, FOOT_M, "Sheet IV &#183; p. 1")}
</div>"""

    p2 = f"""<div class="page">
{R.masthead("Final Round &#183; Speak &#183; Reason &#183; Persuade &#183; Respect", "IV")}
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
{R.foot(FOOT_L, FOOT_M, "Sheet IV &#183; p. 2")}
</div>"""
    return R.head("The Mixed Round &#8211; A2") + p1 + p2 + "</body></html>"


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
<h3>Sheet IV &#183; The Mixed Round</h3>
<p style="margin:0 0 1.4mm;font-size:9.9pt"><span class="key-tag">1 WHO IS IT?</span> {who}</p>
<p style="margin:0 0 1.4mm;font-size:9.9pt"><span class="key-tag">2 ORDER</span> {tl}</p>
<p style="margin:0 0 1.4mm;font-size:9.4pt;color:#5a4a38">Numbers to write in the boxes,
top to bottom as printed: {tl_num}</p>
<p style="margin:0 0 1.4mm;font-size:9.9pt"><span class="key-tag">3 NUMBERS</span> {nums}</p>
<p style="margin:0;font-size:9.9pt"><span class="key-tag">4 FINAL JEOPARDY</span>
No single correct answer. Accept any person if the student gives a reason
<i>and</i> an example from the text.</p>
</div>""")

    notes = "".join(f"<div class='note'><b>{t}</b>{b}</div>" for t, b in C.TEACHER_NOTES)

    p1 = f"""<div class="page">
{R.masthead("Answer Key &#183; For the teacher", "V")}
<div class="key-grid">{''.join(blocks[:2])}</div>
<div style="height:3mm"></div>
<div class="key-grid">{''.join(blocks[2:])}</div>
{R.foot("Answer Key", FOOT_M, "Sheet V &#183; p. 1")}
</div>"""

    p2 = f"""<div class="page">
{R.masthead("Teacher&#8217;s Notes &#183; Checks &amp; Corrections", "V")}
<h2 style="font-family:Cinzel,serif;font-size:12pt;letter-spacing:.16em;color:#1b2a4a;
           margin:0 0 3mm;text-transform:uppercase">Before you print</h2>
{notes}
<div class="note" style="border-left-color:#1b2a4a;background:rgba(27,42,74,.055)">
<b>How the pack maps onto the game</b>
Every item in tasks 1Every item in tasks 1&#8211;5 on Sheets I&#8211;III#8211;5 on Sheets I&#8211;III, and every item on Sheet IV, is built on a fact that
appears on the Jeopardy board, so the handouts and the game test the same knowledge. Suggested order:
read the sheet &#8594; do the exercises &#8594; play the game with the texts face down.</div>
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
{R.foot("Answer Key", FOOT_M, "Sheet V &#183; p. 2")}
</div>"""
    return R.head("Answer Key &#8211; A2") + p1 + p2 + "</body></html>"


# ----------------------------------------------------------------- rendering
SHEETS = []


def write_html():
    """Order matters: person sheets fix the matching keys, the mixed sheet fixes
    the numbers key, and the answer key reads both."""
    os.makedirs(OUT_HTML, exist_ok=True)
    SHEETS[:] = [(f"0{i+1}-{d['slug']}", person_sheet(d)) for i, d in enumerate(C.PEOPLE)]
    SHEETS.append(("04-mixed-round", mixed_sheet()))
    SHEETS.append(("05-answer-key", key_sheet()))
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

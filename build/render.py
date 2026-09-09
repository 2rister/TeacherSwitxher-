# -*- coding: utf-8 -*-
"""HTML fragments shared by every sheet in the pack."""

UNION_JACK = """<svg class="flag" viewBox="0 0 60 30" xmlns="http://www.w3.org/2000/svg">
<clipPath id="uj"><path d="M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z"/></clipPath>
<rect width="60" height="30" fill="#0d2a63"/>
<path d="M0,0 L60,30 M60,0 L0,30" stroke="#f4ecd8" stroke-width="6"/>
<path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#uj)" stroke="#9d2226" stroke-width="4"/>
<path d="M30,0 v30 M0,15 h60" stroke="#f4ecd8" stroke-width="10"/>
<path d="M30,0 v30 M0,15 h60" stroke="#9d2226" stroke-width="6"/></svg>"""


def head(title):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="style.css">
</head><body>
"""


def masthead(kicker, sheet_no):
    return f"""<header class="masthead">{UNION_JACK}
<div class="masthead-mid">
  <div class="masthead-kicker">{kicker}</div>
  <div class="masthead-rule"></div>
</div>
<div class="sheet-no">{sheet_no}</div>
</header>"""


def foot(left, mid, page):
    return (f'<footer class="foot"><span>{left}</span>'
            f'<span class="mid">{mid}</span><span class="pg">{page}</span></footer>')


def task(no, title, hint, body, navy=False):
    cls = "task navy" if navy else "task"
    hint = f'<span class="task-hint">{hint}</span>' if hint else ""
    return (f'<section class="{cls}"><div class="task-head">'
            f'<span class="task-no">{no}</span>'
            f'<span class="task-title">{title}</span>{hint}</div>'
            f'<div class="task-body">{body}</div></section>')


# ------------------------------------------------------------- task builders
def tf_body(items):
    rows = "".join(
        f'<li><div class="tf-row"><span class="stmt">{s}</span>'
        f'<span class="tf-opts"><span>T</span><span>F</span><span>NG</span></span>'
        f'</div></li>' for s, _ in items)
    return f'<ol class="items">{rows}</ol>'


def gap_body(bank, gaps):
    chips = "".join(f"<span>{w}</span>" for w in bank)
    rows = "".join(f"<li>{s}</li>" for s, _ in gaps)
    return f'<div class="bank">{chips}</div><ol class="items">{rows}</ol>'


def q_body(qs):
    rows = "".join(f'<li>{q}<span class="answer-rule"></span>'
                   f'<span class="answer-rule"></span></li>' for q, _ in qs)
    return f'<ol class="items">{rows}</ol>'


def match_body(pairs, shuffled_rhs):
    lhs = "".join(f'<li><span class="matchbox"></span>{a}</li>' for a, _ in pairs)
    rhs = "".join(f"<li>{b}</li>" for b in shuffled_rhs)
    return (f'<div class="match"><ol class="items">{lhs}</ol>'
            f'<ol class="items rhs">{rhs}</ol></div>')


def jeopardy_body(rows, title="Back to the board"):
    out = "".join(f'<div class="jeo-row"><span class="jeo-pts">{p}</span>'
                  f'<span>{q}</span></div>' for p, q, _ in rows)
    return f'<div class="jeo"><div class="jeo-title">{title}</div>{out}</div>'


def glossary(items):
    rows = "".join(f"<div><b>{w}</b> &#8211; <span>{d}</span></div>" for w, d in items)
    return ('<section class="glossary"><div class="glossary-head">Words to know</div>'
            f'<div class="glossary-body">{rows}</div></section>')

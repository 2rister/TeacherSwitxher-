#!/usr/bin/env python3
"""Собирает печатные версии теста «Простейшие»: вариант для учеников и ключ учителя.

Порядок работы:
    python3 build.py            # -> test.html, answers.html, test.pdf, answers.pdf

PDF печатается headless-Chromium'ом (в этом окружении он лежит в /opt/pw-browsers).
Если Chromium не найден, HTML всё равно будет собран — его можно распечатать из браузера.
"""

import base64
import json
import mimetypes
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LETTERS = ["А", "Б", "В", "Г", "Д", "Е"]

CHROMIUM_CANDIDATES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
]


def data_uri(rel_path):
    path = os.path.join(HERE, rel_path)
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as fh:
        return "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode("ascii"))


CSS = """
@page { size: A4; margin: 14mm 12mm 12mm 12mm; }

:root {
  --ink: #111;
  --muted: #555;
  --rule: #bbb;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: "DejaVu Sans", "Liberation Sans", Arial, sans-serif;
  font-size: 9.6pt;
  line-height: 1.35;
  color: var(--ink);
  background: #fff;
}

header.sheet {
  border-bottom: 2px solid var(--ink);
  padding-bottom: 5mm;
  margin-bottom: 5mm;
}

h1 {
  font-size: 15pt;
  margin: 0 0 1mm;
  letter-spacing: .2px;
}

.subtitle {
  font-size: 9.5pt;
  color: var(--muted);
  margin: 0 0 4mm;
}

.fields {
  display: flex;
  gap: 6mm;
  font-size: 9.5pt;
}

.fields span { flex: 1; border-bottom: 1px solid var(--ink); padding-bottom: 1mm; }
.fields span.short { flex: 0 0 32mm; }

.hint {
  font-size: 8.5pt;
  color: var(--muted);
  margin: 3mm 0 4mm;
  padding: 2mm 3mm;
  border-left: 2px solid var(--rule);
}

.questions { column-count: 2; column-gap: 8mm; }

.q {
  break-inside: avoid;
  page-break-inside: avoid;
  margin: 0 0 4.5mm;
  padding-bottom: 3mm;
  border-bottom: 1px dotted var(--rule);
}

.q:last-child { border-bottom: none; }

.q .stem {
  display: flex;
  gap: 2mm;
  font-weight: 600;
  margin-bottom: 1.6mm;
}

.q .num { flex: 0 0 auto; }

.q figure { margin: 1.5mm 0 2mm; text-align: center; }

.q img {
  max-width: 100%;
  max-height: 42mm;
  border: 1px solid var(--rule);
}

ol.opts { list-style: none; margin: 0; padding: 0; }

ol.opts li {
  display: flex;
  gap: 1.8mm;
  padding: .4mm 0;
}

ol.opts .letter {
  flex: 0 0 auto;
  width: 4.6mm;
  height: 4.6mm;
  line-height: 4.4mm;
  text-align: center;
  border: 1px solid var(--ink);
  border-radius: 50%;
  font-size: 8pt;
}

ol.opts .letter.right { background: var(--ink); color: #fff; }

footer.sheet {
  margin-top: 5mm;
  padding-top: 2mm;
  border-top: 1px solid var(--rule);
  font-size: 8pt;
  color: var(--muted);
  column-span: all;
}

/* --- ключ --- */
table.key { width: 100%; border-collapse: collapse; font-size: 10pt; }
table.key th, table.key td { border: 1px solid var(--rule); padding: 1.6mm 2mm; text-align: left; }
table.key th { background: #f2f2f2; font-size: 9pt; }
table.key td.n { width: 10mm; text-align: center; font-weight: 600; }
table.key td.a { width: 12mm; text-align: center; font-weight: 600; }
.key-wrap { column-count: 2; column-gap: 8mm; }
.key-wrap table { break-inside: auto; }
.notes { margin-top: 5mm; font-size: 8.7pt; column-span: all; }
.notes h2 { font-size: 10.5pt; margin: 0 0 2mm; }
.notes li { margin-bottom: 1.5mm; }
"""


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_test(data, embed=True):
    parts = []
    for q in data["questions"]:
        opts = []
        for i, opt in enumerate(q["options"]):
            opts.append(
                '<li><span class="letter">%s</span><span>%s</span></li>'
                % (LETTERS[i], esc(opt))
            )
        img = ""
        if q.get("image"):
            src = data_uri(q["image"]) if embed else q["image"]
            img = '<figure><img src="%s" alt=""></figure>' % src
        parts.append(
            '<article class="q">'
            '<div class="stem"><span class="num">%d.</span><span>%s</span></div>'
            "%s"
            '<ol class="opts">%s</ol>'
            "</article>" % (q["n"], esc(q["text"]), img, "".join(opts))
        )

    return """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<title>%s — тест</title><style>%s</style></head>
<body>
<header class="sheet">
  <h1>%s</h1>
  <p class="subtitle">%s</p>
  <div class="fields">
    <span>Фамилия, имя _______________________________________</span>
    <span class="short">Класс ___________</span>
    <span class="short">Дата ___________</span>
  </div>
</header>
<p class="hint">В каждом задании выберите <b>один</b> правильный ответ и обведите его букву.
Всего %d заданий, максимум %d баллов.</p>
<div class="questions">%s</div>
<footer class="sheet">%s</footer>
</body></html>""" % (
        esc(data["title"]),
        CSS,
        esc(data["title"]),
        esc(data["subtitle"]),
        len(data["questions"]),
        len(data["questions"]),
        "".join(parts),
        esc(data["source"]),
    )


def render_answers(data, embed=True):
    qs = data["questions"]
    half = (len(qs) + 1) // 2
    chunks = [qs[:half], qs[half:]]
    tables = []
    for chunk in chunks:
        rows = []
        for q in chunk:
            mark = " *" if q.get("note") else ""
            rows.append(
                '<tr><td class="n">%d</td><td class="a">%s</td><td>%s%s</td></tr>'
                % (q["n"], LETTERS[q["answer"]], esc(q["options"][q["answer"]]), mark)
            )
        tables.append(
            '<table class="key"><thead><tr><th>№</th><th>Отв.</th>'
            "<th>Правильный ответ</th></tr></thead><tbody>%s</tbody></table>"
            % "".join(rows)
        )

    notes = [q for q in qs if q.get("note")]
    notes_html = ""
    if notes:
        items = "".join(
            "<li><b>Вопрос %d.</b> %s</li>" % (q["n"], esc(q["note"])) for q in notes
        )
        notes_html = (
            '<div class="notes"><h2>* Замечания к формулировкам</h2>'
            "<ul>%s</ul></div>" % items
        )

    return """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<title>%s — ключ</title><style>%s</style></head>
<body>
<header class="sheet">
  <h1>%s — ключ для учителя</h1>
  <p class="subtitle">%s · лист не выдавать ученикам</p>
</header>
<div class="key-wrap">%s</div>
%s
<footer class="sheet">%s</footer>
</body></html>""" % (
        esc(data["title"]),
        CSS,
        esc(data["title"]),
        esc(data["subtitle"]),
        "".join(tables),
        notes_html,
        esc(data["source"]),
    )


def find_chromium():
    for path in CHROMIUM_CANDIDATES:
        if os.path.exists(path):
            return path
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def to_pdf(html_path, pdf_path):
    chrome = find_chromium()
    if not chrome:
        print("Chromium не найден — PDF пропущен, печатайте %s из браузера" % html_path)
        return False
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--print-to-pdf=" + pdf_path,
        "file://" + html_path,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not os.path.exists(pdf_path):
        print(res.stderr[-2000:], file=sys.stderr)
        return False
    return True


def main():
    with open(os.path.join(HERE, "questions.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    for name, html in (
        ("test", render_test(data, embed=False)),
        ("answers", render_answers(data, embed=False)),
    ):
        html_path = os.path.join(HERE, name + ".html")
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(html)
        pdf_path = os.path.join(HERE, name + ".pdf")
        ok = to_pdf(html_path, pdf_path)
        print("%-8s html: %s%s" % (name, html_path, "  pdf: " + pdf_path if ok else ""))


if __name__ == "__main__":
    main()

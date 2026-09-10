# -*- coding: utf-8 -*-
"""End-to-end check with a real office suite:  python3 build/check_with_libreoffice.py

verify.py reads the files the way I wrote them. This opens them the way a
teacher will, through LibreOffice, and asks the application itself what it
found. It is slower (LibreOffice takes ~20 s to start), so it is a separate
step rather than part of the default suite.

Needs: libreoffice-impress, libreoffice-writer, python3-uno, poppler-utils.
    apt-get install -y libreoffice-impress libreoffice-writer poppler-utils

What it proves that a file-format reader cannot:
  * the deck loads as a presentation at all;
  * every click action resolves to the slide it should, as the application
    resolves it - including the shape-level links on the buttons, which do not
    survive PDF export and so cannot be checked from a rendered copy;
  * each Word file really is A4 when opened, not just in its stored settings.
"""
import glob, os, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DECK = os.path.join(ROOT, "materials", "jeopardy", "Jeopardy_Great_Britons_A2.pptx")
DOCX = os.path.join(ROOT, "materials", "docx")
PORT = 2002

fails = []


def check(ok, label, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"   ({detail})" if detail and not ok else ""))
    if not ok:
        fails.append(label)


def deck_click_actions(profile):
    """Ask LibreOffice what every clickable shape in the deck does."""
    import uno
    from com.sun.star.beans import PropertyValue
    proc = subprocess.Popen(
        ["soffice", f"-env:UserInstallation=file://{profile}", "--headless",
         "--norestore", "--invisible",
         f"--accept=socket,host=127.0.0.1,port={PORT};urp;StarOffice.ServiceManager"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local)
    ctx = None
    for _ in range(60):
        try:
            ctx = resolver.resolve(
                f"uno:socket,host=127.0.0.1,port={PORT};urp;StarOffice.ComponentContext")
            break
        except Exception:
            time.sleep(1)
    if ctx is None:
        proc.kill()
        raise SystemExit("could not reach LibreOffice")
    desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    hidden = PropertyValue(); hidden.Name = "Hidden"; hidden.Value = True
    doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(DECK), "_blank", 0, (hidden,))
    pages = doc.getDrawPages()
    names = [pages.getByIndex(i).Name for i in range(pages.getCount())]
    at = {n: i + 1 for i, n in enumerate(names)}
    rows, heads = [], []
    for i in range(pages.getCount()):
        pg = pages.getByIndex(i)
        first = ""
        for j in range(pg.getCount()):
            sh = pg.getByIndex(j)
            txt = ""
            try:
                txt = sh.String.strip().replace("\n", " ")
            except Exception:
                pass
            if txt and not first:
                first = txt
            try:
                if "NONE" in str(sh.OnClick):
                    continue
                rows.append((i + 1, txt, at.get(sh.Bookmark)))
            except Exception:
                continue
        heads.append(first)
    doc.close(False)
    try:
        desktop.terminate()
    except Exception:
        pass
    try:
        proc.wait(timeout=30)
    except Exception:
        proc.kill()
    return len(names), heads, rows


print("Checking the pack with LibreOffice\n")
print("-- Jeopardy deck")
with tempfile.TemporaryDirectory() as tmp:
    count, heads, rows = deck_click_actions(os.path.join(tmp, "profile"))
    check(count == 84, "the deck opens as a presentation with 84 slides", f"got {count}")
    kind = {i + 1: ("Q" if "POINTS" in h else "A" if h.startswith("ANSWER") else "other")
            for i, h in enumerate(heads)}
    tiles = [r for r in rows if r[0] == 2]   # hotspots over the painted plaques
    shows = [r for r in rows if "SHOW" in r[1].upper()]
    backs = [r for r in rows if "BOARD" in r[1].upper() and r[0] != 2]
    check(len(tiles) == 40, "40 board tiles are clickable", str(len(tiles)))
    # the grid is read column by column: Childhood 100..800, then Career, ...
    want = sorted(3 + 16 * c + 2 * r for c in range(5) for r in range(8))
    check(sorted(t[2] for t in tiles) == want,
          "the tiles open the 40 question slides, one each")
    check(all(kind.get(t[2]) == "Q" for t in tiles),
          "every tile lands on a question slide")
    check(all(s[2] == s[0] + 1 and kind.get(s[2]) == "A" for s in shows),
          f"all {len(shows)} SHOW ANSWER buttons open their own answer")
    check(all(b[2] == 2 for b in backs),
          f"all {len(backs)} BACK TO BOARD buttons return to the board")
    check(len(rows) == 161, "161 click actions in total", str(len(rows)))

print("\n-- Word files")
with tempfile.TemporaryDirectory() as tmp:
    files = sorted(glob.glob(os.path.join(DOCX, "*.docx")))
    subprocess.run(["soffice", f"-env:UserInstallation=file://{tmp}/p", "--headless",
                    "--norestore", "--convert-to", "pdf", "--outdir", tmp] + files,
                   capture_output=True, timeout=900)
    bad = []
    for f in files:
        pdf = os.path.join(tmp, os.path.basename(f)[:-5] + ".pdf")
        if not os.path.exists(pdf):
            bad.append(f"{os.path.basename(f)}: did not open"); continue
        info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        if "A4" not in info:
            size = re.search(r"Page size:\s*(.+)", info)
            bad.append(f"{os.path.basename(f)}: {size.group(1) if size else '?'}")
    check(not bad, f"all {len(files)} Word files open and are A4", " | ".join(bad[:3]))

print(f"\n{'all checks passed' if not fails else str(len(fails)) + ' FAILED'}")
sys.exit(1 if fails else 0)

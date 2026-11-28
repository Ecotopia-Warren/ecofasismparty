"""Customs (inburgering) crew sheets: CUSTOMS_CREW_GUIDE.md -> A4 PDF (2 pages) + A5 laminate cheat card,
plus a 2-up A4 (two identical A5 cards side by side, cut once down the dashed middle line).

The cheat card is the "What to say" section of the guide (between <!-- card:start --> and <!-- card:end -->),
so the card and the guide cannot drift apart. Same HTML -> PDF method as passport_v2 (Playwright Chromium).
Black text only and >= 8 mm margins (the Brother HL-2150N loses the outer ~4-5 mm).

Run: python3 customs/make_customs_pdfs.py   (needs pandoc + playwright)
"""
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "CUSTOMS_CREW_GUIDE.md")

BASE_CSS = """
*{box-sizing:border-box}
body{margin:0;font-family:'DejaVu Sans Condensed','DejaVu Sans',sans-serif;color:#000;line-height:1.22}
h1{font-size:17pt;background:#000;color:#fff;margin:0 0 1.5mm;padding:1.2mm 2.5mm;letter-spacing:.5px}
h2{font-size:12.5pt;border-bottom:2.5px solid #000;margin:2.6mm 0 1.2mm;padding-bottom:.3mm}
p{margin:0 0 1.3mm}
ul,ol{margin:0 0 1.3mm;padding-left:5mm}
li{margin:0 0 .5mm}
table{border-collapse:collapse;width:100%;margin:0 0 1.5mm}
th,td{border:1px solid #000;padding:.5mm 1.3mm;text-align:left;vertical-align:top}
th{background:#000;color:#fff}
td:empty{border:none}
em{font-style:italic}
strong{font-weight:800}
.safety{border:3px solid #000;padding:1.3mm 2.5mm;margin:1.5mm 0 1mm}
.safety p:first-child{font-size:12pt;margin-bottom:.8mm}
.safety ul{margin:0}
"""

A4_CSS = """
@page{size:A4 portrait;margin:9mm 10mm}
body{font-size:10pt}
table{font-size:9.6pt}
"""

A5_CSS = """
@page{size:A5 portrait;margin:8mm 9mm}
body{font-size:10.5pt;line-height:1.15}
h1{font-size:13pt}
h2{display:none}
p{margin:0 0 1.1mm}
ul{margin:0 0 1.1mm;padding-left:4mm}
li{margin:0 0 .35mm}
"""


def html_doc(title, body, css):
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{BASE_CSS}{css}</style></head><body>{body}</body></html>')


TWO_UP_CSS = """
@page{size:A4 landscape;margin:0}
.sheet{display:flex;width:297mm;height:209mm;overflow:hidden}
.half{width:148.5mm;height:209mm;padding:8mm 9mm;overflow:hidden}
.half:first-child{border-right:1px dashed #000}
"""


def md2html(md):
    return subprocess.run(["pandoc", "-f", "markdown", "-t", "html5"], input=md, capture_output=True,
                          text=True, check=True).stdout


def render(paths):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page()
        for p in paths:
            page.goto("file://" + p, wait_until="load")
            page.evaluate("document.fonts.ready.then(() => true)")
            page.emulate_media(media="print")
            page.pdf(path=p[:-5] + ".pdf", prefer_css_page_size=True, print_background=True)
        b.close()


def main():
    md = open(SRC).read()
    card = re.search(r"<!-- card:start -->(.*?)<!-- card:end -->", md, re.S).group(1)
    card = "# CUSTOMS · WHAT TO SAY\n\n" + card
    out = {
        "CUSTOMS_CREW_GUIDE": html_doc("Customs crew guide", md2html(md), A4_CSS),
        "CUSTOMS_CHEAT_CARD": html_doc("Customs cheat card", md2html(card), A5_CSS),
    }
    c = md2html(card)
    out["CUSTOMS_CHEAT_CARD_2UP"] = html_doc("Customs cheat card 2-up",
                                             f'<div class="sheet"><div class="half">{c}</div><div class="half">{c}</div></div>',
                                             A5_CSS.replace("@page{size:A5 portrait;margin:8mm 9mm}", "") + TWO_UP_CSS)
    paths = []
    for name, doc in out.items():
        p = os.path.join(HERE, name + ".html")
        open(p, "w").write(doc)
        paths.append(p)
    render(paths)
    # the 2-up halves clip silently: fail loudly if the single A5 card no longer fits one page
    for p in paths:
        pages = subprocess.run(["pdfinfo", p[:-5] + ".pdf"], capture_output=True, text=True).stdout
        n = re.search(r"Pages:\s+(\d+)", pages)
        print(os.path.basename(p[:-5]) + ".pdf", "pages:", n.group(1) if n else "?")
        limit = {"CUSTOMS_CREW_GUIDE": 2}.get(os.path.basename(p[:-5]), 1)
        if not n or int(n.group(1)) > limit:
            raise SystemExit(f"{os.path.basename(p)}: more than {limit} page(s): cut text (don't shrink the type)")


if __name__ == "__main__":
    main()

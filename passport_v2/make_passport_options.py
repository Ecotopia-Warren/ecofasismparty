"""Citizen Passport: five production options, from least to most paper. Made for the SMALL stamp
set (stamps/stampmaker_stl_small: 19.5 mm seals, 15 mm credit stamps).

Run: python3 make_passport_options.py  -> passport_<n>_<name>.html + .pdf for each option

  1 card_single   1 page.   A6 card, one side.   4 per A4, single-sided.   Cut only.
  2 card_double   2 pages.  A6 card, both sides. 4 per A4, double-sided.   Cut only.
  3 zine_micro    8 pages.  ~A8 fold-up.         2 per A4, single-sided.   Cut, slit, fold.
  4 zine_pocket   8 pages.  ~A7 fold-up.         1 per A4, single-sided.   Slit, fold.
  5 booklet16    16 pages.  ~A7 stapled booklet. 1 per A4, double-sided.   Cut, fold, nest, staple.

Print every PDF at 100% / "actual size". Content stays >= 5 mm from the sheet edge.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
STAG = open(os.path.join(HERE, "great_seal_bw.svg")).read().replace("<svg ", '<svg class="crest" ', 1)

_src = open(os.path.join(HERE, "..", "stamps", "insignia", "make_insignia.py")).read()
_ns = {"__file__": os.path.join(HERE, "..", "stamps", "insignia", "x.py")}
exec(_src[:_src.index("for i, n in enumerate(ORDER")], _ns)
ICONS, ORDER = _ns["ICONS"], _ns["ORDER"]
MARGIN = 5  # mm, unprintable-edge safety

# ---------------------------------------------------------------- content blocks

def grid(cols, rows, start=1):
    boxes = "".join(f'<div class="box"><span>{start + i}</span></div>' for i in range(cols * rows))
    return f'<div class="grid" style="grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({rows},1fr)">{boxes}</div>'


def ledger(cols, rows, start, sub=False):
    s = '<p class="sub">Stamp every reward (+) and fine (&minus;)</p>' if sub else ""
    return f'<h2>CREDITS</h2>{s}{grid(cols, rows, start)}<div class="total">Total<span class="line"></span>CC</div>'


def seal(mm):
    return f'<div class="seal" style="width:{mm}mm;height:{mm}mm">MINISTRY<br>SEAL</div>'


COVER = f"""<div class="cover"><div class="big">REPUBLIC OF<br>ECOTOPIA</div>{STAG}
<div class="title">CITIZEN<br>PASSPORT</div><div class="motto">R.E.I.G.N. decides,<br>so that citizens are free.</div></div>"""
BACKCOVER = f"""<div class="cover">{STAG}<div class="motto">Your arrival<br>has been noted.</div>
<div class="title small">BY ORDER OF<br>R.E.I.G.N.</div></div>"""
CITIZEN = f"""<h2>CITIZEN</h2>
<div class="field">Name<span class="line"></span></div>
<div class="field">Ministry<span class="line"></span></div>
<div class="startbox"><div>CARBON DEBT</div><div class="amount">&minus;<span class="line short"></span>CC</div></div>
<div class="seal-wrap">{seal(22)}</div>"""
HOW = """<h2>HOW IT WORKS</h2><ol class="rules">
<li>Debt is written in at the door.</li>
<li>Serve, play, obey: <b>+</b> stamps.</li>
<li>Misbehave: <b>&minus;</b> stamps.</li>
<li>Reach <b>0</b>: debt repaid.</li></ol>
<div class="ozone mt">SAFE WORD<span>OZONE</span><small>stops all play at once</small></div>"""
CLEARANCE = """<h2>CLEARANCE</h2>
<div class="permits"><div class="permit"><i>permit</i></div></div>
<div class="startbox"><div>FINAL BALANCE</div><div class="amount"><span class="line short"></span>CC</div></div>
<div class="field">Officer<span class="line"></span></div>"""
REIGN = """<h2>R.E.I.G.N.</h2><div class="lore">
<p class="reign">Regime for<br>Ecological<br>Integrity and<br>Global<br>Nurturing</p>
<p class="quote">R.E.I.G.N. decides,<br>so that citizens are free.</p></div>"""
ARTICLES = """<h2>ARTICLES</h2><ol class="articles">
<li><b>I.</b> Every citizen is placed where they will flourish.</li>
<li><b>II.</b> Questions are welcome. They have already been answered.</li>
<li><b>III.</b> Rest is a right of every citizen. It is scheduled.</li>
<li><b>IV.</b> R.E.I.G.N. hears every concern. Every single one.</li></ol>"""
MINISTRIES = '<h2>MINISTRIES</h2><div class="mins">' + "".join(
    f'<div class="min"><svg viewBox="60 64 80 80" class="micon">{ICONS[n]}</svg><span>{n.title()}</span></div>' for n in ORDER) + "</div>"
DECREE = """<h2>DECREE</h2><div class="lore">
<p class="decree">By decree of R.E.I.G.N., artificial intelligence is banned in Ecotopia.</p>
<p>Citizens who did not apply are processed at the door: a longer wait, and further obligations.</p></div>"""

# Card faces (A6-ish, ~100 x 143 mm)
CARD_ONE = f"""<div class="chead"><div class="cbig">CITIZEN PASSPORT</div><div class="csmall">Republic of Ecotopia &middot; by order of R.E.I.G.N.</div></div>
<div class="crow"><div class="cfields">
<div class="field">Name<span class="line"></span></div>
<div class="field">Ministry<span class="line"></span></div>
<div class="field">Debt &minus;<span class="line"></span>CC</div></div>{seal(22)}</div>
<h2>CREDITS</h2>{grid(4, 3, 1)}
<div class="field">Final balance<span class="line"></span>CC &nbsp; Officer<span class="line"></span></div>
<div class="foot">Safe word <b>OZONE</b> stops all play at once.</div>"""
CARD_FRONT = f"""<div class="cover"><div class="big">REPUBLIC OF ECOTOPIA</div>{STAG}
<div class="title">CITIZEN PASSPORT</div></div>
<div class="crow"><div class="cfields">
<div class="field">Name<span class="line"></span></div>
<div class="field">Ministry<span class="line"></span></div>
<div class="field">Debt &minus;<span class="line"></span>CC</div></div>{seal(22)}</div>
<div class="foot">Safe word <b>OZONE</b> stops all play at once.</div>"""
CARD_BACK = f"""{ledger(4, 5, 1, sub=True)}
<div class="field">Final balance<span class="line"></span>CC &nbsp; Officer<span class="line"></span></div>"""

# A7 mini cards (landscape, ~100 x 72 mm)
MINI_ONE = f"""<div class="chead"><div class="cbig">CITIZEN PASSPORT</div><div class="csmall">Republic of Ecotopia &middot; by order of R.E.I.G.N.</div></div>
<div class="crow"><div class="cfields">
<div class="field">Name<span class="line"></span></div>
<div class="field">Debt &minus;<span class="line"></span>CC</div>
<div class="field">Final<span class="line"></span>CC</div></div>{seal(22)}</div>
{grid(4, 1, 1)}
<div class="foot">Safe word <b>OZONE</b> stops all play.</div>"""
MINI_FRONT = f"""<div class="crow full">{STAG.replace('class="crest"', 'class="crest side"', 1)}<div class="cfields">
<div class="cbig">CITIZEN<br>PASSPORT</div><div class="csmall">Republic of Ecotopia</div>
<div class="field">Name<span class="line"></span></div>
<div class="field">Ministry<span class="line"></span></div>
<div class="field">Debt &minus;<span class="line"></span>CC</div></div></div>
<div class="foot">Safe word <b>OZONE</b> stops all play at once.</div>"""
MINI_BACK = f"""<div class="crow full">{seal(22)}{grid(3, 2, 1)}</div>
<div class="field">Final balance<span class="line"></span>CC &nbsp; Officer<span class="line"></span></div>"""

# Poster printed on the back of the pocket fold-up: only seen when the passport is unfolded.
POSTER = f"""<div class="poster"><div class="phead">{STAG}<div><div class="pbig">THE REPUBLIC OF ECOTOPIA</div>
<div class="psub">You unfolded your passport. R.E.I.G.N. noticed.</div></div>{STAG}</div>
<div class="pcols"><div>{REIGN}</div><div>{ARTICLES}</div><div>{MINISTRIES}</div><div>{DECREE}</div></div></div>"""

# ---------------------------------------------------------------- CSS

BASE = """
.frame{border:2.5px solid #000;outline:1px solid #000;outline-offset:-2.2mm;padding:4.5mm 4.5mm}
h2{font-family:'Archivo Black',sans-serif;font-size:16pt;letter-spacing:1px;background:#000;color:#fff;text-align:center;padding:1mm 0;line-height:1.2;margin-bottom:2.5mm}
.sub{font-size:10pt;margin:-1mm 0 2mm}
.pn{bottom:1.2mm;right:2.5mm;font-size:8pt}
.line{min-width:12mm}
.line.short{width:26mm}
.grid{gap:1.6mm}
.box span{top:.5mm;left:.8mm;font-size:6pt}
.total{font-size:12pt;gap:2mm;margin-top:2.5mm}
.cover{padding:2mm 0 3mm}
.cover .big{font-size:20pt}
.cover .title{font-size:24pt;border-top:3px solid #000;border-bottom:3px solid #000;padding:2mm 4mm}
.cover .title.small{font-size:15pt}
.crest{width:46mm;height:46mm}
.motto{font-size:11pt}
.field{font-size:13pt;gap:2mm;margin-top:4mm}
.startbox{border:2.5px solid #000;margin-top:5mm;padding:2mm;font-size:11pt}
.startbox .amount{font-size:20pt;margin-top:1mm;gap:1.5mm}
.seal{font-size:9pt}
.rules{font-size:13pt;line-height:1.3;margin:3mm 0 0 6mm}
.rules li{margin-bottom:2.5mm}
.ozone{border:3px solid #000;font-size:11pt;padding:2.5mm}
.ozone span{font-size:28pt;letter-spacing:3px}
.ozone small{font-size:10pt}
.permits{gap:3mm;margin-bottom:1mm}
.permit i{font-size:10pt}
.lore{gap:5mm;font-size:13pt;line-height:1.3;margin-top:4mm}
.reign{font-size:17pt}
.quote{border-top:2px solid #000;border-bottom:2px solid #000;padding:2mm 0}
.decree{font-size:16pt}
.articles{font-size:13pt;line-height:1.3}
.articles li{margin-bottom:4mm}
.mins{gap:2mm 3mm}
.min{font-size:12.5pt;gap:2mm}
.micon{width:13mm;height:13mm}
.chead{border-bottom:3px solid #000;padding-bottom:2mm}
.cbig{font-size:22pt}
.csmall{font-size:10pt}
.crow{gap:4mm;margin:1mm 0 4mm}
.foot{font-size:10pt;margin-top:2.5mm}
"""

FIXED = """
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@500;700;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
body{background:#444;font-family:'Archivo','DejaVu Sans',sans-serif;color:#000;display:flex;flex-direction:column;align-items:center;padding:12px;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
.label{color:#fff;font:700 16px 'Archivo',sans-serif;margin:10px 0 6px;text-align:center}
.sheet{background:#fff;display:flex;flex-direction:column;position:relative}
.pg{position:relative;padding:.8mm;overflow:hidden}
.frame{height:100%;position:relative;display:flex;flex-direction:column;overflow:hidden}
.pn{position:absolute;font-weight:800}
h2{flex:none}
.sub{font-weight:700;text-align:center}
.line{display:inline-block;flex:1;border-bottom:2px solid #000;height:1em}
.line.short{flex:none}
.grid{display:grid;flex:1}
.box{border:1.5px dashed #000;position:relative}
.box span{position:absolute;font-weight:700;color:#666}
.total{font-weight:800;display:flex;align-items:end}
.cover{display:flex;flex-direction:column;align-items:center;justify-content:space-between;text-align:center;flex:1}
.cover .big,.cover .title{font-family:'Archivo Black',sans-serif;line-height:1.05}
.motto{font-weight:700;font-style:italic}
.field{font-weight:800;display:flex;align-items:end}
.startbox{text-align:center;font-weight:800}
.startbox .amount{font-family:'Archivo Black',sans-serif;display:flex;justify-content:center;align-items:end}
.seal-wrap{flex:1;display:flex;align-items:center;justify-content:center}
.seal{flex:none;border:2px dashed #000;border-radius:50%;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;color:#777}
.rules{font-weight:700}
.ozone{text-align:center;font-weight:800}
.ozone span{display:block;font-family:'Archivo Black',sans-serif;line-height:1.1}
.ozone small{display:block}
.mt{margin-top:auto}
.permits{flex:1;display:flex;flex-direction:column}
.permit{flex:1;border:2px dashed #000;display:flex;align-items:center;justify-content:center;color:#999}
.lore{display:flex;flex-direction:column;font-weight:700;text-align:center}
.reign,.decree{font-family:'Archivo Black',sans-serif;line-height:1.15}
.quote{font-style:italic}
.articles{list-style:none;font-weight:700}
.mins{display:grid;grid-template-columns:1fr 1fr;flex:1;align-content:space-evenly}
.min{display:flex;align-items:center;font-weight:800}
.micon{flex:none}
.chead{text-align:center}
.cbig{font-family:'Archivo Black',sans-serif;line-height:1.1}
.csmall{font-weight:700}
.crow{display:flex;align-items:center}
.cfields{flex:1}
.foot{text-align:center;font-weight:700}
/* card + zine + booklet layouts */
.cards{flex:1;display:grid}
.cards .pg{border:1px dashed #999;border-width:0 1px 1px 0}
.crow.full{flex:1}
.crest.side{width:30mm;height:30mm;flex:none}
.crow .grid{height:100%}
.poster{flex:1;display:flex;flex-direction:column;border:3px solid #000;outline:1px solid #000;outline-offset:-3mm;padding:6mm}
.phead{display:flex;align-items:center;gap:6mm;border-bottom:4px solid #000;padding-bottom:3mm;margin-bottom:4mm}
.phead>div{flex:1;text-align:center}.phead .crest{width:42mm;height:42mm}
.pbig{font-family:'Archivo Black',sans-serif;font-size:40pt;line-height:1}
.psub{font-weight:700;font-style:italic;font-size:19pt;margin-top:2mm}
.pcols{flex:1;display:grid;grid-template-columns:1fr 1.3fr 1.2fr 1fr;gap:7mm}
.pcols>div{display:flex;flex-direction:column}
.pcols h2{font-size:20pt}
.pcols .lore,.pcols .articles{font-size:17pt;line-height:1.3}.pcols .articles li{margin-bottom:5mm}
.pcols .reign{font-size:22pt}.pcols .decree{font-size:20pt}
.pcols .min{font-size:17pt}.pcols .micon{width:16mm;height:16mm}
.zine{flex:1;display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:1fr 1fr;position:relative}
.zine+.zine{border-top:1px dashed #000}
.zine .pg+.pg{border-left:1px dotted #bbb}
.zine .pg:nth-child(n+5){border-top:1px dotted #bbb}
.zine .pg:nth-child(-n+4){transform:rotate(180deg)}
.zine .pg:nth-child(6),.zine .pg:nth-child(7){border-top:2px dashed #000}
.cut{position:absolute;top:50%;left:25%;width:50%;transform:translateY(-50%);text-align:center;font:700 7pt 'Archivo',sans-serif;z-index:2}
.cut b{background:#fff;padding:0 1.5mm}
.leaves{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}
.leaf{display:grid;grid-template-columns:1fr 1fr;position:relative;outline:1px dashed #999}
.leaf .pg+.pg{border-left:1px dotted #ccc}
.leaf .tag{position:absolute;top:.3mm;left:50%;transform:translateX(-50%);font:700 5pt 'Archivo',sans-serif;color:#999;z-index:2}
"""


def scale_css(css, k):
    return re.sub(r"(?<![\w.-])(\d*\.?\d+)(pt|mm)\b", lambda m: f"{float(m.group(1)) * k:.2f}{m.group(2)}", css)


def pg(body, n=None):
    num = f'<div class="pn">{n}</div>' if n else ""
    return f'<div class="pg"><div class="frame">{body}{num}</div></div>'


def doc(title, sheets, orient, k):
    w, h = (297, 210) if orient == "landscape" else (210, 297)
    css = FIXED + scale_css(BASE, k) + f"""
.sheet{{width:{w}mm;height:{h}mm;padding:{MARGIN}mm}}
@media print{{body{{background:none;padding:0}}.label{{display:none}}.sheet{{break-after:page}}
 @page{{size:A4 {orient};margin:0}}}}"""
    body = "".join(f'<div class="label">{lbl}</div><div class="sheet">{s}</div>' for lbl, s in sheets)
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>{css}</style></head><body>{body}</body></html>'

# ---------------------------------------------------------------- the ten versions
# Printing on the Brother HL-2150N: "S" = single-sided, one pass.
# "D" = both sides by MANUAL flip: print side 1, put the stack back in the tray turned over, print side 2.

def cards(face, cols, rows):
    return (f'<div class="cards" style="grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({rows},1fr)">'
            + pg(face) * (cols * rows) + "</div>")


ZINE_PAGES = lambda cols, rows: {1: COVER, 2: CITIZEN, 3: HOW, 4: ledger(cols, rows, 1),
                                 5: ledger(cols, rows, 1 + cols * rows), 6: ledger(cols, rows, 1 + 2 * cols * rows),
                                 7: ledger(cols, rows, 1 + 3 * cols * rows), 8: CLEARANCE}


def zine(pages):
    order = [5, 4, 3, 2, 6, 7, 8, 1]  # top row printed upside down
    return ('<div class="zine">' + "".join(pg(pages[n], n) for n in order) +
            '<div class="cut"><b>&#9986; cut only this middle line</b></div></div>')


def booklet(P, N):
    """Saddle-stitched booklet, A7 pages, leaves imposed 2x2 on A4 landscape (short-edge flip)."""
    L = [((N - 2 * k, 2 * k + 1), (2 * k + 2, N - 2 * k - 1)) for k in range(N // 4)]
    items = [(c, k) for c in range(4 // len(L)) for k in range(len(L))]
    copies = 4 // len(L)
    sides = []
    for side in (0, 1):
        cells = []
        for r in range(2):
            for c in range(2):
                cp, k = items[r * 2 + (c if side == 0 else 1 - c)]
                a, b = L[k][side]
                tag = (f"passport {cp + 1} &middot; " if copies > 1 else "") + f"leaf {k + 1}"
                cells.append(f'<div class="leaf"><span class="tag">{tag}</span>{pg(P[a], a)}{pg(P[b], b)}</div>')
        sides.append('<div class="leaves">' + "".join(cells) + "</div>")
    return sides


SAFETY = ('<h2>SAFETY</h2><div class="ozone">SAFE WORD<span>OZONE</span><small>stops all play at once</small></div>'
          '<p class="sub mt">Say it, and play stops.<br>No questions. No penalty.</p>')
D = "Side 2: put the printed stack back in the tray turned over, then print this page."


def v01():
    return doc("01 A6 card (single-sided)", [("Single-sided. Cut on the dashed lines: 4 passports.", cards(CARD_ONE, 2, 2))], "portrait", 0.93)


def v02():
    return doc("02 A7 mini card (single-sided)", [("Single-sided. Cut on the dashed lines: 8 passports.", cards(MINI_ONE, 2, 4))], "portrait", 0.7)


def v03():
    z = zine(ZINE_PAGES(2, 3))
    return doc("03 Micro fold-up (single-sided)", [("Single-sided. Cut in half first, then fold each half.", z + z)], "portrait", 0.55)


def v04():
    return doc("04 Pocket fold-up (single-sided)", [("Single-sided. Slit the middle line, then fold.", zine(ZINE_PAGES(3, 4)))], "landscape", 0.72)


def v05():
    P = {1: COVER, 2: CITIZEN, 3: REIGN, 4: ledger(3, 4, 1), 5: MINISTRIES, 6: ledger(3, 4, 13), 7: HOW, 8: CLEARANCE}
    return doc("05 Pocket fold-up, lore edition (single-sided)", [("Single-sided. Slit the middle line, then fold.", zine(P))], "landscape", 0.72)


def v06():
    return doc("06 A6 card (double-sided)", [("Side 1 (front).", cards(CARD_FRONT, 2, 2)),
                                             (D + " All backs are identical.", cards(CARD_BACK, 2, 2))], "portrait", 0.93)


def v07():
    return doc("07 A7 mini card (double-sided)", [("Side 1 (front).", cards(MINI_FRONT, 2, 4)),
                                                  (D + " All backs are identical.", cards(MINI_BACK, 2, 4))], "portrait", 0.7)


def v08():
    return doc("08 Pocket fold-up + lore poster (double-sided)", [
        ("Side 1: the passport. Slit the middle line, then fold.", zine(ZINE_PAGES(3, 4))),
        (D + " The poster is only seen when unfolded, so alignment does not matter.", POSTER)], "landscape", 0.72)


def v09():
    P = {1: COVER, 2: CITIZEN, 3: HOW, 4: ledger(3, 4, 1), 5: ledger(3, 4, 13), 6: ledger(3, 4, 25), 7: CLEARANCE, 8: BACKCOVER}
    f, b = booklet(P, 8)
    return doc("09 8-page stapled booklet (double-sided)", [
        ("Side 1 (flip on SHORT edge).", f),
        (D + " Cut into 4, fold each, nest leaf 1 around leaf 2, staple: 2 passports.", b)], "landscape", 0.72)


def v10():
    P = {1: COVER, 2: CITIZEN, 3: REIGN, 4: ARTICLES, 5: MINISTRIES, 6: HOW,
         7: ledger(3, 4, 1), 8: ledger(3, 4, 13), 9: ledger(3, 4, 25), 10: ledger(3, 4, 37),
         11: ledger(3, 4, 49), 12: ledger(3, 4, 61), 13: CLEARANCE, 14: DECREE, 15: SAFETY, 16: BACKCOVER}
    f, b = booklet(P, 16)
    return doc("10 16-page stapled booklet (double-sided)", [
        ("Side 1 (flip on SHORT edge).", f),
        (D + " Cut into 4, fold each, nest leaf 1 outside to leaf 4 inside, staple.", b)], "landscape", 0.72)


# name, builder, method, pages, passports per sheet, handwork, what it is
VERSIONS = [
    ("01_a6_card_single", v01, "S", 1, 4, "cut", "A6 card, everything on one face"),
    ("02_a7_card_single", v02, "S", 1, 8, "cut", "A7 mini card, ultra minimal"),
    ("03_zine_micro", v03, "S", 8, 2, "cut, slit, fold", "A8 fold-up booklet"),
    ("04_zine_pocket", v04, "S", 8, 1, "slit, fold", "A7 fold-up, max credits"),
    ("05_zine_pocket_lore", v05, "S", 8, 1, "slit, fold", "A7 fold-up, lore edition"),
    ("06_a6_card_double", v06, "D", 2, 4, "cut", "A6 card, cover front, credits back"),
    ("07_a7_card_double", v07, "D", 2, 8, "cut", "A7 mini card, credits back"),
    ("08_zine_pocket_poster", v08, "D", 8, 1, "slit, fold", "A7 fold-up, lore poster inside"),
    ("09_booklet8", v09, "D", 8, 2, "cut, fold, nest, staple", "A7 stapled booklet"),
    ("10_booklet16", v10, "D", 16, 1, "cut, fold, nest, staple", "A7 stapled booklet, full lore"),
]

if __name__ == "__main__":
    import glob
    for old in glob.glob(os.path.join(HERE, "passport_[0-9]_*.*")):
        os.remove(old)  # outputs of the earlier 5-option version
    paths = []
    for name, fn, *_ in VERSIONS:
        p = os.path.join(HERE, f"passport_{name}.html")
        open(p, "w").write(fn())
        paths.append(p)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            page = b.new_page()
            for p in paths:
                page.goto("file://" + p)
                page.wait_for_load_state("networkidle")
                page.emulate_media(media="print")
                page.pdf(path=p[:-5] + ".pdf", prefer_css_page_size=True, print_background=True)
            b.close()
    except ImportError:
        print("playwright not installed: open the .html files and print to PDF")
    for p in paths:
        print("wrote", os.path.basename(p)[:-5], ".html + .pdf")

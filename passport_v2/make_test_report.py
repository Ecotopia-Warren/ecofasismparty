"""Printable fill-in test report for the passport options (make_passport_options.py).

Run: python3 make_test_report.py -> ecotopia_passport_test_report.html + .pdf
Print: A4, single-sided, 100% / actual size, black & white (Brother HL-2150N).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = open(os.path.join(HERE, "great_seal_bw.svg")).read().replace("<svg ", '<svg class="crest" ', 1)
RUN = 250

# name, file, pages, per sheet, duplex, sheets for RUN, page size, box (expected, mm), boxes per passport, handwork
import math
import make_passport_options as opts


def measure():
    """Expected values, measured from the generated passport HTML files."""
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        for name, *_ in opts.VERSIONS:
            pg.goto("file://" + os.path.join(HERE, f"passport_{name}.html"))
            pg.wait_for_load_state("networkidle")
            out[name] = pg.evaluate("""()=>{const mm=96/25.4;const bx=[...document.querySelectorAll('.box')].map(b=>b.getBoundingClientRect());
              const p=document.querySelector('.pg').getBoundingClientRect();
              return {n:bx.length, bw:Math.min(...bx.map(r=>r.width))/mm, bh:Math.min(...bx.map(r=>r.height))/mm, pw:p.width/mm, ph:p.height/mm}}""")
        b.close()
    rows = []
    for name, _, method, pages, per, hand, what in opts.VERSIONS:
        m = out[name]
        rows.append(dict(n=name[:2], name=what, file=f"passport_{name}.pdf", pages=pages, per=per,
                         duplex="manual flip" if method == "D" else "no", method=method,
                         sheets=math.ceil(RUN / per), size=f"{m['pw']:.1f} x {m['ph']:.1f}",
                         box=f"{m['bw']:.1f} x {m['bh']:.1f}", boxes=m["n"] // per, hand=hand))
    return rows



STAMPS = ["Purity", "Radiance", "Breath", "Flow", "Light", "Industry", "Humus", "Service", "Vigilance", "Joy"]
CREDITS = ["+10", "+20", "+50", "&minus;10", "&minus;20", "&minus;50"]


def box(label=""):
    return f'<span class="cb"></span>{label}'


def pf():
    return f'<td class="pf">{box("pass")} &nbsp; {box("fail")}</td>'


def version_block(v):
    n, name, f, pages, per, duplex, sheets, size, bx, boxes, hand = (v[k] for k in
        ("n", "name", "file", "pages", "per", "duplex", "sheets", "size", "box", "boxes", "hand"))
    checks = [
                (f"Page / card size measures {size} mm", "measured: ______ x ______ mm"),
        (f"Stamp box measures {bx} mm", "measured: ______ x ______ mm"),
        ("Nothing clipped at the sheet edges (all frames complete)", ""),
        ("Black is solid, no grey dots or streaks; small text readable", ""),
        ("15 mm credit stamp fits inside a box without touching the border", ""),
        ("19.5 mm ministry seal fits inside the seal circle", ""),
        ("Ink dry / no smudge after 30 s; pen writes on the lines", ""),
    ]
    if duplex != "no":
        checks.append(("Side 2 lands upright on the back after flipping the stack by hand", "stack orientation: __________"))
    if "fold" in hand:
        checks.append(("Folds into the right page order (1 to last, cover outside)", ""))
    rows = "".join(f"<tr><td>{c}<div class='note'>{m}</div></td>{pf()}</tr>" for c, m in checks)
    return f"""<section class="ver">
<div class="vhead"><span class="vn">{n}</span><div><b>{name}</b><small>{f}</small></div>
<div class="spec">{pages} p &middot; {per}/sheet &middot; duplex: {duplex} &middot; {boxes} boxes &middot; {sheets} sheets for {RUN}</div></div>
<table class="chk">{rows}</table>
<div class="meas">
<div>Time to print 1 sheet<span class="ln"></span>s</div>
<div>Time to finish 1 passport ({hand})<span class="ln"></span>s</div>
<div>&times; {RUN} = <span class="ln"></span>min</div>
</div>
<div class="score">Feel / immersion {"".join(f'<span class="sc">{i}</span>' for i in range(1, 6))}
&nbsp; Durability {"".join(f'<span class="sc">{i}</span>' for i in range(1, 6))}
&nbsp; Verdict {box("GO")} {box("NO-GO")}</div>
<div class="notes">Remarks</div>
</section>"""


def stamp_page():
    seals = "".join(f'<div class="st"><div class="ring"></div><span>{s}</span><div class="mini">{box("sharp")} {box("blurred")} {box("ink blob")}</div></div>' for s in STAMPS)
    creds = "".join(f'<div class="st"><div class="sq"></div><span>{c}</span><div class="mini">{box("sharp")} {box("blurred")} {box("ink blob")}</div></div>' for c in CREDITS)
    return f"""<div class="page">{header("TEST 2 &middot; STAMP IMPRESSION", "Press each small-set stamp once inside its outline.")}
<p class="intro">Stamps: <b>stamps/stampmaker_stl_small</b> (TPU face on PLA handle). Outlines are the size the passport offers:
seal circle &Oslash; 22 mm, credit box 17 x 17 mm. Ink used: ______________ &nbsp; Stamp pad: ______________</p>
<h3>Ministry seals (19.5 mm)</h3><div class="sgrid">{seals}</div>
<h3>Credit stamps (15 mm)</h3><div class="sgrid six">{creds}</div>
<table class="chk tight"><tr><td>All impressions stay inside their outline</td>{pf()}</tr>
<tr><td>Relief prints evenly (no background plate touching the paper)</td>{pf()}</tr>
<tr><td>Stamps are distinguishable at a glance by a door officer</td>{pf()}</tr></table>
<div class="notes">Remarks / reprint list</div>{footer(5)}</div>"""


def header(title, sub):
    return f"""<header>{SEAL}<div><div class="org">REPUBLIC OF ECOTOPIA &middot; MINISTRY OF VIGILANCE</div>
<div class="dept">Bureau of Paper Austerity &amp; Document Integrity</div><h1>{title}</h1><div class="hsub">{sub}</div></div>
<div class="form">FORM R-7/QA<br>Passport trial<br>Run: {RUN} citizens</div></header>"""


TOTAL = 6


def footer(n):
    return (f'<footer><span>R.E.I.G.N. decides, so that citizens are free. Every test result is counted, including yours.</span>'
            f'<span>Page {n} / {TOTAL}</span></footer>')


def page1(V):
    return f"""<div class="page">{header("PASSPORT FIELD TRIAL: RESEARCH PROTOCOL", "Which citizen passport wastes the least paper and still survives the night?")}
<div class="two">
<div class="kv"><div>Test engineer<span class="ln"></span></div><div>Date / time<span class="ln"></span></div>
<div>Location<span class="ln"></span></div><div>Witness<span class="ln"></span></div></div>
<div class="kv"><div>Printer <b>Brother HL-2150N</b> (no auto-duplex)</div><div>Paper<span class="ln"></span>g/m&sup2;</div>
<div>Scale setting {box("100% / actual size")}</div><div>Toner level {box("ok")} {box("low")}</div></div></div>
<h3>1. Objective</h3>
<p class="intro">Select one of ten passport versions for a production run of <b>{RUN}</b> citizens (De Warren, 28 Nov 2026),
printed on a single-sided laser printer and stamped with the small TPU stamp set (19.5 mm seals, 15 mm credits).</p>
<h3>2. Hypotheses</h3>
<ol class="proc"><li><b>H1</b> A passport with 12 to 20 stamp boxes is enough for one night; more boxes add paper, not play.</li>
<li><b>H2</b> Single-sided versions (01 to 05) cost less assembly time per passport than manual-flip versions (06 to 10).</li>
<li><b>H3</b> Fold-up versions feel more like a real passport (immersion) than flat cards, at a cost in paper and time.</li>
<li><b>H4</b> Every printed stamp box fits a 15 mm credit stamp without the impression touching the border.</li></ol>
<h3>3. Variables</h3>
<table class="sum vars"><tr><th>Independent</th><th>Measured (dependent)</th><th>Controlled (keep constant)</th></tr>
<tr><td>Format: card, fold-up, stapled booklet<br>Size: A6, A7, A8<br>Print method: single pass vs manual flip</td>
<td>Dimensions (mm), print defects, stamp fit, time per passport (s), immersion (1 to 5), durability (1 to 5)</td>
<td>Printer, paper, scale 100%, one stamp pad, one test engineer, same stamps</td></tr></table>
<h3>4. Calibration</h3>
<p class="intro">Measure this bar with a ruler. It must be exactly 100 mm; if not, the print dialog is scaling (switch off "fit to page") and every measurement below is void.</p>
<div class="cal"><div class="bar">{"".join("<i></i>" for _ in range(10))}</div><span>100 mm</span>
<span class="intro">&nbsp; Measured: ______ mm &nbsp; {box("pass")} {box("fail")}</span></div>
<h3>5. Equipment</h3>
<p class="intro">{box("Ruler (mm)")} &nbsp; {box("Stopwatch / phone")} &nbsp; {box("Scissors or cutter + mat")} &nbsp; {box("Stapler")} &nbsp;
{box("Small stamp set + handle")} &nbsp; {box("Stamp pad")} &nbsp; {box("Pen")}</p>
{footer(1)}</div>"""


def page2(V):
    rows = "".join(f"""<tr><td class="c"><b>{v['n']}</b></td><td>{v['name']}</td><td class="c">{v['method']}</td><td class="c">{v['pages']}</td>
<td class="c">{v['boxes']}</td><td class="c">{v['per']}</td><td class="c">{v['sheets']}</td><td></td><td></td><td></td><td class="c">{box()}</td></tr>""" for v in V)
    return f"""<div class="page">{header("METHOD &amp; RESULTS SUMMARY", "Fill in the summary after Test 1 and Test 2.")}
<h3>6. Procedure</h3>
<ol class="proc"><li>Print one sheet of every version at 100%. <b>S</b> = single pass. <b>D</b> = manual flip: print side 1,
put the stack back in the tray turned over, print side 2. Mark the top edge of the stack with a pencil first.</li>
<li>Test 1 (pages 3 and 4): measure, check, and time each version with a stopwatch from blank sheet to finished passport.</li>
<li>Test 2 (page 5): press every small-set stamp inside its outline.</li>
<li>Abuse test: carry each passport in a pocket for an hour, stamp it 10 times, bend it, spill a drop of water on it.</li>
<li>Fill in the summary below, accept or reject each hypothesis, and sign the verdict on page 6.</li></ol>
<h3>7. Results summary</h3>
<table class="sum"><tr><th>#</th><th>Version</th><th>S/D</th><th>Pages</th><th>Boxes</th><th>Per sheet</th><th>Sheets for {RUN}</th>
<th>s / passport</th><th>Hours for {RUN}</th><th>Score /10</th><th>Pick</th></tr>{rows}</table>
<h3>8. Hypotheses: outcome</h3>
<table class="sum"><tr><th style="width:9%">#</th><th style="width:22%">Outcome</th><th>Evidence</th></tr>
{"".join(f"<tr><td class='c'><b>H{i}</b></td><td>{box('accept')} {box('reject')}</td><td></td></tr>" for i in range(1, 5))}</table>
{footer(2)}</div>"""


def test_pages(V):
    out = []
    for i, chunk in enumerate((V[:5], V[5:]), 3):
        label = "single-sided, one pass (S)" if i == 3 else "both sides, manual flip (D)"
        blocks = "".join(version_block(v) for v in chunk)
        out.append(f"""<div class="page p2">{header(f"TEST 1{'A' if i == 3 else 'B'} &middot; PRINT &amp; ASSEMBLY", f"Versions printed {label}. Expected values are printed; write what you measure.")}
<div class="vers">{blocks}</div>{footer(i)}</div>""")
    return "".join(out)


def verdict(V):
    picks = " ".join(box(v["n"]) for v in V)
    return f"""<div class="page">{header("9. CONCLUSION &amp; VERDICT", "To be signed by the test engineer and countersigned by a R.E.I.G.N. officer.")}
<h3>Selected version</h3>
<p class="intro big">{picks}</p>
<p class="intro big">Quantity to print: ________ &nbsp; Print method: {box("S")} {box("D")}</p>
<div class="kv"><div>Sheets of A4 to buy<span class="ln"></span></div><div>Toner cartridges needed<span class="ln"></span></div>
<div>Assembly hours (people x hours)<span class="ln"></span></div><div>Stamp pads / ink colours<span class="ln"></span></div></div>
<h3>Reasons</h3><div class="notes tall"></div>
<h3>Changes required before the production run</h3><div class="notes tall"></div>
<h3>Open issues</h3>
<table class="sum"><tr><th style="width:8%">#</th><th>Issue</th><th style="width:20%">Owner</th><th style="width:15%">Done</th></tr>
{"".join(f"<tr><td class='c'>{i}</td><td></td><td></td><td class='c'>{box()}</td></tr>" for i in range(1, 5))}</table>
<div class="sign"><div>Test engineer<span class="ln"></span><small>signature &amp; date</small></div>
<div>R.E.I.G.N. officer<span class="ln"></span><small>signature &amp; date</small></div></div>
<p class="stamp-here">OFFICIAL<br>SEAL</p>
{footer(TOTAL)}</div>"""


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@500;700;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
body{background:#444;font-family:'Archivo','DejaVu Sans',sans-serif;color:#000;font-size:9.5pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;background:#fff;margin:10px auto;padding:10mm 11mm 9mm;display:flex;flex-direction:column;position:relative;overflow:hidden}
header{display:flex;gap:4mm;align-items:center;border-bottom:3px solid #000;padding-bottom:3mm;margin-bottom:3mm}
header>div:nth-child(2){flex:1}
.crest{width:20mm;height:20mm;flex:none}
.org{font-weight:800;font-size:8pt;letter-spacing:.5px}
.dept{font-size:8pt;font-style:italic}
h1{font-family:'Archivo Black',sans-serif;font-size:16pt;line-height:1.1;margin-top:1mm}
.hsub{font-size:9pt;font-weight:700}
.form{border:2px solid #000;padding:1.5mm 2.5mm;font-size:7.5pt;font-weight:800;text-align:right;line-height:1.3}
h3{font-family:'Archivo Black',sans-serif;font-size:10.5pt;background:#000;color:#fff;padding:.6mm 2mm;margin:3.5mm 0 2mm}
.intro{margin-bottom:1.5mm;line-height:1.45}
.intro.big{font-size:12pt;font-weight:800}
.cb{display:inline-block;width:3.2mm;height:3.2mm;border:1.3px solid #000;vertical-align:-.5mm;margin-right:1mm}
.ln{display:inline-block;flex:1;border-bottom:1.3px solid #000;min-width:15mm;height:1em;margin:0 1.5mm}
.two{display:grid;grid-template-columns:1fr 1fr;gap:6mm}
.kv>div{display:flex;align-items:end;margin-bottom:2.6mm;font-weight:700}
.cal{display:flex;align-items:center;gap:3mm;margin:1mm 0 2mm}
.bar{width:100mm;height:5mm;border:1px solid #000;display:flex}
.bar i{flex:1;border-right:1px solid #000}.bar i:nth-child(odd){background:#000}
.cal span{font-weight:800}
.proc{margin-left:5mm;line-height:1.5}
table{border-collapse:collapse;width:100%}
.sum th,.sum td{border:1.2px solid #000;padding:1.6mm 1.5mm;text-align:left;font-size:8.5pt}
.sum th{background:#000;color:#fff;font-weight:800}
.sum td{height:7mm}
.vars td{height:auto;vertical-align:top;line-height:1.4}
.c{text-align:center}
footer{margin-top:auto;display:flex;justify-content:space-between;border-top:1.5px solid #000;padding-top:1.5mm;font-size:7pt;font-style:italic}
/* page 2 */
.p2{padding-top:8mm}
.vers{display:grid;grid-template-columns:1fr 1fr;gap:2.5mm;flex:1}
.ver{border:1.8px solid #000;padding:1.8mm;display:flex;flex-direction:column;font-size:6.6pt}
.ver:last-child{grid-column:span 2}
.vhead{display:grid;grid-template-columns:auto 1fr;gap:0 2mm;align-items:center;border-bottom:1.5px solid #000;padding-bottom:1mm;margin-bottom:.8mm}
.vn{font-family:'Archivo Black',sans-serif;font-size:13pt;background:#000;color:#fff;width:7mm;text-align:center;grid-row:span 2}
.vhead b{font-size:8.5pt}.vhead small{display:block;font-size:6pt;color:#444}
.spec{grid-column:2;font-size:6.3pt;font-weight:700}
.chk td{padding:.35mm .5mm;border-bottom:.6px solid #999;vertical-align:top}
.chk .pf{white-space:nowrap;width:1%;font-size:6.3pt}
.note{font-size:6pt;color:#333}
.chk .cb{width:2.5mm;height:2.5mm;margin-right:.6mm}
.meas{display:flex;flex-wrap:wrap;gap:0 2mm;margin-top:1mm;font-weight:700}
.meas>div{display:flex;align-items:end;flex:1 1 40%;margin-top:.8mm}
.score{margin-top:1mm;font-weight:700}
.score .cb{width:2.5mm;height:2.5mm}
.sc{display:inline-block;border:1px solid #000;width:3.4mm;text-align:center;font-size:5.5pt;margin-left:.4mm}
.notes{border:1.2px solid #000;flex:1;min-height:7mm;margin-top:1mm;padding:.6mm 1mm;font-size:6.3pt;font-weight:700;color:#555}
.notes.tall{min-height:30mm;flex:none}
/* page 3 */
.sgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:2mm}
.sgrid.six{grid-template-columns:repeat(6,1fr)}
.st{border:1px dashed #999;padding:2mm 1mm;display:flex;flex-direction:column;align-items:center;gap:1mm;font-weight:800}
.ring{width:22mm;height:22mm;border:1.5px dashed #000;border-radius:50%}
.sq{width:17mm;height:17mm;border:1.5px dashed #000}
.mini{font-size:6pt;font-weight:600;text-align:center;line-height:1.6}
.mini .cb{width:2.4mm;height:2.4mm}
.tight td{padding:1mm .5mm;border-bottom:.6px solid #999}
/* page 4 */
.sign{display:grid;grid-template-columns:1fr 1fr;gap:10mm;margin-top:8mm}
.sign>div{display:flex;flex-wrap:wrap;align-items:end;font-weight:800}
.sign small{width:100%;text-align:right;font-size:7pt;font-weight:600;margin-top:1mm}
.stamp-here{width:32mm;height:32mm;border:2px dashed #000;border-radius:50%;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;color:#888;margin:7mm auto 0}
@media print{body{background:none}.page{margin:0;break-after:page}@page{size:A4;margin:0}}
"""

if __name__ == "__main__":
    V = measure()
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Passport Test Report</title><style>{CSS}</style></head>'
            f"<body>{page1(V)}{page2(V)}{test_pages(V)}{stamp_page()}{verdict(V)}</body></html>")
    out = os.path.join(HERE, "ecotopia_passport_test_report.html")
    open(out, "w").write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        p = b.new_page()
        p.goto("file://" + out)
        p.wait_for_load_state("networkidle")
        p.emulate_media(media="print")
        p.pdf(path=out[:-5] + ".pdf", prefer_css_page_size=True, print_background=True)
        b.close()
    print("wrote", out[:-5] + ".pdf")

"""Personalised Citizen Passports: format 05 (pocket fold-up). One A4 = one whole 8-page passport, single-sided.

Pages: 1 cover, 2 citizen (name / ministry / debt), 3 citizenship status (stamp boxes), 4 how it works,
5 the night + ministries, 6 credits 1-15, 7 credits 16-30, 8 final balance.

Reads the citizen export (sheet "passport info": Name, Applied, Carbon debt, Ministry, ...) and writes to out/
(git-ignored, personal data):

  passports.pdf         one A4 per citizen, sorted by ministry then name
  passports_blank.pdf   blank passports for walk-ins (fields left empty)
  ministry_lists.pdf    one A4 per ministry: who is in it, debt, tick box (for the inburgering desk)

Run: python3 make_passport_batch.py ["../Citizens export and quests.xlsx"] [--blanks N]
Print at 100% / actual size, single-sided, A4 landscape. Slit the middle line, then fold.
"""
from letters import letter
import html
import os
import re
import sys

import make_passport_options as M
from xlsx_read import read

HERE = M.HERE
OUT = os.path.join(HERE, "out")
SRC = os.path.join(HERE, "..", "Citizens export and quests.xlsx")
UNPLACED = "Not yet placed"
K = 0.72  # same scale as make_passport_options.v05
esc = html.escape

MINI_ROW = '<div class="mrow">' + "".join(
    f'<div class="mi"><svg viewBox="60 64 80 80">{M.ICONS[n]}</svg><span>{n.title()}</span></div>' for n in M.ORDER) + "</div>"

NIGHT = f"""<h2>THE NIGHT</h2><div class="night">
<div class="t"><b>20:30</b><div><i>Inburgering.</i> You are processed at the door and receive this passport, your ministry and your first quest cards.</div></div>
<div class="t"><b>21:00</b><div><i>The game.</i> Work off your debt, serve your ministry, visit the stations.</div></div>
<div class="t"><b>23:30</b><div><i>The Grand Assembly.</i> R.E.I.G.N. arrives. Only the 3 most worthy ministries may compete for Ascension.</div></div>
<div class="t"><b>after</b><div><i>The party.</i> The game is over. Dance until 03:00.</div></div>
</div><h2>THE TEN MINISTRIES</h2>{MINI_ROW}"""

INBURGERING = """<h2>CITIZENSHIP STATUS</h2>
<div class="stamps4">
<div class="sbox wide"><span>INTERROGATION</span></div>
<div class="sbox wide"><span>CORRECTED &middot; CARBON CONFESSIONS</span></div>
<div class="sbox"><span>VERDICT</span></div><div class="sbox"><span>RECYCLING</span></div></div>
<div class="note">Your status is reviewed. Continuously.</div>"""

FINAL = """<h2>FINAL BALANCE</h2>
<div class="calc">
<div class="crow2"><span>Carbon debt (page 2)</span><b>&minus;<span class="line short"></span></b></div>
<div class="crow2"><span>+ Stamps (p. 6, 7) &times; 100</span><b>+<span class="line short"></span></b></div>
<div class="crow2 tot"><span>FINAL BALANCE</span><b><span class="line short"></span>CC</b></div></div>
<div class="field">Counted by<span class="line"></span></div>
<div class="fin">Everything above 0 counts for your ministry.<br><b>Only the top 3 ministries earn the privilege<br>to compete for Ascension.</b></div>
<div class="fine">Nothing outlives the celebration.<br>Every record returns to nature on 19.12.</div>
<div class="motto end">R.E.I.G.N. decides,<br>so that citizens are free.</div>"""

OZONE = """<div class="ozone big">SAFE WORD<span>OZONE</span><small>Say it, and all play stops at once.<br>Step out any time: tell an official.</small></div>"""


def cover(c):
    """Page 1 with the registration number under CITIZEN PASSPORT (blank passports: a line to fill in)."""
    no = f'{c["no"]:03d}' if c.get("no") else '<span class="line short"></span>'
    a = '<div class="title">CITIZEN<br>PASSPORT</div>'
    assert a in M.COVER
    return M.COVER.replace(a, a + f'<div class="cno">No.&nbsp;{no}</div>', 1)


def how(c):
    """Page 4: a personal letter from the citizen's own ministry (letters.py), then the safe word."""
    first = esc(c["name"].split()[0]) if c["name"] else "citizen"
    debt = f'&minus;{c["debt"]}&nbsp;CC' if c["debt"] else '&minus;<span class="line short"></span>CC'
    title, body = letter(c["ministry"], first, debt)
    return f'<h2>{title}</h2><div class="howto">{body}</div>' + OZONE

EXTRA_CSS = """
.pmin{margin-top:2.5mm}.pmin svg{width:8mm;height:8mm}  /* icon inline, no label: more room for ENTRY */
.cno{font-family:'Archivo Black',sans-serif;font-size:14pt;letter-spacing:3px;text-align:center;margin-top:1.5mm}
.pno{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid #000;margin-top:2.5mm;text-align:left;color:#000}
.pno span{font-size:9pt;font-weight:800;letter-spacing:.5px}.pno b{font-family:'Archivo Black',sans-serif;font-size:17pt;letter-spacing:2px}  /* registration number, prominent */
.howto .dear{font-family:'Archivo Black',sans-serif;font-size:1.1em;margin-bottom:1.2mm}
.howto{flex:none}.ozone.big{margin-top:auto;background:#000;color:#fff;border:0;padding:1.8mm 2mm;font-size:8.5pt;letter-spacing:1px}
.ozone.big span{font-size:22pt;letter-spacing:5px;margin:0 0 1mm;color:#fff}.ozone.big small{font-size:8.5pt;letter-spacing:0;margin-top:0;font-weight:700}  /* safety: big, inverted */
.howto{font-size:9pt;line-height:1.25}.howto p{margin:0 0 1.8mm}  /* short REIGN lines: bigger */
.fine{font-size:8pt;font-style:italic;text-align:center;margin-top:3mm}  /* capsule B riddle: 19.12 */
.howto u.k,.howto b u.k{text-decoration:underline;text-decoration-thickness:1.8px;text-underline-offset:1.4px;text-decoration-skip-ink:none}  /* capsule B riddle: underlined digits = code 2 1 0 3 2 3 */
.pname{font-family:'Archivo Black',sans-serif;line-height:1.05;border-bottom:2px solid #000;padding-bottom:1mm;margin-top:3mm;
 overflow:hidden;overflow-wrap:anywhere}
.plabel{font-weight:800;color:#555;margin-top:3mm}
.pmin{display:flex;align-items:center;gap:2mm;font-weight:800;margin-top:1mm}
.pmin svg{flex:none}
.pno{font-weight:700;color:#555;text-align:right;margin-top:1mm}
.howto p b,.night b{font-weight:900}
.howto{font-weight:600;line-height:1.22}
.night{display:flex;flex-direction:column;flex:1;justify-content:space-evenly;font-weight:600;line-height:1.22}
.night .t{display:flex;gap:2mm}
.night .t>b{font-family:'Archivo Black',sans-serif;flex:none;width:11mm}
.night i{font-style:normal;font-weight:900}
.mrow{display:grid;grid-template-columns:repeat(5,1fr);gap:1.5mm .5mm;text-align:center;font-weight:800}
.mi{display:flex;flex-direction:column;align-items:center;gap:.4mm}
.verdict{border:2px solid #000;font-weight:800}
.verdict .vh{background:#000;color:#fff;text-align:center;font-family:'Archivo Black',sans-serif}
.verdict .v{display:flex;align-items:center}
.cb{display:inline-block;border:1.5px solid #000;flex:none}
.entry{flex:1;border:2px dashed #000;display:flex;align-items:center;justify-content:center;color:#999}
.note{text-align:center;font-weight:700;font-style:italic}
.stamps4{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1.6fr 1fr 1fr;gap:2mm;margin-top:3mm}
.sbox.entry{flex:1;margin-top:3mm}
.sbox.wide{grid-column:1/-1}
.sbox{border:2px dashed #000;position:relative}
.sbox span{position:absolute;bottom:.6mm;left:0;right:0;text-align:center;font-size:7.5pt;font-weight:800;color:#000}
.calc{border:2.5px solid #000}
.crow2{display:flex;align-items:end;justify-content:space-between;font-weight:800}
.crow2 b{display:flex;align-items:end;font-family:'Archivo Black',sans-serif}
.crow2.tot{border-top:2px solid #000}
.motto.end{text-align:center}
.fin{margin-top:auto;text-align:center;font-weight:700;line-height:1.3}
.sqgrid{flex:1;display:grid;grid-template-columns:repeat(3,15.5mm);grid-auto-rows:15.5mm;gap:.8mm;
 justify-content:center;align-content:center}
.box.sq span{font-size:6pt;top:.3mm;left:.5mm}
/* no cut line on the slit */
.zine .pg:nth-child(6),.zine .pg:nth-child(7){border-top:none}
/* no space between pages: page frames touch */
.zine .pg{padding:0;border:none!important}
/* white space between page 8 and page 1 (the cover's spine), per test print 2026-11-27.
   zine children: 1=p5 2=p4 3=p3 (top row, rotated 180) 4=p2 ; 5=p6 6=p7 7=p8 8=p1 */
.zine .pg:nth-child(7){padding-right:2mm}
.zine .pg:nth-child(8){padding-left:2mm}
.zine{grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:repeat(2,minmax(0,1fr));flex:1 1 0;min-height:0;overflow:hidden}
.zine .pg{min-height:0;min-width:0}
/* ministry list sheets */
.list{flex:1;display:flex;flex-direction:column;border:3px solid #000;padding:8mm}
.lhead{display:flex;align-items:center;gap:6mm;border-bottom:4px solid #000;padding-bottom:4mm;margin-bottom:4mm}
.lhead svg{width:26mm;height:26mm;flex:none}
.lhead .t{font-family:'Archivo Black',sans-serif;font-size:30pt;line-height:1}
.lhead .s{font-weight:700;font-size:13pt;margin-top:1.5mm}
table{border-collapse:collapse;width:100%;font-size:12pt}
td,th{border-bottom:1px solid #000;padding:1.6mm 2mm;text-align:left}
th{font-weight:800;border-bottom:2px solid #000}
td.tick{width:9mm}td.tick span{display:inline-block;width:5mm;height:5mm;border:1.5px solid #000}
td.num{width:14mm;color:#555;font-weight:700}td.debt{width:22mm;font-weight:800}
"""

BASE_EXTRA = """
.pname{font-size:20pt}
.plabel{font-size:12pt}
.pmin{font-size:14pt}.pmin svg{width:11mm;height:11mm}
.pno{font-size:12pt}
.howto{font-size:11.8pt}.howto p{margin-bottom:1.5mm}
.night{font-size:12.5pt}.night .t>b{font-size:12pt}
.mrow{font-size:9.5pt}.mi svg{width:10mm;height:10mm}
.verdict{margin:4mm 0 3mm;font-size:11pt}.verdict .vh{font-size:10pt;padding:.6mm 0}
.verdict .v{gap:2.5mm;padding:1.5mm 3mm}.cb{width:4.5mm;height:4.5mm}
.entry{font-size:10pt}.note{font-size:12pt;margin-top:2mm}
.calc{margin:3mm 0 5mm;padding:1.5mm 3mm}.crow2{font-size:12pt;padding:5mm 0;gap:2mm}.fin{font-size:11pt}
.crow2.tot{font-size:15pt}.crow2 .line.short{width:22mm}
.motto.end{font-size:10pt;margin-top:3mm}
.ozone{padding:1.5mm}.ozone span{font-size:22pt}
"""


BOX = 15.5  # mm, square credit box: the credit stamps are 15 x 15 mm
COLS, ROWS = 3, 5


def ledger(start):
    boxes = "".join(f'<div class="box sq"><span>{start + i}</span></div>' for i in range(COLS * ROWS))
    return f'<h2>CREDITS</h2><div class="sqgrid">{boxes}</div>'  # the sum is done on page 8


def icon(ministry):
    key = ministry.replace("Ministry of ", "").strip().upper()
    return f'<svg viewBox="60 64 80 80">{M.ICONS[key]}</svg>' if key in M.ICONS else ""


def name_style(name):
    # 20pt fits ~17 characters on one line; longer names shrink to stay on one line (room for ENTRY),
    # down to 12pt, after which they wrap
    n = len(name)
    return "" if n <= 17 else f' style="font-size:{max(20 * 17 / n, 12) * K:.1f}pt"'


def citizen_page(c):
    """Page 2. c = dict(name, ministry, debt, no); empty values give blank lines to fill in by hand."""
    if c["name"]:
        name = f'<div class="plabel">Name</div><div class="pname"{name_style(c["name"])}>{esc(c["name"])}</div>'
    else:
        name = '<div class="field">Name<span class="line"></span></div>'
    if c["ministry"] and c["ministry"] != UNPLACED:
        mn = f'<div class="pmin">{icon(c["ministry"])}<span>{esc(c["ministry"])}</span></div>'
    else:
        mn = '<div class="field">Ministry<span class="line"></span></div>'
    amount = f'&minus;{c["debt"]}&nbsp;CC' if c["debt"] else '&minus;<span class="line short"></span>CC'
    no = ""  # registration number is on the cover (page 1); page 2 keeps the room for the ENTRY stamp
    return (f'<h2>CITIZEN</h2>{name}{mn}'
            f'<div class="startbox"><div>CARBON DEBT</div><div class="amount">{amount}</div></div>{no}'
            '<div class="sbox entry"><span>ENTRY</span></div>'
            '<div class="field">Processed at<span class="line"></span></div>'
            '<div class="field">Officer<span class="line"></span></div>')


def pages(c):
    # entrance (2-3) · the game (4-5, a facing spread) · credits (6-7, a facing spread) · final balance (8)
    return {1: cover(c), 2: citizen_page(c), 3: INBURGERING, 4: how(c), 5: NIGHT,
            6: ledger(1), 7: ledger(1 + COLS * ROWS), 8: FINAL}


def passport(c):
    # single-sided fold-up; the "cut only this middle line" label is left out
    return M.zine(pages(c)).replace('<div class="cut"><b>&#9986; cut only this middle line</b></div>', "")


def document(title, sheets, orient="landscape", k=K, margin=5):
    M.MARGIN = margin  # 5 mm: the Brother HL-2150N cannot print the outer ~4-5 mm of the sheet
    d = M.doc(title, sheets, orient, k)
    d = d.replace("</style>", M.scale_css(BASE_EXTRA, k) + EXTRA_CSS + "</style>", 1)
    return re.sub(r"color:#(?:555|666|777|888|999)\b", "color:#000", d)  # no grey text: unreadable on the laser print


def load(path):
    rows = read(path)["passport info"]
    head = [h.strip().lower() for h in rows[0]]
    col = {k: head.index(k) for k in ("name", "carbon debt", "ministry")}
    out = []
    for r in rows[1:]:
        r = r + [""] * (len(head) - len(r))
        name = re.sub(r"\s+", " ", r[col["name"]]).strip()
        if not name:
            continue
        debt = re.sub(r"[^\d]", "", r[col["carbon debt"]])
        out.append({"name": name, "ministry": r[col["ministry"]].strip() or UNPLACED, "debt": debt})
    order = {f"Ministry of {n.title()}": i for i, n in enumerate(M.ORDER)}
    out.sort(key=lambda c: (order.get(c["ministry"], 99), c["name"].casefold()))
    for i, c in enumerate(out, 1):
        c["no"] = i
    return out


def groups(citizens):
    g = {}
    for c in citizens:
        g.setdefault(c["ministry"], []).append(c)
    return g


def passports(citizens):
    sheets = [(f'{c["no"]:03d} &middot; {esc(c["name"])} &middot; {esc(c["ministry"])}', passport(c)) for c in citizens]
    return document("Citizen passports (personalised)", sheets)


def blanks(n):
    blank = passport({"name": "", "ministry": "", "debt": ""})
    return document("Citizen passports (blank, walk-ins)", [(f"Walk-in blank {i + 1}", blank) for i in range(n)])


def lists(citizens):
    sheets = []
    for m, cs in groups(citizens).items():
        rows = "".join(f'<tr><td class="tick"><span></span></td><td class="num">{c["no"]:03d}</td><td>{esc(c["name"])}</td>'
                       f'<td class="debt">&minus;{c["debt"]} CC</td></tr>' for c in cs)
        sub = "Assign a ministry at the door and write it on the passport." if m == UNPLACED else "Tick each citizen when their passport is handed over."
        body = (f'<div class="list"><div class="lhead">{icon(m)}<div><div class="t">{esc(m)}</div>'
                f'<div class="s">{len(cs)} citizens &middot; {sub}</div></div></div>'
                f'<table><tr><th></th><th>Reg. no.</th><th>Name</th><th>Debt</th></tr>{rows}</table></div>')
        sheets.append((m, body))
    return document("Ministry lists (inburgering desk)", sheets, "portrait", 1, margin=5)


def render(paths):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page()
        page.set_default_timeout(300_000)
        for p in paths:
            page.goto("file://" + p, wait_until="load")
            page.evaluate("document.fonts.ready.then(() => true)")
            page.emulate_media(media="print")
            page.pdf(path=p[:-5] + ".pdf", prefer_css_page_size=True, print_background=True)
        b.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    nblank = 40
    if "--blanks" in args:
        i = args.index("--blanks")
        nblank = int(args[i + 1])
        del args[i:i + 2]
    src = args[0] if args else SRC
    citizens = load(src)
    os.makedirs(OUT, exist_ok=True)
    files = {"passports": passports(citizens), "passports_blank": blanks(nblank), "ministry_lists": lists(citizens)}
    paths = []
    for name, content in files.items():
        p = os.path.join(OUT, name + ".html")
        open(p, "w").write(content)
        paths.append(p)
    render(paths)
    for m, cs in groups(citizens).items():
        print(f"{len(cs):4d}  {m}")
    print(f"{len(citizens)} passports + {nblank} blanks (1 A4 each) -> {OUT}")

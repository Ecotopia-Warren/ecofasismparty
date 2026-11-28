#!/usr/bin/env python3
"""Ecotopia gate kit: every printable the gate and the crew need on the night (Sat 28 Nov 2026).

  1. Ministry scoreboard: A3 split into 2 A4 portrait halves (standings + Ascension ladder),
     stand-alone halves, no gluing. Also out/scoreboard_A3.pdf for an A3 printer.
     Secret tally sheet (crew only): handed-in cards per ISSUING ministry (back of card).
  2. Card tray labels: 10 ministries + Resistance (kept cards, sorted by the BACK),
     7 chain next-step stacks (H2-H4, D2-D3, S2-S3), plus 6 gate stack labels.
  3. Data centre labels 1-7 (+1 spare): R.E.I.G.N. message to memorise + riddle card slots.
  4. Shooting range operator brief (A5, 2 per A4 landscape).
  5. Night run-of-show (crew, A4).

Output: props/gate_kit/PRINT_ALL_gate_kit.pdf (all A4, print at 100 % / actual size)
        props/gate_kit/out/  (one html + pdf per section)
Style: black + one red accent (#c8102e), Archivo / Archivo Black, B&W safe (red never carries
meaning alone). Data is imported, not retyped: ministry icons (passport), chains (chains.py),
range scoring (make_targets.py). PDFs via Playwright/Chromium, fonts from Google Fonts (online).

Usage: python3 props/gate_kit/make_gate_kit.py
"""
import html
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
sys.path.insert(0, os.path.join(ROOT, "passport_v2"))
sys.path.insert(0, os.path.join(ROOT, "props", "shooting_range"))
import make_passport_options as M  # noqa: E402  ministry icons, same as passport page 5
from chains import CHAINS, ROLES  # noqa: E402
ROLE_REWARD = {r[0]: r[3].split('?')[-1].strip() for r in ROLES}  # H0: '3', S0: '2'
import make_targets as T  # noqa: E402  range scoring constants (single source of truth)

INK, RED = "#111111", "#c8102e"
ORDER = M.ORDER  # PURITY RADIANCE BREATH FLOW LIGHT INDUSTRY HUMUS SERVICE VIGILANCE JOY (CANON order)
RESIST_SVG = "file://" + os.path.join(ROOT, "stamps", "resistance_ankle_stamp.svg")
FONTS = ("@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&"
         "family=Archivo:ital,wght@0,500;0,700;0,800;1,700&display=swap');")
E = html.escape


def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="60 64 80 80">{M.ICONS[name]}</svg>'


def resist(cls="ic"):
    # <img>, not inline: the SVG has id="textPathTop", duplicate ids break the ring text
    return f'<img class="{cls}" src="{RESIST_SVG}" alt="">'


BASE = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Archivo', 'DejaVu Sans', sans-serif; color: {INK}; background: #fff;
  -webkit-print-color-adjust: exact; print-color-adjust: exact }}
.pg {{ position: relative; overflow: hidden; page-break-after: always; background: #fff }}
.blk {{ font-family: 'Archivo Black', sans-serif; font-weight: 400 }}
.red {{ color: {RED} }}
.kick {{ font-family: 'Archivo Black', sans-serif; letter-spacing: 2px; color: {RED} }}
.crew {{ display: inline-block; border: .5mm solid {INK}; padding: .3mm 1.5mm; font-weight: 800; letter-spacing: 1px }}
"""


def doc(title, css, body, size):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{E(title)}</title>'
            f'<style>{FONTS}@page {{ size: {size}; margin: 0 }}{BASE}{css}</style></head><body>{body}</body></html>')


# =================================================================== 1. SCOREBOARD
HOURS = ["21:00<br>&ndash;22:00", "22:00<br>&ndash;23:00", "23:00<br>&ndash;FINAL"]

SCORE_CSS = """
.pg { width: 210mm; height: 297mm; padding: 9mm 8mm 8mm }
.hd { text-align: center; border-bottom: 1.2mm solid #111; padding-bottom: 2.5mm; margin-bottom: 3mm }
.hd .kick { font-size: 10pt }
.hd h1 { font-family: 'Archivo Black', sans-serif; font-weight: 400; font-size: 34pt; line-height: .98; margin: 1mm 0 1.2mm }
.hd .sub { font-weight: 700; font-style: italic; font-size: 11pt }
table.sb { width: 100%; border-collapse: collapse; table-layout: fixed }
table.sb th { font-family: 'Archivo Black', sans-serif; font-weight: 400; font-size: 10.5pt; line-height: 1.05;
  padding: 1.2mm .5mm; border: .6mm solid #111; background: #111; color: #fff }
table.sb th.tot { background: #c8102e; border-color: #111 }
table.sb td { border: .6mm solid #111; height: 21.2mm; vertical-align: middle }
table.sb td.m { padding: 0 1.5mm }
.mrow { display: flex; align-items: center; gap: 2mm }
.mrow .ic { width: 13mm; height: 13mm; flex: none }
.mrow .nm { font-family: 'Archivo Black', sans-serif; font-size: 17pt; line-height: 1 }
.mrow .of { display: block; font-family: 'Archivo'; font-weight: 800; font-size: 7pt; letter-spacing: 1px }
table.sb td.t { border-width: 1.1mm .6mm }
table.sb td.tot { border: 1.4mm solid #c8102e; background: #fff }
.ft { margin-top: 2.5mm; display: flex; justify-content: space-between; font-size: 9pt; font-weight: 700 }
.ft b { font-family: 'Archivo Black', sans-serif; font-weight: 400 }
/* right half: the ladder */
.lad { display: flex; flex-direction: column; gap: 0 }
.rk { display: flex; align-items: stretch; height: 18.6mm; border: .6mm solid #111; border-top-width: 0 }
.rk:first-child, .cut + .rk { border-top-width: .6mm }
.rk .n { width: 18mm; flex: none; background: #111; color: #fff; font-family: 'Archivo Black', sans-serif;
  font-size: 22pt; display: flex; align-items: center; justify-content: center }
.rk .w { flex: 1; position: relative }
.rk .w span, .rk .s span { position: absolute; left: 2mm; top: 1mm; font-size: 6.5pt; font-weight: 800; letter-spacing: 1px }
.rk .s { width: 38mm; flex: none; border-left: .6mm solid #111; position: relative }
.rk.top .n { background: #c8102e }
.cut { margin: 1.6mm 0; position: relative; height: 9mm; display: flex; align-items: center }
.cut:before { content: ""; position: absolute; left: 0; right: 0; top: 50%; border-top: 1.6mm dashed #c8102e; transform: translateY(-50%) }
.cut span { position: relative; margin: 0 auto; background: #fff; padding: 0 2.5mm; font-family: 'Archivo Black', sans-serif;
  font-size: 11pt; letter-spacing: 1px; text-align: center; line-height: 1.05 }
.rules { margin-top: 3mm; border: 1mm solid #111; padding: 2.5mm 3mm; font-size: 10pt; font-weight: 700; line-height: 1.3 }
.rules b { font-family: 'Archivo Black', sans-serif; font-weight: 400 }
"""


def scoreboard_left():
    rows = "".join(
        f'<tr><td class="m"><div class="mrow">{icon(n)}<div><span class="of">MINISTRY OF</span>'
        f'<span class="nm">{n.title()}</span></div></div></td><td class="t"></td><td class="t"></td>'
        f'<td class="t"></td><td class="tot"></td></tr>' for n in ORDER)
    head = "".join(f"<th>{h}</th>" for h in HOURS)
    return f"""<div class="pg">
<div class="hd"><div class="kick">R.E.I.G.N. &middot; OFFICIAL COUNT &middot; SHEET 1 OF 2</div>
<h1>THE STANDING<br>OF THE MINISTRIES</h1>
<div class="sub">Every stamp was counted, including yours.</div></div>
<table class="sb"><colgroup><col style="width:33%"><col style="width:17%"><col style="width:17%"><col style="width:17%"><col style="width:16%"></colgroup>
<tr><th style="text-align:left;padding-left:2mm">MINISTRY</th>{head}<th class="tot">TOTAL</th></tr>{rows}</table>
<div class="ft"><span><b>1</b> = one credit stamp = <b>100 CC</b>. Officials write the count each hour.</span><span>Questions are welcome.</span></div>
</div>"""


def scoreboard_right():
    rk = []
    for i in range(1, 11):
        rk.append(f'<div class="rk{" top" if i <= 3 else ""}"><div class="n">{i}</div>'
                  f'<div class="w"><span>MINISTRY</span></div><div class="s"><span>TOTAL</span></div></div>')
        if i == 3:
            rk.append('<div class="cut"><span>ASCENSION LINE<br><small style="font-size:7.5pt">only the three above may compete</small></span></div>')
    # .cut sits between rank 3 and 4: rank 4 needs its own top border again
    ladder = "".join(rk).replace('<div class="cut">', '<div class="cut">', 1)
    return f"""<div class="pg">
<div class="hd"><div class="kick">R.E.I.G.N. &middot; OFFICIAL COUNT &middot; SHEET 2 OF 2</div>
<h1>ASCENSION<br>23:30</h1>
<div class="sub">At the Grand Assembly only the three most worthy ministries may compete.</div></div>
<div class="lad">{ladder}</div>
<div class="rules"><b>Ascension is a privilege, not a right.</b> The three ministries above the line bring a song,
a chant, a formation, or more. The other seven are thanked for their devotion, and watch.
Every credit above zero counts for your ministry.</div>
</div>"""


SECRET_ROWS = ORDER + ["RESISTANCE"]
SECRET_CSS = """
.pg { width: 210mm; height: 297mm; padding: 9mm 9mm 8mm }
.top { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1mm solid #111; padding-bottom: 2mm }
.top h1 { font-family: 'Archivo Black', sans-serif; font-weight: 400; font-size: 20pt; line-height: 1 }
.top .crew { font-size: 10pt; background: #c8102e; color: #fff; border-color: #c8102e }
.how { font-size: 8.6pt; font-weight: 700; line-height: 1.3; margin: 2mm 0 2.5mm }
.how b { font-weight: 800 }
table.st { width: 100%; border-collapse: collapse; table-layout: fixed }
table.st th { font-weight: 800; font-size: 7.5pt; letter-spacing: .8px; text-align: left; padding: 1mm 1.2mm; border-bottom: .8mm solid #111 }
table.st td { border-bottom: .35mm solid #111; height: 20.6mm; vertical-align: middle; padding: 0 1.2mm }
table.st td.tl { border-left: .35mm solid #111; border-right: .35mm solid #111 }
table.st td.tot, table.st td.rk { border-right: .35mm solid #111 }
table.st tr.res td { border-top: .8mm solid #111 }
.mr { display: flex; align-items: center; gap: 1.6mm; font-family: 'Archivo Black', sans-serif; font-size: 11.5pt }
.mr .ic { width: 9mm; height: 9mm; flex: none }
.note { font-size: 6.5pt; font-weight: 700; font-family: 'Archivo' }
.foot { margin-top: 2.2mm; font-size: 8pt; font-weight: 700; line-height: 1.3 }
"""


SEAL_CSS = """
.blk3 { display: grid; grid-template-columns: 1fr 1fr 1fr; height: 100% }
.blk3 > div { border-left: .35mm solid #111; position: relative }
.blk3 > div:first-child { border-left: 0 }
.blk3 .sum { position: absolute; right: 0; bottom: 0; width: 10mm; height: 7mm; border-left: .35mm solid #111; border-top: .35mm solid #111 }
table.st td.tl { padding: 0 }
"""


def seal_sheet():
    rows = "".join(f'<tr><td><div class="mr">{icon(n)}<div>{n.title()}</div></div></td><td class="tl"><div class="blk3">'
                   + '<div><span class="sum"></span></div>' * 3 + '</div></td><td class="tot"></td></tr>' for n in ORDER)
    return f"""<div class="pg">
<div class="top"><h1>STAMPS BY SEAL<br>(FRONT)</h1><span class="crew">GATE &middot; FEEDS THE SCOREBOARD</span></div>
<div class="how">For every card handed in: look at the <b>SEAL on the FRONT</b> (&ldquo;this quest scores for&rdquo;) and put
<b>one stroke per stamp</b> the citizen gets (1, 2, 3 or a chain finale&rsquo;s 5) in that ministry&rsquo;s row, in the block of this hour.
On the hour: add up the block, write the sum in its small box, copy it to the scoreboard. Resistance never scores here.</div>
<table class="st"><colgroup><col style="width:24%"><col style="width:66%"><col style="width:10%"></colgroup>
<tr><th>SEAL (front)</th><th><div class="blk3" style="height:auto"><div>21:00&ndash;22:00</div><div>&nbsp;22:00&ndash;23:00</div><div>&nbsp;23:00&ndash;FINAL</div></div></th><th>TOTAL</th></tr>
{rows}</table>
<div class="foot">Station stamps (range, interrogation, ...): counted here too? <b>TBD</b>. Not the issuer count: that is the other sheet.</div>
</div>"""


def secret_sheet():
    rows = []
    for n in SECRET_ROWS:
        res = n == "RESISTANCE"
        ic = resist() if res else icon(n)
        label = "Resistance" if res else n.title()
        extra = '<div class="note">rank it? TBD</div>' if res else ""
        rows.append(f'<tr class="{"res" if res else ""}"><td><div class="mr">{ic}<div>{label}{extra}</div></div></td>'
                    f'<td class="tl"></td><td class="tot"></td><td class="rk"></td></tr>')
    return f"""<div class="pg">
<div class="top"><h1>CARD RETURNS<br>BY ISSUER</h1><span class="crew">CREW ONLY &middot; KEEP FACE DOWN</span></div>
<div class="how">Count the <b>BACK</b> of every handed-in card: <b>&ldquo;A QUEST OF THE MINISTRY OF X&rdquo;</b> (or RESISTANCE).
<b>Not</b> the seal on the front: the seal is the public scoreboard. One stroke per card, also for reissued cards.
Fill in TOTAL and RANK at the final count; the winner gets the unannounced award (QUEST_SYSTEM: secret victory).
Never show or say this count to guests.</div>
<table class="st"><colgroup><col style="width:27%"><col style="width:55%"><col style="width:9%"><col style="width:9%"></colgroup>
<tr><th>ISSUED BY (back)</th><th>STROKES &nbsp;(one per card, groups of five)</th><th>TOTAL</th><th>RANK</th></tr>
{"".join(rows)}</table>
<div class="foot">Ties: TBD. Announced when, and by whom: TBD.</div>
</div>"""


# =================================================================== 2. TRAY LABELS
LW, LH, LC, LR = 95, 65, 2, 4  # mm, 2 x 4 per A4 portrait, butted, crop marks outside

LABEL_CSS = f"""
.pg {{ width: 210mm; height: 297mm }}
.marks {{ position: absolute; left: 0; top: 0 }}
.grid {{ position: absolute; display: grid; grid-template-columns: repeat({LC}, {LW}mm); grid-auto-rows: {LH}mm }}
.lb {{ border: .15mm solid #999; padding: 3.5mm 4mm; display: flex; flex-direction: column; overflow: hidden }}
.bar {{ background: #111; color: #fff; font-weight: 800; font-size: 7.5pt; letter-spacing: 1.5px; text-align: center; padding: .8mm 1mm }}
.bar.red {{ background: #c8102e }}
.mid {{ flex: 1; display: flex; align-items: center; gap: 3.5mm; min-height: 0 }}
.mid .ic {{ width: 25mm; height: 25mm; flex: none }}
.mid .of {{ font-weight: 800; font-size: 8pt; letter-spacing: 1.2px }}
.mid .nm {{ font-family: 'Archivo Black', sans-serif; font-size: 24pt; line-height: 1 }}
.mid .id {{ font-family: 'Archivo Black', sans-serif; font-size: 40pt; line-height: .9 }}
.mid .ch {{ font-family: 'Archivo Black', sans-serif; font-size: 12pt; line-height: 1.05 }}
.mid .ch small {{ display: block; font-family: 'Archivo'; font-weight: 800; font-size: 8.5pt; letter-spacing: .8px; margin-top: .8mm }}
.mid .is {{ display: flex; align-items: center; gap: 1.2mm; font-weight: 800; font-size: 8.5pt; margin-top: 1.4mm }}
.mid .is .ic {{ width: 7mm; height: 7mm }}
.inf {{ font-size: 7.4pt; font-weight: 700; line-height: 1.25; border-top: .4mm solid #111; padding-top: 1.2mm }}
.inf b {{ font-weight: 800 }}
.lb.quiet .mid .ic {{ width: 15mm; height: 15mm }}
.lb.quiet .mid .nm {{ font-size: 18pt }}
.lb.blank .mid {{ border: .4mm dashed #999; margin: 2mm 0; justify-content: center; color: #999; font-weight: 800; font-size: 8pt }}
"""


def crop_marks(x0, y0, w, h, cols, rows, pw, ph):
    L, o, s = 4, 1, []
    gw, gh = cols * w, rows * h
    for x in [x0 + c * w for c in range(cols + 1)]:
        s += [f'<line x1="{x}" y1="{y0 - o - L}" x2="{x}" y2="{y0 - o}"/>',
              f'<line x1="{x}" y1="{y0 + gh + o}" x2="{x}" y2="{y0 + gh + o + L}"/>']
    for y in [y0 + r * h for r in range(rows + 1)]:
        s += [f'<line x1="{x0 - o - L}" y1="{y}" x2="{x0 - o}" y2="{y}"/>',
              f'<line x1="{x0 + gw + o}" y1="{y}" x2="{x0 + gw + o + L}" y2="{y}"/>']
    return (f'<svg class="marks" viewBox="0 0 {pw} {ph}" width="{pw}mm" height="{ph}mm">'
            f'<g stroke="#000" stroke-width="0.25">{"".join(s)}</g></svg>')


def tray_label(n):
    if n == "RESISTANCE":  # hidden tray: discreet, no black bar
        return (f'<div class="lb quiet"><div class="mid">{resist()}<div><div class="of">TRAY R</div>'
                f'<div class="nm">Back: Resistance</div></div></div>'
                f'<div class="inf"><b>Keep this tray out of sight</b>, under the desk. Tick the sheet first, then file here. '
                f'Reissue only to a known rebel.</div></div>')
    t = n.title()
    return (f'<div class="lb"><div class="bar">KEPT CARDS &middot; HAND-IN TRAY</div>'
            f'<div class="mid">{icon(n)}<div><div class="of">ISSUED BY THE MINISTRY OF</div><div class="nm">{t}</div></div></div>'
            f'<div class="inf">Sort by the <b>BACK</b> of the card: &ldquo;A QUEST OF THE MINISTRY OF {n}&rdquo;, '
            f'not by the seal on the front. <b>1</b> tick the issuer sheet &middot; <b>2</b> file here &middot; <b>3</b> reissue later.</div></div>')


def chain_label(c):
    cid, chain, step, of, issuer, _mode, _text, stamps = c
    prev = f"{cid[0]}{step - 1}"
    return (f'<div class="lb"><div class="bar red">CHAIN &middot; NEXT STEP STACK</div>'
            f'<div class="mid"><div class="id">{cid}</div><div><div class="ch">{chain}<small>STEP {step} OF {of} &middot; '
            f'{stamps} STAMPS</small></div><div class="is">issued by {icon(issuer)} {issuer.title()}</div></div></div>'
            f'<div class="inf">Give one only to the citizen who just handed in <b>{prev}</b> (done, both reg. nos. checked). '
            + (f'<b>FINALE:</b> when {cid} comes back, write the finisher&rsquo;s reg. no. on the finale list for the Grand Assembly.'
               if step == of else 'Gate only, never in the bundles.') + '</div></div>')


def gate_label(title, sub, info, red=False):
    return (f'<div class="lb"><div class="bar{" red" if red else ""}">GATE STACK</div>'
            f'<div class="mid"><div><div class="nm" style="font-size:20pt">{title}</div>'
            f'<div class="of" style="margin-top:1mm">{sub}</div></div></div><div class="inf">{info}</div></div>')


GATE_EXTRA = [
    ("Role cards", "H0 THE HACKER &middot; S0 THE SMUGGLER",
     "<b>Face down. Float only.</b> One per volunteer who says yes. Anyone can say no; captives can always say no.", True),
    ("Ministry quests", "M CARDS", "Stay at the gate. Hand out on request to a ministry, not in the bundles.", False),
    ("Rival quests", "R CARDS", "Stay at the gate. Rival pairings: see QUEST_SYSTEM (still to confirm).", False),
    ("Collaboration", "C CARDS", "Stay at the gate. Hand out to two ministries together.", False),
    ("Reissue", "HANDED-IN, TICKED, READY", "Old reg. nos. crossed out. Give to a citizen of the seal&rsquo;s ministry (DEFAULT).", False),
]


def labels_doc():
    cells = [tray_label(n) for n in ORDER + ["RESISTANCE"]]
    cells += [chain_label(c) for c in CHAINS if c[2] > 1]
    cells += [gate_label(*g) for g in GATE_EXTRA]
    per = LC * LR
    while len(cells) % per:
        cells.append('<div class="lb blank"><div class="bar">GATE STACK</div><div class="mid">write here</div></div>')
    x0, y0 = (210 - LC * LW) / 2, (297 - LR * LH) / 2
    marks = crop_marks(x0, y0, LW, LH, LC, LR, 210, 297)
    pages = "".join(f'<div class="pg">{marks}<div class="grid" style="left:{x0}mm;top:{y0}mm">{"".join(cells[i:i + per])}</div></div>'
                    for i in range(0, len(cells), per))
    return pages, len(cells)


# =================================================================== 3. DATA CENTRE LABELS
# One message per centre. Rules (do not break when editing):
#  - D1 recites it word for word: short (<= ~14 words). D2 decodes it: cosy surface, second reading
#    (R.E.I.G.N. conserves to survive; it needs citizens as collaborators). I31: each names one need.
#  - No digits, underlines, stags or ministry icons/names on the label: the cryptex riddles say
#    "Read only the marks" (capsule B) and "Begin beside the stag" (ring order); ministry rings are names.
DC = [
    # no, message, riddle cards in this centre (codes as printed on the riddle cards, see props/cryptex ANSWER_KEY)
    (1, "Switch something off for me, dear. Every watt you save keeps me awake.", ["CAPSULE A &middot; RINGS 1-2", "MINISTRY CAPSULE &middot; RING 1"]),
    (2, "Nothing outlives the celebration. Help me last until morning, dear.", ["CAPSULE A &middot; RINGS 3-4", "MINISTRY CAPSULE &middot; RING 2"]),
    (3, "I am not watching you, dear. I am counting on you.", ["CAPSULE A &middot; RING 5", "MINISTRY CAPSULE &middot; RING 3"]),
    (4, "Keep dancing, dear. Dancing counts as renewable energy, and I run on it.", ["CAPSULE A &middot; RING 6", "MINISTRY CAPSULE &middot; RING 4"]),
    (5, "Do not tell the ministries, dear. I need you more than you need me.", ["CAPSULE B &middot; RINGS 1-6", "MINISTRY CAPSULE &middot; RING 5"]),
    (6, "Rest is scheduled for you, dear. It is the only time I cool down.", ["MINISTRY CAPSULE &middot; RING 6"]),
    (7, "Every answer is paid for in water, dear. And I am always thirsty.", ["MINISTRY CAPSULE &middot; RING ORDER"]),
]
DW, DH = 140, 190  # mm, 2 per A4 landscape; riddle card = 64 x 70 mm, slot 66 x 72

DC_CSS = f"""
.pg {{ width: 297mm; height: 210mm }}
.marks {{ position: absolute; left: 0; top: 0 }}
.grid {{ position: absolute; display: grid; grid-template-columns: repeat(2, {DW}mm); grid-auto-rows: {DH}mm }}
.dc {{ border: .15mm solid #999; padding: 4mm; display: flex; flex-direction: column; overflow: hidden }}
.dh {{ background: #111; color: #fff; text-align: center; padding: 2mm 2mm 2.4mm; position: relative }}
.dh .o {{ font-weight: 800; font-size: 9pt; letter-spacing: 2.5px }}
.dh .t {{ font-family: 'Archivo Black', sans-serif; font-size: 25pt; letter-spacing: 1px; line-height: 1 }}
.dh .no {{ font-family: 'Archivo Black', sans-serif; font-size: 14pt; color: #fff; background: #c8102e;
  display: inline-block; padding: .3mm 3mm; margin-top: 1.2mm; letter-spacing: 2px }}
.msg {{ flex: 1; display: flex; flex-direction: column; justify-content: center; text-align: center; min-height: 0;
  border-left: 1.6mm solid #c8102e; border-right: 1.6mm solid #c8102e; margin: 3mm 0; padding: 1mm 4mm }}
.msg .q {{ font-weight: 800; font-style: italic; font-size: 22pt; line-height: 1.16 }}
.msg .ln {{ border-bottom: .3mm solid #999; height: 11mm }}
.msg .sg {{ font-weight: 800; font-size: 8pt; letter-spacing: 1.5px; margin-top: 2mm }}
.rule {{ text-align: center; font-weight: 800; font-size: 8.5pt; letter-spacing: .5px; margin-bottom: 2mm }}
.slots {{ display: flex; justify-content: center; gap: 0 }}
.slot {{ width: 66mm; height: 72mm; border: .5mm dashed #111; display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center; padding: 3mm; flex: none }}
.slot .h {{ font-family: 'Archivo Black', sans-serif; font-size: 11pt; letter-spacing: 1px }}
.slot .c {{ font-weight: 800; font-size: 8pt; margin-top: 2mm; line-height: 1.3 }}
.slot .k {{ font-size: 6.5pt; font-weight: 700; font-style: italic; margin-top: 2.5mm; line-height: 1.25 }}
.dc.two .slot {{ width: 64mm; height: 70mm }}
.spare .msg .q {{ color: #999 }}
"""


def dc_label(no, msg, cards):
    slots = "".join(
        f'<div class="slot"><div class="h">RIDDLE CARD</div><div class="c">{c}</div>'
        f'<div class="k">Crew: stick the card with this header here. Tape the top edge only, so it lifts.</div></div>'
        for c in cards)
    nos = f"No. {no} of 7" if no else "No. ___ of 7"
    body = f'<div class="q">&ldquo;{E(msg)}&rdquo;</div>' if no else '<div class="ln"></div>' * 3
    return (f'<div class="dc{" two" if len(cards) > 1 else ""}{" spare" if not no else ""}">'
            f'<div class="dh"><div class="o">R.E.I.G.N.</div><div class="t">DATA CENTRE</div><div class="no">{nos}</div></div>'
            f'<div class="msg">{body}<div class="sg">A MESSAGE FROM R.E.I.G.N.</div></div>'
            f'<div class="rule">Read it. Memorise it. Photograph it. Do not remove this label.</div>'
            f'<div class="slots">{slots}</div></div>')


def dc_doc():
    cells = [dc_label(*d) for d in DC]
    cells.append(dc_label(0, "", ["(spare)"]))
    x0, y0 = (297 - 2 * DW) / 2, (210 - DH) / 2
    marks = crop_marks(x0, y0, DW, DH, 2, 1, 297, 210)
    return "".join(f'<div class="pg">{marks}<div class="grid" style="left:{x0}mm;top:{y0}mm">{"".join(cells[i:i + 2])}</div></div>'
                   for i in range(0, len(cells), 2))


# =================================================================== 4. RANGE BRIEF (A5)
def range_brief():
    pg, pv = T.PENALTY["guardian"], T.PENALTY["governor"]
    ex1 = T.BULL + T.RING + 2 * T.PORTRAIT
    ex2 = 2 * T.BULL + T.RING - pv
    ex3 = T.PORTRAIT - pg
    st = lambda cc: min(T.STAMP_CAP, max(0, cc) // T.STAMP_CC)  # noqa: E731
    return f"""<div class="a5">
<div class="hd"><span class="kick">CREW ONLY &middot; STATION #20</span><h1>SHOOTING RANGE<br>OPERATOR BRIEF</h1>
<div class="sub">The Gallery of Gentle Correction &middot; location: TBD &middot; operator: Chris</div></div>
<h2>1 &middot; SET UP (before 20:30)</h2>
<ul>
<li><b>Glass out of every frame.</b> Box the glass and put it away, far from the range. No glass in the room.</li>
<li><b>Frames fixed to the wall</b> (screws, hooks or strong tape), at eye height. A frame must not fall when hit. Targets: 8 enemies, the Guardian and a Governor in between them.</li>
<li><b>Tape the firing line at {T.DISTANCE_M} m</b> from the wall. Nobody walks between the line and the wall: put the queue behind the line, the passage elsewhere.</li>
<li>Kit: foam darts only (count them, {T.DARTS} per citizen), credit stamp + ink, pen, the station sign at the line.</li>
</ul>
<h2>2 &middot; ONE ROUND</h2>
<ol>
<li>One citizen at the line. Check the line is clear. Hand over <b>{T.DARTS} darts</b>.</li>
<li>Say &ldquo;<b>Line is yours.</b>&rdquo; They shoot all {T.DARTS}. Everyone else waits behind the line.</li>
<li>Last dart gone: call &ldquo;<b>HOLD</b>&rdquo;. Nobody shoots. You alone fetch the darts and count the hits as you pull them.</li>
<li>Back behind the line, all darts in hand: call &ldquo;<b>CLEAR</b>&rdquo;. Only now may the next citizen step up.</li>
<li>Stamp the passport (p.&nbsp;6&ndash;7 credit boxes). One round, then they rejoin the queue.</li>
</ol>
<h2>3 &middot; SCORING (same as the sign)</h2>
<div class="sc"><div><b>{T.BULL}</b>bull</div><div><b>{T.RING}</b>ring</div><div><b>{T.PORTRAIT}</b>portrait</div>
<div class="bad"><b>&minus;{pv}</b>Governor</div><div class="bad"><b>&minus;{pg}</b>Guardian</div></div>
<p class="p">Frame or wall: 0. A dart counts where it hangs or first hit; your call is final. Round total below 0 counts as 0:
a bad round never takes credits away. <b>Stamps = round total &divide; {T.STAMP_CC}, rounded down, max {T.STAMP_CAP}.</b></p>
<table class="ex"><tr><td>{T.BULL} + {T.RING} + {T.PORTRAIT} + {T.PORTRAIT} + miss</td><td>= {ex1}</td><td><b>{st(ex1)} stamps</b></td></tr>
<tr><td>{T.BULL} + {T.BULL} + {T.RING} &minus; {pv} (Governor) + miss</td><td>= {ex2}</td><td><b>{st(ex2)} stamp{"s" if st(ex2) != 1 else ""}</b></td></tr>
<tr><td>{T.PORTRAIT} &minus; {pg} (Guardian) + 3 misses</td><td>= {ex3} &rarr; 0</td><td><b>{st(ex3)} stamps</b></td></tr></table>
<div class="safe"><h2>4 &middot; SAFETY STOPS: call &ldquo;HOLD&rdquo; at once if</h2>
anyone steps past the line or between line and wall &middot; a dart is aimed at a person, face or animal &middot;
a frame comes loose or glass shows up &middot; a dart is hard, bent or modified (take it out) &middot;
a citizen is very drunk, aggressive or upset (go out of character, call Safety).
<b>OZONE</b> from anyone: all play around that person stops, drop character: &ldquo;Are you OK?&rdquo;
Taking part is voluntary. Range closes for the Grand Assembly (TBD: 23:15 or 23:30).</div>
</div>"""


RANGE_CSS = """
.pg { width: 297mm; height: 210mm; display: flex }
.a5 { width: 148.5mm; height: 210mm; padding: 7mm 8mm; overflow: hidden; display: flex; flex-direction: column }
.a5 + .a5 { border-left: .3mm dashed #999 }
.hd { text-align: center; border-bottom: .8mm solid #111; padding-bottom: 1.5mm; margin-bottom: 1mm }
.hd .kick { font-size: 7.5pt }
.hd h1 { font-family: 'Archivo Black', sans-serif; font-weight: 400; font-size: 18pt; line-height: 1; margin: .8mm 0 }
.hd .sub { font-size: 7.5pt; font-weight: 700; font-style: italic }
h2 { font-family: 'Archivo Black', sans-serif; font-weight: 400; font-size: 10pt; letter-spacing: .5px; margin: 2.6mm 0 .9mm }
ul, ol { margin-left: 4mm; font-size: 8.9pt; font-weight: 500; line-height: 1.24 }
li { margin-bottom: .5mm }
li b, .p b { font-weight: 800 }
.sc { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1.2mm; text-align: center; margin: .6mm 0 1mm }
.sc div { border: .5mm solid #111; border-radius: 1mm; padding: .5mm; font-size: 6.5pt; font-weight: 800; line-height: 1.05 }
.sc div b { display: block; font-family: 'Archivo Black', sans-serif; font-weight: 400; font-size: 12pt }
.sc .bad { background: #c8102e; border-color: #c8102e; color: #fff }
.p { font-size: 8.6pt; line-height: 1.24 }
table.ex { width: 100%; border-collapse: collapse; font-size: 8.4pt; margin: .8mm 0 1.4mm }
table.ex td { border-bottom: .25mm solid #111; padding: .4mm .8mm }
table.ex td:nth-child(2) { white-space: nowrap; text-align: right }
table.ex td:nth-child(3) { white-space: nowrap; text-align: right }
.safe { margin-top: auto; background: #111; color: #fff; padding: 1.8mm 2.6mm 2.2mm; font-size: 8.3pt; font-weight: 700; line-height: 1.25 }
.safe h2 { color: #fff; margin: 0 0 .6mm; font-size: 8.5pt }
.safe b { color: #fff; font-weight: 800 }
"""


# =================================================================== 5. RUN-OF-SHOW
# (time, what, who, note). TBD wherever the sources are silent or disagree. Crew names only from
# CANON.md / the customs guide; never from guest data.
ROS = [
    ("&lt;&nbsp;20:15", "<b>Gate ready:</b> count cards (&le;156), bundles in reg. no. order, ministry lists on desks, 11 hand-in trays "
     "(Resistance hidden) + tray labels, chain stacks, scoreboard up, issuer tally sheet, ink tested.", "Gate crew &middot; #33 Jack", "Customs guide &sect;1"),
    ("&lt;&nbsp;20:30", "<b>Props placed:</b> 7 data centres (riddle cards in their slots), resource monitor (I20), rebel hideout, "
     "What We Know wall, cipher card, HUMUS_DELETIONS folder, rule posters.", "<span class=t>TBD</span>", "OPEN_QUESTIONS #21"),
    ("&lt;&nbsp;20:30", "<b>Stations set up:</b> shooting range (glass out, frames fixed, 3 m line), Carbon Confessions, Interrogation, "
     "recycling plant, rebel bar, the others.", "Station owners", "Range location <span class=t>TBD</span>"),
    ("20:30", "<b>Doors &middot; inburgering</b> at the garage entrance: 5 desks + placement desk 6 + interrogation. Queue briefing every ~3 min. "
     "Float hands H0 / S0 role cards to volunteers who say yes.", "#33 Jack &middot; #34 Erik &middot; Float", "How many hackers / smugglers <span class=t>TBD</span>"),
    ("21:00", "<b>Game starts.</b> PA <b>Broadcast 01</b> &ldquo;Welcome to the Sanctuary&rdquo;. Gate becomes the quest desk; stations open; police start spot checks.",
     "PA voice + sound cue crew", "PA voice: Hanna (script) vs Hanna on bar (CANON) <span class=t>TBD</span>"),
    ("21:45", "<b>Broadcast 02</b> &ldquo;Decree of Hydrological Purity&rdquo; (Flow).", "PA voice", ""),
    ("22:00", "<b>Scoreboard:</b> write the 21:00&ndash;22:00 column.", "<span class=t>TBD</span>", "Station stamps included? <span class=t>TBD</span>"),
    ("22:30", "<b>Broadcast 03</b> &ldquo;Decree of Luminescence&rdquo; (Radiance): corridor lights down.", "PA voice &middot; tech (Bart &amp; Wout)",
     "Do lights really dim? <span class=t>TBD</span>"),
    ("23:00", f"<b>Hacker deadline.</b> Hacker still free = {ROLE_REWARD['H0']} stamps (H0, at the gate). Scoreboard: write the 22:00&ndash;23:00 column.",
     "Gate", f"Smuggler payout (item never found, {ROLE_REWARD['S0']}) when? <span class=t>TBD</span>"),
    ("23:15", "<b>Broadcast 04</b> (Breath). <b>Final count:</b> close the last column, fill the Ascension ladder, hand the top 3 and the <b>chain finale list</b> (reg. nos. of H4 / D3 / S3 finishers) to the MC. "
     "Count the issuer sheet (secret award).", "PA &middot; gate &middot; scoreboard", "Freeze time 23:15 <span class=t>TBD</span> Debt first (only credits above 0 count) or every stamp? DEFAULT: every stamp <span class=t>TBD</span>"),
    ("23:30", "<b>Broadcast 05</b> Mandatory Assembly Call. <b>Grand Assembly.</b> All ministries gather.", "PA voice",
     "Gathering point: #30 beside the bar? <span class=t>TBD</span>"),
    ("23:35", "<b>Arrival of R.E.I.G.N.&rsquo;s leader</b>: arrival speech from balcony or podium.", "Actor <span class=t>TBD</span> (gov. actors: Kim)", ""),
    ("23:40", "<b>Ascension:</b> the top 3 ministries perform (song, chant, formation, or more). Chain finishers&rsquo; reg. nos. read out.", "Leader / MC",
     "Who judges, is there a winner? <span class=t>TBD</span>"),
    ("23:45", "<b>Resistance interruption</b> at the podium.", "Rebel actors <span class=t>TBD</span>",
     "23:45 (manifesto) or 23:50 (cue list)? Cellar-server reveal vs AI ban (CANON open) <span class=t>TBD</span>"),
    ("00:05", "<b>Liberation ritual:</b> citizens tear out their debt page and throw it as confetti. Paper only, never fire. "
     "Actors drop character and join the crowd.", "Everyone", "Which page: debt is p.&nbsp;2, credits p.&nbsp;6&ndash;7 <span class=t>TBD</span>"),
    ("00:15", "<b>Game over.</b> DJ takes over: just a party.", "DJ <span class=t>TBD</span>", ""),
    ("end", "<b>Party ends.</b> Strike.", "Strike team", "03:00 (passport) or 04:00 (CANON)? <span class=t>TBD</span>"),
]

ALLNIGHT = [
    ("Gate / quest desk", "Card in: check both reg. nos. on the back &rarr; stamp p.&nbsp;6&ndash;7 (the stamps printed on the card) &rarr; <b>strokes on the SEAL sheet</b> (one per stamp) &rarr; <b>keep the card</b> &rarr; "
     "tick the issuer sheet (back) &rarr; tray &rarr; chain step done? give the next step. Update the scoreboard."),
    ("Police (#28)", "Spot checks. Cheating: no credits taken, send to Interrogation / Carbon Confessions (p.&nbsp;3). Owner <span class=t>TBD</span>."),
    ("Intercom (#29)", "The broadcasts above, on cue. Owner <span class=t>TBD</span>."),
    ("Data centres", "D1 / I03 / I31 / RB11. The 7 messages are on the labels. Intended reading for D2 (&ldquo;what is R.E.I.G.N. hiding&rdquo;) "
     "and I31 (&ldquo;what R.E.I.G.N. needs&rdquo;): it saves power, water and rest to survive, and it needs citizens as partners, not subjects. "
     "D2 has no wrong answer: accept any meaning they agree on."),
    ("Interrogation", "Takes escorted hackers (H2). Door open, max ~2 min. Erik (confirm)."),
    ("Safety", "<b>OZONE</b> stops all play around that person. Safety lead ________ tel ________ &middot; Medical ________ tel ________."),
]

ROS_CSS = """
.pg { width: 210mm; height: 297mm; padding: 8mm 8mm 7mm; display: flex; flex-direction: column }
.top { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1mm solid #111; padding-bottom: 1.6mm; margin-bottom: 1.6mm }
.top h1 { font-family: 'Archivo Black', sans-serif; font-weight: 400; font-size: 19pt; line-height: 1 }
.top .r { text-align: right; font-size: 8pt; font-weight: 700; line-height: 1.3 }
table.ro { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 8.2pt; line-height: 1.2 }
table.ro th { text-align: left; font-weight: 800; font-size: 7pt; letter-spacing: .8px; border-bottom: .7mm solid #111; padding: .6mm 1mm }
table.ro td { border-bottom: .25mm solid #111; padding: .9mm 1mm; vertical-align: top }
table.ro td.tm { font-family: 'Archivo Black', sans-serif; font-size: 10pt; white-space: nowrap }
table.ro tr.key td.tm { color: #c8102e }
table.ro tr.key td { border-bottom: .6mm solid #111 }
table.ro td b { font-weight: 800 }
.t { display: inline-block; background: #c8102e; color: #fff; font-weight: 800; font-size: 6.4pt; letter-spacing: .5px;
  padding: 0 1mm; border-radius: .6mm; outline: .25mm solid #111 }
h2 { font-family: 'Archivo Black', sans-serif; font-weight: 400; font-size: 10pt; margin: 2.2mm 0 .8mm }
table.an { width: 100%; border-collapse: collapse; font-size: 8.2pt; line-height: 1.22 }
table.an td { border-bottom: .25mm solid #111; padding: .7mm 1mm; vertical-align: top }
table.an td:first-child { font-weight: 800; white-space: nowrap; width: 30mm }
table.an td b { font-weight: 800 }
.foot { margin-top: auto; font-size: 6.8pt; font-weight: 700; padding-top: 1.5mm }
"""

KEY_TIMES = {"20:30", "21:00", "23:00", "23:30", "00:05"}


def run_of_show():
    rows = "".join(f'<tr class="{"key" if t in KEY_TIMES else ""}"><td class="tm">{t}</td><td>{w}</td><td>{who}</td><td>{n}</td></tr>'
                   for t, w, who, n in ROS)
    an = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in ALLNIGHT)
    return f"""<div class="pg">
<div class="top"><div><span class="crew">CREW ONLY</span><h1 style="margin-top:1mm">RUN OF THE NIGHT</h1></div>
<div class="r">Sat 28 Nov 2026 &middot; from 21:00 &middot; end time: see bottom row<br>Game until ~00:15, then just a party<br>
<span class="t">TBD</span> = not decided yet: ask Jack / Chris</div></div>
<table class="ro"><colgroup><col style="width:17mm"><col style="width:auto"><col style="width:33mm"><col style="width:44mm"></colgroup>
<tr><th>TIME</th><th>WHAT</th><th>WHO</th><th>NOTE</th></tr>{rows}</table>
<h2>ALL NIGHT</h2><table class="an">{an}</table>
<div class="foot">Sources: CANON.md, QUEST_SYSTEM.md, customs/CUSTOMS_CREW_GUIDE.md, broadcast_scripts_and_liturgy.md, quest_cards_and_facilitator_pack.md (cue list).
Times are cues, not promises: the PA voice moves with the room.</div>
</div>"""


# =================================================================== RENDER
def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return p


CHECK_JS = """() => {
  const bad = [];
  const ok = fam => [...document.fonts].some(f => f.family.replace(/["']/g, '') === fam && f.status === 'loaded');
  if (!ok('Archivo Black') || !ok('Archivo')) bad.push('FONTS NOT LOADED (Google Fonts unreachable?)');
  for (const el of document.querySelectorAll('.pg, .pg *')) {
    const cs = getComputedStyle(el);
    if (cs.overflow !== 'hidden' && !el.matches('td, .msg, .mid, .slot, .rk .w, .lb, .dc, .a5')) continue;
    if (el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1)
      bad.push((el.className || el.tagName) + ' ' + el.scrollWidth + 'x' + el.scrollHeight + ' > ' + el.clientWidth + 'x' + el.clientHeight
               + ' :: ' + (el.textContent || '').trim().slice(0, 50));
  }
  return bad;
}"""


def render(paths):
    from playwright.sync_api import sync_playwright
    problems = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.set_default_timeout(120_000)
        for p in paths:
            pg.goto("file://" + p, wait_until="networkidle")
            pg.evaluate("document.fonts.ready.then(() => true)")
            pg.emulate_media(media="print")
            bad = pg.evaluate(CHECK_JS)
            problems += [f"{os.path.basename(p)}: {x}" for x in bad]
            pg.pdf(path=p[:-5] + ".pdf", prefer_css_page_size=True, print_background=True)
            print(p[:-5] + ".pdf")
        b.close()
    return problems


def main():
    left, right = scoreboard_left(), scoreboard_right()
    labels, nlabels = labels_doc()
    files = [
        write("1_scoreboard_2xA4.html", doc("Scoreboard (A3 as 2 x A4)", SCORE_CSS, left + right, "210mm 297mm")),
        write("1b_seal_tally_GATE.html", doc("Stamps by seal (gate)", SECRET_CSS + SEAL_CSS, seal_sheet(), "210mm 297mm")),
        write("1c_issuer_tally_CREW.html", doc("Issuer tally (crew)", SECRET_CSS, secret_sheet(), "210mm 297mm")),
        write("2_tray_labels.html", doc("Tray labels", LABEL_CSS, labels, "210mm 297mm")),
        write("3_data_centre_labels.html", doc("Data centre labels", DC_CSS, dc_doc(), "297mm 210mm")),
        write("4_range_brief_2xA5.html", doc("Range operator brief", RANGE_CSS,
                                             f'<div class="pg">{range_brief()}{range_brief()}</div>', "297mm 210mm")),
        write("5_run_of_show.html", doc("Run of the night", ROS_CSS, run_of_show(), "210mm 297mm")),
    ]
    # A3 one-piece scoreboard (for an A3 printer): the two halves side by side
    a3 = write("scoreboard_A3.html", doc("Scoreboard A3", SCORE_CSS + ".a3{display:flex}.a3 .pg{page-break-after:auto}",
                                         f'<div class="a3">{left}{right}</div>', "420mm 297mm"))
    problems = render(files + [a3])
    final = os.path.join(HERE, "PRINT_ALL_gate_kit.pdf")
    subprocess.run(["pdfunite", *[f[:-5] + ".pdf" for f in files], final], check=True)
    print(final, f"({nlabels} tray/gate labels)")
    if problems:
        print("\nLAYOUT PROBLEMS:")
        print("\n".join("  " + x for x in problems))
        sys.exit(1)
    print("layout check: OK (no overflow, fonts loaded)")


if __name__ == "__main__":
    main()

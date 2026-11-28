"""Quest cards to stick on the playing cards (61 x 90 mm, 9 per A4 portrait), from the "quests to print" tab.

Run: python3 make_quest_cards.py ["../Citizens export and quests.xlsx"]
  -> quest_cards.html + quest_cards.pdf (fronts, single-sided)
     quest_cards_backs.html + .pdf     (one back per card, themed per ministry; stick on the back of the poker card)
Print at 100% / actual size. Cut on the dashed lines.
"""
import html
import os
import re
import sys

import make_passport_options as M
from xlsx_read import read
from quest_ministries import ISSUER, RESISTANCE, TOGETHER, DELIVER, NOTES
from chains import CHAINS, ROLES, NOTES as CHAIN_NOTES
from quest_texts import TEXT

NOTES = {**NOTES, **CHAIN_NOTES}

ROLE = {r[0]: r for r in ROLES}
CHAIN = {c[0]: c for c in CHAINS}
for _c in CHAINS:
    ISSUER[_c[0]] = _c[4]
    {"T": TOGETHER, "D": DELIVER}.get(_c[5], set()).add(_c[0])

HERE = M.HERE
SRC = os.path.join(HERE, "..", "Citizens export and quests.xlsx")
esc = html.escape
W, H = 61, 90  # mm: measured against the real cards (56x88 was 5 mm too narrow, 2 mm too short)
# Other card stock: CARD_SIZE=57x88 python3 make_quest_cards.py  -> quest_cards_57x88(.pdf) + backs
if os.environ.get("CARD_SIZE"):
    W, H = (float(v) for v in os.environ["CARD_SIZE"].lower().split("x"))
SMALL = 1.0 if (W, H) == (61, 90) else 0.93  # smaller card stock: shrink quest text a little
SUFFIX = "" if (W, H) == (61, 90) else f"_{os.environ['CARD_SIZE'].lower()}"

KINDS = {  # prefix -> label on the card
    "I": "Personal quest",
    "M": "Ministry quest",
    "R": "Rival quest",
    "C": "Collaboration quest",
    "RB": "Rebel quest",
}
STAG = M.STAG.replace('class="crest"', 'class="stag"', 1)

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@500;700;800&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#444;font-family:'Archivo','DejaVu Sans',sans-serif;color:#000;display:flex;flex-direction:column;align-items:center;padding:12px;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}}
.label{{color:#fff;font:700 16px 'Archivo',sans-serif;margin:10px 0 6px}}
.sheet{{background:#fff;width:210mm;height:297mm;display:flex;align-items:center;justify-content:center;position:relative}}
.grid{{display:grid;grid-template-columns:repeat(3,{W}mm);grid-template-rows:repeat(3,{H}mm)}}
.card{{padding:2.2mm;overflow:hidden}}
.cm{{position:absolute;background:#000}}
.in{{height:100%;border:2px solid #000;border-radius:2.5mm;padding:2.6mm 3mm;display:flex;flex-direction:column;position:relative}}
.top{{display:flex;align-items:center;gap:2mm;border-bottom:2px solid #000;padding-bottom:1.5mm}}
.top .stag{{width:11mm;height:11mm;flex:none}}
.top .k{{font-family:'Archivo Black',sans-serif;font-size:10.5pt;line-height:1}}
.top .s{{font-size:6.5pt;font-weight:700;margin-top:.6mm}}
.q{{flex:1;display:flex;align-items:center;font-weight:700;line-height:1.25;padding:2mm 0}}
.cash{{text-align:center;padding-bottom:1.2mm}}
.mode{{font-size:7.6pt;font-weight:800;line-height:1.15}}
.mode b{{font-family:'Archivo Black',sans-serif;letter-spacing:.3px}}
.extra{{font-size:6pt;font-weight:700;font-style:italic;line-height:1.15;margin-top:.4mm}}
.howto{{font-size:5.6pt;font-weight:800;line-height:1.1;margin-top:.8mm;border-top:1px dotted #000;padding-top:.6mm;white-space:nowrap}}
.bot{{display:flex;align-items:end;justify-content:space-between;border-top:2px solid #000;padding-top:1.5mm}}
.rew{{font-weight:800;font-size:8pt;line-height:1.15}}
.rew b{{font-family:'Archivo Black',sans-serif;font-size:13pt;display:block}}
.done{{width:19.5mm;height:19.5mm;border:1.5px dashed #000;border-radius:50%;display:flex;align-items:center;justify-content:center;
 font-size:5.5pt;font-weight:800;color:#000;text-align:center;flex:none}}
.id{{position:absolute;left:50%;transform:translateX(-50%);bottom:1mm;font-size:6pt;font-weight:800;color:#000}}
.back .in{{align-items:center;justify-content:center;text-align:center;gap:2mm;border-width:3px;outline:1px solid #000;outline-offset:-2.2mm}}
.back .micon{{width:18mm;height:18mm}}
.back .k2{{font-family:'Archivo Black',sans-serif;font-size:9pt;letter-spacing:2px;border:2px solid #000;padding:.5mm 2mm}}
.back .t{{font-family:'Archivo Black',sans-serif;font-size:14pt;line-height:1.05}}
.back .m{{font-size:8pt;font-weight:700;font-style:italic;line-height:1.25}}
.back .m.small{{font-size:6.5pt;font-style:normal}}
.back .sig{{width:100%;display:flex;align-items:end;gap:1.5mm;font-size:8pt;height:8mm;font-weight:800;text-align:left}}
.back .who{{width:100%;font-size:7.5pt;font-weight:800;text-align:left;line-height:1.15;margin-bottom:-1mm}}
.back .who b{{font-family:'Archivo Black',sans-serif}}
.back .sig + .sig:not(:nth-of-type(odd)){{}}

.chain{{margin-top:1.5mm;background:#000;color:#fff;font-family:'Archivo Black',sans-serif;font-size:7pt;letter-spacing:.5px;text-align:center;padding:.6mm 0}}
.note{{font-size:6.8pt;font-weight:600;font-style:italic;margin-top:1.5mm;line-height:1.2}}
.back .sig span{{flex:1;border-bottom:1.5px solid #000;height:5mm}}
@media print{{body{{background:none;padding:0}}.label{{display:none}}.sheet{{break-after:page}}@page{{size:A4 portrait;margin:0}}}}
"""


def qsize(text):
    n = len(text)
    pt = 12 if n <= 60 else 11 if n <= 100 else 10 if n <= 140 else 9 if n <= 190 else 8.5
    return round(pt * SMALL, 2)


STAMP = 100  # every credit stamp is worth 100 CC


def reward(s):
    s = s.strip()
    m = re.match(r"(\d+)(?:\.0)?\s*(.*)", s)
    if not m:
        return f"<b>{esc(s)}</b>"
    n = int(m.group(1))
    return f"<b>{n} stamp{'s' if n > 1 else ''}</b>+{n * STAMP} CC {esc(m.group(2))}"


def citizen(issuer):
    """'a Breath citizen', 'an Industry citizen', 'a fellow rebel'."""
    if issuer == RESISTANCE:
        return "a fellow rebel"
    name = issuer.title()
    return f"{'an' if name[0] in 'AEIOU' else 'a'} {name} citizen"


def mode_of(qid):
    return "D" if qid in DELIVER else "T" if qid in TOGETHER else "W"


def partner(qid, issuer):
    """Who the issuing-ministry party is, in plain words (front mode line and back)."""
    if qid.startswith("C") and qid in TOGETHER:
        return f"the Ministry of {issuer.title()} (your collaborator)"
    if qid.startswith("M") and qid in TOGETHER:
        return f"the Ministry of {issuer.title()}"
    return citizen(issuer)


VERB = {"T": ("DO IT WITH", "DONE WITH"), "D": ("BRING IT TO", "BROUGHT TO"), "W": ("SHOW IT TO", "SHOWN TO")}
HOWTO = '<div class="howto">&#10112; Do it &rarr; &#10113; get their reg. no. &rarr; &#10114; hand in at the gate</div>'


def how(qid, issuer):
    """Front: one plain line saying who from the issuing ministry is involved, then the 3-step how-to."""
    m = mode_of(qid)
    tail = " (they watch you do it)" if m == "W" else ""
    return f'<div class="mode"><b>{VERB[m][0]}:</b> {partner(qid, issuer)}{tail}</div>'


def issuer_of(qid):
    return RESISTANCE if qid.startswith("RB") or qid in ROLE else ISSUER[qid]


def card(qid, text, stamps):
    kind = "Secret role" if qid in ROLE else "Chain quest" if qid in CHAIN else KINDS.get(re.match(r"[A-Z]*", qid).group(), "Quest")
    issuer = issuer_of(qid)
    tag, line, extra, rlabel = "", how(qid, issuer), [], "Reward"
    if qid in ROLE:
        tag = f'<div class="chain">ROLE &middot; {ROLE[qid][1]}</div>'
        line = '<div class="mode">You can always say no to being captured or led around.</div>'
        m = re.match(r"(.*\?)\s*(\d+)", stamps)
        rlabel, stamps = m.group(1), m.group(2)
    elif qid in CHAIN:
        c = CHAIN[qid]
        tag = f'<div class="chain">{c[1]} &middot; STEP {c[2]} OF {c[3]}</div>'
        if c[2] < c[3]:
            extra.append("Next step: at the gate.")
        if qid in ("H1", "H2", "H3", "H4", "S1", "S2"):
            extra.append("Captives may say no.")
    if extra:
        line += f'<div class="extra">{" ".join(extra)}</div>'
    if qid not in ROLE:
        line += HOWTO
    if issuer == RESISTANCE:
        icon, who = f'<svg viewBox="0 0 200 200" class="stag">{REB_ICON}</svg>', "The Resistance"
    else:
        icon, who = f'<svg viewBox="60 64 80 80" class="stag">{M.ICONS[issuer]}</svg>', f"Ministry of {issuer.title()}"
    return (f'<div class="card"><div class="in"><span class="id">{esc(qid)}</span>'
            f'<div class="top">{icon}<div><div class="k">{kind.upper()}</div><div class="s">{who}</div></div></div>'
            f'{tag}<div class="q" style="font-size:{qsize(text + NOTES.get(qid, ""))}pt"><div>{esc(text)}'
            + (f'<div class="note">&#9432; {esc(NOTES[qid])}</div>' if qid in NOTES else '') + '</div></div>'
            f'<div class="cash">{line}</div>'
            f'<div class="bot"><div class="rew">{esc(rlabel)}{reward(stamps)}</div><div class="done">SEAL<br>this quest<br>scores for</div></div>'
            f'</div></div>')


def back(ministry, qid, together=False):
    """Card back: the issuing ministry (or the resistance); registration numbers of who completed it and of the witness."""
    if qid in ROLE:
        return (f'<div class="card back"><div class="in"><span class="id">{esc(qid)}</span>'
                f'<svg viewBox="0 0 200 200" class="micon">{REB_ICON}</svg>'
                f'<div class="k2">SECRET ROLE</div><div class="t">{ROLE[qid][1]}</div>'
                '<div class="m">Show this card only when you confess, or are caught.</div>'
                '<div class="sig">Played by: reg. no.<span></span></div>'
                '<div class="m small">Nature first.</div></div></div>')
    reb = ministry == RESISTANCE
    icon = (f'<svg viewBox="0 0 200 200" class="micon">{REB_ICON}</svg>' if reb
            else f'<svg viewBox="60 64 80 80" class="micon">{M.ICONS[ministry]}</svg>')
    title = '<div class="t">RESISTANCE</div>' if reb else f'<div class="t">MINISTRY OF<br>{ministry}</div>'
    m = together if together in VERB else "W"
    order = "Nature first." if reb else "By order of R.E.I.G.N."
    return (f'<div class="card back"><div class="in"><span class="id">{esc(qid)}</span>{icon}'
            f'<div class="k2">A QUEST OF THE</div>{title}'
            '<div class="sig">Completed by: your reg. no.<span></span></div>'
            f'<div class="who"><b>{VERB[m][1]}</b> {citizen(ministry)}:</div>'
            '<div class="sig">Write their reg. no. here<span></span></div>'
            f'<div class="m small">Numbers only, no names. {order}</div></div></div>')


def page(title, sheets):
    body = "".join(f'<div class="label">{lbl}</div><div class="sheet">{CROP}<div class="grid">{g}</div></div>' for lbl, g in sheets)
    tight = "" if SMALL == 1.0 else ".card{padding:1.4mm}.in{padding:2.2mm 1.9mm}.howto{letter-spacing:-.1px}"
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}{tight}</style></head><body>{body}</body></html>'


def crop_marks():
    """Cards touch (no gaps, no lines on the cards); short crop marks in the sheet margin show every cut."""
    x0, y0 = (210 - 3 * W) / 2, (297 - 3 * H) / 2
    L, gap, t = 5, 1, 0.25  # mark length, gap to the cards, line thickness (mm)
    marks = []
    for i in range(4):
        x, y = x0 + i * W, y0 + i * H
        marks.append(f'<div class="cm" style="left:{x - t / 2}mm;top:{y0 - gap - L}mm;width:{t}mm;height:{L}mm"></div>')
        marks.append(f'<div class="cm" style="left:{x - t / 2}mm;top:{y0 + 3 * H + gap}mm;width:{t}mm;height:{L}mm"></div>')
        marks.append(f'<div class="cm" style="top:{y - t / 2}mm;left:{x0 - gap - L}mm;height:{t}mm;width:{L}mm"></div>')
        marks.append(f'<div class="cm" style="top:{y - t / 2}mm;left:{x0 + 3 * W + gap}mm;height:{t}mm;width:{L}mm"></div>')
    return "".join(marks)


CROP = crop_marks()
_svg = open(os.path.join(HERE, '..', 'stamps', 'resistance_ankle_stamp.svg')).read()
REB_ICON = _svg[_svg.index('>') + 1:_svg.rindex('</svg>')]


def load(path):
    rows = read(path)["quests to print"]
    out = []
    for r in rows[1:]:
        r = r + ["", "", ""]
        if r[0].strip() and r[1].strip():
            out.append((r[0].strip(), re.sub(r"\s+", " ", r[1]).strip(), r[2]))
    ids = {q for q, _, _ in out}
    missing, extra = sorted(ids - TEXT.keys()), sorted(TEXT.keys() - ids)
    if missing or extra:
        print(f"WARNING quest_texts.py: no override for {missing}; override without xlsx row {extra}", file=sys.stderr)
    return [(q, TEXT.get(q, t), st) for q, t, st in out]


def render(paths):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.set_default_timeout(300_000)
        for p in paths:
            pg.goto("file://" + p, wait_until="load")
            pg.evaluate("document.fonts.ready.then(() => true)")
            pg.emulate_media(media="print")
            pg.pdf(path=p[:-5] + ".pdf", prefer_css_page_size=True, print_background=True)
        b.close()


if __name__ == "__main__":
    quests = load(sys.argv[1] if len(sys.argv) > 1 else SRC)
    quests += [(r[0], r[2], r[3]) for r in ROLES] + [(c[0], c[6], c[7]) for c in CHAINS]
    cards = [card(*q) for q in quests]
    sheets = []
    for i in range(0, len(cards), 9):
        chunk = quests[i:i + 9]
        sheets.append((f"Sheet {i // 9 + 1}: {chunk[0][0]} to {chunk[-1][0]}",
                       "".join(cards[i:i + 9]) + '<div class="card"></div>' * (9 - len(chunk))))
    fronts = os.path.join(HERE, f"quest_cards{SUFFIX}.html")
    backs = os.path.join(HERE, f"quest_cards_backs{SUFFIX}.html")
    open(fronts, "w").write(page("Quest cards", sheets))
    # one back per card, the ten ministries in turn (11-12 each); backs go on the other side of the poker card,
    # so any back can go with any front
    bks = [back(issuer_of(q[0]), q[0], 'T' if q[0] in TOGETHER else 'D' if q[0] in DELIVER else '') for q in quests]  # issuing ministry: quest_ministries.py
    bsheets = [(f"Backs sheet {i // 9 + 1}", "".join(bks[i:i + 9]) + '<div class="card"></div>' * (9 - len(bks[i:i + 9])))
               for i in range(0, len(bks), 9)]
    open(backs, "w").write(page("Quest card backs", bsheets))
    render([fronts, backs])
    print(f"{len(quests)} quest cards on {len(sheets)} sheets -> quest_cards{SUFFIX}.pdf + quest_cards_backs{SUFFIX}.pdf ({len(bsheets)} sheets)")

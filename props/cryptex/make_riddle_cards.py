"""Guest-facing cryptex riddle cards: 12 cards, 64 x 70 mm, 3 x 4 butted on ONE A4 portrait, crop marks outside.

Run: python3 props/cryptex/make_riddle_cards.py  -> riddle_cards.html + riddle_cards.pdf
Print at 100% / actual size, single-sided. Guillotine on the crop marks: shared cut lines, no gaps. One card per data centre (see ANSWER_KEY).
No answers or hints on these cards: those are in ANSWER_KEY.* (crew only). Source: 3dprints RIDDLES_*.md.
Check after any change: python3 props/cryptex/check_riddles.py
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PV2 = os.path.normpath(os.path.join(HERE, "..", "..", "passport_v2"))
sys.path.insert(0, PV2)
import make_passport_options as M  # noqa: E402  (ministry icons, same as passport page 5)

W, H, GAP, COLS, ROWS = 64, 70, 0, 3, 4  # mm: 12 cards butted on ONE A4 (guillotine)
STAG_FOOT = "Ring 1 sits beside the stag."
LEAVE = "Leave this card in the data centre."

# (label, riddle lines, footer)
CARDS = [
    ("CAPSULE A &middot; RINGS 1-2",
     ["Someone among you stole from R.E.I.G.N. and smiles about it.",
      "Until what hour must they stay free?",
      "Only they know. Find them, dear, and ask nicely."], STAG_FOOT),
    ("CAPSULE A &middot; RINGS 3-4",
     ["The hacker stole a file. Files do not last, dear.",
      "Nothing outlives the celebration.",
      "On which day does every record go back to nature?",
      "The day, dear. Not the month."], STAG_FOOT),
    ("CAPSULE A &middot; RING 5",
     ["In the room of questions, the hacker is questioned about the stolen file.",
      "How many questions must they answer?"], STAG_FOOT),
    ("CAPSULE A &middot; RING 6",
     ["A guilty citizen may say no. Not forever.",
      "How many times may the hacker deny it before the truth comes out?"], STAG_FOOT),
    ("CAPSULE B &middot; RINGS 1-6",
     ["Questions are welcome, dear. They have already been answered.",
      "We wrote to you personally, in your passport.",
      "We marked what matters. Read only the marks."], STAG_FOOT),
    ("MINISTRY CAPSULE &middot; RING 1",
     ["Every sigh you let go is counted, dear.",
      "Exhale gently. It is all on record."], ""),
    ("MINISTRY CAPSULE &middot; RING 2",
     ["Open your passport to the night.",
      "Among the ten, lower row, third from the left: it keeps every citizen in their box."], ""),
    ("MINISTRY CAPSULE &middot; RING 3",
     ["When the hacker has confessed and been corrected, someone walks them to where all things return.",
      "Whose citizens watch the renewal?"], ""),
    ("MINISTRY CAPSULE &middot; RING 4",
     ["My smile is never taken off.",
      "Celebration is not required. It is mandatory."], ""),
    ("MINISTRY CAPSULE &middot; RING 5",
     ["Own nothing you cannot carry, dear.",
      "Walk so softly the floor forgets you, and leave no more behind than a fallen leaf."], ""),
    ("MINISTRY CAPSULE &middot; RING 6",
     ["Before the captive is corrected in the Kinderkamer, they must confess, loudly, to the right citizens.",
      "Whose citizens receive the confession, and glow?"], ""),
    ("MINISTRY CAPSULE &middot; RING ORDER",
     ["Begin beside\u00a0the\u00a0stag.", "Read away from\u00a0it."], "STAG"),
]


def card(label, lines, foot):
    stag = foot == "STAG"
    body = "".join(f"<p>{html.escape(x)}</p>" for x in lines)
    icon = f'<svg class="bigstag" viewBox="60 64 80 80">{M.ICONS["VIGILANCE"]}</svg>' if stag else ""
    f = "" if stag or not foot else f'<div class="sub">{html.escape(foot)}</div>'
    return (f'<div class="card"><div class="hd"><div class="org">R.E.I.G.N. &middot; DATA CENTRE</div>'
            f'<div class="lab">{label.split(" &middot; ")[0]}</div><div class="ring">{label.split(" &middot; ")[1]}</div></div>'
            f'<div class="q{" order" if stag else ""}">{icon}{body}</div>{f}'
            f'<div class="ft">{LEAVE}</div></div>')


def crop_marks(rows=ROWS):
    """Cards are butted (shared cut lines, guillotine). Marks only outside the grid, on every cut line."""
    gw, gh = COLS * W, rows * H
    x0, y0 = (210 - gw) / 2, (297 - ROWS * H) / 2
    L, o, s = 3, 0.8, []
    for x in [x0 + c * W for c in range(COLS + 1)]:
        s += [f'<line x1="{x}" y1="{y0 - o - L}" x2="{x}" y2="{y0 - o}"/>', f'<line x1="{x}" y1="{y0 + gh + o}" x2="{x}" y2="{y0 + gh + o + L}"/>']
    for y in [y0 + r * H for r in range(rows + 1)]:
        s += [f'<line x1="{x0 - o - L}" y1="{y}" x2="{x0 - o}" y2="{y}"/>', f'<line x1="{x0 + gw + o}" y1="{y}" x2="{x0 + gw + o + L}" y2="{y}"/>']
    return (f'<svg class="marks" viewBox="0 0 210 297" width="210mm" height="297mm">'
            f'<g stroke="#000" stroke-width="0.25">{"".join(s)}</g></svg>'), x0, y0


CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@500;700;800&display=swap');
@page {{ size: A4 portrait; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Archivo', 'DejaVu Sans', sans-serif; color: #000; background: #fff }}
.sheet {{ width: 210mm; height: 297mm; position: relative; page-break-after: always; overflow: hidden }}
.marks {{ position: absolute; left: 0; top: 0 }}
.grid {{ position: absolute; display: grid; grid-template-columns: repeat({COLS}, {W}mm);
  grid-auto-rows: {H}mm; gap: {GAP}mm }}
.card {{ border: 0.12mm solid #000; padding: 3mm; display: flex; flex-direction: column; overflow: hidden }}
.hd {{ background: #000; color: #fff; text-align: center; padding: 1mm 1mm 1.2mm; margin: 0 }}
.org {{ font-weight: 800; font-size: 6.5pt; letter-spacing: 1.2px }}
.lab {{ font-family: 'Archivo Black', sans-serif; font-size: 9pt; letter-spacing: .6px; line-height: 1.15; margin-top: .6mm }}
.ring {{ font-family: 'Archivo Black', sans-serif; font-size: 12.5pt; letter-spacing: 1px; line-height: 1.1 }}
.q {{ flex: 1; display: flex; flex-direction: column; justify-content: center; font-weight: 700;
  font-size: 10.5pt; line-height: 1.22; font-style: italic }}
.q p {{ margin: 0 0 1.1mm }}
.q.order {{ align-items: center; text-align: center; font-family: 'Archivo Black', sans-serif; font-style: normal; font-size: 13pt }}
.bigstag {{ width: 18mm; height: 18mm; margin-bottom: 2mm }}
.sub {{ font-weight: 800; font-size: 7.5pt; text-align: center; border-top: 0.3mm solid #000; padding-top: 1.2mm }}
.ft {{ font-size: 6.5pt; font-weight: 700; text-align: center; margin-top: .6mm; letter-spacing: .3px }}
"""


def document():
    per = COLS * ROWS
    sheets = []
    for i in range(0, len(CARDS), per):
        marks, x0, y0 = crop_marks(-(-len(CARDS[i:i + per]) // COLS))
        cs = "".join(card(*c) for c in CARDS[i:i + per])
        sheets.append(f'<div class="sheet">{marks}<div class="grid" style="left:{x0}mm;top:{y0}mm">{cs}</div></div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><title>Cryptex riddle cards</title><style>{CSS}</style></head><body>{"".join(sheets)}</body></html>'


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


if __name__ == "__main__":
    assert len(CARDS) == 12
    p = os.path.join(HERE, "riddle_cards.html")
    open(p, "w", encoding="utf-8").write(document())
    render([p])
    print("->", p, "+ .pdf")

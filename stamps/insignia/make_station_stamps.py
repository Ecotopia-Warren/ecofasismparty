"""Station stamps for passport page 3 (Inburgering): Interrogation, Carbon Confessions, Verdict, Recycling.

Each stamp is drawn at its real size (mm) so it fits its passport box with margin.
Passport boxes (measured, 2026-11-27): INTERROGATION 62 x 26.5, CORRECTED/CARBON CONFESSIONS 62 x 16.6,
VERDICT 30 x 16.6, RECYCLING 30 x 16.6 mm (the label sits at the top of each box).
Output: ../station/<name>.svg (text converted to paths, ready for StampMaker "Graphic" mode),
        ../station/preview.html (the stamps inside the passport boxes, real size).
"""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "station"); os.makedirs(OUT, exist_ok=True)
F = "DejaVu Sans Condensed"

# name, box label, box (w, h), stamp (w, h), lines [(text, size_mm)]
STAMPS = [
    ("interrogation_answered", "INTERROGATION", (62.2, 26.5), (46, 18), [("ANSWERED", 7.0), ("QUESTIONS ARE WELCOME", 2.6)]),
    ("confessions_forgiven", "CORRECTED · CARBON CONFESSIONS", (62.2, 16.6), (40, 11), [("FORGIVEN", 6.5)]),
    ("verdict_approved", "VERDICT", (30.1, 16.6), (25, 11), [("APPROVED", 4.6)]),
    ("verdict_obligations", "VERDICT", (30.1, 16.6), (25, 11), [("FURTHER", 3.6), ("OBLIGATIONS", 3.6)]),
    ("verdict_denied", "VERDICT", (30.1, 16.6), (25, 11), [("DENIED", 5.5)]),
    ("verdict_recycling", "VERDICT", (30.1, 16.6), (25, 11), [("TO", 3.6), ("RECYCLING", 3.6)]),
    ("recycling_renewed", "RECYCLING", (30.1, 16.6), (25, 11), [("RENEWED", 5.0)]),
]
FRAME, RAD = 0.9, 1.6   # frame line and corner radius, mm

from PIL import ImageFont
_FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf", 100)

def fit_lines(w, lines, pad=3.2):
    """text size s = cap height in mm; shrink a line until it fits the stamp width minus padding"""
    out = []
    for txt, s in lines:
        em = s / 0.73                                         # cap height -> font size
        width = _FONT.getlength(txt) / 100 * em + len(txt) * s * 0.06
        if width > w - 2 * pad: s *= (w - 2 * pad) / width
        out.append((txt, s))
    if len(out) > 1 and lines[0][1] == lines[1][1]:   # same size asked: keep lines equal
        m = min(s for _, s in out); out = [(t, m) for t, _ in out]
    return out

def svg(w, h, lines):
    lines = fit_lines(w, lines)
    tot = sum(s for _, s in lines) * 1.5
    y = (h - tot) / 2
    t = []
    for txt, s in lines:
        y += s * 1.5
        t.append(f'<text x="{w/2}" y="{y - s*0.25:.2f}" font-family="{F}" font-weight="bold" font-size="{s/0.73:.2f}" '
                 f'text-anchor="middle" letter-spacing="{s*0.06:.2f}" fill="#000">{txt}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">'
            f'<rect x="{FRAME/2}" y="{FRAME/2}" width="{w-FRAME}" height="{h-FRAME}" rx="{RAD}" fill="none" stroke="#000" stroke-width="{FRAME}"/>'
            + "".join(t) + "</svg>")

cells = []
for name, label, (bw, bh), (w, h), lines in STAMPS:
    src = os.path.join(OUT, f"_{name}.svg"); dst = os.path.join(OUT, f"{name}.svg")
    open(src, "w").write(svg(w, h, lines))
    subprocess.run(["inkscape", src, "--export-text-to-path", "--export-plain-svg", "--export-filename", dst],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(src)
    cells.append(f'<div class="cell"><div class="box" style="width:{bw}mm;height:{bh}mm"><span>{label}</span>'
                 f'<img src="{name}.svg" style="width:{w}mm;height:{h}mm"></div><p>{name}<br>stamp {w} x {h} mm</p></div>')

open(os.path.join(OUT, "preview.html"), "w").write("""<!doctype html><meta charset="utf-8"><style>
@page{size:A4;margin:12mm} body{font-family:'DejaVu Sans',sans-serif;font-size:8pt;color:#000}
h1{font-size:13pt} .grid{display:flex;flex-wrap:wrap;gap:8mm 10mm}
.box{border:1.2px dashed #000;position:relative;display:flex;align-items:center;justify-content:center;padding-top:3mm;box-sizing:border-box}
.box span{position:absolute;top:.8mm;left:0;right:0;text-align:center;font-weight:800;font-size:7.5pt}
.box img{opacity:.85;transform:rotate(-3deg)} p{margin:1.5mm 0 0}
</style><h1>Station stamps in their passport boxes (real size)</h1><div class="grid">""" + "".join(cells) + "</div>")
print("done:", ", ".join(s[0] for s in STAMPS))

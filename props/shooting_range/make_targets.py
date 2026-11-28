#!/usr/bin/env python3
"""Ecotopia shooting range: printable "official portrait" targets + station sign.

Targets sit inside ordinary picture frames on a wall, like official portraits,
and are shot with foam darts. Eight enemies of the green state (shoot) and two
protected official portraits (DO NOT SHOOT, penalty).

Output (props/shooting_range/out/):
  targets_A4.html/.pdf      one A4 target per page (trim = paper, no crop marks)
  targets_13x18.html/.pdf   one 13x18 cm target per A4 sheet, crop marks
  targets_10x15.html/.pdf   two 10x15 cm targets per A4 landscape sheet, crop marks
  station_sign_A5.html/.pdf the range rules
  svg/<id>_<size>.svg       every target as a standalone SVG (edit in Inkscape)

Style follows the passport and quest cards (Archivo / Archivo Black, black
on white) and the posters (sunburst, the geometric Guardian stag).
PDFs via Playwright/Chromium, same as passport_v2/make_quest_cards.py.

Usage: python3 props/shooting_range/make_targets.py
"""
import html
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
OUT = os.path.join(HERE, "out")

# ------------------------------------------------------------------ CONFIG
# Scoring is a PROPOSAL (OPEN_QUESTIONS #14 is still open). Change it here,
# rerun, and the targets and the sign follow.
DISTANCE_M = 3            # firing line, metres from the wall
DARTS = 5                 # foam darts per citizen per round
BULL, RING, PORTRAIT = 100, 50, 25   # CC per hit: bull / ring / anywhere on the portrait
PENALTY = {"guardian": 200, "governor": 100}   # CC off the round score
STAMP_CC = 100            # 1 credit stamp = 100 CC (QUEST_SYSTEM.md)
STAMP_CAP = 3             # max stamps per round (quests give 1-3)

SIZES = {                 # trim size (mm) = the frame insert
    "A4": (210, 297),
    "13x18": (130, 180),
    "10x15": (100, 148.5),   # 1.5 mm short of 150 so four fit on one A4 (297 / 2)
}

INK, RED, GREY, MID, LIGHT, PAPER = "#111111", "#c8102e", "#8a8a8a", "#5a5a5a", "#e6e6e6", "#ffffff"
SW = 1.4                  # character outline width, in character units
FONTS = "@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:ital,wght@0,500;0,700;0,800;1,700&display=swap');"
BLACK = "font-family:'Archivo Black','DejaVu Sans',sans-serif"
ARCH = "font-family:'Archivo','DejaVu Sans',sans-serif"

# ------------------------------------------------------------------ helpers


def esc(s):
    return html.escape(s, quote=True)


def P(pts):
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)


def poly(pts, fill=INK, stroke=INK, sw=SW, extra=""):
    return f'<polygon points="{P(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def path(d, fill=INK, stroke=INK, sw=SW, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def circ(cx, cy, r, fill=PAPER, stroke=INK, sw=SW, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def ell(cx, cy, rx, ry, fill=PAPER, stroke=INK, sw=SW, extra=""):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def rect(x, y, w, h, fill=PAPER, stroke=INK, sw=SW, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def text(x, y, s, size, style=BLACK, fill=INK, anchor="middle", width=None, per_char=0.66, extra=""):
    """SVG text; squeezed to `width` only when its estimated width overflows."""
    fit = ""
    if width and len(s) * per_char * size > width:
        fit = f'textLength="{width:.2f}" lengthAdjust="spacingAndGlyphs"'
    return (f'<text x="{x:.2f}" y="{y:.2f}" style="{style};font-size:{size:.2f}px;text-anchor:{anchor};fill:{fill}" '
            f'{fit} {extra}>{esc(s)}</text>')


def wrap(s, width, size, per_char=0.5):
    """Greedy word wrap on an estimated glyph width (Archivo bold italic)."""
    max_chars = max(8, int(width / (per_char * size)))
    lines, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + ([cur] if cur else [])


def sunburst(cx, cy, r, n=32, fill=LIGHT):
    out = []
    for i in range(n):
        a0, a1 = 2 * i * math.pi / n, (2 * i + 1) * math.pi / n
        out.append(f'<polygon points="{P([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))])}" fill="{fill}"/>')
    return "".join(out)


def inner_svg(path_, x, y, size):
    """Embed an SVG file as a nested <svg> at (x, y), size x size."""
    src = open(path_).read()
    return src.replace("<svg ", f'<svg x="{x:.2f}" y="{y:.2f}" width="{size:.2f}" height="{size:.2f}" ', 1)


SEAL = os.path.join(ROOT, "passport_v2", "great_seal_bw.svg")
RESIST = os.path.join(ROOT, "stamps", "resistance_ankle_stamp.svg")

# ------------------------------------------------------------- the Guardian
# Same geometric stag as scripts/make_posters.py (copied, not imported: that
# module pulls in potrace/scipy). Units around the forehead centre; antlers to
# y=-78, muzzle to y=+48.
_FACE = [(-14, 0), (14, 0), (17, 8), (10, 30), (6, 44), (0, 49), (-6, 44), (-10, 30), (-17, 8)]
_EAR = [(-13, 3), (-36, -5), (-29, 5), (-17, 13)]
_ANTLER = [
    [(-7, 1), (-15, -18), (-20, -38), (-18, -58), (-11, -76)],
    [(-15, -18), (-31, -25)],
    [(-20, -38), (-37, -50)],
    [(-19, -47), (-8, -52)],
    [(-18, -58), (-29, -78)],
]


def _mirror(pts):
    return [(-x, y) for x, y in pts]


def stag(cx, cy, s, fill=INK, cut=PAPER):
    T = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    parts = [f'<polygon points="{P(T(p))}" fill="{fill}"/>' for p in (_FACE, _EAR, _mirror(_EAR))]
    lines = []
    for seg in _ANTLER:
        for side in (seg, _mirror(seg)):
            lines.append("M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in T(side)))
    parts.append(f'<path d="{" ".join(lines)}" fill="none" stroke="{fill}" stroke-width="{5.2 * s:.2f}" '
                 f'stroke-linejoin="round" stroke-linecap="round"/>')
    for sx in (-1, 1):
        parts.append(f'<polygon points="{P(T([(sx * 5, 15), (sx * 11, 13), (sx * 9, 18)]))}" fill="{cut}"/>')
    parts.append(f'<polygon points="{P(T([(-4, 41), (4, 41), (0, 46)]))}" fill="{cut}"/>')
    return "".join(parts)


# --------------------------------------------------------------- characters
# Bust portraits in a 100 x 125 unit box. Head around (50, 48), shoulders from
# y=84, chest (the ring centre) at CHEST.
CHEST = (50, 100)


def torso(fill=GREY):
    return path("M2,127 C3,102 16,89 34,85 L66,85 C84,89 97,102 98,127 Z", fill)


def neck(fill=PAPER):
    return path("M42,62 L42,88 L58,88 L58,62 Z", fill)


def head(cy=47, rx=17, ry=21, fill=PAPER):
    return ell(50, cy, rx, ry, fill)


def ears(cy=49):
    return ell(33, cy, 3.2, 5.5) + ell(67, cy, 3.2, 5.5)


def dot_eyes(y=46, dx=7, r=1.8):
    return circ(50 - dx, y, r, INK, INK, 0) + circ(50 + dx, y, r, INK, INK, 0)


def smile(y=58, w=7, depth=4):
    return path(f"M{50 - w},{y} Q50,{y + depth} {50 + w},{y}", "none")


def ch_hacker():
    hood = path("M24,64 C21,30 34,15 50,15 C66,15 79,30 76,64 C74,80 66,88 50,89 C34,88 26,80 24,64 Z", INK)
    face = ell(50, 50, 13.5, 17.5, PAPER)
    shade = path("M36.6,44 C38,34 44,32.5 50,32.5 C56,32.5 62,34 63.4,44 C58,39 42,39 36.6,44 Z", GREY, GREY, 0.5)
    glasses = (rect(38.5, 44, 10, 6.5, RED, INK, 1.1, 1) + rect(51.5, 44, 10, 6.5, RED, INK, 1.1, 1)
               + path("M48.5,47 L51.5,47", "none", INK, 1.1)
               + text(43.5, 49, "01", 4.2, "font-family:'DejaVu Sans Mono',monospace;font-weight:700", PAPER)
               + text(56.5, 49, "10", 4.2, "font-family:'DejaVu Sans Mono',monospace;font-weight:700", PAPER))
    mouth = path("M45,60 L55,59", "none")
    body = torso(INK)
    strings = (path("M45,88 L44,104", "none", PAPER, 1.2) + path("M55,88 L56,104", "none", PAPER, 1.2)
               + circ(44, 105, 1.4, PAPER, PAPER, 0) + circ(56, 105, 1.4, PAPER, PAPER, 0))
    pocket = path("M30,127 L34,112 L66,112 L70,127", "none", MID, 1.2)
    code = text(50, 121, "? ? ?", 6, BLACK, MID)
    return body + strings + pocket + code + hood + face + shade + glasses + mouth


def ch_smuggler():
    coat = torso(GREY)
    lining = poly([(35, 86), (50, 127), (65, 86)], RED)
    loot = (rect(40.5, 96, 6, 15, PAPER, INK, 1, 2) + rect(42, 93, 3, 3.5, INK, INK, 0.6)
            + rect(53, 99, 6, 13, PAPER, INK, 1, 2) + rect(54.5, 96, 3, 3.5, INK, INK, 0.6)
            + path("M47.5,90 L49,112", "none", INK, 1.6) + path("M50.5,91 L51.5,113", "none", PAPER, 1.6)
            + path("M50.5,91 L51.5,113", "none", INK, 0.5, 'stroke-dasharray="1.6 1.6"'))
    lapels = poly([(35, 86), (44, 100), (40, 86)], MID) + poly([(65, 86), (56, 100), (60, 86)], MID)
    collar = poly([(36, 86), (33, 66), (42, 74)], GREY) + poly([(64, 86), (67, 66), (58, 74)], GREY)
    hat = (ell(50, 32, 30, 5.5, INK) + path("M34,32 C33,14 67,14 66,32 Z", INK)
           + rect(34.6, 25, 30.8, 4.5, RED, INK, 0.8))
    shades = path("M36,44 L49,44 L48,51 C47,53 38,53 37,51 Z", INK) + path("M51,44 L64,44 L63,51 C62,53 53,53 52,51 Z", INK) \
        + path("M49,45 L51,45", "none", INK, 1.2)
    grin = path("M44,59 Q52,62 57,57", "none")
    stubble = "".join(circ(x, y, 0.5, INK, INK, 0) for x, y in [(42, 62), (45, 64), (48, 65), (52, 65), (55, 64), (58, 62), (46, 61), (54, 61)])
    return coat + lining + loot + lapels + neck() + head() + ears() + collar + shades + grin + stubble + hat


def ch_hoarder():
    suit = torso(INK)
    shirt = poly([(38, 86), (50, 112), (62, 86)], PAPER)
    vest = path("M40,90 L50,112 L60,90 L64,127 L36,127 Z", RED)
    buttons = "".join(circ(50, y, 1.1, INK, INK, 0) for y in (116, 121))
    chain = path("M40,113 Q46,119 50,116", "none", PAPER, 1)
    tie = poly([(47.5, 86), (52.5, 86), (50, 92)], INK)
    face = head(48, 18.5, 20) + ears(50)
    monocle = circ(57, 46, 4.6, "none", INK, 1.3) + path("M61.6,46 C66,52 64,60 62,66", "none", INK, 0.7)
    eye = circ(43, 46, 1.8, INK, INK, 0) + circ(57, 46, 1.6, INK, INK, 0)
    stache = path("M50,55 C46,51 39,52 37,56 C40,55 44,57 50,57 C56,57 60,55 63,56 C61,52 54,51 50,55 Z", INK)
    smug = path("M45,61 Q50,63.5 55,61", "none")
    hat = (ell(50, 30, 24, 4.5, INK) + rect(36, 6, 28, 24, INK, INK, SW)
           + rect(36, 22, 28, 4.5, GREY, INK, 0.8) + text(50, 25.6, "CO₂", 4.4, BLACK, INK))
    smoke = (circ(66, 2, 4.5, LIGHT, MID, 0.8) + circ(73, -3, 5.5, LIGHT, MID, 0.8)
             + circ(81, -6, 6.5, LIGHT, MID, 0.8) + rect(58, 2, 6, 6, INK, INK, SW))
    sack = (path("M70,84 C66,74 76,66 86,70 C96,74 98,90 92,96 C86,100 74,96 70,84 Z", GREY)
            + path("M72,80 L80,74", "none", INK, 1.6) + text(84, 88, "CO₂", 7, BLACK, INK))
    return suit + shirt + vest + buttons + chain + tie + neck() + face + monocle + eye + stache + smug + smoke + hat + sack


def ch_rebel():
    pole = path("M84,127 L72,26", "none", MID, 2.6)
    flag = poly([(72, 28), (94, 31), (92, 48), (74, 45)], INK, INK, 1)
    flag_text = (f'<g transform="rotate(7 83 38)">' + text(83, 37, "THE STAG", 3.4, BLACK, PAPER)
                 + text(83, 42, "IS SILICON", 3.4, BLACK, PAPER) + "</g>")
    jacket = torso(INK)
    zipper = path("M50,88 L50,127", "none", GREY, 1.2)
    patch = circ(CHEST[0] + 16, CHEST[1] - 4, 8.6, PAPER, INK, 1) + inner_svg(RESIST, CHEST[0] + 7.5, CHEST[1] - 12.5, 17)
    face = head() + ears()
    brows = path("M37,42 L47,44.5", "none", INK, 2) + path("M63,42 L53,44.5", "none", INK, 2)
    eyes = dot_eyes(47.5, 7, 1.9)
    bandana = path("M31,52 C40,56 60,56 69,52 C69,62 60,70 50,71 C40,70 31,62 31,52 Z", RED)
    dots = "".join(circ(x, y, 0.9, PAPER, PAPER, 0) for x, y in [(40, 58), (46, 60), (54, 60), (60, 58), (44, 65), (50, 66), (56, 65), (50, 61)])
    beanie = path("M31,40 C30,20 70,20 69,40 Z", MID) + rect(30, 36, 40, 6, INK, INK, SW, 2)
    return pole + flag + flag_text + jacket + zipper + patch + neck() + face + brows + eyes + bandana + dots + beanie


def ch_wasteland():
    rags = torso(MID)
    strap = path("M22,92 L76,127", "none", INK, 5) + "".join(circ(22 + i * 9, 92 + i * 5.8, 1.3, GREY, GREY, 0) for i in range(1, 6))
    pads = "".join(
        path(f"M{x - 15},{y + 4} A15,12 0 0 1 {x + 15},{y + 4} Z", INK)
        + "".join(path(f"M{x - 12 + i * 6},{y - 4} L{x - 11 + i * 6},{y + 2}", "none", PAPER, 1.1) for i in range(5))
        for x, y in ((22, 92), (78, 92)))
    wrap_ = path("M30,48 C28,26 72,26 70,48 C72,64 64,74 50,75 C36,74 28,64 30,48 Z", GREY)
    mohawk = "".join(poly([(x - 4, 28), (x, 9 + abs(x - 50) * 0.35), (x + 4, 28)], INK) for x in (40, 46, 52, 58))
    goggles = (path("M30,42 L70,42", "none", INK, 4) + circ(41, 43, 7, RED, INK, 2) + circ(59, 43, 7, RED, INK, 2)
               + path("M38,40 L40,38", "none", PAPER, 1.2) + path("M56,40 L58,38", "none", PAPER, 1.2))
    mask = path("M38,52 C38,49 62,49 62,52 L60,62 C56,68 44,68 40,62 Z", INK)
    filt = circ(50, 69, 6.5, GREY, INK, 1.4) + "".join(path(f"M{45 + i * 2.5},65 L{45 + i * 2.5},73", "none", INK, 0.8) for i in range(5))
    return rags + strap + pads + neck(GREY) + wrap_ + mohawk + goggles + mask + filt


def ch_car():
    jacket = torso(GREY)
    stripes = path("M30,87 L18,127", "none", RED, 4) + path("M70,87 L82,127", "none", RED, 4)
    patch = ""
    collar = rect(40, 80, 20, 8, INK, INK, SW, 2)
    helmet = circ(50, 46, 24, RED, INK, SW) + path("M50,22 L50,70", "none", PAPER, 4)
    visor = rect(31, 37, 38, 15, INK, INK, SW, 6) + circ(42, 44.5, 2.2, PAPER, PAPER, 0) + circ(58, 44.5, 2.2, PAPER, PAPER, 0) \
        + path("M35,40 L41,39", "none", GREY, 1)
    chin = path("M33,58 C38,70 62,70 67,58 Z", INK) + "".join(rect(40 + i * 5, 60, 3, 4, GREY, GREY, 0) for i in range(4))
    exhaust = (rect(74, 70, 16, 6, GREY, INK, 1.2, 1) + ell(90, 73, 2, 3, INK, INK, 0) + text(81, 75, "V8", 4.4, BLACK, PAPER)
               + circ(90, 62, 5, LIGHT, MID, 0.8) + circ(94, 52, 6.5, LIGHT, MID, 0.8) + circ(91, 41, 7.5, LIGHT, MID, 0.8))
    return jacket + stripes + patch + exhaust + collar + helmet + visor + chin


def ch_flyer():
    plane = (f'<g transform="translate(80 20) rotate(-20)">'
             + path("M-11,0 L11,0 C14,0 14,2 11,2 L-11,2 Z", INK, INK, 0.8)
             + poly([(-1, 1), (-7, -9), (-3, -9), (5, 1)], INK, INK, 0.6)
             + poly([(-1, 1), (-7, 11), (-3, 11), (5, 1)], INK, INK, 0.6)
             + poly([(-11, 1), (-14, -4), (-12, -4), (-8, 1)], INK, INK, 0.6) + "</g>"
             + path("M60,32 Q66,30 70,26", "none", MID, 0.8, 'stroke-dasharray="1.5 1.5"'))
    jacket = torso(MID)
    fur = "".join(circ(30 + i * 5, 86 + abs(i - 4) * 0.6, 3.2, PAPER, INK, 0.9) for i in range(9))
    wings = (path(f"M{CHEST[0] - 22},{CHEST[1] - 4} Q{CHEST[0] - 14},{CHEST[1] - 9} {CHEST[0] - 6},{CHEST[1] - 4} "
                  f"Q{CHEST[0] - 14},{CHEST[1] - 1} {CHEST[0] - 22},{CHEST[1] - 4} Z", INK, INK, 0.6)
             + circ(CHEST[0] - 14, CHEST[1] - 4.5, 2.4, RED, INK, 0.6))
    ticket = rect(CHEST[0] + 6, CHEST[1] + 5, 16, 9, PAPER, INK, 1, 1) + "".join(
        path(f"M{CHEST[0] + 8 + i * 1.6},{CHEST[1] + 7} L{CHEST[0] + 8 + i * 1.6},{CHEST[1] + 12}", "none", INK, 0.6 + (i % 3) * 0.35)
        for i in range(8))
    pocket = rect(CHEST[0] + 4, CHEST[1] + 10, 20, 12, MID, INK, 1)
    scarf = path("M40,80 C46,86 54,86 60,80 L60,86 C54,92 46,92 40,86 Z", RED) + path("M57,85 C68,92 78,90 88,96 L84,104 C74,98 66,100 56,92 Z", RED)
    face = head(48) + dot_eyes(48, 7, 1.8) + path("M41,57 Q50,66 59,57 Z", PAPER)
    cap = path("M32,46 C30,20 70,20 68,46 L68,62 C66,64 64,64 63,62 L63,46 L37,46 L37,62 C36,64 34,64 32,62 Z", MID)
    goggles = path("M32,36 L68,36", "none", INK, 2.6) + circ(43, 35, 5.6, PAPER, INK, 1.6) + circ(57, 35, 5.6, PAPER, INK, 1.6) \
        + path("M41,33 L43,31", "none", GREY, 1) + path("M55,33 L57,31", "none", GREY, 1)
    return plane + jacket + pocket + ticket + wings + fur + neck() + face + cap + goggles + scarf


def ch_vegan():
    sweater = torso(GREY)
    knit = "".join(path(f"M{x},90 L{x - 2},127", "none", MID, 0.8) for x in (22, 32, 68, 78))
    strap = path("M30,88 L46,127", "none", INK, 3)
    badge = circ(CHEST[0] - 26, CHEST[1] + 8, 9, PAPER, INK, 1.2) + text(CHEST[0] - 26, CHEST[1] + 7.6, "PLANT", 3.6, BLACK) \
        + text(CHEST[0] - 26, CHEST[1] + 12, "BASED*", 3.6, BLACK) \
        + path(f"M{CHEST[0] - 29},{CHEST[1] + 3} Q{CHEST[0] - 26},{CHEST[1] - 1} {CHEST[0] - 23},{CHEST[1] + 3} Q{CHEST[0] - 26},{CHEST[1] + 4} {CHEST[0] - 29},{CHEST[1] + 3} Z", INK, INK, 0.4)
    drum = (path("M84,96 C78,92 76,84 82,80 C88,76 96,80 95,88 C94,94 90,96 84,96 Z", MID)
            + path("M86,95 L80,106", "none", PAPER, 3.2) + circ(79.5, 107.5, 2, PAPER, INK, 0.8) + circ(81.5, 108.5, 2, PAPER, INK, 0.8)
            + circ(88, 104, 4.5, PAPER, INK, 1.2))
    face = head(49) + ears(51)
    eyes = path("M40,47 Q43,44 46,47", "none", INK, 1.5) + path("M54,47 Q57,44 60,47", "none", INK, 1.5)
    grin = path("M41,57 Q50,67 59,57 Z", PAPER)
    blush = ell(38, 54, 3, 1.6, "#f0b0b8", "none", 0) + ell(62, 54, 3, 1.6, "#f0b0b8", "none", 0)
    hair = path("M32,46 C30,26 70,26 68,46 C64,36 56,33 50,33 C44,33 36,36 32,46 Z", INK) + circ(50, 22, 7.5, INK)
    leaves = "".join(path(f"M{x},55 Q{x - 3},60 {x},64 Q{x + 3},60 {x},55 Z", PAPER, INK, 0.8) for x in (33, 67))
    return sweater + knit + strap + badge + drum + neck() + face + eyes + grin + blush + hair + leaves


def ch_guardian():
    mantle = torso(INK) + path("M28,86 C36,96 64,96 72,86", "none", RED, 3)
    medal = circ(CHEST[0], CHEST[1] + 2, 10, RED, INK, 1.2) + inner_svg(SEAL, CHEST[0] - 8.5, CHEST[1] - 6.5, 17)
    chain = path(f"M30,88 L{CHEST[0] - 6},{CHEST[1] - 6}", "none", RED, 1.6, 'stroke-dasharray="2 1.2"') \
        + path(f"M70,88 L{CHEST[0] + 6},{CHEST[1] - 6}", "none", RED, 1.6, 'stroke-dasharray="2 1.2"')
    neck_ = poly([(42, 60), (58, 60), (64, 90), (36, 90)], INK, INK, 0)
    return mantle + neck_ + chain + medal + stag(50, 44, 0.52)


def ch_governor():
    tunic = torso(GREY)
    collar = path("M38,84 L38,92 C44,96 56,96 62,92 L62,84 Z", INK)
    sash = path("M28,90 L36,86 L80,127 L66,127 Z", RED)
    medals = "".join(
        rect(CHEST[0] - 26 + i * 6, CHEST[1] - 6, 4, 6, [RED, INK, PAPER][i], INK, 0.6)
        + circ(CHEST[0] - 24 + i * 6, CHEST[1] + 3, 2.4, PAPER, INK, 0.8) for i in range(3))
    brooch = path(f"M{CHEST[0] + 12},{CHEST[1] - 10} Q{CHEST[0] + 4},{CHEST[1] - 2} {CHEST[0] + 12},{CHEST[1] + 6} "
                  f"Q{CHEST[0] + 20},{CHEST[1] - 2} {CHEST[0] + 12},{CHEST[1] - 10} Z", PAPER, INK, 1) \
        + path(f"M{CHEST[0] + 12},{CHEST[1] - 8} L{CHEST[0] + 12},{CHEST[1] + 5}", "none", INK, 0.6)
    face = head(48) + ears(50)
    glasses = circ(43, 47, 4.6, "none", INK, 1.1) + circ(57, 47, 4.6, "none", INK, 1.1) + path("M47.6,47 L52.4,47", "none", INK, 1.1)
    eyes = path("M40.5,47.5 Q43,45.5 45.5,47.5", "none", INK, 1.2) + path("M54.5,47.5 Q57,45.5 59.5,47.5", "none", INK, 1.2)
    grin = path("M43,58 Q50,63 57,58", "none", INK, 1.4)
    hair = path("M32,48 C28,22 72,22 68,48 C64,34 54,30 44,34 C38,36 34,42 32,48 Z", INK) + ell(50, 25, 10, 6, INK)
    return tunic + sash + collar + medals + brooch + neck() + face + glasses + eyes + grin + hair


# ------------------------------------------------------------ the roster
# (id, case no., draw, name lines, charge, protected-key or None)
TARGETS = [
    ("hacker", "V-01", ch_hacker, ["THE HACKER"],
     "Asked a banned machine a question, and it answered. Both are being looked after. If found, please return gently.", None),
    ("smuggler", "V-02", ch_smuggler, ["PLASTIC", "SMUGGLER"],
     "Carries single-use items across the border of good taste. The Ministry of Light would love a word.", None),
    ("hoarder", "V-03", ch_hoarder, ["CARBON", "HOARDER"],
     "Kept four tonnes of carbon all to themselves. R.E.I.G.N. believes in sharing, and has already arranged it.", None),
    ("rebel", "V-04", ch_rebel, ["RESISTANCE", "AGITATOR"],
     "Spreads unscheduled questions. Questions are welcome. They have already been answered.", None),
    ("wasteland", "V-05", ch_wasteland, ["WASTELAND", "CARBON CRIMINAL"],
     "Lives outside the dome and breathes unmetered air. Sighing is a form of emission.", None),
    ("car", "V-06", ch_car, ["COMBUSTION", "ENTHUSIAST"],
     "Declared, under oath: “I am, spiritually, a car.” A quieter place to idle has been found.", None),
    ("flyer", "V-07", ch_flyer, ["FREQUENT", "FLYER"],
     "Flew eleven times last year and called it “work”. Every flight was counted, including yours.", None),
    ("vegan", "V-08", ch_vegan, ["“BASICALLY", "VEGAN”"],
     "Said “basically vegan” eleven times tonight. The drumstick has been noted. The Ministry of Purity recommends pulse paste.", None),
    ("guardian", "P-01", ch_guardian, ["THE GUARDIAN"],
     "It sees everything, and it forgives most of it. Most of it.", "guardian"),
    ("governor", "P-02", ch_governor, ["A GOVERNOR", "OF R.E.I.G.N."],
     "Reads every concern. Every single one. Please keep your evenings free.", "governor"),
]


# ------------------------------------------------------------- one target
def target(t, w, h, uid, b=4.5, safe=None):
    """One target, trim box (0,0)-(w,h) in mm. Returns SVG body (no <svg>)."""
    tid, case, draw, name, charge, prot = t
    k = min(w / 130, h / 180)                 # type scale
    if safe is None:
        safe = 8.5 if w >= 120 else 7.5       # frame lip hides ~5 mm
    inner_w = w - 2 * safe
    o = []
    # decorative double frame, just inside where the frame lip ends
    o.append(rect(b, b, w - 2 * b, h - 2 * b, "none", INK, 1.6 * k))
    o.append(rect(b + 2 * k, b + 2 * k, w - 2 * b - 4 * k, h - 2 * b - 4 * k, "none", INK, 0.45 * k))

    # header band
    hh = 14 * k
    hy = safe
    band = RED if prot else INK
    o.append(rect(safe, hy, inner_w, hh, band, band, 0))
    icon = hh - 2.4 * k
    o.append(inner_svg(SEAL, safe + 1.2 * k, hy + 1.2 * k, icon))
    word = "DO NOT SHOOT" if prot else "MOST WANTED"
    tx0 = safe + icon + 3 * k
    o.append(text(tx0, hy + 9.4 * k, word, 9.6 * k, BLACK, PAPER, "start", inner_w - icon - 5 * k - 11 * k))
    o.append(text(safe + inner_w - 1.6 * k, hy + 5.2 * k, case, 3.6 * k, BLACK, PAPER, "end"))
    sub = ("PROTECTED PORTRAIT · BY DECREE OF R.E.I.G.N." if prot
           else "MINISTRY OF VIGILANCE · ENEMY OF THE GREEN STATE")
    o.append(text(w / 2, hy + hh + 4 * k, sub, 3 * k, ARCH + ";font-weight:800;letter-spacing:.3px", INK, "middle",
                  inner_w, 0.6))

    # nameplate (bottom)
    lines = wrap(charge, inner_w - 4 * k, 3.5 * k)
    name_sz = 10.5 * k
    plate_h = 5.5 * k + len(name) * name_sz * 1.02 + 2.5 * k
    charge_h = len(lines) * 3.5 * k * 1.25 + 2 * k
    py = h - safe - charge_h - plate_h
    o.append(rect(safe, py, inner_w, plate_h, INK, INK, 0, 1.5 * k))
    o.append(rect(safe + 1 * k, py + 1 * k, inner_w - 2 * k, plate_h - 2 * k, "none", PAPER, 0.4 * k, 1 * k))
    label = "OFFICIAL PORTRAIT" if prot else "WANTED"
    o.append(text(w / 2, py + 5 * k, label, 3.6 * k, ARCH + ";font-weight:800;letter-spacing:1.5px",
                  "#ffb3bd", "middle"))
    for i, ln in enumerate(name):
        o.append(text(w / 2, py + 5.5 * k + (i + 1) * name_sz * 1.0 - 0.4 * k, ln, name_sz, BLACK, PAPER, "middle",
                      inner_w - 6 * k, 0.7))
    for i, ln in enumerate(lines):
        o.append(text(w / 2, py + plate_h + 4.6 * k + i * 3.5 * k * 1.25, ln, 3.5 * k,
                      ARCH + ";font-weight:700;font-style:italic", INK, "middle", inner_w, 0.5))

    # portrait oval
    top = hy + hh + 6.5 * k
    bot = py - 2.5 * k
    cx, cy = w / 2, (top + bot) / 2
    rx, ry = inner_w / 2, (bot - top) / 2
    cid = f"ov-{uid}"
    o.append(f'<clipPath id="{cid}"><ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}"/></clipPath>')
    s = min(2 * rx / 100, (2 * ry) / 112)
    ox, oy = cx - 50 * s, (cy + ry) - 125 * s + 1.5 * s
    art = f'<g transform="translate({ox:.2f} {oy:.2f}) scale({s:.4f})">{draw()}</g>'
    bg = f'<rect x="0" y="0" width="{w}" height="{h}" fill="{PAPER}"/>' + sunburst(cx, cy + ry * 0.15, max(rx, ry) * 1.6, 36)
    o.append(f'<g clip-path="url(#{cid})">{bg}{art}')
    OVAL = ell(cx, cy, rx, ry, "none", INK, 1.6 * k) + ell(cx, cy, rx - 1.6 * k, ry - 1.6 * k, "none", INK, 0.4 * k)
    if not prot:
        # hit zones: whole portrait = PORTRAIT, ring = RING, bull = BULL
        rcx, rcy = ox + CHEST[0] * s, oy + CHEST[1] * s
        rb = max(12.5, 0.105 * w)
        r50 = 2.15 * rb
        o.append(circ(rcx, rcy, r50, "none", PAPER, 3.4 * k) + circ(rcx, rcy, r50, "none", RED, 1.5 * k))
        o.append(circ(rcx, rcy, rb, PAPER, PAPER, 0, 'fill-opacity="0.82"') + circ(rcx, rcy, rb, "none", RED, 1.7 * k))
        o.append(circ(rcx, rcy, rb - 2.2 * k, "none", RED, 0.5 * k))
        o.append(text(rcx, rcy + rb * 0.3, str(BULL), rb * 0.86, BLACK, RED, "middle"))
        o.append("</g>")
        # ring and portrait value pills (outside the clip so they stay whole)
        def pill(x, y, label, fill=RED):
            pw, ph = (len(label) * 2.9 + 3.4) * k, 5.6 * k
            return (rect(x - pw / 2, y - ph / 2, pw, ph, fill, PAPER, 0.7 * k, ph / 2)
                    + text(x, y + 1.75 * k, label, 4.6 * k, BLACK, PAPER, "middle"))
        o.append(OVAL)
        o.append(pill(rcx, rcy - r50, str(RING)))
        a = math.radians(212)
        o.append(pill(cx + rx * 0.80 * math.cos(a), cy + ry * 0.80 * math.sin(a), str(PORTRAIT), INK))
    else:
        o.append("</g>")
        o.append(OVAL)
        pr = max(10.5, 0.11 * w)
        sx, sy = cx + rx * 0.58, cy + ry * 0.5
        o.append(circ(sx, sy, pr, RED, PAPER, 1.2 * k) + circ(sx, sy, pr - 2 * k, "none", PAPER, 0.5 * k, 'stroke-dasharray="1.2 1"'))
        o.append(text(sx, sy + pr * 0.1, f"−{PENALTY[prot]}", pr * 0.46, BLACK, PAPER, "middle"))
        o.append(text(sx, sy + pr * 0.5, "CC", pr * 0.26, BLACK, PAPER, "middle"))
    return "\n".join(o)


def cut_ticks(xs, ys, pw, ph, top, bot, left, right, ln=6, gap=1.5, sw=0.3):
    """Guillotine marks: every straight cut runs the full sheet. A tick for each
    cut x at the top/bottom margin, for each cut y at the left/right margin.
    Where a margin is 0 (the paper edge is the trim) the tick sits on the edge."""
    out = []
    L = lambda x1, y1, x2, y2: out.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#000" stroke-width="{sw}"/>')
    for x in xs:
        if top > gap:
            L(x, max(0.5, top - gap - ln), x, top - gap)
        if ph - bot > gap:
            L(x, bot + gap, x, min(ph - 0.5, bot + gap + ln))
    for y in ys:
        if left > gap:
            L(max(0.5, left - gap - ln), y, left - gap, y)
        if pw - right > gap:
            L(right + gap, y, min(pw - 0.5, right + gap + ln), y)
    return "".join(out)


def sheet_note(x, y, text_, w_avail, bar=True):
    out = ""
    if bar:
        out = (f'<rect x="{x}" y="{y}" width="50" height="2.4" fill="#000"/>'
               + "".join(f'<rect x="{x + i * 10}" y="{y}" width="10" height="2.4" fill="#fff" stroke="#000" stroke-width="0.2"/>'
                         for i in (1, 3))
               + text(x + 53, y + 2.3, "= 50 mm at 100 % / actual size.", 2.6, ARCH + ";font-weight:700", INK, "start"))
        x += 100
    return out + text(x, y + 2.3, text_, 2.6, ARCH + ";font-weight:800", INK, "start", w_avail - (100 if bar else 0), 0.5)


def svg_doc(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')


# ---------------------------------------------------------------- pages
def page_html(title, pages, pw, ph):
    css = f"""{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#444;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:{pw}mm;height:{ph}mm;background:#fff;margin:6mm auto;overflow:hidden}}
.pg svg{{display:block}}
@page{{size:{pw}mm {ph}mm;margin:0}}
@media print{{body{{background:none}}.pg{{margin:0;page-break-after:always}}}}"""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(title)}</title>'
            f'<style>{css}</style></head><body>' + "".join(f'<div class="pg">{p}</div>' for p in pages) + "</body></html>")


def build_targets():
    """Plain A4 sheets, no full bleed. A4: no cut. 13x18: 2 per landscape A4.
    10x15: 4 per portrait A4. Targets butt together, so cuts are shared."""
    os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)
    for size, (w, h) in SIZES.items():
        for t in TARGETS:
            with open(os.path.join(OUT, "svg", f"{t[0]}_{size}.svg"), "w") as f:
                f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<!-- {FONTS} -->\n'
                        + svg_doc(w, h, target(t, w, h, f"{t[0]}{size}")))
    files = []
    # A4: the sheet is the insert; 6 mm white edge for the printer, the mat hides it
    w, h = SIZES["A4"]
    pages = [svg_doc(w, h, target(t, w, h, f"a4{i}", b=6.5, safe=10.5)) for i, t in enumerate(TARGETS)]
    files.append(write("targets_A4.html", page_html("Ecotopia range targets A4", pages, 210, 297)))
    # 13x18: two side by side on A4 landscape, 3 vertical + 2 horizontal cuts
    w, h = SIZES["13x18"]
    pw, ph = 297, 210
    x0, y0 = (pw - 2 * w) / 2, 12
    pages = []
    for i in range(0, len(TARGETS), 2):
        body = "".join(f'<g transform="translate({x0 + j * w} {y0})">{target(t, w, h, f"m{i + j}")}</g>'
                       for j, t in enumerate(TARGETS[i:i + 2]))
        body += cut_ticks([x0, x0 + w, x0 + 2 * w], [y0, y0 + h], pw, ph, y0, y0 + h, x0, x0 + 2 * w)
        body += f'<line x1="{x0 + w}" y1="{y0}" x2="{x0 + w}" y2="{y0 + h}" stroke="#bbb" stroke-width="0.2" stroke-dasharray="2 2"/>'
        body += sheet_note(x0, y0 + h + 6, "13 x 18 cm inserts · cut on the marks (5 straight cuts) · TAKE THE GLASS OUT OF THE FRAME", 2 * w)
        pages.append(svg_doc(pw, ph, body))
    files.append(write("targets_13x18.html", page_html("Ecotopia range targets 13x18", pages, pw, ph)))
    # 10x15: four on A4 portrait (2 x 148.5 = 297, top and bottom edges are the trim)
    w, h = SIZES["10x15"]
    pw, ph = 210, 297
    x0 = (pw - 2 * w) / 2
    pages = []
    for i in range(0, len(TARGETS), 4):
        body = ""
        for j, t in enumerate(TARGETS[i:i + 4]):
            x, y = x0 + (j % 2) * w, (j // 2) * h
            body += f'<g transform="translate({x} {y})">{target(t, w, h, f"s{i + j}", b=5.5, safe=8.5)}</g>'
        body += cut_ticks([x0, x0 + w, x0 + 2 * w], [h], pw, ph, 0, ph, x0, x0 + 2 * w)
        # marks for the vertical cuts on the paper edge itself
        body += "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="3" stroke="#000" stroke-width="0.3"/>'
                        f'<line x1="{x}" y1="{ph - 3}" x2="{x}" y2="{ph}" stroke="#000" stroke-width="0.3"/>'
                        for x in (x0, x0 + w, x0 + 2 * w))
        pages.append(svg_doc(pw, ph, body))
    files.append(write("targets_10x15.html", page_html("Ecotopia range targets 10x15", pages, pw, ph)))
    return files


def write(name, content):
    p = os.path.join(OUT, name)
    with open(p, "w") as f:
        f.write(content)
    return p


# ----------------------------------------------------------- station sign
def build_sign():
    pen_g, pen_v = PENALTY["guardian"], PENALTY["governor"]
    hdr = svg_doc(128, 34, '<rect width="128" height="34" fill="#111"/>' + sunburst(64, 40, 120, 40, "#333")
                  + stag(64, 21, 0.25, PAPER, "#111"))
    css = f"""{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#444;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:'Archivo','DejaVu Sans',sans-serif;color:#111}}
.pg{{width:148mm;height:210mm;background:#fff;margin:6mm auto;padding:8mm 10mm;display:flex;flex-direction:column;position:relative}}
.frame{{position:absolute;inset:4.5mm;border:2px solid #111;pointer-events:none}}
.frame:after{{content:"";position:absolute;inset:1.2mm;border:.6px solid #111}}
.hdr{{display:block;width:128mm;height:34mm;margin-bottom:2.5mm}}
.k{{font-family:'Archivo Black',sans-serif;font-size:8.5pt;letter-spacing:2px;text-align:center;color:{RED}}}
h1{{font-family:'Archivo Black',sans-serif;font-size:28pt;line-height:.95;text-align:center;margin:1mm 0 1mm}}
.sub{{font-size:9pt;font-weight:700;font-style:italic;text-align:center;margin-bottom:3mm}}
ol{{list-style:none;counter-reset:r;display:flex;flex-direction:column;gap:2.6mm}}
ol li{{counter-increment:r;display:flex;gap:2.5mm;align-items:flex-start;font-size:11.2pt;font-weight:700;line-height:1.24}}
ol li:before{{content:counter(r);flex:none;width:6.5mm;height:6.5mm;border-radius:50%;background:#111;color:#fff;
 font-family:'Archivo Black',sans-serif;font-size:10pt;display:flex;align-items:center;justify-content:center;margin-top:-.4mm}}
b.big{{font-family:'Archivo Black',sans-serif;font-weight:400}}
.score{{display:grid;grid-template-columns:repeat(5,1fr);gap:1.5mm;margin:3mm 0 2.5mm;text-align:center}}
.score div{{border:2px solid #111;border-radius:1.5mm;padding:1mm .5mm;font-size:6.6pt;font-weight:800;line-height:1.1}}
.score div b{{display:block;font-family:'Archivo Black',sans-serif;font-size:13pt;font-weight:400}}
.score .bad{{background:{RED};border-color:{RED};color:#fff}}
.stamp{{border:2.5px solid #111;padding:1.6mm 2mm;text-align:center;font-weight:800;font-size:9.5pt;line-height:1.25}}
.stamp b{{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:11pt}}
.safe{{margin-top:auto;background:#111;color:#fff;padding:2.2mm 3mm;font-size:8.6pt;font-weight:700;line-height:1.3}}
.safe h2{{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:10pt;letter-spacing:1px;color:#fff;margin-bottom:.6mm}}
.ex{{font-size:9.5pt;font-weight:700;text-align:center;margin-top:2.5mm}}
.foot{{font-size:7pt;font-weight:700;font-style:italic;text-align:center;margin-top:1.8mm}}
@page{{size:148mm 210mm;margin:0}}
@media print{{body{{background:none}}.pg{{margin:0}}}}"""
    body = f"""<div class="pg"><div class="frame"></div>
{hdr.replace('<svg ', '<svg class="hdr" ', 1)}
<div class="k">MINISTRY OF VIGILANCE · CITIZEN PRACTICE RANGE</div>
<h1>THE GALLERY OF<br>GENTLE CORRECTION</h1>
<div class="sub">Every dart is a small act of care. R.E.I.G.N. does the aiming, so that you need not.</div>
<ol>
<li><span>Stand behind the line: <b class="big">{DISTANCE_M} metres</b>. Foam darts only, from the range official.</span></li>
<li><span><b class="big">{DARTS} darts</b> per citizen per round. One round, then rejoin the queue.</span></li>
<li><span>Hit an enemy of the green state: bull, ring, or anywhere on the portrait. Frame or wall: nothing.</span></li>
<li><span><b class="big">DO NOT SHOOT</b> the official portraits. A Governor costs {pen_v} CC, the Guardian {pen_g} CC, off this round.</span></li>
</ol>
<div class="score">
<div><b>{BULL}</b>CC<br>bull</div><div><b>{RING}</b>CC<br>ring</div><div><b>{PORTRAIT}</b>CC<br>portrait</div>
<div class="bad"><b>&minus;{pen_v}</b>CC<br>Governor</div><div class="bad"><b>&minus;{pen_g}</b>CC<br>Guardian</div>
</div>
<div class="stamp">Every <b>{STAMP_CC} CC</b> in a round = <b>1 credit stamp</b> (max {STAMP_CAP} per round).<br>
The range official counts and stamps your passport.</div>
<div class="ex">Example round: {BULL} + {RING} + {PORTRAIT} + {PORTRAIT} + miss = {BULL+RING+2*PORTRAIT} CC = <b>{min(STAMP_CAP,(BULL+RING+2*PORTRAIT)//STAMP_CC)} stamps</b>.</div>
<div class="safe"><h2>SAFETY &amp; CONSENT</h2>
Aim only at the frames. Never at faces, people or animals.<br>
Wait behind the line until the official calls <b>CLEAR</b>. Only the official fetches darts.<br>
The official's call is final. Taking part is voluntary: you may step out at any time.</div>
<div class="foot">A bad round never costs you credits you already have. R.E.I.G.N. only adjusts the round.</div>
</div>"""
    html_ = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Ecotopia range sign A5</title>'
             f'<style>{css}</style></head><body>{body}</body></html>')
    two = (css.replace("@page{size:148mm 210mm;margin:0}", "@page{size:297mm 210mm;margin:0}")
           + ".two{width:297mm;height:210mm;display:flex;background:#fff;margin:6mm auto}.two .pg{margin:0}"
           + ".two .pg+.pg{border-left:.3mm dashed #999}@media print{.two{margin:0;overflow:hidden}}")
    html2 = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Ecotopia range sign 2x A5 on A4</title>'
             f'<style>{two}</style></head><body><div class="two">{body}{body}</div></body></html>')
    return [write("station_sign_A5.html", html_), write("station_sign_2xA5_on_A4.html", html2)]


def render(paths):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.set_default_timeout(300_000)
        for p in paths:
            pg.goto("file://" + p, wait_until="networkidle")
            pg.evaluate("document.fonts.ready.then(() => true)")
            pg.emulate_media(media="print")
            pg.pdf(path=p[:-5] + ".pdf", prefer_css_page_size=True, print_background=True)
            print(p[:-5] + ".pdf")
        b.close()


if __name__ == "__main__":
    signs = build_sign()
    paths = build_targets() + signs
    render(paths)
    # one print-ready file, in print order: sign sheet, A4, 13x18, 10x15
    order = [signs[1]] + paths[:3]
    final = os.path.join(HERE, "PRINT_ALL_targets.pdf")
    import subprocess
    subprocess.run(["pdfunite", *[p[:-5] + ".pdf" for p in order], final], check=True)
    print(final)

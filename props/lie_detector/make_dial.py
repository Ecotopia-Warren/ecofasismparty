"""Generate the printable/laser-engravable dial face for the fake lie detector.

Sweep matches the firmware defaults (SERVO_US_LEFT 2300 -> SERVO_US_RIGHT 700,
about 144 degrees on an SG90). Print at 100% on A4 or engrave on 4 mm poplar.
"""
import math
from pathlib import Path

W, H = 180, 120          # mm
CX, CY = W / 2, 100      # needle pivot
R = 78                   # scale radius
SWEEP = 144              # degrees
A0 = 90 + SWEEP / 2      # left end (HARMONIOUS), degrees, math convention
A1 = 90 - SWEEP / 2      # right end (DISHARMONY)

def pt(a, r):
    t = math.radians(a)
    return CX + r * math.cos(t), CY - r * math.sin(t)

def arc(a_from, a_to, r, color, width):
    x0, y0 = pt(a_from, r)
    x1, y1 = pt(a_to, r)
    large = 1 if abs(a_from - a_to) > 180 else 0
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r},{r} 0 {large} 1 {x1:.2f},{y1:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="{width}"/>')

def lerp_angle(f):
    return A0 + (A1 - A0) * f

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
       f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="#f3ead2" stroke="#000" stroke-width="0.6"/>']

# coloured zones: HARMONIOUS / INCONCLUSIVE / DISHARMONY
zones = [(0.0, 0.30, "#2e7d32"), (0.30, 0.65, "#f9a825"), (0.65, 1.0, "#c62828")]
for f0, f1, col in zones:
    out.append(arc(lerp_angle(f0), lerp_angle(f1), R - 6, col, 9))

# ticks + numbers
for i in range(0, 101, 5):
    a = lerp_angle(i / 100)
    major = i % 10 == 0
    x0, y0 = pt(a, R + 1)
    x1, y1 = pt(a, R + (7 if major else 4))
    out.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" '
               f'stroke="#000" stroke-width="{0.7 if major else 0.4}"/>')
    if major:
        tx, ty = pt(a, R + 12)
        out.append(f'<text x="{tx:.2f}" y="{ty+1.4:.2f}" font-size="4" text-anchor="middle" '
                   f'font-family="Courier New, monospace">{i}</text>')

def label(f, text, color):
    x, y = pt(lerp_angle(f), R - 22)
    out.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="4.2" font-weight="bold" fill="{color}" '
               f'text-anchor="middle" font-family="Courier New, monospace">{text}</text>')

label(0.13, "HARMONIOUS", "#1b5e20")
label(0.50, "INCONCLUSIVE", "#8d6e00")
label(0.86, "DISHARMONY", "#8e0000")

out.append(f'<text x="{CX}" y="{CY-38}" font-size="5" font-weight="bold" text-anchor="middle" '
           f'font-family="Courier New, monospace">MINISTRY OF VIGILANCE</text>')
out.append(f'<text x="{CX}" y="{CY-31}" font-size="3.6" text-anchor="middle" '
           f'font-family="Courier New, monospace">TRUTH-HARMONY VERIFIER</text>')
out.append(f'<text x="{CX}" y="{CY-26}" font-size="2.6" text-anchor="middle" font-style="italic" '
           f'font-family="Georgia, serif">"Questions are welcome. They have already been answered."</text>')
out.append(f'<text x="{CX}" y="{H-5}" font-size="2.8" text-anchor="middle" '
           f'font-family="Courier New, monospace">R.E.I.G.N. · THE GUARDIAN SEES EVERYTHING, AND FORGIVES MOST OF IT</text>')

# pivot hole for the servo spline (SG90 shaft boss ~ 6 mm)
out.append(f'<circle cx="{CX}" cy="{CY}" r="3.2" fill="none" stroke="#000" stroke-width="0.4"/>')
out.append(f'<circle cx="{CX}" cy="{CY}" r="7" fill="none" stroke="#000" stroke-width="0.3" stroke-dasharray="1,1"/>')
out.append('</svg>')

dst = Path(__file__).with_name("dial_face.svg")
dst.write_text("\n".join(out))
print("wrote", dst)

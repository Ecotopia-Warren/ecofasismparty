"""Greeter's name index for the inburgering: every citizen A-Z -> reg. no. -> ministry -> customs desk.

Passports are numbered in ministry order (make_passport_batch.load), so a guest who only gives a name can't be found
fast. This prints one alphabetical list for the greeter. PERSONAL DATA: written to passport_v2/out/ (git-ignored).

Run: python3 customs/make_name_index.py
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "passport_v2"))
import make_passport_batch as B  # noqa: E402

DESK = {"Purity": 1, "Radiance": 1, "Breath": 2, "Flow": 2, "Light": 3, "Industry": 3,
        "Humus": 4, "Service": 4, "Vigilance": 5, "Joy": 5}


def desk(ministry):
    return DESK.get(ministry.replace("Ministry of ", "").strip(), 6)


def main():
    cs = sorted(B.load(B.SRC), key=lambda c: c["name"].casefold())
    rows = "".join(f'<tr><td>{html.escape(c["name"])}</td><td>{c["no"]:03d}</td>'
                   f'<td>{html.escape(c["ministry"].replace("Ministry of ", ""))}</td><td class="d">{desk(c["ministry"])}</td></tr>'
                   for c in cs)
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Name index</title><style>
@page{{size:A4 portrait;margin:9mm}}
body{{font-family:'DejaVu Sans Condensed',sans-serif;color:#000;margin:0}}
h1{{font-size:14pt;background:#000;color:#fff;padding:1mm 2mm;margin:0 0 2mm}}
.cols{{column-count:2;column-gap:6mm;font-size:10pt}}
table{{border-collapse:collapse;width:100%}}
td,th{{border-bottom:1px solid #000;padding:.6mm 1mm;text-align:left}}
th{{border-bottom:2px solid #000}}
td.d{{font-weight:800;text-align:center}}
</style></head><body><h1>NAME INDEX · greeter · name → reg. no. → desk (not on it: walk-in → Erik)</h1>
<div class="cols"><table><tr><th>Name</th><th>No.</th><th>Ministry</th><th>Desk</th></tr>{rows}</table></div></body></html>"""
    os.makedirs(B.OUT, exist_ok=True)
    p = os.path.join(B.OUT, "name_index.html")
    open(p, "w").write(doc)
    B.render([p])
    print(f"{len(cs)} citizens -> {p[:-5]}.pdf")


if __name__ == "__main__":
    main()

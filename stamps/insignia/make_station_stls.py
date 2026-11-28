"""Station stamp SVGs (../station/*.svg, real mm) -> rectangular stamp STLs that fit the small set's handle.

Body copied from the small StampMaker set (../stampmaker_stl_small): 7 mm body + 1 mm 45-degree top chamfer,
raised design 1.4 mm on top (mirrored, so it stamps the right way round, grown 0.06 mm like StampMaker_grow),
and the same M9 internal thread in the bottom (cut out of 01_purity.stl), so the existing handle.stl screws in.

Run: <venv with trimesh manifold3d svgelements shapely matplotlib>/python make_station_stls.py
Out: ../station/stl/<name>.stl + <name>.png (top view as printed = mirrored)
"""
import glob, os
import numpy as np, trimesh, manifold3d as mf
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from svgelements import SVG, Path, Shape

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "station"); OUT = os.path.join(SRC, "stl"); os.makedirs(OUT, exist_ok=True)
REF = os.path.join(HERE, "..", "stampmaker_stl_small", "01_purity.stl")
BODY_H, CHAMFER, RELIEF, GROW = 7.0, 1.0, 1.4, 0.06
MARGIN = 1.25          # body edge beyond the design, per side (top face = design + 0.25 mm per side)
CORNER = 1.5

def to_mf(m): return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32), tri_verts=np.asarray(m.faces, np.uint32)))
def to_tm(M): g = M.to_mesh(); return trimesh.Trimesh(np.asarray(g.vert_properties)[:, :3], np.asarray(g.tri_verts))
def cs_from(g):
    polys = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    loops = [np.array(p.exterior.coords[:-1]) for p in polys] + [np.array(h.coords[:-1]) for p in polys for h in p.interiors]
    return mf.CrossSection(loops, mf.FillRule.EvenOdd)
def rrect(w, h, r): return Polygon([(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]).buffer(-r, join_style=2).buffer(r, 32)

def thread_cavity():
    old = to_mf(trimesh.load(REF))
    low = old ^ mf.Manifold.cube((40, 40, 6.9)).translate((-20, -20, -0.5))       # body below the chamfer
    cyl = mf.Manifold.cylinder(6.4, 9.6, 9.6, 128)                                  # well inside the old outer wall
    return cyl - low                                                                # = the threaded hole (r < 4.7)

def design(svg_file):
    svg = SVG.parse(svg_file, ppi=25.4); vb = svg.viewbox; w, h = vb.width, vb.height   # ppi 25.4: 1 unit = 1 mm
    shapes = []
    for el in svg.elements():
        if not isinstance(el, Shape) or isinstance(el, SVG): continue
        p = Path(el); p.reify()
        loops = []
        for sub in p.as_subpaths():
            sp = Path(sub); n = max(24, int(sp.length(error=1e-3) / 0.05))
            pts = [sp.point(t) for t in np.linspace(0, 1, n, endpoint=False)]
            pts = [(q.x - w/2, h/2 - q.y) for q in pts if q is not None]           # centre, y up (reading view)
            if len(pts) >= 3: loops.append(Polygon(pts).buffer(0))
        if not loops: continue
        sw = el.stroke_width if (el.stroke is not None and el.stroke.value is not None) else 0
        if el.fill is None or el.fill.value is None:                                 # stroked outline (the frame)
            g = unary_union([l.buffer(sw/2, join_style=2).difference(l.buffer(-sw/2, join_style=2)) for l in loops])
        else:                                                                       # filled text, even-odd
            g = loops[0]
            for l in loops[1:]: g = g.symmetric_difference(l)
        shapes.append(g)
    g = unary_union(shapes).buffer(GROW, join_style=2)
    return g, w, h

def build(svg_file, cavity):
    g, w, h = design(svg_file)
    W, H = w + 2 * MARGIN, h + 2 * MARGIN
    base = mf.Manifold.extrude(cs_from(rrect(W, H, CORNER)), BODY_H)
    top = mf.Manifold.hull(mf.Manifold.extrude(cs_from(rrect(W, H, CORNER)), 0.01).translate((0, 0, BODY_H - 0.01))
                           + mf.Manifold.extrude(cs_from(rrect(W - 2*CHAMFER, H - 2*CHAMFER, CORNER - 0.5)), 0.01).translate((0, 0, BODY_H + CHAMFER - 0.01)))
    mirrored = cs_from(g).mirror((1, 0))                                            # mirror x: stamps the right way round
    relief = mf.Manifold.extrude(mirrored, RELIEF + 0.01).translate((0, 0, BODY_H + CHAMFER - 0.01))
    stamp = (base + top + relief) - cavity
    m = to_tm(stamp); m.merge_vertices()
    return m, (W, H)

def preview(m, path, title):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5, 2.6)); ax.set_aspect("equal"); ax.axis("off")
    sel = m.triangles_center[:, 2] > BODY_H + CHAMFER + RELIEF - 0.02
    for t in m.triangles[sel]: ax.fill(t[:, 0], t[:, 1], color="k", lw=0)
    b = m.bounds; ax.add_patch(plt.Rectangle(b[0][:2], *(b[1][:2] - b[0][:2]), fill=False, ec="0.6"))
    ax.set_title(title + "\n(top view as printed: mirrored)", fontsize=8)
    fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__":
    cav = thread_cavity()
    for f in sorted(glob.glob(os.path.join(SRC, "*.svg"))):
        name = os.path.basename(f)[:-4]
        m, (W, H) = build(f, cav)
        out = os.path.join(OUT, name + ".stl"); m.export(out); preview(m, out[:-4] + ".png", name)
        print(f"{name}: {W:.1f} x {H:.1f} x {m.bounds[1][2]:.2f} mm, watertight={m.is_watertight}, volume={m.volume:.0f}")

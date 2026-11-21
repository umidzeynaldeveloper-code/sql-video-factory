"""The same 17 s demo built with the CURRENT v2 engine only (v2/studio.py, unchanged) — for A/B comparison."""
import sys, os
sys.path.insert(0, "/home/claude/v2"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio import *            # noqa: F401,F403
from demo_new import B1, B2, Q, HEAD, ROWS, CW, TX, HIT


def s1(g):
    hl = [0, 1, 2] if g.b == 1 else ([min(2, int(2 * g.at(0, 1.7, 2.6) + .4))] if g.b == 0 and g.bt > 1.7 else [])
    sql(g, 140, 330, Q, a=g.on(0, 0, .3), fs=42, w=800, la=lambda i: g.on(0, .15 + i * .4, .3), hl=hl, hlcol=GREEN)
    seen = 8 * g.at(1, .3, 2.7) if g.b >= 1 else 0
    tb = table(g, TX, 700, HEAD, ROWS, CW, rh=62, a=g.on(0, .6, .5), name="accounts", ra=lambda i: g.on(0, .7 + i * .06, .3),
               hl=[HIT] if seen > HIT + .4 else [], dim=[i for i in range(8) if g.b >= 1 and i != HIT and seen > i + 1])
    if g.b == 1 and seen < 8: ring(g, tb.row(min(7, int(seen))), CYAN, a=1)
    if g.b >= 1:
        n = min(8, int(seen + .001)); pill(g, tb.box[2] - 130, 652, f"rows read: {n} / 8", RED if n == 8 else CYAN, a=g.on(1, .2, .3), fs=30)


def s2(g):
    sql(g, 140, 310, Q, a=1, fs=32, w=640)
    levels = [["root"], ["1-40", "41-80"], ["1-20", "21-40", "41-60", "61-80"]]; path_ = (0, 1, 2)
    rv = g.at(0, .5, 2.6) if g.b == 0 else 1.0; rects = []
    for li, labels in enumerate(levels):
        n = len(labels); span = min(960, n * 228); x0 = 540 - span / 2; y = 560 + li * 135
        rects.append([(x0 + i * span / n + 14, y, x0 + (i + 1) * span / n - 14, y + 64) for i in range(n)])
    for li in range(2):
        for i, r in enumerate(rects[li]):
            for j in (range(2) if li == 0 else range(2 * i, 2 * i + 2)):
                k = rects[li + 1][j]; on = path_[li] == i and path_[li + 1] == j and rv * 2 > li + .9
                arrow(g, ((r[0] + r[2]) / 2, r[3]), ((k[0] + k[2]) / 2, k[1]), GREEN if on else DIM, a=g.on(0, 0, .4), w=4, head=14)
    for li, row in enumerate(rects):
        for i, r in enumerate(row):
            on = path_[li] == i and rv * 2 >= li - .05
            chip(g, (r[0] + r[2]) / 2, (r[1] + r[3]) / 2, r[2] - r[0], 64, levels[li][i], GREEN if on else PURP, a=g.on(0, 0, .4), fs=28,
                 tcol=GREEN if on else WHITE)
            if on: badge(g, r[2] + 34, (r[1] + r[3]) / 2, li + 1, GREEN, a=1, r=22)
    rows = [(23, "Murad", "  980"), (42, "Kamran", "3 500"), (57, "Orxan", "1 870")]
    up = g.at(1, 1.05, 1.6) if g.b >= 1 else 0
    tb = table(g, TX, 1035, HEAD, rows, CW, rh=58, a=g.on(0, .3, .4), name="accounts", hl=[1] if up > .3 else [], dim=[0, 2] if up > .5 else [])
    if g.b >= 1:
        leaf = rects[2][2]; r42 = tb.row(1); p0 = ((leaf[0] + leaf[2]) / 2, leaf[3])
        path(g, [p0, (p0[0], p0[1] + 30), (r42[2] + 40, p0[1] + 30), (r42[2] + 40, (r42[1] + r42[3]) / 2), (r42[2] + 6, (r42[1] + r42[3]) / 2)],
             GREEN, a=g.on(1, 0, .3), rv=g.at(1, 0, 1.0), w=5, head=16, dot=True)
        pill(g, 540, 1350, "3 jumps instead of 8 rows", GREEN, a=g.on(1, 1.6, .4), fs=32, fill=True)


SCENES = [("Find one row", CYAN, s1, B1), ("The index shortcut", GREEN, s2, B2)]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    run(SCENES, Stage(1080, 1920, 30), "/home/claude/v21out/old", "/home/claude/v21out/demo_old.mp4", mode, seed=7, max_dur=20)

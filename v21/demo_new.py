"""15-20 s prototype: how Oracle finds one row — full scan vs index. v2.1 engine.
python3 demo_new.py preview|full [preset]     preset: preview | draft | final (default) | final4k
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *          # noqa: F401,F403
import engine as E

B1 = ["We ask Oracle for one account: *id 42*.",
      "Without an index, Oracle reads *every row*, top to bottom."]
B2 = ["With an index, it walks a small *B-tree* instead.",
      "Three jumps, and the row is found. *Instant.*"]

Q = ["SELECT *", "FROM   accounts", "WHERE  id = 42;"]
HEAD = ["id", "owner", "balance"]
ROWS = [(17, "Aysel", "1 250"), (23, "Murad", "  980"), (8, "Leyla", "4 310"), (35, "Tural", "  615"),
        (51, "Nigar", "2 044"), (12, "Elvin", "  730"), (42, "Kamran", "3 500"), (29, "Sevda", "1 120")]
CW = [170, 330, 260]; TX = (1080 - sum(CW)) / 2
HIT = 6


def s1(g):
    g.camera([(1, 0.0, 1.0, 540, 930, 1.08)])
    typed = g.at(0, .15, 1.5); run = 2 * g.at(0, 1.7, 2.6) if g.b == 0 else None
    done = [i for i in range(3) if g.b > 0 or (run is not None and run > i + .6)]
    cd = sql_exec(g, 140, 330, Q, a=g.on(0, 0, .3), fs=42, typed=typed, run=run, done=done, w=800)
    scan = 8 * g.at(1, .3, 2.7) if g.b >= 1 else None
    seen = scan or 0
    tb = table3d(g, TX, 700, HEAD, ROWS, CW, rh=62, a=g.on(0, .6, .5), name="accounts", ra=lambda i: g.on(0, .7 + i * .06, .3),
                 lift=lambda i: E.ep(seen, HIT + .4, HIT + 1.2, "out_back") if i == HIT else 0.0,
                 dim=[i for i in range(8) if g.b >= 1 and i != HIT and seen > i + 1], scan=scan if g.b == 1 and scan < 8 else None)
    if g.b >= 1:
        n = min(8, int(seen + .001)); x1 = tb.box[2]
        pill(g, x1 - 130, 652, f"rows read: {n} / 8", RED if n == 8 else CYAN, a=g.on(1, .2, .3), fs=30)
    if g.b == 1 and seen >= 8:
        g.focus(tb.box, a=g.at(1, 2.75, 3.1), strength=.5)


def s2(g):
    g.camera([(1, .9, 1.1, 540, 1080, 1.08)], ease="in_out_sine")
    sql_exec(g, 140, 310, Q, a=1 - g.at(1, .6, 1.1), fs=32, typed=1, done=[0, 1, 2], w=640)
    rv = g.at(0, .5, 2.6) if g.b == 0 else 1.0
    levels = [["root"], ["1-40", "41-80"], ["1-20", "21-40", "41-60", "61-80"]]
    rects = btree(g, 540, 560, levels, a=g.on(0, 0, .4), path=(0, 1, 2), rv=rv, w=200, h=64, vgap=135, fs=28)
    for li in range(3):
        r = rects[li][(0, 1, 2)[li]]
        badge(g, r[2] + 34, (r[1] + r[3]) / 2, li + 1, GREEN, a=g.on(0, .5 + li * .75, .3) if g.b == 0 else 1, r=22)
    leaf = rects[2][2]
    rows = [(23, "Murad", "  980"), (42, "Kamran", "3 500"), (57, "Orxan", "1 870")]
    up = g.at(1, 1.05, 1.6) if g.b >= 1 else 0
    tb = table3d(g, TX, 1035, HEAD, rows, CW, rh=58, a=g.on(0, .3, .4), name="accounts", lift=lambda i: E.EASE["out_back"](up) if i == 1 else 0,
                 dim=[0, 2] if up > .5 else ())
    if g.b >= 1:
        r42 = tb.row(1); p0 = ((leaf[0] + leaf[2]) / 2, leaf[3]); p1 = (r42[2] + 30, (r42[1] + r42[3]) / 2 - 22 * up)
        flow(g, [p0, (p0[0], p0[1] + 30), (p1[0] + 40, p0[1] + 30), (p1[0] + 40, p1[1]), p1], GREEN, a=g.only(1, 1, 0, .3) * (1 - g.at(1, 1.6, 2.0)), n=4, speed=.9)
        pill(g, 540, 1350, "3 jumps instead of 8 rows", GREEN, a=g.on(1, 1.6, .4), fs=32, fill=True)


SCENES = [("Find one row", CYAN, s1, B1,
           [(0, 0.0, "sub_hit", dict(amp=.55)), (0, .15, "data", dict(dur=1.3, amp=.18, rate=18)),
            (0, 1.7, "click", dict(tone=1.0)), (0, 2.05, "click", dict(tone=1.12)), (0, 2.4, "click", dict(tone=1.26)),
            (1, 0.0, "whoosh", dict(amp=.35))] +
           [(1, .3 + i * .3, "click", dict(tone=.8 + i * .06, amp=.22, pan=-.4 + i * .1)) for i in range(8)] +
           [(1, 2.75, "error", dict(amp=.28))]),
          ("The index shortcut", GREEN, s2, B2,
           [(0, .5, "click", dict(tone=1.3)), (0, 1.2, "click", dict(tone=1.5)), (0, 1.95, "click", dict(tone=1.7)),
            (1, 0.0, "data", dict(dur=1.0, amp=.25)), (1, 1.0, "riser", dict(dur=1.0, amp=.25)),
            (1, 1.05, "impact", dict(amp=.45)), (1, 1.1, "success", dict(amp=.35))])]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    preset = sys.argv[2] if len(sys.argv) > 2 else ("preview" if mode == "preview" else "final")
    cfg = dict(E.PRESETS[preset]); out = f"/home/claude/v21out/new_{preset}"
    st = Stage21(1080, 1920, 30, cfg=cfg)
    run21(SCENES, st, out, f"/home/claude/v21out/demo_new_{preset}.mp4", mode, seed=7, max_dur=20)

"""57 · Execution plans from zero (v2.1 engine, beginner-first).
python3 v21/video57.py preview|check|full [preset]     preset: preview | draft | final (default for full)
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *          # noqa: F401,F403
import engine as E

Q = ["SELECT * FROM orders", "WHERE  customer_id = 7;"]
PLAN = [("0", "SELECT STATEMENT", ""), ("1", " TABLE ACCESS BY INDEX ROWID", "ORDERS"), ("2", "  INDEX RANGE SCAN", "ORD_CUST_IX")]
PCW = [96, 560, 284]
PLAN2 = [("0", "SELECT STATEMENT", ""), ("1", "  TABLE ACCESS BY INDEX ROWID", "ORDERS"), ("2", "    INDEX RANGE SCAN", "ORD_CUST_IX")]


def xmark(g, cx, cy, a, r=24):
    S.check(g, cx, cy, False, a, r)


# ------------------------------------------------------------------ 1 hook
def s_hook(g):
    g.camera([(2, 0.0, 1.2, 540, 900, 1.05)])
    typed = g.at(0, .1, 1.3) if g.b == 0 else 1
    run = 2 * g.at(0, 1.4, 2.4) if g.b == 0 else None
    sql_exec(g, 90, 330, Q, a=g.on(0, 0, .3), fs=40, typed=typed, run=run, w=900)
    if g.b == 0:
        p = g.at(0, 1.4, g.bl)
        pill(g, 540, 560, f"running…  {p * 8.4:4.1f} s", RED, a=g.on(0, 1.4, .3), fs=36)
    if g.b >= 1:
        pill(g, 540, 560, "8.4 s  · why?", RED, a=1, fs=36)
        tb = table3d(g, 70, 680, ["Id", "Operation", "Name"], PLAN, PCW, rh=62, a=g.on(1, .3, .5), fs=28, col=YEL,
                     ra=lambda i: g.on(1, .5 + i * .25, .35), name="the plan Oracle shows you")
        g.glow(tb.box, YEL, g.only(1, 1, .9) * .5)
    if g.b >= 2:
        term(g, "EXECUTION PLAN", "the steps Oracle takes to run your SQL", g.on(2, .3), y=1060, col=YEL)


# ------------------------------------------------------------------ 2 analogy
LEFT = ["where you want to go", "route the GPS picks", "the GPS brain", "estimated travel time"]
RIGHT = ["your SQL", "execution plan", "the optimizer", "cost"]


def s_gps(g):
    LB = {0: (0, .3), 1: (1, .5), 2: (2, 1.6), 3: (3, 2.6)}           # row -> (beat, delay) for the real-life side
    RB = {0: (2, 1.0), 1: (3, .6), 2: (2, 2.6), 3: (3, 2.8)}           # ... and for the database side
    vs_panel(g, 330, LEFT, RIGHT, a_l=lambda i: g.on(*LB[i]), a_r=lambda i: g.on(*RB[i]), h=96, fs=32)
    if g.b >= 3:
        r = pill(g, 540, 900, "SQL says WHAT  ·  the plan says HOW", GREEN, a=g.on(3, 1.2), fs=36, fill=True)
        g.glow(r, GREEN, g.on(3, 1.4) * .6)


# ------------------------------------------------------------------ 3 how to see it
def s_how(g):
    g.camera([(2, 0.0, 1.0, 540, 880, 1.04)])
    L1 = ["EXPLAIN PLAN FOR", "SELECT * FROM orders", "WHERE  customer_id = 7;"]
    typed = g.at(0, .2, 2.0) if g.b == 0 else 1
    run = 3 * g.at(0, 2.1, 2.9) if g.b == 0 else None
    cd = sql_exec(g, 90, 320, L1, a=g.on(0, 0, .3), fs=38, typed=typed, run=run, done=[0] if g.b >= 1 else (), w=900)
    if g.b == 0:
        g.glow(cd.line(0), CYAN, g.on(0, .4) * .6)
    if g.b >= 1:
        tx(g, 120, cd.bottom + 40, "Explained.", S.MB(34), GREEN, g.on(1, .1), "lm")
        c = cyl25(g, 760, 760, 300, 170, CYAN, a=g.on(1, .4), label="PLAN_TABLE", sub="the stored plan", fs=32, fill=g.at(1, 1.2, 2.4))
        xmark(g, 230, 760, g.on(1, .4), r=30)
        tx(g, 230, 830, "query NOT run", S.SB(30), RED, g.on(1, .5), "mm")
        flow(g, [(500, cd.bottom - 10), (500, 650), (610, 700)], CYAN, a=g.only(1, 1, .6), n=4, speed=.8)
    if g.b >= 2:
        L2 = ["SELECT *", "FROM TABLE(DBMS_XPLAN.DISPLAY);"]
        sql_exec(g, 90, 940, L2, a=g.on(2, .1), fs=36, typed=g.at(2, .2, 1.6), done=[1] if g.at(2, 1.7, 1.8) > 0 else (), w=900)
        tx(g, 540, 1150, "→ shows the plan as a table", S.SN(32), SOFT, g.on(2, 1.9), "mm")


# ------------------------------------------------------------------ 4 the plan table
def s_plan(g):
    tb = table3d(g, 70, 380, ["Id", "Operation", "Name"], PLAN2, PCW, rh=66, a=g.on(0, 0, .4), fs=30, col=YEL,
                 ra=lambda i: g.on(0, .4 + i * .35, .35), name="plan for: customer_id = 7",
                 lift=lambda i: E.ep(g.bt, .3, .8, "out_back") if (g.b == 2 and i in (1, 2)) else (1.0 if g.b > 2 and i in (1, 2) else 0.0))
    if g.b == 0:
        term(g, "OPERATION", "one small job: read, find, join, sort…", g.on(0, 1.6), y=1060, col=YEL)
    if g.b >= 1:
        cId, cNm = tb.col(0), tb.col(2)
        g.glow(cId, CYAN, g.only(1) * .7); g.glow(cNm, GREEN, g.only(1, 1, 1.2) * .7)
        pill(g, (cId[0] + cId[2]) / 2 + 60, tb.bottom + 50, "step number", CYAN, g.on(1, .2), fs=30)
        pill(g, (cNm[0] + cNm[2]) / 2, tb.bottom + 50, "table / index", GREEN, g.on(1, 1.2), fs=30)
    if g.b >= 2:
        # indentation brackets: child → parent
        x = tb.cell(0, 1)[0] + 16; sp = S.MB(30).getlength(" ") * 2
        for k in (1, 2):
            rc, rp = tb.cell(k, 1), tb.cell(k - 1, 1); yc = (rc[1] + rc[3]) / 2 - 12 * (k >= 1); yp = rp[3] - 12 - 2
            xp = x + sp * (k - 1) + 8; xc = x + sp * k - 4; d0 = .9 + .5 * (k - 1)
            path(g, [(xp, yp), (xp, yc), (xc, yc)], ORANGE, a=g.on(2, d0), rv=g.at(2, d0, d0 + .5), w=4, head=12)
        box(g, (70, 1060, 1010, 1200), ORANGE, g.on(2, 1.8), "pushed right = CHILD of the line above", "the child does its job first, then hands rows up", 32, 28)


# ------------------------------------------------------------------ 5 read inside-out
NODES = [("SELECT STATEMENT", "returns rows to you"), ("TABLE ACCESS BY INDEX ROWID", "ORDERS: fetch the rows"),
         ("INDEX RANGE SCAN", "ORD_CUST_IX: find addresses")]


def s_tree(g):
    ys = [330, 560, 790]; rects = []
    for k, (op, sub) in enumerate(NODES):
        lvl = [3, 2, 1][k]; lit = g.b >= {0: 3, 1: 2, 2: 0}[k]
        col = GREEN if lit else PURP
        r = box(g, (130 + 40 * k, ys[k], 950 + 40 * k - 80, ys[k] + 130), col, g.on(0, .1 + .2 * (2 - k)), op, sub, 34, 28)
        rects.append(r)
        if lit:
            badge(g, r[0] - 10, r[1] + 10, lvl, GREEN, g.on({0: 3, 1: 2, 2: 0}[k], .2), r=26)
            g.glow(r, GREEN, (g.only({0: 3, 1: 2, 2: 0}[k]) if k else g.only(0, 1)) * .6)
    for k in (1, 2):                                           # data goes up
        p0 = ((rects[k][0] + rects[k][2]) / 2, rects[k][1]); p1 = (p0[0] - 20, rects[k - 1][3])
        arrow(g, p0, p1, OFFB, g.on(0, .6), 1, 5, 16)
    if g.b == 0:
        g.focus(rects[2], a=g.at(0, .8, 1.3), strength=.45)
    if g.b >= 1:                                               # ROWIDs come out of the index
        for j in range(4):
            chip(g, 220 + j * 205, 1010, 185, 66, f"ROWID {j + 1}", CYAN, g.on(1, .5 + j * .25), fs=26)
        if g.b == 1:
            flow(g, [((rects[2][0] + rects[2][2]) / 2, rects[2][3]), (540, 970)], CYAN, a=g.only(1, 1, .4), n=4, speed=.9)
    if g.b >= 2:
        flow(g, [((rects[2][0] + rects[2][2]) / 2 - 20, rects[2][1]), ((rects[1][0] + rects[1][2]) / 2 - 40, rects[1][3])], GREEN,
             a=g.only(2, 3, .3), n=4, speed=.8)
    if g.b >= 3:
        flow(g, [((rects[1][0] + rects[1][2]) / 2 - 20, rects[1][1]), ((rects[0][0] + rects[0][2]) / 2 - 40, rects[0][3])], GREEN,
             a=g.only(3, 3, .2), n=4, speed=.8)
        pill(g, 540, 1150, "deepest first  ·  data flows UP", GREEN, a=g.on(3, 1.0), fs=36, fill=True)
        tx(g, 540, 1225, "simple teaching model for a one-table plan", S.SN(26), DIM, g.on(3, 1.3), "mm")


# ------------------------------------------------------------------ 6 rows & cost
RC = [("SELECT STATEMENT", "5", "4"), (" TABLE ACCESS BY INDEX", "5", "4"), ("  INDEX RANGE SCAN", "5", "1")]


def s_cost(g):
    tb = table3d(g, 70, 380, ["Operation", "Rows", "Cost"], RC, [560, 180, 200], rh=66, a=g.on(0, 0, .4), fs=30, col=PURP,
                 ra=lambda i: g.on(0, .2 + i * .15, .3), name="two more columns")
    if g.b in (0, 1):
        g.glow(tb.col(1), CYAN, g.on(0, .6) * .8)
        c1 = tb.col(1); pill(g, (c1[0] + c1[2]) / 2 - 60, tb.bottom + 50, "rows Oracle EXPECTS", CYAN, g.on(0, .9), fs=30)
    if g.b >= 1:
        box(g, (70, 820, 1010, 940), CYAN, g.on(1, .2), "an ESTIMATE from table statistics", "not a real count", 32, 28)
    if g.b >= 2:
        g.glow(tb.col(2), YEL, g.only(2, 3, .2) * .8)
        tw_ = g.at(2, .6, 1.8)
        hbar(g, 120, 1010, 840, 40, .25 + .55 * tw_, YEL, g.on(2, .4), "cost = estimated work", "more work →")
    if g.b >= 3:
        term(g, "COST", "estimated work, NOT seconds — compare plans of one query", g.on(3, .2), y=1090, col=YEL)


# ------------------------------------------------------------------ 7 index vs full
def s_vs(g):
    sql(g, 70, 310, ["SELECT * FROM orders", "WHERE customer_id = 7;"], g.on(0), fs=34, w=940)
    pill(g, 540, 510, "5 of 1 000 000 rows", CYAN, g.on(0, 1.0), fs=32)
    if g.b >= 1:
        r = box(g, (70, 570, 1010, 670), GREEN, g.on(1, .3), "INDEX RANGE SCAN  ·  jump to 5 rows", None, 34)
        g.glow(r, GREEN, g.only(1) * .6)
        check(g, 960, 620, True, g.on(1, .9), r=24)
    if g.b >= 2:
        sql(g, 70, 730, ["SELECT * FROM orders", "WHERE status = 'SHIPPED';"], g.on(2), fs=34, w=940)
        pill(g, 540, 930, "950 000 of 1 000 000 rows", ORANGE, g.on(2, 1.0), fs=32)
    if g.b >= 3:
        r = box(g, (70, 990, 1010, 1090), ORANGE, g.on(3, .6), "TABLE ACCESS FULL  ·  read it all", None, 34)
        g.glow(r, ORANGE, g.only(3, 3, .8) * .6)
        check(g, 960, 1040, True, g.on(3, 1.4), r=24)
    if g.b >= 4:
        box(g, (70, 1140, 1010, 1270), YEL, g.on(4, .2), "full scan is not always bad", "it depends on how many rows you need", 34, 28)


# ------------------------------------------------------------------ 8 classic mistake
def s_mistake(g):
    sql(g, 70, 310, ["EXPLAIN PLAN FOR", "SELECT * FROM orders", "WHERE  customer_id = :id;"], g.on(0), fs=34, w=940)
    xmark(g, 960, 360, g.on(0, 1.2), r=28)
    if g.b == 0:
        pill(g, 540, 560, "\"this is what ran\"  — not quite", RED, g.on(0, 1.0), fs=32)
    if g.b >= 1:
        box(g, (70, 540, 520, 690), PURP, g.on(1, .2), "predicted", "INDEX RANGE SCAN", 32, 28)
        box(g, (560, 540, 1010, 690), RED, g.on(1, 1.2), "really ran", "TABLE ACCESS FULL", 32, 28)
        tx(g, 540, 730, "bind values · session settings can change the plan", S.SN(28), SOFT, g.on(1, 2.0), "mm")
    if g.b >= 2:
        cd = sql_exec(g, 70, 800, ["SELECT *", "FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR);"], a=g.on(2, .1), fs=34,
                      typed=g.at(2, .3, 2.0), done=[1] if g.at(2, 2.1, 2.2) > 0 else (), w=940)
        pill(g, 860, 780, "10g+", GREEN, g.on(2, .2), fs=26)
        tx(g, 540, cd.bottom + 34, "the REAL plan of the last query you ran", S.SB(30), GREEN, g.on(2, 2.2), "mm")
        tx(g, 540, cd.bottom + 78, "(needs SELECT access to V$ views)", S.SN(24), DIM, g.on(2, 2.4), "mm")
    if g.b >= 3:
        box(g, (70, 1150, 1010, 1270), YEL, g.on(3, .2), "never compare cost of DIFFERENT queries", None, 32)


# ------------------------------------------------------------------ 9 recap
WORDS = [("execution plan", "Oracle's route for your SQL"), ("EXPLAIN PLAN", "the predicted plan"),
         ("indentation", "child steps, read deepest first"), ("Rows / Cost", "estimates, not counts or time"),
         ("INDEX RANGE", "few rows → jump"), ("TABLE FULL", "most rows → read all")]


def s_recap(g):
    la = g.until(0)
    for k, (kw, plain) in enumerate(WORDS):
        if la <= 0: break
        y = 330 + k * 140; lit = pr(g.bt, .8 + k * 1.0, 1.1 + k * 1.0)
        col = [YEL, CYAN, ORANGE, PURP, GREEN, RED][k]
        g.d.rounded_rectangle((70, y, 1010, y + 118), 22, fill=mix(CARD, la), outline=mix(col, la * (.25 + .75 * lit)), width=3)
        badge(g, 140, y + 59, k + 1, col, la * (.3 + .7 * lit), 32)
        tx(g, 205, y + 59, kw, S.MB(32), col, la * (.3 + .7 * lit), "lm")
        tx(g, 985, y + 59, plain, S.SN(30), WHITE, la * lit, "rm")
    if g.b == 1:
        tx(g, 540, 520, "Next video", S.SB(48), DIM, g.on(1, .2), "mm")
        tx(g, 540, 620, "NULL logic", S.XB(80), YEL, g.on(1, .5), "mm")
        tx(g, 540, 720, "TRUE, FALSE … and UNKNOWN", S.SN(38), WHITE, g.on(1, .8), "mm")
        p = 1 + .04 * math.sin(g.t * 7); bw, bh = 760 * p, 130 * p; ab = g.on(1, 1.2)
        g.d.rounded_rectangle((540 - bw / 2, 920 - bh / 2, 540 + bw / 2, 920 + bh / 2), 65, fill=mix(GREEN, ab))
        tx(g, 540, 920, "@sql_developer_no1", S.SB(54), INK, ab, "mm")
        tx(g, 540, 1060, "follow · save · share", S.SN(42), DIM, g.on(1, 1.6), "mm")


SCENES = [
    ("Why is it slow?", WHITE, s_hook, [
        "Your query takes *eight seconds*, and you have no idea why.",
        "But Oracle can show you *exactly* what it does.",
        "That's the *execution plan*. Let's learn to read one, from zero."],
     [(0, 0.0, "sub_hit", dict(amp=.5)), (0, .1, "data", dict(dur=1.1, amp=.16, rate=18)), (0, 1.4, "click", dict(tone=1.0)),
      (0, 1.9, "click", dict(tone=1.15)), (1, .3, "whoosh", dict(amp=.3)), (2, .3, "impact", dict(amp=.35))]),
    ("Think of a GPS", ORANGE, s_gps, [
        "Think of a GPS. You say *where* you want to go, not how to get there.",
        "The GPS picks a *route*: which roads, and in which order.",
        "Oracle is the same: your SQL says *what*, and the *optimizer* picks the route.",
        "That route is the *execution plan*. The estimated effort is called the *cost*."],
     [(0, .1, "whoosh", dict(amp=.3)), (1, .8, "click", dict(tone=1.2)), (2, .8, "click", dict(tone=1.3)),
      (3, .8, "click", dict(tone=1.4)), (3, 1.2, "success", dict(amp=.3))]),
    ("How to see the plan", CYAN, s_how, [
        "Step one: put *EXPLAIN PLAN FOR* in front of your query.",
        "Oracle doesn't run it. It only *plans* it, and saves the plan.",
        "Step two: show it with {*DBMS_XPLAN.DISPLAY*|D B M S X plan dot display}."],
     [(0, .2, "data", dict(dur=1.7, amp=.15, rate=20)), (0, 2.1, "click", dict(tone=1.0)), (1, .4, "whoosh", dict(amp=.3)),
      (1, 1.2, "data", dict(dur=1.0, amp=.2)), (2, .2, "data", dict(dur=1.3, amp=.15, rate=20)), (2, 1.7, "success", dict(amp=.3))]),
    ("Reading the table", YEL, s_plan, [
        "Here's the result. Each line is one *operation*: one small job.",
        "*Id* numbers the steps. *Name* is the table or index the step works on.",
        "Look at the *indentation*: a line pushed right is a *child* of the line above."],
     [(0, .4, "click", dict(tone=1.0)), (0, .75, "click", dict(tone=1.1)), (0, 1.1, "click", dict(tone=1.2)),
      (1, .2, "sweep", dict(amp=.25)), (2, .3, "whoosh", dict(amp=.3)), (2, 1.8, "impact", dict(amp=.3))]),
    ("Read it inside-out", GREEN, s_tree, [
        "In a simple plan like this, start with the *deepest* line.",
        "The index range scan finds the *addresses* of matching rows: the {ROWIDs|row I Ds}.",
        "Its parent uses them to *fetch* the rows from the table.",
        "The top line hands them to *you*. Data flows *bottom up*."],
     [(0, .8, "sub_hit", dict(amp=.35)), (1, .5, "data", dict(dur=1.2, amp=.2)), (2, 0.0, "riser", dict(dur=.8, amp=.2)),
      (2, .3, "whoosh", dict(amp=.3)), (3, .2, "whoosh", dict(amp=.3)), (3, 1.0, "success", dict(amp=.35))]),
    ("Rows and Cost", PURP, s_cost, [
        "*Rows* is how many rows Oracle *expects* at each step.",
        "It's an *estimate*, based on table statistics. Not a real count.",
        "*Cost* is the estimated *work*. Bigger number, more work.",
        "But cost is *not* seconds. Use it to compare plans for the *same* query."],
     [(0, .6, "sweep", dict(amp=.25)), (1, .2, "click", dict(tone=1.1)), (2, .4, "riser", dict(dur=1.4, amp=.2)),
      (3, .2, "impact", dict(amp=.3))]),
    ("Index or full scan?", RED, s_vs, [
        "The two operations you'll see most. Query one wants *five* orders out of a million.",
        "Oracle usually picks an *index range scan*: jump straight to those five rows.",
        "Query two wants *ninety five percent* of the table.",
        "Jumping row by row would be slower, so it reads everything: a *full table scan*.",
        "So a full scan isn't always bad. It depends on *how many rows* you need."],
     [(0, 1.0, "click", dict(tone=1.2)), (1, .3, "whoosh", dict(amp=.3)), (1, .9, "success", dict(amp=.3)),
      (2, 1.0, "click", dict(tone=.9)), (3, .6, "data", dict(dur=1.0, amp=.25)), (3, 1.4, "success", dict(amp=.3)),
      (4, .2, "impact", dict(amp=.3))]),
    ("Classic mistake", PINK, s_mistake, [
        "Classic mistake: trusting *EXPLAIN PLAN* as the plan that really ran.",
        "It's a *prediction*. With bind variables or other session settings, the real plan can differ.",
        "Fix: run the query, then show the plan it *really* used, with {*DISPLAY_CURSOR*|display cursor}.",
        "And never compare the cost of two *different* queries. It's an estimate, not a stopwatch."],
     [(0, 1.2, "error", dict(amp=.3)), (1, 1.2, "impact", dict(amp=.3)), (2, .3, "data", dict(dur=1.7, amp=.15, rate=20)),
      (2, 2.1, "success", dict(amp=.35)), (3, .2, "click", dict(tone=.9))]),
    ("Remember", GREEN, s_recap, [
        "Remember: the plan is Oracle's route. Read the deepest line first. Rows and cost are estimates. Few rows, index. Most rows, full scan.",
        "Next: *NULL logic*. True, false, and unknown. Follow, so you don't miss it."],
     [(1, .5, "impact", dict(amp=.35)), (1, 1.2, "success", dict(amp=.3))]),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    preset = sys.argv[2] if len(sys.argv) > 2 else ("preview" if mode in ("preview", "check") else "final")
    cfg = dict(E.PRESETS[preset]); out = "/home/claude/v21out/out57"
    os.makedirs(out, exist_ok=True); os.makedirs("/home/claude/en", exist_ok=True)
    st = Stage21(1080, 1920, 30, cfg=cfg)
    run21(SCENES, st, out, "/home/claude/en/sql_video57_EN_execution_plans.mp4", mode, seed=57, max_dur=175)

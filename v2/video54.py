"""54 · Subqueries from zero (v2 style)."""
import sys
sys.path.insert(0, "/home/claude/v2")
from studio import *

ORD = [(101, 1, 50), (102, 2, 70), (103, 1, 20), (104, 2, 15), (105, 1, 45)]
CUS = [(1, "Aysel"), (2, "Murad"), (3, "Leyla")]
CC = {1: CYAN, 2: PURP, 3: ORANGE}


def orders(g, x, y, a=1.0, **kw):
    return table(g, x, y, ["id", "customer_id", "amount"], ORD, [130, 250, 170], 60, a, fs=30, name="orders", col=GREEN,
                 ccol=lambda r, c: CC[ORD[r][1]] if c == 1 else None, **kw)


def customers(g, x, y, a=1.0, **kw):
    return table(g, x, y, ["id", "name"], CUS, [100, 220], 60, a, fs=30, name="customers", col=CYAN,
                 ccol=lambda r, c: CC[CUS[r][0]] if c == 0 else None, **kw)


def nest(g, lines, i0, i1, a=1.0, ia=1.0, glow=0.0, y=310, fs=32, collapse=0.0, val=None):
    """the whole query; lines i0..i1 (the subquery) are framed as the INNER query"""
    cd = sql(g, 70, y, lines, a, fs=fs, w=940)
    r = cd.line(i0, i1); ir = (r[0] + 4, r[1] - 4, r[2] - 4, r[3] + 4)
    if ia > 0:
        g.d.rounded_rectangle(ir, 14, outline=mix(YEL, a * ia * (.75 + .25 * glow)), width=4)
        tx(g, ir[2] - 14, ir[1] + 8, "INNER · runs first", SB(22), YEL, a * ia, "ra")
    if collapse > 0:
        g.d.rounded_rectangle(ir, 14, fill=mix((13, 19, 38), collapse), outline=mix(YEL, collapse), width=4)
        pill(g, (ir[0] + ir[2]) / 2, (ir[1] + ir[3]) / 2, val, YEL, collapse, 44, fill=True)
    return cd, ir


# ------------------------------------------------------------------ scenes
def s_hook(g):
    a = g.on(0)
    box(g, (100, 340, 980, 480), WHITE, a, "Which orders are BIGGER than the average?", None, 38, tcol=WHITE)
    if g.b >= 1:
        a1 = g.on(1, .2)
        badge(g, 180, 600, 1, YEL, a1, 32); tx(g, 240, 600, "first: what IS the average?", SB(36), YEL, a1, "lm")
        badge(g, 180, 700, 2, CYAN, g.on(1, 1.6), 32); tx(g, 240, 700, "then: compare every order", SB(36), CYAN, g.on(1, 1.6), "lm")
    if g.b >= 2:
        a2 = g.on(2, .2)
        box(g, (140, 820, 940, 960), GREEN, a2, "a question inside a question", "= SUBQUERY", 40, 32, scol=YEL)
        g.focus((140, 820, 940, 960), a=a2)


def s_analogy(g):
    a = g.on(0)
    person(g, 200, 520, 200, ORANGE, a, "teacher", 28)
    scores = [("Ali", 60), ("Nigar", 90), ("Rauf", 70), ("Sevda", 80)]
    for k, (n, s) in enumerate(scores):
        y = 380 + k * 80; al = g.on(0, .4 + k * .2)
        chip(g, 560, y, 220, 64, n, ORANGE, al, 30, mono=False, tcol=WHITE); chip(g, 760, y, 140, 64, str(s), ORANGE, al, 32)
    if g.b >= 1:
        a1 = g.on(1, .3)
        box(g, (420, 720, 1000, 830), YEL, a1, "average = 75", "step 1 · the INNER question", 38, 26, scol=WHITE)
        g.focus((420, 340, 1000, 830), a=g.only(1))
    if g.b >= 2:
        for k, (n, s) in enumerate(scores):
            check(g, 880, 380 + k * 80, s > 75, g.on(2, .4 + k * .45), 24)
        tx(g, 710, 890, "step 2 · the OUTER question", SB(30), CYAN, g.on(2, .2), "mm")
        tx(g, 710, 940, "Nigar and Sevda", SB(36), GREEN, g.on(2, 2.4), "mm")


def s_scalar(g):
    p = g.at(1, 2.6, 3.4)
    cd, ir = nest(g, ["SELECT id, amount", "FROM   orders", "WHERE  amount >", "  (SELECT AVG(amount)", "   FROM orders);"], 3, 4, 1, 1,
                  glow=g.pulse() if g.b <= 1 else 0, collapse=p, val="40")
    if g.b == 0:
        g.focus(ir, a=g.on(0, 1.4)); callout(g, ir, "this part runs FIRST", YEL, g.on(0, 1.6), at=(540, 680), fs=30, mark=False)
    if g.b >= 1:
        tx(g, 540, 640, "(50 + 70 + 20 + 15 + 45) / 5 = 40", MB(30), YEL, g.on(1, .4) * (1 - g.at(2, 0, .3) if g.b >= 2 else 1), "mm")
    if g.b >= 2:
        tb = orders(g, 220, 700, g.on(2, .2))
        for i, (_, _, amt) in enumerate(ORD):
            r_ = tb.row(i); check(g, r_[2] + 50, (r_[1] + r_[3]) / 2, amt > 40, g.on(2, .9 + i * .35), 22)
        if g.b == 2: g.focus(tb.box, (tb.box[2], tb.box[1], tb.box[2] + 90, tb.box[3]), ir, a=g.on(2, .4))
        if g.b >= 3:
            term(g, "SUBQUERY", "a SELECT inside another SELECT, in brackets", g.on(3, .2), y=1110, col=YEL)


def s_in(g):
    cd, ir = nest(g, ["SELECT name", "FROM   customers", "WHERE  id IN", "  (SELECT customer_id", "   FROM orders);"], 3, 4, 1, 1)
    if g.b == 0: g.focus(ir, a=g.on(0, 1))
    if g.b >= 1:
        a = g.on(1, .2)
        tx(g, 540, 640, "inner result: a LIST", SB(30), YEL, a, "mm")
        for k, v in enumerate((1, 2, 1, 2, 1)):
            chip(g, 300 + k * 120, 710, 96, 70, str(v), CC[v], g.on(1, .4 + k * .2), 34)
        arrow(g, (540, 755), (540, 805), WHITE, g.on(1, 2.0), 1, 5, 16)
        pill(g, 540, 845, "(1, 2)", YEL, g.on(1, 2.2), 38, fill=True)
    if g.b >= 2:
        ct = customers(g, 380, 940, g.on(2, .2), hl=[0, 1], dim=[2] if g.at(2, 1.5, 2) > .5 else ())
        g.focus(ct.box, a=g.only(2))
        tx(g, 540, ct.bottom + 40, "Aysel and Murad", SB(36), GREEN, g.on(2, 2), "mm")


def s_notin(g):
    q = sql(g, 70, 310, ["SELECT name FROM customers", "WHERE id NOT IN (1, 2, NULL);"], 1, fs=32, w=940, hl=[1] if g.b >= 1 else (), hlcol=PINK)
    if g.b == 0:
        tx(g, 540, 520, "the list has one empty value", SB(32), PINK, g.on(0, .8), "mm")
        g.focus(q.line(1), a=g.on(0, .6))
    if g.b >= 1:
        a = g.on(1, .2)
        tx(g, 540, 520, "is 3 NOT IN (1, 2, NULL) ?", MB(34), WHITE, a, "mm")
        rows = [("3 ≠ 1", "true", GREEN), ("3 ≠ 2", "true", GREEN), ("3 ≠ NULL", "unknown", PINK)]
        for k, (l, rres, c) in enumerate(rows):
            y = 600 + k * 86; al = g.on(1, .9 + k * .7)
            chip(g, 380, y, 360, 70, l, c, al, 32); chip(g, 720, y, 240, 70, rres, c, al, 32, tcol=c)
        box(g, (200, 880, 880, 990), RED, g.on(1, 3.6), "unknown  →  row NOT returned", None, 34)
    if g.b >= 2:
        a2 = g.on(2, .2)
        box(g, (70, 1040, 1010, 1150), RED, a2, "result: ZERO rows · no error!", None, 38, fill=(40, 16, 26))
    if g.b >= 3:
        f = sql(g, 70, 1180, ["... WHERE customer_id IS NOT NULL", "-- or use NOT EXISTS"], g.on(3, .2), fs=30, w=940, hl=[0], hlcol=GREEN)
        g.focus(f.box, a=g.on(3, .2))


def s_exists(g):
    q = sql(g, 70, 300, ["SELECT name FROM customers c", "WHERE EXISTS (", "  SELECT 1 FROM orders o", "  WHERE o.customer_id = c.id);"], 1, fs=30, w=940, hl=[3] if g.b >= 1 else [1])
    ct = customers(g, 70, 640, 1); ot = orders(g, 450, 640, g.on(0, .4))
    if g.b >= 1:
        cur = min(2, int(g.at(1, .4, 4.2) * 3)) if g.b == 1 else 2
        for i in range(cur + 1):
            cid = CUS[i][0]; hits = [k for k, o in enumerate(ORD) if o[1] == cid]
            if hits:
                k = hits[0]; r0 = ct.row(i); r1 = ot.row(k)
                arrow(g, (r0[2] + 6, (r0[1] + r0[3]) / 2), (r1[0] - 6, (r1[1] + r1[3]) / 2), CC[cid], 1, 1, 4, 14)
                check(g, 30 + 6, (r0[1] + r0[3]) / 2, True, 1, 18)
            else:
                check(g, 36, (ct.row(i)[1] + ct.row(i)[3]) / 2, False, 1, 18)
        if g.b == 1: ring(g, ct.row(cur), YEL, 1)
    if g.b >= 2:
        box(g, (70, 1060, 1010, 1180), GREEN, g.on(2, .2), "EXISTS stops at the FIRST match", "it only asks: is there at least one?", 36, 28, scol=WHITE)


def s_error(g):
    q = sql(g, 70, 320, ["SELECT name FROM customers", "WHERE id = (SELECT customer_id", "            FROM orders);"], 1, fs=32, w=940, hl=[1], hlcol=RED)
    box(g, (70, 540, 1010, 660), RED, g.on(0, 1.2), "ORA-01427: single-row subquery returns more than one row", None, 26, fill=(40, 16, 26))
    if g.b >= 1:
        a = g.on(1, .2)
        pill(g, 300, 760, "=", WHITE, a, 50); tx(g, 300, 830, "wants ONE value", SB(30), WHITE, a, "mm")
        for k, v in enumerate((1, 2, 1, 2, 1)): chip(g, 560 + k * 92, 760, 80, 66, str(v), CC[v], g.on(1, .8 + k * .15), 30)
        tx(g, 740, 830, "got FIVE", SB(30), RED, g.on(1, 1.8), "mm")
    if g.b >= 2:
        a2 = g.on(2, .2)
        f = sql(g, 70, 920, ["WHERE id IN (SELECT customer_id FROM orders)"], a2, fs=30, w=940, hl=[0], hlcol=GREEN)
        tx(g, 540, 1040, "many values?  use IN", SB(34), GREEN, a2, "mm")
        g.focus(f.box, a=a2)


WORDS = [("( SELECT … )", "a question inside a question"), ("inner first", "its answer feeds the outer"), ("= (…)", "needs ONE value"),
         ("IN (…)", "accepts a list"), ("NOT IN + NULL", "zero rows!"), ("EXISTS", "is there at least one?")]


def s_recap(g):
    la = g.until(0)
    for k, (kw, plain) in enumerate(WORDS):
        if la <= 0: break
        y = 330 + k * 140; lit = pr(g.bt, .8 + k * .85, 1.1 + k * .85)
        col = [YEL, CYAN, RED, GREEN, PINK, PURP][k]
        g.d.rounded_rectangle((70, y, 1010, y + 118), 22, fill=mix(CARD, la), outline=mix(col, la * (.25 + .75 * lit)), width=3)
        badge(g, 140, y + 59, k + 1, col, la * (.3 + .7 * lit), 32)
        tx(g, 205, y + 59, kw, MB(32), col, la * (.3 + .7 * lit), "lm")
        tx(g, 985, y + 59, plain, SN(30), WHITE, la * lit, "rm")
    if g.b == 1:
        tx(g, 540, 520, "Next video", SB(48), DIM, g.on(1, .2), "mm")
        tx(g, 540, 620, "COMMIT & ROLLBACK", XB(70), YEL, g.on(1, .5), "mm")
        tx(g, 540, 720, "transactions from zero", SN(38), WHITE, g.on(1, .8), "mm")
        p = 1 + .04 * math.sin(g.t * 7); bw, bh = 760 * p, 130 * p; ab = g.on(1, 1.2)
        g.d.rounded_rectangle((540 - bw / 2, 920 - bh / 2, 540 + bw / 2, 920 + bh / 2), 65, fill=mix(GREEN, ab))
        tx(g, 540, 920, "@sql_developer_no1", SB(54), INK, ab, "mm")
        tx(g, 540, 1060, "follow · save · share", SN(42), DIM, g.on(1, 1.6), "mm")


SCENES = [
    ("A question inside a question", WHITE, s_hook, [
        "Which orders are *bigger than the average*?",
        "To answer, you first need the average. Only *then* can you compare each order.",
        "In SQL, that first question is written *inside* the second one. It's called a *subquery*."]),
    ("Think of a teacher", ORANGE, s_analogy, [
        "Think of a teacher asking: who scored *above the class average*?",
        "First, she calculates the average: *seventy five*. That's the *inner* question.",
        "Then she checks every student against it: Nigar and Sevda. That's the *outer* question."]),
    ("The subquery runs first", YEL, s_scalar, [
        "Here's the query. The part in brackets is the subquery. It runs *first*.",
        "It adds up all amounts and divides by five. The whole bracket becomes *one number*: forty.",
        "Now the outer query is simple: amount greater than forty. Three orders pass.",
        "So: a subquery is a *SELECT inside another SELECT*, in brackets."]),
    ("IN: a subquery that returns a list", GREEN, s_in, [
        "Which customers have placed *any* order? Here, the subquery returns *customer ids*.",
        "The answer is a *list*: one, two, one, two, one. Repeats don't matter, so it's just one and two.",
        "*IN* keeps the customers whose id is in that list: Aysel and Murad."]),
    ("The NOT IN trap", PINK, s_notin, [
        "Now the opposite: NOT IN. But this time, the list contains one empty value: *NULL*.",
        "Is three not in one, two, null? Three is not one. Not two. But compared with NULL, the answer is *unknown*.",
        "Unknown is not true, so *no row* comes back. Zero rows, and *no error*.",
        "Fix it: remove the NULLs inside the subquery, or use *NOT EXISTS*."]),
    ("EXISTS: is there at least one?", PURP, s_exists, [
        "*EXISTS* asks a yes or no question for each customer: does at least one order exist?",
        "For Aysel, it finds an order and *stops*. Murad: yes. Leyla: no order, so she's out.",
        "It doesn't care how many. It only needs *one* match."]),
    ("The single-row error", RED, s_error, [
        "One more classic error. An *equals sign* in front of a subquery that returns *many* rows.",
        "Equals wants exactly *one* value. The subquery gave back *five*.",
        "If the answer can be a list, use *IN* instead of equals."]),
    ("Remember", GREEN, s_recap, [
        "Remember: the inner query runs first, and its answer feeds the outer one. Equals needs one value, IN takes a list, and watch out for NULL with NOT IN.",
        "Next: *COMMIT and ROLLBACK*. Transactions from zero. Follow, so you don't miss it."]),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    run(SCENES, Stage(1080, 1920, 30), "/home/claude/v2/out54", "/home/claude/en/sql_video54_EN_subqueries.mp4", mode, seed=54, max_dur=175)

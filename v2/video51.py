"""51 · The real order of a SELECT (v2 style: beat-synced, lit, beginner-first)."""
import sys
sys.path.insert(0, "/home/claude/v2")
from studio import *

ROWS = [(1, "Baku", 50), (2, "Ganja", 20), (3, "Baku", 70), (4, "Shaki", 10), (5, "Ganja", 40), (6, "Shaki", 30), (7, "Baku", 5)]
CC = {"Baku": CYAN, "Ganja": PURP, "Shaki": ORANGE}
KEEP = [0, 1, 2, 4, 5]                      # rows that pass WHERE amount > 15
Q = ["SELECT city, SUM(amount) AS total", "FROM   orders", "WHERE  amount > 15", "GROUP BY city", "HAVING SUM(amount) > 50", "ORDER BY total DESC;"]
STEP = {1: 1, 2: 2, 3: 3, 4: 4, 0: 5, 5: 6}   # line -> execution step
LINE = {v: k for k, v in STEP.items()}
TX, TY, CW, RH = 210, 700, [120, 300, 240], 60
PX = {"Baku": 210, "Ganja": 540, "Shaki": 870}


def qblock(g, step, a=1.0):
    """the query, with the clause of the current step lit and the step numbers found so far"""
    num = {LINE[s]: s for s in range(1, step + 1)}
    dim = [LINE[s] for s in range(step + 1, 7)]
    return sql(g, 70, 310, Q, a, fs=32, w=940, hl=[LINE[step]], dim=dim, num=num or {9: 0})


def orders(g, a=1.0, **kw):
    return table(g, TX, TY, ["id", "city", "amount"], ROWS, CW, RH, a, fs=32, name="orders",
                 ccol=lambda r, c: CC[ROWS[r][1]] if c == 1 else None, **kw)


def pile(g, city, vals, a=1.0, total=None, ta=0.0, dead=0.0):
    """one group: header + its receipts + the sum"""
    cx = PX[city]; col = CC[city]; al = a * (1 - .72 * dead)
    pill(g, cx, 760, city, col, al, 34, fill=True)
    for k, v in enumerate(vals): chip(g, cx, 850 + k * 70, 190, 56, str(v), col, al, 32)
    if total is not None and ta > 0:
        y = 850 + len(vals) * 70 + 6
        g.d.line((cx - 95, y - 22, cx + 95, y - 22), fill=mix(col, al * ta), width=3)
        tx(g, cx, y + 16, f"{total}", XB(46), WHITE, al * ta, "mm")
        tx(g, cx, y + 58, "total", SN(26), DIM, al * ta, "mm")
    if dead > 0:
        g.d.line((cx - 120, 740, cx + 120, 1060), fill=mix(RED, dead), width=6); g.d.line((cx + 120, 740, cx - 120, 1060), fill=mix(RED, dead), width=6)


# ------------------------------------------------------------------ scenes
def s_hook(g):
    if g.b < 2:
        cd = sql(g, 70, 330, Q, g.on(0), fs=32, w=940, num={i: i + 1 for i in range(6)})
        tx(g, 540, 720, "the order you WRITE it", SB(36), DIM, g.only(0), "mm")
        a = g.on(1)
        if a > 0:
            r = (84, 344, 136, 652); g.d.line((r[0], r[1], r[2], r[3]), fill=mix(RED, a), width=7); g.d.line((r[2], r[1], r[0], r[3]), fill=mix(RED, a), width=7)
            box(g, (170, 720, 910, 850), RED, a, "NOT the order it RUNS", None, 40)
    else:
        cd = sql(g, 70, 330, Q, 1, fs=32, w=940, hl=[1], dim=[0, 2, 3, 4, 5], num={1: 1})
        a = g.on(2, .3)
        arrow(g, (540, 800), (540, 680), GREEN, a, g.at(2, .3, .9), 7)
        box(g, (220, 810, 860, 930), GREEN, a, "it starts HERE", "in the middle of your query", 40, 28)
        g.focus(cd.line(1), (220, 680, 860, 930), a=a)


def s_analogy(g):
    a = g.on(0)
    person(g, 250, 560, 230, ORANGE, a, "shop owner", 30)
    # the box of receipts
    bx = (560, 470, 900, 690)
    for k in range(5):
        x = 600 + k * 56; y = 420 + (k % 2) * 24 - 6 * math.sin(g.t * 1.3 + k)
        g.d.rounded_rectangle((x, y, x + 46, y + 110), 6, fill=mix(WHITE, a * .92));
        for j in range(3): g.d.line((x + 8, y + 18 + j * 16, x + 38, y + 18 + j * 16), fill=mix(DIM, a), width=3)
    g.d.rounded_rectangle(bx, 16, fill=mix(CARD2, a), outline=mix(ORANGE, a), width=4)
    tx(g, 730, 580, "box of receipts", SB(32), ORANGE, a, "mm")
    q = g.on(1)
    box(g, (110, 770, 970, 880), YEL, q, "Which city brings in the most money?", None, 36, tcol=WHITE)
    if g.b == 2:
        a2 = g.only(2, delay=.2)
        pill(g, 300, 1000, "1 · get the receipts", GREEN, a2, 32, fill=True)
        arrow(g, (520, 1000), (600, 1000), WHITE, a2, 1, 5, 16)
        pill(g, 800, 1000, "2 · the answer", DIM, a2, 32)
        g.focus((540, 380, 920, 710), (90, 950, 990, 1050), a=a2)
    if g.b >= 3:
        vs_panel(g, 930, ["the box", "one receipt", "what is written on it"], ["TABLE", "ROW", "COLUMNS"],
                 a_l=lambda i: g.on(3, i * .5), a_r=lambda i: g.on(3, .25 + i * .5), fs=32)


def s_from(g):
    cd = qblock(g, 1)
    a = g.on(0, .5)
    tb = orders(g, a, ra=lambda i: g.on(0, .7 + i * .16))
    if g.b == 0: g.focus(cd.line(1), tb.box, a=a)
    if g.b == 1:
        a1 = g.only(1)
        l1 = callout(g, tb.row(2), "one ROW = one order", YEL, a1, at=(330, 1310), fs=30)
        l2 = callout(g, tb.col(2, -1, -1), "a COLUMN", GREEN, g.only(1, delay=.9), at=(820, 1310), fs=30)
        g.focus(tb.box, l1, l2, a=a1)


def s_where(g):
    cd = qblock(g, 2)
    gone = g.at(1, .2, .9)
    if g.b == 0: cur = min(6, int(g.at(0, 1.3, g.bl - .4) * 7))
    else: cur = -1
    tb = orders(g, 1, hl=[cur] if cur >= 0 else (), strike=[3, 6] if g.b >= 1 else (), dim=[3, 6] if gone > .6 else ())
    for i, (_, _, amt) in enumerate(ROWS):
        r = tb.row(i); shown = (g.b > 0) or (i <= cur)
        if shown: check(g, r[2] + 60, (r[1] + r[3]) / 2, amt > 15, (1 if amt > 15 or g.b < 2 else .5), 24)
    if g.b == 0:
        pill(g, 540, 1300, "amount > 15 ?", YEL, g.on(0, .8), 38)
        g.focus(cd.line(2), (tb.box[0], tb.box[1], tb.box[2] + 110, tb.box[3]), (330, 1250, 750, 1350), a=g.on(0, .5))
    if g.b == 1:
        g.focus(tb.row(3), tb.row(6), (tb.row(3)[2] + 20, tb.row(3)[1], tb.row(3)[2] + 100, tb.row(3)[3]),
                (tb.row(6)[2] + 20, tb.row(6)[1], tb.row(6)[2] + 100, tb.row(6)[3]), a=g.only(1))
    if g.b == 2:
        a2 = g.on(2, .2)
        pill(g, 400, 1300, "7 rows", DIM, a2, 36); arrow(g, (500, 1300), (580, 1300), WHITE, a2, 1, 5, 16); pill(g, 690, 1300, "5 rows", GREEN, a2, 36, fill=True)


def s_group(g):
    cd = qblock(g, 3)
    fly = g.at(0, 1.0, 3.6)
    ta = 1 - g.at(0, .8, 1.6)
    if ta > 0: table(g, TX, TY, ["id", "city", "amount"], [], CW, RH, ta, fs=32, name="orders")
    tb = Tb(TX, TY, CW, RH, 7, 6)
    slot = {"Baku": 0, "Ganja": 0, "Shaki": 0}
    for j, i in enumerate(KEEP):
        _, city, amt = ROWS[i]; r = tb.row(i); p0 = ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
        p1 = (PX[city], 850 + slot[city] * 70); slot[city] += 1
        p = g.at(0, 1.0 + j * .45, 1.9 + j * .45)
        x, y = mv(p0, p1, p); w = lerp(660, 190, p)
        chip(g, x, y, w, 56, f"{city}  {amt}" if p < .5 else str(amt), CC[city], 1, 32)
    for city in PX:
        vals = [ROWS[i][2] for i in KEEP if ROWS[i][1] == city]
        pill(g, PX[city], 760, city, CC[city], g.at(0, .9, 1.5), 34, fill=True)
        if g.b >= 1:
            k = list(PX).index(city); ta_ = g.on(1, .9 + k * .9)
            y = 850 + len(vals) * 70 + 6
            g.d.line((PX[city] - 95, y - 22, PX[city] + 95, y - 22), fill=mix(CC[city], ta_), width=3)
            tx(g, PX[city], y + 16, str(sum(vals)), XB(46), WHITE, ta_, "mm"); tx(g, PX[city], y + 58, "total", SN(26), DIM, ta_, "mm")
    if g.b == 0: g.focus(cd.line(3), (60, 700, 1020, 1260), a=g.on(0, .4))
    if g.b == 2:
        term(g, "GROUP", "a pile of rows that share the same value", g.on(2, .2), y=1200, col=GREEN)


def s_having(g):
    cd = qblock(g, 4)
    dead = g.at(1, 2.2, 2.9)
    pile(g, "Baku", [50, 70], 1, 120, 1); pile(g, "Ganja", [20, 40], 1, 60, 1); pile(g, "Shaki", [30], 1, 30, 1, dead=dead)
    if g.b <= 1:
        pill(g, 540, 1200, "total > 50 ?", YEL, g.on(0, .9), 38)
    if g.b >= 1:
        for k, (city, tot) in enumerate((("Baku", 120), ("Ganja", 60), ("Shaki", 30))):
            check(g, PX[city], 1125, tot > 50, g.on(1, .3 + k * .7), 26)
    if g.b == 0: g.focus(cd.line(4), (60, 720, 1020, 1200), a=g.on(0, .4))
    if g.b == 2:
        a = g.on(2, .2)
        box(g, (70, 1200, 520, 1380), CYAN, a, "WHERE", "filters ROWS · before groups", 44, 26)
        box(g, (560, 1200, 1010, 1380), YEL, g.on(2, 1.6), "HAVING", "filters GROUPS · after", 44, 26)
        g.focus((60, 1190, 1030, 1390), cd.line(2), cd.line(4), a=a)


def s_select(g):
    cd = qblock(g, 5 if g.b == 0 else 6)
    a = g.on(0, .4)
    hx = 240; cw = [300, 300]
    for c, hname in enumerate(("city", "total")):
        chip(g, hx + c * 300 + 150, 760, 290, 60, hname, YEL if c == 1 else CYAN, a, 32, fill=CARD2, tcol=YEL if c == 1 else CYAN)
    sw = g.at(1, 3.6, 4.6)                       # the swap happens when the voice says ORDER BY
    yA, yB = 835, 905
    for (city, tot, y0, y1, d_) in (("Ganja", 60, yA, yB, .5), ("Baku", 120, yB, yA, .9)):
        y = lerp(y0, y1, sw); al = g.on(0, .4 + d_)
        chip(g, hx + 150, y, 290, 60, city, CC[city], al, 32, tcol=CC[city]); chip(g, hx + 450, y, 290, 60, str(tot), CC[city], al, 32)
    if g.b == 0:
        l = callout(g, (hx + 305, 730, hx + 595, 790), "the sum gets a name", YEL, g.on(0, 3.2), at=(700, 688), fs=28)
        g.focus(cd.line(0), (220, 720, 860, 950), l, a=a)
    if g.b == 1:
        term(g, "ALIAS", "a nickname you give to a column", g.only(1) * (1 - g.at(1, 3.0, 3.4)), y=1020)
        a1 = g.on(1, 3.4)
        tx(g, 930, 870, "biggest", SB(28), GREEN, a1, "mm"); tx(g, 930, 905, "first", SB(28), GREEN, a1, "mm")
        arrow(g, (930, 800), (930, 845), GREEN, a1, 1, 5, 14)
        box(g, (240, 1060, 840, 1170), GREEN, g.on(1, 4.8), "the final result", None, 40)
        g.focus(cd.line(5), cd.line(0), (220, 720, 1010, 950), (230, 1010, 1010, 1180), a=g.on(1))


BADQ = ["SELECT city,", "       amount * 1.18 AS with_tax", "FROM   orders", "WHERE  with_tax > 50;"]


def s_trap(g):
    cd = sql(g, 70, 310, BADQ, 1, fs=32, w=940, hl=[3] if g.b <= 2 else (), hlcol=RED, num={2: 1, 3: 2, 0: 3} if g.b >= 1 else {9: 0})
    box(g, (70, 566, 1010, 676), RED, g.on(0, 1.6), 'ORA-00904: "WITH_TAX": invalid identifier', None, 34, fill=(40, 16, 26))
    if g.b >= 1:
        a = g.on(1)
        y = 800; xs = (190, 540, 890); names = ("FROM", "WHERE", "SELECT")
        g.d.line((xs[0], y, xs[2], y), fill=mix(OFFB, a), width=6)
        for k, (x, nm) in enumerate(zip(xs, names)):
            badge(g, x, y, k + 1, RED if k == 1 else (YEL if k == 2 else DIM), a, 30)
            tx(g, x, y + 50, nm, MB(30), WHITE, a, "ma")
        tx(g, xs[1], y + 96, "needs with_tax", SN(28), RED, g.on(1, .8), "ma")
        tx(g, xs[2], y + 96, "with_tax is born", SN(28), YEL, g.on(1, 2.6), "ma")
        tx(g, (xs[1] + xs[2]) / 2, y - 62, "too early!", SB(30), RED, g.on(1, 3.4), "mm")
    if g.b == 1: g.focus((90, 720, 990, 950), cd.line(3), cd.line(1), a=g.on(1))
    if g.b >= 2:
        a = g.on(2, 1.9)
        f1 = sql(g, 70, 990, ["WHERE  amount * 1.18 > 50"], a, fs=32, w=820); check(g, 950, 1034, True, a, 30)
        if g.b == 2: g.focus(f1.box, (910, 990, 1000, 1080), cd.line(3), a=a)
    if g.b >= 3:
        a = g.on(3, .3)
        f2 = sql(g, 70, 1100, ["ORDER BY with_tax DESC;"], a, fs=32, w=820); check(g, 950, 1144, True, a, 30)
        if g.b == 3: g.focus(f2.box, (910, 1100, 1000, 1190), a=a)
    if g.b >= 4:
        a = g.on(4, .2)
        r = (70, 1220, 1010, 1370); box(g, r, PURP, a, None, None)
        icon(g, "bulb", 140, 1295, 70, PURP, a)
        tx(g, 200, 1250, "Inside, Oracle takes shortcuts for speed.", SB(30), WHITE, a)
        tx(g, 200, 1300, "The result always matches these steps.", SN(30), SOFT, a)
        g.focus(r, a=a)


WORDS = [("FROM", "get the rows"), ("WHERE", "filter rows"), ("GROUP BY", "make groups"), ("HAVING", "filter groups"), ("SELECT", "pick columns"), ("ORDER BY", "sort")]


def s_recap(g):
    la = g.until(1)
    for k, (kw, plain) in enumerate(WORDS):
        y = 340 + k * 150
        lit = 1.0 if g.b >= 1 else pr(g.bt, 1.6 + k * .62, 1.9 + k * .62)
        lit2 = pr(g.bt, .3 + k * .72, .6 + k * .72) if g.b == 1 else (1.0 if g.b > 1 else 0.0)
        col = [GREEN, CYAN, PURP, YEL, PINK, ORANGE][k]
        if la <= 0: continue
        g.d.rounded_rectangle((70, y, 1010, y + 126), 22, fill=mix(CARD, la), outline=mix(col, la * (.25 + .75 * lit)), width=3)
        badge(g, 140, y + 63, k + 1, col, la * (.3 + .7 * lit), 34)
        tx(g, 210, y + 63, kw, MB(40), col, la * (.3 + .7 * lit), "lm")
        tx(g, 980, y + 63, plain, SN(36), WHITE, la * lit2, "rm")
    if g.b == 2:
        a = g.on(2, .2)
        tx(g, 540, 520, "Next video", SB(48), DIM, a, "mm")
        tx(g, 540, 620, "GROUP BY from zero", XB(72), YEL, g.on(2, .5), "mm")
        tx(g, 540, 720, "piles, totals and the classic error", SN(38), WHITE, g.on(2, .8), "mm")
        p = 1 + .04 * math.sin(g.t * 7); bw, bh = 760 * p, 130 * p; ab = g.on(2, 1.2)
        g.d.rounded_rectangle((540 - bw / 2, 920 - bh / 2, 540 + bw / 2, 920 + bh / 2), 65, fill=mix(GREEN, ab))
        tx(g, 540, 920, "@sql_developer_no1", SB(54), INK, ab, "mm")
        tx(g, 540, 1060, "follow · save · share", SN(42), DIM, g.on(2, 1.6), "mm")


SCENES = [
    ("SQL does not read top to bottom", WHITE, s_hook, [
        "You write a query from top to bottom. *SELECT* comes first.",
        "But the database does *not* run it in that order.",
        "It starts in the middle, with *FROM*. Let's follow it, step by step."]),
    ("Think of a box of receipts", ORANGE, s_analogy, [
        "Imagine a shop owner with a *box of receipts*.",
        "She asks: which city brings in the most money?",
        "She can't write the answer first. First, she must *get the receipts*.",
        "In a database, the box is a *table*. Each receipt is a *row*."]),
    ("Step 1 · FROM = open the box", GREEN, s_from, [
        "Step one: *FROM*. The database opens the table and takes *all* its rows.",
        "Seven orders. Every row has an {id|I D}, a city, and an amount."]),
    ("Step 2 · WHERE = remove rows", CYAN, s_where, [
        "Step two: *WHERE*. It checks every row, one by one: is the amount above fifteen?",
        "Ten is too small. Five is too small. These two rows are *thrown away*.",
        "Five rows are left. Notice: WHERE looks at *single rows* only."]),
    ("Step 3 · GROUP BY = make piles", PURP, s_group, [
        "Step three: *GROUP BY* city. Rows with the same city go into *one pile*.",
        "Then each pile is added up: one hundred twenty, sixty, and thirty.",
        "From now on, there are no single rows. Only *groups*."]),
    ("Step 4 · HAVING = remove piles", YEL, s_having, [
        "Step four: *HAVING*. It is also a filter, but for *piles*, not for rows.",
        "Is the total above fifty? Shaki has only thirty, so that pile is removed.",
        "So: *WHERE* filters rows, before grouping. *HAVING* filters groups, after it."]),
    ("Steps 5 and 6 · SELECT, ORDER BY", PINK, s_select, [
        "Only now comes step five: *SELECT*. It writes one line per pile, and names the sum *total*.",
        "That name is called an *alias*. Step six, *ORDER BY*, sorts the result: biggest first."]),
    ("Why the order matters", RED, s_trap, [
        "Now you can understand a famous error. This query *fails*.",
        "*WHERE* is step two. But the name with_tax is created in *SELECT*, later.",
        "For WHERE, that name *does not exist yet*. So, write the formula again.",
        "In *ORDER BY* the name works, because sorting is the *last* step.",
        "One more thing. Inside, the database may take shortcuts. But the result always matches these steps."]),
    ("Remember the real order", GREEN, s_recap, [
        "Remember the real order: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.",
        "Get rows. Filter rows. Make groups. Filter groups. Pick columns. Sort.",
        "Next: *GROUP BY* from zero. Follow, so you don't miss it."]),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    run(SCENES, Stage(1080, 1920, 30), "/home/claude/v2/out51", "/home/claude/en/sql_video51_EN_select_order.mp4", mode, seed=51, max_dur=175)

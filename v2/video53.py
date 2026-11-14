"""53 · JOIN from zero (v2 style)."""
import sys
sys.path.insert(0, "/home/claude/v2")
from studio import *

CUS = [(1, "Aysel"), (2, "Murad"), (3, "Leyla")]
ORD = [(101, 1, 50), (102, 2, 70), (103, 1, 20), (104, 2, 15)]
CC = {1: CYAN, 2: PURP, 3: ORANGE}
CX, CY, CCW = 70, 560, [100, 220]
OX, OY, OCW = 500, 560, [130, 230, 150]
RH = 62


def customers(g, a=1.0, ra=None, **kw):
    return table(g, CX, CY, ["id", "name"], CUS, CCW, RH, a, fs=32, name="customers", col=CYAN,
                 ccol=lambda r, c: CC[CUS[r][0]] if c == 0 else None, ra=ra, **kw)


def orders(g, a=1.0, ra=None, **kw):
    return table(g, OX, OY, ["id", "customer_id", "amount"], ORD, OCW, RH, a, fs=32, name="orders", col=GREEN,
                 ccol=lambda r, c: CC[ORD[r][1]] if c == 1 else None, ra=ra, **kw)


def links(g, ct, ot, a, rv=1.0, which=range(4)):
    for i in which:
        cid = ORD[i][1]; r0 = ot.row(i); r1 = ct.cell(cid - 1, 1)
        p0 = (r0[0] - 8, (r0[1] + r0[3]) / 2); p1 = (r1[2] + 8, (r1[1] + r1[3]) / 2)
        path(g, [p0, (p0[0] - 25, p0[1]), (p1[0] + 25, p1[1]), p1], CC[cid], a, rv, 4, 16)
        if a * rv > .5: g.d.rounded_rectangle(ot.cell(i, 1), 10, outline=mix(CC[cid], a * .8), width=2)


# ------------------------------------------------------------------ scenes
def s_hook(g):
    ct = customers(g, g.on(0, .2)); ot = orders(g, g.on(0, .7))
    if g.b >= 1:
        a = g.on(1, .2)
        box(g, (120, 900, 960, 1030), YEL, a, "Who bought what?", "names are HERE · amounts are THERE", 42, 30, scol=WHITE)
        g.focus(ct.box, ot.box, (120, 900, 960, 1030), a=g.only(1))
    if g.b >= 2:
        pill(g, 540, 1110, "JOIN = put them side by side", GREEN, g.on(2, .2), 36, fill=True)


def s_why(g):
    bad = [(101, "Aysel", 50), (102, "Murad", 70), (103, "Aysel", 20)]
    tb = table(g, 150, 360, ["id", "name", "amount"], bad, [140, 300, 240], RH, g.on(0), fs=32, name="one big table?", col=RED,
               ccol=lambda r, c: RED if (c == 1 and r in (0, 2) and g.b >= 1) else None)
    if g.b >= 1:
        callout(g, tb.cell(2, 1), "the name, again and again", RED, g.on(1, .4), at=(540, 640), fs=30)
        g.focus(tb.cell(0, 1), tb.cell(2, 1), (300, 600, 780, 680), a=g.only(1))
    if g.b >= 2:
        a = g.on(2, .2)
        box(g, (70, 740, 1010, 860), ORANGE, a, "she changes her name → fix EVERY order", None, 32)
    if g.b >= 3:
        a = g.on(3, .2)
        chip(g, 300, 980, 360, 80, "Aysel · ONCE", CYAN, a, 34, mono=False, tcol=CYAN)
        chip(g, 780, 980, 360, 80, "orders: just id 1", GREEN, a, 32, mono=False, tcol=GREEN)
        arrow(g, (595, 980), (485, 980), WHITE, g.on(3, .8), 1, 5, 16)
        tx(g, 540, 1070, "the number points to the person", SB(32), YEL, g.on(3, 1.4), "mm")


def s_ticket(g):
    a = g.on(0)
    # coat check counter
    person(g, 220, 520, 220, ORANGE, a, "you", 30)
    tk = (420, 430, 620, 560)
    g.d.rounded_rectangle(tk, 14, fill=mix(YEL, a)); tx(g, 520, 470, "ticket", SB(26), INK, a, "mm"); tx(g, 520, 520, "No 2", XB(44), INK, a, "mm")
    for k, (n, c) in enumerate(((1, CYAN), (2, PURP), (3, ORANGE))):
        x = 730 + k * 110; al = a
        g.d.line((x, 380, x, 420), fill=mix(SOFT, al), width=4)
        g.d.polygon([(x - 45, 420), (x + 45, 420), (x + 50, 590), (x - 50, 590)], fill=mix(mix(c, .45, CARD), al), outline=mix(c, al))
        tx(g, x, 620, str(n), SB(30), c, al, "mm")
    if g.b >= 1:
        hl = g.on(1, .5)
        ring(g, (725 + 110 - 55, 400, 725 + 110 + 55, 640), YEL, hl)
        path(g, [(620, 495), (690, 495), (780, 495)], YEL, hl, g.at(1, .4, 1.2), 5, 16)
    if g.b >= 2:
        vs_panel(g, 760, ["ticket number", "the coats", "your number = coat number"], ["customer_id", "customers table", "ON  o.customer_id = c.id"],
                 a_l=lambda i: g.on(2, i * .7), a_r=lambda i: g.on(2, .35 + i * .7), fs=30)


def s_inner(g):
    if g.b == 0:
        q = sql(g, 70, 330, ["SELECT c.name, o.amount", "FROM   orders o", "JOIN   customers c", "  ON   o.customer_id = c.id;"], g.on(0), fs=32, w=940, hl=[3])
        callout(g, q.line(3), "the matching rule", YEL, g.on(0, 2.4), at=(540, 680), fs=32, mark=False)
        sm = (70, 760, 1010, 900)
        box(g, sm, CYAN, g.on(0, 4.0), "order.customer_id = customer.id", "the order's ticket number = the person's number", 32, 26, scol=WHITE)
        g.focus(q.box, sm, (330, 650, 750, 710), a=g.on(0, 2))
        return
    ct = customers(g); ot = orders(g)
    cur = min(3, int(g.at(1, .1, 3.6) * 4)) if g.b == 1 else (3 if g.b > 1 else -1)
    if True:
        links(g, ct, ot, 1, 1, which=range(cur + 1))
        if g.b == 1:
            r0 = ot.row(cur); ring(g, r0, YEL, 1)
            g.focus(ot.row(cur), ct.row(ORD[cur][1] - 1), a=g.on(1, .2))
    if g.b >= 2:
        res = [(CUS[o[1] - 1][1], o[2]) for o in ORD]
        rt = table(g, 270, 940, ["name", "amount"], res, [300, 240], RH, g.on(2, .2), fs=32, col=YEL, name="result",
                   ra=lambda i: g.on(2, .3 + i * .3), ccol=lambda r, c: CC[ORD[r][1]] if c == 0 else None)


def s_missing(g):
    ct = customers(g, hl=[2] if g.b >= 0 else (), hlcol=ORANGE); ot = orders(g); links(g, ct, ot, .5)
    a = g.on(0, .4)
    callout(g, ct.row(2), "no orders at all", ORANGE, a, at=(240, 880), fs=30, mark=False)
    if g.b >= 1:
        a1 = g.on(1, .2)
        res = [(CUS[o[1] - 1][1], o[2]) for o in ORD]
        rt = table(g, 270, 980, ["name", "amount"], res, [300, 240], 56, a1, fs=30, col=YEL, name="JOIN result",
                   ccol=lambda r, c: CC[ORD[r][1]] if c == 0 else None)
        tx(g, 540, rt.bottom + 36, "Leyla is missing", SB(36), ORANGE, g.on(1, 1.4), "mm")
        g.focus(ct.row(2), rt.box, (300, rt.bottom + 10, 780, rt.bottom + 70), a=g.only(1))
    if g.b >= 2:
        term(g, "INNER JOIN", "keeps only rows that found a partner", g.on(2, .2), y=1240, col=YEL)


def s_left(g):
    q = sql(g, 70, 290, ["SELECT c.name, o.amount", "FROM   customers c", "LEFT JOIN orders o", "  ON   o.customer_id = c.id;"], 1, fs=30, w=940, hl=[2], hlcol=GREEN)
    res = [("Aysel", 50), ("Aysel", 20), ("Murad", 70), ("Murad", 15), ("Leyla", "NULL")]
    cmap = {"Aysel": CYAN, "Murad": PURP, "Leyla": ORANGE}
    rt = table(g, 270, 620, ["name", "amount"], res, [300, 240], RH, g.on(0, .4), fs=32, col=GREEN, name="LEFT JOIN result",
               ra=lambda i: g.on(0, .6 + i * .3), hl=[4] if g.b >= 1 else (), hlcol=ORANGE,
               ccol=lambda r, c: cmap[res[r][0]] if c == 0 else (PINK if res[r][1] == "NULL" and c == 1 else None))
    if g.b == 0: g.focus(q.line(1), q.line(2), a=g.on(0, 1.5))
    if g.b >= 1:
        callout(g, rt.cell(4, 1), "no partner → empty (NULL)", PINK, g.on(1, 1.2), at=(540, rt.bottom + 70), fs=30, mark=False)
        g.focus(rt.row(4), (230, rt.bottom + 30, 850, rt.bottom + 110), a=g.only(1))
    if g.b >= 2:
        a = g.on(2, .3)
        f = sql(g, 70, 1150, ["... WHERE o.id IS NULL;   -- never ordered"], a, fs=30, w=940, hl=[0], hlcol=GREEN)
        g.focus(f.box, rt.row(4), a=a)


def s_trap(g):
    q = sql(g, 70, 290, ["SELECT c.name, o.amount", "FROM   customers c, orders o;   -- no rule!"], 1, fs=30, w=940, hl=[1], hlcol=RED)
    a = g.on(0, .4)
    # 3 x 4 grid of pairs
    for i in range(3):
        for j in range(4):
            al = g.on(0, .8 + (i * 4 + j) * .14)
            x = 210 + j * 220; y = 560 + i * 120
            chip(g, x, y, 200, 90, f"{CUS[i][1][:5]}·{ORD[j][2]}", CC[CUS[i][0]], al, 26, mono=False, tcol=WHITE)
    tx(g, 540, 940, "3 × 4 = 12 rows", XB(50), RED, g.on(0, 2.6), "mm")
    if g.b >= 1:
        a1 = g.on(1, .2)
        box(g, (70, 1010, 1010, 1150), RED, a1, "100 000 × 1 000 000", "= 100 000 000 000 rows", 40, 32, scol=WHITE)
        g.focus((70, 1010, 1010, 1150), q.line(1), a=g.only(1))
    if g.b >= 2:
        box(g, (70, 1190, 1010, 1300), GREEN, g.on(2, .2), "always write the ON rule", None, 38)


WORDS = [("JOIN", "put two tables side by side"), ("ON", "the matching rule"), ("INNER JOIN", "only rows with a partner"),
         ("LEFT JOIN", "keep all left rows"), ("no ON", "every row × every row")]


def s_recap(g):
    la = g.until(0)
    for k, (kw, plain) in enumerate(WORDS):
        if la <= 0: break
        y = 340 + k * 150; lit = pr(g.bt, .9 + k * 1.0, 1.2 + k * 1.0)
        col = [GREEN, YEL, CYAN, PURP, RED][k]
        g.d.rounded_rectangle((70, y, 1010, y + 126), 22, fill=mix(CARD, la), outline=mix(col, la * (.25 + .75 * lit)), width=3)
        badge(g, 140, y + 63, k + 1, col, la * (.3 + .7 * lit), 34)
        tx(g, 210, y + 63, kw, MB(36), col, la * (.3 + .7 * lit), "lm")
        tx(g, 980, y + 63, plain, SN(32), WHITE, la * lit, "rm")
    if g.b == 1:
        tx(g, 540, 520, "Next video", SB(48), DIM, g.on(1, .2), "mm")
        tx(g, 540, 620, "Subqueries from zero", XB(70), YEL, g.on(1, .5), "mm")
        tx(g, 540, 720, "a question inside a question", SN(38), WHITE, g.on(1, .8), "mm")
        p = 1 + .04 * math.sin(g.t * 7); bw, bh = 760 * p, 130 * p; ab = g.on(1, 1.2)
        g.d.rounded_rectangle((540 - bw / 2, 920 - bh / 2, 540 + bw / 2, 920 + bh / 2), 65, fill=mix(GREEN, ab))
        tx(g, 540, 920, "@sql_developer_no1", SB(54), INK, ab, "mm")
        tx(g, 540, 1060, "follow · save · share", SN(42), DIM, g.on(1, 1.6), "mm")


SCENES = [
    ("Two tables, one question", WHITE, s_hook, [
        "Customer names are in one table. Their orders are in another.",
        "So how do you answer: *who bought what*?",
        "You *JOIN* them: you put matching rows side by side."]),
    ("Why not one big table?", RED, s_why, [
        "Why not keep everything in one big table?",
        "Because then every order repeats the customer's *name*.",
        "If Aysel changes her name, you must fix *every single order*.",
        "So the name is stored *once*, and each order keeps only a *number* that points to the person."]),
    ("Think of a coat check", ORANGE, s_ticket, [
        "It's like a coat check. You give your coat, and get a ticket: number two.",
        "Later, the number finds your coat. *Same number, same owner.*",
        "In SQL, the ticket is *customer_id*. The coats are the *customers* table. And the matching rule is written after *ON*."]),
    ("How JOIN works", CYAN, s_inner, [
        "Here is the query. The line after *ON* is the matching rule: the order's customer_id must equal the customer's id.",
        "For every order, the database takes its customer_id, and looks for the customer with the *same* id.",
        "Each match becomes one *result row*: the name, and the amount, side by side."]),
    ("Where is Leyla?", ORANGE, s_missing, [
        "But look at Leyla. She has *no orders* at all.",
        "No order points to her, so she *does not appear* in the result.",
        "A normal JOIN is an *INNER JOIN*. It keeps only rows that found a *partner*."]),
    ("LEFT JOIN keeps everyone", GREEN, s_left, [
        "Want every customer, even without orders? Use *LEFT JOIN*. It keeps *all* rows of the left table.",
        "Leyla is back. Her order columns are empty: *NULL*.",
        "Add where order id is null, and you get customers who *never* ordered."]),
    ("The dangerous mistake", RED, s_trap, [
        "Forget the matching rule, and every customer is paired with *every* order. Three times four: *twelve* rows.",
        "With real tables, that's *billions* of rows, and a very slow query.",
        "So always write the *ON* rule."]),
    ("Remember", GREEN, s_recap, [
        "Remember: JOIN puts rows side by side. ON is the rule. INNER keeps only partners. LEFT keeps everyone from the left.",
        "Next: *subqueries* from zero. A question inside a question. Follow, so you don't miss it."]),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    run(SCENES, Stage(1080, 1920, 30), "/home/claude/v2/out53", "/home/claude/en/sql_video53_EN_join.mp4", mode, seed=53, max_dur=175)

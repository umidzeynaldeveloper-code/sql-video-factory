"""52 · GROUP BY from zero (v2 style)."""
import sys
sys.path.insert(0, "/home/claude/v2")
from studio import *

ROWS = [(1, "Baku", 50), (2, "Ganja", 20), (3, "Baku", 70), (4, "Shaki", 10), (5, "Ganja", 40), (6, "Shaki", 30), (7, "Baku", 5)]
CC = {"Baku": CYAN, "Ganja": PURP, "Shaki": ORANGE}
PX = {"Baku": 210, "Ganja": 540, "Shaki": 870}
TX, TY, CW, RH = 210, 640, [120, 300, 240], 60


def orders(g, a=1.0, y=TY, **kw):
    return table(g, TX, y, ["id", "city", "amount"], ROWS, CW, RH, a, fs=32, name="orders",
                 ccol=lambda r, c: CC[ROWS[r][1]] if c == 1 else None, **kw)


def piles(g, a=1.0, y=720, fly=None, src=None):
    """three piles of receipts; fly: 0..1 progress of rows flying from the table"""
    slot = {c: 0 for c in PX}
    for i, (_, city, amt) in enumerate(ROWS):
        p1 = (PX[city], y + 90 + slot[city] * 68); slot[city] += 1
        if fly is not None and src is not None:
            r = src.row(i); p0 = ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            p = clamp((fly - i * .1) / .4); x, yy = mv(p0, p1, ease(p)); w = lerp(660, 190, ease(p))
            chip(g, x, yy, w, 54, f"{city}  {amt}" if p < .5 else str(amt), CC[city], a, 30)
        else:
            chip(g, p1[0], p1[1], 190, 54, str(amt), CC[city], a, 30)
    for city in PX: pill(g, PX[city], y, city, CC[city], a if fly is None else a * clamp(fly * 3), 32, fill=True)


# ------------------------------------------------------------------ scenes
def s_hook(g):
    cd = sql(g, 70, 330, ["SELECT city, amount", "FROM   orders", "GROUP BY city;"], g.on(0), fs=34, w=940, hl=[0] if g.b >= 1 else (), hlcol=RED)
    box(g, (70, 600, 1010, 720), RED, g.on(0, 1.4), "ORA-00979: not a GROUP BY expression", None, 32, fill=(40, 16, 26))
    if g.b >= 1:
        a = g.on(1, .2)
        icon(g, "warn", 540, 860, 110, YEL, a)
        tx(g, 540, 960, "the #1 beginner error", SB(40), YEL, a, "mm")
        tx(g, 540, 1020, "with GROUP BY", SN(34), WHITE, a, "mm")
        g.focus(cd.box, (70, 600, 1010, 720), a=g.only(1))
    if g.b >= 2:
        a = g.on(2, .3)
        box(g, (170, 1100, 910, 1220), GREEN, a, "understand GROUP BY → it disappears", None, 34)


def s_analogy(g):
    a = g.on(0)
    # a messy heap of receipts
    rnd = random.Random(4)
    heap = [(rnd.uniform(260, 820), rnd.uniform(380, 560), rnd.choice(list(CC))) for _ in range(14)]
    sort_p = g.at(1, .3, 2.6)
    tgt = {"Baku": 230, "Ganja": 540, "Shaki": 850}; cnt = {c: 0 for c in CC}
    for k, (x, y, c) in enumerate(heap):
        tx_, ty_ = tgt[c] + (cnt[c] % 2) * 40 - 20, 760 - (cnt[c]) * 26; cnt[c] += 1
        p = clamp((sort_p - k * .04) / .5) if g.b >= 1 else 0
        px, py = mv((x, y), (tx_, ty_), ease(p))
        g.d.rounded_rectangle((px - 34, py - 22, px + 34, py + 22), 6, fill=mix(WHITE, a * .9), outline=mix(CC[c], a), width=5)
    tx(g, 540, 340, "a heap of receipts", SB(34), SOFT, a * (1 - sort_p), "mm")
    if g.b >= 1:
        for c in CC:
            g.d.rounded_rectangle((tgt[c] - 120, 800, tgt[c] + 120, 830), 10, fill=mix(CC[c], g.on(1, .2) * .6))
            pill(g, tgt[c], 880, c, CC[c], g.on(1, .4), 32, fill=True)
    if g.b >= 2:
        for k, (c, n) in enumerate((("Baku", 3), ("Ganja", 2), ("Shaki", 2))):
            al = g.on(2, .4 + k * .5)
            tx(g, tgt[c], 980, f"{n} receipts", SB(32), WHITE, al, "mm")
        g.focus((80, 560, 1000, 1020), a=g.only(2))
    if g.b >= 3:
        term(g, "GROUP BY", "sort rows into piles that share a value", g.on(3, .2), y=1110, col=GREEN)


def s_piles(g):
    cd = sql(g, 70, 300, ["SELECT city, COUNT(*), SUM(amount)", "FROM   orders", "GROUP BY city;"], 1, fs=32, w=940, hl=[2])
    if g.b == 0:
        tb = orders(g, g.on(0, .3), y=560, ra=lambda i: g.on(0, .4 + i * .12))
        g.focus(cd.line(2), tb.col(1, -1), a=g.on(0, 1.8))
        callout(g, tb.col(1, -1), "same value → same pile", YEL, g.on(0, 2.2), at=(540, 1110), fs=30)
    else:
        src = Tb(TX, 560, CW, RH, 7, 6)
        fly = g.at(1, .1, 3.2) * 1.6
        ta = 1 - g.at(1, 0, .6)
        if ta > 0: orders(g, ta, y=560)
        piles(g, 1, 640, fly=fly, src=src)
        if g.b >= 2:
            g.focus((60, 600, 1020, 940), a=g.only(2))
            tx(g, 540, 1010, "7 rows  →  3 piles", XB(46), GREEN, g.on(2, .3), "mm")


AGG = [("COUNT(*)", "how many", "3"), ("SUM(amount)", "add up", "125"), ("AVG(amount)", "average", "41.7"),
       ("MIN(amount)", "smallest", "5"), ("MAX(amount)", "biggest", "70")]


def s_agg(g):
    # the Baku pile on the left, the functions on the right
    a = g.on(0)
    pill(g, 200, 330, "Baku pile", CYAN, a, 32, fill=True)
    for k, v in enumerate((50, 70, 5)): chip(g, 200, 420 + k * 72, 200, 58, str(v), CYAN, a, 32)
    for k, (fn, plain, res) in enumerate(AGG):
        y = 320 + k * 116; al = g.on(1, .2 + k * 1.05) if k else g.on(0, 1.0)
        if g.b == 0 and k > 0: al = 0
        if al <= 0: continue
        r = (360, y, 1010, y + 98)
        g.d.rounded_rectangle(r, 18, fill=mix(CARD, al), outline=mix(GREEN, al), width=3)
        tx(g, 390, y + 32, fn, MB(32), GREEN, al, "lm"); tx(g, 390, y + 72, plain, SN(26), SOFT, al, "lm")
        tx(g, 980, y + 49, res, XB(44), WHITE, al, "rm")
        cur = (g.b == 0 and k == 0) or (g.b == 1 and int(g.at(1, .2, 5.4) * 5) == k and g.at(1, .2, 5.4) < 1)
        if cur: ring(g, r, YEL, al)
    if g.b == 0: g.focus((100, 300, 300, 620), (360, 320, 1010, 418), a=g.on(0, 1.0))
    if g.b >= 2:
        term(g, "AGGREGATE", "turns many values into ONE value", g.on(2, .2), y=930, col=GREEN)
        a2 = g.on(2, 2.2)
        sql(g, 70, 1110, ["SELECT city, COUNT(*), SUM(amount)"], a2, fs=30, w=940)
        tx(g, 540, 1220, "= one line per pile", SB(34), YEL, a2, "mm")


def s_error(g):
    a = g.on(0)
    pill(g, 330, 330, "city", CYAN, a, 32, fill=True); pill(g, 750, 330, "amount", YEL, a, 32, fill=True)
    chip(g, 330, 430, 300, 70, "Baku", CYAN, a, 34, tcol=CYAN)
    cell = chip(g, 750, 430, 300, 70, "?" if g.b >= 1 else "", YEL, a, 44, tcol=YEL)
    tx(g, 540, 520, "ONE line for the whole Baku pile", SN(30), SOFT, a, "mm")
    if g.b >= 1:
        for k, v in enumerate((50, 70, 5)):
            p = g.at(1, .3 + k * .35, 1.1 + k * .35)
            x, y = mv((750 + (k - 1) * 150, 700), (750 + (k - 1) * 150, 610), ease(p))
            chip(g, x, y, 130, 56, str(v), CYAN, g.on(1, .2 + k * .35), 30)
            arrow(g, (x, y - 34), (750, 472), CYAN, g.on(1, 1.2 + k * .2), 1, 4, 14)
        tx(g, 540, 720, "three numbers · one cell", SB(36), RED, g.on(1, 2.2), "mm")
        g.focus((560, 380, 940, 700), a=g.only(1, 1))
    if g.b >= 2:
        box(g, (70, 820, 1010, 940), RED, g.on(2, .2), "Oracle refuses: ORA-00979", None, 36, fill=(40, 16, 26))
    if g.b >= 3:
        a3 = g.on(3, .2)
        tx(g, 540, 1000, "the rule", SB(30), DIM, a3, "mm")
        box(g, (70, 1040, 1010, 1180), GREEN, a3, "every column in SELECT is", "in GROUP BY  —  or inside COUNT / SUM / MIN / MAX…", 34, 28, tcol=WHITE, scol=GREEN)
        g.focus((60, 990, 1020, 1190), a=g.only(3))


def s_fix(g):
    a = g.on(0)
    sql(g, 70, 300, ["SELECT city, amount", "FROM orders GROUP BY city;"], a, fs=32, w=940, hl=[0], hlcol=RED)
    check(g, 960, 343, False, a, 26)
    if g.b >= 0:
        a1 = g.on(0, 1.2)
        tx(g, 80, 480, "Fix 1 · summarise it", SB(32), GREEN, a1)
        f1 = sql(g, 70, 510, ["SELECT city, MAX(amount)", "FROM orders GROUP BY city;"], a1, fs=32, w=940, hl=[0], hlcol=GREEN)
        check(g, 960, 553, True, a1, 26)
        if g.b == 0: g.focus(f1.box, a=a1)
    if g.b >= 1:
        a2 = g.on(1, .2)
        tx(g, 80, 690, "Fix 2 · make smaller piles", SB(32), CYAN, a2)
        f2 = sql(g, 70, 720, ["SELECT city, amount", "FROM orders GROUP BY city, amount;"], a2, fs=32, w=940, hl=[1], hlcol=CYAN)
        check(g, 960, 763, True, a2, 26)
        tx(g, 540, 900, "Baku 50 · Baku 70 · Baku 5  →  each its own pile", SN(30), SOFT, g.on(1, 2.2), "mm")
        if g.b == 1: g.focus(f2.box, (60, 870, 1020, 930), a=a2)
    if g.b >= 2:
        a3 = g.on(2, .2)
        box(g, (70, 990, 1010, 1130), YEL, a3, "Which one?", "ask: what ONE value do I want per pile?", 40, 30, scol=WHITE)
        g.focus((60, 980, 1020, 1140), a=a3)


def s_two(g):
    data = [("Baku", 2025, 50), ("Baku", 2026, 70), ("Baku", 2026, 5), ("Ganja", 2025, 20), ("Ganja", 2026, 40)]
    sql(g, 70, 300, ["SELECT city, year, SUM(amount)", "FROM   orders", "GROUP BY city, year;"], 1, fs=32, w=940, hl=[2])
    tb = table(g, 150, 560, ["city", "year", "amount"], data, [280, 260, 240], 58, g.on(0, .4), fs=30,
               ccol=lambda r, c: CC[data[r][0]] if c == 0 else (YEL if c == 1 else None), hlc=[1] if g.b >= 1 else ())
    if g.b >= 1:
        res = [("Baku", 2025, 50), ("Baku", 2026, 75), ("Ganja", 2025, 20), ("Ganja", 2026, 40)]
        a = g.on(1, .6)
        arrow(g, (540, tb.bottom + 10), (540, tb.bottom + 70), GREEN, a, g.at(1, .6, 1.1), 6)
        rt = table(g, 150, tb.bottom + 90, ["city", "year", "SUM"], res, [280, 260, 240], 58, a, fs=30, col=GREEN,
                   ccol=lambda r, c: CC[res[r][0]] if c == 0 else None, hl=[1] if g.b >= 1 else ())
        callout(g, rt.row(1), "70 + 5 = 75", YEL, g.on(1, 2.4), at=(880, rt.row(1)[1] - 50), fs=30, mark=False)
        g.focus(tb.box, rt.box, a=g.only(1))
    if g.b >= 2:
        tx(g, 540, 1380, "one pile for every city + year pair", SB(32), YEL, g.on(2, .2), "mm")


def s_count(g):
    data = [("Baku", 50, "SALE10"), ("Baku", 70, "—"), ("Baku", 5, "—")]
    tb = table(g, 120, 360, ["city", "amount", "coupon"], data, [260, 240, 340], 62, g.on(0), fs=32,
               ccol=lambda r, c: CYAN if c == 0 else (DIM if data[r][2] == "—" and c == 2 else None))
    if g.b >= 0:
        l = callout(g, tb.cell(1, 2), "empty = NULL", PINK, g.on(0, 1.2), at=(760, 650), fs=28, mark=False)
    a = g.on(1)
    if a > 0:
        r1 = box(g, (70, 760, 520, 960), GREEN, a, "COUNT(*)", "counts ROWS → 3", 40, 32, scol=WHITE)
        r2 = box(g, (560, 760, 1010, 960), PINK, g.on(1, 2.6), "COUNT(coupon)", "counts VALUES → 1", 40, 32, scol=WHITE)
        g.focus(r1, r2, tb.col(2, -1), a=g.only(1))
    if g.b >= 2:
        box(g, (70, 1030, 1010, 1150), YEL, g.on(2, .2), "NULLs are skipped by SUM, AVG, COUNT(col)", None, 32)


WORDS = [("GROUP BY", "rows into piles"), ("COUNT / SUM", "one value per pile"), ("SELECT", "only grouped or summarised"), ("ORA-00979", "a column with many values"), ("COUNT(col)", "skips NULLs")]


def s_recap(g):
    la = g.until(0)
    for k, (kw, plain) in enumerate(WORDS):
        if la <= 0: break
        y = 340 + k * 150; lit = pr(g.bt, .9 + k * .9, 1.2 + k * .9)
        col = [GREEN, CYAN, PURP, RED, PINK][k]
        g.d.rounded_rectangle((70, y, 1010, y + 126), 22, fill=mix(CARD, la), outline=mix(col, la * (.25 + .75 * lit)), width=3)
        badge(g, 140, y + 63, k + 1, col, la * (.3 + .7 * lit), 34)
        tx(g, 210, y + 63, kw, MB(36), col, la * (.3 + .7 * lit), "lm")
        tx(g, 980, y + 63, plain, SN(32), WHITE, la * lit, "rm")
    if g.b == 1:
        tx(g, 540, 520, "Next video", SB(48), DIM, g.on(1, .2), "mm")
        tx(g, 540, 620, "JOIN from zero", XB(76), YEL, g.on(1, .5), "mm")
        tx(g, 540, 720, "how two tables meet", SN(38), WHITE, g.on(1, .8), "mm")
        p = 1 + .04 * math.sin(g.t * 7); bw, bh = 760 * p, 130 * p; ab = g.on(1, 1.2)
        g.d.rounded_rectangle((540 - bw / 2, 920 - bh / 2, 540 + bw / 2, 920 + bh / 2), 65, fill=mix(GREEN, ab))
        tx(g, 540, 920, "@sql_developer_no1", SB(54), INK, ab, "mm")
        tx(g, 540, 1060, "follow · save · share", SN(42), DIM, g.on(1, 1.6), "mm")


SCENES = [
    ("The #1 GROUP BY error", RED, s_hook, [
        "This query looks fine. But it *fails* with an error.",
        "It is the most common mistake people make with *GROUP BY*.",
        "Once you understand what GROUP BY really does, this error *disappears forever*."]),
    ("Think of sorting receipts", ORANGE, s_analogy, [
        "Imagine a messy heap of receipts from three cities.",
        "To understand them, you first *sort* them into piles: one pile per city.",
        "Now it's easy: Baku has three receipts, Ganja two, Shaki two.",
        "That sorting is exactly what *GROUP BY* does."]),
    ("Rows become piles", PURP, s_piles, [
        "Here is the table. GROUP BY city looks at the *city* column of every row.",
        "Rows with the *same city* fly into the *same pile*.",
        "Seven rows became *three piles*. Now we can ask questions about each pile."]),
    ("One answer per pile", GREEN, s_agg, [
        "Take the Baku pile. *COUNT* asks: how many receipts? Three.",
        "*SUM* adds them up: one hundred twenty five. *AVG* gives the average. *MIN* and *MAX*: the smallest and the biggest.",
        "These are called *aggregate* functions. Each turns a whole pile into *one* number."]),
    ("Now the error makes sense", RED, s_error, [
        "After grouping, every pile becomes *one line*. So Baku gets one line.",
        "But we asked for *amount*. Baku has three amounts: fifty, seventy, and five. Which one goes in the single cell?",
        "Oracle can't choose for you, so it *refuses*.",
        "The rule: every column in SELECT must be in *GROUP BY*, or inside a function like *SUM* or *MAX*."]),
    ("Two ways to fix it", GREEN, s_fix, [
        "Fix one: *summarise* it. MAX of amount gives one value per pile: the biggest.",
        "Fix two: add amount to GROUP BY. Then every city and amount pair becomes its *own* pile.",
        "To choose, ask yourself: what *one* value do I want for each pile?"]),
    ("Grouping by two columns", CYAN, s_two, [
        "You can group by *more than one* column. Here: city *and* year.",
        "Now each pile is one city in one year. Baku in twenty twenty six: seventy plus five, *seventy five*.",
        "More columns in GROUP BY means *smaller* piles."]),
    ("COUNT(*) vs COUNT(column)", PINK, s_count, [
        "One last trap. Only one Baku order used a coupon. The other cells are empty: *NULL*.",
        "*COUNT star* counts rows: three. *COUNT coupon* counts only filled values: one.",
        "SUM, AVG and COUNT of a column all *skip* the NULLs."]),
    ("Remember", GREEN, s_recap, [
        "Remember: GROUP BY makes piles. Aggregates give one value per pile. Everything else in SELECT must be grouped or summarised.",
        "Next: *JOIN* from zero. How two tables meet. Follow, so you don't miss it."]),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    run(SCENES, Stage(1080, 1920, 30), "/home/claude/v2/out52", "/home/claude/en/sql_video52_EN_group_by.mp4", mode, seed=52, max_dur=175)

"""56 · Indexes from zero (v2 style)."""
import sys
sys.path.insert(0, "/home/claude/v2")
from studio import *


def blocks(g, x0, y0, cols, rows, s, a, scanned=-1, hit=None, col=CYAN):
    k = 0
    for r in range(rows):
        for c in range(cols):
            x = x0 + c * (s + 8); y = y0 + r * (s + 8)
            if k == hit: fc, oc = mix(GREEN, .7, CARD), GREEN
            elif k <= scanned: fc, oc = mix(RED, .25, CARD), mix(RED, .7, CARD)
            else: fc, oc = CARD, OFFB
            g.d.rounded_rectangle((x, y, x + s, y + s), 6, fill=mix(fc, a), outline=mix(oc, a), width=2)
            k += 1


# ------------------------------------------------------------------ scenes
def s_hook(g):
    q = sql(g, 70, 310, ["SELECT * FROM customers", "WHERE  phone = '055 123 45 67';"], 1, fs=32, w=940)
    a = g.on(0, .8)
    box(g, (70, 520, 520, 700), RED, a, "4.2 s", "1 000 000 rows read", 64, 28, scol=WHITE)
    box(g, (560, 520, 1010, 700), GREEN, g.on(1, .4), "0.01 s", "4 small reads", 64, 28, scol=WHITE)
    if g.b >= 1:
        tx(g, 540, 760, "same query · same data", SB(34), SOFT, g.on(1, 1.4), "mm")
    if g.b >= 2:
        pill(g, 540, 860, "the difference: an INDEX", YEL, g.on(2, .3), 40, fill=True)


def s_book(g):
    a = g.on(0)
    # a thick book
    bx = (140, 330, 520, 760)
    for k in range(6): g.d.rounded_rectangle((bx[0] + k * 6, bx[1] + k * 6, bx[2] + k * 6, bx[3] + k * 6), 10, fill=mix((230, 228, 220), a), outline=mix((160, 160, 170), a))
    g.d.rounded_rectangle(bx, 10, fill=mix(mix(ORANGE, .8, CARD), a), outline=mix(ORANGE, a), width=3)
    tx(g, 330, 500, "ORACLE", XB(44), INK, a, "mm"); tx(g, 330, 560, "900 pages", SB(30), INK, a, "mm")
    tx(g, 780, 380, "find: \"deadlock\"", SB(34), WHITE, a, "mm")
    if g.b >= 1:
        p = g.at(1, .3, 3.5)
        tx(g, 780, 470, f"page {int(1 + 899 * p)} / 900", MB(36), RED, g.on(1, .2), "mm")
        hbar(g, 600, 520, 360, 26, p, RED, g.on(1, .2))
        tx(g, 780, 600, "read EVERY page", SB(32), RED, g.on(1, 1.2), "mm")
    if g.b >= 2:
        a2 = g.on(2, .2)
        ir = (570, 680, 1000, 1010)
        g.d.rounded_rectangle(ir, 14, fill=mix((236, 238, 244), a2), outline=mix(YEL, a2), width=4)
        tx(g, 785, 715, "INDEX (back of the book)", SB(24), INK, a2, "mm")
        for k, (w, pg) in enumerate((("commit", "212"), ("cursor", "305"), ("deadlock", "418"), ("deferred", "421"), ("delete", "97"))):
            y = 770 + k * 46; hl_ = k == 2 and g.at(2, 2.0, 2.4) > 0
            if hl_: g.d.rounded_rectangle((590, y - 20, 980, y + 20), 8, fill=mix(mix(YEL, .5, (236, 238, 244)), a2, (236, 238, 244)))
            tx(g, 610, y, w, MN(28), INK, a2, "lm"); tx(g, 960, y, pg, MB(28), INK, a2, "rm")
        g.focus(ir, a=g.only(2))
    if g.b >= 3:
        box(g, (70, 1060, 1010, 1180), GREEN, g.on(3, .2), "sorted words + page numbers → jump straight there", None, 30)


def s_scan(g):
    q = sql(g, 70, 300, ["WHERE phone = '055 123 45 67'"], 1, fs=32, w=940)
    sc = int(g.at(0, .6, g.bl - .3) * 159) if g.b == 0 else 159
    blocks(g, 95, 440, 16, 10, 48, 1, scanned=sc, hit=157 if sc >= 157 else None)
    tx(g, 540, 1045, f"blocks read: {sc + 1}", MB(34), RED, 1, "mm")
    if g.b >= 1:
        term(g, "FULL TABLE SCAN", "read every row, from first to last", g.on(1, .2), y=1110, col=RED)


ENTRIES = [("050 111 22 33", "row 812"), ("051 404 10 10", "row 37"), ("055 123 45 67", "row 99 041"), ("055 990 00 01", "row 5"), ("070 222 33 44", "row 61 200")]


def s_what(g):
    sql(g, 70, 300, ["CREATE INDEX cust_phone_ix ON customers(phone);"], g.on(0), fs=28, w=940)
    a = g.on(1, .2)
    if a > 0:
        tb = table(g, 120, 520, ["phone (sorted)", "where is the row?"], ENTRIES, [440, 400], 64, a, fs=30, col=YEL, name="cust_phone_ix",
                   ra=lambda i: g.on(1, .4 + i * .2), hl=[2] if g.b >= 2 else ())
        if g.b >= 2:
            callout(g, tb.cell(2, 1), "ROWID = the row's address", GREEN, g.on(2, .6), at=(540, tb.bottom + 70), fs=30, mark=False)
    if g.b >= 3:
        term(g, "INDEX", "a sorted copy of one column + the address of each row", g.on(3, .2), y=1080, col=YEL)


def s_tree(g):
    a = g.on(0)
    root = box(g, (390, 320, 690, 420), YEL, a, "050 … 099", None, 32)
    br = [(120, 530, 420, 620, "050 … 059"), (660, 530, 960, 620, "060 … 099")]
    for k, (x0, y0, x1, y1, s) in enumerate(br):
        al = g.on(0, .5 + k * .2); box(g, (x0, y0, x1, y1), CYAN, al, s, None, 30)
        arrow(g, (540, 420), ((x0 + x1) / 2, y0), CYAN if k == 0 else OFFB, al, 1, 4, 14)
    lv = [(40, 740, 330, 830, "050 – 054"), (360, 740, 650, 830, "055 – 059")]
    for k, (x0, y0, x1, y1, s) in enumerate(lv):
        al = g.on(0, 1 + k * .2); box(g, (x0, y0, x1, y1), GREEN, al, s, None, 30)
        arrow(g, (270, 620), ((x0 + x1) / 2, y0), GREEN if k == 1 else OFFB, al, 1, 4, 14)
    tx(g, 830, 785, "… more leaves", SN(28), DIM, g.on(0, 1.4), "mm")
    if g.b >= 1:
        hop = g.at(1, .3, 3.6)
        segs = [((540, 422), (270, 528)), ((270, 622), (505, 738)), ((505, 832), (540, 918))]
        for j, (p0, p1) in enumerate(segs):
            f = clamp(hop * 3 - j)
            if f > 0: arrow(g, p0, p1, YEL, 1, f, 6, 18)
            if 0 < f < 1:
                x, y = mv(p0, p1, f); g.d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=YEL)
        box(g, (330, 920, 750, 1010), PURP, g.on(1, 3.2), "row 99 041 in the table", None, 30)
    if g.b >= 2:
        box(g, (70, 1060, 1010, 1180), GREEN, g.on(2, .2), "1 000 000 rows → only 3 or 4 jumps", "the tree stays short, even when the table grows", 36, 26, scol=WHITE)


def s_cost(g):
    a = g.on(0)
    sql(g, 70, 300, ["INSERT INTO customers VALUES (...);"], a, fs=30, w=940)
    box(g, (70, 440, 520, 580), CYAN, g.on(0, .8), "write the row", "in the table", 34, 26, scol=WHITE)
    for k in range(3):
        box(g, (560, 440 + k * 120, 1010, 540 + k * 120), YEL, g.on(0, 1.4 + k * .5), f"update index {k + 1}", None, 30)
    if g.b >= 1:
        hbar(g, 120, 880, 840, 40, .35, GREEN, g.on(1, .2), "SELECT", "faster")
        hbar(g, 120, 990, 840, 40, .8, RED, g.on(1, .9), "INSERT / UPDATE / DELETE", "slower")
    if g.b >= 2:
        box(g, (70, 1080, 1010, 1200), YEL, g.on(2, .2), "index the columns you SEARCH by — not every column", None, 30)


def s_ignored(g):
    q = sql(g, 70, 300, ["WHERE UPPER(name) = 'AYSEL'"], 1, fs=34, w=940, hl=[0] if g.b <= 1 else (), hlcol=RED)
    a = g.on(0, .6)
    box(g, (70, 450, 520, 600), CYAN, a, "index is sorted by", "name: Aysel, Leyla…", 32, 30, scol=WHITE)
    box(g, (560, 450, 1010, 600), RED, g.on(0, 1.6), "you search by", "UPPER(name): AYSEL", 32, 30, scol=WHITE)
    if g.b >= 1:
        box(g, (70, 650, 1010, 760), RED, g.on(1, .2), "different value → index can't help → full scan", None, 30)
        f = sql(g, 70, 800, ["WHERE name = 'Aysel'      -- index works"], g.on(1, 1.6), fs=30, w=940, hl=[0], hlcol=GREEN)
    if g.b >= 2:
        box(g, (70, 960, 1010, 1100), YEL, g.on(2, .2), "returning most of the table?", "a full scan is faster — Oracle chooses it", 34, 28, scol=WHITE)


WORDS = [("index", "sorted column + row address"), ("ROWID", "where the row lives"), ("full scan", "read everything"),
         ("B-tree", "3–4 jumps to any row"), ("cost", "slower writes, more space"), ("UPPER(col)", "normal index not used")]


def s_recap(g):
    la = g.until(0)
    for k, (kw, plain) in enumerate(WORDS):
        if la <= 0: break
        y = 330 + k * 140; lit = pr(g.bt, .8 + k * .85, 1.1 + k * .85)
        col = [YEL, GREEN, RED, CYAN, ORANGE, PINK][k]
        g.d.rounded_rectangle((70, y, 1010, y + 118), 22, fill=mix(CARD, la), outline=mix(col, la * (.25 + .75 * lit)), width=3)
        badge(g, 140, y + 59, k + 1, col, la * (.3 + .7 * lit), 32)
        tx(g, 205, y + 59, kw, MB(32), col, la * (.3 + .7 * lit), "lm")
        tx(g, 985, y + 59, plain, SN(30), WHITE, la * lit, "rm")
    if g.b == 1:
        tx(g, 540, 520, "Next video", SB(48), DIM, g.on(1, .2), "mm")
        tx(g, 540, 620, "Execution plans", XB(72), YEL, g.on(1, .5), "mm")
        tx(g, 540, 720, "see what the database really does", SN(38), WHITE, g.on(1, .8), "mm")
        p = 1 + .04 * math.sin(g.t * 7); bw, bh = 760 * p, 130 * p; ab = g.on(1, 1.2)
        g.d.rounded_rectangle((540 - bw / 2, 920 - bh / 2, 540 + bw / 2, 920 + bh / 2), 65, fill=mix(GREEN, ab))
        tx(g, 540, 920, "@sql_developer_no1", SB(54), INK, ab, "mm")
        tx(g, 540, 1060, "follow · save · share", SN(42), DIM, g.on(1, 1.6), "mm")


SCENES = [
    ("4 seconds or 0.01?", WHITE, s_hook, [
        "Find one customer by phone number. Without help, it takes *four seconds*.",
        "With help, *one hundredth* of a second. Same query, same data.",
        "The difference is an *index*. Let's build one in our heads."]),
    ("Think of a book", ORANGE, s_book, [
        "You need the word *deadlock* in a nine hundred page book.",
        "You could read *every page*, from the first to the last. That takes hours.",
        "Or you open the *index* at the back. Words are sorted, so you find deadlock instantly: page four eighteen.",
        "Sorted words, plus page numbers. You *jump* straight to the right page."]),
    ("Without an index", RED, s_scan, [
        "Without an index, the database does the same as reading every page. It reads *every block* of the table.",
        "That's called a *full table scan*."]),
    ("What an index is", YEL, s_what, [
        "So we create an index on the phone column.",
        "Inside, it keeps every phone number, *sorted*, like the words at the back of a book.",
        "Next to each number: the *address* of its row in the table. That address is called the *ROWID*.",
        "So an index is a sorted copy of one column, plus the address of each row."]),
    ("How it finds a row so fast", CYAN, s_tree, [
        "The sorted list is stored as a small *tree*. The top says which way to go, like a signpost.",
        "Our number starts with zero five five. Go left. Then to the right leaf. Then straight to the row.",
        "Even with a million rows, it takes only *three or four* jumps. This tree is called a *B-tree*."]),
    ("Indexes are not free", ORANGE, s_cost, [
        "But every new row must also be written into *every index* of the table.",
        "So indexes make searching *faster*, but inserts, updates and deletes *slower*. And they need space.",
        "Index the columns you *search by*. Not every column."]),
    ("When the index is ignored", PINK, s_ignored, [
        "One common surprise. The index is sorted by *name*. But here we search by *UPPER* of name.",
        "That's a *different* value, so the index can't help, and the database scans the whole table. Search by the column itself.",
        "And if a query returns *most* of the table, a full scan is simply faster. Oracle knows this, and chooses it."]),
    ("Remember", GREEN, s_recap, [
        "Remember: an index is a sorted column plus row addresses. A B-tree finds any row in a few jumps. It costs space and slower writes. And a function on the column hides it.",
        "Next: *execution plans*. See what the database really does. Follow, so you don't miss it."]),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    run(SCENES, Stage(1080, 1920, 30), "/home/claude/v2/out56", "/home/claude/en/sql_video56_EN_indexes.mp4", mode, seed=56, max_dur=175)

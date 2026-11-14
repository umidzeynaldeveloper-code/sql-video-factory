"""Long video 3 (16:9): What happens when you run a SELECT — parse, optimize, execute, fetch. Beginner-first, v2 style."""
import sys
sys.path.insert(0, "/home/claude/v2")
from studio import *

W_, H_ = 1920, 1080
Q = ["SELECT name", "FROM   customers", "WHERE  city = 'Baku';"]
STAGES = [("PARSE", "check & understand", CYAN), ("OPTIMIZE", "choose the best way", YEL), ("EXECUTE", "do the work", GREEN), ("FETCH", "send the rows", PINK)]


def pipeline(g, y, a=1.0, cur=-1, lit=None, small=False):
    """the 4-stage pipeline strip; cur = highlighted stage"""
    n = 4; w = 340 if not small else 300; gap = 70; x0 = (W_ - (n * w + (n - 1) * gap)) / 2; h = 120 if not small else 90
    rects = []
    for k, (nm, sub, col) in enumerate(STAGES):
        al = a * (lit(k) if lit else 1.0)
        x = x0 + k * (w + gap); r = (x, y, x + w, y + h); rects.append(r)
        on = cur < 0 or k == cur
        box(g, r, col if on else OFFB, al * (1 if on else .7), nm, sub, 40 if not small else 32, 26 if not small else 22, scol=WHITE if on else DIM, tcol=col if on else DIM)
        if k == cur: ring(g, r, col, al)
        if k < n - 1: arrow(g, (x + w + 8, y + h / 2), (x + w + gap - 8, y + h / 2), WHITE if on else OFFB, al, 1, 5, 16)
    return rects


def stage_strip(g, k):
    return pipeline(g, 215, 1, cur=k, small=True)


# ------------------------------------------------------------------ chapters
def c_intro(g):
    cd = sql(g, 560, 230, Q, g.on(0), fs=44, w=800)
    if g.b >= 0:
        k = g.at(0, 2.0, 2.6)
        pill(g, 960, 520, "ENTER  ↵", GREEN, k, 40, fill=True)
    if g.b >= 1:
        box(g, (610, 600, 1310, 760), YEL, g.on(1, .2), "0.01 seconds later: the answer", "but what happened in between?", 44, 32, scol=WHITE)
    if g.b >= 2:
        pipeline(g, 775, 1, lit=lambda k: g.on(2, .4 + k * .6))


def c_restaurant(g):
    a = g.on(0)
    person(g, 260, 470, 230, CYAN, a, "you", 30)
    note = (430, 330, 760, 560)
    g.d.rounded_rectangle(note, 14, fill=mix((236, 238, 244), a), outline=mix(YEL, a), width=3)
    tx(g, 595, 365, "ORDER", SB(26), INK, a, "mm")
    for k, s_ in enumerate(("1 × plov", "no onion", "table 7")): tx(g, 460, 410 + k * 46, s_, MN(30), INK, a)
    if g.b >= 1:
        steps = [("waiter", "reads & checks the order", CYAN), ("head chef", "plans how to cook", YEL), ("cooks", "follow the plan", GREEN), ("plates", "come out to you", PINK)]
        for k, (nm, sub, col) in enumerate(steps):
            al = g.on(1, .3 + k * 1.1) if g.b == 1 else 1
            x = 840 + (k % 2) * 520; y = 300 + (k // 2) * 220
            box(g, (x, y, x + 480, y + 180), col, al, nm, sub, 42, 28, scol=WHITE)
            badge(g, x + 40, y + 40, k + 1, col, al, 26)
    if g.b >= 2:
        vs = [("waiter", "PARSE"), ("head chef", "OPTIMIZE"), ("cooks", "EXECUTE"), ("plates", "FETCH")]
        for k, (l, r_) in enumerate(vs):
            al = g.on(2, .3 + k * .45)
            x = 840 + (k % 2) * 520; y = 300 + (k // 2) * 220
            pill(g, x + 380, y + 34, r_, STAGES[k][2], al, 24, fill=True)


def c_syntax(g):
    stage_strip(g, 0)
    if g.b <= 1:
        cd = sql(g, 480, 380, ["SELECT name", "FORM   customers;"], 1, fs=44, w=960, hl=[1] if g.b >= 1 else (), hlcol=RED)
        if g.b >= 1:
            box(g, (480, 600, 1440, 720), RED, g.on(1, .4), "ORA-00923: FROM keyword not found where expected", None, 34, fill=(40, 16, 26))
            callout(g, (cd.line(1)[0] + 20, cd.line(1)[1], cd.line(1)[0] + 260, cd.line(1)[3]), "a typo: FORM", RED, g.on(1, 1.2), at=(300, 520), fs=30, mark=True)
    else:
        term(g, "SYNTAX", "the grammar of SQL: right words, right order", g.on(2, .2), y=480, col=CYAN)


def c_semantic(g):
    stage_strip(g, 0)
    rows = [("Does the table exist?", "customers", "ORA-00942: table or view does not exist"),
            ("Do the columns exist?", "name, city", "ORA-00904: invalid identifier"),
            ("Are you allowed to read it?", "privileges", "no rights → also ORA-00942")]
    for k, (q_, what, err) in enumerate(rows):
        al = g.on(0, .4 + k * .9) if g.b == 0 else 1
        y = 390 + k * 150
        g.d.rounded_rectangle((200, y, 1720, y + 124), 20, fill=mix(CARD, al), outline=mix(CYAN, al), width=3)
        badge(g, 260, y + 62, k + 1, CYAN, al, 28)
        tx(g, 320, y + 40, q_, SB(36), WHITE, al, "lm"); tx(g, 320, y + 88, what, MN(28), SOFT, al, "lm")
        if g.b >= 1: tx(g, 1690, y + 62, err, MN(26), RED, g.on(1, .3 + k * .5), "rm")
        else: check(g, 1660, y + 62, True, g.on(0, 1 + k * .9), 28)
    if g.b >= 2:
        g.focus((190, 380, 1730, 840), a=g.only(2))


def c_shared(g):
    stage_strip(g, 0)
    a = g.on(0)
    # the shared pool shelf with recipe cards
    shelf = (980, 380, 1720, 820)
    box(g, shelf, PURP, a, None, None, fill=(16, 22, 44))
    tx(g, 1350, 410, "SHARED POOL · plans already made", SB(28), PURP, a, "mm")
    cards = ["SELECT name FROM customers WHERE city = 'Baku'", "SELECT * FROM orders WHERE id = :id", "UPDATE accounts SET …"]
    for k, c_ in enumerate(cards):
        al = g.on(0, .6 + k * .3); y = 470 + k * 110
        chip(g, 1350, y + 40, 680, 84, c_, PURP if k else YEL, al, 24, tcol=WHITE)
    sql(g, 160, 420, Q, a, fs=34, w=700)
    if g.b >= 1:
        p = g.at(1, .4, 1.6)
        path(g, [(860, 500), (1000, 510)], YEL, g.on(1, .2), p, 6, 18)
        ring(g, (1010, 470, 1690, 554), YEL, g.on(1, 1.6))
        pill(g, 510, 720, "SOFT PARSE · found it, reuse", GREEN, g.on(1, 2.0), 32, fill=True)
    if g.b >= 2:
        pill(g, 510, 800, "HARD PARSE · new, plan it", RED, g.on(2, .3), 32, fill=True)
    if g.b >= 3:
        g.focus((180, 680, 840, 840), a=g.only(3))


def c_optimizer(g):
    stage_strip(g, 1)
    a = g.on(0)
    opts = [("Plan A", "read the whole table", "1 000 000 rows", 900, RED), ("Plan B", "use the index on city", "4 jumps + 12 500 rows", 40, GREEN)]
    for k, (nm, how, cost, c_, col) in enumerate(opts):
        al = g.on(0, .4 + k * 1.3) if g.b == 0 else 1
        x = 200 + k * 800; r = (x, 400, x + 720, 620)
        box(g, r, col if g.b >= 2 else OFFB, al, None, None)
        tx(g, x + 40, 450, nm, XB(44), col, al, "lm"); tx(g, x + 40, 520, how, SN(34), WHITE, al, "lm"); tx(g, x + 40, 575, cost, MN(28), SOFT, al, "lm")
        if g.b >= 2:
            hbar(g, x + 40, 700, 640, 34, c_ / 900, col, g.on(2, .3 + k * .5), "estimated cost", str(c_))
    if g.b >= 2:
        icon(g, "star", 1560, 450, 60, YEL, g.on(2, 2.0))
    if g.b >= 3:
        term(g, "OPTIMIZER", "the part of Oracle that picks the cheapest plan", g.on(3, .2), y=740, col=YEL)


def c_stats(g):
    stage_strip(g, 1)
    a = g.on(0)
    note = (200, 380, 900, 780)
    box(g, note, YEL, a, None, None)
    tx(g, 550, 420, "STATISTICS · notes about the data", SB(30), YEL, a, "mm")
    facts = [("rows in customers", "1 000 000"), ("different cities", "80"), ("rows per city ≈", "12 500"), ("index on city", "yes")]
    for k, (l, v) in enumerate(facts):
        al = g.on(0, .5 + k * .5); y = 490 + k * 66
        tx(g, 240, y, l, SN(32), WHITE, al, "lm"); tx(g, 860, y, v, MB(32), YEL, al, "rm")
    if g.b >= 1:
        box(g, (1000, 380, 1720, 560), RED, g.on(1, .3), "old or missing statistics", "→ wrong guess → slow plan", 36, 30, scol=WHITE)
    if g.b >= 2:
        box(g, (1000, 600, 1720, 780), GREEN, g.on(2, .3), "keep statistics fresh", "Oracle gathers them every night", 36, 30, scol=WHITE)


PLAN = [("SELECT STATEMENT", 0), ("TABLE ACCESS BY INDEX ROWID  customers", 1), ("INDEX RANGE SCAN  cust_city_ix", 2)]


def c_plan(g):
    stage_strip(g, 2)
    a = g.on(0)
    x0, y0 = 220, 350
    for k, (op, ind) in enumerate(PLAN):
        al = g.on(0, .4 + k * .5)
        r = (x0 + ind * 90, y0 + k * 120, x0 + ind * 90 + 980, y0 + k * 120 + 92)
        lit_ = g.b >= 1 and ((k == 2 and g.at(1, .5, 1.0) > 0) or (k == 1 and g.at(1, 2.6, 3.0) > 0) or (k == 0 and g.at(1, 4.4, 4.8) > 0))
        box(g, r, GREEN if lit_ else CYAN, al, None, None, glow=lit_)
        tx(g, r[0] + 30, (r[1] + r[3]) / 2, op, MB(32), GREEN if lit_ else WHITE, al, "lm")
        badge(g, r[0] - 34, (r[1] + r[3]) / 2, 3 - k, GREEN if lit_ else DIM, al if g.b >= 1 else 0, 22)
    if g.b >= 1:
        for k in (2, 1):
            p = g.at(1, 1.4 if k == 2 else 3.4, 2.2 if k == 2 else 4.2)
            r0y = y0 + k * 120 + 46; r1y = y0 + (k - 1) * 120 + 46
            path(g, [(x0 + k * 90 + 1000, r0y), (x0 + k * 90 + 1060, r0y), (x0 + (k - 1) * 90 + 1060, r1y), (x0 + (k - 1) * 90 + 1000, r1y)], YEL, 1, p, 5, 16)
        tx(g, 1580, 450, "rows flow UP", SB(32), YEL, g.on(1, 4.0), "mm")
    if g.b >= 2:
        term(g, "EXECUTION PLAN", "the recipe: which steps, in which order", g.on(2, .2), y=730, col=GREEN)


def c_cache(g):
    stage_strip(g, 2)
    a = g.on(0)
    cyl(g, 1480, 600, 300, 300, CYAN, a, "DISK", "slow · huge", 36)
    mem = (300, 420, 1000, 780); box(g, mem, GREEN, a, None, None, fill=(16, 26, 40))
    tx(g, 650, 450, "BUFFER CACHE · memory", SB(30), GREEN, a, "mm")
    for k in range(12):
        x = 340 + (k % 6) * 106; y = 500 + (k // 6) * 120
        filled = g.b >= 1 and k < 5 and g.at(1, .5 + k * .4, .9 + k * .4) > 0
        chip(g, x + 45, y + 45, 90, 90, "", GREEN if filled else OFFB, a, 20, fill=mix(GREEN, .45, CARD) if filled else CARD)
    if g.b >= 1:
        p = g.at(1, .5, 2.5)
        for k in range(5):
            f = clamp(p * 5 - k)
            if 0 < f < 1:
                x, y = mv((1330, 600), (385 + k * 106, 545), ease(f)); g.d.rounded_rectangle((x - 30, y - 30, x + 30, y + 30), 8, fill=mix(GREEN, 1))
        pill(g, 650, 840, "1st time: from disk (slow)", RED, g.on(1, 2.6), 28)
    if g.b >= 2:
        pill(g, 1480, 840, "next time: from memory (fast)", GREEN, g.on(2, .3), 28, fill=True)


def c_fetch(g):
    stage_strip(g, 3)
    a = g.on(0)
    cyl(g, 330, 560, 280, 280, CYAN, a, "Oracle", "has 12 500 rows", 34)
    person(g, 1600, 590, 220, ORANGE, a, "your app", 30)
    if g.b >= 0:
        p = (g.t * .45) % 1 if g.b >= 1 else g.at(0, 1.0, 3.0)
        for k in range(3):
            f = (p + k / 3) % 1 if g.b >= 1 else clamp(p * 3 - k)
            if f <= 0: continue
            x, y = mv((520, 560), (1440, 560), f)
            g.d.rounded_rectangle((x - 70, y - 40, x + 70, y + 40), 12, fill=mix(PINK, .5 * a, CARD), outline=mix(PINK, a), width=3)
            tx(g, x, y, "100 rows", SB(24), WHITE, a, "mm")
    if g.b >= 1:
        box(g, (560, 720, 1360, 840), PINK, g.on(1, .3), "rows travel in batches", "the first rows can arrive before the last are found", 34, 26, scol=WHITE)
    if g.b >= 2:
        g.focus((560, 720, 1360, 840), a=g.only(2))


def c_binds(g):
    a = g.on(0)
    lits = ["WHERE id = 101", "WHERE id = 102", "WHERE id = 103", "WHERE id = 104"]
    for k, s_ in enumerate(lits):
        al = g.on(0, .3 + k * .3)
        sql(g, 160, 260 + k * 100, [s_], al, fs=32, w=620)
        pill(g, 900, 300 + k * 100, "HARD PARSE", RED, al, 24)
    if g.b >= 1:
        sql(g, 1060, 260, ["WHERE id = :id"], g.on(1, .2), fs=40, w=640)
        tx(g, 1380, 400, "values 101, 102, 103 … plug in", SN(30), WHITE, g.on(1, .9), "mm")
        pill(g, 1380, 480, "1 hard parse, then reuse", GREEN, g.on(1, 1.6), 30, fill=True)
    if g.b >= 2:
        term(g, "BIND VARIABLE", "a placeholder like :id — same text, new value", g.on(2, .2), y=640, col=GREEN)


RECAP = [("PARSE", "grammar · names · rights · plan already made?", CYAN), ("OPTIMIZE", "compare plans · use statistics · pick cheapest", YEL),
         ("EXECUTE", "follow the plan · blocks from memory or disk", GREEN), ("FETCH", "rows travel to you in batches", PINK)]


def c_recap(g):
    if g.b <= 1:
        for k, (nm, s_, col) in enumerate(RECAP):
            al = g.on(0, .4 + k * 1.4) if g.b == 0 else 1
            y = 230 + k * 150
            g.d.rounded_rectangle((260, y, 1660, y + 124), 22, fill=mix(CARD, al), outline=mix(col, al), width=3)
            badge(g, 330, y + 62, k + 1, col, al, 32)
            tx(g, 400, y + 62, nm, XB(44), col, al, "lm"); tx(g, 1620, y + 62, s_, SN(32), WHITE, al, "rm")
    else:
        tx(g, 960, 260, "Every stage has its own short on the channel", SB(48), WHITE, g.on(2, .2), "mm")
        tx(g, 960, 340, "playlist: SQL Basics · Oracle Performance", SN(36), CYAN, g.on(2, .5), "mm")
        p = 1 + .04 * math.sin(g.t * 7); bw, bh = 760 * p, 130 * p; ab = g.on(2, 1.0)
        g.d.rounded_rectangle((960 - bw / 2, 520 - bh / 2, 960 + bw / 2, 520 + bh / 2), 65, fill=mix(GREEN, ab))
        tx(g, 960, 520, "SUBSCRIBE", XB(60), INK, ab, "mm")
        tx(g, 960, 680, "Which stage surprised you? Tell me in the comments.", SN(38), YEL, g.on(2, 1.6), "mm")


SCENES = [
    ("What happens when you press Enter?", WHITE, c_intro, [
        "You write a simple query: give me the names of customers from Baku. And you press *Enter*.",
        "A hundredth of a second later, the answer is on your screen. But what happened *in between*?",
        "Inside Oracle, every query goes through *four stages*: parse, optimize, execute, and fetch. In this video we'll walk through each one, slowly, with pictures."]),
    ("Think of a restaurant", ORANGE, c_restaurant, [
        "Think of a restaurant. You write your order on a piece of paper. That paper is your *SQL*.",
        "The *waiter* reads it and checks it. The *head chef* decides how to cook it. The *cooks* follow that plan. And the *plates* come out to your table.",
        "Oracle works the same way. The waiter is the *parse* stage. The head chef is the *optimizer*. The cooks are the *execution*. And the plates are the *fetch*."]),
    ("Stage 1 · Parse: is it written correctly?", CYAN, c_syntax, [
        "Stage one: *parse*. First, Oracle checks the grammar of your query, like a teacher checking spelling.",
        "Here, FROM is written as *FORM*. Oracle can't understand the sentence, so it stops immediately with an error.",
        "This grammar is called *syntax*: the right words, in the right order. Nothing else happens until the syntax is correct."]),
    ("Stage 1 · Parse: does it make sense?", CYAN, c_semantic, [
        "Next, Oracle checks the *meaning*. Does the table exist? Do these columns exist? Are *you* allowed to read them?",
        "Each failed check has its own error. Table not found. Column not found. And if you have no rights, Oracle simply says the table *does not exist*. It doesn't even tell you it's there.",
        "Only when every check passes does Oracle move on. Like a waiter confirming that every dish is really on the menu."]),
    ("Stage 1 · Parse: have I seen this before?", PURP, c_shared, [
        "Then comes a clever step. Oracle keeps the plans of recent queries in memory, in an area called the *shared pool*.",
        "It looks for your *exact* query text there. If it finds it, it reuses the plan. That's a *soft parse*, and it's very fast.",
        "If it doesn't find it, it must plan the query from scratch. That's a *hard parse*, and it costs much more time.",
        "Remember these two words. They come back at the end of this video."]),
    ("Stage 2 · Optimize: choose a plan", YEL, c_optimizer, [
        "Stage two: the *optimizer*. There are usually many ways to answer the same question.",
        "Plan A reads the whole table, one million rows. Plan B uses the index on city: a few jumps, then about twelve and a half thousand rows.",
        "The optimizer *estimates the cost* of each plan, and chooses the cheapest one. Here, plan B wins easily.",
        "So the optimizer is the part of Oracle that picks the *cheapest* plan. Like a head chef planning the fastest way to cook."]),
    ("Stage 2 · How does it estimate?", YEL, c_stats, [
        "How does it know the cost? It reads *statistics*: notes about your data. How many rows, how many different cities, which indexes exist.",
        "If those notes are *old* or *missing*, the guess is wrong. And a wrong guess can choose a *slow* plan.",
        "That's why Oracle gathers fresh statistics automatically, usually every night."]),
    ("Stage 3 · Execute: follow the plan", GREEN, c_plan, [
        "Stage three: *execute*. The chosen plan looks like this. It's a small tree of steps.",
        "It runs from the *inside out*. First, the index finds the right rows. Then those rows are read from the table. Then they go up to the result.",
        "This tree is called the *execution plan*. It's the recipe the cooks follow."]),
    ("Stage 3 · Memory or disk?", GREEN, c_cache, [
        "Where does the data come from? Tables live on *disk*, in small pieces called *blocks*.",
        "The first time, the blocks are read from disk into memory, into the *buffer cache*. Disk is slow.",
        "The next time someone needs the same blocks, they're already in memory. That's much *faster*."]),
    ("Stage 4 · Fetch: send the rows", PINK, c_fetch, [
        "Stage four: *fetch*. The rows travel to your application.",
        "They don't come one by one, and not all at once. They travel in *batches*. Your app can show the first rows while the rest are still on the way.",
        "That's why a big query can show its first rows quickly, and still take a while to finish."]),
    ("Why bind variables matter", GREEN, c_binds, [
        "Now back to soft and hard parse. Here, an application sends a new query for every customer id. Every text is *different*, so every one is a *hard parse*.",
        "With a *bind variable*, the text stays the same: id equals colon id. Only the value changes. One hard parse, and then Oracle *reuses* the plan.",
        "A bind variable is just a *placeholder*. Same text, new value. Your database will thank you."]),
    ("Remember the four stages", GREEN, c_recap, [
        "Let's recap. *Parse* checks the grammar, the names, your rights, and looks for a plan already made. *Optimize* compares plans using statistics.",
        "*Execute* follows the plan, reading blocks from memory or disk. And *fetch* sends the rows to you in batches.",
        "Each of these stages has its own short video on the channel. If this helped, subscribe, and tell me in the comments: which stage surprised you the most?"]),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    run(SCENES, Stage(1920, 1080, 30), "/home/claude/v2/outL3", "/home/claude/v2/long3_how_a_select_runs.mp4", mode, seed=3)

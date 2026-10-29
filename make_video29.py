from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

PLAN = [(0, "SELECT STATEMENT", ""), (1, "HASH JOIN", ""), (2, "TABLE ACCESS FULL", "BRANCHES"),
        (2, "NESTED LOOPS", ""), (3, "INDEX RANGE SCAN", "ACC_TYPE_IX"), (3, "TABLE ACCESS BY ROWID", "ACCOUNTS")]
ORDER = [2, 4, 5, 3, 1, 0]  # execution order of ids

def plan(d, y0, a, hl=None, cols=None, fs=26, order_shown=0, dim_rows=None):
    for k, (lv, op, nm) in enumerate(PLAN):
        y = y0 + k * 62
        on = hl is not None and k in hl
        d.rounded_rectangle((60, y, W - 60, y + 54), 10, fill=mix((40, 46, 30) if on else CARD, a),
                            outline=mix(YEL if on else DIM, a * (1 if on else .4)), width=3 if on else 1)
        d.text((80, y + 12), f"{k}", font=MB(fs), fill=mix(DIM, a))
        d.text((130 + lv * 30, y + 12), op + ("  " + nm if nm else ""), font=MN(fs), fill=mix(YEL if on else WHITE, a))
        if order_shown and k in ORDER[:order_shown]:
            n = ORDER.index(k) + 1
            d.ellipse((W - 120, y + 5, W - 76, y + 49), fill=mix(GREEN, a))
            ct(d, y + 12, str(n), SB(26), BG, a, W - 98)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "You open the execution plan…", SB(48), WHITE, a)
        plan(d, 320, pr(lt, .6, 1) * fo)
        ct(d, 740, "Where do you even start? 🤯".replace(" 🤯", ""), SB(48), YEL, pr(lt, 2, 2.4) * fo)
        ct(d, 820, "Hint: NOT at the top.", SB(40), PINK, pr(lt, 3, 3.4) * fo)
        caption(d, "Let's read a plan the way Oracle runs it, and find the slow step in seconds.", pr(lt, 4, 4.4) * fo)

    # 1 GET THE REAL PLAN
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Get the REAL plan", SB(56), GREEN, a)
        glow_box(d, (60, 320, 520, 470), RED, pr(lt, .6, 1) * fo, "EXPLAIN PLAN", "a prediction, can lie", 36, 28)
        glow_box(d, (560, 320, 1020, 470), GREEN, pr(lt, 2, 2.4) * fo, "DISPLAY_CURSOR", "what really ran", 36, 28)
        code(d, 530, [("SELECT /*+ GATHER_PLAN_STATISTICS */ …", YEL)], pr(lt, 3.5, 3.9) * fo, 28)
        code(d, 650, [("SELECT * FROM TABLE(", CYAN), ("  DBMS_XPLAN.DISPLAY_CURSOR(", CYAN),
                      ("    sql_id => '7h2kq9x…',", CYAN), ("    format => 'ALLSTATS LAST'));", CYAN)], pr(lt, 5, 5.4) * fo, 28)
        card_list(d, 950, [("ALLSTATS = estimates AND actual numbers", GREEN, 8)], lt, fo, 80, 30)
        caps = ["Explain plan only predicts. With bind variables and real data, the plan that actually ran can be different.",
                "Run the query with the gather plan statistics hint, so Oracle counts real rows and work per step.",
                "Then display the cursor with format ALLSTATS LAST: estimates and actual numbers, side by side."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    # 2 READ ORDER
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Read it as a TREE", SB(56), YEL, a)
        n = int(min(6, max(0, (lt - 2) * 1.2)))
        cur = ORDER[n - 1] if n else None
        plan(d, 320, a, hl={cur} if cur is not None else None, order_shown=n)
        card_list(d, 720, [("indent = child of the line above it", WHITE, .8),
                           ("parent needs its children first", CYAN, 1.6),
                           ("first child, deepest first → runs first", GREEN, 4),
                           ("then its sibling, then up to the parent", YEL, 6)], lt, fo, 80, 30)
        caps = ["Indentation shows the tree. Each line is a child of the less indented line above it.",
                "A parent can't produce rows until its children do. So start with the first child, go as deep as you can.",
                "Here: branches full scan, then the index range scan, the table access, the nested loops, the hash join, and finally the select."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    # 3 DATA FLOW ANIMATION
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Watch the rows flow", SB(56), CYAN, a)
        boxes = {0: (390, 320, "SELECT"), 1: (390, 470, "HASH JOIN"), 2: (90, 640, "FULL: branches"),
                 3: (690, 640, "NESTED LOOPS"), 4: (540, 820, "INDEX RANGE"), 5: (840, 820, "BY ROWID")}
        for k, (x, y, nm) in boxes.items():
            w = 300 if k not in (4, 5) else 220
            x0 = x - (0 if k in (0, 1) else 0)
            glow_box(d, (x0, y, x0 + w, y + 100), [WHITE, PURP, CYAN, PINK, GREEN, GREEN][k], a, nm, None, 26)
        links = [(2, 1, 1), (4, 3, 3), (5, 3, 4.5), (3, 1, 6), (1, 0, 7.5)]
        for c, p, st in links:
            if lt > st:
                cx, cy, _ = boxes[c]; px, py, _ = boxes[p]
                wc = 300 if c not in (4, 5) else 220; wp = 300
                flow(d, [(cx + wc / 2, cy), (px + wp / 2, py + 100)], YEL, a, t, pr(lt, st, st + .8))
        ab = pr(lt, 2, 2.4) * fo
        ct(d, 960, "hash table built from BRANCHES", SN(28), CYAN, ab)
        ct(d, 1010, "probe rows stream up from NESTED LOOPS", SN(28), PINK, pr(lt, 6, 6.4) * fo)
        caps = ["The hash join first reads all branches and builds a hash table in memory.",
                "Then the nested loops start: for each index entry, fetch the account row by ROWID.",
                "Those rows stream up into the hash join, which probes the hash table and sends matches to the top."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 4 E-ROWS vs A-ROWS
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The #1 trick: E-Rows vs A-Rows", SB(48), YEL, a)
        hdr = ["Id", "Operation", "E-Rows", "A-Rows"]
        xs = [80, 160, 640, 840]
        for x, h in zip(xs, hdr): d.text((x, 330), h, font=SB(28), fill=mix(DIM, a))
        rows = [("2", "FULL branches", "50", "50", False), ("4", "INDEX RANGE SCAN", "10", "1 000 000", True),
                ("5", "BY ROWID accounts", "1 /start", "1 000 000", False)]
        for k, (idx, op, e, ar, bad) in enumerate(rows):
            y = 380 + k * 80; al = pr(lt, .6 + k * .6, 1 + k * .6) * fo
            d.rounded_rectangle((60, y, W - 60, y + 66), 10, fill=mix((60, 22, 34) if bad and lt > 3 else CARD, al))
            for x, v in zip(xs, [idx, op, e, ar]):
                d.text((x, y + 16), v, font=MN(28), fill=mix(RED if bad and lt > 3 and v == ar else WHITE, al))
        bar(d, 110, 680, 970, 40, pr(lt, 4, 4.4) * .02, CYAN, pr(lt, 3.8, 4.2) * fo, "estimated", "10 rows")
        bar(d, 110, 790, 970, 40, pr(lt, 4.5, 6), RED, pr(lt, 4.3, 4.7) * fo, "actual", "1 000 000 rows")
        ct(d, 900, "100 000× off → nested loops was the WRONG choice", SB(32), RED, pr(lt, 6.5, 6.9) * fo)
        card_list(d, 970, [("fix the estimate: stats, histograms (video 15)", GREEN, 8.5)], lt, fo, 80, 30)
        caps = ["The most powerful trick: compare estimated rows with actual rows, line by line.",
                "The optimizer expected ten rows from the index, and got a million. For ten rows, nested loops is perfect. For a million, it's a disaster.",
                "Find the first line where the estimate goes wrong. That's the root cause. Fix the statistics or histograms, and the plan fixes itself."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 5 STARTS + BUFFERS
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Starts, Buffers, A-Time", SB(54), PINK, a)
        rows = [("INDEX RANGE SCAN", "1", "4 K", "0.4 s"), ("BY ROWID accounts", "1 M", "3.1 M", "41 s"),
                ("HASH JOIN", "1", "0", "0.2 s")]
        xs = [80, 520, 700, 880]
        for x, h in zip(xs, ["Operation", "Starts", "Buffers", "A-Time"]): d.text((x, 330), h, font=SB(28), fill=mix(DIM, a))
        for k, r in enumerate(rows):
            y = 380 + k * 80; al = pr(lt, .6 + k * .5, 1 + k * .5) * fo
            hot = k == 1 and lt > 3
            d.rounded_rectangle((60, y, W - 60, y + 66), 10, fill=mix((60, 22, 34) if hot else CARD, al),
                                outline=mix(RED, al * (1 if hot else 0)), width=4)
            for x, v in zip(xs, r):
                d.text((x, y + 16), v, font=MN(28), fill=mix(RED if hot else WHITE, al))
        bars = [("index", .01, GREEN, "0.4 s"), ("table by ROWID", 1, RED, "41 s"), ("hash join", .005, CYAN, "0.2 s")]
        for k, (nm, p, col, v) in enumerate(bars):
            bar(d, 110, 660 + k * 110, 970, 40, pr(lt, 3.5 + k * .4, 4.5 + k * .4) * p, col, pr(lt, 3.3, 3.7) * fo, nm, v)
        card_list(d, 1000, [("Starts = how many times the step ran", YEL, 7),
                            ("biggest Buffers / A-Time = your hotspot", RED, 8.5)], lt, fo, 80, 30)
        caps = ["Starts shows how many times a step ran. Under nested loops, the inner step runs once per outer row.",
                "Buffers shows logical reads, and A-Time the real elapsed time. Here, the table access by ROWID ran a million times and took forty one seconds.",
                "Sort by buffers or time, and the hotspot is obvious. Tune that one line."]
        caption(d, caps[0 if lt < 3.3 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 6 PREDICATES + NOTE
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Don't skip the bottom!", SB(54), GREEN, a)
        code(d, 310, [("Predicate Information:", WHITE), ("  4 - access(\"ACC_TYPE\"='SAV')", GREEN),
                      ("  5 - filter(\"STATUS\"='ACTIVE')", RED)], pr(lt, .6, 1) * fo, 30)
        glow_box(d, (60, 520, 520, 660), GREEN, pr(lt, 2, 2.4) * fo, "access", "used to FIND rows", 36, 28)
        glow_box(d, (560, 520, 1020, 660), RED, pr(lt, 3.5, 3.9) * fo, "filter", "read, then THROWN AWAY", 36, 28)
        ct(d, 700, "1 M rows fetched → 2 000 kept", SB(34), RED, pr(lt, 5, 5.4) * fo)
        code(d, 780, [("Note:", WHITE), ("  - SQL plan baseline used", CYAN), ("  - dynamic statistics used", YEL)],
             pr(lt, 7, 7.4) * fo, 28)
        caps = ["Under the plan is the predicate section. Access predicates are used to find rows, through an index.",
                "Filter predicates are applied after the rows were read. Here a million rows are fetched, and only two thousand survive.",
                "Add status to the index, and the filter becomes an access. And read the note section: baselines, dynamic statistics, and more."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 7 CHECKLIST
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Your 5-step plan checklist", SB(50), WHITE, a)
        steps = [("real plan: DISPLAY_CURSOR ALLSTATS LAST", GREEN), ("read the tree: deepest first child", YEL),
                 ("find the hotspot: Buffers / A-Time", RED), ("first big E-Rows ≠ A-Rows → root cause", PINK),
                 ("predicates: filter that should be access?", CYAN)]
        for k, (s_, col) in enumerate(steps):
            y = 330 + k * 140; al = pr(lt, .6 + k * 1.6, 1 + k * 1.6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 120), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.ellipse((95, y + 30, 155, y + 90), fill=mix(col, al)); ct(d, y + 40, str(k + 1), SB(34), BG, al, 125)
            for j, ln in enumerate(wrap(d, s_, SB(30), 780)): d.text((180, y + 22 + j * 40), ln, font=SB(30), fill=mix(WHITE, al))
        caps = ["So here's the routine. Get the real plan with actual statistics, and read it as a tree.",
                "Find the hotspot by buffers and time, then find the first line where estimated and actual rows split apart.",
                "Finally, check the predicates: a filter that should be an access is often the cheapest fix."]
        caption(d, caps[0 if lt < 3.8 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("DISPLAY_CURSOR", "→ the plan that really ran"), ("Tree", "→ deepest first child first"),
                          ("E vs A-Rows", "→ where estimates break"), ("Starts/Buffers", "→ the hotspot"),
                          ("Predicates", "→ access vs filter")],
              "Don't guess. The plan tells you exactly where the time went.", 470)
    else:
        cta(d, t - T[9], "SQL HINTS", "when to use them, and when not", 66)
    return im

if __name__ == "__main__":
    preview(frame, T, "v29_sheet.png")

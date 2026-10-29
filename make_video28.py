from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def node(d, x, y, w, keys, col, a, hl=False):
    h = 70
    d.rounded_rectangle((x, y, x + w, y + h), 12, fill=mix(CARD, a), outline=mix(YEL if hl else col, a), width=5 if hl else 3)
    ct(d, y + 18, keys, MB(26), YEL if hl else WHITE, a, x + w / 2)
    return (x + w / 2, y + h)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        code(d, 230, [("CREATE INDEX acc_br_ix", CYAN), ("  ON accounts(branch_id);", CYAN)], a, 32)
        code(d, 400, [("SELECT * FROM accounts", YEL), ("WHERE branch_id = 12;", YEL)], pr(lt, .8, 1.2) * fo, 32)
        ap = pr(lt, 1.8, 2.2) * fo
        d.rounded_rectangle((110, 570, 970, 650), 14, fill=mix(CARD, ap), outline=mix(RED, ap), width=4)
        d.text((140, 590), "TABLE ACCESS FULL  ACCOUNTS", font=MB(32), fill=mix(RED, ap))
        ct(d, 720, "The index exists… Oracle ignores it?! 🤔".replace(" 🤔", ""), SB(44), YEL, pr(lt, 2.8, 3.2) * fo)
        caption(d, "Often Oracle is right to ignore it. Let's look inside a B-tree and see why.", pr(lt, 4, 4.4) * fo)

    # 1 B-TREE WALK
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Inside a B-tree index", SB(54), WHITE, a)
        step = 0 if lt < 2 else 1 if lt < 3.5 else 2 if lt < 5 else 3
        r = node(d, 390, 320, 300, "< 500 | ≥ 500", PURP, a, step == 1)
        ct(d, 395, "ROOT", SN(24), PURP, a, 540)
        b1 = node(d, 120, 480, 300, "< 250 | ≥ 250", CYAN, a)
        b2 = node(d, 660, 480, 300, "< 750 | ≥ 750", CYAN, a, step == 2)
        ct(d, 555, "BRANCH", SN(24), CYAN, a, 540)
        d.line((470, 390, 270, 480), fill=mix(DIM, a), width=3); d.line((610, 390, 810, 480), fill=mix(DIM, a), width=3)
        leaves = ["101 105 120", "260 300 410", "520 600 742", "760 801 990"]
        for k, kv in enumerate(leaves):
            x = 40 + k * 255
            node(d, x, 660, 235, kv, GREEN, a, step == 3 and k == 2)
            if k < 3: arrow(d, x + 235, 695, x + 255, 695, GREEN, a, 3)
        for (x0, x1) in [(230, 157), (310, 412), (770, 667), (850, 922)]:
            d.line((x0, 550, x1, 660), fill=mix(DIM, a), width=3)
        ct(d, 745, "LEAVES: sorted key + ROWID, linked ⇄", SN(26), GREEN, a)
        ct(d, 820, "WHERE id = 742", MB(34), YEL, pr(lt, 1.6, 2) * fo)
        if lt > 5.2:
            ct(d, 880, "3 block reads → ROWID → table row", SB(34), GREEN, pr(lt, 5.2, 5.6) * fo)
        card_list(d, 950, [("height 3–4 even for 100 M rows", CYAN, 7.5)], lt, fo, 80, 32)
        caps = ["A B-tree has a root, branch blocks, and leaf blocks. Leaves hold sorted keys with the ROWID of each table row.",
                "To find 742, Oracle reads the root, follows the right branch, and lands on one leaf. Three block reads.",
                "The tree stays very flat: three or four levels even for a hundred million rows. That's why a single-row lookup is so fast."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 2 RANGE SCAN + TABLE ACCESS
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Range scan = 2 lookups per row", SB(50), CYAN, a)
        for k in range(4):
            x = 60 + k * 245
            node(d, x, 330, 225, f"leaf {k + 1}", GREEN, a, int(lt * .9) % 4 == k and lt > 1)
            if k < 3: arrow(d, x + 225, 365, x + 245, 365, GREEN, a, 3)
        ct(d, 420, "walk the leaves in key order →", SN(28), GREEN, pr(lt, 1, 1.4) * fo)
        for k in range(8):
            r_, c = divmod(k, 4); x = 100 + c * 230; y = 640 + r_ * 130
            d.rounded_rectangle((x, y, x + 190, y + 100), 12, fill=mix(CARD, a), outline=mix(PINK, a), width=2)
            ct(d, y + 34, f"table blk {k + 1}", SN(24), PINK, a, x + 95)
        ct(d, 590, "TABLE ACCESS BY INDEX ROWID", MB(28), PINK, pr(lt, 2.5, 2.9) * fo)
        if lt > 3:
            for j in range(4):
                p = (t * .8 + j / 4) % 1
                k = (j * 3 + int(t)) % 8
                r_, c = divmod(k, 4)
                x = lerp(170 + j * 245, 195 + c * 230, p); y = lerp(400, 640 + r_ * 130, p)
                d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=mix(YEL, pr(lt, 3, 3.4) * fo))
        card_list(d, 930, [("each ROWID may hit a DIFFERENT table block", YEL, 6),
                           ("1 row → cheap · 1 M rows → 1 M block visits", RED, 8)], lt, fo, 80, 30)
        caps = ["For a range, Oracle walks the leaf blocks in key order, collecting ROWIDs.",
                "Then for every ROWID, it visits the table block that holds the row. That's the expensive part.",
                "For a few rows, it's perfect. For a million rows, it's a million single-block visits."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 3 CLUSTERING FACTOR
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Clustering factor", SB(56), YEL, a)
        for side, (x0, title, col, perm, st) in enumerate([(70, "GOOD: table in index order", GREEN, [0, 0, 0, 1, 1, 1, 2, 2], .6),
                                                           (560, "BAD: rows scattered", RED, [0, 3, 1, 2, 0, 3, 2, 1], 3.5)]):
            al = pr(lt, st, st + .4) * fo
            d.text((x0, 320), title, font=SB(28), fill=mix(col, al))
            for k in range(8):
                y = 380 + k * 52
                d.rounded_rectangle((x0, y, x0 + 140, y + 42), 8, fill=mix(CARD, al), outline=mix(GREEN, al), width=2)
                ct(d, y + 8, f"key {k + 1}", SN(22), WHITE, al, x0 + 70)
            for b in range(4):
                y = 390 + b * 100
                d.rounded_rectangle((x0 + 290, y, x0 + 450, y + 80), 10, fill=mix(CARD, al), outline=mix(PINK, al), width=2)
                ct(d, y + 24, f"blk {b + 1}", SN(24), PINK, al, x0 + 370)
            n = int(min(8, max(0, (lt - st - .4) * 4)))
            for k in range(n):
                b = perm[k]
                d.line((x0 + 140, 401 + k * 52, x0 + 290, 430 + b * 100), fill=mix(col, al), width=3)
            jumps = sum(1 for k in range(1, 8) if perm[k] != perm[k - 1]) + 1
            ct(d, 830, f"CF ≈ {jumps if n == 8 else '…'}", MB(36), col, al, x0 + 225)
        card_list(d, 910, [("CF ≈ #blocks → index range scans are cheap", GREEN, 7),
                           ("CF ≈ #rows → optimizer prefers full scan", RED, 8.5)], lt, fo, 80, 30)
        caps = ["The clustering factor counts how often the table block changes as you walk the index in order.",
                "If the table is stored in index order, neighbours share blocks: a low clustering factor. If rows are scattered, every key jumps to another block.",
                "A clustering factor close to the number of rows makes range scans expensive, so the optimizer prefers a full scan."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 4 COST CROSSOVER
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Index or full scan?", SB(56), WHITE, a)
        gx0, gy0, gx1, gy1 = 130, 340, 970, 800
        d.line((gx0, gy1, gx1, gy1), fill=mix(DIM, a), width=3); d.line((gx0, gy0, gx0, gy1), fill=mix(DIM, a), width=3)
        d.text((gx0 + 10, gy0 - 10), "cost", font=SN(26), fill=mix(DIM, a))
        ct(d, gy1 + 10, "% of rows returned →", SN(26), DIM, a)
        p = pr(lt, .8, 3.5)
        fy = gy1 - .45 * (gy1 - gy0)
        d.line((gx0, fy, gx0 + p * (gx1 - gx0), fy), fill=mix(CYAN, a), width=6)
        ct(d, fy - 44, "FULL SCAN (flat)", SB(28), CYAN, pr(lt, 1, 1.4) * fo, 820)
        pts = [(gx0 + xx / 60 * (gx1 - gx0), gy1 - min(1, xx / 60 * 6) * (gy1 - gy0)) for xx in range(int(60 * p) + 1)]
        if len(pts) > 1: d.line(pts, fill=mix(PINK, a), width=6)
        ct(d, gy0 + 20, "INDEX (steep)", SB(28), PINK, pr(lt, 1.5, 1.9) * fo, 400)
        if lt > 4:
            ak = pr(lt, 4, 4.4) * fo
            cx = gx0 + .45 / 6 * (gx1 - gx0)
            d.ellipse((cx - 14, fy - 14, cx + 14, fy + 14), fill=mix(YEL, ak))
            ct(d, fy + 24, "crossover: a few %", SB(28), YEL, ak, cx + 150)
        card_list(d, 880, [("branch 12 = 30% of accounts → FULL SCAN wins", GREEN, 6.5),
                           ("check stats & histograms (video 15)", CYAN, 8.5)], lt, fo, 80, 30)
        caps = ["The cost of a full scan is flat: it reads the whole table once, with big multiblock reads.",
                "The index cost grows with every row. Somewhere around a few percent of the table, the lines cross.",
                "If branch twelve owns thirty percent of all accounts, the full scan really is faster. The optimizer was right."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 5 COMPOSITE + SKIP SCAN
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Composite index: order matters", SB(48), PURP, a)
        code(d, 310, [("INDEX (branch_id, acc_type, open_date)", PURP)], a, 30)
        rows = [("WHERE branch_id = 12", "✓ leading column", GREEN, 1),
                ("WHERE branch_id = 12 AND acc_type = 'SAV'", "✓ even better", GREEN, 2.5),
                ("WHERE acc_type = 'SAV'", "✗ no leading column", RED, 4),
                ("…but few branches?", "→ INDEX SKIP SCAN", YEL, 6)]
        for k, (q, r, col, st) in enumerate(rows):
            y = 440 + k * 135; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 115), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 16), q, font=MN(28), fill=mix(WHITE, al))
            d.text((100, y + 64), r, font=SB(30), fill=mix(col, al))
        card_list(d, 1000, [("put equality columns first, range columns last", CYAN, 8.5)], lt, fo, 80, 30)
        caps = ["In a composite index, the column order matters. Queries on the leading column, or the first few columns, use it directly.",
                "A query that skips the leading column usually can't use it.",
                "Exception: if the leading column has only a few distinct values, Oracle can do an index skip scan, one probe per value. Put equality columns first."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 6 FUNCTIONS KILL INDEXES
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Index killers", SB(58), RED, a)
        bad = [("WHERE UPPER(name) = 'ALI'", "function on column", .6),
               ("WHERE TRUNC(op_date) = :d", "function on column", 2),
               ("WHERE acc_no = 12345", "acc_no is VARCHAR2 → TO_NUMBER!", 3.4)]
        for k, (q, why, st) in enumerate(bad):
            y = 320 + k * 130; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 110), 16, fill=mix((60, 22, 34), al), outline=mix(RED, al), width=3)
            d.text((100, y + 14), q, font=MN(28), fill=mix(WHITE, al))
            d.text((100, y + 62), "✗ " + why, font=SB(28), fill=mix(RED, al))
        good = [("op_date >= :d AND op_date < :d + 1", 6), ("CREATE INDEX … (UPPER(name))", 7.2), ("acc_no = '12345'", 8.4)]
        for k, (q, st) in enumerate(good):
            y = 740 + k * 95; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 80), 14, fill=mix((20, 50, 36), al))
            d.text((100, y + 22), "✓ " + q, font=MN(28), fill=mix(GREEN, al))
        caps = ["A function on the indexed column hides it from the index. Upper of name, or trunc of a date: full scan.",
                "Watch out for implicit conversion: comparing a VARCHAR2 column with a number makes Oracle apply TO_NUMBER to every row.",
                "Rewrite the condition as a range, create a function-based index, or compare with the right data type."]
        caption(d, caps[0 if lt < 3.4 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 7 COST OF INDEXES
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Indexes aren't free", SB(56), YEL, a)
        glow_box(d, (90, 320, 510, 450), CYAN, pr(lt, .6, 1) * fo, "covering index", "all columns in index → no table", 32, 24)
        glow_box(d, (570, 320, 990, 450), GREEN, pr(lt, 1.6, 2) * fo, "INDEX FAST FULL", "scan index like a table", 32, 24)
        ct(d, 520, "1 INSERT into accounts =", SB(34), WHITE, pr(lt, 3.5, 3.9) * fo)
        n = int(min(6, max(0, (lt - 4) * 2)))
        for k in range(6):
            al = pr(lt, 4 + k * .5, 4.4 + k * .5) * fo
            x = 90 + k * 155
            d.rounded_rectangle((x, 590, x + 135, 680), 12, fill=mix(PINK if k else CYAN, al))
            ct(d, 615, "table" if k == 0 else f"idx {k}", SB(26), BG, al, x + 67)
        ct(d, 720, "6 block changes + 6× redo", SB(34), RED, pr(lt, 7, 7.4) * fo)
        card_list(d, 810, [("unused index? → test with ALTER INDEX … INVISIBLE", GREEN, 8.5)], lt, fo, 80, 30)
        caps = ["An index that contains every column the query needs is a covering index: no table visit at all. Or scan the whole index with a fast full scan.",
                "But every index has a price. One insert into a table with five indexes changes six structures, and generates redo for each.",
                "Before dropping an index you suspect is unused, make it invisible and watch."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("B-tree", "→ root, branch, leaf: 3 reads"), ("Range scan", "→ + 1 table visit per row"),
                          ("Clust. factor", "→ scattered rows = costly"), ("Composite", "→ leading column first"),
                          ("Functions", "→ hide the index")],
              "An ignored index is often the right decision. Know why before you force it.", 470)
    else:
        cta(d, t - T[9], "READING EXECUTION PLANS", "where to start, what to look at", 54)
    return im

if __name__ == "__main__":
    preview(frame, T, "v28_sheet.png")

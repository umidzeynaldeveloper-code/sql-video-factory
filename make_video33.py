from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def table(d, x0, y0, cols, widths, rows, a, colors=None, fs=26, rh=56, hl=None):
    x = x0
    for c, w in zip(cols, widths):
        d.text((x + 10, y0), c, font=SB(fs - 2), fill=mix(DIM, a)); x += w
    for r, row in enumerate(rows):
        y = y0 + 40 + r * rh
        rc = colors[r] if colors else CARD
        d.rounded_rectangle((x0, y, x0 + sum(widths), y + rh - 8), 8, fill=mix(rc, a),
                            outline=mix(YEL, a) if hl and r in hl else None, width=3)
        x = x0
        for v, w in zip(row, widths):
            d.text((x + 10, y + 10), str(v), font=MN(fs), fill=mix(WHITE, a)); x += w

ACC = [(1, 500), (1, 900), (1, 200), (1, 700), (2, 300), (2, 800), (2, 100)]
PCOL = {1: (24, 52, 76), 2: (66, 30, 60)}

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Top 3 payments per account?", SB(50), WHITE, a)
        code(d, 310, [("SELECT … FROM tx t1 WHERE 3 >", RED), ("  (SELECT COUNT(*) FROM tx t2", RED),
                      ("   WHERE t2.acc = t1.acc", RED), ("     AND t2.amt > t1.amt) …", RED)], pr(lt, .6, 1) * fo, 28)
        ct(d, 560, "self-join: slow & unreadable", SB(32), RED, pr(lt, 1.6, 2) * fo)
        code(d, 630, [("ROW_NUMBER() OVER (", GREEN), ("  PARTITION BY acc ORDER BY amt DESC)", GREEN)], pr(lt, 2.6, 3) * fo, 30)
        ct(d, 790, "one pass ⚡ one line", SB(40), GREEN, pr(lt, 3.2, 3.6) * fo)
        caption(d, "Analytic functions: answers that need neighbours, without self-joins.", pr(lt, 4, 4.4) * fo)

    # 1 GROUP BY vs ANALYTIC
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "GROUP BY collapses. OVER keeps.", SB(48), WHITE, a)
        rows = [(acc, amt) for acc, amt in ACC]
        table(d, 60, 320, ["acc", "amt"], [100, 140], rows, a, [PCOL[r[0]] for r in rows], 26, 52)
        p = pr(lt, 1.5, 3)
        ag = pr(lt, 1.5, 1.9) * fo
        d.text((380, 330), "GROUP BY acc", font=SB(28), fill=mix(YEL, ag))
        table(d, 380, 370, ["acc", "SUM"], [90, 130], [(1, 2300), (2, 1200)], ag, [PCOL[1], PCOL[2]], 26, 52)
        aa = pr(lt, 4.5, 4.9) * fo
        d.text((700, 330), "SUM() OVER", font=SB(28), fill=mix(GREEN, aa))
        tot = {1: 2300, 2: 1200}
        table(d, 640, 370, ["acc", "amt", "total"], [80, 110, 130], [(r[0], r[1], tot[r[0]]) for r in rows], aa,
              [PCOL[r[0]] for r in rows], 24, 52)
        ct(d, 800, "2 rows ← 7 rows → 7 rows + extra column", SB(30), YEL, pr(lt, 6, 6.4) * fo)
        card_list(d, 880, [("% of account total = amt / total, same query", GREEN, 8)], lt, fo, 80, 30)
        caps = ["Group by collapses each group into one row. You get the totals, but you lose the details.",
                "An analytic function, with the over clause, keeps every row, and adds the group's value next to it.",
                "Now each payment can be compared with its account total, in the same query."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 2 OVER ANATOMY
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Anatomy of OVER ( )", SB(56), CYAN, a)
        parts = [("PARTITION BY acc", "split into groups (like GROUP BY, rows stay)", PINK, .8),
                 ("ORDER BY tx_date", "order inside each group", YEL, 3),
                 ("ROWS BETWEEN 2 PRECEDING AND CURRENT ROW", "the window: which rows to look at", GREEN, 5.5)]
        for k, (h, s_, col, st) in enumerate(parts):
            y = 330 + k * 200; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 170), 18, fill=mix(CARD, al), outline=mix(col, al), width=4)
            d.text((100, y + 26), h, font=MB(30), fill=mix(col, al))
            d.text((100, y + 96), s_, font=SN(28), fill=mix(WHITE, al))
        if lt > 7:
            ab = pr(lt, 7, 7.4) * fo
            for k in range(6):
                x = 110 + k * 150; win = 2 + int((lt - 7) * 1.5) % 4
                inw = win - 2 <= k <= win
                d.rounded_rectangle((x, 960, x + 130, 1030), 10, fill=mix(GREEN if inw else OFFB, ab))
                ct(d, 978, f"row {k + 1}", SB(24), BG if inw else DIM, ab, x + 65)
        caps = ["The over clause has three parts. Partition by splits the rows into groups, but the rows stay.",
                "Order by sorts the rows inside each group.",
                "And the window frame says which rows the function looks at: here, the current row and the two before it. It slides along."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 3 ROW_NUMBER / RANK / DENSE_RANK
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Ties: three ways to count", SB(52), YEL, a)
        amts = [900, 700, 700, 500, 200]
        rn = [1, 2, 3, 4, 5]; rk = [1, 2, 2, 4, 5]; dr = [1, 2, 2, 3, 4]
        cols = ["amt", "ROW_NUMBER", "RANK", "DENSE_RANK"]
        widths = [160, 270, 220, 270]
        x = 70
        for c, w, st in zip(cols, widths, [0, 1, 3, 5]):
            d.text((x + 10, 330), c, font=SB(26), fill=mix([WHITE, CYAN, PINK, GREEN][cols.index(c)], pr(lt, st, st + .4) * fo)); x += w
        for r in range(5):
            y = 380 + r * 80; tie = r in (1, 2)
            d.rounded_rectangle((70, y, 990, y + 66), 10, fill=mix((60, 50, 20) if tie and lt > 2 else CARD, a))
            vals = [amts[r], rn[r], rk[r], dr[r]]; x = 70
            for j, (v, w) in enumerate(zip(vals, widths)):
                al = pr(lt, [0, 1, 3, 5][j], [0, 1, 3, 5][j] + .4) * fo
                d.text((x + 30, y + 14), str(v), font=MB(32), fill=mix([WHITE, CYAN, PINK, GREEN][j], al)); x += w
        card_list(d, 820, [("ROW_NUMBER: always unique, ties broken arbitrarily", CYAN, 7),
                           ("RANK: ties share, then GAP · DENSE_RANK: no gap", PINK, 8.5)], lt, fo, 80, 29)
        caps = ["Two payments of seven hundred: a tie. Row number gives every row a unique number, and breaks the tie arbitrarily.",
                "Rank gives both the same number, then skips: one, two, two, four.",
                "Dense rank gives both the same number, with no gap: one, two, two, three. Add a second order by column if you need a stable result."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    # 4 TOP-N PER GROUP
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Top-N per group", SB(56), GREEN, a)
        code(d, 310, [("SELECT * FROM (", WHITE), ("  SELECT t.*, ROW_NUMBER() OVER (", GREEN),
                      ("    PARTITION BY acc ORDER BY amt DESC) rn", GREEN), ("  FROM tx t)", WHITE), ("WHERE rn ≤ 3;", YEL)], a, 28)
        srt = sorted(ACC, key=lambda r: (r[0], -r[1]))
        rnk = []; last = None; n = 0
        for acc, amt in srt:
            n = n + 1 if acc == last else 1; last = acc; rnk.append(n)
        for r, ((acc, amt), k) in enumerate(zip(srt, rnk)):
            y = 640 + r * 62; keep = k <= 3
            al = pr(lt, 2 + r * .3, 2.4 + r * .3) * fo
            gone = (not keep) and lt > 6
            d.rounded_rectangle((110, y, 970, y + 52), 10, fill=mix(PCOL[acc], al * (.3 if gone else 1)),
                                outline=mix(GREEN if keep and lt > 6 else DIM, al), width=3 if keep and lt > 6 else 1)
            d.text((140, y + 10), f"acc {acc}   amt {amt}", font=MN(28), fill=mix(WHITE, al * (.3 if gone else 1)))
            d.text((800, y + 10), f"rn={k}", font=MB(28), fill=mix(GREEN if keep else RED, al))
        caps = ["Now the top three payments per account. Number the rows inside each account, highest amount first.",
                "You can't filter on an analytic function in the same select, because it's calculated after where. So wrap it in a subquery.",
                "Then keep row number three or less. One pass over the table, no self-join."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 5 LAG / LEAD
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "LAG & LEAD: look at neighbours", SB(48), PINK, a)
        code(d, 310, [("bal - LAG(bal) OVER (PARTITION BY acc", PINK), ("                  ORDER BY dt) AS change", PINK)], a, 28)
        bals = [("01 Oct", 1000), ("02 Oct", 1200), ("03 Oct", 900), ("04 Oct", 900), ("05 Oct", 1500)]
        for r, (dt, b) in enumerate(bals):
            y = 470 + r * 90
            d.rounded_rectangle((110, y, 970, y + 74), 12, fill=mix(CARD, a))
            d.text((140, y + 20), dt, font=MN(30), fill=mix(DIM, a))
            d.text((380, y + 20), str(b), font=MB(30), fill=mix(WHITE, a))
            if r and lt > 1.5 + r * .9:
                al = pr(lt, 1.5 + r * .9, 1.9 + r * .9) * fo
                d.arc((520, y - 60, 600, y + 40), 270, 90, fill=mix(PINK, al), width=4)
                ch = b - bals[r - 1][1]
                d.text((660, y + 20), ("+" if ch > 0 else "") + str(ch), font=MB(30), fill=mix(GREEN if ch > 0 else RED if ch < 0 else DIM, al))
            elif r == 0 and lt > 1.5:
                d.text((660, y + 20), "NULL", font=MB(30), fill=mix(DIM, pr(lt, 1.5, 1.9) * fo))
        card_list(d, 950, [("LEAD = next row · LAG(bal, 1, 0) = default 0", CYAN, 7)], lt, fo, 80, 30)
        caps = ["LAG reads a value from the previous row in the window. Here: yesterday's balance, to compute the daily change.",
                "The first row has no previous one, so LAG returns null, unless you give a default.",
                "LEAD does the same with the next row. No self-join on date minus one, and no gaps problem."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 6 RUNNING TOTAL
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Running total", SB(56), CYAN, a)
        code(d, 310, [("SUM(amt) OVER (PARTITION BY acc ORDER BY dt", CYAN), ("  ROWS UNBOUNDED PRECEDING)", CYAN)], a, 28)
        amts = [200, 500, -300, 400, 100]
        run = 0; n = int(min(5, max(0, (lt - 1) * 1.2)))
        for k, v in enumerate(amts):
            run += v
            x = 120 + k * 175; al = a if k < n else a * .15
            h = run / 900 * 380
            d.rounded_rectangle((x, 880 - h, x + 140, 880), 10, fill=mix(CYAN, al))
            ct(d, 880 - h - 40, str(run), MB(28), WHITE, al, x + 70)
            ct(d, 900, ("+" if v > 0 else "") + str(v), SN(26), GREEN if v > 0 else RED, al, x + 70)
        ab = pr(lt, 7, 7.4) * fo
        card_list(d, 970, [("ROWS, not the default RANGE: ties on dt add up together!", YEL, 7)], lt, fo, 80, 28)
        caps = ["A running total is a sum whose window grows: from the first row up to the current row.",
                "Each bar is the balance after that payment. One sort, one pass.",
                "Write ROWS unbounded preceding. With only order by, the default is RANGE, and rows with the same date are summed together."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 7 PERFORMANCE
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Fast, but know the cost", SB(54), GREEN, a)
        bar(d, 110, 360, 970, 44, pr(lt, .8, 2.5), RED, pr(lt, .6, 1) * fo, "self-join version", "48 s")
        bar(d, 110, 490, 970, 44, pr(lt, 2.5, 3) * .06, GREEN, pr(lt, 2.3, 2.7) * fo, "analytic version", "3 s")
        code(d, 610, [("WINDOW SORT", YEL), ("  TABLE ACCESS FULL  TX", WHITE)], pr(lt, 4, 4.4) * fo, 30)
        card_list(d, 790, [("1 sort per different PARTITION/ORDER combo", YEL, 5.5),
                           ("big sorts use PGA → TEMP (video 32)", PINK, 7),
                           ("filter rows BEFORE the analytic, not after", GREEN, 8.5)], lt, fo, 80, 30)
        caps = ["Replacing a self-join with an analytic function often turns minutes into seconds.",
                "In the plan you'll see a window sort. Each different partition and order combination needs its own sort.",
                "Big sorts use PGA and may spill to temp, so filter rows before the analytic function, in the inner query."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("OVER", "→ keeps every row"), ("PARTITION BY", "→ groups, rows stay"),
                          ("ROW_NUMBER", "→ top-N per group"), ("LAG / LEAD", "→ previous / next row"),
                          ("SUM OVER", "→ running totals, use ROWS")],
              "Need a neighbour or a group value? Reach for OVER, not a self-join.", 450)
    else:
        cta(d, t - T[9], "MERGE", "insert or update in one statement", 80)
    return im

if __name__ == "__main__":
    preview(frame, T, "v33_sheet.png")

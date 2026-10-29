from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        code(d, 230, [("SELECT /*+ INDEX(a acc_ix) */ …", YEL)], a, 32)
        bar(d, 110, 400, 970, 44, pr(lt, .8, 1.2) * .05, GREEN, pr(lt, .6, 1) * fo, "test, 10K rows", "0.1 s ✓")
        bar(d, 110, 540, 970, 44, pr(lt, 2, 3.5), RED, pr(lt, 1.8, 2.2) * fo, "prod, 6 months later", "25 min ✗")
        ct(d, 680, "The hint froze a plan.", SB(46), WHITE, pr(lt, 3.2, 3.6) * fo)
        ct(d, 750, "The data didn't freeze.", SB(46), RED, pr(lt, 3.6, 4) * fo)
        caption(d, "Hints are powerful, and dangerous. Let's see when to use them, and when not.", pr(lt, 4, 4.4) * fo)

    # 1 WHAT A HINT IS
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "A hint = an order to the optimizer", SB(46), WHITE, a)
        code(d, 320, [("SELECT /*+ FULL(a) */ *", GREEN), ("FROM   accounts a", WHITE)], pr(lt, .6, 1) * fo, 32)
        ab = pr(lt, 2, 2.4) * fo
        d.line((258, 446, 258, 474), fill=mix(YEL, ab), width=4)
        ct(d, 480, "right after SELECT, with a +", SB(30), YEL, ab, 400)
        code(d, 580, [("SELECT /*+ FUL(a) */ *", RED), ("SELECT /* FULL(a) */ *", RED)], pr(lt, 4, 4.4) * fo, 32)
        ax = pr(lt, 5.5, 5.9) * fo
        glow_box(d, (110, 760, 970, 900), RED, ax, "typo or missing + → silently IGNORED", "no error, no warning", 34, 28)
        caps = ["A hint is a special comment, starting with slash star plus, placed right after SELECT, UPDATE, INSERT or DELETE.",
                "It tells the optimizer what to do: here, scan accounts in full.",
                "But a typo, or a missing plus sign, and the hint is just a comment. Oracle ignores it silently. No error at all."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 2 HINT FAMILIES
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The hint families", SB(56), CYAN, a)
        fam = [("ACCESS", "FULL · INDEX · NO_INDEX", CYAN), ("JOIN ORDER", "LEADING(b a)", YEL),
               ("JOIN METHOD", "USE_NL · USE_HASH · USE_MERGE", PINK), ("PARALLEL", "PARALLEL(4)", PURP),
               ("LOAD", "APPEND (direct path)", GREEN), ("DIAGNOSTIC", "GATHER_PLAN_STATISTICS", WHITE)]
        for k, (h, ex, col) in enumerate(fam):
            r, c = divmod(k, 2); x = 70 + c * 480; y = 320 + r * 230
            al = pr(lt, .6 + k * 1.2, 1 + k * 1.2) * fo
            glow_box(d, (x, y, x + 460, y + 200), col, al, h, ex, 36, 26)
        caps = ["Hints come in families. Access hints choose full scan or index.",
                "Join hints choose the join order, and the join method: nested loops, hash, or merge.",
                "Others enable parallel execution, direct path loads with append, or extra diagnostics."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    # 3 ALIAS TRAP
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The alias trap", SB(58), RED, a)
        code(d, 320, [("SELECT /*+ INDEX(accounts acc_ix) */ *", RED), ("FROM   accounts a", WHITE)], a, 30)
        ax = pr(lt, 1.5, 1.9) * fo
        d.rounded_rectangle((304, 334, 566, 374), 8, outline=mix(RED, ax * (.5 + .5 * math.sin(t * 8))), width=4)
        d.rounded_rectangle((393, 380, 423, 420), 8, outline=mix(YEL, ax), width=4)
        ct(d, 470, "table has alias a → \"accounts\" not found → ignored", SN(30), RED, ax)
        code(d, 580, [("SELECT /*+ INDEX(a acc_ix) */ *", GREEN), ("FROM   accounts a", WHITE)], pr(lt, 4.5, 4.9) * fo, 30)
        ct(d, 730, "✓ use the ALIAS", SB(40), GREEN, pr(lt, 5, 5.4) * fo)
        card_list(d, 820, [("query block names (QB_NAME) for subqueries & views", CYAN, 8)], lt, fo, 80, 30)
        caps = ["The most common mistake: the table has an alias, but the hint uses the table name.",
                "Once a table has an alias, the hint must use that alias. Otherwise Oracle can't match it, and ignores it.",
                "For subqueries and views, name the query block with QB NAME, and point your hints at it."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 4 DANGER OVER TIME
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Why hints age badly", SB(56), YEL, a)
        gx0, gy0, gx1, gy1 = 130, 340, 970, 780
        d.line((gx0, gy1, gx1, gy1), fill=mix(DIM, a), width=3); d.line((gx0, gy0, gx0, gy1), fill=mix(DIM, a), width=3)
        d.text((gx0 + 10, gy0 - 10), "run time", font=SN(26), fill=mix(DIM, a))
        ct(d, gy1 + 10, "table size over months →", SN(26), DIM, a)
        p = pr(lt, .8, 5)
        hint = [(gx0 + x / 60 * (gx1 - gx0), gy1 - 20 - (x / 60) ** 2 * (gy1 - gy0 - 40)) for x in range(int(60 * p) + 1)]
        free = [(gx0 + x / 60 * (gx1 - gx0), gy1 - 20 - (x / 60) * .22 * (gy1 - gy0 - 40)) for x in range(int(60 * p) + 1)]
        if len(hint) > 1:
            d.line(hint, fill=mix(RED, a), width=6); d.line(free, fill=mix(GREEN, a), width=6)
        ct(d, 380, "hinted: frozen plan", SB(30), RED, pr(lt, 3, 3.4) * fo, 400)
        ct(d, 680, "optimizer: adapts", SB(30), GREEN, pr(lt, 3.5, 3.9) * fo, 800)
        card_list(d, 860, [("hint = YOUR knowledge today, forever", YEL, 6),
                           ("stats change, data grows, versions upgrade", WHITE, 8)], lt, fo, 80, 30)
        caps = ["A hint encodes what you knew on the day you wrote it.",
                "The data grows, distributions change, Oracle upgrades. The optimizer adapts its plan. The hinted plan stays frozen.",
                "That's how a perfect hint turns into a twenty five minute query six months later."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 5 GOOD HINTS
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Hints that are usually SAFE", SB(50), GREEN, a)
        good = [("GATHER_PLAN_STATISTICS", "measure, don't change the plan", .6),
                ("MONITOR", "real-time SQL monitoring", 1.8),
                ("APPEND", "direct path load in batch inserts", 3),
                ("PARALLEL(n)", "big batch / EOD jobs, on purpose", 4.2),
                ("RESULT_CACHE", "cache a small lookup (video 19)", 5.4)]
        for k, (h, w, st) in enumerate(good):
            y = 320 + k * 130; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 112), 16, fill=mix(CARD, al), outline=mix(GREEN, al), width=3)
            d.text((100, y + 14), "✓ " + h, font=MB(32), fill=mix(GREEN, al))
            d.text((140, y + 64), w, font=SN(28), fill=mix(WHITE, al))
        caps = ["Some hints don't fight the optimizer: they add measurement or describe intent.",
                "Gather plan statistics and monitor only measure. Append and parallel describe how a batch should run.",
                "Hints that force a join order or an index on OLTP queries are the risky ones."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 6 BETTER ALTERNATIVES
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Before you hint, try…", SB(56), CYAN, a)
        alt = [("1", "fix statistics & histograms", "video 15", CYAN, .6),
               ("2", "SQL plan baseline", "lock a proven plan, video 17", YEL, 2.4),
               ("3", "SQL patch", "add a hint WITHOUT changing code", PINK, 4.2),
               ("4", "rewrite the SQL", "functions on columns, video 28", GREEN, 6)]
        for k, (n, h, s_, col, st) in enumerate(alt):
            y = 320 + k * 160; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 140), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.ellipse((100, y + 40, 160, y + 100), fill=mix(col, al)); ct(d, y + 50, n, SB(34), BG, al, 130)
            d.text((190, y + 26), h, font=SB(34), fill=mix(col, al))
            d.text((190, y + 82), s_, font=SN(28), fill=mix(WHITE, al))
        code(d, 980, [("DBMS_SQLDIAG.CREATE_SQL_PATCH(sql_id, hint_text)", PINK)], pr(lt, 8, 8.4) * fo, 26)
        caps = ["First fix the cause: wrong statistics or missing histograms give wrong estimates.",
                "Need stability? A SQL plan baseline locks a proven plan, and still lets better plans be tested.",
                "Can't change the code? A SQL patch attaches a hint to a SQL ID from outside. And sometimes, simply rewrite the query."]
        caption(d, caps[0 if lt < 2.4 else 1 if lt < 4.2 else 2], pr(lt, .6, 1) * fo)

    # 7 HINT REPORT
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Was my hint USED?", SB(56), WHITE, a)
        code(d, 320, [("DBMS_XPLAN.DISPLAY_CURSOR(", CYAN), ("  format => 'ALLSTATS LAST +HINT_REPORT')", CYAN)], a, 28)
        code(d, 500, [("Hint Report: Total hints: 3", WHITE), ("  Used (2):  LEADING(b a)  USE_HASH(a)", GREEN),
                      ("  Unused (1): INDEX(accounts acc_ix)", RED), ("     E - Syntax error / unresolved alias", RED)],
             pr(lt, 1.5, 1.9) * fo, 28)
        ab = pr(lt, 5, 5.4) * fo
        glow_box(d, (110, 790, 970, 910), GREEN, ab, "Oracle 19c+: no more guessing", None, 36)
        caps = ["How do you know a hint was actually used? Add plus hint report to the display cursor format.",
                "Oracle lists every hint as used or unused, and tells you why: a syntax error, or an alias it couldn't resolve.",
                "Available from Oracle nineteen c. Always check it after adding a hint."]
        caption(d, caps[0 if lt < 1.5 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("/*+ … */", "→ typo = silently ignored"), ("Alias", "→ hint must use it"),
                          ("Danger", "→ plan frozen, data grows"), ("Safe", "→ stats, APPEND, PARALLEL"),
                          ("Better", "→ stats, baseline, SQL patch")],
              "A hint is a last resort, not a first fix. And always check the hint report.", 400)
    else:
        cta(d, t - T[9], "BULK COLLECT & FORALL", "10 minutes → 20 seconds", 58)
    return im

if __name__ == "__main__":
    preview(frame, T, "v30_sheet.png")

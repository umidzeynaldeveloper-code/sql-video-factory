from vhelp import *
from make_video14 import cyl

T = T10; DUR = T[-1]

def code(d, y, lines, a, fs=30, x0=80, x1=1000):
    h = 30 + len(lines) * (fs + 16)
    d.rounded_rectangle((x0, y, x1, y + h), 18, fill=mix((14, 20, 34), a), outline=mix(DIM, a * .5), width=2)
    for k, (tx, col) in enumerate(lines):
        d.text((x0 + 30, y + 18 + k * (fs + 16)), tx, font=MN(fs), fill=mix(col, a))
    return y + h

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Same query. 10 000 times a minute.", SB(46), WHITE, a)
        code(d, 310, [("SELECT rate FROM fx_rates", CYAN), ("WHERE ccy = 'USD';", CYAN)], a, 34)
        bar(d, 110, 560, 970, 40, pr(lt, .8, 2.2), RED, pr(lt, .6, 1) * fo, "every time: read blocks", "50 ms")
        bar(d, 110, 700, 970, 40, pr(lt, 2.6, 2.7) * .01, GREEN, pr(lt, 2.4, 2.8) * fo, "result cache", "0.1 ms ⚡")
        ct(d, 830, "Why compute the same answer twice?", SB(46), YEL, pr(lt, 3.2, 3.6) * fo)
        caption(d, "Oracle can remember the ANSWER itself. That's the result cache.", pr(lt, 3.8, 4.2) * fo)

    # 1 CONCEPT
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "A cache of ANSWERS", SB(58), WHITE, a)
        d.rounded_rectangle((60, 310, 1020, 720), 28, outline=mix(DIM, a * .7), width=3)
        d.text((90, 322), "SGA · SHARED POOL", font=SB(28), fill=mix(DIM, a))
        a1 = pr(lt, .6, 1) * fo; a2 = pr(lt, 2, 2.4) * fo
        glow_box(d, (90, 380, 500, 690), OFFB, a1)
        ct(d, 410, "BUFFER CACHE", SB(32), CYAN, a1, 295); ct(d, 455, "data BLOCKS", SN(28), WHITE, a1, 295)
        for k in range(6):
            x = 130 + (k % 3) * 115; y = 530 + (k // 3) * 70
            d.rounded_rectangle((x, y, x + 95, y + 52), 8, fill=mix(OFFB, a1 * .8))
        glow_box(d, (580, 380, 990, 690), GREEN, a2)
        ct(d, 410, "RESULT CACHE", SB(32), GREEN, a2, 785); ct(d, 455, "final RESULTS", SN(28), WHITE, a2, 785)
        ar = pr(lt, 3.5, 3.9) * fo
        if ar > 0:
            for k, (q, r) in enumerate([("USD rate", "1.70"), ("branches", "42 rows"), ("EUR rate", "1.85")]):
                y = 500 + k * 58
                d.rounded_rectangle((610, y, 960, y + 48), 10, fill=mix(CARD, ar))
                d.text((630, y + 8), q, font=SN(26), fill=mix(WHITE, ar))
                d.text((850, y + 8), r, font=SB(26), fill=mix(YEL, ar))
        card_list(d, 790, [("buffer cache: rows still need joins, sorts, functions", DIM, 5),
                           ("result cache: the finished answer, ready to return", GREEN, 6.5)], lt, fo, 80, 32)
        caps = ["The buffer cache keeps data blocks. The query still has to read, join, sort, and compute.",
                "The result cache, in the shared pool, keeps the FINISHED result of a query or function.",
                "Same query, same binds, same data? Oracle just returns the stored answer."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 2 HOW TO ENABLE
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Three ways to switch it on", SB(54), WHITE, a)
        a1 = pr(lt, .8, 1.2) * fo; a2 = pr(lt, 4.5, 4.9) * fo; a3 = pr(lt, 8.5, 8.9) * fo
        chip(d, 140, 340, "1", GREEN, a1, 34, BG)
        ct(d, 320, "hint, per query", SB(32), GREEN, a1, 560)
        code(d, 380, [("SELECT /*+ RESULT_CACHE */ rate", YEL), ("FROM fx_rates WHERE ccy = :c;", CYAN)], a1, 30)
        chip(d, 140, 610, "2", CYAN, a2, 34, BG)
        ct(d, 590, "table annotation", SB(32), CYAN, a2, 560)
        code(d, 650, [("ALTER TABLE fx_rates", CYAN), ("  RESULT_CACHE (MODE FORCE);", YEL)], a2, 30)
        chip(d, 140, 880, "3", PURP, a3, 34, BG)
        ct(d, 860, "PL/SQL function", SB(32), PURP, a3, 560)
        code(d, 920, [("FUNCTION get_rate(p VARCHAR2)", CYAN), ("  RETURN NUMBER RESULT_CACHE IS", YEL)], a3, 30)
        caps = ["The simplest way: add the RESULT_CACHE hint to one query.",
                "Or annotate a table, so every query on it uses the cache automatically.",
                "Or mark a PL/SQL function with RESULT_CACHE. We'll see that one in a moment."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 3 HIT / MISS FLOW
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "1st run: MISS · then: HIT", SB(54), WHITE, a)
        glow_box(d, (80, 330, 420, 470), CYAN, a, "SESSION", "SELECT …", 34, 28)
        glow_box(d, (620, 330, 1000, 470), GREEN, a, "RESULT CACHE", None, 34)
        cyl(d, 810, 900, 340, 170, OFFB, a, "DATAFILES", "fx_rates")
        miss = lt < 5.5
        if miss:
            flow(d, [(420, 400), (620, 400)], YEL, a, t, pr(lt, .8, 1.6))
            ct(d, 500, "not found → execute", SB(32), RED, pr(lt, 1.6, 2) * fo, 810)
            flow(d, [(810, 470), (810, 800)], OFFB, a, t, pr(lt, 2, 3))
            ct(d, 1030, "read · join · compute", SN(30), DIM, pr(lt, 3, 3.4) * fo, 810)
            ap = pr(lt, 3.6, 4) * fo
            d.rounded_rectangle((680, 560, 940, 620), 12, fill=mix(GREEN, ap))
            ct(d, 570, "stored ✓", SB(30), BG, ap, 810)
        else:
            n = int(min(9999, (lt - 5.5) * 1500)) + 2
            flow(d, [(420, 400), (620, 400)], GREEN, a, t, 1)
            flow(d, [(620, 440), (420, 440)], GREEN, a, t + .3, 1)
            ct(d, 520, f"HIT  #{n}", SB(56), GREEN, a, 540)
            ct(d, 610, "no block reads, no execution", SN(34), WHITE, pr(lt, 6, 6.4) * fo, 540)
            ct(d, 1160, "datafiles: idle", SB(36), DIM, pr(lt, 7, 7.4) * fo, 540)
        caps = ["The first execution finds nothing in the cache. So Oracle runs the query normally.",
                "Then it stores the result in the result cache.",
                "Every next execution with the same binds is a hit. The answer comes straight from memory."]
        caption(d, caps[0 if lt < 3.6 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 4 INVALIDATION
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Data changed? Cache knows.", SB(54), WHITE, a)
        code(d, 320, [("UPDATE fx_rates SET rate = 1.71", PINK), ("WHERE ccy = 'USD';  COMMIT;", PINK)], pr(lt, .6, 1) * fo, 30)
        inv = lt > 3
        col = RED if inv and lt < 8 else GREEN
        glow_box(d, (240, 560, 840, 760), col, a, "USD rate = 1.70" if lt < 8 else "USD rate = 1.71",
                 ("INVALID ✗" if inv else "PUBLISHED") if lt < 8 else "PUBLISHED ✓ (recomputed)", 40, 32)
        if 1.8 < lt < 3.2: flow(d, [(540, 470), (540, 560)], PINK, a, t, pr(lt, 1.8, 2.8))
        ct(d, 850, "→ next query recomputes once", SB(34), YEL, pr(lt, 5.5, 5.9) * fo)
        card_list(d, 960, [("✓ automatic: dependent results invalidated on COMMIT", GREEN, 8.5),
                           ("✓ you never read a stale answer", GREEN, 9.5)], lt, fo, 80, 32)
        caps = ["Someone updates the rate and commits.",
                "Oracle tracks which tables each cached result depends on, and marks the result invalid.",
                "The next query recomputes it once and caches the new answer. No stale data, ever."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 5 PL/SQL FUNCTION CACHE
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "PL/SQL function result cache", SB(50), PURP, a)
        code(d, 310, [("FUNCTION get_rate(p_ccy VARCHAR2)", CYAN), ("  RETURN NUMBER RESULT_CACHE IS", YEL),
                      ("BEGIN  SELECT rate INTO … ;", CYAN), ("END;", CYAN)], a, 28)
        ct(d, 600, "cache key = the ARGUMENTS", SB(36), WHITE, pr(lt, 2, 2.4) * fo)
        rows = [("get_rate('USD')", "1.70", 3), ("get_rate('EUR')", "1.85", 4), ("get_rate('GBP')", "2.15", 5)]
        for k, (q, r, st) in enumerate(rows):
            al = pr(lt, st, st + .4) * fo; y = 670 + k * 90
            d.rounded_rectangle((140, y, 940, y + 74), 14, fill=mix(CARD, al))
            d.text((170, y + 18), q, font=MN(32), fill=mix(CYAN, al))
            d.text((720, y + 18), "→ " + r, font=SB(34), fill=mix(YEL, al))
        ct(d, 970, "called from 1 000 000 rows → 3 real executions", SB(32), GREEN, pr(lt, 7, 7.4) * fo)
        caps = ["Mark a PL/SQL function as RESULT_CACHE, and Oracle caches its return value per set of arguments.",
                "Call get_rate for USD a million times from a big query: it really runs once per currency.",
                "And it's shared across ALL sessions, not just yours."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 9 else 2], pr(lt, .6, 1) * fo)

    # 6 GOOD vs BAD FIT
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Good fit vs bad fit", SB(56), WHITE, a)
        ag = pr(lt, .6, 1) * fo; ab = pr(lt, 5, 5.4) * fo
        glow_box(d, (60, 320, 520, 420), GREEN, ag, "✓ CACHE IT", None, 40)
        glow_box(d, (560, 320, 1020, 420), RED, ab, "✗ DON'T", None, 40)
        good = ["FX rates", "branch list", "product codes", "stable aggregates"]
        bad = ["transactions", "balances", "huge results", "one-off queries"]
        for k in range(4):
            y = 460 + k * 100
            ag2 = pr(lt, 1.2 + k * .8, 1.6 + k * .8) * fo; ab2 = pr(lt, 5.6 + k * .8, 6 + k * .8) * fo
            d.rounded_rectangle((60, y, 520, y + 80), 14, fill=mix((20, 50, 36), ag2))
            ct(d, y + 20, good[k], SB(32), WHITE, ag2, 290)
            d.rounded_rectangle((560, y, 1020, y + 80), 14, fill=mix((60, 22, 28), ab2))
            ct(d, y + 20, bad[k], SB(32), WHITE, ab2, 790)
        ct(d, 900, "small · read often · change rarely", SB(36), YEL, pr(lt, 4, 4.4) * fo)
        caps = ["Great for small, read-mostly lookups: rates, branches, codes, and summaries over stable data.",
                "Bad for hot tables like transactions and balances: every commit invalidates the cache.",
                "Huge results waste memory, and queries that never repeat never hit."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 7 MONITORING
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Is it working?", SB(58), WHITE, a)
        code(d, 310, [("SELECT name, status, scan_count", CYAN), ("FROM v$result_cache_objects;", CYAN)], a, 30)
        rows = [("fx_rates USD", "Published", "9 812", GREEN), ("branches", "Published", "4 120", GREEN), ("balances", "Invalid", "1", RED)]
        for k, (n, s, c, col) in enumerate(rows):
            al = pr(lt, 1.5 + k * .6, 1.9 + k * .6) * fo; y = 510 + k * 80
            d.rounded_rectangle((80, y, 1000, y + 66), 12, fill=mix(CARD, al))
            d.text((110, y + 16), n, font=SN(30), fill=mix(WHITE, al))
            d.text((480, y + 16), s, font=SB(30), fill=mix(col, al))
            d.text((800, y + 16), c, font=MB(30), fill=mix(YEL, al))
        card_list(d, 790, [("V$RESULT_CACHE_STATISTICS → find vs create count", CYAN, 5),
                           ("DBMS_RESULT_CACHE.MEMORY_REPORT", CYAN, 6.2),
                           ("RESULT_CACHE_MAX_SIZE → how much memory", CYAN, 7.4)], lt, fo, 80, 32)
        caps = ["V dollar result cache objects shows each cached result, its status, and how often it was reused.",
                "High scan count: great. Constantly invalid: that table doesn't belong in the cache.",
                "Check statistics and the memory report, and size it with result cache max size."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("RESULT_CACHE", "→ stores final answers"), ("1st run", "→ miss, compute, store"),
                          ("next runs", "→ hit, from memory"), ("COMMIT", "→ auto invalidation"),
                          ("best for", "→ small, read-mostly data")],
              "Don't compute the same answer twice. Cache it, and let Oracle keep it fresh.", 500)
    else:
        cta(d, t - T[9], "FRAGMENTATION & SHRINK", "why DELETE doesn't make a table smaller", 56)
    return im

if __name__ == "__main__":
    preview(frame, T, "v19_sheet.png")

from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def engines(d, a, y=330):
    glow_box(d, (70, y, 430, y + 170), PURP, a, "PL/SQL", "engine", 40, 28)
    glow_box(d, (650, y, 1010, y + 170), CYAN, a, "SQL", "engine", 40, 28)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        code(d, 230, [("FOR r IN (SELECT id FROM accounts) LOOP", YEL), ("  UPDATE accounts SET … WHERE id = r.id;", YEL),
                      ("END LOOP;   -- 1 000 000 rows", DIM)], a, 28)
        bar(d, 110, 470, 970, 44, pr(lt, .8, 2.6), RED, pr(lt, .6, 1) * fo, "row by row", "10 min")
        bar(d, 110, 610, 970, 44, pr(lt, 2.8, 3) * .033, GREEN, pr(lt, 2.6, 3) * fo, "BULK COLLECT + FORALL", "20 s")
        ct(d, 750, "Same logic. 30× faster.", SB(48), YEL, pr(lt, 3.3, 3.7) * fo)
        caption(d, "The secret is context switches. Let's count them.", pr(lt, 4, 4.4) * fo)

    # 1 CONTEXT SWITCH
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Two engines, one ping-pong", SB(50), WHITE, a)
        engines(d, a)
        if lt > 1.5:
            p = (t * 1.6) % 2
            x = lerp(430, 650, p) if p < 1 else lerp(650, 430, p - 1)
            d.ellipse((x - 22, 395, x + 22, 439), fill=mix(YEL, a))
        cnt = int(min(2000000, max(0, lt - 1.5) ** 3 * 6000)) // 2 * 2
        ct(d, 560, f"switches: {cnt:,}".replace(",", " "), MB(48), YEL, pr(lt, 1.5, 1.9) * fo)
        bar(d, 110, 690, 970, 40, cnt / 2000000, RED, pr(lt, 3, 3.4) * fo, "time lost switching", "")
        card_list(d, 820, [("1 row = 1 round trip PL/SQL ⇄ SQL", RED, 4.5),
                           ("1 M rows = 2 M switches", RED, 6.5),
                           ("fix: send work in BATCHES", GREEN, 8.5)], lt, fo, 80, 32)
        caps = ["PL/SQL code runs in the PL/SQL engine. Every SQL statement inside it runs in the SQL engine.",
                "Each time control passes between them, that's a context switch. A loop with one update per row pays that price again and again.",
                "A million rows means millions of switches. The fix: send the work in batches."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 2 BULK COLLECT
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "BULK COLLECT: fetch in one go", SB(48), GREEN, a)
        engines(d, a)
        if lt > 1.5:
            p = pr(lt, 1.5, 3.5)
            x = lerp(650, 430, p)
            for k in range(6):
                d.rounded_rectangle((x - 60 + k * 6, 380 + k * 12, x + 60 + k * 6, 410 + k * 12), 6, fill=mix(GREEN, a))
        ct(d, 520, "1 switch → 1 000 rows", SB(38), GREEN, pr(lt, 3.5, 3.9) * fo)
        code(d, 600, [("SELECT id, bal", CYAN), ("BULK COLLECT INTO l_ids, l_bals", GREEN), ("FROM accounts;", CYAN)], pr(lt, 5, 5.4) * fo, 30)
        ab = pr(lt, 7, 7.4) * fo
        for k in range(8):
            x = 110 + k * 108
            d.rounded_rectangle((x, 830, x + 96, 900), 8, fill=mix(PURP, ab))
            ct(d, 846, f"[{k + 1}]", SB(26), BG, ab, x + 48)
        ct(d, 920, "collection in PGA memory", SN(28), PURP, ab)
        caps = ["BULK COLLECT fetches many rows with a single context switch.",
                "Instead of one row per trip, a whole batch arrives at once.",
                "The rows land in a collection, an array in the session's memory, ready to process."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 3 LIMIT
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Always use LIMIT", SB(56), YEL, a)
        bar(d, 110, 360, 970, 44, pr(lt, .6, 3), RED, pr(lt, .4, .8) * fo, "no LIMIT: 50 M rows in PGA", "8 GB 💥".replace(" 💥", " !!"))
        bar(d, 110, 490, 970, 44, .05, GREEN, pr(lt, 3.2, 3.6) * fo, "LIMIT 1000", "~200 KB, constant")
        code(d, 600, [("OPEN c;", CYAN), ("LOOP", CYAN), ("  FETCH c BULK COLLECT INTO l_rows LIMIT 1000;", GREEN),
                      ("  EXIT WHEN l_rows.COUNT = 0;", YEL), ("  -- process 1 000 rows", DIM), ("END LOOP;", CYAN)],
             pr(lt, 4.5, 4.9) * fo, 26)
        caps = ["Without a limit, BULK COLLECT loads every row into memory. Fifty million rows can eat gigabytes of PGA.",
                "With LIMIT, you fetch a batch of a thousand, process it, then fetch the next. Memory stays small and constant.",
                "Exit when the collection count is zero, not with cursor not found, or you'll skip the last partial batch."]
        caption(d, caps[0 if lt < 3.2 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 4 FORALL
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "FORALL: send all DML at once", SB(48), CYAN, a)
        engines(d, a)
        if lt > 1.2:
            p = pr(lt, 1.2, 3.2)
            x = lerp(430, 650, p)
            for k in range(6):
                d.rounded_rectangle((x - 60 + k * 6, 380 + k * 12, x + 60 + k * 6, 410 + k * 12), 6, fill=mix(CYAN, a))
        code(d, 560, [("FORALL i IN 1 .. l_ids.COUNT", CYAN), ("  UPDATE accounts", WHITE),
                      ("     SET bal = l_bals(i)", WHITE), ("   WHERE id  = l_ids(i);", WHITE)], pr(lt, 3.5, 3.9) * fo, 30)
        ab = pr(lt, 6.5, 6.9) * fo
        ct(d, 830, "FORALL is NOT a loop: 1 statement, many binds", SB(32), YEL, ab)
        bar(d, 110, 920, 970, 40, pr(lt, 7.5, 8) * .03, GREEN, pr(lt, 7.3, 7.7) * fo, "switches per 1 000 rows", "1")
        caps = ["FORALL does the opposite: it sends a whole array of binds to the SQL engine in one trip.",
                "One update statement, executed for every element of the collection.",
                "It looks like a loop, but it isn't. It's one call with many bind values. One switch per batch instead of per row."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 5 SAVE EXCEPTIONS
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "One bad row? Don't stop.", SB(52), PINK, a)
        code(d, 320, [("FORALL i IN 1 .. l_ids.COUNT SAVE EXCEPTIONS", PINK)], a, 28)
        for k in range(10):
            x = 90 + k * 92; bad = k in (3, 7)
            done = lt > 1.5 + k * .4
            col = (RED if bad else GREEN) if done else OFFB
            d.rounded_rectangle((x, 450, x + 80, 530), 10, fill=mix(col, a))
            ct(d, 470, "✗" if bad and done else ("✓" if done else str(k + 1)), SB(30), BG, a, x + 40)
        ct(d, 560, "all good rows processed ✓", SB(34), GREEN, pr(lt, 6, 6.4) * fo)
        code(d, 640, [("EXCEPTION WHEN e_bulk_errors THEN", CYAN),
                      ("  FOR j IN 1 .. SQL%BULK_EXCEPTIONS.COUNT LOOP", CYAN),
                      ("    log( SQL%BULK_EXCEPTIONS(j).ERROR_INDEX,", WHITE),
                      ("         SQL%BULK_EXCEPTIONS(j).ERROR_CODE );", WHITE)], pr(lt, 7, 7.4) * fo, 26)
        caps = ["By default, the first failing row stops FORALL, and the rest of the batch is not processed.",
                "Add SAVE EXCEPTIONS, and Oracle keeps going. Every good row is processed, the failures are remembered.",
                "At the end, it raises ORA twenty four three eighty one, and SQL percent BULK EXCEPTIONS tells you which index failed, and why."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 6 ROWCOUNT + SPARSE
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Useful extras", SB(58), GREEN, a)
        glow_box(d, (70, 320, 1010, 470), CYAN, pr(lt, .6, 1) * fo, "SQL%BULK_ROWCOUNT(i)", "rows affected by the i-th element", 36, 28)
        cells = [1, 1, 0, 1, 0, 1, 1, 0]
        for k, v in enumerate(cells):
            x = 110 + k * 108; al = pr(lt, 1.5 + k * .2, 1.9 + k * .2) * fo
            d.rounded_rectangle((x, 500, x + 96, 570), 8, fill=mix(GREEN if v else OFFB, al))
            ct(d, 515, str(v), SB(30), BG, al, x + 48)
        glow_box(d, (70, 640, 1010, 790), PURP, pr(lt, 4.5, 4.9) * fo, "INDICES OF / VALUES OF", "sparse collections, gaps allowed", 36, 28)
        for k in range(8):
            x = 110 + k * 108; al = pr(lt, 5.5, 5.9) * fo
            gap = k in (2, 5)
            d.rounded_rectangle((x, 820, x + 96, 890), 8, fill=mix(OFFB if gap else PURP, al), outline=mix(DIM, al), width=2)
            ct(d, 835, "—" if gap else f"[{k + 1}]", SB(26), BG if not gap else DIM, al, x + 48)
        caps = ["SQL percent BULK ROWCOUNT tells you how many rows each element of the FORALL changed. Zero means its key wasn't found.",
                "If you deleted elements and your collection has gaps, a plain range fails.",
                "Use INDICES OF to skip the gaps, or VALUES OF to drive FORALL from a list of positions."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 7 PURE SQL FIRST
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Even faster: no loop at all", SB(50), YEL, a)
        bars = [("row-by-row loop", 1, RED, "10 min"), ("BULK + FORALL", .033, YEL, "20 s"), ("one SQL statement", .012, GREEN, "7 s")]
        for k, (nm, p, col, v) in enumerate(bars):
            bar(d, 110, 360 + k * 130, 970, 44, pr(lt, .8 + k * 1.2, 1.8 + k * 1.2) * p, col, pr(lt, .6 + k * 1.2, 1 + k * 1.2) * fo, nm, v)
        code(d, 760, [("UPDATE accounts a", GREEN), ("   SET bal = (SELECT … )", GREEN), (" WHERE …;   -- or MERGE", GREEN)], pr(lt, 4.5, 4.9) * fo, 30)
        glow_box(d, (110, 960, 970, 1080), GREEN, pr(lt, 7.5, 7.9) * fo, "SQL if you can · BULK if you must", None, 36)
        caps = ["Bulk processing is great. But the fastest loop is no loop at all.",
                "If the logic fits in one UPDATE, INSERT SELECT, or MERGE, the SQL engine does everything in one call.",
                "The rule: do it in SQL if you can. If you need PL/SQL logic per row, use BULK COLLECT with LIMIT, and FORALL."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Switch", "→ PL/SQL ⇄ SQL costs time"), ("BULK COLLECT", "→ fetch batches"),
                          ("LIMIT", "→ keep PGA small"), ("FORALL", "→ DML in one call"),
                          ("SAVE EXC.", "→ don't stop on bad rows")],
              "Fewer trips, faster code. And if one SQL can do it, use one SQL.", 460)
    else:
        cta(d, t - T[9], "PGA, SORTS & TEMP", "why ORA-01652 wakes you up at 3 AM", 64)
    return im

if __name__ == "__main__":
    preview(frame, T, "v31_sheet.png")

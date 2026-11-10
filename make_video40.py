from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "\"Top 10 biggest payments\"", SB(52), WHITE, a)
        code(d, 320, [("SELECT * FROM payments", CYAN), ("WHERE ROWNUM <= 10", YEL), ("ORDER BY amount DESC;", CYAN)], a, 32)
        ab = pr(lt, 2, 2.4) * fo
        glow_box(d, (120, 600, 960, 760), RED, ab, "10 RANDOM rows, sorted", "not the 10 biggest", 40, 30)
        caption(d, "Looks right, runs fast, returns the wrong rows. Pagination in Oracle, done properly.", pr(lt, 3, 3.4) * fo)

    # 1 ROWNUM BEFORE ORDER BY
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "ROWNUM comes BEFORE ORDER BY", SB(48), YEL, a)
        steps = [("1. read rows", CYAN), ("2. ROWNUM 1, 2, 3 …", YEL), ("3. stop at 10", PINK), ("4. ORDER BY those 10", GREEN)]
        for k, (s, col) in enumerate(steps):
            y = 320 + k * 150; al = pr(lt, .6 + k * 1.2, 1 + k * 1.2) * fo
            glow_box(d, (200, y, 880, y + 110), col, al, s, None, 38)
            if k < 3: flow(d, [(540, y + 110), (540, y + 150)], col, al, t, pr(lt, 1 + k * 1.2, 1.6 + k * 1.2))
        card_list(d, 950, [("the sort only sees the first 10 rows Oracle found", RED, 7)], lt, fo, 80, 30)
        caps = ["Oracle numbers the rows as it reads them, before any sorting happens.",
                "It stops at ten, and only then sorts those ten. Which ten? Whatever it found first.",
                "So the result depends on the plan, and it can change tomorrow."]
        caption(d, caps[0 if lt < 2.4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 2 ROWNUM > 1 TRAP
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "WHERE ROWNUM > 1 → 0 rows", SB(52), RED, a)
        rows = ["row A", "row B", "row C", "row D"]
        for k, r in enumerate(rows):
            y = 340 + k * 120; al = pr(lt, .8 + k * 1.2, 1.2 + k * 1.2) * fo
            d.rounded_rectangle((120, y, 960, y + 100), 16, fill=mix(CARD, al), outline=mix(RED, al), width=3)
            d.text((150, y + 28), r + "  →  gets ROWNUM 1", font=MB(32), fill=mix(WHITE, al))
            d.text((800, y + 26), "✗", font=SB(40), fill=mix(RED, al))
        card_list(d, 860, [("a row only gets 2 after a row got 1", YEL, 6.5),
                           ("ROWNUM = 1 ✓   ROWNUM <= n ✓   ROWNUM > n ✗", CYAN, 8.5)], lt, fo, 80, 30)
        caps = ["The first row gets ROWNUM one. It fails the filter, so it's thrown away.",
                "The next row becomes number one again, and fails again. Nothing ever reaches two.",
                "ROWNUM works for equals one, or less than n. Never for greater than."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 3 CORRECT OLD WAY
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Before 12c: sort first, then cut", SB(48), GREEN, a)
        code(d, 300, [("SELECT * FROM (", WHITE), ("  SELECT * FROM payments", CYAN), ("  ORDER BY amount DESC", GREEN),
                      (")", WHITE), ("WHERE ROWNUM <= 10;", YEL)], a, 32)
        ap = pr(lt, 4, 4.4) * fo
        glow_box(d, (120, 700, 960, 840), CYAN, ap, "plan: SORT ORDER BY STOPKEY", "keeps only the top 10 while sorting", 34, 26)
        caption(d, ["Put the order by inside an inline view, and apply ROWNUM outside. Now you get the real top ten.",
                    "Oracle is smart about it: sort order by stopkey keeps only ten rows in memory while it sorts."][0 if lt < 4 else 1], pr(lt, .6, 1) * fo)

    # 4 FETCH FIRST
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "12c+: FETCH FIRST", SB(56), CYAN, a)
        code(d, 300, [("SELECT * FROM payments", CYAN), ("ORDER BY amount DESC", GREEN), ("FETCH FIRST 10 ROWS ONLY;", YEL)], a, 32)
        code(d, 560, [("OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;", PURP), ("FETCH FIRST 10 ROWS WITH TIES;", PINK)], pr(lt, 3.5, 3.9) * fo, 30)
        card_list(d, 780, [("standard SQL, ORDER BY runs first", GREEN, 6),
                           ("WITH TIES: the 10th value repeats? you get all of them", PINK, 8)], lt, fo, 80, 30)
        caps = ["Since twelve c, write it the standard way: order by, then fetch first ten rows only.",
                "Offset skips rows for page three. With ties also returns rows equal to the last one.",
                "The order by always happens first, so the result is the one you meant."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 5 OFFSET COST
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Deep pages get slower and slower", SB(48), RED, a)
        pages = [("page 1", .02, GREEN, "read 10"), ("page 100", .25, YEL, "read 1,000 → keep 10"),
                 ("page 10,000", .95, RED, "read 100,000 → keep 10")]
        for k, (lb, p, col, ex) in enumerate(pages):
            y = 380 + k * 170; al = pr(lt, .5 + k * 1, .9 + k * 1) * fo
            bar(d, 100, y, 980, 46, p * pr(lt, .5 + k, 1.6 + k), col, al, lb, None)
            d.text((100, y + 60), ex, font=SN(28), fill=mix(DIM, al))
        caption(d, ["OFFSET doesn't jump. To return page ten thousand, Oracle reads and sorts every row before it.",
                    "Then it throws away ninety nine thousand nine hundred and ninety of them."][0 if lt < 6 else 1], pr(lt, .6, 1) * fo)

    # 6 KEYSET PAGINATION
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Keyset: continue after the last row", SB(46), GREEN, a)
        code(d, 300, [("SELECT * FROM payments", CYAN),
                      ("WHERE created < :last_created", YEL),
                      ("   OR (created = :last_created AND id < :last_id)", YEL),
                      ("ORDER BY created DESC, id DESC", GREEN),
                      ("FETCH FIRST 10 ROWS ONLY;", CYAN)], a, 26)
        ai = pr(lt, 4, 4.4) * fo
        glow_box(d, (120, 700, 960, 840), GREEN, ai, "index (created, id)", "jump straight to the page → same speed on every page", 34, 26)
        card_list(d, 900, [("no 'jump to page 517', but perfect for 'load more'", CYAN, 8)], lt, fo, 80, 30)
        caps = ["Keyset pagination remembers where the last page ended, and asks only for the rows after it.",
                "With an index on created and id, Oracle jumps straight there. Page ten thousand is as fast as page one.",
                "You lose random page numbers, but infinite scroll and load more work perfectly."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 7 STABLE ORDER
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Same row on two pages?", SB(52), YEL, a)
        glow_box(d, (70, 320, 500, 520), CYAN, a, "page 1", "… 500 AZN (id 7)", 36, 28)
        glow_box(d, (580, 320, 1010, 520), PINK, pr(lt, 1, 1.4) * fo, "page 2", "500 AZN (id 7) again!", 36, 28)
        code(d, 600, [("ORDER BY amount DESC          ✗", RED), ("ORDER BY amount DESC, id DESC ✓", GREEN)], pr(lt, 4, 4.4) * fo, 32)
        caption(d, ["Many rows have the same amount. Without a unique order, ties can come back in any order on each query.",
                    "Always add a unique column, like the id, as the last sort key. Then every page is stable."][0 if lt < 4 else 1], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("ROWNUM", "→ before ORDER BY"), ("ROWNUM > 1", "→ always 0 rows"),
                          ("FETCH FIRST", "→ sort, then cut"), ("Deep OFFSET", "→ slow, use keyset"),
                          ("ORDER BY", "→ end with a unique key")],
              "Sort first, cut second, and continue from the last row.", 420)
    else:
        cta(d, t - T[9], "MUTATING TABLE", "ORA-04091 in triggers", 64)
    return im


if __name__ == "__main__":
    preview(frame, T, "v40_sheet.png")

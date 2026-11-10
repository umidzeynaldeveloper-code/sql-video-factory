from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "50 users run the same report", SB(50), WHITE, a)
        ct(d, 300, "…all writing to one scratch table?", SB(40), YEL, pr(lt, .8, 1.2) * fo)
        for k in range(10):
            x = 140 + (k % 5) * 170; y = 400 + (k // 5) * 150; al = pr(lt, 1 + k * .1, 1.3 + k * .1) * fo
            d.ellipse((x, y, x + 100, y + 100), fill=mix(CARD, al), outline=mix(CYAN, al), width=3)
            ct(d, y + 28, f"S{k + 1}", SB(32), CYAN, al, x + 50)
        caption(d, "Temporary tables: one definition, private data for every session. No clean-up, no collisions.", pr(lt, 3, 3.4) * fo)

    # 1 SESSION-PRIVATE DATA
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Global temporary table", SB(54), CYAN, a)
        code(d, 300, [("CREATE GLOBAL TEMPORARY TABLE tmp_report (", CYAN), ("  account_id NUMBER, total NUMBER", WHITE), (") ON COMMIT PRESERVE ROWS;", YEL)], a, 28)
        glow_box(d, (300, 540, 780, 640), PURP, pr(lt, 2, 2.4) * fo, "definition: shared, permanent", None, 32)
        for k, (nm, col, rows) in enumerate((("Session A", GREEN, "3 rows"), ("Session B", PINK, "7 rows"), ("Session C", YEL, "0 rows"))):
            x = 70 + k * 330; al = pr(lt, 3.5 + k * .6, 3.9 + k * .6) * fo
            flow(d, [(540, 640), (x + 145, 720)], col, al, t, pr(lt, 3.5 + k * .6, 4.2 + k * .6))
            glow_box(d, (x, 720, x + 290, 860), col, al, nm, rows, 32, 28)
        card_list(d, 920, [("data lives in TEMP, visible only to its session", GREEN, 7.5)], lt, fo, 80, 30)
        caps = ["You create a global temporary table once, like any other table.",
                "The definition is shared by everyone. The rows are not.",
                "Each session sees only its own rows, stored in the temp tablespace. No locks between users."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 2 ON COMMIT
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "When do the rows disappear?", SB(52), YEL, a)
        glow_box(d, (70, 330, 1010, 520), CYAN, pr(lt, .5, .9) * fo, "ON COMMIT DELETE ROWS (default)", "COMMIT → rows gone · scratch inside one transaction", 34, 26)
        glow_box(d, (70, 570, 1010, 760), GREEN, pr(lt, 4, 4.4) * fo, "ON COMMIT PRESERVE ROWS", "rows stay until the session ends (or you delete)", 34, 26)
        card_list(d, 830, [("TRUNCATE on a GTT → only YOUR rows", PURP, 8)], lt, fo, 80, 30)
        caps = ["On commit delete rows is the default. A commit empties the table for that session.",
                "On commit preserve rows keeps the data until the session logs out.",
                "Even truncate is private: it removes only your own rows."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 3 LESS REDO
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Why it's fast: less redo", SB(52), GREEN, a)
        bars = [("normal table", .9, RED, "redo for data + undo"), ("GTT", .35, YEL, "undo only (undo makes redo)"),
                ("GTT + TEMP_UNDO_ENABLED (12c)", .05, GREEN, "undo in TEMP → almost no redo")]
        for k, (lb, p, col, ex) in enumerate(bars):
            y = 380 + k * 170; al = pr(lt, .5 + k * 1.5, .9 + k * 1.5) * fo
            bar(d, 100, y, 980, 46, p * pr(lt, .5 + k * 1.5, 1.6 + k * 1.5), col, al, lb, None)
            d.text((100, y + 60), ex, font=SN(28), fill=mix(DIM, al))
        caps = ["Nobody needs to recover your scratch data after a crash, so the rows themselves create no redo.",
                "Undo is still written, and undo produces redo. In twelve c, temp undo enabled moves that undo into temp too.",
                "Result: far less log traffic for big intermediate results."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 4 STATS
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Statistics: 10 rows or 1 million?", SB(50), PURP, a)
        glow_box(d, (70, 330, 500, 480), GREEN, a, "Session A", "10 rows", 36, 28)
        glow_box(d, (580, 330, 1010, 480), RED, a, "Session B", "1 000 000 rows", 36, 28)
        card_list(d, 560, [("one shared plan can't fit both", RED, 2),
                           ("12c+: session-private statistics (default)", GREEN, 4.5),
                           ("gather stats in the session after loading", CYAN, 6.5),
                           ("or let dynamic sampling look at it", YEL, 8.5)], lt, fo, 90, 30)
        caps = ["The same temporary table can hold ten rows in one session and a million in another.",
                "Since twelve c, statistics on temporary tables are private to the session by default.",
                "Gather them right after you load the data, or let dynamic sampling estimate the size."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 5 CONNECTION POOL TRAP
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Trap: connection pools", SB(54), RED, a)
        glow_box(d, (320, 330, 760, 450), PURP, a, "pooled session #7", None, 32)
        glow_box(d, (70, 560, 500, 700), CYAN, pr(lt, 1.5, 1.9) * fo, "User 1", "loads 500 rows", 34, 26)
        flow(d, [(285, 560), (500, 450)], CYAN, pr(lt, 1.5, 1.9) * fo, t, pr(lt, 1.5, 2.2))
        glow_box(d, (580, 560, 1010, 700), RED, pr(lt, 4, 4.4) * fo, "User 2", "sees User 1's rows!", 34, 26)
        flow(d, [(795, 560), (600, 450)], RED, pr(lt, 4, 4.4) * fo, t, pr(lt, 4, 4.7))
        card_list(d, 780, [("PRESERVE ROWS + pool = leftovers", RED, 6.5), ("fix: DELETE / TRUNCATE before use, or DELETE ROWS", GREEN, 8)], lt, fo, 80, 30)
        caps = ["Applications reuse database sessions from a pool. The session never logs out.",
                "With preserve rows, the next user of that session finds the previous user's rows.",
                "Clean the table at the start of every call, or use on commit delete rows."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 6 PRIVATE TEMPORARY TABLES 18c
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "18c+: private temporary tables", SB(50), CYAN, a)
        code(d, 300, [("CREATE PRIVATE TEMPORARY TABLE ora$ptt_calc (", CYAN), ("  id NUMBER, amount NUMBER", WHITE), (") ON COMMIT DROP DEFINITION;", YEL)], a, 27)
        card_list(d, 520, [("definition AND data private to the session", GREEN, 2.5),
                           ("name must start with ORA$PTT_", YEL, 4.5),
                           ("DROP DEFINITION → gone at commit", PURP, 6.5),
                           ("PRESERVE DEFINITION → gone at logout", CYAN, 8)], lt, fo, 90, 30)
        caps = ["Eighteen c added private temporary tables: even the definition belongs to one session.",
                "The name needs the ORA dollar P T T prefix, and the table lives only in memory.",
                "Drop definition removes it at commit, preserve definition at the end of the session."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 7 RULES
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Rules", SB(56), YEL, a)
        card_list(d, 330, [("✓ create the GTT once, in your install script", GREEN, .5),
                           ("✗ CREATE / DROP tables inside procedures", RED, 1.5),
                           ("✓ index it like a normal table", GREEN, 2.5),
                           ("✓ clean it at the start of each call", GREEN, 3.5),
                           ("? one SQL with WITH … could replace it", CYAN, 4.5)], lt, fo, 95, 30)
        caption(d, "And before you add a temp table, ask: can one SQL statement with a with clause do the same job?", pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("GTT", "→ shared definition"), ("Rows", "→ private, in TEMP"),
                          ("ON COMMIT", "→ DELETE / PRESERVE"), ("Pools", "→ clean before use"),
                          ("18c PTT", "→ private definition")],
              "One definition, private rows, and always start clean.", 420)
    else:
        cta(d, t - T[9], "PIPELINED FUNCTIONS", "SELECT from PL/SQL", 60)
    return im


if __name__ == "__main__":
    preview(frame, T, "v43_sheet.png")

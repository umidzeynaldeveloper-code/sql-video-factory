from vhelp import *
from make_video19 import code
from make_video14 import cyl

T = T10; DUR = T[-1]

def snap_line(d, y, a, n, lt, sel=None, x0=110, x1=970):
    d.line((x0, y, x1, y), fill=mix(DIM, a), width=4)
    step = (x1 - x0) / (n - 1)
    for k in range(n):
        x = x0 + k * step
        on = sel is not None and k in sel
        r = 16 if on else 11
        d.ellipse((x - r, y - r, x + r, y + r), fill=mix(YEL if on else CYAN, a))
    return step

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "\"Yesterday 14:00 it was SLOW\"", SB(50), WHITE, a)
        ct(d, 320, "…but today everything is fine.", SN(40), DIM, pr(lt, .8, 1.2) * fo)
        ax = pr(lt, 1.4, 1.8) * fo
        # load graph
        pts = []
        for k in range(25):
            x = 110 + k * 36; v = 120 + (230 if 13 <= k <= 15 else 0) + 30 * math.sin(k * 1.7)
            pts.append((x, 900 - v))
        n = int(len(pts) * pr(lt, 1.4, 3))
        if n > 1: d.line(pts[:n], fill=mix(CYAN, ax), width=6)
        d.line((100, 900, 990, 900), fill=mix(DIM, ax), width=3)
        ct(d, 920, "10:00            14:00            18:00", SN(30), DIM, ax)
        if lt > 3: d.rounded_rectangle((560, 480, 680, 905), 12, outline=mix(RED, pr(lt, 3, 3.4) * fo), width=5)
        glow_box(d, (190, 1010, 890, 1130), YEL, pr(lt, 3.6, 4) * fo, "AWR = the flight recorder", None, 40)
        caption(d, "Oracle already recorded what happened. You just need to read the AWR report.", pr(lt, 4, 4.4) * fo)

    # 1 HOW AWR WORKS
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Snapshots every hour", SB(56), WHITE, a)
        chip(d, 540, 345, "MMON", CYAN, pr(lt, .6, 1) * fo, 36, BG)
        n = int(min(9, max(2, (lt - .8) * 2.5)))
        snap_line(d, 480, a, 9, lt, set(range(n)))
        for k in range(min(n, 9)):
            x = 110 + k * 107.5
            d.text((x - 22, 510), f"#{k + 1}", font=SN(26), fill=mix(DIM, a))
        ab = pr(lt, 4, 4.4) * fo
        cyl(d, 540, 700, 460, 190, PURP, ab, "SYSAUX", "DBA_HIST_* views")
        card_list(d, 860, [("default: every 60 min, kept 8 days", CYAN, 5.5),
                           ("report = DIFFERENCE between 2 snapshots", YEL, 7),
                           ("needs Diagnostics Pack license (EE)", RED, 9.5)], lt, fo, 80, 32)
        caps = ["A background process, MMON, takes a snapshot of the database's statistics every hour.",
                "Snapshots are stored in SYSAUX and kept for eight days by default.",
                "An AWR report compares two snapshots: what happened between them. And check your license: AWR needs the Diagnostics Pack."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 2 GENERATE
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Get the report", SB(58), GREEN, a)
        code(d, 320, [("SQL> @?/rdbms/admin/awrrpt.sql", YEL)], a, 32)
        ap = pr(lt, 1.5, 1.9) * fo
        code(d, 450, [("report type:   html", CYAN), ("begin snap:    1405  (14:00)", WHITE),
                      ("end snap:      1406  (15:00)", WHITE)], ap, 30)
        snap_line(d, 760, pr(lt, 3, 3.4) * fo, 9, lt, {4, 5})
        if lt > 3.5:
            ab = pr(lt, 3.5, 3.9) * fo
            x0 = 110 + 4 * 107.5; x1 = 110 + 5 * 107.5
            d.rounded_rectangle((x0 - 30, 720, x1 + 30, 800), 14, outline=mix(YEL, ab), width=4)
            ct(d, 820, "the slow hour", SB(32), YEL, ab, (x0 + x1) / 2)
        card_list(d, 920, [("keep the window SHORT: just the problem", GREEN, 6),
                           ("on-demand: DBMS_WORKLOAD_REPOSITORY.CREATE_SNAPSHOT", CYAN, 8)], lt, fo, 80, 29)
        caps = ["Run awrrpt dot sql from SQL Plus and choose HTML.",
                "Pick the snapshots around the problem: begin at 14:00, end at 15:00.",
                "Keep the window short. A whole day hides a one-hour spike in the average."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 3 DB TIME
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Step 1: DB Time", SB(58), YEL, a)
        bar(d, 110, 380, 970, 44, pr(lt, .8, 1.6) * .125, CYAN, pr(lt, .6, 1) * fo, "Elapsed", "60 min")
        bar(d, 110, 520, 970, 44, pr(lt, 2, 3.5), RED, pr(lt, 1.8, 2.2) * fo, "DB Time", "480 min")
        ad = pr(lt, 4, 4.4) * fo
        glow_box(d, (110, 640, 970, 790), YEL, ad, "480 / 60 = 8 active sessions", "on average, all hour long", 40, 30)
        ac = pr(lt, 6.5, 6.9) * fo
        glow_box(d, (110, 830, 520, 960), CYAN, ac, "CPUs: 4", None, 40)
        glow_box(d, (560, 830, 970, 960), RED, pr(lt, 7.5, 7.9) * fo, "8 > 4: busy", None, 40)
        card_list(d, 1000, [("DB Time = time sessions spent working or waiting", WHITE, 9)], lt, fo, 80, 30)
        caps = ["Start with the header. Elapsed time is sixty minutes, but DB time is four hundred eighty.",
                "DB time divided by elapsed gives the average number of active sessions: eight.",
                "DB time counts CPU and waits. Eight active sessions on four CPUs is a busy database. Now: busy doing what?"]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 4 TOP EVENTS
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Step 2: Top 10 Foreground Events", SB(46), PINK, a)
        ev = [("db file sequential read", .45, RED, "45%"), ("DB CPU", .25, CYAN, "25%"),
              ("log file sync", .15, YEL, "15%"), ("enq: TX - row lock", .10, PURP, "10%")]
        for k, (nm, p, col, v) in enumerate(ev):
            y = 350 + k * 140; al = pr(lt, .8 + k * .6, 1.2 + k * .6) * fo
            bar(d, 110, y, 970, 44, pr(lt, 1 + k * .6, 2 + k * .6) * p / .45, col, al, nm, v)
        ah = pr(lt, 5, 5.4) * fo
        d.rounded_rectangle((90, 300, 990, 420), 16, outline=mix(RED, ah), width=5)
        card_list(d, 950, [("% DB time = where the hour went", WHITE, 6),
                           ("fix the BIGGEST bar first", GREEN, 8)], lt, fo, 80, 32)
        caps = ["Next, the top foreground events: where did that time go?",
                "Here, single-block reads take almost half of DB time. That's the bottleneck.",
                "Always attack the biggest bar first. Tuning a five percent event saves five percent at best."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 5 TOP SQL
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Step 3: SQL ordered by Elapsed Time", SB(44), CYAN, a)
        rows = [("7h2kq9x…", "62%", "EOD balance calc", RED), ("a91fz0c…", "11%", "account lookup", CYAN),
                ("c3m8w1p…", "6%", "fx_rates", CYAN), ("…", "21%", "everything else", DIM)]
        d.text((110, 330), "SQL_ID", font=SB(28), fill=mix(DIM, a))
        d.text((420, 330), "% DB Time", font=SB(28), fill=mix(DIM, a))
        d.text((640, 330), "module", font=SB(28), fill=mix(DIM, a))
        for k, (sid, pct, mod, col) in enumerate(rows):
            y = 380 + k * 100; al = pr(lt, .8 + k * .5, 1.2 + k * .5) * fo
            d.rounded_rectangle((90, y, 990, y + 80), 14, fill=mix(CARD, al), outline=mix(col, al * (1 if k == 0 else .3)), width=4 if k == 0 else 2)
            d.text((110, y + 22), sid, font=MN(30), fill=mix(WHITE, al))
            d.text((420, y + 22), pct, font=SB(32), fill=mix(col, al))
            d.text((640, y + 22), mod, font=SN(30), fill=mix(WHITE, al))
        ab = pr(lt, 4.5, 4.9) * fo
        glow_box(d, (160, 820, 920, 940), RED, ab, "ONE statement = 62% of the hour", None, 38)
        card_list(d, 990, [("check its plan: DBMS_XPLAN.DISPLAY_AWR", CYAN, 6.5),
                           ("also: by CPU, by Gets, by Reads, by Executions", YEL, 8.5)], lt, fo, 80, 30)
        caps = ["Then jump to SQL ordered by elapsed time. Which statements used that DB time?",
                "Often one statement dominates. Here, the end of day balance calculation takes sixty-two percent.",
                "Take its SQL ID and pull its plan from AWR. Other lists show the top SQL by CPU, gets, reads, and executions."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 6 EVENT CHEAT SHEET
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "What the top event tells you", SB(48), WHITE, a)
        rows = [("db file sequential read", "single-block reads: index lookups", RED),
                ("db file scattered read", "multiblock reads: full scans", PINK),
                ("log file sync", "waiting on COMMIT: too many commits", YEL),
                ("enq: TX - row lock", "sessions blocking each other", PURP),
                ("DB CPU", "busy CPU: heavy logic / logical reads", CYAN)]
        for k, (e, m, col) in enumerate(rows):
            y = 330 + k * 150; al = pr(lt, .6 + k * 1.4, 1 + k * 1.4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 130), 16, fill=mix(CARD, al))
            d.text((100, y + 18), e, font=MB(32), fill=mix(col, al))
            d.text((100, y + 70), "→ " + m, font=SN(30), fill=mix(WHITE, al))
        caps = ["Learn the top events. Sequential read means single block reads, usually index lookups. Scattered read means full scans.",
                "Log file sync means sessions are waiting on commit, often from committing every row. Remember the redo video.",
                "Enqueue TX row lock means sessions are blocking each other. High DB CPU means heavy logic or too many logical reads."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 7 COMPARE / ADDM / ASH
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "More tools from the same data", SB(48), GREEN, a)
        glow_box(d, (70, 330, 1010, 480), CYAN, pr(lt, .6, 1) * fo, "awrddrpt.sql", "good hour vs bad hour, side by side", 36, 30)
        glow_box(d, (70, 520, 1010, 670), YEL, pr(lt, 3, 3.4) * fo, "ADDM", "automatic findings + recommendations", 36, 30)
        glow_box(d, (70, 710, 1010, 860), PINK, pr(lt, 6, 6.4) * fo, "ASH (ashrpt.sql)", "per-second samples: short spikes", 36, 30)
        card_list(d, 920, [("no license? Statspack: free, similar idea", GREEN, 9)], lt, fo, 80, 30)
        caps = ["The compare report puts a good hour next to a bad hour. What changed jumps out immediately.",
                "ADDM reads the same snapshots and writes findings for you: the cause, and what to do.",
                "For a two-minute spike, use ASH: active session samples every second. No Diagnostics Pack? Statspack is the free alternative."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Snapshot", "→ every hour, diff = report"), ("DB Time", "→ ÷ elapsed = load"),
                          ("Top Events", "→ where time went"), ("Top SQL", "→ who spent it"),
                          ("ASH / ADDM", "→ spikes & advice")],
              "Read in order: DB time, top events, top SQL. Then fix the biggest bar first.", 440)
    else:
        cta(d, t - T[9], "UNDO vs REDO", "the deep dive", 70)
    return im

if __name__ == "__main__":
    preview(frame, T, "v21_sheet.png")

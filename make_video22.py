from vhelp import *
from make_video19 import code
from make_video14 import cyl

T = T10; DUR = T[-1]

def ring(d, cx, cy, R, n, states, a, lbl=True, hl=None):
    """states: list of 'A' active, 'U' unexpired, 'E' expired"""
    cols = {"A": RED, "U": YEL, "E": GREEN}
    for k in range(n):
        an = math.radians(-90 + k * 360 / n)
        x, y = cx + R * math.cos(an), cy + R * math.sin(an)
        col = cols[states[k]]
        r = 52 if hl == k else 44
        d.ellipse((x - r, y - r, x + r, y + r), fill=mix(col, a * .9), outline=mix(WHITE, a if hl == k else 0), width=5)
        if lbl: ct(d, y - 18, states[k], SB(30), BG, a, x)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Two journals. Opposite directions.", SB(48), WHITE, a)
        au = pr(lt, .8, 1.2) * fo; ar = pr(lt, 1.6, 2) * fo
        glow_box(d, (80, 380, 500, 560), PURP, au, "UNDO", "how it WAS", 52, 32)
        glow_box(d, (580, 380, 1000, 560), PINK, ar, "REDO", "what CHANGED", 52, 32)
        if lt > 1.2: arrow(d, 440, 640, 140, 640, PURP, au, 10)
        if lt > 2: arrow(d, 640, 640, 940, 640, PINK, ar, 10)
        ct(d, 680, "← go back", SB(34), PURP, au, 290); ct(d, 680, "go forward →", SB(34), PINK, ar, 790)
        ct(d, 820, "Why does Oracle need BOTH?", SB(48), YEL, pr(lt, 3, 3.4) * fo)
        caption(d, "Last time we saw them side by side. Today: how each one really works inside.", pr(lt, 3.6, 4) * fo)

    # 1 LIFE OF AN UPDATE
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "One UPDATE, four steps", SB(54), WHITE, a)
        code(d, 310, [("UPDATE acc SET bal = 500", YEL), ("WHERE id = 7;   -- bal was 1000", DIM)], a, 30)
        steps = [("1", "undo record: bal = 1000", PURP, 1.5), ("2", "redo for the UNDO change", PINK, 3.5),
                 ("3", "redo for the DATA change", PINK, 5.5), ("4", "block in cache: bal = 500", CYAN, 7.5)]
        for k, (n, tx, col, st) in enumerate(steps):
            y = 480 + k * 130; al = pr(lt, st, st + .4) * fo
            d.ellipse((90, y, 180, y + 90), fill=mix(col, al))
            ct(d, y + 22, n, SB(40), BG, al, 135)
            d.rounded_rectangle((210, y, 990, y + 90), 16, fill=mix(CARD, al), outline=mix(col, al * .6), width=3)
            d.text((240, y + 24), tx, font=SN(34), fill=mix(WHITE, al))
        ct(d, 1020, "redo protects undo too!", SB(36), YEL, pr(lt, 9.5, 9.9) * fo)
        caps = ["First, Oracle writes an undo record with the old value: balance was one thousand.",
                "Writing undo is itself a change, so it generates redo. Then the data change gets its own redo.",
                "Only then is the block changed in the buffer cache. Redo protects both the data and the undo."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 2 REDO RECORD ANATOMY
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Inside a REDO record", SB(54), PINK, a)
        d.rounded_rectangle((70, 320, 1010, 760), 24, outline=mix(PINK, a), width=4, fill=mix(CARD, a * .5))
        d.text((100, 340), "REDO RECORD   ·   SCN 1 000 205", font=MB(30), fill=mix(PINK, a))
        cvs = [("change vector 1", "undo block 0x3a: store bal=1000", PURP, 1.5),
               ("change vector 2", "data block 0x81, row 7: bal=500", CYAN, 3)]
        for k, (h, tx, col, st) in enumerate(cvs):
            y = 410 + k * 160; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((100, y, 980, y + 130), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((130, y + 18), h, font=SB(30), fill=mix(col, al))
            d.text((130, y + 70), tx, font=MN(28), fill=mix(WHITE, al))
        ab = pr(lt, 5.5, 5.9) * fo
        glow_box(d, (70, 800, 1010, 930), YEL, ab, "no SQL inside: only BLOCK changes", "physical: which block, which bytes", 36, 28)
        card_list(d, 970, [("log buffer → LGWR → online redo log", PINK, 8.5)], lt, fo, 80, 32)
        caps = ["A redo record is stamped with an SCN, the database's clock, and holds change vectors.",
                "Each change vector describes one block change: one for the undo block, one for the data block.",
                "There's no SQL in redo. It's physical: which block and which bytes. That's why replay is fast and exact."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 3 UNDO SEGMENTS RING
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "UNDO is a ring of extents", SB(52), PURP, a)
        st = list("AAUUUEEE")
        if lt > 6: st = list("EAAUUUUE") if lt < 8 else list("EEAAUUUU")
        ring(d, 540, 590, 210, 8, st, a, hl=1 if 6 < lt < 8 else (2 if lt >= 8 else None))
        ct(d, 565, "UNDO", SB(40), WHITE, a)
        leg = [("A  ACTIVE: uncommitted, never overwrite", RED, 1.5),
               ("U  UNEXPIRED: committed, kept for readers", YEL, 3),
               ("E  EXPIRED: free to reuse", GREEN, 4.5)]
        card_list(d, 870, leg, lt, fo, 80, 31)
        caps = ["Undo lives in undo segments, in the undo tablespace. Each segment is a ring of extents.",
                "Active undo belongs to uncommitted transactions. Unexpired undo is committed, but kept for readers. Expired undo is free.",
                "As transactions run, the ring moves forward and reuses expired extents first."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 4 READ CONSISTENCY
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "UNDO's second job: readers", SB(52), CYAN, a)
        # SCN timeline
        d.line((110, 400, 970, 400), fill=mix(DIM, a), width=4)
        for x, lb, col, st in [(200, "query starts\nSCN 100", CYAN, .6), (620, "row updated\nSCN 105", PINK, 2)]:
            al = pr(lt, st, st + .4) * fo
            d.ellipse((x - 14, 386, x + 14, 414), fill=mix(col, al))
            for j, ln in enumerate(lb.split("\n")): ct(d, 430 + j * 38, ln, SN(28), col, al, x)
        glow_box(d, (80, 560, 500, 740), PINK, pr(lt, 3, 3.4) * fo, "current block", "bal = 500 @105", 34, 30)
        glow_box(d, (580, 560, 1000, 740), CYAN, pr(lt, 5, 5.4) * fo, "CR copy", "bal = 1000 @100", 34, 30)
        if lt > 4.5: flow(d, [(500, 650), (580, 650)], PURP, a, t, pr(lt, 4.5, 5.2))
        ct(d, 765, "+ undo applied", SB(30), PURP, pr(lt, 4.5, 4.9) * fo)
        glow_box(d, (190, 860, 890, 970), GREEN, pr(lt, 7.5, 7.9) * fo, "readers never block writers", None, 38)
        caps = ["A query that starts at SCN one hundred must see the data as of one hundred, even if rows change later.",
                "When it reaches a block changed at SCN one hundred five, Oracle clones the block and applies undo to roll it back.",
                "The query gets a consistent read copy. No locks, no waiting. Readers never block writers."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 5 ORA-01555
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "ORA-01555: snapshot too old", SB(50), RED, a)
        bar(d, 110, 380, 970, 40, pr(lt, .6, 6), CYAN, pr(lt, .4, .8) * fo, "long report query", "2 h")
        bar(d, 110, 500, 970, 40, pr(lt, 1.5, 2.5) * .25, YEL, pr(lt, 1.2, 1.6) * fo, "UNDO_RETENTION", "15 min")
        ax = pr(lt, 3, 3.4) * fo
        glow_box(d, (110, 600, 970, 740), RED, ax, "needed undo was overwritten", "can't rebuild the old block", 36, 30)
        card_list(d, 790, [("raise UNDO_RETENTION ≥ longest query", GREEN, 5.5),
                           ("size the undo tablespace (autoextend)", GREEN, 6.5),
                           ("RETENTION GUARANTEE for critical reports", YEL, 7.5),
                           ("don't COMMIT inside a cursor loop you're fetching", CYAN, 8.5)], lt, fo, 80, 30)
        caps = ["A report runs for two hours, but undo is only kept for fifteen minutes.",
                "Other transactions reuse the expired undo. The report needs it to rebuild an old block, and it's gone: snapshot too old.",
                "Size undo for your longest query, set undo retention, and never commit inside the loop you are fetching from."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 6 REDO LOG SIZING
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "REDO side: groups & switches", SB(50), PINK, a)
        for k in range(3):
            x = 90 + k * 310; act = int(lt * 1.2) % 3 == k
            glow_box(d, (x, 320, x + 280, 470), PINK if act else OFFB, a, f"GROUP {k + 1}", "CURRENT" if act else "ACTIVE / INACTIVE", 32, 24)
            for m in range(2):
                d.rounded_rectangle((x + 30 + m * 120, 490, x + 130 + m * 120, 540), 10, fill=mix(CARD, a), outline=mix(DIM, a), width=2)
                ct(d, 498, f"m{m + 1}", SN(26), DIM, a, x + 80 + m * 120)
        ct(d, 560, "2 members per group = mirrored", SN(30), DIM, pr(lt, 1.5, 1.9) * fo)
        bar(d, 110, 690, 970, 40, pr(lt, 3, 4), RED, pr(lt, 2.8, 3.2) * fo, "log switches / hour (too small)", "60")
        bar(d, 110, 810, 970, 40, pr(lt, 4, 5) * .07, GREEN, pr(lt, 3.8, 4.2) * fo, "healthy", "3–4")
        card_list(d, 900, [("wait: 'checkpoint not complete' = logs too small", YEL, 6),
                           ("check: V$LOG_HISTORY, V$LOG", CYAN, 8)], lt, fo, 80, 30)
        caps = ["Redo goes into online log groups. Each group should have at least two members on different disks.",
                "If the logs are too small, Oracle switches constantly and forces checkpoints. Aim for a few switches per hour.",
                "Checkpoint not complete in your waits means the logs are too small. Check V dollar log history."]
        caption(d, caps[0 if lt < 2.8 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 7 WHAT IF LOST
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Who needs what?", SB(58), WHITE, a)
        glow_box(d, (60, 320, 520, 420), PURP, a, "UNDO", None, 44)
        glow_box(d, (560, 320, 1020, 420), PINK, a, "REDO", None, 44)
        rows = [("ROLLBACK", "✓", "—"), ("consistent reads", "✓", "—"), ("Flashback Query", "✓", "—"),
                ("crash recovery", "✓ (rolls back)", "✓ (rolls forward)"), ("media recovery", "—", "✓ + archives"),
                ("Data Guard", "—", "✓")]
        for k, (lab, u, r) in enumerate(rows):
            y = 450 + k * 105; al = pr(lt, .8 + k * 1.1, 1.2 + k * 1.1) * fo
            ct(d, y, lab, SN(28), DIM, al)
            d.rounded_rectangle((60, y + 34, 520, y + 92), 12, fill=mix((40, 26, 66), al))
            d.rounded_rectangle((560, y + 34, 1020, y + 92), 12, fill=mix((70, 26, 50), al))
            ct(d, y + 42, u, SB(30), WHITE, al, 290); ct(d, y + 42, r, SB(30), WHITE, al, 790)
        caps = ["Undo serves rollback, consistent reads, and flashback query.",
                "After a crash, both work together: redo rolls forward, then undo rolls back uncommitted work.",
                "Redo plus archived logs restore a whole database, and feed Data Guard. Lose current redo, and committed work is gone."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("UNDO", "→ old value, ring of extents"), ("REDO", "→ change vectors, by SCN"),
                          ("Readers", "→ CR copy from undo"), ("ORA-01555", "→ undo overwritten"),
                          ("Log switch", "→ few per hour, mirrored")],
              "Undo lets Oracle go back in time. Redo lets it replay the future. And redo protects undo too.", 420)
    else:
        cta(d, t - T[9], "DATAFILES vs LOG FILES", "what's on disk, who writes it", 58)
    return im

if __name__ == "__main__":
    preview(frame, T, "v22_sheet.png")

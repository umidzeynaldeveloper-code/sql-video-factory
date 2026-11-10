from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "5 workers · 1 queue", SB(56), WHITE, a)
        glow_box(d, (340, 330, 740, 450), YEL, a, "job #1", "pay 500 AZN", 36, 28)
        for k in range(5):
            x = 120 + k * 190; al = pr(lt, .6 + k * .2, 1 + k * .2) * fo
            d.ellipse((x - 60, 640, x + 60, 760), fill=mix(CARD, al), outline=mix(CYAN, al), width=3)
            ct(d, 680, f"W{k + 1}", SB(34), CYAN, al, x)
            flow(d, [(x, 640), (540, 450)], RED, al, t, pr(lt, 1.6, 2.2))
        ct(d, 830, "paid 5 times 💸".replace(" 💸", ""), SB(44), RED, pr(lt, 2.5, 2.9) * fo)
        caption(d, "Every worker grabs the same job. Or they all wait. SELECT FOR UPDATE fixes both.", pr(lt, 3, 3.4) * fo)

    # 1 FOR UPDATE LOCKS
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "FOR UPDATE = row locks", SB(54), GREEN, a)
        code(d, 310, [("SELECT * FROM jobs", CYAN), ("WHERE status = 'NEW' FOR UPDATE;", GREEN)], a, 30)
        for k in range(4):
            y = 480 + k * 90; al = pr(lt, 1.5 + k * .3, 1.9 + k * .3) * fo
            d.rounded_rectangle((120, y, 600, y + 72), 12, fill=mix(CARD, al), outline=mix(GREEN, al), width=3)
            d.text((150, y + 16), f"job {k + 1}   🔒".replace("   🔒", "   [locked]"), font=MB(30), fill=mix(WHITE, al))
        glow_box(d, (660, 480, 1010, 600), CYAN, pr(lt, 4, 4.4) * fo, "SELECT", "reads ✓", 34, 28)
        glow_box(d, (660, 650, 1010, 770), RED, pr(lt, 5.5, 5.9) * fo, "UPDATE", "waits ⏳".replace(" ⏳", ""), 34, 28)
        ct(d, 880, "held until COMMIT / ROLLBACK", SB(38), YEL, pr(lt, 8, 8.4) * fo)
        caps = ["Select for update locks every selected row when the cursor opens.",
                "Plain readers still read them. Writers and other lockers must wait.",
                "The locks stay until you commit or roll back."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 2 NOWAIT / WAIT n
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How long to wait?", SB(56), YEL, a)
        rows = [("FOR UPDATE", "wait forever", DIM, .5), ("FOR UPDATE NOWAIT", "ORA-00054 resource busy, at once", RED, 2.5),
                ("FOR UPDATE WAIT 3", "ORA-30006 after 3 seconds", YEL, 6)]
        for k, (s, ex, col, st) in enumerate(rows):
            y = 330 + k * 190; al = pr(lt, st, st + .4) * fo
            glow_box(d, (70, y, 1010, y + 160), col, al, s, ex, 38, 30)
        caps = ["By default, the second session waits with no time limit.",
                "Nowait fails immediately with resource busy.",
                "Wait three gives up after three seconds."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 3 SKIP LOCKED
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "SKIP LOCKED = a safe queue", SB(52), GREEN, a)
        cols = [CYAN, PURP, PINK]
        for k in range(12):
            x = 100 + (k % 6) * 150; y = 340 + (k // 6) * 120
            w_ = k // 4; al = pr(lt, 1 + w_ * 1.5, 1.4 + w_ * 1.5) * fo
            d.rounded_rectangle((x, y, x + 130, y + 100), 14, fill=mix(CARD, a), outline=mix(cols[w_] if al > 0 else DIM, max(a * .4, al)), width=4)
            ct(d, y + 30, f"#{k + 1}", MB(32), cols[w_] if al > .5 else WHITE, a, x + 65)
        for k in range(3):
            glow_box(d, (90 + k * 310, 640, 370 + k * 310, 760), cols[k], pr(lt, 1 + k * 1.5, 1.4 + k * 1.5) * fo, f"worker {k + 1}", f"jobs {k * 4 + 1}–{k * 4 + 4}", 32, 28)
        card_list(d, 840, [("locked rows are skipped, not waited for", GREEN, 6), ("no duplicates · no waiting", CYAN, 8)], lt, fo, 90, 32)
        caps = ["Skip locked jumps over rows that another session already holds.",
                "Each worker gets its own set of jobs.",
                "No duplicates, and nobody waits."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 4 CODE
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The worker", SB(56), CYAN, a)
        code(d, 310, [("CURSOR c IS SELECT id FROM jobs", CYAN), ("  WHERE status = 'NEW' ORDER BY id", CYAN),
                      ("  FOR UPDATE SKIP LOCKED;", GREEN), ("", WHITE), ("OPEN c;", WHITE),
                      ("FETCH c BULK COLLECT INTO l_ids LIMIT 10;", YEL), ("-- process the 10 jobs", DIM),
                      ("FORALL i IN 1 .. l_ids.COUNT", WHITE), ("  UPDATE jobs SET status = 'DONE'", WHITE),
                      ("  WHERE id = l_ids(i);", WHITE), ("CLOSE c; COMMIT;", YEL)], a, 26)
        caps = ["A cursor over new jobs, for update skip locked.",
                "Fetch ten rows with a limit. With skip locked, rows are locked as they are fetched.",
                "Process them, mark them done, and commit."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 5 ROWNUM TRAP
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Trap: ROWNUM + SKIP LOCKED", SB(50), RED, a)
        code(d, 310, [("WHERE status = 'NEW' AND ROWNUM <= 10", RED), ("FOR UPDATE SKIP LOCKED;", RED)], a, 28)
        for k in range(10):
            x = 90 + (k % 5) * 185; y = 470 + (k // 5) * 110; al = pr(lt, 1.5, 1.9) * fo
            d.rounded_rectangle((x, y, x + 160, y + 90), 12, fill=mix(CARD, al), outline=mix(RED, al), width=3)
            ct(d, y + 24, f"#{k + 1} held", SN(26), RED, al, x + 80)
        ct(d, 720, "result: 0 rows", SB(46), RED, pr(lt, 4, 4.4) * fo)
        ct(d, 790, "…while jobs #11–#500 are free", SB(36), YEL, pr(lt, 5, 5.4) * fo)
        code(d, 880, [("FETCH c BULK COLLECT INTO l_ids LIMIT 10;  ✓", GREEN)], pr(lt, 8, 8.4) * fo, 28)
        caps = ["Rownum takes the first ten rows before locked ones are skipped.",
                "If another worker holds those ten, you get nothing, while hundreds of jobs wait.",
                "Use no rownum. Fetch with a limit instead."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 6 OF / CURRENT OF
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Two more tools", SB(56), PURP, a)
        code(d, 310, [("SELECT j.id, c.name FROM jobs j", CYAN), ("JOIN clients c ON c.id = j.client_id", CYAN),
                      ("FOR UPDATE OF j.status;", PURP)], a, 28)
        ct(d, 520, "locks JOBS rows only, not CLIENTS", SB(34), GREEN, pr(lt, 2.5, 2.9) * fo)
        code(d, 620, [("UPDATE jobs SET status = 'DONE'", WHITE), ("WHERE CURRENT OF c;", PURP)], pr(lt, 5.5, 5.9) * fo, 28)
        ct(d, 780, "updates the row just fetched", SB(34), GREEN, pr(lt, 7, 7.4) * fo)
        caps = ["In a join, for update of names the table whose rows you lock.",
                "Where current of updates exactly the row the cursor just fetched.",
                "No second lookup by id."]
        caption(d, caps[0 if lt < 5.5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 7 COMMIT IN LOOP
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Never commit inside the loop", SB(50), RED, a)
        code(d, 310, [("FOR r IN c LOOP   -- c is FOR UPDATE", WHITE), ("  UPDATE … WHERE CURRENT OF c;", WHITE),
                      ("  COMMIT;          -- releases ALL locks", RED), ("END LOOP;", WHITE)], a, 28)
        glow_box(d, (100, 600, 980, 760), RED, pr(lt, 3, 3.4) * fo, "ORA-01002", "fetch out of sequence", 44, 32)
        ct(d, 840, "commit after the batch ✓", SB(40), GREEN, pr(lt, 6, 6.4) * fo)
        caption(d, "A commit releases every lock the cursor holds, and the next fetch fails. Commit after the batch.", pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("FOR UPDATE", "→ lock until commit"), ("NOWAIT / WAIT n", "→ stop waiting"),
                          ("SKIP LOCKED", "→ safe job queue"), ("LIMIT, not ROWNUM", "→ real batches"),
                          ("No COMMIT in loop", "→ ORA-01002")],
              "Lock what you process, skip what others hold, commit after the batch.", 480)
    else:
        cta(d, t - T[9], "DATE TRAPS", "why November 30 went missing", 64)
    return im


if __name__ == "__main__":
    preview(frame, T, "v46_sheet.png")

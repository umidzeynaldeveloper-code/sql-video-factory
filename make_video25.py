from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def sess(d, x, y, col, a, lbl, fs=26, r=40):
    d.ellipse((x - r, y - r, x + r, y + r), fill=mix(col, a))
    ct(d, y - fs * .6, lbl, SB(fs), BG, a, x)

def row(d, x, y, w, txt, a, lock=None, col=WHITE):
    d.rounded_rectangle((x, y, x + w, y + 70), 12, fill=mix(CARD, a), outline=mix(lock or DIM, a), width=4 if lock else 2)
    d.text((x + 24, y + 18), txt, font=MN(30), fill=mix(col, a))
    if lock:
        lx = x + w - 60
        d.rounded_rectangle((lx, y + 28, lx + 36, y + 58), 6, fill=mix(lock, a))
        d.arc((lx + 6, y + 10, lx + 30, y + 40), 180, 360, fill=mix(lock, a), width=5)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        code(d, 230, [("UPDATE accounts SET bal = bal - 100", YEL), ("WHERE id = 7;", YEL)], a, 32)
        sp = int(lt * 2) % 4
        ct(d, 420, "waiting" + "." * sp, SB(48), WHITE, pr(lt, .8, 1.2) * fo)
        secs = int(max(0, lt - 1) * 37)
        ct(d, 500, f"{secs // 60:02d}:{secs % 60:02d}", MB(80), RED, pr(lt, 1, 1.4) * fo)
        glow_box(d, (110, 650, 970, 780), PURP, pr(lt, 2.4, 2.8) * fo, "enq: TX - row lock contention", "top wait", 34, 28)
        ct(d, 860, "Who is blocking me?!", SB(52), YEL, pr(lt, 3.3, 3.7) * fo)
        caption(d, "Your session isn't slow. It's waiting in a queue. Let's see how Oracle locks really work.", pr(lt, 4, 4.4) * fo)

    # 1 ROW LOCK IN THE BLOCK
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The lock lives IN the row", SB(52), WHITE, a)
        d.rounded_rectangle((90, 320, 990, 860), 24, outline=mix(CYAN, a), width=4)
        d.text((120, 335), "DATA BLOCK", font=SB(30), fill=mix(CYAN, a))
        ai = pr(lt, 3, 3.4) * fo
        d.rounded_rectangle((120, 390, 960, 480), 14, fill=mix((40, 26, 66), ai))
        d.text((145, 410), "ITL slot 1:  TX 0007.019.0000412", font=MN(30), fill=mix(PURP, ai))
        lk = PINK if lt > 1.5 else None
        for k, (txt) in enumerate(["id=5  bal=300", "id=6  bal=120", "id=7  bal=1000", "id=8  bal=75"]):
            hit = k == 2
            row(d, 120, 510 + k * 85, 840, txt if not (hit and lt > 1.5) else "id=7  bal=900", a, lk if hit else None)
        if lt > 4.5:
            al = pr(lt, 4.5, 4.9) * fo
            d.line((900, 723, 900, 480), fill=mix(PINK, al), width=4)
        card_list(d, 900, [("no central lock list: scales to millions of rows", GREEN, 6),
                           ("waiter waits on the TX enqueue of the holder", YEL, 8.5)], lt, fo, 80, 30)
        caps = ["When you update a row, Oracle doesn't keep a big list of row locks. It marks the row itself.",
                "The row points to a slot in the block's interested transaction list, the ITL, which names your transaction.",
                "That's why Oracle can lock millions of rows for free. Anyone who wants that row waits on your transaction's TX enqueue."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 2 BLOCKING + QUEUE
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Blocking, step by step", SB(54), PINK, a)
        committed = lt > 7.5
        row(d, 290, 340, 500, "id=7", a, CYAN if lt > 8.6 else (None if committed else PINK))
        sess(d, 160, 375, PINK, a * (1 - pr(lt, 7.5, 8)), "S1")
        if not committed: ct(d, 430, "holds TX", SN(28), PINK, a, 160)
        # queue
        q = [("S2", CYAN, 1.5), ("S3", YEL, 3), ("S4", PURP, 4.5)]
        for k, (nm, col, st) in enumerate(q):
            p = pr(lt, st, st + .8)
            pos = k - (1 if committed and k > 0 else 0)
            tx = 360 + pos * 170 if not (committed and k == 0) else 540
            ty = 600 if not (committed and k == 0) else 375
            if committed and k == 0: tx, ty = lerp(360, 160, pr(lt, 7.8, 8.6)), lerp(600, 375, pr(lt, 7.8, 8.6))
            x = lerp(1060, tx, p)
            sess(d, x, ty, col, a * pr(lt, st, st + .2), nm)
        ct(d, 680, "FIFO queue", SB(32), DIM, pr(lt, 2, 2.4) * fo, 530)
        if lt > 6.5:
            ac = pr(lt, 6.5, 6.9) * fo
            code(d, 780, [("S1: COMMIT;", GREEN)], ac, 32, 300, 780)
        ct(d, 920, "S2 gets the row → S3 waits for S2", SB(34), GREEN, pr(lt, 9, 9.4) * fo)
        caps = ["Session one updates account seven and doesn't commit yet.",
                "Sessions two, three and four want the same row. They queue in order, first in, first out.",
                "When session one commits or rolls back, the next one in line gets the row. A long transaction blocks everyone behind it."]
        caption(d, caps[0 if lt < 1.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 3 TM LOCKS
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "TM: the table-level guard", SB(52), YEL, a)
        glow_box(d, (300, 330, 780, 470), YEL, a, "TABLE accounts", "TM lock: Row-X (SX)", 36, 28)
        for k in range(3):
            p = pr(lt, .8 + k * .4, 1.6 + k * .4)
            x = 180 + k * 360
            sess(d, x, lerp(700, 560, p), CYAN, a, f"DML{k + 1}", 22, 52)
        ct(d, 650, "many DML sessions share it ✓", SB(32), GREEN, pr(lt, 2.4, 2.8) * fo)
        ad = pr(lt, 4, 4.4) * fo
        code(d, 740, [("ALTER TABLE accounts ADD c NUMBER;", RED)], ad, 30)
        glow_box(d, (110, 860, 970, 990), RED, pr(lt, 5.5, 5.9) * fo, "DDL needs EXCLUSIVE → waits / ORA-00054", None, 32)
        card_list(d, 1030, [("every DML takes a TM lock to stop DDL mid-change", WHITE, 8)], lt, fo, 80, 30)
        caps = ["Every insert, update and delete also takes a TM lock on the table, in row exclusive mode.",
                "Row exclusive locks are compatible with each other, so thousands of DML sessions work in parallel.",
                "But DDL needs an exclusive lock. While any transaction is open on the table, ALTER waits or fails with ORA-00054, resource busy."]
        caption(d, caps[0 if lt < 2.4 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 4 UNINDEXED FOREIGN KEY
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The unindexed foreign key trap", SB(48), RED, a)
        glow_box(d, (90, 330, 450, 470), CYAN, a, "CUSTOMERS", "parent", 36, 28)
        glow_box(d, (630, 330, 990, 470), PINK, a, "ACCOUNTS", "child: customer_id FK", 34, 26)
        arrow(d, 630, 400, 450, 400, WHITE, a, 5)
        code(d, 520, [("DELETE FROM customers WHERE id = 42;", YEL)], pr(lt, 1, 1.4) * fo, 30)
        if lt > 2.5:
            ab = pr(lt, 2.5, 2.9) * fo
            d.rounded_rectangle((610, 310, 1010, 490), 24, outline=mix(RED, ab * (.5 + .5 * math.sin(t * 8))), width=8)
            ct(d, 650, "no index on customer_id → whole child table locked (TM share)", SN(28), RED, ab)
        for k in range(4):
            al = pr(lt, 4 + k * .3, 4.4 + k * .3) * fo
            sess(d, 180 + k * 240, 780, DIM, al, "wait", 22, 50)
        ct(d, 860, "every INSERT/UPDATE on ACCOUNTS stalls", SB(32), YEL, pr(lt, 5.5, 5.9) * fo)
        code(d, 950, [("CREATE INDEX acc_cust_ix ON accounts(customer_id);", GREEN)], pr(lt, 8, 8.4) * fo, 28)
        caps = ["A classic. Accounts has a foreign key to customers, but the foreign key column has no index.",
                "Delete or update a parent key, and Oracle must lock the whole child table to check it. Suddenly every insert on accounts waits.",
                "The fix is one line: index your foreign key columns."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 5 FOR UPDATE + SKIP LOCKED
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Lock on purpose: FOR UPDATE", SB(50), GREEN, a)
        code(d, 310, [("SELECT * FROM payment_queue", CYAN), ("WHERE status = 'NEW'", CYAN),
                      ("FOR UPDATE SKIP LOCKED;", YEL)], a, 30)
        cols = [PINK, CYAN, YEL]
        for k in range(6):
            y = 560 + k * 75
            owner = k // 2 if lt > 1.5 + (k // 2) * 1.2 else None
            row(d, 290, y, 500, f"payment #{101 + k}", a, cols[owner] if owner is not None else None)
        for w in range(3):
            st = 1.5 + w * 1.2; al = pr(lt, st, st + .4) * fo
            sess(d, 150 if w != 1 else 930, 600 + w * 150, cols[w], al, f"W{w + 1}", 24, 44)
        card_list(d, 1030, [("NOWAIT → error at once · WAIT 5 → max 5 s", WHITE, 6),
                            ("SKIP LOCKED → parallel workers, no waiting", GREEN, 7.5)], lt, fo, 80, 30)
        caps = ["Sometimes you lock rows on purpose. SELECT FOR UPDATE locks the rows you read, before you change them.",
                "With SKIP LOCKED, each worker takes rows nobody else holds. Three workers process the payment queue in parallel, nobody waits.",
                "Use NOWAIT to fail immediately, or WAIT with seconds to limit how long you block."]
        caption(d, caps[0 if lt < 1.5 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 6 DIAGNOSE
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Find the blocker", SB(58), WHITE, a)
        nodes = [(540, 380, "SID 101", RED, "idle in transaction!"), (300, 600, "SID 230", YEL, "waiting"),
                 (780, 600, "SID 245", YEL, "waiting"), (300, 800, "SID 311", DIM, "waiting on 230")]
        for k, (x, y, nm, col, sub) in enumerate(nodes):
            al = pr(lt, .6 + k * .7, 1 + k * .7) * fo
            glow_box(d, (x - 150, y - 55, x + 150, y + 55), col, al, nm, sub, 32, 24)
        for (x0, y0, x1, y1, st) in [(300, 545, 470, 435, 1.4), (780, 545, 610, 435, 2.1), (300, 745, 300, 655, 2.8)]:
            if lt > st: arrow(d, x0, y0, x1, y1, WHITE, pr(lt, st, st + .4) * fo, 5)
        code(d, 900, [("SELECT sid, blocking_session, event,", CYAN), ("       seconds_in_wait, sql_id", CYAN),
                      ("FROM   v$session", CYAN), ("WHERE  blocking_session IS NOT NULL;", CYAN)], pr(lt, 4.5, 4.9) * fo, 28)
        caps = ["Blocking forms a tree. The root is often a session that is idle in a transaction: someone forgot to commit.",
                "V dollar session tells you everything: who waits, on which event, and which session blocks it.",
                "Fix the root, usually by asking the owner to commit. Kill a session only as a last resort, and remember: its rollback takes time too."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 7 RULES
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Locking rules for developers", SB(50), GREEN, a)
        rules = [("keep transactions SHORT", "commit when the unit of work is done", GREEN),
                 ("no user think-time inside a transaction", "never wait for a click holding locks", YEL),
                 ("index foreign keys", "avoid whole-table TM locks", CYAN),
                 ("lock rows in the same ORDER", "or you'll meet ORA-00060 deadlock", PINK)]
        for k, (h, s_, col) in enumerate(rules):
            y = 330 + k * 175; al = pr(lt, .6 + k * 2.2, 1 + k * 2.2) * fo
            d.rounded_rectangle((70, y, W - 70, y + 150), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.ellipse((100, y + 45, 160, y + 105), fill=mix(col, al)); ct(d, y + 55, str(k + 1), SB(34), BG, al, 130)
            d.text((190, y + 30), h, font=SB(32), fill=mix(col, al))
            d.text((190, y + 85), s_, font=SN(28), fill=mix(WHITE, al))
        caps = ["Keep transactions short, and never keep a transaction open while waiting for a user.",
                "Index your foreign keys.",
                "And always lock rows in the same order, or two sessions can block each other forever: a deadlock."]
        caption(d, caps[0 if lt < 4.4 else 1 if lt < 6.6 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Row lock", "→ in the block, ITL → TX"), ("Waiters", "→ fair FIFO queue"),
                          ("TM lock", "→ DML vs DDL"), ("FK index", "→ or the child table locks"),
                          ("SKIP LOCKED", "→ parallel queue workers")],
              "Locks protect your data, and they're held until COMMIT. Keep transactions short.", 430)
    else:
        cta(d, t - T[9], "SHARED POOL & HARD PARSE", "why literals kill your CPU", 54)
    return im

if __name__ == "__main__":
    preview(frame, T, "v25_sheet.png")

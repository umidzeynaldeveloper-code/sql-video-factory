from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK: missing invoice numbers
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Where did 1003 and 1004 go?", SB(50), WHITE, a)
        ids = [("1001", GREEN), ("1002", GREEN), ("1003", RED), ("1004", RED), ("1005", GREEN), ("1006", GREEN)]
        for k, (s, col) in enumerate(ids):
            y = 340 + k * 105; al = pr(lt, .3 + k * .25, .6 + k * .25) * fo
            miss = col == RED
            d.rounded_rectangle((260, y, 820, y + 85), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((300, y + 20), "invoice_id = " + s, font=MB(36), fill=mix(DIM if miss else WHITE, al))
            if miss and lt > 2.2:
                d.line((290, y + 42, 790, y + 42), fill=mix(RED, al), width=5)
                d.text((700, y + 22), "?", font=SB(40), fill=mix(RED, al))
        caption(d, "Gaps in your IDs are not a bug. Here is exactly where they come from, and when they matter.", pr(lt, 3, 3.4) * fo)

    # 1 HOW A SEQUENCE WORKS
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "A sequence = a number dispenser", SB(48), CYAN, a)
        code(d, 300, [("CREATE SEQUENCE invoice_seq", CYAN), ("  START WITH 1001 CACHE 20;", CYAN),
                      ("INSERT INTO invoices VALUES", WHITE), ("  (invoice_seq.NEXTVAL, …);", GREEN)], a, 28)
        am = pr(lt, 2.5, 2.9) * fo
        glow_box(d, (70, 640, 500, 820), CYAN, am, "SGA cache", "1001 … 1020", 34, 28)
        glow_box(d, (580, 640, 1010, 820), PURP, am, "Dictionary", "next = 1021", 34, 28)
        flow(d, [(500, 730), (580, 730)], PURP, am, t, pr(lt, 3, 3.6))
        n = 1001 + int(max(0, min(19, (lt - 5) * 3)))
        ct(d, 880, f"NEXTVAL → {n}", MB(52), GREEN, pr(lt, 5, 5.4) * fo)
        card_list(d, 980, [("20 numbers live in memory, no disk I/O per call", GREEN, 7.5),
                           ("NEXTVAL is never rolled back", YEL, 9)], lt, fo, 80, 31)
        caps = ["A sequence hands out numbers. Each NEXTVAL gives the next one, to any session, without locking a table.",
                "With CACHE 20, Oracle keeps twenty numbers in memory and writes to the dictionary only once per twenty.",
                "That's why it's fast. But a number, once handed out, is never given back."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 2 WHERE GAPS COME FROM
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Three sources of gaps", SB(54), YEL, a)
        g1 = pr(lt, .6, 1) * fo
        glow_box(d, (70, 320, 1010, 520), RED, g1, "1. ROLLBACK", "1003 was used, the insert rolled back → 1003 is gone", 36, 26)
        g2 = pr(lt, 4.5, 4.9) * fo
        glow_box(d, (70, 560, 1010, 760), PINK, g2, "2. Instance restart", "cached 1004 … 1020 lost → next is 1021", 36, 26)
        g3 = pr(lt, 8.5, 8.9) * fo
        glow_box(d, (70, 800, 1010, 1000), PURP, g3, "3. RAC: one cache per node", "node 1: 1001 … · node 2: 1021 …", 36, 26)
        caps = ["One: a session takes a number, then its transaction rolls back. The row disappears, but the number does not come back.",
                "Two: the instance restarts, or the cache is flushed. Every cached number that was never used is simply lost.",
                "Three: on RAC, every node has its own cache. Numbers are unique, but not in time order across nodes."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 3 MAX(ID)+1 RACE
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Never: SELECT MAX(id) + 1", SB(52), RED, a)
        for k, (x, nm, col) in enumerate(((70, "Session A", CYAN), (570, "Session B", PINK))):
            al = pr(lt, .5 + k * .3, .9 + k * .3) * fo
            glow_box(d, (x, 320, x + 440, 430), col, al, nm, None, 36)
            d.text((x + 20, 470), "MAX(id) = 1004", font=MB(30), fill=mix(WHITE, pr(lt, 2, 2.4) * fo))
            d.text((x + 20, 530), "INSERT 1005", font=MB(30), fill=mix(col, pr(lt, 3.5, 3.9) * fo))
        ae = pr(lt, 5.5, 5.9) * fo
        glow_box(d, (200, 640, 880, 780), RED, ae, "ORA-00001", "unique constraint violated", 40, 28)
        card_list(d, 850, [("both read the same MAX → same new id", YEL, 7.5),
                           ("locking the table fixes it… and kills concurrency", RED, 9)], lt, fo, 80, 30)
        caps = ["The homemade alternative: read the maximum id and add one. Two sessions do it at the same moment.",
                "Both see 1004, both insert 1005. One of them gets O R A one, unique constraint violated.",
                "Locking the table fixes the race, but then only one session can insert at a time."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 4 IDENTITY COLUMNS
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "12c+: IDENTITY columns", SB(54), GREEN, a)
        code(d, 300, [("CREATE TABLE invoices (", WHITE),
                      ("  id NUMBER GENERATED ALWAYS AS IDENTITY,", GREEN),
                      ("  amount NUMBER );", WHITE)], a, 27)
        rows = [("GENERATED ALWAYS", "you can't insert your own id", GREEN),
                ("BY DEFAULT", "your value wins if you give one", CYAN),
                ("BY DEFAULT ON NULL", "NULL → next value", YEL)]
        for k, (kw, ex, col) in enumerate(rows):
            y = 540 + k * 130; al = pr(lt, 2.5 + k * 1.5, 2.9 + k * 1.5) * fo
            d.rounded_rectangle((70, y, W - 70, y + 110), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 14), kw, font=MB(32), fill=mix(col, al))
            d.text((100, y + 60), "→ " + ex, font=SN(30), fill=mix(WHITE, al))
        ct(d, 950, "behind the scenes: a system sequence ISEQ$$_…", SB(30), DIM, pr(lt, 8, 8.4) * fo)
        caps = ["Since twelve c, a column can generate its own numbers: generated always as identity.",
                "Always means you can't supply your own value. By default lets yours win. On null fills only the missing ones.",
                "Under the hood it's still a sequence, created and managed by Oracle. Same cache, same gaps."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 5 PERFORMANCE: CACHE SIZE
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Busy inserts? Check CACHE", SB(52), CYAN, a)
        bars = [("NOCACHE", .95, RED, "dictionary write per number"), ("CACHE 20", .45, YEL, "one write per 20"),
                ("CACHE 1000", .06, GREEN, "one write per 1000")]
        for k, (lb, p, col, ex) in enumerate(bars):
            y = 380 + k * 170; al = pr(lt, .5 + k * .8, .9 + k * .8) * fo
            bar(d, 100, y, 980, 46, p * pr(lt, .5 + k * .8, 1.6 + k * .8), col, al, lb, None)
            d.text((100, y + 60), ex, font=SN(28), fill=mix(DIM, al))
        ct(d, 900, "wait event: enq: SQ - contention", MB(34), RED, pr(lt, 5, 5.4) * fo)
        card_list(d, 980, [("ALTER SEQUENCE invoice_seq CACHE 1000;", GREEN, 7.5)], lt, fo, 80, 31)
        caps = ["With NOCACHE, every number costs a dictionary update. At thousands of inserts per second that's a bottleneck.",
                "Sessions start waiting on enq S Q contention. The fix is one line: a bigger cache.",
                "Bigger cache, faster inserts. The price: more numbers lost on a restart. Usually a great trade."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 9 else 2], pr(lt, .6, 1) * fo)

    # 6 RAC ORDER
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "RAC: unique ≠ in order", SB(54), PURP, a)
        glow_box(d, (70, 330, 500, 470), CYAN, a, "Node 1", "cache 1001–1020", 34, 26)
        glow_box(d, (580, 330, 1010, 470), PINK, a, "Node 2", "cache 1021–1040", 34, 26)
        seq = [("10:00:01", "1001", CYAN), ("10:00:02", "1021", PINK), ("10:00:03", "1002", CYAN), ("10:00:04", "1022", PINK)]
        for k, (tm, v, col) in enumerate(seq):
            y = 540 + k * 85; al = pr(lt, 1.5 + k * .6, 1.9 + k * .6) * fo
            d.rounded_rectangle((200, y, 880, y + 70), 14, fill=mix(CARD, al))
            d.text((230, y + 16), tm, font=MB(32), fill=mix(DIM, al)); d.text((560, y + 16), "id " + v, font=MB(32), fill=mix(col, al))
        card_list(d, 900, [("ORDER → strict order, but nodes must coordinate", YEL, 6.5),
                           ("need time order? use a timestamp column", GREEN, 8.5)], lt, fo, 80, 30)
        caps = ["On RAC each node caches its own range, so a later row can get a smaller id.",
                "The ORDER option forces strict order, but every NEXTVAL must coordinate between nodes, which is slow.",
                "If you need to know what happened first, don't read it from the id. Store a timestamp."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 7 GAP-FREE REQUIREMENT
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Law says: no gaps allowed?", SB(52), YEL, a)
        code(d, 300, [("SELECT last_no FROM doc_counters", CYAN), ("  WHERE doc_type = 'INV' FOR UPDATE;", CYAN),
                      ("UPDATE doc_counters SET last_no = last_no + 1 …", WHITE), ("-- same transaction as the insert", DIM)], a, 26)
        aq = pr(lt, 3.5, 3.9) * fo
        for k, (nm, col) in enumerate((("A: holds the row", GREEN), ("B: waits…", YEL), ("C: waits…", YEL))):
            d.rounded_rectangle((140 + k * 60, 640 + k * 90, 940, 720 + k * 90), 14, fill=mix(CARD, aq), outline=mix(col, aq), width=3)
            d.text((170 + k * 60, 660 + k * 90), nm, font=SB(30), fill=mix(col, aq))
        card_list(d, 960, [("rollback → counter rolls back too → no gap", GREEN, 6.5),
                           ("price: one invoice at a time", RED, 8.5)], lt, fo, 80, 30)
        caps = ["Some numbers must have no gaps, like invoice numbers in some countries. A sequence can't promise that.",
                "Use a counter row, locked with select for update, in the same transaction as the insert.",
                "If the transaction rolls back, the counter rolls back too. The cost: inserts are serialized."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("NEXTVAL", "→ never rolled back"), ("Gaps", "→ rollback · restart · RAC"),
                          ("MAX(id)+1", "→ race, ORA-00001"), ("CACHE", "→ fast inserts"),
                          ("No gaps?", "→ counter row FOR UPDATE")],
              "Sequences promise unique numbers, not gap-free ones.", 400)
    else:
        cta(d, t - T[9], "PAGINATION", "ROWNUM vs FETCH FIRST", 64)
    return im


if __name__ == "__main__":
    preview(frame, T, "v39_sheet.png")

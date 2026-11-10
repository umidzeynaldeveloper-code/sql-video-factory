from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Balance: 100", SB(60), WHITE, a)
        glow_box(d, (70, 360, 500, 500), CYAN, pr(lt, .6, 1) * fo, "Cashier A", "+10", 36, 34)
        glow_box(d, (580, 360, 1010, 500), PURP, pr(lt, .9, 1.3) * fo, "Cashier B", "+50", 36, 34)
        flow(d, [(285, 500), (540, 640)], CYAN, pr(lt, 1.4, 1.8) * fo, t, pr(lt, 1.4, 2))
        flow(d, [(795, 500), (540, 640)], PURP, pr(lt, 1.4, 1.8) * fo, t, pr(lt, 1.4, 2))
        glow_box(d, (300, 640, 780, 790), RED, pr(lt, 2.2, 2.6) * fo, "150", "expected 160", 52, 32)
        caption(d, "Two updates, one balance, and ten is gone. No error. The answer is isolation.", pr(lt, 3, 3.4) * fo)

    # 1 READ COMMITTED
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Default: READ COMMITTED", SB(54), GREEN, a)
        d.line((100, 470, 980, 470), fill=mix(DIM, a), width=4)
        for k, (x, lb, col) in enumerate(((200, "commit", GREEN), (480, "SELECT starts", CYAN), (760, "commit", RED))):
            al = pr(lt, .8 + k * .9, 1.2 + k * .9) * fo
            d.ellipse((x - 14, 456, x + 14, 484), fill=mix(col, al))
            ct(d, 380, lb, SB(30), col, al, x)
        ct(d, 520, "sees ✓", SB(32), GREEN, pr(lt, 3.5, 3.9) * fo, 200)
        ct(d, 520, "doesn't see ✗", SB(32), RED, pr(lt, 4, 4.4) * fo, 760)
        card_list(d, 650, [("each STATEMENT sees data committed before it began", WHITE, 5),
                           ("readers never block writers, writers never block readers", CYAN, 7),
                           ("dirty reads: impossible in Oracle", GREEN, 8.5)], lt, fo, 95, 30)
        caps = ["Every statement sees only data committed before that statement started.",
                "Older versions are rebuilt from undo, so nobody waits for anybody.",
                "And reading uncommitted data is simply impossible in Oracle."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 2 NON-REPEATABLE READ
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Same query, same transaction…", SB(50), YEL, a)
        code(d, 320, [("SELECT balance FROM accounts", CYAN), ("WHERE id = 42;          -- 100", WHITE)], a, 30)
        glow_box(d, (180, 540, 900, 660), PURP, pr(lt, 3, 3.4) * fo, "other session: UPDATE … COMMIT", None, 32)
        code(d, 730, [("SELECT balance FROM accounts", CYAN), ("WHERE id = 42;          -- 150", RED)], pr(lt, 5.5, 5.9) * fo, 30)
        ct(d, 950, "non-repeatable read: allowed", SB(40), YEL, pr(lt, 8, 8.4) * fo)
        caps = ["Read committed is per statement, not per transaction.",
                "Another session commits in between…",
                "…and the second read in the same transaction returns a different value."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 3 LOST UPDATE
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The lost update", SB(56), RED, a)
        steps = [("A reads 100", CYAN, 70, 330, .6), ("B reads 100", PURP, 580, 330, 1.4),
                 ("A writes 110", CYAN, 70, 520, 3.5), ("B writes 150", PURP, 580, 520, 5)]
        for s, col, x, y, st in steps:
            glow_box(d, (x, y, x + 430, y + 130), col, pr(lt, st, st + .4) * fo, s, None, 36)
        glow_box(d, (240, 740, 840, 900), RED, pr(lt, 7, 7.4) * fo, "final: 150", "the +10 is gone · no error", 44, 30)
        caps = ["Both applications read one hundred.",
                "Each computes a new value in its own code and writes it back.",
                "The last write wins. The other change silently disappears."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 4 FIXES
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "3 fixes", SB(56), GREEN, a)
        code(d, 310, [("UPDATE accounts SET balance = balance + 10", GREEN), ("WHERE id = 42;", GREEN)], pr(lt, .5, .9) * fo, 28)
        ct(d, 440, "1 · let the database do the math", SB(30), DIM, pr(lt, .5, .9) * fo)
        code(d, 510, [("SELECT balance FROM accounts", CYAN), ("WHERE id = 42 FOR UPDATE;", CYAN)], pr(lt, 4, 4.4) * fo, 28)
        ct(d, 640, "2 · lock first (pessimistic)", SB(30), DIM, pr(lt, 4, 4.4) * fo)
        code(d, 710, [("UPDATE accounts SET balance = :b, ver = ver + 1", PURP),
                      ("WHERE id = 42 AND ver = :ver_read;", PURP),
                      ("-- 0 rows? someone was faster → retry", DIM)], pr(lt, 7, 7.4) * fo, 26)
        ct(d, 880, "3 · version column (optimistic)", SB(30), DIM, pr(lt, 7, 7.4) * fo)
        caps = ["One: let the database compute it, in a single update.",
                "Two: lock the row first with select for update.",
                "Three: a version column. Zero rows updated means read again and retry."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 5 SERIALIZABLE
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "SERIALIZABLE", SB(60), PURP, a)
        code(d, 320, [("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;", PURP)], a, 26)
        glow_box(d, (100, 450, 980, 580), CYAN, pr(lt, 2, 2.4) * fo, "every query: data as of transaction start", None, 32)
        glow_box(d, (100, 650, 980, 820), RED, pr(lt, 5, 5.4) * fo, "ORA-08177", "can't serialize access for this transaction", 44, 28)
        card_list(d, 890, [("row changed & committed by others after you began", YEL, 6.5), ("→ catch it, roll back, retry", GREEN, 8.5)], lt, fo, 90, 30)
        caps = ["Serializable gives one consistent picture for the whole transaction.",
                "Change a row that someone else changed and committed after you started…",
                "…and you get ORA-08177. The application must retry."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 6 READ ONLY
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Reports: READ ONLY", SB(56), CYAN, a)
        code(d, 320, [("SET TRANSACTION READ ONLY;", CYAN), ("SELECT … totals …;", WHITE), ("SELECT … details …;", WHITE), ("COMMIT;", YEL)], a, 30)
        card_list(d, 640, [("all queries see the same moment", GREEN, 2.5), ("no INSERT / UPDATE / DELETE allowed", RED, 4.5),
                           ("long report → needs undo for the whole time", YEL, 7)], lt, fo, 95, 30)
        caps = ["For multi-query reports: set transaction read only.",
                "Totals and details always match, because they see the same moment.",
                "A long report needs that undo the whole time, so size undo retention for it."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 7 LEVELS TABLE
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Oracle's isolation levels", SB(52), YEL, a)
        rows = [("READ COMMITTED", "default · per statement", GREEN, .5), ("SERIALIZABLE", "per transaction · ORA-08177", PURP, 1.5),
                ("READ ONLY", "per transaction · no DML", CYAN, 2.5), ("READ UNCOMMITTED", "doesn't exist ✗", RED, 4)]
        for k, (s, ex, col, st) in enumerate(rows):
            y = 330 + k * 150; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 125), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 16), s, font=SB(36), fill=mix(col, al)); d.text((100, y + 68), ex, font=SN(30), fill=mix(WHITE, al))
        caption(d, "Three levels. No read uncommitted, and serializable already covers repeatable reads.", pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("READ COMMITTED", "→ per statement"), ("Lost update", "→ read·compute·write"),
                          ("Fix", "→ +10 · FOR UPDATE · ver"), ("SERIALIZABLE", "→ retry 08177"),
                          ("READ ONLY", "→ consistent report")],
              "Know your isolation level, and never read, compute, write without a lock.", 480)
    else:
        cta(d, t - T[9], "SELECT FOR UPDATE", "nowait · skip locked · job queues", 60)
    return im


if __name__ == "__main__":
    preview(frame, T, "v45_sheet.png")

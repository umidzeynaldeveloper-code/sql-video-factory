from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "One UPDATE. One trigger. Boom.", SB(52), WHITE, a)
        code(d, 320, [("UPDATE payments SET amount = amount * 1.1", CYAN), ("WHERE account_id = 42;", CYAN)], a, 30)
        ae = pr(lt, 1.8, 2.2) * fo
        glow_box(d, (90, 520, 990, 700), RED, ae, "ORA-04091", "table APP.PAYMENTS is mutating,", 44, 30)
        ct(d, 650, "trigger/function may not see it", SN(30), WHITE, ae)
        caption(d, "The famous mutating table error. Why Oracle stops you, and the clean way around it.", pr(lt, 3, 3.4) * fo)

    # 1 WHY: HALF-CHANGED TABLE
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "A row trigger sees a half-changed table", SB(44), YEL, a)
        code(d, 300, [("AFTER UPDATE ON payments FOR EACH ROW", PURP), ("  SELECT SUM(amount) FROM payments …", RED)], a, 28)
        prog = min(6, max(0, int((lt - 2) * 1.2)))
        for k in range(6):
            y = 470 + k * 80; done = k < prog
            al = pr(lt, 1.5, 1.9) * fo
            d.rounded_rectangle((200, y, 880, y + 64), 12, fill=mix(CARD, al), outline=mix(GREEN if done else DIM, al), width=3)
            d.text((230, y + 14), f"row {k + 1}", font=MB(30), fill=mix(WHITE, al))
            d.text((560, y + 14), "1.1 × ✓" if done else "old value", font=MB(30), fill=mix(GREEN if done else DIM, al))
        ct(d, 970, "SUM in the middle = neither old nor new", SB(34), RED, pr(lt, 7, 7.4) * fo)
        caps = ["The trigger fires for every row, while the update is still running.",
                "Halfway through, some rows have the new amount and some the old one.",
                "A sum read at that moment is neither the old answer nor the new one. Oracle refuses to show it."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 2 WHEN IT HAPPENS
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "When does it fire?", SB(54), CYAN, a)
        rows = [("ROW trigger reads / changes its own table", RED, "ORA-04091"),
                ("multi-row UPDATE / DELETE / INSERT … SELECT", RED, "ORA-04091"),
                ("single-row INSERT … VALUES", GREEN, "allowed"),
                ("STATEMENT trigger (no FOR EACH ROW)", GREEN, "allowed")]
        for k, (s, col, r) in enumerate(rows):
            y = 330 + k * 140; al = pr(lt, .6 + k * 1.6, 1 + k * 1.6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 120), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 16), s, font=SN(30), fill=mix(WHITE, al))
            d.text((100, y + 64), "→ " + r, font=SB(32), fill=mix(col, al))
        caps = ["The error comes from a row level trigger that reads or changes the table it belongs to.",
                "Multi row statements trigger it. A single row insert with values is allowed.",
                "A statement level trigger runs once, before or after everything, so it can read the table safely."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6.8 else 2], pr(lt, .6, 1) * fo)

    # 3 WRONG FIX
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The 'fix' you'll find online ✗", SB(50), RED, a)
        code(d, 300, [("CREATE TRIGGER …", WHITE), ("  PRAGMA AUTONOMOUS_TRANSACTION;", RED)], a, 32)
        ab = pr(lt, 2.5, 2.9) * fo
        glow_box(d, (70, 520, 500, 700), DIM, ab, "Main transaction", "new amounts (uncommitted)", 34, 26)
        glow_box(d, (580, 520, 1010, 700), RED, ab, "Autonomous", "sees only COMMITTED data", 34, 26)
        card_list(d, 780, [("no error… and a silently WRONG total", RED, 5.5),
                           ("can even deadlock with its own parent", YEL, 7.5)], lt, fo, 80, 30)
        caps = ["The popular workaround: make the trigger an autonomous transaction. The error disappears.",
                "But the autonomous part can't see the uncommitted changes of the update that fired it.",
                "So the check runs on old data. No error, wrong result. Worse than the error."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 4 COMPOUND TRIGGER IDEA
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "11g+: compound trigger", SB(54), GREEN, a)
        glow_box(d, (100, 320, 980, 450), CYAN, pr(lt, .5, .9) * fo, "AFTER EACH ROW", "only remember the account_id", 36, 28)
        flow(d, [(540, 450), (540, 530)], CYAN, pr(lt, 2, 2.4) * fo, t, pr(lt, 2, 2.6))
        acc = pr(lt, 2.5, 2.9) * fo
        d.rounded_rectangle((260, 530, 820, 620), 16, fill=mix(CARD, acc), outline=mix(YEL, acc), width=3)
        ct(d, 552, "collection: [42, 42, 42 …]", MB(32), YEL, acc)
        flow(d, [(540, 620), (540, 700)], GREEN, pr(lt, 4, 4.4) * fo, t, pr(lt, 4, 4.6))
        glow_box(d, (100, 700, 980, 830), GREEN, pr(lt, 4.5, 4.9) * fo, "AFTER STATEMENT", "table is complete → SELECT SUM is safe", 36, 28)
        caps = ["A compound trigger has several timing points in one object, sharing the same variables.",
                "Each row only remembers which account changed. No reading of the table yet.",
                "After the statement, the table is complete again. Now the sum is correct, and allowed."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 4.5 else 2], pr(lt, .6, 1) * fo)

    # 5 COMPOUND TRIGGER CODE
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The code", SB(56), GREEN, a)
        code(d, 300, [("CREATE TRIGGER pay_limit_trg", WHITE),
                      ("FOR UPDATE ON payments COMPOUND TRIGGER", PURP),
                      ("  TYPE t_ids IS TABLE OF NUMBER;", CYAN),
                      ("  g_ids t_ids := t_ids();", CYAN),
                      ("AFTER EACH ROW IS BEGIN", GREEN),
                      ("  g_ids.EXTEND; g_ids(g_ids.LAST) := :NEW.account_id;", WHITE),
                      ("END AFTER EACH ROW;", GREEN),
                      ("AFTER STATEMENT IS BEGIN", YEL),
                      ("  FOR i IN 1 .. g_ids.COUNT LOOP check_limit(g_ids(i));", WHITE),
                      ("  END LOOP;", WHITE),
                      ("END AFTER STATEMENT;", YEL), ("END;", WHITE)], a, 23)
        caption(d, ["Collect the ids in after each row. Do the real work in after statement.",
                    "Tip: remove duplicate ids first, so every account is checked only once."][0 if lt < 7 else 1], pr(lt, .6, 1) * fo)

    # 6 BEST: NO TRIGGER
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Even better: do you need a trigger?", SB(46), CYAN, a)
        rows = [("Business rule → in the API package", GREEN, "payment_api.transfer(…)"),
                ("Simple rule → a constraint", CYAN, "CHECK (amount > 0)"),
                ("Totals → computed when needed", PURP, "view / materialized view")]
        for k, (s, col, ex) in enumerate(rows):
            y = 330 + k * 170; al = pr(lt, .6 + k * 2, 1 + k * 2) * fo
            glow_box(d, (70, y, 1010, y + 140), col, al, s, ex, 34, 28)
        caps = ["Triggers are hidden logic. Six months later nobody remembers why an update is slow, or why it fails.",
                "Put business rules in the package that changes the data, and simple rules in constraints.",
                "Keep triggers for auditing and technical columns. Your future self will thank you."]
        caption(d, caps[0 if lt < 2.6 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 7 CHECKLIST
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Checklist", SB(56), YEL, a)
        card_list(d, 330, [("✓ row trigger never queries its own table", GREEN, .5),
                           ("✓ need the table? → compound trigger", GREEN, 1.5),
                           ("✗ autonomous transaction as a workaround", RED, 2.5),
                           ("✓ rules in the API, constraints for simple checks", GREEN, 3.5),
                           ("✓ test with multi-row UPDATE, not only one row", CYAN, 4.5)], lt, fo, 95, 30)
        caption(d, "And always test triggers with a multi row update. One row tests hide this error.", pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("ORA-04091", "→ table mid-change"), ("Row trigger", "→ don't read own table"),
                          ("Autonomous", "→ hides the bug"), ("Compound", "→ collect, then process"),
                          ("Best", "→ logic in the API")],
              "Remember rows in each row, do the work after the statement.", 420)
    else:
        cta(d, t - T[9], "COLLECTIONS", "associative array · nested table · VARRAY", 56)
    return im


if __name__ == "__main__":
    preview(frame, T, "v41_sheet.png")

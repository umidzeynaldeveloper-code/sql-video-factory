from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "DELETE one parent row…", SB(54), WHITE, a)
        code(d, 320, [("DELETE FROM clients WHERE id = 42;", CYAN)], a, 30)
        glow_box(d, (160, 460, 920, 620), RED, pr(lt, 1.2, 1.6) * fo, "PAYMENTS: table locked", "50 sessions waiting", 40, 32)
        ct(d, 720, "foreign key without an index", SB(40), YEL, pr(lt, 2.4, 2.8) * fo)
        caption(d, "One delete, and fifty sessions wait. The culprit: an unindexed foreign key.", pr(lt, 3, 3.4) * fo)

    # 1 TYPES + ERRORS
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "5 rules the database enforces", SB(50), CYAN, a)
        rows = [("PRIMARY KEY / UNIQUE", "ORA-00001", .5), ("FOREIGN KEY: no parent", "ORA-02291", 2),
                ("FOREIGN KEY: child exists", "ORA-02292", 3.5), ("CHECK", "ORA-02290", 5.5), ("NOT NULL", "ORA-01400", 7)]
        for k, (s, e, st) in enumerate(rows):
            y = 330 + k * 120; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 100), 16, fill=mix(CARD, al), outline=mix(CYAN, al), width=3)
            d.text((100, y + 28), s, font=SB(32), fill=mix(WHITE, al)); d.text((780, y + 28), e, font=MB(32), fill=mix(RED, al))
        caps = ["Primary key, unique, foreign key, check and not null.",
                "Break one, and the error tells you exactly which rule.",
                "Missing parent, existing child, or a check that failed."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 2 PK INDEX, FK NO INDEX
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Who creates an index?", SB(54), YEL, a)
        glow_box(d, (70, 340, 500, 520), GREEN, pr(lt, .5, .9) * fo, "PRIMARY KEY", "index ✓ (new or reused)", 36, 28)
        glow_box(d, (580, 340, 1010, 520), GREEN, pr(lt, 1.5, 1.9) * fo, "UNIQUE", "index ✓", 36, 28)
        glow_box(d, (200, 620, 880, 800), RED, pr(lt, 4, 4.4) * fo, "FOREIGN KEY", "NO index ✗ · your job", 40, 30)
        caps = ["A primary key or unique constraint creates an index, or reuses one that fits.",
                "A foreign key creates no index at all.",
                "Indexing it is your job."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 3 UNINDEXED FK LOCK
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Unindexed FK", SB(56), RED, a)
        glow_box(d, (340, 320, 740, 440), CYAN, a, "CLIENTS (parent)", "DELETE id 42", 32, 26)
        flow(d, [(540, 440), (540, 540)], RED, pr(lt, 1.5, 1.9) * fo, t, pr(lt, 1.5, 2.1))
        glow_box(d, (140, 540, 940, 700), RED, pr(lt, 2, 2.4) * fo, "PAYMENTS (child): TABLE LOCK", "for the statement · + full scan for children", 34, 26)
        for k in range(5):
            x = 160 + k * 170; al = pr(lt, 4 + k * .3, 4.4 + k * .3) * fo
            d.ellipse((x, 760, x + 100, 860), fill=mix(CARD, al), outline=mix(YEL, al), width=3)
            ct(d, 790, "wait", SN(26), YEL, al, x + 50)
        code(d, 920, [("CREATE INDEX pay_client_ix ON payments(client_id);", GREEN)], pr(lt, 8, 8.4) * fo, 24)
        caps = ["Delete a parent row, or change its key, and Oracle locks the whole child table.",
                "And it scans the child table to look for children. Sessions start to block, even deadlock.",
                "Index the foreign key columns, and the table lock is gone."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 4 DEFERRABLE
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "DEFERRABLE: check at COMMIT", SB(50), PURP, a)
        code(d, 310, [("ALTER TABLE payments ADD CONSTRAINT pay_cli_fk", PURP), ("  FOREIGN KEY (client_id) REFERENCES clients", PURP),
                      ("  DEFERRABLE INITIALLY DEFERRED;", YEL)], a, 25)
        steps = [("INSERT child", GREEN, 2.5), ("INSERT parent", GREEN, 3.5), ("COMMIT → checked ✓", CYAN, 4.5)]
        for k, (s, col, st) in enumerate(steps):
            glow_box(d, (90 + k * 310, 560, 370 + k * 310, 680), col, pr(lt, st, st + .4) * fo, s, None, 28)
        glow_box(d, (100, 760, 980, 900), RED, pr(lt, 7.5, 7.9) * fo, "invalid at COMMIT?", "ORA-02091: whole transaction rolled back", 34, 26)
        caps = ["A deferrable constraint is checked at commit, not after each statement.",
                "Insert in any order. Only the final state must be valid.",
                "If it isn't, the whole transaction is rolled back."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 5 NOVALIDATE
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "ENABLE NOVALIDATE", SB(56), CYAN, a)
        code(d, 310, [("ALTER TABLE payments MODIFY CONSTRAINT", CYAN), ("  pay_amount_ck ENABLE NOVALIDATE;", CYAN)], a, 28)
        bar(d, 100, 520, 980, 50, .85, DIM, pr(lt, 2, 2.4) * fo, "1 billion old rows", "trusted, not checked")
        bar(d, 100, 680, 980, 50, .15, GREEN, pr(lt, 4, 4.4) * fo, "new rows", "checked ✓")
        ct(d, 830, "clean later → VALIDATE", SB(40), YEL, pr(lt, 7, 7.4) * fo)
        caps = ["Novalidate checks every new row, but trusts the old ones.",
                "On a huge legacy table you protect new data today, without a long scan.",
                "Clean the old data later, then validate."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 6 OPTIMIZER
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Constraints make SQL faster", SB(50), GREEN, a)
        rows = [("validated FK + NOT NULL", "→ join elimination", .5), ("NOT NULL column", "→ COUNT(*) from a small index", 3.5),
                ("CHECK (status IN ('A','C'))", "→ status = 'X' costs nothing", 6.5)]
        for k, (s, ex, st) in enumerate(rows):
            y = 330 + k * 180; al = pr(lt, st, st + .4) * fo
            glow_box(d, (70, y, 1010, y + 150), GREEN, al, s, ex, 34, 30)
        caps = ["A validated foreign key on a not null column lets Oracle drop a join it doesn't need.",
                "Not null lets count star read a small index instead of the table.",
                "A check constraint can prove a condition returns nothing."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 7 CHECKLIST
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Checklist", SB(56), YEL, a)
        card_list(d, 330, [("✓ index FKs you delete / update through", GREEN, .5),
                           ("✓ NOT NULL whenever it's true", GREEN, 1.5),
                           ("✓ CHECK instead of trigger code", GREEN, 2.5),
                           ("✓ name constraints: pay_cli_fk, not SYS_C00123", CYAN, 3.5),
                           ("✗ FK without index on a busy parent", RED, 4.5)], lt, fo, 95, 30)
        caption(d, "Index foreign keys, declare what's true, and name your constraints so errors are readable.", pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("PK / UK", "→ bring an index"), ("FK", "→ index it yourself"),
                          ("Unindexed FK", "→ child table lock"), ("DEFERRABLE", "→ check at COMMIT"),
                          ("NOVALIDATE", "→ trust old rows")],
              "Constraints protect your data and help the optimizer. Index every foreign key.", 420)
    else:
        cta(d, t - T[9], "PIVOT / UNPIVOT", "rows into columns, one statement", 64)
    return im


if __name__ == "__main__":
    preview(frame, T, "v49_sheet.png")

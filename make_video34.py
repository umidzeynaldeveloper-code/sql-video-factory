from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def rowbox(d, x, y, w, txt, col, a, outline=None, fs=28):
    d.rounded_rectangle((x, y, x + w, y + 60), 10, fill=mix(col, a), outline=mix(outline, a) if outline else None, width=4)
    d.text((x + 20, y + 14), txt, font=MN(fs), fill=mix(WHITE, a))

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Daily FX rates: update or insert?", SB(48), WHITE, a)
        code(d, 310, [("UPDATE fx SET rate = :r WHERE ccy = :c;", RED), ("IF SQL%ROWCOUNT = 0 THEN", RED),
                      ("  INSERT INTO fx VALUES (:c, :r);", RED), ("END IF;   -- per row, in a loop", DIM)], pr(lt, .5, .9) * fo, 28)
        ct(d, 560, "2 statements per row · slow · race conditions", SB(30), RED, pr(lt, 1.8, 2.2) * fo)
        code(d, 640, [("MERGE INTO fx USING new_rates …", GREEN)], pr(lt, 2.8, 3.2) * fo, 32)
        ct(d, 760, "one statement, whole set ⚡", SB(40), GREEN, pr(lt, 3.3, 3.7) * fo)
        caption(d, "MERGE: insert what's new, update what exists, in a single pass.", pr(lt, 4, 4.4) * fo)

    # 1 ANATOMY
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Anatomy of MERGE", SB(56), CYAN, a)
        parts = [("MERGE INTO fx t", "the TARGET table", CYAN, .6), ("USING new_rates s", "the SOURCE: table, view or query", PURP, 1.6),
                 ("ON (t.ccy = s.ccy)", "how to match a source row to a target row", YEL, 2.8),
                 ("WHEN MATCHED THEN UPDATE …", "row exists → update it", PINK, 4.4),
                 ("WHEN NOT MATCHED THEN INSERT …", "row is new → insert it", GREEN, 6)]
        for k, (h, s_, col, st) in enumerate(parts):
            y = 320 + k * 150; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 130), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 18), h, font=MB(30), fill=mix(col, al))
            d.text((100, y + 76), s_, font=SN(28), fill=mix(WHITE, al))
        caps = ["A merge names a target table, and a source: another table, a view, or any query.",
                "The ON condition decides which source row belongs to which target row.",
                "Matched rows are updated. Rows that don't exist yet are inserted. Both branches are optional."]
        caption(d, caps[0 if lt < 2.8 else 1 if lt < 4.4 else 2], pr(lt, .6, 1) * fo)

    # 2 ANIMATION
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Watch it run", SB(56), WHITE, a)
        d.text((80, 320), "SOURCE (today)", font=SB(28), fill=mix(PURP, a))
        d.text((600, 320), "TARGET fx", font=SB(28), fill=mix(CYAN, a))
        src = [("USD", "1.70"), ("EUR", "1.98"), ("GBP", "2.31"), ("TRY", "0.05")]
        tgt = {"USD": "1.69", "EUR": "1.95", "GBP": "2.30"}
        for k, (c, r) in enumerate(src):
            st = 1 + k * 1.6
            al = a
            rowbox(d, 70, 370 + k * 90, 400, f"{c}  {r}", (40, 26, 66), al)
            if lt > st:
                p = pr(lt, st, st + .8)
                y = 370 + k * 90
                x = lerp(470, 590, p)
                d.ellipse((x - 12, y + 18, x + 12, y + 42), fill=mix(YEL, pr(lt, st, st + .2) * fo * (1 - pr(lt, st + .8, st + 1))))
        for k, c in enumerate(["USD", "EUR", "GBP"]):
            st = 1 + k * 1.6
            done = lt > st + .8
            r = dict(src)[c] if done else tgt[c]
            rowbox(d, 590, 370 + k * 90, 420, f"{c}  {r}", (60, 50, 20) if done else CARD, a, PINK if done else None)
            if done: d.text((900, 384 + k * 90), "UPD", font=SB(24), fill=mix(PINK, a))
        st = 1 + 3 * 1.6
        if lt > st + .8:
            ai = pr(lt, st + .8, st + 1.2) * fo
            rowbox(d, 590, 370 + 3 * 90, 420, "TRY  0.05", (20, 50, 36), ai, GREEN)
            d.text((900, 384 + 270), "INS", font=SB(24), fill=mix(GREEN, ai))
        card_list(d, 800, [("3 updated · 1 inserted · 1 statement", YEL, 8), ("one JOIN of source and target, not 4 round trips", GREEN, 9.5)], lt, fo, 80, 30)
        caps = ["Each source row is matched to the target on the currency code.",
                "Dollar, euro and pound already exist, so their rates are updated. Lira is new, so it's inserted.",
                "Under the hood, Oracle joins the source to the target once, and applies everything in one statement."]
        caption(d, caps[0 if lt < 2.6 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 3 EXTRAS: WHERE + DELETE
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Conditions & DELETE", SB(56), PINK, a)
        code(d, 310, [("WHEN MATCHED THEN", PINK), ("  UPDATE SET t.rate = s.rate", WHITE),
                      ("  WHERE t.rate != s.rate", YEL), ("  DELETE WHERE s.active = 'N'", RED),
                      ("WHEN NOT MATCHED THEN", GREEN), ("  INSERT … WHERE s.rate IS NOT NULL", YEL)], a, 28)
        card_list(d, 720, [("WHERE on UPDATE: skip unchanged rows → less redo", YEL, 2),
                           ("DELETE: removes matched rows after the update", RED, 4.5),
                           ("WHERE on INSERT: filter what gets added", GREEN, 7)], lt, fo, 80, 29)
        caps = ["Each branch can have its own condition. Update only rows whose rate really changed: fewer changes, less redo.",
                "In the matched branch you can also delete: rows that match and are marked inactive are removed, after the update.",
                "And the insert branch can filter which new rows are added."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 4 ORA-30926
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "ORA-30926: unstable set of rows", SB(46), RED, a)
        d.text((80, 320), "SOURCE", font=SB(28), fill=mix(PURP, a))
        d.text((640, 320), "TARGET", font=SB(28), fill=mix(CYAN, a))
        rowbox(d, 70, 370, 400, "USD  1.70", (40, 26, 66), a)
        rowbox(d, 70, 460, 400, "USD  1.72", (40, 26, 66), a, RED if lt > 2 else None)
        rowbox(d, 630, 415, 380, "USD  1.69", CARD, a, RED if lt > 2 else None)
        if lt > 1:
            al = pr(lt, 1, 1.4) * fo
            arrow(d, 470, 400, 630, 440, YEL, al, 5); arrow(d, 470, 490, 630, 450, YEL, al, 5)
        ct(d, 580, "which rate wins? 1.70 or 1.72?", SB(36), YEL, pr(lt, 2, 2.4) * fo)
        glow_box(d, (110, 650, 970, 770), RED, pr(lt, 3.5, 3.9) * fo, "duplicate key in SOURCE → ORA-30926", None, 32)
        code(d, 820, [("USING (SELECT * FROM (SELECT s.*, ROW_NUMBER() OVER", GREEN),
                      ("        (PARTITION BY ccy ORDER BY ts DESC) rn", GREEN),
                      ("        FROM rates s) WHERE rn = 1) s", GREEN)], pr(lt, 6, 6.4) * fo, 26)
        caps = ["The classic merge error. The source has two rows for the dollar, and both match the same target row.",
                "Oracle refuses to guess which one should win, and raises ORA thirty nine twenty six.",
                "Fix the source: keep exactly one row per key. Row number from the last video, latest rate first, keep row one."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 5 RULES
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Rules to remember", SB(56), YEL, a)
        rules = [("ON columns can't be updated", "ORA-38104", RED, .6),
                 ("1 target row ← max 1 source row", "or ORA-30926", RED, 2.4),
                 ("ON columns should be indexed / unique", "fast match, no duplicates", GREEN, 4.2),
                 ("triggers fire for UPDATE and INSERT", "know your table's triggers", CYAN, 6)]
        for k, (h, s_, col, st) in enumerate(rules):
            y = 320 + k * 165; al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((70, y, W - 70, y + 145), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 24), h, font=SB(32), fill=mix(col, al))
            d.text((100, y + 84), s_, font=SN(28), fill=mix(WHITE, al))
        caps = ["The columns in the ON clause can't be updated in the same merge: ORA thirty eight one zero four.",
                "Each target row may be matched by at most one source row.",
                "Make the matching columns unique and indexed, and remember that insert and update triggers both fire."]
        caption(d, caps[0 if lt < 2.4 else 1 if lt < 4.2 else 2], pr(lt, .6, 1) * fo)

    # 6 PERFORMANCE + ERROR LOGGING
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Speed & bad rows", SB(56), GREEN, a)
        bar(d, 110, 360, 970, 44, pr(lt, .8, 2.5), RED, pr(lt, .6, 1) * fo, "loop: UPDATE, else INSERT", "6 min")
        bar(d, 110, 490, 970, 44, pr(lt, 2.5, 3) * .05, GREEN, pr(lt, 2.3, 2.7) * fo, "one MERGE", "18 s")
        code(d, 610, [("MERGE … ", WHITE), ("LOG ERRORS INTO err$_fx ('EOD 29-10')", YEL), ("REJECT LIMIT UNLIMITED;", YEL)], pr(lt, 4.5, 4.9) * fo, 28)
        card_list(d, 820, [("bad rows go to the error table, the rest succeeds", GREEN, 6.5),
                           ("create it once: DBMS_ERRLOG.CREATE_ERROR_LOG", CYAN, 8)], lt, fo, 80, 29)
        caps = ["One merge over a hundred thousand rows beats a PL SQL loop of updates and inserts by a wide margin.",
                "And if a few rows are bad, add log errors into an error table, with reject limit unlimited.",
                "Bad rows are saved with their error message, and everything else is merged. Create the error table once with DBMS ERRLOG."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 7 CONCURRENCY
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "MERGE is not a lock", SB(56), RED, a)
        for k, (nm, col, x) in enumerate([("S1", CYAN, 200), ("S2", PINK, 880)]):
            d.ellipse((x - 45, 330, x + 45, 420), fill=mix(col, a)); ct(d, 355, nm, SB(32), BG, a, x)
            ct(d, 440, "MERGE new key JPY", SN(26), col, pr(lt, .8 + k * .3, 1.2 + k * .3) * fo, x)
            ct(d, 490, "not matched → INSERT", SN(26), WHITE, pr(lt, 2 + k * .3, 2.4 + k * .3) * fo, x)
        if lt > 3:
            p = pr(lt, 3, 4)
            for x0 in (200, 880):
                y = lerp(520, 640, p)
                d.rounded_rectangle((lerp(x0, 540, p) - 70, y, lerp(x0, 540, p) + 70, y + 50), 8, fill=mix(GREEN, a))
        glow_box(d, (300, 640, 780, 760), RED, pr(lt, 4.5, 4.9) * fo, "ORA-00001", "unique constraint", 36, 28)
        card_list(d, 820, [("keep a UNIQUE constraint on the key", GREEN, 6.5),
                           ("handle DUP_VAL_ON_INDEX → retry the MERGE", YEL, 8)], lt, fo, 80, 30)
        caps = ["Merge is not an atomic upsert. Two sessions merging the same new key at the same moment both see: not matched.",
                "Both try to insert. One wins, the other fails with a unique constraint violation.",
                "So always keep a unique constraint on the key, and handle duplicate value on index by retrying the merge."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("MERGE", "→ update + insert in one pass"), ("ON", "→ how rows match"),
                          ("ORA-30926", "→ dedupe the source"), ("LOG ERRORS", "→ bad rows aside"),
                          ("Concurrency", "→ unique key + retry")],
              "One statement for a whole set, as long as the source has one row per key.", 450)
    else:
        cta(d, t - T[9], "EXCEPTION HANDLING", "stop hiding your errors", 62)
    return im

if __name__ == "__main__":
    preview(frame, T, "v34_sheet.png")

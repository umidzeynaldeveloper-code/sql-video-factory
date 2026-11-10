from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "3 kinds of arrays in PL/SQL", SB(52), WHITE, a)
        for k, (s, col) in enumerate((("Associative array", CYAN), ("Nested table", GREEN), ("VARRAY", PURP))):
            al = pr(lt, .5 + k * .5, .9 + k * .5) * fo
            glow_box(d, (180, 330 + k * 150, 900, 450 + k * 150), col, al, s, None, 40)
        ct(d, 830, "pick the wrong one → ORA-06531, ORA-06533…", SB(32), RED, pr(lt, 2.5, 2.9) * fo)
        caption(d, "Which collection should you use, and why do some of them crash before you store a single value?", pr(lt, 3, 3.4) * fo)

    # 1 ASSOCIATIVE ARRAY
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Associative array = a lookup map", SB(48), CYAN, a)
        code(d, 300, [("TYPE t_rates IS TABLE OF NUMBER", CYAN), ("  INDEX BY VARCHAR2(3);", CYAN), ("l_rate t_rates;", WHITE),
                      ("l_rate('USD') := 1.70;", GREEN), ("l_rate('EUR') := 1.98;", GREEN)], a, 30)
        keys = [("'EUR'", "1.98"), ("'GBP'", "2.27"), ("'USD'", "1.70")]
        for k, (kk, v) in enumerate(keys):
            y = 650 + k * 90; al = pr(lt, 3 + k * .5, 3.4 + k * .5) * fo
            d.rounded_rectangle((260, y, 820, y + 74), 14, fill=mix(CARD, al), outline=mix(CYAN, al), width=3)
            d.text((300, y + 18), kk, font=MB(34), fill=mix(YEL, al)); d.text((620, y + 18), v, font=MB(34), fill=mix(WHITE, al))
        card_list(d, 960, [("no init, no EXTEND · keys can have gaps · PL/SQL only", GREEN, 7)], lt, fo, 80, 29)
        caps = ["The associative array, or index by table, is a map from a key to a value. The key can even be a string.",
                "Just assign. No constructor, no extend. Keys stay sorted, and any gaps are fine.",
                "Perfect as an in-memory cache: load the rates once, then look them up a million times for free."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 2 NESTED TABLE
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Nested table: initialize, then EXTEND", SB(44), GREEN, a)
        lines = [("TYPE t_ids IS TABLE OF NUMBER;", GREEN), ("l_ids t_ids;", WHITE)]
        code(d, 300, lines, a, 30)
        e1 = pr(lt, 1.5, 1.9) * fo
        d.text((100, 440), "l_ids(1) := 42;", font=MB(32), fill=mix(WHITE, e1))
        d.text((560, 440), "ORA-06531 ✗", font=SB(32), fill=mix(RED, e1))
        e2 = pr(lt, 4, 4.4) * fo
        d.text((100, 520), "l_ids := t_ids();  l_ids(1) := 42;", font=MB(30), fill=mix(WHITE, e2))
        d.text((760, 560), "ORA-06533 ✗", font=SB(32), fill=mix(RED, e2))
        e3 = pr(lt, 6.5, 6.9) * fo
        d.text((100, 640), "l_ids := t_ids();  l_ids.EXTEND;", font=MB(30), fill=mix(WHITE, e3))
        d.text((100, 690), "l_ids(1) := 42;", font=MB(30), fill=mix(WHITE, e3)); d.text((760, 690), "✓", font=SB(40), fill=mix(GREEN, e3))
        card_list(d, 800, [("can be a SQL type → usable in SELECT … TABLE()", CYAN, 9)], lt, fo, 80, 29)
        caps = ["A nested table must exist before you use it. Assign without a constructor: reference to uninitialized collection.",
                "Call the constructor, but forget to extend: subscript beyond count.",
                "Constructor, then extend, then assign. And as a SQL type, it can be queried with the table operator."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 3 VARRAY
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "VARRAY: fixed maximum, always dense", SB(46), PURP, a)
        code(d, 300, [("TYPE t_phones IS VARRAY(3) OF VARCHAR2(20);", PURP)], a, 30)
        for k in range(4):
            x = 120 + k * 220; al = pr(lt, 1.5 + k * .8, 1.9 + k * .8) * fo
            col = RED if k == 3 else PURP
            d.rounded_rectangle((x, 450, x + 190, 580), 16, fill=mix(CARD, al), outline=mix(col, al), width=4)
            ct(d, 490, f"({k + 1})", MB(36), col, al, x + 95)
        ct(d, 620, "4th element → ORA-06532 ✗", SB(34), RED, pr(lt, 4.5, 4.9) * fo)
        card_list(d, 720, [("order kept, no holes, small lists", GREEN, 6.5),
                           ("stored inline when used as a column", CYAN, 8)], lt, fo, 80, 30)
        caps = ["A VARRAY has a maximum size you declare up front. Here: three phone numbers.",
                "Try to add a fourth: subscript outside of limit.",
                "Use it for small, ordered lists with a known limit. It never has holes."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 4 SPARSE LOOP TRAP
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The FOR 1 .. COUNT trap", SB(52), RED, a)
        idx = [1, 2, 3, 4, 5]
        for k, n in enumerate(idx):
            x = 110 + k * 180; deleted = n == 3 and lt > 1.5
            al = a
            d.rounded_rectangle((x, 330, x + 150, 450), 14, fill=mix(CARD, al), outline=mix(RED if deleted else GREEN, al), width=3)
            ct(d, 365, "✗" if deleted else str(n), MB(38), RED if deleted else WHITE, al, x + 75)
        code(d, 510, [("l_ids.DELETE(3);", RED), ("FOR i IN 1 .. l_ids.COUNT LOOP  -- COUNT = 4", WHITE), ("  … l_ids(i) …   -- i = 3 → NO_DATA_FOUND", RED)],
             pr(lt, 2, 2.4) * fo, 26)
        code(d, 740, [("i := l_ids.FIRST;", GREEN), ("WHILE i IS NOT NULL LOOP … i := l_ids.NEXT(i);", GREEN)], pr(lt, 6.5, 6.9) * fo, 26)
        caps = ["Delete element three. Now the collection has holes, but count still says four.",
                "Loop from one to count: element three doesn't exist. No data found, and element five is never reached.",
                "Walk it with first and next, or use FORALL with INDICES OF. Holes are skipped safely."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 5 COLLECTIONS IN SQL
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Collections inside SQL", SB(52), CYAN, a)
        code(d, 300, [("CREATE TYPE t_num_list AS TABLE OF NUMBER;", GREEN), ("", WHITE),
                      ("SELECT * FROM accounts", CYAN), ("WHERE id IN (SELECT column_value", CYAN), ("             FROM TABLE(:ids));", CYAN)], a, 28)
        card_list(d, 640, [("pass 500 ids as ONE bind, not 500 literals", GREEN, 3),
                           ("MEMBER OF · MULTISET UNION / EXCEPT", PURP, 5.5),
                           ("12c+: TABLE() also works on package-level types", YEL, 8)], lt, fo, 90, 29)
        caps = ["A nested table created as a SQL type can be used inside a query with the table operator.",
                "Pass five hundred ids as one bind variable: one shared cursor, no giant in-list of literals.",
                "There are also set operators: member of, multiset union and except."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 6 CHOOSE
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Which one?", SB(56), YEL, a)
        rows = [("Lookup by key, cache, BULK COLLECT", "Associative array", CYAN),
                ("Pass a list to SQL / store a set", "Nested table", GREEN),
                ("Small ordered list, fixed max", "VARRAY", PURP)]
        for k, (need, ans, col) in enumerate(rows):
            y = 330 + k * 180; al = pr(lt, .6 + k * 2, 1 + k * 2) * fo
            d.rounded_rectangle((70, y, W - 70, y + 150), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 20), need, font=SN(32), fill=mix(WHITE, al))
            d.text((100, y + 80), "→ " + ans, font=SB(38), fill=mix(col, al))
        caps = ["Need a fast lookup or a buffer for bulk collect? Associative array.",
                "Need to hand a list to SQL, or work with sets? Nested table.",
                "A short, ordered list with a hard limit? VARRAY."]
        caption(d, caps[0 if lt < 2.6 else 1 if lt < 4.6 else 2], pr(lt, .6, 1) * fo)

    # 7 METHODS CHEAT SHEET
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Methods cheat sheet", SB(54), GREEN, a)
        card_list(d, 330, [("COUNT · FIRST · LAST · NEXT · PRIOR", CYAN, .5),
                           ("EXISTS(i) → TRUE/FALSE, never an error", GREEN, 1.5),
                           ("EXTEND / TRIM → nested table, VARRAY", PURP, 2.5),
                           ("DELETE(i) → creates a hole (not VARRAY)", RED, 3.5),
                           ("LIMIT → VARRAY max size", YEL, 4.5)], lt, fo, 95, 30)
        caption(d, "Use exists before reading an element you're not sure about. It's the only method that never raises.", pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Assoc. array", "→ map, no init"), ("Nested table", "→ init + EXTEND"),
                          ("VARRAY", "→ fixed max, dense"), ("Holes", "→ FIRST / NEXT"),
                          ("In SQL", "→ TABLE(:ids)")],
              "Map, set, or short list: pick the collection by its job.", 430)
    else:
        cta(d, t - T[9], "TEMPORARY TABLES", "global · private · session vs commit", 60)
    return im


if __name__ == "__main__":
    preview(frame, T, "v42_sheet.png")

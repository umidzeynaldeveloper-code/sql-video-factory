from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "SELECT * FROM my_plsql_function()", MB(40), CYAN, a)
        ct(d, 310, "…as if it were a table", SB(40), WHITE, pr(lt, .8, 1.2) * fo)
        glow_box(d, (180, 420, 900, 560), PURP, pr(lt, 1.5, 1.9) * fo, "PL/SQL logic", None, 40)
        flow(d, [(540, 560), (540, 660)], GREEN, pr(lt, 2, 2.4) * fo, t, pr(lt, 2, 2.8))
        glow_box(d, (180, 660, 900, 800), GREEN, pr(lt, 2.5, 2.9) * fo, "rows → SQL, joins, reports", None, 36)
        caption(d, "Table functions turn PL/SQL into rows. The pipelined kind streams them, one by one.", pr(lt, 3, 3.4) * fo)

    # 1 NORMAL TABLE FUNCTION
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Normal table function", SB(52), YEL, a)
        p = min(1, max(0, (lt - 1) / 6))
        d.rounded_rectangle((100, 330, 980, 400), 20, fill=mix(OFFB, a))
        d.rounded_rectangle((100, 330, 100 + 880 * p, 400), 20, fill=mix(RED, a))
        ct(d, 345, f"PGA: building {int(p * 1000000):,} rows…", SB(30), WHITE, a)
        ct(d, 470, "first row to the client:", SN(34), DIM, a)
        ct(d, 520, "only after ALL rows are built" if lt < 7 else "now. after 40 s", SB(40), RED, a)
        card_list(d, 650, [("whole collection in memory", RED, 3), ("nothing returned until the end", YEL, 5)], lt, fo, 80, 30)
        caps = ["A normal table function fills a whole collection in memory, then returns it at the end.",
                "A million rows means a million rows of PGA, and the caller waits for all of them.",
                "Nothing arrives until the last row is built."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 2 PIPELINED STREAMING
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "PIPELINED: stream rows as you go", SB(48), GREEN, a)
        glow_box(d, (70, 340, 420, 480), PURP, a, "function", "PIPE ROW(r)", 34, 28)
        glow_box(d, (660, 340, 1010, 480), CYAN, a, "SQL caller", "consumes", 34, 28)
        for k in range(5):
            ph = ((lt * .7) + k * .2) % 1
            x = 420 + 240 * ph
            d.rounded_rectangle((x - 30, 395, x + 30, 425), 8, fill=mix(GREEN, a))
        bar(d, 100, 600, 980, 46, .08, GREEN, pr(lt, 3, 3.4) * fo, "PGA used", "small, constant")
        card_list(d, 720, [("first rows arrive immediately", GREEN, 5), ("memory stays flat for any row count", CYAN, 7)], lt, fo, 80, 30)
        caps = ["A pipelined function sends each row the moment it's ready, with pipe row.",
                "The caller starts working on the first rows while the function is still producing the rest.",
                "Memory stays small and flat, whether you return a hundred rows or a hundred million."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 3 CODE
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The code", SB(56), GREEN, a)
        code(d, 300, [("CREATE TYPE t_pay_row AS OBJECT (id NUMBER, fee NUMBER);", CYAN),
                      ("CREATE TYPE t_pay_tab AS TABLE OF t_pay_row;", CYAN), ("", WHITE),
                      ("FUNCTION fees RETURN t_pay_tab PIPELINED IS", PURP),
                      ("BEGIN", WHITE),
                      ("  FOR p IN (SELECT id, amount FROM payments) LOOP", WHITE),
                      ("    PIPE ROW (t_pay_row(p.id, calc_fee(p.amount)));", GREEN),
                      ("  END LOOP;", WHITE),
                      ("  RETURN;", YEL), ("END;", WHITE)], a, 24)
        code(d, 820, [("SELECT * FROM TABLE(fees());  -- 12.2+: FROM fees()", CYAN)], pr(lt, 6, 6.4) * fo, 26)
        caps = ["Declare a row type and a table type, mark the function pipelined, and pipe each row out.",
                "End with a plain return: no value, the rows have already been sent.",
                "Then select from it like a table. From twelve two, even the table keyword is optional."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 4 USE CASES
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Where it shines", SB(54), CYAN, a)
        rows = [("Parse a CSV / CLOB into rows", "join it with real tables", GREEN),
                ("Complex PL/SQL rules in a report", "one SELECT for the BI tool", CYAN),
                ("ETL transform chain", "f3(f2(f1(source)))", PURP)]
        for k, (s, ex, col) in enumerate(rows):
            y = 330 + k * 170; al = pr(lt, .6 + k * 2, 1 + k * 2) * fo
            glow_box(d, (70, y, 1010, y + 140), col, al, s, ex, 34, 28)
        caps = ["Turn a file or a big text into rows, and join it with your tables in plain SQL.",
                "Give a reporting tool a single select, while the hard rules stay in PL/SQL.",
                "Or chain several functions into a streaming transformation, with no staging tables in between."]
        caption(d, caps[0 if lt < 2.6 else 1 if lt < 4.6 else 2], pr(lt, .6, 1) * fo)

    # 5 NO_DATA_NEEDED
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Caller stops early?", SB(54), YEL, a)
        code(d, 300, [("SELECT * FROM TABLE(fees()) FETCH FIRST 5 ROWS ONLY;", CYAN)], a, 28)
        ae = pr(lt, 2, 2.4) * fo
        glow_box(d, (120, 450, 960, 590), YEL, ae, "NO_DATA_NEEDED", "raised inside the function at the next PIPE ROW", 38, 26)
        code(d, 660, [("EXCEPTION WHEN NO_DATA_NEEDED THEN", PURP), ("  close_files; RAISE;", WHITE)], pr(lt, 5, 5.4) * fo, 28)
        caps = ["If the query needs only five rows, Oracle stops the function early.",
                "It does that by raising no data needed inside it, at the next pipe row.",
                "Catch it to close files or cursors you opened. Then re-raise it."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    # 6 CARDINALITY
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The optimizer guesses 8168 rows", SB(50), RED, a)
        glow_box(d, (70, 330, 500, 480), DIM, a, "estimate", "8 168 rows", 36, 30)
        glow_box(d, (580, 330, 1010, 480), RED, pr(lt, 1.5, 1.9) * fo, "reality", "12 or 5 000 000", 36, 30)
        card_list(d, 560, [("wrong join method, wrong order", RED, 3.5),
                           ("/*+ CARDINALITY(f 50) */ quick hint", YEL, 5.5),
                           ("better: dynamic sampling or statistics extensions", GREEN, 7.5)], lt, fo, 90, 30)
        caps = ["Oracle can't know how many rows a function will return. With 8 K blocks it assumes eight one six eight.",
                "If the real number is twelve, or five million, joins around it get the wrong plan.",
                "Tell the optimizer: a cardinality hint, dynamic sampling, or the extensible optimizer interface."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 7 PARALLEL
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Bonus: parallel pipelines", SB(52), PURP, a)
        code(d, 300, [("FUNCTION fees(c SYS_REFCURSOR) RETURN t_pay_tab", WHITE), ("  PIPELINED PARALLEL_ENABLE", PURP),
                      ("  (PARTITION c BY ANY) IS …", PURP)], a, 27)
        for k in range(4):
            x = 120 + k * 220; al = pr(lt, 2.5 + k * .4, 2.9 + k * .4) * fo
            glow_box(d, (x, 560, x + 180, 680), PURP, al, f"PX {k + 1}", None, 32)
        card_list(d, 760, [("input cursor split across parallel servers", GREEN, 5.5),
                           ("each server runs its own copy of the function", CYAN, 7.5)], lt, fo, 80, 30)
        caps = ["Pass the input as a ref cursor and add parallel enable.",
                "Oracle splits the input rows between parallel servers, and each one runs the function on its share.",
                "Perfect for heavy transformations over big tables."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Table function", "→ PL/SQL as rows"), ("PIPELINED", "→ stream, flat memory"),
                          ("PIPE ROW", "→ send one row"), ("NO_DATA_NEEDED", "→ clean up, re-raise"),
                          ("8168", "→ fix the estimate")],
              "Stream rows from PL/SQL straight into SQL.", 480)
    else:
        cta(d, t - T[9], "FULL TUNING GUIDE", "why is my query slow? (long video)", 60)
    return im


if __name__ == "__main__":
    preview(frame, T, "v44_sheet.png")

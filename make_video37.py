from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Search customer by name", SB(50), WHITE, a)
        d.rounded_rectangle((140, 320, 940, 410), 14, fill=mix(CARD, a), outline=mix(CYAN, a), width=3)
        txt = "' OR '1'='1"
        n = int(min(len(txt), max(0, (lt - .6) * 8)))
        d.text((170, 342), txt[:n] + ("|" if int(t * 3) % 2 else ""), font=MN(38), fill=mix(YEL, a))
        ab = pr(lt, 2, 2.4) * fo
        bar(d, 110, 520, 970, 44, pr(lt, 2.2, 3.2), RED, ab, "rows returned", "ALL 1 200 000 customers")
        ct(d, 680, "One input. Whole table leaked.", SB(44), RED, pr(lt, 3.2, 3.6) * fo)
        caption(d, "That's SQL injection. It only happens with dynamic SQL built the wrong way.", pr(lt, 4, 4.4) * fo)

    # 1 STATIC vs DYNAMIC
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Static vs dynamic SQL", SB(54), CYAN, a)
        glow_box(d, (70, 320, 510, 560), GREEN, pr(lt, .6, 1) * fo, "STATIC", "known at compile time · auto binds · checked", 36, 22)
        glow_box(d, (570, 320, 1010, 560), YEL, pr(lt, 2, 2.4) * fo, "DYNAMIC", "text built at runtime", 36, 24)
        card_list(d, 620, [("table / column name decided at runtime", YEL, 3.5),
                           ("optional search filters", YEL, 4.5),
                           ("DDL inside PL/SQL", YEL, 5.5),
                           ("everything else → STATIC SQL", GREEN, 7.5)], lt, fo, 80, 31)
        caps = ["Static SQL is written directly in PL/SQL. It's checked at compile time and uses bind variables automatically. Injection is impossible.",
                "Dynamic SQL is a string built at runtime and executed with execute immediate or a ref cursor.",
                "You need it only for runtime table or column names, optional filters, or DDL. For everything else, stay static."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 2 CONCAT vs BIND
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The bug: concatenation", SB(54), RED, a)
        code(d, 310, [("EXECUTE IMMEDIATE", RED), ("  'SELECT … WHERE name = ''' || p_name || ''''", RED)], a, 26)
        ab = pr(lt, 1.8, 2.2) * fo
        d.text((90, 470), "SQL Oracle actually runs:", font=SB(28), fill=mix(DIM, ab))
        d.rounded_rectangle((70, 510, 1010, 600), 14, fill=mix((60, 22, 34), ab))
        d.text((95, 535), "… WHERE name = '", font=MN(30), fill=mix(WHITE, ab))
        x = 95 + d.textlength("… WHERE name = '", font=MN(30))
        d.text((x, 535), "' OR '1'='1", font=MN(30), fill=mix(YEL, ab))
        d.text((x + d.textlength("' OR '1'='1", font=MN(30)), 535), "'", font=MN(30), fill=mix(WHITE, ab))
        ct(d, 620, "user input became CODE", SB(34), RED, pr(lt, 3.5, 3.9) * fo)
        ag = pr(lt, 5.5, 5.9) * fo
        code(d, 700, [("EXECUTE IMMEDIATE", GREEN), ("  'SELECT … WHERE name = :n'", GREEN), ("  USING p_name;", GREEN)], ag, 28)
        ct(d, 900, "with a bind, input is only DATA ✓", SB(34), GREEN, pr(lt, 7, 7.4) * fo)
        caps = ["The mistake is gluing user input into the SQL text with the concatenation operator.",
                "The quote in the input closes the string, and OR one equals one becomes part of the condition. The input turned into code.",
                "With a bind variable, the SQL text never changes. Whatever the user types is only a value, never code."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 3 UNION ATTACK
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "It gets worse: UNION", SB(54), RED, a)
        d.rounded_rectangle((70, 320, 1010, 420), 14, fill=mix(CARD, a), outline=mix(YEL, a), width=3)
        d.text((95, 345), "x' UNION SELECT username, pwd_hash", font=MN(28), fill=mix(YEL, a))
        d.text((95, 380), "   FROM app_users --", font=MN(28), fill=mix(YEL, a))
        rows = [("Ali Aliyev", WHITE), ("admin  · 9f2c…", RED), ("teller1 · a7d1…", RED), ("ceo    · 3b8e…", RED)]
        for k, (r, col) in enumerate(rows):
            y = 480 + k * 85; al = pr(lt, 2 + k * .6, 2.4 + k * .6) * fo
            d.rounded_rectangle((110, y, 970, y + 70), 12, fill=mix(CARD, al), outline=mix(col, al), width=2)
            d.text((140, y + 18), r, font=MN(30), fill=mix(col, al))
        glow_box(d, (110, 860, 970, 980), RED, pr(lt, 5.5, 5.9) * fo, "any table the schema can read", "a search box became a data export", 32, 26)
        caps = ["A smarter attacker adds UNION SELECT, and reads a completely different table through your search screen.",
                "User names and password hashes come back as if they were customer names.",
                "Whatever the package owner can read, the attacker can read. That's why injection in a bank is critical."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 4 IDENTIFIERS: DBMS_ASSERT
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Names can't be binds", SB(54), YEL, a)
        code(d, 310, [("'SELECT * FROM ' || p_table   -- table name", YEL), (":tab won't work for a table name ✗", RED)], a, 28)
        code(d, 470, [("l_tab := DBMS_ASSERT.SQL_OBJECT_NAME(p_table);", GREEN),
                      ("l_col := DBMS_ASSERT.SIMPLE_SQL_NAME(p_col);", GREEN)], pr(lt, 2.5, 2.9) * fo, 26)
        ac = pr(lt, 5, 5.4) * fo
        d.rounded_rectangle((70, 650, 1010, 760), 14, fill=mix(CARD, ac), outline=mix(GREEN, ac), width=3)
        d.text((100, 668), "ACCOUNTS", font=MN(30), fill=mix(GREEN, ac)); d.text((640, 668), "✓ allowed", font=SB(30), fill=mix(GREEN, ac))
        d.text((100, 712), "x UNION SELECT…", font=MN(28), fill=mix(RED, ac)); d.text((640, 712), "✗ ORA-44002", font=SB(30), fill=mix(RED, ac))
        card_list(d, 820, [("best: a WHITELIST (CASE p_table WHEN …)", CYAN, 7.5)], lt, fo, 80, 30)
        caps = ["Bind variables work only for values. A table or column name can't be a bind, so it has to go into the text.",
                "Validate it first. DBMS ASSERT checks that the input is a real object name or a simple identifier, and nothing more.",
                "Anything else raises an error before the SQL runs. Even better: allow only names from a fixed whitelist."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 5 OPTIONAL FILTERS
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Optional filters, safely", SB(54), CYAN, a)
        code(d, 310, [("l_sql := 'SELECT … FROM accounts WHERE 1=1';", WHITE),
                      ("IF p_branch IS NOT NULL THEN", CYAN), ("  l_sql := l_sql || ' AND branch_id = :b';", GREEN),
                      ("ELSE", CYAN), ("  l_sql := l_sql || ' AND (1=1 OR :b IS NULL)';", GREEN), ("END IF;", CYAN),
                      ("OPEN c FOR l_sql USING p_branch;", YEL)], a, 24)
        card_list(d, 740, [("values ALWAYS as binds, only fixed text concatenated", GREEN, 4),
                           ("same number of binds in every variant", YEL, 6),
                           ("many variants? DBMS_SQL binds by name", CYAN, 8)], lt, fo, 80, 29)
        caps = ["Search screens often need optional filters. Build the SQL text, but only ever append fixed text written by you.",
                "Every value goes in as a bind. A small trick keeps the number of binds the same in every variant, so USING always matches.",
                "With many optional filters, DBMS SQL lets you bind by name. And every variant is a shareable cursor, as in video twenty six."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 6 DEFINER RIGHTS
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Whose privileges run it?", SB(54), PURP, a)
        glow_box(d, (70, 330, 510, 500), RED, a, "DEFINER rights", "runs as the OWNER (default)", 34, 26)
        glow_box(d, (570, 330, 1010, 500), GREEN, pr(lt, 2, 2.4) * fo, "AUTHID CURRENT_USER", "runs as the CALLER", 30, 26)
        ab = pr(lt, 3.5, 3.9) * fo
        d.ellipse((240, 580, 340, 680), fill=mix(YEL, ab)); ct(d, 612, "app", SB(28), BG, ab, 290)
        arrow(d, 340, 630, 520, 630, YEL, ab, 5)
        glow_box(d, (520, 570, 1000, 690), RED, ab, "injected SQL as the OWNER", "all tables of the schema", 28, 22)
        card_list(d, 760, [("injection + definer rights = owner's full power", RED, 5.5),
                           ("least privilege: app user gets EXECUTE only", GREEN, 7.5)], lt, fo, 80, 30)
        caps = ["By default, a package runs with the privileges of its owner, not of the caller.",
                "So an injectable package owned by a powerful schema hands the attacker that schema's power.",
                "Keep owners' privileges minimal, give the application only execute rights, and consider invoker rights where it fits."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 7 CHECKLIST
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Injection checklist", SB(56), GREEN, a)
        steps = [("static SQL whenever possible", GREEN), ("values → bind variables, ALWAYS", CYAN),
                 ("names → DBMS_ASSERT / whitelist", YEL), ("least privilege for owners", PURP),
                 ("code review: search for || near EXECUTE IMMEDIATE", PINK)]
        for k, (s_, col) in enumerate(steps):
            y = 330 + k * 140; al = pr(lt, .6 + k * 1.6, 1 + k * 1.6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 120), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.ellipse((95, y + 30, 155, y + 90), fill=mix(col, al)); ct(d, y + 40, str(k + 1), SB(34), BG, al, 125)
            for j, ln in enumerate(wrap(d, s_, SB(30), 780)): d.text((180, y + 22 + j * 40), ln, font=SB(30), fill=mix(WHITE, al))
        caps = ["Use static SQL whenever you can, and bind variables for every value in dynamic SQL.",
                "Validate names with DBMS ASSERT or a whitelist, and keep privileges minimal.",
                "In code review, search for the concatenation operator near execute immediate. That's where injections hide."]
        caption(d, caps[0 if lt < 3.8 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Concatenation", "→ input becomes code"), ("Bind", "→ input stays data"),
                          ("UNION", "→ any table leaks"), ("DBMS_ASSERT", "→ for names"),
                          ("Definer rights", "→ owner's power")],
              "Values as binds, names validated, privileges minimal. No injection.", 460)
    else:
        cta(d, t - T[9], "DBMS_SCHEDULER", "let the database run your batches", 66)
    return im

if __name__ == "__main__":
    preview(frame, T, "v37_sheet.png")

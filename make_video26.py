from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def step_box(d, y, txt, col, a, x0=200, x1=880, hl=False):
    d.rounded_rectangle((x0, y, x1, y + 90), 16, fill=mix(CARD, a), outline=mix(col, a), width=5 if hl else 3)
    ct(d, y + 26, txt, SB(32), col, a, (x0 + x1) / 2)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Same query. 10 000 times.", SB(54), WHITE, a)
        n = int(min(6, max(0, (lt - .5) * 3)))
        for k in range(n):
            d.text((110, 320 + k * 52), f"... WHERE id = {1001 + k * 37};", font=MN(32), fill=mix(YEL, a))
        p = pr(lt, 1.5, 3.2)
        bar(d, 110, 680, 970, 44, p * .95, RED, pr(lt, 1.4, 1.8) * fo, "CPU", f"{int(95 * p)}%")
        bar(d, 110, 800, 970, 44, p * .7, PINK, pr(lt, 1.8, 2.2) * fo, "hard parse time", f"{int(70 * p)}% of DB time")
        ct(d, 930, "Oracle re-plans EVERY one of them", SB(40), YEL, pr(lt, 3.2, 3.6) * fo)
        caption(d, "Literals force a hard parse every time. Let's see what happens inside the shared pool.", pr(lt, 4, 4.4) * fo)

    # 1 SHARED POOL MAP
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Inside the SHARED POOL", SB(54), WHITE, a)
        d.rounded_rectangle((60, 310, 1020, 900), 28, outline=mix(DIM, a), width=3)
        d.text((90, 320), "SGA → SHARED POOL", font=SB(28), fill=mix(DIM, a))
        glow_box(d, (100, 380, 980, 600), PURP, pr(lt, .8, 1.2) * fo, None, None)
        d.text((130, 395), "LIBRARY CACHE", font=SB(34), fill=mix(PURP, pr(lt, .8, 1.2) * fo))
        for k, nm in enumerate(["cursor A", "cursor B", "pkg EOD", "proc X"]):
            al = pr(lt, 1.4 + k * .4, 1.8 + k * .4) * fo
            d.rounded_rectangle((130 + k * 210, 470, 320 + k * 210, 570), 14, fill=mix((40, 26, 66), al))
            ct(d, 500, nm, SN(28), WHITE, al, 225 + k * 210)
        glow_box(d, (100, 630, 520, 860), CYAN, pr(lt, 4, 4.4) * fo, "DICTIONARY", "CACHE: tables, columns, privs", 32, 24)
        glow_box(d, (560, 630, 980, 860), GREEN, pr(lt, 6, 6.4) * fo, "RESULT", "CACHE (video 19)", 32, 24)
        caps = ["The shared pool is part of the SGA. Its heart is the library cache: parsed SQL cursors and PL/SQL code, shared by everyone.",
                "The dictionary cache keeps metadata: tables, columns, and privileges, so parsing doesn't read the dictionary from disk.",
                "And the result cache from video nineteen also lives here."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 2 PARSE FLOW
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "What happens when you parse", SB(50), WHITE, a)
        steps = [("1. syntax check", WHITE, .6), ("2. semantic check (dictionary)", CYAN, 1.6), ("3. hash the SQL text → look up", YEL, 2.6)]
        for k, (tx, col, st) in enumerate(steps):
            y = 320 + k * 125; al = pr(lt, st, st + .4) * fo
            step_box(d, y, tx, col, al)
            if k: arrow(d, 540, y - 35, 540, y, WHITE, al, 5)
        y = 700
        af = pr(lt, 4, 4.4) * fo; ah = pr(lt, 6, 6.4) * fo
        arrow(d, 440, 660, 290, y, GREEN, af, 5); arrow(d, 640, 660, 790, y, RED, ah, 5)
        glow_box(d, (60, y + 20, 520, y + 200), GREEN, af, "FOUND", "SOFT parse: reuse plan", 40, 28)
        glow_box(d, (560, y + 20, 1020, y + 200), RED, ah, "NOT FOUND", "HARD parse", 40, 28)
        for k, tx in enumerate(["optimize: 1000s of plans", "allocate memory (latches!)", "load into library cache"]):
            al = pr(lt, 7 + k * .6, 7.4 + k * .6) * fo
            d.text((590, y + 220 + k * 50), "• " + tx, font=SN(28), fill=mix(WHITE, al))
        caps = ["Every SQL is checked: is the syntax valid, do the tables and columns exist, do you have the privileges.",
                "Then Oracle hashes the exact SQL text and looks for it in the library cache. Found? That's a soft parse: reuse the plan.",
                "Not found is a hard parse: the optimizer evaluates many plans, allocates shared memory under latches, and loads the new cursor. Very expensive."]
        caption(d, caps[0 if lt < 2.6 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 3 LITERALS vs BINDS
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Literals vs bind variables", SB(52), YEL, a)
        glow_box(d, (60, 310, 520, 420), RED, a, "WHERE id = 1001", "literal", 32, 24)
        glow_box(d, (560, 310, 1020, 420), GREEN, a, "WHERE id = :id", "bind", 32, 24)
        nl = int(min(40, max(0, (lt - 1) * 6)))
        for k in range(nl):
            r, c = divmod(k, 5); x = 80 + c * 88; y = 450 + r * 62
            d.rounded_rectangle((x, y, x + 76, y + 50), 8, fill=mix(RED, a * .85))
        ab = pr(lt, 1, 1.4) * fo
        d.rounded_rectangle((690, 450, 890, 600), 16, fill=mix(GREEN, ab))
        ct(d, 495, "1 cursor", SB(34), BG, ab, 790)
        execs = int(min(10000, max(0, (lt - 1) * 1500)))
        ct(d, 630, f"executed {execs}×", SB(30), GREEN, ab, 790)
        ct(d, 960, f"{int(min(10000, max(0, (lt - 1) * 1500)))} cursors", SB(34), RED, pr(lt, 1, 1.4) * fo, 290)
        card_list(d, 1030, [("PL/SQL static SQL binds automatically ✓", GREEN, 7.5)], lt, fo, 80, 30)
        caps = ["With literals, every value makes a different SQL text, a different hash, and a brand new cursor. Ten thousand hard parses.",
                "With a bind variable, the text never changes. One cursor, parsed once, executed ten thousand times.",
                "Good news for PL/SQL developers: static SQL in PL/SQL uses binds automatically. The danger is dynamic SQL built by concatenation."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 4 HARD vs SOFT vs NO PARSE
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Hard → soft → no parse", SB(54), CYAN, a)
        bars = [("hard parse", 1.0, RED, "~ms, latches, CPU"), ("soft parse", .15, YEL, "lookup + checks"),
                ("no parse (cached cursor)", .02, GREEN, "just EXECUTE")]
        for k, (nm, p, col, v) in enumerate(bars):
            bar(d, 110, 380 + k * 140, 970, 50, pr(lt, .8 + k * 1.5, 1.8 + k * 1.5) * p, col, pr(lt, .6 + k * 1.5, 1 + k * 1.5) * fo, nm, v)
        ab = pr(lt, 6, 6.4) * fo
        glow_box(d, (110, 820, 970, 950), GREEN, ab, "parse ONCE, execute MANY", None, 40)
        card_list(d, 990, [("PL/SQL caches cursors · SESSION_CACHED_CURSORS", CYAN, 8)], lt, fo, 80, 30)
        caps = ["A hard parse costs milliseconds of CPU and grabs shared pool latches. A soft parse is much cheaper, but still a lookup.",
                "Best of all is no parse: the session keeps the cursor open and simply executes it again.",
                "PL/SQL does this for you, and session cached cursors helps applications. Parse once, execute many."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 5 ORA-04031
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "ORA-04031: out of shared memory", SB(46), RED, a)
        d.rounded_rectangle((80, 320, 1000, 700), 20, outline=mix(DIM, a), width=3)
        n = int(min(60, max(0, lt * 9)))
        rng = __import__("random").Random(7)
        for k in range(60):
            r, c = divmod(k, 12); x = 100 + c * 74; y = 340 + r * 70
            if k < n:
                free = rng.random() < .25
                d.rounded_rectangle((x, y, x + 66, y + 60), 6, fill=mix(GREEN if free else RED, a * (.5 if free else .85)))
        ab = pr(lt, 5, 5.4) * fo
        d.rounded_rectangle((300, 730, 780, 820), 14, fill=mix(YEL, ab))
        ct(d, 752, "need 4 KB in one piece", SB(32), BG, ab, 540)
        ct(d, 850, "free memory exists… but in tiny holes", SN(32), WHITE, pr(lt, 6.5, 6.9) * fo)
        card_list(d, 930, [("cause: thousands of one-time literal cursors", RED, 8),
                           ("fix: binds first, then size the pool", GREEN, 9.5)], lt, fo, 80, 30)
        caps = ["Thousands of single-use cursors fill the shared pool, and keep getting aged out and replaced.",
                "Memory becomes fragmented. There's free space, but only in small pieces, and a large allocation fails: ORA zero four zero three one.",
                "Increasing the pool only delays it. The real fix is sharable SQL with bind variables."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 6 CHILD CURSORS
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "One SQL text, many children", SB(52), PURP, a)
        glow_box(d, (290, 320, 790, 440), PURP, a, "parent: SELECT … :id", "same text, same hash", 32, 24)
        kids = [("child 0", "bind NUMBER", CYAN), ("child 1", "bind VARCHAR2(32)", YEL),
                ("child 2", "other optimizer env", PINK), ("child 3", "ACS: rare value", GREEN)]
        for k, (nm, why, col) in enumerate(kids):
            x = 90 + k * 235; al = pr(lt, 1 + k * 1, 1.4 + k * 1) * fo
            arrow(d, 540, 440, x + 105, 540, DIM, al, 4)
            glow_box(d, (x, 540, x + 210, 700), col, al, nm, why, 28, 20)
        ah = pr(lt, 6, 6.4) * fo
        glow_box(d, (110, 770, 970, 890), RED, ah, "VERSION_COUNT 500 → mutex waits", None, 34)
        code(d, 930, [("V$SQL_SHARED_CURSOR  -- WHY not shared", CYAN)], pr(lt, 8, 8.4) * fo, 28)
        caps = ["Even with the same text, Oracle may need several child cursors: different bind types, a different optimizer setting, or adaptive cursor sharing.",
                "A few children are normal. Hundreds mean every execution searches a long list under a mutex.",
                "V dollar SQL shared cursor tells you exactly why a child couldn't be shared."]
        caption(d, caps[0 if lt < 6 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 7 DIAGNOSE
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Find the literal SQL", SB(56), GREEN, a)
        bar(d, 110, 370, 970, 44, pr(lt, .8, 1.8) * .9, RED, pr(lt, .6, 1) * fo, "AWR: hard parses / sec", "450")
        bar(d, 110, 490, 970, 44, pr(lt, 1.4, 2.4) * .05, GREEN, pr(lt, 1.2, 1.6) * fo, "healthy", "< 10")
        code(d, 600, [("SELECT force_matching_signature,", CYAN), ("       COUNT(*) copies, MIN(sql_text)", CYAN),
                      ("FROM   v$sqlarea", CYAN), ("GROUP  BY force_matching_signature", CYAN),
                      ("HAVING COUNT(*) > 100;", CYAN)], pr(lt, 3, 3.4) * fo, 28)
        card_list(d, 960, [("CURSOR_SHARING=FORCE: band-aid, not a cure", YEL, 8)], lt, fo, 80, 30)
        caps = ["In the AWR load profile, check hard parses per second. Hundreds per second is a red flag.",
                "Group V dollar SQL area by force matching signature: statements that differ only in literals share it. A high count shows the culprit.",
                "Cursor sharing force replaces literals automatically, but treat it as a temporary band-aid. Fix the code with binds."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Library cache", "→ shared cursors & PL/SQL"), ("Hard parse", "→ plan + memory + latches"),
                          ("Binds", "→ 1 cursor, many executions"), ("ORA-04031", "→ fragmented pool"),
                          ("Children", "→ V$SQL_SHARED_CURSOR")],
              "Parse once, execute many. Bind variables keep the shared pool healthy.", 450)
    else:
        cta(d, t - T[9], "BUFFER CACHE", "how Oracle keeps hot blocks in memory", 66)
    return im

if __name__ == "__main__":
    preview(frame, T, "v26_sheet.png")

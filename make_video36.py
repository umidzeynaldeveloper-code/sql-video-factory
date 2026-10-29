from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def sess(d, x, y, col, a, lbl, r=40):
    d.ellipse((x - r, y - r, x + r, y + r), fill=mix(col, a))
    ct(d, y - 16, lbl, SB(26), BG, a, x)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "14:00 · deploy batch_pkg ✓", SB(48), GREEN, a)
        ct(d, 310, "14:01 · the app:", SN(36), DIM, pr(lt, .8, 1.2) * fo)
        ab = pr(lt, 1.4, 1.8) * fo
        d.rounded_rectangle((70, 380, 1010, 560), 18, fill=mix((60, 22, 34), ab), outline=mix(RED, ab), width=4)
        d.text((100, 400), "ORA-04068: existing state of", font=MB(32), fill=mix(RED, ab))
        d.text((100, 445), "packages has been discarded", font=MB(32), fill=mix(RED, ab))
        d.text((100, 500), "ORA-04061 · ORA-04065", font=MB(28), fill=mix(PINK, ab))
        n = int(min(40, max(0, (lt - 2) * 25)))
        ct(d, 620, f"errors: {n}", MB(56), RED, pr(lt, 2, 2.4) * fo)
        ct(d, 740, "The code is correct. So why?", SB(44), YEL, pr(lt, 3.2, 3.6) * fo)
        caption(d, "Every PL/SQL developer meets this error after a deploy. Let's see where it comes from.", pr(lt, 4, 4.4) * fo)

    # 1 PACKAGE STATE
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Package state lives in EACH session", SB(46), WHITE, a)
        code(d, 310, [("PACKAGE BODY batch_pkg IS", CYAN), ("  g_run_date DATE;       -- global", YEL),
                      ("  g_cache    t_rates;    -- global", YEL), ("BEGIN  -- init block, runs once", PURP)], a, 28)
        for k in range(3):
            x = 200 + k * 340; al = pr(lt, 2 + k * .7, 2.4 + k * .7) * fo
            sess(d, x, 640, PINK, al, f"S{k + 1}")
            d.rounded_rectangle((x - 140, 700, x + 140, 860), 14, fill=mix(CARD, al), outline=mix(YEL, al), width=3)
            ct(d, 712, "own copy", SN(24), DIM, al, x)
            ct(d, 750, "g_run_date", MN(24), YEL, al, x)
            ct(d, 790, "g_cache", MN(24), YEL, al, x)
        card_list(d, 900, [("first call → init block runs → state lives until logout", CYAN, 6),
                           ("connection pools keep sessions for DAYS", PINK, 8.5)], lt, fo, 80, 29)
        caps = ["Package-level variables, declared outside any procedure, are package state.",
                "Each session gets its own private copy, initialized the first time it calls the package.",
                "That state lives until the session ends. And application connection pools keep sessions open for days."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 2 RECOMPILE DISCARDS STATE
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Recompile = old state is invalid", SB(48), RED, a)
        v = "v1" if lt < 2.5 else "v2"
        glow_box(d, (340, 320, 740, 450), GREEN if v == "v2" else CYAN, a, f"batch_pkg {v}", "in the library cache", 36, 26)
        if 2 < lt < 3: ct(d, 470, "CREATE OR REPLACE …", MB(30), YEL, a)
        sess(d, 220, 640, PINK, a, "S1")
        d.rounded_rectangle((90, 700, 350, 790), 12, fill=mix(CARD, a), outline=mix(RED if lt > 3 else YEL, a), width=3)
        ct(d, 725, "state of v1", SN(26), RED if lt > 3 else YEL, a, 220)
        if lt > 4:
            al = pr(lt, 4, 4.4) * fo
            arrow(d, 300, 620, 480, 450, PINK, al, 5)
            glow_box(d, (480, 560, 1010, 680), RED, pr(lt, 4.6, 5) * fo, "1st call: ORA-04068", "state discarded", 32, 26)
        if lt > 7:
            glow_box(d, (480, 720, 1010, 840), GREEN, pr(lt, 7, 7.4) * fo, "2nd call: works ✓", "re-initialized with v2", 32, 26)
        caps = ["You deploy a new version of the package. Sessions that already used it still hold state built for the old version.",
                "On their next call, Oracle can't keep that old state. It discards it, and raises ORA-04068 once.",
                "The second call works: the package is initialized again. But that first error hits the user."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 3 SPEC vs BODY DEPENDENCIES
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Spec vs body: who gets invalid?", SB(48), YEL, a)
        glow_box(d, (90, 330, 500, 450), CYAN, a, "batch_pkg SPEC", None, 32)
        glow_box(d, (580, 330, 990, 450), PURP, a, "batch_pkg BODY", None, 32)
        deps = ["interest_pkg", "report_pkg", "fx_job"]
        bad = lt > 1.5 and lt < 6
        for k, nm in enumerate(deps):
            y = 560 + k * 110
            col = RED if bad else GREEN
            glow_box(d, (90, y, 500, y + 90), col, a, nm, "INVALID" if bad else "VALID", 28, 22)
            arrow(d, 295, y, 295, 450, DIM, a * .6, 3) if k == 0 else None
        ct(d, 520, "change SPEC → dependents INVALID" if lt < 6 else "change BODY only → dependents OK", SB(30), RED if lt < 6 else GREEN, a)
        if lt > 6:
            d.rounded_rectangle((576, 326, 994, 454), 20, outline=mix(YEL, pr(lt, 6, 6.4) * fo), width=6)
        card_list(d, 900, [("11g+: a NEW spec item doesn't break users of others", CYAN, 8.5)], lt, fo, 80, 27)
        caps = ["Other code depends on the package specification. Change the spec, and every dependent becomes invalid and must recompile.",
                "Change only the body, and dependents stay valid. Session state is still discarded, though, if the package has state.",
                "Since 11g, fine-grained dependencies help: adding a new procedure to the spec doesn't invalidate code that uses other items."]
        caption(d, caps[0 if lt < 6 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 4 FIXES
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Make packages stateless", SB(52), GREEN, a)
        fx = [("no global variables", "pass values as parameters", GREEN),
              ("state in a table or context", "SYS_CONTEXT / global temp table", CYAN),
              ("PRAGMA SERIALLY_REUSABLE", "state lives for one call only", PURP),
              ("app: retry once on ORA-04068", "the 2nd call succeeds", YEL)]
        for k, (h, s_, col) in enumerate(fx):
            y = 330 + k * 165; al = pr(lt, .6 + k * 2, 1 + k * 2) * fo
            d.rounded_rectangle((70, y, W - 70, y + 145), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.ellipse((95, y + 42, 155, y + 102), fill=mix(col, al)); ct(d, y + 52, str(k + 1), SB(34), BG, al, 125)
            d.text((180, y + 24), h, font=SB(32), fill=mix(col, al))
            d.text((180, y + 84), s_, font=SN(28), fill=mix(WHITE, al))
        caps = ["The best fix: no package-level variables. A package without state can be recompiled without ORA-04068.",
                "If you need state, keep it in a table, a global temporary table, or an application context.",
                "Serially reusable packages keep state only for one call. And as a safety net, applications can retry once on ORA-04068."]
        caption(d, caps[0 if lt < 2.6 else 1 if lt < 4.6 else 2], pr(lt, .6, 1) * fo)

    # 5 EBR
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Zero-downtime: Editions", SB(52), PURP, a)
        glow_box(d, (70, 330, 500, 470), CYAN, a, "edition V1", "batch_pkg v1", 34, 28)
        glow_box(d, (580, 330, 1010, 470), GREEN, pr(lt, 1.5, 1.9) * fo, "edition V2", "batch_pkg v2", 34, 28)
        for k in range(3):
            sess(d, 160 + k * 120, 600, PINK, a, f"S{k + 1}", 36)
            arrow(d, 160 + k * 120, 564, 285, 470, PINK, a * .5, 3)
        if lt > 4:
            al = pr(lt, 4, 4.4) * fo
            for k in range(3):
                sess(d, 680 + k * 120, 600, YEL, al, f"N{k + 1}", 36)
                arrow(d, 680 + k * 120, 564, 795, 470, YEL, al * .6, 3)
            ct(d, 680, "new sessions → V2", SB(30), YEL, al, 795)
        ct(d, 680, "old sessions stay on V1", SB(30), PINK, pr(lt, 2.5, 2.9) * fo, 285)
        code(d, 760, [("CREATE EDITION v2;", PURP), ("ALTER SESSION SET EDITION = v2;", PURP)], pr(lt, 6, 6.4) * fo, 28)
        caps = ["For real zero-downtime deploys, Oracle has Edition-Based Redefinition.",
                "You compile the new version in a new edition. Sessions already running keep using the old one, with no errors.",
                "New sessions pick up the new edition. When the old sessions are gone, you retire the old version."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 6 DEPLOY CHECKLIST
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Before you deploy", SB(56), CYAN, a)
        code(d, 320, [("SELECT sid, program FROM v$session", CYAN), ("WHERE  sid IN (SELECT sid FROM v$access", CYAN),
                      ("               WHERE object = 'BATCH_PKG');", CYAN)], a, 26)
        ct(d, 500, "who is using it right now?", SB(30), YEL, pr(lt, 1.5, 1.9) * fo)
        code(d, 570, [("EXEC DBMS_UTILITY.COMPILE_SCHEMA('APP', FALSE);", GREEN)], pr(lt, 4, 4.4) * fo, 26)
        ct(d, 680, "recompile only the invalid objects", SB(30), GREEN, pr(lt, 4.5, 4.9) * fo)
        code(d, 740, [("SELECT object_name FROM user_objects", PINK), ("WHERE  status = 'INVALID';", PINK)], pr(lt, 7, 7.4) * fo, 26)
        ct(d, 880, "nothing left INVALID? ✓", SB(32), PINK, pr(lt, 8, 8.4) * fo)
        caps = ["Before deploying, check which sessions are using the package right now. Deploy outside the busy hours, not during end of day.",
                "After deploying, recompile what became invalid, so the first user doesn't pay the compile cost.",
                "And finish with a simple check: no invalid objects left."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 7 ERRORS MAP
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The error family", SB(56), RED, a)
        rows = [("ORA-04068", "existing state discarded", RED), ("ORA-04061", "existing state has been invalidated", PINK),
                ("ORA-04065", "not executed, package altered or dropped", YEL), ("ORA-06508", "could not find program unit", PURP)]
        for k, (e, m, col) in enumerate(rows):
            y = 330 + k * 150; al = pr(lt, .6 + k * 1.6, 1 + k * 1.6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 130), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 18), e, font=MB(34), fill=mix(col, al))
            d.text((100, y + 74), m, font=SN(28), fill=mix(WHITE, al))
        caps = ["They usually arrive together. ORA-04068 says the state was discarded. ORA-04061 and 04065 add that the package was invalidated or altered.",
                "ORA-06508 means a unit couldn't be found or loaded, often because a dependency is still invalid.",
                "All of them point to the same moment: a deploy while sessions were using the package."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("State", "→ globals, one copy per session"), ("Recompile", "→ old state discarded"),
                          ("ORA-04068", "→ 1st call fails, 2nd works"), ("Stateless", "→ no globals, no error"),
                          ("Editions", "→ zero-downtime deploys")],
              "Keep packages stateless, and deploys stop breaking sessions.", 430)
    else:
        cta(d, t - T[9], "DYNAMIC SQL & INJECTION", "' OR '1'='1", 56)
    return im

if __name__ == "__main__":
    preview(frame, T, "v36_sheet.png")

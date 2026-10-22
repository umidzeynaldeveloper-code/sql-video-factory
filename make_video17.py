from vhelp import *
import sys

T = T10; DUR = T[-1]

def plan_card(d, box, name, sub, col, a, badge=None, bcol=GREEN):
    glow_box(d, box, col, a, name, sub, 32, 26)
    if badge:
        x1, y0 = box[2], box[1]
        chip(d, x1 - 60, y0 + 2, badge, bcol, a, 24, BG)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 240, "Monday morning…", SB(60), WHITE, a)
        steps = [("Friday: EOD query", "2 s", GREEN, .4), ("weekend: stats refresh / upgrade", "", YEL, 1.2), ("Monday: EOD query", "40 min", RED, 2)]
        for k, (h, v, col, st) in enumerate(steps):
            y = 340 + k * 150; al = pr(lt, st, st + .3) * fo
            glow_box(d, (90, y, 990, y + 110), col, al)
            d.text((130, y + 32), h, font=SB(38), fill=mix(WHITE, al))
            if v: d.text((950 - d.textlength(v, font=MB(44)), y + 28), v, font=MB(44), fill=mix(col, al))
        ct(d, 850, "the PLAN flipped", SB(56), RED, pr(lt, 3, 3.4) * fo)
        ct(d, 940, "What if Oracle could only use", SB(42), YEL, pr(lt, 3.8, 4.2) * fo)
        ct(d, 1000, "plans you APPROVED?", SB(42), YEL, pr(lt, 3.8, 4.2) * fo)
        caption(d, "Same SQL, new plan, ruined night. SQL Plan Baselines exist to stop exactly this.", pr(lt, 4, 4.4) * fo)

    # 1 CONCEPT
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "SQL Plan Management", SB(58), CYAN, a)
        glow_box(d, (330, 300, 750, 390), WHITE, pr(lt, .4, .8) * fo, "your SQL", None, 36)
        glow_box(d, (330, 450, 750, 550), YEL, pr(lt, 1, 1.4) * fo, "Optimizer", "builds a plan", 34, 26)
        flow(d, [(540, 390), (540, 450)], WHITE, a, t, pr(lt, .8, 1.1))
        diamond(d, 540, 680, 260, 90, "in the BASELINE?", "accepted plans only", GREEN, pr(lt, 2.4, 2.8) * fo)
        flow(d, [(540, 550), (540, 590)], YEL, a, t, pr(lt, 2.2, 2.6))
        ab = pr(lt, 4, 4.4) * fo
        glow_box(d, (90, 850, 990, 1180), GREEN, ab)
        ct(d, 870, "SQL PLAN BASELINE", SB(38), GREEN, ab)
        for k, (p, s) in enumerate([("Plan A", "ACCEPTED ✓"), ("Plan C", "ACCEPTED ✓")]):
            y = 940 + k * 110
            d.rounded_rectangle((140, y, 940, y + 90), 16, fill=mix(CARD, ab), outline=mix(GREEN, ab), width=3)
            d.text((180, y + 22), p, font=MB(38), fill=mix(WHITE, ab)); d.text((600, y + 26), s, font=SB(32), fill=mix(GREEN, ab))
        caps = ["SQL Plan Management adds a gatekeeper between the optimizer and execution.",
                "For each SQL statement, Oracle keeps a baseline: the set of ACCEPTED plans.",
                "The optimizer may only run a plan that's in the baseline."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 2 CAPTURE
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How plans get in", SB(58), WHITE, a)
        a1 = pr(lt, .5, .9) * fo
        glow_box(d, (70, 320, 1010, 560), CYAN, a1)
        d.text((110, 340), "1. Load from cursor cache", font=SB(38), fill=mix(CYAN, a1))
        d.text((110, 410), "the plan running fine TODAY", font=SN(32), fill=mix(WHITE, a1))
        d.text((110, 470), "DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE", font=MB(28), fill=mix(PURP, a1))
        a2 = pr(lt, 4.5, 4.9) * fo
        glow_box(d, (70, 610, 1010, 850), YEL, a2)
        d.text((110, 630), "2. Automatic capture", font=SB(38), fill=mix(YEL, a2))
        d.text((110, 700), "first plan of repeated SQL", font=SN(32), fill=mix(WHITE, a2))
        d.text((110, 760), "OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES", font=MB(28), fill=mix(PURP, a2))
        a3 = pr(lt, 8.5, 8.9) * fo
        plan_card(d, (290, 920, 790, 1040), "Plan A", "first plan in", GREEN, a3, "ACCEPTED", GREEN)
        caps = ["The common way: load the plan that runs well right now, straight from the cursor cache.",
                "Or let Oracle capture baselines automatically for statements that run repeatedly.",
                "The first plan that enters a baseline is accepted. That's your known good plan."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 3 PROTECTION
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Stats change. New plan appears.", SB(52), YEL, a)
        glow_box(d, (330, 300, 750, 400), YEL, a, "Optimizer", "now prefers Plan B", 34, 26)
        diamond(d, 540, 540, 240, 85, "in the BASELINE?", None, GREEN, a)
        flow(d, [(540, 400), (540, 455)], YEL, a, t, pr(lt, .6, 1))
        plan_card(d, (60, 760, 500, 880), "Plan B", "NOT accepted", RED, pr(lt, 2.4, 2.8) * fo)
        if lt > 2: flow(d, [(300, 540), (280, 540), (280, 760)], RED, a, t, pr(lt, 2, 2.6))
        ah = pr(lt, 3.4, 3.8) * fo
        glow_box(d, (60, 930, 500, 1060), PURP, ah, "PLAN HISTORY", "saved for later", 32, 26)
        if lt > 3.4: flow(d, [(280, 880), (280, 930)], PURP, a, t, pr(lt, 3.4, 3.8))
        plan_card(d, (580, 760, 1020, 880), "Plan A", "ACCEPTED ✓", GREEN, pr(lt, 5, 5.4) * fo)
        if lt > 5: flow(d, [(780, 540), (800, 540), (800, 760)], GREEN, a, t, pr(lt, 5, 5.6))
        ct(d, 1130, "EOD still runs in 2 s ✓", SB(46), GREEN, pr(lt, 7, 7.4) * fo)
        caps = ["New statistics or a new version: the optimizer now prefers a different plan, Plan B.",
                "Plan B isn't accepted. It's stored in the plan history, but NOT executed.",
                "Oracle runs the accepted Plan A instead. Your Monday is saved."]
        caption(d, caps[0 if lt < 2.4 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    # 4 EVOLVE
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "But what if Plan B is BETTER?", SB(52), WHITE, a)
        glow_box(d, (300, 300, 780, 400), CYAN, pr(lt, .4, .8) * fo, "EVOLVE", "test-drive new plans", 36, 26)
        ra = pr(lt, 1.5, 1.9) * fo
        bar(d, 110, 520, 970, 40, pr(lt, 2, 5) * .8, YEL, ra, "Plan A (baseline)", "8 s")
        bar(d, 110, 640, 970, 40, pr(lt, 2, 3.5) * .2, GREEN, ra, "Plan B (candidate)", "2 s")
        ab = pr(lt, 6, 6.4) * fo
        plan_card(d, (290, 760, 790, 880), "Plan B", "verified faster", GREEN, ab, "ACCEPTED", GREEN)
        ac = pr(lt, 8, 8.4) * fo
        glow_box(d, (90, 960, 990, 1080), PURP, ac, "SPM Evolve Advisor: nightly, automatic", None, 32)
        caps = ["Evolution: Oracle actually runs the new plan and the baseline plan, and compares them.",
                "Only if the new plan is clearly faster does it become accepted.",
                "Since 12c an automatic evolve task does this in the nightly maintenance window."]
        caption(d, caps[0 if lt < 6 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 5 FIXED + check
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How to see it working", SB(56), WHITE, a)
        a1 = pr(lt, .5, .9) * fo
        glow_box(d, (60, 310, 1020, 600), CYAN, a1)
        d.text((95, 330), "DBA_SQL_PLAN_BASELINES", font=MB(34), fill=mix(CYAN, a1))
        hdr = ["PLAN", "ENABLED", "ACCEPTED", "FIXED"]
        for j, h in enumerate(hdr): d.text((95 + j * 230, 400), h, font=SB(28), fill=mix(DIM, a1))
        for r, row in enumerate([("Plan A", "YES", "YES", "NO"), ("Plan B", "YES", "NO", "NO")]):
            for j, v in enumerate(row):
                c = GREEN if v == "YES" else RED if v == "NO" and j == 2 else WHITE
                d.text((95 + j * 230, 460 + r * 60), v, font=MB(32), fill=mix(c, a1))
        a2 = pr(lt, 4, 4.4) * fo
        glow_box(d, (60, 650, 1020, 790), GREEN, a2)
        d.text((95, 670), "DBMS_XPLAN note:", font=SB(30), fill=mix(GREEN, a2))
        d.text((95, 720), "SQL plan baseline \"SQL_PLAN_…\" used", font=MN(30), fill=mix(WHITE, a2))
        a3 = pr(lt, 7, 7.4) * fo
        glow_box(d, (60, 840, 1020, 990), YEL, a3)
        d.text((95, 860), "FIXED = YES", font=MB(36), fill=mix(YEL, a3))
        d.text((95, 920), "pin it: no new plans are evolved in", font=SN(32), fill=mix(WHITE, a3))
        caps = ["The dictionary view shows each plan: enabled, accepted, fixed.",
                "And the execution plan's Note section tells you when a baseline was used.",
                "Mark a plan FIXED when you never want anything else for that SQL."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 6 BANK USE
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Bank playbook: upgrades", SB(56), GREEN, a)
        steps = [("1", "Before: capture baselines for critical EOD SQL", CYAN, .5),
                 ("2", "Upgrade / patch / new statistics", YEL, 3),
                 ("3", "Same accepted plans → no surprises", GREEN, 5.5),
                 ("4", "Let evolve accept only proven better plans", PURP, 8)]
        for k, (n, tx, col, st) in enumerate(steps):
            y = 330 + k * 170; al = pr(lt, st, st + .4) * fo
            glow_box(d, (150, y, 1010, y + 130), col, al)
            d.ellipse((60, y + 25, 140, y + 105), fill=mix(col, al))
            ct(d, y + 40, n, SB(44), BG, al, 100)
            d.text((180, y + 42), tx, font=SN(32), fill=mix(WHITE, al))
            if k: flow(d, [(100, y - 40), (100, y + 25)], col, al, t, pr(lt, st - .3, st), width=4)
        caps = ["Before an upgrade, capture baselines for your most critical statements.",
                "After the upgrade, Oracle keeps using the same accepted plans.",
                "Then new plans are allowed in only after they prove they're faster."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 7 TRAP
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Trap: plan can't be reproduced", SB(52), RED, a)
        plan_card(d, (290, 320, 790, 440), "Plan A", "uses IDX_ACC_CLIENT", GREEN, a, "ACCEPTED", GREEN)
        ad = pr(lt, 2, 2.4) * fo
        glow_box(d, (190, 520, 890, 620), RED, ad, "DROP INDEX idx_acc_client", None, 34)
        if lt > 3:
            ax = pr(lt, 3, 3.4) * fo
            d.line((300, 330, 780, 430), fill=mix(RED, ax), width=8)
        ab = pr(lt, 4.5, 4.9) * fo
        glow_box(d, (90, 700, 990, 860), YEL, ab, "optimizer can't build Plan A", "→ silently uses its own new plan", 34, 30)
        ac = pr(lt, 7.5, 7.9) * fo
        card_list(d, 930, [("✓ keep objects that baseline plans depend on", GREEN, 7.5), ("✓ re-check baselines after schema changes", GREEN, 8.2)], lt, fo)
        caps = ["A baseline stores HOW to build a plan, not the plan's result.",
                "Drop an index the plan needs, and Oracle can't reproduce it.",
                "Then the optimizer quietly falls back to its own plan. Watch schema changes."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 4.5 else 2], pr(lt, .6, 1) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Baseline", "→ set of ACCEPTED plans"), ("New plan", "→ goes to history, not run"),
                          ("Evolve", "→ accept only if faster"), ("FIXED", "→ pin one plan"),
                          ("Before upgrades", "→ capture critical SQL")],
              "Plan stability without freezing progress.")
    else:
        cta(d, t - T[9], "REDO & COMMIT", "why COMMIT is so fast")
    return im

if __name__ == "__main__":
    preview(frame, T, "v17_sheet.png")

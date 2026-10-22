from common import *
from make_video5 import arrow
from make_video11 import glow_box, flow
from make_video12 import chip, bar
import subprocess, math, sys

T = [0, 6, 18, 32, 46, 60, 72, 84, 96, 104, 110]
DUR = T[-1]; N = FPS * DUR

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def lerp(a, b, p): return a + (b - a) * p

def eye(d, cx, cy, a, s=1.0, col=YEL):
    d.ellipse((cx - 50 * s, cy - 26 * s, cx + 50 * s, cy + 26 * s), outline=mix(col, a), width=6)
    d.ellipse((cx - 16 * s, cy - 16 * s, cx + 16 * s, cy + 16 * s), fill=mix(col, a))
    d.ellipse((cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s), fill=mix(BG, a))

def exec_row(d, y, val, rows, ok, a, plan=None):
    d.rounded_rectangle((70, y, W - 70, y + 70), 16, fill=mix(CARD, a), outline=mix(GREEN if ok else RED, a), width=3)
    d.text((95, y + 16), f":status = '{val}'", font=MB(32), fill=mix(WHITE, a))
    d.text((560, y + 18), rows, font=SN(30), fill=mix(DIM, a))
    tx = "fast ✓" if ok else "SLOW ✗"
    d.text((W - 95 - d.textlength(tx, font=SB(32)), y + 16), tx, font=SB(32), fill=mix(GREEN if ok else RED, a))

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, 0); a = pr(lt, 0, .3) * fo
        ct(d, 240, "One SQL. Two users.", SB(60), WHITE, a)
        glow_box(d, (90, 330, 990, 450), CYAN, pr(lt, .4, .8) * fo, "SELECT * FROM accounts", "WHERE status = :status", 34, 32)
        exec_row(d, 530, "FROZEN", "1 000 rows", True, pr(lt, 1.4, 1.8) * fo)
        exec_row(d, 630, "ACTIVE", "970 000 rows", False, pr(lt, 2.4, 2.8) * fo)
        ct(d, 780, "Same text → same plan…", SB(48), YEL, pr(lt, 3.4, 3.8) * fo)
        ct(d, 850, "and that's the problem", SB(48), RED, pr(lt, 3.8, 4.2) * fo)
        caption(d, "Bind variables share one plan. But not every value deserves the same plan.", pr(lt, 4, 4.4) * fo)

    # 1 CONFLICT
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Two good ideas collide", SB(56), WHITE, a)
        a1 = pr(lt, .5, .9) * fo
        glow_box(d, (60, 330, 500, 560), GREEN, a1, "BIND variables", "one shared plan", 36, 30)
        a2 = pr(lt, 2.5, 2.9) * fo
        glow_box(d, (580, 330, 1020, 560), PURP, a2, "HISTOGRAMS", "plan per value", 36, 30)
        if lt > 4:
            flow(d, [(280, 560), (280, 700), (500, 700)], GREEN, a, t, pr(lt, 4, 4.6))
            flow(d, [(800, 560), (800, 700), (580, 700)], PURP, a, t, pr(lt, 4, 4.6))
            p = 1 + .08 * math.sin(lt * 9)
            ac = pr(lt, 4.6, 5) * fo
            d.ellipse((540 - 60 * p, 700 - 60 * p, 540 + 60 * p, 700 + 60 * p), fill=mix(RED, ac))
            ct(d, 672, "⚡", SB(54), WHITE, ac, 540)
        a3 = pr(lt, 6.5, 6.9) * fo
        glow_box(d, (110, 830, 970, 960), YEL, a3, "Which value decides the plan?", None, 40)
        caps = ["Bind variables: one cursor, one plan, reused by everyone. Great for the shared pool.",
                "Histograms: rare and common values may need different plans.",
                "Put them together, and Oracle has to choose: which value decides the plan?"]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 2 BIND PEEKING
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "BIND PEEKING", SB(64), YEL, a)
        ct(d, 320, "first execution = hard parse", SN(38), WHITE, a)
        glow_box(d, (300, 400, 780, 500), CYAN, pr(lt, .6, 1) * fo, ":status = 'FROZEN'", None, 38)
        glow_box(d, (300, 620, 780, 740), YEL, pr(lt, 1.6, 2) * fo, "Optimizer", None, 40)
        ae = pr(lt, 2.5, 2.9) * fo
        eye(d, 880, 560, ae, 1.0)
        if lt > 2.5: flow(d, [(850, 540), (780, 470)], YEL, a, t, pr(lt, 2.6, 3.2), width=4)
        ct(d, 600, "peek!", SB(34), YEL, ae, 960)
        a2 = pr(lt, 4, 4.4) * fo
        ct(d, 540, "histogram: FROZEN = 1 000 rows", MN(32), PURP, a2, 430)
        if lt > 5: flow(d, [(540, 740), (540, 860)], GREEN, a, t, pr(lt, 5, 5.6))
        a3 = pr(lt, 5.6, 6) * fo
        glow_box(d, (200, 860, 880, 1000), GREEN, a3, "plan: INDEX RANGE SCAN", "stored in the shared pool", 38, 28)
        caps = ["On the very first execution, the cursor is hard parsed.",
                "The optimizer peeks at the actual bind value, as if it were a literal.",
                "FROZEN is rare, so it builds an index plan and caches it for everyone."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 3 REUSE PROBLEM
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Then everyone reuses it", SB(58), WHITE, a)
        glow_box(d, (200, 320, 880, 440), GREEN, a, "cached plan: INDEX RANGE SCAN", None, 34)
        rows = [("FROZEN", "1 000 rows", True), ("CLOSED", "20 000 rows", True), ("ACTIVE", "970 000 rows", False), ("ACTIVE", "970 000 rows", False)]
        for k, (v, r, ok) in enumerate(rows):
            st = 1 + k * 1.3
            exec_row(d, 520 + k * 95, v, r, ok, pr(lt, st, st + .3) * fo)
        a4 = pr(lt, 7, 7.4) * fo
        d.rounded_rectangle((70, 930, W - 70, 1150), 22, fill=mix((70, 18, 28), a4), outline=mix(RED, a4), width=4)
        d.text((100, 950), "970 000 index lookups", font=SB(38), fill=mix(RED, a4))
        d.text((100, 1010), "instead of one full scan", font=SN(34), fill=mix(WHITE, a4))
        d.text((100, 1070), "The plan depends on WHO CAME FIRST", font=SB(34), fill=mix(YEL, pr(lt, 9, 9.4) * fo))
        caps = ["Every next execution reuses that cached index plan, whatever the value.",
                "For ACTIVE, that means almost a million single-row index lookups. Painfully slow.",
                "Restart the database on a Monday, and a different first value can flip the plan."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 9 else 2], pr(lt, .6, 1) * fo)

    # 4 ADAPTIVE CURSOR SHARING
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Adaptive Cursor Sharing", SB(58), GREEN, a)
        glow_box(d, (300, 320, 780, 430), CYAN, pr(lt, .4, .8) * fo, "parent cursor", "same SQL text", 34, 26)
        steps = [("BIND SENSITIVE", "histogram on the column → watch it", YEL, 1.2),
                 ("monitoring…", "rows: 1 000 vs 970 000!", PINK, 3.6),
                 ("BIND AWARE", "build plans per value range", GREEN, 6)]
        for k, (h, s, col, st) in enumerate(steps):
            y = 500 + k * 150; al = pr(lt, st, st + .4) * fo
            glow_box(d, (150, y, 930, y + 120), col, al, h, s, 36, 28)
            if k: flow(d, [(540, y - 30), (540, y)], col, al, t, pr(lt, st - .3, st))
        if lt > 1: flow(d, [(540, 430), (540, 500)], CYAN, a, t, pr(lt, 1, 1.2))
        caps = ["Since Oracle 11g, the optimizer can learn from its own mistakes.",
                "The cursor is marked bind sensitive, because the column has a histogram. Oracle watches it.",
                "When row counts differ wildly between executions, the cursor becomes BIND AWARE."]
        caption(d, caps[0 if lt < 1.2 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 5 CHILD CURSORS ROUTING
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "One SQL → two plans", SB(58), WHITE, a)
        glow_box(d, (300, 300, 780, 400), CYAN, a, "parent cursor", None, 36)
        cx, cy = 540, 520; ad = pr(lt, .6, 1) * fo
        d.polygon([(cx, cy - 75), (cx + 230, cy), (cx, cy + 75), (cx - 230, cy)], fill=mix(CARD, ad), outline=mix(YEL, ad))
        ct(d, cy - 40, "selectivity", SB(30), YEL, ad, cx)
        ct(d, cy + 2, "of the value?", SN(28), WHITE, ad, cx)
        flow(d, [(540, 400), (540, 445)], CYAN, a, t, pr(lt, .4, .8))
        a1 = pr(lt, 1.4, 1.8) * fo
        glow_box(d, (60, 700, 500, 860), GREEN, a1, "child #0", "INDEX · rare values", 36, 28)
        glow_box(d, (580, 700, 1020, 860), YEL, a1, "child #1", "FULL SCAN · common", 36, 28)
        flow(d, [(330, 520), (280, 520), (280, 700)], GREEN, a1, t, pr(lt, 1.4, 2))
        flow(d, [(750, 520), (800, 520), (800, 700)], YEL, a1, t, pr(lt, 1.4, 2))
        vals = [("FROZEN", 0), ("ACTIVE", 1), ("CLOSED", 0), ("ACTIVE", 1)]
        k = min(3, int(max(0, lt - 3) / 1.8)) if lt > 3 else -1
        if k >= 0:
            v, ch = vals[k]; pl = lt - 3 - k * 1.8
            x = lerp(540, 280 if ch == 0 else 800, pr(pl, .6, 1.3)); y = lerp(420, 650, pr(pl, 0, 1.3))
            chip(d, x, y, v, CYAN, a, 28)
        for j in range(4):
            if lt > 3 + j * 1.8 + 1.3:
                v, ch = vals[j]
                exec_row(d, 920 + j * 82, v, "→ child #%d" % ch, True, fo)
        caps = ["Now Oracle keeps separate child cursors, each with its own plan.",
                "For each execution, it peeks at the value's selectivity and routes it to the right child.",
                "Rare values get the index, common values get the full scan. Everyone is fast."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 6 LEARNING COST
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "But it learns AFTER the pain", SB(56), YEL, a)
        d.line((110, 520, 970, 520), fill=mix(DIM, a), width=6)
        ev = [(200, "exec 1", "FROZEN", "fast", GREEN, .8), (430, "exec 2", "ACTIVE", "SLOW", RED, 2.4),
              (660, "exec 3", "ACTIVE", "fast", GREEN, 4.4), (890, "exec 4", "FROZEN", "fast", GREEN, 5.6)]
        for x, h, v, r, col, st in ev:
            al = pr(lt, st, st + .4) * fo
            d.ellipse((x - 22, 498, x + 22, 542), fill=mix(col, al))
            ct(d, 420, h, SB(30), WHITE, al, x)
            ct(d, 570, v, MN(28), DIM, al, x)
            ct(d, 615, r, SB(32), col, al, x)
        ab = pr(lt, 3.4, 3.8) * fo
        d.line((545, 470, 545, 680), fill=mix(YEL, ab), width=4)
        ct(d, 700, "becomes BIND AWARE here", SB(32), YEL, ab, 545)
        an = pr(lt, 7, 7.4) * fo
        d.rounded_rectangle((70, 820, W - 70, 1060), 22, fill=mix(CARD, an))
        d.text((100, 845), "✗ at least one slow run to learn", font=SN(34), fill=mix(RED, an))
        d.text((100, 905), "✗ learning lost if the cursor ages out", font=SN(34), fill=mix(RED, an))
        d.text((100, 965), "✓ still much better than one plan forever", font=SN(34), fill=mix(GREEN, an))
        caps = ["Adaptive cursor sharing reacts, it doesn't predict.",
                "It needs to see a badly performing execution before it creates a better plan.",
                "And if the cursor is flushed from the shared pool, the learning starts again."]
        caption(d, caps[0 if lt < 3.4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 7 TOOLS
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Your toolbox", SB(60), WHITE, a)
        cards = [("V$SQL", "IS_BIND_SENSITIVE · IS_BIND_AWARE", CYAN, .5),
                 ("SQL Plan Baselines", "lock in a proven good plan", GREEN, 3),
                 ("Think about the data", "few values + huge skew? a literal may be OK", YEL, 6)]
        for k, (h, s, col, st) in enumerate(cards):
            y = 330 + k * 230; al = pr(lt, st, st + .4) * fo
            glow_box(d, (70, y, 1010, y + 190), col, al)
            d.text((110, y + 30), h, font=SB(42), fill=mix(col, al))
            d.text((110, y + 110), s, font=SN(32), fill=mix(WHITE, al))
        caps = ["Check V$SQL: is the cursor bind sensitive, has it become bind aware, how many children?",
                "SQL Plan Baselines let you fix a known good plan, so a bad peek can't take over.",
                "For a column with only a handful of very skewed values, sometimes a literal is the honest choice."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Remember:", SB(66), WHITE, a)
        items = [("Bind peeking", "→ first value decides"), ("Cached plan", "→ reused for everyone"),
                 ("Skewed data", "→ some values suffer"), ("ACS", "→ child cursor per range"),
                 ("Baselines", "→ lock a good plan")]
        for k, (q, ex) in enumerate(items):
            y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
            d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
            d.text((100, y + 32), q, font=MB(34), fill=mix(GREEN, al))
            d.text((440, y + 32), ex, font=SN(34), fill=mix(WHITE, al))
        caption(d, "One SQL text doesn't have to mean one plan anymore.", pr(lt, 2, 2.4) * fo)

    # 9 CTA
    else:
        lt = t - T[9]
        ct(d, 440, "Next video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 540, "SQL PLAN BASELINES", SB(64), YEL, pr(lt, .2, .5))
        ct(d, 650, "freeze a good plan forever", SB(44), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "follow · save · share", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.5, T[1] + 7, T[2] + 7, T[3] + 9.5, T[4] + 8, T[5] + 6, T[5] + 11, T[6] + 8, T[7] + 8, T[8] + 4, T[9] + 3, T[1] + 3]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v16_{k}.png")
        sys.exit()

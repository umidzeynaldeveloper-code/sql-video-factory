from common import *
from make_video5 import arrow
from make_video11 import glow_box, flow
from make_video12 import chip, bar
import subprocess, math, sys

T = [0, 6, 18, 32, 46, 60, 72, 84, 96, 104, 110]
DUR = T[-1]; N = FPS * DUR
BR = [("BAKU", 920), ("GANJA", 310), ("SUMGAIT", 240), ("LANKARAN", 120)]

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def lerp(a, b, p): return a + (b - a) * p

def user(d, cx, cy, col, a, s=1.0):
    d.ellipse((cx - 16 * s, cy - 40 * s, cx + 16 * s, cy - 8 * s), fill=mix(col, a))
    d.pieslice((cx - 30 * s, cy - 2 * s, cx + 30 * s, cy + 56 * s), 180, 360, fill=mix(col, a))

def cyl(d, cx, cy, w, h, col, a, label=None, sub=None):
    eh = h * .22
    d.rectangle((cx - w / 2, cy - h / 2 + eh / 2, cx + w / 2, cy + h / 2 - eh / 2), fill=mix(CARD, a))
    d.ellipse((cx - w / 2, cy + h / 2 - eh, cx + w / 2, cy + h / 2), fill=mix(CARD, a), outline=mix(col, a), width=4)
    d.line((cx - w / 2, cy - h / 2 + eh / 2, cx - w / 2, cy + h / 2 - eh / 2), fill=mix(col, a), width=4)
    d.line((cx + w / 2, cy - h / 2 + eh / 2, cx + w / 2, cy + h / 2 - eh / 2), fill=mix(col, a), width=4)
    d.ellipse((cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + eh), fill=mix((30, 44, 80), a), outline=mix(col, a), width=4)
    if label: ct(d, cy - 14, label, SB(30), col, a, cx)
    if sub: ct(d, cy + 26, sub, MN(26), WHITE, a, cx)

def mv_table(d, x0, y0, x1, a, vals, col=GREEN, title="MV: branch totals", stale=False, hl=None):
    h = 80 + 56 * len(vals)
    glow_box(d, (x0, y0, x1, y0 + h), RED if stale else col, a)
    ct(d, y0 + 16, title, SB(30), RED if stale else col, a, (x0 + x1) / 2)
    for k, (b, v) in enumerate(vals):
        y = y0 + 68 + k * 56
        if hl == k: d.rounded_rectangle((x0 + 12, y - 6, x1 - 12, y + 44), 10, fill=mix((30, 80, 55), a))
        d.text((x0 + 26, y), b, font=SN(30), fill=mix(WHITE, a))
        txt = f"{v}M"; d.text((x1 - 26 - d.textlength(txt, font=MB(32)), y - 2), txt, font=MB(32), fill=mix(YEL, a))
    if stale:
        chip(d, x1 - 70, y0 + 6, "STALE", RED, a, 24, WHITE)
    return y0 + h

def funnel(d, cx, y0, y1, w0, w1, col, a):
    d.polygon([(cx - w0 / 2, y0), (cx + w0 / 2, y0), (cx + w1 / 2, y1), (cx - w1 / 2, y1)], fill=mix(CARD, a), outline=mix(col, a))
    ct(d, (y0 + y1) / 2 - 22, "GROUP BY", MB(30), col, a, cx)

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
        ct(d, 240, "Dashboard: totals per branch", SB(54), WHITE, a)
        n = min(12, int(max(0, lt - .5) / .25))
        for k in range(12):
            x = 110 + (k % 6) * 172; y = 380 + (k // 6) * 140
            user(d, x, y, CYAN, a if k < n else 0, .9)
        cyl(d, 540, 820, 420, 240, RED, a, "TRANSACTIONS", "2 000 000 000 rows")
        for k in range(min(n, 12)):
            x = 110 + (k % 6) * 172; y = 380 + (k // 6) * 140 + 55
            flow(d, [(x, y), (540, 700)], RED, a * .8, t + k * .1, 1, width=3)
        load = min(1, n / 10)
        bar(d, 110, 1060, 970, 36, load, RED if load > .8 else YEL, pr(lt, 1, 1.3) * fo, "server load", f"{int(load * 100)}%")
        ct(d, 1150, "each click = 30 s of heavy work", SB(42), RED, pr(lt, 3, 3.4) * fo)
        caption(d, "Every user re-calculates the same answer from 2 billion rows. Again and again.", pr(lt, 3.6, 4) * fo)

    # 1 VIEW vs MV
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "VIEW vs MATERIALIZED VIEW", SB(52), WHITE, a)
        av = pr(lt, .5, .9) * fo
        d.text((80, 320), "VIEW = a saved QUERY", font=SB(38), fill=mix(PURP, av))
        user(d, 140, 450, CYAN, av)
        glow_box(d, (260, 400, 560, 500), PURP, av, "VIEW", "just SQL text", 34, 24)
        cyl(d, 850, 450, 260, 150, RED, av, "base tables")
        if lt > 1: flow(d, [(170, 450), (260, 450)], CYAN, av, t, pr(lt, 1, 1.5))
        if lt > 1.5: flow(d, [(560, 450), (720, 450)], RED, av, t, pr(lt, 1.5, 2.2), width=9)
        ct(d, 560, "recomputed EVERY time ✗", SB(34), RED, pr(lt, 2.4, 2.8) * fo)
        am = pr(lt, 4.5, 4.9) * fo
        d.text((80, 680), "MV = a saved RESULT", font=SB(38), fill=mix(GREEN, am))
        user(d, 140, 810, CYAN, am)
        mv_table(d, 260, 740, 640, am, BR[:2], title="MV")
        cyl(d, 870, 810, 220, 130, DIM, am * .6, "base tables")
        if lt > 5: flow(d, [(170, 810), (260, 810)], GREEN, am, t, pr(lt, 5, 5.5))
        ct(d, 1010, "read ready-made rows ✓", SB(34), GREEN, pr(lt, 5.8, 6.2) * fo)
        ac = pr(lt, 8, 8.4) * fo
        glow_box(d, (110, 1080, 970, 1190), YEL, ac, "Recipe  vs  cooked meal", None, 40)
        caps = ["A normal view is just a stored query. Every SELECT runs the whole thing again.",
                "A materialized view stores the RESULT physically, like a real table.",
                "A view is the recipe. A materialized view is the meal, already cooked."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 2 BUILD
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How an MV is built", SB(58), WHITE, a)
        cyl(d, 300, 400, 340, 170, CYAN, pr(lt, .4, .8) * fo, "TRANSACTIONS", "2 billion rows")
        cyl(d, 790, 400, 300, 170, CYAN, pr(lt, .8, 1.2) * fo, "BRANCHES", "4 rows")
        af = pr(lt, 2, 2.4) * fo
        funnel(d, 540, 560, 760, 700, 220, YEL, af)
        if lt > 2.5:
            flow(d, [(300, 485), (300, 560)], CYAN, a, t, pr(lt, 2.5, 3))
            flow(d, [(790, 485), (790, 560)], CYAN, a, t, pr(lt, 2.5, 3))
        if lt > 4: flow(d, [(540, 760), (540, 830)], GREEN, a, t, pr(lt, 4, 4.6))
        am = pr(lt, 4.6, 5) * fo
        mv_table(d, 290, 830, 790, am, BR)
        ct(d, 1170, "2 billion rows → 4 rows", SB(46), GREEN, pr(lt, 7, 7.4) * fo)
        caps = ["The MV query joins and aggregates the base tables once.",
                "The tiny result is stored as a real segment on disk.",
                "Now 500 users read 4 rows instead of crunching 2 billion."]
        caption(d, caps[0 if lt < 4.6 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 3 STALE
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "But data keeps changing", SB(58), WHITE, a)
        cyl(d, 540, 420, 420, 180, CYAN, a, "TRANSACTIONS", "new rows arriving")
        n = min(6, int(max(0, lt - 1) / .7))
        for k in range(n):
            x = 160 + k * 150; p = pr(lt, 1 + k * .7, 1.6 + k * .7)
            y = lerp(300, 380, p)
            d.rounded_rectangle((x - 60, y - 20, x + 60, y + 20), 10, fill=mix(PINK, a * (1 - p * .6)))
            ct(d, y - 15, "+tx", SB(24), BG, a * (1 - p * .6), x)
        stale = lt > 4
        mv_table(d, 290, 640, 790, a, BR, stale=stale)
        if stale:
            ct(d, 1000, "real BAKU total: 925M", MB(36), YEL, pr(lt, 5, 5.4) * fo)
            ct(d, 1060, "MV still says: 920M", MB(36), RED, pr(lt, 5.6, 6) * fo)
        caps = ["New transactions keep arriving in the base table.",
                "The MV doesn't know about them. Its numbers are now STALE.",
                "So the big question: how and when do we refresh it?"]
        caption(d, caps[0 if lt < 4 else 1 if lt < 9 else 2], pr(lt, .6, 1) * fo)

    # 4 COMPLETE REFRESH
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Refresh #1: COMPLETE", SB(58), YEL, a)
        cyl(d, 540, 400, 420, 170, CYAN, a, "TRANSACTIONS", "2 billion rows")
        funnel(d, 540, 540, 720, 700, 220, YEL, a)
        wiping = 1 < lt < 3
        if lt > 3: flow(d, [(540, 485), (540, 540)], CYAN, a, t, pr(lt, 3, 3.5), width=9)
        if lt > 3.5: flow(d, [(540, 720), (540, 790)], GREEN, a, t, pr(lt, 6, 6.5))
        vals = BR if lt > 6.5 else [(b, 0) for b, v in BR] if lt > 1.5 else BR
        mv_table(d, 290, 790, 790, a * (.4 if wiping else 1), [(b, 925 if b == "BAKU" and lt > 6.5 else v) for b, v in vals], stale=lt < 1.5)
        bar(d, 110, 1180, 970, 36, pr(lt, 3, 6.5), RED, pr(lt, 1, 1.3) * fo, "re-reading everything…", "heavy")
        caps = ["COMPLETE refresh throws away the MV contents...",
                "...and runs the whole query again over all 2 billion rows.",
                "Always correct, but expensive. Usually done at night or after EOD."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 5 FAST REFRESH
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Refresh #2: FAST", SB(58), GREEN, a)
        cyl(d, 270, 420, 340, 170, CYAN, a, "TRANSACTIONS", "base table")
        al = pr(lt, 1, 1.4) * fo
        glow_box(d, (620, 330, 1010, 640), PURP, al)
        ct(d, 345, "MV LOG", SB(36), PURP, al, 815)
        changes = [("+5M", "BAKU"), ("+2M", "GANJA"), ("-1M", "SUMGAIT")]
        nlog = min(3, int(max(0, lt - 1.5) / .8) + (1 if lt > 1.5 else 0))
        for k in range(nlog):
            y = 410 + k * 70
            d.rounded_rectangle((650, y, 980, y + 56), 12, fill=mix(CARD, al), outline=mix(PURP, al), width=2)
            d.text((670, y + 10), changes[k][0], font=MB(30), fill=mix(YEL, al)); d.text((800, y + 12), changes[k][1], font=SN(28), fill=mix(WHITE, al))
        if lt > 1.5: flow(d, [(440, 420), (620, 420)], PURP, a, t, pr(lt, 1.5, 2))
        done = lt > 6
        vals = [("BAKU", 925 if done else 920), ("GANJA", 312 if done else 310), ("SUMGAIT", 239 if done else 240), ("LANKARAN", 120)]
        mv_table(d, 290, 780, 790, a, vals, stale=not done)
        if lt > 5: flow(d, [(815, 640), (815, 720), (540, 720), (540, 780)], GREEN, a, t, pr(lt, 5, 5.8))
        bar(d, 110, 1170, 970, 36, pr(lt, 5, 5.8) * .04, GREEN, pr(lt, 5, 5.3) * fo, "applying only the changes", "seconds ✓")
        caps = ["An MV LOG on the base table records every change, like a small journal.",
                "FAST refresh reads only that journal and applies the deltas to the MV.",
                "No full re-scan. Seconds instead of minutes."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 6 WHEN: ON COMMIT vs ON DEMAND
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "WHEN to refresh?", SB(60), WHITE, a)
        a1 = pr(lt, .5, .9) * fo
        glow_box(d, (70, 320, 1010, 640), CYAN, a1)
        d.text((100, 340), "ON COMMIT", font=MB(42), fill=mix(CYAN, a1))
        d.line((110, 480, 970, 480), fill=mix(DIM, a1), width=4)
        for k in range(6):
            x = 170 + k * 150
            d.ellipse((x - 14, 466, x + 14, 494), fill=mix(PINK, a1))
            d.line((x, 494, x, 540), fill=mix(GREEN, a1), width=4); d.ellipse((x - 9, 536, x + 9, 554), fill=mix(GREEN, a1))
        d.text((100, 575), "✓ always fresh   ✗ every commit gets slower", font=SN(30), fill=mix(WHITE, a1))
        a2 = pr(lt, 4.5, 4.9) * fo
        glow_box(d, (70, 700, 1010, 1020), YEL, a2)
        d.text((100, 720), "ON DEMAND / scheduled", font=MB(40), fill=mix(YEL, a2))
        d.line((110, 860, 970, 860), fill=mix(DIM, a2), width=4)
        for k in range(6):
            x = 170 + k * 150
            d.ellipse((x - 14, 846, x + 14, 874), fill=mix(PINK, a2))
        d.line((900, 874, 900, 930), fill=mix(GREEN, a2), width=6); d.ellipse((888, 924, 912, 948), fill=mix(GREEN, a2))
        ct(d, 950, "after EOD", SN(28), GREEN, a2, 900)
        d.text((100, 960), "✓ no impact on OLTP   ✗ fresh only after refresh", font=SN(30), fill=mix(WHITE, a2))
        caps = ["ON COMMIT: the MV is refreshed as part of every commit on the base table.",
                "ON DEMAND: you refresh when you decide, e.g. a scheduled job after EOD.",
                "Pick by how fresh the numbers must be, and how busy your OLTP is."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 9 else 2], pr(lt, .6, 1) * fo)

    # 7 QUERY REWRITE
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Magic: QUERY REWRITE", SB(58), PURP, a)
        glow_box(d, (110, 300, 970, 420), CYAN, pr(lt, .4, .8) * fo, "SELECT branch, SUM(amount)", "FROM transactions GROUP BY branch", 30, 28)
        glow_box(d, (380, 500, 700, 590), YEL, pr(lt, 1.2, 1.6) * fo, "Optimizer", None, 36)
        flow(d, [(540, 420), (540, 500)], CYAN, a, t, pr(lt, 1, 1.4))
        cyl(d, 250, 800, 320, 180, RED, a * (.4 if lt > 4 else 1), "TRANSACTIONS", "2 billion rows")
        mv_table(d, 600, 700, 1000, pr(lt, 2, 2.4) * fo, BR[:3], title="MV")
        if lt < 4:
            flow(d, [(460, 590), (460, 640), (250, 640), (250, 710)], RED, a, t, pr(lt, 2.4, 3.2))
        else:
            ax = pr(lt, 4, 4.4) * fo
            d.line((180, 620, 330, 700), fill=mix(RED, ax), width=8); d.line((330, 620, 180, 700), fill=mix(RED, ax), width=8)
            flow(d, [(620, 590), (620, 640), (800, 640), (800, 700)], GREEN, a, t, pr(lt, 4.2, 5))
        chip(d, 540, 1060, "MAT_VIEW REWRITE ACCESS FULL", GREEN, pr(lt, 6, 6.4) * fo, 30)
        ct(d, 1140, "same SQL, no code change", SB(40), WHITE, pr(lt, 7, 7.4) * fo)
        caps = ["The user writes a normal query against the base table.",
                "With ENABLE QUERY REWRITE, the optimizer notices an MV already holds the answer...",
                "...and silently reads the MV instead. The application doesn't change at all."]
        caption(d, caps[0 if lt < 2.4 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Remember:", SB(66), WHITE, a)
        items = [("VIEW", "→ saved query"), ("MATERIALIZED VIEW", "→ saved result"),
                 ("COMPLETE", "→ recompute everything"), ("FAST + MV LOG", "→ apply only changes"),
                 ("QUERY REWRITE", "→ optimizer uses MV for you")]
        for k, (q, ex) in enumerate(items):
            y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
            d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
            d.text((100, y + 32), q, font=MB(32), fill=mix(GREEN, al))
            d.text((520, y + 32), ex, font=SN(34), fill=mix(WHITE, al))
        caption(d, "Compute once, read many times. The price: storage and refresh.", pr(lt, 2, 2.4) * fo)

    # 9 CTA
    else:
        lt = t - T[9]
        ct(d, 440, "Next video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 540, "OPTIMIZER STATISTICS", SB(62), YEL, pr(lt, .2, .5))
        ct(d, 650, "how Oracle guesses row counts", SB(44), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "follow · save · share", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.5, T[1] + 3, T[1] + 9, T[2] + 8, T[3] + 7, T[4] + 7.5, T[5] + 7, T[6] + 8, T[7] + 3, T[7] + 8, T[8] + 4, T[9] + 3]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v14_{k}.png")
        sys.exit()

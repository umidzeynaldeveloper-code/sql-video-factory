from common import *
from make_video5 import arrow
from make_video11 import glow_box, flow
from make_video12 import chip, bar
import subprocess, math, sys

T = [0, 6, 18, 32, 46, 60, 72, 84, 96, 104, 110]
DUR = T[-1]; N = FPS * DUR
DIST = [("ACTIVE", 970000), ("CLOSED", 20000), ("BLOCKED", 9000), ("FROZEN", 1000)]

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def fmt(n): return f"{int(n):,}".replace(",", " ")

def bars(d, x0, y0, w, h, vals, a, cols, labels, maxv, p=1.0, numfmt=fmt, logscale=False):
    n = len(vals); bw = (w - (n - 1) * 30) / n
    for k, v in enumerate(vals):
        x = x0 + k * (bw + 30)
        if logscale:
            hh = h * (math.log10(max(v, 1)) / math.log10(maxv)) * p
        else:
            hh = h * v / maxv * p
        d.rounded_rectangle((x, y0 + h - max(hh, 6), x + bw, y0 + h), 10, fill=mix(cols[k], a))
        ct(d, y0 + h - max(hh, 6) - 44, numfmt(v), MB(28), cols[k], a, x + bw / 2)
        ct(d, y0 + h + 12, labels[k], SB(26), WHITE, a, x + bw / 2)

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
        ct(d, 240, "Same query. Same code.", SB(58), WHITE, a)
        glow_box(d, (110, 340, 970, 470), GREEN, pr(lt, .5, .9) * fo, "Yesterday: 2 seconds", None, 44)
        glow_box(d, (110, 520, 970, 650), RED, pr(lt, 1.5, 1.9) * fo, "Today: 20 minutes", None, 44)
        ct(d, 740, "What changed?", SB(60), YEL, pr(lt, 2.6, 3) * fo)
        ct(d, 840, "Nothing… except the optimizer's GUESS", SB(42), WHITE, pr(lt, 3.4, 3.8) * fo)
        caption(d, "Oracle didn't break. It chose a different plan, because its picture of your data was wrong.", pr(lt, 3.8, 4.2) * fo)

    # 1 GPS
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The optimizer is a GPS", SB(58), CYAN, a)
        glow_box(d, (330, 300, 750, 390), WHITE, pr(lt, .4, .8) * fo, "your SQL", None, 38)
        glow_box(d, (330, 460, 750, 560), CYAN, pr(lt, 1, 1.4) * fo, "Optimizer", "cost-based (CBO)", 36, 26)
        flow(d, [(540, 390), (540, 460)], WHITE, a, t, pr(lt, .8, 1.1))
        routes = [("FULL SCAN", "cost 9 000", RED, 150), ("INDEX", "cost 40", GREEN, 540), ("HASH JOIN", "cost 600", YEL, 930)]
        pick = lt > 6
        for k, (nm, c, col, x) in enumerate(routes):
            st = 2 + k * .8; al = pr(lt, st, st + .4) * fo
            if lt > st: flow(d, [(540, 560), (540, 690)] if x == 540 else [(540, 560), (540, 620), (x, 620), (x, 690)], col, a * (1 if not pick or k == 1 else .3), t, pr(lt, st, st + .5))
            glow_box(d, (x - 140, 690, x + 140, 810), col, al * (1 if not pick or k == 1 else .35), nm, c, 30, 26)
        if pick: chip(d, 540, 880, "picks the CHEAPEST estimate ✓", GREEN, pr(lt, 6, 6.4) * fo, 32)
        am = pr(lt, 7.5, 7.9) * fo
        glow_box(d, (110, 980, 970, 1100), PURP, am, "The map = STATISTICS", None, 42)
        caps = ["Your SQL can run in many ways. Each way is a route, an execution plan.",
                "The optimizer estimates the cost of each route, and picks the cheapest.",
                "But every estimate comes from its map of your data: the statistics."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 2 WHAT STATS CONTAIN
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "What's inside the map?", SB(58), WHITE, a)
        cards = [("TABLE", CYAN, ["num_rows = 1 000 000", "blocks = 12 000", "avg_row_len = 96"], .5),
                 ("COLUMN: status", YEL, ["num_distinct = 4", "num_nulls = 0", "low / high value"], 3.5),
                 ("INDEX", GREEN, ["blevel = 2", "leaf_blocks = 2 400", "clustering_factor"], 6.5)]
        for k, (h, col, lines, st) in enumerate(cards):
            y = 320 + k * 290; al = pr(lt, st, st + .4) * fo
            glow_box(d, (90, y, 990, y + 250), col, al)
            d.text((130, y + 20), h, font=SB(40), fill=mix(col, al))
            for j, ln in enumerate(lines):
                d.text((150, y + 85 + j * 52), "• " + ln, font=MN(32), fill=mix(WHITE, pr(lt, st + .3 + j * .3, st + .6 + j * .3) * fo))
        caps = ["Table statistics: how many rows and blocks the table has.",
                "Column statistics: how many distinct values, how many NULLs, the min and max.",
                "Index statistics: how deep the tree is, and how well-ordered the table is for it."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 3 CARDINALITY MATH
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How Oracle estimates rows", SB(56), WHITE, a)
        glow_box(d, (110, 320, 970, 420), YEL, pr(lt, .4, .8) * fo, "WHERE status = 'FROZEN'", None, 40)
        af = pr(lt, 1.8, 2.2) * fo
        ct(d, 490, "estimated rows =", SB(44), WHITE, af)
        ct(d, 570, "num_rows / num_distinct", MB(44), CYAN, af)
        a2 = pr(lt, 4, 4.4) * fo
        ct(d, 680, "1 000 000 / 4", MB(60), WHITE, a2)
        a3 = pr(lt, 5.5, 5.9) * fo
        glow_box(d, (230, 790, 850, 910), GREEN, a3, "= 250 000 rows", None, 52)
        a4 = pr(lt, 7.5, 7.9) * fo
        ct(d, 990, "Assumption: values are spread EVENLY", SB(40), YEL, a4)
        bars(d, 150, 1110, 780, 170, [250000] * 4, a4, [CYAN] * 4, [b for b, _ in DIST], 250000, pr(lt, 7.5, 8.5))
        caps = ["Without extra information, the optimizer uses a simple formula.",
                "One million rows, four distinct statuses: it expects 250 thousand rows per value.",
                "That only works if every value appears about equally often."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 4 SKEW
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Reality is SKEWED", SB(60), RED, a)
        ct(d, 320, "estimated", SB(34), CYAN, pr(lt, .4, .8) * fo, 300)
        ct(d, 320, "real", SB(34), PINK, pr(lt, 1.5, 1.9) * fo, 790)
        bars(d, 90, 400, 420, 380, [250000] * 4, pr(lt, .4, .8) * fo, [CYAN] * 4, ["ACT", "CLO", "BLO", "FRO"], 970000, 1, numfmt=lambda v: "250k")
        bars(d, 570, 400, 420, 380, [v for _, v in DIST], pr(lt, 1.5, 1.9) * fo, [PINK, PINK, PINK, YEL], ["ACT", "CLO", "BLO", "FRO"], 970000, pr(lt, 1.5, 2.5),
             numfmt=lambda v: f"{v // 1000}k" if v >= 1000 else str(v))
        a3 = pr(lt, 4.5, 4.9) * fo
        d.rounded_rectangle((70, 900, W - 70, 1150), 22, fill=mix(CARD, a3))
        d.text((100, 920), "status = 'FROZEN'", font=MB(36), fill=mix(YEL, a3))
        d.text((100, 980), "expects 250 000 → picks FULL SCAN ✗", font=SN(36), fill=mix(RED, a3))
        d.text((100, 1040), "really 1 000 → INDEX would be 250× better", font=SN(36), fill=mix(GREEN, pr(lt, 6.5, 6.9) * fo))
        caps = ["But real data is rarely even. Almost all accounts are ACTIVE.",
                "Only 1 000 are FROZEN. The optimizer still expects 250 thousand.",
                "Wrong estimate, wrong plan: a full scan instead of a fast index lookup."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 5 HISTOGRAM
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Fix: HISTOGRAMS", SB(60), GREEN, a)
        ct(d, 320, "the real shape of the column", SN(38), WHITE, a)
        ah = pr(lt, 1, 1.4) * fo
        glow_box(d, (90, 390, 990, 820), GREEN, ah)
        ct(d, 410, "frequency histogram: status", SB(32), GREEN, ah)
        bars(d, 150, 520, 780, 220, [v for _, v in DIST], ah, [GREEN] * 4, [b for b, _ in DIST], 970000, pr(lt, 1.5, 3), logscale=True)
        a3 = pr(lt, 5, 5.4) * fo
        d.rounded_rectangle((70, 880, W - 70, 1080), 22, fill=mix((14, 50, 36), a3), outline=mix(GREEN, a3), width=4)
        d.text((100, 905), "status = 'FROZEN'  →  estimate 1 000 ✓", font=SN(36), fill=mix(WHITE, a3))
        d.text((100, 970), "plan: INDEX RANGE SCAN ✓", font=MB(36), fill=mix(GREEN, a3))
        ct(d, 1130, "(bars on a log scale)", SN(28), DIM, ah)
        caps = ["A histogram stores how often each value really appears.",
                "Now the optimizer knows FROZEN is rare, and chooses the index. Same SQL, right plan."]
        caption(d, caps[0 if lt < 5 else 1], pr(lt, .6, 1) * fo)

    # 6 STALE STATS
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The silent killer: STALE stats", SB(54), RED, a)
        am = pr(lt, .5, .9) * fo
        glow_box(d, (70, 330, 520, 640), PURP, am)
        ct(d, 350, "the MAP says", SB(34), PURP, am, 295)
        ct(d, 420, "1 000 000", MB(52), WHITE, am, 295)
        ct(d, 490, "rows", SN(30), DIM, am, 295)
        ct(d, 560, "analyzed 3 months ago", SN(28), YEL, am, 295)
        ar = pr(lt, 2, 2.4) * fo
        glow_box(d, (560, 330, 1010, 640), RED, ar)
        ct(d, 350, "REALITY", SB(34), RED, ar, 785)
        grow = 1_000_000 + 49_000_000 * pr(lt, 2.4, 4.4)
        ct(d, 420, f"{grow / 1e6:.0f} 000 000", MB(52), WHITE, ar, 785)
        ct(d, 490, "rows", SN(30), DIM, ar, 785)
        ct(d, 560, "after migration", SN(28), YEL, ar, 785)
        a3 = pr(lt, 5.5, 5.9) * fo
        d.rounded_rectangle((70, 700, W - 70, 960), 22, fill=mix((70, 18, 28), a3), outline=mix(RED, a3), width=4)
        d.text((100, 725), "optimizer plans for 1 million…", font=SN(36), fill=mix(WHITE, a3))
        d.text((100, 790), "→ NESTED LOOPS over 50 million ✗", font=MB(34), fill=mix(RED, a3))
        d.text((100, 855), "→ 2 seconds become 20 minutes", font=SN(36), fill=mix(YEL, a3))
        caps = ["Statistics are a snapshot. Data keeps growing, the snapshot does not.",
                "After a big load, the table has 50 million rows, but the map still says 1 million.",
                "The optimizer confidently picks a plan for a small table. That's yesterday's 2 s vs today's 20 min."]
        caption(d, caps[0 if lt < 2.4 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 7 GATHERING
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Keep the map fresh", SB(58), GREEN, a)
        a1 = pr(lt, .5, .9) * fo
        glow_box(d, (70, 320, 1010, 620), CYAN, a1)
        d.text((100, 340), "Automatic: nightly maintenance window", font=SB(34), fill=mix(CYAN, a1))
        mx, my = 160, 470
        d.ellipse((mx - 50, my - 50, mx + 50, my + 50), fill=mix(YEL, a1))
        d.ellipse((mx - 25, my - 60, mx + 65, my + 30), fill=mix(CARD, a1))
        ch = pr(lt, 1.5, 4)
        bar(d, 260, 470, 960, 34, ch * .3, YEL if ch * .3 < .1 else RED, a1, "rows changed since last stats", f"{int(ch * 30)}%")
        d.line((260 + 700 * .1, 450, 260 + 700 * .1, 520), fill=mix(WHITE, a1), width=4)
        ct(d, 535, "10% → STALE → regathered", SN(28), WHITE, a1, 330 + 40)
        a2 = pr(lt, 5, 5.4) * fo
        glow_box(d, (70, 680, 1010, 900), YEL, a2)
        d.text((100, 700), "Manual: after big loads / EOD batches", font=SB(34), fill=mix(YEL, a2))
        d.text((100, 770), "DBMS_STATS.GATHER_TABLE_STATS(", font=MB(32), fill=mix(WHITE, a2))
        d.text((100, 820), "    USER, 'TRANSACTIONS');", font=MB(32), fill=mix(WHITE, a2))
        a3 = pr(lt, 8, 8.4) * fo
        d.rounded_rectangle((70, 960, W - 70, 1050), 18, fill=mix((70, 18, 28), a3), outline=mix(RED, a3), width=3)
        d.text((100, 980), "✗ don't use old ANALYZE for optimizer stats", font=SN(32), fill=mix(WHITE, a3))
        caps = ["By default, Oracle regathers statistics at night for objects that changed by more than 10%.",
                "But after a huge load mid-day, don't wait for the night: gather stats right away with DBMS_STATS.",
                "And use DBMS_STATS, not the old ANALYZE command."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Remember:", SB(66), WHITE, a)
        items = [("Optimizer", "→ GPS: cheapest estimate"), ("Statistics", "→ the map of your data"),
                 ("rows / distinct", "→ assumes even spread"), ("Histogram", "→ handles skewed data"),
                 ("Stale stats", "→ yesterday 2 s, today 20 min")]
        for k, (q, ex) in enumerate(items):
            y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
            d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
            d.text((100, y + 32), q, font=MB(32), fill=mix(GREEN, al))
            d.text((440, y + 32), ex, font=SN(34), fill=mix(WHITE, al))
        caption(d, "A great optimizer with a wrong map still drives you into a traffic jam.", pr(lt, 2, 2.4) * fo)

    # 9 CTA
    else:
        lt = t - T[9]
        ct(d, 440, "Next video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 540, "BIND PEEKING", SB(68), YEL, pr(lt, .2, .5))
        ct(d, 650, "one plan for every value?", SB(44), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "follow · save · share", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.5, T[1] + 4, T[1] + 9, T[2] + 9, T[3] + 9, T[4] + 7.5, T[5] + 7, T[6] + 7, T[7] + 4, T[7] + 9, T[8] + 4, T[9] + 3]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v15_{k}.png")
        sys.exit()

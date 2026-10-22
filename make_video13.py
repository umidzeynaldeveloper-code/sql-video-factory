from common import *
from make_video5 import arrow
from make_video11 import glow_box, flow
from make_video12 import chip, bar
import subprocess, math, sys, random

T = [0, 6, 18, 32, 46, 60, 72, 84, 96, 104, 110]
DUR = T[-1]; N = FPS * DUR

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def lerp(a, b, p): return a + (b - a) * p

def worker(d, cx, cy, label, col, a, r=46, busy=False, t=0):
    if busy:
        for k in range(8):
            an = t * 4 + k * math.pi / 4
            d.ellipse((cx + (r + 12) * math.cos(an) - 5, cy + (r + 12) * math.sin(an) - 5, cx + (r + 12) * math.cos(an) + 5, cy + (r + 12) * math.sin(an) + 5), fill=mix(col, a * (.3 + .7 * ((k / 8 + t) % 1))))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=mix(CARD, a), outline=mix(col, a), width=5)
    ct(d, cy - 18, label, SB(30), col, a, cx)

def table_grid(d, x0, y0, cols, rows, cw, ch, a, done=set(), active=set(), col=CYAN):
    for r in range(rows):
        for c in range(cols):
            k = r * cols + c
            x = x0 + c * (cw + 6); y = y0 + r * (ch + 6)
            f = (30, 90, 70) if k in done else (90, 80, 20) if k in active else CARD
            d.rounded_rectangle((x, y, x + cw, y + ch), 6, fill=mix(f, a), outline=mix(col if k not in done else GREEN, a * .6), width=2)

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    # 0 HOOK: one worker
    if t < T[1]:
        lt, fo = sc(t, 0); a = pr(lt, 0, .3) * fo
        ct(d, 240, "10 GB report. 1 process.", SB(58), WHITE, a)
        n = int(64 * pr(lt, .8, 5.5) * .25)
        table_grid(d, 140, 360, 8, 8, 92, 52, a, done=set(range(n)), active={n})
        worker(d, 540, 900, "P1", CYAN, a, busy=True, t=t)
        bar(d, 140, 1060, 940, 36, n / 64, RED, pr(lt, .8, 1.1) * fo, "progress", "~40 min")
        ct(d, 1160, "What if 8 workers shared the job?", SB(46), YEL, pr(lt, 3.6, 4) * fo)
        caption(d, "A single server process reads every block one by one. On a big table, that takes ages.", pr(lt, 1.5, 1.9) * fo)

    # 1 QC + PX servers
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 240, "PARALLEL QUERY", SB(64), CYAN, a)
        glow_box(d, (300, 340, 780, 470), YEL, pr(lt, .6, 1) * fo, "Query Coordinator", "your session (QC)", 38, 28)
        xs = [110 + k * 123 for k in range(8)]
        for k, x in enumerate(xs):
            st = 2 + k * .25; al = pr(lt, st, st + .3) * fo
            if lt > st: flow(d, [(540, 470), (540, 560), (x, 560), (x, 650)], YEL, a, t, pr(lt, st - .3, st + .2), dots=lt > 5)
            worker(d, x, 700, f"P{k + 1}", CYAN, al, r=48, busy=lt > 5, t=t + k * .1)
        ct(d, 790, "parallel servers · DOP = 8", SB(36), CYAN, pr(lt, 4.5, 4.9) * fo)
        ac = pr(lt, 7, 7.4) * fo
        glow_box(d, (110, 880, 970, 990), PURP, ac, "SELECT /*+ PARALLEL(t 8) */ ...", None, 32)
        ct(d, 1030, "DOP = Degree Of Parallelism", SN(34), DIM, pr(lt, 7.5, 7.9) * fo)
        caps = ["Your session becomes the Query Coordinator, the boss of the operation.",
                "It recruits parallel server processes. How many? That's the DOP, degree of parallelism.",
                "You can ask for it with a hint, or let Oracle decide automatically."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 7 else 2], pr(lt, .8, 1.2) * fo)

    # 2 GRANULES
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The table is cut into GRANULES", SB(52), WHITE, a)
        cols, rows = 8, 4; ng = cols * rows
        random.seed(5)
        speed = [1.0, .8, 1.2, .9, 1.1, .7, 1.0, .95]
        # schedule: dynamic assignment
        tl = max(0, lt - 1.5) * 0.7
        assign = []; free = [0.0] * 8; g = 0
        while g < ng:
            w = min(range(8), key=lambda k: free[k])
            start = free[w]; dur = 1 / speed[w]
            assign.append((g, w, start, start + dur)); free[w] = start + dur; g += 1
        done = {g for g, w, s, e in assign if tl >= e}
        act = {g for g, w, s, e in assign if s <= tl < e}
        counts = [sum(1 for g, w, s, e in assign if w == k and tl >= e) for k in range(8)]
        x0, y0, cw, ch = 110, 340, 102, 62
        table_grid(d, x0, y0, cols, rows, cw, ch, a, done=done, active=act)
        xs = [110 + k * 123 for k in range(8)]
        for g, w, s, e in assign:
            if s <= tl < s + .45:
                p = (tl - s) / .45
                gx = x0 + (g % cols) * (cw + 6) + cw / 2; gy = y0 + (g // cols) * (ch + 6) + ch / 2
                x = lerp(gx, xs[w], p); y = lerp(gy, 900, p) - 80 * math.sin(math.pi * p)
                d.rounded_rectangle((x - 30, y - 18, x + 30, y + 18), 6, fill=mix(YEL, a))
        for k, x in enumerate(xs):
            worker(d, x, 900, f"P{k + 1}", CYAN, a, r=48, busy=k in {w for g, w, s, e in assign if s <= tl < e}, t=t + k * .1)
            ct(d, 965, str(counts[k]), MB(36), GREEN, a, x)
        ct(d, 1030, "granules done", SN(30), DIM, a)
        caps = ["The QC splits the table into granules: small ranges of blocks.",
                "Each free worker grabs the next granule. Faster workers simply take more.",
                "No one waits for a slow teammate. That's dynamic load balancing."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 3 PRODUCERS / CONSUMERS
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Two teams: producers → consumers", SB(50), WHITE, a)
        px = [200 + k * 227 for k in range(4)]
        ap = pr(lt, .5, .9) * fo; ac = pr(lt, 2, 2.4) * fo
        d.text((70, 340), "SCAN", font=MB(32), fill=mix(CYAN, ap))
        d.text((70, 880), "GROUP / JOIN", font=MB(32), fill=mix(PINK, ac))
        cols = [GREEN, YEL, PURP, PINK]
        if lt > 3.5:
            for i2, x0 in enumerate(px):
                for j2, x1 in enumerate(px):
                    flow(d, [(x0, 490), (x1, 760)], cols[j2], a * .9, t + i2 * .13, pr(lt, 3.5, 4.5), width=3)
        for k, x in enumerate(px):
            worker(d, x, 440, f"P{k + 1}", CYAN, ap, r=50, busy=lt > 3.5, t=t)
            worker(d, x, 810, f"C{k + 1}", cols[k], ac, r=50, busy=lt > 4.5, t=t + .3)
        aq = pr(lt, 7.5, 7.9) * fo
        glow_box(d, (330, 1010, 750, 1110), YEL, aq, "QC", None, 40)
        if lt > 7.5:
            for x in px: flow(d, [(x, 860), (x, 950), (540, 950), (540, 1010)], YEL, a, t, pr(lt, 7.6, 8.4), width=3)
        chip(d, 540, 1200, "DOP 4 → up to 8 processes", PURP, pr(lt, 9.5, 9.9) * fo, 32, WHITE)
        caps = ["For joins and GROUP BY, Oracle uses two sets of workers.",
                "Producers scan the data and redistribute each row by its key, through table queues.",
                "Every consumer gets all rows for its keys, does its part, and sends results to the QC.",
                "That's why DOP 4 can actually use 8 processes: two teams of 4."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6 else 2 if lt < 9.5 else 3], pr(lt, .6, 1) * fo)

    # 4 MERGE
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "QC assembles the answer", SB(56), WHITE, a)
        ct(d, 320, "SELECT SUM(amount) FROM transactions", MB(32), YEL, a)
        parts = [120, 95, 130, 105]
        xs = [200 + k * 227 for k in range(4)]
        for k, x in enumerate(xs):
            st = .8 + k * .4; al = pr(lt, st, st + .3) * fo
            worker(d, x, 480, f"P{k + 1}", CYAN, al, r=50)
            glow_box(d, (x - 95, 560, x + 95, 640), GREEN, al, f"{parts[k]}M", None, 36)
            if lt > 3.5: flow(d, [(x, 640), (x, 760), (540, 760), (540, 840)], GREEN, a, t, pr(lt, 3.5 + k * .2, 4.3 + k * .2))
        aq = pr(lt, 4.5, 4.9) * fo
        glow_box(d, (300, 840, 780, 980), YEL, aq, "QC", "120 + 95 + 130 + 105", 40, 30)
        ar = pr(lt, 6.5, 6.9) * fo
        glow_box(d, (300, 1040, 780, 1150), GREEN, ar, "SUM = 450M ✓", None, 44)
        caps = ["Each worker computes a partial sum over its own granules.",
                "The QC adds up the partial results and returns one final answer to you."]
        caption(d, caps[0 if lt < 4.5 else 1], pr(lt, .6, 1) * fo)

    # 5 SPEEDUP CHART
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How much faster?", SB(60), WHITE, a)
        ct(d, 310, "example timings", SN(32), DIM, a)
        data = [("1", 40), ("2", 21), ("4", 11), ("8", 6), ("16", 5.5)]
        base = 1080; maxh = 620
        for k, (dop, mins) in enumerate(data):
            x = 130 + k * 175; al = pr(lt, .6 + k * .5, 1 + k * .5) * fo
            h = maxh * mins / 40 * pr(lt, .6 + k * .5, 1.4 + k * .5)
            col = RED if k == 0 else YEL if k == 4 else GREEN
            d.rounded_rectangle((x, base - h, x + 130, base), 14, fill=mix(col, al))
            ct(d, base - h - 55, f"{mins:g}m", MB(34), col, al, x + 65)
            ct(d, base + 15, dop, SB(38), WHITE, al, x + 65)
        ct(d, base + 70, "DOP", SN(34), DIM, a)
        an = pr(lt, 4, 4.4) * fo
        d.rounded_rectangle((640, 400, 1010, 520), 18, fill=mix((60, 40, 10), an), outline=mix(YEL, an), width=3)
        ct(d, 418, "16 ≈ 8 ?", SB(38), YEL, an, 825)
        ct(d, 468, "CPU / disk limit", SN(30), WHITE, an, 825)
        caps = ["More workers, less time. But it's never perfectly linear.",
                "At some point CPUs or disks are saturated. Doubling the DOP gives almost nothing."]
        caption(d, caps[0 if lt < 4 else 1], pr(lt, .6, 1) * fo)

    # 6 WHEN
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "When to use it?", SB(60), WHITE, a)
        good = ["Big full scans & reports", "EOD / batch jobs", "CREATE INDEX, CTAS", "Data warehouse queries"]
        bad = ["Short OLTP queries", "Fetch 1 row by index", "Hundreds of users at once"]
        ag = pr(lt, .5, .9) * fo
        glow_box(d, (70, 320, 1010, 700), GREEN, ag)
        d.text((110, 345), "✓ GREAT FOR", font=SB(40), fill=mix(GREEN, ag))
        for k, s in enumerate(good):
            d.text((130, 420 + k * 66), "• " + s, font=SN(36), fill=mix(WHITE, pr(lt, .9 + k * .4, 1.2 + k * .4) * fo))
        ab = pr(lt, 4, 4.4) * fo
        glow_box(d, (70, 760, 1010, 1080), RED, ab)
        d.text((110, 785), "✗ BAD FOR", font=SB(40), fill=mix(RED, ab))
        for k, s in enumerate(bad):
            d.text((130, 860 + k * 66), "• " + s, font=SN(36), fill=mix(WHITE, pr(lt, 4.4 + k * .4, 4.7 + k * .4) * fo))
        caps = ["Parallelism shines when one query has a LOT of data to chew through.",
                "For tiny queries, starting workers costs more than the work itself."]
        caption(d, caps[0 if lt < 4 else 1], pr(lt, .6, 1) * fo)

    # 7 TRAP: OVERLOAD
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Trap: everyone goes parallel", SB(54), RED, a)
        nsess = min(6, int(max(0, lt - .5) / .9) + 1) if lt > .5 else 0
        for k in range(6):
            al = a if k < nsess else 0
            y = 330 + k * 85
            d.rounded_rectangle((70, y, 470, y + 70), 14, fill=mix(CARD, al), outline=mix(PINK, al), width=3)
            d.text((95, y + 16), f"session {k + 1}: DOP 16", font=MN(30), fill=mix(WHITE, al))
            if k < nsess: flow(d, [(470, y + 35), (600, 560)], PINK, al, t, pr(lt, .5 + k * .9, 1 + k * .9), width=3)
        load = min(1.0, nsess / 3.5)
        cx, cy, R = 800, 560, 170
        d.arc((cx - R, cy - R, cx + R, cy + R), 135, 405, fill=mix(OFFB, a), width=30)
        if load > 0: d.arc((cx - R, cy - R, cx + R, cy + R), 135, 135 + 270 * load, fill=mix(RED if load >= 1 else YEL, a), width=30)
        ct(d, cy - 35, f"{int(load * 100)}%", MB(56), RED if load >= 1 else YEL, a, cx)
        ct(d, cy + 35, "CPU", SB(34), WHITE, a, cx)
        aw = pr(lt, 6.5, 6.9) * fo
        d.rounded_rectangle((70, 900, W - 70, 1150), 22, fill=mix(CARD, aw))
        d.text((100, 925), "✗ CPUs saturated, everyone slows down", font=SN(34), fill=mix(RED, aw))
        d.text((100, 985), "✗ queries get DOWNGRADED or queued", font=SN(34), fill=mix(RED, aw))
        d.text((100, 1045), "✓ use Resource Manager / auto DOP", font=SN(34), fill=mix(GREEN, aw))
        caps = ["One parallel query is fast. Six of them at DOP 16 is a traffic jam.",
                "Oracle runs out of parallel servers: queries get downgraded or wait in a queue.",
                "Control it centrally with Resource Manager and automatic DOP, not with hints everywhere."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Remember:", SB(66), WHITE, a)
        items = [("QC", "→ your session, the boss"), ("PX servers", "→ the workers (DOP)"),
                 ("Granules", "→ dynamic load balancing"), ("2 teams", "→ producers + consumers"),
                 ("Not for OLTP", "→ use it for big work")]
        for k, (q, ex) in enumerate(items):
            y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
            d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
            d.text((100, y + 32), q, font=MB(34), fill=mix(GREEN, al))
            d.text((440, y + 32), ex, font=SN(34), fill=mix(WHITE, al))
        caption(d, "Parallel query trades more resources for less time. Spend them wisely.", pr(lt, 2, 2.4) * fo)

    # 9 CTA
    else:
        lt = t - T[9]
        ct(d, 440, "Next video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 540, "MATERIALIZED VIEWS", SB(64), YEL, pr(lt, .2, .5))
        ct(d, 650, "answers computed in advance", SB(44), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "follow · save · share", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.5, T[1] + 8, T[2] + 4, T[2] + 9, T[3] + 6, T[3] + 10, T[4] + 7, T[5] + 6, T[6] + 7, T[7] + 8, T[8] + 4, T[9] + 3]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v13_{k}.png")
        sys.exit()

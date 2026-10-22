from common import *
from make_video5 import arrow
from make_video11 import glow_box, flow
import subprocess, math, sys

T = [0, 6, 18, 32, 46, 60, 72, 84, 96, 104, 110]
DUR = T[-1]; N = FPS * DUR
MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def lerp(a, b, p): return a + (b - a) * p

def drawer(d, box, label, a, col=CYAN, state="on", fill_p=1.0):
    x0, y0, x1, y1 = box
    c = col if state == "on" else RED if state == "x" else (60, 70, 100)
    al = a if state != "dim" else a * .45
    d.rounded_rectangle(box, 14, fill=mix(CARD, al), outline=mix(c, al), width=4)
    # rows inside
    rows = 3; h = (y1 - y0 - 40) / rows
    for r in range(rows):
        yy = y0 + 32 + r * h
        d.line((x0 + 14, yy + h / 2, x0 + 14 + (x1 - x0 - 28) * fill_p, yy + h / 2), fill=mix(c, al * .5), width=6)
    hw = (x1 - x0) * .28; cx = (x0 + x1) / 2
    d.rounded_rectangle((cx - hw / 2, y0 + 6, cx + hw / 2, y0 + 18), 6, fill=mix(c, al))
    ct(d, y1 - 34, label, SB(26), WHITE, al, cx)
    if state == "x":
        d.line((x0 + 10, y0 + 10, x1 - 10, y1 - 10), fill=mix(RED, a * .6), width=4)
        d.line((x1 - 10, y0 + 10, x0 + 10, y1 - 10), fill=mix(RED, a * .6), width=4)

def grid_boxes(x0, y0, cols, w, h, gx, gy, n=12):
    return [(x0 + (k % cols) * (w + gx), y0 + (k // cols) * (h + gy), x0 + (k % cols) * (w + gx) + w, y0 + (k // cols) * (h + gy) + h) for k in range(n)]

def chip(d, cx, cy, txt, col, a, fs=34, tcol=BG):
    w = d.textlength(txt, font=SB(fs)) + 50
    d.rounded_rectangle((cx - w / 2, cy - fs * .95, cx + w / 2, cy + fs * .95), int(fs * .95), fill=mix(col, a))
    ct(d, cy - fs * .62, txt, SB(fs), tcol, a, cx)

def tree(d, cx, cy, s, col, a):
    d.ellipse((cx - 8 * s, cy - 8 * s, cx + 8 * s, cy + 8 * s), fill=mix(col, a))
    for dx in (-1, 1):
        d.line((cx, cy, cx + dx * 20 * s, cy + 22 * s), fill=mix(col, a), width=max(2, int(3 * s)))
        d.ellipse((cx + dx * 20 * s - 6 * s, cy + 22 * s - 6 * s, cx + dx * 20 * s + 6 * s, cy + 22 * s + 6 * s), fill=mix(col, a))

def bar(d, x0, y0, x1, h, p, col, a, label=None, val=None):
    d.rounded_rectangle((x0, y0, x1, y0 + h), h // 2, fill=mix(OFFB, a))
    if p > 0: d.rounded_rectangle((x0, y0, x0 + max(h, (x1 - x0) * p), y0 + h), h // 2, fill=mix(col, a))
    if label: d.text((x0, y0 - 46), label, font=SB(32), fill=mix(WHITE, a))
    if val: d.text((x1 - d.textlength(val, font=MB(32)), y0 - 46), val, font=MB(32), fill=mix(col, a))

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
        ct(d, 240, "2 000 000 000 transactions", SB(56), WHITE, a)
        chip(d, 540, 345, "Query: only MARCH", YEL, pr(lt, .6, 1) * fo)
        x0, y0, x1, y1 = 300, 430, 780, 1050
        d.rounded_rectangle((x0, y0, x1, y1), 20, fill=mix(CARD, a), outline=mix(RED, a), width=5)
        for k in range(28):
            yy = y0 + 18 + k * 21.5
            d.line((x0 + 20, yy, x1 - 20, yy), fill=mix(OFFB, a), width=6)
        sy = lerp(y0, y1, pr(lt, 1.2, 4.6))
        if 1.2 < lt < 4.8:
            d.rectangle((x0 + 6, sy - 6, x1 - 6, sy + 6), fill=mix(RED, a))
        n = int(2_000_000_000 * pr(lt, 1.2, 4.6))
        ct(d, 1090, f"rows scanned: {n:,}".replace(",", " "), MB(40), RED, pr(lt, 1.2, 1.5) * fo)
        caption(d, "You need one month, but Oracle reads all of history. Unless the table is PARTITIONED.", pr(lt, 3.6, 4) * fo)

    # 1 CONCEPT: SPLIT
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 240, "PARTITIONING", SB(66), CYAN, a)
        ct(d, 330, "one table · many physical pieces", SN(40), WHITE, pr(lt, .5, .9) * fo)
        slab = (300, 430, 780, 1050)
        tg = grid_boxes(95, 420, 3, 280, 150, 30, 30)
        p = pr(lt, 1.5, 3.5)
        for k, box in enumerate(tg):
            b = tuple(lerp(slab[j], box[j], p) for j in range(4)) if p < 1 else box
            if p < .05:
                continue
            drawer(d, b, MON[k] if p > .7 else "", a)
        if p < .05:
            d.rounded_rectangle(slab, 20, fill=mix(CARD, a), outline=mix(RED, a), width=5)
        ab = pr(lt, 5.5, 6) * fo
        if ab > 0:
            d.line((70, 420, 70, 1150), fill=mix(YEL, ab), width=6)
            d.line((70, 420, 90, 420), fill=mix(YEL, ab), width=6); d.line((70, 1150, 90, 1150), fill=mix(YEL, ab), width=6)
            chip(d, 540, 1230, "Your SQL still sees ONE table: TRANSACTIONS", YEL, ab, 30)
        caps = ["Partitioning splits one huge table into smaller physical pieces.",
                "Here: one piece per month. Each partition is stored separately.",
                "But for your SQL, nothing changes. It's still one table."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 5.5 else 2], pr(lt, .8, 1.2) * fo)

    # 2 ROUTING
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Where does a new row go?", SB(56), WHITE, a)
        g = grid_boxes(80, 820, 4, 215, 110, 20, 22)
        rows = [("15-MAR · 500 AZN", 2), ("02-JUL · 80 AZN", 6), ("30-DEC · 1200 AZN", 11)]
        k = min(2, int(max(0, lt - 1) / 4)); pl = lt - 1 - k * 4
        tgt = rows[k][1] if lt > 1 else -1
        lit = {rows[j][1] for j in range(3) if lt > 1 + j * 4 + 3}
        for j, box in enumerate(g):
            drawer(d, box, MON[j], a, GREEN if j == tgt and pl > 2.6 else CYAN, "on" if (j in lit or (j == tgt and pl > 2.6)) else "dim")
        # router diamond
        cx, cy = 540, 610; ad = pr(lt, .4, .8) * fo
        d.polygon([(cx, cy - 95), (cx + 260, cy), (cx, cy + 95), (cx - 260, cy)], fill=mix(CARD, ad), outline=mix(YEL, ad))
        ct(d, cy - 48, "PARTITION KEY", SB(30), YEL, ad, cx)
        ct(d, cy + 2, "txn_date", MB(40), WHITE, ad, cx)
        if lt > 1:
            ry = lerp(330, 450, pr(pl, 0, .8))
            glow_box(d, (260, ry - 45, 820, ry + 45), PINK, a * (1 - pr(pl, 3.6, 4)), rows[k][0], None, 34)
            flow(d, [(540, ry + 45), (540, cy - 95)], PINK, a, t, pr(pl, .8, 1.4))
            bx = g[tgt]
            flow(d, [(540, cy + 95), (540, 760), ((bx[0] + bx[2]) / 2, 760), ((bx[0] + bx[2]) / 2, bx[1])], GREEN, a, t, pr(pl, 1.5, 2.6))
        caps = ["Every table has a partition key. Here it's the transaction date.",
                "Oracle reads the key of each new row and routes it to the right partition automatically."]
        caption(d, caps[0 if lt < 2.5 else 1], pr(lt, .8, 1.2) * fo)

    # 3 PRUNING
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Partition PRUNING", SB(60), GREEN, a)
        chip(d, 540, 350, "WHERE txn_date in MARCH", YEL, pr(lt, .4, .8) * fo, 34)
        glow_box(d, (330, 430, 750, 520), CYAN, pr(lt, 1, 1.4) * fo, "Optimizer", None, 38)
        flow(d, [(540, 395), (540, 430)], YEL, a, t, pr(lt, .8, 1.1))
        g = grid_boxes(80, 600, 4, 215, 110, 20, 22)
        pruned = lt > 3
        for j, box in enumerate(g):
            st = "on" if (not pruned or j == 2) else "dim"
            drawer(d, box, MON[j], a, GREEN if (pruned and j == 2) else CYAN, st, fill_p=1 if j != 2 or lt < 5 else pr(lt, 5, 7))
        if pruned:
            bx = g[2]; flow(d, [(540, 520), (540, 560), ((bx[0] + bx[2]) / 2, 560), ((bx[0] + bx[2]) / 2, bx[1])], GREEN, a, t, pr(lt, 3, 4))
        ab = pr(lt, 7, 7.4) * fo
        bar(d, 110, 1060, 970, 34, pr(lt, 7, 8), RED, ab, "Without pruning", "12 / 12")
        bar(d, 110, 1170, 970, 34, pr(lt, 7.6, 8.6) / 12, GREEN, ab, "With pruning", "1 / 12")
        chip(d, 540, 1300, "PARTITION RANGE SINGLE", PURP, pr(lt, 9.5, 9.9) * fo, 32, WHITE)
        caps = ["The query filters on the partition key: only March.",
                "The optimizer knows which partitions can hold the data and skips all the others.",
                "Oracle reads 1 partition out of 12. In the plan you'll see PARTITION RANGE SINGLE."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 4 TYPES
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "3 ways to split", SB(60), WHITE, a)
        # RANGE
        a1 = pr(lt, .5, .9) * fo
        glow_box(d, (70, 310, 1010, 590), CYAN, a1)
        d.text((100, 330), "RANGE", font=MB(42), fill=mix(CYAN, a1)); d.text((330, 338), "by date or number", font=SN(32), fill=mix(WHITE, a1))
        for k, m in enumerate(["JAN", "FEB", "MAR", "APR"]):
            x = 110 + k * 220
            d.rounded_rectangle((x, 420, x + 200, 500), 12, fill=mix(CARD, a1), outline=mix(CYAN, a1), width=3)
            ct(d, 440, m, SB(30), WHITE, a1, x + 100)
        d.line((110, 540, 970, 540), fill=mix(DIM, a1), width=4)
        dx = lerp(110, 650, pr(lt, 1.2, 2.6))
        d.ellipse((dx - 12, 528, dx + 12, 552), fill=mix(YEL, a1))
        # LIST
        a2 = pr(lt, 3.5, 3.9) * fo
        glow_box(d, (70, 640, 1010, 920), YEL, a2)
        d.text((100, 660), "LIST", font=MB(42), fill=mix(YEL, a2)); d.text((330, 668), "by exact values", font=SN(32), fill=mix(WHITE, a2))
        for k, c in enumerate(["BAKU", "GANJA", "SUMGAIT", "OTHER"]):
            x = 110 + k * 220
            d.rounded_rectangle((x, 750, x + 200, 830), 12, fill=mix(CARD, a2), outline=mix(YEL, a2), width=3)
            ct(d, 770, c, SB(28), WHITE, a2, x + 100)
        if lt > 4.5:
            flow(d, [(540, 880), (540, 850), (430, 850), (430, 830)], YEL, a2, t, pr(lt, 4.5, 5.4))
            ct(d, 875, "branch = 'GANJA'", MN(28), YEL, a2, 760)
        # HASH
        a3 = pr(lt, 6.5, 6.9) * fo
        glow_box(d, (70, 970, 1010, 1250), PINK, a3)
        d.text((100, 990), "HASH", font=MB(42), fill=mix(PINK, a3)); d.text((330, 998), "spread evenly", font=SN(32), fill=mix(WHITE, a3))
        fill = pr(lt, 7.2, 10)
        for k in range(4):
            x = 110 + k * 220
            d.rounded_rectangle((x, 1080, x + 200, 1220), 12, fill=mix(CARD, a3), outline=mix(PINK, a3), width=3)
            hh = 120 * fill
            d.rounded_rectangle((x + 10, 1210 - hh, x + 190, 1210), 8, fill=mix((90, 40, 70), a3))
            ct(d, 1090, f"H{k + 1}", SB(28), WHITE, a3, x + 100)
        caps = ["RANGE: each partition holds a range. Perfect for dates: months, years.",
                "LIST: each partition holds specific values, like regions or branches.",
                "HASH: Oracle spreads rows evenly by a hash of the key, like account_id. No hot spots."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 5 INTERVAL + DROP vs DELETE
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Lifecycle superpowers", SB(58), WHITE, a)
        g = grid_boxes(80, 320, 4, 215, 110, 20, 22, 4)
        labels = ["JAN 26", "FEB 26", "MAR 26", "APR 26"]
        for j, box in enumerate(g[:3]):
            drawer(d, box, labels[j], a)
        if lt > 1.5:
            p = pr(lt, 1.5, 2.5); box = g[3]; cx = (box[0] + box[2]) / 2; cy = (box[1] + box[3]) / 2
            s = .3 + .7 * p
            drawer(d, (cx - 107 * s, cy - 55 * s, cx + 107 * s, cy + 55 * s), labels[3] if p > .7 else "", a, GREEN)
            chip(d, 540, 500, "INTERVAL: new month → new partition, automatically", GREEN, pr(lt, 2.4, 2.8) * fo, 28)
        ab = pr(lt, 4.5, 4.9) * fo
        ct(d, 600, "Archive 2019: 300 million rows", SB(40), YEL, ab)
        bar(d, 110, 720, 970, 40, min(.25, pr(lt, 5, 11) * .25), RED, ab, "DELETE ... WHERE year = 2019", "hours…")
        bar(d, 110, 850, 970, 40, pr(lt, 5, 5.3), GREEN, ab, "DROP PARTITION p2019", "instant ✓")
        an = pr(lt, 7.5, 7.9) * fo
        d.rounded_rectangle((70, 950, W - 70, 1100), 22, fill=mix(CARD, an))
        d.text((100, 970), "DELETE: row by row, UNDO + REDO, locks", font=SN(34), fill=mix(RED, an))
        d.text((100, 1030), "DROP: removes a whole segment at once", font=SN(34), fill=mix(GREEN, an))
        caps = ["With INTERVAL partitioning, Oracle creates next month's partition by itself.",
                "Old data? Don't DELETE millions of rows. Drop the whole partition in a second."]
        caption(d, caps[0 if lt < 4.5 else 1], pr(lt, .6, 1) * fo)

    # 6 LOCAL vs GLOBAL INDEX
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Indexes: LOCAL vs GLOBAL", SB(56), WHITE, a)
        dropped = lt > 6
        # LOCAL
        al = pr(lt, .5, .9) * fo
        d.text((90, 320), "LOCAL", font=MB(42), fill=mix(GREEN, al)); d.text((300, 328), "one index per partition", font=SN(32), fill=mix(WHITE, al))
        g = grid_boxes(80, 390, 4, 215, 130, 20, 0, 4)
        for j, box in enumerate(g):
            if dropped and j == 0:
                fa = 1 - pr(lt, 6, 6.8)
                if fa <= 0: continue
                drawer(d, (box[0], box[1] + 60 * (1 - fa), box[2], box[3] + 60 * (1 - fa)), "Q1", al * fa, RED)
                tree(d, (box[0] + box[2]) / 2, box[3] + 30 + 60 * (1 - fa), 1.4, RED, al * fa)
                continue
            drawer(d, box, ["Q1", "Q2", "Q3", "Q4"][j], al)
            tree(d, (box[0] + box[2]) / 2, box[3] + 30, 1.4, GREEN, al)
        if dropped: ct(d, 610, "✓ index leaves with its partition", SB(34), GREEN, pr(lt, 6.8, 7.2) * fo)
        # GLOBAL
        ag = pr(lt, 2.5, 2.9) * fo
        d.text((90, 700), "GLOBAL", font=MB(42), fill=mix(PURP, ag)); d.text((330, 708), "one index over everything", font=SN(32), fill=mix(WHITE, ag))
        g2 = grid_boxes(80, 770, 4, 215, 130, 20, 0, 4)
        for j, box in enumerate(g2):
            if dropped and j == 0: continue
            drawer(d, box, ["Q1", "Q2", "Q3", "Q4"][j], ag)
        bad = dropped and lt > 7.5
        gcol = RED if bad else PURP
        d.rounded_rectangle((80, 930, 1000, 990), 16, fill=mix((40, 24, 60) if not bad else (70, 18, 28), ag), outline=mix(gcol, ag), width=4)
        ct(d, 942, "UNUSABLE ✗" if bad else "global index", SB(32), gcol, ag)
        if bad: chip(d, 540, 1080, "fix: DROP PARTITION ... UPDATE GLOBAL INDEXES", YEL, pr(lt, 8.5, 8.9) * fo, 28)
        caps = ["A LOCAL index is split the same way as the table. Every partition has its own small index.",
                "A GLOBAL index covers all partitions at once.",
                "Drop a partition: the local index simply goes with it.",
                "But a global index becomes UNUSABLE, unless you maintain it during the operation."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 6 else 2 if lt < 7.5 else 3], pr(lt, .6, 1) * fo)

    # 7 TRAP
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Trap: pruning switched OFF", SB(56), RED, a)
        fixed = lt > 6.5
        if fixed:
            glow_box(d, (60, 300, 1020, 420), GREEN, pr(lt, .4, .8) * fo, "WHERE txn_date >= DATE '2026-03-01'", "AND txn_date < DATE '2026-04-01'", 28, 28)
        else:
            glow_box(d, (60, 310, 1020, 410), RED, pr(lt, .4, .8) * fo, "WHERE TO_CHAR(txn_date, 'MM') = '03'", None, 30)
        g = grid_boxes(80, 470, 4, 215, 110, 20, 22)
        for j, box in enumerate(g):
            if fixed: drawer(d, box, MON[j], a, GREEN if j == 2 else CYAN, "on" if j == 2 else "dim")
            else: drawer(d, box, MON[j], a, RED, "on" if lt > 2 else "dim")
        chip(d, 540, 940, "PARTITION RANGE SINGLE ✓" if fixed else "PARTITION RANGE ALL ✗", GREEN if fixed else RED, pr(lt, 2.2, 2.6) * fo, 32, BG if fixed else WHITE)
        an = pr(lt, 4, 4.4) * fo * (1 - pr(lt, 6.2, 6.5))
        d.rounded_rectangle((70, 1030, W - 70, 1180), 22, fill=mix(CARD, an))
        d.text((100, 1050), "✗ function on the partition key", font=SN(34), fill=mix(RED, an))
        d.text((100, 1110), "✗ no partition key in WHERE at all", font=SN(34), fill=mix(RED, an))
        caps = ["Wrap the partition key in a function, and the optimizer can't map it to partitions.",
                "Result: all 12 partitions are scanned. Same as no partitioning at all.",
                "Compare the raw column with a date range, and pruning is back."]
        caption(d, caps[0 if lt < 2.2 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Remember:", SB(66), WHITE, a)
        items = [("Partition key", "→ routes every row"), ("Pruning", "→ read only what you need"),
                 ("RANGE / LIST / HASH", "→ pick by data shape"), ("DROP PARTITION", "→ instant archive"),
                 ("Function on key", "→ pruning OFF")]
        for k, (q, ex) in enumerate(items):
            y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
            d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
            d.text((100, y + 32), q, font=MB(32), fill=mix(GREEN, al))
            d.text((500, y + 32), ex, font=SN(34), fill=mix(WHITE, al))
        caption(d, "Note: Partitioning is a separately licensed Enterprise Edition option.", pr(lt, 2, 2.4) * fo)

    # 9 CTA
    else:
        lt = t - T[9]
        ct(d, 440, "Next video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 540, "PARALLEL QUERY", SB(72), YEL, pr(lt, .2, .5))
        ct(d, 650, "one query, many workers", SB(46), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "follow · save · share", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.5, T[1] + 7, T[2] + 4, T[2] + 11.5, T[3] + 9, T[4] + 9, T[5] + 8, T[6] + 4, T[6] + 10, T[7] + 4, T[7] + 9, T[8] + 4]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v12_{k}.png")
        sys.exit()

from vhelp import *
from make_video19 import code
from make_video14 import cyl

T = T10; DUR = T[-1]

def buf(d, x, y, w, h, col, a, txt=None, fs=24):
    d.rounded_rectangle((x, y, x + w, y + h), 8, fill=mix(col, a))
    if txt: ct(d, y + h / 2 - fs * .6, txt, SB(fs), BG, a, x + w / 2)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        code(d, 230, [("SELECT SUM(bal) FROM accounts", YEL), ("WHERE branch_id = 12;", YEL)], a, 32)
        bar(d, 110, 460, 970, 44, pr(lt, .6, 2), RED, pr(lt, .5, .9) * fo, "1st run", "2.0 s · 50 000 disk reads")
        bar(d, 110, 600, 970, 44, pr(lt, 2.2, 2.4) * .025, GREEN, pr(lt, 2.1, 2.5) * fo, "2nd run", "0.05 s · 0 disk reads")
        ct(d, 740, "40× faster. Same SQL. Why?", SB(48), YEL, pr(lt, 2.8, 3.2) * fo)
        caption(d, "The second run never touched the disk. Meet the buffer cache.", pr(lt, 4, 4.4) * fo)

    # 1 WHAT IT IS
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Blocks live in MEMORY", SB(54), WHITE, a)
        d.rounded_rectangle((60, 310, 1020, 620), 26, outline=mix(CYAN, a), width=3)
        d.text((90, 322), "SGA → BUFFER CACHE", font=SB(28), fill=mix(CYAN, a))
        n = int(min(24, max(0, (lt - 2) * 6)))
        for k in range(24):
            r, c = divmod(k, 8); x = 100 + c * 112; y = 380 + r * 76
            buf(d, x, y, 96, 60, CYAN if k < n else OFFB, a * (.9 if k < n else .4))
        cyl(d, 540, 820, 420, 150, PURP, a, "DATAFILES", "8 KB blocks")
        if 1.5 < lt < 6:
            p = (lt * .8) % 1
            y = lerp(760, 560, p); d.rounded_rectangle((510, y, 570, y + 40), 6, fill=mix(YEL, a))
        card_list(d, 980, [("logical read = from memory (µs)", GREEN, 5),
                           ("physical read = from disk (ms)", RED, 7)], lt, fo, 80, 32)
        caps = ["Oracle never works on data directly on disk. It copies each block from the datafiles into the buffer cache.",
                "Once a block is in memory, every session can read it from there.",
                "Reading from memory is a logical read: microseconds. Reading from disk is a physical read: milliseconds. A thousand times slower."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 2 LOOKUP: HASH
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Is the block in memory?", SB(54), WHITE, a)
        glow_box(d, (90, 320, 470, 430), YEL, a, "file 7, block 4812", None, 32)
        arrow(d, 470, 375, 560, 375, WHITE, pr(lt, 1, 1.4) * fo, 5)
        glow_box(d, (570, 320, 990, 430), PURP, pr(lt, 1, 1.4) * fo, "hash → bucket 3", None, 32)
        for k in range(5):
            y = 480 + k * 95; hit = k == 3
            col = CYAN
            al = pr(lt, 1.8, 2.2) * fo
            buf(d, 90, y, 160, 70, col, al, f"bucket {k}", 22)
            for j in range(3 if k != 3 else 2):
                x = 300 + j * 180
                d.rounded_rectangle((x, y + 5, x + 150, y + 65), 8, fill=mix(CARD, al), outline=mix(DIM, al), width=2)
                ct(d, y + 20, "blk", SN(24), DIM, al, x + 75)
                arrow(d, x - 50, y + 35, x, y + 35, DIM, al, 3)
        if lt > 3:
            ah = pr(lt, 3, 3.4) * fo
            d.rounded_rectangle((86, 761, 254, 829), 10, outline=mix(YEL, ah), width=5)
        hit = lt < 7
        ar = pr(lt, 4.5, 4.9) * fo
        if hit:
            d.rounded_rectangle((475, 770, 635, 830), 8, fill=mix(GREEN, ar))
            ct(d, 785, "4812 ✓", SB(26), BG, ar, 555)
            ct(d, 1000, "CACHE HIT → logical read", SB(40), GREEN, ar)
        else:
            am = pr(lt, 7, 7.4) * fo
            ct(d, 1000, "MISS → read from disk → free buffer", SB(38), RED, am)
            d.rounded_rectangle((660, 770, 810, 830), 8, fill=mix(YEL, am))
            ct(d, 785, "4812 new", SB(24), BG, am, 735)
        caps = ["Every block has an address: file number and block number. Oracle hashes the address to pick a bucket.",
                "Each bucket holds a short chain of buffer headers. Oracle walks the chain, protected by a cache buffers chains latch.",
                "Found it? A cache hit. Not there? Oracle reads the block from disk into a free buffer, and links it into the chain."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 3 LRU + TOUCH COUNT
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Who stays? LRU + touch count", SB(50), YEL, a)
        d.text((90, 320), "HOT end", font=SB(30), fill=mix(RED, a))
        d.text((830, 320), "COLD end", font=SB(30), fill=mix(CYAN, a))
        for k in range(12):
            x = 90 + k * 78
            h = 1 - k / 11
            col = tuple(int(RED[j] * h + CYAN[j] * (1 - h)) for j in range(3))
            buf(d, x, 380, 66, 90, col, a * .85)
        # new block into middle
        p = pr(lt, 1.5, 3)
        if lt > 1.5:
            x = lerp(540, 520, p); y = lerp(560, 480, p)
            buf(d, 500, lerp(620, 490, p), 80, 60, YEL, a, "new", 22)
            ct(d, 700, "new blocks enter the MIDDLE", SB(32), YEL, pr(lt, 1.5, 1.9) * fo)
        # touched block moves to hot
        if lt > 4:
            p2 = pr(lt, 5, 6.5)
            tc = min(3, int((lt - 4) * 1.5))
            bx = lerp(830, 90, p2)
            d.rounded_rectangle((bx, 780, bx + 120, 870), 10, fill=mix(GREEN, a))
            ct(d, 800, f"tc={tc}", SB(28), BG, a, bx + 60)
            ct(d, 900, "touched often → promoted to HOT", SB(32), GREEN, pr(lt, 4, 4.4) * fo)
        card_list(d, 980, [("cold & untouched → reused for the next read", CYAN, 8.5)], lt, fo, 80, 31)
        caps = ["The cache is full most of the time, so Oracle must decide which blocks to keep. It uses an LRU list with a hot and a cold end.",
                "A new block is inserted in the middle, not at the hot end. One read is not enough to push out your hot data.",
                "Each access raises the block's touch count. Busy blocks are promoted to the hot end, and cold, untouched buffers are reused first."]
        caption(d, caps[0 if lt < 1.5 else 1 if lt < 4 else 2], pr(lt, .6, 1) * fo)

    # 4 FULL SCANS / DIRECT PATH
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Big full scan? Bypass the cache", SB(48), PINK, a)
        cyl(d, 270, 470, 340, 170, PURP, a, "BIG TABLE", "40 GB")
        d.rounded_rectangle((600, 360, 1000, 580), 22, outline=mix(CYAN, a), width=3)
        ct(d, 380, "BUFFER CACHE", SB(28), CYAN, a, 800)
        for k in range(8):
            buf(d, 630 + (k % 4) * 90, 430 + (k // 4) * 70, 76, 54, RED if k < 4 else CYAN, a * .85)
        glow_box(d, (600, 700, 1000, 830), GREEN, pr(lt, 2, 2.4) * fo, "session PGA", "direct path read", 32, 26)
        if lt > 2.5:
            for k in range(3):
                p = (t * .9 + k / 3) % 1
                x = lerp(440, 600, p); y = lerp(500, 765, p)
                d.rounded_rectangle((x - 22, y - 16, x + 22, y + 16), 6, fill=mix(YEL, pr(lt, 2.5, 2.9) * fo))
        ct(d, 620, "hot data stays safe ✓", SB(30), RED, pr(lt, 4, 4.4) * fo, 800)
        card_list(d, 900, [("wait event: direct path read", PINK, 6),
                           ("small tables → cached normally", CYAN, 7.5)], lt, fo, 80, 32)
        caps = ["A full scan of a huge table would flush everything useful out of the cache.",
                "So for large tables, Oracle often reads blocks straight into the session's private memory, the PGA: a direct path read.",
                "Your hot index and lookup blocks stay in the cache. Small tables are still cached the normal way."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 5 DIRTY BUFFERS
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Changed blocks = DIRTY", SB(54), YEL, a)
        n = int(min(16, max(0, (lt - .8) * 3)))
        written = int(max(0, (lt - 5) * 4))
        for k in range(16):
            r, c = divmod(k, 8); x = 100 + c * 112; y = 330 + r * 90
            dirty = k < n and k >= written
            buf(d, x, y, 96, 70, YEL if dirty else (GREEN if k < written else CYAN), a * .9, "dirty" if dirty else "clean", 20)
        chip(d, 540, 590, "DBWn", CYAN, pr(lt, 4.5, 4.9) * fo, 34, BG)
        cyl(d, 540, 760, 400, 140, PURP, a, "DATAFILES", None)
        if lt > 5: flow(d, [(540, 620), (540, 700)], CYAN, a, t, pr(lt, 5, 5.6))
        ab = pr(lt, 7.5, 7.9) * fo
        glow_box(d, (110, 880, 970, 1000), RED, ab, "free buffer waits", "DBWn can't keep up", 34, 26)
        caps = ["When you change a row, the block changes in memory and becomes dirty. The datafile is not touched yet.",
                "The database writer, DBWn, writes dirty blocks to disk later, in batches, and they become clean and reusable.",
                "If DBWn falls behind, sessions find no clean buffer to read into, and wait: free buffer waits."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 6 HIT RATIO MYTH
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The 99% hit ratio myth", SB(54), RED, a)
        glow_box(d, (90, 320, 520, 470), GREEN, pr(lt, .6, 1) * fo, "hit ratio 99.9%", "looks perfect…", 36, 28)
        glow_box(d, (560, 320, 990, 470), RED, pr(lt, 2, 2.4) * fo, "500M logical reads", "per hour", 36, 28)
        bar(d, 110, 560, 970, 44, pr(lt, 3, 4.5), RED, pr(lt, 2.8, 3.2) * fo, "bad SQL: logical reads", "500 M")
        bar(d, 110, 680, 970, 44, pr(lt, 5, 6) * .02, GREEN, pr(lt, 4.8, 5.2) * fo, "tuned SQL", "10 M")
        ct(d, 800, "both have a ~99% hit ratio!", SB(36), YEL, pr(lt, 6.5, 6.9) * fo)
        card_list(d, 880, [("logical reads cost CPU + latches", WHITE, 8),
                           ("measure: buffer gets per execution", GREEN, 9.5)], lt, fo, 80, 32)
        caps = ["A high buffer cache hit ratio doesn't mean a healthy database.",
                "A badly written query that re-reads the same cached blocks millions of times has a perfect hit ratio, and still burns the CPU.",
                "Logical reads are cheap, not free. Look at buffer gets per execution of your top SQL, not at the ratio."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 7 SIZING: CACHE ADVICE GRAPH
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How big should it be?", SB(54), CYAN, a)
        gx0, gy0, gx1, gy1 = 130, 330, 970, 760
        d.line((gx0, gy1, gx1, gy1), fill=mix(DIM, a), width=3); d.line((gx0, gy0, gx0, gy1), fill=mix(DIM, a), width=3)
        d.text((gx0 + 10, gy0 - 10), "physical reads", font=SN(26), fill=mix(DIM, a))
        ct(d, gy1 + 10, "cache size →", SN(26), DIM, a)
        p = pr(lt, .8, 4)
        pts = []
        for k in range(int(60 * p) + 1):
            xx = k / 60
            yy = 0.9 * math.exp(-4 * xx) + .06
            pts.append((gx0 + xx * (gx1 - gx0), gy1 - yy * (gy1 - gy0)))
        if len(pts) > 1: d.line(pts, fill=mix(CYAN, a), width=6)
        if lt > 4.5:
            ak = pr(lt, 4.5, 4.9) * fo
            x = gx0 + .45 * (gx1 - gx0)
            d.line((x, gy0 + 60, x, gy1), fill=mix(YEL, ak), width=3)
            ct(d, gy0 + 20, "knee: more memory ≈ no gain", SB(28), YEL, ak, x + 60)
        code(d, 840, [("V$DB_CACHE_ADVICE  -- this curve", CYAN), ("KEEP pool / RECYCLE pool", PINK)], pr(lt, 6.5, 6.9) * fo, 28)
        caps = ["How much memory? Oracle predicts it for you. V dollar D B cache advice estimates physical reads for different cache sizes.",
                "The curve drops quickly, then flattens. Past the knee, more memory buys almost nothing.",
                "You can also pin small hot tables in a keep pool, and send big one-time scans to a recycle pool."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Buffer cache", "→ blocks in memory"), ("Lookup", "→ hash bucket, chain, latch"),
                          ("LRU", "→ middle insert, touch count"), ("Big scans", "→ direct path, bypass"),
                          ("Hit ratio", "→ watch gets per exec")],
              "Memory is a thousand times faster than disk. But fewer reads beat faster reads.", 450)
    else:
        cta(d, t - T[9], "INDEXES DEEP DIVE", "why Oracle ignores your index", 64)
    return im

if __name__ == "__main__":
    preview(frame, T, "v27_sheet.png")

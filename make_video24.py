from vhelp import *
from make_video19 import code
from make_video14 import user

T = T10; DUR = T[-1]

def sess(d, x, y, col, a, lbl):
    d.ellipse((x - 34, y - 34, x + 34, y + 34), fill=mix(col, a))
    ct(d, y - 16, lbl, SB(26), BG, a, x)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "CPU 100% … but nothing gets done?", SB(48), WHITE, a)
        p = pr(lt, .6, 2.4)
        cpu = min(1, p * (1 + .05 * math.sin(t * 20)))
        bar(d, 110, 380, 970, 50, cpu, RED, pr(lt, .5, .9) * fo, "CPU", f"{int(cpu * 100)}%")
        bar(d, 110, 520, 970, 50, .12 * p, GREEN, pr(lt, .8, 1.2) * fo, "useful work", "12%")
        ae = pr(lt, 2.6, 3) * fo
        glow_box(d, (110, 640, 970, 770), YEL, ae, "latch: cache buffers chains", "top wait event", 36, 28)
        # spinning sessions
        for k in range(6):
            an = t * 4 + k * math.pi / 3
            x, y = 540 + 150 * math.cos(an), 960 + 70 * math.sin(an)
            sess(d, x, y, CYAN, pr(lt, 3, 3.4) * fo, f"S{k + 1}")
        caption(d, "Sessions spinning on tiny memory locks: latches and mutexes. Let's open them up.", pr(lt, 4, 4.4) * fo)

    # 1 WHY: SHARED MEMORY
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Shared memory needs a guard", SB(52), WHITE, a)
        d.rounded_rectangle((300, 520, 780, 760), 24, outline=mix(DIM, a), width=3)
        ct(d, 535, "SGA list", SB(32), DIM, a)
        for k in range(4):
            x = 340 + k * 110
            d.rounded_rectangle((x, 600, x + 90, 690), 12, fill=mix(CYAN, a * .8))
            if k < 3: arrow(d, x + 90, 645, x + 110, 645, WHITE, a, 4)
        p = pr(lt, 1, 3)
        sess(d, lerp(120, 300, p), 640, PINK, a, "S1")
        sess(d, lerp(960, 780, p), 640, YEL, a, "S2")
        if 3 < lt < 6:
            ab = (int(lt * 6) % 2) * fo
            ct(d, 430, "BOTH change it at once!", SB(40), RED, ab)
            ct(d, 800, "→ corrupted list", SB(36), RED, pr(lt, 3.5, 3.9) * fo)
        if lt > 6:
            al = pr(lt, 6, 6.4) * fo
            d.rounded_rectangle((470, 440, 610, 510), 14, fill=mix(GREEN, al))
            ct(d, 455, "LATCH", SB(30), BG, al, 540)
            ct(d, 800, "one at a time ✓", SB(40), GREEN, al)
        caps = ["The SGA is shared memory. Hundreds of sessions read and change the same lists and hash chains.",
                "If two processes change the same pointer at the same instant, the structure is corrupted.",
                "So Oracle guards each structure with a tiny lock that lives in memory: a latch, or a mutex."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 2 LATCH vs LOCK
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Latch ≠ Lock", SB(64), WHITE, a)
        glow_box(d, (60, 320, 520, 420), CYAN, pr(lt, .5, .9) * fo, "LATCH / MUTEX", None, 38)
        glow_box(d, (560, 320, 1020, 420), PURP, pr(lt, 1, 1.4) * fo, "LOCK (enqueue)", None, 38)
        rows = [("protects", "memory structures", "rows, tables"), ("held for", "microseconds", "until COMMIT"),
                ("waiters", "spin → sleep, no queue", "FIFO queue"), ("you control it?", "no, Oracle does", "yes: your DML"),
                ("wait event", "latch: … / mutex …", "enq: TX / TM …")]
        for k, (lab, l, r) in enumerate(rows):
            y = 450 + k * 120; al = pr(lt, 2 + k * 1.4, 2.4 + k * 1.4) * fo
            ct(d, y, lab, SN(28), DIM, al)
            d.rounded_rectangle((60, y + 34, 520, y + 100), 14, fill=mix((20, 46, 66), al))
            d.rounded_rectangle((560, y + 34, 1020, y + 100), 14, fill=mix((40, 26, 66), al))
            ct(d, y + 48, l, SB(29), WHITE, al, 290); ct(d, y + 48, r, SB(29), WHITE, al, 790)
        caps = ["Don't confuse latches with locks. Latches and mutexes protect memory. Locks protect your data.",
                "A latch is held for microseconds. A row lock is held until you commit.",
                "Lock waiters line up in a fair queue. Latch waiters have no queue: they spin and retry."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 3 SPIN THEN SLEEP
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Busy? Spin… then sleep", SB(54), YEL, a)
        d.rounded_rectangle((440, 330, 640, 430), 16, fill=mix(RED, a))
        ct(d, 352, "LATCH", SB(34), BG, a, 540)
        ct(d, 450, "held by S1", SN(30), RED, a)
        sess(d, 540, 560, PINK, a, "S1")
        # S2 spinning loop
        cx, cy = 300, 760
        if lt < 7:
            an = t * 10
            d.arc((cx - 110, cy - 110, cx + 110, cy + 110), math.degrees(an) % 360, math.degrees(an) % 360 + 270, fill=mix(YEL, a), width=8)
        sess(d, cx, cy, CYAN, a, "S2")
        spins = int(min(2000, max(0, (lt - 1) * 400)))
        ct(d, 900, f"spins: {spins}", MB(36), YEL, pr(lt, 1, 1.4) * fo, cx)
        bar(d, 560, 720, 980, 40, pr(lt, 1, 4), RED, pr(lt, 1, 1.4) * fo, "CPU burned", "")
        if lt > 4.5:
            az = pr(lt, 4.5, 4.9) * fo
            ct(d, 820, "zzz sleep", SB(40), PURP, az, 770)
            ct(d, 880, "→ retry", SB(34), WHITE, pr(lt, 6, 6.4) * fo, 770)
        card_list(d, 1000, [("spinning = CPU, sleeping = wait time", WHITE, 8),
                            ("hot latch → high CPU AND high waits", RED, 9.5)], lt, fo, 80, 32)
        caps = ["When a latch is busy, the session doesn't queue. It spins on the CPU, checking again and again.",
                "Spinning is cheap if the holder releases in microseconds. If not, the session goes to sleep and retries later.",
                "That's why a hot latch shows up twice: as burned CPU, and as latch wait time."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 4 CACHE BUFFERS CHAINS
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "cache buffers chains", SB(54), CYAN, a)
        for k in range(5):
            y = 330 + k * 110; hot = k == 2
            col = RED if hot and lt > 3 else CYAN
            d.rounded_rectangle((80, y, 230, y + 80), 12, fill=mix(col, a * .9))
            ct(d, y + 22, f"bucket {k}", SB(26), BG, a, 155)
            n = 3 if k != 2 else 4
            for j in range(n):
                x = 280 + j * 150
                d.rounded_rectangle((x, y + 10, x + 120, y + 70), 10, fill=mix(CARD, a), outline=mix(col, a), width=2)
                ct(d, y + 24, "blk" if not (hot and j == 1) else "HOT", SN(24), WHITE if not (hot and j == 1) else YEL, a, x + 60)
                arrow(d, x - 30, y + 40, x, y + 40, DIM, a, 3)
        if lt > 3:
            for k in range(6):
                p = (t * .7 + k / 6) % 1
                x = lerp(1040, 470, p); y = lerp(330 + (k % 5) * 110 + 40, 590, p)
                d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=mix(PINK, pr(lt, 3, 3.4) * fo))
        card_list(d, 900, [("1 hot block → 1 chain → 1 latch", RED, 5),
                           ("cause: SQL doing MILLIONS of logical reads", YEL, 7),
                           ("fix the SQL, not the latch", GREEN, 9)], lt, fo, 80, 32)
        caps = ["The buffer cache is a hash table. Each bucket has a chain of buffers, guarded by a cache buffers chains latch.",
                "When everyone hammers the same hot block, for example one index root or one popular row, they all need the same latch.",
                "The real cause is usually SQL doing millions of logical reads. Fix the SQL and the latch calms down."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 5 MUTEXES
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Mutexes: guarding cursors", SB(52), PURP, a)
        glow_box(d, (300, 340, 780, 520), PURP, a, "CURSOR  7h2kq9x", "in the library cache", 36, 28)
        am = pr(lt, 1.5, 1.9) * fo
        d.rounded_rectangle((680, 300, 820, 360), 12, fill=mix(YEL, am))
        ct(d, 312, "mutex", SB(28), BG, am, 750)
        for k in range(5):
            p = pr(lt, 2.5 + k * .3, 3.5 + k * .3)
            x = lerp(100 + k * 220, 300 + k * 120, p)
            sess(d, x, 680, CYAN, a, f"S{k + 1}")
            if p > .9: arrow(d, 300 + k * 120, 646, 400 + k * 70, 520, CYAN, a * .7, 3)
        ae = pr(lt, 5.5, 5.9) * fo
        glow_box(d, (90, 790, 520, 900), RED, ae, "cursor: pin S", "1000s exec/sec of ONE cursor", 30, 24)
        glow_box(d, (560, 790, 990, 900), RED, pr(lt, 6.5, 6.9) * fo, "library cache: mutex X", "hard parse / invalidation", 30, 24)
        card_list(d, 950, [("mutex = tiny lock INSIDE each object", YEL, 8.5)], lt, fo, 80, 32)
        caps = ["Since Oracle 10g and 11g, cursors in the library cache are protected by mutexes, not by a few global latches.",
                "A mutex lives inside each object, so contention is spread out. But one extremely hot cursor still serializes everyone.",
                "Cursor pin S waits mean thousands of executions per second of the same cursor. Library cache mutex X points to parsing and invalidations."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 6 CAUSE -> FIX
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Symptom → real fix", SB(56), GREEN, a)
        rows = [("cache buffers chains", "tune SQL: fewer logical reads", CYAN),
                ("shared pool / library cache", "bind variables, no hard parse", YEL),
                ("cursor: pin S", "fewer calls: batch, cache results", PURP),
                ("high version count", "fix bind mismatch, stats, env", PINK)]
        for k, (sym, fix, col) in enumerate(rows):
            y = 330 + k * 175; al = pr(lt, .6 + k * 2, 1 + k * 2) * fo
            d.rounded_rectangle((70, y, 500, y + 140), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            for j, ln in enumerate(sym.split(" / ")): ct(d, y + 30 + j * 40, ln, SB(30), col, al, 285)
            arrow(d, 510, y + 70, 570, y + 70, WHITE, al, 6)
            d.rounded_rectangle((580, y, 1010, y + 140), 16, fill=mix((20, 50, 36), al))
            for j, ln in enumerate(wrap(d, fix, SN(30), 400)): d.text((605, y + 30 + j * 40), ln, font=SN(30), fill=mix(WHITE, al))
        caps = ["Latch waits are symptoms. Cache buffers chains? Find the SQL with the most logical reads and tune it.",
                "Shared pool and library cache contention usually means hard parsing: use bind variables.",
                "Cursor pin S means the same cursor is called too often: batch the calls. And investigate high version counts."]
        caption(d, caps[0 if lt < 2.6 else 1 if lt < 6.6 else 2], pr(lt, .6, 1) * fo)

    # 7 DIAGNOSE
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How to diagnose", SB(58), WHITE, a)
        d.text((110, 320), "V$LATCH", font=MB(32), fill=mix(CYAN, a))
        lat = [("gets", 1.0, CYAN, "10 000 000"), ("misses", .3, YEL, "3 000 000"), ("sleeps", .08, RED, "800 000")]
        for k, (nm, p, col, v) in enumerate(lat):
            bar(d, 110, 400 + k * 110, 970, 40, pr(lt, .8 + k * .6, 1.8 + k * .6) * p, col, pr(lt, .6 + k * .6, 1 + k * .6) * fo, nm, v)
        ct(d, 730, "misses / gets = 30% → contention!", SB(34), YEL, pr(lt, 3, 3.4) * fo)
        code(d, 800, [("V$MUTEX_SLEEP      -- mutex hot spots", PURP), ("ASH: event + sql_id -- WHO causes it", PINK),
                      ("AWR: Latch / Mutex sections", CYAN)], pr(lt, 5, 5.4) * fo, 28)
        caps = ["V dollar latch shows gets, misses, and sleeps for every latch. A high miss ratio means contention.",
                "V dollar mutex sleep shows the mutex hot spots.",
                "Then use ASH to join the wait event with the SQL ID. The latch is never the culprit, the SQL is."]
        caption(d, caps[0 if lt < 5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Latch", "→ guards SGA memory, µs"), ("Waiters", "→ spin on CPU, then sleep"),
                          ("CBC", "→ hot block, tune the SQL"), ("Mutex", "→ guards cursors"),
                          ("Fix", "→ the SQL, not the latch")],
              "Latches and mutexes are symptoms. Find the SQL behind them.", 400)
    else:
        cta(d, t - T[9], "LOCKS & ENQUEUES", "who is blocking me?", 64)
    return im

if __name__ == "__main__":
    preview(frame, T, "v24_sheet.png")

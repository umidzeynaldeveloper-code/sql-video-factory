from vhelp import *
from make_video19 import code
from make_video14 import cyl

T = T10; DUR = T[-1]

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "03:12 AM · EOD batch", SB(50), DIM, a)
        ab = pr(lt, .8, 1.2) * fo
        d.rounded_rectangle((90, 320, 990, 470), 18, fill=mix((60, 22, 34), ab), outline=mix(RED, ab), width=4)
        d.text((120, 345), "ORA-01652: unable to extend", font=MB(32), fill=mix(RED, ab))
        d.text((120, 400), "temp segment by 128 in TEMP", font=MB(32), fill=mix(RED, ab))
        bar(d, 110, 560, 970, 44, pr(lt, 1.5, 3), RED, pr(lt, 1.4, 1.8) * fo, "TEMP used", "100%")
        ct(d, 700, "Who used all the TEMP? And why?", SB(44), YEL, pr(lt, 3, 3.4) * fo)
        caption(d, "To answer that, we need to look at private session memory: the PGA.", pr(lt, 4, 4.4) * fo)

    # 1 SGA vs PGA
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "SGA is shared. PGA is private.", SB(48), WHITE, a)
        glow_box(d, (90, 320, 990, 470), CYAN, a, "SGA", "buffer cache · shared pool · log buffer: ONE for all", 40, 26)
        for k in range(4):
            x = 90 + k * 230; al = pr(lt, 2 + k * .5, 2.4 + k * .5) * fo
            d.ellipse((x + 70, 540, x + 140, 610), fill=mix(PINK, al))
            ct(d, 555, f"S{k + 1}", SB(26), BG, al, x + 105)
            d.line((x + 105, 520, x + 105, 470), fill=mix(DIM, al), width=3)
            glow_box(d, (x, 640, x + 210, 800), PURP, al, "PGA", "private", 32, 24)
        card_list(d, 860, [("each server process gets its OWN PGA", PURP, 5),
                           ("200 sessions × 50 MB = 10 GB of RAM", YEL, 7.5)], lt, fo, 80, 31)
        caps = ["The SGA is one shared memory area for the whole instance.",
                "The PGA is different: every server process gets its own private memory.",
                "It adds up fast. Two hundred sessions using fifty megabytes each is ten gigabytes of RAM."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 2 WHAT USES PGA
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "What lives in the PGA?", SB(54), PURP, a)
        items = [("SORT area", "ORDER BY · GROUP BY · DISTINCT · index build", YEL),
                 ("HASH area", "hash joins: the build table", PINK),
                 ("COLLECTIONS", "BULK COLLECT arrays (video 31)", GREEN),
                 ("session state", "package variables, cursors", CYAN)]
        for k, (h, s_, col) in enumerate(items):
            y = 320 + k * 160; al = pr(lt, .6 + k * 1.8, 1 + k * 1.8) * fo
            d.rounded_rectangle((70, y, W - 70, y + 140), 18, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 22), h, font=SB(36), fill=mix(col, al))
            d.text((100, y + 82), s_, font=SN(28), fill=mix(WHITE, al))
        card_list(d, 990, [("sort & hash areas = \"work areas\"", WHITE, 8)], lt, fo, 80, 31)
        caps = ["The biggest PGA users are work areas. The sort area handles ORDER BY, GROUP BY, DISTINCT, and index builds.",
                "The hash area holds the build table of a hash join.",
                "PL/SQL collections from BULK COLLECT and package variables live there too."]
        caption(d, caps[0 if lt < 2.4 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    # 3 OPTIMAL / ONE-PASS / MULTI-PASS
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Fits in memory? Or spills?", SB(52), YEL, a)
        modes = [("OPTIMAL", "all in PGA", GREEN, 0, .6), ("ONE-PASS", "spill once to TEMP", YEL, 1, 3), ("MULTI-PASS", "spill again & again", RED, 3, 6)]
        for k, (nm, s_, col, passes, st) in enumerate(modes):
            y = 330 + k * 230; al = pr(lt, st, st + .4) * fo
            glow_box(d, (70, y, 400, y + 160), col, al, nm, s_, 34, 24)
            d.rounded_rectangle((470, y + 20, 640, y + 140), 14, fill=mix(PURP, al * .8)); ct(d, y + 60, "PGA", SB(30), BG, al, 555)
            if passes:
                cyl(d, 880, y + 85, 200, 110, CYAN, al, "TEMP", None)
                for j in range(passes):
                    pp = (t * 1.2 + j / passes) % 1
                    x = lerp(640, 780, pp) if (j % 2 == 0) else lerp(780, 640, pp)
                    d.ellipse((x - 12, y + 70, x + 12, y + 94), fill=mix(col, al))
        bar(d, 110, 1040, 970, 36, pr(lt, 8, 9) * .2, GREEN, pr(lt, 7.8, 8.2) * fo, "optimal", "fast")
        caps = ["If a sort fits in the PGA, it runs optimally, entirely in memory.",
                "If not, it spills to the temporary tablespace. One pass: write once, read back once. Slower, but acceptable.",
                "Multi-pass means the data goes to TEMP and back again and again. That's when sorts get really slow, and TEMP fills up."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 4 PGA_AGGREGATE_TARGET
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Who decides the size?", SB(54), CYAN, a)
        code(d, 320, [("PGA_AGGREGATE_TARGET = 4G   -- soft goal", CYAN), ("PGA_AGGREGATE_LIMIT  = 8G   -- hard cap", RED)], a, 30)
        n = int(min(10, max(1, lt * 1.3)))
        per = 1 / n
        ct(d, 520, f"{n} active work areas share the target", SB(32), WHITE, pr(lt, 1, 1.4) * fo)
        for k in range(n):
            x0 = 110 + k * (860 / n)
            d.rounded_rectangle((x0 + 4, 580, x0 + 860 / n - 4, 660), 8, fill=mix(PURP, a * .85))
        ct(d, 690, "more sorts at once → smaller share each", SB(32), PURP, pr(lt, 1, 1.4) * fo)
        ab = pr(lt, 6, 6.4) * fo
        glow_box(d, (110, 790, 970, 920), RED, ab, "LIMIT hit → sessions killed: ORA-04036", None, 32)
        caps = ["Oracle manages work areas automatically. PGA aggregate target is the goal for all sessions together.",
                "The more sessions sort at the same time, the smaller each one's share, and the more they spill to TEMP.",
                "PGA aggregate limit is the hard cap. Go over it, and Oracle aborts the calls of the sessions using the most memory."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 5 TEMP TABLESPACE
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "TEMP: the overflow tank", SB(54), PINK, a)
        cyl(d, 540, 520, 520, 300, PINK, a, None, None)
        users = [("big sort", YEL, 1), ("hash join", PINK, 2.2), ("global temp tables", GREEN, 3.4), ("index build", CYAN, 4.6)]
        fill_ = 0
        for k, (nm, col, st) in enumerate(users):
            al = pr(lt, st, st + .4) * fo
            fill_ += .22 * pr(lt, st, st + 1)
            ct(d, 720 + k * 50, "• " + nm, SN(30), col, al)
        d.rectangle((300, 640 - 220 * fill_, 780, 640), fill=mix(RED, a * .5))
        ct(d, 420, "TEMP", SB(44), WHITE, a)
        ct(d, 930, f"{int(fill_ * 100 / .88)}% used", MB(40), RED if fill_ > .7 else YEL, pr(lt, 1, 1.4) * fo)
        card_list(d, 1000, [("full → ORA-01652 for whoever asks next", RED, 7.5)], lt, fo, 80, 31)
        caps = ["When work areas spill, they write to the temporary tablespace, built from temp files.",
                "Big sorts, hash joins, global temporary tables and index builds all share it.",
                "When it's full, the next session that needs space fails with ORA zero one six five two. Often not the one that caused it."]
        caption(d, caps[0 if lt < 3.4 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 6 DIAGNOSE
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Find the TEMP hog", SB(56), GREEN, a)
        code(d, 320, [("SELECT s.sid, s.username, u.sql_id,", CYAN), ("       u.blocks * 8192/1048576 mb", CYAN),
                      ("FROM   v$tempseg_usage u", CYAN), ("JOIN   v$session s", CYAN), ("  ON   s.saddr = u.session_addr", CYAN),
                      ("ORDER  BY mb DESC;", CYAN)], a, 28)
        rows = [("SID 412", "7h2kq9x…", "38 GB", RED), ("SID 118", "a91fz0c…", "1.2 GB", YEL), ("SID 77", "c3m8w1p…", "0.1 GB", GREEN)]
        for k, (sid, sq, mb, col) in enumerate(rows):
            y = 730 + k * 80; al = pr(lt, 3 + k * .5, 3.4 + k * .5) * fo
            d.rounded_rectangle((90, y, 990, y + 66), 12, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((120, y + 16), sid, font=MN(30), fill=mix(WHITE, al))
            d.text((400, y + 16), sq, font=MN(30), fill=mix(WHITE, al))
            d.text((780, y + 16), mb, font=SB(30), fill=mix(col, al))
        card_list(d, 990, [("history: ASH temp_space_allocated · V$SQL_WORKAREA", PURP, 7)], lt, fo, 80, 28)
        caps = ["While it's happening, join V dollar temp seg usage with V dollar session to see who holds TEMP, and with which SQL.",
                "Usually one statement holds most of it. Here, thirty eight gigabytes.",
                "For the past, ASH records temp space allocated per sample, and V dollar SQL workarea shows optimal, one-pass and multi-pass counts."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 7 FIXES
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Fix the cause, not the size", SB(52), YEL, a)
        fx = [("filter early", "fewer rows to sort or hash", GREEN), ("drop needless ORDER BY / DISTINCT", "they all sort", CYAN),
              ("check the join (video 29)", "a missing condition = huge result", PINK), ("LIMIT your BULK COLLECT", "video 31", PURP),
              ("then size TEMP & PGA", "for the real peak", YEL)]
        for k, (h, s_, col) in enumerate(fx):
            y = 320 + k * 140; al = pr(lt, .6 + k * 1.6, 1 + k * 1.6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 122), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.ellipse((95, y + 31, 155, y + 91), fill=mix(col, al)); ct(d, y + 41, str(k + 1), SB(34), BG, al, 125)
            d.text((180, y + 20), h, font=SB(32), fill=mix(col, al))
            d.text((180, y + 72), s_, font=SN(28), fill=mix(WHITE, al))
        caps = ["Adding TEMP space only moves the problem. First reduce what needs sorting: filter rows as early as possible.",
                "Remove sorts nobody needs, and check the join. A missing join condition creates a huge cartesian result.",
                "Limit your bulk collects. Then size TEMP and PGA for the real peak of your end of day."]
        caption(d, caps[0 if lt < 2.2 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("PGA", "→ private memory per process"), ("Work areas", "→ sorts, hash joins"),
                          ("Spill", "→ one-pass, multi-pass → TEMP"), ("ORA-01652", "→ TEMP full"),
                          ("Find it", "→ V$TEMPSEG_USAGE + SQL_ID")],
              "Every sort needs memory. Too little, and it spills. Too much spill, and TEMP runs out.", 440)
    else:
        cta(d, t - T[9], "ANALYTIC FUNCTIONS", "ROW_NUMBER, LAG, running totals", 64)
    return im

if __name__ == "__main__":
    preview(frame, T, "v32_sheet.png")

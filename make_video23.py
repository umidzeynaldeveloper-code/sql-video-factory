from vhelp import *
from make_video19 import code
from make_video14 import cyl
import random

T = T10; DUR = T[-1]

def file_icon(d, x, y, w, h, col, a, title, sub=None):
    f = 30
    d.polygon([(x, y), (x + w - f, y), (x + w, y + f), (x + w, y + h), (x, y + h)], fill=mix(CARD, a), outline=mix(col, a))
    d.line((x + w - f, y, x + w - f, y + f, x + w, y + f), fill=mix(col, a), width=3)
    ct(d, y + h / 2 - (34 if sub else 18), title, SB(30), col, a, x + w / 2)
    if sub: ct(d, y + h / 2 + 6, sub, SN(24), WHITE, a, x + w / 2)

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        code(d, 230, [("SELECT * FROM accounts;", YEL)], a, 40, 120, 960)
        ct(d, 420, "Where do these rows actually LIVE?", SB(46), WHITE, pr(lt, .8, 1.2) * fo)
        ab = pr(lt, 1.8, 2.2) * fo
        cyl(d, 290, 680, 340, 200, CYAN, ab, "DATAFILES", "the data")
        cyl(d, 790, 680, 340, 200, PINK, pr(lt, 2.4, 2.8) * fo, "LOG FILES", "the journal")
        ct(d, 880, "different files · different writers · different I/O", SN(34), YEL, pr(lt, 3.4, 3.8) * fo)
        caption(d, "Let's open the disk and see which files Oracle keeps, and who writes them.", pr(lt, 4, 4.4) * fo)

    # 1 STORAGE HIERARCHY
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Logical → physical", SB(56), WHITE, a)
        lv = [("TABLESPACE", "USERS", CYAN, .6, 70, 330, 1010, 1030),
              ("DATAFILE", "users01.dbf", YEL, 2, 110, 410, 970, 1000),
              ("SEGMENT", "table ACCOUNTS", GREEN, 4, 150, 490, 930, 970),
              ("EXTENT", "1 MB chunk", PINK, 6, 190, 570, 890, 940)]
        for nm, sub, col, st, x0, y0, x1, y1 in lv:
            al = pr(lt, st, st + .4) * fo
            d.rounded_rectangle((x0, y0, x1, y1), 20, outline=mix(col, al), width=4)
            d.text((x0 + 24, y0 + 16), nm, font=SB(30), fill=mix(col, al))
            d.text((x0 + 24 + d.textlength(nm, font=SB(30)) + 20, y0 + 20), sub, font=SN(26), fill=mix(WHITE, al))
        ab = pr(lt, 8, 8.4) * fo
        for k in range(16):
            r, c = divmod(k, 8); x = 220 + c * 82; y = 660 + r * 120
            d.rounded_rectangle((x, y, x + 70, y + 100), 8, fill=mix(CYAN if k < 11 else OFFB, ab * .85))
        ct(d, 905, "BLOCKS · 8 KB each", SB(30), CYAN, ab)
        caps = ["A tablespace is a logical container, and it's stored in one or more datafiles on disk.",
                "Inside, each table or index is a segment, made of extents: contiguous chunks of space.",
                "And extents are made of blocks, usually eight kilobytes. A block is the unit Oracle reads and writes."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 2 FILE TYPES
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The files of a database", SB(54), WHITE, a)
        fl = [("DATAFILES", "tables, indexes, undo", CYAN, .6), ("CONTROL FILE", "the map", YEL, 2),
              ("ONLINE REDO", "current journal", PINK, 3.5), ("ARCHIVED LOGS", "old journal copies", PURP, 5),
              ("TEMP FILES", "sorts, hash joins", GREEN, 6.5), ("SPFILE", "parameters", DIM, 8)]
        for k, (nm, sub, col, st) in enumerate(fl):
            r, c = divmod(k, 2); x = 90 + c * 470; y = 320 + r * 230
            file_icon(d, x, y, 430, 200, col, pr(lt, st, st + .4) * fo, nm, sub)
        caps = ["Datafiles hold your tables and indexes, and also the undo tablespace.",
                "The control file is the map of the database. Online redo logs are the current journal; archived logs are old copies.",
                "Temp files hold sorts and hash joins that don't fit in memory, and the spfile holds the parameters."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 3 WHO WRITES WHAT
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Who writes which file?", SB(54), WHITE, a)
        d.rounded_rectangle((70, 300, 1010, 470), 24, outline=mix(DIM, a * .7), width=3)
        d.text((100, 310), "SGA", font=SB(28), fill=mix(DIM, a))
        glow_box(d, (110, 350, 500, 450), CYAN, a, "buffer cache", None, 32)
        glow_box(d, (580, 350, 970, 450), PINK, a, "log buffer", None, 32)
        procs = [("DBWn", 305, 580, CYAN, 1), ("LGWR", 775, 580, PINK, 3), ("CKPT", 305, 880, YEL, 5.5), ("ARCn", 775, 880, PURP, 7.5)]
        for nm, x, y, col, st in procs:
            chip(d, x, y, nm, col, pr(lt, st, st + .4) * fo, 34, BG)
        ad = pr(lt, 1.2, 1.6) * fo; ar = pr(lt, 3.2, 3.6) * fo
        file_icon(d, 110, 680, 390, 130, CYAN, ad, "DATAFILES")
        file_icon(d, 580, 680, 390, 130, PINK, ar, "ONLINE REDO")
        if lt > 1.4: flow(d, [(305, 450), (305, 555), (305, 680)], CYAN, a, t, pr(lt, 1.4, 2.2))
        if lt > 3.4: flow(d, [(775, 450), (775, 555), (775, 680)], PINK, a, t, pr(lt, 3.4, 4.2))
        ac = pr(lt, 5.5, 5.9) * fo
        file_icon(d, 110, 960, 390, 120, YEL, ac, "CONTROL FILE", "+ datafile headers")
        if lt > 5.8: flow(d, [(305, 905), (305, 960)], YEL, a, t, pr(lt, 5.8, 6.3))
        aa = pr(lt, 7.5, 7.9) * fo
        file_icon(d, 580, 960, 390, 120, PURP, aa, "ARCHIVED LOGS")
        if lt > 7.8: flow(d, [(775, 810), (775, 855)], PURP, a, t, pr(lt, 7.8, 8.4))
        caps = ["The database writer, DBWn, writes dirty blocks from the buffer cache to the datafiles.",
                "The log writer, LGWR, writes the log buffer to the online redo logs.",
                "The checkpoint process records progress in the control file and datafile headers, and ARCn copies full logs to archives."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 4 I/O PATTERN GRAPHS
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Two very different I/O patterns", SB(48), WHITE, a)
        for gi, (y0, col, nm, st) in enumerate([(320, CYAN, "DATAFILES (DBWn): random", .6), (720, PINK, "REDO (LGWR): sequential", 4)]):
            al = pr(lt, st, st + .4) * fo
            d.text((110, y0), nm, font=SB(32), fill=mix(col, al))
            gx0, gy0, gx1, gy1 = 110, y0 + 60, 970, y0 + 320
            d.rectangle((gx0, gy0, gx1, gy1), outline=mix(DIM, al * .6), width=2)
            d.text((gx0 + 10, gy1 + 8), "time →", font=SN(24), fill=mix(DIM, al))
            d.text((gx0 + 10, gy0 + 6), "block address", font=SN(24), fill=mix(DIM, al))
            rng = random.Random(gi)
            n = int(60 * pr(lt, st, st + 3))
            for k in range(n):
                x = gx0 + 20 + k * (gx1 - gx0 - 40) / 60
                if gi == 0: y = gy0 + 20 + rng.random() * (gy1 - gy0 - 40)
                else: y = gy1 - 20 - k * (gy1 - gy0 - 40) / 60
                d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=mix(col, al))
        ab = pr(lt, 8, 8.4) * fo
        ct(d, 1100, "redo = small, fast disks · never on RAID-5", SB(32), YEL, ab)
        caps = ["Plot block address against time. DBWn jumps all over the datafiles: random I/O, in big batches.",
                "LGWR only appends to the end of the log: perfectly sequential, small, and latency critical, because commits wait for it.",
                "So put redo on fast, low-latency storage, separate from datafiles. Never on slow parity RAID."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 5 CHECKPOINT GRAPH
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Checkpoint: where they meet", SB(52), YEL, a)
        gx0, gy0, gx1, gy1 = 110, 330, 970, 700
        d.rectangle((gx0, gy0, gx1, gy1), outline=mix(DIM, a * .6), width=2)
        d.text((gx0 + 10, gy0 + 6), "dirty blocks in memory", font=SN(26), fill=mix(DIM, a))
        p = pr(lt, .8, 6)
        pts = []
        for k in range(int(100 * p) + 1):
            ph = (k % 33) / 33
            v = ph * 0.85
            pts.append((gx0 + k * (gx1 - gx0) / 100, gy1 - 20 - v * (gy1 - gy0 - 60)))
        if len(pts) > 1: d.line(pts, fill=mix(CYAN, a), width=6)
        for k in (33, 66, 99):
            if k <= 100 * p:
                x = gx0 + k * (gx1 - gx0) / 100
                d.line((x, gy0 + 40, x, gy1), fill=mix(YEL, a), width=3)
                ct(d, gy1 + 10, "CKPT", SB(26), YEL, a, x)
        ab = pr(lt, 6.5, 6.9) * fo
        glow_box(d, (110, 790, 970, 920), GREEN, ab, "after a checkpoint: datafiles are up to date", "to that SCN", 34, 28)
        card_list(d, 960, [("recovery replays redo only FROM the last checkpoint", PINK, 8.5)], lt, fo, 80, 31)
        caps = ["Dirty blocks pile up in memory. At a checkpoint, DBWn writes them, and the datafiles catch up with the redo.",
                "The checkpoint SCN is stored in the control file and in every datafile header.",
                "So after a crash, Oracle only needs the redo after the last checkpoint. Frequent checkpoints mean faster recovery, but more writes."]
        caption(d, caps[0 if lt < 6.5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 6 CONTROL FILE
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The control file = the map", SB(52), YEL, a)
        file_icon(d, 250, 310, 580, 520, YEL, a, "", None)
        items = [("DB name, DBID", .8), ("datafile names + status", 1.6), ("redo log groups + members", 2.4),
                 ("current log sequence", 3.2), ("checkpoint SCN", 4), ("RMAN backup records", 4.8)]
        for k, (tx, st) in enumerate(items):
            al = pr(lt, st, st + .4) * fo
            d.text((290, 350 + k * 75), "• " + tx, font=SN(32), fill=mix(WHITE, al))
        ab = pr(lt, 6.5, 6.9) * fo
        glow_box(d, (110, 880, 970, 1000), RED, ab, "lose it → database won't mount", None, 36)
        card_list(d, 1040, [("multiplex it: 2–3 copies on different disks", GREEN, 8.5)], lt, fo, 80, 32)
        caps = ["The control file is small, but it's the map: which datafiles and redo logs exist, and how far the database has progressed.",
                "Without it, the instance can't mount the database.",
                "So always keep two or three copies on different disks. Oracle writes them all, every time."]
        caption(d, caps[0 if lt < 6.5 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 7 VIEWS
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "See it yourself", SB(58), GREEN, a)
        code(d, 320, [("DBA_DATA_FILES    -- datafiles, size", CYAN), ("V$LOG / V$LOGFILE -- redo groups", PINK),
                      ("V$CONTROLFILE     -- control copies", YEL), ("V$ARCHIVED_LOG    -- archives", PURP),
                      ("V$TEMPFILE        -- temp files", GREEN)], a, 30)
        card_list(d, 760, [("datafile full? → autoextend / add file", CYAN, 4),
                           ("archive dest full? → database hangs!", RED, 6),
                           ("redo mirrored? → 2 members per group", PINK, 8)], lt, fo, 80, 31)
        caps = ["Every file has a view. DBA data files for datafiles, V dollar log and log file for redo, V dollar control file for the map.",
                "Watch space: a full datafile stops inserts, and a full archive destination stops the whole database.",
                "And check that every redo group and the control file are mirrored."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Datafiles", "→ blocks, random I/O, DBWn"), ("Redo logs", "→ journal, sequential, LGWR"),
                          ("Checkpoint", "→ datafiles catch up"), ("Control file", "→ the map, multiplex it"),
                          ("Archives", "→ ARCn, don't let it fill")],
              "Datafiles hold the data, log files hold the story of every change.", 450)
    else:
        cta(d, t - T[9], "LATCHES & MUTEXES", "tiny locks, huge waits", 64)
    return im

if __name__ == "__main__":
    preview(frame, T, "v23_sheet.png")

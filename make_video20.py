from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]
NB = 24  # blocks in segment

def blocks(d, y, full, a, hwm, cols=8, scan=None, lbl=True):
    """full: list of fill fractions 0..1 per block; hwm: block index of high water mark"""
    bw, gap = 110, 12; x0 = (W - (cols * bw + (cols - 1) * gap)) / 2
    for k, f in enumerate(full):
        r, c = divmod(k, cols); x = x0 + c * (bw + gap); yy = y + r * (bw + 44)
        below = k < hwm
        d.rounded_rectangle((x, yy, x + bw, yy + bw), 12, outline=mix(DIM if below else (40, 46, 60), a), width=3,
                            fill=mix(CARD, a))
        if f > 0:
            h = (bw - 16) * f
            d.rounded_rectangle((x + 8, yy + bw - 8 - h, x + bw - 8, yy + bw - 8), 8, fill=mix(CYAN, a))
        if scan is not None and k == scan:
            d.rounded_rectangle((x - 4, yy - 4, x + bw + 4, yy + bw + 4), 14, outline=mix(YEL, a), width=6)
    # HWM marker
    if hwm is not None and lbl:
        r, c = divmod(min(hwm, len(full)), cols)
        if c == 0 and r > 0: r, c = r - 1, cols
        x = x0 + c * (bw + gap) - gap / 2; yy = y + r * (bw + 44)
        d.line((x, yy - 18, x, yy + bw + 18), fill=mix(RED, a), width=8)
        chip(d, x, yy - 22, "HWM", RED, a, 24, WHITE)

def fills(n_full, empty=(), part=None):
    out = []
    for k in range(NB):
        if k >= n_full: out.append(0)
        elif k in empty: out.append(0)
        else: out.append(1)
    if part:
        for k, v in part.items(): out[k] = v
    return out

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "DELETE 90% of the rows…", SB(56), WHITE, a)
        p = pr(lt, .8, 2.4)
        bar(d, 110, 380, 970, 40, 1 - .9 * p, CYAN, a, "rows", f"{int(100 - 90 * p)} M")
        bar(d, 110, 520, 970, 40, 1, PINK, pr(lt, 2.4, 2.8) * fo, "table size", "10 GB")
        bar(d, 110, 660, 970, 40, 1, RED, pr(lt, 3, 3.4) * fo, "full scan time", "same")
        ct(d, 800, "…and nothing got smaller?!", SB(48), YEL, pr(lt, 3.6, 4) * fo)
        caption(d, "Meet the high water mark: why DELETE doesn't give space back.", pr(lt, 4, 4.4) * fo)

    # 1 BLOCKS & HWM
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "A table = blocks + a HIGH WATER MARK", SB(46), WHITE, a)
        n = int(min(18, max(0, (lt - 1) * 3)))
        blocks(d, 360, fills(n), a, max(n, 1))
        card_list(d, 830, [("inserts fill blocks left → right", CYAN, 3),
                           ("HWM = the highest block EVER used", RED, 6),
                           ("full scan reads EVERY block below the HWM", YEL, 8.5)], lt, fo, 80, 32)
        caps = ["A table segment is a set of blocks. Inserts fill them, one after another.",
                "The high water mark marks the highest block that was ever used.",
                "A full table scan reads every block below it. Remember that."]
        caption(d, caps[0 if lt < 6 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 2 DELETE
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "DELETE: rows go, HWM stays", SB(52), PINK, a)
        nd = int(min(15, max(0, (lt - 1) * 4)))
        gone = set([k for k in range(18) if k % 6 != 0][:nd])
        sc_ = int((lt - 5.5) * 3) if 5.5 < lt < 11.5 else None
        blocks(d, 360, fills(18, gone), a, 18, scan=sc_ if sc_ is not None and sc_ < 18 else None)
        if lt > 5.5:
            rd = min(18, max(0, int((lt - 5.5) * 3)))
            ct(d, 830, f"full scan: {rd} blocks read · {max(0, rd - (rd + 5) // 6)} empty", SB(36), YEL, pr(lt, 5.5, 5.9) * fo)
        caps = ["DELETE removes rows. The blocks become empty, but they still belong to the table.",
                "And the high water mark doesn't move.",
                "So a full scan still reads all those empty blocks. Same I/O, a fraction of the data."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 3 TRUNCATE vs DELETE
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "TRUNCATE resets the HWM", SB(54), GREEN, a)
        done = lt > 2
        blocks(d, 360, fills(0 if done else 18), a, 1 if done else 18)
        if 1.5 < lt < 2.5:
            ab = 1 - abs(lt - 2) * 2
            d.rectangle((60, 330, 1020, 790), fill=mix(GREEN, ab * .25 * a))
        ad = pr(lt, 4, 4.4) * fo; at = pr(lt, 5, 5.4) * fo
        glow_box(d, (60, 820, 520, 920), PINK, ad, "DELETE", None, 40)
        glow_box(d, (560, 820, 1020, 920), GREEN, at, "TRUNCATE", None, 40)
        rows = [("row by row", "deallocates blocks"), ("undo + redo per row", "minimal undo"),
                ("HWM stays", "HWM reset ✓"), ("can ROLLBACK", "DDL: no rollback")]
        for k, (l, r) in enumerate(rows):
            y = 950 + k * 80; al = pr(lt, 5.8 + k * .8, 6.2 + k * .8) * fo
            d.rounded_rectangle((60, y, 520, y + 66), 12, fill=mix((70, 26, 50), al))
            d.rounded_rectangle((560, y, 1020, y + 66), 12, fill=mix((20, 50, 36), al))
            ct(d, y + 16, l, SB(30), WHITE, al, 290); ct(d, y + 16, r, SB(30), WHITE, al, 790)
        caps = ["TRUNCATE removes all rows at once, and resets the high water mark to the start.",
                "DELETE works row by row, with undo and redo for every row, and can be rolled back.",
                "TRUNCATE is DDL: fast, minimal undo, no rollback. Great for staging tables, not for keeping some rows."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 4 SHRINK SPACE
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "SHRINK SPACE: compact + lower HWM", SB(46), YEL, a)
        code(d, 300, [("ALTER TABLE t ENABLE ROW MOVEMENT;", CYAN), ("ALTER TABLE t SHRINK SPACE CASCADE;", YEL)], a, 30)
        keep = [0, 6, 12]
        p = pr(lt, 3, 7)
        fl = [0] * NB
        n_live = len(keep)
        for j, k in enumerate(keep):
            pos = round(lerp(k, j, p))
            fl[pos] = 1
        hwm = 18 if lt < 8 else max(n_live, round(lerp(18, n_live, pr(lt, 8, 9.5))))
        blocks(d, 500, fl, a, hwm)
        card_list(d, 960, [("phase 1 COMPACT: rows move toward the start", CYAN, 3),
                           ("phase 2: HWM drops, space released", GREEN, 8),
                           ("needs ROW MOVEMENT + ASSM · ROWIDs change", RED, 10)], lt, fo, 80, 32)
        caps = ["SHRINK SPACE moves rows from the end of the segment into free space at the start.",
                "Then it lowers the high water mark and gives the empty blocks back. Online, while users keep working.",
                "It needs row movement and automatic segment space management, and rowids change."]
        caption(d, caps[0 if lt < 8 else 1 if lt < 10 else 2], pr(lt, .6, 1) * fo)

    # 5 MOVE
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "ALTER TABLE … MOVE", SB(56), CYAN, a)
        code(d, 300, [("ALTER TABLE t MOVE ONLINE;", YEL)], a, 32)
        glow_box(d, (60, 430, 480, 700), PINK, a, "OLD segment", "10 GB, 90% empty", 32, 28)
        an = pr(lt, 1.5, 2) * fo
        glow_box(d, (600, 430, 1020, 700), GREEN, an, "NEW segment", "1 GB, packed", 32, 28)
        if lt > 2: flow(d, [(480, 565), (600, 565)], GREEN, a, t, pr(lt, 2, 3))
        ai = pr(lt, 4.5, 4.9) * fo
        glow_box(d, (190, 780, 890, 900), RED, ai, "indexes → UNUSABLE", "unless ONLINE / UPDATE INDEXES", 34, 28)
        card_list(d, 960, [("needs free space for a full copy", YEL, 7.5),
                           ("then: rebuild indexes, gather stats", CYAN, 8.5)], lt, fo, 80, 32)
        caps = ["MOVE copies the table into a brand new, packed segment, and drops the old one.",
                "Careful: rowids change, so plain MOVE leaves indexes unusable. Use ONLINE or UPDATE INDEXES.",
                "It needs room for a full copy, and afterwards gather fresh statistics."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 6 PREVENTION: PARTITIONS
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Best fix: don't fragment at all", SB(50), GREEN, a)
        months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN"]
        dropped = lt > 4.5
        for k, m in enumerate(months):
            x = 80 + k * 155; al = a
            if k == 0 and dropped: al = a * (1 - pr(lt, 4.5, 5.5))
            glow_box(d, (x, 340, x + 140, 520), CYAN if k else PINK, al, m, None, 32)
        code(d, 580, [("DELETE FROM txn WHERE dt < :d;", PINK)], pr(lt, 1.5, 1.9) * fo, 30)
        ct(d, 680, "↓ instead ↓", SB(32), DIM, pr(lt, 3, 3.4) * fo)
        code(d, 730, [("ALTER TABLE txn DROP PARTITION p_jan;", GREEN)], pr(lt, 3.4, 3.8) * fo, 30)
        card_list(d, 880, [("instant, no row-by-row undo/redo, no holes", GREEN, 6),
                           ("indexes: shrink/rebuild only with real evidence", YEL, 8.5)], lt, fo, 80, 32)
        caps = ["In banking, old transactions get purged every month. With DELETE, that leaves holes everywhere.",
                "Partition by date instead, and drop or truncate the old partition. Instant, and no fragmentation.",
                "Indexes can fragment too, but only shrink or rebuild them when you have real evidence."]
        caption(d, caps[0 if lt < 3.4 else 1 if lt < 8.5 else 2], pr(lt, .6, 1) * fo)

    # 7 DETECT
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How to spot it", SB(58), WHITE, a)
        bar(d, 110, 360, 970, 44, 1, PINK, pr(lt, .6, 1) * fo, "allocated (DBA_SEGMENTS)", "10 GB")
        bar(d, 110, 500, 970, 44, pr(lt, 1.6, 2.6) * .1, CYAN, pr(lt, 1.4, 1.8) * fo, "real data (rows × avg_row_len)", "1 GB")
        ct(d, 620, "big gap → candidate", SB(38), YEL, pr(lt, 3, 3.4) * fo)
        card_list(d, 720, [("DBMS_SPACE.SPACE_USAGE → block fullness", CYAN, 4.5),
                           ("Segment Advisor → recommends SHRINK", CYAN, 6),
                           ("slow full scans on a mostly empty table", YEL, 7.5)], lt, fo, 80, 32)
        caps = ["Compare the allocated size in DBA segments with the real data: number of rows times average row length.",
                "DBMS space shows how full the blocks are, and the Segment Advisor recommends what to shrink.",
                "Big gap plus slow full scans? That table is a shrink candidate."]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("DELETE", "→ rows go, HWM stays"), ("TRUNCATE", "→ HWM reset, no rollback"),
                          ("SHRINK SPACE", "→ compact online"), ("MOVE", "→ copy, check indexes"),
                          ("PARTITION", "→ drop, don't delete")],
              "Full scans read up to the high water mark, not up to your data.", 490)
    else:
        cta(d, t - T[9], "AWR IN 3 MINUTES", "read your database's health report")
    return im

if __name__ == "__main__":
    preview(frame, T, "v20_sheet.png")

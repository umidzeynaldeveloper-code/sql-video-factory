from vhelp import *
from make_video14 import cyl
import sys

T = T10; DUR = T[-1]

SGA = (60, 300, 1020, 640)

def sga(d, a, lbl=True):
    d.rounded_rectangle(SGA, 28, outline=mix(DIM, a * .7), width=3)
    if lbl: d.text((90, 312), "MEMORY (SGA)", font=SB(28), fill=mix(DIM, a))

def disk_row(d, a, y=820):
    d.line((60, y - 60, 1020, y - 60), fill=mix(DIM, a * .5), width=2)
    d.text((90, y - 52), "DISK", font=SB(28), fill=mix(DIM, a))
    cyl(d, 260, y + 90, 300, 170, CYAN, a, "DATAFILES", "tables · undo")
    cyl(d, 800, y + 90, 300, 170, PINK, a, "REDO LOGS", "online")

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 240, "UPDATE 1 000 000 rows", SB(56), WHITE, a)
        bar(d, 110, 400, 970, 40, pr(lt, .5, 2.5), YEL, pr(lt, .4, .7) * fo, "UPDATE", "30 s")
        bar(d, 110, 540, 970, 40, pr(lt, 2.8, 2.9) * .01, GREEN, pr(lt, 2.6, 2.9) * fo, "COMMIT", "0.01 s ⚡")
        ct(d, 680, "Why is COMMIT so fast?", SB(52), YEL, pr(lt, 3.2, 3.6) * fo)
        ct(d, 760, "…and how does a power cut lose nothing?", SB(40), WHITE, pr(lt, 3.8, 4.2) * fo)
        caption(d, "The answer is REDO, Oracle's write-ahead journal. Let's look inside.", pr(lt, 4, 4.4) * fo)

    # 1 UPDATE IN MEMORY
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "An UPDATE lives in MEMORY", SB(54), WHITE, a)
        sga(d, a)
        glow_box(d, (90, 370, 380, 610), CYAN, pr(lt, .6, 1) * fo, "BUFFER", "CACHE", 34, 34)
        if lt > 2:
            ad = pr(lt, 2, 2.4) * fo
            d.rounded_rectangle((140, 540, 330, 590), 10, fill=mix(YEL, ad))
            ct(d, 548, "dirty block", SB(26), BG, ad, 235)
        glow_box(d, (410, 370, 700, 610), PURP, pr(lt, 3.5, 3.9) * fo, "UNDO", "old value", 34, 30)
        glow_box(d, (730, 370, 1000, 610), PINK, pr(lt, 5.5, 5.9) * fo, "REDO LOG", "BUFFER", 32, 32)
        disk_row(d, a * .6)
        caps = ["The UPDATE changes the block in the buffer cache, in memory. Nothing is written to the table on disk yet.",
                "The old value is saved in UNDO, for rollback and for readers.",
                "And a tiny REDO record describing the change goes into the redo log buffer."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 2 UNDO vs REDO
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "UNDO vs REDO", SB(64), WHITE, a)
        au = pr(lt, .6, 1) * fo; ar = pr(lt, 1.2, 1.6) * fo
        glow_box(d, (60, 320, 520, 420), PURP, au, "UNDO", None, 46)
        glow_box(d, (560, 320, 1020, 420), PINK, ar, "REDO", None, 46)
        rows = [("stores", "OLD value", "the CHANGE"), ("goal", "go BACK", "go FORWARD"),
                ("used for", "rollback, readers", "crash recovery"), ("lives in", "undo tablespace", "redo log files"),
                ("example", "balance was 1000", "set balance = 500")]
        for k, (lab, u, r) in enumerate(rows):
            y = 460 + k * 120; al = pr(lt, 2 + k * 1.3, 2.4 + k * 1.3) * fo
            ct(d, y, lab, SN(28), DIM, al)
            d.rounded_rectangle((60, y + 34, 520, y + 100), 14, fill=mix((40, 26, 66), al))
            d.rounded_rectangle((560, y + 34, 1020, y + 100), 14, fill=mix((70, 26, 50), al))
            ct(d, y + 46, u, SB(32), WHITE, al, 290); ct(d, y + 46, r, SB(32), WHITE, al, 790)
        caps = ["Two journals, opposite directions.",
                "UNDO remembers how things WERE, so Oracle can go back: rollback and consistent reads.",
                "REDO remembers what CHANGED, so Oracle can replay it after a crash.",
                "Fun fact: even writing UNDO generates REDO, so undo itself survives a crash."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 5 else 2 if lt < 9 else 3], pr(lt, .6, 1) * fo)

    # 3 COMMIT
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "COMMIT = write the journal", SB(54), GREEN, a)
        sga(d, a)
        glow_box(d, (90, 370, 380, 610), CYAN, a, "BUFFER", "CACHE", 34, 34)
        d.rounded_rectangle((140, 540, 330, 590), 10, fill=mix(YEL, a)); ct(d, 548, "dirty block", SB(26), BG, a, 235)
        glow_box(d, (730, 370, 1000, 610), PINK, a, "REDO LOG", "BUFFER", 32, 32)
        disk_row(d, a)
        chip(d, 540, 700, "LGWR", PINK, pr(lt, 1.2, 1.6) * fo, 34, BG)
        if lt > 1.6: flow(d, [(865, 610), (865, 690), (800, 690), (800, 830)], PINK, a, t, pr(lt, 1.6, 2.6), width=8)
        ok = pr(lt, 3.4, 3.8) * fo
        glow_box(d, (240, 1130, 840, 1240), GREEN, ok, "COMMIT complete ✓", None, 40)
        ab = pr(lt, 6, 6.4) * fo
        ct(d, 1280, "datafiles: not touched yet!", SB(36), YEL, ab)
        caps = ["On COMMIT, the log writer, LGWR, writes the redo buffer to the online redo log on disk.",
                "It's a small, sequential write. As soon as it's on disk, your COMMIT returns.",
                "The changed table block is still only in memory. And that's perfectly safe."]
        caption(d, caps[0 if lt < 3.4 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 4 DBWR LATER
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Data blocks? Later. Lazily.", SB(54), CYAN, a)
        sga(d, a)
        blocks = 10
        for k in range(blocks):
            x = 100 + (k % 5) * 180; y = 380 + (k // 5) * 110
            written = lt > 4 + k * .25
            d.rounded_rectangle((x, y, x + 160, y + 80), 12, fill=mix(GREEN if written else YEL, a * (.5 if written else 1)))
            ct(d, y + 22, "clean" if written else "dirty", SB(26), BG, a, x + 80)
        disk_row(d, a)
        chip(d, 260, 700, "DBWR", CYAN, pr(lt, 2.5, 2.9) * fo, 34, BG)
        if lt > 3: flow(d, [(260, 640), (260, 820)], CYAN, a, t, pr(lt, 3, 3.8), width=8)
        ct(d, 1130, "random I/O · big batches · checkpoint", SB(34), WHITE, pr(lt, 6, 6.4) * fo)
        caps = ["Dirty blocks are written to the datafiles later, by the database writer, DBWR.",
                "It writes in big batches, at checkpoints, completely independent of your COMMIT.",
                "Fast sequential redo on commit, slow random datafile writes in the background. That's the trick."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 5 CRASH RECOVERY
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        crashed = 1.5 < lt < 3.5
        ct(d, 230, "Power cut! ⚡" if lt < 3.5 else "Restart: instance recovery", SB(56), RED if lt < 3.5 else GREEN, a)
        if lt < 1.5:
            sga(d, a); glow_box(d, (90, 370, 1000, 610), YEL, a, "dirty blocks + committed changes", None, 34)
        elif crashed:
            ab = (int(lt * 8) % 2) * a
            d.rounded_rectangle(SGA, 28, fill=mix((40, 10, 16), a), outline=mix(RED, ab), width=6)
            ct(d, 440, "MEMORY LOST", SB(56), RED, a)
        disk_row(d, a)
        if lt > 3.5:
            p1 = pr(lt, 4, 6.5)
            glow_box(d, (60, 330, 520, 470), PINK, pr(lt, 3.8, 4.2) * fo, "1. ROLL FORWARD", "replay REDO", 32, 28)
            flow(d, [(800, 820), (800, 760), (290, 760), (290, 820)], PINK, a, t, p1)
            glow_box(d, (560, 330, 1020, 470), PURP, pr(lt, 7, 7.4) * fo, "2. ROLL BACK", "uncommitted via UNDO", 32, 26)
            ag = pr(lt, 9.5, 9.9) * fo
            glow_box(d, (190, 520, 890, 620), GREEN, ag, "all COMMITs safe ✓", None, 40)
        caps = ["The power goes out. Everything in memory, including dirty blocks, is gone.",
                "On restart, Oracle replays the redo log: every change since the last checkpoint is re-applied.",
                "Then it uses undo to roll back anything that was never committed. Nothing committed is lost."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 6 LOG GROUPS + ARCHIVE
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Redo logs go in circles", SB(56), PINK, a)
        cx, cy, R = 540, 620, 230
        cur = int(max(0, lt - 1) / 2.5) % 3
        for k in range(3):
            an = math.radians(-90 + k * 120)
            x, y = cx + R * math.cos(an), cy + R * math.sin(an)
            col = PINK if k == cur else OFFB
            glow_box(d, (x - 130, y - 70, x + 130, y + 70), col, a, f"GROUP {k + 1}", "CURRENT" if k == cur else "full / free", 32, 26)
        chip(d, cx, cy, "LGWR", PINK, a, 34, BG)
        aa = pr(lt, 6, 6.4) * fo
        cyl(d, 540, 1060, 420, 150, YEL, aa, "ARCHIVED LOGS", "copied by ARCn")
        if lt > 6: flow(d, [(540, 920), (540, 985)], YEL, a, t, pr(lt, 6, 6.6))
        caps = ["There are several online redo log groups. LGWR fills one, then switches to the next.",
                "When it comes back around, the old content is overwritten.",
                "In ARCHIVELOG mode, each full log is first copied away: that's your backup, point-in-time recovery, and Data Guard."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 7 COMMIT FREQUENCY
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "How often should you COMMIT?", SB(54), WHITE, a)
        ct(d, 310, "1 000 000 row batch (example)", SN(32), DIM, a)
        bar(d, 110, 450, 970, 44, pr(lt, .8, 4), RED, pr(lt, .6, 1) * fo, "COMMIT every row", "1 000 000 waits")
        bar(d, 110, 600, 970, 44, pr(lt, 2, 2.6) * .12, GREEN, pr(lt, 1.8, 2.2) * fo, "COMMIT every 10 000 rows", "100 waits ✓")
        bar(d, 110, 750, 970, 44, pr(lt, 3.5, 5) * .7, YEL, pr(lt, 3.3, 3.7) * fo, "never COMMIT", "huge undo, long locks")
        card_list(d, 900, [("✗ every COMMIT waits for a disk write: log file sync", RED, 5.5),
                           ("✓ commit by logical unit of work / sensible batches", GREEN, 7)], lt, fo, 80, 32)
        caps = ["Each COMMIT waits for LGWR to write to disk. Commit every row, and you wait a million times.",
                "Never committing a huge batch is bad too: undo grows and locks are held for hours.",
                "Commit at the end of a logical unit of work, or in sensible batches."]
        caption(d, caps[0 if lt < 3.3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("UPDATE", "→ changes memory only"), ("UNDO", "→ old value, go back"),
                          ("REDO", "→ the change, go forward"), ("COMMIT", "→ LGWR writes redo"),
                          ("Crash", "→ replay redo, undo the rest")],
              "Write the journal first, the data later. That's how Oracle is both fast and safe.")
    else:
        cta(d, t - T[9], "RESULT CACHE", "answers straight from memory")
    return im

if __name__ == "__main__":
    preview(frame, T, "v18_sheet.png")

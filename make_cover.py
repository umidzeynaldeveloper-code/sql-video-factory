"""Eye-catching 1080x1920 covers for Reels/Shorts. Key content kept inside the centre 1080x1440 (Instagram 3:4 grid crop)."""
import sys
from common import *
from PIL import Image, ImageDraw

COVERS = {
    1: ("ZEROS &\nONES", "What the computer really sees", CYAN),
    2: ("UTF-8\nBYTES", "Why 'ə' takes 2 bytes", PINK),
    3: ("NULL", "Not zero. Not empty.", YEL),
    4: ("COUNT(*)\nvs COUNT(col)", "They don't return the same!", GREEN),
    5: ("INDEX", "From full scan to 3 reads", CYAN),
    6: ("EXPLAIN\nPLAN", "See what Oracle really does", YEL),
    7: ("JOINS", "Nested loops · Hash · Merge", PURP),
    8: ("DEADLOCK", "Two transfers, one freeze", RED),
    9: ("BIND\nVARIABLES", "Same query, 10 000 times", GREEN),
    10: ("UNDO", "How Oracle remembers the past", PURP),
    11: ("FLASHBACK", "Undo a DELETE without backup", CYAN),
    12: ("PARTITIONING", "2 billion rows, read 1 month", YEL),
    13: ("PARALLEL\nQUERY", "10 GB report, 8 workers", PINK),
    14: ("MATERIALIZED\nVIEWS", "Dashboard in 0.1 s", GREEN),
    15: ("OPTIMIZER\nSTATISTICS", "Fast yesterday, slow today", CYAN),
    16: ("BIND\nPEEKING", "One SQL, two users", PINK),
    17: ("SQL PLAN\nBASELINES", "Stop plans from flipping", YEL),
    18: ("REDO &\nCOMMIT", "Why COMMIT is so fast", GREEN),
    19: ("RESULT\nCACHE", "Answers straight from memory", CYAN),
    20: ("HIGH WATER\nMARK", "DELETE didn't shrink it?", RED),
    21: ("AWR IN\n3 MINUTES", "Yesterday 14:00 it was slow", YEL),
    22: ("UNDO\nvs REDO", "Two journals, two directions", PURP),
    23: ("DATAFILES\nvs LOG FILES", "What's really on disk", CYAN),
    24: ("LATCHES &\nMUTEXES", "CPU 100%… nothing gets done", PINK),
    25: ("LOCKS &\nENQUEUES", "Who is blocking my UPDATE?", PURP),
    26: ("HARD\nPARSE", "Why literals kill your CPU", RED),
    27: ("BUFFER\nCACHE", "2nd run = 40× faster", CYAN),
    28: ("WHY ORACLE\nIGNORES\nYOUR INDEX", "B-tree deep dive", GREEN),
    29: ("READ AN\nEXECUTION\nPLAN", "Hint: NOT from the top", YEL),
    30: ("SQL\nHINTS", "Last resort, not first fix", PINK),
    31: ("BULK COLLECT\n& FORALL", "10 min → 20 seconds", GREEN),
    32: ("ORA-01652", "PGA, sorts & TEMP at 3 AM", RED),
    33: ("ANALYTIC\nFUNCTIONS", "Top-N · LAG · running totals", CYAN),
    34: ("MERGE", "Insert or update in ONE go", YEL),
    35: ("WHEN OTHERS\nTHEN NULL", "The most expensive line", RED),
}

def cover(n, out):
    title, sub, col = COVERS[n]
    im = rain.crop((0, 0, W, H)).copy(); d = ImageDraw.Draw(im)
    # darken + coloured glow
    ov = Image.new("RGB", (W, H), BG); im = Image.blend(im, ov, .55); d = ImageDraw.Draw(im)
    for r in range(520, 0, -20):
        a = .10 * (1 - r / 520)
        d.ellipse((540 - r, 900 - r, 540 + r, 900 + r), fill=mix(col, a))
    # giant ghost number
    ct(d, 330, str(n), SB(560), mix(col, .18), 1)
    # top chip
    d.rounded_rectangle((300, 300, 780, 390), 45, fill=col)
    ct(d, 318, f"ORACLE  ·  #{n}", SB(48), BG)
    # title
    lines = title.split("\n")
    L = max(len(l) for l in lines); fs = 150 if L <= 7 else 124 if L <= 9 else 104 if L <= 11 else 92
    y = 900 - len(lines) * (fs + 20) / 2
    for l in lines:
        ct(d, y + 6, l, SB(fs), (0, 0, 0))
        ct(d, y, l, SB(fs), WHITE); y += fs + 20
    # underline
    d.rounded_rectangle((340, y + 20, 740, y + 34), 7, fill=col)
    # subtitle
    ct(d, y + 70, sub, SB(54), col)
    # bottom handle
    d.rounded_rectangle((250, 1530, 830, 1620), 45, fill=mix(CARD, 1), outline=col, width=4)
    ct(d, 1550, "@sql_developer_no1", SB(46), GREEN)
    im.save(out, quality=92)

if __name__ == "__main__":
    import os
    os.makedirs("/home/claude/sql-developer-videos/covers", exist_ok=True)
    for n in (map(int, sys.argv[1:]) if len(sys.argv) > 1 else COVERS):
        cover(n, f"/home/claude/sql-developer-videos/covers/cover{n}.jpg")
    print("ok")

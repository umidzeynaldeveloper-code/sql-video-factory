"""Eye-catching 1080x1920 covers for Reels/Shorts. Key content kept inside the centre 1080x1440 (Instagram 3:4 grid crop)."""
import sys
from common import *
from PIL import Image, ImageDraw

COVERS = {
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
    fs = 150 if max(len(l) for l in lines) <= 9 else 118 if max(len(l) for l in lines) <= 12 else 98
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

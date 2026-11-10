from common import *
from PIL import Image, ImageDraw
WW, HH = 1920, 1080
col = RED
im = rain.crop((0, 0, W, HH)).resize((WW, HH))
im = Image.blend(im, Image.new("RGB", (WW, HH), BG), .6); d = ImageDraw.Draw(im)
for r in range(800, 0, -25):
    d.ellipse((560 - r, 540 - r * .7, 560 + r, 540 + r * .7), fill=mix(col, .09 * (1 - r / 800)))
d.rounded_rectangle((80, 80, 700, 170), 45, fill=YEL)
ct(d, 98, "ORACLE · FULL GUIDE", SB(50), BG, 1, cx=390)
ct(d, 250, "WHY IS MY", SB(150), WHITE, 1, cx=640)
ct(d, 420, "QUERY SLOW?", SB(150), RED, 1, cx=640)
d.rounded_rectangle((120, 640, 1160, 760), 30, fill=CARD, outline=GREEN, width=5)
ct(d, 662, "8-step tuning method", SB(66), GREEN, 1, cx=640)
# right: before/after
d.rounded_rectangle((1260, 230, 1840, 450), 30, fill=CARD, outline=RED, width=6)
ct(d, 255, "BEFORE", SB(46), DIM, 1, cx=1550); ct(d, 320, "40 min", SB(100), RED, 1, cx=1550)
ct(d, 470, "↓", SB(110), WHITE, 1, cx=1550)
d.rounded_rectangle((1260, 620, 1840, 840), 30, fill=CARD, outline=GREEN, width=6)
ct(d, 645, "AFTER", SB(46), DIM, 1, cx=1550); ct(d, 710, "2 sec", SB(100), GREEN, 1, cx=1550)
ct(d, 900, "E-Rows 10  vs  A-Rows 970,000", MB(48), CYAN, 1, cx=640)
d.rounded_rectangle((1400, 955, 1890, 1045), 40, fill=CARD, outline=YEL, width=4)
ct(d, 976, "@sql_developer_no1", SB(40), GREEN, 1, cx=1645)
im.resize((1280, 720), Image.LANCZOS).save("/home/claude/sql-developer-videos/thumbs/long1.jpg", quality=92)
print("ok")

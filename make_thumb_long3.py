from common import *
from PIL import Image, ImageDraw
WW, HH = 1920, 1080
im = rain.crop((0, 0, W, HH)).resize((WW, HH))
im = Image.blend(im, Image.new("RGB", (WW, HH), BG), .6); d = ImageDraw.Draw(im)
for r in range(800, 0, -25):
    d.ellipse((960 - r * 1.3, 470 - r * .6, 960 + r * 1.3, 470 + r * .6), fill=mix(CYAN, .07 * (1 - r / 800)))
d.rounded_rectangle((80, 70, 760, 160), 45, fill=YEL)
ct(d, 88, "ORACLE · FROM ZERO", SB(50), BG, 1, cx=420)
ct(d, 220, "YOU PRESS ENTER…", SB(130), WHITE, 1, cx=960)
ct(d, 390, "THEN WHAT?", SB(150), YEL, 1, cx=960)
cols = [CYAN, YEL, GREEN, PINK]; names = ["PARSE", "OPTIMIZE", "EXECUTE", "FETCH"]
for k in range(4):
    x = 150 + k * 430
    d.rounded_rectangle((x, 660, x + 360, 800), 30, fill=CARD, outline=cols[k], width=7)
    ct(d, 700, names[k], SB(58), cols[k], 1, cx=x + 180)
    if k < 3:
        d.polygon([(x + 375, 715), (x + 415, 730), (x + 375, 745)], fill=WHITE)
ct(d, 870, "4 stages inside Oracle, explained with pictures", SB(50), WHITE, 1, cx=960)
d.rounded_rectangle((1400, 960, 1890, 1050), 40, fill=CARD, outline=YEL, width=4)
ct(d, 981, "@sql_developer_no1", SB(40), GREEN, 1, cx=1645)
im.resize((1280, 720), Image.LANCZOS).save("/home/claude/sql-developer-videos/thumbs/long3.jpg", quality=92)
print("ok")

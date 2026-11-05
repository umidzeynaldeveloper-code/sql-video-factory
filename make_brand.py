import sys, random
sys.path.insert(0, '/home/claude')
from common import *
from PIL import Image, ImageDraw, ImageFilter

def bin_rain(w, h, seed=7):
    random.seed(seed)
    im = Image.new("RGB", (w, h), BG); d = ImageDraw.Draw(im)
    for x in range(14, w, 40):
        for y in range(0, h, 40):
            if random.random() < 0.5:
                d.text((x, y), random.choice("01"), font=MN(26),
                       fill=random.choice([(20, 30, 52), (24, 38, 64), (18, 27, 46)]))
    return im

def glow(im, box_fn, col, rad=40, strength=1.0):
    layer = Image.new("RGB", im.size, (0, 0, 0)); ld = ImageDraw.Draw(layer)
    box_fn(ld, col)
    layer = layer.filter(ImageFilter.GaussianBlur(rad))
    return Image.blend(im, Image.composite(layer, im, layer.convert("L")), .55 * strength)

def cylinder(d, cx, cy, w, h, col, width=10, fill=None):
    e = w * .28
    d.rectangle((cx - w/2, cy - h/2 + e/2, cx + w/2, cy + h/2 - e/2), fill=fill)
    d.ellipse((cx - w/2, cy + h/2 - e, cx + w/2, cy + h/2), fill=fill, outline=col, width=width)
    d.rectangle((cx - w/2 + width, cy - h/2 + e/2, cx + w/2 - width, cy + h/2 - e/2), fill=fill)
    d.line((cx - w/2, cy - h/2 + e/2, cx - w/2, cy + h/2 - e/2), fill=col, width=width)
    d.line((cx + w/2, cy - h/2 + e/2, cx + w/2, cy + h/2 - e/2), fill=col, width=width)
    for k in (1, 2):
        y = cy - h/2 + e/2 + k * (h - e) / 3
        d.arc((cx - w/2, y - e/2, cx + w/2, y + e/2), 0, 180, fill=col, width=max(3, width // 2))
    d.ellipse((cx - w/2, cy - h/2, cx + w/2, cy - h/2 + e), fill=mix(col, .25), outline=col, width=width)

def logo(path, size=800):
    S = size
    im = bin_rain(S, S, 3)
    im = glow(im, lambda d, c: d.ellipse((S*.18, S*.18, S*.82, S*.82), fill=c), CYAN, 70)
    d = ImageDraw.Draw(im)
    cylinder(d, S/2, S*.47, S*.56, S*.6, CYAN, 14, fill=mix(CARD, 1))
    f = SB(int(S*.19)); t = "SQL"; w = d.textlength(t, font=f)
    d.text((S/2 - w/2 + 4, S*.42 + 4), t, font=f, fill=(0, 0, 0))
    d.text((S/2 - w/2, S*.42), t, font=f, fill=WHITE)
    d.rounded_rectangle((S*.30, S*.78, S*.70, S*.88), S*.05, fill=GREEN)
    f2 = SB(int(S*.06)); t2 = "ORACLE"; w2 = d.textlength(t2, font=f2)
    d.text((S/2 - w2/2, S*.795), t2, font=f2, fill=BG)
    im.save(path, quality=95)

def banner(path):
    Wb, Hb = 2048, 1152
    im = bin_rain(Wb, Hb, 5)
    cx, cy = Wb/2, Hb/2
    im = glow(im, lambda d, c: d.ellipse((cx-700, cy-260, cx+700, cy+260), fill=c), CYAN, 120, .9)
    d = ImageDraw.Draw(im)
    # safe area 1546x423 → content inside 1235x338
    cylinder(d, cx - 525, cy, 150, 190, CYAN, 9, fill=mix(CARD, 1))
    fs = SB(34); t = "SQL"; w = d.textlength(t, font=fs); d.text((cx - 525 - w/2, cy - 12), t, font=fs, fill=WHITE)
    x0 = cx - 410
    d.text((x0 + 4, cy - 132 + 4), "ORACLE INTERNALS", font=SB(84), fill=(0, 0, 0))
    d.text((x0, cy - 132), "ORACLE INTERNALS", font=SB(84), fill=WHITE)
    d.text((x0, cy - 34), "explained visually · in under 3 minutes", font=SB(40), fill=CYAN)
    chips = [("Indexes", GREEN), ("Execution plans", YEL), ("Locks", PINK), ("UNDO / REDO", PURP), ("PL/SQL", CYAN)]
    x = x0; y = cy + 40
    for s, col in chips:
        f = SB(27); tw = d.textlength(s, font=f)
        d.rounded_rectangle((x, y, x + tw + 36, y + 50), 25, fill=mix(col, .18), outline=col, width=3)
        d.text((x + 18, y + 9), s, font=f, fill=col); x += tw + 46
    d.text((x0, cy + 112), "Instagram: @sql_developer_no1", font=SN(28), fill=DIM)
    im.save(path, quality=93)

if __name__ == "__main__":
    out = "/home/claude/sql-developer-videos/branding"
    import os; os.makedirs(out, exist_ok=True)
    logo(out + "/logo.png"); banner(out + "/banner.jpg")
    # preview with safe-area guides
    b = Image.open(out + "/banner.jpg").copy(); d = ImageDraw.Draw(b)
    for (w, h, c) in ((1546, 423, (255, 0, 0)), (1235, 338, (0, 255, 0))):
        d.rectangle((1024 - w/2, 576 - h/2, 1024 + w/2, 576 + h/2), outline=c, width=3)
    b.resize((1024, 576)).save("/tmp/claude-0/-home-claude/894fd1c7-2643-5f56-8244-6fc152e1e722/scratchpad/banner_prev.png")
    Image.open(out + "/logo.png").resize((300, 300)).save("/tmp/claude-0/-home-claude/894fd1c7-2643-5f56-8244-6fc152e1e722/scratchpad/logo_prev.png")
    print("ok")

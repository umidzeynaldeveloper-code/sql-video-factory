import subprocess, random, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/truetype/dejavu/"
def F(n, s): return ImageFont.truetype(FD + n, s)
SB = lambda s: F("DejaVuSans-Bold.ttf", s)
SN = lambda s: F("DejaVuSans.ttf", s)
MN = lambda s: F("DejaVuSansMono.ttf", s)
MB = lambda s: F("DejaVuSansMono-Bold.ttf", s)

BG = (10, 14, 28); WHITE = (238, 242, 255); DIM = (125, 138, 178)
GREEN = (52, 230, 140); CYAN = (70, 200, 255); YEL = (255, 205, 70)
PINK = (255, 95, 150); RED = (255, 80, 80); CARD = (22, 32, 60); OFFB = (45, 55, 85)
PURP = (170, 120, 255)

random.seed(11)
rain = Image.new("RGB", (W, H * 2), BG)
rd = ImageDraw.Draw(rain)
for x in range(20, W, 46):
    for y in range(0, H * 2, 44):
        if random.random() < 0.5:
            rd.text((x, y), random.choice("01"), font=MN(30),
                    fill=random.choice([(20, 30, 52), (24, 38, 64), (18, 27, 46)]))

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def pr(t, a, b): return ease((t - a) / (b - a))
def mix(c, a): return tuple(int(BG[i] + (c[i] - BG[i]) * a) for i in range(3))
def ct(d, y, s, f, c, a=1.0, cx=W / 2):
    w = d.textlength(s, font=f); d.text((cx - w / 2, y), s, font=f, fill=mix(c, a))

def wrap(d, s, f, maxw):
    out, cur = [], ""
    for w in s.split():
        tst = (cur + " " + w).strip()
        if d.textlength(tst, font=f) > maxw: out.append(cur); cur = w
        else: cur = tst
    out.append(cur); return out

def caption(d, s, a):
    if a <= 0: return
    f = SN(44); lines = wrap(d, s, f, W - 200)
    h = 70 + 60 * len(lines); y0 = 1650 - h
    d.rounded_rectangle((60, y0, W - 60, 1650), 30, fill=mix((18, 26, 50), a), outline=mix(GREEN, a * .5), width=3)
    for k, ln in enumerate(lines): ct(d, y0 + 35 + k * 60, ln, f, WHITE, a)

def bulb(d, cx, cy, r, lit, a, label="", col=YEL):
    if lit:
        for rr in range(int(r * 1.45), r, -5):
            g = (1 - (rr - r) / (r * .45)) * .45
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=mix((90, 70, 10), a * g))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=mix(col if lit else OFFB, a))
    if label:
        f = MB(int(r * .95)); w = d.textlength(label, font=f)
        d.text((cx - w / 2, cy - r * .62), label, font=f, fill=mix(BG if lit else WHITE, a))

def byte_row(d, y, bits, a, nshow=8, prefix=0, pcol=PINK):
    for j in range(8):
        cx = 130 + j * 117
        if j >= nshow: bulb(d, cx, y, 44, False, a * .3); continue
        lit = bits[j] == "1"
        col = pcol if j < prefix else YEL
        bulb(d, cx, y, 44, lit, a, bits[j], col)
        if j < prefix and not lit:
            d.ellipse((cx - 44, y - 44, cx + 44, y + 44), outline=mix(pcol, a), width=5)

def code_box(d, y0, y1, lines, t0, t, a, speed=.045):
    d.rounded_rectangle((60, y0, W - 60, y1), 30, fill=mix((16, 22, 42), a), outline=mix((50, 70, 120), a), width=3)
    for k, c in enumerate([PINK, YEL, GREEN]):
        d.ellipse((100 + k * 50, y0 + 30, 130 + k * 50, y0 + 60), fill=mix(c, a))
    full = "\n".join(lines); n = int(max(0, (t - t0) / speed)); shown = full[:n]
    yy = y0 + 100
    KW = ("SELECT", "FROM", "INSERT", "INTO", "VALUES", "CREATE", "TABLE", "WHERE", "IN", "NOT", "IS", "AND", "OR", "EXISTS")
    for line in shown.split("\n"):
        x = 100
        for word in line.split(" "):
            wd = word.strip("(),;*")
            col = PINK if wd == "NULL" or wd == "''" else CYAN if wd in KW else (YEL if "'" in word else (PURP if "VARCHAR2" in word or "LENGTH" in word else WHITE))
            d.text((x, yy), word, font=MB(46), fill=mix(col, a))
            x += d.textlength(word + " ", font=MB(46))
        yy += 70
    return n >= len(full)


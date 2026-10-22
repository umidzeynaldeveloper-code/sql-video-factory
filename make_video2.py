import subprocess, random, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 30
N = FPS * DUR
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
    KW = ("SELECT", "FROM", "INSERT", "INTO", "VALUES", "CREATE", "TABLE")
    for line in shown.split("\n"):
        x = 100
        for word in line.split(" "):
            col = CYAN if word.strip("(),;") in KW else (YEL if "'" in word else (PURP if "VARCHAR2" in word or "LENGTH" in word else WHITE))
            d.text((x, yy), word, font=MB(46), fill=mix(col, a))
            x += d.textlength(word + " ", font=MB(46))
        yy += 70
    return n >= len(full)

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    # 1. HOOK 0-3.5
    if t < 3.5:
        fo = 1 - pr(t, 3.1, 3.5); a = pr(t, 0, .4) * fo
        ct(d, 330, "Keçən dəfə soruşduq:", SB(62), DIM, a)
        # a vs ə
        ct(d, 520, "a", MB(260), WHITE, a, 300)
        ct(d, 520, "ə", MB(260), PINK, a, 780)
        ct(d, 870, "1 bayt", SB(64), GREEN, pr(t, .6, 1) * fo, 300)
        q = "2 bayt!" if t > 1.8 else "? bayt"
        ct(d, 870, q, SB(64), YEL if t > 1.8 else DIM, pr(t, .9, 1.3) * fo, 780)
        if t > 1.8:
            r = 150 + 15 * math.sin(t * 10)
            d.ellipse((780 - r, 690 - r, 780 + r, 690 + r), outline=mix(YEL, fo), width=8)
        ct(d, 1080, "Niyə 2 qat çox?", SB(78), WHITE, pr(t, 2.1, 2.5) * fo)
        caption(d, "Eyni ölçüdə hərflər, amma yaddaşda fərqli yer tuturlar. Gəl səbəbini görək.", pr(t, 2.3, 2.7) * fo)

    # 2. ASCII 3.5-8.5
    elif t < 8.5:
        lt = t - 3.5; fo = 1 - pr(lt, 4.6, 5); a = pr(lt, 0, .4) * fo
        ct(d, 270, "ASCII cədvəli", SB(72), WHITE, a)
        ct(d, 365, "1 bayt · ingilis əlifbası üçün", SN(44), DIM, a)
        # box of letters
        d.rounded_rectangle((110, 440, 970, 900), 30, fill=mix(CARD, a), outline=mix(GREEN, a), width=6)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        for k, ch in enumerate(letters[:56]):
            cx = 160 + (k % 14) * 58; cy = 480 + (k // 14) * 95
            al = pr(lt, .2 + k * .012, .5 + k * .012) * fo
            hl = ch == "a" and lt > 1.3
            if hl: d.rounded_rectangle((cx - 8, cy - 4, cx + 48, cy + 70), 10, fill=mix(GREEN, fo))
            d.text((cx, cy), ch, font=MB(52), fill=mix(BG if hl else WHITE, al) if not hl else BG)
        ct(d, 840, "a = 97 = 01100001", MB(44), GREEN, pr(lt, 1.3, 1.7) * fo)
        # ə tries to enter and bounces
        if lt > 2.2:
            p = lt - 2.2
            x = 980 - 300 * pr(p, 0, .5) + 300 * pr(p, .55, 1.0)
            shake = 12 * math.sin(p * 40) * (1 - pr(p, .5, .9)) if p > .45 else 0
            ct(d, 960, "ə", MB(200), PINK, fo, x + shake)
            if p > .5:
                ct(d, 1210, "Yer yoxdur!", SB(64), RED, pr(p, .5, .8) * fo)
        caption(d, "ASCII yalnız 128 işarə saxlayır: latın hərfləri, rəqəmlər, simvollar. 'ə' bu cədvəldə yoxdur.", pr(lt, .6, 1) * fo)

    # 3. UNICODE 8.5-14
    elif t < 14:
        lt = t - 8.5; fo = 1 - pr(lt, 5.1, 5.5); a = pr(lt, 0, .4) * fo
        ct(d, 270, "Həll: UNICODE", SB(76), WHITE, a)
        ct(d, 370, "Dünyadakı hər hərfin nömrəsi var", SN(46), DIM, a)
        # chips of world letters
        chips = [("ə", "601"), ("ş", "351"), ("ğ", "287"), ("ж", "1078"), ("中", "20013")]
        for k, (c, n) in enumerate(chips):
            x = 85 + k * 185; al = pr(lt, .3 + k * .12, .7 + k * .12) * fo
            hl = k == 0
            d.rounded_rectangle((x, 450, x + 165, 640), 22, fill=mix(PINK if hl else CARD, al))
            fnt = SB(80) if c == "中" else MB(90)
            if c == "中": fnt = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc", 80)
            ct(d, 455, c, fnt, BG if hl else WHITE, al, x + 82)
            ct(d, 580, n, MN(36), BG if hl else CYAN, al, x + 82)
        a2 = pr(lt, 1.6, 2) * fo
        ct(d, 730, "ə = 601", MB(110), PINK, a2)
        a3 = pr(lt, 2.4, 2.8) * fo
        ct(d, 900, "Amma 1 bayt maksimum 255!", SB(58), YEL, a3)
        # meter 601 vs 255
        a4 = pr(lt, 2.8, 3.2) * fo
        d.rounded_rectangle((110, 1010, 970, 1080), 35, fill=mix(OFFB, a4))
        fill = 110 + 860 * (255 / 601) * pr(lt, 3.0, 3.6)
        d.rounded_rectangle((110, 1010, fill, 1080), 35, fill=mix(GREEN, a4))
        if lt > 3.6:
            over = 110 + 860 * (255 / 601) + (860 * (346 / 601)) * pr(lt, 3.6, 4.2)
            d.rounded_rectangle((110 + 860 * 255 / 601 - 30, 1010, over, 1080), 35, fill=mix(RED, fo))
        ct(d, 1100, "255", MB(40), GREEN, a4, 110 + 860 * 255 / 601)
        ct(d, 1100, "601", MB(40), RED, pr(lt, 4, 4.3) * fo, 940)
        ct(d, 1200, "→ 2 bayt lazımdır", SB(68), WHITE, pr(lt, 4.3, 4.7) * fo)
        caption(d, "601 bir bayta (8 bit) sığmır. Ona görə kompüter 'ə' üçün 2 bayt ayırır.", pr(lt, 2.6, 3) * fo)

    # 4. UTF-8 bytes 14-18.5
    elif t < 18.5:
        lt = t - 14; fo = 1 - pr(lt, 4.1, 4.5); a = pr(lt, 0, .4) * fo
        ct(d, 270, "UTF-8-də 'ə' belə görünür:", SB(62), WHITE, a)
        b1, b2 = "11001001", "10011001"
        n1 = int(max(0, min(8, (lt - .5) / .1 + 1))); n2 = int(max(0, min(8, (lt - 1.5) / .1 + 1)))
        ct(d, 420, "1-ci bayt = 201", MB(44), CYAN, pr(lt, .4, .8) * fo)
        byte_row(d, 540, b1, a, n1, 3 if lt > 2.6 else 0)
        ct(d, 660, "2-ci bayt = 153", MB(44), CYAN, pr(lt, 1.4, 1.8) * fo)
        byte_row(d, 780, b2, a, n2, 2 if lt > 2.6 else 0)
        a3 = pr(lt, 2.6, 3) * fo
        d.rounded_rectangle((90, 900, 990, 1020), 24, fill=mix(CARD, a3))
        d.text((120, 920), "110", font=MB(56), fill=mix(PINK, a3))
        d.text((250, 932), "= \"mən 2 baytlıq hərfəm\"", font=SN(42), fill=mix(WHITE, a3))
        a4 = pr(lt, 3.1, 3.5) * fo
        d.rounded_rectangle((90, 1040, 990, 1160), 24, fill=mix(CARD, a4))
        d.text((120, 1060), "10", font=MB(56), fill=mix(PINK, a4))
        d.text((250, 1072), "= \"mən davamıyam\"", font=SN(42), fill=mix(WHITE, a4))
        caption(d, "Çəhrayı bitlər işarədir: kompüter onlara baxıb hərfin neçə baytdan ibarət olduğunu anlayır.", pr(lt, 2.6, 3) * fo)

    # 5. LENGTH vs LENGTHB 18.5-23
    elif t < 23:
        lt = t - 18.5; fo = 1 - pr(lt, 4.1, 4.5); a = pr(lt, 0, .4) * fo
        ct(d, 270, "Oracle-da yoxlayaq:", SB(66), WHITE, a)
        code_box(d, 380, 760, ["SELECT LENGTH('ə'),", "       LENGTHB('ə')", "  FROM dual;"], .5, lt, a, .035)
        a2 = pr(lt, 1.8, 2.2) * fo
        for k, (lab, val, c) in enumerate([("LENGTH", "1", GREEN), ("LENGTHB", "2", PINK)]):
            x = 110 + k * 440
            d.rounded_rectangle((x, 820, x + 420, 1100), 30, fill=mix(CARD, a2))
            ct(d, 845, lab, MB(46), DIM, a2, x + 210)
            ct(d, 900, val, MB(150), c, a2, x + 210)
        ct(d, 1130, "simvol          bayt", SN(44), DIM, a2)
        caption(d, "LENGTH simvolları sayır, LENGTHB baytları. 'ə' 1 simvoldur, amma 2 bayt yer tutur.", pr(lt, 2.2, 2.6) * fo)

    # 6. ORA-12899 23-27.5
    elif t < 27.5:
        lt = t - 23; fo = 1 - pr(lt, 4.1, 4.5); a = pr(lt, 0, .3) * fo
        ct(d, 260, "Bankda real hal:", SB(66), WHITE, a)
        code_box(d, 360, 700, ["city VARCHAR2(4 BYTE)", "", "INSERT ... VALUES ('Bakı');"], .3, lt, a, .03)
        a2 = pr(lt, 1.4, 1.7) * fo
        sh = 10 * math.sin(lt * 50) * (1 - pr(lt, 1.4, 2.0))
        d.rounded_rectangle((60 + sh, 740, W - 60 + sh, 900), 24, fill=mix((70, 18, 28), a2), outline=mix(RED, a2), width=4)
        d.text((100 + sh, 760), "ORA-12899", font=MB(54), fill=mix(RED, a2))
        d.text((100 + sh, 830), "value too large (actual: 5, max: 4)", font=MN(36), fill=mix(WHITE, a2))
        ct(d, 930, "B-a-k-ı = 4 hərf, amma 5 bayt (ı = 2 bayt)", SN(40), DIM, a2)
        a3 = pr(lt, 2.4, 2.8) * fo
        d.rounded_rectangle((60, 1010, W - 60, 1150), 24, fill=mix((14, 50, 36), a3), outline=mix(GREEN, a3), width=4)
        d.text((100, 1045), "city VARCHAR2(4 CHAR)", font=MB(52), fill=mix(GREEN, a3))
        ct(d, 1175, "✓ Problem həll olundu", SB(56), GREEN, pr(lt, 2.8, 3.1) * fo)
        caption(d, "Azərbaycan hərfli adlar üçün sütunu BYTE yox, CHAR ilə təyin et.", pr(lt, 2.6, 3) * fo)

    # 7. CTA 27.5-30
    else:
        lt = t - 27.5
        ct(d, 560, "Yadda saxla:", SB(70), WHITE, pr(lt, 0, .3))
        ct(d, 680, "ə ş ğ ı ö ü ç", MB(100), PINK, pr(lt, .2, .5))
        ct(d, 830, "= 2 bayt", SB(80), YEL, pr(lt, .4, .7))
        a = pr(lt, .8, 1.2); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 1080, (W + bw) / 2, 1080 + bh), 65, fill=mix(GREEN, a))
        ct(d, 1080 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, a)
        ct(d, 1260, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 1.2, 1.6))
    return im

p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v2_silent.mp4"], stdin=subprocess.PIPE)
for i in range(N):
    fr = frame(i); p.stdin.write(fr.tobytes())
    if i in (80, 200, 380, 520, 640, 760, 870): fr.save(f"v2_{i}.png")
p.stdin.close(); p.wait(); print("video done")

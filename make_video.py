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
PINK = (255, 95, 150); CARD = (22, 32, 60); OFFB = (45, 55, 85)

random.seed(7)
rain = Image.new("RGB", (W, H * 2), BG)
rd = ImageDraw.Draw(rain)
for x in range(20, W, 46):
    for y in range(0, H * 2, 44):
        if random.random() < 0.5:
            rd.text((x, y), random.choice("01"), font=MN(30),
                    fill=random.choice([(20, 30, 52), (24, 38, 64), (18, 27, 46)]))

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def pr(t, a, b): return ease((t - a) / (b - a))
def mix(c, a, base=None):
    b = base or BG
    return tuple(int(b[i] + (c[i] - b[i]) * a) for i in range(3))
def ct(d, y, s, f, c, a=1.0):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=mix(c, a))

def wrap(d, s, f, maxw):
    out, cur = [], ""
    for w in s.split():
        tst = (cur + " " + w).strip()
        if d.textlength(tst, font=f) > maxw: out.append(cur); cur = w
        else: cur = tst
    out.append(cur); return out

def caption(d, s, a):
    """Explanation box at bottom"""
    if a <= 0: return
    f = SN(44)
    lines = wrap(d, s, f, W - 200)
    h = 70 + 60 * len(lines)
    y0 = 1640 - h
    d.rounded_rectangle((60, y0, W - 60, 1640), 30, fill=mix((18, 26, 50), a), outline=mix(GREEN, a * .5), width=3)
    for k, ln in enumerate(lines):
        ct(d, y0 + 35 + k * 60, ln, f, WHITE, a)

def bulb(d, cx, cy, r, lit, a, label=None, lf=None):
    if lit:
        for rr in range(int(r * 1.5), r, -6):
            g = (1 - (rr - r) / (r * .5)) * .5
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=mix((90, 70, 10), a * g))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=mix(YEL if lit else OFFB, a))
    d.rectangle((cx - r * .4, cy + r * .85, cx + r * .4, cy + r * 1.25), fill=mix((140, 150, 175), a))
    if label is not None:
        f = lf or MB(int(r * 1.1))
        w = d.textlength(label, font=f)
        d.text((cx - w / 2, cy - r * .7), label, font=f, fill=mix(BG if lit else WHITE, a))

LET = [("S", 83, "01010011"), ("Q", 81, "01010001"), ("L", 76, "01001100")]

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 420, 160), 35, fill=CARD)
    d.text((90, 104), "SQL Developer", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    # ---- 1. HOOK 0-3.5
    if t < 3.5:
        fo = 1 - pr(t, 3.1, 3.5); a = pr(t, 0, .5) * fo
        ct(d, 520, "Sən 'SQL' yazırsan...", SB(70), WHITE, a)
        sc = 1 + .05 * math.sin(t * 6)
        ct(d, 680, "SQL", MB(int(230 * sc)), GREEN, a)
        a2 = pr(t, 1.2, 1.7) * fo
        ct(d, 1000, "Kompüter isə bunu görür:", SB(62), WHITE, a2)
        bits = "010100110101000101001100"
        n = int(max(0, (t - 1.7) / .05))
        s = bits[:n]
        for row in range(3):
            seg = s[row * 8:row * 8 + 8]
            ct(d, 1110 + row * 95, " ".join(seg), MB(66), YEL, fo)
        caption(d, "Necə olur ki, hərf 0 və 1-ə çevrilir? 30 saniyəyə izah edirəm.", pr(t, 2, 2.4) * fo)

    # ---- 2. SWITCH 3.5-8.5
    elif t < 8.5:
        lt = t - 3.5; fo = 1 - pr(lt, 4.6, 5)
        a = pr(lt, 0, .5) * fo
        ct(d, 280, "Kompüterin içində", SB(68), WHITE, a)
        ct(d, 370, "milyardlarla kiçik açar var", SB(56), CYAN, a)
        on = lt > 2.2  # switch flips
        # circuit: battery -- switch -- bulb
        y = 800
        L, R = 160, 920
        wc = mix(YEL if on else OFFB, a)
        d.line((L, y, 420, y), fill=wc, width=10)
        d.line((640, y, R, y), fill=wc, width=10)
        d.line((L, y, L, 1150), fill=wc, width=10)
        d.line((L, 1150, R, 1150), fill=wc, width=10)
        d.line((R, 1150, R, 1060), fill=wc, width=10)
        # battery
        d.rectangle((L - 45, 930, L + 45, 1050), fill=mix((60, 75, 110), a))
        d.text((L - 20, 950), "+", font=SB(60), fill=mix(WHITE, a))
        # switch lever
        d.ellipse((410, y - 15, 440, y + 15), fill=mix(WHITE, a))
        d.ellipse((620, y - 15, 650, y + 15), fill=mix(WHITE, a))
        ang = 0 if on else -35
        if lt > 1.8: ang = -35 + 35 * pr(lt, 1.8, 2.2)
        ex = 425 + 210 * math.cos(math.radians(ang)); ey = y + 210 * math.sin(math.radians(ang))
        d.line((425, y, ex, ey), fill=mix(WHITE, a), width=12)
        # bulb
        bulb(d, R, 960, 95, on, a)
        # electrons moving
        if on:
            path = [(L, 1150), (L, y), (R, y), (R, 1150), (L, 1150)]
            segs = [(path[k], path[k + 1]) for k in range(4)]
            lens = [math.dist(p, q) for p, q in segs]; tot = sum(lens)
            for e in range(14):
                s = (e / 14 * tot + lt * 400) % tot
                for (p, q), ln in zip(segs, lens):
                    if s <= ln:
                        x = p[0] + (q[0] - p[0]) * s / ln; yy = p[1] + (q[1] - p[1]) * s / ln
                        d.ellipse((x - 9, yy - 9, x + 9, yy + 9), fill=mix(CYAN, a)); break
                    s -= ln
        big = "1" if on else "0"
        ct(d, 1200, big, MB(150), YEL if on else DIM, a)
        txt = ("Açar BAĞLIDIR → cərəyan axır → bunu 1 sayırıq." if on
               else "Açar AÇIQDIR → cərəyan yoxdur → bunu 0 sayırıq.")
        caption(d, txt, pr(lt, .6, 1) * fo)

    # ---- 3. BYTE 8.5-13
    elif t < 13:
        lt = t - 8.5; fo = 1 - pr(lt, 4.1, 4.5)
        a = pr(lt, 0, .5) * fo
        ct(d, 300, "Bir açar = 1 bit", SB(72), WHITE, a)
        a2 = pr(lt, 1, 1.5) * fo
        ct(d, 400, "8 açar yan-yana = 1 BAYT", SB(64), GREEN, a2)
        # 8 bulbs cycling patterns
        pat = format(int(lt * 9) % 256, "08b") if lt > 1.5 else "00000000"
        for j in range(8):
            cx = 130 + j * 117
            bulb(d, cx, 760, 46, pat[j] == "1", pr(lt, .3 + j * .08, .7 + j * .08) * fo,
                 pat[j], MB(44))
        a3 = pr(lt, 2, 2.5) * fo
        ct(d, 950, "2⁸ = 256 fərqli kombinasiya", SB(60), YEL, a3)
        ct(d, 1050, "Bütün hərflər, rəqəmlər, işarələr", SN(46), DIM, a3)
        ct(d, 1110, "bu 256 yerə sığır", SN(46), DIM, a3)
        caption(d, "Lampaları müxtəlif yandırıb-söndürməklə 256 fərqli işarə kodlaya bilərik.", pr(lt, .8, 1.2) * fo)

    # ---- 4. ASCII 13-20.5
    elif t < 20.5:
        lt = t - 13; fo = 1 - pr(lt, 7.1, 7.5)
        a = pr(lt, 0, .5) * fo
        ct(d, 260, "Hər hərfin öz nömrəsi var", SB(60), WHITE, a)
        ct(d, 345, "(ASCII cədvəli)", SN(44), DIM, a)
        # mini table strip
        cols = [("P", 80), ("Q", 81), ("R", 82), ("S", 83), ("K", 75), ("L", 76), ("M", 77)]
        idx = 0 if lt < 3.2 else (1 if lt < 5.2 else 2)
        target = ["S", "Q", "L"][idx]
        for k, (ch, n) in enumerate(cols):
            x = 75 + k * 135
            hl = ch == target and lt > .8
            fill = mix(GREEN if hl else CARD, a)
            d.rounded_rectangle((x, 430, x + 120, 590), 18, fill=fill)
            tc = BG if hl else WHITE
            w = d.textlength(ch, font=MB(56)); d.text((x + 60 - w / 2, 440), ch, font=MB(56), fill=mix(tc, a, fill if not hl else None) if not hl else BG)
            w = d.textlength(str(n), font=MN(38)); d.text((x + 60 - w / 2, 525), str(n), font=MN(38), fill=BG if hl else mix(CYAN, a))
        # big conversion for current letter
        ch, num, bits = LET[idx]
        st = [0.8, 3.2, 5.2][idx]
        la = pr(lt, st, st + .4) * fo
        ct(d, 680, f"{ch}  →  {num}", MB(120), WHITE, la)
        nb = int(max(0, min(8, (lt - st - .6) / .12 + 1)))
        for j in range(8):
            cx = 130 + j * 117
            lit = j < nb and bits[j] == "1"
            bulb(d, cx, 1000, 46, lit, la if j < nb else la * .35, bits[j] if j < nb else "", MB(44))
        # done-letters row
        done = "".join(c for c, _, _ in LET[:idx + (1 if nb == 8 else 0)])
        ct(d, 1150, done, MB(90), GREEN, fo)
        caption(d, f"'{ch}' hərfi = {num} = {bits}. Kompüter bu 8 lampanı yaddaşda belə saxlayır.", la)

    # ---- 5. ORACLE 20.5-25.5
    elif t < 25.5:
        lt = t - 20.5; fo = 1 - pr(lt, 4.6, 5)
        ct(d, 290, "Oracle-da öz gözünlə gör:", SB(64), WHITE, pr(lt, 0, .5) * fo)
        a = pr(lt, .3, .8) * fo
        d.rounded_rectangle((60, 420, W - 60, 980), 30, fill=mix((16, 22, 42), a), outline=mix((50, 70, 120), a), width=3)
        for k, c in enumerate([PINK, YEL, GREEN]):
            d.ellipse((100 + k * 50, 455, 130 + k * 50, 485), fill=mix(c, a))
        full = "SELECT DUMP('SQL')\n  FROM dual;"
        n = int(max(0, (lt - .8) / .05)); shown = full[:n]
        yy = 540
        for line in shown.split("\n"):
            x = 110
            for word in line.split(" "):
                col = CYAN if word in ("SELECT", "FROM") else (YEL if "DUMP" in word else WHITE)
                d.text((x, yy), word, font=MB(56), fill=mix(col, fo))
                x += d.textlength(word + " ", font=MB(56))
            yy += 90
        a3 = pr(lt, 2.4, 2.9) * fo
        d.text((110, 770), "Typ=96 Len=3:", font=MN(50), fill=mix(DIM, a3))
        d.text((110, 850), "83,81,76", font=MB(80), fill=mix(GREEN, a3))
        ct(d, 1080, "3 hərf = 3 bayt = 24 bit", SB(62), YEL, pr(lt, 3, 3.5) * fo)
        caption(d, "DUMP funksiyası sətrin yaddaşda real olaraq necə saxlandığını göstərir: S=83, Q=81, L=76.", pr(lt, 2.6, 3) * fo)

    # ---- 6. CTA 25.5-30
    else:
        lt = t - 25.5
        ct(d, 480, "Bəs bilirsən?", SB(80), WHITE, pr(lt, 0, .5))
        ct(d, 640, "'ə'", MB(240), PINK, pr(lt, .3, .8))
        ct(d, 940, "hərfi neçə bayt tutur?", SB(70), WHITE, pr(lt, .5, 1))
        ct(d, 1060, "Cavabı növbəti story-də", SN(50), DIM, pr(lt, 1, 1.5))
        a = pr(lt, 1.6, 2.1); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(660 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 1300, (W + bw) / 2, 1300 + bh), 65, fill=mix(GREEN, a))
        ct(d, 1300 + bh / 2 - 34, "İzlə: SQL Developer", SB(54), BG, a)
    return im

p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
    "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-movflags", "+faststart", "sql_binary_story.mp4"], stdin=subprocess.PIPE)
for i in range(N):
    fr = frame(i); p.stdin.write(fr.tobytes())
    if i in (75, 200, 330, 470, 700, 860): fr.save(f"prev_{i}.png")
p.stdin.close(); p.wait(); print("done")

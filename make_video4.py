from common import *
import subprocess, math

DUR = 47; N = FPS * DUR
T = [0, 4, 11, 18, 24, 35, 40, 44, 47]
ROWS = [("101", "Əli", "050-111"), ("205", "Leyla", None), ("318", "Murad", "055-222"),
        ("412", "Nigar", None), ("520", "Orxan", "070-333")]

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def table(d, y0, a, scan=-1, mode=None, done=99):
    """mode: 'star' or 'col' — highlights scanned rows"""
    d.rounded_rectangle((90, y0, 990, y0 + 90 + 85 * len(ROWS)), 22, fill=mix(CARD, a))
    for k, h in enumerate(["ID", "NAME", "PHONE"]):
        d.text((140 + k * 280, y0 + 22), h, font=MB(40), fill=mix(CYAN, a))
    for r, (id_, nm, ph) in enumerate(ROWS):
        y = y0 + 95 + r * 85
        counted = None
        if mode and r <= scan:
            counted = True if mode == "star" else ph is not None
            col = (20, 70, 50) if counted else (70, 22, 32)
            d.rounded_rectangle((100, y - 8, 980, y + 68), 14, fill=mix(col, a))
        if r == scan and mode:
            d.rounded_rectangle((100, y - 8, 980, y + 68), 14, outline=mix(YEL, a), width=4)
        d.text((140, y), id_, font=MN(40), fill=mix(WHITE, a))
        d.text((420, y), nm, font=SN(40), fill=mix(WHITE, a))
        d.text((700, y), ph if ph else "NULL", font=MB(40), fill=mix(WHITE if ph else PINK, a))
        if counted is not None:
            ct(d, y - 6, "✓" if counted else "✗", SB(50), GREEN if counted else RED, a, 945)

def counter(d, y, label, val, col, a):
    d.rounded_rectangle((200, y, 880, y + 150), 30, fill=mix((16, 22, 42), a), outline=mix(col, a), width=5)
    d.text((240, y + 45), label, font=MB(50), fill=mix(WHITE, a))
    w = d.textlength(str(val), font=MB(100))
    d.text((840 - w, y + 18), str(val), font=MB(100), fill=mix(col, a))

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    if t < T[1]:  # 1. HOOK
        lt, fo = sc(t, 0); a = pr(lt, 0, .3) * fo
        ct(d, 290, "Eyni cədvəl, iki sorğu:", SB(64), WHITE, a)
        for k, (q, v, c) in enumerate([("COUNT(*)", 5, GREEN), ("COUNT(phone)", 3, PINK)]):
            al = pr(lt, .4 + k * .6, .8 + k * .6) * fo
            y = 450 + k * 230
            d.rounded_rectangle((90, y, 990, y + 190), 30, fill=mix(CARD, al))
            d.text((140, y + 60), "SELECT " + q, font=MB(50), fill=mix(CYAN, al))
            vv = pr(lt, 1.6 + k * .4, 2 + k * .4)
            ct(d, y + 35, str(v), MB(120), c, vv * fo, 900)
        ct(d, 960, "Hansı düzdür?", SB(84), YEL, pr(lt, 2.5, 2.9) * fo)
        caption(d, "Cavab: ikisi də! Sadəcə fərqli şeyləri sayırlar. Gəl görək nəyi.", pr(lt, 2.6, 3) * fo)

    elif t < T[2]:  # 2. COUNT(*)
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 260, "COUNT(*)", MB(84), GREEN, a)
        ct(d, 370, "hər SƏTRİ sayır", SB(56), WHITE, a)
        scan = int((lt - 1) / .9) if lt > 1 else -1
        scan = min(scan, 4)
        table(d, 470, a, scan, "star")
        cnt = scan + 1 if scan >= 0 else 0
        counter(d, 1000, "COUNT(*) =", cnt, GREEN, pr(lt, .8, 1.1) * fo)
        caption(d, "Sətirdə NULL olub-olmamasının fərqi yoxdur. Sətir varsa, sayılır.", pr(lt, 1.2, 1.6) * fo)

    elif t < T[3]:  # 3. COUNT(phone)
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 260, "COUNT(phone)", MB(84), PINK, a)
        ct(d, 370, "yalnız NULL OLMAYANLARI sayır", SB(52), WHITE, a)
        scan = min(int((lt - 1) / .9) if lt > 1 else -1, 4)
        table(d, 470, a, scan, "col")
        cnt = sum(1 for r in ROWS[:scan + 1] if r[2]) if scan >= 0 else 0
        counter(d, 1000, "COUNT(phone) =", cnt, PINK, pr(lt, .8, 1.1) * fo)
        caption(d, "Leyla və Nigarın telefonu NULL-dur, ona görə sayılmırlar. 5 deyil, 3.", pr(lt, 2.6, 3) * fo)

    elif t < T[4]:  # 4. rule
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 270, "Qayda:", SB(72), WHITE, a)
        cards = [("COUNT(*)", "sətirlərin sayı", GREEN),
                 ("COUNT(col)", "NULL olmayan dəyərlər", PINK),
                 ("COUNT(DISTINCT col)", "unikal, NULL olmayan", CYAN)]
        for k, (q, ex, c) in enumerate(cards):
            y = 400 + k * 200; al = pr(lt, .3 + k * .5, .7 + k * .5) * fo
            d.rounded_rectangle((70, y, W - 70, y + 170), 26, fill=mix(CARD, al), outline=mix(c, al), width=4)
            d.text((110, y + 28), q, font=MB(52), fill=mix(c, al))
            d.text((110, y + 100), ex, font=SN(42), fill=mix(WHITE, al))
        a2 = pr(lt, 2.4, 2.8) * fo
        d.rounded_rectangle((70, 1030, W - 70, 1200), 26, fill=mix((60, 40, 10), a2), outline=mix(YEL, a2), width=4)
        ct(d, 1050, "Mif: COUNT(1) daha sürətlidir?", SB(44), YEL, a2)
        ct(d, 1120, "Yox! Oracle-da COUNT(1) = COUNT(*)", SB(44), WHITE, pr(lt, 3.2, 3.6) * fo)
        caption(d, "Hamısı eyni cədvəldən fərqli sual soruşur. Sualını düzgün seç.", pr(lt, 1.6, 2) * fo)

    elif t < T[5]:  # 5. AVG trap
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 250, "⚠ Gizli tələ: AVG".replace("⚠ ", ""), SB(66), RED, a)
        ct(d, 340, "4 işçinin bonusu:", SN(46), DIM, a)
        bon = [("Əli", 100), ("Leyla", None), ("Murad", 200), ("Nigar", None)]
        base_y = 800; scale = 1.5
        for k, (nm, v) in enumerate(bon):
            x = 140 + k * 220; al = pr(lt, .4 + k * .2, .8 + k * .2) * fo
            if v:
                h = v * scale * pr(lt, .6 + k * .2, 1.2 + k * .2)
                d.rounded_rectangle((x, base_y - h, x + 150, base_y), 14, fill=mix(GREEN, al))
                ct(d, base_y - h - 60, str(v), MB(44), WHITE, al, x + 75)
            else:
                d.rounded_rectangle((x, base_y - 70, x + 150, base_y), 14, outline=mix(PINK, al), width=4)
                ct(d, base_y - 55, "NULL", MB(36), PINK, al, x + 75)
            ct(d, base_y + 15, nm, SN(38), WHITE, al, x + 75)
        # avg lines
        if lt > 2.8:
            y150 = base_y - 150 * scale; al = pr(lt, 2.8, 3.2) * fo
            w = int(880 * pr(lt, 2.8, 3.4))
            for xx in range(100, 100 + w, 30): d.line((xx, y150, xx + 16, y150), fill=mix(RED, al), width=5)
        ag = pr(lt, 3.0, 3.4) * fo
        d.rounded_rectangle((70, 900, W - 70, 1030), 24, fill=mix(CARD, ag))
        d.text((100, 935), "AVG(bonus)", font=MB(48), fill=mix(WHITE, ag))
        d.text((540, 935), "= 150", font=MB(48), fill=mix(RED, ag))
        d.text((760, 942), "✗ (300/2)", font=MN(36), fill=mix(DIM, ag))
        if lt > 6:
            y75 = base_y - 75 * scale; al = pr(lt, 6, 6.4) * fo
            w = int(880 * pr(lt, 6, 6.6))
            for xx in range(100, 100 + w, 30): d.line((xx, y75, xx + 16, y75), fill=mix(YEL, al), width=5)
        ag2 = pr(lt, 6.2, 6.6) * fo
        d.rounded_rectangle((70, 1050, W - 70, 1180), 24, fill=mix((14, 50, 36), ag2), outline=mix(GREEN, ag2), width=4)
        d.text((100, 1085), "AVG(NVL(bonus,0))", font=MB(44), fill=mix(WHITE, ag2))
        d.text((640, 1085), "= 75 ✓", font=MB(48), fill=mix(GREEN, ag2))
        txt = ("AVG NULL-ları atır və 300-ü 4-ə yox, 2-yə bölür. Nəticə 2 dəfə şişir!" if lt < 6.2
               else "NVL ilə NULL-u 0 et: 300 / 4 = 75. İndi hesabat düzgündür.")
        caption(d, txt, pr(lt, 3.4, 3.8) * fo)

    elif t < T[6]:  # 6. trick
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 270, "Faydalı fənd:", SB(66), WHITE, a)
        ct(d, 360, "Neçə müştərinin telefonu YOXDUR?", SB(48), CYAN, a)
        code_box(d, 450, 700, ["SELECT COUNT(*) - COUNT(phone)", "  FROM clients;"], .5, lt, a, .03)
        ag = pr(lt, 2, 2.3) * fo
        ct(d, 760, "5 − 3 = 2", MB(110), YEL, ag)
        ct(d, 920, "Leyla və Nigar", SB(52), PINK, pr(lt, 2.6, 3) * fo)
        caption(d, "Bir sorğu ilə həm ümumi sayı, həm də boş sahələrin sayını tapırsan.", pr(lt, 2.3, 2.7) * fo)

    elif t < T[7]:  # 7. recap
        lt, fo = sc(t, 6); a = pr(lt, 0, .3) * fo
        ct(d, 300, "Yadda saxla:", SB(72), WHITE, a)
        items = [("COUNT(*)", "→ bütün sətirlər", GREEN), ("COUNT(col)", "→ NULL-suz", PINK),
                 ("AVG / SUM", "→ NULL-u atır!", RED), ("NVL(col, 0)", "→ həll", YEL)]
        for k, (q, ex, c) in enumerate(items):
            y = 440 + k * 150; al = pr(lt, .2 + k * .35, .5 + k * .35) * fo
            d.rounded_rectangle((70, y, W - 70, y + 125), 24, fill=mix(CARD, al))
            d.text((110, y + 35), q, font=MB(50), fill=mix(c, al))
            d.text((540, y + 40), ex, font=SN(44), fill=mix(WHITE, al))
        caption(d, "Hesabat yazanda həmişə soruş: bu sütunda NULL ola bilərmi?", pr(lt, 1.6, 2) * fo)

    else:  # 8. CTA
        lt = t - T[7]
        ct(d, 460, "Növbəti video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 560, "İNDEKS necə işləyir?", SB(70), YEL, pr(lt, .2, .5))
        ct(d, 670, "1 milyon sətirdə 1 saniyə 🚀".replace(" 🚀", ""), SB(52), WHITE, pr(lt, .4, .7))
        a = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 900, (W + bw) / 2, 900 + bh), 65, fill=mix(GREEN, a))
        ct(d, 900 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, a)
        ct(d, 1080, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v4_silent.mp4"], stdin=subprocess.PIPE)
snaps = [int((T[k] + (T[k + 1] - T[k]) * .8) * FPS) for k in range(8)]
snaps[4] = int((T[4] + 5.5) * FPS)
for i in range(N):
    fr = frame(i); p.stdin.write(fr.tobytes())
    if i in snaps: fr.save(f"v4_{snaps.index(i)}.png")
    if i == int((T[4] + 10) * FPS): fr.save("v4_avg2.png")
p.stdin.close(); p.wait(); print("video done")

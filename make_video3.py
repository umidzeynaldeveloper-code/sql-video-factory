from common import *
import subprocess, math

DUR = 48; N = FPS * DUR
T = [0, 4, 10.5, 17.5, 23.5, 29.5, 39, 45, 48]   # scene starts

def sc(t, k):  # local time + fade-out factor
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def result_box(d, y, txt, col, a, sub=None):
    d.rounded_rectangle((60, y, W - 60, y + (170 if sub else 120)), 24, fill=mix(CARD, a), outline=mix(col, a), width=4)
    ct(d, y + 25, txt, MB(60), col, a)
    if sub: ct(d, y + 105, sub, SN(40), DIM, a)

def gift(d, cx, cy, s, a, lid_open=0.0, label="?"):
    box = (200, 120, 60)
    d.rectangle((cx - s, cy - s * .6, cx + s, cy + s), fill=mix(box, a))
    d.rectangle((cx - s * .15, cy - s * .6, cx + s * .15, cy + s), fill=mix(PINK, a))
    ly = cy - s * .6 - 40 - lid_open * 80
    d.rectangle((cx - s * 1.1, ly, cx + s * 1.1, ly + 40), fill=mix((220, 140, 70), a))
    ct(d, cy - s * .35, label, SB(int(s * 1.1)), WHITE, a, cx)

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    if t < T[1]:  # 1. HOOK
        lt, fo = sc(t, 0); a = pr(lt, 0, .3) * fo
        ct(d, 290, "Bu sorğu nə qaytarır?", SB(66), WHITE, a)
        code_box(d, 400, 660, ["SELECT * FROM clients", " WHERE phone = NULL;"], .3, lt, a, .035)
        a2 = pr(lt, 1.6, 1.9) * fo
        result_box(d, 720, "0 rows selected", RED, a2, "Xəta yoxdur... amma nəticə də yoxdur!")
        ct(d, 990, "Niyə? 🤔".replace("🤔", ""), SB(90), YEL, pr(lt, 2.4, 2.8) * fo)
        caption(d, "Cədvəldə telefonu boş olan müştərilər VAR. Bəs sorğu niyə heç nə tapmır?", pr(lt, 2.2, 2.6) * fo)

    elif t < T[2]:  # 2. NULL = unknown (gift boxes)
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 270, "NULL = \"boş\" DEYİL", SB(70), WHITE, a)
        ct(d, 365, "NULL = \"BİLİNMİR\"", SB(70), PINK, pr(lt, .6, 1) * fo)
        b = pr(lt, 1.2, 1.6) * fo
        gift(d, 300, 720, 150, b); gift(d, 780, 720, 150, b)
        ct(d, 930, "NULL", MB(54), PINK, b, 300); ct(d, 930, "NULL", MB(54), PINK, b, 780)
        ct(d, 690, "=", SB(110), WHITE, pr(lt, 2.2, 2.5) * fo)
        ct(d, 690, "?", SB(110), YEL, pr(lt, 2.8, 3.1) * fo, 540) if False else None
        a3 = pr(lt, 3.2, 3.6) * fo
        ct(d, 1040, "Qutularda eyni şey var?", SB(56), WHITE, a3)
        ct(d, 1130, "Bilmirik!", SB(80), YEL, pr(lt, 4, 4.3) * fo)
        caption(d, "İki bağlı qutunu müqayisə edə bilməzsən. NULL da belədir: dəyər məlum deyil.", pr(lt, 1.5, 1.9) * fo)

    elif t < T[3]:  # 3. three-valued logic
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 270, "SQL-də 3 cavab var:", SB(68), WHITE, a)
        for k, (lab, c) in enumerate([("TRUE", GREEN), ("FALSE", RED), ("UNKNOWN", YEL)]):
            x = 90 + k * 310; al = pr(lt, .3 + k * .2, .6 + k * .2) * fo
            d.rounded_rectangle((x, 370, x + 290, 470), 50, fill=mix(c, al))
            ct(d, 393, lab, SB(46), BG, al, x + 145)
        rows = [("5 = 5", "TRUE", GREEN), ("5 = 3", "FALSE", RED),
                ("5 = NULL", "UNKNOWN", YEL), ("NULL = NULL", "UNKNOWN", YEL)]
        for k, (expr, res, c) in enumerate(rows):
            y = 560 + k * 150; st = 1.3 + k * 1.1
            al = pr(lt, st, st + .3) * fo; ar = pr(lt, st + .5, st + .8) * fo
            d.rounded_rectangle((90, y, 990, y + 120), 24, fill=mix(CARD, al))
            parts = expr.split(" ")
            x = 130
            for p_ in parts:
                d.text((x, y + 28), p_, font=MB(54), fill=mix(PINK if p_ == "NULL" else WHITE, al))
                x += d.textlength(p_ + " ", font=MB(54))
            d.text((540, y + 28), "→", font=SB(54), fill=mix(DIM, ar))
            d.text((620, y + 28), res, font=SB(54), fill=mix(c, ar))
        caption(d, "Bilinməyən bir şeylə müqayisənin nəticəsi də bilinmir: UNKNOWN. Hətta NULL = NULL belə!", pr(lt, 4.6, 5) * fo)

    elif t < T[4]:  # 4. WHERE gate
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 270, "WHERE yalnız TRUE-nu buraxır", SB(58), WHITE, a)
        # gate with 3 lanes
        gx = 600
        d.text((gx - 75, 400), "WHERE", font=MB(44), fill=mix(CYAN, a))
        lanes = [("TRUE", GREEN, True), ("FALSE", RED, False), ("UNKNOWN", YEL, False)]
        for k, (lab, c, passes) in enumerate(lanes):
            y = 560 + k * 170
            if not passes:
                d.rectangle((gx - 14, y - 70, gx + 14, y + 70), fill=mix(RED if lt > .6 + k * 1.2 + .7 else DIM, a))
            else:
                d.line((gx, y - 70, gx, y - 45), fill=mix(GREEN, a), width=28); d.line((gx, y + 45, gx, y + 70), fill=mix(GREEN, a), width=28)
            st = .6 + k * 1.2; p = lt - st
            if p < 0: continue
            w = d.textlength(lab, font=SB(42)) + 50
            x0 = 80 + w / 2
            x = x0 + (800 - x0) * pr(p, 0, 1.2) if passes else x0 + (gx - 30 - w / 2 - x0) * pr(p, 0, .6)
            al = fo * (1 if passes else 1 - .55 * pr(p, .8, 1.1))
            d.rounded_rectangle((x - w / 2, y - 40, x + w / 2, y + 40), 40, fill=mix(c, al))
            ct(d, y - 26, lab, SB(42), BG, al, x)
            mark, mc = ("✓", GREEN) if passes else ("✗", RED)
            if p > .7: ct(d, y - 50, mark, SB(80), mc, pr(p, .7, 1) * fo, 985 if passes else gx + 90)
        ct(d, 1080, "UNKNOWN = sətir göstərilmir", SB(54), YEL, pr(lt, 3.6, 4) * fo)
        caption(d, "phone = NULL həmişə UNKNOWN verir. WHERE onu süzgəcdən keçirmir, ona görə 0 sətir.", pr(lt, 4, 4.4) * fo)

    elif t < T[5]:  # 5. IS NULL fix
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 270, "Düzgün yol: IS NULL", SB(68), GREEN, a)
        code_box(d, 380, 640, ["SELECT * FROM clients", " WHERE phone IS NULL;"], .4, lt, a, .035)
        a2 = pr(lt, 1.8, 2.1) * fo
        result_box(d, 700, "3 rows selected ✓", GREEN, a2)
        # mini table
        a3 = pr(lt, 2.3, 2.7) * fo
        rows = [("101", "Əli"), ("205", "Leyla"), ("318", "Murad")]
        d.rounded_rectangle((140, 870, 940, 1200), 20, fill=mix(CARD, a3))
        for k, h in enumerate(["ID", "NAME", "PHONE"]):
            d.text((180 + k * 260, 890), h, font=MB(40), fill=mix(CYAN, a3))
        for r, (id_, nm) in enumerate(rows):
            y = 960 + r * 75
            d.text((180, y), id_, font=MN(40), fill=mix(WHITE, a3))
            d.text((440, y), nm, font=SN(40), fill=mix(WHITE, a3))
            d.text((700, y), "NULL", font=MB(40), fill=mix(PINK, a3))
        caption(d, "IS NULL müqayisə etmir, yoxlayır: 'dəyər bilinmirmi?' Cavab həmişə TRUE və ya FALSE olur.", pr(lt, 2.5, 2.9) * fo)

    elif t < T[6]:  # 6. NOT IN trap
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 260, "⚠ Ən təhlükəli tələ".replace("⚠ ", ""), SB(64), RED, a)
        ct(d, 345, "NOT IN + NULL", MB(56), YEL, a)
        code_box(d, 430, 690, ["SELECT * FROM clients", " WHERE id NOT IN (1, 2, NULL);"], .4, lt, a, .03)
        a2 = pr(lt, 1.9, 2.2) * fo
        result_box(d, 740, "0 rows selected", RED, a2, "Heç bir müştəri qaytarılmadı!")
        # expansion
        a3 = pr(lt, 3, 3.4) * fo
        ct(d, 960, "Oracle bunu belə oxuyur:", SN(44), DIM, a3)
        parts = [("id<>1", GREEN, "TRUE"), ("AND", CYAN, None), ("id<>2", GREEN, "TRUE"), ("AND", CYAN, None), ("id<>NULL", YEL, "UNKNOWN")]
        x = 75
        for k, (p_, c, r) in enumerate(parts):
            al = pr(lt, 3.4 + k * .3, 3.7 + k * .3) * fo
            f = MB(40); w = d.textlength(p_, font=f)
            d.text((x, 1040), p_, font=f, fill=mix(c if r is None else WHITE, al))
            if r: ct(d, 1100, r, SB(32), c, pr(lt, 5 + k * .2, 5.3 + k * .2) * fo, x + w / 2)
            x += w + 28
        a4 = pr(lt, 6.3, 6.7) * fo
        ct(d, 1190, "TRUE AND UNKNOWN = UNKNOWN", MB(46), YEL, a4)
        caption(d, "Siyahıda bircə NULL olsa, NOT IN heç vaxt TRUE vermir. Hesabatlar səssizcə boş çıxır!", pr(lt, 2.2, 2.6) * fo)

    elif t < T[7]:  # 7. rules
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 270, "Yadda saxla:", SB(72), WHITE, a)
        rules = [("= NULL", "IS NULL", "NULL yoxlamaq üçün"),
                 ("NOT IN", "NOT EXISTS", "NULL-a davamlıdır"),
                 ("NULL", "NVL(col, 0)", "əvəzedici dəyər ver")]
        for k, (bad, good, why) in enumerate(rules):
            y = 400 + k * 230; al = pr(lt, .4 + k * .5, .8 + k * .5) * fo
            d.rounded_rectangle((70, y, W - 70, y + 200), 26, fill=mix(CARD, al))
            d.text((110, y + 30), "✗ " + bad, font=MB(46), fill=mix(RED, al))
            d.text((530, y + 30), "✓ " + good, font=MB(46), fill=mix(GREEN, al))
            d.text((110, y + 115), why, font=SN(40), fill=mix(DIM, al))
        a2 = pr(lt, 2.4, 2.8) * fo
        d.rounded_rectangle((70, 1110, W - 70, 1250), 26, fill=mix((60, 40, 10), a2), outline=mix(YEL, a2), width=4)
        ct(d, 1125, "Oracle bonusu:", SB(40), YEL, a2)
        ct(d, 1180, "'' (boş sətir) da NULL sayılır!", SB(44), WHITE, a2)
        caption(d, "Bu 3 qayda NULL səhvlərinin böyük hissəsinin qarşısını alır.", pr(lt, 1.6, 2) * fo)

    else:  # 8. CTA
        lt = t - T[7]
        ct(d, 460, "Növbəti video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 560, "COUNT(*) vs COUNT(col)", MB(64), YEL, pr(lt, .2, .5))
        ct(d, 660, "Niyə fərqli rəqəm verir?", SB(56), WHITE, pr(lt, .4, .7))
        a = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 900, (W + bw) / 2, 900 + bh), 65, fill=mix(GREEN, a))
        ct(d, 900 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, a)
        ct(d, 1080, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v3_silent.mp4"], stdin=subprocess.PIPE)
snaps = [int((T[k] + (T[k + 1] - T[k]) * .8) * FPS) for k in range(8)]
for i in range(N):
    fr = frame(i); p.stdin.write(fr.tobytes())
    if i in snaps: fr.save(f"v3_{snaps.index(i)}.png")
p.stdin.close(); p.wait(); print("video done")

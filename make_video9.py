from common import *
from make_video5 import arrow, counter
import subprocess, math, sys

T = [0, 6, 16, 30, 44, 56, 68, 80, 90, 98, 104]
DUR = T[-1]; N = FPS * DUR

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

KW = {"SELECT", "FROM", "WHERE", "EXECUTE", "IMMEDIATE", "USING", "INTO", "OR", "ALTER", "SYSTEM", "SET"}
def code(d, y0, lines, t0, t, a, size=36, speed=.025):
    lh = int(size * 1.5); h = 85 + lh * len(lines) + 10
    d.rounded_rectangle((60, y0, W - 60, y0 + h), 24, fill=mix((16, 22, 42), a), outline=mix((50, 70, 120), a), width=3)
    for k, c in enumerate([PINK, YEL, GREEN]):
        d.ellipse((95 + k * 45, y0 + 25, 120 + k * 45, y0 + 50), fill=mix(c, a))
    full = "\n".join(lines); n = int(max(0, (t - t0) / speed)); shown = full[:n]
    yy = y0 + 78; f = MB(size)
    for line in shown.split("\n"):
        x = 95
        for word in line.split(" "):
            wd = word.strip("(),;*'")
            c = CYAN if wd in KW else PINK if word.startswith(":") else YEL if "'" in word else PURP if "||" in word else WHITE
            d.text((x, yy), word, font=f, fill=mix(c, a))
            x += d.textlength(word + " ", font=f)
        yy += lh
    return y0 + h

def qcard(d, cx, cy, txt, col, a, w=860, fs=32):
    d.rounded_rectangle((cx - w / 2, cy - 38, cx + w / 2, cy + 38), 16, fill=mix(CARD, a), outline=mix(col, a), width=4)
    ct(d, cy - fs * .62, txt, MB(fs), WHITE, a, cx)

def shelf(d, y0, cards, a, hl=None, newk=None, label="SHARED POOL (yaddaş)"):
    d.rounded_rectangle((60, y0, W - 60, y0 + 380), 24, fill=mix((14, 20, 38), a), outline=mix(PURP, a), width=4)
    d.text((90, y0 + 18), label, font=SB(34), fill=mix(PURP, a))
    for k, txt in enumerate(cards):
        r, c = divmod(k, 3); x = 90 + c * 305; y = y0 + 80 + r * 72
        if y > y0 + 330: continue
        col = GREEN if hl == k else YEL if newk == k else OFFB
        d.rounded_rectangle((x, y, x + 285, y + 60), 12, fill=mix(CARD, a), outline=mix(col, a), width=4 if col != OFFB else 2)
        ct(d, y + 14, txt, MN(26), WHITE, a, x + 142)

def badge(d, y, txt, col, a):
    w = d.textlength(txt, font=SB(50)) + 60
    d.rounded_rectangle(((W - w) / 2, y, (W + w) / 2, y + 90), 45, fill=mix(col, a))
    ct(d, y + 16, txt, SB(50), BG, a)

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, 0); a = pr(lt, 0, .3) * fo
        ct(d, 250, "Eyni sorğu, 10 000 dəfə...", SB(60), WHITE, a)
        for k in range(5):
            y = 400 + k * 95; al = pr(lt, .3 + k * .25, .6 + k * .25) * fo
            qcard(d, 540, y, f"SELECT * FROM clients WHERE id = {101 + k}", OFFB, al, fs=30)
        n = int(10000 * pr(lt, 1.2, 4.2) ** 1.4)
        counter(d, 900, "Hard parse:", f"{n:,}".replace(",", " "), RED, pr(lt, 1, 1.3) * fo, 120, 960)
        ab = pr(lt, 1.2, 1.5) * fo
        d.text((120, 1060), "CPU", font=SB(40), fill=mix(WHITE, ab))
        d.rounded_rectangle((230, 1065, 960, 1105), 20, fill=mix(OFFB, ab))
        d.rounded_rectangle((230, 1065, 230 + 730 * min(.97, .2 + .8 * pr(lt, 1.2, 4.2)), 1105), 20, fill=mix(RED, ab))
        ct(d, 1170, "Oracle hər dəfə sıfırdan başlayır!", SB(52), YEL, pr(lt, 4, 4.4) * fo)
        caption(d, "Problem sorğunun özündə deyil, onu NECƏ yazmağındadır. Gəl görək.", pr(lt, 4.2, 4.6) * fo)

    # 1 PIPELINE
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 250, "SQL gələndə Oracle nə edir?", SB(56), WHITE, a)
        steps = [("1. PARSE", "sintaksis, cədvəllər, icazələr", CYAN), ("2. OPTIMIZE", "ən yaxşı planı seç", YEL), ("3. EXECUTE", "icra et", GREEN)]
        for k, (h, s, c) in enumerate(steps):
            y = 380 + k * 220; al = pr(lt, .6 + k * 1.2, 1 + k * 1.2) * fo
            on = lt > 1 + k * 1.2
            d.rounded_rectangle((110, y, 970, y + 170), 26, fill=mix(CARD, al), outline=mix(c if on else OFFB, al), width=5)
            d.text((150, y + 30), h, font=MB(52), fill=mix(c, al))
            d.text((150, y + 105), s, font=SN(38), fill=mix(WHITE, al))
            if k < 2: arrow(d, 540, y + 175, 540, y + 215, DIM, al, 5)
        ab = pr(lt, 5, 5.4) * fo
        d.rounded_rectangle((110, 1060, 970, 1250), 26, fill=mix((70, 18, 28), ab), outline=mix(RED, ab), width=4)
        ct(d, 1080, "HARD PARSE = 1 + 2 + 3", MB(46), RED, ab)
        ct(d, 1160, "Ən baha addımlar: parse və optimize", SN(38), WHITE, ab)
        caption(d, "Hər yeni sorğu üçün Oracle onu təhlil edir və plan qurur. Bu, CPU və kilid baxımından bahalıdır.", pr(lt, 1.2, 1.6) * fo)

    # 2 SHARED POOL
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Oracle-ın yaddaşı: SHARED POOL", SB(52), PURP, a)
        q = "WHERE id = :id"
        k = 0 if lt < 7 else 1; pl = lt - (1 if k == 0 else 7.5)
        cards = ["…status = 'A'", "…branch = :b"] + ([q] if (k == 1 or pl > 3.2) else [])
        qy = 400 + 160 * pr(pl, 0, 1)
        if pl > 0: qcard(d, 540, qy, "SELECT * FROM clients " + q, CYAN, a * (1 - pr(pl, 4.6, 5)), fs=30)
        ah = pr(pl, 1, 1.3) * fo
        if pl > 1 and pl < 5:
            ct(d, 640, "hash(mətn) → yaddaşda axtar...", MN(38), YEL, ah)
        hit = k == 1
        res_a = pr(pl, 2.4, 2.7) * fo
        shelf(d, 760, cards, a, hl=2 if (hit and pl > 2.4) else None, newk=2 if (not hit and pl > 3.2) else None)
        if pl > 2.4:
            badge(d, 1180, "SOFT PARSE ✓  plan hazırdır" if hit else "TAPILMADI → HARD PARSE", GREEN if hit else RED, res_a)
        caps = ["Oracle hazır planları SHARED POOL-da saxlayır. Açar: sorğunun DƏQİQ mətni.",
                "İlk dəfə: mətn yaddaşda yoxdur → hard parse, sonra plan yaddaşa yazılır.",
                "İkinci dəfə: eyni mətn tapıldı → soft parse. Plan hazırdır, çox sürətlidir!"]
        caption(d, caps[0 if lt < 2.5 else 1 if k == 0 else 2], pr(lt, .6, 1) * fo)

    # 3 LITERALS
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Problem: LİTERAL dəyərlər", SB(56), RED, a)
        n = min(11, int(max(0, lt - .8) / 1.1) + 1) if lt > .8 else 0
        cur = 100 + n
        if n: qcard(d, 540, 400, f"SELECT * FROM clients WHERE id = {cur}", RED, a, fs=30)
        if n: ct(d, 470, "mətn fərqlidir → yeni hash → TAPILMADI", SN(36), YEL, a)
        cards = [f"…id = {101 + j}" for j in range(n)]
        shelf(d, 560, cards, a, newk=n - 1 if n else None)
        counter(d, 980, "Hard parse:", str(n if lt < 13 else 10000), RED, pr(lt, .8, 1.1) * fo, 120, 960)
        ct(d, 1130, "Yaddaş eyni sorğunun surətləri ilə dolur!", SB(42), YEL, pr(lt, 6, 6.4) * fo)
        caption(d, "101, 102, 103... Hər rəqəm mətni dəyişir. Oracle hər birini yeni sorğu sayır və yenidən plan qurur.", pr(lt, 1, 1.4) * fo)

    # 4 BIND VARIABLES
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Həll: BIND dəyişənləri", SB(58), GREEN, a)
        n = min(8, int(max(0, lt - 1.5) / 1.2) + 1) if lt > 1.5 else 0
        qcard(d, 540, 390, "SELECT * FROM clients WHERE id = :id", GREEN, pr(lt, .4, .8) * fo, fs=30)
        if n: ct(d, 455, f":id = {100 + n}   (dəyər ayrıca ötürülür)", MN(34), YEL, a)
        pulse = n and ((lt - 1.5) % 1.2) < .5
        shelf(d, 540, ["…id = :id"], a, hl=0 if pulse else None)
        counter(d, 960, "Hard parse:", "1", GREEN, pr(lt, 1, 1.3) * fo, 120, 960)
        counter(d, 1100, "Soft parse:", str(max(0, n - 1)) if lt < 11 else "9 999", GREEN, pr(lt, 1.2, 1.5) * fo, 120, 960)
        caption(d, "Mətn həmişə eynidir, yalnız dəyər dəyişir. Bir plan, minlərlə istifadə!", pr(lt, 1.5, 1.9) * fo)

    # 5 COMPARISON
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 250, "10 000 sorğu:", SB(64), WHITE, a)
        base = 1000
        for k, (lab, v, col, h) in enumerate([("Literal", "10 000", RED, 520), ("Bind", "1", GREEN, 8)]):
            x = 230 + k * 420; al = pr(lt, .4 + k * .4, .8 + k * .4) * fo
            hh = max(8, h * pr(lt, .6 + k * .4, 1.8 + k * .4))
            d.rounded_rectangle((x, base - hh, x + 200, base), 16, fill=mix(col, al))
            ct(d, base - hh - 80, v, MB(58), col, al, x + 100)
            ct(d, base + 20, lab, SB(44), WHITE, al, x + 100)
        ct(d, base + 85, "hard parse", SN(38), DIM, a)
        rows = [("CPU", "çox yüklənir", "rahat"), ("Shared pool", "doludur", "təmiz"), ("Miqyas", "yavaşlayır", "böyüyür")]
        for j, (h, b1, b2) in enumerate(rows):
            y = 1170 + j * 70; al = pr(lt, 3 + j * .5, 3.4 + j * .5) * fo
            d.text((90, y), h, font=SB(38), fill=mix(WHITE, al))
            d.text((430, y), "✗ " + b1, font=SN(36), fill=mix(RED, al))
            d.text((740, y), "✓ " + b2, font=SN(36), fill=mix(GREEN, al))
        caption(d, "Çox istifadəçili sistemlərdə (məs. bank) bu fərq sistemin dayanması ilə rahat işləməsi arasındakı fərqdir.", pr(lt, 2, 2.4) * fo)

    # 6 SQL INJECTION
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Bonus: TƏHLÜKƏSİZLİK", SB(58), RED, a)
        y = code(d, 330, ["EXECUTE IMMEDIATE", "  'SELECT * FROM clients", "    WHERE name = ''' || p_name || '''';"], .4, lt, a, 32, .02)
        ai = pr(lt, 2.6, 3) * fo
        d.text((90, y + 25), "p_name =", font=MB(36), fill=mix(WHITE, ai))
        d.text((300, y + 25), "x' OR '1'='1", font=MB(36), fill=mix(RED, ai))
        ar = pr(lt, 3.8, 4.2) * fo
        d.rounded_rectangle((60, y + 90, W - 60, y + 200), 22, fill=mix((70, 18, 28), ar), outline=mix(RED, ar), width=4)
        ct(d, y + 120, "BÜTÜN müştərilər qaytarıldı!", SB(44), RED, ar)
        ab = pr(lt, 6, 6.4) * fo
        y2 = code(d, y + 230, ["EXECUTE IMMEDIATE", "  'SELECT * FROM clients WHERE name = :n'", "  USING p_name;"], 6.2, lt, ab, 30, .02)
        ct(d, y2 + 20, "✓ Dəyər həmişə DƏYƏR kimi qalır", SB(42), GREEN, pr(lt, 8.5, 8.9) * fo)
        caps = ["Mətni birləşdirmək (||) təhlükəlidir. Daxil edilən dəyər SQL-in bir hissəsinə çevrilir.",
                "Bu, SQL INJECTION-dır: hücumçu sorğunun məntiqini dəyişir.",
                "Bind dəyişəni ilə dəyər heç vaxt kod kimi icra olunmur. Sürət + təhlükəsizlik!"]
        caption(d, caps[0 if lt < 3.8 else 1 if lt < 6 else 2], pr(lt, .8, 1.2) * fo)

    # 7 PL/SQL GOOD NEWS
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 240, "PL/SQL-də yaxşı xəbər", SB(58), GREEN, a)
        y = code(d, 330, ["SELECT balance INTO v_bal", "  FROM accounts", " WHERE id = p_id;"], .4, lt, a, 38, .025)
        ag = pr(lt, 2, 2.4) * fo
        ct(d, y + 25, "p_id avtomatik BIND olur ✓", SB(44), GREEN, ag)
        aw = pr(lt, 4, 4.4) * fo
        d.rounded_rectangle((70, y + 110, W - 70, y + 330), 22, fill=mix((60, 40, 10), aw), outline=mix(YEL, aw), width=4)
        d.text((105, y + 130), "Risk harada?", font=SB(42), fill=mix(YEL, aw))
        d.text((105, y + 195), "• Dinamik SQL: EXECUTE IMMEDIATE + ||", font=SN(36), fill=mix(WHITE, aw))
        d.text((105, y + 250), "• Java / .NET / Python kodunda birləşdirmə", font=SN(36), fill=mix(WHITE, aw))
        ac = pr(lt, 6.5, 6.9) * fo
        d.rounded_rectangle((70, y + 360, W - 70, y + 470), 22, fill=mix(CARD, ac))
        d.text((105, y + 380), "CURSOR_SHARING = FORCE", font=MB(36), fill=mix(PURP, ac))
        d.text((105, y + 428), "təcili yamaqdır, əsl həll deyil", font=SN(32), fill=mix(DIM, ac))
        caption(d, "Statik PL/SQL-də dəyişənlər özü bind olur. Problem dinamik SQL-də və tətbiq kodunda yaranır.", pr(lt, 1.2, 1.6) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Yadda saxla:", SB(66), WHITE, a)
        items = [("Literal", "→ hər dəfə hard parse"), ("Bind :id", "→ bir plan, min istifadə"),
                 ("Shared pool", "→ mətnə görə axtarır"), ("|| birləşdirmə", "→ SQL injection riski"),
                 ("USING", "→ dinamik SQL-də bind")]
        for k, (q, ex) in enumerate(items):
            y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
            d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
            d.text((105, y + 30), q, font=MB(38), fill=mix(GREEN, al))
            d.text((480, y + 32), ex, font=SN(38), fill=mix(WHITE, al))
        caption(d, "Bind dəyişənləri: daha sürətli, daha təhlükəsiz, daha az yaddaş.", pr(lt, 2, 2.4) * fo)

    # 9 CTA
    else:
        lt = t - T[9]
        ct(d, 440, "Növbəti video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 540, "UNDO sirri", SB(72), YEL, pr(lt, .2, .5))
        ct(d, 650, "Oxuyan yazana niyə mane olmur?", SB(46), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.8, T[1] + 6, T[2] + 4.5, T[2] + 11, T[3] + 8, T[4] + 7, T[5] + 5, T[6] + 5, T[6] + 10, T[7] + 8, T[8] + 5, T[9] + 3]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v9_{k}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v9_silent.mp4"], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print("video done")

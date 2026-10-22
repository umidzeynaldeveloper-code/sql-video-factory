from common import *
from make_video5 import arrow, counter
import subprocess, math, sys

T = [0, 6, 14, 34, 42, 64, 78, 88, 98, 104]
DUR = T[-1]; N = FPS * DUR

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

KW = {"SELECT", "FROM", "WHERE", "JOIN", "ON", "FOR", "IN", "LOOP", "END"}
def code(d, y0, lines, t0, t, a, size=38, speed=.028):
    lh = int(size * 1.5); h = 90 + lh * len(lines) + 10
    d.rounded_rectangle((60, y0, W - 60, y0 + h), 26, fill=mix((16, 22, 42), a), outline=mix((50, 70, 120), a), width=3)
    for k, c in enumerate([PINK, YEL, GREEN]):
        d.ellipse((95 + k * 45, y0 + 25, 120 + k * 45, y0 + 50), fill=mix(c, a))
    full = "\n".join(lines); n = int(max(0, (t - t0) / speed)); shown = full[:n]
    yy = y0 + 80; f = MB(size)
    for line in shown.split("\n"):
        x = 95
        for word in line.split(" "):
            wd = word.strip("(),;*")
            c = CYAN if wd in KW else PURP if "/*+" in word or "USE_" in word or "*/" in word else WHITE
            d.text((x, yy), word, font=f, fill=mix(c, a))
            x += d.textlength(word + " ", font=f)
        yy += lh
    return y0 + h

CLIENTS = [(101, "Əli"), (205, "Leyla"), (318, "Murad")]
ACCS = [(101, "AZ01"), (318, "AZ02"), (205, "AZ03"), (101, "AZ04"), (412, "AZ05"), (318, "AZ06"), (520, "AZ07"), (101, "AZ08")]

def mini_table(d, x0, y0, x1, title, rows, a, hl=None, green=(), dim=(), rh=52, tcol=CYAN):
    h = 70 + rh * len(rows) + 10
    d.rounded_rectangle((x0, y0, x1, y0 + h), 18, fill=mix(CARD, a))
    d.text((x0 + 20, y0 + 16), title, font=SB(32), fill=mix(tcol, a))
    for r, row in enumerate(rows):
        y = y0 + 70 + r * rh
        if r == hl: d.rounded_rectangle((x0 + 8, y - 4, x1 - 8, y + rh - 8), 10, fill=mix((80, 68, 20), a))
        if r in green: d.rounded_rectangle((x0 + 8, y - 4, x1 - 8, y + rh - 8), 10, fill=mix((20, 80, 55), a))
        al = a * (.35 if r in dim else 1)
        d.text((x0 + 25, y + 4), str(row[0]), font=MB(34), fill=mix(YEL if r == hl else WHITE, al))
        d.text((x0 + 140, y + 4), str(row[1]), font=SN(34), fill=mix(WHITE, al))
    return y0 + h

def chip(d, cx, cy, txt, col, a, fs=32):
    w = d.textlength(txt, font=MB(fs)) + 30
    d.rounded_rectangle((cx - w / 2, cy - 26, cx + w / 2, cy + 26), 14, fill=mix(col, a))
    ct(d, cy - fs * .62, txt, MB(fs), BG, a, cx)

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    # 1 HOOK
    if t < T[1]:
        lt, fo = sc(t, 0); a = pr(lt, 0, .3) * fo
        ct(d, 270, "JOIN yazırsan...", SB(70), WHITE, a)
        ct(d, 370, "Bəs Oracle iki cədvəli", SB(56), DIM, pr(lt, .5, .9) * fo)
        ct(d, 440, "NECƏ birləşdirir?", SB(70), YEL, pr(lt, .8, 1.2) * fo)
        items = [("NESTED LOOPS", "iç-içə dövr", CYAN), ("HASH JOIN", "kovalar", GREEN), ("MERGE JOIN", "fermuar", PINK)]
        for k, (n, s, c) in enumerate(items):
            y = 600 + k * 170; al = pr(lt, 1.6 + k * .5, 2 + k * .5) * fo
            d.rounded_rectangle((110, y, 970, y + 140), 30, fill=mix(CARD, al), outline=mix(c, al), width=5)
            d.text((150, y + 35), n, font=MB(56), fill=mix(c, al))
            tw = d.textlength(s, font=SN(40)); d.text((930 - tw, y + 48), s, font=SN(40), fill=mix(WHITE, al))
        caption(d, "Eyni sorğu, 3 fərqli alqoritm. Səhv seçim = saniyə yerinə saatlar.", pr(lt, 3.6, 4) * fo)

    # 2 SETUP
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Sorğumuz:", SB(60), WHITE, a)
        y = code(d, 330, ["SELECT c.name, a.acc_no", "  FROM clients c", "  JOIN accounts a", "    ON a.client_id = c.id;"], .4, lt, a, 40, .025)
        ab = pr(lt, 3, 3.4) * fo
        mini_table(d, 70, y + 40, 480, "CLIENTS", CLIENTS, ab)
        mini_table(d, 540, y + 40, 1010, "ACCOUNTS", ACCS[:4] + [("...", "")], ab)
        ct(d, y + 440, "3 müştəri", SB(40), CYAN, pr(lt, 3.6, 4) * fo, 275)
        ct(d, y + 440, "5 000 000 hesab", SB(40), PINK, pr(lt, 3.8, 4.2) * fo, 775)
        caption(d, "Kiçik cədvəl və böyük cədvəl. Hər hesabı öz müştərisi ilə birləşdirmək lazımdır.", pr(lt, 4, 4.4) * fo)

    # 3 NESTED LOOPS
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 250, "1. NESTED LOOPS", MB(60), CYAN, a)
        ct(d, 330, "Hər sətir üçün, digər cədvələ get", SN(42), WHITE, a)
        k = min(2, int(max(0, lt - 2) / 5.5)) if lt > 2 else -1
        pl = lt - 2 - k * 5.5 if k >= 0 else 0
        hl = k if k >= 0 else None
        cid = CLIENTS[k][0] if k >= 0 else None
        matches = [r for r, ac in enumerate(ACCS) if ac[0] == cid] if (k >= 0 and pl > 1.6) else []
        done_clients = set(range(k)) if k >= 0 else set()
        mini_table(d, 70, 400, 480, "CLIENTS (xarici)", CLIENTS, a, hl=hl, dim=done_clients)
        mini_table(d, 540, 400, 1010, "ACCOUNTS (indeksli)", ACCS, a, green=matches, tcol=PINK)
        if k >= 0 and pl > .8:
            ay = 400 + 70 + k * 52 + 22; aa = pr(pl, .8, 1.2) * fo
            targets = [r for r, ac in enumerate(ACCS) if ac[0] == cid]
            for r in targets:
                arrow(d, 470, ay, 555, 400 + 70 + r * 52 + 22, YEL, aa, 4)
        y = code(d, 900, ["FOR c IN clients LOOP", "  -- indeksdə c.id-ni axtar", "END LOOP;"], .6, lt, a, 38, .03)
        lookups = 0 if k < 0 else k + (1 if pl > .8 else 0)
        counter(d, y + 20, "İndeks müraciəti:", str(lookups), CYAN, pr(lt, 1.6, 2) * fo, 120, 960)
        names = ["Əli", "Leyla", "Murad"]
        cap = ("Xarici cədvəldən 1 sətir götür, indekslə daxili cədvəldə uyğunlarını tap, sonra növbəti sətrə keç." if k < 0
               else f"{names[k]} ({cid}) → indeks → {len([1 for ac in ACCS if ac[0] == cid])} hesab tapıldı. Növbəti müştəri...")
        if lt > 18.5: cap = "3 müştəri = cəmi 3 indeks müraciəti. Xarici cədvəl kiçikdirsə, NL ən sürətlisidir!"
        caption(d, cap, pr(lt, 1, 1.4) * fo)

    # 4 NL BAD
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 260, "Bəs xarici cədvəl böyük olsa?", SB(56), RED, a)
        ct(d, 360, "1 000 000 müştəri", MB(56), WHITE, a)
        n = int(1_000_000 * (pr(lt, 1, 5.5) ** 1.5))
        counter(d, 500, "İndeks müraciəti:", f"{n:,}".replace(",", " "), RED, pr(lt, .6, 1) * fo, 100, 980)
        # many arrows burst
        ab = pr(lt, 1, 1.5) * fo
        for j in range(int(28 * pr(lt, 1, 5))):
            y = 700 + (j * 37) % 300
            arrow(d, 150 + (j * 53) % 120, y, 860 - (j * 31) % 120, y + ((j * 17) % 40 - 20), RED, ab * .6, 3)
        ct(d, 1060, "→ çox yavaş 🐢".replace(" 🐢", ""), SB(56), RED, pr(lt, 5, 5.4) * fo)
        caption(d, "Milyonlarla kiçik oxuma. Böyük dəstlər üçün Oracle başqa üsul seçir: HASH JOIN.", pr(lt, 2, 2.4) * fo)

    # 5 HASH JOIN
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 250, "2. HASH JOIN", MB(60), GREEN, a)
        phase = 1 if lt < 8.3 else 2 if lt < 17.5 else 3
        sub = {1: "Mərhələ 1: BUILD (kiçik cədvəldən)", 2: "Mərhələ 2: PROBE (böyük cədvəli yoxla)", 3: "Nəyi bilmək lazımdır:"}[phase]
        ct(d, 330, sub, SB(42), YEL, a)
        bx = [70 + k * 240 for k in range(4)]
        BY = 760
        # buckets
        for b in range(4):
            d.rounded_rectangle((bx[b], BY, bx[b] + 210, BY + 260), 20, fill=mix(CARD, a), outline=mix(OFFB, a), width=4)
            ct(d, BY - 52, f"kova {b}", SB(32), DIM, a, bx[b] + 105)
        slots = {}
        placed = []
        for k, (cid, nm) in enumerate(CLIENTS):
            b = cid % 4; s = slots.get(b, 0); slots[b] = s + 1
            placed.append((k, b, s))
        if phase == 1:
            mini_table(d, 70, 400, 480, "CLIENTS", CLIENTS, a, dim={k for k in range(3) if lt > 1 + k * 2.2})
        for k, b, s in placed:
            st = 1 + k * 2.2; p = pr(lt, st + .6, st + 1.6)
            if lt < st: continue
            sx, sy = 260, 400 + 70 + k * 52 + 22
            tx, ty = bx[b] + 105, BY + 50 + s * 70
            cx, cy = sx + (tx - sx) * p, sy + (ty - sy) * p - 120 * math.sin(math.pi * p)
            chip(d, cx, cy, f"{CLIENTS[k][0]}", CYAN, a)
            if phase == 1 and lt < st + 1.8:
                ct(d, 470, f"{CLIENTS[k][0]} % 4 = {b}", MB(46), YEL, pr(lt, st, st + .3) * fo, 780)
        # PROBE
        if phase >= 2:
            probe = [ACCS[0], ACCS[1], ACCS[2], ACCS[4], ACCS[6]]
            q = min(4, int((lt - 8.3) / 1.8)); pl = lt - 8.3 - q * 1.8
            cid, acc = probe[q]; b = cid % 4
            hit = b in slots and any(CLIENTS[k][0] == cid for k, bb, s in placed)
            if phase == 2:
                d.rounded_rectangle((70, 400, 1010, 560), 22, fill=mix(CARD, a), outline=mix(PINK, a), width=4)
                d.text((100, 415), "ACCOUNTS axını →", font=SB(32), fill=mix(PINK, a))
                d.text((100, 470), f"{cid} | {acc}", font=MB(52), fill=mix(WHITE, a))
                ap = pr(pl, .3, .6) * fo
                tw = f"{cid} % 4 = {b}"; d.text((980 - d.textlength(tw, font=MB(48)), 472), tw, font=MB(48), fill=mix(YEL, ap))
                aa = pr(pl, .6, .9) * fo
                arrow(d, 800, 565, bx[b] + 105, BY - 60, YEL, aa, 6)
                ar = pr(pl, .9, 1.2) * fo
                d.rounded_rectangle((bx[b], BY, bx[b] + 210, BY + 260), 20, outline=mix(GREEN if hit else RED, ar), width=8)
                res = f"✓ {cid} → {dict(CLIENTS)[cid]}" if hit else f"✗ {cid}: uyğun yoxdur, keç"
                ct(d, 1080, res, SB(50), GREEN if hit else RED, ar)
            else:
                notes = [("✓", "Hər cədvəl yalnız 1 dəfə oxunur", GREEN), ("✓", "Böyük dəstlər üçün ən sürətli", GREEN),
                         ("!", "Yalnız bərabərlik (=) şərti", YEL), ("!", "Hash cədvəli yaddaşda (PGA) qurulur", YEL)]
                for j, (ic, tx, c) in enumerate(notes):
                    al = pr(lt, 17.7 + j * .5, 18.1 + j * .5) * fo
                    d.rounded_rectangle((70, 400 + j * 75, W - 70, 465 + j * 75), 14, fill=mix(CARD, al))
                    d.text((100, 410 + j * 75), ic, font=SB(40), fill=mix(c, al))
                    d.text((150, 413 + j * 75), tx, font=SN(36), fill=mix(WHITE, al))
        caps = {1: "Kiçik cədvəlin hər sətri üçün hash hesablanır və sətir uyğun kovaya qoyulur. Qarderobdakı nömrəli asılqanlar kimi.",
                2: "Böyük cədvəl bir dəfə oxunur. Hər sətir üçün hash hesablanır və birbaşa öz kovasına baxılır. Axtarış yoxdur!",
                3: "Yaddaşa sığmasa, TEMP-ə yazılır və yavaşlayır. Kiçik cədvəli BUILD tərəfinə qoymaq vacibdir."}
        caption(d, caps[phase], pr(lt, 1, 1.4) * fo)

    # 6 MERGE JOIN
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 250, "3. MERGE JOIN", MB(60), PINK, a)
        ct(d, 330, "İki sıralı siyahı, fermuar kimi", SN(42), WHITE, a)
        L = [101, 205, 318]; R = [101, 101, 205, 318, 318, 520]
        steps = []; i_, j_ = 0, 0
        while i_ < len(L) and j_ < len(R):
            if L[i_] == R[j_]: steps.append((i_, j_, True)); j_ += 1
            elif L[i_] < R[j_]: steps.append((i_, j_, False)); i_ += 1
            else: steps.append((i_, j_, False)); j_ += 1
        cur = min(len(steps) - 1, int((lt - 1.5) / .8)) if lt > 1.5 else -1
        lx, rx = 270, 810; ly = 470
        ct(d, 395, "CLIENTS ↑ sıralı", SB(32), CYAN, a, lx); ct(d, 395, "ACCOUNTS ↑ sıralı", SB(32), PINK, a, rx)
        for k, v in enumerate(L):
            y = ly + k * 90
            d.rounded_rectangle((lx - 110, y, lx + 110, y + 70), 14, fill=mix(CARD, a))
            ct(d, y + 12, str(v), MB(40), WHITE, a, lx)
        for k, v in enumerate(R):
            y = ly + k * 90
            d.rounded_rectangle((rx - 110, y, rx + 110, y + 70), 14, fill=mix(CARD, a))
            ct(d, y + 12, str(v), MB(40), WHITE, a, rx)
        for s in range(cur + 1):
            i2, j2, m = steps[s]
            if m: d.line((lx + 110, ly + i2 * 90 + 35, rx - 110, ly + j2 * 90 + 35), fill=mix(GREEN, a), width=6)
        if cur >= 0:
            i2, j2, m = steps[cur]
            for (x, idx) in ((lx - 150, i2), (rx + 150, j2)):
                y = ly + idx * 90 + 35; s_ = -1 if x < 540 else 1
                d.polygon([(x - 25 * s_, y), (x + 15 * s_, y - 22), (x + 15 * s_, y + 22)], fill=mix(YEL, a))
            msg = "= uyğun ✓" if m else ("sol < sağ → sol irəli" if L[i2] < R[j2] else "sol > sağ → sağ irəli")
            ct(d, 1030, msg, SB(46), GREEN if m else YEL, a)
        an = pr(lt, 9, 9.4) * fo
        d.rounded_rectangle((70, 1110, W - 70, 1330), 22, fill=mix(CARD, an))
        d.text((100, 1130), "! Əvvəlcə hər iki tərəf SIRALANMALIDIR", font=SN(36), fill=mix(YEL, an))
        d.text((100, 1190), "✓ >, <, BETWEEN şərtləri ilə də işləyir", font=SN(36), fill=mix(GREEN, an))
        d.text((100, 1250), "✓ Məlumat artıq sıralıdırsa, çox effektivdir", font=SN(36), fill=mix(GREEN, an))
        caption(d, "Göstəricilər geri qayıtmadan irəliləyir. Hər siyahı yalnız bir dəfə keçilir.", pr(lt, 1.2, 1.6) * fo)

    # 7 COMPARISON
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .3) * fo
        ct(d, 260, "Hansı nə vaxt?", SB(64), WHITE, a)
        cards = [("NESTED LOOPS", CYAN, ["Kiçik xarici dəst", "Daxili cədvəldə indeks", "OLTP: 1 müştərinin hesabları"]),
                 ("HASH JOIN", GREEN, ["Böyük, sırasız dəstlər", "Yalnız = şərti", "Hesabatlar, EOD prosesləri"]),
                 ("MERGE JOIN", PINK, ["Sıralı məlumat", ">, <, BETWEEN şərtləri", "Tarix aralığı birləşmələri"])]
        for k, (n, c, lines) in enumerate(cards):
            y = 370 + k * 300; al = pr(lt, .3 + k * .6, .7 + k * .6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 270), 26, fill=mix(CARD, al), outline=mix(c, al), width=4)
            d.text((105, y + 22), n, font=MB(48), fill=mix(c, al))
            for j, ln in enumerate(lines):
                d.text((115, y + 95 + j * 56), "• " + ln, font=SN(38), fill=mix(WHITE, al))
        caption(d, "Heç biri 'həmişə yaxşı' deyil. Hər biri öz vəziyyəti üçündür.", pr(lt, 2.2, 2.6) * fo)

    # 8 OPTIMIZER + HINTS
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Kim seçir? Optimizator!", SB(60), WHITE, a)
        ab = pr(lt, .6, 1) * fo
        d.rounded_rectangle((70, 340, W - 70, 520), 24, fill=mix((70, 18, 28), ab), outline=mix(RED, ab), width=4)
        d.text((105, 360), "E-Rows = 1  →  NESTED LOOPS seçdi", font=MB(36), fill=mix(WHITE, ab))
        d.text((105, 430), "real 1 000 000 sətir → saatlarla ✗", font=MB(36), fill=mix(RED, ab))
        ag = pr(lt, 2.6, 3) * fo
        d.rounded_rectangle((70, 550, W - 70, 680), 24, fill=mix((14, 50, 36), ag), outline=mix(GREEN, ag), width=4)
        d.text((105, 585), "Statistika yeniləndi → HASH JOIN ✓", font=MB(36), fill=mix(GREEN, ag))
        y = code(d, 720, ["SELECT /*+ USE_HASH(a) */ ...", "SELECT /*+ USE_NL(a) */ ..."], 4.5, lt, pr(lt, 4.3, 4.6) * fo, 40, .03)
        ah = pr(lt, 6.4, 6.8) * fo
        ct(d, y + 30, "Hint = son çarə. Əvvəlcə statistikanı düzəlt!", SB(40), YEL, ah)
        caption(d, "Optimizator seçimi sətir sayının təxmininə görə edir. Təxmin səhvdirsə, seçim də səhvdir.", pr(lt, 1, 1.4) * fo)

    # 9 CTA
    else:
        lt = t - T[8]
        ct(d, 330, "Yadda saxla:", SB(60), WHITE, pr(lt, 0, .3))
        for k, (n, s, c) in enumerate([("NL", "az sətir + indeks", CYAN), ("HASH", "çox sətir + =", GREEN), ("MERGE", "sıralı + aralıq", PINK)]):
            al = pr(lt, .2 + k * .2, .5 + k * .2)
            d.text((150, 430 + k * 80), n, font=MB(48), fill=mix(c, al))
            d.text((420, 436 + k * 80), "→ " + s, font=SN(42), fill=mix(WHITE, al))
        ct(d, 730, "Növbəti video:", SB(50), DIM, pr(lt, 1, 1.3))
        ct(d, 800, "DEADLOCK: iki tranzaksiya", SB(54), YEL, pr(lt, 1.2, 1.5))
        ct(d, 870, "bir-birini gözləyəndə", SB(54), YEL, pr(lt, 1.2, 1.5))
        ap = pr(lt, 1.8, 2.2); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 1000, (W + bw) / 2, 1000 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 1000 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1170, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 2.2, 2.6))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.5, T[1] + 5, T[2] + 4.5, T[2] + 14, T[3] + 6, T[4] + 5, T[4] + 10, T[4] + 19.5, T[5] + 6, T[6] + 5, T[7] + 8, T[8] + 4]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v7_{k}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v7_silent.mp4"], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print("video done")

from common import *
import subprocess, math, random

T = [0, 6, 16, 29, 39, 57, 65, 74, 91, 101, 107, 113]
DUR = T[-1]; N = FPS * DUR

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def code(d, y0, lines, t0, t, a, size=42, speed=.03, h=None):
    lh = int(size * 1.5)
    h = h or (90 + lh * len(lines) + 20)
    d.rounded_rectangle((60, y0, W - 60, y0 + h), 26, fill=mix((16, 22, 42), a), outline=mix((50, 70, 120), a), width=3)
    for k, c in enumerate([PINK, YEL, GREEN]):
        d.ellipse((95 + k * 45, y0 + 25, 120 + k * 45, y0 + 50), fill=mix(c, a))
    full = "\n".join(lines); n = int(max(0, (t - t0) / speed)); shown = full[:n]
    KW = {"SELECT", "FROM", "WHERE", "CREATE", "INDEX", "ON", "LIKE", "IS", "NULL", "AND", "UNIQUE"}
    yy = y0 + 80
    f = MB(size)
    for line in shown.split("\n"):
        x = 95
        for word in line.split(" "):
            wd = word.strip("(),;*")
            c = PINK if wd == "NULL" else CYAN if wd.upper() in KW and wd.isupper() else YEL if "'" in word else PURP if "(" in word and wd.upper() == wd and wd.isalpha() else WHITE
            if wd in ("UPPER", "TO_NUMBER"): c = PURP
            d.text((x, yy), word, font=f, fill=mix(c, a))
            x += d.textlength(word + " ", font=f)
        yy += lh
    return y0 + h

def node(d, x, y, w, h, keys, a, hl=None, col=CYAN, fs=34):
    d.rounded_rectangle((x - w / 2, y, x + w / 2, y + h), 16, fill=mix(CARD, a), outline=mix(col, a), width=4)
    cw = w / len(keys)
    for k, key in enumerate(keys):
        cx = x - w / 2 + cw * (k + .5)
        if hl == k:
            d.rounded_rectangle((x - w / 2 + cw * k + 6, y + 6, x - w / 2 + cw * (k + 1) - 6, y + h - 6), 12, fill=mix(YEL, a))
        ct(d, y + h / 2 - fs * .62, key, MB(fs), BG if hl == k else WHITE, a, cx)
        if k: d.line((x - w / 2 + cw * k, y + 8, x - w / 2 + cw * k, y + h - 8), fill=mix(OFFB, a), width=2)

def arrow(d, x0, y0, x1, y1, col, a, width=6):
    d.line((x0, y0, x1, y1), fill=mix(col, a), width=width)
    ang = math.atan2(y1 - y0, x1 - x0); L = 22
    for s in (-.45, .45):
        d.line((x1, y1, x1 - L * math.cos(ang + s), y1 - L * math.sin(ang + s)), fill=mix(col, a), width=width)

def blocks_grid(d, y0, a, scanned=0, target=None, hit=False, cols=12, rows=10):
    s = 66; gap = 10; x0 = (W - (cols * s + (cols - 1) * gap)) / 2
    for r in range(rows):
        for c in range(cols):
            k = r * cols + c
            x = x0 + c * (s + gap); y = y0 + r * (s + gap)
            fill = CARD
            if k < scanned: fill = (70, 90, 135)
            if k == scanned and scanned < cols * rows: fill = YEL
            if target is not None and k == target and hit: fill = GREEN
            d.rounded_rectangle((x, y, x + s, y + s), 8, fill=mix(fill, a))
    return x0, s, gap

def counter(d, y, label, val, col, a, x0=160, x1=920):
    d.rounded_rectangle((x0, y, x1, y + 120), 26, fill=mix((16, 22, 42), a), outline=mix(col, a), width=4)
    d.text((x0 + 35, y + 38), label, font=SB(42), fill=mix(WHITE, a))
    w = d.textlength(val, font=MB(70)); d.text((x1 - 35 - w, y + 20), val, font=MB(70), fill=mix(col, a))

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    # 1. HOOK
    if t < T[1]:
        lt, fo = sc(t, 0); a = pr(lt, 0, .3) * fo
        ct(d, 270, "1 000 000 müştəri", SB(70), WHITE, a)
        ct(d, 365, "client_no = 777777 tap", MB(50), CYAN, a)
        for k, (lab, col, dur, res) in enumerate([("İndekssiz", RED, 3.6, "10 000 blok"), ("İndekslə", GREEN, .25, "4 blok")]):
            y = 520 + k * 260; al = pr(lt, .5, .8) * fo
            d.text((90, y), lab, font=SB(50), fill=mix(col, al))
            d.rounded_rectangle((90, y + 80, 990, y + 150), 35, fill=mix(OFFB, al))
            p = pr(lt, 1, 1 + dur) if k == 0 else min(1, max(0, (lt - 1) / dur))
            if p > 0: d.rounded_rectangle((90, y + 80, 90 + 900 * p, y + 150), 35, fill=mix(col, al))
            if p >= 1: d.text((620, y), res + " ✓", font=SB(44), fill=mix(col, al))
        ct(d, 1080, "Bu fərq necə yaranır?", SB(66), YEL, pr(lt, 4.4, 4.8) * fo)
        caption(d, "Eyni sorğu, eyni cədvəl. Sirr: İNDEKS. Gəl başdan-sona görək necə işləyir.", pr(lt, 4.5, 4.9) * fo)

    # 2. BOOK
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 260, "Təsəvvür et: 500 səhifəlik kitab", SB(54), WHITE, a)
        ct(d, 340, "\"Bakı\" sözü hansı səhifədədir?", SN(46), DIM, a)
        # book left
        bx, by = 310, 470
        al = pr(lt, .4, .8) * fo
        d.rounded_rectangle((bx - 190, by, bx + 190, by + 500), 16, fill=mix((235, 225, 200), al))
        d.rectangle((bx - 6, by, bx + 6, by + 500), fill=mix((170, 150, 120), al))
        if lt < 5.5:
            pg = int(1 + min(lt, 5.5) * 60) if lt > 1 else 1
            ct(d, by + 200, f"s. {pg}", MB(60), (60, 60, 80), al, bx)
            ct(d, by + 520, "Səhifə-səhifə vərəqlə...", SN(40), RED, pr(lt, 1, 1.4) * fo, bx)
            for k in range(6):
                ly = by + 40 + k * 26
                d.line((bx - 170, ly, bx - 30, ly), fill=mix((150, 140, 120), al), width=4)
                d.line((bx + 30, ly, bx + 170, ly), fill=mix((150, 140, 120), al), width=4)
        else:
            ct(d, by + 200, "s. 342", MB(60), (20, 120, 70), al, bx)
            ct(d, by + 520, "Birbaşa açdıq!", SN(40), GREEN, fo, bx)
        # index page right
        ax = 790; ap = pr(lt, 3, 3.5) * fo
        d.rounded_rectangle((ax - 200, by, ax + 200, by + 500), 16, fill=mix((235, 225, 200), ap))
        ct(d, by + 25, "İNDEKS", SB(46), (40, 40, 60), ap, ax)
        entries = [("Ağdam", 12), ("Bakı", 342), ("Gəncə", 87), ("Lənkəran", 205), ("Şəki", 410)]
        for k, (w_, p_) in enumerate(entries):
            y = by + 110 + k * 70
            if w_ == "Bakı" and lt > 4.2:
                d.rounded_rectangle((ax - 185, y - 8, ax + 185, y + 52), 10, fill=mix(YEL, ap))
            d.text((ax - 170, y), w_, font=SN(38), fill=mix((40, 40, 60), ap))
            d.text((ax + 100, y), str(p_), font=MB(38), fill=mix((40, 40, 60), ap))
        if lt > 5: arrow(d, ax - 190, by + 210, bx + 200, by + 230, GREEN, pr(lt, 5, 5.5) * fo, 8)
        caption(d, "Kitabın sonundakı indeks: söz → səhifə nömrəsi. Verilənlər bazasında indeks tam belə işləyir!", pr(lt, 6, 6.4) * fo)

    # 3. FULL TABLE SCAN
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 250, "İndekssiz: FULL TABLE SCAN", SB(56), RED, a)
        ct(d, 335, "Cədvəl bloklarda saxlanır (hər blok ≈ 100 sətir)", SN(38), DIM, a)
        total = 120; target = 97
        scanned = int(min(total, max(0, (lt - 2.5) / 6.5 * total)))
        hit = scanned > target
        x0, s, gap = blocks_grid(d, 410, a, scanned if lt > 2.5 else 0, target, hit)
        # zoom label for one block
        if lt < 2.5:
            al = pr(lt, .6, 1) * fo
            d.rounded_rectangle((180, 1180, 900, 1260), 18, fill=mix(CARD, al))
            ct(d, 1195, "Sətirlər SIRALANMAYIB: 412, 9, 777777, 53...", MN(32), WHITE, al)
        blocks_read = int(scanned / total * 10000)
        counter(d, 1200 if lt >= 2.5 else 1290, "Oxunan blok:", f"{blocks_read:,}".replace(",", " "), RED, pr(lt, 2.3, 2.6) * fo)
        if hit:
            ct(d, 1340, "Tapıldı... amma axtarış davam edir!", SB(42), YEL, pr(lt, 2.5 + target / total * 6.5, 3 + target / total * 6.5) * fo)
        caption(d, "Oracle bilmir ki, 777777 harada yerləşir. Ona görə HƏR bloku diskdən oxuyub yoxlayır.", pr(lt, 1.6, 2) * fo)

    # 4. INDEX = key + ROWID
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 250, "İndeks nədir?", SB(66), GREEN, a)
        ct(d, 340, "Ayrıca, SIRALANMIŞ siyahı: açar + ünvan", SN(42), WHITE, a)
        al = pr(lt, .6, 1) * fo
        d.rounded_rectangle((110, 420, 970, 860), 22, fill=mix(CARD, al))
        d.text((150, 440), "client_no", font=MB(40), fill=mix(CYAN, al))
        d.text((520, 440), "ROWID", font=MB(40), fill=mix(CYAN, al))
        rows = [("777775", "AAAR3sAAEAAAAgVAAB"), ("777776", "AAAR3sAAEAAAA9kAAH"),
                ("777777", "AAAR3sAAEAAAAPxAAE"), ("777778", "AAAR3sAAEAAAAa2AAC")]
        for k, (key, rid) in enumerate(rows):
            y = 520 + k * 80; ar = pr(lt, .9 + k * .15, 1.2 + k * .15) * fo
            if key == "777777" and lt > 2.2:
                d.rounded_rectangle((125, y - 8, 955, y + 60), 12, fill=mix((70, 60, 20), ar))
            d.text((150, y), key, font=MB(40), fill=mix(WHITE, ar))
            d.text((420, y + 4), rid, font=MN(34), fill=mix(YEL, ar))
        # ROWID breakdown
        ab = pr(lt, 3.2, 3.6) * fo
        ct(d, 900, "ROWID = sətrin fiziki ünvanı", SB(48), WHITE, ab)
        parts = [("AAAR3s", "obyekt", PURP), ("AAE", "fayl", CYAN), ("AAAAPx", "blok", GREEN), ("AAE", "sətir", PINK)]
        x = 140
        for k, (p_, lab, c) in enumerate(parts):
            ap = pr(lt, 3.8 + k * .4, 4.2 + k * .4) * fo
            w = d.textlength(p_, font=MB(52))
            d.rounded_rectangle((x - 10, 990, x + w + 10, 1070), 12, fill=mix(c, ap))
            d.text((x, 1000), p_, font=MB(52), fill=mix(BG, ap) if ap > .5 else mix(c, ap))
            ct(d, 1085, lab, SN(36), c, ap, x + w / 2)
            x += w + 40
        ct(d, 1170, "Poçt ünvanı kimi: şəhər → küçə → ev → mənzil", SN(40), DIM, pr(lt, 5.6, 6) * fo)
        caption(d, "İndeks dəyəri və onun harada olduğunu saxlayır. Ünvanı bilən Oracle birbaşa həmin bloka gedir.", pr(lt, 1.4, 1.8) * fo)

    # 5. B-TREE SEARCH
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 250, "B-tree: indeksin daxili quruluşu", SB(52), WHITE, a)
        ct(d, 330, "Axtarırıq: 777777", MB(46), YEL, a)
        step = 0 if lt < 3 else 1 if lt < 6.5 else 2 if lt < 10 else 3 if lt < 13 else 4
        # root
        ar = pr(lt, .5, .9) * fo
        ct(d, 395, "KÖK", SB(30), DIM, ar)
        node(d, 540, 435, 720, 90, ["< 333K", "333K–666K", "≥ 666K"], ar, 2 if step >= 1 else None, fs=34)
        # branches
        ab = pr(lt, 1, 1.4) * fo
        bx = [170, 540, 910]
        for k in range(3):
            if k < 2: node(d, bx[k], 640, 300, 80, ["...", "..."], ab * .5, fs=30)
            arrow(d, 540 - 240 + k * 240, 525, bx[k], 635, GREEN if (k == 2 and step >= 1) else OFFB, ab, 5 if k != 2 or step < 1 else 8)
        node(d, 910, 640, 300, 80, ["<720K", "<780K", "≥780K"], ab, 1 if step >= 2 else None, fs=28)
        ct(d, 730, "BUDAQ", SB(30), DIM, ab, 910)
        # leaf
        al = pr(lt, 4, 4.4) * fo
        arrow(d, 910, 720, 700, 840, GREEN if step >= 2 else OFFB, al, 8 if step >= 2 else 5)
        d.rounded_rectangle((330, 845, 990, 1085), 18, fill=mix(CARD, al), outline=mix(GREEN, al), width=4)
        ct(d, 800, "YARPAQ", SB(30), DIM, al, 850)
        leaf = [("777776", "...A9kAAH"), ("777777", "...APxAAE"), ("777778", "...Aa2AAC")]
        for k, (key, rid) in enumerate(leaf):
            y = 865 + k * 70
            if k == 1 and step >= 3: d.rounded_rectangle((345, y - 6, 975, y + 58), 10, fill=mix(YEL, al))
            d.text((370, y), key, font=MB(40), fill=mix(BG if (k == 1 and step >= 3) else WHITE, al))
            d.text((640, y + 2), rid, font=MN(36), fill=mix(BG if (k == 1 and step >= 3) else YEL, al))
        # table block
        at = pr(lt, 10.5, 11) * fo
        if step >= 3: arrow(d, 400, 1085, 300, 1180, GREEN, at, 8)
        d.rounded_rectangle((90, 1185, 640, 1330), 18, fill=mix(CARD, at), outline=mix(GREEN if step >= 4 else OFFB, at), width=4)
        d.text((120, 1200), "Cədvəl bloku AAAAPx", font=SB(32), fill=mix(DIM, at))
        if step >= 4:
            d.rounded_rectangle((110, 1250, 620, 1315), 10, fill=mix(GREEN, fo))
            d.text((130, 1258), "777777 | Əli | 050...", font=MB(36), fill=BG)
        # read counter
        reads = [0, 1, 2, 3, 4][step]
        counter(d, 1195, "Blok:", f"{reads}", GREEN, pr(lt, .5, .9) * fo, 680, 990)
        caps = ["Kök: 777777 ≥ 666K → sağa get. Yalnız 1 blok oxunur.",
                "Kök: 777777 ≥ 666K → sağa get. Yalnız 1 blok oxunur.",
                "Budaq: 777777 < 780K → ortadakı yarpağa get. 2-ci blok.",
                "Yarpaq: 777777 tapıldı, yanında ünvanı (ROWID) var. 3-cü blok.",
                "ROWID ilə birbaşa cədvəl blokuna! Cəmi 4 blok, axtarış yoxdur."]
        caption(d, caps[step], pr(lt, 1.6, 2) * fo)

    # 6. COMPARISON
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 260, "Nəticə:", SB(70), WHITE, a)
        base = 1050
        for k, (lab, v, col, h) in enumerate([("İndekssiz", "10 000", RED, 600), ("İndekslə", "4", GREEN, 6)]):
            x = 230 + k * 420; al = pr(lt, .4 + k * .3, .8 + k * .3) * fo
            hh = max(6, h * pr(lt, .6 + k * .3, 1.8 + k * .3))
            d.rounded_rectangle((x, base - hh, x + 200, base), 16, fill=mix(col, al))
            ct(d, base - hh - 80, v, MB(60), col, al, x + 100)
            ct(d, base + 20, lab, SB(42), WHITE, al, x + 100)
            ct(d, base + 80, "blok", SN(36), DIM, al, x + 100)
        ct(d, 1230, "≈ 2500 dəfə az oxuma!", SB(64), YEL, pr(lt, 2.6, 3) * fo)
        caption(d, "B-tree hündürlüyü adətən 3–4 səviyyədir. Cədvəl 1000 dəfə böyüsə də, axtarış cəmi 1–2 addım artır.", pr(lt, 3.2, 3.6) * fo)

    # 7. EXPLAIN PLAN
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Oracle-da necə yaradılır?", SB(58), WHITE, a)
        code(d, 330, ["CREATE INDEX idx_client_no", "    ON clients(client_no);"], .4, lt, a, 42, .03)
        ab = pr(lt, 2.2, 2.6) * fo
        ct(d, 600, "EXPLAIN PLAN: əvvəl", SB(40), RED, ab)
        d.rounded_rectangle((60, 660, W - 60, 760), 20, fill=mix((70, 18, 28), ab), outline=mix(RED, ab), width=3)
        d.text((95, 685), "TABLE ACCESS FULL", font=MB(46), fill=mix(WHITE, ab))
        aa = pr(lt, 4, 4.4) * fo
        ct(d, 800, "EXPLAIN PLAN: sonra", SB(40), GREEN, aa)
        d.rounded_rectangle((60, 860, W - 60, 1040), 20, fill=mix((14, 50, 36), aa), outline=mix(GREEN, aa), width=3)
        d.text((95, 885), "TABLE ACCESS BY INDEX ROWID", font=MB(40), fill=mix(WHITE, aa))
        d.text((135, 960), "└ INDEX RANGE SCAN", font=MB(40), fill=mix(GREEN, aa))
        caption(d, "Planda INDEX RANGE SCAN görürsənsə, Oracle indeksdən istifadə edir. FULL görürsənsə, bütün cədvəli oxuyur.", pr(lt, 4.6, 5) * fo)

    # 8. TRAPS
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 250, "İndeks var, amma İŞLƏMİR! 😱".replace(" 😱", ""), SB(56), RED, a)
        ct(d, 330, "4 tələ", SB(44), YEL, a)
        traps = [("UPPER(name) = 'ƏLİ'", "Sütuna funksiya tətbiq olunub", "Function-based index"),
                 ("phone = 0501234567", "Mətn sütununa rəqəm verilib", "'0501234567' (dırnaqla)"),
                 ("name LIKE '%li'", "Əvvəldə % işarəsi var", "LIKE 'Əl%' işləyir"),
                 ("col IS NULL", "B-tree NULL saxlamır", "NOT NULL + default")]
        k = min(3, int(lt / 4))
        for j in range(4):
            y = 410 + j * 82
            done = j < k; cur = j == k
            al = (1 if done or cur else .4) * a
            d.rounded_rectangle((70, y, W - 70, y + 68), 14, fill=mix(CARD if not cur else (40, 30, 55), al))
            d.text((100, y + 14), f"{j + 1}. WHERE {traps[j][0]}", font=MB(34), fill=mix(WHITE if not done else DIM, al))
        q, why, fix = traps[k]
        pl = lt - k * 4
        ab = pr(pl, .3, .7) * fo
        d.rounded_rectangle((60, 780, W - 60, 1180), 26, fill=mix((16, 22, 42), ab), outline=mix(RED, ab), width=4)
        d.text((100, 810), "✗ WHERE " + q, font=MB(40), fill=mix(RED, ab))
        d.text((100, 890), why, font=SN(40), fill=mix(WHITE, ab))
        d.text((100, 960), "→ TABLE ACCESS FULL", font=MB(36), fill=mix(DIM, ab))
        af = pr(pl, 1.6, 2) * fo
        d.rounded_rectangle((90, 1040, W - 90, 1150), 20, fill=mix((14, 50, 36), af), outline=mix(GREEN, af), width=3)
        d.text((120, 1070), "✓ " + fix, font=MB(38), fill=mix(GREEN, af))
        caps = ["İndeks 'name' üzərindədir, 'UPPER(name)' üzərində yox. Oracle indeksi istifadə edə bilmir.",
                "Oracle gizlicə TO_NUMBER(phone) edir, bu da funksiyadır. İndeks sıradan çıxır.",
                "İndeks sıralıdır: 'Əl...' ilə başlayanı tapır, amma '...li' ilə bitəni tapa bilmir.",
                "Tamamilə NULL olan dəyərlər adi B-tree indeksə yazılmır, IS NULL indeksi keçir."]
        caption(d, caps[k], pr(pl, .8, 1.2) * fo)

    # 9. FASTER
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Daha sürətli etmək üçün", SB(58), GREEN, a)
        tips = [("Composite", "(branch_id, open_date)", "Sıra vacibdir: əvvəlcə tez-tez axtarılan sütun"),
                ("Covering", "SELECT yalnız indeksdəki sütunlar", "Cədvələ heç getmir: 3 blok kifayətdir"),
                ("Selectivity", "gender (2 dəyər) ✗ · client_no ✓", "Unikal dəyərlər çoxdursa, indeks faydalıdır")]
        for k, (h, ex, why) in enumerate(tips):
            y = 360 + k * 280; al = pr(lt, .4 + k * 2.6, .8 + k * 2.6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 250), 26, fill=mix(CARD, al), outline=mix(GREEN, al * .6), width=3)
            d.text((105, y + 25), f"{k + 1}. {h}", font=SB(50), fill=mix(YEL, al))
            d.text((105, y + 100), ex, font=MB(34), fill=mix(CYAN, al))
            for j, ln in enumerate(wrap(d, why, SN(36), W - 230)):
                d.text((105, y + 160 + j * 44), ln, font=SN(36), fill=mix(WHITE, al))
        caption(d, "Düzgün sütun seçimi və düzgün sıra = maksimum sürət.", pr(lt, 8, 8.4) * fo)

    # 10. COST
    elif t < T[10]:
        lt, fo = sc(t, 9); a = pr(lt, 0, .4) * fo
        ct(d, 260, "Amma pulsuz deyil!", SB(64), RED, a)
        ops = ["INSERT", "UPDATE", "DELETE"]
        for k, op in enumerate(ops):
            y = 420 + k * 150; al = pr(lt, .4 + k * .3, .8 + k * .3) * fo
            d.rounded_rectangle((90, y, 470, y + 110), 20, fill=mix(CARD, al))
            ct(d, y + 28, op, MB(50), CYAN, al, 280)
            arrow(d, 490, y + 55, 600, y + 55, YEL, al)
            d.rounded_rectangle((620, y, 990, y + 110), 20, fill=mix((60, 40, 10), al))
            ct(d, y + 32, "+ indeks yenilə", SN(38), YEL, al, 805)
        ct(d, 920, "Hər indeks = əlavə disk + yavaş yazma", SB(46), WHITE, pr(lt, 1.8, 2.2) * fo)
        ct(d, 1010, "Hər sütuna indeks QOYMA!", SB(56), RED, pr(lt, 2.5, 2.9) * fo)
        caption(d, "İndeksi yalnız WHERE və JOIN-də tez-tez istifadə olunan sütunlara yarat.", pr(lt, 2.8, 3.2) * fo)

    # 11. RECAP + CTA
    else:
        lt = t - T[10]
        ct(d, 280, "Yadda saxla:", SB(66), WHITE, pr(lt, 0, .3))
        items = [("İndeks", "→ sıralı siyahı + ROWID"), ("B-tree", "→ 3–4 addımda tapır"),
                 ("Funksiya, %x", "→ indeksi söndürür"), ("Çox indeks", "→ yavaş yazma")]
        for k, (q, ex) in enumerate(items):
            y = 390 + k * 115; al = pr(lt, .2 + k * .25, .5 + k * .25)
            d.rounded_rectangle((70, y, W - 70, y + 95), 20, fill=mix(CARD, al))
            d.text((105, y + 25), q, font=MB(42), fill=mix(GREEN, al))
            d.text((460, y + 28), ex, font=SN(40), fill=mix(WHITE, al))
        ct(d, 880, "Növbəti video: EXPLAIN PLAN necə oxunur?", SB(42), YEL, pr(lt, 1.6, 2))
        ap = pr(lt, 2.2, 2.6); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 980, (W + bw) / 2, 980 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 980 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1150, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 2.6, 3))
    return im

if __name__ == "__main__":
    import sys
    snaps = {}
    for k in range(len(T) - 1):
        snaps[int((T[k] + (T[k + 1] - T[k]) * .75) * FPS)] = f"v5_{k}"
    for extra, nm in [(T[4] + 5, "v5_bt1"), (T[4] + 12, "v5_bt3"), (T[7] + 6, "v5_tr2"), (T[2] + 9, "v5_fts")]:
        snaps[int(extra * FPS)] = nm
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        for i, nm in snaps.items(): frame(i).save(nm + ".png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v5_silent.mp4"], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print("video done")

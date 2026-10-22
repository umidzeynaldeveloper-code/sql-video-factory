from common import *
from make_video5 import arrow, counter
import subprocess, math, sys

T = [0, 6, 15, 27, 43, 53, 66, 79, 91, 97, 103]
DUR = T[-1]; N = FPS * DUR

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

KW = {"SELECT", "FROM", "WHERE", "CREATE", "INDEX", "ON", "JOIN", "EXPLAIN", "PLAN", "FOR", "TABLE", "EXEC"}
def code(d, y0, lines, t0, t, a, size=40, speed=.028):
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
            c = CYAN if wd in KW else YEL if "'" in word else PURP if ("DBMS" in word or "/*+" in word or "GATHER" in word) else WHITE
            d.text((x, yy), word, font=f, fill=mix(c, a))
            x += d.textlength(word + " ", font=f)
        yy += lh
    return y0 + h

GOOD = [("0", "SELECT STATEMENT", "", "3", "7"),
        ("1", " NESTED LOOPS", "", "3", "7"),
        ("2", "  TABLE ACCESS BY INDEX ROWID", "CLIENTS", "1", "3"),
        ("3", "   INDEX RANGE SCAN", "IDX_CLIENT_NO", "1", "2"),
        ("4", "  TABLE ACCESS BY INDEX ROWID", "ACCOUNTS", "3", "4"),
        ("5", "   INDEX RANGE SCAN", "IDX_ACC_CLIENT", "3", "1")]
BAD = [("0", "SELECT STATEMENT", "", "3", "12457"),
       ("1", " HASH JOIN", "", "3", "12457"),
       ("2", "  TABLE ACCESS BY INDEX ROWID", "CLIENTS", "1", "3"),
       ("3", "   INDEX RANGE SCAN", "IDX_CLIENT_NO", "1", "2"),
       ("4", "  TABLE ACCESS FULL", "ACCOUNTS", "5M", "12450")]
COLX = {"id": 85, "op": 125, "name": 610, "rows_r": 905, "cost_r": 1000}

def plan(d, y0, rows, a, hl_col=None, hl_rows=(), red_rows=(), badges=None, reveal=99, fs=27):
    rh = 58; h = 70 + rh * len(rows) + 20
    d.rounded_rectangle((60, y0, W - 60, y0 + h), 20, fill=mix((16, 22, 42), a), outline=mix((50, 70, 120), a), width=3)
    f = MB(fs); fh = MB(fs)
    heads = [("Id", COLX["id"], "l"), ("Operation", COLX["op"], "l"), ("Name", COLX["name"], "l"),
             ("Rows", COLX["rows_r"], "r"), ("Cost", COLX["cost_r"], "r")]
    keys = ["id", "op", "name", "rows", "cost"]
    for k, (hname, x, al_) in enumerate(heads):
        c = YEL if hl_col == keys[k] else CYAN
        tx = x - d.textlength(hname, font=fh) if al_ == "r" else x
        d.text((tx, y0 + 22), hname, font=fh, fill=mix(c, a))
    if hl_col:
        spans = {"id": (72, 118), "op": (118, 600), "name": (600, 840), "rows": (840, 915), "cost": (915, 1012)}
        x0, x1 = spans[hl_col]
        d.rounded_rectangle((x0, y0 + 10, x1, y0 + h - 10), 12, outline=mix(YEL, a), width=4)
    d.line((75, y0 + 68, W - 75, y0 + 68), fill=mix(OFFB, a), width=2)
    for r, row in enumerate(rows):
        if r >= reveal: break
        y = y0 + 80 + r * rh
        if r in hl_rows: d.rounded_rectangle((70, y - 6, W - 70, y + rh - 10), 10, fill=mix((70, 60, 20), a))
        if r in red_rows: d.rounded_rectangle((70, y - 6, W - 70, y + rh - 10), 10, fill=mix((80, 22, 32), a))
        id_, op, nm, rw, cs = row
        if not (badges and r in badges and badges[r][1] > 0):
            d.text((COLX["id"], y), id_, font=f, fill=mix(DIM, a))
        opc = RED if "FULL" in op else GREEN if "INDEX" in op else WHITE
        d.text((COLX["op"], y), op, font=f, fill=mix(opc, a))
        d.text((COLX["name"], y), nm, font=f, fill=mix(WHITE, a))
        d.text((COLX["rows_r"] - d.textlength(rw, font=f), y), rw, font=f, fill=mix(WHITE, a))
        d.text((COLX["cost_r"] - d.textlength(cs, font=f), y), cs, font=f, fill=mix(RED if len(cs) > 3 else WHITE, a))
        if badges and r in badges:
            n, ab = badges[r]
            if ab > 0:
                bx = 95; by = y + 16
                d.ellipse((bx - 22, by - 22, bx + 22, by + 22), fill=mix(YEL, ab))
                ct(d, by - 17, str(n), SB(28), BG, ab, bx)
    return y0 + h

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
        ct(d, 280, "Sorğun yavaşdır?", SB(76), WHITE, a)
        ct(d, 380, "Oracle səbəbini özü deyir 👇".replace(" 👇", ""), SB(54), CYAN, pr(lt, .6, 1) * fo)
        plan(d, 500, GOOD, pr(lt, 1, 1.4) * fo * (.35 if lt < 3 else 1), reveal=int(max(0, (lt - 1) / .25)))
        ct(d, 1000, "...sadəcə oxumağı bilməlisən", SB(52), YEL, pr(lt, 3.2, 3.6) * fo)
        caption(d, "Bu cədvəl EXPLAIN PLAN-dır: Oracle-ın sorğunu necə icra edəcəyinin xəritəsi.", pr(lt, 3.6, 4) * fo)

    # 2 HOW TO GET
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 260, "Planı necə görmək olar?", SB(60), WHITE, a)
        y = code(d, 350, ["EXPLAIN PLAN FOR", "SELECT c.name, a.balance", "  FROM clients c", "  JOIN accounts a", "    ON a.client_id = c.id", " WHERE c.client_no = 777777;"], .4, lt, a, 38, .022)
        y2 = code(d, y + 30, ["SELECT * FROM", " TABLE(DBMS_XPLAN.DISPLAY);"], 4.2, lt, pr(lt, 4, 4.3) * fo, 38, .03)
        ab = pr(lt, 6.3, 6.7) * fo
        d.rounded_rectangle((60, y2 + 30, W - 60, y2 + 130), 20, fill=mix((60, 40, 10), ab), outline=mix(YEL, ab), width=3)
        ct(d, y2 + 58, "SQL Developer-də: F10 düyməsi", SB(44), YEL, ab)
        caption(d, "EXPLAIN PLAN sorğunu icra etmir, yalnız planı hazırlayır. Təhlükəsizdir, istənilən vaxt yoxlaya bilərsən.", pr(lt, 2, 2.4) * fo)

    # 3 COLUMNS
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 260, "Sütunlar nə deyir?", SB(62), WHITE, a)
        cols = [("op", "Operation", "Nə edir? (oxuyur, birləşdirir...)", CYAN),
                ("name", "Name", "Hansı cədvəl / indeks?", CYAN),
                ("rows", "Rows", "Neçə sətir GÖZLƏYİR (təxmin)", YEL),
                ("cost", "Cost", "Nisbi qiymət. Saniyə DEYİL!", PINK)]
        k = min(3, int(max(0, lt - .8) / 2.6))
        hl = cols[k][0] if lt > .8 else None
        plan(d, 370, GOOD, a, hl_col=hl)
        if lt > .8:
            _, nm, ex, c = cols[k]; pl = lt - .8 - k * 2.6
            ab = pr(pl, 0, .4) * fo
            d.rounded_rectangle((70, 860, W - 70, 1040), 26, fill=mix(CARD, ab), outline=mix(c, ab), width=4)
            d.text((110, 885), nm, font=MB(56), fill=mix(c, ab))
            d.text((110, 965), ex, font=SN(42), fill=mix(WHITE, ab))
        caps = ["Operation: Oracle-ın bu addımda nə etdiyi. Ən vacib sütun budur.",
                "Name: əməliyyatın hansı cədvəl və ya indeks üzərində getdiyi.",
                "Rows: optimizatorun təxmini. Real rəqəmdən çox fərqlənirsə, problem var.",
                "Cost: planları müqayisə üçün xal. Kiçik = adətən yaxşı. Amma bu, vaxt deyil."]
        caption(d, caps[k], pr(lt, 1, 1.4) * fo)

    # 4 READING ORDER
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Hansı addım BİRİNCİ işləyir?", SB(56), YEL, a)
        order = [3, 2, 5, 4, 1, 0]  # row ids in execution order
        steps_t = [3.5 + k * 1.6 for k in range(6)]
        badges = {r: (k + 1, pr(lt, steps_t[k], steps_t[k] + .3) * fo) for k, r in enumerate(order)}
        cur = max([k for k in range(6) if lt >= steps_t[k]], default=-1)
        hl = (order[cur],) if cur >= 0 else ()
        plan(d, 340, GOOD, a, hl_rows=hl, badges=badges)
        # rule box
        ar = pr(lt, .6, 1) * fo
        d.rounded_rectangle((70, 800, W - 70, 1030), 24, fill=mix(CARD, ar))
        rules = ["① Ən İÇƏRİDƏKİ (sağa sürüşən) birinci", "② Eyni səviyyədə: YUXARIDAKI birinci", "③ Valideyn uşaqlarından SONRA"]
        for j, r in enumerate(rules):
            d.text((105, 825 + j * 66), r, font=SN(40), fill=mix(WHITE, pr(lt, .8 + j * .6, 1.2 + j * .6) * fo))
        story = ["",
                 "1. İndeksdə 777777-ni tap",
                 "2. ROWID ilə CLIENTS-dən sətri götür",
                 "3. Bu müştərinin hesablarını indeksdə tap",
                 "4. ROWID ilə ACCOUNTS-dan oxu",
                 "5. NESTED LOOPS: ikisini birləşdir",
                 "6. Nəticəni qaytar ✓"]
        if cur >= 0:
            ab = pr(lt, steps_t[cur], steps_t[cur] + .3) * fo
            d.rounded_rectangle((70, 1060, W - 70, 1160), 20, fill=mix((40, 34, 10), ab), outline=mix(YEL, ab), width=3)
            ct(d, 1085, story[cur + 1], SB(42), YEL, ab)
        caption(d, "Plan yuxarıdan aşağı oxunmur! İcra ən dərindəki addımdan başlayır: əvvəl indeks, sonra cədvəl, ən sonda birləşmə.", pr(lt, 2.4, 2.8) * fo)

    # 5 OPERATIONS CHEAT SHEET
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 260, "Əməliyyatları tanı:", SB(60), WHITE, a)
        groups = [(GREEN, "Yaxşı", [("INDEX UNIQUE SCAN", "1 sətir, ən sürətli"), ("INDEX RANGE SCAN", "aralıq, sürətli"), ("BY INDEX ROWID", "ünvanla birbaşa")]),
                  (YEL, "Konteksdən asılı", [("NESTED LOOPS", "kiçik dəstlər üçün"), ("HASH JOIN", "böyük dəstlər üçün"), ("SORT ORDER BY", "sıralama, yaddaş")]),
                  (RED, "Diqqət!", [("TABLE ACCESS FULL", "böyük cədvəldə, az nəticə"), ("MERGE JOIN CARTESIAN", "JOIN şərti unudulub?")])]
        y = 360
        for g, (c, title, items) in enumerate(groups):
            ag = pr(lt, .4 + g * 2.5, .8 + g * 2.5) * fo
            d.text((90, y), "● " + title, font=SB(42), fill=mix(c, ag)); y += 62
            for op, ex in items:
                d.rounded_rectangle((80, y, W - 80, y + 64), 14, fill=mix(CARD, ag))
                d.text((105, y + 14), op, font=MB(32), fill=mix(c, ag))
                d.text((600, y + 16), ex, font=SN(30), fill=mix(WHITE, ag))
                y += 74
            y += 12
        caption(d, "FULL həmişə pis deyil: kiçik cədvəldə və ya çox sətir lazım olanda o, ən sürətli yoldur.", pr(lt, 6.4, 6.8) * fo)

    # 6 BAD PLAN -> FIX
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        fixed = lt > 8
        ct(d, 250, "Pis plan → düzəliş" if not fixed else "İndeksdən sonra:", SB(60), RED if not fixed else GREEN, a)
        if not fixed:
            plan(d, 340, BAD, a, red_rows=(4,) if lt > 1.5 else (), reveal=int(max(0, (lt - .3) / .2)))
            ab = pr(lt, 2.2, 2.6) * fo
            d.rounded_rectangle((70, 760, W - 70, 900), 24, fill=mix((70, 18, 28), ab), outline=mix(RED, ab), width=3)
            d.text((105, 780), "ACCOUNTS: 5 000 000 sətir tam oxunur", font=SB(38), fill=mix(WHITE, ab))
            d.text((105, 838), "amma bizə cəmi 3 sətir lazımdır!", font=SN(36), fill=mix(DIM, ab))
            code(d, 930, ["CREATE INDEX idx_acc_client", "    ON accounts(client_id);"], 4.4, lt, pr(lt, 4.2, 4.5) * fo, 40, .03)
        else:
            pl = lt - 8
            plan(d, 340, GOOD, a, hl_rows=(4, 5) if pl > .6 else ())
            ac = pr(pl, .8, 1.2) * fo
            d.text((140, 800), "Cost:", font=SB(50), fill=mix(WHITE, ac))
            d.text((320, 795), "12 457", font=MB(60), fill=mix(RED, ac))
            d.line((310, 832, 540, 832), fill=mix(RED, ac), width=6)
            arrow(d, 570, 830, 680, 830, YEL, ac)
            d.text((710, 795), "7", font=MB(70), fill=mix(GREEN, ac))
            ct(d, 920, "≈ 1800 dəfə ucuz!", SB(58), YEL, pr(pl, 1.6, 2) * fo)
        caps = (["HASH JOIN + TABLE ACCESS FULL: 5 milyon sətir oxunur. Səbəb: accounts.client_id üzərində indeks yoxdur."]
                if lt < 4.2 else ["Həll: JOIN sütununa indeks yarat."] if not fixed else
                ["Plan dəyişdi: NESTED LOOPS + INDEX RANGE SCAN. Cost 12 457-dən 7-yə düşdü."])
        caption(d, caps[0], pr(lt, 1.6, 2) * fo)

    # 7 PREDICATE
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Gizli xəzinə:", SB(58), WHITE, a)
        ct(d, 330, "Predicate Information", MB(48), CYAN, a)
        ag = pr(lt, .8, 1.2) * fo
        d.rounded_rectangle((60, 420, W - 60, 640), 22, fill=mix((14, 50, 36), ag), outline=mix(GREEN, ag), width=4)
        d.text((95, 445), "3 - access(\"C\".\"CLIENT_NO\"=777777)", font=MB(31), fill=mix(GREEN, ag))
        d.text((95, 520), "ACCESS = indeks ilə birbaşa tapıldı ✓", font=SB(38), fill=mix(WHITE, ag))
        d.text((95, 575), "yalnız lazım olan sətirlər oxundu", font=SN(34), fill=mix(DIM, ag))
        ab = pr(lt, 4.4, 4.8) * fo
        d.rounded_rectangle((60, 680, W - 60, 900), 22, fill=mix((70, 18, 28), ab), outline=mix(RED, ab), width=4)
        d.text((95, 705), "1 - filter(TO_NUMBER(\"PHONE\")=501234567)", font=MB(29), fill=mix(RED, ab))
        d.text((95, 780), "FILTER = oxuduqdan SONRA yoxlanır ✗", font=SB(38), fill=mix(WHITE, ab))
        d.text((95, 835), "gizli TO_NUMBER → indeks işləmədi", font=SN(34), fill=mix(DIM, ab))
        af = pr(lt, 8, 8.4) * fo
        ct(d, 950, "Keçən videodakı tələni plan özü göstərir!", SB(42), YEL, af)
        caption(d, "Planın altındakı bu bölməyə mütləq bax: 'access' yaxşıdır, böyük cədvəldə 'filter' isə şübhəlidir.", pr(lt, 2, 2.4) * fo)

    # 8 E-ROWS vs A-ROWS
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Optimizator səhv edə bilər!", SB(56), RED, a)
        y = code(d, 340, ["SELECT /*+ GATHER_PLAN_STATISTICS */ ...", "", "SELECT * FROM TABLE(", "  DBMS_XPLAN.DISPLAY_CURSOR(", "    format => 'ALLSTATS LAST'));"], .4, lt, a, 34, .022)
        ar = pr(lt, 3.6, 4) * fo
        for k, (lab, v, c) in enumerate([("E-Rows (təxmin)", "1", YEL), ("A-Rows (real)", "250 000", RED)]):
            x = 90 + k * 460
            d.rounded_rectangle((x, y + 30, x + 440, y + 230), 24, fill=mix(CARD, ar), outline=mix(c, ar), width=4)
            ct(d, y + 50, lab, SB(36), DIM, ar, x + 220)
            ct(d, y + 110, v, MB(72), c, ar, x + 220)
        af = pr(lt, 6.4, 6.8) * fo
        y3 = code(d, y + 270, ["EXEC DBMS_STATS.GATHER_TABLE_STATS(", "       USER, 'ACCOUNTS');"], 6.6, lt, af, 36, .03)
        caps = ["GATHER_PLAN_STATISTICS sorğunu icra edib həm təxmini, həm də real sətir sayını göstərir.",
                "Təxmin 1, real 250 000! Optimizator 1 sətir gözləyib səhv plan seçdi. Səbəb: köhnə statistika.",
                "Statistikanı yenilə, optimizator real rəqəmləri görüb düzgün plan seçəcək."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6.6 else 2], pr(lt, 1.6, 2) * fo)

    # 9 CHECKLIST
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Plan yoxlama siyahısı:", SB(60), WHITE, a)
        items = [("1", "Böyük cədvəldə TABLE ACCESS FULL?"), ("2", "Rows real rəqəmə yaxındır?"),
                 ("3", "Predicate: access, yoxsa filter?"), ("4", "Cost harada sıçrayır?")]
        for k, (n, tx) in enumerate(items):
            y = 380 + k * 140; al = pr(lt, .3 + k * .5, .6 + k * .5) * fo
            d.rounded_rectangle((70, y, W - 70, y + 115), 22, fill=mix(CARD, al))
            d.ellipse((100, y + 25, 165, y + 90), fill=mix(YEL, al))
            ct(d, y + 33, n, SB(40), BG, al, 132)
            d.text((195, y + 35), tx, font=SN(40), fill=mix(WHITE, al))
        caption(d, "Bu 4 sual yavaş sorğuların əksəriyyətinin səbəbini tapmağa kömək edir.", pr(lt, 2.4, 2.8) * fo)

    # 10 CTA
    else:
        lt = t - T[9]
        ct(d, 420, "Növbəti video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 520, "JOIN növləri", SB(72), YEL, pr(lt, .2, .5))
        ct(d, 630, "NESTED LOOPS vs HASH JOIN", MB(46), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [T[0] + 4.5, T[1] + 7, T[2] + 4, T[2] + 10, T[3] + 12, T[4] + 8, T[5] + 5, T[5] + 11, T[6] + 10, T[7] + 9, T[8] + 4, T[9] + 3]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v6_{k}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v6_silent.mp4"], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print("video done")

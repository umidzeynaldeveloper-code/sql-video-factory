from common import *
from make_video5 import arrow
import subprocess, math, sys

T = [0, 6, 18, 32, 46, 60, 74, 86, 96, 102, 108]
DUR = T[-1]; N = FPS * DUR
ORIG = [1200, 800, 3000, 500, 1500]

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

# ---------- schematic helpers ----------
def glow_box(d, box, col, a, title=None, sub=None, tfs=36, sfs=30, fill=CARD):
    x0, y0, x1, y1 = box
    for k, f in enumerate((.10, .18, .30)):
        g = 14 - k * 5
        d.rounded_rectangle((x0 - g, y0 - g, x1 + g, y1 + g), 26 + g, outline=mix(col, a * f), width=4)
    d.rounded_rectangle(box, 24, fill=mix(fill, a), outline=mix(col, a), width=4)
    cx = (x0 + x1) / 2
    if title and sub:
        ct(d, y0 + (y1 - y0) / 2 - tfs - 2, title, SB(tfs), col, a, cx)
        ct(d, y0 + (y1 - y0) / 2 + 8, sub, SN(sfs), WHITE, a, cx)
    elif title:
        ct(d, y0 + (y1 - y0) / 2 - tfs * .62, title, SB(tfs), col, a, cx)

def flow(d, pts, col, a, t, reveal=1.0, dots=True, width=5):
    """polyline edge drawn up to `reveal` fraction, with moving particles"""
    segs = list(zip(pts[:-1], pts[1:])); lens = [math.dist(p, q) for p, q in segs]; tot = sum(lens)
    def at(s):
        for (p, q), ln in zip(segs, lens):
            if s <= ln: return (p[0] + (q[0] - p[0]) * s / ln, p[1] + (q[1] - p[1]) * s / ln)
            s -= ln
        return pts[-1]
    rv = tot * max(0, min(1, reveal)); s = 0
    for (p, q), ln in zip(segs, lens):
        if s >= rv: break
        f = min(1, (rv - s) / ln)
        d.line((p[0], p[1], p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f), fill=mix(col, a * .55), width=width)
        s += ln
    if reveal >= 1:
        end = pts[-1]; prev = pts[-2]; ang = math.atan2(end[1] - prev[1], end[0] - prev[0])
        for sg in (-.5, .5):
            d.line((end[0], end[1], end[0] - 22 * math.cos(ang + sg), end[1] - 22 * math.sin(ang + sg)), fill=mix(col, a), width=width + 1)
        if dots:
            for k in range(4):
                x, y = at((t * 260 + k * tot / 4) % tot)
                d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=mix(col, a))
                d.ellipse((x - 14, y - 14, x + 14, y + 14), outline=mix(col, a * .35), width=3)
    elif rv > 0:
        x, y = at(rv); d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=mix(WHITE, a))

def clock(d, cx, cy, r, a, ang_deg, col=CYAN):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=mix(col, a), width=6)
    for k in range(12):
        an = math.radians(k * 30)
        d.line((cx + (r - 14) * math.sin(an), cy - (r - 14) * math.cos(an), cx + (r - 4) * math.sin(an), cy - (r - 4) * math.cos(an)), fill=mix(col, a), width=3)
    an = math.radians(ang_deg)
    d.line((cx, cy, cx + r * .75 * math.sin(an), cy - r * .75 * math.cos(an)), fill=mix(YEL, a), width=6)
    d.line((cx, cy, cx + r * .45 * math.sin(an / 12), cy - r * .45 * math.cos(an / 12)), fill=mix(WHITE, a), width=7)
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=mix(YEL, a))

def bal_table(d, x0, y0, x1, title, vals, a, col=CYAN, vcols=None):
    d.rounded_rectangle((x0, y0, x1, y0 + 80 + 62 * len(vals)), 22, fill=mix(CARD, a), outline=mix(col, a), width=4)
    ct(d, y0 + 18, title, SB(34), col, a, (x0 + x1) / 2)
    for k, v in enumerate(vals):
        y = y0 + 75 + k * 62
        d.text((x0 + 25, y), f"A{k + 1}", font=SN(34), fill=mix(DIM, a))
        txt = f"{v:,}".replace(",", " ")
        c = (vcols[k] if vcols else WHITE)
        d.text((x1 - 25 - d.textlength(txt, font=MB(38)), y - 2), txt, font=MB(38), fill=mix(c, a))

def timeline(d, y, a, knob_x, labels, now_x, win=None):
    if win:
        d.rounded_rectangle((win[0], y - 26, win[1], y + 26), 26, fill=mix((14, 60, 40), a))
    d.line((100, y, 980, y), fill=mix(DIM, a), width=6)
    for x, lab in labels:
        d.line((x, y - 14, x, y + 14), fill=mix(DIM, a), width=4)
        ct(d, y + 28, lab, MN(30), WHITE, a, x)
    d.polygon([(now_x, y - 30), (now_x - 14, y - 52), (now_x + 14, y - 52)], fill=mix(PINK, a))
    ct(d, y - 100, "İNDİ", SB(30), PINK, a, now_x)
    d.ellipse((knob_x - 22, y - 22, knob_x + 22, y + 22), fill=mix(YEL, a), outline=mix(WHITE, a), width=4)

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
        ct(d, 240, "Saat 14:05...", SB(64), WHITE, a)
        ct(d, 330, "kimsə səhvən balansları SIFIRLADI", SB(44), RED, pr(lt, .6, 1) * fo)
        vals = [0 if lt > 1.4 + k * .25 else v for k, v in enumerate(ORIG)]
        vc = [RED if v == 0 else WHITE for v in vals]
        bal_table(d, 240, 420, 840, "BALANCES", vals, a, CYAN, vc)
        if lt > 2.8:
            sa = pr(lt, 2.8, 3.1) * fo; s = 1 + .6 * (1 - pr(lt, 2.8, 3.1))
            w, h = 420 * s, 120 * s; cx, cy = 540, 610
            d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 20, outline=mix(RED, sa), width=10)
            ct(d, cy - 44 * s, "COMMIT", SB(int(76 * s)), RED, sa, cx)
        ct(d, 900, "Geri qaytarmaq olar?", SB(66), YEL, pr(lt, 3.8, 4.2) * fo)
        caption(d, "COMMIT olunub, backup isə dünən gecə alınıb. Panika? Yox. Oracle keçmişi xatırlayır.", pr(lt, 4, 4.4) * fo)

    # 1 TIME MACHINE
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Oracle-ın zaman maşını", SB(60), CYAN, a)
        xs = {"13:55": 180, "14:00": 380, "14:05": 620, "14:10": 860}
        kx = 860 - (860 - 380) * pr(lt, 1.5, 4.5)
        timeline(d, 480, a, kx, [(x, l) for l, x in xs.items()], 860)
        ac = pr(lt, 4.5, 4.9) * fo
        w = 330; d.rounded_rectangle((kx - w / 2, 360, kx + w / 2, 425), 30, fill=mix(YEL, ac))
        ct(d, 372, "AS OF 14:00", MB(36), BG, ac, kx)
        clock(d, 120, 370, 48, a, 360 * (1 - pr(lt, 1.5, 4.5)) * 2)
        past = kx < 620
        vals = ORIG if past else [0] * 5
        vc = [GREEN] * 5 if past else [RED] * 5
        bal_table(d, 240, 600, 840, "AS OF 14:00" if past else "İNDİ (14:10)", vals, a, PURP if past else PINK, vc)
        caps = ["Keçmiş məlumatı görmək üçün sadəcə zamanı göstər.",
                "Dəyişiklik COMMIT olunsa belə, Oracle keçmiş vəziyyəti göstərə bilir.",
                "Bu sehr deyil, UNDO-dur. Gəl içəri baxaq: necə işləyir?"]
        caption(d, caps[0 if lt < 4.5 else 1 if lt < 8 else 2], pr(lt, .8, 1.2) * fo)

    # 2 MECHANISM SCHEMATIC
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "İçəridə nə baş verir?", SB(56), WHITE, a)
        nodes = [((290, 300, 790, 400), YEL, "Sorğu", "AS OF 14:00", .5),
                 ((290, 470, 790, 570), CYAN, "Zaman → SCN", "14:00 = SCN 5000", 2.2),
                 ((90, 650, 500, 760), PINK, "Data blok", "0 · SCN 5200", 4),
                 ((580, 650, 990, 760), PURP, "UNDO zənciri", "köhnə versiyalar", 7.2),
                 ((290, 1000, 790, 1100), GREEN, "Nəticə", "A1 = 1200 ✓", 9.6)]
        for box, col, ti, su, st in nodes:
            glow_box(d, box, col, pr(lt, st, st + .4) * fo, ti, su, 34, 30)
        # diamond compare
        ad = pr(lt, 5.4, 5.8) * fo; cx, cy = 295, 875
        d.polygon([(cx, cy - 70), (cx + 150, cy), (cx, cy + 70), (cx - 150, cy)], fill=mix(CARD, ad), outline=mix(YEL, ad))
        ct(d, cy - 40, "5200 > 5000 ?", MB(30), YEL, ad, cx)
        ct(d, cy + 2, "yeni dəyişiklik?", SN(26), WHITE, ad, cx)
        flow(d, [(540, 400), (540, 470)], YEL, a, t, pr(lt, 1.2, 2.2))
        flow(d, [(540, 570), (540, 610), (295, 610), (295, 650)], CYAN, a, t, pr(lt, 3, 4))
        flow(d, [(295, 760), (295, 805)], PINK, a, t, pr(lt, 4.6, 5.4))
        flow(d, [(445, 875), (785, 875), (785, 760)], PURP, a, t, pr(lt, 6.4, 7.2))
        if lt > 6.4: ct(d, 885, "BƏLİ → geri get", SB(28), PURP, pr(lt, 6.4, 6.8) * fo, 620)
        flow(d, [(785, 650), (785, 610), (900, 610)], PURP, a, t, 0)
        flow(d, [(860, 760), (860, 1050), (790, 1050)], GREEN, a, t, pr(lt, 8.6, 9.6))
        caps = ["Sorğu deyir: mənə saat 14:00-dakı vəziyyəti göstər.",
                "Oracle vaxtı öz daxili saatına, SCN-ə çevirir. Hər COMMIT SCN-i artırır.",
                "Blokdakı dəyər daha yenidir (SCN 5200 > 5000). Deməli bu, sonradan edilmiş dəyişiklikdir.",
                "Oracle UNDO-ya gedir, köhnə versiyanı tapır və nəticəni qaytarır."]
        caption(d, caps[0 if lt < 2.2 else 1 if lt < 4 else 2 if lt < 7.2 else 3], pr(lt, .6, 1) * fo)

    # 3 VERSION CHAIN
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Versiya zənciri", SB(58), PURP, a)
        ct(d, 310, "Hədəf: SCN 5000 (14:00)", MB(38), YEL, a)
        cards = [("0", "SCN 5200 · 14:05", PINK, "data blok"), ("1200", "SCN 4900 · 13:58", PURP, "UNDO"),
                 ("900", "SCN 4500 · 13:40", PURP, "UNDO"), ("700", "SCN 4000 · 13:10", PURP, "UNDO")]
        ptr = -1 if lt < 1.5 else 0 if lt < 4 else 1
        for k, (v, s, col, kind) in enumerate(cards):
            y = 390 + k * 210; al = pr(lt, .3 + k * .25, .7 + k * .25) * fo
            hit = ptr == 1 and k == 1
            c = GREEN if hit else YEL if ptr == k else col
            glow_box(d, (240, y, 840, y + 150), c, al, None, None, fill=(26, 18, 48) if kind == "UNDO" else CARD)
            d.text((280, y + 22), v, font=MB(64), fill=mix(WHITE, al))
            d.text((520, y + 30), s, font=MN(30), fill=mix(DIM, al))
            d.text((520, y + 82), kind, font=SB(30), fill=mix(col, al))
            if k < 3: flow(d, [(540, y + 150), (540, y + 210)], PURP, al, t, 1, dots=lt > 1)
        if ptr >= 0:
            py = 390 + ptr * 210 + 75
            d.polygon([(200, py), (160, py - 26), (160, py + 26)], fill=mix(YEL, a))
            msg = ("5200 > 5000 → çox yeni, geri get" if ptr == 0 else "4900 ≤ 5000 → TAPILDI ✓")
            ct(d, py + 95 if ptr == 0 else py + 95, "", SN(10), WHITE, 0)
            d.rounded_rectangle((860, py - 40, 1040, py + 40), 16, fill=mix(GREEN if ptr == 1 else YEL, a))
            ct(d, py - 20, "✓" if ptr == 1 else "↓", SB(40), BG, a, 950)
        caps = ["Hər dəyişiklik özündən əvvəlki versiyaya ox saxlayır. Bu oxlar zəncir yaradır.",
                "Blokdakı 0 dəyəri SCN 5200-dədir, hədəfdən yenidir. Oracle bir addım geri gedir.",
                "SCN 4900 ≤ 5000. Saat 14:00-da balans 1200 idi. Dəqiq versiya tapıldı!"]
        caption(d, caps[0 if lt < 1.5 else 1 if lt < 4 else 2], pr(lt, .6, 1) * fo)

    # 4 RESTORE
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Məlumatı bərpa et", SB(60), GREEN, a)
        done = [lt > 2.5 + k * .9 for k in range(5)]
        right = [ORIG[k] if done[k] else 0 for k in range(5)]
        bal_table(d, 70, 360, 480, "14:00 (keçmiş)", ORIG, a, PURP, [GREEN] * 5)
        bal_table(d, 600, 360, 1010, "İNDİ", right, a, PINK, [GREEN if x else RED for x in done])
        for k in range(5):
            y = 360 + 75 + k * 62 + 20; st = 1.8 + k * .9
            if lt > st: flow(d, [(485, y), (595, y)], GREEN, a, t, pr(lt, st, st + .6), dots=False)
        ac = pr(lt, 7.5, 7.9) * fo
        glow_box(d, (110, 860, 970, 980), YEL, ac, "UPDATE  ←  SELECT ... AS OF", None, 36)
        ct(d, 1030, "Bir sorğu ilə 1000 hesab bərpa olunur", SB(42), WHITE, pr(lt, 8.5, 8.9) * fo)
        caps = ["Keçmiş vəziyyəti oxuyuruq və indiki cədvələ geri yazırıq.",
                "Hər hesab 14:00-dakı dəyərini geri alır. Backup-a ehtiyac yoxdur!"]
        caption(d, caps[0 if lt < 6 else 1], pr(lt, .8, 1.2) * fo)

    # 5 FLASHBACK FAMILY HUB
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Flashback ailəsi", SB(60), WHITE, a)
        hub = (390, 600, 690, 720)
        glow_box(d, hub, PURP, pr(lt, .4, .8) * fo, "UNDO", "keçmiş versiyalar", 44, 28)
        kids = [((60, 320, 500, 450), CYAN, "Flashback Query", "AS OF → bir an", 1.5, (390, 640), (280, 450)),
                ((580, 320, 1020, 450), YEL, "Versions Query", "VERSIONS → tarixçə", 3.5, (690, 640), (800, 450)),
                ((60, 870, 500, 1000), GREEN, "Flashback Table", "bütün cədvəl geri", 5.5, (390, 690), (280, 870))]
        for box, col, ti, su, st, p0, p1 in kids:
            al = pr(lt, st, st + .4) * fo
            glow_box(d, box, col, al, ti, su, 34, 28)
            if lt > st: flow(d, [p0, ((p0[0] + p1[0]) / 2, p0[1]), ((p0[0] + p1[0]) / 2, p1[1]), p1], col, a, t, pr(lt, st, st + .8))
        ab = pr(lt, 8, 8.4) * fo
        glow_box(d, (580, 1080, 1020, 1200), PINK, ab, "Recycle Bin", "DROP olunmuş cədvəllər", 34, 26)
        glow_box(d, (580, 870, 1020, 1000), PINK, ab, "Flashback DROP", "TO BEFORE DROP", 34, 28)
        if lt > 8: flow(d, [(800, 1080), (800, 1000)], PINK, a, t, pr(lt, 8.4, 9))
        caps = ["Hamısının mərkəzində UNDO dayanır.",
                "AS OF: bir anın şəkli. VERSIONS BETWEEN: sətrin bütün dəyişiklik tarixçəsi.",
                "Flashback Table bütün cədvəli keçmiş vaxta qaytarır (ROW MOVEMENT lazımdır).",
                "Silinmiş cədvəl isə UNDO-dan yox, Recycle Bin-dən qayıdır."]
        caption(d, caps[0 if lt < 1.5 else 1 if lt < 5.5 else 2 if lt < 8 else 3], pr(lt, .8, 1.2) * fo)

    # 6 LIMITS
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Amma limit var!", SB(60), RED, a)
        labels = [(180, "dünən"), (420, "-2 saat"), (640, "-15 dəq"), (900, "indi")]
        kx = 900 - 200 * pr(lt, 1.5, 3) - 520 * pr(lt, 4.2, 6.2)
        inside = kx >= 600
        timeline(d, 470, a, kx, labels, 900, win=(600, 920))
        ct(d, 545, "UNDO pəncərəsi", SB(30), GREEN, pr(lt, .8, 1.2) * fo, 760)
        st = pr(lt, 1.5, 1.8) * fo
        glow_box(d, (180, 610, 900, 710), GREEN if inside else RED, st, "✓ Keçmiş görünür" if inside else "✗ ORA-01555", None, 40)
        line = [("TRUNCATE  →  UNDO yazmır, geri qayıtmaq olmur", 7), ("ALTER TABLE  →  ORA-01466: struktur dəyişib", 8.5)]
        for k, (tx, s) in enumerate(line):
            al = pr(lt, s, s + .4) * fo
            d.rounded_rectangle((70, 760 + k * 100, W - 70, 840 + k * 100), 18, fill=mix((70, 18, 28), al), outline=mix(RED, al), width=3)
            d.text((100, 780 + k * 100), tx, font=SN(34), fill=mix(WHITE, al))
        caps = ["Keçmişə yalnız UNDO saxlanılan qədər qayıtmaq olar (UNDO_RETENTION).",
                "Pəncərədən kənara çıxsan, köhnə versiya artıq yoxdur.",
                "Bəzi əməliyyatlar flashback-i tamamilə bağlayır."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .8, 1.2) * fo)

    # 7 USE CASES
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Bankda harada lazımdır?", SB(58), WHITE, a)
        cases = [("Səhv UPDATE / DELETE", "dəqiqələr içində bərpa", GREEN),
                 ("Auditor sualı", "dünən 18:00-da balans nə idi?", CYAN),
                 ("EOD yoxlaması", "prosesdən əvvəl və sonra müqayisə", YEL)]
        for k, (h, s, col) in enumerate(cases):
            y = 360 + k * 250; al = pr(lt, .4 + k * 1.5, .8 + k * 1.5) * fo
            glow_box(d, (180, y, 1010, y + 190), col, al)
            ic = (110, y + 95)
            d.ellipse((ic[0] - 55, ic[1] - 55, ic[0] + 55, ic[1] + 55), fill=mix(col, al))
            if k == 0:
                d.arc((ic[0] - 28, ic[1] - 28, ic[0] + 28, ic[1] + 28), 40, 320, fill=mix(BG, al), width=8)
                d.polygon([(ic[0] + 14, ic[1] - 38), (ic[0] + 34, ic[1] - 20), (ic[0] + 8, ic[1] - 14)], fill=mix(BG, al))
            elif k == 1:
                d.ellipse((ic[0] - 26, ic[1] - 30, ic[0] + 14, ic[1] + 10), outline=mix(BG, al), width=7)
                d.line((ic[0] + 8, ic[1] + 4, ic[0] + 30, ic[1] + 28), fill=mix(BG, al), width=9)
            else:
                d.rectangle((ic[0] - 26, ic[1] - 10, ic[0] - 8, ic[1] + 28), fill=mix(BG, al))
                d.rectangle((ic[0] + 6, ic[1] - 30, ic[0] + 24, ic[1] + 28), fill=mix(BG, al))
            d.text((230, y + 40), h, font=SB(42), fill=mix(col, al))
            d.text((230, y + 110), s, font=SN(34), fill=mix(WHITE, al))
        caption(d, "Flashback = təhlükəsizlik kəməri. Amma backup-ı əvəz etmir!", pr(lt, 5, 5.4) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Yadda saxla:", SB(66), WHITE, a)
        items = [("AS OF", "→ keçmiş bir an"), ("SCN", "→ Oracle-ın daxili saatı"),
                 ("UNDO zənciri", "→ köhnə versiyalar"), ("VERSIONS", "→ bütün tarixçə"),
                 ("UNDO pəncərəsi", "→ limit var!")]
        for k, (q, ex) in enumerate(items):
            y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
            d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
            d.text((105, y + 30), q, font=MB(38), fill=mix(GREEN, al))
            d.text((470, y + 32), ex, font=SN(38), fill=mix(WHITE, al))
        caption(d, "Oracle keçmişi unutmur, sadəcə UNDO saxlanılan qədər xatırlayır.", pr(lt, 2, 2.4) * fo)

    # 9 CTA
    else:
        lt = t - T[9]
        ct(d, 440, "Növbəti video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 540, "PARTITIONING", SB(72), YEL, pr(lt, .2, .5))
        ct(d, 650, "Milyardlarla sətri hissələrə bölmək", SB(44), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.5, T[1] + 6, T[2] + 4.5, T[2] + 11, T[3] + 2.5, T[3] + 8, T[4] + 8.5, T[5] + 10, T[6] + 3, T[6] + 10, T[7] + 6, T[8] + 4]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v11_{k}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v11_silent.mp4"], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print("video done")

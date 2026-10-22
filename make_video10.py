from common import *
from make_video5 import arrow, counter
import subprocess, math, sys

T = [0, 6, 18, 32, 46, 60, 72, 84, 94, 100, 106]
DUR = T[-1]; N = FPS * DUR

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

BLK = (110, 470, 520, 700); UND = (560, 470, 970, 700)

def block(d, a, val, tag=None, tagcol=PINK, y0=470):
    x0, _, x1, _ = BLK; y1 = y0 + 230
    d.rounded_rectangle((x0, y0, x1, y1), 24, fill=mix(CARD, a), outline=mix(CYAN, a), width=4)
    ct(d, y0 + 18, "DATA BLOK", SB(30), CYAN, a, (x0 + x1) / 2)
    ct(d, y0 + 62, "Hesab 101", SN(34), WHITE, a, (x0 + x1) / 2)
    ct(d, y0 + 110, str(val), MB(72), YEL, a, (x0 + x1) / 2)
    if tag:
        w = d.textlength(tag, font=SB(26)) + 24
        cx = (x0 + x1) / 2
        d.rounded_rectangle((cx - w / 2, y1 - 8, cx + w / 2, y1 + 32), 14, fill=mix(tagcol, a))
        ct(d, y1 - 4, tag, SB(26), BG, a, cx)

def undo(d, a, items, hl=None, y0=470):
    x0, _, x1, _ = UND; y1 = y0 + 230
    d.rounded_rectangle((x0, y0, x1, y1), 24, fill=mix((26, 18, 48), a), outline=mix(PURP, a), width=4)
    ct(d, y0 + 18, "UNDO", SB(34), PURP, a, (x0 + x1) / 2)
    for k, it in enumerate(items):
        y = y0 + 75 + k * 70; cx = (x0 + x1) / 2
        d.rounded_rectangle((cx - 150, y, cx + 150, y + 58), 12, fill=mix(CARD, a), outline=mix(GREEN if hl == k else PURP, a), width=4 if hl == k else 2)
        ct(d, y + 10, it, MB(34), WHITE, a, cx)

def chip(d, cx, cy, txt, col, a, fs=36):
    w = d.textlength(txt, font=SB(fs)) + 50
    d.rounded_rectangle((cx - w / 2, cy - 35, cx + w / 2, cy + 35), 35, fill=mix(col, a))
    ct(d, cy - fs * .62, txt, SB(fs), BG, a, cx)

def flycard(d, p, x0, y0, x1, y1, txt, a):
    if p <= 0 or p >= 1: return
    x = x0 + (x1 - x0) * p; y = y0 + (y1 - y0) * p - 90 * math.sin(math.pi * p)
    d.rounded_rectangle((x - 95, y - 34, x + 95, y + 34), 14, fill=mix(YEL, a))
    ct(d, y - 24, txt, MB(40), BG, a, x)

def line_items(d, y0, items, a, fs=34):
    for k, (tx, col, al) in enumerate(items):
        if al <= 0: continue
        y = y0 + k * 72
        d.rounded_rectangle((70, y, W - 70, y + 60), 14, fill=mix(CARD, al * a))
        d.text((100, y + 12), tx, font=SN(fs), fill=mix(col, al * a))

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
        ct(d, 260, "Sən hesabat oxuyursan...", SB(60), WHITE, a)
        ct(d, 350, "eyni anda kimsə balansı dəyişir", SB(46), PINK, pr(lt, .8, 1.2) * fo)
        chip(d, 300, 520, "Oxuyan (R)", CYAN, pr(lt, 1.2, 1.5) * fo)
        chip(d, 780, 520, "Yazan (W)", PINK, pr(lt, 1.5, 1.8) * fo)
        ab = pr(lt, 2, 2.4) * fo
        block(d, ab, 1000 if lt < 3 else 500, y0=640)
        arrow(d, 300, 560, 250, 635, CYAN, ab, 6); arrow(d, 780, 560, 470, 635, PINK, ab, 6)
        ct(d, 950, "Hesabat hansı rəqəmi görəcək?", SB(54), YEL, pr(lt, 3.4, 3.8) * fo)
        caption(d, "Oracle-ın ən gözəl sirlərindən biri: UNDO. Gəl addım-addım görək.", pr(lt, 3.8, 4.2) * fo)

    # 1 PROBLEM
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Problem", SB(64), WHITE, a)
        val = 1000 if lt < 2.5 else 500
        block(d, a, val, "COMMIT olunmayıb" if lt >= 2.5 else None)
        ct(d, 480, "W:", SB(40), PINK, pr(lt, 1, 1.3) * fo, 640)
        d.text((600, 540), "UPDATE ...", font=MB(34), fill=mix(PINK, pr(lt, 1, 1.3) * fo))
        d.text((600, 590), "balance = 500", font=MB(34), fill=mix(WHITE, pr(lt, 1, 1.3) * fo))
        ar = pr(lt, 4, 4.3) * fo
        d.text((600, 650), "R: SELECT balance?", font=MB(32), fill=mix(CYAN, ar))
        line_items(d, 800, [
            ("500?  → təsdiqlənməmiş məlumat (dirty read) ✗", RED, pr(lt, 5.5, 5.8)),
            ("Gözləsin?  → hamı bir-birini gözləyir ✗", RED, pr(lt, 7, 7.3)),
            ("1000  → son COMMIT olunmuş dəyər ✓", GREEN, pr(lt, 8.5, 8.8))], fo)
        ap = pr(lt, 9.8, 10.2) * fo
        d.rounded_rectangle((70, 1040, W - 70, 1190), 22, fill=mix((14, 50, 36), ap), outline=mix(GREEN, ap), width=4)
        ct(d, 1060, "Oxuyan yazanı bloklamır,", SB(40), GREEN, ap)
        ct(d, 1115, "yazan oxuyanı bloklamır!", SB(40), GREEN, ap)
        caps = ["W hesabın balansını 500 edir, amma hələ COMMIT etməyib.",
                "Eyni anda R balansı oxuyur. Nə görməlidir?",
                "Oracle-ın cavabı: R gözləmir və son COMMIT olunmuş dəyəri, 1000-i görür."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8.5 else 2], pr(lt, 1.2, 1.6) * fo)

    # 2 UNDO WRITE
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 250, "UPDATE zamanı nə baş verir?", SB(56), WHITE, a)
        p = pr(lt, 1.5, 3)
        items = ["1000"] if lt >= 3 else []
        block(d, a, 1000 if lt < 3.6 else 500, "kilid: W" if lt >= 3.6 else None)
        undo(d, a, items, hl=0 if 3 <= lt < 5 else None)
        flycard(d, p, 315, 610, 765, 580, "1000", a)
        line_items(d, 800, [
            ("1. Köhnə dəyər (1000) UNDO-ya köçürülür", PURP, pr(lt, 1.5, 1.8)),
            ("2. Yeni dəyər (500) bloka yazılır", YEL, pr(lt, 3.6, 3.9)),
            ("3. Sətir W tərəfindən kilidlənir", PINK, pr(lt, 5.5, 5.8)),
            ("UNDO = dəyişiklikdən ƏVVƏLKİ vəziyyət", GREEN, pr(lt, 8, 8.3))], fo)
        caption(d, "Oracle hər dəyişiklikdən əvvəl köhnə dəyərin surətini UNDO-da saxlayır. Bütün sirr budur!", pr(lt, 1.6, 2) * fo)

    # 3 READ CONSISTENCY
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Oxuyan nəyi görür?", SB(58), WHITE, a)
        # SCN timeline
        al = pr(lt, .4, .8) * fo
        d.line((120, 380, 960, 380), fill=mix(DIM, al), width=6)
        for x, lab, col, st in [(300, "SCN 100: R başladı", CYAN, .6), (720, "SCN 105: W dəyişdi", PINK, 1.6)]:
            am = pr(lt, st, st + .3) * fo
            d.ellipse((x - 14, 366, x + 14, 394), fill=mix(col, am))
            ct(d, 405, lab, SB(30), col, am, x)
        block(d, a, 500, "SCN 105 · commit yox")
        undo(d, a, ["1000"], hl=0 if lt > 7 else None)
        chip(d, 315, 820, "R  (SCN 100)", CYAN, pr(lt, 2.5, 2.9) * fo)
        if lt > 4: arrow(d, 315, 785, 315, 735, CYAN, pr(lt, 4, 4.3) * fo, 6)
        a5 = pr(lt, 5, 5.4) * fo
        ct(d, 900, "105 > 100 → bu dəyişiklik R üçün \"gələcəkdir\"", SN(36), YEL, a5)
        if lt > 7: arrow(d, 520, 600, 560, 600, PURP, pr(lt, 7, 7.3) * fo, 6)
        flycard(d, pr(lt, 8.3, 9.6), 765, 580, 600, 830, "1000", a)
        ar = pr(lt, 9.8, 10.2) * fo
        d.rounded_rectangle((560, 790, 990, 860), 18, fill=mix(GREEN, ar))
        ct(d, 802, "balance = 1000 ✓", MB(38), BG, ar, 775)
        line_items(d, 980, [("Hər sorğu başladığı anın \"fotosunu\" görür", GREEN, pr(lt, 10.5, 10.8))], fo, 36)
        caps = ["R sorğusu SCN 100 anında başlayıb. W isə dəyişikliyi SCN 105-də edib.",
                "R bloku oxuyanda görür ki, bu dəyişiklik özündən sonra baş verib.",
                "Oracle köhnə versiyanı UNDO-dan bərpa edir və R-ə 1000 qaytarır. Gözləmə yoxdur!"]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .8, 1.2) * fo)

    # 4 LONG REPORT
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Bank hesabatı: ümumi balans", SB(54), WHITE, a)
        rows = 10; rh = 66; y0 = 330
        ptr = min(rows, int(max(0, lt - 1) / 1.0)) if lt > 1 else -1
        moved = lt >= 4.2
        for r in range(rows):
            y = y0 + r * rh; read = r < ptr; cur = r == ptr
            val = 1000
            if moved and r == 1: val = 1300
            if moved and r == 8: val = 700
            fill = (40, 60, 95) if read else CARD
            d.rounded_rectangle((90, y, 600, y + rh - 10), 12, fill=mix(fill, a), outline=mix(YEL if cur else OFFB, a), width=4 if cur else 2)
            d.text((115, y + 12), f"Hesab A{r + 1}", font=SN(32), fill=mix(WHITE, a))
            col = PINK if (moved and r in (1, 8)) else WHITE
            d.text((420, y + 10), str(val), font=MB(36), fill=mix(col, a))
            if moved and r == 8 and ptr >= 8:
                d.text((620, y + 10), "UNDO → 1000", font=MB(32), fill=mix(PURP, a))
        if 4.2 <= lt < 8:
            at = pr(lt, 4.2, 4.6) * fo
            arrow(d, 600, y0 + 8 * rh + 25, 600, y0 + rh + 25, PINK, at, 6)
            ct(d, y0 + 4 * rh, "köçürmə 300", SB(34), PINK, at, 800)
            ct(d, y0 + 4 * rh + 50, "+ COMMIT", MB(32), PINK, at, 800)
        ar = pr(lt, 11.2, 11.6) * fo
        yb = y0 + rows * rh + 20
        d.rounded_rectangle((70, yb, 520, yb + 120), 20, fill=mix((70, 18, 28), ar), outline=mix(RED, ar), width=4)
        ct(d, yb + 12, "Naiv oxuma", SB(32), RED, ar, 295); ct(d, yb + 55, "9 700 ✗", MB(44), RED, ar, 295)
        d.rounded_rectangle((560, yb, 1010, yb + 120), 20, fill=mix((14, 50, 36), ar), outline=mix(GREEN, ar), width=4)
        ct(d, yb + 12, "Oracle", SB(32), GREEN, ar, 785); ct(d, yb + 55, "10 000 ✓", MB(44), GREEN, ar, 785)
        caps = ["Hesabat 10 hesabı bir-bir oxuyur. Hər birində 1000 var, cəmi 10 000.",
                "Oxuma davam edərkən A9-dan A2-yə 300 köçürülür. A2 artıq oxunub, A9 hələ yox!",
                "Oracle A9-u sorğunun başladığı ana görə UNDO-dan oxuyur: 1000. Cəm düzgün qalır!"]
        caption(d, caps[0 if lt < 4.2 else 1 if lt < 9 else 2], pr(lt, .8, 1.2) * fo)

    # 5 ROLLBACK
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 250, "UNDO-nun 2-ci işi: ROLLBACK", SB(54), YEL, a)
        restored = lt >= 4
        block(d, a, 1000 if restored else 500, None if restored else "kilid: W")
        undo(d, a, [] if restored else ["1000"])
        chip(d, 540, 820, "W: ROLLBACK;", PINK, pr(lt, 1.2, 1.6) * fo)
        flycard(d, pr(lt, 2.4, 3.9), 765, 580, 315, 610, "1000", a)
        if restored: ct(d, 920, "Köhnə dəyər bərpa olundu ✓", SB(46), GREEN, pr(lt, 4, 4.4) * fo)
        line_items(d, 1020, [("Sistem çöksə də: commit olunmamışlar geri alınır", WHITE, pr(lt, 6, 6.4))], fo, 34)
        caption(d, "ROLLBACK edəndə Oracle köhnə dəyəri sadəcə UNDO-dan götürüb geri yazır.", pr(lt, 1.6, 2) * fo)

    # 6 ORA-01555
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Tələ: ORA-01555", SB(60), RED, a)
        cx, cy, R = 540, 680, 230
        ct(d, cy - 30, "UNDO", SB(44), PURP, a, cx)
        ct(d, cy + 25, "dairəvi yaddaş", SN(32), DIM, a, cx)
        wptr = (lt * 0.75) % 8 if lt < 6.2 else 5.2
        need = 5
        for k in range(8):
            a0 = -90 + k * 45; a1 = a0 + 43
            col = OFFB
            if k == need: col = CYAN
            if k < int(wptr) or (lt >= 6.2 and k == need): col = PINK if k != need else (RED if lt >= 6.2 else CYAN)
            if k == need and lt >= 6.2 and int(lt * 6) % 2: col = RED
            d.pieslice((cx - R, cy - R, cx + R, cy + R), a0, a1, fill=mix(col, a))
        d.ellipse((cx - R + 70, cy - R + 70, cx + R - 70, cy + R - 70), fill=mix(BG, a))
        ct(d, cy - 30, "UNDO", SB(44), PURP, a, cx)
        ct(d, cy + 25, "dairəvi yaddaş", SN(32), DIM, a, cx)
        ang = math.radians(-90 + wptr * 45)
        arrow(d, cx, cy, cx + (R + 40) * math.cos(ang), cy + (R + 40) * math.sin(ang), YEL, a, 6)
        an = pr(lt, .8, 1.2) * fo
        d.text((90, 960), "■ R-in lazım olan köhnə dəyəri", font=SN(32), fill=mix(CYAN, an))
        d.text((90, 1010), "■ yeni tranzaksiyalar üzərinə yazır", font=SN(32), fill=mix(PINK, an))
        ae = pr(lt, 6.4, 6.7) * fo; sh = 8 * math.sin(lt * 50) * (1 - pr(lt, 6.4, 7.2))
        d.rounded_rectangle((60 + sh, 1080, W - 60 + sh, 1220), 22, fill=mix((70, 18, 28), ae), outline=mix(RED, ae), width=5)
        d.text((95 + sh, 1095), "ORA-01555", font=MB(50), fill=mix(RED, ae))
        d.text((95 + sh, 1160), "snapshot too old", font=MN(34), fill=mix(WHITE, ae))
        caps = ["UNDO sonsuz deyil. COMMIT olunmuş köhnə dəyərlər bir müddət sonra üzərinə yazıla bilər.",
                "Uzun sorğu köhnə versiyaya ehtiyac duyanda, o artıq silinib ola bilər. Nəticə: ORA-01555."]
        caption(d, caps[0 if lt < 6.2 else 1], pr(lt, 1.2, 1.6) * fo)

    # 7 FIXES
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 250, "ORA-01555-dən necə qaçmaq?", SB(54), GREEN, a)
        cards = [("UNDO_RETENTION / UNDO ölçüsü", "köhnə dəyərləri daha uzun saxla"),
                 ("Uzun sorğunu sürətləndir", "indeks, tuning, daha az sətir"),
                 ("Loop içində COMMIT etmə", "açıq kursoru oxuyarkən (fetch across commit)")]
        for k, (h, s) in enumerate(cards):
            y = 380 + k * 230; al = pr(lt, .4 + k * 1.6, .8 + k * 1.6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 200), 26, fill=mix(CARD, al), outline=mix(GREEN, al), width=4)
            d.text((110, y + 35), f"{k + 1}. " + h, font=SB(40), fill=mix(YEL, al))
            d.text((110, y + 115), s, font=SN(34), fill=mix(WHITE, al))
        caption(d, "Ən çox rast gəlinən səbəb: böyük kursoru oxuyarkən hər sətirdə COMMIT etmək.", pr(lt, 5.5, 5.9) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Yadda saxla:", SB(66), WHITE, a)
        items = [("UPDATE", "→ köhnə dəyər UNDO-ya"), ("Oxuyan", "→ yazanı gözləmir"),
                 ("Hər sorğu", "→ başlanğıc anın fotosu"), ("ROLLBACK", "→ UNDO-dan bərpa"),
                 ("ORA-01555", "→ UNDO artıq yoxdur")]
        for k, (q, ex) in enumerate(items):
            y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
            d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
            d.text((105, y + 30), q, font=MB(38), fill=mix(GREEN, al))
            d.text((440, y + 32), ex, font=SN(38), fill=mix(WHITE, al))
        caption(d, "UNDO sayəsində Oracle eyni anda həm sürətli, həm də dəqiqdir.", pr(lt, 2, 2.4) * fo)

    # 9 CTA
    else:
        lt = t - T[9]
        ct(d, 440, "Növbəti video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 540, "FLASHBACK QUERY", SB(68), YEL, pr(lt, .2, .5))
        ct(d, 650, "Keçmişə səyahət: AS OF TIMESTAMP", SB(44), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.5, T[1] + 10.5, T[2] + 9, T[3] + 10.5, T[4] + 6, T[4] + 12.5, T[5] + 7, T[6] + 4, T[6] + 8, T[7] + 7, T[8] + 4, T[9] + 3]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v10_{k}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v10_silent.mp4"], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print("video done")

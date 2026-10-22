from common import *
from make_video5 import arrow
import subprocess, math, sys

T = [0, 6, 16, 30, 42, 54, 66, 78, 90, 98, 104]
DUR = T[-1]; N = FPS * DUR
SCOL = {"A": CYAN, "B": PINK}
ACC = {101: (290, 900), 202: (790, 900)}
SES = {"A": (270, 470), "B": (810, 470)}
SUB = {"A": "101 → 202", "B": "202 → 101"}

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def lock_icon(d, x, y, col, a, s=1.0):
    d.arc((x - 18 * s, y - 34 * s, x + 18 * s, y + 2 * s), 180, 360, fill=mix(col, a), width=int(7 * s))
    d.line((x - 18 * s, y - 16 * s, x - 18 * s, y), fill=mix(col, a), width=int(7 * s))
    d.line((x + 18 * s, y - 16 * s, x + 18 * s, y), fill=mix(col, a), width=int(7 * s))
    d.rounded_rectangle((x - 28 * s, y - 2 * s, x + 28 * s, y + 40 * s), 8, fill=mix(col, a))
    d.ellipse((x - 6 * s, y + 10 * s, x + 6 * s, y + 22 * s), fill=mix(BG, a))

def hourglass(d, x, y, a, t):
    c = mix(YEL, a); r = (t * 90) % 180
    pts = [(-14, -20), (14, -20), (-14, 20), (14, 20)]
    ca, sa = math.cos(math.radians(r)), math.sin(math.radians(r))
    P = [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]
    d.polygon([P[0], P[1], P[2], P[3]], outline=c, width=5)

def dashed(d, x0, y0, x1, y1, col, a, w=6, dash=22):
    L = math.dist((x0, y0), (x1, y1)); n = int(L / dash)
    for k in range(0, n, 2):
        s, e = k / n, min(1, (k + 1) / n)
        d.line((x0 + (x1 - x0) * s, y0 + (y1 - y0) * s, x0 + (x1 - x0) * e, y0 + (y1 - y0) * e), fill=mix(col, a), width=w)
    ang = math.atan2(y1 - y0, x1 - x0)
    for sgn in (-.45, .45):
        d.line((x1, y1, x1 - 24 * math.cos(ang + sgn), y1 - 24 * math.sin(ang + sgn)), fill=mix(col, a), width=w)

def world(d, a, t, holds=None, waits=(), accs=(101, 202), sess=("A", "B"), flash=None, fail=None, sub=True):
    holds = holds or {}
    for acc in accs:
        x, y = ACC[acc]; own = holds.get(acc)
        d.rounded_rectangle((x - 145, y - 85, x + 145, y + 85), 22, fill=mix(CARD, a), outline=mix(SCOL[own] if own else OFFB, a), width=6 if own else 3)
        ct(d, y - 55, f"Hesab {acc}", SB(40), WHITE, a, x)
        ct(d, y + 5, "1 000 AZN", MN(36), DIM, a, x)
        if own: lock_icon(d, x + 120, y - 95, SCOL[own], a)
    for s in sess:
        x, y = SES[s]
        d.rounded_rectangle((x - 160, y - 65, x + 160, y + 65), 22, fill=mix(CARD, a), outline=mix(SCOL[s], a), width=5)
        ct(d, y - 50 if sub else y - 25, f"Sessiya {s}", SB(42), SCOL[s], a, x)
        if sub: ct(d, y + 5, SUB[s], MN(36), WHITE, a, x)
        if any(w[0] == s for w in waits): hourglass(d, x + 132 if s == "A" else x - 132, y - 30, a, t)
        if fail == s:
            d.rounded_rectangle((x - 160, y - 65, x + 160, y + 65), 22, outline=mix(RED, a), width=9)
    for acc, s in holds.items():
        if s in sess and acc in accs:
            sx, sy = SES[s]; ax, ay = ACC[acc]
            d.line((sx, sy + 65, ax, ay - 85), fill=mix(SCOL[s], a), width=9)
    for s, acc in waits:
        sx, sy = SES[s]; ax, ay = ACC[acc]
        col = RED if flash == (s, acc) and int(t * 6) % 2 == 0 else YEL
        dashed(d, sx + (25 if acc > 150 and s == "A" else -25 if s == "B" else 0), sy + 65, ax, ay - 92, col, a)

def steps_box(d, y0, items, a):
    for k, (txt, col, al) in enumerate(items):
        if al <= 0: continue
        y = y0 + k * 68
        d.rounded_rectangle((70, y, W - 70, y + 58), 14, fill=mix(CARD, al * a))
        d.text((100, y + 12), txt, font=SN(34), fill=mix(col, al * a))

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
        ct(d, 250, "Eyni anda iki köçürmə...", SB(60), WHITE, a)
        world(d, a * .9, t, {101: "A", 202: "B"}, [("A", 202), ("B", 101)] if lt > 1.5 else [])
        ae = pr(lt, 2.4, 2.7) * fo; sh = 10 * math.sin(lt * 50) * (1 - pr(lt, 2.4, 3.2))
        d.rounded_rectangle((60 + sh, 1060, W - 60 + sh, 1220), 24, fill=mix((70, 18, 28), ae), outline=mix(RED, ae), width=5)
        d.text((100 + sh, 1080), "ORA-00060", font=MB(56), fill=mix(RED, ae))
        d.text((100 + sh, 1155), "deadlock detected while waiting for resource", font=MN(28), fill=mix(WHITE, ae))
        ct(d, 1270, "Nə baş verdi?", SB(70), YEL, pr(lt, 3.6, 4) * fo)
        caption(d, "İki tranzaksiya bir-birini sonsuz gözləyir. Buna DEADLOCK deyilir.", pr(lt, 3.8, 4.2) * fo)

    # 1 LOCK BASICS
    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .4) * fo
        ct(d, 250, "UPDATE sətri KİLİDLƏYİR", SB(60), YEL, a)
        holds = {}; waits = []
        if 1.5 <= lt < 6.5: holds = {101: "A"}
        if 3.5 <= lt < 6.5: waits = [("B", 101)]
        if lt >= 7: holds = {101: "B"}
        world(d, a, t, holds, waits, accs=(101,), sub=False)
        if 6.5 <= lt < 7.5:
            ct(d, 610, "COMMIT ✓", MB(48), GREEN, a * (1 - pr(lt, 7.1, 7.5)), 270)
        caps = ["Sessiya A hesab 101-i yeniləyir. Oracle o sətri kilidləyir.",
                "Sessiya B eyni sətri yeniləmək istəyir, amma GÖZLƏMƏLİDİR.",
                "A COMMIT etdi, kilid açıldı. İndi B davam edə bilər."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 6.5 else 2], pr(lt, 1.2, 1.6) * fo)

    # 2 SCENARIO
    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Eyni anda iki köçürmə:", SB(60), WHITE, a)
        holds = {}; waits = []
        if lt >= 2: holds[101] = "A"
        if lt >= 5: holds[202] = "B"
        if lt >= 8.5: waits.append(("A", 202))
        if lt >= 11: waits.append(("B", 101))
        world(d, a, t, holds, waits)
        steps_box(d, 1100, [
            ("1. A: UPDATE hesab 101  →  kilid ✓", CYAN, pr(lt, 2, 2.3)),
            ("2. B: UPDATE hesab 202  →  kilid ✓", PINK, pr(lt, 5, 5.3)),
            ("3. A: hesab 202 lazımdır  →  GÖZLƏ", YEL, pr(lt, 8.5, 8.8)),
            ("4. B: hesab 101 lazımdır  →  GÖZLƏ", YEL, pr(lt, 11, 11.3))], fo)
        caption(d, "A 101-dən 202-yə, B isə 202-dən 101-ə pul köçürür. Hər biri əvvəlcə öz hesabını kilidləyir.", pr(lt, .6, 1) * fo)

    # 3 CYCLE
    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .3) * fo
        p = 1 + .05 * math.sin(lt * 7)
        ct(d, 230, "DEADLOCK!", SB(int(90 * p)), RED, a)
        world(d, a, t, {101: "A", 202: "B"}, [("A", 202), ("B", 101)], flash=("A", 202) if lt < 6 else ("B", 101))
        steps_box(d, 1100, [
            ("A  →  B-nin kilidini gözləyir", CYAN, pr(lt, 1, 1.3)),
            ("B  →  A-nın kilidini gözləyir", PINK, pr(lt, 2, 2.3)),
            ("Heç kim irəliləyə bilmir. Sonsuz dövr!", RED, pr(lt, 3.5, 3.8))], fo)
        caption(d, "Dar körpüdə üz-üzə gələn iki maşın kimi: heç biri geri çəkilmirsə, ikisi də əbədi gözləyir.", pr(lt, 5.5, 6) * fo)

    # 4 ORACLE RESOLVES
    elif t < T[5]:
        lt, fo = sc(t, 4); a = pr(lt, 0, .4) * fo
        ct(d, 250, "Oracle bunu özü aşkarlayır", SB(56), GREEN, a)
        holds = {101: "A", 202: "B"}; waits = [("A", 202), ("B", 101)]; fail = None
        if lt >= 3: waits = [("A", 202)]; fail = "B"
        if lt >= 8: holds = {101: "A"}
        if lt >= 9: holds = {101: "A", 202: "A"}; waits = []
        if lt >= 10.5: holds = {}
        world(d, a, t, holds, waits, flash=("B", 101) if lt < 3 else None, fail=fail if lt < 8 else None)
        ae = pr(lt, 3, 3.3) * fo * (1 - pr(lt, 7.6, 8))
        d.rounded_rectangle((540, 590, 1020, 690), 18, fill=mix((70, 18, 28), ae), outline=mix(RED, ae), width=4)
        ct(d, 612, "B: ORA-00060", MB(44), RED, ae, 780)
        an = pr(lt, 5, 5.4) * fo
        d.rounded_rectangle((70, 1100, W - 70, 1260), 22, fill=mix((60, 40, 10), an), outline=mix(YEL, an), width=4)
        ct(d, 1120, "Yalnız SON əmr geri alınır!", SB(44), YEL, an)
        ct(d, 1185, "B hələ də 202-ni saxlayır → ROLLBACK et", SN(38), WHITE, an)
        if lt >= 8: ct(d, 1290, "B: ROLLBACK  →  A: 202 ✓  →  COMMIT ✓", MB(36), GREEN, pr(lt, 8, 8.4) * fo)
        caps = ["Oracle bir neçə saniyə ərzində dövrü tapır.",
                "Sessiyalardan birinin əmri ORA-00060 xətası ilə dayandırılır.",
                "Diqqət: tranzaksiya yox, yalnız son əmr ləğv olunur. Kod mütləq ROLLBACK etməlidir.",
                "B ROLLBACK etdi, kilid açıldı. A işini bitirdi. B köçürməni yenidən cəhd edə bilər."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5 else 2 if lt < 8 else 3], pr(lt, .8, 1.2) * fo)

    # 5 FIX 1: ORDER
    elif t < T[6]:
        lt, fo = sc(t, 5); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Həll 1: həmişə EYNİ SIRA", SB(56), GREEN, a)
        ct(d, 320, "əvvəlcə kiçik ID, sonra böyük ID", SN(40), WHITE, a)
        holds = {}; waits = []
        if lt >= 1.5: holds[101] = "A"
        if lt >= 3: waits = [("B", 101)]
        if lt >= 5: holds[202] = "A"
        if lt >= 7: holds = {101: "B"}; waits = []
        if lt >= 9: holds = {101: "B", 202: "B"}
        if lt >= 10.5: holds = {}
        world(d, a, t, holds, waits)
        if 7 <= lt < 8: ct(d, 610, "A: COMMIT ✓", MB(40), GREEN, a, 270)
        lines = ["UPDATE accounts ...", "  WHERE id = LEAST(:a, :b);", "UPDATE accounts ...", "  WHERE id = GREATEST(:a, :b);"]
        ac = pr(lt, .6, 1) * fo
        d.rounded_rectangle((60, 1080, W - 60, 1380), 22, fill=mix((16, 22, 42), ac), outline=mix((50, 70, 120), ac), width=3)
        for k, ln in enumerate(lines):
            d.text((95, 1105 + k * 66), ln, font=MB(38), fill=mix(CYAN if ln.startswith("UPDATE") else WHITE, ac))
        caps = ["Hər iki sessiya əvvəlcə 101-i kilidləməyə çalışır.",
                "B ilk addımda gözləyir, amma heç nə saxlamır. Dövr yaranmır!",
                "A işini bitirib COMMIT edir, sonra B rahatca davam edir."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, 1, 1.4) * fo)

    # 6 FIX 2: NOWAIT
    elif t < T[7]:
        lt, fo = sc(t, 6); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Həll 2: gözləməni məhdudlaşdır", SB(50), GREEN, a)
        ct(d, 315, "Qısa tranzaksiya + gözləmə limiti", SN(42), WHITE, a)
        ac = pr(lt, .5, .9) * fo
        lines = ["SELECT * FROM accounts", " WHERE id = 101", "   FOR UPDATE NOWAIT;"]
        d.rounded_rectangle((60, 400, W - 60, 660), 22, fill=mix((16, 22, 42), ac), outline=mix((50, 70, 120), ac), width=3)
        n = int(max(0, (lt - .8) / .03)); shown = "\n".join(lines)[:n]
        for k, ln in enumerate(shown.split("\n")):
            d.text((95, 430 + k * 70), ln, font=MB(42), fill=mix(YEL if "NOWAIT" in ln else CYAN if ln.startswith("SELECT") else WHITE, ac))
        ar = pr(lt, 2.6, 3) * fo
        d.rounded_rectangle((60, 690, W - 60, 830), 22, fill=mix((70, 18, 28), ar), outline=mix(RED, ar), width=4)
        d.text((95, 710), "ORA-00054: resource busy", font=MB(40), fill=mix(RED, ar))
        d.text((95, 770), "Gözləmə yox, dərhal xəta → yenidən cəhd et", font=SN(34), fill=mix(WHITE, ar))
        aw = pr(lt, 5, 5.4) * fo
        d.rounded_rectangle((60, 860, W - 60, 1000), 22, fill=mix(CARD, aw), outline=mix(CYAN, aw), width=4)
        d.text((95, 880), "FOR UPDATE WAIT 5", font=MB(40), fill=mix(CYAN, aw))
        d.text((95, 940), "5 saniyə gözlə, sonra ORA-30006", font=SN(34), fill=mix(WHITE, aw))
        tips = [("✓ COMMIT-i gecikdirmə", GREEN), ("✓ Tranzaksiya içində istifadəçini gözləmə", GREEN)]
        for k, (tx, c) in enumerate(tips):
            al = pr(lt, 7.5 + k * .6, 7.9 + k * .6) * fo
            d.rounded_rectangle((70, 1040 + k * 80, W - 70, 1105 + k * 80), 14, fill=mix(CARD, al))
            d.text((100, 1052 + k * 80), tx, font=SN(36), fill=mix(c, al))
        caption(d, "Kilid nə qədər qısa saxlanılırsa, deadlock ehtimalı bir o qədər az olur.", pr(lt, 7, 7.4) * fo)

    # 7 FIX 3: FK INDEX
    elif t < T[8]:
        lt, fo = sc(t, 7); a = pr(lt, 0, .4) * fo
        ct(d, 240, "Gizli səbəb:", SB(56), RED, a)
        ct(d, 320, "indekssiz FOREIGN KEY", MB(48), YEL, a)
        fixed = lt >= 7
        ap = pr(lt, .5, .9) * fo
        d.rounded_rectangle((70, 410, 470, 610), 20, fill=mix(CARD, ap), outline=mix(CYAN, ap), width=4)
        ct(d, 425, "CLIENTS", SB(38), CYAN, ap, 270)
        for k, r in enumerate(["7  Əli", "8  Leyla"]):
            if k == 0 and lt > 2: d.rounded_rectangle((85, 485, 455, 535), 10, fill=mix((80, 22, 32), ap))
            d.text((110, 490 + k * 55), r, font=MN(34), fill=mix(WHITE, ap))
        arrow(d, 470, 510, 600, 560, DIM, ap, 4)
        ct(d, 450, "FK", MB(32), DIM, ap, 540)
        d.rounded_rectangle((600, 410, 1010, 860), 20, fill=mix(CARD, ap), outline=mix(PINK, ap), width=4)
        ct(d, 425, "ACCOUNTS", SB(38), PINK, ap, 805)
        rows = [("AZ01", "7"), ("AZ02", "8"), ("AZ03", "7"), ("AZ04", "9"), ("AZ05", "8"), ("AZ06", "3")]
        for k, (acn, cid) in enumerate(rows):
            y = 480 + k * 60
            if fixed and cid == "7" and lt > 8.5: d.rounded_rectangle((615, y - 6, 995, y + 48), 10, fill=mix((70, 60, 20), ap))
            d.text((630, y), acn, font=MN(32), fill=mix(WHITE, ap)); d.text((820, y), "client " + cid, font=MN(30), fill=mix(DIM, ap))
        if 2.5 <= lt < 7:
            al = pr(lt, 2.5, 2.9) * fo
            d.rounded_rectangle((600, 410, 1010, 860), 20, outline=mix(RED, al), width=10)
            lock_icon(d, 990, 410, RED, al, 1.2)
            ct(d, 880, "Bütün cədvəl kilidli!", SB(40), RED, pr(lt, 3, 3.3) * fo, 805)
        ac = pr(lt, .3, .6) * fo
        d.text((90, 680), "DELETE FROM clients", font=MB(34), fill=mix(CYAN, ac))
        d.text((90, 730), " WHERE id = 7;", font=MB(34), fill=mix(WHITE, ac))
        if fixed:
            af = pr(lt, 7, 7.4) * fo
            d.rounded_rectangle((60, 950, W - 60, 1130), 22, fill=mix((14, 50, 36), af), outline=mix(GREEN, af), width=4)
            d.text((95, 975), "CREATE INDEX idx_acc_client", font=MB(38), fill=mix(GREEN, af))
            d.text((95, 1040), "    ON accounts(client_id);", font=MB(38), fill=mix(WHITE, af))
            ct(d, 1160, "✓ Yalnız əlaqəli sətirlər yoxlanır", SB(40), GREEN, pr(lt, 8.5, 8.9) * fo)
        caps = ["Müştəri silinir. Oracle uşaq cədvəldə ona bağlı hesab olub-olmadığını yoxlamalıdır.",
                "client_id-də indeks yoxdursa, Oracle bütün ACCOUNTS cədvəlini kilidləyir. Digər sessiyalar ilişib qalır!",
                "Həll: FOREIGN KEY sütununa həmişə indeks yarat."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 8 RECAP
    elif t < T[9]:
        lt, fo = sc(t, 8); a = pr(lt, 0, .3) * fo
        ct(d, 270, "Yadda saxla:", SB(66), WHITE, a)
        items = [("Eyni sıra", "→ kiçik ID əvvəl"), ("Qısa tranzaksiya", "→ tez COMMIT"),
                 ("NOWAIT / WAIT n", "→ sonsuz gözləmə yox"), ("FK sütunu", "→ mütləq indeks"),
                 ("ORA-00060", "→ ROLLBACK + təkrar")]
        for k, (q, ex) in enumerate(items):
            y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
            d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
            d.text((105, y + 30), q, font=MB(38), fill=mix(GREEN, al))
            d.text((520, y + 32), ex, font=SN(38), fill=mix(WHITE, al))
        caption(d, "Deadlock bazanın xətası deyil, tətbiqin dizayn xətasıdır.", pr(lt, 2, 2.4) * fo)

    # 9 CTA
    else:
        lt = t - T[9]
        ct(d, 440, "Növbəti video:", SB(60), DIM, pr(lt, 0, .3))
        ct(d, 540, "BIND dəyişənləri", SB(72), YEL, pr(lt, .2, .5))
        ct(d, 650, "Hard parse vs Soft parse", MB(46), WHITE, pr(lt, .4, .7))
        ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
        ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
        ct(d, 1040, "izlə · saxla · dostuna göndər", SN(46), DIM, pr(lt, 1.3, 1.7))
    return im

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [4.5, T[1] + 5, T[2] + 12, T[3] + 7, T[4] + 6, T[4] + 9.5, T[5] + 4, T[6] + 9, T[7] + 4, T[7] + 9.5, T[8] + 5, T[9] + 3]
        for k, p_ in enumerate(pts): frame(int(p_ * FPS)).save(f"v8_{k}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "v8_silent.mp4"], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print("video done")

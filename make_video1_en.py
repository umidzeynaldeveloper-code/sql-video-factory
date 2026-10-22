from common import *
import subprocess, math, json, sys

J = json.load(open("/home/claude/en/n1.json"))
LINES, DURS = J["lines"], J["durs"]
LEAD = 0.3
T = [0]
for k, dd in enumerate(DURS): T.append(T[-1] + dd + LEAD + (1.6 if k == len(DURS) - 1 else 0.6))
DUR = T[-1]; N = int(FPS * DUR)

def when(k, word, nth=0):
    s = LINES[k]; idx = -1
    for _ in range(nth + 1): idx = s.index(word, idx + 1)
    return LEAD + DURS[k] * idx / len(s)

def sc(t, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

LET = [("S", 83, "01010011"), ("Q", 81, "01010001"), ("L", 76, "01001100")]

def frame(i):
    t = i / FPS
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)

    if t < T[1]:
        lt, fo = sc(t, 0); a = pr(lt, 0, .5) * fo
        ct(d, 520, "You type 'SQL'...", SB(70), WHITE, a)
        sc_ = 1 + .05 * math.sin(t * 6)
        ct(d, 680, "SQL", MB(int(230 * sc_)), GREEN, a)
        t1 = when(0, "But")
        ct(d, 1000, "The computer sees:", SB(62), WHITE, pr(lt, t1, t1 + .4) * fo)
        bits = "010100110101000101001100"
        n = int(max(0, (lt - t1 - .4) / .05)); s = bits[:n]
        for row in range(3):
            ct(d, 1110 + row * 95, " ".join(s[row * 8:row * 8 + 8]), MB(66), YEL, fo)
        caption(d, "How does a letter turn into 0s and 1s? Let me show you.", pr(lt, when(0, "How"), when(0, "How") + .4) * fo)

    elif t < T[2]:
        lt, fo = sc(t, 1); a = pr(lt, 0, .5) * fo
        ct(d, 280, "Inside your computer", SB(68), WHITE, a)
        ct(d, 370, "billions of tiny switches", SB(56), CYAN, a)
        t_on = when(1, "When it's closed")
        on = lt > t_on + .4
        y = 800; L, R = 160, 920
        wc = mix(YEL if on else OFFB, a)
        for seg in [(L, y, 420, y), (640, y, R, y), (L, y, L, 1150), (L, 1150, R, 1150), (R, 1150, R, 1060)]:
            d.line(seg, fill=wc, width=10)
        d.rectangle((L - 45, 930, L + 45, 1050), fill=mix((60, 75, 110), a))
        d.text((L - 20, 950), "+", font=SB(60), fill=mix(WHITE, a))
        d.ellipse((410, y - 15, 440, y + 15), fill=mix(WHITE, a)); d.ellipse((620, y - 15, 650, y + 15), fill=mix(WHITE, a))
        ang = -35 + 35 * pr(lt, t_on, t_on + .4)
        ex = 425 + 210 * math.cos(math.radians(ang)); ey = y + 210 * math.sin(math.radians(ang))
        d.line((425, y, ex, ey), fill=mix(WHITE, a), width=12)
        bulb(d, R, 960, 95, on, a)
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
        ct(d, 1200, "1" if on else "0", MB(150), YEL if on else DIM, pr(lt, when(1, "When a switch"), when(1, "When a switch") + .4) * fo)
        txt = "Switch CLOSED → current flows → we call it 1." if on else "Switch OPEN → no current → we call it 0."
        caption(d, txt, pr(lt, when(1, "When a switch"), when(1, "When a switch") + .4) * fo)

    elif t < T[3]:
        lt, fo = sc(t, 2); a = pr(lt, 0, .5) * fo
        ct(d, 300, "1 switch = 1 bit", SB(72), WHITE, a)
        tb = when(2, "Eight")
        ct(d, 400, "8 switches = 1 BYTE", SB(64), GREEN, pr(lt, tb, tb + .4) * fo)
        pat = format(int(lt * 9) % 256, "08b") if lt > tb else "00000000"
        for j in range(8):
            bulb(d, 130 + j * 117, 760, 46, pat[j] == "1", pr(lt, .3 + j * .08, .7 + j * .08) * fo, pat[j])
        t2 = when(2, "That's")
        ct(d, 950, "2⁸ = 256 combinations", SB(60), YEL, pr(lt, t2, t2 + .4) * fo)
        t3 = when(2, "Enough")
        ct(d, 1050, "Every letter, digit and symbol", SN(46), DIM, pr(lt, t3, t3 + .4) * fo)
        ct(d, 1110, "fits into these 256 slots", SN(46), DIM, pr(lt, t3, t3 + .4) * fo)
        caption(d, "Turning bulbs on and off in different patterns gives us 256 unique codes.", pr(lt, t2, t2 + .4) * fo)

    elif t < T[4]:
        lt, fo = sc(t, 3); a = pr(lt, 0, .5) * fo
        ct(d, 260, "Every letter has a number", SB(60), WHITE, a)
        ct(d, 345, "(ASCII table)", SN(44), DIM, a)
        starts = [when(3, "S is"), when(3, "Q is"), when(3, "L is")]
        idx = 0 if lt < starts[1] else (1 if lt < starts[2] else 2)
        target = "SQL"[idx]
        cols = [("P", 80), ("Q", 81), ("R", 82), ("S", 83), ("K", 75), ("L", 76), ("M", 77)]
        for k, (ch, n) in enumerate(cols):
            x = 75 + k * 135; hl = ch == target and lt > starts[0]
            d.rounded_rectangle((x, 430, x + 120, 590), 18, fill=mix(GREEN if hl else CARD, a))
            w = d.textlength(ch, font=MB(56)); d.text((x + 60 - w / 2, 440), ch, font=MB(56), fill=BG if hl else mix(WHITE, a))
            w = d.textlength(str(n), font=MN(38)); d.text((x + 60 - w / 2, 525), str(n), font=MN(38), fill=BG if hl else mix(CYAN, a))
        ch, num, bits = LET[idx]; st = starts[idx]
        la = pr(lt, st, st + .4) * fo
        ct(d, 680, f"{ch}  →  {num}", MB(120), WHITE, la)
        nb = int(max(0, min(8, (lt - st - .6) / .12 + 1)))
        for j in range(8):
            lit = j < nb and bits[j] == "1"
            bulb(d, 130 + j * 117, 1000, 46, lit, la if j < nb else la * .35, bits[j] if j < nb else "")
        done = "SQL"[:idx + (1 if nb == 8 else 0)]
        ct(d, 1150, done, MB(90), GREEN, fo)
        caption(d, f"'{ch}' = {num} = {bits}. The computer stores these 8 bulbs in memory.", la)

    elif t < T[5]:
        lt, fo = sc(t, 4)
        ct(d, 290, "See it yourself in Oracle:", SB(64), WHITE, pr(lt, 0, .5) * fo)
        a = pr(lt, .3, .8) * fo
        d.rounded_rectangle((60, 420, W - 60, 980), 30, fill=mix((16, 22, 42), a), outline=mix((50, 70, 120), a), width=3)
        for k, c in enumerate([PINK, YEL, GREEN]):
            d.ellipse((100 + k * 50, 455, 130 + k * 50, 485), fill=mix(c, a))
        full = "SELECT DUMP('SQL')\n  FROM dual;"
        n = int(max(0, (lt - .8) / .05)); shown = full[:n]; yy = 540
        for line in shown.split("\n"):
            x = 110
            for word in line.split(" "):
                col = CYAN if word in ("SELECT", "FROM") else (YEL if "DUMP" in word else WHITE)
                d.text((x, yy), word, font=MB(56), fill=mix(col, fo)); x += d.textlength(word + " ", font=MB(56))
            yy += 90
        tr = when(4, "Eighty")
        a3 = pr(lt, tr, tr + .4) * fo
        d.text((110, 770), "Typ=96 Len=3:", font=MN(50), fill=mix(DIM, a3))
        d.text((110, 850), "83,81,76", font=MB(80), fill=mix(GREEN, a3))
        t3 = when(4, "Three")
        ct(d, 1080, "3 letters = 3 bytes = 24 bits", SB(60), YEL, pr(lt, t3, t3 + .4) * fo)
        caption(d, "DUMP shows how a string is really stored in memory: S=83, Q=81, L=76.", pr(lt, tr, tr + .4) * fo)

    else:
        lt = t - T[5]
        ct(d, 480, "Quick question:", SB(80), WHITE, pr(lt, 0, .5))
        tq = when(5, "How")
        ct(d, 640, "'ə'", MB(240), PINK, pr(lt, tq, tq + .5))
        ct(d, 940, "how many bytes does it take?", SB(64), WHITE, pr(lt, tq + .3, tq + .8))
        tn = when(5, "Find")
        ct(d, 1060, "Answer in the next video", SN(50), DIM, pr(lt, tn, tn + .5))
        tf = when(5, "Follow")
        a = pr(lt, tf, tf + .5); p = 1 + .04 * math.sin(lt * 8)
        bw, bh = int(760 * p), int(130 * p)
        d.rounded_rectangle(((W - bw) / 2, 1300, (W + bw) / 2, 1300 + bh), 65, fill=mix(GREEN, a))
        ct(d, 1300 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, a)
    return im

if __name__ == "__main__":
    json.dump({"T": T}, open("/home/claude/en/v1_T.json", "w"))
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        for k in range(6): frame(int((T[k] + (T[k + 1] - T[k]) * .7) * FPS)).save(f"/home/claude/en/p1_{k}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "/home/claude/en/v1en_silent.mp4"], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait(); print("video done", DUR)

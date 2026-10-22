"""Shared helpers for schematic videos 17+."""
from common import *
from make_video5 import arrow
from make_video11 import glow_box, flow
from make_video12 import chip, bar
import math

T10 = [0, 6, 18, 32, 46, 60, 72, 84, 96, 104, 110]

def sc(t, T, k):
    lt = t - T[k]; ln = T[k + 1] - T[k]
    return lt, 1 - pr(lt, ln - .4, ln)

def lerp(a, b, p): return a + (b - a) * p

def base(t, DUR):
    off = int((t * 50) % H)
    im = rain.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 90, 520, 160), 35, fill=CARD)
    d.text((90, 104), "@sql_developer_no1", font=SB(34), fill=GREEN)
    d.rectangle((0, H - 14, int(W * t / DUR), H), fill=GREEN)
    return im, d

def recap(d, lt, fo, items, cap, xex=470):
    a = pr(lt, 0, .3) * fo
    ct(d, 270, "Remember:", SB(66), WHITE, a)
    for k, (q, ex) in enumerate(items):
        y = 380 + k * 125; al = pr(lt, .2 + k * .3, .5 + k * .3) * fo
        d.rounded_rectangle((70, y, W - 70, y + 105), 20, fill=mix(CARD, al))
        d.text((100, y + 32), q, font=MB(32), fill=mix(GREEN, al))
        d.text((xex, y + 32), ex, font=SN(34), fill=mix(WHITE, al))
    caption(d, cap, pr(lt, 2, 2.4) * fo)

def cta(d, lt, title, sub, tfs=64):
    ct(d, 440, "Next video:", SB(60), DIM, pr(lt, 0, .3))
    ct(d, 540, title, SB(tfs), YEL, pr(lt, .2, .5))
    ct(d, 650, sub, SB(44), WHITE, pr(lt, .4, .7))
    ap = pr(lt, .9, 1.3); p = 1 + .04 * math.sin(lt * 8)
    bw, bh = int(760 * p), int(130 * p)
    d.rounded_rectangle(((W - bw) / 2, 860, (W + bw) / 2, 860 + bh), 65, fill=mix(GREEN, ap))
    ct(d, 860 + bh / 2 - 32, "@sql_developer_no1", SB(54), BG, ap)
    ct(d, 1040, "follow · save · share", SN(46), DIM, pr(lt, 1.3, 1.7))

def diamond(d, cx, cy, w, h, l1, l2, col, a):
    d.polygon([(cx, cy - h), (cx + w, cy), (cx, cy + h), (cx - w, cy)], fill=mix(CARD, a), outline=mix(col, a))
    ct(d, cy - 40, l1, SB(30), col, a, cx)
    if l2: ct(d, cy + 2, l2, SN(28), WHITE, a, cx)

def card_list(d, y0, rows, lt, fo, step=72, fs=34):
    """rows: list of (text, color, start_time)"""
    for k, (tx, col, st) in enumerate(rows):
        al = pr(lt, st, st + .4) * fo
        if al <= 0: continue
        y = y0 + k * step
        d.rounded_rectangle((70, y, W - 70, y + step - 12), 14, fill=mix(CARD, al))
        d.text((100, y + 12), tx, font=SN(fs), fill=mix(col, al))

def preview(frame, T, name, extra=()):
    from PIL import Image
    pts = [T[k] + (T[k + 1] - T[k]) * .75 for k in range(len(T) - 1)] + list(extra)
    pts = pts[:12]
    im = Image.new("RGB", (270 * 6, 480 * 2))
    for k, p_ in enumerate(pts):
        im.paste(frame(int(p_ * FPS)).resize((270, 480)), ((k % 6) * 270, (k // 6) * 480))
    im.save(name)

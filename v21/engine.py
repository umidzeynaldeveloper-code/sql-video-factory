"""engine.py — v2.1 engine (PROTOTYPE). Extends v2/studio.py without modifying it.

Same SCENES contract as v2:  (title, colour, fn, [beats...])  — plus an optional 5th item: sound events
    [(beat_index_in_scene, delay_seconds, "sound_name", {params}), ...]
Every v2 primitive (box, table, sql, arrow, ...) works unchanged, because drawing goes through an ImageDraw proxy
that maps 1080-space coordinates through the camera onto a supersampled canvas.

New: supersampled anti-aliasing, layout scaling (1080p / 4K), camera zoom + pan, parallax background, drop shadows,
glow, 2.5D table / cylinder, easing library, zoom transitions, animated SQL execution, data-flow particles, B-tree
traversal, event-based sound design (audio.py), Kokoro with resample_poly + pronunciation dictionary + estimated
word-level subtitles (voice21.py), render config, per-stage timing / RAM log, error handling.
"""
import sys, os, json, math, time, random, subprocess, hashlib, resource, traceback
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/claude/v2"); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont
import studio as S
from studio import *            # noqa: F401,F403  (colours, fonts, all v2 primitives)
from studio import clamp, lerp, mix, pr, tw, BG, CARD, CARD2, INK, WHITE, DIM, GREEN, CYAN, YEL, RED, PURP, ORANGE, OFFB
import audio as A
import voice21 as V

# ------------------------------------------------------------------ configuration
CFG = dict(ss=2, scale=1, fps=30, workers=2, crf=18, preset="medium",
           camera=True, parallax=True, shadows=True, glow=True, bloom=True, transitions="zoom",
           word_subs=True, voice=dict(provider="kokoro", sid=16, speed=0.9),
           auto_sfx=True, music=.13, atmos=.05, sfx=.8, voice_level=.95)
PRESETS = {
    "preview": dict(ss=1, crf=28, preset="ultrafast", shadows=False, glow=False, parallax=False),
    "draft":   dict(ss=1, crf=21, preset="veryfast"),
    "final":   dict(ss=2, crf=18, preset="medium"),
    "final4k": dict(ss=1, scale=2, crf=18, preset="medium"),
}


class RenderError(RuntimeError):
    def __init__(s, stage, msg): super().__init__(f"[{stage}] {msg}"); s.stage = stage


# ------------------------------------------------------------------ easing library
def _c(t): return clamp(t)
EASE = {
    "linear": lambda t: _c(t),
    "out_cubic": lambda t: 1 - (1 - _c(t)) ** 3,
    "in_out_cubic": lambda t: 4 * _c(t) ** 3 if _c(t) < .5 else 1 - (-2 * _c(t) + 2) ** 3 / 2,
    "in_out_sine": lambda t: -(math.cos(math.pi * _c(t)) - 1) / 2,
    "out_expo": lambda t: 1.0 if _c(t) >= 1 else 1 - 2 ** (-10 * _c(t)),
    "out_back": lambda t: 1 + 2.70158 * (_c(t) - 1) ** 3 + 1.70158 * (_c(t) - 1) ** 2,
    "out_elastic": lambda t: (0 if _c(t) == 0 else 1 if _c(t) == 1 else
                              2 ** (-10 * _c(t)) * math.sin((_c(t) * 10 - .75) * (2 * math.pi) / 3) + 1),
    "spring": lambda t: 1 - math.exp(-6 * _c(t)) * math.cos(9 * _c(t)) if _c(t) < 1 else 1.0,
}


def ep(t, a, b, ease="in_out_cubic"):
    """eased progress of t between a and b"""
    return EASE[ease]((t - a) / (b - a)) if b > a else (1.0 if t >= a else 0.0)


# ------------------------------------------------------------------ drawing proxy
_FC = {}


def _font(f, k):
    if k == 1: return f
    size = round(f.size * k * 4) / 4; key = (f.path, size)
    if key not in _FC: _FC[key] = ImageFont.truetype(f.path, size)
    return _FC[key]


class SD:
    """ImageDraw proxy: base coords -> canvas coords (x*k+ox, y*k+oy). Records filled rounded rects for drop shadows."""
    def __init__(s, d, k, ox=0.0, oy=0.0, rec=None): s.d, s.k, s.ox, s.oy, s.rec = d, k, ox, oy, rec

    def P(s, x, y): return (x * s.k + s.ox, y * s.k + s.oy)

    def xy(s, v):
        if isinstance(v[0], (tuple, list)): return [s.P(*p) for p in v]
        o = []
        for i in range(0, len(v), 2): o += s.P(v[i], v[i + 1])
        return o

    def _w(s, w): return max(1, int(round(w * s.k))) if w else w

    @staticmethod
    def _ok(r): return r[2] >= r[0] and r[3] >= r[1]

    def text(s, xy, txt, font=None, fill=None, anchor=None, **kw):
        s.d.text(s.P(*xy), txt, font=_font(font, s.k), fill=fill, anchor=anchor)

    def rounded_rectangle(s, xy, radius=0, fill=None, outline=None, width=1, **kw):
        r = s.xy(xy)
        if not s._ok(r): return
        if fill is not None and s.rec is not None and (xy[2] - xy[0]) * (xy[3] - xy[1]) > 900: s.rec.append((r, radius * s.k))
        s.d.rounded_rectangle(r, radius * s.k, fill=fill, outline=outline, width=s._w(width))

    def rectangle(s, xy, fill=None, outline=None, width=1):
        r = s.xy(xy)
        if s._ok(r): s.d.rectangle(r, fill=fill, outline=outline, width=s._w(width))

    def ellipse(s, xy, fill=None, outline=None, width=1):
        r = s.xy(xy)
        if s._ok(r): s.d.ellipse(r, fill=fill, outline=outline, width=s._w(width))

    def line(s, xy, fill=None, width=0, joint=None):
        s.d.line(s.xy(xy), fill=fill, width=s._w(width) if width else 0, joint=joint)

    def polygon(s, xy, fill=None, outline=None, width=1):
        s.d.polygon(s.xy(xy), fill=fill, outline=outline, width=s._w(width))

    def arc(s, xy, start, end, fill=None, width=1):
        r = s.xy(xy)
        if s._ok(r): s.d.arc(r, start, end, fill=fill, width=s._w(width))

    def pieslice(s, xy, start, end, fill=None, outline=None, width=1):
        r = s.xy(xy)
        if s._ok(r): s.d.pieslice(r, start, end, fill=fill, outline=outline, width=s._w(width))


# ------------------------------------------------------------------ frame context
class G21(S.G):
    """v2 frame context + camera, glow and shadow recording"""
    def __init__(s, st, world, t, bt, fade, tz=1.0):
        super().__init__(st, world, t, bt, fade)
        s.R = st.R; s.cfg = st.cfg; s.shadows = []; s.glows = []; s.tz = tz
        s.cx, s.cy, s.z = st.W / 2, st.H / 2, 1.0
        s.d = SD(ImageDraw.Draw(world), s.R, rec=s.shadows if st.cfg["shadows"] else None)
        s._apply()

    def _apply(s):
        z = s.z * s.tz if s.cfg["camera"] else 1.0; cx, cy = (s.cx, s.cy) if s.cfg["camera"] else (s.W / 2, s.H / 2)
        s.d.k = z * s.R; s.d.ox = (s.W / 2 - cx * z) * s.R; s.d.oy = (s.H / 2 - cy * z) * s.R

    def camera(s, keys, ease="in_out_cubic"):
        """keys: [(beat, delay, dur, cx, cy, zoom), ...] applied in order; call at the START of the scene fn"""
        cam = (s.W / 2, s.H / 2, 1.0)
        for (k, a, d, cx, cy, z) in keys:
            if s.b < k: break
            p = 1.0 if s.b > k else ep(s.bt, a, a + d, ease)
            cam = tuple(lerp(u, v, p) for u, v in zip(cam, (cx, cy, z)))
        s.cx, s.cy, s.z = cam; s._apply()

    def to_canvas(s, r): return (*s.d.P(r[0], r[1]), *s.d.P(r[2], r[3]))

    def glow(s, r, col, a=1.0, rad=24, spread=18):
        """soft coloured light around a rect (base coords); additive, blurred"""
        if a > 0 and s.cfg["glow"]: s.glows.append((s.to_canvas((r[0] - spread, r[1] - spread, r[2] + spread, r[3] + spread)), col, a, rad * s.d.k))

    def focus(s, *rects, a=1.0, pad=16, strength=.62):
        if a <= 0: return
        s._lit += [s.to_canvas((r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad)) for r in rects]
        s._lit_a = max(s._lit_a, a); s._strength = strength


# ------------------------------------------------------------------ new primitives
def table3d(g, x, y, head, rows, cw, rh=64, a=1.0, fs=30, col=CYAN, depth=14, lift=None, hl=(), ra=None, name=None, gap=8,
            hlcol=YEL, dim=(), scan=None):
    """2.5D table: every cell is an extruded slab with a lit top edge. lift(i)->0..1 raises a row towards the viewer.
    scan: float row position of a scanning light bar (None = off). Returns S.Tb (same rect API as v2 table)."""
    tb = S.Tb(x, y, cw, rh, len(rows), gap); d = g.d
    if a <= 0: return tb
    if name: S.tx(g, x + 4, y - 18, name, S.MB(fs - 2), col, a, "ls")

    def slab(r, top, side, edge, al, up=0.0):
        x0, y0, x1, y1 = r[0], r[1] - up, r[2], r[3] - up; dp = depth * (1 + up / 20)
        d.rounded_rectangle((x0 + dp * .35, y0 + dp, x1 + dp * .35, y1 + dp), 10, fill=mix(side, al))       # extrusion
        d.polygon([(x1, y0 + 10), (x1 + dp * .35, y0 + 10 + dp), (x1 + dp * .35, y1 + dp - 6), (x1, y1 - 6)], fill=mix(mix(side, .7, BG), al))
        d.rounded_rectangle((x0, y0, x1, y1), 10, fill=mix(top, al), outline=mix(edge, al), width=2)
        d.line((x0 + 12, y0 + 2, x1 - 12, y0 + 2), fill=mix(mix(WHITE, .35, top), al), width=2)              # lit top edge
        return (x0, y0, x1, y1)

    for c, hname in enumerate(head):
        r = slab(tb.cell(-1, c), CARD2, mix(col, .3, (6, 9, 20)), mix(col, .6, CARD2), a)
        S.tx(g, r[0] + 16, (r[1] + r[3]) / 2, hname, S.fit(hname, S.MB, fs - 2, cw[c] - 24), col, a, "lm")
    for i, row in enumerate(rows):
        al = a * (ra(i) if ra else 1.0)
        if al <= 0: continue
        if i in dim: al *= .3
        up = 12 * (lift(i) if lift else 0.0); h = i in hl or up > 2
        for c, v in enumerate(row):
            r = slab(tb.cell(i, c), mix(hlcol, .2, CARD) if h else CARD, mix(hlcol if h else col, .28, (6, 9, 20)), hlcol if h else mix(col, .35, CARD), al, up)
            S.tx(g, r[0] + 16, (r[1] + r[3]) / 2, str(v), S.fit(str(v), S.MB, fs, cw[c] - 24), hlcol if h else WHITE, al, "lm")
        if h and up > 2: g.glow(tb.row(i), hlcol, al * min(1, up / 12) * .7)
    if scan is not None and 0 <= scan <= len(rows):
        y_ = tb.y + (scan + 1) * rh; bx = tb.box
        d.rounded_rectangle((bx[0] - 14, y_ - 5, bx[2] + 14, y_ + 5), 5, fill=mix(CYAN, a))
        g.glow((bx[0], y_ - 6, bx[2], y_ + 6), CYAN, a, rad=10, spread=22)
    return tb


def cyl25(g, cx, cy, w, h, col, a=1.0, label=None, sub=None, fs=30, fill=0.0):
    """2.5D cylinder with shaded body (lighter on the left) and optional fill level 0..1"""
    if a <= 0: return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    d = g.d; e = w * .17; x0, x1 = cx - w / 2, cx + w / 2; y0, y1 = cy - h / 2, cy + h / 2; n = 40
    for k in range(n):
        u = k / (n - 1); sh = .55 + .45 * math.cos((u - .32) * math.pi)
        xx = x0 + u * w; c = mix(mix(col, .16 + .2 * sh, CARD), a)
        d.line((xx, y0, xx, y1), fill=c, width=w / n + 1.5)
    d.ellipse((x0, y1 - e, x1, y1 + e), fill=mix(mix(col, .25, CARD), a))
    if fill > 0:
        fy = y1 - (h * clamp(fill))
        d.rectangle((x0 + 2, fy, x1 - 2, y1), fill=mix(mix(col, .45, CARD), a))
        d.ellipse((x0 + 2, fy - e, x1 - 2, fy + e), fill=mix(mix(col, .65, CARD), a))
    d.line((x0, y0, x0, y1), fill=mix(col, a), width=3); d.line((x1, y0, x1, y1), fill=mix(col, a), width=3)
    d.arc((x0, y1 - e, x1, y1 + e), 0, 180, fill=mix(col, a), width=3)
    d.ellipse((x0, y0 - e, x1, y0 + e), fill=mix(mix(col, .4, CARD), a), outline=mix(col, a), width=3)
    if label: S.tx(g, cx, cy + (8 if not sub else -10), label, S.fit(label, S.SB, fs, w - 20), WHITE, a, "mm")
    if sub: S.tx(g, cx, cy + fs, sub, S.fit(sub, S.SN, fs - 6, w - 16), mix(col, .9, WHITE), a, "mm")
    return (x0, y0 - e, x1, y1 + e)


def sql_exec(g, x, y, lines, a=1.0, fs=32, typed=1.0, run=None, done=(), w=None, col=GREEN):
    """animated SQL: typing (typed 0..1 of all characters), execution cursor at float line `run`,
    executed lines in `done` get a check. Returns S.Cd."""
    total = sum(len(s) for s in lines); n = int(total * clamp(typed)); shown = []
    for s in lines: shown.append(s[:max(0, min(len(s), n))]); n -= len(s)
    f = S.MB(fs); ww = w or (max(tw(s, f) for s in lines) + 64 + 60)
    cd = S.sql(g, x, y, shown, a=a, fs=fs, w=ww)
    if a <= 0: return cd
    if typed < 1:                                          # blinking caret
        li = next((i for i, s in enumerate(shown) if len(s) < len(lines[i])), len(lines) - 1)
        cxp = x + 30 + tw(shown[li], f); cyp = y + 22 + li * cd.lh
        if (g.t * 2.2) % 1 < .6: g.d.rectangle((cxp + 2, cyp + 2, cxp + 6, cyp + fs + 4), fill=mix(col, a))
    if run is not None and 0 <= run <= len(lines) - .01:
        yy = y + 22 + run * cd.lh - 4; r = (x + 8, yy, x + ww - 8, yy + cd.lh)
        g.d.rounded_rectangle(r, 10, outline=mix(col, a), width=3)
        g.d.polygon([(x - 26, yy + cd.lh / 2 - 13), (x - 6, yy + cd.lh / 2), (x - 26, yy + cd.lh / 2 + 13)], fill=mix(col, a))
        g.glow(r, col, a * .8, rad=12, spread=10)
    for i in done:
        S.check(g, x + ww - 40, y + 22 + i * cd.lh + cd.lh / 2 - 4, True, a, r=17)
    return cd


def flow(g, pts, col, a=1.0, n=5, speed=.55, size=9, trail=6, phase=0.0, line=True):
    """data-flow particles travelling along a polyline (base coords); glowing heads + fading trails"""
    if a <= 0: return
    segs = list(zip(pts[:-1], pts[1:])); lens = [math.dist(p, q) for p, q in segs]; tot = sum(lens)
    if tot <= 0: return
    if line:
        for p, q in segs: g.d.line((*p, *q), fill=mix(mix(col, .35, BG), a), width=4)

    def at(u):
        u = (u % 1) * tot
        for (p, q), ln in zip(segs, lens):
            if u <= ln: return S.mv(p, q, u / ln)
            u -= ln
        return pts[-1]
    for k in range(n):
        u0 = g.t * speed + k / n + phase
        for j in range(trail, -1, -1):
            px, py = at(u0 - j * .012); s_ = size * (1 - j / (trail + 1)); al = a * (1 - j / (trail + 1)) ** 1.5
            g.d.ellipse((px - s_, py - s_, px + s_, py + s_), fill=mix(col if j else WHITE, al))
        px, py = at(u0); g.glow((px - size, py - size, px + size, py + size), col, a * .9, rad=size, spread=14)


def btree(g, cx, y, levels, a=1.0, path=(), rv=0.0, col=PURP, hlcol=GREEN, w=150, h=62, vgap=150, fs=26):
    """B-tree: levels = [[labels], [labels], ...]; path = node index per level; rv 0..1 reveals the traversal.
    Returns list of node rects per level."""
    rects = []
    for li, labels in enumerate(levels):
        n = len(labels); span = min(g.W - 120, n * (w + 28)); x0 = cx - span / 2
        rects.append([(x0 + i * span / n + 14, y + li * vgap, x0 + (i + 1) * span / n - 14, y + li * vgap + h) for i in range(n)])
    if a <= 0: return rects
    steps = max(1, len(levels) - 1); prog = rv * steps
    for li in range(len(levels) - 1):                                  # edges
        for i, r in enumerate(rects[li]):
            kids = rects[li + 1]; per = max(1, len(kids) // len(rects[li]))
            for kk in kids[i * per:(i + 1) * per]:
                p0 = ((r[0] + r[2]) / 2, r[3]); p1 = ((kk[0] + kk[2]) / 2, kk[1])
                on_path = li < len(path) - 1 and path[li] == i and kids.index(kk) == path[li + 1]
                g.d.line((*p0, *p1), fill=mix(mix(col, .4, BG), a), width=3)
                if on_path and prog > li:
                    q = S.mv(p0, p1, clamp(prog - li)); g.d.line((*p0, *q), fill=mix(hlcol, a), width=6)
                    g.glow((min(p0[0], q[0]), min(p0[1], q[1]), max(p0[0], q[0]), max(p0[1], q[1])), hlcol, a * .7, rad=6, spread=8)
    for li, row in enumerate(rects):
        for i, r in enumerate(row):
            vis = li < len(path) and path[li] == i and prog >= li - .05
            S.chip(g, (r[0] + r[2]) / 2, (r[1] + r[3]) / 2, r[2] - r[0], h, str(levels[li][i]), hlcol if vis else col, a, fs,
                   fill=mix(hlcol, .2, CARD) if vis else CARD, tcol=hlcol if vis else WHITE)
            if vis: g.glow(r, hlcol, a * .8)
    return rects


# ------------------------------------------------------------------ stage
class Stage21(S.Stage):
    def __init__(s, W, H, fps=30, handle="@sql_developer_no1", cfg=None):
        s.cfg = dict(CFG); s.cfg.update(cfg or {})
        s.W, s.H, s.fps, s.handle = W, H, fps, handle; s.V = H > W
        s.R = s.cfg["scale"] * s.cfg["ss"]; s.CW, s.CH = int(W * s.R), int(H * s.R)
        s.OW, s.OH = int(W * s.cfg["scale"]), int(H * s.cfg["scale"])
        R = s.R; m = int(120 * R); s.margin = m
        rnd = random.Random(11); s.rain = Image.new("RGB", (s.CW + 2 * m, s.CH * 2), BG); rd = ImageDraw.Draw(s.rain)
        fnt = ImageFont.truetype(S.FDJ + "DejaVuSansMono.ttf", 28 * R)
        for x in range(int(20 * R), s.CW + 2 * m, int(46 * R)):
            for y in range(0, s.CH * 2, int(44 * R)):
                if rnd.random() < .45: rd.text((x, y), rnd.choice("01"), font=fnt, fill=rnd.choice([(13, 21, 40), (16, 26, 48), (12, 19, 36)]))
        yy, xx = np.mgrid[0:s.CH, 0:s.CW].astype("float32")
        cx, cy = s.CW / 2, s.CH * (.43 if s.V else .46); rx, ry = s.CW * (.8 if s.V else .55), s.CH * (.4 if s.V else .62)
        gl = np.clip(1 - ((xx - cx) / rx) ** 2 - ((yy - cy) / ry) ** 2, 0, 1) ** 1.5
        s.light = Image.fromarray(np.stack([gl * 12, gl * 22, gl * 46], -1).astype("uint8"), "RGB")
        vv = np.clip(1 - ((xx - s.CW / 2) / (s.CW * .78)) ** 2 - ((yy - s.CH / 2) / (s.CH * .78)) ** 2, 0, 1)
        s.vig = Image.fromarray((np.stack([.58 + .42 * np.clip(vv * 1.7, 0, 1)] * 3, -1) * 255).astype("uint8"), "RGB")
        del yy, xx, gl, vv
        # mid parallax layer: soft bokeh discs (pre-blurred once)
        q = 4; bk = Image.new("RGB", ((s.CW + 2 * m) // q, (s.CH + 2 * m) // q), (0, 0, 0)); bd = ImageDraw.Draw(bk); rb = random.Random(5)
        for _ in range(26):
            px, py, rr = rb.random() * bk.width, rb.random() * bk.height, (14 + rb.random() * 46) * R / q
            c = rb.choice([(10, 26, 46), (16, 20, 44), (8, 30, 36)]); bd.ellipse((px - rr, py - rr, px + rr, py + rr), fill=c)
        s.bokeh = bk.filter(ImageFilter.GaussianBlur(10 * R / q)).resize((s.CW + 2 * m, s.CH + 2 * m), Image.BILINEAR)
        s.lut_bloom = [max(0, int((v_ - 100) * .6)) for v_ in range(256)] * 3
        s._dark = {}

    def background(s, t, cx=None, cy=None):
        m = s.margin; R = s.R
        dx = dy = 0
        if s.cfg["parallax"] and cx is not None:
            dx = int(clamp(-(cx - s.W / 2) * .12 * R, -m, m)); dy = int(clamp(-(cy - s.H / 2) * .12 * R, -m, m))
        off = int((t * 34 * R) % s.CH)
        bg = s.rain.crop((m - dx, s.CH - off, m - dx + s.CW, 2 * s.CH - off))
        if s.cfg["parallax"]:
            bx = int(clamp(-(cx - s.W / 2) * .3 * R if cx is not None else 0, -m, m)); by = int(clamp(-(cy - s.H / 2) * .3 * R if cy is not None else 0, -m, m))
            by += int(math.sin(t * .4) * 18 * R)
            bg = ImageChops.add(bg, s.bokeh.crop((m - bx, m - by, m - bx + s.CW, m - by + s.CH)))
        return ImageChops.add(bg, s.light)

    def _darken(s, k):
        if k not in s._dark: s._dark[k] = [int(v * (1 - k / 40)) for v in range(256)] * 3
        return s._dark[k]

    def shadows(s, bg, recs, R, strength=.75):
        q = 4; mm = Image.new("L", (s.CW // q, s.CH // q), 0); md = ImageDraw.Draw(mm); off = 10 * R / q
        for r, rad in recs:
            md.rounded_rectangle((r[0] / q + off * .4, r[1] / q + off, r[2] / q + off * .4, r[3] / q + off), rad / q, fill=255)
        mm = mm.filter(ImageFilter.GaussianBlur(7 * R / q)).resize((s.CW, s.CH), Image.BILINEAR)
        return Image.composite(bg.point(s._darken(int(40 * strength))), bg, mm)

    def glowpass(s, im, glows):
        q = 4; gl = Image.new("RGB", (s.CW // q, s.CH // q), (0, 0, 0)); gd = ImageDraw.Draw(gl)
        for r, col, a, rad in glows:      # halo: outer rect minus inner core, so the lit element itself is not washed out
            c = tuple(int(v * .55 * clamp(a)) for v in col); x0, y0, x1, y1 = r[0] / q, r[1] / q, max(r[0], r[2]) / q, max(r[1], r[3]) / q
            gd.rounded_rectangle((x0, y0, x1, y1), rad / q, fill=c)
            e = min((x1 - x0) / 2, (y1 - y0) / 2) * .55
            if e > 2: gd.rounded_rectangle((x0 + e, y0 + e, x1 - e, y1 - e), rad / q, fill=tuple(v // 4 for v in c))
        gl = gl.filter(ImageFilter.GaussianBlur(9 * s.R / q)).resize((s.CW, s.CH), Image.BILINEAR)
        return ImageChops.add(im, gl)

    def spot21(s, im, boxes, a, strength):
        q = 4; mm = Image.new("L", (s.CW // q, s.CH // q), 0); md = ImageDraw.Draw(mm)
        for (x0, y0, x1, y1) in boxes:
            if x1 > x0 and y1 > y0: md.rounded_rectangle((x0 / q, y0 / q, x1 / q, y1 / q), 8 * s.R / q, fill=255)
        mm = mm.filter(ImageFilter.GaussianBlur(5 * s.R)).resize((s.CW, s.CH), Image.BILINEAR)
        k = int(clamp(a) * strength * 40)
        return im if k == 0 else Image.composite(im, im.point(s._darken(k)), mm)

    def post(s, im):
        if not s.cfg["bloom"]: return ImageChops.multiply(im, s.vig)
        q = 6 * s.R; sm = im.reduce(q).point(s.lut_bloom).filter(ImageFilter.GaussianBlur(4))
        return ImageChops.multiply(ImageChops.screen(im, sm.resize((s.CW, s.CH), Image.BILINEAR)), s.vig)

    # UI: title, handle, chapter dots, progress, karaoke subtitles with word timing — drawn on the canvas (anti-aliased)
    def ui21(s, im, tl, bt, t, title, col):
        d = SD(ImageDraw.Draw(im), s.R); W, H = s.W, s.H; ns = tl["ns"]; ci = bt["ci"]
        if title:
            f = S.fit(title, S.XB, 58 if s.V else 54, W - (130 if s.V else 300)); d.text((W / 2, 232 if s.V else 150), title, font=f, fill=col, anchor="mm")
        if s.V:
            d.rounded_rectangle((60, 92, 60 + tw(s.handle, S.SB(32)) + 56, 158), 33, fill=CARD)
            d.text((88, 125), s.handle, font=S.SB(32), fill=GREEN, anchor="lm")
            x = W - 64
            for k in range(ns - 1, -1, -1):
                w_ = 46 if k == ci else 14
                d.rounded_rectangle((x - w_, 118, x, 132), 7, fill=GREEN if k == ci else (mix(GREEN, .45) if k < ci else OFFB)); x -= w_ + 10
        else:
            d.rounded_rectangle((40, 30, 40 + tw(s.handle, S.SB(30)) + 56, 92), 31, fill=CARD)
            d.text((68, 61), s.handle, font=S.SB(30), fill=GREEN, anchor="lm")
        d.rectangle((0, H - (12 if s.V else 8), W * t / tl["dur"], H), fill=GREEN)
        lt = t - bt["t0"]; a = pr(lt, bt["lead"] - .12, bt["lead"] + .15) * (1 - pr(lt, bt["L"] - .22, bt["L"]))
        if a <= 0: return
        f = S.SN(42 if s.V else 36); fb = S.SB(42 if s.V else 36); maxw = W - (200 if s.V else 440); sp = tw(" ", f)
        lines, cur, cw_ = [], [], 0
        for k, (w_, e) in enumerate(bt["toks"]):
            ww = tw(w_, fb if e else f)
            if cur and cw_ + sp + ww > maxw: lines.append((cur, cw_)); cur, cw_ = [], 0
            cw_ += (sp if cur else 0) + ww; cur.append((k, w_, e, ww))
        if cur: lines.append((cur, cw_))
        lh = 58 if s.V else 48; hh = 44 + lh * len(lines); yb = 1668 if s.V else H - 34; y0 = yb - hh
        x0, x1 = (56, W - 56) if s.V else (200, W - 200)
        d.rounded_rectangle((x0, y0, x1, yb), 26, fill=mix((14, 20, 40), a), outline=mix(mix(GREEN, .55), a), width=3)
        vt = lt - bt["lead"]; wt = bt.get("tok_t")
        if wt is None:   # v2 fallback: proportional by characters
            tot = sum(len(w_) + 1 for w_, _ in bt["toks"]); done = clamp(vt / max(.3, bt["vd"] - .25)) * tot
        for li, (ws, lw) in enumerate(lines):
            x = W / 2 - lw / 2; y = y0 + 22 + li * lh
            for (k, w_, e, ww) in ws:
                if wt is not None:
                    st_ = wt[k]; said = vt >= st_; act = said and (k + 1 >= len(wt) or vt < wt[k + 1])
                else:
                    pre = sum(len(bt["toks"][j][0]) + 1 for j in range(k)); said = pre < done; act = False
                c = (YEL if e else WHITE) if said else (mix(YEL, .62, (14, 20, 40)) if e else (150, 162, 200))
                if act: d.rounded_rectangle((x - 6, y - 4, x + ww + 6, y + lh - 10), 10, fill=mix(mix(GREEN, .22, (14, 20, 40)), a))
                d.text((x, y), w_, font=fb if e else f, fill=mix(c, a, (14, 20, 40))); x += ww + sp


# ------------------------------------------------------------------ timeline
ST = None; TL = None; SCN = None
LOG = print


def build21(scenes, out, cfg, gap=.42, gap_end=.85, lead0=.45, lead=.12):
    import soundfile as sf
    os.makedirs(out, exist_ok=True)
    prov = V.get_provider(cfg["voice"], LOG); vkey = prov.key()
    beats = []; t0 = 0.0; k = 0; titles = []; starts = []; events = []
    cache_p = f"{out}/tts.json"; cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    for ci, sc in enumerate(scenes):
        title, col, fn, bs = sc[:4]; ev = sc[4] if len(sc) > 4 else []
        titles.append(title); starts.append(t0); s0 = t0; bstarts = []
        for bi, raw in enumerate(bs):
            toks, spoken_v2 = S.split_beat(raw)
            braces = "{" in raw
            sp_tok = None if braces else V.spoken_tokens(toks)
            spoken = spoken_v2 if braces else " ".join(sp_tok)
            hsh = hashlib.md5(json.dumps([spoken, vkey], sort_keys=True).encode()).hexdigest()[:12]; wav = f"{out}/v_{hsh}.wav"
            if hsh not in cache or not os.path.exists(wav):
                try: dur, sr = prov.synth(spoken, wav)
                except Exception as e: raise RenderError("tts", f"scene {ci} beat {bi}: {e}")
                cache[hsh] = dur; json.dump(cache, open(cache_p, "w"))
            vd = cache[hsh]; ld = lead0 if bi == 0 else lead
            tok_t = None
            if cfg["word_subs"] and sp_tok is not None:
                x, sr = sf.read(wav); words = " ".join(sp_tok).split(); wts = V.word_times(x, sr, words)
                tok_t = []; wi = 0
                for st_ in sp_tok:
                    nw = max(1, len(st_.split())); tok_t.append(wts[min(wi, len(wts) - 1)][0]); wi += nw
            L = ld + vd + (gap_end if bi == len(bs) - 1 else gap)
            beats.append(dict(t0=t0, L=L, ci=ci, bi=bi, nb=len(bs), toks=toks, spoken=spoken, raw=raw, wav=wav, vd=vd, lead=ld,
                              s0=s0, k=k, tok_t=tok_t))
            bstarts.append(t0); t0 += L; k += 1
        for e in ev:
            b, delay, name = e[:3]; p = dict(e[3]) if len(e) > 3 else {}
            events.append(dict(t=bstarts[b] + delay, name=name, **p))
        if cfg["auto_sfx"] and ci > 0: events.append(dict(t=s0 - .18, name="sweep", amp=.32))
    for b in beats: b["sL"] = (starts[b["ci"] + 1] if b["ci"] + 1 < len(starts) else t0) - b["s0"]
    return dict(beats=beats, dur=t0, ns=len(scenes), titles=titles, starts=starts, events=events)


def frame21(t):
    st, tl = ST, TL; bt = S.beat_at(tl, t); sc = SCN[bt["ci"]]; title, col, fn = sc[:3]
    sp = t - bt["s0"]; last = bt["ci"] == tl["ns"] - 1
    fin = pr(sp, 0, .35); fout = 1 - pr(sp, bt["sL"] - .3, bt["sL"]) if not last else 1.0; fade = fin * fout
    tz = 1.0
    if st.cfg["transitions"] == "zoom":
        tz = lerp(.94, 1.0, ep(sp, 0, .5, "out_cubic")) * lerp(1.0, 1.1, ep(sp, bt["sL"] - .45, bt["sL"], "in_out_sine") if not last else 0)
    world = Image.new("RGBA", (st.CW, st.CH), (0, 0, 0, 0))
    g = G21(st, world, t, bt, fade, tz)
    fn(g)
    bg = st.background(t, g.cx, g.cy)
    if g.shadows and st.cfg["shadows"]: bg = st.shadows(bg, g.shadows, g.d.k)
    im = bg.convert("RGBA"); im.alpha_composite(world); im = im.convert("RGB")
    if g.glows: im = st.glowpass(im, g.glows)
    if g._lit and g._lit_a > 0: im = st.spot21(im, g._lit, g._lit_a, g._strength)
    im = st.post(im)
    if fade < 1: im = Image.blend(st.post(st.background(t, g.cx, g.cy)), im, fade)
    st.ui21(im, tl, bt, t, title, col)
    if st.cfg["ss"] > 1: im = im.reduce(st.cfg["ss"])
    return im


def _part21(args):
    i0, i1, path = args; st = ST; t0 = time.time()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{st.OW}x{st.OH}",
                          "-r", str(st.fps), "-i", "-", "-c:v", "libx264", "-preset", st.cfg["preset"], "-crf", str(st.cfg["crf"]),
                          "-pix_fmt", "yuv420p", "-threads", "1", path], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for i in range(i0, i1): p.stdin.write(frame21(i / st.fps).tobytes())
        p.stdin.close(); err = p.stderr.read().decode(); p.wait()
    except Exception:
        p.kill(); return (path, False, traceback.format_exc(), 0, 0)
    if p.returncode != 0: return (path, False, err[-500:], 0, 0)
    return (path, True, "", time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def _ff(args, stage):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], capture_output=True, text=True)
    if r.returncode != 0: raise RenderError(stage, r.stderr[-600:])


def run21(scenes, stage, out, final, mode="preview", seed=0, max_dur=None):
    """mode: preview | frames:<t1,t2> | check | full.  Writes {out}/perf.json with per-stage timings and peak RAM."""
    global ST, TL, SCN
    perf = dict(mode=mode, cfg={k: v for k, v in stage.cfg.items() if k != "voice"}, stages={}); T = time.time()

    def mark(name, t0): perf["stages"][name] = round(time.time() - t0, 2)
    ST, SCN = stage, scenes
    t0 = time.time(); TL = tl = build21(scenes, out, stage.cfg); mark("tts+timeline", t0)
    dur = tl["dur"]; perf["duration_s"] = round(dur, 2)
    LOG(f"duration {dur:.1f}s  beats {len(tl['beats'])}  scenes {tl['ns']}  canvas {stage.CW}x{stage.CH} -> {stage.OW}x{stage.OH}")
    if max_dur and dur > max_dur: LOG(f"!! TOO LONG by {dur - max_dur:.1f}s")
    if mode == "preview":
        t0 = time.time(); tw_, th_ = (405, 720) if stage.V else (640, 360); per = 8 if stage.V else 9; cols = 4 if stage.V else 3
        ims = [frame21(b["t0"] + b["L"] * .86).resize((tw_, th_), Image.LANCZOS) for b in tl["beats"]]
        for pg in range(0, len(ims), per):
            chunk = ims[pg:pg + per]; rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new("RGB", (tw_ * cols, th_ * rows), (0, 0, 0))
            for i, im in enumerate(chunk): sheet.paste(im, ((i % cols) * tw_, (i // cols) * th_))
            sheet.save(f"{out}/sheet{pg // per}.png")
        mark("preview", t0); json.dump(perf, open(f"{out}/perf.json", "w"), indent=1); return tl
    if mode.startswith("frames:"):
        t0 = time.time()
        for k, tt in enumerate(mode[7:].split(",")): frame21(float(tt)).save(f"{out}/f{k}.png")
        mark("frames", t0); perf["frames"] = mode[7:]; json.dump(perf, open(f"{out}/perf.json", "w"), indent=1); return tl
    if mode == "check":
        from voice import asr, sim
        bad = 0
        for b in tl["beats"]:
            h = asr(b["wav"]); disp = " ".join(w for w, _ in b["toks"]); sc_ = max(sim(disp, h), sim(b["spoken"], h))
            if sc_ < .86: bad += 1; LOG(f"  {sc_:.2f} [{b['ci']}.{b['bi']}] {disp}\n        heard: {h}")
        LOG("asr check done, flagged", bad); return tl
    import soundfile as sf, multiprocessing as mp
    # ---- video
    t0 = time.time(); nf = int(dur * stage.fps); P = stage.cfg["workers"]; cut = [nf * i // P for i in range(P + 1)]
    parts = [(cut[i], cut[i + 1], f"{out}/part{i}.mp4") for i in range(P)]
    with mp.get_context("fork").Pool(P) as pool: res = pool.map(_part21, parts)
    bad = [r for r in res if not r[1]]
    if bad: raise RenderError("video", bad[0][2])
    perf["frames"] = nf; perf["workers_peak_rss_mb"] = [round(r[4] / 1024) for r in res]
    open(f"{out}/list.txt", "w").write("".join(f"file '{p[2]}'\n" for p in parts))
    _ff(["-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/silent.mp4"], "concat")
    mark("video", t0); perf["s_per_frame"] = round(perf["stages"]["video"] * P / max(1, nf), 3)
    # ---- audio
    t0 = time.time(); SR = A.SR; n = int(dur * SR) + SR; voice_ = np.zeros(n)
    try:
        for b in tl["beats"]:
            v, sr = sf.read(b["wav"]); v = A.resample(v, sr, SR)
            s0 = int((b["t0"] + b["lead"]) * SR); en = min(n, s0 + len(v)); voice_[s0:en] += v[:en - s0]
        voice_ /= np.max(np.abs(voice_)) + 1e-9; sf.write(f"{out}/voice_raw.wav", voice_, SR)
        _ff(["-i", f"{out}/voice_raw.wav", "-af",
             "highpass=f=75,equalizer=f=190:t=q:w=1:g=1.5,equalizer=f=3400:t=q:w=1.4:g=2.5,"
             "acompressor=threshold=0.14:ratio=2.5:attack=8:release=140:makeup=1.6,alimiter=limit=0.95", f"{out}/voice.wav"], "voice-chain")
        voice_, _ = sf.read(f"{out}/voice.wav"); voice_ = np.pad(voice_, (0, max(0, n - len(voice_))))[:n]
        S.music(dur, f"{out}/music.wav", seed); mus, msr = sf.read(f"{out}/music.wav"); mus = A.resample(mus, msr, SR)
        m_ = np.zeros((n, 2)); L_ = min(n, len(mus)); m_[:L_, 0] = mus[:L_]; m_[:L_, 1] = mus[:L_]
        bed = A.atmos(dur + 1, amp=1.0)[:n]; bed_ = np.zeros((n, 2)); bed_[:len(bed)] = bed
        c = stage.cfg
        music_bus = A.duck(m_ * c["music"] + bed_ * c["atmos"], voice_, depth=.6)
        sfx_ = A.place_events(tl["events"], n) * c["sfx"]
        mix_ = voice_[:, None] / (np.max(np.abs(voice_)) + 1e-9) * c["voice_level"] + music_bus + sfx_
        mix_ /= max(1, np.max(np.abs(mix_)) / .97)
        sf.write(f"{out}/mix.wav", mix_.astype(np.float32), SR)
        perf["loudness_pass1"] = A.master_2pass(f"{out}/mix.wav", f"{out}/master.wav")
    except RenderError: raise
    except Exception as e: raise RenderError("audio", traceback.format_exc()[-800:]) from e
    mark("audio", t0)
    # ---- mux
    t0 = time.time()
    _ff(["-i", f"{out}/silent.mp4", "-i", f"{out}/master.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-shortest", "-movflags", "+faststart", final], "mux")
    mark("mux", t0)
    perf["total_s"] = round(time.time() - T, 2); perf["peak_rss_mb_main"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
    perf["peak_rss_mb_children"] = round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024)
    json.dump(perf, open(f"{out}/perf.json", "w"), indent=1)
    LOG("DONE", final, json.dumps(perf["stages"]))
    return tl

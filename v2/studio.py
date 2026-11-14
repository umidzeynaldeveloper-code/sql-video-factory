"""studio.py — v2 engine for @sql_developer_no1.

Beat-synced narration (one sentence = one visual step), stage lighting (spotlight, bloom, vignette),
beginner-first schematic primitives. Works for 9:16 shorts (1080x1920) and 16:9 long videos (1920x1080).

A video script defines SCENES = [(title, color, fn, [beats...]), ...] and calls run().
A beat is the on-screen sentence. *word* = emphasised; {shown|spoken} = different text for the voice.
fn(g) draws the scene for the current beat: g.b (beat index), g.bt (seconds into beat), g.on(k) (alpha: visible from beat k).
"""
import sys, os, json, math, random, subprocess, re, hashlib
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont

sys.path.insert(0, "/home/claude/v2")
FI = "/usr/share/fonts/opentype/inter/"; FDJ = "/usr/share/fonts/truetype/dejavu/"
_fc = {}


def _f(path, s):
    k = (path, int(s))
    if k not in _fc: _fc[k] = ImageFont.truetype(path, int(s))
    return _fc[k]


XB = lambda s: _f(FI + "Inter-ExtraBold.otf", s)
SB = lambda s: _f(FI + "Inter-Bold.otf", s)
SM = lambda s: _f(FI + "Inter-SemiBold.otf", s)
SN = lambda s: _f(FI + "Inter-Medium.otf", s)
MN = lambda s: _f(FDJ + "DejaVuSansMono.ttf", s)
MB = lambda s: _f(FDJ + "DejaVuSansMono-Bold.ttf", s)

BG = (8, 12, 26); WHITE = (240, 244, 255); DIM = (128, 142, 184); SOFT = (176, 188, 222)
GREEN = (52, 230, 140); CYAN = (70, 200, 255); YEL = (255, 205, 70); PINK = (255, 95, 150); RED = (255, 84, 84)
PURP = (172, 124, 255); ORANGE = (255, 150, 70); CARD = (20, 30, 58); CARD2 = (30, 43, 80); OFFB = (46, 58, 92)
INK = (12, 17, 34)


def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def ease(t): t = clamp(t); return 1 - (1 - t) ** 3
def pr(t, a, b): return ease((t - a) / (b - a)) if b > a else (1.0 if t >= a else 0.0)
def lerp(a, b, p): return a + (b - a) * p
def mv(p0, p1, p): return (lerp(p0[0], p1[0], p), lerp(p0[1], p1[1], p))
def mix(c, a, base=BG):
    a = clamp(a); return tuple(int(base[i] + (c[i] - base[i]) * a) for i in range(3))
def tw(s, f): return f.getlength(s)


# ------------------------------------------------------------------ speech text
SAY = {"SQL": "S Q L", "PL/SQL": "P L S Q L", "ID": "I D", "DDL": "D D L", "DML": "D M L", "PGA": "P G A", "SGA": "S G A",
       "CPU": "C P U", "OK": "okay", "VS": "versus", "DB": "database", "ROWID": "row I D", "VARCHAR2": "var char two"}


def split_beat(s):
    """-> (display tokens [(word, emph)], spoken text)"""
    spoken = re.sub(r"\{([^|}]*)\|([^}]*)\}", lambda m: m.group(2), s).replace("*", "")
    def fix(m):
        w = m.group(0)
        if w in SAY: return SAY[w]
        return w.lower() if len(w) > 1 else w
    spoken = re.sub(r"\b[A-Z][A-Z0-9_/]*[A-Z0-9]\b|\bPL/SQL\b", fix, spoken)
    spoken = spoken.replace("_", " ").replace("→", ", then ").replace("=", " equals ").replace("  ", " ")
    disp = re.sub(r"\{([^|}]*)\|([^}]*)\}", lambda m: m.group(1), s)
    toks = []; emph = False
    for part in re.split(r"(\*)", disp):
        if part == "*": emph = not emph; continue
        for k, w in enumerate(part.split()):
            if toks and re.fullmatch(r"[.,:;!?)]+", w):
                toks[-1] = (toks[-1][0] + w, toks[-1][1]); continue
            if toks and k == 0 and not part[0].isspace() and re.match(r"[.,:;!?)]", w):
                toks[-1] = (toks[-1][0] + w, toks[-1][1]); continue
            toks.append((w, emph))
    return toks, spoken.strip()


# ------------------------------------------------------------------ frame context
class G:
    def __init__(s, st, im, t, bt, fade):
        s.st = st; s.im = im; s.d = ImageDraw.Draw(im); s.t = t; s.W = st.W; s.H = st.H
        s.b = bt["bi"]; s.bt = t - bt["t0"]; s.bl = bt["L"]; s.nb = bt["nb"]; s.p = clamp(s.bt / s.bl)
        s.sp = t - bt["s0"]; s.ci = bt["ci"]; s.last = s.b == s.nb - 1; s.fade = fade
        s._lit = []; s._lit_a = 0.0; s._strength = .62

    def on(s, k, delay=0.0, dur=.45):
        """alpha of an element that appears at beat k and stays"""
        if s.b < k: return 0.0
        if s.b > k: return 1.0
        return pr(s.bt, delay, delay + dur)

    def only(s, k, k2=None, delay=0.0, dur=.4):
        """alpha of an element visible only during beats k..k2"""
        k2 = k if k2 is None else k2
        if s.b < k or s.b > k2: return 0.0
        a = pr(s.bt, delay, delay + dur) if s.b == k else 1.0
        if s.b == k2 and not s.last: a *= 1 - pr(s.bt, s.bl - .3, s.bl)
        return a

    def until(s, k):
        """1 until the end of beat k, then gone"""
        if s.b < k: return 1.0
        if s.b > k: return 0.0
        return 1 - pr(s.bt, s.bl - .3, s.bl)

    def at(s, k, a=0.0, b=1.0):
        """progress 0..1 of a motion that happens during beat k between seconds a..b"""
        if s.b < k: return 0.0
        if s.b > k: return 1.0
        return pr(s.bt, a, b)

    def pulse(s, f=1.4): return .5 + .5 * math.sin(s.t * f * 2 * math.pi)

    def focus(s, *rects, a=1.0, pad=16, strength=.62):
        """spotlight: everything outside these rects is dimmed"""
        if a <= 0: return
        s._lit += [(int(r[0] - pad), int(r[1] - pad), int(r[2] + pad), int(r[3] + pad)) for r in rects]
        s._lit_a = max(s._lit_a, a); s._strength = strength


# ------------------------------------------------------------------ primitives
def tx(g, x, y, s, f, c, a=1.0, anchor="la"):
    if a <= 0: return
    g.d.text((x, y), s, font=f, fill=mix(c, a), anchor=anchor)


def fit(s, fn, size, maxw):
    while size > 16 and fn(size).getlength(s) > maxw: size -= 2
    return fn(size)


def wrap(s, f, maxw):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if f.getlength(t) > maxw and cur: out.append(cur); cur = w
        else: cur = t
    if cur: out.append(cur)
    return out


def para(g, cx, y, s, f, c, a=1.0, maxw=900, lh=None):
    if a <= 0: return y
    lh = lh or int(f.size * 1.3)
    for k, ln in enumerate(wrap(s, f, maxw)): tx(g, cx, y + k * lh, ln, f, c, a, "ma")
    return y + len(wrap(s, f, maxw)) * lh


def box(g, r, col, a=1.0, title=None, sub=None, tfs=36, sfs=28, fill=CARD, rad=22, w=3, glow=True, tcol=None, scol=WHITE):
    if a <= 0: return r
    x0, y0, x1, y1 = r; d = g.d
    if glow:
        for k, f in enumerate((.08, .17)):
            e = 10 - k * 5
            d.rounded_rectangle((x0 - e, y0 - e, x1 + e, y1 + e), rad + e, outline=mix(col, a * f), width=3)
    d.rounded_rectangle(r, rad, fill=mix(fill, a), outline=mix(col, a), width=w)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if title and sub:
        tx(g, cx, cy - sfs * .68, title, fit(title, SB, tfs, x1 - x0 - 24), tcol or col, a, "mm")
        tx(g, cx, cy + tfs * .62, sub, fit(sub, SN, sfs, x1 - x0 - 24), scol, a, "mm")
    elif title:
        tx(g, cx, cy, title, fit(title, SB, tfs, x1 - x0 - 24), tcol or col, a, "mm")
    return r


def ring(g, r, col, a=1.0, pad=8, w=4, rad=18):
    """pulsing outline that marks 'look here'"""
    if a <= 0: return
    p = g.pulse(); x0, y0, x1, y1 = r; e = pad + 5 * p
    g.d.rounded_rectangle((x0 - e - 5, y0 - e - 5, x1 + e + 5, y1 + e + 5), rad + e + 5, outline=mix(col, a * .22), width=w)
    g.d.rounded_rectangle((x0 - e, y0 - e, x1 + e, y1 + e), rad + e, outline=mix(col, a * (.7 + .3 * p)), width=w)


def pill(g, cx, cy, s, col, a=1.0, fs=30, fill=False, padx=22, h=None, font=None):
    if a <= 0: return (cx, cy, cx, cy)
    f = (font or SB)(fs); w = tw(s, f) + 2 * padx; h = h or int(fs * 1.75)
    r = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    g.d.rounded_rectangle(r, h / 2, fill=mix(col if fill else CARD, a), outline=mix(col, a), width=3)
    tx(g, cx, cy, s, f, INK if fill else col, a, "mm")
    return r


def chip(g, cx, cy, w, h, s, col, a=1.0, fs=28, fill=CARD, tcol=WHITE, mono=True, rad=12, bw=3):
    if a <= 0: return (cx, cy, cx, cy)
    r = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    g.d.rounded_rectangle(r, rad, fill=mix(fill, a), outline=mix(col, a), width=bw)
    if s: tx(g, cx, cy, s, fit(s, MB if mono else SB, fs, w - 14), tcol, a, "mm")
    return r


def badge(g, cx, cy, n, col, a=1.0, r=28):
    if a <= 0: return
    g.d.ellipse((cx - r - 5, cy - r - 5, cx + r + 5, cy + r + 5), outline=mix(col, a * .3), width=3)
    g.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=mix(col, a))
    tx(g, cx, cy, str(n), SB(int(r * 1.15)), INK, a, "mm")


def arrow(g, p0, p1, col, a=1.0, rv=1.0, w=6, head=22, dot=False):
    if a <= 0 or rv <= 0: return
    q = mv(p0, p1, clamp(rv)); d = g.d
    d.line((*p0, *q), fill=mix(col, a), width=w)
    if rv >= .98:
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        d.polygon([p1, (p1[0] - head * math.cos(ang - .42), p1[1] - head * math.sin(ang - .42)),
                   (p1[0] - head * math.cos(ang + .42), p1[1] - head * math.sin(ang + .42))], fill=mix(col, a))
        if dot:
            ph = (g.t * .7) % 1; x, y = mv(p0, p1, ph)
            d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=mix(WHITE, a))


def path(g, pts, col, a=1.0, rv=1.0, w=6, head=22, dot=False):
    """polyline arrow with progressive reveal"""
    if a <= 0 or rv <= 0: return
    segs = list(zip(pts[:-1], pts[1:])); lens = [math.dist(p, q) for p, q in segs]; tot = sum(lens); done = tot * clamp(rv); s = 0
    for k, ((p, q), ln) in enumerate(zip(segs, lens)):
        if s >= done: break
        f = min(1, (done - s) / ln)
        if k == len(segs) - 1: arrow(g, p, q, col, a, f, w, head, dot)
        else:
            e = mv(p, q, f); g.d.line((*p, *e), fill=mix(col, a), width=w)
            g.d.ellipse((e[0] - w / 2, e[1] - w / 2, e[0] + w / 2, e[1] + w / 2), fill=mix(col, a))
        s += ln


def _edge(r, p):
    """point on rect border in the direction of p from the rect centre"""
    cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2; dx, dy = p[0] - cx, p[1] - cy
    if dx == 0 and dy == 0: return (cx, cy)
    hw, hh = (r[2] - r[0]) / 2, (r[3] - r[1]) / 2
    k = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
    return (cx + dx * k, cy + dy * k)


def callout(g, target, s, col, a=1.0, at=None, fs=30, mark=True, sub=None):
    """name a detail: outline on the target rect, leader line, label pill centred at `at`"""
    if a <= 0: return (0, 0, 0, 0)
    f = SB(fs); w = tw(s, f) + 44; h = int(fs * 1.8)
    if sub: w = max(w, tw(sub, SN(fs - 4)) + 44); h += int(fs * 1.15)
    cx, cy = at; lr = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    if mark: g.d.rounded_rectangle((target[0] - 6, target[1] - 6, target[2] + 6, target[3] + 6), 14, outline=mix(col, a), width=4)
    tc = ((target[0] + target[2]) / 2, (target[1] + target[3]) / 2)
    p0 = _edge(lr, tc); p1 = _edge((target[0] - 6, target[1] - 6, target[2] + 6, target[3] + 6), (cx, cy))
    g.d.line((*p0, *p1), fill=mix(col, a), width=4)
    g.d.ellipse((p1[0] - 9, p1[1] - 9, p1[0] + 9, p1[1] + 9), fill=mix(col, a))
    g.d.rounded_rectangle(lr, 18, fill=mix(INK, a), outline=mix(col, a), width=3)
    if sub:
        tx(g, cx, cy - fs * .55, s, f, col, a, "mm"); tx(g, cx, cy + fs * .62, sub, SN(fs - 4), WHITE, a, "mm")
    else: tx(g, cx, cy, s, f, col, a, "mm")
    return lr


class Tb:
    def __init__(s, x, y, cw, rh, n, gap): s.x, s.y, s.cw, s.rh, s.n, s.gap = x, y, cw, rh, n, gap
    def cell(s, r, c):
        x = s.x + sum(s.cw[:c]); y = s.y + (r + 1) * s.rh
        return (x, y, x + s.cw[c] - s.gap, y + s.rh - s.gap)
    def row(s, r, c0=0, c1=None):
        c1 = len(s.cw) - 1 if c1 is None else c1; a = s.cell(r, c0); b = s.cell(r, c1); return (a[0], a[1], b[2], b[3])
    def col(s, c, r0=-1, r1=None):
        r1 = s.n - 1 if r1 is None else r1; a = s.cell(r0, c); b = s.cell(r1, c); return (a[0], a[1], b[2], b[3])
    def rows(s, r0, r1): a = s.row(r0); b = s.row(r1); return (a[0], a[1], b[2], b[3])
    @property
    def box(s): return s.rows(-1, s.n - 1)
    @property
    def bottom(s): return s.y + (s.n + 1) * s.rh


def table(g, x, y, head, rows, cw, rh=62, a=1.0, fs=30, col=CYAN, hl=(), dim=(), strike=(), ra=None, ccol=None,
          hlcol=YEL, hlc=(), name=None, gap=6, mono=True):
    """data table. ra(i) -> alpha of row i; hl: highlighted rows; dim: faded rows; strike: crossed-out rows;
    hlc: highlighted columns; ccol(r, c) -> text colour override. returns Tb with cell/row/col rects."""
    tb = Tb(x, y, cw, rh, len(rows), gap); d = g.d
    if a <= 0: return tb
    if name:
        tx(g, x + 4, y - 14, name, MB(fs - 2), col, a, "ls")
    for c, hname in enumerate(head):
        r = tb.cell(-1, c)
        d.rounded_rectangle(r, 10, fill=mix(CARD2 if c not in hlc else mix(hlcol, .35, CARD2), a))
        tx(g, r[0] + 16, (r[1] + r[3]) / 2, hname, fit(hname, MB, fs - 2, cw[c] - 24), hlcol if c in hlc else col, a, "lm")
    for i, row in enumerate(rows):
        al = a * (ra(i) if ra else 1.0)
        if al <= 0: continue
        if i in dim: al *= .26
        for c, v in enumerate(row):
            r = tb.cell(i, c); h = i in hl
            d.rounded_rectangle(r, 10, fill=mix(mix(hlcol, .16, CARD) if h else CARD, al), outline=mix(hlcol, al) if h else None, width=2)
            tc = (ccol(i, c) if ccol else None) or (hlcol if c in hlc else WHITE)
            tx(g, r[0] + 16, (r[1] + r[3]) / 2, str(v), fit(str(v), MB if mono else SN, fs, cw[c] - 24), tc, al, "lm")
        if i in strike:
            r = tb.row(i); d.line((r[0] + 8, (r[1] + r[3]) / 2, r[2] - 8, (r[1] + r[3]) / 2), fill=mix(RED, al if i not in dim else a), width=4)
    return tb


KW = set("SELECT FROM WHERE GROUP BY HAVING ORDER AS AND OR NOT IN IS NULL ON JOIN LEFT INNER INSERT INTO VALUES UPDATE SET DELETE "
         "TRUNCATE DROP TABLE CREATE COMMIT ROLLBACK DISTINCT DESC ASC FETCH FIRST ROWS ONLY EXISTS BETWEEN LIKE UNION ALL "
         "OPEN CLOSE CURSOR LOOP END FOR BEGIN DECLARE EXIT WHEN THEN IF ELSE FLASHBACK TO BEFORE PURGE ALTER INDEX".split())
FN = set("COUNT SUM AVG MIN MAX NVL ROUND UPPER LOWER TRUNC TO_CHAR TO_DATE".split())


class Cd:
    def __init__(s, x, y, w, lh, n, pad): s.x, s.y, s.w, s.lh, s.n, s.pad = x, y, w, lh, n, pad
    def line(s, i, i2=None):
        i2 = i if i2 is None else i2
        return (s.x + 8, s.y + s.pad + i * s.lh - 4, s.x + s.w - 8, s.y + s.pad + (i2 + 1) * s.lh - 2)
    @property
    def box(s): return (s.x, s.y, s.x + s.w, s.y + 2 * s.pad + s.n * s.lh)
    @property
    def bottom(s): return s.y + 2 * s.pad + s.n * s.lh


def sql(g, x, y, lines, a=1.0, fs=32, w=None, hl=(), dim=(), la=None, hlcol=YEL, num=None):
    """code block with syntax colours. hl: lit lines; dim: faded lines; la(i) -> alpha per line; num: {line: badge number}"""
    f = MB(fs); lh = int(fs * 1.5); pad = 22
    ww = w or (max(tw(s, f) for s in lines) + 64 + (50 if num else 0))
    cd = Cd(x, y, ww, lh, len(lines), pad)
    if a <= 0: return cd
    d = g.d; d.rounded_rectangle(cd.box, 18, fill=mix((13, 19, 38), a), outline=mix(OFFB, a), width=2)
    xo = x + 30 + (50 if num else 0)
    for i, s in enumerate(lines):
        al = a * (la(i) if la else 1.0)
        if al <= 0: continue
        if i in dim: al *= .3
        yy = y + pad + i * lh
        if i in hl:
            r = cd.line(i); d.rounded_rectangle(r, 10, fill=mix(mix(hlcol, .2, CARD), al), outline=mix(hlcol, al), width=2)
        if num and i in num: badge(g, x + 40, yy + lh / 2 - 3, num[i], hlcol if i in hl else DIM, al, r=int(fs * .6))
        code, _, com = s.partition("--")
        xx = xo
        for tok in re.findall(r"'[^']*'|[A-Za-z_][A-Za-z0-9_$#.]*|\d+(?:\.\d+)?|\s+|.", code):
            if tok.isspace(): xx += tw(tok, f); continue
            up = tok.upper()
            c = YEL if tok[0] == "'" else CYAN if up in KW and tok == up else GREEN if up in FN and tok == up else PURP if tok[0].isdigit() else WHITE
            d.text((xx, yy), tok, font=f, fill=mix(c, al)); xx += tw(tok, f)
        if com: d.text((xx, yy), "--" + com, font=MN(fs), fill=mix(DIM, al))
    return cd


def check(g, cx, cy, ok, a=1.0, r=26):
    if a <= 0: return
    col = GREEN if ok else RED; d = g.d
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=mix(mix(col, .2, CARD), a), outline=mix(col, a), width=4)
    if ok: d.line((cx - r * .45, cy, cx - r * .1, cy + r * .38, cx + r * .5, cy - r * .35), fill=mix(col, a), width=6, joint="curve")
    else:
        d.line((cx - r * .4, cy - r * .4, cx + r * .4, cy + r * .4), fill=mix(col, a), width=6)
        d.line((cx - r * .4, cy + r * .4, cx + r * .4, cy - r * .4), fill=mix(col, a), width=6)


def hbar(g, x, y, w, h, p, col, a=1.0, label=None, val=None, fs=30):
    if a <= 0: return
    g.d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=mix(OFFB, a))
    if p > 0: g.d.rounded_rectangle((x, y, x + max(h, w * clamp(p)), y + h), h // 2, fill=mix(col, a))
    if label: tx(g, x, y - 12, label, SB(fs), WHITE, a, "ls")
    if val: tx(g, x + w, y - 12, val, MB(fs), col, a, "rs")


def person(g, cx, cy, s, col, a=1.0, label=None, fs=28):
    if a <= 0: return
    d = g.d
    d.ellipse((cx - s * .24, cy - s * .62, cx + s * .24, cy - s * .14), fill=mix(col, a))
    d.pieslice((cx - s * .46, cy - s * .06, cx + s * .46, cy + s * .9), 180, 360, fill=mix(col, a))
    if label: tx(g, cx, cy + s * .52, label, SB(fs), WHITE, a, "ma")


def cyl(g, cx, cy, w, h, col, a=1.0, label=None, sub=None, fs=30):
    if a <= 0: return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    d = g.d; e = w * .16; x0, x1 = cx - w / 2, cx + w / 2; y0, y1 = cy - h / 2, cy + h / 2
    d.ellipse((x0, y1 - e, x1, y1 + e), fill=mix(CARD, a), outline=mix(col, a), width=4)
    d.rectangle((x0, y0, x1, y1), fill=mix(CARD, a))
    d.line((x0, y0, x0, y1), fill=mix(col, a), width=4); d.line((x1, y0, x1, y1), fill=mix(col, a), width=4)
    for k in (1, 2): d.arc((x0, y0 + (h * k / 3) - e, x1, y0 + (h * k / 3) + e), 0, 180, fill=mix(col, a * .45), width=3)
    d.ellipse((x0, y0 - e, x1, y0 + e), fill=mix(mix(col, .25, CARD), a), outline=mix(col, a), width=4)
    if label: tx(g, cx, cy + (8 if not sub else -8), label, fit(label, SB, fs, w - 20), col, a, "mm")
    if sub: tx(g, cx, cy + fs, sub, fit(sub, SN, fs - 6, w - 16), WHITE, a, "mm")
    return (x0, y0 - e, x1, y1 + e)


def icon(g, name, cx, cy, s, col, a=1.0):
    """tiny pictograms drawn with shapes; s = size (px)"""
    if a <= 0: return
    d = g.d; c = mix(col, a); h = s / 2; w = max(3, int(s * .08))
    if name == "doc":
        d.rounded_rectangle((cx - h * .7, cy - h, cx + h * .7, cy + h), s * .1, fill=mix(CARD2, a), outline=c, width=w)
        for k in range(3): d.line((cx - h * .4, cy - h * .45 + k * h * .42, cx + h * .4, cy - h * .45 + k * h * .42), fill=c, width=w)
    elif name == "trash":
        d.rounded_rectangle((cx - h * .6, cy - h * .5, cx + h * .6, cy + h), s * .08, fill=mix(CARD2, a), outline=c, width=w)
        d.line((cx - h * .85, cy - h * .5, cx + h * .85, cy - h * .5), fill=c, width=w); d.rectangle((cx - h * .25, cy - h * .8, cx + h * .25, cy - h * .5), outline=c, width=w)
        for k in (-1, 0, 1): d.line((cx + k * h * .3, cy - h * .2, cx + k * h * .3, cy + h * .7), fill=c, width=w)
    elif name == "lock":
        d.arc((cx - h * .45, cy - h, cx + h * .45, cy + h * .1), 180, 360, fill=c, width=w + 2)
        d.rounded_rectangle((cx - h * .7, cy - h * .3, cx + h * .7, cy + h * .8), s * .1, fill=c)
    elif name == "search":
        d.ellipse((cx - h * .8, cy - h * .8, cx + h * .3, cy + h * .3), outline=c, width=w + 2)
        d.line((cx + h * .2, cy + h * .2, cx + h * .85, cy + h * .85), fill=c, width=w + 4)
    elif name == "clock":
        d.ellipse((cx - h, cy - h, cx + h, cy + h), fill=mix(CARD2, a), outline=c, width=w)
        d.line((cx, cy, cx, cy - h * .6), fill=c, width=w); d.line((cx, cy, cx + h * .45, cy + h * .15), fill=c, width=w)
    elif name == "funnel":
        d.polygon([(cx - h, cy - h * .8), (cx + h, cy - h * .8), (cx + h * .22, cy + h * .1), (cx + h * .22, cy + h * .9), (cx - h * .22, cy + h * .6), (cx - h * .22, cy + h * .1)], fill=mix(mix(col, .25, CARD), a), outline=c)
        d.line((cx - h, cy - h * .8, cx + h, cy - h * .8), fill=c, width=w + 2)
    elif name == "warn":
        d.polygon([(cx, cy - h), (cx + h, cy + h * .8), (cx - h, cy + h * .8)], fill=mix(mix(col, .22, CARD), a), outline=c)
        d.line((cx, cy - h * .35, cx, cy + h * .25), fill=c, width=w + 2); d.ellipse((cx - w, cy + h * .42, cx + w, cy + h * .42 + 2 * w), fill=c)
    elif name == "bulb":
        d.ellipse((cx - h * .6, cy - h, cx + h * .6, cy + h * .2), fill=mix(mix(col, .3, CARD), a), outline=c, width=w)
        d.rounded_rectangle((cx - h * .3, cy + h * .25, cx + h * .3, cy + h * .75), s * .06, fill=c)
    elif name == "bookmark":
        d.polygon([(cx - h * .5, cy - h), (cx + h * .5, cy - h), (cx + h * .5, cy + h), (cx, cy + h * .5), (cx - h * .5, cy + h)], fill=c)
    elif name == "eraser":
        d.polygon([(cx - h, cy + h * .2), (cx - h * .2, cy - h * .6), (cx + h, cy - h * .1), (cx + h * .2, cy + h * .7)], fill=mix(mix(col, .3, CARD), a), outline=c)
        d.line((cx - h * .5, cy - h * .15, cx + h * .7, cy + h * .35), fill=c, width=w)
    elif name == "scissors":
        d.line((cx - h * .7, cy - h * .7, cx + h * .7, cy + h * .5), fill=c, width=w + 2); d.line((cx - h * .7, cy + h * .7, cx + h * .7, cy - h * .5), fill=c, width=w + 2)
        d.ellipse((cx - h, cy - h, cx - h * .4, cy - h * .4), outline=c, width=w); d.ellipse((cx - h, cy + h * .4, cx - h * .4, cy + h), outline=c, width=w)
    elif name == "book":
        d.rounded_rectangle((cx - h * .8, cy - h, cx + h * .8, cy + h), s * .08, fill=mix(mix(col, .25, CARD), a), outline=c, width=w)
        d.line((cx - h * .45, cy - h, cx - h * .45, cy + h), fill=c, width=w)
    elif name == "hand":
        d.polygon([(cx - h, cy - h * .25), (cx + h * .3, cy - h * .25), (cx + h * .3, cy - h * .6), (cx + h, cy), (cx + h * .3, cy + h * .6), (cx + h * .3, cy + h * .25), (cx - h, cy + h * .25)], fill=c)
    elif name == "star":
        pts = []
        for k in range(10):
            rr = h if k % 2 == 0 else h * .45; an = -math.pi / 2 + k * math.pi / 5
            pts.append((cx + rr * math.cos(an), cy + rr * math.sin(an)))
        d.polygon(pts, fill=c)


def term(g, word, meaning, a=1.0, y=None, col=YEL):
    """dictionary card: a new word and its plain-language meaning"""
    if a <= 0: return
    W = g.W; y = y if y is not None else (1215 if g.st.V else 760)
    x0, x1 = (70, W - 70) if g.st.V else (360, W - 360)
    r = (x0, y, x1, y + 150); d = g.d
    d.rounded_rectangle(r, 24, fill=mix(INK, a), outline=mix(col, a), width=3)
    icon(g, "book", x0 + 70, y + 75, 70, col, a)
    tx(g, x0 + 130, y + 26, "NEW WORD", SB(22), DIM, a)
    tx(g, x0 + 130 + tw("NEW WORD", SB(22)) + 18, y + 14, word, fit(word, MB, 38, 520), col, a)
    tx(g, x0 + 130, y + 84, meaning, fit(meaning, SN, 34, x1 - x0 - 160), WHITE, a)
    return r


def vs_panel(g, y, left, right, a_l=1.0, a_r=1.0, h=92, lcol=ORANGE, rcol=CYAN, fs=30, lt="REAL LIFE", rt="DATABASE"):
    """two-column mapping: everyday thing  ->  database word. left/right: lists of strings; a_l/a_r may be callables(i)"""
    W = g.W; x0, xm, x1 = 70, W / 2, W - 70
    al0 = a_l(0) if callable(a_l) else a_l
    tx(g, (x0 + xm - 30) / 2, y, lt, SB(26), lcol, al0, "ma"); tx(g, (xm + 30 + x1) / 2, y, rt, SB(26), rcol, a_r(0) if callable(a_r) else a_r, "ma")
    for i, (l, r_) in enumerate(zip(left, right)):
        yy = y + 48 + i * (h + 16); al = a_l(i) if callable(a_l) else a_l; ar = a_r(i) if callable(a_r) else a_r
        chip(g, (x0 + xm - 30) / 2, yy + h / 2, xm - 30 - x0, h, l, lcol, al, fs, mono=False, rad=18)
        chip(g, (xm + 30 + x1) / 2, yy + h / 2, x1 - xm - 30, h, r_, rcol, ar, fs, mono=False, rad=18, tcol=rcol)
        arrow(g, (xm - 24, yy + h / 2), (xm + 24, yy + h / 2), WHITE, ar, 1, 5, 14)


# ------------------------------------------------------------------ stage (lighting + UI)
class Stage:
    def __init__(s, W, H, fps=30, handle="@sql_developer_no1"):
        import numpy as np
        s.W, s.H, s.fps, s.handle = W, H, fps, handle; s.V = H > W
        rnd = random.Random(11)
        s.rain = Image.new("RGB", (W, H * 2), BG); rd = ImageDraw.Draw(s.rain)
        for x in range(20, W, 46):
            for y in range(0, H * 2, 44):
                if rnd.random() < .45:
                    rd.text((x, y), rnd.choice("01"), font=MN(28), fill=rnd.choice([(13, 21, 40), (16, 26, 48), (12, 19, 36)]))
        yy, xx = np.mgrid[0:H, 0:W].astype("float32")
        cx, cy = W / 2, H * (.43 if s.V else .46); rx, ry = W * (.8 if s.V else .55), H * (.4 if s.V else .62)
        gl = np.clip(1 - ((xx - cx) / rx) ** 2 - ((yy - cy) / ry) ** 2, 0, 1) ** 1.5
        s.light = Image.fromarray(np.stack([gl * 12, gl * 22, gl * 46], -1).astype("uint8"), "RGB")
        vv = np.clip(1 - ((xx - W / 2) / (W * .78)) ** 2 - ((yy - H / 2) / (H * .78)) ** 2, 0, 1)
        v = .58 + .42 * np.clip(vv * 1.7, 0, 1)
        s.vig = Image.fromarray((np.stack([v] * 3, -1) * 255).astype("uint8"), "RGB")
        s.lut_bloom = [max(0, int((v_ - 100) * .6)) for v_ in range(256)] * 3
        s._mask = {}; s._dark = {}

    def background(s, t):
        off = int((t * 34) % s.H)
        return ImageChops.add(s.rain.crop((0, s.H - off, s.W, 2 * s.H - off)), s.light)

    def spot(s, im, boxes, a, strength):
        key = tuple(sorted(set(boxes))); m = s._mask.get(key)
        if m is None:
            q = 4; mm = Image.new("L", (s.W // q, s.H // q), 0); md = ImageDraw.Draw(mm)
            for (x0, y0, x1, y1) in key: md.rounded_rectangle((x0 / q, y0 / q, x1 / q, y1 / q), 8, fill=255)
            m = mm.filter(ImageFilter.GaussianBlur(5)).resize((s.W, s.H), Image.BILINEAR)
            if len(s._mask) > 48: s._mask.clear()
            s._mask[key] = m
        k = int(clamp(a) * strength * 40)
        if k == 0: return im
        if k not in s._dark: s._dark[k] = [int(v * (1 - k / 40)) for v in range(256)] * 3
        return Image.composite(im, im.point(s._dark[k]), m)

    def post(s, im):
        q = 6
        sm = im.reduce(q).point(s.lut_bloom).filter(ImageFilter.GaussianBlur(4))
        im = ImageChops.screen(im, sm.resize((s.W, s.H), Image.BILINEAR))
        return ImageChops.multiply(im, s.vig)

    # ---- UI drawn after lighting so it stays crisp
    def ui(s, im, tl, bt, t):
        d = ImageDraw.Draw(im); W, H = s.W, s.H; ns = tl["ns"]; ci = bt["ci"]
        if s.V:
            d.rounded_rectangle((60, 92, 60 + tw(s.handle, SB(32)) + 56, 158), 33, fill=CARD)
            d.text((88, 125), s.handle, font=SB(32), fill=GREEN, anchor="lm")
            x = W - 64
            for k in range(ns - 1, -1, -1):
                w_ = 46 if k == ci else 14
                d.rounded_rectangle((x - w_, 118, x, 132), 7, fill=GREEN if k == ci else (mix(GREEN, .45) if k < ci else OFFB)); x -= w_ + 10
        else:
            d.rounded_rectangle((40, 30, 40 + tw(s.handle, SB(30)) + 56, 92), 31, fill=CARD)
            d.text((68, 61), s.handle, font=SB(30), fill=GREEN, anchor="lm")
            ttl = f"{ci + 1} / {ns}"; w_ = tw(ttl, SB(30))
            d.rounded_rectangle((W - 96 - w_, 30, W - 40, 92), 31, fill=CARD)
            d.text((W - 68 - w_, 61), ttl, font=SB(30), fill=YEL, anchor="lm")
            x = W / 2 + (ns * 24) / 2
            for k in range(ns - 1, -1, -1):
                w_ = 40 if k == ci else 12
                d.rounded_rectangle((x - w_, 54, x, 66), 6, fill=GREEN if k == ci else (mix(GREEN, .45) if k < ci else OFFB)); x -= w_ + 8
        d.rectangle((0, H - (12 if s.V else 8), int(W * t / tl["dur"]), H), fill=GREEN)
        # subtitle with progressive highlight
        lt = t - bt["t0"]; a = pr(lt, bt["lead"] - .12, bt["lead"] + .15) * (1 - pr(lt, bt["L"] - .22, bt["L"]))
        if a <= 0: return
        f = SN(42 if s.V else 36); fb = SB(42 if s.V else 36); maxw = W - (200 if s.V else 440); sp = tw(" ", f)
        lines, cur, cw_ = [], [], 0
        for k, (w_, e) in enumerate(bt["toks"]):
            ww = tw(w_, fb if e else f)
            if cur and cw_ + sp + ww > maxw: lines.append((cur, cw_)); cur, cw_ = [], 0
            cw_ += (sp if cur else 0) + ww; cur.append((k, w_, e, ww))
        if cur: lines.append((cur, cw_))
        lh = 58 if s.V else 48; hh = 44 + lh * len(lines); yb = 1668 if s.V else H - 34; y0 = yb - hh
        x0, x1 = (56, W - 56) if s.V else (200, W - 200)
        d.rounded_rectangle((x0, y0, x1, yb), 26, fill=mix((14, 20, 40), a), outline=mix(mix(GREEN, .55), a), width=3)
        tot = sum(len(w_) + 1 for w_, _ in bt["toks"]); frac = clamp((lt - bt["lead"]) / max(.3, bt["vd"] - .25)); done = frac * tot; acc = 0
        for li, (ws, lw) in enumerate(lines):
            x = W / 2 - lw / 2; y = y0 + 22 + li * lh
            for (k, w_, e, ww) in ws:
                said = acc < done; acc += len(w_) + 1
                c = (YEL if e else WHITE) if said else (mix(YEL, .62, (14, 20, 40)) if e else (150, 162, 200))
                d.text((x, y), w_, font=fb if e else f, fill=mix(c, a, (14, 20, 40))); x += ww + sp


# ------------------------------------------------------------------ timeline, render, audio
ST = None; TL = None; SCN = None
VOICE = dict(sid=16, speed=0.9, model="k10")


def build(scenes, out, gap=.42, gap_end=.85, lead0=.45, lead=.12):
    from voice import say
    os.makedirs(out, exist_ok=True)
    beats = []; t0 = 0.0; k = 0; titles = []; starts = []
    cache_p = f"{out}/tts.json"; cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    for ci, (title, col, fn, bs) in enumerate(scenes):
        titles.append(title); starts.append(t0); s0 = t0
        for bi, raw in enumerate(bs):
            toks, spoken = split_beat(raw)
            hsh = hashlib.md5(json.dumps([spoken, VOICE], sort_keys=True).encode()).hexdigest()[:12]; wav = f"{out}/v_{hsh}.wav"
            if hsh not in cache or not os.path.exists(wav):
                cache[hsh] = say(spoken, wav, **VOICE); json.dump(cache, open(cache_p, "w"))
            vd = cache[hsh]; ld = lead0 if bi == 0 else lead
            L = ld + vd + (gap_end if bi == len(bs) - 1 else gap)
            beats.append(dict(t0=t0, L=L, ci=ci, bi=bi, nb=len(bs), toks=toks, spoken=spoken, raw=raw, wav=wav, vd=vd, lead=ld, s0=s0, k=k))
            t0 += L; k += 1
    for b in beats: b["sL"] = (starts[b["ci"] + 1] if b["ci"] + 1 < len(starts) else t0) - b["s0"]
    return dict(beats=beats, dur=t0, ns=len(scenes), titles=titles, starts=starts)


def beat_at(tl, t):
    bs = tl["beats"]; lo, hi = 0, len(bs) - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if bs[m]["t0"] <= t: lo = m
        else: hi = m - 1
    return bs[lo]


def frame(t):
    st, tl = ST, TL; bt = beat_at(tl, t); title, col, fn, _ = SCN[bt["ci"]]
    bg = st.background(t); im = bg.copy()
    sp = t - bt["s0"]; fade = pr(sp, 0, .35) * (1 - pr(sp, bt["sL"] - .3, bt["sL"])) if bt["ci"] < tl["ns"] - 1 else pr(sp, 0, .35)
    g = G(st, im, t, bt, fade)
    if title:
        if st.V: tx(g, st.W / 2, 232, title, fit(title, XB, 58, st.W - 130), col, 1, "mm")
        else: tx(g, st.W / 2, 150, title, fit(title, XB, 54, st.W - 300), col, 1, "mm")
    fn(g)
    if g._lit and title: g._lit.append((0, 180, st.W, 290) if st.V else (0, 100, st.W, 200))
    im = g.im
    if g._lit and g._lit_a > 0: im = st.spot(im, g._lit, g._lit_a, g._strength)
    im = st.post(im)
    if fade < 1: im = Image.blend(st.post(bg), im, fade)
    st.ui(im, tl, bt, t)
    return im


def _part(args):
    i0, i1, path = args; st = ST
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{st.W}x{st.H}", "-r", str(st.fps),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-threads", "1", path], stdin=subprocess.PIPE)
    for i in range(i0, i1): p.stdin.write(frame(i / st.fps).tobytes())
    p.stdin.close(); p.wait(); return path


def music(dur, path, seed=0):
    import numpy as np, soundfile as sf
    from scipy.signal import lfilter
    SR = 44100; n = int(SR * dur) + SR; out = np.zeros(n)
    def note(m): return 440 * 2 ** ((m - 69) / 12)
    progs = [[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]],
             [[52, 55, 59], [48, 52, 55], [50, 53, 57], [47, 50, 54]], [[53, 57, 60], [50, 53, 57], [46, 50, 53], [48, 52, 55]]]
    chords = progs[seed % 4]; bar = 4 * 60 / 80
    for b in range(int(dur / bar) + 1):
        ch = chords[b % 4]; st = int(b * bar * SR); L = int((bar + .6) * SR); tt = np.arange(L) / SR
        s = sum(np.sin(2 * np.pi * note(m) * tt * (1 + dd)) for m in ch for dd in (-.003, .003)) + .8 * np.sin(2 * np.pi * note(ch[0] - 12) * tt)
        e = np.minimum(1, tt / .9) * np.minimum(1, (L / SR - tt) / .9)
        seg = s * e; en = min(n, st + L); out[st:en] += seg[:en - st]
    out = lfilter([0.05], [1, -0.95], out)
    step = 60 / 80 / 2; tt0 = 0.0; k = 0
    while tt0 < dur - 2:
        b = int(tt0 / bar); m = chords[b % 4][[0, 1, 2, 1, 2, 1, 0, 1][k % 8]] + 12
        L = int(.5 * SR); tt = np.arange(L) / SR
        sig = np.sin(2 * np.pi * note(m) * tt) * np.exp(-tt * 7) * .18
        st = int(tt0 * SR); en = min(n, st + L); out[st:en] += sig[:en - st]; tt0 += step; k += 1
    out /= np.max(np.abs(out)); fade = int(3 * SR); out[-fade:] *= np.linspace(1, 0, fade); out[:SR] *= np.linspace(0, 1, SR)
    sf.write(path, out, SR)


def sfx(tl, n, SR):
    """soft whoosh on scene changes, tiny blip when a new step appears"""
    import numpy as np
    rs = np.random.RandomState(3); out = np.zeros(n)
    for b in tl["beats"]:
        st = int(b["t0"] * SR)
        if b["bi"] == 0 and b["ci"] > 0:
            L = int(.5 * SR); tt = np.arange(L) / SR; nz = rs.randn(L)
            nz = np.convolve(nz, np.ones(40) / 40, mode="same") * np.sin(np.pi * tt / .5) ** 2 * .5
            en = min(n, st + L); out[st:en] += nz[:en - st]
        else:
            L = int(.16 * SR); tt = np.arange(L) / SR
            bl = np.sin(2 * np.pi * 1175 * tt) * np.exp(-tt * 34) * .1
            s2 = st + int(.05 * SR); en = min(n, s2 + L); out[s2:en] += bl[:en - s2]
    return out


def run(scenes, stage, out, final, mode="preview", seed=0, max_dur=None, voice=None):
    """mode: preview | frames:<t1,t2,..> | check | full"""
    global ST, TL, SCN
    if voice: VOICE.update(voice)
    ST, SCN = stage, scenes; TL = tl = build(scenes, out)
    dur = tl["dur"]; st = stage
    words = sum(len(b["spoken"].split()) for b in tl["beats"]); vt = sum(b["vd"] for b in tl["beats"])
    print(f"duration {dur:.1f}s  beats {len(tl['beats'])}  scenes {tl['ns']}  voice {vt:.0f}s  {words / vt * 60:.0f} wpm")
    if max_dur and dur > max_dur: print(f"!! TOO LONG by {dur - max_dur:.1f}s")
    json.dump({"chapters": list(zip(tl["starts"], tl["titles"])), "dur": dur}, open(f"{out}/chapters.json", "w"))
    if mode == "preview":
        tw_, th_ = (405, 720) if st.V else (640, 360); per = 8 if st.V else 9; cols = 4 if st.V else 3
        ims = [frame(b["t0"] + b["L"] * .86).resize((tw_, th_)) for b in tl["beats"]]
        for pg in range(0, len(ims), per):
            chunk = ims[pg:pg + per]; rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new("RGB", (tw_ * cols, th_ * rows), (0, 0, 0))
            for i, im in enumerate(chunk): sheet.paste(im, ((i % cols) * tw_, (i // cols) * th_))
            sheet.save(f"{out}/sheet{pg // per}.png")
        print("sheets", (len(ims) + per - 1) // per); return tl
    if mode.startswith("frames:"):
        for k, tt in enumerate(mode[7:].split(",")):
            frame(float(tt)).save(f"{out}/f{k}.png")
        return tl
    if mode == "check":
        from voice import asr, sim
        bad = 0
        for b in tl["beats"]:
            h = asr(b["wav"]); disp = " ".join(w for w, _ in b["toks"]); sc_ = max(sim(disp, h), sim(b["spoken"], h))
            if sc_ < .86: bad += 1; print(f"  {sc_:.2f} [{b['ci']}.{b['bi']}] {disp}\n        heard: {h}")
        print("asr check done, flagged", bad); return tl
    import numpy as np, soundfile as sf, multiprocessing as mp
    nf = int(dur * st.fps); P = 2; cut = [nf * i // P for i in range(P + 1)]
    parts = [(cut[i], cut[i + 1], f"{out}/part{i}.mp4") for i in range(P)]
    with mp.get_context("fork").Pool(P) as pool: pool.map(_part, parts)
    open(f"{out}/list.txt", "w").write("".join(f"file '{p[2]}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/silent.mp4"], check=True)
    SR = 44100; n = int(dur * SR) + SR; voice_ = np.zeros(n)
    for b in tl["beats"]:
        v, sr = sf.read(b["wav"]); m = int(len(v) * SR / sr)
        v = np.interp(np.arange(m) * sr / SR, np.arange(len(v)), v)
        s0 = int((b["t0"] + b["lead"]) * SR); en = min(n, s0 + len(v)); voice_[s0:en] += v[:en - s0]
    voice_ /= np.max(np.abs(voice_)); sf.write(f"{out}/voice_raw.wav", voice_, SR)
    # voice chain: rumble cut, a little warmth and presence, gentle compression
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/voice_raw.wav", "-af",
                    "highpass=f=75,equalizer=f=190:t=q:w=1:g=1.5,equalizer=f=3400:t=q:w=1.4:g=2.5,"
                    "acompressor=threshold=0.14:ratio=2.5:attack=8:release=140:makeup=1.6,alimiter=limit=0.95", f"{out}/voice.wav"], check=True)
    voice_, _ = sf.read(f"{out}/voice.wav"); voice_ = np.pad(voice_, (0, max(0, n - len(voice_))))[:n]
    music(dur, f"{out}/music.wav", seed); mus, _ = sf.read(f"{out}/music.wav"); m_ = np.zeros(n); m_[:min(n, len(mus))] = mus[:n]
    w = int(.3 * SR); env = np.convolve(np.abs(voice_), np.ones(w) / w, mode="same")
    duck = 1 - 0.6 * np.clip(env / (env.max() * .15), 0, 1)
    mix_ = voice_ / np.max(np.abs(voice_)) * .95 + m_ * .15 * duck + sfx(tl, n, SR) * .5
    mix_ /= max(1, np.max(np.abs(mix_)) / .97)
    sf.write(f"{out}/mix.wav", np.stack([mix_, mix_], 1), SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/silent.mp4", "-i", f"{out}/mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", final], check=True)
    print("DONE", final, round(dur, 1)); return tl

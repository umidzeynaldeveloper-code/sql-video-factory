"""audio.py — v2.1 sound design for @sql_developer_no1 (NumPy + SciPy only, no samples, no new libraries).

Every sound is synthesised and returned as a stereo float32 array of shape (n, 2) at SR.
Common parameters for every sound:
    dur   seconds            amp   peak level 0..1
    tone  pitch multiplier   pan   -1 (left) .. +1 (right)
Mastering helpers: resample(), duck(), place_events(), master_2pass().
"""
import json, math, subprocess
import numpy as np
from scipy import signal

SR = 48000
_rs = np.random.RandomState(7)


# ------------------------------------------------------------------ helpers
def _t(dur): return np.arange(max(1, int(dur * SR))) / SR


def _pan(x, p=0.0):
    """equal-power pan of a mono signal -> stereo"""
    a = (clip(p, -1, 1) + 1) * math.pi / 4
    return np.stack([x * math.cos(a), x * math.sin(a)], 1).astype(np.float32)


def _pan_moving(x, p0, p1):
    a = (np.clip(np.linspace(p0, p1, len(x)), -1, 1) + 1) * math.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], 1).astype(np.float32)


def clip(v, a, b): return max(a, min(b, v))


def _norm(x, amp):
    m = np.max(np.abs(x)) if len(x) else 0
    return x * (amp / m) if m > 0 else x


def _env(n, a=.005, r=.2, curve=4.0):
    """attack (linear) + exponential release envelope over n samples"""
    t = np.arange(n) / SR; na = max(1, int(a * SR))
    e = np.exp(-curve * np.maximum(0, t - a) / max(r, 1e-3))
    e[:na] *= np.linspace(0, 1, na)
    return e


def _noise(n, color="white"):
    x = _rs.randn(n)
    if color == "pink":   # Voss-McCartney approximation via 1/f filter
        b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]; a = [1, -2.494956002, 2.017265875, -0.522189400]
        x = signal.lfilter(b, a, x)
    elif color == "brown":
        x = np.cumsum(x); x -= signal.lfilter([1], [1, -0.995], x) * 0.005
        x = signal.lfilter([1, -1], [1, -0.995], x)
    return x / (np.max(np.abs(x)) + 1e-9)


def _tv_filter(x, f0, f1, kind="bandpass", q=1.2, blocks=96):
    """time-varying 2nd-order filter: centre frequency glides f0 -> f1 (log), block-wise with state carry-over"""
    n = len(x); out = np.zeros(n); zi = None
    edges = np.linspace(0, n, blocks + 1).astype(int)
    for k in range(blocks):
        f = f0 * (f1 / f0) ** (k / max(1, blocks - 1)); f = clip(f, 30, SR / 2.3)
        if kind == "bandpass": sos = signal.butter(2, [f / (1 + .5 / q), f * (1 + .5 / q)], "bandpass", fs=SR, output="sos")
        elif kind == "lowpass": sos = signal.butter(2, f, "lowpass", fs=SR, output="sos")
        else: sos = signal.butter(2, f, "highpass", fs=SR, output="sos")
        if zi is None or zi.shape != (sos.shape[0], 2): zi = signal.sosfilt_zi(sos) * 0
        seg, zi = signal.sosfilt(sos, x[edges[k]:edges[k + 1]], zi=zi); out[edges[k]:edges[k + 1]] = seg
    return out


def _reverb(st, size=1.2, mix=.25, damp=4000):
    """cheap stereo room: decorrelated exponentially decaying noise impulse responses"""
    n = int(size * SR); t = np.arange(n) / SR
    out = np.zeros((len(st) + n - 1, 2))
    for ch in range(2):
        ir = np.random.RandomState(11 + ch).randn(n) * np.exp(-6.9 * t / size)
        ir = signal.sosfilt(signal.butter(1, damp, "lowpass", fs=SR, output="sos"), ir); ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
        out[:, ch] = signal.fftconvolve(st[:, ch], ir)
    dry = np.zeros_like(out); dry[:len(st)] = st
    return ((1 - mix) * dry + mix * out).astype(np.float32)


def _sat(x, drive=1.5): return np.tanh(x * drive) / np.tanh(drive)


# ------------------------------------------------------------------ sounds
def whoosh(dur=.7, tone=1.0, amp=.5, pan=0.0, spread=.8):
    """cinematic whoosh: band-passed noise sweeping up then down, moving across the stereo field"""
    n = int(dur * SR); x = _noise(n, "pink")
    up = _tv_filter(x, 350 * tone, 4200 * tone, "bandpass", q=.9)
    sh = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.6                  # swell
    y = up * sh
    st = _pan_moving(y, pan - spread, pan + spread)
    return _norm(_reverb(st, .9, .22), amp)


def impact(dur=1.4, tone=1.0, amp=.8, pan=0.0):
    """deep impact: pitch-dropping body + noise transient + room tail"""
    t = _t(dur); f = 110 * tone * np.exp(-t * 9) + 38 * tone
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    tr = _noise(len(t)) * np.exp(-t * 60); tr = signal.sosfilt(signal.butter(2, 2200, "lowpass", fs=SR, output="sos"), tr)
    y = _sat(body * .9 + tr * .5, 1.8)
    return _norm(_reverb(_pan(y, pan), 1.6, .3, 2500), amp)


def sub_hit(dur=1.1, freq=46.0, amp=.8, pan=0.0, tone=1.0):
    """sub-bass hit: sine with a short downward pitch bend and soft saturation"""
    t = _t(dur); f = freq * tone * (1 + 1.2 * np.exp(-t * 18))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), .004, dur * .55, 3.5)
    return _norm(_pan(_sat(y, 2.2), pan), amp)


def click(dur=.07, tone=1.0, amp=.35, pan=0.0):
    """digital UI click: short bright tick with a tiny body"""
    t = _t(dur)
    y = np.sin(2 * np.pi * 2600 * tone * t) * np.exp(-t * 140) + .6 * np.sin(2 * np.pi * 1300 * tone * t) * np.exp(-t * 90)
    y += _noise(len(t)) * np.exp(-t * 400) * .4
    y = signal.sosfilt(signal.butter(2, [600, 9000], "bandpass", fs=SR, output="sos"), y)
    return _norm(_pan(y, pan), amp)


def data(dur=.9, tone=1.0, amp=.3, pan=-.7, rate=26, pan_to=.7, seed=3):
    """data transfer: fast stream of tiny pitched blips travelling across the stereo field"""
    rs = np.random.RandomState(seed); n = int(dur * SR); out = np.zeros((n, 2), np.float32)
    scale = [0, 2, 4, 7, 9, 12, 14, 16]; k = 0; step = 1 / rate
    while k * step < dur - .05:
        st = int(k * step * SR); L = int(.045 * SR); tt = np.arange(L) / SR
        f = 880 * tone * 2 ** (scale[rs.randint(len(scale))] / 12)
        b = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 70) * (.6 + .4 * rs.rand())
        p = pan + (pan_to - pan) * (k * step / dur); s2 = _pan(b, p); en = min(n, st + L)
        out[st:en] += s2[:en - st]; k += 1
    out *= np.minimum(1, np.linspace(0, 6, n))[:, None] * np.minimum(1, np.linspace(6, 0, n))[:, None]
    return _norm(_reverb(out, .6, .18), amp)


def riser(dur=1.6, tone=1.0, amp=.45, pan=0.0):
    """smooth riser: noise with rising high-pass + rising sine, swelling to the end"""
    n = int(dur * SR); t = np.arange(n) / SR
    nz = _tv_filter(_noise(n, "pink"), 400 * tone, 7000 * tone, "highpass")
    f = 180 * tone * (8 ** (t / dur)); s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    sw = (t / dur) ** 2.2
    y = (nz * .7 + s * .35) * sw
    y[-int(.03 * SR):] *= np.linspace(1, 0, int(.03 * SR))
    return _norm(_reverb(_pan_moving(y, pan - .3, pan + .3), 1.0, .2), amp)


def sweep(dur=.6, tone=1.0, amp=.4, pan=0.0):
    """transition sweep: falling filtered saw + air, for scene changes"""
    t = _t(dur); f = 1400 * tone * np.exp(-t * 4.5) + 120
    ph = np.cumsum(f) / SR; saw = 2 * (ph % 1) - 1
    y = _tv_filter(saw, 5000, 300, "lowpass") * np.sin(np.pi * np.linspace(0, 1, len(t))) ** 1.2
    air = _tv_filter(_noise(len(t)), 6000, 1500, "bandpass") * .5 * np.sin(np.pi * np.linspace(0, 1, len(t)))
    return _norm(_reverb(_pan_moving(y * .6 + air, pan + .6, pan - .6), .8, .25), amp)


def atmos(dur=10.0, tone=1.0, amp=.12, pan=0.0, seed=5):
    """atmospheric bed: detuned low pad + slowly breathing filtered noise, decorrelated L/R"""
    t = _t(dur); rs = np.random.RandomState(seed); n = len(t); st = np.zeros((n, 2))
    for ch in range(2):
        pad = sum(np.sin(2 * np.pi * f * tone * (1 + d) * t + rs.rand() * 6) for f in (55, 82.4, 110, 164.8) for d in (-.004, .004))
        lfo = .6 + .4 * np.sin(2 * np.pi * (.07 + .02 * ch) * t + ch)
        nz = signal.sosfilt(signal.butter(2, [300, 1600], "bandpass", fs=SR, output="sos"), _noise(n, "pink")) * lfo
        st[:, ch] = pad / 8 + nz * .5
    fade = min(n // 3, int(1.5 * SR)); w = np.ones(n); w[:fade] = np.linspace(0, 1, fade); w[-fade:] = np.linspace(1, 0, fade)
    return _norm(st * w[:, None], amp).astype(np.float32)


def success(dur=1.3, tone=1.0, amp=.4, pan=0.0):
    """completion: bright bell arpeggio (major triad + octave)"""
    n = int(dur * SR); out = np.zeros(n)
    for k, semi in enumerate((0, 4, 7, 12)):
        st = int(k * .075 * SR); L = n - st; tt = np.arange(L) / SR; f = 784 * tone * 2 ** (semi / 12)
        b = (np.sin(2 * np.pi * f * tt) + .35 * np.sin(2 * np.pi * 2.76 * f * tt) * np.exp(-tt * 6)) * np.exp(-tt * 4.2)
        out[st:] += b * (.8 + .1 * k)
    return _norm(_reverb(_pan(out, pan), 1.4, .3), amp)


def error(dur=.55, tone=1.0, amp=.4, pan=0.0):
    """warning / error: two short buzzy notes falling a semitone"""
    n = int(dur * SR); out = np.zeros(n)
    for k, f in enumerate((233.1 * tone, 220.0 * tone)):
        st = int(k * .2 * SR); L = int(.18 * SR); tt = np.arange(L) / SR
        sq = signal.square(2 * np.pi * f * tt) * .6 + np.sin(2 * np.pi * f * tt)
        b = signal.sosfilt(signal.butter(2, 1800, "lowpass", fs=SR, output="sos"), sq) * _env(L, .004, .12, 3)
        en = min(n, st + L); out[st:en] += b[:en - st]
    return _norm(_reverb(_pan(out, pan), .7, .15), amp)


SOUNDS = dict(whoosh=whoosh, impact=impact, sub_hit=sub_hit, click=click, data=data, riser=riser,
              sweep=sweep, atmos=atmos, success=success, error=error)


# ------------------------------------------------------------------ timeline + mastering
def place_events(events, n):
    """events: list of dict(t=seconds, name=str, **params). 'riser' is placed so that it ENDS at t."""
    out = np.zeros((n, 2), np.float32)
    for e in events:
        p = {k: v for k, v in e.items() if k not in ("t", "name")}
        s = SOUNDS[e["name"]](**p)
        t0 = e["t"] - (len(s) / SR if e["name"] == "riser" else 0)
        st = max(0, int(t0 * SR)); en = min(n, st + len(s))
        if en > st: out[st:en] += s[:en - st]
    return out


def resample(x, sr_in, sr_out=SR):
    """band-limited polyphase resampling (replaces np.interp)"""
    if sr_in == sr_out: return np.asarray(x, np.float64)
    g = math.gcd(int(sr_in), int(sr_out))
    return signal.resample_poly(x, sr_out // g, sr_in // g)


def duck(music, voice, depth=.65, attack=.03, release=.35, thresh=.08):
    """side-chain ducking with separate attack/release (envelope computed on 1 ms hops, then interpolated)"""
    hop = SR // 1000; v = np.abs(voice if voice.ndim == 1 else voice.mean(1))
    m = len(v) // hop; e = v[:m * hop].reshape(m, hop).max(1)
    ca, cr = math.exp(-1 / (attack * 1000)), math.exp(-1 / (release * 1000)); env = np.zeros(m); s = 0.0
    for i in range(m):
        c = ca if e[i] > s else cr; s = c * s + (1 - c) * e[i]; env[i] = s
    env = np.interp(np.arange(len(v)) / hop, np.arange(m), env)
    g = 1 - depth * np.clip(env / (thresh * (np.max(env) + 1e-9)) , 0, 1)
    return music * (g[:, None] if music.ndim == 2 else g)


def _ff(args):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-y", *args], capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError("ffmpeg failed: " + r.stderr[-600:])
    return r.stderr


def master_2pass(inp, out, I=-14.0, TP=-1.5, LRA=11.0):
    """two-pass EBU R128 loudness normalisation (measure, then apply measured values linearly)"""
    err = _ff(["-i", inp, "-af", f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"])
    j = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    f = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
         f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    _ff(["-i", inp, "-af", f, "-ar", str(SR), out])
    return j


def loudness(path):
    """measure integrated loudness / true peak / LRA of a file (for reports)"""
    err = _ff(["-i", path, "-af", "loudnorm=print_format=json", "-f", "null", "-"])
    j = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    return dict(I=float(j["input_i"]), TP=float(j["input_tp"]), LRA=float(j["input_lra"]))


if __name__ == "__main__":   # audition: writes every sound to a wav
    import soundfile as sf, sys
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    for k, fn in SOUNDS.items():
        sf.write(f"{d}/sfx_{k}.wav", fn(dur=4.0) if k == "atmos" else fn(), SR)
    print("ok", list(SOUNDS))

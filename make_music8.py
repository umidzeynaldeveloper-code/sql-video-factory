import numpy as np, wave
SR = 44100; DUR = 104.0
n = int(SR * DUR); t = np.arange(n) / SR
out = np.zeros(n)

def note(f): return 440 * 2 ** ((f - 69) / 12)
def env(length, a=0.01, r=0.3):
    L = int(length * SR); e = np.ones(L)
    A = max(1, int(a * SR)); R = max(1, int(r * SR))
    e[:A] = np.linspace(0, 1, A); e[-R:] *= np.linspace(1, 0, R)
    return e
def add(sig, start, gain=1.0):
    s = int(start * SR); e = min(n, s + len(sig))
    if s < n: out[s:e] += sig[:e - s] * gain
def lowpass(x, a):  # one-pole
    y = np.zeros_like(x); acc = 0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y

BPM = 100; beat = 60 / BPM; bar = beat * 4
# Am - F - C - G (midi)
chords = [[52, 55, 59], [48, 52, 55], [50, 53, 57], [47, 50, 54]]
bass = [40, 36, 38, 35]

# --- warm pad (all the way)
pad = np.zeros(n)
for b in range(int(DUR / bar) + 1):
    ch = chords[b % 4]; st = b * bar; L = bar + 0.4
    tt = np.arange(int(L * SR)) / SR
    s = sum(np.sin(2 * np.pi * note(m) * tt * (1 + d)) for m in ch for d in (-.003, .003))
    s += 0.3 * sum(np.sin(2 * np.pi * note(m + 12) * tt) for m in ch)
    s *= env(L, .6, .8)
    ps = int(st * SR); pe = min(n, ps + len(s)); pad[ps:pe] += s[:pe - ps]
pad = lowpass(pad, 0.08)
add(pad / np.max(np.abs(pad)), 0, 0.22)

# --- sub bass from 3.5s
for b in range(int(DUR / bar) + 1):
    st = b * bar
    if st < 3.4: continue
    tt = np.arange(int(bar * SR)) / SR
    s = np.sin(2 * np.pi * note(bass[b % 4]) * tt) * env(bar, .02, .4)
    add(s, st, 0.20)

# --- pluck arpeggio (8ths) from 3.5s, "digital" feel
arp_pat = [0, 1, 2, 1, 0, 2, 1, 2]
step = beat / 2
k = 0; tt0 = 3.5
while tt0 < DUR - 1.5:
    b = int(tt0 / bar); ch = chords[b % 4]
    m = ch[arp_pat[k % 8]] + 12
    L = 0.35; tt = np.arange(int(L * SR)) / SR
    s = (np.sin(2 * np.pi * note(m) * tt) + .25 * np.sin(2 * np.pi * note(m) * 2 * tt)) * np.exp(-tt * 9)
    gain = 0.10 if tt0 < 8.5 else 0.13
    add(s, tt0, gain); tt0 += step; k += 1

# --- soft kick + hats from 8.5s
tb = 16.0
while tb < DUR - 1.5:
    L = 0.25; tt = np.arange(int(L * SR)) / SR
    f = 120 * np.exp(-tt * 25) + 45
    kick = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 14)
    add(kick, tb, 0.35)
    hat = np.random.randn(int(.04 * SR)) * np.exp(-np.arange(int(.04 * SR)) / SR * 120)
    hat = np.diff(hat, prepend=0)
    add(hat, tb + beat / 2, 0.035)
    tb += beat

# SFX
def tick(at, g=0.06, f=2200):
    L = .03; tt = np.arange(int(L * SR)) / SR
    add(np.sin(2 * np.pi * f * tt) * np.exp(-tt * 200), at, g)
def ding(at, f=1320, g=0.12):
    L = .9; tt = np.arange(int(L * SR)) / SR
    s = (np.sin(2 * np.pi * f * tt) + .4 * np.sin(2 * np.pi * f * 2.01 * tt)) * np.exp(-tt * 5)
    add(s, at, g)
def whoosh(at, g=0.10):
    L = .6; x = np.random.randn(int(L * SR))
    x = lowpass(x, 0.05) * np.sin(np.linspace(0, np.pi, len(x))) ** 2
    add(x / np.max(np.abs(x)), at - .3, g)
def click(at, g=0.25):
    L = .05; tt = np.arange(int(L * SR)) / SR
    add(np.random.randn(len(tt)) * np.exp(-tt * 150) + np.sin(2 * np.pi * 900 * tt) * np.exp(-tt * 80), at, g)



T = [0, 6, 16, 30, 42, 54, 66, 78, 90, 98]
for ts in T[1:]: whoosh(ts)
def typing(start, nchar, speed):
    for j in range(0, nchar, 3): tick(start + j*speed, .025, 3000)
def lock(at): click(at, .2); ding(at + .02, 1568, .07)
def wait(at): tick(at, .06, 900); tick(at + .15, .05, 800)
def err(at): click(at, .3); ding(at + .03, 311, .12); ding(at + .2, 294, .08)
def ok(at): ding(at, 1318, .09); ding(at + .15, 1760, .07)
wait(1.5); err(2.4)
lock(T[1] + 1.5); wait(T[1] + 3.5); ok(T[1] + 6.5); lock(T[1] + 7)
lock(T[2] + 2); lock(T[2] + 5); wait(T[2] + 8.5); wait(T[2] + 11)
for k in range(6): tick(T[3] + .3 + k * .6, .05, 700 + (k % 2) * 200)
ding(T[3] + 3.5, 330, .1)
ding(T[4] + 1, 1046, .07); err(T[4] + 3); ding(T[4] + 5, 880, .08); click(T[4] + 8, .2); lock(T[4] + 9); ok(T[4] + 10.5)
lock(T[5] + 1.5); wait(T[5] + 3); lock(T[5] + 5); ok(T[5] + 7); lock(T[5] + 9); ok(T[5] + 10.5)
typing(T[6] + .8, 60, .03); err(T[6] + 2.6); ding(T[6] + 5, 1046, .08)
for k in range(2): ding(T[6] + 7.5 + k * .6, 1318, .07)
typing(T[7] + .3, 30, .03); err(T[7] + 2.5); ok(T[7] + 7); ding(T[7] + 8.5, 1568, .08)
for k in range(5): ding(T[8] + .2 + k * .3, 1046 + k * 100, .06)
ok(T[9] + .9)
# master fade + normalize
fade = np.ones(n); fi = int(.8 * SR); fo = int(2 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
out *= fade
out = np.tanh(out * 1.2); out /= np.max(np.abs(out)); out *= 0.85
pcm = (out * 32767).astype(np.int16)
st = np.stack([pcm, pcm], 1)
with wave.open("music8.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print("ok")

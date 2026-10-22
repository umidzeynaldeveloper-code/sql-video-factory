import numpy as np, wave
SR = 44100; DUR = 113.0
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
chords = [[50, 53, 57], [46, 50, 53], [48, 52, 55], [45, 48, 52]]
bass = [38, 34, 36, 33]

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



T = [0, 6, 16, 29, 39, 57, 65, 74, 91, 101, 107]
for ts in T[1:]: whoosh(ts)
def typing(start, nchar, speed):
    for j in range(0, nchar, 3): tick(start + j*speed, .025, 3000)
ding(1.3, 1568, .12); click(4.6, .2); ding(4.65, 523, .08)
for j in range(30): tick(T[1] + 1 + j*.15, .03, 1400 + (j % 3)*200)
ding(T[1] + 3.1, 880, .07); ding(T[1] + 4.2, 1318, .10); whoosh(T[1] + 5.3, .07); ding(T[1] + 5.5, 1568, .10)
for j in range(65): tick(T[2] + 2.5 + j*.1, .03, 1200 + (j % 4)*100)
ding(T[2] + 7.75, 1046, .08); click(T[2] + 9.0, .2)
for k in range(4): tick(T[3] + .9 + k*.15, .05, 2200)
ding(T[3] + 2.2, 1318, .10)
for k in range(4): ding(T[3] + 3.8 + k*.4, [784, 988, 1175, 1568][k], .06)
ding(T[4] + .5, 659, .07)
for k, st in enumerate([3, 6.5, 10, 13]): ding(T[4] + st, [880, 1046, 1318, 1760][k], .11); tick(T[4] + st, .07, 2600)
for k in range(8): tick(T[5] + .6 + k*.15, .04, 900 + k*120)
ding(T[5] + 2.6, 1568, .12); ding(T[5] + 2.75, 2093, .07)
typing(T[6] + .4, 50, .03); click(T[6] + 2.2, .25); ding(T[6] + 2.25, 330, .10)
ding(T[6] + 4.0, 1318, .10); ding(T[6] + 4.15, 1760, .07)
for k in range(4): click(T[7] + k*4 + .3, .22); ding(T[7] + k*4 + .35, 311, .08); ding(T[7] + k*4 + 1.6, 1318, .09)
for k in range(3): ding(T[8] + .4 + k*2.6, 1046 + k*130, .09)
for k in range(3): tick(T[9] + .4 + k*.3, .06, 1800)
click(T[9] + 2.5, .25); ding(T[9] + 2.55, 330, .10)
for k in range(4): tick(T[10] + .2 + k*.25, .05, 2000 + k*200)
ding(T[10] + 2.2, 1046, .10); ding(T[10] + 2.35, 1568, .08)
# master fade + normalize
fade = np.ones(n); fi = int(.8 * SR); fo = int(2 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
out *= fade
out = np.tanh(out * 1.2); out /= np.max(np.abs(out)); out *= 0.85
pcm = (out * 32767).astype(np.int16)
st = np.stack([pcm, pcm], 1)
with wave.open("music5.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print("ok")

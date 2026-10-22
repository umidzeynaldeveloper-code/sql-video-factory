import sys, os, re, json, subprocess, importlib.util
sys.path.insert(0, "/home/claude/en"); sys.path.insert(0, "/home/claude")
import numpy as np, soundfile as sf
from narration import T_ORIG, N as NARR, SLUG
from translations import TR, COMMON

V = int(sys.argv[1]); MODE = sys.argv[2] if len(sys.argv) > 2 else "full"
OUT = f"/home/claude/en/v{V}"; os.makedirs(OUT, exist_ok=True)
FPS = 30; LEAD = 0.35

# 1) translated source module
src = open(f"/home/claude/make_video{V}.py").read()
for cut in ("\np = subprocess.Popen", "\nif __name__"):
    if cut in src: src = src[:src.index(cut)]
for az, en in TR.get(V, {}).items():
    src = src.replace(f'"{az}"', f'"{en}"')
for az, en in COMMON.items():
    src = src.replace(f'"{az}"', f'"{en}"')
src = src.replace("Əli", "Ali")
mod_path = f"{OUT}/video{V}_en_src.py"; open(mod_path, "w").write(src)
spec = importlib.util.spec_from_file_location(f"v{V}en", mod_path); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

# 2) narration
meta_p = f"{OUT}/narr.json"
lines = NARR[V]
meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
if meta.get("lines") != lines:
    from tts import say
    durs = [say(l, f"{OUT}/n_{k}.wav", sid=6) for k, l in enumerate(lines)]
    meta = {"lines": lines, "durs": durs}; json.dump(meta, open(meta_p, "w"))
durs = meta["durs"]
To = T_ORIG[V]
Tn = [0.0]
for k, dd in enumerate(durs):
    Tn.append(Tn[-1] + max(dd + LEAD + (1.8 if k == len(durs) - 1 else 0.7), (To[k + 1] - To[k]) * 0.9))
DUR = Tn[-1]; NF = int(DUR * FPS)

def frame_en(i):
    t = i / FPS
    k = max(j for j in range(len(Tn) - 1) if Tn[j] <= t) if t < Tn[-1] else len(Tn) - 2
    lt = t - Tn[k]
    lo = lt * (To[k + 1] - To[k]) / (Tn[k + 1] - Tn[k])
    return M.frame((To[k] + min(lo, To[k + 1] - To[k] - 1e-3)) * FPS)

if MODE == "preview":
    from PIL import Image
    ns = len(Tn) - 1; cols = min(ns, 6); rows = (ns + cols - 1) // cols
    sheet = Image.new("RGB", (270 * cols, 480 * rows))
    for k in range(ns):
        im = frame_en(int((Tn[k] + (Tn[k + 1] - Tn[k]) * .72) * FPS))
        sheet.paste(im.resize((270, 480)), ((k % cols) * 270, (k // cols) * 480))
    sheet.save(f"{OUT}/sheet.png"); print("preview", round(DUR, 1)); sys.exit()

# 3) video
W, H = 1080, 1920
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
    "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart", f"{OUT}/silent.mp4"], stdin=subprocess.PIPE)
for i in range(NF): p.stdin.write(frame_en(i).tobytes())
p.stdin.close(); p.wait()

# 4) music
msrc = open("/home/claude/make_music7.py").read()
head, rest = msrc.split("# SFX", 1)
fx = rest.split("\nT = [")[0]; tail = rest.split("# master fade")[1]
head = re.sub(r"DUR = [\d.]+", f"DUR = {DUR:.3f}", head)
head = head.replace("tb = 14.0", f"tb = {Tn[1]:.3f}")
prog = {2: ("[[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]]", "[38, 34, 41, 36]"),
        3: ("[[52, 55, 59], [48, 52, 55], [55, 59, 62], [50, 54, 57]]", "[40, 36, 43, 38]"),
        4: ("[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]", "[45, 41, 36, 43]"),
        5: ("[[50, 53, 57], [46, 50, 53], [48, 52, 55], [45, 48, 52]]", "[38, 34, 36, 33]"),
        6: ("[[52, 55, 59], [50, 53, 57], [48, 52, 55], [47, 50, 54]]", "[40, 38, 36, 35]"),
        7: ("[[57, 60, 64], [55, 59, 62], [53, 57, 60], [52, 56, 59]]", "[45, 43, 41, 40]"),
        8: ("[[52, 55, 59], [48, 52, 55], [50, 53, 57], [47, 50, 54]]", "[40, 36, 38, 35]"),
        9: ("[[50, 53, 57], [48, 52, 55], [46, 50, 53], [45, 49, 52]]", "[38, 36, 34, 33]"),
        10: ("[[53, 57, 60], [50, 53, 57], [46, 50, 53], [48, 52, 55]]", "[41, 38, 34, 36]"),
        11: ("[[57, 60, 64], [52, 55, 59], [53, 57, 60], [55, 59, 62]]", "[45, 40, 41, 43]"),
        12: ("[[52, 55, 59], [55, 59, 62], [57, 60, 64], [50, 54, 57]]", "[40, 43, 45, 38]"),
        13: ("[[50, 53, 57], [53, 57, 60], [55, 58, 62], [48, 52, 55]]", "[38, 41, 43, 36]"),
        14: ("[[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]]", "[45, 41, 43, 40]"),
        15: ("[[52, 55, 59], [50, 53, 57], [48, 52, 55], [47, 50, 54]]", "[40, 38, 36, 35]"),
        16: ("[[55, 59, 62], [52, 55, 59], [53, 57, 60], [50, 54, 57]]", "[43, 40, 41, 38]")}.get(V, [
        ("[[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]]", "[45, 41, 43, 40]"),
        ("[[50, 53, 57], [46, 50, 53], [48, 52, 55], [45, 48, 52]]", "[38, 34, 36, 33]"),
        ("[[52, 55, 59], [48, 52, 55], [50, 53, 57], [47, 50, 54]]", "[40, 36, 38, 35]"),
        ("[[53, 57, 60], [50, 53, 57], [46, 50, 53], [48, 52, 55]]", "[41, 38, 34, 36]")][V % 4])
head = re.sub(r"chords = \[\[.*?\]\]", f"chords = {prog[0]}", head)
head = re.sub(r"bass = \[[\d, ]+\]", f"bass = {prog[1]}", head)
ev = f"\nT = {Tn[:-1]}\nfor ts in T[1:]: whoosh(ts, .06)\nfor ts in T: ding(ts + .5, 1318, .05)\n"
open(f"{OUT}/music.py", "w").write(head + "# SFX" + fx + ev + "# master fade" + tail.replace('"music7.wav"', f'"{OUT}/music.wav"'))
subprocess.run(["python3", f"{OUT}/music.py"], check=True)

# 5) voice + duck + mix
SR = 44100; n = int(DUR * SR) + SR; voice = np.zeros(n)
for k in range(len(durs)):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/n_{k}.wav", "-ar", str(SR), "-ac", "1", f"{OUT}/n_{k}_44.wav"], check=True)
    v, _ = sf.read(f"{OUT}/n_{k}_44.wav"); s = int((Tn[k] + LEAD) * SR); e = min(n, s + len(v)); voice[s:e] += v[:e - s]
mus, _ = sf.read(f"{OUT}/music.wav"); mus = mus[:, 0] if mus.ndim > 1 else mus
m = np.zeros(n); m[:min(n, len(mus))] = mus[:n]
w = int(.3 * SR); env = np.convolve(np.abs(voice), np.ones(w) / w, mode="same")
duck = 1 - 0.55 * np.clip(env / (env.max() * .15), 0, 1)
mix = voice / np.max(np.abs(voice)) * 0.95 + m * 0.32 * duck
mix /= max(1, np.max(np.abs(mix)) / 0.97)
sf.write(f"{OUT}/mix.wav", np.stack([mix, mix], 1), SR)
final = f"/home/claude/en/sql_video{V}_EN_{SLUG[V]}.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/silent.mp4", "-i", f"{OUT}/mix.wav", "-map", "0:v", "-map", "1:a",
    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "192k", "-shortest",
    "-movflags", "+faststart", final], check=True)
print("DONE", final, round(DUR, 1))

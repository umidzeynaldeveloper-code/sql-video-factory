"""A/B comparison of demo_old.mp4 (v2) and demo_new_final.mp4 (v2.1): stills, crops, smoothness, audio, A/B video."""
import sys, os, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audio as A
from scipy import signal

O = "/home/claude/v21out"; OLD = f"{O}/demo_old.mp4"; NEW = f"{O}/demo_new_final.mp4"; CMP = f"{O}/compare"; os.makedirs(CMP, exist_ok=True)
F = lambda s: ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", s)


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,sample_rate,bit_rate:format=duration,size",
                        "-of", "json", p], capture_output=True, text=True)
    return json.loads(r.stdout)


def grab(p, t, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", p, "-frames:v", "1", out], check=True); return Image.open(out)


def frames_gray(p, w=270, h=480):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)


def smooth(p):
    """frame-to-frame change: mean abs diff per frame; 'jumps' = frames whose change is > 4x the median of moving frames"""
    f = frames_gray(p); d = np.abs(np.diff(f, axis=0)).mean((1, 2)); mv = d[d > .05]
    med = float(np.median(mv)) if len(mv) else 0.0
    return dict(frames=len(f), moving_frames_pct=round(100 * len(mv) / len(d), 1), median_change=round(med, 3),
                jumps=int((d > 4 * med).sum()) if med else 0, p95_change=round(float(np.percentile(d, 95)), 3))


def resample_test():
    """24 kHz sweep (100 Hz .. 11.5 kHz) -> output rate; energy that should not exist above 12.5 kHz (imaging/aliasing)"""
    sr = 24000; t = np.arange(3 * sr) / sr; x = signal.chirp(t, 100, 3, 11500, method="log") * .5
    old = np.interp(np.arange(int(len(x) * 44100 / sr)) * sr / 44100, np.arange(len(x)), x)
    new = A.resample(x, sr, 48000)

    def bad_db(y, fs):
        f, P = signal.welch(y, fs, nperseg=8192); band = P[f > 12500].sum(); tot = P.sum()
        return round(10 * np.log10(band / tot + 1e-20), 1)
    return dict(v2_np_interp_44k1_dB=bad_db(old, 44100), v21_resample_poly_48k_dB=bad_db(new, 48000))


def label(im, s, col):
    d = ImageDraw.Draw(im); d.rounded_rectangle((20, 20, 40 + d.textlength(s, F(40)), 84), 20, fill=(0, 0, 0)); d.text((30, 26), s, font=F(40), fill=col); return im


if __name__ == "__main__":
    rep = dict(probe_old=probe(OLD), probe_new=probe(NEW))
    # stills at matching moments (the timelines differ slightly: voice-driven) -> use relative positions
    do = float(rep["probe_old"]["format"]["duration"]); dn = float(rep["probe_new"]["format"]["duration"])
    rels = [.13, .35, .52, .72, .93]; tiles = []
    for k, r in enumerate(rels):
        a = grab(OLD, r * do, f"{CMP}/old_{k}.png").resize((405, 720), Image.LANCZOS); b = grab(NEW, r * dn, f"{CMP}/new_{k}.png").resize((405, 720), Image.LANCZOS)
        tiles.append((a, b))
    sheet = Image.new("RGB", (405 * len(rels), 720 * 2 + 70), (0, 0, 0)); d = ImageDraw.Draw(sheet)
    for k, (a, b) in enumerate(tiles): sheet.paste(a, (k * 405, 0)); sheet.paste(b, (k * 405, 720 + 70))
    d.text((20, 724), "TOP: v2 (current)   BOTTOM: v2.1 prototype", font=F(36), fill=(255, 205, 70)); sheet.save(f"{CMP}/stills_ab.png")
    # 1:1 detail crops (anti-aliasing, extrusion, shadow)
    ca = Image.open(f"{CMP}/old_2.png").crop((120, 640, 620, 1040)); cb = Image.open(f"{CMP}/new_2.png").crop((120, 640, 620, 1040))
    crop = Image.new("RGB", (1000, 400)); crop.paste(ca, (0, 0)); crop.paste(cb, (500, 0))
    crop = crop.resize((2000, 800), Image.NEAREST); label(crop, "v2", (240, 244, 255)); ImageDraw.Draw(crop).text((1030, 26), "v2.1", font=F(40), fill=(52, 230, 140))
    crop.save(f"{CMP}/crop_2x.png")
    rep["smooth_old"] = smooth(OLD); rep["smooth_new"] = smooth(NEW)
    rep["loud_old"] = A.loudness(OLD); rep["loud_new"] = A.loudness(NEW)
    rep["resample_out_of_band"] = resample_test()
    json.dump(rep, open(f"{CMP}/report.json", "w"), indent=1); print(json.dumps({k: v for k, v in rep.items() if not k.startswith("probe")}, indent=1))
    # A/B video: v2 then v2.1, each with a label, original audio
    for src, lab, col, out in ((OLD, "BEFORE  v2", "white", "a.mp4"), (NEW, "AFTER  v2.1", "0x34E68C", "b.mp4")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf",
                        f"drawbox=x=40:y=1730:w=520:h=110:color=black@0.75:t=fill,drawtext=fontfile=/usr/share/fonts/opentype/inter/Inter-Bold.otf:text='{lab}':x=70:y=1752:fontsize=60:fontcolor={col}",
                        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", f"{CMP}/{out}"], check=True)
    open(f"{CMP}/ab.txt", "w").write(f"file '{CMP}/a.mp4'\nfile '{CMP}/b.mp4'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{CMP}/ab.txt", "-c", "copy", f"{O}/demo_AB_before_after.mp4"], check=True)
    print("ok")

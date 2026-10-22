import sys, sherpa_onnx, soundfile as sf
M = "/home/claude/tts_dl/n/package/kokoro-int8-en-v0_19"
cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=f"{M}/model.int8.onnx", voices=f"{M}/voices.bin",
        tokens=f"{M}/tokens.txt", data_dir=f"{M}/espeak-ng-data"), num_threads=4))
tts = sherpa_onnx.OfflineTts(cfg)
def say(text, out, sid=6, speed=1.0):
    a = tts.generate(text, sid=sid, speed=speed)
    sf.write(out, a.samples, a.sample_rate); return len(a.samples) / a.sample_rate
if __name__ == "__main__":
    for sid in (3, 6, 9):
        print(sid, say("You type S Q L. But the computer sees only zeros and ones. Let me show you why.", f"test_{sid}.wav", sid))

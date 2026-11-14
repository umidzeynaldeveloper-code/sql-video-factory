"""TTS (Kokoro v1.0 fp32) + ASR round-trip check (Whisper base.en) for the v2 engine."""
import os, re, sherpa_onnx, soundfile as sf, numpy as np
K10 = "/home/claude/tts2/kokoro-multi-lang-v1_0"; K19 = "/home/claude/tts2/kokoro-en-v0_19"
WB = "/home/claude/tts2/sherpa-onnx-whisper-base.en"
_tts = {}; _asr = None

def tts(model="k10"):
    if model not in _tts:
        if model == "k10":
            kc = sherpa_onnx.OfflineTtsKokoroModelConfig(model=f"{K10}/model.onnx", voices=f"{K10}/voices.bin", tokens=f"{K10}/tokens.txt",
                data_dir=f"{K10}/espeak-ng-data", dict_dir=f"{K10}/dict", lexicon=f"{K10}/lexicon-us-en.txt,{K10}/lexicon-zh.txt")
        elif model == "k19":
            kc = sherpa_onnx.OfflineTtsKokoroModelConfig(model=f"{K19}/model.onnx", voices=f"{K19}/voices.bin", tokens=f"{K19}/tokens.txt", data_dir=f"{K19}/espeak-ng-data")
        else:
            M = "/home/claude/tts_dl/n/package/kokoro-int8-en-v0_19"
            kc = sherpa_onnx.OfflineTtsKokoroModelConfig(model=f"{M}/model.int8.onnx", voices=f"{M}/voices.bin", tokens=f"{M}/tokens.txt", data_dir=f"{M}/espeak-ng-data")
        _tts[model] = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=kc, num_threads=2)))
    return _tts[model]

def say(text, out, sid=16, speed=1.0, model="k10"):
    a = tts(model).generate(text, sid=sid, speed=speed)
    x = np.array(a.samples, dtype=np.float32)
    sf.write(out, x, a.sample_rate); return len(x) / a.sample_rate

def asr(path):
    global _asr
    if _asr is None:
        _asr = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{WB}/base.en-encoder.onnx", decoder=f"{WB}/base.en-decoder.onnx",
                                                          tokens=f"{WB}/base.en-tokens.txt", num_threads=2)
    x, sr = sf.read(path, dtype="float32")
    if x.ndim > 1: x = x[:, 0]
    out = []
    step = 28 * sr
    for i in range(0, len(x), step):
        s = _asr.create_stream(); s.accept_waveform(sr, x[i:i + step]); _asr.decode_stream(s); out.append(s.result.text.strip())
    return " ".join(out)

def norm(s):
    s = s.lower().replace("-", " ")
    return re.sub(r"[^a-z0-9 ]", "", s).split()

def sim(a, b):
    import difflib
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()

"""voice21.py — TTS providers, SQL pronunciation dictionary and word timing for the v2.1 engine.

Kokoro (local, default) is unchanged: it calls v2/voice.say().
Google Cloud TTS is an optional provider interface only. It is never called unless a config asks for it,
and it refuses to run without the SDK and credentials (the workspace has neither, and its network blocks the API).
"""
import os, re, math, sys
import numpy as np

sys.path.insert(0, "/home/claude/v2")

# ------------------------------------------------------------------ pronunciation
# token -> how the voice should say it (display text stays unchanged)
PRON = {
    "SQL": "S Q L", "PL/SQL": "P L S Q L", "ID": "I D", "IDs": "I Ds", "DDL": "D D L", "DML": "D M L", "DCL": "D C L",
    "PGA": "P G A", "SGA": "S G A", "CPU": "C P U", "OK": "okay", "VS": "versus", "vs": "versus", "DB": "database",
    "ROWID": "row I D", "ROWIDs": "row I Ds", "VARCHAR2": "var char two", "NVL": "N V L", "NVL2": "N V L two",
    "CTE": "C T E", "JSON": "jay son", "XML": "X M L", "SYSDATE": "sys date", "SYSTIMESTAMP": "sys timestamp",
    "DBMS_OUTPUT": "D B M S output", "DBMS_SCHEDULER": "D B M S scheduler", "DBA": "D B A", "AWR": "A W R",
    "TO_CHAR": "to char", "TO_DATE": "to date", "TRUNC": "trunc", "B-tree": "B tree", "I/O": "I O", "IO": "I O",
    "UNDO": "undo", "REDO": "redo", "TEMP": "temp", "LRU": "L R U", "OLTP": "O L T P", "ETL": "E T L",
    "ACID": "acid", "API": "A P I", "UUID": "U U I D", "NULL": "null", "NULLs": "nulls", "ASC": "ascending", "DESC": "descending",
    "PK": "primary key", "FK": "foreign key", "CBO": "C B O", "SQL*Plus": "S Q L plus", "DBMS_XPLAN": "D B M S X plan", "DBMS_XPLAN.DISPLAY": "D B M S X plan dot display",
    "DISPLAY_CURSOR": "display cursor", "PLAN_TABLE": "plan table", "&": "and", "%": "percent",
}


def _ora(m):  # ORA-00979 -> "O R A, zero zero nine seven nine"
    digits = " ".join("zero one two three four five six seven eight nine".split()[int(c)] for c in m.group(1))
    return f"O R A {digits}"


def speak_token(tok):
    """spoken form of one display token (keeps trailing punctuation)"""
    m = re.match(r"^([(\"']*)(.*?)([.,:;!?)\"']*)$", tok); pre, core, post = m.groups()
    if not core: return tok
    if re.fullmatch(r"ORA-(\d{5})", core): core = re.sub(r"ORA-(\d{5})", _ora, core)
    elif core in PRON: core = PRON[core]
    elif re.fullmatch(r"[A-Z][A-Z0-9_/]*[A-Z0-9]", core): core = core.lower()
    core = core.replace("_", " ").replace("→", ", then").replace("=", " equals ")
    return f"{pre}{core}{post}".strip()


def spoken_tokens(display_tokens):
    """[(word, emph)] -> list of spoken strings, one per display token"""
    return [speak_token(w) for w, _ in display_tokens]


# ------------------------------------------------------------------ providers
class ProviderUnavailable(RuntimeError): pass


# ------------------------------------------------------------------ OOV patch lexicon (v2.1.1)
# sherpa-onnx Kokoro with a lexicon SKIPS every word that is not in lexicon-us-en.txt ("OOV word skipped"),
# and that lexicon lacks many inflected forms (wants, columns, expects, optimizer, Oracle's, here's ...).
# Fix: derive the missing form from its base word and write it to an extra lexicon that is loaded AFTER the
# original one (original entries always win). Words that cannot be derived are reported so the script is reworded.
K10 = "/home/claude/tts2/kokoro-multi-lang-v1_0"
EXTRA_LEX = "/home/claude/tts2/lexicon-extra-en.txt"
_BASE = None; _EXTRA = {}; _TTS = {"obj": None, "n": -1}
VOICELESS = set("ptkfθ"); SIBIL = set("szʃʒʧʤ")
MANUAL = {"gps": "ʤ ˌ i p ˌ i ˈ ɛ s"}


def _base():
    global _BASE
    if _BASE is None:
        _BASE = {}
        for ln in open(f"{K10}/lexicon-us-en.txt", encoding="utf-8"):
            w, _, ph = ln.rstrip("\n").partition(" ")
            if w and ph and w not in _BASE: _BASE[w] = ph
        if os.path.exists(EXTRA_LEX):
            for ln in open(EXTRA_LEX, encoding="utf-8"):
                w, _, ph = ln.rstrip("\n").partition(" ")
                if w and ph: _EXTRA.setdefault(w, ph)
    return _BASE


def _s(ph):  # plural / 3rd person / possessive ending
    last = ph.split()[-1]
    return ph + (" ᵻ z" if last in SIBIL else " s" if last in VOICELESS else " z")


def derive(w, depth=0):
    B = _base(); w = w.lower()
    if w in B: return B[w]
    if w in _EXTRA: return _EXTRA[w]
    if w in MANUAL: return MANUAL[w]
    look = lambda x: B.get(x) or _EXTRA.get(x) or MANUAL.get(x) or (derive(x, depth + 1) if depth < 1 and len(x) > 2 else None)
    if w.endswith("'s") and look(w[:-2]): return _s(look(w[:-2]))
    if w.endswith("s'") and look(w[:-2]): return _s(look(w[:-2]))
    if w.endswith("ies") and look(w[:-3] + "y"): return look(w[:-3] + "y")[:-1].rstrip() + " i z"
    if w.endswith("es") and look(w[:-2]) and w[-3] in "sxzh": return look(w[:-2]) + " ᵻ z"
    if w.endswith("s") and look(w[:-1]): return _s(look(w[:-1]))
    if w.endswith("ed"):
        b = look(w[:-2]) or look(w[:-1])
        if b: last = b.split()[-1]; return b + (" ᵻ d" if last in "td" else " t" if last in VOICELESS else " d")
    if w.endswith("er"):
        b = look(w[:-1]) or look(w[:-2])
        if b: return b + " ə ɹ"
    if w.endswith("ers"):
        b = look(w[:-2]) or look(w[:-3])
        if b: return b + " ə ɹ z"
    if w.endswith("ing"):
        b = look(w[:-3]) or look(w[:-3] + "e")
        if b: return b + " ɪ ŋ"
    return None


def patch_lexicon(text, log=print):
    """add derivable OOV words of `text` to the extra lexicon; returns list of words that stay unknown"""
    B = _base(); new = {}; unknown = []
    for raw in re.findall(r"[A-Za-z][A-Za-z']*", text):
        w = raw.strip("'").lower()
        if not w or w in B or w in _EXTRA or w in new: continue
        ph = derive(w)
        if ph: new[w] = ph
        else: unknown.append(raw)
    if new:
        _EXTRA.update(new)
        with open(EXTRA_LEX, "w", encoding="utf-8") as f:
            for w, ph in sorted(_EXTRA.items()): f.write(f"{w} {ph}\n")
    if unknown: log(f"[voice] OOV (will be SKIPPED by Kokoro, reword or add to MANUAL): {sorted(set(unknown))}")
    return unknown


def _tts21():
    import sherpa_onnx
    if _TTS["obj"] is None or _TTS["n"] != len(_EXTRA):
        lex = f"{K10}/lexicon-us-en.txt,{EXTRA_LEX},{K10}/lexicon-zh.txt" if _EXTRA else f"{K10}/lexicon-us-en.txt,{K10}/lexicon-zh.txt"
        kc = sherpa_onnx.OfflineTtsKokoroModelConfig(model=f"{K10}/model.onnx", voices=f"{K10}/voices.bin", tokens=f"{K10}/tokens.txt",
                                                     data_dir=f"{K10}/espeak-ng-data", dict_dir=f"{K10}/dict", lexicon=lex)
        _TTS["obj"] = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=kc, num_threads=2)))
        _TTS["n"] = len(_EXTRA)
    return _TTS["obj"]


class KokoroProvider:
    name = "kokoro"

    def __init__(self, sid=16, speed=0.9, model="k10", oov_patch=True):
        self.sid, self.speed, self.model, self.oov = sid, speed, model, oov_patch and model == "k10"

    def key(self):
        k = dict(p="kokoro", sid=self.sid, speed=self.speed, model=self.model)
        if self.oov: k["lex"] = "oov1"            # different audio than v2.1.0 -> separate cache entries
        return k

    def synth(self, text, wav):
        import soundfile as sf
        if not self.oov:
            from voice import say          # v2/voice.py, unchanged
            dur = say(text, wav, sid=self.sid, speed=self.speed, model=self.model)
            return dur, sf.info(wav).samplerate
        patch_lexicon(text)
        a = _tts21().generate(text, sid=self.sid, speed=self.speed)
        x = np.array(a.samples, dtype=np.float32); sf.write(wav, x, a.sample_rate)
        return len(x) / a.sample_rate, a.sample_rate


class GoogleTTSProvider:
    """Google Cloud Text-to-Speech (Chirp 3 HD voices or Gemini-TTS models).
    Interface only: requires `google-cloud-texttospeech`, credentials (ADC / GOOGLE_APPLICATION_CREDENTIALS)
    and network access to texttospeech.googleapis.com. NOT tested against the real API."""
    name = "google"

    def __init__(self, voice="en-US-Chirp3-HD-Charon", language="en-US", model=None, prompt=None, sample_rate=24000):
        self.voice, self.language, self.model, self.prompt, self.sr = voice, language, model, prompt, sample_rate
        try:
            from google.cloud import texttospeech  # noqa: F401
        except Exception as e:
            raise ProviderUnavailable("google-cloud-texttospeech is not installed") from e
        if not (os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or os.path.exists(os.path.expanduser("~/.config/gcloud/application_default_credentials.json"))):
            raise ProviderUnavailable("no Google credentials (GOOGLE_APPLICATION_CREDENTIALS / ADC) in this workspace")

    def key(self): return dict(p="google", voice=self.voice, model=self.model, prompt=self.prompt, sr=self.sr)

    def synth(self, text, wav):
        from google.cloud import texttospeech as tts
        import soundfile as sf
        client = tts.TextToSpeechClient()
        inp = tts.SynthesisInput(text=text, prompt=self.prompt) if self.prompt else tts.SynthesisInput(text=text)
        vp = dict(language_code=self.language, name=self.voice)
        if self.model: vp["model_name"] = self.model
        cfg = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16, sample_rate_hertz=self.sr)
        r = client.synthesize_speech(input=inp, voice=tts.VoiceSelectionParams(**vp), audio_config=cfg)
        pcm = np.frombuffer(r.audio_content[44:] if r.audio_content[:4] == b"RIFF" else r.audio_content, dtype="<i2").astype(np.float32) / 32768
        sf.write(wav, pcm, self.sr)
        return len(pcm) / self.sr, self.sr


def get_provider(cfg=None, log=print):
    """cfg: dict(provider='kokoro'|'google', fallback=True, ...). Google falls back to Kokoro when unavailable."""
    cfg = dict(cfg or {}); name = cfg.pop("provider", "kokoro"); fb = cfg.pop("fallback", True)
    if name == "google":
        try: return GoogleTTSProvider(**cfg)
        except ProviderUnavailable as e:
            if not fb: raise
            log(f"[voice] Google TTS unavailable ({e}) -> using Kokoro"); cfg = {}
    return KokoroProvider(**{k: v for k, v in cfg.items() if k in ("sid", "speed", "model")})


# ------------------------------------------------------------------ word timing (estimate)
def _syll(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee")): n -= 1
    return max(1, n)


def word_times(x, sr, words, min_gap=.07):
    """Estimated start/end (seconds) of each spoken word in a mono clip.
    Kokoro and the local Whisper model return no timestamps, so this splits the clip at real pauses
    (energy below threshold for >= min_gap) and spreads words over the speech segments by syllable weight."""
    x = np.asarray(x, np.float64); hop = int(sr * .01)
    m = len(x) // hop
    if m == 0 or not words: return [(0.0, len(x) / sr)] * len(words)
    rms = np.sqrt((x[:m * hop].reshape(m, hop) ** 2).mean(1)); thr = .08 * rms.max()
    sp = rms > thr; segs = []; i = 0
    while i < m:
        if sp[i]:
            j = i
            while j < m and (sp[j] or (j + int(min_gap / .01) < m and sp[j:j + int(min_gap / .01)].any())): j += 1
            segs.append((i * .01, j * .01)); i = j
        else: i += 1
    if not segs: segs = [(0.0, len(x) / sr)]
    wts = np.array([_syll(w) + .35 for w in words], float); cw = np.cumsum(wts) / wts.sum()
    sd = np.array([b - a for a, b in segs]); cs = np.cumsum(sd) / sd.sum()
    assign = [int(np.searchsorted(cs, c - wts[k] / wts.sum() / 2)) for k, c in enumerate(cw)]
    out = [None] * len(words)
    for si, (a, b) in enumerate(segs):
        idx = [k for k, s in enumerate(assign) if min(s, len(segs) - 1) == si]
        if not idx: continue
        tot = wts[idx].sum(); t = a
        for k in idx: d = (b - a) * wts[k] / tot; out[k] = (t, t + d); t += d
    last = (0.0, 0.0)
    for k in range(len(out)):
        if out[k] is None: out[k] = (last[1], last[1])
        last = out[k]
    return out

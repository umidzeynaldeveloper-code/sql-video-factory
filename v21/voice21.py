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
    "PK": "primary key", "FK": "foreign key", "CBO": "C B O", "SQL*Plus": "S Q L plus", "&": "and", "%": "percent",
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


class KokoroProvider:
    name = "kokoro"

    def __init__(self, sid=16, speed=0.9, model="k10"): self.sid, self.speed, self.model = sid, speed, model

    def key(self): return dict(p="kokoro", sid=self.sid, speed=self.speed, model=self.model)

    def synth(self, text, wav):
        from voice import say          # v2/voice.py, unchanged
        import soundfile as sf
        dur = say(text, wav, sid=self.sid, speed=self.speed, model=self.model)
        return dur, sf.info(wav).samplerate


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

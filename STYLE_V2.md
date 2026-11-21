# Video standard v2 (approved by the owner, 2026-11-15) ⭐

> Subordinate to [SQL_VIDEO_PRODUCTION_MASTER.md](SQL_VIDEO_PRODUCTION_MASTER.md). Still valid as the base layer; from video 57 the engine is v2.1 (`v21/engine.py`), publishing is direct (not Metricool) and needs no approval.

Video 51 is the reference ("51-ci video əladır, belə davam edə bilərik").
**Every new video — short or long — is made with the v2 engine (`v2/studio.py`) and follows every rule below.**
The old engine (`make_videoN.py` + `en/build.py`) is kept only for re-renders of videos 1–50.

## 1. Formats (always Full HD)
| Kind | Size | FPS | Length |
|---|---|---|---|
| Short (YouTube Shorts / Instagram Reel) | **1080 × 1920** (9:16) | 30 | ≤ 2:55 (`max_dur=175`) |
| Long video | **1920 × 1080** (16:9) | 30 | 5–10 min, chapters in the description |

## 2. Audience: someone with ZERO experience
- Every topic starts with an **everyday analogy** (box of receipts, coat-check ticket, pencil/pen/eraser, book index, restaurant…). The analogy maps to database words with `vs_panel` (REAL LIFE → DATABASE).
- Every new term gets a **NEW WORD card** (`term()`): the word + one plain sentence.
- One idea per sentence. Short, concrete sentences. Real numbers on screen (7 rows → 3 piles, 4.2 s vs 0.01 s).
- Always show the **classic mistake** + the exact ORA- error + the fix.
- Facts must be exact (versions, error codes, behaviour). Verify before writing.

## 3. Beat-synced narration (the core idea)
- A scene = `(title, colour, draw_fn, [beats…])`. **One beat = one sentence = one visual step.**
- The video timeline is built from the real TTS length of each sentence, so picture and voice are always in sync.
- `*word*` in a beat = emphasised (yellow, bold) in the subtitle; `{shown|spoken}` = different text on screen vs in the voice.
- Subtitles: karaoke style, words light up as they are spoken.
- Voice: Kokoro v1.0 fp32 (`tts2/kokoro-multi-lang-v1_0`), voice id 16 (am_michael), speed 0.9 (calm, ~150 wpm), EQ + gentle compression, music ducked under the voice, soft whoosh on scene change, tiny blip per step.
- `python3 videoNN.py check` = Whisper round-trip check of every sentence (fix words the voice says badly).

## 4. Lighting & visuals
- **Spotlight** (`g.focus(rects)`): what the voice talks about stays bright, everything else dims.
- `ring()` pulses on the current detail, `callout()` names a detail with a leader line, `badge()` numbers steps.
- Bloom + vignette + code-rain background, chapter dots and progress bar.
- Diagram-heavy: tables (`table`), code with syntax colours (`sql`), arrows/paths, piles, trees, cylinders, people, icons.
- Nothing may overlap the subtitle box; content stays above y ≈ 1380 (short) / 880 (long).

## 5. Structure of a short
1. Hook (problem/error/surprise, 2–3 beats)
2. Everyday analogy (3–4 beats)
3. 3–5 concept scenes, step by step
4. The classic mistake + fix
5. Recap (numbered list) + "Next video" + follow CTA

Long video: same building blocks, 10–12 chapters, pipeline/progress strip on top, recap + subscribe at the end.

## 6. Workflow
```
python3 v2/videoNN.py preview   # contact sheets → check every beat visually
python3 v2/videoNN.py check     # Whisper check of the voice
python3 v2/videoNN.py full      # render → /home/claude/en/sql_videoNN_EN_<slug>.mp4
```
Then: cover (`make_cover.py`), captions JSON (`sql-developer-videos/meta/capXXYY.json`), push to `sql-developer-videos`,
YouTube upload (cover, Education, not for kids, AI = yes, notify off, public, playlist), Instagram: directly on instagram.com in the owner's Chrome (no Metricool limit) — `sql-developer-videos/tools/pump.html` (opened via htmlpreview.github.io as a popup) streams the mp4/cover from GitHub into the composer, caption pasted with a synthetic paste event, crop Original, AI label off, Facebook share off ("Don't share this reel"), then Instagram's own **Schedule content**. Metricool only as a fallback (free plan = 20 posts/month).

## 7. Never
- Real work data of any kind (see README rule 0) — only generic names: `orders`, `customers`, `payments`, `accounts`, `APP`, `batch_pkg`, IPs from 192.0.2.x.
- `<` or `>` in descriptions/captions.
- Unexplained jargon, walls of text, or a step on screen that the voice is not talking about.

# SQL VIDEO PRODUCTION MASTER — single source of truth (v3.0, 2026-11-21)

Channel: Instagram **@sql_developer_no1** · YouTube **@UmidZeynalDeveloper** (channel `UCGt3BALyCUs48uXlcvxQWFQ`).
Owner: Umid. Talk to him **in Azerbaijani**. Video language: **English**.

This file is the only rulebook. Other docs keep details and are subordinate:
| Doc | Role now |
|---|---|
| `SQL_VIDEO_PRODUCTION_MASTER.md` (this) | rules, standards, pipeline, QA — **wins every conflict** |
| `HANDOFF.md` | current status + operational recipes (setup, YouTube/Instagram upload code) |
| `CONTENT_REGISTRY.md` | every video ever made + planned topics + production log |
| `STYLE_V2.md` | v2 visual standard (still valid as the base layer; §6 here extends it) |
| `README.md` | repo overview + caption/description templates (§2–3 there still valid) |
| `v21/RESULTS.md` | measured v2 vs v2.1 benchmark baseline |

Conflicts resolved in v3.0 (older text is superseded):
- "Ask the owner to approve topics before each batch" (README §4) → **removed**. Full autonomy, see §2.
- "privacy=private, owner publishes himself" (README §4) → **public** (practice since video 39).
- "Publish via Metricool" → **YouTube Studio + Instagram web directly**; Metricool only as fallback (free plan: 20 posts/month).
- "Every new video uses v2" (STYLE_V2) → **v2.1 engine (`v21/engine.py`) is the default from video 57**; v2 stays as fallback.

---

## 0. Start of every session (mandatory)
1. Read this file, then `HANDOFF.md` (status), then `CONTENT_REGISTRY.md`.
2. Read the private block list from Claude memory (`topics/confidential-work-data.md` in the "Sql developer" project) and write it, one regex per line, to `/home/claude/.sqlvf_blocklist` (never into a repo). `v21/qa.py` refuses to run without it.
3. `cd /home/claude/sql-video-factory && bash setup_v2.sh` (deps that the engine already uses + Kokoro/Whisper models; no new libraries).
4. Continue from "Next" in `HANDOFF.md` without asking.

## 1. Confidentiality ⛔ (highest priority, above autonomy)
- Nothing from the owner's real job may appear in any frame, narration, caption, title, cover, file name or repo: no real schema/package/procedure/table/column names, IPs, hosts, users, bank or system names, real numbers or code structure.
- Generic names only: schema `APP`, `batch_pkg`, `orders`, `customers`, `payments`, `accounts`; IPs `192.0.2.x` / `198.51.100.x` / `203.0.113.x`. Generic "end of day" is fine.
- Gate: `python3 v21/qa.py ...` greps script + captions against the private list. Any hit = stop, rename, re-render.
- Never store API keys, tokens or credentials in code, Markdown or git.

## 2. Autonomy (owner directive v3.0)
Do **without asking**: choose the topic, research, script, storyboard, voice, timeline, motion graphics, sound design, render, QA, cover/thumbnail, title, description, caption, publish (YouTube + Instagram, existing logged-in browser flow), update registry/HANDOFF, commit.
**Ask the owner only for**: a new paid service, a new credential/account permission, an architecture change that could break production, a security/confidentiality risk, or a technical blocker you cannot solve.
Autonomy never authorises: new paid services, new accounts, sharing secrets, or breaking the working pipeline.

## 3. Content strategy & topic selection
Pool: real SQL problems, Oracle internals, query optimisation, indexes & plans, joins & aggregation, transactions/locking/concurrency, PL/SQL, performance tuning, beginner mistakes, advanced SQL, architecture, real-world troubleshooting.
- Since video 51 the channel line is **beginner-first** (explain to someone with zero experience); alternate with practical/advanced topics when the beginner line has covered the basics of an area.
- Pick by audience value, not complexity: a great visual of a simple idea beats a complex topic.
- Check `CONTENT_REGISTRY.md`: no repeats unless the row states a clearly new angle.
- Write the chosen topic + angle into the registry before scripting.

## 4. Script & storytelling
- Hook in the first 2–3 s (a problem, an error, a surprising number) and say what problem the video solves.
- Structure (short): hook → everyday analogy (`vs_panel`: REAL LIFE → DATABASE) → 3–5 concept steps → classic mistake + exact ORA- error + fix → numbered recap → "next video" + follow CTA.
- Long video: 10–12 chapters, own 16:9 layout (never a stretched short), chapters in the description.
- Every new term gets a NEW WORD card (`term()`). One idea per sentence, short concrete sentences, real numbers on screen.
- **One beat = one sentence = one visual step.** Decide the visual while writing the sentence; never a step on screen the voice is not talking about.
- At least one concrete SQL example per video. No filler intros, no repetition. End with a precise, memorable takeaway.
- Length follows the topic: shorts ≤ 2:55 (`max_dur=175`), don't stretch simple topics.

## 5. Technical accuracy & SQL validation
1. Oracle only, never mix dialects (no `LIMIT`, `TOP`, `ISNULL`, backticks …). Mark version-dependent features (e.g. "12c+: FETCH FIRST", "11g+: PIVOT").
2. Optimizer behaviour is never a universal rule: say "usually / often / depends on statistics and data".
3. Simplified teaching models must be labelled as models, not presented as real execution traces.
4. Distinguish logical processing order from physical execution.
5. ORA- codes only in their real context; verify each code and message against Oracle documentation (web search) before use.
6. There is **no Oracle database in the workspace**: never claim code was executed. `v21/qa.py` runs a static SQL check (quotes/brackets balanced, statements terminated, known keywords, banned non-Oracle syntax); anything it flags is fixed before render. If a DB connection is ever available, execute the examples and record it in the log.
7. If validation fails, fix the script and the visuals before publishing.

## 6. Visual standard (v2.1+, GPU-free 2.5D motion graphics)
Stack: Python, Pillow, NumPy, SciPy, FFmpeg + `v2/studio.py` primitives + `v21/engine.py` (proxy drawing, so every v2 primitive works).
Available and to be used **with purpose** (clarity before decoration): anti-aliasing (supersampling), easing library (`EASE`), camera pan/zoom (`g.camera`), parallax background, soft shadows (automatic on filled cards), controlled glow (`g.glow`, halo), 2.5D tables (`table3d`) and cylinders (`cyl25`), animated SQL (`sql_exec`: typing, execution cursor, ✓), data flow (`flow`), B-tree traversal (`btree`), spotlight (`g.focus`), zoom transitions, karaoke subtitles with active-word highlight.
Mobile-first layout (1080×1920):
- Title zone y ≈ 180–290, handle/chapter dots y 90–160. Content y **300–1380**. Subtitle box ends at y 1668.
- Keep key text out of the right 120 px between y 900–1700 and out of y > 1680 (Reels/Shorts UI).
- Code ≥ 32 px (prefer 38–42 for the main query), table rows ≥ 58 px, max ~8 rows / 3 columns per table; split dense diagrams into scenes.
- Camera zoom ≤ ~1.1 when the scene has content near the top, so nothing slides under the title; fade out what leaves the frame.
- Subtitles, code and animation never overlap (check preview sheets).
Long 16:9: content y 200–880, subtitles at the bottom, chapter counter "k / n" top right.

## 7. Audio standard
- Voice: Kokoro v1.0 (sherpa-onnx, local), sid 16 (am_michael), speed 0.9 — consistent narrator. Pronunciation dictionary `v21/voice21.py: PRON` (+ ORA-code reader); extend it whenever the Whisper check mishears a term.
- Provider config: default `kokoro`; optional `google` (adapter in `voice21.py`); fallback kokoro. Google may be enabled only after a real connection + authentication + audible test succeed (today: no SDK, no credentials, host blocked by the workspace proxy).
- TTS cache key = provider + model + voice + speed + text (md5) — never reuse audio across providers.
- Word timing: Kokoro and local Whisper give **no** timestamps; subtitles use the estimate in `word_times()` (pause detection + syllables). Say so honestly; check sync by watching the preview.
- Resampling: polyphase (`audio.resample`, 24 kHz → 48 kHz).
- Sound design (`v21/audio.py`): whoosh, impact, sub_hit, riser, click, data, sweep (transition), atmos, success, error; scan = clicks/data during a scan. Attach effects to **visual events** via the SCENES 5th item `[(beat, delay, name, {params})]`, not to every sentence. Intensity follows meaning (success/impact for the payoff, error for the mistake). Voice always clearly on top.
- Mastering: 48 kHz stereo, voice EQ + compression + limiter, ducked music + atmos bed, two-pass loudnorm **−14 LUFS / −1.5 dBTP** (starting preset; check every video).

## 8. Engine, presets, performance
| Preset | Engine cfg | Use |
|---|---|---|
| FAST_PREVIEW | `PRESETS["preview"]` (ss 1, no shadows/glow/parallax, ultrafast) | layout/timing check, contact sheets |
| PRODUCTION | `PRESETS["final"]` (ss 2 supersampling, crf 18, medium) | every published video |
| HIGH_QUALITY | `final` + `preset=slow, crf=16` | special videos |
| 4K | `PRESETS["final4k"]` (scale 2 = native 2160×3840 layout) | only when it gives a real visible gain; **never upscale 1080p and call it 4K** |

Measured baseline (`v21/RESULTS.md`, 2 vCPU, no GPU): 17 s demo — v2 34.7 s, v2.1 PRODUCTION 115 s (0.35 s/frame/process; 1148 MB peak). A 2:30 short ≈ 15 min (estimate from per-frame time).
**Optimisation backlog** (do incrementally, benchmark each, never trade away visible quality): static layer caching (title/UI/background per scene), cached shadow & glow masks while the rect set is unchanged, selective supersampling (only the world layer), adaptive blur radius, avoid the second background render on fades, reuse font objects, NumPy composition for spotlight/vignette, preview at half resolution.

## 9. Production pipeline (every video, no approval gates)
1. **Topic** — registry check, write row (topic + angle).
2. **Research** — verify facts, versions, ORA- codes (web, Oracle docs).
3. **Script** — `v21/videoNN.py`: `SCENES = [(title, colour, fn, [beats], [events])]`.
4. **Storyboard** — in the scene fns: objects, motions, camera keys per beat.
5. **Voice** — automatic in `build21` (Kokoro, cached).
6. **Timeline** — automatic from real voice durations.
7. **Motion graphics** — `python3 v21/videoNN.py preview preview` → look at every `sheetN.png`; fix overlaps.
8. **Sound design** — events on visual moments.
9. **Render** — `python3 v21/videoNN.py check` (Whisper) → `python3 v21/videoNN.py full final` → `/home/claude/en/sql_videoNN_EN_<slug>.mp4`.
10. **QA** — §10, all gates green.
11. **Packaging** — cover (`make_cover.py`), long thumbnail (`make_thumb_longN.py`), title, YouTube description (starts "NN. ", no `<` `>`), Instagram caption (≤ 5 hashtags), metadata JSON in `sql-developer-videos/meta/`.
12. **Publish & registry** — push mp4/cover/meta to `sql-developer-videos`; YouTube (public, Education, not for kids, altered/AI content = yes, notify off, thumbnail, playlist) and Instagram the **same day** (Reel, cover, AI label off, Facebook off, scheduled natively); recipes in `HANDOFF.md`. Add the production-log row, update HANDOFF "Next", commit.

## 10. Quality gates (a video is not final until all pass)
Automated: `python3 v21/qa.py <final.mp4> --script v21/videoNN.py --meta <meta.json> --expect 1080x1920 --max 175`
- Technical: opens, resolution, constant 30 fps, H.264 + AAC stereo 48 kHz, duration in range, no decode errors to the end.
- Audio: integrated loudness −14 ± 1 LUFS, true peak ≤ −1.0 dBTP, no clipped samples.
- Text/meta: no `<` `>` in descriptions/captions, ≤ 5 IG hashtags, YouTube title without number, description starts with the number.
- Confidentiality: private block list grep on script + metadata = 0 hits.
- SQL static check on every SQL line found in the script.
Manual (Claude looks): preview sheets + 6 frames from the final (texts readable, nothing cut, no overlap with subtitles, transitions clean, no empty/too long scenes); Whisper check flags fixed; voice clearly above effects; sync by watching a few beats.
Fix → re-run → only then publish. Never present a failing video as final.

## 11. Registry & continuous improvement
After every video add to `CONTENT_REGISTRY.md` → production log: id, topic, engine, res/fps, duration, render time (`perf.json`), peak RAM, TTS provider, QA result, file names, publishing status, issues → fixes.
Recurring problems: find the cause, fix it in the engine (not per video), add it to this file. Improve the stable engine step by step; never rewrite the architecture inside a video job.

## 12. Compatibility, safety, regression
- Never modify the v1 engine (videos 1–50: `make_videoN.py`, `en/`), never delete published content or audio.
- `v2/` stays untouched; v2.1 builds on it. SCENES 4-tuples (v2) must keep working in v2.1.
- Engine changes go to a branch first (e.g. `v21-opt`), then regression:
  1. `python3 v21/compat_and_4k.py` — video51 SCENES under v2.1 (frames) + per-frame timing.
  2. `python3 v21/demo_new.py full final` + `python3 v21/compare.py` — compare with `v21/RESULTS.md` (render time, RAM, loudness, out-of-band resampling, stills).
  3. Look at the stills; merge only if quality is equal or better and nothing broke. Record new numbers in `RESULTS.md`.
- Rollback = `git revert` / switch back to the previous engine; v2 remains a working fallback.

## 13. How future sessions load these rules
- `CLAUDE.md` in this repo points here (loaded automatically when a session starts in the repo).
- Claude.ai Project "Sql developer" → doc `claude/START_HERE_sql_video_factory.md` (starter command + pointer).
- Claude memory (project) → `areas/sql-developer-channel.md` has the standing instruction to read this file first.
- Starter command for the owner: **"sql-video-factory reposundakı SQL_VIDEO_PRODUCTION_MASTER.md və HANDOFF.md-ni oxu, sonra növbəti videoya avtonom davam et."**

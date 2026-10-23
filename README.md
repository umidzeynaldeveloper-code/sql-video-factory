# SQL video factory

Renders the vertical (1080x1920) explainer videos for @sql_developer_no1 / @UmidZeynalDeveloper.

- `vhelp.py` — shared scene helpers for videos 17+ (base frame, recap, CTA, card lists, preview sheet)
- `make_videoN.py` — scene-by-scene frame renderer for video N (schematic style from 11+)
- `en/narration.py` — English narration per scene + original scene timings
- `en/build.py N full` — TTS (Kokoro via sherpa-onnx), scene retiming, music, ducking, loudnorm → `en/sql_videoN_EN_<slug>.mp4`
- `setup.sh` — prepares a fresh workspace

Rendered videos are pushed to the public repo `sql-developer-videos`; Metricool pulls them from raw.githubusercontent.com.

## Published / planned topics
1 binary · 2 UTF-8 bytes · 3 NULL · 4 COUNT · 5 index · 6 explain plan · 7 joins · 8 deadlock · 9 bind variables · 10 UNDO · 11 flashback · 12 partitioning · 13 parallel query · 14 materialized views · 15 optimizer statistics · 16 bind peeking · 17 SQL plan baselines · 18 redo & COMMIT (incl. UNDO vs REDO) · 19 result cache · 20 fragmentation & SHRINK

## Next topics
21 AWR in 3 minutes ✓ · 22 UNDO vs REDO deep-dive ✓ · 23 Datafiles vs log files ✓ · next: 24 latches & mutexes

Owner's backlog requests: (21–23 covered both)

## Publishing rule
Every YouTube upload: privacy=private, isAiGeneratedContent=true (YouTube AI disclosure), notifySubscribers=false, category EDUCATION. Number goes only in the description.

## Publishing rules (YouTube via Metricool)
- YouTube title = the short "Caption your Short" line (≤100 chars, ends with `#sql #oracle #shorts`).
- Description = `"<video number>. "` + the full detailed description (e.g. `16. The same SQL is fast...`).
- Post videos in numerical order; privacy as requested by the owner; madeForKids=false; isAiGeneratedContent=true; category EDUCATION.

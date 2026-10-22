# SQL video factory

Renders the vertical (1080x1920) explainer videos for @sql_developer_no1 / @UmidZeynalDeveloper.

- `make_videoN.py` — scene-by-scene frame renderer for video N (schematic style from 11+)
- `en/narration.py` — English narration per scene + original scene timings
- `en/build.py N full` — TTS (Kokoro via sherpa-onnx), scene retiming, music, ducking, loudnorm → `en/sql_videoN_EN_<slug>.mp4`
- `setup.sh` — prepares a fresh workspace

Rendered videos are pushed to the public repo `sql-developer-videos`; Metricool pulls them from raw.githubusercontent.com.

## Published / planned topics
1 binary · 2 UTF-8 bytes · 3 NULL · 4 COUNT · 5 index · 6 explain plan · 7 joins · 8 deadlock · 9 bind variables · 10 UNDO · 11 flashback · 12 partitioning · 13 parallel query · 14 materialized views · 15 optimizer statistics · 16 bind peeking

## Next topics
17 SQL plan baselines · 18 result cache · 19 table/index fragmentation & shrink · 20 redo & commit internals · 21 latches & mutexes · 22 AWR in 3 minutes

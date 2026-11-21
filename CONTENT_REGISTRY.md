# Content registry

One row per published or planned video. **Update this file in the same commit as every new video** (MASTER §11).
Before choosing a topic, search this table: a topic may repeat only with a clearly new angle (write the angle in the row).
Engine: v1 = `make_videoN.py` + `en/build.py` · v2 = `v2/studio.py` · v2.1 = `v21/engine.py`.

| # | Topic | Format | Engine | YouTube | Instagram |
|---|---|---|---|---|---|
| 1 | binary numbers | short 9:16 | v1 | published | published |
| 2 | UTF-8 bytes | short 9:16 | v1 | published | published |
| 3 | NULL | short 9:16 | v1 | published | published |
| 4 | COUNT | short 9:16 | v1 | published | published |
| 5 | index basics | short 9:16 | v1 | published | published |
| 6 | explain plan | short 9:16 | v1 | published | published |
| 7 | joins | short 9:16 | v1 | published | published |
| 8 | deadlock | short 9:16 | v1 | published | published |
| 9 | bind variables | short 9:16 | v1 | published | published |
| 10 | UNDO | short 9:16 | v1 | published | published |
| 11 | flashback | short 9:16 | v1 | published | published |
| 12 | partitioning | short 9:16 | v1 | published | published |
| 13 | parallel query | short 9:16 | v1 | published | published |
| 14 | materialized views | short 9:16 | v1 | published | published |
| 15 | optimizer statistics | short 9:16 | v1 | published | published |
| 16 | bind peeking | short 9:16 | v1 | published | published |
| 17 | SQL plan baselines | short 9:16 | v1 | published | published |
| 18 | redo & COMMIT | short 9:16 | v1 | published | published |
| 19 | result cache | short 9:16 | v1 | published | published |
| 20 | fragmentation & SHRINK | short 9:16 | v1 | published | published |
| 21 | AWR in 3 minutes | short 9:16 | v1 | published | published |
| 22 | UNDO vs REDO deep-dive | short 9:16 | v1 | published | published |
| 23 | datafiles vs log files | short 9:16 | v1 | published | published |
| 24 | latches & mutexes | short 9:16 | v1 | published | published |
| 25 | locks & enqueues | short 9:16 | v1 | published | published |
| 26 | shared pool & hard parse | short 9:16 | v1 | published | published |
| 27 | buffer cache | short 9:16 | v1 | published | published |
| 28 | indexes deep-dive | short 9:16 | v1 | published | published |
| 29 | reading execution plans | short 9:16 | v1 | published | published |
| 30 | SQL hints | short 9:16 | v1 | published | published |
| 31 | BULK COLLECT & FORALL | short 9:16 | v1 | published | published |
| 32 | PGA, sorts & TEMP | short 9:16 | v1 | published | published |
| 33 | analytic functions | short 9:16 | v1 | published | published |
| 34 | MERGE | short 9:16 | v1 | published | published |
| 35 | exception handling | short 9:16 | v1 | published | published |
| 36 | package state & ORA-04068 | short 9:16 | v1 | published | published |
| 37 | dynamic SQL & injection | short 9:16 | v1 | published | published |
| 38 | DBMS_SCHEDULER | short 9:16 | v1 | published | published |
| 39 | sequences & identity | short 9:16 | v1 | published | published |
| 40 | pagination | short 9:16 | v1 | published | published |
| 41 | mutating table | short 9:16 | v1 | published | published |
| 42 | collections | short 9:16 | v1 | published | published |
| 43 | temporary tables | short 9:16 | v1 | published | published |
| 44 | pipelined functions | short 9:16 | v1 | published | scheduled (Metricool, Nov 16-19) |
| 45 | isolation levels | short 9:16 | v1 | published | scheduled (Metricool, Nov 16-19) |
| 46 | FOR UPDATE SKIP LOCKED | short 9:16 | v1 | published | scheduled (Metricool, Nov 16-19) |
| 47 | DATE & TIMESTAMP traps | short 9:16 | v1 | published | scheduled (Metricool, Nov 16-19) |
| 48 | hierarchical queries | short 9:16 | v1 | published | scheduled (IG native, Nov 16-22) |
| 49 | constraints & unindexed FK | short 9:16 | v1 | published | scheduled (IG native, Nov 16-22) |
| 50 | PIVOT / UNPIVOT | short 9:16 | v1 | published | scheduled (IG native, Nov 16-22) |
| 51 | real order of SELECT | short 9:16 | v2 | published | scheduled (IG native, Nov 16-22) |
| 52 | GROUP BY & ORA-00979 | short 9:16 | v2 | published | scheduled (IG native, Nov 16-22) |
| 53 | JOIN from zero | short 9:16 | v2 | published | scheduled (IG native, Nov 16-22) |
| 54 | subqueries & NOT IN NULL trap | short 9:16 | v2 | published | scheduled (IG native, Nov 16-22) |
| 55 | COMMIT / ROLLBACK | short 9:16 | v2 | published | scheduled (IG native, Nov 16-22) |
| 56 | indexes from zero | short 9:16 | v2 | published | scheduled (IG native, Nov 16-22) |
| 57 | execution plans from zero (beginner angle; 6 & 29 were advanced) | short 9:16 | v2.1 | published (youtube.com/shorts/8ASy_q1y8k4) | **pending** — instagram.com blocked on the network used 2026-11-21 |
| long1 | Oracle query tuning guide | long 16:9 | v1 | published (youtu.be/4wCKJUGmJkI) | — |
| long2 | row-by-row → set-based PL/SQL (52× faster) | long 16:9 | v1 | published (youtu.be/PsdrJkilqTY) | — |
| long3 | how a SELECT runs (parse → optimize → execute → fetch) | long 16:9 | v2 | published (youtu.be/y4A-vURIPH4) | — |

## Planned / ideas (not yet made)
| # | Topic | Angle |
|---|---|---|
| long4 | (choose) | 10–12 chapters, own 16:9 layout |
| 58 | NULL logic in WHERE / three-valued logic | beginner (announced at the end of 57) |
| — | CASE expressions | beginner |
| — | window functions from zero (ROW_NUMBER, RANK) | beginner angle (33 was advanced) |
| — | LIKE, wildcards and why leading % kills an index | beginner + performance |
| — | INSERT / UPDATE / DELETE basics | beginner |
| — | views | beginner |
| — | PL/SQL block basics, cursors | beginner |

## Production log (v2.1+): one entry per video
| # | Date | Engine | Res/FPS | Duration | Render time | Peak RAM | TTS | QA | Files | Issues → fixes |
|---|---|---|---|---|---|---|---|---|---|---|
| demo | 2026-11-21 | v2.1 final | 1080×1920/30 | 17.1 s | 115 s (cold TTS) | 1148 MB | Kokoro sid16 0.9 | passed (A/B) | v21out/demo_new_final.mp4 | glow washed out highlighted row → halo glow; camera zoom hid title → zoom ≤1.08 |
| 57 | 2026-11-21 | v2.1.1 final | 1080×1920/30 | 173.9 s | 907 s video + 21 s audio (5216 frames, 0.35 s/frame/proc) | 1369 MB | Kokoro sid16 0.9 + OOV patch | all gates passed (−14.03 LUFS, −1.24 dBTP) | sql_video57_EN_execution_plans.mp4, covers/cover57.jpg, meta/cap5762.json | Kokoro silently SKIPPED words missing from lexicon-us-en (wants, columns, expects, optimizer, Oracle's…) → engine fix v2.1.1 `voice21.patch_lexicon` derives inflected forms; callout lines crossed table rows → pills under columns; camera pan pushed code under title → removed |

# SQL video factory

> ⚠️ **Read the "Quality rules" section before making ANY video.** These are the owner's standing rules. They apply to every video, the 1st and the 50th alike. Quality must never drop over time.

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
21 AWR in 3 minutes ✓ · 22 UNDO vs REDO deep-dive ✓ · 23 Datafiles vs log files ✓ · 24 latches & mutexes ✓ · 25 locks & enqueues ✓ · 26 shared pool & hard parse ✓ · 27 buffer cache ✓ · 28 indexes deep-dive ✓ · 29 reading execution plans ✓ · 30 SQL hints ✓ · 31 BULK COLLECT & FORALL ✓ · 32 PGA, sorts & TEMP ✓ · 33 analytic functions ✓ · 34 MERGE ✓ · 35 exception handling ✓ · next: 36 package state & ORA-04068 (needs approval)

Owner's backlog requests: (21–23 covered both)

## Quality rules (owner's standing requirements) ⚠️

These rules apply to EVERY video, caption and description. Never simplify or "clean up" an established good format on your own. If a format is changed, it must get better, not plainer.

### 1. Videos: schematic, diagrams, motion
- Every scene is a **diagram**: boxes, arrows, flows, timelines, graphs, tables. No scene that is just text.
- **Motion in every scene**: elements appear step by step, data flows along arrows, bars grow, counters change.
- Show the **mechanism** (how it works inside Oracle), not just a definition.
- Concrete, realistic examples (banking: accounts, balances, EOD, fx rates).
- Check the preview sheet for overlaps and clipped text before rendering. Facts must be technically correct.

### 2. Instagram caption: rich, eye-catching, with fitting emoji
Template (the style of videos 1–16 and the rewritten 18–23):
```
<Hook line with a number/contrast> <emoji>
<Second hook line / the question> <emoji>

<emoji> point 1: short, concrete
<emoji> point 2
   → sub-point (use arrows for lists)
<emoji> ... 6–10 points, each with a FITTING emoji (📍🔎🗑️⚡🧹📦🗓️🕵️ etc.)

<One-line takeaway> <emoji>

<Question to the audience>? 👇
Follow @sql_developer_no1 for more Oracle internals explained visually 🚀

#oracle #sql #... (max 5 hashtags: Instagram limit)
```

### 3. YouTube description: same rich style, readable, schematic
- Description = `"<N>. "` + the same structure as the Instagram caption (hook, emoji-bulleted points, takeaway, question 👇, follow line).
- Short lines, one idea per line, arrows (→) for flows and sub-lists. Easy to scan on a phone.
- Hashtags at the end, finishing with `#shorts`.
- Never a plain "Inside this episode: - item - item" list.
- **No `<` or `>` characters** in the description (YouTube rejects it: "invalid video description"). Write `=>` as words, e.g. "with format 'ALLSTATS LAST'". Use → arrows instead.

### 4. Publishing (YouTube via Metricool)
- YouTube title = short caption line (≤100 chars, ends with `#sql #oracle #shorts`). **No number in the title.**
- Description starts with `<N>. `
- `privacy=private` (the owner reviews and publishes himself), `type=short`, `madeForKids=false`, `category=EDUCATION`
- **`isAiGeneratedContent=true` on EVERY upload** (YouTube AI disclosure, protects the channel). If any uploaded video is missing it, tell the owner.
- `notifySubscribers=false`
- Post in numerical order. Ask the owner to approve topics before each new batch.
- English voiceover and text only.

### 4b. Instagram (connected to Metricool since 2026-10-29)
- Post every video ALSO as an Instagram Reel: `providers=[instagram]`, `instagramData={type: REEL, showReelOnFeed: true, isAiGenerated: false}` (owner: NO "AI info" label on Instagram; the AI label rule is for YouTube only).
- Caption = the Instagram caption (no number), max 5 hashtags. Instagram has no private mode, so it's public immediately.
- **Every Reel gets a custom cover** (`make_cover.py N` → `covers/coverN.jpg` in sql-developer-videos, sent as `videoThumbnailUrl`). Big title + episode number + hook line, key content inside the centre 3:4 area so the profile grid looks attractive. Never rely on the first frame.
- Owner posted 1–23 himself; 24–35 were scheduled by Claude on 2026-10-29.

### 5. Before delivering, check:
- [ ] Every scene is a moving diagram, no text-only scenes, no overlaps
- [ ] Caption and description follow the templates above (emoji bullets, hook, question 👇)
- [ ] Description starts with the number, title has no number
- [ ] Description has no `<` or `>` (grep before posting)
- [ ] Private + AI label set in Metricool

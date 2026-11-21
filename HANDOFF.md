# HANDOFF — read this first in every new chat

Starter prompt for the owner: **"sql-video-factory reposundakı SQL_VIDEO_PRODUCTION_MASTER.md və HANDOFF.md-ni oxu, sonra növbəti videoya avtonom davam et."**

Then Claude: read **`SQL_VIDEO_PRODUCTION_MASTER.md` (rules, wins every conflict)** → this file (status + recipes) → `CONTENT_REGISTRY.md`; write `~/.sqlvf_blocklist` from memory; run `bash setup_v2.sh`; continue from "Next" without asking for approval.
Talk to the owner **in Azerbaijani**. Work nonstop; ask only when something can't be undone.

---

## 1. Who / what
- Owner: Umid, PL/SQL developer. Channels: Instagram **@sql_developer_no1**, YouTube **@UmidZeynalDeveloper** (channel id `UCGt3BALyCUs48uXlcvxQWFQ`).
- Product: English Oracle/SQL explainer videos, Shorts/Reels (1080×1920, ≤2:55) + long videos (1920×1080, 5–10 min).
- Video 51 is the approved reference ("51-ci video əladır"). Every new video = v2 engine + `STYLE_V2.md`.

## 2. ⛔ Confidentiality (highest priority)
Nothing from the owner's real job may appear in frames, narration, captions, titles, covers, file names or this repo.
- The private block list lives in Claude memory (`topics/confidential-work-data.md` in the "Sql developer" project). Read it at the start.
- Use only generic names: schema `APP`, `batch_pkg`, `orders`, `customers`, `payments`, `accounts`; IPs only `192.0.2.x`. Generic "end of day" / `batch_pkg.run_day` is OK.
- Before every render and every publish: grep scripts + captions against the private list (must return nothing) and look at the preview sheets.

## 3. Status (2026-11-21, after v3.0 directive)
| | YouTube | Instagram |
|---|---|---|
| 1–47 | published | published / Metricool (44–47 at 20:00 on Nov 16–19) |
| 48–56 | published, in playlists | scheduled natively on IG: 48 Nov16 13:00 · 49 Nov17 · 50 Nov18 · 51 Nov19 · 52 Nov20 13:00 · 53 Nov20 20:00 · 54 Nov21 13:00 · 55 Nov21 20:00 · 56 Nov22 13:00 |
| long1–3 | published (long3 = youtu.be/y4A-vURIPH4) | — (long videos are YouTube only) |

- Metricool copies of 48–56 (Dec 1–9) were switched to **draft** to avoid duplicates. Don't re-enable them.
- Pinned comments on YouTube: blocked until the channel's phone verification is done.

## 4. Next
Engine for new videos: **v2.1** (`v21/engine.py`, PRODUCTION preset), scripts as `v21/videoNN.py` (copy the structure of `v21/demo_new.py`), QA with `v21/qa.py`. Topic list + production log: `CONTENT_REGISTRY.md`.
1. **57 — execution plans from zero** (v2, beginner-first: analogy → plan as a tree, read bottom-up/inside-out, rows/cost, FULL vs INDEX RANGE SCAN, classic mistake).
2. **long4** (16:9, 10–12 chapters).
3. Then continue beginner-first topics (ideas: NULL logic, CASE, window functions, LIKE & wildcards, INSERT/UPDATE/DELETE basics, views, sequences basics, PL/SQL block basics, cursors, exceptions basics).
After each video: publish to **both** YouTube and Instagram the same day, so Instagram never falls behind.
After every 5–6 videos: update this file (status + next), commit, and tell the owner to start a new chat.

## 5. Setup in a fresh workspace
```
cd /home/claude && git clone https://github.com/umidzeynaldeveloper-code/sql-video-factory   # if missing
cd sql-video-factory && bash setup_v2.sh
```
Gives: `/home/claude/v2/*` (engine + scripts), Kokoro multi-lang v1.0 + Whisper base.en in `/home/claude/tts2`, `make_cover.py`, and the public repo `/home/claude/sql-developer-videos`.

## 6. Make a video
> v2.1 (default from 57): same SCENES format + optional 5th item (sound events); run `python3 v21/videoNN.py preview preview` → `check` → `full final`, then `python3 v21/qa.py <mp4> --script … --meta …`. The v2 steps below remain valid for the v2 fallback.
1. Copy the nearest script (e.g. `v2/video56.py`) to `v2/video57.py`. Format:
   `SCENES = [(title, colour, draw_fn, [beats…]), …]` → `run(SCENES, Stage(1080,1920,30), "/home/claude/v2/out57", "/home/claude/en/sql_video57_EN_<slug>.mp4", mode, seed=57, max_dur=175)`.
   Long: `Stage(1920,1080,30)`, no max_dur limit, output `/home/claude/v2/long4_<slug>.mp4`.
2. `python3 /home/claude/v2/video57.py preview` → check `out57/sheetN.png` (no overlaps, nothing below y≈1380 short / 880 long).
3. `python3 … check` → Whisper round-trip, fix words the voice says badly.
4. `python3 … full` → render. Check duration ≤ 2:55.
5. Cover: add an entry to `COVERS` in `make_cover.py` (e.g. `57: "EXPLAIN\nPLANS"`) → `sql-developer-videos/covers/cover57.jpg`. Long video thumbnail: script like `make_thumb_long3.py` → `thumbs/long4.jpg`.
6. Captions: add `"57": {"title", "yt", "ig"}` to a `sql-developer-videos/meta/capXXYY.json`.
   - YouTube title without a number; description starts with "57. ". Instagram: rich emoji style (see README template), max 5 hashtags. Never `<` or `>`.
7. Push the mp4 + cover + meta to `sql-developer-videos`; push scripts to `sql-video-factory/v2/`.

## 7. Publish — YouTube (Chrome, owner's browser)
Settings every time: Education · not made for kids · altered/AI content = **Yes** · notify subscribers **off** · Public · custom thumbnail · add to playlist.
Flow (split into separate JS calls to avoid timeouts; use a fresh foreground tab):
1. Go to `studio.youtube.com/channel/UCGt3BALyCUs48uXlcvxQWFQ/videos/upload?d=ud`.
2. JS: fetch the raw GitHub mp4 → `new File([...])` → DataTransfer into `input[type=file]`, dispatch `change`. Wait ~8 s.
3. JS: fill title/description (focus the textbox, `execCommand('selectAll')` + `insertText`), set the radios, uncheck notify, put the cover into the thumbnail image input. Only treat it as blocked if the **visible dialog** says "one-time verif|verification needed" (descriptions may contain "Verify").
4. JS: `#next-button` ×3 → `[name=PUBLIC]` → `#done-button` → "Publish anyway" if shown → read the video link.
5. Playlist: on `/videos/short`, select rows matching `#shorts N. ` and use "Add to playlist".

## 8. Publish — Instagram (Chrome, instagram.com, no Metricool limit)
Instagram's CSP blocks fetch, so the file comes in through a popup:
- `sql-developer-videos/tools/pump.html`, opened via `https://htmlpreview.github.io/?https://github.com/umidzeynaldeveloper-code/sql-developer-videos/blob/main/tools/pump.html` as a popup whose **window name = repo-relative path** (e.g. `sql_video57_EN_x.mp4` or `covers/cover57.jpg`). It fetches from raw.githubusercontent and `postMessage`s `{kind:'reel', name, blob}` to the opener.
- The popup must be opened by a **real click**, so inject a button once per page load:
```js
window.addEventListener('message',e=>{if(e.data&&e.data.kind==='reel')window.__got=e.data});
const b=document.createElement('button');b.id='__opener';b.textContent='FETCH';
b.style='position:fixed;top:6px;left:50%;z-index:99999;background:#0f0;padding:10px';
b.onclick=()=>window.open('https://htmlpreview.github.io/?https://github.com/umidzeynaldeveloper-code/sql-developer-videos/blob/main/tools/pump.html',window.__F,'width=300,height=200');
document.body.appendChild(b);
```
- Helpers (inject once):
```js
window.__inj=(n,kind)=>{const g=window.__got;const ins=[...document.querySelectorAll('input[type=file]')];
 const input=kind==='v'?ins[ins.length-1]:ins.find(i=>/image/.test(i.accept)&&!/video/.test(i.accept));
 const f=new File([g.blob],kind==='v'?'reel'+n+'.mp4':'cover'+n+'.jpg',{type:kind==='v'?'video/mp4':'image/jpeg'});
 const dt=new DataTransfer();dt.items.add(f);input.files=dt.files;input.dispatchEvent(new Event('change',{bubbles:true}))};
window.__paste=txt=>{const ed=document.querySelector('div[role=dialog] div[contenteditable=true]');ed.focus();
 const dt=new DataTransfer();dt.setData('text/plain',txt);
 ed.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}))}; // keeps newlines
window.__sched=()=>{const i=[...document.querySelectorAll('div[role=dialog] input[type=checkbox]')];if(!i[1].checked)i[1].click()};
window.__fb=()=>{const i=[...document.querySelectorAll('div[role=dialog] input[type=checkbox]')];const l=i[i.length-1];if(l.checked)l.click()};
```
- Per reel: `__F`=video file → click FETCH (wait ~9 s) → Create → Post → `__inj(n,'v')` → crop icon → **Original** → Next → `__F`=`covers/coverN.jpg` → FETCH → `__inj(n,'c')` → Next → `__paste(caption)` → click empty panel area (closes hashtag popup) → `__sched()` → `__fb()` → dialog "Stop sharing to Facebook?" → **Don't share this reel** → date picker → day → Hours/Minutes/AM-PM spinbuttons (find refs, type values) → Schedule → wait ~30 s for "Your reel has been scheduled."
- AI label stays **off**. Times are Asia/Baku. Default slot: 20:00; catch-up slots 13:00.

## 9. Metricool (fallback only)
- blogId `7589850`, timezone `Asia/Baku`, free plan = 20 published posts/month (November is full).
- No delete tool: to cancel, `updateScheduledPost` with the full original content and `draft: true`.

## 10. Where things are
- `sql-video-factory` (this repo): `v2/` engine + scripts, `STYLE_V2.md`, `make_cover.py`, old engine (`make_videoN.py`, `en/`) for re-renders of 1–50.
- `sql-developer-videos` (public): rendered mp4s, `covers/`, `thumbs/`, `meta/` captions, `tools/pump.html`.

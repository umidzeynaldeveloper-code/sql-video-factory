# SQL Video Factory — instructions for Claude

**Before any video work, read `SQL_VIDEO_PRODUCTION_MASTER.md` (the single source of truth), then `HANDOFF.md` (status, recipes) and `CONTENT_REGISTRY.md` (what was already made).**

- Talk to the owner in Azerbaijani; videos are in English.
- Work autonomously (MASTER §2): pick the topic, script, render, QA, publish, update the registry — no approval gates.
- Confidentiality first (MASTER §1): private block list lives in Claude memory → `~/.sqlvf_blocklist`, never in git.
- Default engine: `v21/engine.py` (PRODUCTION preset). Never touch the v1 engine (videos 1–50) or `v2/`.

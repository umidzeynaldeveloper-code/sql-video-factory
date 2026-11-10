"""Long-form 16:9 video: Why is my Oracle query slow? A step-by-step tuning guide."""
import sys, os, json, math, random, subprocess
sys.path.insert(0, "/home/claude"); sys.path.insert(0, "/home/claude/en")
from common import SB, SN, MN, MB, BG, WHITE, DIM, GREEN, CYAN, YEL, PINK, RED, CARD, OFFB, PURP, mix, pr
from PIL import Image, ImageDraw

W, H, FPS = 1920, 1080, 24
OUT = "/home/claude/long1/out"; os.makedirs(OUT, exist_ok=True)

random.seed(5)
RAIN = Image.new("RGB", (W, H * 2), BG); _rd = ImageDraw.Draw(RAIN)
for x in range(16, W, 44):
    for y in range(0, H * 2, 42):
        if random.random() < .5:
            _rd.text((x, y), random.choice("01"), font=MN(26), fill=random.choice([(20, 30, 52), (24, 38, 64), (18, 27, 46)]))


def r(p, a, b):
    return pr(p, a, b)


def ctx(d, y, s, f, c, a=1.0, cx=W / 2):
    w = d.textlength(s, font=f); d.text((cx - w / 2, y), s, font=f, fill=mix(c, a))


def wraptxt(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines


def box(d, b, col, a, title=None, sub=None, tfs=36, sfs=28):
    x0, y0, x1, y1 = b
    if a <= 0: return
    for k, f in enumerate((.10, .20)):
        g = 10 - k * 5
        d.rounded_rectangle((x0 - g, y0 - g, x1 + g, y1 + g), 24 + g, outline=mix(col, a * f), width=3)
    d.rounded_rectangle(b, 22, fill=mix(CARD, a), outline=mix(col, a), width=3)
    cx = (x0 + x1) / 2
    if title and sub:
        ctx(d, (y0 + y1) / 2 - tfs - 2, title, SB(tfs), col, a, cx); ctx(d, (y0 + y1) / 2 + 6, sub, SN(sfs), WHITE, a, cx)
    elif title:
        ctx(d, (y0 + y1) / 2 - tfs * .62, title, SB(tfs), col, a, cx)


def code(d, x, y, lines, a, fs=30, w=None):
    if a <= 0: return
    f = MB(fs); lh = int(fs * 1.45)
    ww = w or max(d.textlength(s, font=f) for s, _ in lines) + 60
    d.rounded_rectangle((x, y, x + ww, y + len(lines) * lh + 34), 16, fill=mix((14, 20, 38), a), outline=mix(OFFB, a), width=2)
    for k, (s, c) in enumerate(lines):
        d.text((x + 30, y + 17 + k * lh), s, font=f, fill=mix(c, a))


def arrow(d, p0, p1, col, a, width=5):
    if a <= 0: return
    d.line((*p0, *p1), fill=mix(col, a), width=width)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]); L = 18
    d.polygon([p1, (p1[0] - L * math.cos(ang - .45), p1[1] - L * math.sin(ang - .45)),
               (p1[0] - L * math.cos(ang + .45), p1[1] - L * math.sin(ang + .45))], fill=mix(col, a))


def hbar(d, x, y, w, h, p, col, a, label=None, val=None):
    if a <= 0: return
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=mix(OFFB, a))
    if p > 0: d.rounded_rectangle((x, y, x + max(h, w * p), y + h), h // 2, fill=mix(col, a))
    if label: d.text((x, y - 44), label, font=SB(30), fill=mix(WHITE, a))
    if val: d.text((x + w - d.textlength(val, font=MB(30)), y - 44), val, font=MB(30), fill=mix(col, a))


def items(d, x, y, rows, p, step=74, fs=34, w=1500):
    for k, (s, col, st) in enumerate(rows):
        al = r(p, st, st + .08)
        if al <= 0: continue
        d.rounded_rectangle((x, y + k * step, x + w, y + k * step + step - 14), 14, fill=mix(CARD, al))
        d.text((x + 28, y + k * step + 12), s, font=SN(fs), fill=mix(col, al))


# ---------- execution plans ----------
COLS = [("Id", 70), ("Operation", 640), ("Name", 230), ("Starts", 150), ("E-Rows", 150), ("A-Rows", 150), ("A-Time", 190), ("Buffers", 160)]
BAD = [("0", "SELECT STATEMENT", "", "1", "", "12", "00:40:12", "9.8M"),
       ("1", " HASH GROUP BY", "", "1", "12", "12", "00:40:12", "9.8M"),
       ("2", "  NESTED LOOPS", "", "1", "40", "4.1M", "00:40:10", "9.8M"),
       ("3", "   TABLE ACCESS FULL", "ACCOUNTS", "1", "10", "970K", "00:00:01", "12K"),
       ("4", "   TABLE ACCESS BY INDEX ROWID", "PAYMENTS", "970K", "4", "4.1M", "00:39:55", "9.7M"),
       ("5", "    INDEX RANGE SCAN", "PAY_ACC_IX", "970K", "4", "4.1M", "00:21:30", "3.1M")]
GOOD = [("0", "SELECT STATEMENT", "", "1", "", "12", "00:00:02.1", "85K"),
        ("1", " HASH GROUP BY", "", "1", "12", "12", "00:00:02.1", "85K"),
        ("2", "  HASH JOIN", "", "1", "4.0M", "4.1M", "00:00:01.8", "85K"),
        ("3", "   TABLE ACCESS FULL", "ACCOUNTS", "1", "968K", "970K", "00:00:00.3", "12K"),
        ("4", "   PARTITION RANGE SINGLE", "", "1", "4.2M", "4.1M", "00:00:00.9", "73K"),
        ("5", "    TABLE ACCESS FULL", "PAYMENTS", "1", "4.2M", "4.1M", "00:00:00.9", "73K")]


def plan(d, x, y, rows, a, hl_rows=(), hl_cells=(), dim_rows=(), fs=24, rowp=None):
    if a <= 0: return
    tw = sum(w for _, w in COLS); rh = 52
    d.rounded_rectangle((x - 16, y - 12, x + tw + 16, y + rh * (len(rows) + 1) + 8), 16, fill=mix((14, 20, 38), a), outline=mix(OFFB, a), width=2)
    cx = x
    for name, w in COLS:
        d.text((cx + 8, y + 6), name, font=SB(fs), fill=mix(DIM, a)); cx += w
    d.line((x, y + rh - 6, x + tw, y + rh - 6), fill=mix(OFFB, a), width=2)
    for k, row in enumerate(rows):
        ra = a * (r(rowp, k * .1, k * .1 + .1) if rowp is not None else 1)
        if ra <= 0: continue
        yy = y + rh * (k + 1)
        if k in hl_rows:
            d.rounded_rectangle((x - 6, yy - 4, x + tw + 6, yy + rh - 10), 10, fill=mix((40, 46, 80), ra), outline=mix(YEL, ra), width=2)
        cx = x
        for j, (val, (name, w)) in enumerate(zip(row, COLS)):
            col = WHITE
            if (k, j) in hl_cells: col = hl_cells[(k, j)] if isinstance(hl_cells, dict) else RED
            if k in dim_rows: col = DIM
            f = MB(fs) if j != 1 else MB(fs)
            if j >= 3: d.text((cx + w - 16 - d.textlength(val, font=f), yy + 6), val, font=f, fill=mix(col, ra))
            else: d.text((cx + 8, yy + 6), val, font=f, fill=mix(col, ra))
            cx += w


# ---------- chapters: (title, step label, beats[(narration, draw(d, p, t))]) ----------
Q = [("SELECT b.name, SUM(p.amount)", CYAN),
     ("FROM   payments p", WHITE),
     ("JOIN   accounts a ON a.id = p.account_id", WHITE),
     ("JOIN   branches b ON b.id = a.branch_id", WHITE),
     ("WHERE  a.status = 'ACTIVE'", YEL),
     ("AND    p.created >= DATE '2026-10-01'", YEL),
     ("AND    p.created <  DATE '2026-11-01'", YEL),
     ("GROUP  BY b.name;", CYAN)]


def c0(d, b, p, t):
    if b == 0:
        ctx(d, 230, "branch_report.sql", MB(44), DIM, r(p, 0, .1))
        ctx(d, 330, "Friday: 2 seconds", SB(80), GREEN, r(p, .1, .2))
        ctx(d, 470, "Monday: 40 minutes", SB(80), RED, r(p, .4, .5))
        ctx(d, 630, "code changes: none", SB(44), YEL, r(p, .7, .8))
    elif b == 1:
        steps = ["Real plan", "Read the tree", "Biggest gap", "Why wrong?", "Binds", "Index ignored?", "Fix in order", "Verify"]
        for k, s in enumerate(steps):
            al = r(p, k * .08, k * .08 + .1); x = 140 + (k % 4) * 420; y = 300 + (k // 4) * 230
            box(d, (x, y, x + 380, y + 170), [CYAN, GREEN, YEL, PINK, PURP, CYAN, GREEN, YEL][k], al, f"Step {k + 1}", s, 36, 30)
    else:
        ctx(d, 380, "a method, not a guess", SB(86), WHITE, r(p, 0, .15))
        ctx(d, 520, "works on any slow query", SB(50), CYAN, r(p, .3, .45))


def c1(d, b, p, t):
    code(d, 160, 220, Q, r(p, 0, .1) if b == 0 else 1, 36)
    if b >= 1:
        a = r(p, 0, .15) if b == 1 else 1
        box(d, (1180, 230, 1760, 400), CYAN, a, "ACCOUNTS", "≈ 1 million rows", 40, 32)
        box(d, (1180, 450, 1760, 620), PURP, a, "PAYMENTS", "≈ 50 million rows · monthly partitions", 40, 28)
        box(d, (1180, 670, 1760, 790), GREEN, a, "BRANCHES", "12 rows", 36, 28)
    if b == 2:
        ctx(d, 860, "Step 1: don't stare at the SQL. Ask Oracle what it DID.", SB(42), YEL, r(p, .1, .25))


def c2(d, b, p, t):
    if b == 0:
        box(d, (140, 260, 900, 560), DIM, r(p, 0, .1), "EXPLAIN PLAN", "what Oracle THINKS it would do", 44, 30)
        box(d, (1020, 260, 1780, 560), GREEN, r(p, .35, .45), "DISPLAY_CURSOR", "what Oracle REALLY did", 44, 30)
        ctx(d, 640, "estimates only  vs  real row counts & time", SB(40), WHITE, r(p, .6, .7))
    elif b == 1:
        code(d, 160, 220, [("SELECT /*+ GATHER_PLAN_STATISTICS */ b.name, SUM(p.amount)", GREEN),
                           ("FROM payments p JOIN accounts a …;", WHITE), ("", WHITE),
                           ("SELECT * FROM TABLE(", CYAN),
                           ("  DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));", CYAN)], r(p, 0, .1), 36)
        ctx(d, 640, "run once → then ask for the last execution's statistics", SB(36), YEL, r(p, .55, .65))
    elif b == 2:
        box(d, (300, 260, 1620, 460), PURP, r(p, 0, .1), "Still running after 40 minutes?", "SQL Monitor shows the same numbers LIVE", 44, 32)
        code(d, 360, 540, [("SELECT DBMS_SQLTUNE.REPORT_SQL_MONITOR(sql_id => :id,", CYAN), ("       type => 'TEXT') FROM dual;", CYAN)], r(p, .35, .45), 32)
    else:
        plan(d, 120, 260, BAD, r(p, 0, .1), rowp=p * 1.6)


def c3(d, b, p, t):
    order = [3, 5, 4, 2, 1, 0]
    if b == 0:
        k = min(5, int(p * 7))
        plan(d, 120, 220, BAD, 1, hl_rows=(order[k],))
        ctx(d, 640, "most indented first · siblings top to bottom · parent after children", SB(36), YEL, r(p, .1, .2))
    elif b == 1:
        plan(d, 120, 220, BAD, 1)
        lbl = [("full scan ACCOUNTS", CYAN, .05), ("for EACH account → index into PAYMENTS", PURP, .3),
               ("NESTED LOOPS joins them", YEL, .55), ("HASH GROUP BY → 12 branches", GREEN, .75)]
        items(d, 210, 620, lbl, p, 74, 34, 1500)
    else:
        plan(d, 120, 220, BAD, 1)
        for k in range(5):
            y0 = 220 + 52 * (6 - k) + 26; al = r(p, k * .12, k * .12 + .1)
            arrow(d, (1880, y0), (1880, y0 - 40), GREEN, al, 6)
        ctx(d, 640, "rows flow UP: each parent consumes what its children produce", SB(38), GREEN, r(p, .2, .3))


def c4(d, b, p, t):
    if b == 0:
        plan(d, 120, 220, BAD, 1, hl_cells={(k, 4): YEL for k in range(6)} | {(k, 5): CYAN for k in range(6)})
        ctx(d, 640, "E-Rows = expected   ·   A-Rows = actual", SB(44), WHITE, r(p, .2, .3))
    elif b == 1:
        plan(d, 120, 220, BAD, 1, hl_rows=(3,), hl_cells={(3, 4): YEL, (3, 5): RED})
        ctx(d, 640, "expected 10  →  got 970,000", SB(56), RED, r(p, .3, .4))
        ctx(d, 730, "off by ×97,000", SB(44), YEL, r(p, .6, .7))
    elif b == 2:
        plan(d, 120, 220, BAD, 1, hl_rows=(4, 5), hl_cells={(4, 3): RED, (5, 3): RED, (4, 7): RED, (4, 6): RED})
        hbar(d, 300, 700, 1320, 40, .001 * r(p, 0, .3), GREEN, r(p, 0, .1), "plan built for: 10 index lookups", "10")
        hbar(d, 300, 830, 1320, 40, r(p, .35, .7), RED, r(p, .3, .4), "what happened: 970,000 index lookups", "970K")
    else:
        ctx(d, 300, "The rule", SB(70), YEL, r(p, 0, .1))
        ctx(d, 440, "Find the first line, from the bottom,", SB(52), WHITE, r(p, .1, .2))
        ctx(d, 520, "where E-Rows and A-Rows differ by orders of magnitude.", SB(52), WHITE, r(p, .2, .3))
        ctx(d, 660, "Fix that estimate → the rest of the plan usually fixes itself.", SB(44), GREEN, r(p, .5, .6))


def c5(d, b, p, t):
    if b == 0:
        code(d, 160, 220, [("SELECT num_rows, last_analyzed FROM user_tab_statistics", CYAN), ("WHERE table_name = 'ACCOUNTS';", CYAN),
                           ("--  1,004,210   2026-10-02", DIM), ("", WHITE),
                           ("SELECT num_distinct, histogram FROM user_tab_col_statistics", CYAN),
                           ("WHERE table_name = 'ACCOUNTS' AND column_name = 'STATUS';", CYAN),
                           ("--  2   FREQUENCY  (ACTIVE: 10 · CLOSED: 1,004,200)", DIM)], r(p, 0, .1), 32)
    elif b == 1:
        box(d, (160, 260, 900, 600), DIM, r(p, 0, .1), "Statistics (old map)", "ACTIVE: 10 · CLOSED: 1,004,200", 42, 32)
        arrow(d, (920, 430), (1000, 430), YEL, r(p, .3, .4), 6)
        box(d, (1020, 260, 1760, 600), RED, r(p, .3, .4), "Reality (after migration)", "ACTIVE: 970,000 · CLOSED: 34,210", 42, 32)
        ctx(d, 700, "the optimizer is driving with an old map", SB(44), YEL, r(p, .6, .7))
    elif b == 2:
        code(d, 160, 240, [("BEGIN", WHITE), ("  DBMS_STATS.GATHER_TABLE_STATS(", GREEN), ("    ownname    => 'APP',", WHITE),
                           ("    tabname    => 'ACCOUNTS',", WHITE), ("    method_opt => 'FOR ALL COLUMNS SIZE AUTO');", YEL), ("END;", WHITE)], r(p, 0, .1), 36)
        box(d, (1200, 300, 1760, 520), GREEN, r(p, .5, .6), "histogram", "ACTIVE: 970,000 ✓", 40, 32)
    else:
        items(d, 210, 300, [("✓ gather stats right after big loads and migrations", GREEN, 0),
                            ("✓ the nightly job only touches 'stale' tables (more than 10 % changed)", CYAN, .25),
                            ("✓ skewed columns need histograms", YEL, .5),
                            ("✗ don't wait for tomorrow when the report is slow today", RED, .75)], p, 100, 38)


def c6(d, b, p, t):
    if b == 0:
        ctx(d, 280, "Fast for one user, slow for another?", SB(64), WHITE, r(p, 0, .1))
        code(d, 460, 420, [("WHERE a.status = :status", YEL)], r(p, .3, .4), 46)
    elif b == 1:
        box(d, (160, 240, 760, 420), GREEN, r(p, 0, .1), "1st call: 'FROZEN'", "1,000 rows → index plan", 38, 30)
        arrow(d, (780, 330), (960, 330), CYAN, r(p, .2, .3), 6)
        box(d, (980, 240, 1760, 420), CYAN, r(p, .2, .3), "cursor in shared pool", "plan: INDEX RANGE SCAN", 38, 30)
        box(d, (160, 520, 760, 700), RED, r(p, .45, .55), "2nd call: 'ACTIVE'", "970,000 rows → same plan!", 38, 30)
        arrow(d, (780, 610), (960, 380), RED, r(p, .6, .7), 6)
        ctx(d, 790, "bind peeking: the FIRST value decides the plan for everyone", SB(38), YEL, r(p, .7, .8))
    else:
        code(d, 160, 240, [("SELECT child_number, is_bind_sensitive, is_bind_aware, executions", CYAN), ("FROM v$sql WHERE sql_id = :id;", CYAN)], r(p, 0, .1), 32)
        items(d, 210, 470, [("bind sensitive = Oracle is watching", YEL, .25), ("bind aware = it learned: separate plans per value range", GREEN, .5),
                            ("needs a few bad runs first → baselines help", CYAN, .75)], p, 90, 36)


def c7(d, b, p, t):
    if b == 0:
        ctx(d, 300, "You have an index. Oracle ignores it.", SB(64), WHITE, r(p, 0, .1))
        box(d, (560, 440, 1360, 620), CYAN, r(p, .3, .4), "index on payments(created)", "TABLE ACCESS FULL anyway", 40, 32)
    elif b == 1:
        code(d, 160, 240, [("WHERE TRUNC(p.created) = DATE '2026-10-15'      ✗", RED)], r(p, 0, .1), 36)
        code(d, 160, 400, [("WHERE p.created >= DATE '2026-10-15'", GREEN), ("  AND p.created <  DATE '2026-10-16'          ✓", GREEN)], r(p, .4, .5), 36)
        ctx(d, 700, "a function on the column hides it from the index", SB(40), YEL, r(p, .7, .8))
    elif b == 2:
        code(d, 160, 260, [("-- account_no is VARCHAR2", DIM), ("WHERE a.account_no = 40817810", RED), ("-- Oracle runs: TO_NUMBER(account_no) = 40817810 on EVERY row", YEL)], r(p, 0, .1), 34)
        code(d, 160, 560, [("WHERE a.account_no = '40817810'   ✓", GREEN)], r(p, .5, .6), 34)
    else:
        hbar(d, 300, 360, 1320, 44, .03, GREEN, r(p, 0, .1), "read 0.1 % of rows → index wins", "")
        hbar(d, 300, 520, 1320, 44, .4, YEL, r(p, .25, .35), "read 40 % of rows → full scan wins", "")
        ctx(d, 700, "sometimes the full scan IS the right answer", SB(44), CYAN, r(p, .55, .65))


def c8(d, b, p, t):
    steps = [("1. Fix the SQL", "predicates · joins · needless sorts", GREEN), ("2. Fix statistics", "fresh stats · histograms", CYAN),
             ("3. Index", "only for a real access pattern", YEL), ("4. Baseline / SQL patch", "pin a plan without code changes", PURP),
             ("5. Hint in the code", "last resort: it freezes the plan", RED)]
    upto = [0, 2, 3, 4][b]
    for k, (s, sub, col) in enumerate(steps):
        if k > upto: continue
        al = r(p, 0, .12) if k == upto or (b == 1 and k == 1) else 1
        y = 200 + k * 150
        box(d, (360, y, 1560, y + 120), col, al, s, sub, 40, 28)


def c9(d, b, p, t):
    if b == 0:
        plan(d, 120, 220, GOOD, 1, rowp=p * 1.6, hl_cells={(3, 4): GREEN, (3, 5): GREEN, (2, 1): GREEN})
    elif b == 1:
        plan(d, 120, 220, GOOD, 1, hl_rows=(2, 3, 5), hl_cells={(3, 4): GREEN, (3, 5): GREEN})
        ctx(d, 640, "estimate ≈ reality → each table read once → HASH JOIN", SB(42), GREEN, r(p, .2, .3))
    elif b == 2:
        hbar(d, 300, 300, 1320, 50, 1, RED, r(p, 0, .1), "before", "40 min · 9.8M buffers")
        hbar(d, 300, 480, 1320, 50, .0009 * 1 + .01, GREEN, r(p, .3, .4), "after", "2.1 s · 85K buffers")
        ctx(d, 640, "×1,150 faster", SB(80), GREEN, r(p, .55, .65))
    else:
        code(d, 160, 260, [("DECLARE n PLS_INTEGER;", WHITE), ("BEGIN", WHITE),
                           ("  n := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(sql_id => :id);", PURP), ("END;", WHITE)], r(p, 0, .1), 34)
        ctx(d, 620, "lock the good plan → a future stats change can't flip it back", SB(40), YEL, r(p, .4, .5))


def c10(d, b, p, t):
    steps = ["Get the REAL plan (ALLSTATS LAST / SQL Monitor)", "Read it as a tree, rows flow up", "Find the biggest E-Rows vs A-Rows gap",
             "Why wrong? stats · binds · functions on columns", "Fix in order: SQL → stats → index → baseline → hint", "Verify with real numbers, then lock the plan"]
    if b < 2:
        for k, s in enumerate(steps):
            st = (k * .15) if b == 0 else 0
            if b == 0 and k > 2: continue
            al = r(p, st, st + .1) if (b == 0 or k > 2) else 1
            if b == 1 and k > 2: al = r(p, (k - 3) * .2, (k - 3) * .2 + .1)
            y = 180 + k * 115
            d.rounded_rectangle((260, y, 1660, y + 95), 18, fill=mix(CARD, al), outline=mix(GREEN, al), width=2)
            d.text((300, y + 26), f"{k + 1}.  {s}", font=SB(36), fill=mix(WHITE, al))
    else:
        ctx(d, 260, "Every step has its own short on the channel", SB(54), WHITE, r(p, 0, .1))
        ctx(d, 360, "→ Playlists: Oracle Performance & SQL Tuning", SB(44), CYAN, r(p, .2, .3))
        d.rounded_rectangle((560, 500, 1360, 620), 60, fill=mix(GREEN, r(p, .4, .5)))
        ctx(d, 528, "SUBSCRIBE", SB(60), BG, r(p, .4, .5))
        ctx(d, 700, "Which query is killing YOUR database? Tell me below 👇".replace(" 👇", ""), SB(40), YEL, r(p, .6, .7))


CHAPTERS = [
    ("Intro", "", c0, [
        "Monday morning. The monthly branch report, which took two seconds on Friday, now runs for forty minutes. Nobody changed a single line of code.",
        "In this video we'll fix it together, step by step, the way you would in production. Eight steps, no guessing, and no random hints.",
        "By the end, you'll have a repeatable method you can use on any slow query in any Oracle database."]),
    ("The query", "", c1, [
        "Here's the query. It sums the October payments per branch, for active accounts only.",
        "Three tables: accounts, with about a million rows. Payments, with about fifty million rows, partitioned by month. And twelve branches.",
        "The first instinct is to stare at the SQL and start rewriting it. Don't. Step one is to ask Oracle what it actually did."]),
    ("Step 1 · Get the real plan", "1", c2, [
        "Explain plan only shows what Oracle thinks it would do. It's a prediction. We want what really happened, with real row counts and real time.",
        "So add the gather plan statistics hint and run the query once. Then call D B M S X plan dot display cursor, with the format all stats last. That's the plan of the last execution, with the actual numbers.",
        "And if the query is still running after forty minutes, you don't have to wait for it. SQL Monitor shows the same numbers live, while it runs.",
        "Here's our plan. Estimates and actuals, side by side. Now let's read it."]),
    ("Step 2 · Read it as a tree", "2", c3, [
        "Don't read a plan from the top. Read it as a tree. The most indented operation runs first. Siblings run from top to bottom, and a parent runs after its children.",
        "Here: a full scan of accounts. Then, for every account, an index lookup into payments. Nested loops joins the two, and a hash group by adds up twelve branch totals.",
        "Rows flow upwards. Every parent consumes what its children produce. Keep that picture in mind."]),
    ("Step 3 · Find the biggest gap", "3", c4, [
        "Now the most important trick in tuning. Compare E rows, what the optimizer expected, with A rows, what actually happened.",
        "On the accounts line, Oracle expected ten active accounts. It got nine hundred and seventy thousand. Off by a factor of almost a hundred thousand.",
        "Nested loops was a great plan for ten accounts: ten quick index lookups. For nine hundred and seventy thousand accounts, it's nine hundred and seventy thousand lookups, and almost ten million buffer gets. That's where forty minutes go.",
        "So here's the rule. Find the first line, from the bottom, where the estimate and the actual rows differ by orders of magnitude. Fix that estimate, and the rest of the plan usually fixes itself."]),
    ("Step 4 · Why was the estimate wrong?", "4", c5, [
        "So why did Oracle think only ten accounts were active? Ask the statistics. The table was last analyzed at the beginning of October, and the histogram on status says: ten active, one million closed.",
        "Last week a migration activated almost a million accounts. The statistics are from before that. The optimizer is driving with an old map.",
        "Fix the map. Gather table statistics on accounts, and let Oracle decide where histograms are needed, with for all columns size auto. Now the histogram says nine hundred and seventy thousand active.",
        "Make it a habit: gather statistics right after big loads and migrations. The nightly job only touches tables that changed by more than ten percent, and it runs tonight. Your report is slow today."]),
    ("Step 5 · Bind variables", "5", c6, [
        "Sometimes the statistics are perfect, and still the same query is fast for one user and slow for another. Then look at bind variables.",
        "On the first hard parse, Oracle peeks at the bind value. If the first caller asks for frozen accounts, a thousand rows, it builds an index plan. The next caller asks for active accounts, nine hundred and seventy thousand rows, and gets the same plan.",
        "Adaptive cursor sharing can notice this and create a second plan, but only after a few bad executions. Check V dollar SQL: is it bind sensitive, is it bind aware, and how many child cursors are there."]),
    ("Step 6 · Index ignored?", "6", c7, [
        "Another classic: you have an index, and Oracle still does a full table scan.",
        "Functions on the column hide it from the index. Trunc of created, upper of a name. Rewrite the condition as a range on the raw column, and the index is usable again.",
        "Hidden conversions do the same. Compare a VARCHAR2 column with a number, and Oracle converts the column on every row. Compare with a string instead.",
        "And sometimes the full scan is simply right. If you read a large part of the table, one big multiblock read beats a million single block reads."]),
    ("Step 7 · Fix in the right order", "7", c8, [
        "Now, how to fix it, in the right order. First, fix the SQL itself: wrong predicates, missing join conditions, sorts you don't need.",
        "Second, fix the statistics, like we just did. Third, add or change an index, but only for a real access pattern.",
        "Fourth, if you can't change the code, use a SQL plan baseline or a SQL patch to pin a good plan from outside.",
        "And last, a hint in the code. It's the last resort, because it freezes a plan while your data keeps changing."]),
    ("Step 8 · Verify", "8", c9, [
        "After gathering statistics, we run the query again, with the same plan statistics.",
        "Now the estimates match reality. Oracle reads accounts once, reads only the October partition of payments, and joins them with a hash join.",
        "Forty minutes became two seconds. Buffer gets dropped from almost ten million to about eighty five thousand.",
        "If this report is critical, lock the good plan with a SQL plan baseline, so a future statistics change can't flip it back."]),
    ("Recap", "", c10, [
        "Here's the whole method on one screen. Get the real plan. Read it as a tree. Find the biggest gap between estimate and reality.",
        "Ask why the estimate was wrong: statistics, bind variables, or functions on columns. Fix in the right order. And always verify with real numbers.",
        "Every step here has its own short video on the channel, in the Oracle performance playlist. If this helped, subscribe, and tell me in the comments which query is killing your database."]),
]


def header(d, ch, step, t, DUR):
    d.rounded_rectangle((40, 30, 470, 92), 31, fill=CARD)
    d.text((70, 44), "@sql_developer_no1", font=SB(30), fill=GREEN)
    title = ch
    w = d.textlength(title, font=SB(34))
    d.rounded_rectangle((W - 80 - w, 30, W - 40, 92), 31, fill=CARD)
    d.text((W - 60 - w, 44), title, font=SB(34), fill=YEL if step else CYAN)
    d.rectangle((0, H - 8, int(W * t / DUR), H), fill=GREEN)


def subtitle(d, s, a):
    if a <= 0: return
    f = SN(34); lines = wraptxt(d, s, f, 1600)[:3]
    h = len(lines) * 46 + 28; y0 = H - 40 - h
    d.rounded_rectangle((120, y0, W - 120, H - 40), 18, fill=mix((12, 18, 34), a), outline=mix(OFFB, a), width=2)
    for k, l in enumerate(lines):
        ctx(d, y0 + 14 + k * 46, l, f, WHITE, a)


def build():
    from tts import say
    meta_p = f"{OUT}/meta.json"
    texts = [s for _, _, _, bs in CHAPTERS for s in bs]
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
    if meta.get("texts") != texts:
        durs = [say(s, f"{OUT}/n_{k}.wav", sid=6) for k, s in enumerate(texts)]
        meta = {"texts": texts, "durs": durs}; json.dump(meta, open(meta_p, "w"))
    durs = meta["durs"]
    # timeline
    beats = []; t0 = 0.0; k = 0; chap_starts = []
    for ci, (title, step, fn, bs) in enumerate(CHAPTERS):
        chap_starts.append((t0, title))
        for bi, s in enumerate(bs):
            L = durs[k] + (0.9 if bi < len(bs) - 1 else 1.6) + (0.6 if bi == 0 else 0)
            beats.append((t0, L, ci, bi, s, k, (0.6 if bi == 0 else 0.25))); t0 += L; k += 1
    DUR = t0
    json.dump({"chapters": chap_starts, "dur": DUR}, open(f"{OUT}/chapters.json", "w"))
    return beats, DUR, chap_starts


def render_frame(beats, DUR, t):
    off = int((t * 30) % H)
    im = RAIN.crop((0, H - off, W, 2 * H - off)); d = ImageDraw.Draw(im)
    bt = max((b for b in beats if b[0] <= t), key=lambda b: b[0])
    t0, L, ci, bi, s, k, lead = bt
    title, step, fn, bs = CHAPTERS[ci]
    p = min(1, max(0, (t - t0) / L))
    if bi == 0 and step and (t - t0) < 0.9:
        a = 1 - pr(t - t0, .5, .9)
        ctx(d, 420, f"STEP {step}", SB(60), YEL, a); ctx(d, 510, title.split("· ")[-1], SB(80), WHITE, a)
    else:
        fn(d, bi, p, t)
    header(d, title, step, t, DUR)
    subtitle(d, s, pr(t - t0, lead - .1, lead + .2) * (1 - pr(t - t0, L - .25, L)))
    return im


def music(DUR, path):
    import numpy as np, soundfile as sf
    from scipy.signal import lfilter
    SR = 44100; n = int(SR * DUR) + SR; out = np.zeros(n)
    def note(m): return 440 * 2 ** ((m - 69) / 12)
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    bar = 4 * 60 / 84
    for b in range(int(DUR / bar) + 1):
        ch = chords[b % 4]; st = int(b * bar * SR); L = int((bar + .5) * SR); tt = np.arange(L) / SR
        s = sum(np.sin(2 * np.pi * note(m) * tt * (1 + dd)) for m in ch for dd in (-.003, .003))
        e = np.minimum(1, tt / .8) * np.minimum(1, (L / SR - tt) / .8)
        seg = s * e; en = min(n, st + L); out[st:en] += seg[:en - st]
    out = lfilter([0.06], [1, -0.94], out)
    step = 60 / 84 / 2; tt0 = 0.0; k = 0
    while tt0 < DUR - 2:
        b = int(tt0 / bar); m = chords[b % 4][[0, 1, 2, 1][k % 4]] + 12
        L = int(.4 * SR); tt = np.arange(L) / SR
        sig = np.sin(2 * np.pi * note(m) * tt) * np.exp(-tt * 8) * .25
        st = int(tt0 * SR); en = min(n, st + L); out[st:en] += sig[:en - st]; tt0 += step; k += 1
    out /= np.max(np.abs(out)); fade = int(3 * SR); out[-fade:] *= np.linspace(1, 0, fade); out[:SR] *= np.linspace(0, 1, SR)
    sf.write(path, out, SR)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    beats, DUR, chaps = build()
    if mode == "preview":
        ims = []
        for b in beats:
            ims.append(render_frame(beats, DUR, b[0] + b[1] * .8).resize((480, 270)))
        cols = 6; rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (480 * cols, 270 * rows))
        for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 480, (i // cols) * 270))
        sheet.save(f"{OUT}/sheet.png"); print("preview", round(DUR, 1), len(beats)); sys.exit()
    import numpy as np, soundfile as sf
    NF = int(DUR * FPS)
    pr_ = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", f"{OUT}/silent.mp4"], stdin=subprocess.PIPE)
    for i in range(NF): pr_.stdin.write(render_frame(beats, DUR, i / FPS).tobytes())
    pr_.stdin.close(); pr_.wait()
    SR = 44100; n = int(DUR * SR) + SR; voice = np.zeros(n)
    for (t0, L, ci, bi, s, k, lead) in beats:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/n_{k}.wav", "-ar", str(SR), "-ac", "1", f"{OUT}/n_{k}_44.wav"], check=True)
        v, _ = sf.read(f"{OUT}/n_{k}_44.wav"); st = int((t0 + lead) * SR); en = min(n, st + len(v)); voice[st:en] += v[:en - st]
    music(DUR, f"{OUT}/music.wav")
    mus, _ = sf.read(f"{OUT}/music.wav"); m = np.zeros(n); m[:min(n, len(mus))] = mus[:n]
    w = int(.3 * SR); env = np.convolve(np.abs(voice), np.ones(w) / w, mode="same")
    duck = 1 - 0.6 * np.clip(env / (env.max() * .15), 0, 1)
    mix_ = voice / np.max(np.abs(voice)) * .95 + m * .18 * duck
    mix_ /= max(1, np.max(np.abs(mix_)) / .97)
    sf.write(f"{OUT}/mix.wav", np.stack([mix_, mix_], 1), SR)
    final = "/home/claude/long1/oracle_query_tuning_guide.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/silent.mp4", "-i", f"{OUT}/mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", final], check=True)
    print("DONE", final, round(DUR, 1))

"""Long-form 16:9 video: From row-by-row to set-based: a PL/SQL batch 50x faster."""
import sys, os, json, math, random, subprocess
sys.path.insert(0, "/home/claude"); sys.path.insert(0, "/home/claude/en")
from common import SB, SN, MN, MB, BG, WHITE, DIM, GREEN, CYAN, YEL, PINK, RED, CARD, OFFB, PURP, mix, pr
from PIL import Image, ImageDraw

W, H, FPS = 1920, 1080, 24
OUT = "/home/claude/long2/out"; os.makedirs(OUT, exist_ok=True)

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



# ---------- chapters ----------
LOOP = [("FOR r IN (SELECT id, amount, ccy FROM payments", CYAN),
        ("          WHERE status = 'NEW') LOOP", CYAN),
        ("  SELECT fee_pct INTO l_pct FROM fx_rates", YEL),
        ("  WHERE ccy = r.ccy;", YEL),
        ("  UPDATE payments SET fee = r.amount * l_pct,", PURP),
        ("         status = 'DONE' WHERE id = r.id;", PURP),
        ("  INSERT INTO fee_log VALUES (r.id, r.amount * l_pct);", GREEN),
        ("  COMMIT;", RED),
        ("END LOOP;", CYAN)]

TIMES = [("start", 190, RED), ("no commit per row", 138, YEL), ("BULK + FORALL", 38, YEL),
         ("join, not lookup", 14, CYAN), ("one SQL", 6, GREEN), ("parallel", 3.67, GREEN)]


def timeline(d, upto, p, y0=230):
    for k, (lb, mins, col) in enumerate(TIMES[:upto + 1]):
        al = r(p, 0, .15) if k == upto else 1
        y = y0 + k * 105
        d.text((160, y + 6), lb, font=SB(32), fill=mix(WHITE, al))
        hbar(d, 620, y + 10, 1000, 40, mins / 190, col, al)
        s = f"{int(mins // 60)} h {int(mins % 60):02d} min" if mins >= 60 else (f"{int(mins)} min" if mins >= 5 else "3 min 40 s")
        d.text((1650, y + 6), s, font=MB(32), fill=mix(col, al))


def c0(d, b, p, t):
    if b == 0:
        ctx(d, 220, "batch_pkg.calc_fees", MB(46), DIM, r(p, 0, .1))
        ctx(d, 330, "runtime: 3 h 10 min", SB(84), RED, r(p, .15, .25))
        ctx(d, 480, "batch window: 1 hour", SB(60), YEL, r(p, .45, .55))
        ctx(d, 600, "2,000,000 payments every night", SB(44), WHITE, r(p, .7, .8))
    elif b == 1:
        steps = ["Measure", "No commit per row", "BULK + FORALL", "Join, not lookup", "One SQL", "Parallel"]
        for k, s in enumerate(steps):
            al = r(p, k * .1, k * .1 + .1); x = 140 + (k % 3) * 560; y = 280 + (k // 3) * 230
            box(d, (x, y, x + 520, y + 170), [CYAN, RED, YEL, PURP, GREEN, PINK][k], al, f"Step {k + 1}", s, 38, 32)
    else:
        ctx(d, 340, "same result", SB(70), WHITE, r(p, 0, .15))
        ctx(d, 460, "3 h 10 min  →  3 min 40 s", SB(80), GREEN, r(p, .3, .45))


def c1(d, b, p, t):
    code(d, 140, 200, LOOP, 1 if b else r(p, 0, .1), 32)
    if b >= 1:
        rows = [("1 SELECT", YEL), ("1 UPDATE", PURP), ("1 INSERT", GREEN), ("1 COMMIT", RED)]
        for k, (s, col) in enumerate(rows):
            al = r(p, k * .12, k * .12 + .1) if b == 1 else 1
            box(d, (1380, 210 + k * 140, 1780, 320 + k * 140), col, al, s, "per row", 36, 26)
    if b == 2:
        ctx(d, 820, "× 2,000,000 rows = 8,000,000 trips", SB(46), RED, r(p, .1, .25))


def c2(d, b, p, t):
    if b == 0:
        code(d, 160, 220, [("SELECT sql_text, executions, elapsed_time / 6e7 AS min", CYAN),
                           ("FROM   v$sql WHERE module = 'FEES'", CYAN),
                           ("ORDER  BY elapsed_time DESC;", CYAN)], r(p, 0, .1), 34)
        code(d, 160, 520, [("DBMS_APPLICATION_INFO.SET_MODULE('FEES', 'calc');", PURP)], r(p, .55, .65), 32)
        ctx(d, 700, "tag the batch → find its SQL in seconds", SB(38), YEL, r(p, .7, .8))
    elif b == 1:
        rows = [("UPDATE payments", "2,000,000 ×", 58, PURP), ("waits: log file sync (COMMIT)", "2,000,000 ×", 52, RED),
                ("SELECT fee_pct FROM fx_rates", "2,000,000 ×", 41, YEL), ("INSERT INTO fee_log", "2,000,000 ×", 33, GREEN)]
        for k, (s, ex, m, col) in enumerate(rows):
            y = 260 + k * 150; al = r(p, k * .15, k * .15 + .1)
            d.text((160, y), s, font=SB(34), fill=mix(WHITE, al)); d.text((160, y + 48), ex, font=MB(28), fill=mix(DIM, al))
            hbar(d, 900, y + 20, 700, 40, m / 60, col, al)
            d.text((1640, y + 14), f"{m} min", font=MB(34), fill=mix(col, al))
    else:
        ctx(d, 380, "Measure first. Don't guess.", SB(80), GREEN, r(p, 0, .15))
        ctx(d, 520, "every statement is fast — there are just 8 million of them", SB(42), WHITE, r(p, .35, .5))


def c3(d, b, p, t):
    if b == 0:
        box(d, (160, 260, 760, 460), CYAN, r(p, 0, .1), "COMMIT", "session waits…", 44, 32)
        arrow(d, (780, 360), (1000, 360), YEL, r(p, .2, .3), 6)
        box(d, (1020, 260, 1760, 460), YEL, r(p, .2, .3), "LGWR writes redo to disk", "event: log file sync", 40, 30)
        ctx(d, 580, "≈ 1.5 ms × 2,000,000 commits = 52 min of waiting", SB(42), RED, r(p, .55, .65))
    elif b == 1:
        code(d, 160, 220, [("FOR r IN (…) LOOP", CYAN), ("  …", DIM), ("END LOOP;", CYAN), ("COMMIT;   -- once, or every 50,000 rows", GREEN)], r(p, 0, .1), 38)
        items(d, 210, 600, [("restartable? status = 'DONE' marks what's finished", CYAN, .3),
                            ("✗ committing inside a cursor you still read → ORA-01555 risk", RED, .6)], p, 90, 34)
    else:
        timeline(d, 1, p)


def c4(d, b, p, t):
    if b == 0:
        box(d, (160, 280, 760, 520), PURP, r(p, 0, .1), "PL/SQL engine", "loops, variables", 46, 32)
        box(d, (1160, 280, 1760, 520), CYAN, r(p, 0, .1), "SQL engine", "SELECT, UPDATE, INSERT", 46, 32)
        for k in range(6):
            ph = (t * .8 + k / 6) % 1; x = 780 + 360 * ph; y = 360 if k % 2 == 0 else 440
            if k % 2: x = 1140 - 360 * ph
            d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=mix(YEL, r(p, .2, .3)))
        ctx(d, 640, "a context switch for EVERY statement, EVERY row", SB(44), YEL, r(p, .4, .5))
    elif b == 1:
        code(d, 120, 190, [("OPEN c;  LOOP", CYAN), ("  FETCH c BULK COLLECT INTO l_rows LIMIT 1000;", GREEN),
                           ("  EXIT WHEN l_rows.COUNT = 0;", WHITE),
                           ("  FORALL i IN 1 .. l_rows.COUNT", PURP),
                           ("    UPDATE payments SET fee = l_rows(i).fee, status = 'DONE'", PURP),
                           ("    WHERE id = l_rows(i).id;", PURP),
                           ("  FORALL i IN 1 .. l_rows.COUNT", GREEN),
                           ("    INSERT INTO fee_log VALUES (l_rows(i).id, l_rows(i).fee);", GREEN),
                           ("END LOOP;  CLOSE c;  COMMIT;", CYAN)], r(p, 0, .1), 30)
    elif b == 2:
        hbar(d, 300, 330, 1320, 50, 1, RED, r(p, 0, .1), "row by row", "2,000,000 switches per statement")
        hbar(d, 300, 520, 1320, 50, .02, GREEN, r(p, .3, .4), "BULK COLLECT + FORALL, LIMIT 1000", "2,000 switches")
        ctx(d, 680, "LIMIT keeps PGA memory small and flat", SB(40), YEL, r(p, .6, .7))
    else:
        timeline(d, 2, p)


def c5(d, b, p, t):
    if b == 0:
        code(d, 160, 230, [("SELECT fee_pct INTO l_pct FROM fx_rates", YEL), ("WHERE ccy = r.ccy;   -- 2,000,000 times", RED)], r(p, 0, .1), 38)
        ctx(d, 520, "12 currencies · asked 2,000,000 times", SB(48), RED, r(p, .4, .5))
    elif b == 1:
        code(d, 160, 220, [("CURSOR c IS", CYAN), ("  SELECT p.id, p.amount * r.fee_pct AS fee", GREEN),
                           ("  FROM   payments p", WHITE), ("  JOIN   fx_rates r ON r.ccy = p.ccy", GREEN),
                           ("  WHERE  p.status = 'NEW';", WHITE)], r(p, 0, .1), 38)
        ctx(d, 640, "the join reads fx_rates once → HASH JOIN", SB(42), GREEN, r(p, .55, .65))
    else:
        timeline(d, 3, p)


def c6(d, b, p, t):
    if b == 0:
        ctx(d, 300, "Now the loop only moves data around.", SB(60), WHITE, r(p, 0, .1))
        ctx(d, 420, "So let SQL do all of it.", SB(70), GREEN, r(p, .4, .5))
    elif b == 1:
        code(d, 120, 190, [("MERGE INTO payments p", PURP), ("USING (SELECT p.id, p.amount * r.fee_pct AS fee", CYAN),
                           ("       FROM payments p JOIN fx_rates r ON r.ccy = p.ccy", CYAN),
                           ("       WHERE p.status = 'NEW') s", CYAN), ("ON (p.id = s.id)", WHITE),
                           ("WHEN MATCHED THEN UPDATE SET p.fee = s.fee,", PURP),
                           ("  p.status = 'DONE', p.calc_date = TRUNC(SYSDATE);", PURP),
                           ("INSERT INTO fee_log (id, fee)", GREEN), ("SELECT id, fee FROM payments", GREEN),
                           ("WHERE status = 'DONE' AND calc_date = TRUNC(SYSDATE);", GREEN)], r(p, 0, .1), 29)
    elif b == 2:
        code(d, 120, 210, [("EXEC DBMS_ERRLOG.CREATE_ERROR_LOG('PAYMENTS');", YEL), ("", WHITE),
                           ("MERGE INTO payments p USING (…) s ON (p.id = s.id)", PURP),
                           ("WHEN MATCHED THEN UPDATE SET …", PURP),
                           ("LOG ERRORS INTO err$_payments REJECT LIMIT UNLIMITED;", GREEN)], r(p, 0, .1), 32)
        ctx(d, 640, "bad rows go to a table · good rows still commit", SB(42), GREEN, r(p, .5, .6))
    else:
        timeline(d, 4, p)


def c7(d, b, p, t):
    if b == 0:
        code(d, 160, 220, [("ALTER SESSION ENABLE PARALLEL DML;", PURP), ("", WHITE),
                           ("MERGE /*+ PARALLEL(p 8) */ INTO payments p …;", PURP), ("COMMIT;", YEL)], r(p, 0, .1), 38)
        for k in range(8):
            x = 220 + k * 190; al = r(p, .4 + k * .04, .5 + k * .04)
            box(d, (x, 560, x + 160, 660), PURP, al, f"PX {k + 1}", None, 30)
        ctx(d, 740, "after parallel DML: COMMIT before you touch the table again (ORA-12838)", SB(34), YEL, r(p, .75, .85))
    elif b == 1:
        code(d, 160, 220, [("DBMS_PARALLEL_EXECUTE.CREATE_CHUNKS_BY_ROWID(", CYAN), ("  'fees', 'APP', 'PAYMENTS', TRUE, 50000);", CYAN),
                           ("DBMS_PARALLEL_EXECUTE.RUN_TASK('fees', l_sql,", GREEN), ("  DBMS_SQL.NATIVE, parallel_level => 8);", GREEN)], r(p, 0, .1), 34)
        items(d, 210, 600, [("each chunk commits on its own → restartable", GREEN, .4), ("failed chunks can be resumed", CYAN, .65)], p, 90, 36)
    else:
        timeline(d, 5, p)


def c8(d, b, p, t):
    if b == 0:
        code(d, 160, 230, [("SELECT COUNT(*), SUM(fee) FROM payments_old_run", CYAN), ("MINUS", YEL),
                           ("SELECT COUNT(*), SUM(fee) FROM payments_new_run;", CYAN), ("-- no rows → identical totals ✓", GREEN)], r(p, 0, .1), 36)
        ctx(d, 640, "faster AND the same numbers — prove it on a copy", SB(42), YEL, r(p, .55, .65))
    elif b == 1:
        timeline(d, 5, 1)
    else:
        ctx(d, 320, "×52 faster", SB(140), GREEN, r(p, 0, .15))
        ctx(d, 560, "8,000,000 statements  →  2 statements", SB(56), WHITE, r(p, .35, .5))


def c9(d, b, p, t):
    steps = ["Measure first: V$SQL, module tags, waits", "Don't COMMIT every row", "BULK COLLECT + FORALL with LIMIT",
             "Replace lookups with joins", "One SQL: MERGE / INSERT…SELECT + LOG ERRORS", "Still too big? Parallel DML or chunks"]
    if b < 2:
        for k, s in enumerate(steps):
            if b == 0 and k > 2: continue
            al = r(p, k * .15, k * .15 + .1) if b == 0 else (1 if k < 3 else r(p, (k - 3) * .2, (k - 3) * .2 + .1))
            y = 180 + k * 115
            d.rounded_rectangle((260, y, 1660, y + 95), 18, fill=mix(CARD, al), outline=mix(GREEN, al), width=2)
            d.text((300, y + 26), f"{k + 1}.  {s}", font=SB(36), fill=mix(WHITE, al))
    else:
        ctx(d, 260, "Each step has its own short on the channel", SB(54), WHITE, r(p, 0, .1))
        ctx(d, 360, "→ Playlist: PL/SQL & Advanced SQL", SB(44), CYAN, r(p, .2, .3))
        d.rounded_rectangle((560, 500, 1360, 620), 60, fill=mix(GREEN, r(p, .4, .5)))
        ctx(d, 528, "SUBSCRIBE", SB(60), BG, r(p, .4, .5))
        ctx(d, 700, "How long does YOUR slowest batch run? Tell me below", SB(40), YEL, r(p, .6, .7))


CHAPTERS = [
    ("Intro", "", c0, [
        "Every night, a P L SQL batch calculates fees for two million payments. It takes three hours and ten minutes. The batch window is one hour.",
        "In this video we'll make it fast, in six steps: measure, stop committing every row, bulk processing, joins instead of lookups, one SQL statement, and parallel execution.",
        "Same business logic, same result. At the end it runs in three minutes and forty seconds."]),
    ("The code", "", c1, [
        "Here's the original code. A cursor loop over new payments. For every payment, it looks up the fee percentage, updates the payment, writes a log row, and commits.",
        "That's one select, one update, one insert and one commit, for every single row.",
        "Times two million rows: eight million trips between P L SQL and the SQL engine. Each one is fast. Together, they take hours."]),
    ("Step 1 · Measure first", "1", c2, [
        "Before changing anything, measure. Tag the batch with D B M S application info, set module. Then V dollar SQL shows you exactly which statements belong to it, how often they ran, and how long they took.",
        "Here's the result. The update: fifty eight minutes. Waiting for commits: fifty two minutes. The fee lookup: forty one minutes. The log insert: thirty three.",
        "Notice: no single statement is slow. Each takes a fraction of a millisecond. There are just eight million of them. That's the real problem with row by row."]),
    ("Step 2 · Stop committing every row", "2", c3, [
        "Every commit waits until the log writer has written the redo to disk. That wait is called log file sync. One and a half milliseconds, two million times, is fifty two minutes of pure waiting.",
        "Commit once at the end, or every fifty thousand rows if you need restart points. The status column already tells you which rows are done. And never commit inside a cursor you're still reading: that's how you get snapshot too old.",
        "One small change: three hours ten becomes two hours eighteen."]),
    ("Step 3 · BULK COLLECT + FORALL", "3", c4, [
        "Every SQL statement inside a P L SQL loop is a context switch between two engines: the P L SQL engine and the SQL engine. Millions of switches cost real time.",
        "So fetch a thousand rows at once with bulk collect limit, and send all the updates and inserts for them in one go with forall.",
        "Two million switches per statement become two thousand. And the limit clause keeps memory small and flat, whatever the table size.",
        "Two hours eighteen becomes thirty eight minutes."]),
    ("Step 4 · Join, don't look up", "4", c5, [
        "Look at the fee lookup. There are twelve currencies, and we ask for their rates two million times.",
        "Put the rates into the cursor query instead. Join payments with the rates table. Oracle reads the twelve rates once, and a hash join attaches them to every payment.",
        "Thirty eight minutes become fourteen."]),
    ("Step 5 · One SQL statement", "5", c6, [
        "Look at the loop now. It doesn't make decisions anymore. It only moves data from one query into another. So let SQL do all of it.",
        "One merge calculates and updates every fee at once. One insert select writes the whole log. The entire batch is now two SQL statements.",
        "But what about bad rows? In the loop, you could catch an exception per row. In SQL, use D M L error logging. Create an error log table, and add log errors with an unlimited reject limit. Bad rows land in the error table, and the good ones still go through.",
        "Fourteen minutes become six."]),
    ("Step 6 · Parallel", "6", c7, [
        "Still too slow for your window? Enable parallel D M L, and let eight parallel servers share the merge. Remember to commit right after it: the same transaction can't read the table again after a parallel change.",
        "If the logic must stay in P L SQL, use D B M S parallel execute. It splits the table into rowid chunks and runs your code on each chunk in parallel. Each chunk commits on its own, so a failure doesn't throw everything away.",
        "Six minutes become three minutes and forty seconds."]),
    ("Verify", "", c8, [
        "Faster is worthless if the numbers change. Run the old and the new version on a copy, and compare counts and totals. Minus returns nothing: identical results.",
        "Here's the whole journey. Three hours ten. Two hours eighteen. Thirty eight minutes. Fourteen. Six. And finally, three minutes forty.",
        "Fifty two times faster. Eight million statements became two."]),
    ("Recap", "", c9, [
        "The method again. Measure first. Stop committing every row. Use bulk collect and forall with a limit.",
        "Replace lookups with joins. Turn the loop into one SQL statement, with error logging. And only then, go parallel.",
        "Every step has its own short video on the channel, in the P L SQL playlist. If this helped, subscribe, and tell me in the comments how long your slowest batch runs."]),
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
    final = "/home/claude/long2/plsql_batch_set_based.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/silent.mp4", "-i", f"{OUT}/mix.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", final], check=True)
    print("DONE", final, round(DUR, 1))

"""55 · COMMIT & ROLLBACK from zero (v2 style)."""
import sys
sys.path.insert(0, "/home/claude/v2")
from studio import *


def acct(g, cx, cy, name, val, col, a=1.0, sub=None, w=360, ring_=0.0):
    r = (cx - w / 2, cy - 90, cx + w / 2, cy + 90)
    box(g, r, col, a, None, None)
    tx(g, cx, cy - 46, name, SB(32), col, a, "mm")
    tx(g, cx, cy + 14, val, XB(56), WHITE, a, "mm")
    if sub: tx(g, cx, cy + 62, sub, SN(24), SOFT, a, "mm")
    if ring_ > 0: ring(g, r, YEL, ring_)
    return r


def pencil(g, x, y, a, col=SOFT):
    d = g.d
    d.polygon([(x, y), (x + 120, y - 120), (x + 150, y - 90), (x + 30, y + 30)], fill=mix(YEL, a), outline=mix(col, a))
    d.polygon([(x, y), (x + 30, y + 30), (x - 12, y + 42)], fill=mix((240, 210, 170), a))
    d.polygon([(x + 120, y - 120), (x + 150, y - 90), (x + 165, y - 105), (x + 135, y - 135)], fill=mix(PINK, a))


# ------------------------------------------------------------------ scenes
def s_hook(g):
    q = sql(g, 70, 300, ["UPDATE accounts SET balance = balance - 100", "WHERE  name = 'Ali';", "-- power cut here", "UPDATE accounts SET balance = balance + 100",
                         "WHERE  name = 'Sara';"], 1, fs=28, w=940, hl=[2] if g.b >= 1 else (), hlcol=RED, dim=[3, 4] if g.b >= 1 else ())
    a = g.on(0, 1)
    ali = 1000 - int(100 * g.at(0, 2.0, 2.8))
    acct(g, 300, 760, "Ali", str(ali), CYAN, a); acct(g, 780, 760, "Sara", "500", PURP, a)
    if g.b >= 1:
        a1 = g.on(1, .4)
        icon(g, "warn", 540, 980, 100, RED, a1)
        tx(g, 540, 1080, "100 AZN … gone?", XB(48), RED, g.on(1, 1.2), "mm")
    if g.b >= 2:
        box(g, (120, 1160, 960, 1280), GREEN, g.on(2, .3), "No. Oracle puts it back. Here's why.", None, 34)


def s_pencil(g):
    a = g.on(0)
    paper = (180, 330, 900, 760)
    g.d.rounded_rectangle(paper, 18, fill=mix((235, 236, 242), a))
    for k in range(5): g.d.line((220, 410 + k * 70, 860, 410 + k * 70), fill=mix((190, 200, 220), a), width=2)
    write = g.at(0, .8, 2.2)
    s = "Ali: 900"; n = int(len(s) * write)
    era = g.at(2, 1.0, 1.8) if g.b == 2 else (0 if g.b < 2 else 1)
    ink = g.b >= 1 and g.at(1, .8, 1.6) > 0
    col = (40, 50, 80) if (g.b == 1 and g.at(1, 1.0, 1.6) > .5) else (120, 128, 150)
    if g.b < 2:
        tx(g, 230, 440, s[:n], fit(s, SB, 64, 600), col, a)
    if g.b == 0: pencil(g, 260 + 380 * write, 520, a)
    if g.b == 1:
        pill(g, 540, 860, "COMMIT = rewrite in PEN", GREEN, g.on(1, .4), 38, fill=True)
        tx(g, 540, 940, "permanent · everyone can see it", SN(32), WHITE, g.on(1, 1.0), "mm")
    if g.b == 2:
        tx(g, 230, 440, s, fit(s, SB, 64, 600), (120, 128, 150), a * (1 - era))
        icon(g, "eraser", 260 + 360 * era, 500, 110, PINK, g.on(2, .3))
        pill(g, 540, 860, "ROLLBACK = the eraser", PINK, g.on(2, .4), 38, fill=True)
        tx(g, 540, 940, "back to how it was", SN(32), WHITE, g.on(2, 1.0), "mm")
    if g.b >= 3:
        term(g, "TRANSACTION", "a group of changes: all saved together, or none", g.on(3, .2), y=1000, col=YEL)


def s_private(g):
    a = g.on(0)
    tx(g, 290, 330, "YOUR session", SB(32), CYAN, a, "mm"); tx(g, 790, 330, "a colleague", SB(32), PURP, a, "mm")
    person(g, 290, 470, 150, CYAN, a); person(g, 790, 470, 150, PURP, a)
    sql(g, 70, 600, ["UPDATE … -100;"], a, fs=30, w=440)
    acct(g, 290, 830, "Ali", "900", CYAN, g.on(0, 1.4), "you see the change")
    acct(g, 790, 830, "Ali", "1000", PURP, g.on(1, .4), "still the OLD value", ring_=g.only(1, delay=1.4))
    if g.b >= 2:
        a2 = g.on(2, .2)
        pill(g, 330, 1020, "COMMIT", GREEN, a2, 40, fill=True)
        arrow(g, (470, 1020), (600, 1020), WHITE, a2, 1, 5, 16)
        tx(g, 790, 1020, "both see 900", SB(38), GREEN, g.on(2, 1.2), "mm")
        g.focus((180, 980, 1010, 1060), a=a2)
    if g.b >= 3:
        box(g, (70, 1110, 1010, 1220), YEL, g.on(3, .2), "nobody ever sees half-finished work", None, 34)


def s_rollback(g):
    q = sql(g, 70, 300, ["UPDATE accounts ... Ali   -100", "UPDATE accounts ... Sara  +100", "DELETE FROM accounts ...  -- oops!", "ROLLBACK;"], 1, fs=30, w=940,
            la=lambda i: g.on(0, i * .6) if i < 3 else g.on(1, .2), hl=[3] if g.b >= 1 else [2], hlcol=PINK if g.b >= 1 else RED)
    if g.b >= 1:
        p = g.at(1, .8, 2.4)
        for k in range(3):
            r = q.line(2 - k); al = clamp(p * 3 - k)
            if al > 0: g.d.line((r[0] + 20, (r[1] + r[3]) / 2, r[0] + 20 + (r[2] - r[0] - 40) * al, (r[1] + r[3]) / 2), fill=mix(PINK, 1), width=4)
        acct(g, 300, 760, "Ali", "1000", CYAN, g.on(1, 2.6)); acct(g, 780, 760, "Sara", "500", PURP, g.on(1, 2.8))
        tx(g, 540, 900, "everything since the last COMMIT is undone", SB(32), PINK, g.on(1, 3.0), "mm")
    if g.b >= 2:
        box(g, (70, 980, 1010, 1110), GREEN, g.on(2, .2), "crash or lost connection?", "Oracle rolls back automatically", 36, 30, scol=WHITE)


def s_ddl(g):
    q = sql(g, 70, 300, ["UPDATE accounts SET balance = 0;", "CREATE TABLE tmp (id NUMBER);", "ROLLBACK;"], 1, fs=32, w=940,
            hl=[1] if g.b >= 1 else (), hlcol=RED, la=lambda i: g.on(0, .4 + i * .6))
    if g.b >= 1:
        a1 = g.on(1, .3)
        callout(g, q.line(1), "secret COMMIT before and after", RED, a1, at=(540, 620), fs=30, mark=False)
    if g.b >= 2:
        a2 = g.on(2, .2)
        acct(g, 540, 830, "every balance", "0", RED, a2, "the ROLLBACK came too late")
    if g.b >= 3:
        term(g, "DDL", "CREATE, ALTER, DROP, TRUNCATE: they commit for you", g.on(3, .2), y=1000, col=RED)


def s_lock(g):
    a = g.on(0)
    person(g, 220, 470, 150, CYAN, a, "you", 28); person(g, 860, 470, 150, PURP, a, "colleague", 28)
    row = (370, 420, 710, 520); box(g, row, YEL, a, "Ali · 900", "changed, NOT committed", 34, 24, scol=WHITE)
    icon(g, "lock", 540, 600, 70, YEL, g.on(0, 1.2))
    if g.b >= 1:
        arrow(g, (790, 470), (720, 470), PURP, g.on(1, .2), 1, 6, 18)
        icon(g, "clock", 860, 650, 90, PURP, g.on(1, .8)); tx(g, 860, 730, "waiting…", SB(32), PURP, g.on(1, 1.0), "ma")
    if g.b >= 2:
        box(g, (70, 860, 1010, 980), RED, g.on(2, .2), "forgot to COMMIT → everyone waits", None, 34)
        box(g, (70, 1010, 1010, 1130), GREEN, g.on(2, 2.0), "finish every transaction: COMMIT or ROLLBACK", None, 32)


WORDS = [("transaction", "all changes, or none"), ("before COMMIT", "only YOU see them"), ("COMMIT", "permanent, for everyone"),
         ("ROLLBACK", "undo since last COMMIT"), ("DDL", "commits automatically"), ("open transaction", "locks rows → others wait")]


def s_recap(g):
    la = g.until(0)
    for k, (kw, plain) in enumerate(WORDS):
        if la <= 0: break
        y = 330 + k * 140; lit = pr(g.bt, .8 + k * .85, 1.1 + k * .85)
        col = [YEL, CYAN, GREEN, PINK, RED, PURP][k]
        g.d.rounded_rectangle((70, y, 1010, y + 118), 22, fill=mix(CARD, la), outline=mix(col, la * (.25 + .75 * lit)), width=3)
        badge(g, 140, y + 59, k + 1, col, la * (.3 + .7 * lit), 32)
        tx(g, 205, y + 59, kw, MB(32), col, la * (.3 + .7 * lit), "lm")
        tx(g, 985, y + 59, plain, SN(30), WHITE, la * lit, "rm")
    if g.b == 1:
        tx(g, 540, 520, "Next video", SB(48), DIM, g.on(1, .2), "mm")
        tx(g, 540, 620, "Indexes from zero", XB(72), YEL, g.on(1, .5), "mm")
        tx(g, 540, 720, "why some queries are instant", SN(38), WHITE, g.on(1, .8), "mm")
        p = 1 + .04 * math.sin(g.t * 7); bw, bh = 760 * p, 130 * p; ab = g.on(1, 1.2)
        g.d.rounded_rectangle((540 - bw / 2, 920 - bh / 2, 540 + bw / 2, 920 + bh / 2), 65, fill=mix(GREEN, ab))
        tx(g, 540, 920, "@sql_developer_no1", SB(54), INK, ab, "mm")
        tx(g, 540, 1060, "follow · save · share", SN(42), DIM, g.on(1, 1.6), "mm")


SCENES = [
    ("A transfer goes wrong", RED, s_hook, [
        "Ali sends one hundred manats to Sara. First, Ali's balance goes *down* by one hundred.",
        "And right then, the power goes out. Sara never got the money. Did one hundred manats *disappear*?",
        "No. The database puts it *back*. Let's see how."]),
    ("Pencil and pen", ORANGE, s_pencil, [
        "Think of every change as written in *pencil*. It's there, but it's not final yet.",
        "*COMMIT* rewrites it in *pen*. Now it's permanent, and everyone can see it.",
        "*ROLLBACK* is the *eraser*. It removes the pencil, and everything is as it was.",
        "All the changes between two commits form one *transaction*: all of them are saved, or *none*."]),
    ("Your changes are private", CYAN, s_private, [
        "Before you commit, *you* already see the new balance: nine hundred.",
        "But your colleague, in another session, still sees the *old* value: one thousand.",
        "Only after *COMMIT* does everyone see nine hundred.",
        "That's why nobody ever sees *half-finished* work."]),
    ("ROLLBACK: undo everything", PINK, s_rollback, [
        "Two updates, and then a delete that was a *mistake*.",
        "*ROLLBACK* undoes *all* of them, back to the last commit. Ali and Sara have their old balances.",
        "And if the session *crashes*, Oracle does this rollback *automatically*. That's what saved Ali's money."]),
    ("The silent COMMIT", RED, s_ddl, [
        "Now a trap. You set every balance to zero. Then you create a table. Then you roll back.",
        "But commands like *CREATE TABLE* do a *secret commit*, before and after themselves.",
        "So your update was *already committed*. The rollback has nothing left to undo.",
        "These commands are called *DDL*: create, alter, drop, and truncate. Be careful with them."]),
    ("Don't forget to finish", PURP, s_lock, [
        "One more thing. A row you changed is *locked* until you commit or roll back.",
        "If a colleague wants to change the same row, they *wait*.",
        "So always *finish* your transaction. Forgetting it can make a whole team wait."]),
    ("Remember", GREEN, s_recap, [
        "Remember: a transaction is all or nothing. Only you see your changes until you commit. Rollback undoes them. DDL commits by itself. And always finish what you start.",
        "Next: *indexes* from zero. Why some queries are instant. Follow, so you don't miss it."]),
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    run(SCENES, Stage(1080, 1920, 30), "/home/claude/v2/out55", "/home/claude/en/sql_video55_EN_commit_rollback.mp4", mode, seed=55, max_dur=175)

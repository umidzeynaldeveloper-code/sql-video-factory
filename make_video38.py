from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def clock(d, cx, cy, r, hh, mm, col, a):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=mix(CARD, a), outline=mix(col, a), width=6)
    for k in range(12):
        an = k * math.pi / 6
        d.line((cx + (r - 18) * math.sin(an), cy - (r - 18) * math.cos(an), cx + (r - 6) * math.sin(an), cy - (r - 6) * math.cos(an)), fill=mix(DIM, a), width=4)
    am = mm / 60 * 2 * math.pi; ah = ((hh % 12) + mm / 60) / 12 * 2 * math.pi
    d.line((cx, cy, cx + r * .75 * math.sin(am), cy - r * .75 * math.cos(am)), fill=mix(WHITE, a), width=6)
    d.line((cx, cy, cx + r * .5 * math.sin(ah), cy - r * .5 * math.cos(ah)), fill=mix(col, a), width=10)
    d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=mix(col, a))


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "02:00 · who starts the night batch?", SB(46), WHITE, a)
        mm = min(59, lt * 20) if lt < 3 else 0
        hh = 1 if lt < 3 else 2
        clock(d, 300, 520, 150, hh, mm, YEL, a)
        ab = pr(lt, 1, 1.4) * fo
        glow_box(d, (520, 380, 1010, 500), RED, ab, "cron on an app server", "server down = no batch", 30, 24)
        ag = pr(lt, 3, 3.4) * fo
        glow_box(d, (520, 560, 1010, 680), GREEN, ag, "DBMS_SCHEDULER", "inside the database", 34, 24)
        if lt > 3:
            p = (lt - 3) % 1.2 / 1.2
            d.ellipse((450 + 60 * p - 12, 620 - 12, 450 + 60 * p + 12, 620 + 12), fill=mix(GREEN, ag))
        caption(d, "The database can run its own jobs: on time, with history, retries and dependencies.", pr(lt, 4, 4.4) * fo)

    # 1 BUILDING BLOCKS
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Three building blocks", SB(54), CYAN, a)
        glow_box(d, (70, 330, 510, 500), PURP, pr(lt, .6, 1) * fo, "PROGRAM", "WHAT runs", 40, 28)
        glow_box(d, (570, 330, 1010, 500), YEL, pr(lt, 2.5, 2.9) * fo, "SCHEDULE", "WHEN it runs", 40, 28)
        aj = pr(lt, 4.5, 4.9) * fo
        flow(d, [(290, 500), (290, 580), (540, 640)], PURP, aj, t, pr(lt, 4.5, 5.3))
        flow(d, [(790, 500), (790, 580), (540, 640)], YEL, aj, t, pr(lt, 4.5, 5.3))
        glow_box(d, (290, 640, 790, 800), GREEN, pr(lt, 5.3, 5.7) * fo, "JOB", "program + schedule", 44, 28)
        card_list(d, 860, [("procedure · PL/SQL block · executable", PURP, 7),
                           ("one schedule → many jobs", YEL, 8.2),
                           ("simple job: everything inline", CYAN, 9.4)], lt, fo, 80, 31)
        caps = ["A program says what to run: a stored procedure, an anonymous PL/SQL block, or an external executable.",
                "A schedule says when. A job connects the two, and can be enabled, disabled, run or stopped.",
                "One schedule can drive many jobs. For a simple case, put everything inline in a single job."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 8.2 else 2], pr(lt, .6, 1) * fo)

    # 2 CREATE_JOB
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "One call creates the job", SB(52), GREEN, a)
        code(d, 300, [("DBMS_SCHEDULER.CREATE_JOB(", WHITE),
                      ("  job_name        => 'NIGHT_BATCH',", CYAN),
                      ("  job_type        => 'STORED_PROCEDURE',", PURP),
                      ("  job_action      => 'batch_pkg.process_all',", PURP),
                      ("  start_date      => SYSTIMESTAMP,", YEL),
                      ("  repeat_interval => 'FREQ=DAILY;BYHOUR=2;BYMINUTE=0',", YEL),
                      ("  enabled         => TRUE);", GREEN)], a, 24)
        at = pr(lt, 4, 4.4) * fo
        d.line((100, 820, 980, 820), fill=mix(DIM, at), width=4)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        for k, dy in enumerate(days):
            x = 160 + k * 190; al = pr(lt, 4.6 + k * .7, 5 + k * .7) * fo
            d.ellipse((x - 16, 804, x + 16, 836), fill=mix(GREEN, al))
            ct(d, 850, dy, SB(28), WHITE, al, x); ct(d, 890, "02:00 ✓", SN(26), GREEN, al, x)
        caps = ["One call creates the job: a name, what to run, when to start, how often to repeat, and enabled true.",
                "From now on, Oracle starts it every night at two. No cron, no external server, no forgotten script."]
        caption(d, caps[0 if lt < 6 else 1], pr(lt, .6, 1) * fo)

    # 3 CALENDAR SYNTAX
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Calendar syntax", SB(56), YEL, a)
        rows = [("FREQ=DAILY;BYHOUR=2", "every night 02:00", GREEN),
                ("FREQ=WEEKLY;BYDAY=MON-FRI", "work days only", CYAN),
                ("FREQ=MINUTELY;INTERVAL=15", "every 15 minutes", PURP),
                ("FREQ=MONTHLY;BYMONTHDAY=-1", "last day of month", PINK)]
        for k, (s_, ex, col) in enumerate(rows):
            y = 320 + k * 135; al = pr(lt, .6 + k * 1.6, 1 + k * 1.6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 115), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((100, y + 16), s_, font=MN(30), fill=mix(col, al))
            d.text((100, y + 62), "→ " + ex, font=SN(30), fill=mix(WHITE, al))
        code(d, 880, [("DBMS_SCHEDULER.EVALUATE_CALENDAR_STRING(…)", YEL), ("→ shows the next run dates BEFORE you go live", GREEN)], pr(lt, 8, 8.4) * fo, 24)
        caps = ["The repeat interval is a calendar string: frequency first, then by-hour, by-day, by-month-day and more.",
                "Work days only, every fifteen minutes, or the last day of every month: minus one means the last day.",
                "Not sure what you wrote? Evaluate calendar string returns the next run dates, so you can test it first."]
        caption(d, caps[0 if lt < 3.8 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 4 CHAINS
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Chains: steps with rules", SB(54), PURP, a)
        steps = [(330, "LOAD", "fx rates · payments", CYAN), (560, "CALC", "interest", PURP), (790, "REPORT", "daily totals", GREEN)]
        for k, (y, l1, l2, col) in enumerate(steps):
            al = pr(lt, .6 + k * 1.8, 1 + k * 1.8) * fo
            glow_box(d, (250, y, 830, y + 130), col, al, l1, l2, 38, 26)
            if k < 2:
                flow(d, [(540, y + 130), (540, y + 230)], GREEN, al, t, pr(lt, 1.4 + k * 1.8, 2.2 + k * 1.8))
                ct(d, y + 160, "SUCCEEDED", SB(24), GREEN, al, 700)
        ae = pr(lt, 6.5, 6.9) * fo
        flow(d, [(830, 625), (950, 625), (950, 990)], RED, ae, t, pr(lt, 6.5, 7.3))
        glow_box(d, (620, 990, 1010, 1100), RED, pr(lt, 7.3, 7.7) * fo, "ALERT step", "on FAILED", 32, 24)
        caps = ["A chain runs several steps in order. Each step is a program, and rules decide what starts next.",
                "Load finishes, so calculation starts. Calculation succeeds, so the report runs.",
                "And if a step fails, a rule can start a different step instead: for example an alert. Dependencies live in the database."]
        caption(d, caps[0 if lt < 2.4 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 5 MONITORING
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Did it run? Ask Oracle", SB(54), CYAN, a)
        code(d, 300, [("SELECT log_date, status, error#, run_duration", CYAN),
                      ("FROM   user_scheduler_job_run_details", CYAN),
                      ("WHERE  job_name = 'NIGHT_BATCH';", CYAN)], a, 26)
        hdr = pr(lt, 1.5, 1.9) * fo
        d.rounded_rectangle((70, 490, W - 70, 550), 12, fill=mix(CARD, hdr))
        for x, h in ((95, "date"), (330, "status"), (620, "error#"), (790, "duration")):
            d.text((x, 503), h, font=SB(28), fill=mix(DIM, hdr))
        data = [("27 Oct", "SUCCEEDED", "0", "00:41:12", GREEN), ("28 Oct", "SUCCEEDED", "0", "00:43:05", GREEN),
                ("29 Oct", "FAILED", "1652", "00:12:40", RED), ("30 Oct", "SUCCEEDED", "0", "00:40:58", GREEN)]
        for k, (dt_, st, er, du, col) in enumerate(data):
            y = 565 + k * 70; al = pr(lt, 2 + k * .6, 2.4 + k * .6) * fo
            d.rounded_rectangle((70, y, W - 70, y + 60), 10, fill=mix(CARD, al), outline=mix(col, al * .6), width=2)
            for x, v, c in ((95, dt_, WHITE), (330, st, col), (620, er, col), (790, du, WHITE)):
                d.text((x, y + 13), v, font=MN(28), fill=mix(c, al))
        card_list(d, 870, [("USER_SCHEDULER_JOBS → state, next_run_date", YEL, 6.5),
                           ("USER_SCHEDULER_RUNNING_JOBS → running now", PURP, 8)], lt, fo, 80, 30)
        caps = ["Every run is logged. Job run details shows the status, the error number and how long it took.",
                "One failed night stands out immediately, with its error number: here O R A sixteen fifty two, temp space.",
                "Scheduler jobs shows the state and the next run date. Running jobs shows what's running right now."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 6 PITFALLS
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Four classic traps", SB(54), RED, a)
        at = a
        d.line((100, 420, 980, 420), fill=mix(DIM, at), width=4)
        ct(d, 320, "run every 15 min · one run takes 25 min", SN(30), WHITE, at)
        d.rounded_rectangle((120, 395, 120 + 25 * 26, 445), 12, fill=mix(CYAN, at))
        for k, x in enumerate((120, 120 + 15 * 26, 120 + 30 * 26)):
            d.line((x, 375, x, 465), fill=mix(YEL, at), width=4)
        ct(d, 470, "a job never overlaps itself → next run waits", SB(28), GREEN, pr(lt, 1.2, 1.6) * fo)
        card_list(d, 560, [("start_date without a region → DST shifts the time", YEL, 3.5),
                           ("JOB_QUEUE_PROCESSES = 0 → nothing runs", RED, 5.5),
                           ("max_failures reached → state BROKEN", PINK, 7.5),
                           ("check failure_count, not only 'enabled'", CYAN, 9)], lt, fo, 90, 30)
        caps = ["A job never runs twice at the same time. If one run takes longer than the interval, the next one simply waits.",
                "Give start date a region time zone, so daylight saving doesn't shift your job. And job queue processes zero means no job runs at all.",
                "With max failures set, a job that keeps failing ends up broken. Check the failure count, not only enabled."]
        caption(d, caps[0 if lt < 3.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 7 DBMS_JOB LEGACY
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Still using DBMS_JOB?", SB(54), YEL, a)
        glow_box(d, (70, 330, 510, 520), DIM, a, "DBMS_JOB", "job number · interval string", 38, 26)
        ag = pr(lt, 2, 2.4) * fo
        flow(d, [(510, 425), (570, 425)], GREEN, ag, t, pr(lt, 2, 2.6))
        glow_box(d, (570, 330, 1010, 520), GREEN, ag, "DBMS_SCHEDULER", "names · calendars · logs", 34, 26)
        card_list(d, 590, [("19c+: DBMS_JOB jobs run as scheduler jobs", CYAN, 4),
                           ("RUN_JOB · STOP_JOB · DISABLE · ENABLE", PURP, 6),
                           ("new code → DBMS_SCHEDULER only", GREEN, 8)], lt, fo, 90, 31)
        caps = ["The old DBMS JOB package still works, but it's legacy.",
                "Since 19c, DBMS JOB jobs are implemented as scheduler jobs anyway. Run, stop, disable and enable are all one call.",
                "For new code, use DBMS SCHEDULER only: real names, readable calendars, and a full run history."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Job", "→ program + schedule"), ("Calendar", "→ FREQ=DAILY;BYHOUR=2"),
                          ("Chain", "→ steps + rules"), ("Run details", "→ status & error#"),
                          ("No overlap", "→ next run waits")],
              "Let the database run your batches, and let it keep the history.", 400)
    else:
        cta(d, t - T[9], "SEQUENCES & IDENTITY", "why gaps are normal", 64)
    return im


if __name__ == "__main__":
    preview(frame, T, "v38_sheet.png")

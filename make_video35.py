from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

def block(d, x0, y0, x1, y1, title, col, a, hl=False):
    d.rounded_rectangle((x0, y0, x1, y1), 16, outline=mix(RED if hl else col, a), width=5 if hl else 3, fill=mix(CARD, a * .6))
    d.text((x0 + 20, y0 + 10), title, font=SB(28), fill=mix(RED if hl else col, a))

def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Batch done ✓ … but balances are wrong", SB(42), WHITE, a)
        code(d, 320, [("EXCEPTION", RED), ("  WHEN OTHERS THEN", RED), ("    NULL;   -- \"just in case\"", RED)], pr(lt, .8, 1.2) * fo, 34)
        ab = pr(lt, 2.2, 2.6) * fo
        bar(d, 110, 600, 970, 44, .6, YEL, ab, "accounts processed", "600 000 of 1 000 000")
        ct(d, 740, "The error happened. Nobody saw it.", SB(42), RED, pr(lt, 3, 3.4) * fo)
        caption(d, "WHEN OTHERS THEN NULL is the most expensive line in PL/SQL. Let's handle errors properly.", pr(lt, 4, 4.4) * fo)

    # 1 PROPAGATION
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "An exception bubbles UP", SB(54), WHITE, a)
        block(d, 70, 320, 1010, 960, "batch_pkg.run_day", CYAN, a, hl=lt > 6.5)
        block(d, 130, 400, 950, 900, "interest.accrue", PURP, a, hl=4.5 < lt <= 6.5)
        block(d, 190, 480, 890, 840, "calc_rate", PINK, a, hl=2.5 < lt <= 4.5)
        ab = pr(lt, 1, 1.4) * fo
        d.rounded_rectangle((250, 600, 830, 680), 12, fill=mix((60, 22, 34), ab))
        ct(d, 618, "ZERO_DIVIDE  (ORA-01476)", MB(30), RED, ab)
        if lt > 2.5:
            y = lerp(600, 330, pr(lt, 2.5, 6.5))
            d.ellipse((520, y - 22, 560, y + 18), fill=mix(RED, a))
        card_list(d, 1000, [("no handler here? → goes to the caller", YEL, 3),
                            ("handled? → the error STOPS there", GREEN, 7.5)], lt, fo, 80, 30)
        caps = ["When an error is raised, Oracle looks for a handler in the current block.",
                "If there isn't one, the exception travels up to the caller, then its caller, all the way to the top.",
                "The first handler that catches it decides what happens next. If it swallows the error, nobody above ever knows."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 2 WHEN OTHERS THEN NULL
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The error swallower", SB(56), RED, a)
        for k in range(10):
            x = 90 + k * 92; st = .8 + k * .45
            al = pr(lt, st, st + .3) * fo
            state = "ok" if k < 6 else "err" if k == 6 else "skip"
            col = GREEN if state == "ok" else RED if state == "err" else OFFB
            d.rounded_rectangle((x, 340, x + 80, 420), 10, fill=mix(col, al))
            ct(d, 360, "✓" if state == "ok" else "✗" if state == "err" else "?", SB(32), BG, al, x + 40)
        ab = pr(lt, 4, 4.4) * fo
        glow_box(d, (110, 490, 970, 610), RED, ab, "WHEN OTHERS THEN NULL", "error erased", 36, 28)
        ct(d, 660, "caller sees: SUCCESS ✓", SB(38), GREEN, pr(lt, 5.5, 5.9) * fo)
        ct(d, 720, "→ COMMIT of half-done work", SB(38), RED, pr(lt, 6.5, 6.9) * fo)
        card_list(d, 820, [("no log, no alert, no rollback", RED, 8),
                           ("compiler warns: PLW-06009", YEL, 9.5)], lt, fo, 80, 30)
        caps = ["The batch processes six accounts, the seventh fails, and the error is caught by when others then null.",
                "To the caller, everything succeeded. The rest is skipped, and the half-done work gets committed.",
                "No log, no alert. Oracle even has a compiler warning for it: P L W zero six zero zero nine."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 3 LOG + RAISE with BACKTRACE
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Log it. Then RAISE.", SB(56), GREEN, a)
        code(d, 310, [("EXCEPTION WHEN OTHERS THEN", GREEN), ("  log_error(", WHITE),
                      ("    DBMS_UTILITY.FORMAT_ERROR_STACK,", CYAN), ("    DBMS_UTILITY.FORMAT_ERROR_BACKTRACE);", CYAN),
                      ("  RAISE;", YEL)], a, 28)
        ab = pr(lt, 3, 3.4) * fo
        code(d, 640, [("ORA-01476: divisor is equal to zero", RED), ("ORA-06512: at \"APP.CALC_RATE\", line 42", YEL),
                      ("ORA-06512: at \"APP.INTEREST\", line 118", WHITE), ("ORA-06512: at \"APP.NIGHT_BATCH\", line 905", WHITE)], ab, 26)
        d.rounded_rectangle((82, 700, 960, 740), 8, outline=mix(YEL, pr(lt, 5, 5.4) * fo), width=3)
        card_list(d, 900, [("BACKTRACE = the exact line that failed", YEL, 6),
                           ("RAISE = the caller still knows", GREEN, 8)], lt, fo, 80, 30)
        caps = ["If you catch everything, do two things: log it, and raise it again.",
                "Format error stack gives the message. Format error backtrace gives the exact package and line where it started.",
                "Line forty two of calc rate. And the plain raise keeps the error moving up, so the caller still knows."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 4 AUTONOMOUS LOG
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "A log that survives ROLLBACK", SB(50), PURP, a)
        code(d, 310, [("PROCEDURE log_error(…) IS", PURP), ("  PRAGMA AUTONOMOUS_TRANSACTION;", YEL),
                      ("BEGIN", PURP), ("  INSERT INTO err_log …;  COMMIT;", WHITE), ("END;", PURP)], a, 28)
        rb = lt > 5
        am = pr(lt, 1.5, 1.9) * fo
        glow_box(d, (90, 640, 500, 800), RED if rb else CYAN, am, "main transaction", "ROLLED BACK" if rb else "updates…", 32, 28)
        glow_box(d, (580, 640, 990, 800), GREEN, pr(lt, 3, 3.4) * fo, "err_log row", "COMMITTED ✓", 32, 28)
        if lt > 3: arrow(d, 500, 720, 580, 720, PURP, pr(lt, 3, 3.4) * fo, 5)
        if rb:
            ar = pr(lt, 5, 5.4) * fo
            d.line((110, 660, 480, 780), fill=mix(RED, ar), width=6)
        card_list(d, 870, [("independent transaction: own COMMIT", PURP, 6.5),
                           ("use it ONLY for logging", YEL, 8)], lt, fo, 80, 30)
        caps = ["A problem: if you insert the log row in the same transaction, the rollback deletes your log too.",
                "Mark the logging procedure with pragma autonomous transaction. It runs and commits in its own, separate transaction.",
                "The main work is rolled back, but the log row stays. Use autonomous transactions for logging, not for business logic."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 5 NAMED + USER ERRORS
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Give errors a NAME", SB(56), CYAN, a)
        code(d, 310, [("e_deadlock EXCEPTION;", CYAN), ("PRAGMA EXCEPTION_INIT(e_deadlock, -60);", CYAN), ("…", DIM),
                      ("WHEN e_deadlock THEN retry_later;", GREEN)], a, 28)
        code(d, 600, [("IF l_bal - p_amt < 0 THEN", WHITE),
                      ("  RAISE_APPLICATION_ERROR(-20010,", YEL), ("    'Insufficient funds: acc ' || p_acc);", YEL), ("END IF;", WHITE)],
             pr(lt, 4, 4.4) * fo, 28)
        card_list(d, 880, [("catch only what you can FIX", GREEN, 6.5),
                           ("-20000 … -20999 = your business errors", YEL, 8)], lt, fo, 80, 30)
        caps = ["Catch specific errors, not everything. Pragma exception init gives a name to an Oracle error number, like sixty, deadlock.",
                "Then handle exactly that case, for example by retrying later.",
                "For business rules, raise application error with a number from minus twenty thousand to minus twenty thousand nine ninety nine, and a clear message."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 4 else 2], pr(lt, .6, 1) * fo)

    # 6 WHAT GETS ROLLED BACK
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "What gets rolled back?", SB(54), YEL, a)
        steps = [("UPDATE #1", GREEN), ("UPDATE #2", GREEN), ("UPDATE #3  ✗ error", RED)]
        for k, (nm, col) in enumerate(steps):
            y = 330 + k * 90; al = pr(lt, .6 + k * .6, 1 + k * .6) * fo
            d.rounded_rectangle((110, y, 970, y + 74), 12, fill=mix(CARD, al), outline=mix(col, al), width=3)
            d.text((140, y + 20), nm, font=MB(30), fill=mix(col, al))
        ah = pr(lt, 3, 3.4) * fo
        glow_box(d, (70, 640, 520, 820), GREEN, ah, "handled", "#3 undone, #1 #2 STAY", 34, 26)
        glow_box(d, (560, 640, 1010, 820), RED, pr(lt, 5, 5.4) * fo, "unhandled to client", "whole call undone", 34, 26)
        card_list(d, 870, [("failed statement → always rolled back", WHITE, 7),
                           ("handled + COMMIT = half the work saved!", RED, 8.5)], lt, fo, 80, 30)
        caps = ["The statement that fails is always rolled back. But what about the ones before it?",
                "If you handle the exception, updates one and two stay. Commit later, and you've saved half the work.",
                "If the exception reaches the client unhandled, Oracle rolls back everything the call did. That's often the safer outcome."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    # 7 ALERT
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "From error to alert", SB(56), PINK, a)
        nodes = [(540, 360, "exception in batch", RED), (540, 540, "log_error (autonomous)", PURP),
                 (240, 740, "err_log table", CYAN), (840, 740, "alert: chat / e-mail / call", YEL)]
        for k, (x, y, nm, col) in enumerate(nodes):
            al = pr(lt, .6 + k * 1.2, 1 + k * 1.2) * fo
            glow_box(d, (x - 220, y - 55, x + 220, y + 55), col, al, nm, None, 30)
        for (x0, y0, x1, y1, st) in [(540, 415, 540, 485, 1.6), (480, 595, 300, 685, 2.8), (600, 595, 780, 685, 4)]:
            if lt > st: flow(d, [(x0, y0), (x1, y1)], WHITE, a, t, pr(lt, st, st + .6))
        card_list(d, 900, [("log: who, what, which line, which input", CYAN, 6),
                           ("alert: someone sees it at 03:00, not at 09:00", YEL, 8)], lt, fo, 80, 30)
        caps = ["In a real system, an error should end up in front of a person.",
                "Log it with the backtrace and the input that caused it, in an autonomous transaction.",
                "Then raise an alert, to a chat channel, an e-mail, or a phone call, so the night batch problem is seen at three, not at nine."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("Propagation", "→ first handler decides"), ("OTHERS NULL", "→ never. Ever."),
                          ("Log + RAISE", "→ BACKTRACE gives the line"), ("Autonomous", "→ log survives rollback"),
                          ("Named errors", "→ catch what you can fix")],
              "Handle what you can fix. Log and re-raise everything else.", 460)
    else:
        cta(d, t - T[9], "PACKAGE STATE & ORA-04068", "why deploys break sessions", 52)
    return im

if __name__ == "__main__":
    preview(frame, T, "v35_sheet.png")

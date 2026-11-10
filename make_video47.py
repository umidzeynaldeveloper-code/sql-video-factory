from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "November report", SB(56), WHITE, a)
        code(d, 330, [("WHERE created BETWEEN DATE '2026-11-01'", CYAN), ("                  AND DATE '2026-11-30'", CYAN)], a, 28)
        glow_box(d, (200, 560, 880, 720), RED, pr(lt, 1.5, 1.9) * fo, "Nov 30 payments: missing", "but they're in the table", 40, 30)
        caption(d, "Every payment is there. The report still misses the last day. Why?", pr(lt, 3, 3.4) * fo)

    # 1 DATE HAS TIME
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "A DATE always has a time", SB(52), YEL, a)
        parts = ["2026", "11", "30", "00", "00", "00"]; lbl = ["year", "month", "day", "hour", "min", "sec"]
        for k in range(6):
            x = 80 + k * 155; al = pr(lt, .6 + k * .3, 1 + k * .3) * fo; col = CYAN if k < 3 else YEL
            d.rounded_rectangle((x, 360, x + 140, 480), 16, fill=mix(CARD, al), outline=mix(col, al), width=3)
            ct(d, 385, parts[k], MB(40), col, al, x + 70); ct(d, 500, lbl[k], SN(26), DIM, al, x + 70)
        code(d, 610, [("DATE '2026-11-30'  =  2026-11-30 00:00:00", GREEN)], pr(lt, 4, 4.4) * fo, 28)
        card_list(d, 760, [("no fractions · no time zone", WHITE, 7)], lt, fo, 90, 32)
        caps = ["An Oracle date stores year, month, day, hours, minutes and seconds.",
                "A date literal without a time means exactly midnight.",
                "No fractional seconds and no time zone in a DATE."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 2 HALF-OPEN RANGE
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "BETWEEN stops at midnight", SB(52), RED, a)
        d.line((100, 420, 980, 420), fill=mix(DIM, a), width=4)
        for x, lb in ((140, "Nov 1"), (640, "Nov 30 00:00"), (940, "Dec 1")):
            d.ellipse((x - 12, 408, x + 12, 432), fill=mix(WHITE, a)); ct(d, 340, lb, SB(28), WHITE, a, x)
        d.rounded_rectangle((140, 450, 640, 490), 20, fill=mix(CYAN, pr(lt, 1, 1.4) * fo))
        d.rounded_rectangle((640, 450, 940, 490), 20, fill=mix(RED, pr(lt, 2.5, 2.9) * fo))
        ct(d, 510, "Nov 30 10:15 → outside ✗", SB(32), RED, pr(lt, 3, 3.4) * fo, 790)
        code(d, 640, [("WHERE created >= DATE '2026-11-01'", GREEN), ("  AND created <  DATE '2026-12-01'", GREEN)], pr(lt, 6, 6.4) * fo, 30)
        ct(d, 830, "half-open range ✓ · index friendly ✓", SB(36), GREEN, pr(lt, 8, 8.4) * fo)
        caps = ["Between the first and the thirtieth ends at midnight of the thirtieth.",
                "A payment at ten in the morning on the thirtieth is outside.",
                "Use greater or equal to the first, and strictly less than the next month."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 3 TIMESTAMP + ARITHMETIC
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "TIMESTAMP & arithmetic", SB(52), CYAN, a)
        code(d, 310, [("TIMESTAMP '2026-11-30 10:15:42.123456'", CYAN)], a, 28)
        ct(d, 420, "fractions: up to 9 digits (default 6)", SB(32), WHITE, pr(lt, 1.5, 1.9) * fo)
        glow_box(d, (70, 520, 1010, 660), GREEN, pr(lt, 4, 4.4) * fo, "DATE − DATE = NUMBER of days", "12 hours = 0.5", 36, 30)
        glow_box(d, (70, 720, 1010, 860), PURP, pr(lt, 7, 7.4) * fo, "TS − TS = INTERVAL DAY TO SECOND", "+00 12:00:00.000000", 36, 30)
        caps = ["Timestamp adds fractional seconds, up to nine digits.",
                "Subtract two dates and you get a number of days. Half a day is zero point five.",
                "Subtract two timestamps and you get an interval."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 4 TIME ZONES
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Whose clock?", SB(56), YEL, a)
        glow_box(d, (70, 320, 500, 480), PURP, pr(lt, .5, .9) * fo, "SYSDATE", "DB server clock", 38, 30)
        glow_box(d, (580, 320, 1010, 480), CYAN, pr(lt, 2, 2.4) * fo, "CURRENT_DATE", "session time zone", 38, 30)
        ct(d, 560, "server UTC 16:00  ·  user Baku 20:00", SB(34), RED, pr(lt, 4, 4.4) * fo)
        ct(d, 620, "+04:00 → every report 4 hours off", SB(34), RED, pr(lt, 5, 5.4) * fo)
        glow_box(d, (70, 720, 1010, 880), GREEN, pr(lt, 7.5, 7.9) * fo, "TIMESTAMP WITH LOCAL TIME ZONE", "stored normalized · shown in each session's zone", 32, 26)
        caps = ["Sysdate and systimestamp come from the database server's clock.",
                "Current date uses the session's time zone. Mix them, and reports shift by hours.",
                "With local time zone stores one moment and shows it in each user's own zone."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 5 MONTH MATH
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Adding one month", SB(56), PURP, a)
        code(d, 320, [("ADD_MONTHS(DATE '2026-01-31', 1)", GREEN)], a, 30)
        ct(d, 430, "→ 2026-02-28 ✓  end of month kept", SB(34), GREEN, pr(lt, 1.5, 1.9) * fo)
        code(d, 560, [("DATE '2026-01-31' + INTERVAL '1' MONTH", RED)], pr(lt, 4, 4.4) * fo, 30)
        glow_box(d, (100, 690, 980, 850), RED, pr(lt, 5.5, 5.9) * fo, "ORA-01839", "date not valid for month specified", 44, 30)
        caps = ["Add months to January thirty first: February twenty eighth.",
                "Oracle keeps the end of the month.",
                "An interval of one month tries February thirty first, and fails."]
        caption(d, caps[0 if lt < 4 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 6 IMPLICIT CONVERSION
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Never trust NLS", SB(56), RED, a)
        code(d, 320, [("TO_DATE('11/12/2026')   -- no format!", RED)], a, 28)
        glow_box(d, (70, 450, 500, 590), CYAN, pr(lt, 2, 2.4) * fo, "MM/DD/YYYY", "Nov 12", 34, 32)
        glow_box(d, (580, 450, 1010, 590), PURP, pr(lt, 3, 3.4) * fo, "DD/MM/YYYY", "Dec 11", 34, 32)
        ct(d, 640, "or ORA-01843: not a valid month", SB(32), YEL, pr(lt, 4.5, 4.9) * fo)
        code(d, 750, [("TO_DATE('11/12/2026', 'DD/MM/YYYY')  ✓", GREEN), ("DATE '2026-12-11'                    ✓", GREEN)], pr(lt, 6.5, 6.9) * fo, 28)
        caps = ["Without a format, to date depends on the session's NLS date format.",
                "Same text, two different dates, or an error.",
                "Always give the format, or use an ANSI date literal."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 7 CHECKLIST
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Checklist", SB(56), GREEN, a)
        card_list(d, 330, [("✓ half-open ranges: >= start AND < next", GREEN, .5),
                           ("✓ DATE literals or explicit formats", GREEN, 1.5),
                           ("✗ dates stored as VARCHAR2", RED, 2.5),
                           ("✓ one time zone strategy for the system", CYAN, 3.5),
                           ("✗ TRUNC(column) in WHERE → no index", RED, 4.5)], lt, fo, 95, 30)
        caption(d, "Store dates as dates, use half open ranges, and agree on one time zone strategy.", pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("DATE", "→ always has a time"), ("BETWEEN", "→ hides the last day"),
                          ("TS − TS", "→ INTERVAL"), ("SYSDATE", "→ server clock"),
                          ("ADD_MONTHS", "→ keeps month end")],
              "A date has a time. Use half open ranges and explicit formats.", 420)
    else:
        cta(d, t - T[9], "HIERARCHICAL QUERIES", "a whole tree in one SELECT", 56)
    return im


if __name__ == "__main__":
    preview(frame, T, "v47_sheet.png")

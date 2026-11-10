from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]


def grid(d, x, y, rows, a, cw, rh=64, hl=None):
    for k, row in enumerate(rows):
        for j, v in enumerate(row):
            xx = x + sum(cw[:j]); col = DIM if k == 0 else (hl(k, j) if hl else WHITE)
            d.rounded_rectangle((xx, y + k * rh, xx + cw[j] - 8, y + k * rh + rh - 8), 10, fill=mix(OFFB if k == 0 else CARD, a))
            d.text((xx + 16, y + k * rh + 12), v, font=MB(28), fill=mix(col, a))


LONG = [("branch", "month", "amount"), ("Baku", "JAN", "120"), ("Baku", "FEB", "140"), ("Baku", "MAR", "90"),
        ("Ganja", "JAN", "60"), ("Ganja", "FEB", "75"), ("Ganja", "MAR", "80")]
WIDE = [("branch", "jan", "feb", "mar"), ("Baku", "120", "140", "90"), ("Ganja", "60", "75", "80")]


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "Rows → columns", SB(56), WHITE, a)
        grid(d, 220, 320, LONG, a, [220, 200, 220])
        grid(d, 170, 860, WIDE, pr(lt, 2, 2.4) * fo, [220, 170, 170, 170], hl=lambda k, j: GREEN if j else WHITE)
        flow(d, [(540, 780), (540, 850)], GREEN, pr(lt, 1.6, 2) * fo, t, pr(lt, 1.6, 2.2))
        caption(d, "One row per branch and month. The manager wants months as columns. That's pivot.", pr(lt, 3, 3.4) * fo)

    # 1 OLD WAY
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The old way: CASE", SB(54), DIM, a)
        code(d, 310, [("SELECT branch,", WHITE), ("  SUM(CASE WHEN month = 'JAN'", CYAN), ("           THEN amount END) AS jan,", CYAN),
                      ("  SUM(CASE WHEN month = 'FEB'", CYAN), ("           THEN amount END) AS feb,", CYAN),
                      ("  SUM(CASE WHEN month = 'MAR'", CYAN), ("           THEN amount END) AS mar", CYAN),
                      ("FROM sales GROUP BY branch;", WHITE)], a, 27)
        caption(d, "Conditional aggregation: one sum of case per month. It works everywhere, but it grows fast.", pr(lt, .6, 1) * fo)

    # 2 PIVOT
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "11g+: PIVOT", SB(56), GREEN, a)
        code(d, 310, [("SELECT * FROM (", WHITE), ("  SELECT branch, month, amount FROM sales", CYAN), (")", WHITE),
                      ("PIVOT (", GREEN), ("  SUM(amount)", YEL), ("  FOR month IN ('JAN' AS jan,", PURP),
                      ("                'FEB' AS feb, 'MAR' AS mar)", PURP), (");", GREEN)], a, 26)
        grid(d, 170, 800, WIDE, pr(lt, 7, 7.4) * fo, [220, 170, 170, 170], hl=lambda k, j: GREEN if j else WHITE)
        caps = ["Select from an inline view with only branch, month and amount.",
                "Pivot: the aggregate, then for month, in the values you want as columns.",
                "One row per branch, one column per month."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 3 IMPLICIT GROUP BY TRAP
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Trap: hidden GROUP BY", SB(54), RED, a)
        code(d, 310, [("SELECT * FROM sales      -- has an ID column!", RED), ("PIVOT (SUM(amount) FOR month IN (…));", RED)], a, 26)
        bad = [("id", "branch", "jan", "feb"), ("1", "Baku", "120", "–"), ("2", "Baku", "–", "140"), ("3", "Baku", "–", "–")]
        grid(d, 170, 470, bad, pr(lt, 2.5, 2.9) * fo, [130, 220, 170, 170], hl=lambda k, j: RED if j == 0 else (DIM if True else WHITE))
        ct(d, 760, "every other column = a GROUP BY column", SB(34), YEL, pr(lt, 5, 5.4) * fo)
        ct(d, 830, "→ always pivot from an inline view", SB(36), GREEN, pr(lt, 8, 8.4) * fo)
        caps = ["Pivot groups by every column that isn't aggregated or pivoted.",
                "With an id in the source you get one row per id, full of empty cells.",
                "Always pivot from an inline view with only the columns you need."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 8 else 2], pr(lt, .6, 1) * fo)

    # 4 MULTIPLE AGGREGATES
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Several aggregates", SB(54), CYAN, a)
        code(d, 310, [("PIVOT (SUM(amount) AS total,", YEL), ("       COUNT(*)    AS cnt", YEL), ("  FOR month IN ('JAN' AS jan, 'FEB' AS feb))", PURP)], a, 26)
        cols = ["JAN_TOTAL", "JAN_CNT", "FEB_TOTAL", "FEB_CNT"]
        for k, c in enumerate(cols):
            x = 80 + k * 235; al = pr(lt, 3 + k * .5, 3.4 + k * .5) * fo
            d.rounded_rectangle((x, 560, x + 220, 650), 14, fill=mix(CARD, al), outline=mix(GREEN, al), width=3)
            ct(d, 586, c, MB(26), GREEN, al, x + 110)
        caption(d, "Two aggregates, two months: four columns, named value alias, underscore, aggregate alias.", pr(lt, .6, 1) * fo)

    # 5 STATIC IN LIST
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "The IN list is fixed", SB(54), YEL, a)
        code(d, 310, [("FOR month IN (SELECT month FROM …)   ✗", RED)], a, 26)
        glow_box(d, (70, 460, 500, 620), CYAN, pr(lt, 3, 3.4) * fo, "dynamic SQL", "build the IN list", 34, 28)
        glow_box(d, (580, 460, 1010, 620), PURP, pr(lt, 5, 5.4) * fo, "PIVOT XML … ANY", "result as XML", 34, 28)
        caps = ["The values in the in list must be constants. A subquery isn't allowed in normal pivot.",
                "For a dynamic list, build the statement with dynamic SQL.",
                "Or use pivot XML with any, which returns one XML column."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    # 6 UNPIVOT
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "UNPIVOT: columns → rows", SB(52), PURP, a)
        code(d, 310, [("SELECT * FROM report", WHITE), ("UNPIVOT (amount FOR month IN", PURP),
                      ("  (jan AS 'JAN', feb AS 'FEB', mar AS 'MAR'));", PURP)], a, 26)
        grid(d, 220, 520, LONG[:4], pr(lt, 3, 3.4) * fo, [220, 200, 220])
        code(d, 820, [("UNPIVOT INCLUDE NULLS (…)", YEL)], pr(lt, 7, 7.4) * fo, 28)
        caps = ["Unpivot turns columns back into rows.",
                "Each column becomes one row, with its name in month and its value in amount.",
                "Nulls are dropped by default. Include nulls keeps them."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 7 else 2], pr(lt, .6, 1) * fo)

    # 7 PERFORMANCE
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Speed?", SB(56), GREEN, a)
        bar(d, 100, 400, 980, 50, .5, CYAN, pr(lt, .5, .9) * fo, "SUM(CASE …)", "1 pass")
        bar(d, 100, 560, 980, 50, .5, GREEN, pr(lt, 2, 2.4) * fo, "PIVOT", "1 pass")
        card_list(d, 700, [("same plan: one scan + one GROUP BY", WHITE, 4), ("filter BEFORE pivot, not after", YEL, 6.5)], lt, fo, 95, 32)
        caption(d, "Pivot is about readable SQL, not speed. Filter the rows before you pivot.", pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("PIVOT", "→ rows to columns"), ("UNPIVOT", "→ columns to rows"),
                          ("Inline view", "→ no hidden groups"), ("IN list", "→ constants only"),
                          ("Nulls", "→ INCLUDE NULLS")],
              "Pivot from an inline view, and filter before you pivot.", 420)
    else:
        cta(d, t - T[9], "LONG VIDEO", "row-by-row → set-based, 50× faster", 64)
    return im


if __name__ == "__main__":
    preview(frame, T, "v50_sheet.png")

from vhelp import *
from make_video19 import code

T = T10; DUR = T[-1]

NODES = {1: ("CEO", 540, 360), 2: ("CFO", 280, 520), 3: ("CTO", 800, 520),
         4: ("Accounting", 160, 680), 5: ("Treasury", 400, 680), 6: ("Dev", 680, 680), 7: ("Ops", 920, 680)}
PARENT = {2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}


def tree(d, a, t, col=CYAN, hl=(), cut=(), ord_=None):
    for c, p in PARENT.items():
        _, x0, y0 = NODES[p]; _, x1, y1 = NODES[c]
        al = a * (.25 if c in cut else 1)
        d.line((x0, y0 + 40, x1, y1 - 40), fill=mix(DIM, al), width=4)
    for k, (nm, x, y) in NODES.items():
        al = a * (.25 if k in cut else 1)
        c = YEL if k in hl else col
        d.rounded_rectangle((x - 105, y - 40, x + 105, y + 40), 16, fill=mix(CARD, al), outline=mix(c, al), width=3)
        ct(d, y - 18, nm, SB(28), c, al, x)


def frame(i):
    t = i / FPS
    im, d = base(t, DUR)

    # 0 HOOK
    if t < T[1]:
        lt, fo = sc(t, T, 0); a = pr(lt, 0, .3) * fo
        ct(d, 230, "A whole tree in ONE SELECT?", SB(52), WHITE, a)
        tree(d, pr(lt, .5, 1.2) * fo, t)
        caption(d, "Org charts, account trees, bills of materials: every row points to its parent.", pr(lt, 3, 3.4) * fo)

    # 1 TABLE
    elif t < T[2]:
        lt, fo = sc(t, T, 1); a = pr(lt, 0, .4) * fo
        ct(d, 230, "One column holds the tree", SB(52), CYAN, a)
        rows = [("id", "parent_id", "name")] + [(str(k), str(PARENT.get(k, "NULL")), NODES[k][0]) for k in range(1, 8)]
        for k, (c1, c2, c3) in enumerate(rows):
            y = 320 + k * 72; al = pr(lt, .5 + k * .3, .9 + k * .3) * fo
            col = DIM if k == 0 else WHITE
            d.rounded_rectangle((140, y, 940, y + 62), 10, fill=mix(CARD if k else OFFB, al))
            d.text((180, y + 12), c1, font=MB(30), fill=mix(col, al))
            d.text((360, y + 12), c2, font=MB(30), fill=mix(YEL if c2 == "NULL" else (PURP if k else col), al))
            d.text((620, y + 12), c3, font=SN(30), fill=mix(col, al))
        caption(d, "An id, a parent id, a name. The root has no parent. Every other row points one level up.", pr(lt, .6, 1) * fo)

    # 2 CONNECT BY
    elif t < T[3]:
        lt, fo = sc(t, T, 2); a = pr(lt, 0, .4) * fo
        ct(d, 230, "CONNECT BY", SB(56), GREEN, a)
        code(d, 310, [("SELECT LEVEL, LPAD(' ', 2*LEVEL) || name", CYAN), ("FROM   org", WHITE),
                      ("START WITH parent_id IS NULL", YEL), ("CONNECT BY PRIOR id = parent_id;", GREEN)], a, 27)
        out = [(1, "CEO"), (2, "CFO"), (3, "Accounting"), (3, "Treasury"), (2, "CTO"), (3, "Dev"), (3, "Ops")]
        for k, (lv, nm) in enumerate(out):
            y = 560 + k * 62; al = pr(lt, 4 + k * .5, 4.4 + k * .5) * fo
            d.text((140, y), str(lv), font=MB(30), fill=mix(DIM, al)); d.text((220 + (lv - 1) * 60, y), nm, font=SB(32), fill=mix(GREEN, al))
        caps = ["Start with the roots: rows where parent id is null.",
                "Connect by prior id equals parent id: each child points to the previous row.",
                "Level gives the depth, so you can indent the names."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 3 HELPERS
    elif t < T[4]:
        lt, fo = sc(t, T, 3); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Built-in helpers", SB(56), PURP, a)
        rows = [("SYS_CONNECT_BY_PATH(name, '/')", "/CEO/CFO/Treasury", .5), ("CONNECT_BY_ISLEAF", "1 = no children", 2.5),
                ("CONNECT_BY_ROOT name", "top of the branch", 5), ("ORDER SIBLINGS BY name", "sort, keep the tree", 7.5)]
        for k, (s, ex, st) in enumerate(rows):
            y = 330 + k * 170; al = pr(lt, st, st + .4) * fo
            glow_box(d, (70, y, 1010, y + 140), PURP, al, s, ex, 32, 28)
        caps = ["Sys connect by path builds the full path, like a folder.",
                "Is leaf flags rows without children. Connect by root returns the top.",
                "Order siblings by sorts children without breaking the tree."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 7.5 else 2], pr(lt, .6, 1) * fo)

    # 4 CYCLES
    elif t < T[5]:
        lt, fo = sc(t, T, 4); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Bad data loops", SB(56), RED, a)
        glow_box(d, (120, 340, 440, 480), CYAN, a, "A", "parent = B", 44, 28)
        glow_box(d, (640, 340, 960, 480), CYAN, a, "B", "parent = A", 44, 28)
        flow(d, [(440, 380), (640, 380)], RED, pr(lt, 1, 1.4) * fo, t, pr(lt, 1, 1.6))
        flow(d, [(640, 450), (440, 450)], RED, pr(lt, 1.6, 2) * fo, t, pr(lt, 1.6, 2.2))
        glow_box(d, (100, 560, 980, 700), RED, pr(lt, 2.5, 2.9) * fo, "ORA-01436", "CONNECT BY loop in user data", 44, 30)
        code(d, 770, [("CONNECT BY NOCYCLE PRIOR id = parent_id", GREEN), ("… CONNECT_BY_ISCYCLE  -- 1 = closes a loop", GREEN)], pr(lt, 6, 6.4) * fo, 26)
        caps = ["A points to B, and B points back to A.",
                "Oracle stops with connect by loop in user data.",
                "Nocycle keeps going, and is cycle shows the row that closes the loop."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 6 else 2], pr(lt, .6, 1) * fo)

    # 5 WHERE vs CONNECT BY
    elif t < T[6]:
        lt, fo = sc(t, T, 5); a = pr(lt, 0, .4) * fo
        ct(d, 230, "WHERE vs CONNECT BY", SB(54), YEL, a)
        if lt < 5.5:
            tree(d, a, t, CYAN, cut=(3,))
            code(d, 820, [("WHERE name <> 'CTO'", RED)], a, 30)
            ct(d, 940, "CTO gone · Dev & Ops still there", SB(34), RED, pr(lt, 2, 2.4) * fo)
        else:
            tree(d, a, t, CYAN, cut=(3, 6, 7))
            code(d, 820, [("CONNECT BY PRIOR id = parent_id", GREEN), ("       AND name <> 'CTO'", GREEN)], a, 30)
            ct(d, 1010, "whole branch pruned ✓", SB(36), GREEN, pr(lt, 6.5, 6.9) * fo)
        caps = ["Where filters rows after the tree is built.",
                "Remove a manager with where, and his team still appears.",
                "Put the condition in connect by, and the whole branch is cut off."]
        caption(d, caps[0 if lt < 2 else 1 if lt < 5.5 else 2], pr(lt, .6, 1) * fo)

    # 6 RECURSIVE WITH
    elif t < T[7]:
        lt, fo = sc(t, T, 6); a = pr(lt, 0, .4) * fo
        ct(d, 230, "11gR2+: recursive WITH", SB(52), CYAN, a)
        code(d, 310, [("WITH t (id, name, lvl) AS (", CYAN), ("  SELECT id, name, 1 FROM org", YEL),
                      ("  WHERE parent_id IS NULL", YEL), ("  UNION ALL", WHITE),
                      ("  SELECT o.id, o.name, t.lvl + 1", GREEN), ("  FROM org o JOIN t ON o.parent_id = t.id", GREEN),
                      (")", CYAN), ("SEARCH DEPTH FIRST BY name SET ord", PURP),
                      ("CYCLE id SET is_cycle TO 'Y' DEFAULT 'N'", PURP), ("SELECT * FROM t ORDER BY ord;", CYAN)], a, 25)
        caps = ["The anchor member selects the roots.",
                "Union all, then the recursive member joins the next level to the previous one.",
                "Search depth first sets the order. The cycle clause catches loops."]
        caption(d, caps[0 if lt < 2.5 else 1 if lt < 6.5 else 2], pr(lt, .6, 1) * fo)

    # 7 PERFORMANCE / CHOICE
    elif t < T[8]:
        lt, fo = sc(t, T, 7); a = pr(lt, 0, .4) * fo
        ct(d, 230, "Speed & choice", SB(56), GREEN, a)
        code(d, 310, [("CREATE INDEX org_parent_ix ON org(parent_id);", GREEN)], a, 26)
        ct(d, 420, "each level = children looked up by parent", SB(30), WHITE, pr(lt, 1, 1.4) * fo)
        glow_box(d, (70, 520, 500, 700), PURP, pr(lt, 3, 3.4) * fo, "CONNECT BY", "short · Oracle-only", 36, 28)
        glow_box(d, (580, 520, 1010, 700), CYAN, pr(lt, 5, 5.4) * fo, "Recursive WITH", "ANSI · running values", 36, 28)
        caps = ["Index parent id: every level looks up children by their parent.",
                "Connect by is short and Oracle specific.",
                "Recursive with is standard SQL and can carry calculations down the tree."]
        caption(d, caps[0 if lt < 3 else 1 if lt < 5 else 2], pr(lt, .6, 1) * fo)

    elif t < T[9]:
        lt, fo = sc(t, T, 8)
        recap(d, lt, fo, [("START WITH", "→ the roots"), ("CONNECT BY PRIOR", "→ parent link"),
                          ("ORA-01436", "→ NOCYCLE"), ("WHERE", "→ filters rows only"),
                          ("parent_id", "→ index it")],
              "Start with the roots, connect by prior, and index the parent column.", 470)
    else:
        cta(d, t - T[9], "CONSTRAINTS", "the missing index that locks a table", 64)
    return im


if __name__ == "__main__":
    preview(frame, T, "v48_sheet.png")

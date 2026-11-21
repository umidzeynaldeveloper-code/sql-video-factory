"""qa.py — automated quality gates (MASTER §10). Exit code 0 = all gates passed.

python3 v21/qa.py final.mp4 [--script v21/video57.py] [--meta meta.json] [--expect 1080x1920] [--max 175] [--min 20]
The private block list is read from ~/.sqlvf_blocklist (one regex per line, written from Claude memory, never committed).
"""
import sys, os, re, json, ast, argparse, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BLOCK = os.path.expanduser("~/.sqlvf_blocklist")
SQL_START = re.compile(r"^\s*(SELECT|FROM|WHERE|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|TRUNCATE|BEGIN|DECLARE|MERGE|WITH|GROUP BY|ORDER BY|HAVING|JOIN|LEFT JOIN|INNER JOIN|COMMIT|ROLLBACK|SAVEPOINT|EXPLAIN|END|FOR|LOOP|IF|EXCEPTION|OPEN|FETCH|CLOSE|SET|VALUES|USING|ON|AND|OR|UNION)\b")
NON_ORACLE = [(r"\bLIMIT\s+\d", "LIMIT is not Oracle (use FETCH FIRST n ROWS ONLY, 12c+)"), (r"\bSELECT\s+TOP\s+\d", "TOP is SQL Server"),
              (r"\bISNULL\s*\(", "ISNULL is SQL Server (use NVL)"), (r"\bIFNULL\s*\(", "IFNULL is MySQL (use NVL)"), (r"`", "backticks are MySQL"),
              (r"\bAUTO_INCREMENT\b", "AUTO_INCREMENT is MySQL (use IDENTITY, 12c+)"), (r"\bGETDATE\s*\(", "GETDATE is SQL Server (use SYSDATE)"),
              (r"\bNOW\s*\(\s*\)", "NOW() is not Oracle (use SYSDATE / SYSTIMESTAMP)"), (r"\bSERIAL\b", "SERIAL is PostgreSQL"),
              (r"::\w", ":: casts are PostgreSQL")]


def run(a): return subprocess.run(a, capture_output=True, text=True)


def gate(res, name, ok, detail=""):
    res.append(dict(gate=name, ok=bool(ok), detail=detail)); return ok


def strings_in(obj):
    if isinstance(obj, str): yield obj
    elif isinstance(obj, dict):
        for v in obj.values(): yield from strings_in(v)
    elif isinstance(obj, list):
        for v in obj: yield from strings_in(v)


def sql_blocks(path):
    """lists of string literals in the script where at least one item looks like SQL -> joined blocks"""
    tree = ast.parse(open(path).read()); out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.List, ast.Tuple)) and node.elts and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
            vals = [e.value for e in node.elts]
            if sum(bool(SQL_START.match(v)) for v in vals) >= max(1, len(vals) // 2): out.append((node.lineno, "\n".join(vals)))
    return out


def check_sql(block):
    issues = []; code = re.sub(r"--[^\n]*", "", block)
    if code.count("'") % 2: issues.append("unbalanced single quotes")
    s = re.sub(r"'[^']*'", "", code)
    if s.count("(") != s.count(")"): issues.append("unbalanced parentheses")
    for pat, msg in NON_ORACLE:
        if re.search(pat, s, re.I): issues.append(msg)
    return issues


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--script"); ap.add_argument("--meta")
    ap.add_argument("--expect", default="1080x1920"); ap.add_argument("--max", type=float, default=175); ap.add_argument("--min", type=float, default=10)
    ap.add_argument("--fps", default="30/1"); a = ap.parse_args(); res = []
    # ---- technical
    p = run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,channels,sample_rate:format=duration",
             "-of", "json", a.video])
    gate(res, "opens", p.returncode == 0, p.stderr[-200:])
    if p.returncode: print(json.dumps(res, indent=1)); sys.exit(1)
    j = json.loads(p.stdout); v = [s for s in j["streams"] if s["codec_type"] == "video"]; au = [s for s in j["streams"] if s["codec_type"] == "audio"]
    dur = float(j["format"]["duration"])
    gate(res, "video stream h264", v and v[0]["codec_name"] == "h264", v[0]["codec_name"] if v else "none")
    gate(res, "resolution", v and f"{v[0]['width']}x{v[0]['height']}" == a.expect, f"{v[0]['width']}x{v[0]['height']}" if v else "")
    gate(res, "constant fps", v and v[0]["r_frame_rate"] == a.fps and v[0]["avg_frame_rate"] == a.fps, f"{v[0]['r_frame_rate']} / {v[0]['avg_frame_rate']}" if v else "")
    gate(res, "audio aac stereo 48k", au and au[0]["codec_name"] == "aac" and au[0]["channels"] == 2 and au[0]["sample_rate"] == "48000",
         f"{au[0]['codec_name']} {au[0]['channels']}ch {au[0]['sample_rate']}" if au else "no audio")
    gate(res, "duration", a.min <= dur <= a.max, f"{dur:.1f}s (allowed {a.min}-{a.max})")
    d = run(["ffmpeg", "-v", "error", "-i", a.video, "-f", "null", "-"])
    gate(res, "decodes to the end", d.returncode == 0 and not d.stderr.strip(), d.stderr[-300:])
    # ---- audio
    import audio as A
    L = A.loudness(a.video)
    gate(res, "loudness -14±1 LUFS", abs(L["I"] + 14) <= 1, f"I={L['I']} LUFS")
    gate(res, "true peak <= -1.0 dBTP", L["TP"] <= -1.0, f"TP={L['TP']} dBTP")
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-f", "f32le", "-ac", "2", "-"], capture_output=True)
    x = np.frombuffer(r.stdout, np.float32); clip = int((np.abs(x) >= .999).sum())
    gate(res, "no clipping", clip == 0, f"{clip} samples at full scale")
    # ---- text / metadata
    texts = []
    if a.script: texts.append(("script", open(a.script).read()))
    meta = json.load(open(a.meta)) if a.meta else None
    if meta is not None:
        texts.append(("meta", json.dumps(meta, ensure_ascii=False)))
        bad = [s[:40] for s in strings_in(meta) if "<" in s or ">" in s]
        gate(res, "no < > in metadata", not bad, "; ".join(bad))
        for k, item in (meta.items() if isinstance(meta, dict) else []):
            if isinstance(item, dict):
                if "ig" in item: n = len(re.findall(r"#\w+", item["ig"])); gate(res, f"[{k}] IG hashtags <= 5", n <= 5, f"{n}")
                if "title" in item: gate(res, f"[{k}] title without number", not re.match(r"^\s*\d+[.)]", item["title"]), item["title"][:50])
                if "yt" in item: gate(res, f"[{k}] description starts with number", bool(re.match(rf"^\s*{re.escape(str(k))}\.\s", item["yt"])), item["yt"][:20])
    # ---- confidentiality
    if not os.path.exists(BLOCK):
        gate(res, "confidentiality block list present", False, f"{BLOCK} missing: write it from Claude memory first")
    else:
        pats = [l.strip() for l in open(BLOCK) if l.strip() and not l.startswith("#")]
        hits = [f"{name}:{m.group(0)}" for name, t in texts for pt in pats for m in re.finditer(pt, t)]
        gate(res, "confidentiality (private block list)", not hits, f"{len(pats)} patterns, hits: {hits[:5]}")
    # ---- SQL static check
    if a.script:
        probs = [f"line {ln}: {', '.join(iss)}" for ln, blk in sql_blocks(a.script) for iss in [check_sql(blk)] if iss]
        gate(res, "SQL static check (Oracle)", not probs, "; ".join(probs) or f"{len(sql_blocks(a.script))} blocks ok (static only, not executed)")
    ok = all(g["ok"] for g in res)
    for g in res: print(("PASS " if g["ok"] else "FAIL ") + g["gate"] + (f"  — {g['detail']}" if g["detail"] else ""))
    print("RESULT:", "ALL GATES PASSED" if ok else "FAILED")
    json.dump(dict(video=a.video, ok=ok, gates=res), open(os.path.splitext(a.video)[0] + ".qa.json", "w"), indent=1)
    sys.exit(0 if ok else 1)


if __name__ == "__main__": main()

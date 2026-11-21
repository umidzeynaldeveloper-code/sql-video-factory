"""(1) video51 SCENES (approved v2 video) rendered by the v2.1 engine: frames at final quality, no code changes.
   (2) 4K cost: same demo frames at 1080p-final vs 4K (scale=2) -> seconds per frame."""
import sys, os, time, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.argv = ["x"]
import engine as E
v51 = importlib.import_module("video51")
st = E.Stage21(1080, 1920, 30, cfg=dict(E.PRESETS["final"]))
t = time.time(); tl = E.run21(v51.SCENES, st, "/home/claude/v21out/compat51", "-", "frames:" + ",".join(str(x) for x in (6, 30, 60, 90, 120, 150)))
res = dict(v51_frames_ok=True, v51_duration=round(tl["dur"], 1))
import demo_new as D
times = [1.8, 5.6, 9.4, 15.6]
for name, cfg in (("1080_final_ss2", E.PRESETS["final"]), ("4k_scale2_ss1", E.PRESETS["final4k"]), ("1080_ss1", E.PRESETS["draft"])):
    s2 = E.Stage21(1080, 1920, 30, cfg=dict(cfg)); E.ST, E.SCN = s2, D.SCENES
    E.TL = E.build21(D.SCENES, "/home/claude/v21out/new_final", s2.cfg)
    t = time.time()
    for k, tt in enumerate(times): E.frame21(tt).save(f"/home/claude/v21out/compare/{name}_{k}.png")
    res[name + "_s_per_frame"] = round((time.time() - t) / len(times), 2)
json.dump(res, open("/home/claude/v21out/compare/compat_4k.json", "w"), indent=1); print(res)

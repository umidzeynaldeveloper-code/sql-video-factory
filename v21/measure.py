"""Run a render command, report wall time and peak RSS of the largest process (incl. pool workers)."""
import sys, time, subprocess, resource, json
t = time.time(); r = subprocess.run(sys.argv[2:], capture_output=True, text=True)
res = dict(name=sys.argv[1], rc=r.returncode, wall_s=round(time.time() - t, 1),
           peak_rss_mb=round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024),
           cpu_user_s=round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime, 1))
print(json.dumps(res)); open(f"/home/claude/v21out/measure_{sys.argv[1]}.json", "w").write(json.dumps(res))
if r.returncode: print(r.stdout[-1500:], r.stderr[-2500:])
else: print("\n".join(l for l in r.stdout.splitlines() if "csrc" not in l)[-600:])

#!/usr/bin/env python3
import argparse
import json
import statistics
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor


def request(url):
    started = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            ok = response.status == 200
    except Exception:
        ok = False
    return ok, (time.monotonic() - started) * 1000


parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("--clients", type=int, default=500)
args = parser.parse_args()
with ThreadPoolExecutor(max_workers=args.clients) as pool:
    results = list(pool.map(request, [args.url] * args.clients))
durations = sorted(duration for _, duration in results)
report = {
    "clients": args.clients,
    "successes": sum(ok for ok, _ in results),
    "failures": sum(not ok for ok, _ in results),
    "median_ms": round(statistics.median(durations), 2),
    "p95_ms": round(durations[int(len(durations) * 0.95) - 1], 2),
}
print(json.dumps(report, indent=2))
raise SystemExit(1 if report["failures"] else 0)

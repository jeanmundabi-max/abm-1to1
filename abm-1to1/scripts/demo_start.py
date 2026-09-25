#!/usr/bin/env python3
"""
Cold start for a demonstration. One command, from a bare company URL to a run
folder that is ready and a screen that says what happens next.

    python3 demo_start.py <client-slug> [--url https://...] [--live]

It creates the run, records whether this is a demo or a live engagement, and
prints the opening question the operator has to answer out loud. It touches no
API and spends nothing.

Why it exists: a demonstration that starts with three minutes of setup is a
demonstration nobody watches. Everything deterministic happens here so the
camera only ever sees the parts that are actually interesting.
"""
import argparse, json, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser(description="cold start for a demo run")
    ap.add_argument("client", help="short slug, lowercase, e.g. revolut")
    ap.add_argument("--url", default=None, help="the client's own website")
    ap.add_argument("--live", action="store_true",
                    help="a real engagement rather than a demonstration")
    ap.add_argument("--base", default="~/abm-runs",
                    help="where run folders live")
    a = ap.parse_args()

    run = Path(a.base).expanduser() / a.client / "abm-1to1"
    if run.exists() and any(run.iterdir()):
        print("%s already exists and is not empty. Refusing to write into it." % run)
        print("Pick another slug, or point --base somewhere else.")
        return 1

    subprocess.run([sys.executable, str(HERE / "new_run.py"), str(run)], check=True)

    # The mode is recorded, not remembered. A demo never activates, never needs
    # conversions and never needs a real budget: three blockers that stall a live
    # build simply do not apply, and the run should say which one it is.
    mode = {"mode": "live" if a.live else "demonstration",
            "client": a.client,
            "url": a.url,
            "_note": ("A demonstration never activates and never spends. Say so on camera. "
                      "A live engagement needs the LinkedIn Marketing API applied for on day "
                      "one, because approval runs four weeks at best and about four months "
                      "typically.")}
    (run / "00-inputs" / "MODE.json").write_text(json.dumps(mode, indent=1), encoding="utf-8")

    print("\n" + "=" * 68)
    print("  %s, %s" % (a.client.upper(), mode["mode"]))
    print("=" * 68)
    print("""
  export ABM_RUN_DIR=%s

  Two questions before anything else. They cost nothing now and hours later:

    1. Are we selling to this company, or are we building the campaign
       this company would run at the companies it wants as customers?

    2. When one of those companies has the problem we fix, who finds out,
       and does anyone have to write it down in public?

  The second answer decides where the evidence comes from. Their investors
  and their auditor means company filings. A regulator means the file that
  regulator publishes. Nobody means there is no list yet, and that is worth
  saying on day one rather than in week three.

  Then, at any point, where we are:

    python3 %s/status.py --run "$ABM_RUN_DIR"
""" % (run, HERE))
    return 0

if __name__ == "__main__":
    sys.exit(main())

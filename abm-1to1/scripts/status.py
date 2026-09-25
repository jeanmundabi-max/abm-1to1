#!/usr/bin/env python3
"""
Where is this run, and what is it waiting on.

    python3 status.py --run ~/abm-runs/<client>/abm-1to1

Reads the run folder and says which of the eight legs are done, which is next, and
**what it needs from the human before it can move**. It invents nothing: every line is a
file that either exists or does not.

It exists because the expensive part of this play was never the work. It was re-deriving,
at the start of every session, where the work had got to.
"""
import argparse, json, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runpaths import Run, add_run_arg

G, Y, R, D, B = "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[1m"
X = "\033[0m"
def plain(): 
    global G, Y, R, D, B, X
    G = Y = R = D = B = X = ""

CONFIG = Path(__file__).resolve().parent.parent / "config"
# new_run.py copies config/*.example.* into the run. An untouched copy is a TEMPLATE,
# not work done. Compared byte for byte rather than guessed at, so it stays true as the
# templates change. A status tool that reports a template as progress is worse than none.
TEMPLATES = {"account_list.csv": "account_list.example.csv",
             "narrow_uk.json": "narrow.example.json",
             "deploy.json": "deploy.example.json",
             "champion-search.json": "champion-search.example.json",
             "pages.json": "pages.example.json",
             "films.json": "films.example.json",
             "transcripts.json": "transcripts.example.json"}

def untouched(f):
    """True when this file is still byte-identical to the template it was copied from."""
    t = TEMPLATES.get(f.name)
    if not t: return False
    src = CONFIG / t
    try: return src.exists() and src.read_bytes() == f.read_bytes()
    except Exception: return False

def has(p, pat=None):
    """A leg is done when its artefact is on disk AND is not still the template."""
    if pat:
        return bool(list(p.glob(pat))) if p.is_dir() else False
    if not p.exists(): return False
    if p.is_file(): return p.stat().st_size > 0 and not untouched(p)
    return any(c for c in p.iterdir() if not untouched(c))

def n_rows(p):
    if not p.exists() or untouched(p): return 0
    try: return max(0, sum(1 for _ in p.open(encoding="utf-8", errors="ignore")) - 1)
    except Exception: return 0

def main():
    ap = add_run_arg(argparse.ArgumentParser(description="where this run is, and what it is waiting on"))
    ap.add_argument("--plain", action="store_true", help="no colour, for piping")
    a = ap.parse_args()
    if a.plain or not sys.stdout.isatty(): plain()
    run = Run(a.run)

    acc  = run.inputs / "accounts_merged.csv"
    if not acc.exists(): acc = run.inputs / "account_list.csv"
    cfgs = sorted(run.inputs.glob("abm_config*.json")) if run.inputs.is_dir() else []
    cfg  = {}
    for c in cfgs:
        try: cfg = json.loads(c.read_text(encoding="utf-8")); break
        except Exception: pass

    LEGS = [
      ("Part 1  What they sell", run.inputs / "CLIENT-PROFILE.md", None,
       "Are we pitching this company, or building the campaign it would run at its own targets"),
      ("Part 2  The list", acc, lambda: "%d companies" % n_rows(acc),
       "Twenty named companies to say yes to, before anything is built on them"),
      ("Part 3  Is it still true today", run.evidence, lambda: "%d file(s)" % len(list(run.evidence.glob("*.md"))),
       "Nothing, unless a figure has died"),
      ("Part 4  Who we can reach", run.campaign / "narrowing-walk.csv",
       lambda: "%d companies measured" % n_rows(run.campaign / "narrowing-walk.csv"),
       "Only if a company comes out too small to reach"),
      ("Part 5  Who decides", run.committee / "committee.csv",
       lambda: "%d named" % n_rows(run.committee / "committee.csv"),
       "Only if a name has to be bought. Free sources first"),
      ("Part 6  The page and the film", run.live, lambda: "%d page(s), %d film(s)"
       % (len(list(run.live.glob("*.html"))), len(list(run.vsl.glob("*.mp4"))) + len(list(run.live.glob("*.mp4")))),
       "You see each page and film as it is made"),
      ("Part 7  The ad", run.creative, lambda: "%d file(s)" % len(list(run.creative.glob("*"))),
       "You see every card before anything is pushed"),
      ("Part 8  The campaign, as drafts", run.campaign / "HANDOVER.html", None,
       "The daily budget. We never guess it"),
    ]

    print("\n%s%s%s" % (B, run.root, X))
    nxt = None
    for name, art, detail, asks in LEGS:
        ok = has(art)
        mark = "%sdone%s" % (G, X) if ok else "%s todo%s" % (Y, X)
        extra = ""
        if ok and detail:
            try: extra = "%s  %s%s" % (D, detail(), X)
            except Exception as ex:
                # un pass muet est ce qui laisse une casse invisible pendant des heures
                extra = "%s  (compte illisible: %s)%s" % (R, type(ex).__name__, X)
        print("  [%s] %-44s%s" % (mark, name, extra))
        if not ok and nxt is None: nxt = (name, asks)

    print()
    if nxt:
        print("%sNext:%s %s" % (B, X, nxt[0]))
        print("%sIt needs from you:%s %s" % (Y, X, nxt[1]))
    else:
        print("%sAll eight parts are done.%s" % (G, X))
        print("%sIt needs from you:%s your verdict on the previews. Going live is a separate decision, on another day." % (Y, X))

    # the three that block activation and are invisible in the folder
    print("\n%sBlocks on activation, checked every time%s" % (B, X))
    budget = (cfg.get("daily_budget") or cfg.get("dailyBudget"))
    obj = (cfg.get("objective") or {}).get("type") if isinstance(cfg.get("objective"), dict) else cfg.get("objective")
    note = str(cfg.get("_budget_note") or "")
    print("  %-38s %s" % ("daily budget confirmed by the client",
          ("%sno, %s is a placeholder until they say so%s" % (R, budget, X)) if budget and "confirmed" not in note
          else ("%syes%s" % (G, X) if budget else "%snot set%s" % (R, X))))
    print("  %-38s %s" % ("objective matches the funnel stage",
          ("%s%s%s" % (G if obj == "ENGAGEMENT" else R, obj or "not set", X))
          + ("" if obj == "ENGAGEMENT" else "  cold accounts take ENGAGEMENT")))
    print("  %-38s %s" % ("conversions attached",
          "%sneeds the client to say what counts as a result%s" % (Y, X)))
    print("  %-38s %s\n" % ("everything still DRAFT",
          "%sverify against the API, not this folder%s" % (D, X)))

if __name__ == "__main__":
    main()

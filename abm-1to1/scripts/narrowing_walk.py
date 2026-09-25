#!/usr/bin/env python3
"""
The narrowing walk. One lever at a time, with the number after each.

    python3 narrowing_walk.py --run ~/path/to/client-run
    python3 narrowing_walk.py --run ... --company "The Gym Group"

This is the beat the demonstration is built around: the terminal beside Campaign Manager,
showing the same number. Every figure is read live from LinkedIn's `audienceCounts`, and
the walk prints what each lever cost so nobody has to take the final number on trust.

**It reads. It never writes.** No campaign, no ad set, no creative, no spend.

It refuses to take the first typeahead result on trust, because that result is often a
duplicate or impostor page with zero members and the API reports it exactly like a company
that is too small. See ../knowledge-base/audience-api-behaviour.md.

The API calls live in build_campaign.py next door. This imports that module and drives its
functions rather than reimplementing them, so there is one place where a LinkedIn endpoint
is spelled out and one place to fix when one moves.

Reads <run>/00-inputs/narrow_uk.json for the levers and, if present,
<run>/00-inputs/account_list.csv or accounts.json for the companies.
"""
import argparse, csv, importlib.util, json, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runpaths import Run, add_run_arg

KIT = Path(__file__).resolve().parent

def load_kit():
    f = KIT / "build_campaign.py"
    if not f.exists():
        raise SystemExit("build_campaign.py not found beside %s" % Path(__file__).name)
    spec = importlib.util.spec_from_file_location("build_campaign", f)
    m = importlib.util.module_from_spec(spec)
    sys.modules["build_campaign"] = m
    spec.loader.exec_module(m)
    return m

SUSPECT = ("-", ".", " LTD", " LIMITED", " INC", " S.A.", " GMBH", " SRL")

def looks_like_a_clone(name):
    """Duplicate and scraped pages announce themselves in the display name."""
    n = name.strip()
    return n.endswith(("-", ".")) or (n.isupper() and len(n) > 6)

def resolve(bc, name):
    """Never take candidate[0] on trust. Print them all and say what is suspect."""
    cands = bc.typeahead_employer(name, limit=6)
    time.sleep(0.2)
    if not cands:
        print("    NO PAGE FOUND. That is not 'too small', it is the wrong name.")
        print("    Try the short name, the legal name, and the name in their LinkedIn address.")
        return None
    if len(cands) > 1:
        print("    %d pages with that name. Picking the real one, not a copy:" % len(cands))
        for c in cands:
            flag = "  <- a copycat page, skipped" if looks_like_a_clone(c["name"]) else ""
            print("      %-38s%s" % (c["name"][:38], flag))
    pick = cands[0]
    if looks_like_a_clone(pick["name"]):
        print("    STOPPING: %r looks like a copycat page." % pick["name"])
        print("    Confirm the real page by hand, then write it into the list.")
        return None
    return pick


def companies_from(run):
    """Whatever the run happens to carry. A name is enough; an org_urn skips the typeahead."""
    j = run.inputs / "accounts.json"
    if j.exists():
        d = json.loads(j.read_text(encoding="utf-8"))
        items = d if isinstance(d, list) else d.get("accounts") or list(d.values())
        out = []
        for a in items:
            if isinstance(a, dict) and (a.get("name") or a.get("company")):
                out.append({"name": a.get("name") or a.get("company"), "org_urn": a.get("org_urn")})
        if out: return out
    c = run.inputs / "account_list.csv"
    if c.exists():
        return [{"name": r.get("company") or r.get("name"), "org_urn": r.get("org_urn")}
                for r in csv.DictReader(c.open()) if (r.get("company") or r.get("name"))]
    raise SystemExit("no accounts.json or account_list.csv in %s" % run.inputs)

def main():
    ap = add_run_arg(argparse.ArgumentParser(description="size and narrow, one lever at a time"))
    ap.add_argument("--company", action="append", default=[], help="just this one. Repeatable")
    ap.add_argument("--config", default="narrow_uk.json", help="the lever file in 00-inputs/")
    a = ap.parse_args()
    run = Run(a.run)
    bc = load_kit()
    cfg = json.loads(run.need(run.inputs / a.config).read_text(encoding="utf-8"))

    geo = cfg["region"]
    funcs = cfg.get("buyer_functions") or []
    junior = cfg.get("junior_seniorities") or []
    band = cfg.get("band") or {"min": 300, "ideal_max": 1000, "hard_max": 1200}
    named = cfg.get("_functions_named") or {}

    print("Reading LinkedIn live. Nothing is written, nothing is spent.\n")
    print("What we are asking LinkedIn for, so nobody has to guess:")
    print("  where          United Kingdom" if geo == ["urn:li:geo:101165590"] else "  where          %s" % ", ".join(geo))
    print("  which teams    %s" % (", ".join(named.get(f.split(':')[-1], f.split(':')[-1]) for f in funcs) or "everyone"))
    print("  leaving out    junior roles: interns, trainees, entry level")
    print("  aiming for     %d to %d people at each company\n" % (band["min"], band["ideal_max"]))

    wanted = [c.lower() for c in a.company]
    rows = [c for c in companies_from(run) if not wanted or c["name"].lower() in wanted]
    if not rows: raise SystemExit("no matching company in the run's account list")

    results = []
    for c in rows:
        name, urn = c["name"], c.get("org_urn")
        if not urn:
            print("%-18s finding their page..." % name)
            pick = resolve(bc, name)
            if not pick:
                print(); continue
            urn = pick["urn"]
            print("    using: %s" % pick["name"])
        else:
            print("%-18s (page already confirmed)" % name)

        steps, prev = [], None
        for label, tcfg in [
            ("everyone who works there", {"geo": geo}),
            ("without junior roles",     {"geo": geo, "exclude_seniorities": junior}),
            ("only the buying teams",    {"geo": geo, "job_functions": funcs, "exclude_seniorities": junior}),
        ]:
            n, err = bc.audience_size(bc.build_targeting(urn, tcfg)); time.sleep(0.25)
            delta = "" if prev is None or n is None else "   %+d" % (n - prev)
            print("    %-22s %s%s" % (label, ("%s" % n) if n is not None else "ERROR " + str(err), delta))
            steps.append((label, n)); prev = n if n is not None else prev

        final, raw = steps[-1][1], steps[0][1]
        if final is None:                      verdict = "could not be measured"
        elif raw == 0:
            verdict = ("zero before any filter. This does NOT mean the company is too small. "
                       "It also means: wrong company page, a copycat page, or nobody there in "
                       "this country. Find out which before concluding")
        elif final == 0:
            verdict = ("too few once filtered. There are %s people in all, so the company is "
                       "real: there is simply nobody left after the filters" % raw)
        elif final < band["min"]:              verdict = "TOO FEW. LinkedIn will not run an ad below 300. Widen a filter"
        elif final <= band["ideal_max"]:       verdict = "GOOD. Right in the band"
        elif final <= band["hard_max"]:        verdict = "fine, near the top of the band"
        else:                                  verdict = "TOO MANY. Filter harder, this is not one to one yet"
        if raw and raw < 600 and final and final >= band["min"]:
            verdict += ". CAREFUL: only %s people in all, almost no room to filter" % raw
        print("    -> %s\n" % verdict)
        results.append({"company": name, "org_urn": urn,
                        **{k: v for k, v in steps}, "verdict": verdict})

    out = run.campaign / "narrowing-walk.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys())); w.writeheader(); w.writerows(results)
    print("%d companies measured. Saved to %s" % (len(results), out))
    print("Open LinkedIn on the same ad set: the last number should match, to the person.")

if __name__ == "__main__":
    main()

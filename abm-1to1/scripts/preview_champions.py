#!/usr/bin/env python3
"""
Preview the champion seat at each account: names, titles, LinkedIn. No emails.

    python3 preview_champions.py --run ~/path/to/client-run            # prices it and stops
    python3 preview_champions.py --run ~/path/to/client-run --confirm  # actually runs it

Accounts and the titles to hunt come from <run>/02-committee/champion-search.json.

Step 5 left one seat open on all four accounts: the person who runs collections day to
day. Filings and corporate websites give the C-suite and never that seat, so this is the
one part of the committee that has to be bought.

**This is NOT free.** AI Ark's people search costs 0.5 credits per result returned. It
returns name, title and LinkedIn but never an email; an email is a separate 1-credit
export that this script does not call and must not be added to.
"""
import argparse, csv, json, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runpaths import Run, add_run_arg

# The people-search client and the spend guard are NOT in this repo. This step is the one
# place the play spends money, and the provider is yours to choose, so the dependency is
# explicit rather than vendored. Put two modules on the path:
#
#   ark_client   .search_people(account, contact, size) -> results with name, title, profile
#   spend_guard  .guard(label, units, unit_cost, floor) -> refuses if it would breach a reserve
#
# Point ABM_VENDOR_PATH at the directory holding them.
if os.environ.get("ABM_VENDOR_PATH"):
    sys.path.insert(0, os.environ["ABM_VENDOR_PATH"])
try:
    from tools import ark_client as ark
    from spend_guard import guard
except ImportError:
    raise SystemExit(
        "This step needs a people-search client and a spend guard, and neither ships with\n"
        "this skill. See the comment at the top of preview_champions.py for the two functions\n"
        "it expects, then set ABM_VENDOR_PATH.\n\n"
        "You do not need this to run the play. Part 5 names the four seats from public sources\n"
        "and only the champion seat has to be bought. On the Serval run it was declined and the\n"
        "campaign still built.")

UNIT_COST = 0.5          # credits per person returned, measured
FLOOR = 200              # reserve

# accounts and titles are the client's, so they live in the run folder, not in here

def preview(domain, limit, TITLES):
    account = {"domain": ark.f_any_include([domain])}
    contact = {"experience": {"current": {"title": {"any": {"include": {"mode": "SMART", "content": TITLES}}}}}}
    try:
        r = ark.search_people(account, contact, size=limit)
    except ark.ArkError as e:
        if "400" not in str(e): raise
        contact = {"skill": ark.f_any_smart(TITLES)}          # some accounts reject nested experience
        r = ark.search_people(account, contact, size=limit)
    return r.get("content") or [], r.get("totalElements", 0)

def row(account, p):
    prof = p.get("profile") or {}
    link = p.get("link") or {}
    name = prof.get("full_name") or ((prof.get("first_name") or "") + " " + (prof.get("last_name") or "")).strip()
    return {"account": account, "name": name,
            "title": prof.get("title") or prof.get("headline") or "",
            "linkedin": link.get("linkedin") or link.get("url") or "",
            "location": (prof.get("location") or {}).get("name") if isinstance(prof.get("location"), dict) else prof.get("location") or ""}

def main():
    ap = add_run_arg(argparse.ArgumentParser(description="preview the champion seat. Costs credits."))
    ap.add_argument("--limit", type=int, default=12, help="results per account. 0.5 credits each")
    ap.add_argument("--confirm", action="store_true", help="without this it prices the run and stops")
    a = ap.parse_args()
    run = Run(a.run)
    cfg = json.loads(run.need(run.committee / "champion-search.json").read_text(encoding="utf-8"))
    ACCOUNTS, TITLES = cfg["accounts"], cfg["titles"]

    n = a.limit * len(ACCOUNTS)
    balance = ark.get_credits()                    # this GET is free
    print("AI Ark balance: %s credits" % format(balance, ",.0f"))
    print("Preview of the champion seat, %d accounts x %d results = %d results" % (len(ACCOUNTS), a.limit, n))
    print("Cost: %.1f credits. Emails are NOT included and are not pulled here.\n" % (n * UNIT_COST))
    if not a.confirm:
        print("Nothing was called. Re-run with --confirm to spend %.1f credits." % (n * UNIT_COST))
        return

    guard("Ark people preview, champion seat, %d accounts" % len(ACCOUNTS),
          "credit", UNIT_COST, n, already_have=0, balance=balance, floor=FLOOR,
          skip_cost="Step 5 stays amber and the demonstration cannot show the one seat that owns the pain")

    out, spent = [], 0.0
    for name, domain in ACCOUNTS.items():
        people, total = preview(domain, a.limit, TITLES)
        spent += len(people) * UNIT_COST
        print("%-15s %2d returned of %s matching" % (name, len(people), total))
        for p in people:
            r = row(name, p)
            out.append(r)
            print("    %-30s %s" % (r["name"][:30], r["title"][:60]))

    p = run.committee / "champion-preview.csv"
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["account", "name", "title", "linkedin", "location"])
        w.writeheader(); w.writerows(out)
    print("\n%d rows -> %s" % (len(out), p.name))
    print("Spent %.1f credits. Balance now %s." % (spent, format(ark.get_credits(), ",.0f")))

if __name__ == "__main__":
    main()

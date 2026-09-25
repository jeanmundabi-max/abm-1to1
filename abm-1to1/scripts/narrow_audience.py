#!/usr/bin/env python3
"""Narrow one company's audience to the band, one lever at a time, showing the cost of each.

    python3 narrow_audience.py --org 19857
    python3 narrow_audience.py --org 19857 --geo urn:li:geo:103644278 \
        --functions urn:li:function:13 --exclude-seniorities 1 2 3

Prints what each filter cost, so a number can be argued with rather than taken on trust.
LinkedIn will not deliver an ad set below 300 people, and that single constraint decides
which companies can be targeted at all.

Two things this refuses to do, both learned the hard way:

  - **It will not report a bare 0.** Four different situations return an identical 200 with
    total 0. Any zero here gets a follow-up call that says which one it is.
  - **It will not let you set the locale to the audience's country.** `locale` is the
    member's INTERFACE language, LinkedIn injects it into the targeting criteria server
    side, and anything but en_US is rejected there. The audience's country is carried by
    the geography, which is a separate facet.

Reads. Never writes to LinkedIn, never spends.
"""
import argparse, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import linkedin_api as L

SENIORITY = {1: "Unpaid", 2: "Training", 3: "Entry level", 4: "Senior", 5: "Manager",
             6: "Director", 7: "VP", 8: "Chief officer", 9: "Partner", 10: "Owner"}


def verdict(n, lo, hi, hard):
    if n is None:                 return "could not be measured"
    if n == 0:                    return "zero. See the diagnosis above, it is not a size"
    if n < lo:                    return "TOO FEW. LinkedIn will not run below %d. Widen a lever" % lo
    if n <= hi:                   return "GOOD. In the band"
    if n <= hard:                 return "fine, near the top of the band"
    return "TOO MANY. Filter harder, this is not one to one yet"


def main():
    ap = argparse.ArgumentParser(description="narrow one company to the band")
    ap.add_argument("--org", required=True, help="organization id or full URN")
    ap.add_argument("--geo", nargs="*", default=["urn:li:geo:103644278"])
    ap.add_argument("--functions", nargs="*", default=[],
                    help="function URNs, e.g. urn:li:function:13 for Information Technology")
    ap.add_argument("--exclude-seniorities", nargs="*", type=int, default=[1, 2, 3],
                    help="seniority numbers to exclude. Default 1 2 3, the junior tier")
    ap.add_argument("--band", nargs=3, type=int, default=[300, 1000, 1200],
                    metavar=("MIN", "IDEAL", "HARD"))
    ap.add_argument("--distribution", action="store_true",
                    help="also size each seniority separately, 10 extra calls")
    a = ap.parse_args()

    org = a.org if a.org.startswith("urn:") else "urn:li:organization:%s" % a.org
    lo, hi, hard = a.band
    ex = ["urn:li:seniority:%d" % s for s in a.exclude_seniorities]

    print("Reading LinkedIn live. Nothing is written, nothing is spent.\n")
    print("  company    %s" % org)
    print("  where      %s" % ", ".join(a.geo))
    print("  functions  %s" % (", ".join(a.functions) or "all of them"))
    print("  excluding  %s" % (", ".join(SENIORITY.get(s, str(s)) for s in a.exclude_seniorities) or "nobody"))
    print("  aiming for %d to %d\n" % (lo, hi))

    steps = [("everyone who works there", {L.FACET_EMPLOYER: [org], L.FACET_GEO: a.geo}, None)]
    if ex:
        steps.append(("without junior roles",
                      {L.FACET_EMPLOYER: [org], L.FACET_GEO: a.geo}, {L.FACET_SENIORITY: ex}))
    if a.functions:
        steps.append(("only the buying teams",
                      {L.FACET_EMPLOYER: [org], L.FACET_GEO: a.geo, L.FACET_FUNCTION: a.functions},
                      {L.FACET_SENIORITY: ex} if ex else None))

    prev, last = None, None
    for label, inc, exc in steps:
        n, err = L.size(inc, exc); time.sleep(0.2)
        delta = "" if prev is None or n is None else "   %+d" % (n - prev)
        print("    %-24s %s%s" % (label, n if n is not None else "ERROR " + str(err), delta))
        if n == 0 and label == steps[0][0]:
            print("    %-24s -> %s" % ("", L.diagnose_zero(org, a.geo)))
        prev = n if n is not None else prev
        last = n

    print("\n  -> %s" % verdict(last, lo, hi, hard))

    if a.distribution:
        print("\n  Seniority distribution, for deciding which lever to move:")
        for s in range(1, 11):
            n, _ = L.size({L.FACET_EMPLOYER: [org], L.FACET_GEO: a.geo,
                           L.FACET_SENIORITY: ["urn:li:seniority:%d" % s]}); time.sleep(0.15)
            print("    %-14s %s" % (SENIORITY[s], n))


if __name__ == "__main__":
    main()

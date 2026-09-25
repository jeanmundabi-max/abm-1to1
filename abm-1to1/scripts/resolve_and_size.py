#!/usr/bin/env python3
"""Resolve a list of companies to LinkedIn org URNs and size each audience.

    python3 resolve_and_size.py --in candidates.csv --out sized.csv --geo urn:li:geo:103644278

Input CSV needs a `company` column. A `domain` or `url` column is used as a second query
form if present, because the query string matters: "Monzo" finds the real page and
"Monzo Bank" finds nothing.

What this does that a thinner version does not: **it never reports a bare 0.** A zero from
`audienceCounts` has four possible causes and the API returns an identical 200 for all of
them. Every zero here gets a follow-up call and comes back as one of `under_floor`,
`not_in_geography`, `dead_page` or `unknown`. That distinction is the difference between
"too small for this play" and "you searched for the wrong page", and the second one is a
company you would otherwise have discarded by mistake.

Reads. Never writes to LinkedIn, never spends.
"""
import argparse, csv, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import linkedin_api as L


def slug_from(url):
    m = re.search(r"/company/([^/?]+)", str(url or ""))
    return m.group(1).strip().rstrip("/") if m else ""


def pick(candidates):
    """The best candidate, and why. Returns (candidate, reason) or (None, reason)."""
    if not candidates:
        return None, "no page found for any query form"
    clean = [c for c in candidates if not c["suspect"]]
    if not clean:
        return None, "every candidate looks like a scraped page (%d of them)" % len(candidates)
    if len(clean) == 1:
        return clean[0], "one candidate that does not look scraped"
    return clean[0], "%d plausible candidates, took the first. CHECK THIS ONE" % len(clean)


def main():
    ap = argparse.ArgumentParser(description="resolve companies to org URNs and size them")
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--out", dest="outfile", required=True)
    ap.add_argument("--geo", nargs="*", default=["urn:li:geo:103644278"],
                    help="geo URN(s). Default United States")
    a = ap.parse_args()

    rows = list(csv.DictReader(Path(a.infile).open(encoding="utf-8")))
    if not rows:
        raise SystemExit("no rows in %s" % a.infile)
    print("Sizing %d companies. Reading only, nothing is written to LinkedIn.\n" % len(rows))

    out = []
    for r in rows:
        name = (r.get("company") or r.get("name") or "").strip()
        if not name:
            continue
        cands = L.resolve(name, slug_from(r.get("url") or r.get("domain")))
        chosen, why = pick(cands)
        if not chosen:
            print("%-26s UNRESOLVED. %s" % (name[:26], why))
            out.append({**r, "org_urn": "", "audience": "", "verdict": "unresolved", "note": why})
            continue

        n, err = L.size({L.FACET_EMPLOYER: [chosen["urn"]], L.FACET_GEO: a.geo})
        time.sleep(0.2)
        if err:
            verdict, note = "error", err
        elif n == 0:
            cause = L.diagnose_zero(chosen["urn"], a.geo)
            verdict, note = cause, "zero, and the follow-up says: %s" % cause
        elif n < L.FLOOR:
            verdict, note = "below_floor", "LinkedIn will not run an ad set under %d" % L.FLOOR
        else:
            verdict, note = "ok", why

        flag = "  <- %d other candidates" % (len(cands) - 1) if len(cands) > 1 else ""
        print("%-26s %-9s %-18s %s%s" % (name[:26], n if n is not None else "-", verdict,
                                         chosen["name"][:28], flag))
        out.append({**r, "org_urn": chosen["urn"], "audience": n or 0,
                    "verdict": verdict, "note": note})

    fields = list(out[0].keys())
    with Path(a.outfile).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(out)
    ok = sum(1 for r in out if r["verdict"] == "ok")
    print("\n%d of %d usable. Written to %s" % (ok, len(out), a.outfile))
    for v in ("dead_page", "not_in_geography", "unresolved"):
        bad = [r["company"] for r in out if r["verdict"] == v]
        if bad:
            print("  %-18s %s" % (v, ", ".join(bad[:6])))
    print("\nA 'dead_page' or 'unresolved' is a SEARCH failure, not a small company. "
          "Try the legal name and the name in their LinkedIn address before dropping it.")


if __name__ == "__main__":
    main()

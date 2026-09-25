#!/usr/bin/env python3
"""The three LinkedIn read calls this play needs, and the traps in each.

Written against the LinkedIn Marketing API and against what it was actually observed to
do, which is not the same thing. Every behaviour handled here is recorded in
`knowledge-base/audience-api-behaviour.md` and `knowledge-base/linkedin-api-gotchas.md`
with the date it was probed.

The three that cost the most:

1. `audienceCounts` returns **HTTP 200 with total 0** for four different situations: a real
   company under the reporting floor, an organisation that does not exist, a real company
   with nobody in that geography, and a duplicate or impostor page. The API will not tell
   you which. `size()` returns the number; `diagnose_zero()` is what tells them apart.

2. The typeahead does not reliably return the real company, and the first result is often a
   scraped duplicate with no members. "Starling Bank" returns two dead pages and the real
   one is absent entirely. Never take candidate[0] on trust: `resolve()` returns all of them.

3. A retired `LinkedIn-Version` returns **426**, which reads like an auth failure and is not.
   The version is a parameter here so it can be moved without editing code.
"""
import json, os, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

BASE = "https://api.linkedin.com/rest"
VERSION = os.environ.get("LINKEDIN_VERSION", "202601")

FACET_EMPLOYER  = "urn:li:adTargetingFacet:employers"
FACET_GEO       = "urn:li:adTargetingFacet:profileLocations"
FACET_FUNCTION  = "urn:li:adTargetingFacet:jobFunctions"
FACET_SENIORITY = "urn:li:adTargetingFacet:seniorities"
FACET_TITLE     = "urn:li:adTargetingFacet:titles"

# LinkedIn will not deliver an ad set below this. It is the platform's floor, not a preference.
FLOOR = 300

enc = lambda s: urllib.parse.quote(str(s), safe="")


def _token():
    if os.environ.get("LINKEDIN_ACCESS_TOKEN"):
        return os.environ["LINKEDIN_ACCESS_TOKEN"]
    local = Path(__file__).resolve().parent / ".env"
    path = local if local.exists() else Path.home() / ".config/abm-1to1/secrets.env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("LINKEDIN_ACCESS_TOKEN=") and not line.startswith("#"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit(
        "No LINKEDIN_ACCESS_TOKEN. Put it in ~/.config/abm-1to1/secrets.env, or a .env beside "
        "this script to override for one run. See sops/00-preflight-and-rules.md, Step 0.")


def _headers():
    return {"Authorization": "Bearer " + _token(),
            "LinkedIn-Version": VERSION,
            "X-Restli-Protocol-Version": "2.0.0"}


def get(path, tries=3):
    """GET, with a retry on the transient codes. Returns (status, body-or-text)."""
    url = path if path.startswith("http") else BASE + path
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=_headers())
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code == 426:
                raise SystemExit(
                    "HTTP 426 from LinkedIn. The API version %s has been retired.\n"
                    "This is NOT an authentication failure and the token is probably fine.\n"
                    "Set LINKEDIN_VERSION to a current one and run again." % VERSION)
            if e.code in (429, 500, 502, 503) and attempt < tries - 1:
                time.sleep(1.5 * (attempt + 1)); continue
            return e.code, body
        except Exception as e:
            if attempt < tries - 1:
                time.sleep(1); continue
            return 0, str(e)


# --------------------------------------------------------------- resolving a company
def _looks_scraped(name):
    """Duplicate and scraped pages announce themselves in the display name.

    Observed: `Starling Bank-`, `STARLING BANK LIMITED.`, `Monzo-`. A trailing hyphen or
    full stop, or a name shouted entirely in capitals, is a page with no members attached.
    """
    n = (name or "").strip()
    return bool(n) and (n.endswith(("-", ".")) or (n.isupper() and len(n) > 6))


def typeahead(query, limit=8):
    """Candidate company pages for a query string.

    The query string matters more than it should: "Monzo" finds the real page and
    "Monzo Bank" finds nothing. Try more than one form before concluding anything.
    """
    st, body = get("/adTargetingEntities?q=typeahead&facet=%s&query=%s"
                   "&queryVersion=QUERY_USES_URNS&locale=(language:en,country:US)&count=%d"
                   % (enc(FACET_EMPLOYER), enc(query), limit))
    if st != 200 or not isinstance(body, dict):
        return []
    return [{"urn": e["urn"], "id": e["urn"].rsplit(":", 1)[-1],
             "name": e.get("name", ""), "suspect": _looks_scraped(e.get("name", ""))}
            for e in body.get("elements", [])]


def resolve(*queries):
    """Every candidate for every query form, de-duplicated, suspects flagged but NOT dropped.

    Deliberately returns the whole list. The caller decides, because the one case that
    matters is the one where every candidate is a dead page and the real company is absent
    from the results entirely. A function that silently returned "the best" would hide it.
    """
    seen, out = set(), []
    for q in [q for q in queries if q]:
        for c in typeahead(q):
            if c["urn"] in seen:
                continue
            seen.add(c["urn"]); c["matched_query"] = q; out.append(c)
        time.sleep(0.15)
    return out


# --------------------------------------------------------------- sizing an audience
def _clause(facet, urns):
    return "(or:(%s:List(%s)))" % (enc(facet), ",".join(enc(u) for u in urns))


def build_targeting(include, exclude=None):
    """include/exclude are {facet: [urns]}. Returns the targetingCriteria expression."""
    inc = ",".join(_clause(f, u) for f, u in include.items() if u)
    expr = "(include:(and:List(%s))" % inc
    if exclude:
        # exclude takes the facets bare inside one or:(), not wrapped the way include is
        parts = ",".join("%s:List(%s)" % (enc(f), ",".join(enc(u) for u in urns))
                         for f, urns in exclude.items() if urns)
        if parts:
            expr += ",exclude:(or:(%s))" % parts
    return expr + ")"


def size(include, exclude=None):
    """The audience count. Returns (count, error). A count of 0 is NOT an answer on its own.

    Only one response here is unambiguous: HTTP 400 means the URN is malformed, which is a
    bug in the caller. Everything else that goes wrong arrives as 200 with total 0.
    """
    st, body = get("/audienceCounts?q=targetingCriteriaV2&targetingCriteria=%s"
                   % build_targeting(include, exclude))
    if st == 400:
        return None, "malformed targeting expression (HTTP 400). A URN is wrong."
    if st != 200 or not isinstance(body, dict):
        return None, "HTTP %s %s" % (st, str(body)[:120])
    els = body.get("elements") or []
    return (els[0].get("total") if els else 0), None


def diagnose_zero(org_urn, geo_urns):
    """A 0 has four possible causes. This separates them, which the API will not do for you.

    Returns one of:
      under_floor      real company, real presence, just below LinkedIn's reporting minimum
      not_in_geography real company, nobody in the region you asked about
      dead_page        the URN resolves but has no members anywhere: a duplicate or impostor
      unknown          the follow-up call failed, so nothing is claimed
    """
    n, err = size({FACET_EMPLOYER: [org_urn]})          # same company, no geography at all
    if err is not None:
        return "unknown"
    if n and n > 0:
        # It has members somewhere. Either they are not where you looked, or the slice is small.
        return "not_in_geography" if geo_urns else "under_floor"
    return "dead_page"

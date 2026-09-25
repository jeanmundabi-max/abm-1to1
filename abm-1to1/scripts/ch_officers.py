#!/usr/bin/env python3
"""
Companies House officers for a named company. Free, authoritative, dated.

    python3 ch_officers.py "The Gym Group"          # search, then list officers
    python3 ch_officers.py --number 08528493

Step 5 rule: a committee derived from a filing is evidence, one guessed from LinkedIn
titles is a hypothesis. This is the floor of the evidence ladder for a private company,
and the risk-ownership table of a listed one sits above it.
"""
import base64, json, sys, urllib.parse, urllib.request
from pathlib import Path

def env(k):
    for line in Path.home().joinpath(".config/abm-1to1/secrets.env").read_text().splitlines():
        line = line.strip()
        if line.startswith(k + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no " + k)

KEY = env("COMPANIES_HOUSE_API_KEY")
AUTH = "Basic " + base64.b64encode((KEY + ":").encode()).decode()

def get(path, **params):
    url = "https://api.company-information.service.gov.uk" + path
    if params: url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": AUTH, "User-Agent": "mdb-abm"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def search(q):
    d = get("/search/companies", q=q, items_per_page=8)
    for it in d.get("items", []):
        print("  %-12s %-9s %s" % (it["company_number"], it.get("company_status", "?"), it["title"]))

def officers(num):
    d = get("/company/%s/officers" % num, items_per_page=100)
    c = get("/company/%s" % num)
    print("%s  (%s, %s)" % (c["company_name"], num, c.get("company_status")))
    live = [o for o in d.get("items", []) if not o.get("resigned_on")]
    for o in sorted(live, key=lambda x: x.get("appointed_on", "")):
        print("  %-34s %-22s appointed %s  %s" % (
            o["name"][:34], o.get("officer_role", ""), o.get("appointed_on", "?"),
            (o.get("occupation") or "")[:26]))
    print("  %d current, %d resigned" % (len(live), len(d.get("items", [])) - len(live)))

if __name__ == "__main__":
    if sys.argv[1] == "--number":
        for n in sys.argv[2:]: officers(n); print()
    else:
        for q in sys.argv[1:]: print(q); search(q); print()

#!/usr/bin/env python3
"""The clickable drafts page: one row per company, the ad card as a thumbnail, four links.

    python3 build_open_page.py --run ~/abm-runs/<client>/abm-1to1 --client "<Client>"

Writes <run>/05-campaign/OPEN-THE-DRAFTS.html.

WHY BOTH LINK KINDS, AND WHY BOTH ARE NEEDED. The feed preview shows the ad as a human will see
it. Campaign Manager shows the setting behind it. Somebody shown only the first cannot check the
targeting; somebody shown only the second cannot see what was made.

THE CAMPAIGN GROUP IS A QUERY FILTER, NOT A PATH SEGMENT. `/campaigns/{group}/...` returns "the
page you are looking for could not be found". Verified against a real session on 2026-09-23 after
an invented URL was handed over and clicked. The working shape is
`/campaigns?campaignGroupIds=%5B{group}%5D`.

JOIN ON THE CAMPAIGN ID, NEVER ON THE COMPANY NAME. An earlier version keyed results by
`org_urn` while the kit wrote `company`, and every row silently read "not built". The campaign id
is the only field both files agree on exactly.

A RUN CAN HAVE MORE THAN ONE CONFIG. WYN shipped two groups from `abm_config_finance.json` and
`abm_config_wide.json`. Every `abm_config*.results.json` is picked up and every distinct group
gets its own filter link at the top.
"""
import argparse, base64, html, json, urllib.request
from pathlib import Path

e = html.escape
ap = argparse.ArgumentParser()
ap.add_argument("--run", required=True, help="the run folder, the one holding 00-inputs")
ap.add_argument("--client", required=True, help="the client name, as it goes in the title")
ap.add_argument("--note", default="", help="one extra line under the heading, optional")
ap.add_argument("--no-check", action="store_true",
                help="skip fetching every landing page. Checking is the default because this "
                     "page is read on a record day and a dead link is found on camera otherwise")
A = ap.parse_args()

RUN = Path(A.run).expanduser().resolve()
IN, CAMP = RUN / "00-inputs", RUN / "05-campaign"
amap = json.loads((CAMP / "account_map.json").read_text())
by_adset = {str(v.get("adset")): (k, v) for k, v in amap.items() if v.get("adset")}

pairs = []
for res in sorted(IN.glob("abm_config*.results.json")):
    cfg = res.with_name(res.name.replace(".results.json", ".json"))
    if cfg.exists():
        pairs.append((json.loads(cfg.read_text()), json.loads(res.read_text())))
if not pairs:
    raise SystemExit("no abm_config*.results.json in %s" % IN)

ACCT = str(pairs[0][0]["account_id"])
CM = "https://www.linkedin.com/campaignmanager/accounts/%s" % ACCT
groups, rows, missing, dead = [], [], [], []


def alive(url):
    """A landing page that 404s is found on camera otherwise. GET, never HEAD: a HEAD is not the
    file, and GitHub Pages has served a 200 HEAD for a path whose GET is the 404 page."""
    if A.no_check or not url:
        return True
    try:
        r = urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=20)
        return r.status == 200 and len(r.read()) > 5000
    except Exception:
        return False


def thumb(path):
    """The ad card, inlined, so the page survives being moved or opened from anywhere."""
    p = Path(path)
    if not p.exists():
        return ""
    return '<img src="data:image/png;base64,%s">' % base64.b64encode(p.read_bytes()).decode()


def preview(row, org):
    """The feed preview. account_map holds the finished one; the results file may predate it."""
    u = row.get("preview")
    if u:
        return u
    ad = row.get("ad") or {}
    if ad.get("post") and ad.get("creative"):
        return ("https://www.linkedin.com/feed/update/urn:li:sponsoredContentV2:(%s,%s)/"
                "?actorCompanyId=%s&viewContext=REVIEWER" % (ad["post"], ad["creative"], org))
    return ""


for cfg, res in pairs:
    org = str(cfg.get("org_id", ""))
    gid = str(res.get("group_id", ""))
    if gid and gid not in [g[0] for g in groups]:
        groups.append((gid, cfg.get("group_name", "")))
    co_by_name = {c["name"]: c for c in cfg.get("companies", [])}
    for r in res.get("ad_sets", []):
        cid = str(r.get("campaign_id") or "")
        slug, m = by_adset.get(cid, (None, {}))
        c = co_by_name.get(r.get("company"), {})
        if not cid:
            missing.append(r.get("company", "?"))
            continue
        name = m.get("display") or r.get("company") or "?"
        aud = m.get("audience") or r.get("audience") or "?"
        pv = preview({**r, **m}, org)
        page = c.get("landing_page", "")
        quote, cite = m.get("quote", ""), m.get("cite", "")
        ev = ('<div class="q">&ldquo;%s&rdquo;<span class="cite">%s</span></div>'
              % (e(quote), e(cite))) if quote else ""
        links = []
        if pv:
            links.append('<a href="%s">The ad, in the feed</a>' % e(pv))
        else:
            links.append('<span class="dead">No feed preview built</span>')
        links.append('<a href="%s/campaigns/%s">The draft, its settings</a>' % (CM, cid))
        links.append('<a href="%s/campaigns/%s/creatives">The draft, its ads</a>' % (CM, cid))
        if page and alive(page):
            links.append('<a href="%s">The page it lands on</a>' % e(page))
        elif page:
            dead.append("%s: %s" % (name, page))
            links.append('<span class="dead">The page it lands on is DEAD</span>')
        rows.append(
            '<tr><td class="th">%s</td><td><div class="co">%s</div><div class="hl">%s</div>%s'
            '<div class="meta">Ad set %s &middot; %s people &middot; draft &middot; '
            'daily budget is a placeholder</div></td><td class="lk">%s</td></tr>'
            % (thumb(c.get("image", "")), e(name), e(c.get("headline", "")), ev,
               cid, aud, "".join(links)))

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,system-ui,sans-serif;background:#FDFCFC;color:#000;padding:44px;line-height:1.5}
h1{font-size:2rem;letter-spacing:-.03em;font-weight:900}
.sub{color:#5C5752;margin-top:8px;max-width:74ch}
.flag{display:inline-block;margin-top:16px;padding:9px 16px;border:1px solid #D8CEC4;border-radius:999px;font-size:.86rem;font-weight:600}
.flag b{color:#3F8F7A}
table{width:100%;border-collapse:collapse;margin-top:26px;max-width:1180px}
td{padding:18px 14px;border-bottom:1px solid #D8CEC4;vertical-align:middle}
.th{width:150px}.th img{width:130px;border-radius:10px;display:block}
.co{font-weight:900;font-size:1.15rem}.hl{font-weight:600;margin-top:3px}
.q{margin-top:8px;font-size:.88rem;color:#2F2A26;border-left:3px solid #D8CEC4;padding-left:11px;max-width:58ch}
.cite{display:block;font-size:.76rem;color:#7B7B92;margin-top:3px;font-style:normal}
.meta{font-size:.8rem;color:#5C5752;margin-top:8px}
.lk{width:310px}
.lk a{display:block;color:#3F8F7A;font-weight:700;font-size:.92rem;text-decoration:none;padding:3px 0}
.dead{display:block;color:#A8A29B;font-weight:700;font-size:.92rem;padding:3px 0}
.top{margin-top:22px;padding:16px 20px;background:#F5F3F1;border-radius:12px;max-width:1180px}
.top a{color:#3F8F7A;font-weight:700;display:inline-block;margin-right:22px}
.top b{display:block;margin-bottom:7px}
footer{margin-top:32px;font-size:.8rem;color:#7B7B92;max-width:84ch}"""

top = ['<b>The whole thing on LinkedIn:</b>']
for gid, gname in groups:
    top.append('<a href="%s/campaigns?campaignGroupIds=%%5B%s%%5D">%s</a>'
               % (CM, gid, e(gname or "The campaign group")))
top.append('<a href="%s/campaigns">Every campaign in the account</a>' % CM)
if (CAMP / "HANDOVER.html").exists():
    top.append('<a href="HANDOVER.html">The handover document</a>')

doc = ('<!doctype html><meta charset="utf-8"><title>%s, the drafts</title>'
       '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">'
       '<style>%s</style>'
       '<h1>%s, the drafts</h1>'
       '<p class="sub">One row per company. The ad as it appears in the feed, the draft on LinkedIn '
       'with its settings and its ads, and the page the click lands on.%s</p>'
       '<div class="flag">Nothing is live. <b>Nothing has been spent.</b></div>'
       '<div class="top">%s</div><table>%s</table>'
       '<footer>Account %s, %d company%s, %d campaign group%s. The ads post from the MDB page: in '
       'production they would post from the client\'s own. The daily budget is an unconfirmed '
       'placeholder. Strategy and GTM research by Jean Mundabi Fala.</footer>'
       % (e(A.client), CSS, e(A.client), (" " + e(A.note)) if A.note else "",
          "".join(top), "".join(rows), ACCT,
          len(rows), "" if len(rows) == 1 else "s",
          len(groups), "" if len(groups) == 1 else "s"))

out = CAMP / "OPEN-THE-DRAFTS.html"
out.write_text(doc, encoding="utf-8")
print("-> %s  %d rows, %d group(s)%s" % (out, len(rows), len(groups),
      (", NO CAMPAIGN ID: " + ", ".join(missing)) if missing else ""))
skipped = [f.name for f in sorted(IN.glob("abm_config*.json"))
           if not f.name.endswith(".results.json")
           and not f.with_name(f.name[:-5] + ".results.json").exists()]
if skipped:
    print("   configs with no results, not on the page: %s" % ", ".join(skipped))
for d in dead:
    print("   DEAD LANDING PAGE  %s" % d)

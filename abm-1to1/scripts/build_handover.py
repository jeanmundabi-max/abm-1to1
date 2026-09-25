#!/usr/bin/env python3
"""
The handover. One page that says what was done, for whom, and why.

    python3 build_handover.py --run ~/path/to/client-run

Every other artefact in a run is for the operator. This one is for the client. It exists
because a campaign that is built but not explained looks like a black box, and a black box
is impossible to approve. It is written to be readable by someone who has never opened a
Campaign Manager.

It reads the run's own files and invents nothing. If a number is not in the run folder it
does not appear on the page.

**It is honest about what has NOT happened.** Nothing activated, nothing spent, and the
things that failed are named with the reason. A handover that only lists successes is a
sales document, and this is not one.
"""
import argparse, csv, html, json, os, sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runpaths import Run, add_run_arg

e = html.escape
def gbp(n):
    try: return "£" + "{:,.0f}".format(float(n))
    except Exception: return str(n)
ACRO={"Llp":"LLP","Ltd":"Ltd","Uk":"UK","Emea":"EMEA","Sarl":"SARL","Kpmg":"KPMG","Plc":"plc"}
def firm(x):
    """Une raison sociale en capitales est du bruit de registre, pas le nom de la societe."""
    x=(x or "").split(" | ")[0].strip().rstrip(",")
    L=[c for c in x if c.isalpha()]
    if L and all(c.isupper() for c in L):
        return " ".join(ACRO.get(w.capitalize(), w.capitalize()) for w in x.split())
    return " ".join(ACRO.get(w, w) for w in x.split())

def dt(x):
    try: return datetime.strptime(str(x)[:10], "%Y-%m-%d").strftime("%-d %B %Y")
    except Exception: return str(x)

CSS = """
:root{--ink:#16163F;--accent:#9E3FFD;--muted:#5B5B78;--rule:#E6E2F2;--wash:#F7F5FC}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,system-ui,-apple-system,sans-serif;color:var(--ink);background:#fff;
 line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding:0 32px}
header{padding:72px 0 40px;border-bottom:1px solid var(--rule)}
.eyebrow{font-size:.78rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
h1{font-size:2.7rem;line-height:1.08;letter-spacing:-.03em;margin-top:14px;font-weight:700}
.sub{color:var(--muted);margin-top:16px;font-size:1.05rem;max-width:62ch}
.flag{display:inline-flex;align-items:center;gap:9px;margin-top:24px;padding:9px 16px;
 border:1px solid var(--rule);border-radius:99px;font-size:.86rem;font-weight:600}
.flag .dot{width:8px;height:8px;border-radius:50%;background:var(--accent)}
.cmbar{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin-top:18px;padding:14px 18px;
 background:var(--wash);border:1px solid var(--rule);border-radius:12px;font-size:.9rem}
.cmbar b{font-weight:700} .cmbar a{color:var(--accent);font-weight:600}
/* the narrowing funnel, and the decision ledger. Section 03. */
.funnel{display:grid;gap:26px;margin:26px 0 8px}
.fn{border-top:2px solid var(--ink);padding-top:16px}
.fn__co{font-weight:700;font-size:1.05rem;margin-bottom:12px}
.fn__row{position:relative;display:grid;grid-template-columns:96px 1fr;align-items:baseline;
 gap:14px;padding:9px 0 9px 0}
.fn__bar{position:absolute;left:0;top:0;bottom:0;width:var(--w,100%);background:var(--wash);
 border-left:3px solid var(--accent);z-index:0;border-radius:0 4px 4px 0}
.fn__n{position:relative;z-index:1;font-weight:700;font-variant-numeric:tabular-nums;
 padding-left:12px;font-size:1.02rem}
.fn__l{position:relative;z-index:1;color:var(--muted);font-size:.95rem}
.fn__l em{font-style:normal;color:#8A8AA5}
.fn__foot{margin-top:10px;font-size:.9rem;font-weight:600}
.fn__foot.ok{color:#1E7A46} .fn__foot.no{color:#A32E2E}
.ledger{width:100%;border-collapse:collapse;margin-top:16px;font-size:.92rem}
.ledger th{text-align:left;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
 color:var(--muted);font-weight:700;padding:0 14px 10px 0;border-bottom:1px solid var(--rule);vertical-align:bottom}
.ledger td{padding:16px 14px 16px 0;border-bottom:1px solid var(--rule);vertical-align:top;line-height:1.5}
.ledger td:nth-child(4){color:var(--muted)}
.ledger td.who{font-weight:600;min-width:104px}
.fn__na{color:var(--muted);font-size:.9rem;margin-top:10px;max-width:64ch}
@media (max-width:820px){
 .ledger,.ledger tbody,.ledger tr,.ledger td{display:block;width:100%}
 .ledger thead{display:none}
 .ledger tr{border-bottom:2px solid var(--ink);padding:14px 0}
 .ledger td{border:0;padding:4px 0}
 .fn__row{grid-template-columns:1fr}
}
section{padding:52px 0;border-bottom:1px solid var(--rule)}
h2{font-size:1.55rem;letter-spacing:-.02em;font-weight:700}
h2 .n{color:var(--accent);font-variant-numeric:tabular-nums;margin-right:12px}
.lede{color:var(--muted);margin-top:10px;max-width:70ch}
table{width:100%;border-collapse:collapse;margin-top:22px;font-size:.93rem}
th{text-align:left;font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;
 color:var(--muted);padding:0 12px 10px 0;font-weight:700;border-bottom:1px solid var(--rule)}
td{padding:13px 12px 13px 0;border-bottom:1px solid var(--rule);vertical-align:top}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.acct{margin-top:26px;border:1px solid var(--rule);border-radius:14px;overflow:hidden}
.acct h3{background:var(--wash);padding:16px 22px;font-size:1.05rem;border-bottom:1px solid var(--rule)}
.acct .body{padding:20px 22px;display:grid;grid-template-columns:1fr 1fr;gap:18px 30px}
.kv{font-size:.9rem}
.kv b{display:block;font-size:.72rem;letter-spacing:.09em;text-transform:uppercase;
 color:var(--muted);margin-bottom:3px;font-weight:700}
.kv a{color:var(--accent);text-decoration:none;word-break:break-all}
.kv a:hover{text-decoration:underline}
.walk{grid-column:1/-1;font-size:.88rem;color:var(--muted);padding-top:6px;border-top:1px solid var(--rule)}
.walk code{font-family:inherit;color:var(--ink);font-weight:600}
ul{margin-top:16px;padding-left:0;list-style:none}
li{padding:9px 0 9px 26px;position:relative;border-bottom:1px solid var(--rule)}
li:before{content:"";position:absolute;left:0;top:19px;width:12px;height:2px;background:var(--accent)}
li.no:before{background:var(--muted);opacity:.5}
.why{color:var(--muted);font-size:.9rem;display:block;margin-top:3px}
footer{padding:44px 0 80px;color:var(--muted);font-size:.85rem}
.bars{grid-column:1/-1;margin-top:4px}
.bar{display:grid;grid-template-columns:1fr 92px;align-items:center;gap:14px;margin-top:7px;font-size:.82rem}
.bar .t{height:19px;border-radius:4px;background:var(--accent);opacity:.9}
.bar.b2 .t{opacity:.55}.bar.b3 .t{opacity:1}
.bar .lab{color:var(--muted);font-size:.76rem}
.bar .v{text-align:right;font-variant-numeric:tabular-nums;font-weight:700}
.bar.b3 .v{color:var(--accent)}
.steps{display:grid;grid-template-columns:repeat(5,1fr);gap:0;margin-top:26px;
 border:1px solid var(--rule);border-radius:14px;overflow:hidden}
.steps div{padding:18px 16px;border-right:1px solid var(--rule);position:relative}
.steps div:last-child{border-right:0;background:var(--wash)}
.steps b{display:block;font-size:1.5rem;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.steps span{display:block;font-size:.76rem;color:var(--muted);margin-top:5px;line-height:1.35}
.stage{display:grid;grid-template-columns:34px 1fr;gap:18px;margin-top:18px;align-items:start}
.stage .mark{position:relative;height:100%;min-height:74px}
.stage .mark i{position:absolute;left:12px;top:5px;width:11px;height:11px;border-radius:50%;
 background:var(--accent);box-shadow:0 0 0 4px #fff,0 0 0 6px var(--accent)}
.stage.todo .mark i{background:#fff;box-shadow:0 0 0 4px #fff,0 0 0 2px var(--rule)}
.stage .mark:after{content:"";position:absolute;left:17px;top:20px;bottom:-18px;width:1px;background:var(--rule)}
.stage:last-child .mark:after{display:none}
.stage .card{border:1px solid var(--rule);border-radius:14px;padding:18px 22px}
.stage.now .card{border-color:var(--accent);background:var(--wash)}
.stage.todo .card{border-style:dashed}
.stage h4{font-size:1.02rem;display:flex;align-items:baseline;gap:11px;flex-wrap:wrap}
.tag{font-size:.66rem;letter-spacing:.11em;text-transform:uppercase;font-weight:700;
 padding:3px 9px;border-radius:99px;background:var(--accent);color:#fff}
.tag.off{background:transparent;color:var(--muted);border:1px solid var(--rule)}
.stage p{color:var(--muted);font-size:.9rem;margin-top:8px;max-width:72ch}
.pools{display:flex;gap:9px;flex-wrap:wrap;margin-top:13px}
.pool{font-size:.79rem;border:1px solid var(--rule);border-radius:9px;padding:8px 12px;background:#fff}
.pool b{display:block;font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:2px}
.url{margin-top:24px;border:1px solid var(--rule);border-radius:12px;padding:20px 22px;background:var(--wash)}
.url .line{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.8rem;
 line-height:2.1;word-break:break-all}
.url .base{color:var(--muted)}
.url .p{background:#fff;border:1px solid var(--accent);border-radius:6px;padding:3px 6px;
 color:var(--ink);font-weight:600;white-space:nowrap}
.url .amp{color:var(--muted)}
.legend{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:20px;
 padding-top:18px;border-top:1px solid var(--rule)}
.legend div{font-size:.82rem}
.legend b{display:block;font-family:ui-monospace,Menlo,monospace;font-size:.74rem;color:var(--accent);margin-bottom:4px}
.legend span{color:var(--muted)}
.gantt{margin-top:26px;border:1px solid var(--rule);border-radius:14px;overflow:hidden}
.gantt .hd,.gantt .row{display:grid;grid-template-columns:186px repeat(12,1fr)}
.gantt .hd{background:var(--wash);border-bottom:1px solid var(--rule)}
.gantt .hd div{padding:11px 0;text-align:center;font-size:.68rem;font-weight:700;color:var(--muted);
 letter-spacing:.06em}
.gantt .hd div:first-child{text-align:left;padding-left:18px;letter-spacing:.1em;text-transform:uppercase}
.gantt .row{border-bottom:1px solid var(--rule);align-items:center}
.gantt .row:last-child{border-bottom:0}
.gantt .ch{padding:13px 14px 13px 18px;font-size:.83rem;font-weight:600;line-height:1.3}
.gantt .ch em{display:block;font-style:normal;font-weight:400;font-size:.72rem;color:var(--muted);margin-top:2px}
.gantt .c{height:13px;margin:0 1px;border-radius:3px}
.gantt .on{background:var(--accent)}
.gantt .on.soft{opacity:.42}
.gantt .off{border:1px dashed var(--rule);height:13px}
.gantt .row.todo .ch{color:var(--muted)}
.gantt .row.todo .on{background:transparent;border:1px dashed var(--accent);opacity:.75}
.phases{display:grid;grid-template-columns:186px repeat(12,1fr);margin-top:10px}
.phases div{grid-column:span 4;font-size:.73rem;color:var(--muted);padding:0 4px;
 border-top:2px solid var(--rule);padding-top:7px;margin-right:6px}
.phases div:first-child{grid-column:1;border:0}
.risk{margin-top:26px;border:1px solid var(--rule);border-left:3px solid var(--accent);
 border-radius:0 12px 12px 0;padding:18px 22px;background:var(--wash)}
.risk b{display:block;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-bottom:7px}
.risk p{font-size:.9rem;color:var(--muted);max-width:74ch}
.risk p+p{margin-top:9px}
@media(max-width:900px){.gantt .hd,.gantt .row,.phases{grid-template-columns:130px repeat(12,1fr)}}
.two{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:24px}
.two h3{font-size:.76rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);
 padding-bottom:10px;border-bottom:1px solid var(--rule)}
.two ul{margin-top:0}
.two li{padding-left:24px}
.two li:before{top:17px}
.q{border-left:2px solid var(--accent);padding:2px 0 2px 18px;margin-top:20px;
 font-size:.92rem;color:var(--muted);max-width:74ch}
.q b{color:var(--ink);font-weight:600}
@media(max-width:760px){.acct .body{grid-template-columns:1fr}h1{font-size:2rem}
 .steps{grid-template-columns:1fr 1fr}.two{grid-template-columns:1fr}}
"""

def term_phrase(y):
    """0 est falsy. `y or 1` transformait une duree absente en 'one year', c'est-a-dire
    en un chiffre invente sur une page que le client lit. Une duree absente se DIT."""
    try: y = float(y)
    except (TypeError, ValueError): return "over an unstated term"
    if y <= 0: return "over an unstated term"
    return "over one year" if round(y) == 1 else "over %d years" % round(y)

def read_csv(p):
    return list(csv.DictReader(p.open())) if p.exists() else []


# ---------------------------------------------------------------------------
# Sections 01 and 02 are THE PLAY'S ARGUMENT, not the template's. They say why
# each account is on the list, and that reason differs per play: an expiring
# software contract for WYN, a currency line in a filing for Revolut. A version
# that could say both would say nothing, so this is a seam, not a setting.
#
# A run may supply <run>/00-inputs/handover_evidence.py exposing
#     sections(ctx) -> list[str]      the HTML for sections 01 and 02
#     PHRASES = {...}                 optional, overrides the wording below
# With no module the WYN text runs unchanged, so porting a play is opt-in and
# cannot break a run that has not been ported.
def _default_evidence(ctx):
    """The WYN block: UK public procurement, contract expiry as the trigger."""
    e, gbp, dt = ctx["e"], ctx["gbp"], ctx["dt"]
    firm, term_phrase, page_url = ctx["firm"], ctx["term_phrase"], ctx["page_url"]
    previews, amap, walk = ctx["previews"], ctx["amap"], ctx["walk"]
    pages, accounts, live, ev = ctx["pages"], ctx["accounts"], ctx["live"], ctx["ev"]
    o = []
    # 1. the list
    o.append('<section><h2><span class="n">01</span>Who we are targeting, and how the list was built</h2>')
    o.append('<p class="lede">The list was not bought or guessed. Every organisation on it publishes '
             'its own software contracts, with the supplier, the value and the expiry date, on the UK '
             'government\'s Contracts Finder. A contract that is about to expire is the only moment '
             'the price is negotiable, so that expiry date is what put each organisation on the list.</p>')
    if accounts:
        tot = sum(int(x.get("annual_at_stake") or 0) for x in accounts)
        n_acc = len(pages.get("accounts", {}))
        o.append('<div class="steps">')
        o.append('<div><b>%d</b><span>organisations publish a software contract expiring in the next nine months</span></div>' % len(accounts))
        o.append('<div><b>%d</b><span>contracts behind them, each checked as still live and not already re-let</span></div>' % len(live))
        o.append('<div><b>%s</b><span>a year is what those contracts are worth in total</span></div>' % gbp(tot))
        o.append('<div><b>%d</b><span>accounts taken forward, chosen on expiry date and size</span></div>' % n_acc)
        o.append('<div><b>%d</b><span>ads and %d pages, one of each per account, sharing nothing</span></div>' % (n_acc, n_acc))
        o.append('</div>')
    o.append("</section>")

    # 2. per account
    o.append('<section><h2><span class="n">02</span>The four accounts, and the evidence behind each</h2>')
    o.append('<p class="lede">Each account has its own page and its own ad. Nothing is shared between them, '
             'because the argument for each one is a different contract with a different date.</p>')
    for slug, mp in amap.items():
        full = mp["evidence"]
        if full not in ev: continue
        d = ev[full]; top = d["top"][0]
        nm = mp["display"]
        w = walk.get(mp["walk"], {})
        pct = round(float(top["annual_value"]) / float(d["annual_total"]) * 100)
        o.append('<div class="acct"><h3>%s</h3><div class="body">' % e(nm))
        o.append('<div class="kv"><b>The contract that put them on the list</b>%s<br>%s %s, which is %s a year'
                 '<br>Ends %s</div>'
                 % (e(firm(top["suppliers"])), gbp(top["value"]), 
                    term_phrase(top.get("term_years")),
                    gbp(top["annual_value"]), dt(top["end"])))
        o.append('<div class="kv"><b>Days until it expires</b>%s</div>' % e(str(top["days_to_expiry"])))
        o.append('<div class="kv"><b>Share of their software spend</b>%d%% of %s a year, across %d contracts</div>'
                 % (pct, gbp(d["annual_total"]), d["n"]))
        o.append('<div class="kv"><b>Where the figures come from</b>Their own award notice on Contracts Finder</div>')
        if slug:
            url = page_url(slug)
            o.append('<div class="kv"><b>The page they land on</b><a href="%s">%s</a></div>' % (url, url))
        if mp.get("adset") in previews:
            o.append('<div class="kv"><b>The ad, as it appears in the feed</b><a href="%s">Open the preview</a></div>'
                     % e(previews[mp["adset"]]))
        vals = [w.get("company only"), w.get("+ exclude junior"), w.get("+ buyer functions")]
        if w and all(v and str(v).strip() not in ("", "0") for v in vals):
            n0, n1, n2 = (int(str(v).replace(",", "")) for v in vals)
            labs = [("Everyone who works there, in the UK", n0),
                    ("Once junior roles are taken out", n1),
                    ("Once it is only %s roles" % w.get("functions_label", "finance and commercial"), n2)]
            o.append('<div class="bars">')
            for i, (lab, v) in enumerate(labs):
                o.append('<div class="bar b%d"><div><div class="lab">%s</div>'
                         '<div class="t" style="width:%.1f%%"></div></div><div class="v">%s</div></div>'
                         % (i + 1, e(lab), max(2.0, v / float(n0) * 100), "{:,}".format(v)))
            o.append('<div class="walk" style="border:0;padding-top:11px">The last bar is who actually sees '
                     'the ad. Measured on %s.</div></div>' % dt(w.get("measured", "")))
        else:
            o.append('<div class="walk">The audience size for this account has not been measured since the targeting '
                     'was last changed, so no figure is shown rather than a stale one.</div>')
        o.append("</div></div>")
    o.append("</section>")
    return o



# LinkedIn facet urns are meaningless to a client. A handover that prints
# "urn:li:function:10" has told them nothing and looks like a leak of internal plumbing.
FACET = {
 "urn:li:function:1":"Accounting", "urn:li:function:10":"Finance",
 "urn:li:function:18":"Operations", "urn:li:function:20":"Programme and project management",
 "urn:li:function:4":"Business development", "urn:li:function:8":"Consulting",
 "urn:li:function:13":"Information technology", "urn:li:function:16":"Legal",
 "urn:li:function:25":"Sales", "urn:li:function:12":"Human resources",
 "urn:li:seniority:1":"Unpaid", "urn:li:seniority:2":"Training",
 "urn:li:seniority:3":"Entry level", "urn:li:seniority:4":"Senior",
 "urn:li:seniority:5":"Manager", "urn:li:seniority:6":"Director",
 "urn:li:seniority:7":"Vice president", "urn:li:seniority:8":"Chief officer",
 "urn:li:seniority:9":"Partner", "urn:li:seniority:10":"Owner",
 "urn:li:geo:101165590":"United Kingdom", "urn:li:geo:103644278":"United States",
 "urn:li:geo:105646813":"Spain", "urn:li:geo:105015875":"France",
 "urn:li:geo:101282230":"Germany", "urn:li:geo:100565514":"Netherlands",
}
def _funnel(run, amap):
    """The funnel, in plain words. The question this answers: "we start with 20 and end up with 5, there
    should be a place to explain that." Reads 00-inputs/candidates.csv (a verdict column: IN or
    BENCH: reason) and, if present, 00-inputs/FUNNEL.json {"shown": n, "note": "..."}. Invents
    nothing: a run without a candidates file gets no section."""
    cand = read_csv(run.inputs / "candidates.csv")
    if not cand: return []
    extra = json.loads((run.inputs / "FUNNEL.json").read_text()) if (run.inputs / "FUNNEL.json").exists() else {}
    looked = len(cand)
    built = [r for r in cand if (r.get("verdict") or "").upper().startswith("IN")]
    bench = [r for r in cand if (r.get("verdict") or "").upper().startswith("BENCH")]
    shown = extra.get("shown") or looked
    reasons = {}
    for r in bench:
        why = (r.get("verdict") or "").split(":", 1)[-1].strip() or "seat taken"
        PLAIN = {"seat taken": "another company in the same sector had the stronger figure, and it is one per sector",
                 "weak evidence": "the figure on file was not strong enough to build a page on",
                 "UK arm thin": "too few UK staff on LinkedIn to reach"}
        why = PLAIN.get(why, why)
        reasons.setdefault(why, []).append(r.get("company") or r.get("name") or "?")
    o = ['<section><h2><span class="n">02b</span>How %d became %d, in plain words</h2>' % (looked, len(built))]
    o.append('<p class="lede">A one-to-one campaign builds a page, a film and an ad for each company, so the '
             'list gets shorter at every step on purpose. Here is where each company went and why.</p>')
    o.append('<div class="steps">')
    o.append('<div><b>%d</b><span>looked at, read off the public files</span></div>' % looked)
    o.append('<div><b>%d</b><span>shown as named rows before anything was built</span></div>' % shown)
    o.append('<div><b>%d</b><span>set aside, each with a reason below</span></div>' % len(bench))
    o.append('<div><b>%d</b><span>built, one per sector</span></div>' % len(built))
    o.append('</div>')
    if reasons:
        o.append('<ul>')
        for why, names in sorted(reasons.items(), key=lambda kv: -len(kv[1])):
            o.append('<li>%s<span class="why">%s</span></li>' % (e(", ".join(firm(n) for n in names)), e(why)))
        o.append('</ul>')
    if extra.get("note"): o.append('<p class="lede">%s</p>' % e(extra["note"]))
    o.append('</section>')
    return o

def facets(v):
    """A list of urns, or one, rendered as the names a client can argue with."""
    if v is None: return "not set"
    if isinstance(v, str): v = [v]
    out = [FACET.get(str(x), str(x)) for x in v]
    return ", ".join(out) if out else "not set"

def _decision_ledger(ctx, cfg, walk_rows):
    """Section 03. The thing the client cannot get from Campaign Manager.

    Campaign Manager shows WHAT was set. It never shows what else was on the table or why
    this was chosen, so a client reading it has to either trust the operator or re-litigate
    every field. This section is the record of the argument: the choice, the alternative
    that was genuinely considered, the reason, and who owns the decision now.

    Every number comes from the run's own abm_config.json and narrowing-walk.csv. Nothing
    here is written by hand, so a config change shows up on the client page automatically.
    """
    e = ctx["e"]; o = []
    ph = ctx.get("ph") or (lambda k, d: d)
    nacc = ctx.get("nacc") or "four"
    o.append('<section><h2><span class="n">03</span>Every decision, and why it went that way</h2>')
    o.append('<p class="lede">Campaign Manager shows what was set. It cannot show what else was on '
             'the table, or why this was chosen over it. That is what this section is for, so you can '
             'disagree with a decision without having to open the ad account to find it.</p>')

    # ---- the funnel, drawn from the run's own narrowing walk -------------------------
    amap = ctx.get("amap") or {}
    byname = {}
    for r in walk_rows:
        byname[(r.get("company") or "").strip().lower()] = r
    live = []
    for slug, m in amap.items():
        disp = (m.get("display") or slug)
        r = byname.get(disp.strip().lower()) or byname.get(disp.replace(" plc","").strip().lower()) or {}
        final = _int(m.get("audience")) or _int(r.get("+ buyer functions"))
        live.append({"company": disp,
                     "a": _int(r.get("company only")),
                     "b": _int(r.get("+ exclude junior")),
                     "c": final})
    live = [x for x in live if x["c"] > 0]
    if live:
        o.append('<h3>How one company narrows to one audience</h3>')
        o.append('<p>Each step below is a filter, and each number is what LinkedIn returned when that '
                 'filter was applied. The floor is 300: below it LinkedIn refuses to run the ad set at '
                 'all, which is the single constraint that decided which companies could be targeted.</p>')
        o.append('<div class="funnel">')
        fnames = facets(cfg.get("job_functions"))
        snames = facets(cfg.get("exclude_seniorities"))
        for r in live:
            a, b, c = r["a"], r["b"], r["c"]
            top = max(a, b, c, 1)
            o.append('<div class="fn"><div class="fn__co">%s</div>' % e(ctx["firm"](r["company"])))
            steps = []
            if a: steps.append(("Everyone at the company", a, ""))
            if b: steps.append(("%s removed" % snames, b, ph("junior_step_why", "they cannot approve a treasury change")))
            steps.append(("Buying functions only", c, fnames.lower()))
            for lab, v, note in steps:
                w = max(6.0, 100.0 * v / top)
                o.append('<div class="fn__row" style="--w:%.1f%%"><span class="fn__bar"></span>'
                         '<span class="fn__n">%s</span><span class="fn__l">%s%s</span></div>' % (
                         w, "{:,}".format(v), e(lab), (' <em>%s</em>' % e(note)) if note else ""))
            if not a:
                o.append('<p class="fn__na">The intermediate counts are not on record for this account: '
                         'the narrowing was walked against a different company page before the correct one '
                         'was resolved. The final number is the one the ad set was built on.</p>')
            floor_ok = c >= 300
            o.append('<div class="fn__foot %s">%s</div></div>' % (
                "ok" if floor_ok else "no",
                ("%s people, above the 300 floor, so this one runs" % "{:,}".format(c)) if floor_ok
                else ("%s people, under the 300 floor, so this one cannot run" % "{:,}".format(c))))
        o.append('</div>')

    # ---- the ledger -----------------------------------------------------------------
    obj = (cfg.get("objective") or {})
    funcs = cfg.get("job_functions") or []
    excl  = cfg.get("exclude_seniorities") or []
    geo   = cfg.get("geo")
    daily = cfg.get("daily_budget"); cur = cfg.get("currency","GBP")
    n_acc = len([r for r in walk_rows if _int(r.get("+ buyer functions")) > 0]) or len(ctx.get("amap") or {})

    rows = [
      ("One ad set per company",
       "%d ad sets, one company each" % max(n_acc, len(ctx.get("amap") or {})),
       "One ad set with all the companies uploaded as a list",
       "A list campaign spends where the cheapest impressions are, which is the largest company on it. "
       "Separate ad sets mean each company gets its own budget, its own creative and its own read, and a "
       "company that does not work can be switched off without touching the others.",
       "Us"),
      ("Objective: %s" % e(str(obj.get("type","not set"))),
       "%s, billed %s, optimised for %s" % (obj.get("type","not set"), obj.get("cost","not set"), obj.get("optimization","not set")),
       "Website visits, which optimises for the click",
       "Website visits tells LinkedIn to find the people most likely to click any link, and at an audience "
       "of a few hundred that is a handful of habitual clickers, not " + ph("buyer_desk", "the finance desk") + ". Engagement keeps the "
       "ad in front of the whole audience so the committee sees it repeatedly. The click still works and is "
       "still counted; it is simply not what the auction is told to chase.",
       "Yours to change"),
      ("Who is excluded",
       ("%s, excluded" % facets(excl)) if excl else "nobody excluded",
       "Leaving everyone in, to keep the audience larger",
       "Junior seniorities " + ph("junior_cannot", "cannot approve a treasury change") + ", and every impression served to them is "
       "budget that never reaches the committee. Excluding them costs audience size, which is why it is "
       "applied before the 300 floor is checked rather than after.",
       "Us"),
      ("Which departments",
       facets(funcs) if funcs else "not restricted",
       "No function filter at all",
       ph("function_reason", "The offer is read by a treasury or finance seat and by whoever runs the systems that touch payments. ") +
       "Anything wider spends on people who will never forward it.",
       "Yours to change"),
      ("Where",
       facets(geo),
       "Every country the company operates in",
       ph("geo_reason", "The evidence on each page is a UK filing, and a page that cites a UK filing to a reader in another "
       "market reads as a mistake. ") + "The geography follows the evidence, not the headcount.",
       "Us"),
      ("Interface locale",
       str((cfg.get("locale") or {}).get("language","")) + "_" + str((cfg.get("locale") or {}).get("country","")),
       ph("locale_alt", "en_GB, to match a UK audience"),
       "LinkedIn copies the campaign locale into the targeting criteria on its side, and it rejects en_GB "
       "there. The first attempt failed on all ad sets with INVALID_INTERFACE_LOCALE_CODE. This is a "
       "platform constraint, not a targeting choice, and it does not change who sees the ad.",
       "Fixed by the platform"),
      ("Daily budget",
       "%s %s a day, per ad set" % (daily, cur) if daily else "not set",
       "A budget sized to the audience",
       "This is a placeholder, not a recommendation. Nothing has spent it and nothing will until you "
       "activate. The right number depends on how many times you want the committee to see the ad in a "
       "week, and that is a conversation, not a default.",
       "Yours, before launch"),
      ("The image",
       "One built card per company, 4:5",
       "A stock photograph, or the same card for all companies",
       "The headline is the creative on this platform: the card has to be readable at thumbnail size in a "
       "feed, and it carries one company's own filed number drawn in that company's own visual world. A "
       "stock photograph carries no information at all, and one shared card would tell each reader the page "
       "was not built for them.",
       "Us"),
      ("Nothing is live",
       "Every ad set is a draft",
       "Launching on approval of the copy alone",
       "A draft can be read, argued with and changed for free. Once a creative has served it cannot be "
       "paused until it has been reviewed, so every change after launch is permanent and additive.",
       "Yours to release"),
    ]
    o.append('<h3>The ledger</h3>')
    o.append('<table class="ledger"><thead><tr><th>Decision</th><th>What is set</th>'
             '<th>What else was on the table</th><th>Why this one</th><th>Whose call now</th></tr></thead><tbody>')
    for d, setv, alt, why, who in rows:
        o.append("<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td class=\"who\">%s</td></tr>" % (
            d, e(str(setv)), e(str(alt)), why, e(str(who))))
    o.append('</tbody></table>')
    o.append('</section>')
    return o

def _int(x):
    try: return int(str(x).replace(",", "").strip() or 0)
    except Exception: return 0

def main():
    ap = add_run_arg(argparse.ArgumentParser(description="the client-facing handover page"))
    ap.add_argument("--client", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    run = Run(a.run)

    pages = json.loads((run.pages / "pages.json").read_text()) if (run.pages / "pages.json").exists() else {}
    # Le depot ne s'ecrit PAS en dur: c'est deploy.json qui sait ou les pages vivent.
    # Un renommage de depot a deja tue six destinations d'annonces parce que l'ancien nom
    # etait fige dans du code. GitHub Pages ne redirige pas apres un renommage.
    dep = json.loads((run.inputs / "deploy.json").read_text(encoding="utf-8")) \
          if (run.inputs / "deploy.json").exists() else {}
    # No fallback. A default username here silently points somebody else's pages at
    # whoever wrote it, and GitHub Pages does not redirect once the URL is wrong.
    owner = dep.get("owner") or os.environ.get("GITHUB_USERNAME")
    if not owner:
        raise SystemExit("No GitHub owner. Set \"owner\" in 00-inputs/deploy.json or export "
                         "GITHUB_USERNAME. Without it every ad destination on this page would "
                         "point at the wrong account.")
    repo  = dep.get("repo")
    dpath = dep.get("path") or "{slug}"
    if not repo or repo.startswith("<"):
        raise SystemExit("00-inputs/deploy.json ne dit pas dans quel depot les pages vivent. "
                         "Sans lui cette page afficherait des URL inventees.")
    def page_url(slug):
        return "https://%s.github.io/%s/%s/" % (owner, repo, dpath.replace("{slug}", slug).strip("/"))
    narrow = json.loads((run.inputs / "narrow_uk.json").read_text()) if (run.inputs / "narrow_uk.json").exists() else {}
    ev = json.loads((run.inputs / "evidence_by_account.json").read_text()) if (run.inputs / "evidence_by_account.json").exists() else {}
    walk = {r["company"]: r for r in read_csv(run.campaign / "narrowing-walk.csv")}
    accounts = read_csv(run.inputs / "accounts_merged.csv") or read_csv(run.inputs / "account_list.csv")
    live = read_csv(run.inputs / "contracts_live.csv")
    prev = (run.campaign / "PREVIEWS.txt").read_text() if (run.campaign / "PREVIEWS.txt").exists() else ""

    import re
    previews = dict(re.findall(r"^(\S.*)\n(?:.*\n)?\s*apercu (\S+)", prev, re.M)) if prev else {}
    # une table explicite, jamais un appariement de noms: "HMRC" n'est pas dans
    # "H M Revenue & Customs" et la carte tombait dans le vide en silence
    amap_p = run.campaign / "account_map.json"
    if not amap_p.exists():
        raise SystemExit("il manque %s. Ce fichier lie la cle d'evidence, le slug, le nom "
                         "affiche, la ligne de narrowing et l'ad set. Sans lui la page mentirait "
                         "par omission." % amap_p)
    amap = json.loads(amap_p.read_text(encoding="utf-8"))
    # A key starting with an underscore is a note to the operator, not an account. The GoCardless
    # map carries one recording that the run folder's ad set ids were stale and were re-read from
    # the live account. Without this filter the ledger tries to call .get on a string.
    _CM = amap.get("_cm") if isinstance(amap.get("_cm"), dict) else None
    amap = {k: v for k, v in amap.items() if not k.startswith("_") and isinstance(v, dict)}
    if _CM: amap["_cm"] = _CM   # remis pour l'en-tete, retire juste apres

    o = []
    o.append('<div class="wrap"><header>')
    o.append('<div class="eyebrow">Campaign handover</div>')
    o.append("<h1>%s: what was built, and why</h1>" % e(a.client))
    o.append('<p class="sub">Everything below was built from information %s published itself. '
             'This page exists so you can check the work rather than take it on trust.</p>' % e(a.client))
    o.append('<div class="flag"><span class="dot"></span>Nothing is live. Every ad set is a draft and no money has been spent.</div>')
    # Les liens qui ouvrent le travail la ou il vit. Sans eux la page decrit un brouillon que
    # personne ne peut aller regarder, ce qui est exactement ce qu'un client ne peut pas verifier.
    _cm = amap.pop("_cm", None)
    if _cm:
        o.append('<div class="cmbar"><b>See it yourself, on LinkedIn</b>'
                 '<a href="%s">The whole campaign group</a>'
                 '<a href="%s">The ad account</a>'
                 '<a href="OUVRIR-LES-BROUILLONS.html">Every draft, on one page</a></div>'
                 % (e(_cm.get("group","")), e(_cm.get("account",""))))
    else:
        # No Campaign Manager links. Say why, rather than leaving a reader to wonder whether
        # the drafts exist. A LinkedIn ad set is only visible to someone signed in with access
        # to the advertising account, so a link here would lead nowhere for everyone else.
        o.append('<div class="cmbar"><b>Why there are no LinkedIn links on this copy</b>'
                 'An ad set and its preview can only be opened by someone signed in with access '
                 'to the advertising account they live in. The ids on this page are placeholders '
                 'and the links are in the client\'s copy, not this one.</div>')
    o.append("</header>")

    ctx = {"e": e, "gbp": gbp, "dt": dt, "firm": firm, "term_phrase": term_phrase,
           "page_url": page_url, "previews": previews, "amap": amap, "walk": walk,
           "narrow": narrow, "pages": pages, "accounts": accounts, "live": live,
           "ev": ev, "client": a.client}
    _mod = run.inputs / "handover_evidence.py"
    if _mod.exists():
        import importlib.util as _il
        _s = _il.spec_from_file_location("handover_evidence", _mod)
        _m = _il.module_from_spec(_s); _s.loader.exec_module(_m)
        o.extend(_m.sections(ctx)); PHRASES = getattr(_m, "PHRASES", {})
    else:
        o.extend(_default_evidence(ctx)); PHRASES = {}
    # Wording that is play-specific but threaded through the SHARED sections. Every
    # call carries the WYN text as its default, so an unported run is byte-identical.
    # Found 2026-09-02: the shared sections were less shared than the section count
    # implied, and a Revolut handover printed "an expiry date on the public record"
    # about a currency filing.
    def ph(k, d):
        return PHRASES.get(k, d)

    cfg = json.loads((run.inputs / "abm_config.json").read_text(encoding="utf-8")) \
          if (run.inputs / "abm_config.json").exists() else {}
    ctx["ph"] = ph          # les sections partagees portent aussi du texte propre a un play
    # "four accounts" etait ecrit en dur et se trompait sur toute course qui n'en a pas quatre.
    _W = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"ten"}
    ctx["nacc"] = _W.get(len(amap), str(len(amap)))
    nacc = ctx["nacc"]
    _utm = (cfg.get("utm") or {})
    utm_std = bool(_utm) and all(k.startswith("utm_") for k in _utm)
    utm_has_content = any(k in ("utm_content", "content") for k in _utm)
    o.extend(_funnel(run, amap))
    o.extend(_decision_ledger(ctx, cfg, read_csv(run.campaign / "narrowing-walk.csv")))

    # 4. targeting
    o.append('<section><h2><span class="n">04</span>Who sees the ad, and who does not</h2>')
    o.append('<p class="lede">Each ad is shown to one organisation only. LinkedIn will not run an audience '
             'below 300 people, so the filters have to leave enough of an organisation in.</p>')
    o.append("<ul>")
    o.append('<li>Only people who work at that organisation<span class="why">This is the whole point of a '
             'one-to-one campaign. The ad for one department is never shown to another.</span></li>')
    o.append('<li>' + ph('geo_label', 'United Kingdom only') + '<span class="why">Large organisations have people abroad who are not '
             + ph('seniority_tail', 'involved in a UK procurement decision') + '.</span></li>')
    named = narrow.get("_functions_named", {})
    if named:
        o.append('<li>' + ph('function_label', 'Finance and accounting roles') + '<span class="why">'
                 + ph('function_who', 'The buyer for this is a finance or commercial lead. ')
                 + ph('function_caveat', 'Note that LinkedIn has no separate procurement category, so this group also contains ')
                 + ph('function_tail', 'finance people who do not buy software. That is deliberate: the ad names a specific contract '
                 'and a specific date, so the people it does not concern will ignore it.') + '</span></li>')
    if narrow.get("junior_seniorities"):
        o.append('<li class="no">Junior roles are excluded<span class="why">Interns, trainees and entry level. '
                 'They are not on the buying committee and including them would spend the budget on impressions '
                 'that cannot act.</span></li>')
    o.append("</ul></section>")

    # 3b. the tracking tag, explained
    utm = (json.loads((run.inputs / "abm_config.json").read_text())
           if (run.inputs / "abm_config.json").exists() else {}).get("utm", {})
    if utm:
        first = next(iter(amap)) if amap else "account"
        base = page_url(first)
        # Les etiquettes affichees sont celles que la course a REELLEMENT posees, jamais un
        # jeu suppose. Trouve le 2026-09-24: cette section imprimait utm_source/utm_medium/
        # utm_campaign/utm_content quelles que soient les cles du config, alors que le kit
        # envoie cfg["utm"].items() tel quel. Une remise montrait donc au client une URL qui
        # n'existe sur aucune annonce, avec un utm_campaign de repli et un utm_content jamais pose.
        DESCR = {"utm_source": "Which platform sent them. Here, always LinkedIn.",
                 "source": "Which platform sent them. Here, always LinkedIn.",
                 "utm_medium": "Paid or not. This separates ads from a post someone shared.",
                 "medium": "Paid or not. This separates ads from a post someone shared.",
                 "utm_campaign": "Which campaign. Lets you compare this against anything else you run.",
                 "campaign": "Which campaign. Lets you compare this against anything else you run.",
                 "utm_content": "Which of the %s ads. This is the one that makes the campaign readable." % nacc,
                 "content": "Which of the %s ads. This is the one that makes the campaign readable." % nacc}
        parts = [(k, v, DESCR.get(k, "Set on every ad set in this campaign."))
                 for k, v in utm.items()]
        has_content, std = utm_has_content, utm_std
        o.append('<section><h2><span class="n">05</span>How a visit gets traced back to the ad</h2>')
        _n = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six"}.get(len(parts), str(len(parts)))
        o.append('<p class="lede">When somebody clicks one of these ads, %s short labels are added to the '
                 'end of the web address.' % _n + ' Your analytics reads them and can then say where that visitor came '
                 'from. Nothing is installed on your site and nothing is collected about the person. It is a '
                 'label on the visit, not a tag on the visitor.</p>')
        o.append('<div class="url"><div class="line"><span class="base">%s</span>' % e(base))
        for i, (k, v, _d) in enumerate(parts):
            o.append('<span class="amp">%s</span><span class="p">%s=%s</span>' % ("?" if i == 0 else "&amp;", k, e(str(v))))
        o.append('</div><div class="legend">')
        for k, _v, d in parts:
            o.append('<div><b>%s</b><span>%s</span></div>' % (k, d))
        o.append('</div></div>')
        if has_content:
            o.append('<div class="q">Without the last label every visit from every ad arrives looking identical, '
                     'and there is no way to tell which of the %s accounts is reacting. <b>That single label is '
                     'the difference between %s campaigns you can compare and one number you cannot act on.</b></div>' % (nacc, nacc))
        else:
            o.append('<div class="q"><b>There is no per-account label on these ad sets, and that is a gap, not a choice.</b> '
                     'Every one of the %s ad sets carries the same labels, so a visit from one is indistinguishable '
                     'from a visit from another and you cannot tell which account is reacting. Adding one label per '
                     'ad set fixes it, changes nothing else, and is worth doing before anything runs.</div>' % nacc)
        if not std:
            o.append('<div class="q"><b>These labels are not named the way analytics tools expect.</b> '
                     'Google Analytics and most other tools only recognise a label when its name begins with '
                     '<code>utm_</code>. The names above do not, so the visits will arrive but will not be '
                     'grouped as campaign traffic. Renaming them is a settings change on each ad set. '
                     'It creates nothing and it can be done before launch.</div>')
        o.append('<p class="lede" style="margin-top:26px">Two honest limits. <b>This shows a visit arriving, '
                 'not what the visitor did next</b>, which is the separate piece of tracking that is not yet in '
                 'place. And this naming was chosen by us, because there is no existing campaign on the account '
                 'to copy a convention from. If you already use a different naming scheme elsewhere, yours '
                 'should win and these are quick to change.</p>')
        o.append("</section>")

    # 5. what this stage is for, drawn as the three stages
    o.append('<section><h2><span class="n">06</span>Where this sits, and what comes after it</h2>')
    o.append('<p class="lede">A campaign like this has three stages and this is the first one. Each stage '
             'has a different job, a different audience and a different way of being judged. Getting them '
             'in the wrong order is the usual reason paid campaigns disappoint.</p>')

    o.append('<div class="stage now"><div class="mark"><i></i></div><div class="card">'
             '<h4>Stage one, cold<span class="tag">this is what is built</span></h4>'
             '<p>Nobody in these organisations has heard of you. The job of this stage is to be recognised '
             'and to build the list of people who reacted. It is deliberately not trying to make anyone '
             'buy. The ads are set to optimise for engagement rather than for visits, because asking '
             'LinkedIn to buy clicks from people with no reason to be interested spends the budget on the '
             'wrong clicks.</p>'
             '<p>Judge this stage on how many of the right people saw it and reacted, not on sales.</p>'
             '</div></div>')

    o.append('<div class="stage todo"><div class="mark"><i></i></div><div class="card">'
             '<h4>Stage two, warm<span class="tag off">not built</span></h4>'
             '<p>This is where the first stage pays off. The people who reacted are now a much smaller and '
             'much warmer audience, and they get different ads: proof, a case study, a worked example. '
             'Only here does it become worth paying for a visit to the site.</p>'
             '<p>The important part is who counts as having reacted. It is not only the people who clicked.</p>'
             '<div class="pools">'
             '<div class="pool"><b>Watched the video</b>Half of it or more</div>'
             '<div class="pool"><b>Visited the site</b>Any page, from any source</div>'
             '<div class="pool"><b>Reacted to the ad</b>A like, a comment, an expand</div>'
             '</div>'
             '<p>Three separate groups, and two of them never clicked anything. Someone who watched thirty '
             'seconds of a video and moved on is a warmer contact than most people who click, and they can '
             'be followed up.</p>'
             '</div></div>')

    o.append('<div class="stage todo"><div class="mark"><i></i></div><div class="card">'
             '<h4>Stage three, ready<span class="tag off">not built</span></h4>'
             '<p>The smallest group: people who watched nearly all of a video, or visited the pages that '
             'only a serious buyer visits. These get a direct ask, and this is the only stage judged on '
             'meetings booked.</p></div></div>')

    o.append('<div class="q">The reason for the order: <b>only about one in twenty organisations is ready '
             'to buy at any given moment, and most of those prefer a name they already know.</b> The first '
             + ph('stage2_why', 'stage exists so that when a contract does come up for renewal, you are already a name they ') + 
             'recognise rather than a cold email.</div>')
    o.append("</section>")

    # 6. multi-channel orchestration
    o.append('<section><h2><span class="n">07</span>Ads are one channel, not the campaign</h2>')
    o.append('<p class="lede">Paid ads on their own rarely produce a meeting. What produces a meeting is the '
             'same organisation meeting your name in several places over a few weeks, and then a person '
             'getting in touch at the moment the interest is real. The ads handle the first part. A human '
             'handles the second. Below is the order, and it matters more than any single piece of it.</p>')

    ROWS = [
        ("LinkedIn ads, cold", "built and ready", False,
         [(0, 12, "on")]),
        ("LinkedIn ads, follow-up", "needs a LinkedIn permission", True,
         [(3, 12, "on")]),
        ("Email to the named buyer", "names already found in public records", True,
         [(3, 12, "on")]),
        ("A phone call", "only once there is a reason to call", True,
         [(5, 12, "on")]),
        ("A letter, for the largest accounts", ph("letter_note", "reserved for the biggest contracts"), True,
         [(7, 11, "on")]),
    ]
    o.append('<div class="gantt"><div class="hd"><div>Channel</div>')
    for w in range(1, 13):
        o.append('<div>%d</div>' % w)
    o.append('</div>')
    for name, note, todo, spans in ROWS:
        cells = ["off"] * 12
        for st, en, kind in spans:
            for k in range(st, en):
                cells[k] = kind
        o.append('<div class="row%s"><div class="ch">%s<em>%s</em></div>' % (" todo" if todo else "", e(name), e(note)))
        for c in cells:
            o.append('<div class="c %s"></div>' % c)
        o.append('</div>')
    o.append('</div>')
    o.append('<div class="phases"><div>Week</div>'
             '<div>Ads only. Nobody is contacted, on purpose.</div>'
             '<div>The accounts that reacted get a person.</div>'
             '<div>Conversations, and the ads turn to proof.</div>'
             '</div>')

    o.append('<div class="q">The line that is easiest to get wrong is the first four weeks. '
             '<b>Nobody is contacted in that window, deliberately.</b> Reaching out to an organisation that '
             'has only just seen your name is a cold approach with extra steps, and it burns the account. '
             'The waiting is the part that makes the later contact land.</div>')

    o.append('<p class="lede" style="margin-top:28px">When somebody is contacted, what they reacted to '
             'decides what is said. ' + ph('retarget_example', 'An organisation that read the page about a contract ending in November ') + 
             'gets a different opening line from one that only watched a video. That is the whole reason for '
             'running one ad per account rather than one ad for everybody. One rule holds throughout: '
             '<b>the ad is never mentioned.</b> You reference the subject they showed interest in, never the '
             'fact that you watched them click something.</p>')

    o.append('<div class="risk"><b>One risk worth knowing now</b>'
             '<p>LinkedIn hides engagement figures when too few people at an organisation have reacted, as a '
             'privacy measure. On a campaign aimed at one organisation at a time, that threshold is close to '
             'the volumes involved, so the first weeks may show less detail than expected.</p>'
             '<p>The way around it is to read the figures over a month rather than week by week, which is how '
             'this will be reported. It is worth saying in advance rather than explaining later.</p></div>')
    o.append("</section>")

    # 7. done / not done, side by side
    o.append('<section><h2><span class="n">08</span>Done, and not done</h2>')
    o.append('<p class="lede">Side by side, because a handover that only lists successes is a sales document.</p>')
    o.append('<div class="two"><div><h3>Done</h3><ul>')
    o.append(('<li>%s accounts chosen from published evidence<span class="why">Each one traces to a named '
              % nacc.capitalize())
             + ph('evidence_recap', 'contract, a value and an expiry date on the public record') + '.</span></li>')
    o.append('<li>One page and one ad per account<span class="why">Nothing is shared between them. Each '
             + ph('per_account_recap', 'argument is a different contract with a different date') + '.</span></li>')
    o.append('<li>The audience narrowed and measured<span class="why">Measured again after every change to '
             'the filters, so the figures on this page are current.</span></li>')
    if utm_std and utm_has_content:
        o.append('<li>Click tracking attached<span class="why">A visit arriving from one of these ads can be '
                 'told apart from ordinary traffic in your analytics.</span></li>')
    else:
        o.append('<li>Click tracking labels are on every ad set<span class="why">A visit from these ads carries '
                 'labels. Section 05 says what still has to change about them before your analytics will group '
                 'them as campaign traffic.</span></li>')
    o.append('<li>Audience expansion and the off-site network switched off<span class="why">Both are on by '
             'default and both would show the ads to people outside the %s organisations.</span></li>' % nacc)
    o.append('</ul></div><div><h3>Not done</h3><ul>')
    o.append('<li class="no">Nothing activated, nothing spent<span class="why">Every ad set is a draft. '
             'Going live is one deliberate action that has not been taken.</span></li>')
    o.append('<li class="no">Conversion tracking is not in place<span class="why">We can see a visit arrive. '
             'We cannot yet see what that visitor did next, which needs a tag on your site and a decision '
             'from you about what counts as a result.</span></li>')
    o.append('<li class="no">Stage two cannot run yet<span class="why">Following up with the people who '
             'reacted needs a separate LinkedIn permission on this account. Worth requesting now, because '
             'it takes weeks and the first stage is building that list from day one.</span></li>')
    o.append('<li class="no">The named buyers are incomplete<span class="why">Public records name the senior '
             'people at some of these organisations and not others.</span></li>')
    o.append('<li class="no">The daily budget was assumed<span class="why">A figure is set on each ad set so '
             'it is ready to run. It is a placeholder until you confirm it.</span></li>')
    if not (utm_std and utm_has_content):
        o.append('<li class="no">The click labels are not finished<span class="why">They are set, but not named '
                 'the way analytics tools read, and there is no label that differs per account. Section 05 has '
                 'the detail. Fixing it is a settings change and creates nothing.</span></li>')
    o.append('</ul></div></div></section>')

    # 6. the four things to decide
    o.append('<section><h2><span class="n">09</span>What we need from you before anything runs</h2>')
    o.append('<p class="lede">Four decisions. None of them are large, and all four block something specific.</p><ul>')
    o.append('<li>Confirm the daily budget<span class="why">Blocks activation. The figure currently set is a '
             'placeholder, not a recommendation.</span></li>')
    o.append('<li>Say what counts as a result on your site<span class="why">Blocks conversion tracking. A form, '
             'a demo request, a download. Once it is named it can be measured.</span></li>')
    o.append('<li>Request the follow-up permission from LinkedIn<span class="why">Blocks stage two. It takes '
             'weeks, so it should be requested before stage one starts rather than after.</span></li>')
    o.append(('<li>Check the %s accounts are ones you want to be seen by<span class="why">Blocks nothing ' % nacc)
             + 'technically, but ' + ph('activation_caution', 'these ads name a real contract to real staff and that should be a deliberate ')
             + 'choice.</span></li>')
    o.append("</ul></section>")

    # La remise est le document qui circule. S'il s'agit d'une demonstration, elle doit le dire
    # elle-meme: les pages de compte portent la mention, la remise ne la portait pas, et c'est
    # elle qu'on transfere. Trouve le 2026-09-24 avant de publier la remise Serval.
    _mode = {}
    _mp = run.inputs / "MODE.json"
    if _mp.exists():
        try: _mode = json.loads(_mp.read_text(encoding="utf-8"))
        except Exception: _mode = {}
    _disc = ""
    if (_mode.get("mode") or "").lower().startswith("demo"):
        _disc = ('<div class="flag" style="margin:0 0 20px">This is a <b>demonstration</b>. '
                 'It was produced independently and is <b>not affiliated with, endorsed by, or produced '
                 'on behalf of %s</b>, nor of the companies named in it. Names and marks belong to their '
                 'owners. Nothing was activated and nothing was spent. Where an offer appears, it was '
                 '<b>inferred by the operator</b> from %s\'s own published customer results, because %s '
                 'publishes no pricing and no trial terms, and has not been asked to approve any of this.'
                 '</div>' % (e(a.client), e(a.client), e(a.client)))
    o.append('<footer><div class="wrap" style="padding:0">%sBuilt %s. Every figure on this page traces to a '
             'published source named beside it. Nothing here is an estimate.<br><br>'
             '<em>Strategy &amp; GTM research by Jean Mundabi Fala</em></div></footer></div>'
             % (_disc, dt(date.today().isoformat())))

    doc = ("<!doctype html><html lang=en-GB><head><meta charset=utf-8>"
           "<meta name=viewport content='width=device-width,initial-scale=1'>"
           "<meta name=robots content='noindex,nofollow'>"
           "<title>%s: campaign handover</title>"
           "<link rel=preconnect href='https://fonts.googleapis.com'>"
           "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap' rel=stylesheet>"
           "<style>%s</style></head><body>%s</body></html>" % (e(a.client), CSS, "".join(o)))
    out = Path(a.out) if a.out else (run.campaign / "HANDOVER.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print("-> %s  %d bytes" % (out, len(doc)))

if __name__ == "__main__":
    main()

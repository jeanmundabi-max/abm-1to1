#!/usr/bin/env python3
"""
Build one landing page per named account, in the 13-section Mind-Reader structure.

    python3 build_page.py --run ~/path/to/client-run
    python3 build_page.py --run ... --only the-gym-group

The structure is the method and lives here. Everything client-specific lives in
<run>/04-pages/pages.json: the vendor's name, logo and contact URL, the brand tokens, the
disclaimer, and the map of slug to content module. **If adding an account means editing
this file, the account is in the wrong place.**

Content comes from <run>/04-pages/content_<account>.py, one dict per account, traced line
by line to that account's Mind-Reader survey and to the vendor's own published proof.

This is the content-fidelity pass. A design pass follows with the copy LOCKED, and a
visible-word diff must show zero content change. **After that, patch the pages, never
re-run this**, or the design pass is gone.
"""
import argparse, base64, html, importlib, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from runpaths import Run, add_run_arg

_ap = add_run_arg(argparse.ArgumentParser(description="build the account pages"))
_ap.add_argument("--only", help="one slug instead of all of them")
ARGS = _ap.parse_args()
RUN = Run(ARGS.run)
CFG = json.loads(RUN.need(RUN.pages / "pages.json").read_text(encoding="utf-8"))

V = CFG["vendor"]
ACCOUNTS = CFG["accounts"]
BRAND = (RUN.pages / CFG.get("brand_dir", "../03-creative/brand")).resolve()
OUT = RUN.live
sys.path.insert(0, str(RUN.pages))          # so content_<account>.py imports
e = html.escape

_b = CFG["brand"]
INK = _b["ink"]; BLUE = _b["blue"]; WASH = _b["wash"]; MUTED = _b["muted"]; RULE = _b["rule"]

GUARD = """
================================================================================
 REBUILT. The hero film is NOT in this output.
 The player lives in a patch, because these pages carry a design pass that this
 generator overwrites. Re-apply it now or the pages ship without the film in the
 first viewport, which is the failure logged as RUN-LOG row 8:

     python3 patch_vsl_recut.py --run <run>

================================================================================
"""

CSS = f"""
:root{{--ink:{INK};--blue:{BLUE};--wash:{WASH};--muted:{MUTED};--rule:{RULE}}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}
body{{font-family:Inter,system-ui,-apple-system,sans-serif;color:var(--ink);background:#fff;
 font-size:18px;line-height:1.62;overflow-x:clip}}
.wrap{{max-width:1060px;margin:0 auto;padding:0 26px}}
section{{padding:86px 0}}
h1,h2,h3{{line-height:1.09;letter-spacing:-.028em;font-weight:700}}
h1{{font-size:clamp(2.4rem,5.8vw,4.1rem)}}
h2{{font-size:clamp(1.75rem,3.5vw,2.6rem)}}
h3{{font-size:clamp(1.05rem,1.9vw,1.32rem);letter-spacing:-.015em}}
p{{max-width:66ch}}
em{{font-style:normal;color:var(--blue)}}
.lede{{font-size:clamp(1.04rem,1.75vw,1.24rem);color:var(--muted);line-height:1.58;margin-top:14px}}
.eyebrow{{font-size:.72rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
 color:var(--blue);margin-bottom:18px}}
.wash{{background:var(--wash)}} .dark{{background:var(--ink);color:#fff}}
.dark .lede{{color:rgba(255,255,255,.74)}} .dark .eyebrow{{color:#7CB8FF}}
.top{{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;
 padding:26px 0;border-bottom:1px solid var(--rule)}}
.top img{{height:26px}} .prep{{font-size:.86rem;color:var(--muted);display:flex;align-items:center;gap:10px}}
.prep img{{height:30px;border-radius:6px}}
.btn{{display:inline-block;background:var(--blue);color:#fff;text-decoration:none;font-weight:600;
 padding:16px 30px;border-radius:10px;font-size:1.02rem}}
.btn.ghost{{background:transparent;color:var(--ink);border:1.5px solid var(--rule)}}
.dark .btn.ghost{{color:#fff;border-color:rgba(255,255,255,.28)}}
.btns{{display:flex;gap:14px;flex-wrap:wrap;margin-top:32px}}
.stamp{{display:inline-flex;align-items:center;gap:10px;margin-top:30px;font-size:.9rem;
 color:var(--muted);border:1px solid var(--rule);border-radius:999px;padding:9px 18px}}
.dot{{width:8px;height:8px;border-radius:50%;background:var(--blue)}}
.checks{{margin-top:34px;display:grid;gap:14px}}
.check{{display:flex;gap:13px;align-items:flex-start;font-size:1.02rem}}
.check svg{{flex:none;width:21px;height:21px;margin-top:3px}}
.beats{{margin-top:34px;border-top:1px solid var(--rule)}}
.beat{{display:grid;grid-template-columns:88px 1fr;gap:24px;padding:20px 0;border-bottom:1px solid var(--rule)}}
.beat .tc{{font-variant-numeric:tabular-nums;color:var(--blue);font-weight:700;font-size:.95rem}}
.vslbox{{margin-top:30px;border:1.5px dashed var(--rule);border-radius:16px;padding:46px;text-align:center;
 color:var(--muted);font-size:.95rem;background:#fff}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin-top:34px}}
.stat{{border:1px solid var(--rule);border-radius:14px;padding:26px}}
.dark .stat{{border-color:rgba(255,255,255,.16)}}
.stat .k{{display:block;font-size:2rem;font-weight:700;letter-spacing:-.03em;color:var(--blue)}}
.stat .v{{display:block;margin-top:8px;font-size:.95rem;color:var(--muted)}}
.dark .stat .v{{color:rgba(255,255,255,.7)}}
.pain{{display:grid;grid-template-columns:64px 1fr;gap:26px;padding:36px 0;border-top:1px solid var(--rule)}}
.pain .num{{font-size:1.5rem;font-weight:700;color:var(--blue);letter-spacing:-.03em}}
blockquote{{margin:14px 0 0;padding:22px 26px;background:#fff;border-left:3px solid var(--blue);
 border-radius:0 12px 12px 0;font-size:1.06rem;line-height:1.5}}
.wash blockquote{{background:#fff}}
cite{{display:block;margin-top:12px;font-style:normal;font-size:.84rem;color:var(--blue);font-weight:600}}
.gap{{margin-top:34px;border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:#fff}}
.gaprow{{display:grid;grid-template-columns:190px 1fr 260px;gap:20px;padding:20px 26px;border-bottom:1px solid var(--rule);align-items:baseline}}
.gaprow:last-child{{border-bottom:0}}
.gaprow b{{font-size:1.35rem;letter-spacing:-.02em;color:var(--ink)}}
.gaprow .s{{font-size:.82rem;color:var(--muted)}}
.gaprow.hot{{background:#F2F8FF}} .gaprow.hot b{{color:var(--blue)}}
.cmp{{margin-top:34px;border:1px solid var(--rule);border-radius:16px;overflow:hidden}}
.cmphead,.cmprow{{display:grid;grid-template-columns:1fr 1fr}}
.cmphead div{{padding:18px 26px;font-weight:700;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase}}
.cmphead .a{{background:#F7F8FA;color:var(--muted)}} .cmphead .b{{background:var(--blue);color:#fff}}
.cmprow div{{padding:22px 26px;border-top:1px solid var(--rule);font-size:1rem}}
.cmprow .a{{color:var(--muted);background:#FBFCFD}} .cmprow .b{{background:#fff;font-weight:500}}
.steps{{display:grid;gap:20px;margin-top:34px}}
.step{{border:1px solid var(--rule);border-radius:16px;padding:30px;background:#fff;
 display:grid;grid-template-columns:56px 1fr;gap:22px}}
.step .n{{font-size:1.1rem;font-weight:700;color:var(--blue)}}
.pill{{display:inline-block;margin-top:14px;background:#EAF3FF;color:var(--blue);font-weight:600;
 font-size:.8rem;padding:6px 13px;border-radius:999px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:20px;margin-top:34px}}
.card{{border:1px solid var(--rule);border-radius:16px;padding:28px;background:#fff}}
.dark .card{{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.14)}}
.card .m{{font-size:1.7rem;font-weight:700;color:var(--blue);letter-spacing:-.03em}}
.card .ml{{font-size:.86rem;color:var(--muted);margin-bottom:16px}}
.dark .card .ml{{color:rgba(255,255,255,.62)}}
.card q{{quotes:none}} .card p.q{{font-size:.99rem;line-height:1.52}}
.offer{{margin-top:34px;display:grid;gap:0;border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:#fff}}
.orow{{display:grid;grid-template-columns:250px 1fr;gap:24px;padding:24px 28px;border-bottom:1px solid var(--rule)}}
.orow:last-child{{border-bottom:0}}
.orow .mp{{margin-top:10px;font-size:.93rem;color:#9A3412;background:#FFF7ED;border-radius:8px;padding:10px 14px;display:inline-block}}
.tiers{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px;margin-top:34px}}
.tier{{border:1px solid var(--rule);border-radius:14px;padding:24px;background:#fff}}
.tier.on{{border-color:var(--blue);border-width:2px;box-shadow:0 12px 30px rgba(26,136,255,.12)}}
.tier b{{display:block;font-size:1.1rem;margin-bottom:8px}}
.tier .yours{{display:inline-block;margin-bottom:10px;background:var(--blue);color:#fff;font-size:.7rem;
 font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:5px 11px;border-radius:999px}}
details{{border-top:1px solid var(--rule);padding:22px 0}}
details summary{{cursor:pointer;font-weight:600;font-size:1.08rem;list-style:none;display:flex;
 justify-content:space-between;gap:20px;align-items:flex-start}}
details summary::-webkit-details-marker{{display:none}}
details summary::after{{content:"+";color:var(--blue);font-weight:700;font-size:1.5rem;line-height:1}}
details[open] summary::after{{content:"\\2212"}}
details p{{margin-top:14px;color:var(--muted)}}
.note{{margin-top:26px;font-size:.9rem;color:var(--muted);border-left:2px solid var(--rule);padding-left:18px}}
.dark .note{{color:rgba(255,255,255,.62);border-color:rgba(255,255,255,.2)}}
footer{{padding:52px 0;border-top:1px solid var(--rule);font-size:.84rem;color:var(--muted)}}
.disc{{margin-top:14px;max-width:78ch;font-size:.76rem;line-height:1.6}}
@media(max-width:780px){{
 .gaprow,.cmphead,.cmprow,.orow,.step,.pain,.beat{{grid-template-columns:1fr;gap:10px}}
 section{{padding:60px 0}}
}}
"""

TICK = f'<svg viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>'


def img(name, alt, h=26):
    p = BRAND / name
    if not p.exists():
        return f'<strong>{e(alt)}</strong>'
    return f'<img src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}" alt="{e(alt)}">'


def build(C, NAME, LOGO, TITLE):
    h = C["hero"]; v = C["vsl"]; sp = C["socialproof"]; pn = C["pains"]; gp = C["gap"]
    cm = C["compare"]; me = C["mechanism"]; pr = C["proof"]; of = C["offer"]
    gu = C["guarantee"]; pc = C["pricing"]; ql = C["qualify"]; fq = C["faq"]; fn = C["final"]

    bullets = "".join(f'<div class="check">{TICK}<span>{e(b)}</span></div>' for b in h["bullets"])
    # The written-out transcript sits at position 2 of 14, directly under the hero, and
    # repeats in text the film the reader has just been shown. On a cold page that stops the
    # momentum before it starts, so a content module may switch it off with
    # C["vsl"]["show_transcript"] = False. DEFAULT IS TRUE, so an unported run is byte
    # identical. patch_vsl_recut.py still needs C["vsl"] to exist, so the key stays and only
    # the rendering is suppressed.
    beats = "".join(f'<div class="beat"><div class="tc">{e(t)}</div><div><h3>{e(ti)}</h3><p class="lede" style="margin-top:6px">{e(bd)}</p></div></div>'
                    for t, ti, bd in v["beats"])
    stats = "".join(f'<div class="stat"><span class="k">{e(k)}</span><span class="v">{e(val)}</span></div>'
                    for k, val in sp["stats"])
    pains = "".join(
        f'<div class="pain"><div class="num">{e(i["n"])}</div><div><h3>{e(i["t"])}</h3>'
        f'<blockquote>&ldquo;{e(i["q"])}&rdquo;<cite>{e(i["src"])}</cite></blockquote>'
        f'<p class="lede">{e(i["why"])}</p></div></div>' for i in pn["items"])
    gaps = "".join(
        f'<div class="gaprow{" hot" if "one percentage point" in lbl else ""}"><b>{e(k)}</b>'
        f'<span>{e(lbl)}</span><span class="s">{e(src)}</span></div>' for k, lbl, src in gp["rows"])
    cmps = "".join(f'<div class="cmprow"><div class="a">{e(a)}</div><div class="b">{e(b)}</div></div>'
                   for a, b in cm["rows"])
    steps = "".join(f'<div class="step"><div class="n">{e(n)}</div><div><h3>{e(t)}</h3>'
                    f'<p class="lede" style="margin-top:8px">{e(d)}</p><span class="pill">{e(p)}</span></div></div>'
                    for n, t, d, p in me["steps"])
    proofs = "".join(f'<div class="card"><div class="m">{e(c["metric"])}</div><div class="ml">{e(c["label"])}</div>'
                     f'<p class="q">&ldquo;{e(c["q"])}&rdquo;</p><cite>{e(c["who"])}</cite></div>'
                     for c in pr["cards"])
    offers = "".join(f'<div class="orow"><div><h3>{e(t)}</h3></div><div><p>{e(d)}</p>'
                     f'<div class="mp">{e(m)}</div></div></div>' for t, d, m in of["items"])
    gus = "".join(f'<div class="card"><h3>{e(t)}</h3><p class="lede" style="margin-top:8px">{e(d)}</p></div>'
                  for t, d in gu["points"])
    tiers = "".join(f'<div class="tier{" on" if on else ""}">{"<span class=\'yours\'>Your tier</span>" if on else ""}'
                    f'<b>{e(t)}</b><span class="v" style="font-size:.93rem;color:var(--muted)">{e(d)}</span></div>'
                    for t, d, on in pc["tiers"])
    faqs = "".join(f'<details{" open" if op else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>'
                   for q, a, op in fq["items"])

    walkthrough = ("" if v.get("show_transcript") is False else
      '<section class="wash"><div class="wrap">\n'
      ' <div class="eyebrow">%s</div><h2>%s</h2>\n'
      ' <div class="vslbox">%s</div>\n'
      ' <div class="beats">%s</div>\n'
      '</div></section>' % (e(v.get("eyebrow", "The walkthrough")), e(v["h2"]),
                            e(v["note"]), beats))

    return f"""<!doctype html><html lang="en-GB"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(TITLE)} | For {e(NAME)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>

<div class="wrap"><div class="top">{img(V["logo"], V["name"])}
<span class="prep">Prepared for {img(LOGO,NAME,30)}</span></div></div>

<section><div class="wrap">
 <div class="eyebrow">{e(h["eyebrow"])}</div>
 <h1>{h["h1"]}</h1>
 <p class="lede">{e(h["sub"])}</p>
 <div class="checks">{bullets}</div>
 <div class="btns"><a class="btn" href="{ql["href"]}">{e(h["cta"])}</a>
  <a class="btn ghost" href="{V["contact_url"]}">{e(h["cta2"])}</a></div>
 <div class="stamp"><span class="dot"></span>{e(h["stamp"])}</div>
 <p class="lede" style="margin-top:22px;font-size:.9rem">{e(h["trust"])}</p>
</div></section>

{walkthrough}

<section class="dark"><div class="wrap">
 <div class="eyebrow">{e(sp.get("eyebrow","Somebody in your business already did this"))}</div>
 <h2>{e(sp["line"])}</h2>
 <blockquote style="background:rgba(255,255,255,.06);border-left-color:#7CB8FF;color:#fff;margin-top:26px">
  &ldquo;{e(sp["quote"])}&rdquo;<cite style="color:#7CB8FF">{e(sp["who"])}</cite></blockquote>
 <div class="stats">{stats}</div>
</div></section>

<section><div class="wrap">
 <div class="eyebrow">{e(pn.get("eyebrow","What your members wrote"))}</div><h2>{e(pn["h2"])}</h2>
 <p class="lede">{e(pn["lede"])}</p>
 {pains}
</div></section>

<section class="wash"><div class="wrap">
 <div class="eyebrow">The revenue gap</div><h2>{e(gp["h2"])}</h2>
 <p class="lede">{e(gp["lede"])}</p>
 <div class="gap">{gaps}</div>
 <div class="card" style="margin-top:24px"><h3>{e(gp["kicker_t"])}</h3>
  <p class="lede" style="margin-top:10px">{e(gp["kicker"])}</p></div>
</div></section>

<section><div class="wrap">
 <div class="eyebrow">Belief breaking</div><h2>{e(cm["h2"])}</h2>
 <p class="lede">{e(cm["lede"])}</p>
 <div class="cmp"><div class="cmphead"><div class="a">What has been tried</div><div class="b">What changes how the money moves</div></div>{cmps}</div>
</div></section>

<section class="wash"><div class="wrap">
 <div class="eyebrow">The mechanism</div><h2>{e(me["h2"])}</h2>
 <p class="lede">{e(me["lede"])}</p>
 <div class="steps">{steps}</div>
 <p class="lede" style="margin-top:26px"><strong>{e(me["close"])}</strong></p>
</div></section>

<section class="dark"><div class="wrap">
 <div class="eyebrow">Proof</div><h2>{e(pr["h2"])}</h2>
 <p class="lede">{e(pr["lede"])}</p>
 <div class="cards">{proofs}</div>
 <div class="note">{e(pr["note"])}</div>
</div></section>

<section><div class="wrap">
 <div class="eyebrow">What is included</div><h2>{e(of["h2"])}</h2>
 <p class="lede">{e(of["lede"])}</p>
 <div class="offer">{offers}</div>
</div></section>

<section class="wash"><div class="wrap">
 <div class="eyebrow">Risk</div><h2>{e(gu["h2"])}</h2>
 <p class="lede">{e(gu["lede"])}</p>
 <div class="cards">{gus}</div>
 <div class="card" style="margin-top:22px;border-color:{BLUE}"><h3>{e(gu["fear_t"])}</h3>
  <p class="lede" style="margin-top:10px">{e(gu["fear"])}</p></div>
</div></section>

<section><div class="wrap">
 <div class="eyebrow">Pricing</div><h2>{e(pc["h2"])}</h2>
 <p class="lede">{e(pc["lede"])}</p>
 <div class="tiers">{tiers}</div>
 <div class="note">{e(pc["note"])}</div>
</div></section>

<section class="wash"><div class="wrap">
 <div class="eyebrow">Another way in</div><h2>{e(ql["h2"])}</h2>
 <p class="lede">{e(ql["lede"])}</p>
 <div class="btns"><a class="btn" href="{ql["href"]}">{e(ql["cta"])}</a></div>
 <p class="lede" style="margin-top:16px;font-size:.92rem">{e(ql["after"])}</p>
</div></section>

<section><div class="wrap">
 <div class="eyebrow">Objections</div><h2>{e(fq["h2"])}</h2>
 <div style="margin-top:28px">{faqs}</div>
</div></section>

<section class="dark"><div class="wrap" style="text-align:center">
 <h2>{e(fn["h2"])}</h2>
 <p class="lede" style="margin:18px auto 0">{e(fn["recap"])}</p>
 <div class="btns" style="justify-content:center"><a class="btn" href="{ql["href"]}">{e(fn["cta"])}</a>
  <a class="btn ghost" href="{V["contact_url"]}">{e(fn["cta2"])}</a></div>
 <p class="lede" style="margin:22px auto 0;font-size:.9rem">{e(fn["trust"])}</p>
</div></section>

<footer><div class="wrap">
 <div>{CFG["byline"]}</div>
 <p class="disc">{DISCLAIMER}</p>
</div></footer>
</body></html>"""



DISCLAIMER = None   # set per account inside main, because it names the account

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    global DISCLAIMER
    for slug, a in ACCOUNTS.items():
        if ARGS.only and slug != ARGS.only:
            continue
        C = importlib.import_module(a["module"]).C
        DISCLAIMER = CFG["disclaimer"].format(vendor=e(V["name"]), account=e(a["name"]))
        p = OUT / f"{slug}.html"
        p.write_text(build(C, a["name"], a["logo"], a["title"]))
        print(f"wrote {p}  {p.stat().st_size:,} bytes")
    print(GUARD)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The gold standard gate. A page or an ad card is not finished until this passes.

    python3 page_standard.py page <build dir>      # the dir, not the html: process artefacts count
    python3 page_standard.py ad   <card.png> [...]
    python3 page_standard.py set  <dir of builds>   # every sibling, and the spread

Why this exists, written on the day it was needed.

On 2026-09-08 the same operator built a Revolut page and a WYN page a few hours apart. The
Revolut one ran the play: an interview and a BRIEF, a page grammar, a bespoke film, a
signature move, four rounds of rejection. The WYN one was a single pass generator script.
Measured against each other the second had 41% of the words, 50% of the sections, 13% of the
interactive elements and no film at all.

The lessons from the Revolut run HAD been consigned that same morning. They were consigned as
prose, into files an operator in a hurry does not open. **An instruction is not a mechanism.**
The quality on the first page came from a human rejecting the work four times, and that does
not scale and does not travel.

So this file encodes the standard as counts and required artefacts, and exits non-zero.
It cannot judge whether a page is good. It can refuse a page that is obviously thin, which is
the failure that actually happened.

Every floor is measured against the Hays build, then set BELOW it, so the gate marks the
bottom of acceptable rather than a copy of one page.
"""
import argparse, json, re, sys
from pathlib import Path

# --------------------------------------------------------------------------- page
# Counting words and sections is optimising the wrong variable. A WYN page cleared every count
# below and was still pale beside the build the floors were measured from, because it was a
# DOCUMENT and the gold standard is a scroll-driven film. These three rules carry that, and rule
# 3 is the one that matters most: a score the page does not implement is a fiction.
SPINE_RULES = [
 ("acts",        4, "The page is scroll-driven, not a document. Acts with declared spans."),
 ("respite",     1, "THE RULE OF RESPITE. After a dense beat, a beat that asks nothing: one "
                    "sentence, no figure, no table, no accent. A page that is loud all the way "
                    "is as flat as one that is quiet all the way, and the reader has nowhere to "
                    "put what they just took in."),
 ("proof",       1, "Named proof, with attribution and its qualifier. Not a logo wall."),
 ("cues",        8, "Cues that fire on act progress. The wheel is the instrument."),
 ("progress",    1, "Bespoke behaviour driven off the act progress variable, not off a timer."),
]
PAGE_RULES = [
 # key,                 floor, what it is, and why the page is worse without it
 ("words",        2800, "A cold page carries the whole argument. Under this it is a flyer."),
 ("sections",       12, "Hero, evidence, mechanism, cost of inaction, offer, proof, sample, "
                        "what happens after, committee, objections, close."),
 ("figures",         2, "The account's own numbers DRAWN, not only quoted. A page that only "
                        "quotes is a document."),
 ("interactive",     6, "At least one object the reader can move. An argument they perform is "
                        "an argument they keep."),
 ("objections",     12, "Everything anyone has asked, answered. Under twelve, the awkward ones "
                        "have been left out."),
 ("forms",           1, "Something on the page must receive the yes."),
 ("routes",          2, "Two ways in with equal weight, and the low trust one is not an "
                        "afterthought."),
 ("committee",       1, "A seat each for the buying committee, and a paragraph to forward."),
 ("computed_dates",  1, "Any interval is computed at open time. A hardcoded countdown is wrong "
                        "the next morning."),
 ("disclosure",      1, "The footer discloses what was inferred, away from the CTA."),
]
# The vendor narrating itself. Nobody buys a product from the vendor's own wall.
# A page is written from the buyer's seat (sops/07b). These strings mean it was not.
VENDOR_VOICE = [r"in [A-Z][A-Za-z']+ own words", r"own words", r"sells three things", r"Pricing is public",
                r"The mechanism, in one sentence"]
REQUIRED_FILES = [
 ("BRIEF.md",  "The interview, verbatim. Without it the page was built from assumptions."),
 ("SCORE.md",  "The grammar, the feeling curve, the acts and the signature move."),
]
OPTIONAL_FILES = [
 ("hero.mp4",  "The bespoke film. Not every grammar needs one, but its absence must be a "
               "decision recorded in SCORE.md, not an omission."),
 ("contact-sheet.png", "The fold, five film frames and the card on one picture, made by "
               "scripts/contact_sheet.py and SENT to the human before the next account is "
               "built. A gate result is not a view of the creative."),
]

def _respite(html):
    """A breathing beat: a stage whose whole content is short prose, with no table, no figure
    and no form. Counted on the ACTS, because the long-form body is allowed to be dense."""
    n = 0
    for blk in re.findall(r'<section[^>]*data-sc-act=.*?</section>', html, re.S):
        if re.search(r'<table|<svg|<form|<video|<details', blk): continue
        words = len(re.sub(r"<[^>]+>", " ", blk).split())
        if words <= 90: n += 1
    return n

def measure_page(html):
    body = re.sub(r"<(script|style).*?</\1>", "", html, flags=re.S)
    txt  = re.sub(r"<[^>]+>", " ", body)
    return {
      "words":       len(txt.split()),
      "sections":    len(re.findall(r"<section", html)),
      "figures":     len(re.findall(r"<svg|<canvas", html)),
      "interactive": len(re.findall(r"addEventListener|pointerdown|oninput|<input|<details", html)),
      "objections":  len(re.findall(r"<details|<dt[\s>]", html)),
      "forms":       len(re.findall(r"<form", html)),
      "routes":      len(re.findall(r'class="(?:rt|route)(?:["\s])|name="route"', html)),
      "committee":   int(bool(re.search(r"committee|seats? this has to survive|what they ask first",
                                        html, re.I))),
      "computed_dates": int(bool(re.search(r"new Date\(|toLocaleDateString|setDate\(", html))),
      "disclosure":  int(bool(re.search(r"not affiliated with|inferred by the operator", html, re.I))),
      "acts":        len(re.findall(r'data-sc-act=', html)),
      "cues":        len(re.findall(r'data-sc-cue=', html)),
      "progress":    len(re.findall(r'--sc-p|getPropertyValue\([\'"]--sc', html)),
      "respite":     _respite(html),
      # An attributed third-party claim. `data-proof` is the convention going forward; the
      # `cite` class is how the first build marked its sources, and retro-editing the gold
      # standard so it passes a gate written after it would be fitting the ruler to the wood.
      "proof":       len(re.findall(r'data-proof|class="[^"]*\bcite\b[^"]*"', html)),
    }

def check_page(d):
    d = Path(d)
    idx = d / "index.html"
    if not idx.exists(): sys.exit("no index.html in %s" % d)
    html = idx.read_text(encoding="utf-8")
    m = measure_page(html)
    fails = []
    print("PAGE  %s" % idx)
    for k, floor, why in SPINE_RULES + PAGE_RULES:
        ok = m[k] >= floor
        print("  %-16s %6s  floor %-5s %s" % (k, m[k], floor, "ok" if ok else "FAIL"))
        if not ok: fails.append("%s: %d, floor %d. %s" % (k, m[k], floor, why))
    # THE SCORE MUST BE IMPLEMENTED. SCORE.md for the pale build declared a grammar and seven
    # acts and the page had none of them. Writing a score the page does not implement is worse
    # than writing no score, because it makes the process look like it ran.
    sc = d / "SCORE.md"
    if sc.exists():
        txt = sc.read_text(encoding="utf-8")
        rows = re.findall(r"^\s*\|\s*\d+\s*\|", txt, re.M)
        declared = len(rows)
        if declared:
            ok = m["acts"] >= declared
            print("  %-16s %6s  score declares %-3s %s" % ("acts vs SCORE", m["acts"], declared,
                  "ok" if ok else "FAIL"))
            if not ok:
                fails.append("SCORE.md declares %d acts and the page implements %d. A score the "
                             "page does not implement is a fiction." % (declared, m["acts"]))
        sig = re.search(r"[Ss]ignature move[:\s]*([A-Za-z ,'\-]+)", txt)
        if sig:
            key = sig.group(1).strip().split(".")[0].lower()
            words = [w for w in re.findall(r"[a-z]{4,}", key) if w not in
                     ("signature","move","the","and","never","with")]
            hit = any(w in html.lower() for w in words) if words else True
            print("  %-16s %6s  %s" % ("signature move", "yes" if hit else "no",
                  "ok" if hit else "FAIL"))
            if not hit:
                fails.append("SCORE.md names a signature move (%s) that appears nowhere in the "
                             "page." % key)
    # Un geste signature dans un bloc a cue est rendu inerte par le moteur. Deux lignes le
    # sauvent et un oubli est invisible a la lecture: la page est belle et ne repond pas.
    if re.search(r"pointerdown", html):
        esc = bool(re.search(r"pointer-events\s*:\s*auto\s*!important", html))
        print("  %-16s %6s  %s" % ("geste vivant", "yes" if esc else "no", "ok" if esc else "FAIL"))
        if not esc:
            fails.append("the page has a pointer gesture and no pointer-events:auto!important on "
                         "its block. The engine hands pointer events back only to a block that is "
                         "half visible, so the gesture is dead to a press. sops/07b.")
    hits = [p for p in VENDOR_VOICE if re.search(p, html)]
    print("  %-16s %6s  %s" % ("buyer's seat", "no" if hits else "yes", "ok" if not hits else "FAIL"))
    if hits:
        fails.append("vendor voice on the page (%s). The page is written from the buyer's seat, "
                     "proof comes from peers, the vendor never narrates itself. sops/07b." % ", ".join(hits))
    for f, why in REQUIRED_FILES:
        ok = (d / f).exists()
        print("  %-16s %6s  %s" % (f, "yes" if ok else "no", "ok" if ok else "FAIL"))
        if not ok: fails.append("%s missing. %s" % (f, why))
    for f, why in OPTIONAL_FILES:
        print("  %-16s %6s  %s" % (f, "yes" if (d/f).exists() else "no",
              "ok" if (d/f).exists() else "note: %s" % why))
    return fails

# ----------------------------------------------------------------------------- ad
def check_ad(paths):
    """The card is checked by still_guard for fit; here we check the SYSTEM around it."""
    fails = []
    for p in paths:
        # resolve first: Path('x.png').parent is '.', and '.'.parent is '.' again, so a bare
        # filename searched for the brief and the copy in the wrong folder and reported both
        # missing. Caught 2026-09-11 on a card whose brief and copy were both present.
        p = Path(p).resolve()
        d = p.parent
        print("AD    %s" % p)
        # A brief only counts if it is ABOUT THIS CARD and NEWER THAN IT. The first version
        # accepted any file named *BRIEF* anywhere in the creative folder, and duly passed a
        # WYN card that never saw the council, on the strength of a brief from another session.
        # A gate that passes the wrong thing is worse than no gate.
        # 1x1 joined 4x5 on 2026-09-11: LinkedIn's spec says vertical does not deliver to desktop,
        # so every card now has a square variant, and the gate must recognise it as the same card.
        slug = p.stem.replace("-ad-4x5", "").replace("-ad-1x1", "").replace("-ad", "")
        mt = p.stat().st_mtime
        cand = list(d.glob("*BRIEF*")) + list(d.glob("*COUNCIL*")) + \
               list(d.parent.glob("*BRIEF*")) + list(d.parent.glob("*COUNCIL*"))
        brief = [c for c in cand
                 if c.stat().st_mtime >= mt - 86400
                 and (slug in c.read_text(encoding="utf-8", errors="ignore").lower()
                      or slug in c.name.lower())]
        cp = (d.parent / "copy")
        copy = [c for c in (cp.glob("LOCKED-*.md") if cp.exists() else [])
                if slug in c.read_text(encoding="utf-8", errors="ignore").lower()]
        for label, hit, why in (
            ("council brief", brief, "A brief naming THIS card, written no earlier than the day it was "
                                     "rendered. The council directed the Revolut cards and the brief "
                                     "recorded why the idea won. Without it the card is one "
                                     "person's first idea."),
            ("locked copy",    copy,  "The body copy, frozen, with the checks that changed it. "
                                      "Headline and image are create-only on LinkedIn, so the "
                                      "copy has to be settled before the first push.")):
            print("  %-16s %6s  %s" % (label, "yes" if hit else "no", "ok" if hit else "FAIL"))
            if not hit: fails.append("%s: %s missing. %s" % (p.name, label, why))
    return fails

# --------------------------------------------------------------------------- set
def check_set(root):
    """Every build under one directory, and the SPREAD between them.

    Added 2026-09-08. On 3 September a clone script produced three pages from one thin source.
    On 7 September one of the three was rebuilt, 486 words to 3,971, and the other two were left
    live at the old depth for five days. Nobody inside the work notices, because the file you
    just improved is the file you look at.

    A set whose members sit at two standards is worse than a set uniformly at the lower one: the
    claim the set makes is that each member was built for its own case. So raising one member is
    not finished until every sibling passes, and the spread between them is bounded.
    """
    root = Path(root)
    builds = sorted(d for d in root.iterdir() if d.is_dir() and (d / "index.html").exists())
    if not builds: sys.exit("no build folders under %s" % root)
    fails, words = [], {}
    for d in builds:
        f = check_page(d)
        words[d.name] = measure_page((d / "index.html").read_text(encoding="utf-8"))["words"]
        fails += ["%s: %s" % (d.name, x) for x in f]
        print()
    lo, hi = min(words.values()), max(words.values())
    print("SET   %d builds   words %d to %d   spread %.1fx"
          % (len(builds), lo, hi, hi / max(lo, 1)))
    for n, w in sorted(words.items(), key=lambda kv: kv[1]):
        print("  %-16s %5d" % (n, w))
    # 2x is generous: the three Revolut pages that shipped together sit inside 1.1x of each
    # other, and the failure this catches was 8x.
    if lo and hi / lo > 2.0:
        fails.append("the thinnest build has %d words and the fattest has %d, a %.1fx spread. "
                     "One of these was raised and the others were not." % (lo, hi, hi / lo))
    return fails

ap = argparse.ArgumentParser()
ap.add_argument("what", choices=["page", "ad", "set"])
ap.add_argument("target", nargs="+")
A = ap.parse_args()
fails = (check_page(A.target[0]) if A.what == "page" else
         check_set(A.target[0])  if A.what == "set"  else check_ad(A.target))
print()
if fails:
    print("NOT FINISHED. %d gate(s) failed:" % len(fails))
    for f in fails: print("  - %s" % f)
    sys.exit(1)
print("PASS")

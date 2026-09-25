# WYN run, 2026-09-08. HMRC rebuilt to the gold standard.

## What was found before anything was built

**The live page carried a countdown that had been wrong for eighteen days.** `wyn/hmrc/` says the
AWS call-off "ends in 101 days", frozen on 21 August 2026. On 8 September it is 83.

**The offer as written dies in governance.** A civil servant cannot engage a third party on a share
of savings through a form, nor hand a live vendor proposal to an unappointed party. So the page
leads with the route that asks for nothing: a document built entirely from HMRC's own published
award notices.

**The direction nearly shipped as a lie.** Home Office pays £150,196,594 a year and HMRC
£116,746,575, same supplier, same 30 November 2026 expiry. The comparison is devastating for the
Home Office and flattering to HMRC. A hook saying "you are overpaying" would have been false in
front of the one reader who can check it.

## The first attempt, and why it failed

Built as a one-pass generator script. Against the Hays build: 41% of the words, 50% of the
sections, 13% of the interactive elements, no film. It cleared every count in the gate and was
still pale, because the gate counted and did not check that the page implemented its own plan.
`SCORE.md` declared a ruled ledger grammar and seven acts. The page implemented zero.

## The rebuild

Council of four directors in parallel, converging without contact on **the accent belongs to the
date, not the money**. THE RAIL from the McDonald's director, grafted with Beats' one-object accent
rule, Super Bowl's align-on-the-date, Apple's permanent source line at 20% ink.

Seven real acts, 25 cues, engine mounted, the ruled left margin carrying the act name, and the
held verdict driven off act progress. Named proof from WYN's own blog: four UK institutions, each
with its limit stated. 3,229 words, 15 sections.

## Defects my own tools caught, and two they invented

- Motion QA: 27 identical frames at 15.57s. The travelling mark was too faint to register and I
  had skipped the scale creep the council prescribed. After the fix: 900 frames, body dwell 2.
- `still_guard` measured the BRIGHTEST ink against the ground, which assumes a dark page. On WYN's
  white card it scored 1.3:1 on near-black type. Now takes whichever extreme is furthest from the
  measured ground. Regression: 92 of 92.
- **Two false failures from my own harness.** A test server with no HTTP range support made a
  working scrub look completely broken. A test that clicked 3,600px below the viewport reported a
  working drag as dead. Both nearly caused a fix to code that was not broken.

## Live

`https://jeanmundabi-max.github.io/mdb-abm/wyn/hmrc-v2/` 200, 41,015 bytes. Nothing is in a
LinkedIn account for WYN. No ad sets, no spend.

_Strategy & GTM research by Jean Mundabi Fala_

---

## Later the same day. The other three accounts, and HMRC finally published

**Two findings before any building.** The new HMRC page had never been published: all four live
WYN URLs were still serving the 52KB single-pass generator pages from 21 August, with zero acts.
And the other three accounts had no new build at all.

**`07-pages/build_account.py`.** The HMRC page's grammar, chrome, act shape, close and signature
move, carried across unchanged, because four pages for one advertiser are one system. What differs is
the world, the evidence and the copy, and here that is not decoration: the four departments have
genuinely different registers.

| Account | The finding the page is built on |
|---|---|
| HMRC | sixteen contracts, the largest renews first, eight buyers to compare against |
| Home Office | two suppliers at opposite ends of the register. Amazon Web Services has **8 other public buyers**; Phoenix Software has **77**. The Home Office is the largest line on both |
| MHCLG | the register is filed under **two buyer names**, and six of the eight contracts sit under the name the department stopped using. £12,108,289 of £17,145,869 a year is invisible to anyone searching the current name |
| UKHSA | **nine contracts, £23,022,463 a year, all ending 31 March 2027**. And the two largest suppliers appear on **no other buyer's live notice anywhere**, so for 61% of the annual value a comparison cannot be produced by anybody |

**The UKHSA page says the second half out loud**, in the peak act and in the ad copy. A weaker
version would have promised the benchmark and let the reader find the hole in the document. That
version gets read once.

**A number that nearly shipped wrong.** The Home Office AWS call-off at £150,196,594 a year is the
**second** largest annual value on the register, not the largest. Highways England's is
£250,171,233. Checked before it was written, not after.

**Seats left unnamed on purpose.** The published organogram returns this run holds cover HMRC and
the Home Office. There is no current return naming the finance and commercial seats at MHCLG or
UKHSA, so those rows carry the title and no name, and the page says why. Filling them with
plausible names would have been inventing them.

**Films and cards.** Same THE RAIL direction, one accent, on the date, at 24s. The Home Office
card was given its own hook, **"The biggest line on both lists"**, rather than reusing HMRC's
"A framework caps. A call-off pays." Two accounts in one campaign wearing the same headline is
the template tell the whole run exists to avoid.

**Gates:** all three pages PASS on all seventeen checks. 3,729 / 3,633 / 3,837 words, fifteen
sections, seven acts each, `acts vs SCORE` clean. `motion_hash.py` passes on all three films,
longest static run 4 against a floor of 6. `still_guard.py` passes on all three cards at 17.8:1.
The ad gate passes once the locked copy exists for each.

**Published.** All four live and verified: `wyn/hmrc/` 41,015 bytes, `wyn/home-office/` 44,766,
`wyn/mhclg/` 42,961, `wyn/ukhsa/` 45,365, seven acts each. The four old generator pages are gone.

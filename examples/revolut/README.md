# Revolut Business, three listed UK companies

**The client:** Revolut Business sells currency exchange at the interbank rate to companies
paying a spread to their bank.

**The run:** layer 2, a demonstration. Built as drafts, never activated. Five accounts were
selected and **three shipped**, which is the most useful thing about it.

## The page that refuses to give you a number

Every other page in this repository puts a figure in front of the reader. These do not.

> "Conversion volume is not public and neither is the spread you are paying, so no honest page
> can tell you the figure. What it can do is show you the shape of it. Move these and the
> arithmetic is yours."

Two sliders. The reader supplies the volume and the spread, the page does the arithmetic in
front of them, and nothing is asserted about the company. Compare it against the Serval pages,
which answer the same problem by setting the dial to the reader's own rate against a filed
headcount. Two different solutions to "how do you put a number on a cold page without
inventing one".

| Account | Sector | Reachable |
|---|---|---|
| [Hays](accounts/hays/) | Recruitment | 1,100 |
| [Currys](accounts/currys/) | Electrical retail | 1,200 |
| [Renishaw](accounts/renishaw/) | Precision engineering | 310 |

## Why two accounts were dropped after the research was done

**Games Workshop and Bunzl both cleared the evidence gate and neither could be reached.** The
audience did not exist on LinkedIn at a size that will deliver. That research was wasted, and
the lesson is an ordering one: **check reachability before you check evidence.** Reachability
is one API call. Evidence is hours of filings.

**Smith & Nephew was dropped for the opposite reason.** It cleared reachability, then failed on
evidence: currency movement is a *tailwind* for them, 230 basis points on H1 2026 revenue, and
they report in USD. The pitch would have been backwards.

## The legal name is the wrong query

Searching LinkedIn for the registered name failed on all three:

- **"Renishaw plc"** returned no match at all
- **"Games Workshop Group plc"** returned no match at all
- **"Hays plc"** returned one result, **"works of Hays PLC"**, a clone page with nobody on it

All three trading names resolved first try. A company's registered name and the name on its
LinkedIn page are different strings, and searching the wrong one returns `0`, which reads
exactly like a company too small to bother with.

## Three defects that shipped, and were caught

**All three footers cited Renishaw's results.** On Currys and Hays that was factually false, on
pages whose entire credibility rests on citation accuracy. The clone step substituted the
citation in the body and missed the one in the footer. *A substitution that misses a citation
produces a lie with a date on it.*

**Three pages were live for five days at three very different depths.** One page was rebuilt
from 486 words to 3,971 and the other two were left on the thin clone, failing the quality gate
on seven checks each, while the campaign's whole claim was that each page was built for one
company.

**The figure on the page did not match the figure on the ad.** Message match now holds.

## One piece of proof that was found and not used

Revolut publish a customer case study with a video on it. The film was downloaded, checked
frame by frame, and turned out to be a five second decorative loop of SIM cards. Presenting it
as proof on film would have overstated it, so it is not used and **it is not in this
repository**. The case study text is real, is quoted, and stays.

## What else is here

- [The handover](handover.html)
- [The run log](RUN-LOG.md) · 5,500 words. The longest and the most self-critical of the four

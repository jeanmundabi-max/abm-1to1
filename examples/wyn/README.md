# WYN, four government departments

**The client:** WYN Procurement helps organisations pay less for software they have already
bought, by comparing what a supplier charges them against what the same supplier charges
other buyers.

**The run:** layer 2, a demonstration. Built as drafts, never activated. Rebuilt on
8 September 2026 after the first version was found to have three problems, all recorded in
[the run log](RUN-LOG.md).

## How the list was built

Every UK public body must publish its contract awards on Contracts Finder: the supplier, the
value, the term and the expiry date. That is a **statutory publication duty**, not a leak and
not an inference. A contract about to expire is the only moment its price is negotiable, so
the expiry date is what put each department on the list.

| Department | Software contracts | Annual value | The date that matters |
|---|---|---|---|
| [HM Revenue & Customs](accounts/hmrc/) | 16 | £194,303,302 | AWS call-off, £350,000,000, ends 30 November 2026 |
| [Home Office](accounts/home-office/) | 24 | £176,976,498 | Two registers under two supplier names |
| [UK Health Security Agency](accounts/ukhsa/) | 21 | £31,776,683 | Nine contracts share one expiry |
| [MHCLG](accounts/mhclg/) | 3 | £17,145,869 | Register filed under two different names |

## The three things this run got wrong first

This is the most useful part, and it is why the run log is worth more than the pages.

**A countdown that had been wrong for eighteen days.** The live page said a call-off "ends in
101 days", frozen at the moment it was written. Intervals are now computed when the page
loads. The ad copy was never regenerated, so [the ad sheets](accounts/hmrc/ad/ad.md) still
carry the stale number, shown rather than quietly fixed.

**An offer that dies in governance.** A civil servant cannot engage a third party on a share
of savings through a web form, nor hand a live vendor proposal to an unappointed party. The
page was rebuilt to lead with the one route that asks for nothing: a document built entirely
from the department's own published award notices.

**A direction that nearly shipped as a lie.** The Home Office pays £150,196,594 a year and
HMRC £116,746,575, to the same supplier, expiring on the same day. That comparison is
devastating for one and flattering to the other. A hook saying "you are overpaying" would
have been false in front of the one reader able to check it.

## On naming people

The committee tables name **seats, not individuals**. Where a gov.uk organogram publishes the
person holding a seat, that name is deliberately not reproduced here. Where it does not, the
seat was left unnamed rather than inferred. The pages say so in their own footers.

## What else is here

- [The handover](handover.html) · how the list was built, every decision, and what is not done
- [The run log](RUN-LOG.md) · the 8 September rebuild, finding by finding

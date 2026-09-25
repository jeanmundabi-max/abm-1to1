# What `audienceCounts` actually returns, and why a 0 is not an answer

Probed live against the LinkedIn Marketing API, version 202601, on 2026-08-20. Every row
below is an observed response, not documentation.

This exists because a 0 was read as "too small" and it cost an account.

---

## The response table

| What you did | HTTP | Body | What it means |
|---|---|---|---|
| Valid URN, real company, above the floor | 200 | `{"elements":[{"active":N,"total":N}]}` | The number. Usable |
| Valid URN, real company, **below the floor** | **200** | `{"elements":[{"active":0,"total":0}]}` | Under LinkedIn's minimum |
| Valid URN, **organisation does not exist** (`urn:li:organization:999999999999`) | **200** | `{"elements":[{"active":0,"total":0}]}` | **Identical response** |
| Valid URN, real company, **no presence in that geography** | **200** | `{"elements":[{"active":0,"total":0}]}` | **Identical response** |
| Valid URN, but a **duplicate or impostor page** | **200** | `{"elements":[{"active":0,"total":0}]}` | **Identical response** |
| **Malformed URN** (`urn:li:organization:notanumber`) | **400** | `TargetingPartialComputationException: Failed to fully deserialize expression` | A bug in your code |

**So there is exactly one thing the API tells you unambiguously: a 400 means your URN is
malformed.** Everything else that goes wrong arrives as `200` with `total: 0`.

**A 0 has four possible causes and the API will not tell you which one you have.**

---

## The typeahead trap, and it is worse than the floor

`adTargetingEntities?q=typeahead` does not reliably return the real company, and taking the
first result is unsafe. Observed, same session:

**Query "Starling Bank" returns two results. Both are dead pages.**

| Result | URN | UK audience |
|---|---|---|
| `Starling Bank-` | `urn:li:organization:117265090` | **0** |
| `STARLING BANK LIMITED.` | `urn:li:organization:117474179` | **0** |

Starling Bank employs thousands of people in the UK. **The real page is not in the results
at all.** Note the trailing hyphen and the trailing full stop: these are duplicate or
scraped pages with no members attached.

**Query "Monzo" returns the real page first, and an impostor second.**

| Result | URN | UK audience |
|---|---|---|
| `Monzo` | `urn:li:organization:9471107` | **8,100** |
| `Monzo-` | `urn:li:organization:117225201` | **0** |
| `Monzone Group`, `MonZon Sverige`, `MONZON & SON ENTERPRISES INC`, `MONZON S.A.S` | various | 0 |

And `typeahead_employer("Monzo Bank")` returns **no match at all**, while `"Monzo"` returns
the right page. **The query string matters more than it should.**

**The consequence:** an operator who searches "Starling Bank", takes the first result and
reads the 0 concludes that Starling is too small for 1:1 ABM. That conclusion is false, and
nothing in the response reveals it.

---

## How to disambiguate a 0

In this order, and none of it is optional:

1. **Did the typeahead return anything at all?** No results is not "too small", it is
   "your query string is wrong". Try the trading name, the legal name, and the LinkedIn
   vanity slug.
2. **Ask for several candidates, never one.** Print them all. Impostor pages announce
   themselves: a trailing hyphen, a trailing full stop, ALL CAPS with `LIMITED.`, or a
   country suffix that is not the company you want.
3. **Confirm the URN against the company's real LinkedIn page**, by vanity slug rather than
   by display name. This is the `match_basis: vanity_matches_slug` check the house config
   already records, and it is the only check that separates the real page from a clone.
4. **Only then**, if the URN is confirmed and the count is still 0, size it without the geo
   filter. If it returns a number globally and 0 in your geography, the company is real and
   simply is not where you are targeting.
5. **If it is still 0 with a confirmed URN and no geo lever, the company is genuinely under
   the floor.** That is the only route to that conclusion.

---

## Where the numbers actually start

UK, no levers, probed the same session. This is what "too small" looks like in practice:

| Company | UK audience |
|---|---|
| Octopus Energy | 7,100 |
| Wise | 6,000 |
| Monzo | 8,100 |
| Gousto | 1,100 |
| Trainline | 930 |
| Tide | 450 |
| **Zego** | **310** |
| GetGround | 0 |
| Cleo AI | 0 |
| About:Energy, Venluto, MDB Growth Capital | 0 |

**The first usable numbers appear a little above 300**, which is consistent with LinkedIn's
documented 300-member floor for an ad set.

### The scoping fact this gives you at intake

**A company with a few hundred employees will return 0 and cannot be run as 1:1 ABM at all.**
GetGround and Cleo AI are real, funded, well-known UK companies, and both are under the
floor for a UK-only ad set.

And clearing 300 is not enough, because the play narrows to a buying committee and the
levers routinely strip 60 to 80%. **In practice 1:1 ABM on LinkedIn needs an account with
roughly 600+ addressable members in the target geography**, which usually means a company of
around a thousand employees or more.

**Say this at intake.** If the client's target accounts are mid-market, this play is the
wrong instrument and the answer is 1:few with an uploaded list, or email. That is a much
better conversation to have in hour one than in week six.

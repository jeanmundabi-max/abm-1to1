# Size the audience and narrow it to the band

## Step 6. Size and narrow

```bash
cd "$HOME/.claude/skills/abm-1to1/scripts"
python3 resolve_and_size.py          # -> account_list_sized.csv
python3 narrow_audience.py --org <ID> --geo-mode light
```

Lever order: light geo → job function (+ exclude junior seniority) → job titles
→ years of experience → final geo. Geo goes first only when geo *is* the
strategy. Rows flagged `first_unverified` matched a same-name entity. Eyeball
them before trusting them.

---

### The seniority trap that the junior exclusion does not catch

`junior_seniorities` excludes {1,2,3}. It does **not** touch **Partner (9)** or
**Owner (10)**. Some companies run a self-employed distributor or franchise network
whose members list the company as their employer on LinkedIn. They are not staff and
they are not the buying committee.

Utility Warehouse's UK base of 5,100 contained **1,000 Partners and 530 Owners.**
Excluding 9 and 10 took the narrowed audience from 1,100 to **860**, into the sweet
spot, and removed about 240 non-buyers.

**Read the seniority mix before accepting a narrowed number.** If Partner or Owner is
material, ask what that company calls its distributors before excluding them, because
at a law firm or an agency Owner *is* the buyer.

### Capture the walk

The printed narrowing walk is a **Step 13 deliverable**, not console noise. Save it.


### What LinkedIn itself says the minimums are

Not the upstream kit's numbers. LinkedIn's own Marketing Solutions help pages, read 2026-08-20.

| What | LinkedIn's words |
|---|---|
| **The hard floor for an ad set** | *"The minimum audience size required for an ad set is **300 member accounts**"* |
| What they recommend | *"we suggest a minimum of **50,000** to drive results"* |
| Sponsored Content and Sponsored Messaging | *"we suggest a minimum of **300,000**"* |
| Text ads | *"we suggest you target between **60,000 and 400,000**"* |
| An uploaded company list | *"Your list must have at least **300 rows** for a successful upload"* and *"Your list must match a minimum of **300 member accounts** to be used in an active ad set"* |

Sources: [Target audience size best practices](https://www.linkedin.com/help/lms/answer/a423690)
and [Requirements for company targeting lists](https://www.linkedin.com/help/lms/answer/a423102).

**300 is a hard gate, not advice.** Below it the ad set cannot serve. Everything above 300
is LinkedIn's opinion about performance, not a rule.

### This play runs at one hundredth of what LinkedIn recommends, on purpose

LinkedIn suggests **50,000**, and **300,000** for Sponsored Content. This skill targets
**300 to 1,000**. That is a deliberate departure, and it is worth being able to defend when
a client's own media agency objects.

**What you give up:** optimisation room. LinkedIn's algorithm has almost nothing to learn
from at this size, so delivery is close to a flat serve rather than an optimised one.

**What you buy it back with:** relevance. Hyper-personalised 1:1 creative runs roughly
**5 to 10% CTR against 0.5 to 1%** for standard creative. **That trade is the entire reason
this play builds a page per account.** Take away the personalisation and you are left with
a tiny, unoptimised, expensive audience and no compensating mechanism.

### Below the floor, LinkedIn stops giving you a number

Campaign Manager's documented behaviour for a list under the minimum:

> *"If your audience size doesn't reach 300 member accounts, you'll see **< 300 members** in
> the Last audience count column on your Audiences page and the list name will be gray. You
> can't use that audience in an ad set until it has been updated and hits the minimum
> number."*

**The API's equivalent is a 0, and a 0 has four possible causes.** Probed live:

| Cause | HTTP | Body |
|---|---|---|
| Real company, under the floor | 200 | `{"active":0,"total":0}` |
| Organisation does not exist | 200 | `{"active":0,"total":0}` |
| Real company, no presence in that geography | 200 | `{"active":0,"total":0}` |
| A duplicate or impostor page | 200 | `{"active":0,"total":0}` |
| **Malformed URN** | **400** | `TargetingPartialComputationException` |

**The only thing the API tells you unambiguously is that a 400 means your URN is malformed.**
A 0 is not a measurement and it is not an answer. **Never conclude "too small" from a 0**
without running the disambiguation in `../knowledge-base/audience-api-behaviour.md`.

**And never take the first typeahead result on trust.** Searching "Starling Bank" returns
two candidates and **both are dead clone pages returning 0**, while the real page is not in
the results at all. Confirm the URN against the company's LinkedIn vanity slug, which is
what `match_basis: vanity_matches_slug` in the config means.
`scripts/narrowing_walk.py` now refuses to auto-pick a candidate that looks like a clone.

### The floor, and the two things it breaks

**Restating the consequence, because it costs accounts.**

**So you cannot isolate a lever by measuring that lever alone.** Every isolated slice of a
mid-sized account falls under the floor and returns 0, which looks like a finding and is
an artefact. **Measure the full stack minus one lever**, and confirm any diagnosis by a
second, independent route. A function-set bug was once diagnosed from an isolated 0; the
diagnosis held only because the function IDs were also resolved against the live API.

**And re-size after any change to the lever config.** A green recorded before a config fix
is not a green. One account was carried as sized and in band for two days after the buyer
functions changed underneath it, and turned out to have no runnable audience at all: 310
before any lever, against a 300 minimum, and 0 after every one of them. It already had a
page, a film and a named committee by then.

**The gate is not "is it above 300". It is "is it above 300 with room to narrow".**

An account can clear LinkedIn's floor and still fail this step. One did: **310 member
accounts** in the UK unnarrowed, which is **10 above the documented minimum**, and 0 after
every lever tried. It passed the letter of the 300 rule and failed the play, because the
play requires narrowing to a buying committee and there was nothing to narrow.

**Treat 300 to roughly 600 before any lever as a fail, not a narrow pass.** The levers
routinely remove 60 to 80% of an account: 2,100 to 500, 3,800 to 850, 3,800 to 470. An
account needs to survive that, not merely to start above the line.

Run it with `scripts/narrowing_walk.py`, which prints the number after each lever, reads
`audienceCounts` live and never writes.

### Guardrail

| Failure, really happened | Fix |
|---|---|
| The upstream kit's junior exclusion applied to none of six ad sets. Gousto was **36.4% entry-level** | Exclude {1,2,3} as standard, and measure the mix **after** the lever, not on the base |
| Excluded juniors at an account already at the 300 floor and read the reported 0 as a real zero | That is LinkedIn's privacy floor. Back the lever off |
| Accepted a `first_unverified` name match. David Lloyd resolved to `davidlloydamsterdam`, Saga to `sagagroupaus` | Eyeball every `first_unverified` row before trusting it |
| 1,530 distributor Partners and Owners counted as addressable staff | Read the seniority mix. Exclude 9 and 10 when the network is not the buyer |
| **`function:14` is Legal, not Operations. Operations is 18.** A config comment said "finance, operations, IT" and shipped `[10,14,13]`. Every account was targeted at lawyers | **Resolve every function URN against the API before trusting a config comment**: `GET /rest/adTargetingEntities?q=urns&urns=List(urn%3Ali%3Afunction%3A{id})`. The Gym Group collapsed to 0 under the lever and that is what exposed it |
| A lever returned 0 and I nearly read it as "this account has nobody in those seats" | **Isolate the levers.** Run function-only and seniority-only separately. It took two calls to prove the function set was the cause, not the seniority exclusion |
| One function set applied to every account | Derive it per account. Operations is the buying committee at a gym operator and the contact centre at a utility reseller. Dropping 18 took Utility Warehouse from 1,400 to 910 |


---

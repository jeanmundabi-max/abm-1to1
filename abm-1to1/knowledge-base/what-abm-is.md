# What ABM actually is, and what this skill is doing

Read this before the first client conversation. It is the difference between running the
play and describing it.

Sourced from Ivan Falco's `curated-abm-skills`, specifically `sops/01-abm-strategy.md` and
`account-targeting/account-selection-framework.md`, with what the GoCardless run added.

## ABM is a reach problem, not a targeting problem

This is the sentence everything else hangs off:

> *"ABM campaigns are not just about targeting your ideal accounts, they're about reaching
> them."*

A perfectly segmented list that only delivers impressions into 15% of its companies has
wasted the other 85%. The work is not choosing the accounts. The work is making sure the
ads actually land inside all of them.

**And LinkedIn will not do that for you.** It prioritises spend on the enterprises in a
mixed list, so the small accounts on the same list get starved. That is why the accounts
are segmented by headcount, industry, geography or deal stage rather than run as one list.

**ABM starts with accounts, not leads.**

## The three tiers, and which one this skill is

| Tier | What it is | Targeting | When |
|---|---|---|---|
| **1:1** | One whale account at a time | The company entered by name, one ad set each | Large enterprises with enough people actually on LinkedIn |
| **1:few** | A named-account programme, 10 to 20 companies | Uploaded as a list, which gives better analytics | The usual middle |
| **1:many** | Vertical ABM, segmented by industry | Company lists or native targeting | Closer to *"scaled prospecting with list-based precision"* |

**This skill is 1:1 only.** One named company per ad set, `employers = {that company}`, one
page built for that account and nothing else. For 1:few or 1:many, use `abm-playbook`.

The reason 1:1 justifies the effort is the gap in performance. Ivan's recorded figures for
hyper-personalised 1:1 creative are roughly **5 to 10% CTR against 0.5 to 1% for standard
creative**, a five to ten times difference. That is what pays for building a page per
account.

## The numbers that constrain the build

| Constraint | Figure | Why |
|---|---|---|
| Audience per account | **>300, ideally 300 to 1,000** | Below 300 LinkedIn will not run it |
| List for a 1:few upload | 300 rows minimum, 1,000+ preferred for cold | Match rates are never 100% |
| Cold 1:many audience | ~15,000 | *"enough room for the algorithm to optimise"* |
| Frequency | **~3 impressions per person per week** | Above that, fatigue |
| Touches before a sales conversation | **7 to 10, across channels** | The ad is one of them, not all of them |
| Entry-level seniority | ≤5% of the audience | They are not on the committee |

## The funnel, and what a 1:1 ad is actually for

The ad is the **top and the middle**, never the whole thing:

    1:1 ad into a named account       awareness and repeated exposure
    the click                         the account is now a known, retargetable audience
    engagement spike                  sales moves within 48 hours
    email, events, direct mail        the other 6 to 9 touches
    the named committee               who the email is actually for
    the conversation                  the conversion event

**Track which companies and individuals engage**, and let a spike trigger the outreach. The
ads are not there to produce a form fill. They are there to make the fifth touch land on
someone who has already seen you four times.

**Say which parts you have built.** A demonstration that shows only the ad and the page is
showing the top of the funnel, and it should say so rather than implying a system.

## Fatigue, and the answer to "how many creatives"

Ivan's strategy SOP **does not mandate a creative count.** It mandates rotation *when
frequency climbs*:

- Rotate the creative to reset relevance without growing the audience, **or**
- Expand the audience inside the account by adding job functions or seniority
- Use LinkedIn's Company Engagement Feature to build **dynamic exclusion lists** by
  engagement threshold. Start at **500 impressions per 7 days**, drop to **300** if fatigue
  persists, raise to **750** if you need reach
- Pausing and restarting resets delivery

So "at least three creatives" is a sound instinct but it is **not** a number from the kit.
The number that is in the kit is the frequency ceiling, and the creative count follows from
it. What the GoCardless run proved separately is that **three formats of one idea is not
three creatives** — five accounts shipped a single ad format because nobody checked.
See `sops/08-the-creative.md`.

## How accounts get chosen

Four layers, and this skill's derived gates are a fifth that sits on top:

1. **Firmographic** — size, revenue, vertical, geography, business model
2. **Technographic** — competitor tools in place, missing capability, a recent stack change
3. **CRM intelligence** — closed-lost, competitor losses, churned customers, past engagement
4. **Lookalike** — the shared attributes of the best current customers

Sizing runs backwards from revenue: target ARR ÷ ACV, then back through stage conversion.
Ivan's worked example is **$1M ARR at $50K ACV needing roughly 3,250 target accounts**.

**What this skill adds is layer 5: gates derived from what the client sells**, so the list
can be built when the client has no CRM to mine and no list to hand over. See
`sops/02-layers-and-account-list.md`.

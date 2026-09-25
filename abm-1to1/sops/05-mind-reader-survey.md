# The Mind-Reader Survey

_Part of the `abm-1to1` skill. The one-screen index is `../SKILL.md`._

## Step 7. Mind-Reader Survey. MANDATORY. Never skip.

**No creative or page copy is written before this step.** Added 2026-08-17 after
writing five creatives from hypothesis and finding four of the five wrong.

**Run the Mind-Reader Survey.** It already exists:
`~/.claude/skills/prospect-research-engine/references/mind-reader-survey.md`, ten
questions, and it is the house VOC framework. Do not invent a lighter version of it,
which is the mistake that produced this note.

It also already contains the things a copy critique will otherwise flag later:

| Question | What it gives you |
|---|---|
| Q1 Bleeding-neck pains | the hook, with a cited quote per pain |
| **Q2 Dream After State** | **the WIIFM outcome.** A hook with no outcome fails Alisha's first test |
| Q3 Failed solutions | why the incumbent is not enough |
| Q7 Revenue Gap | the cost of inaction, conservative or it destroys credibility |
| Q8 Sea of Grey | the words to **avoid**. If a competitor could say it, cut it |
| Q9 Dog Whistle | insider language that buys instant credibility |

Grounding: `px-methodology` in the vault. *"Whoever shows the market they understand
it best wins"*, copy should read *"like a page from their journal"*, and *"most people
start at Execution and fail"*. That was the failure exactly.

### Evidence sources that feed Q1, Q3, Q8 and Q9

Q1 says "extract from competitive review complaints, cite your sources". These are the
routes, with live status as of 2026-08-17:

| Source | Access | Note |
|---|---|---|
| **Apple App Store reviews** | `itunes.apple.com/gb/rss/customerreviews/page={n}/id={appId}/sortby=mostrecent/json`, free, no auth, up to 10 pages | Find the app id via `itunes.apple.com/search?term=&country=gb&entity=software`. The best route by far |
| **Feefo API** | `api.feefo.com/api/20/reviews/all?merchant_identifier={slug}&page_size=50&page={n}`, **open, no key**, 200 as of 2026-08-17 | The route for B2B firms with no consumer app. Invited post-purchase, so it skews POSITIVE. State that bias |
| Trustpilot | **403, Cloudflare** as of 2026-08-17 | Needs a Cloudflare-capable renderer. Costs credits, so `guard()` first |
| Reddit | **403** unauthenticated as of 2026-08-17 | Needs an OAuth app |
| Their own review or complaints pages | varies | |

Then answer the ten questions with the quotes attached, and **write the copy from the
answers.** The survey output, not the raw reviews, is what the creative and page consume.

Rules:
- **A theme counts when you can quote it.** No paraphrase standing in for a quote.
- **State the sample**: how many reviews, what date, what storefront.
- **Say when there is none.** A B2B broker often has no consumer app. Copy for that
  account is then labelled inference, not voice of customer. Never fill the gap.
- Reviews **skew negative** and are partly about the app. That is the complaint
  distribution, not the customer distribution. Say so.
- This is the **payer's** voice, not the buyer's. It is the argument *to* the buyer.
- **Know each source's bias and say it.** App Store skews negative (people review when
  angry). Feefo is invited post-purchase and skews positive. Do not average them into a
  false middle; quote each with its bias named.
- **LOOK at every scraped logo before using it.** A "largest element in the top strip"
  heuristic grabs badges, not marks. It returned a **Feefo review badge** for Simply
  Business and a **yellow "NEW" flash** for Gousto. Both would have shipped as that
  company's logo. Open the PNG, or use the type fallback. A wrong logo is worse than none.
- **If the survey finds no pain in your product's area, that account does not belong in
  the play.** Bupa had 282 one-star reviews and only 3 mentioning a premium: the anger
  was about claiming, not paying. Drop it rather than write copy with nothing under it.
- **But run that test on VOC *and* the financial ladder together, never on VOC alone.**
  **The people who fail to pay do not write app reviews.** That cohort is absent from
  every review platform by construction. On 2026-08-18 The AA showed £36m of receivables
  at 60+ days overdue and a 4.82-star app whose complaints are about auto-renewal.
  Utility Warehouse showed a £41.2m impairment charge and 350 reviews about a prepaid
  cashback card. Quiet reviews do not disprove a collection problem. Drop an account only
  when **both** the ledger and the voice come back empty, as Bupa's did.
- **Check what the reviewers' words actually refer to before treating them as a theme.**
  47% of Utility Warehouse reviews mention payment, and almost all of it is "top up",
  which is the UW Cashback Card, a prepaid card the customer loads voluntarily. That is
  the opposite mechanism to a failed collection. A word-match is not a finding.

Worked example: the voice-of-customer section of any finished run in `examples/`
(2,374 reviews, 404 payment-related, and it overturned four of five hypotheses), then
`MIND-READER-*.md` per account for the survey answers built on top of it.

**The lesson that produced this step, kept in full because it repeats:** the first five
creatives were written from my own hypotheses about each account's payer. Four of five
were wrong, and the one real finding (PureGym members publicly asking for Direct Debit)
was invisible until the reviews were read. Then, having added a voice-of-customer step,
I wrote a thinner one from scratch while the Mind-Reader Survey already sat in
`prospect-research-engine`. **Check the house framework before building a new one.**

---

### Guardrail

| Failure, really happened | Fix |
|---|---|
| Wrote all five creatives from my own hypotheses about the payer. **Four of five were wrong** and the one real finding was invisible until the reviews were read | This step, before any copy |
| Built a thinner voice-of-customer framework from scratch while the Mind-Reader Survey already existed in `prospect-research-engine` | Check the house framework before building a new one |
| Read a 47% payment-word match as a finding. Utility Warehouse's "top up" is a **prepaid cashback card the customer loads voluntarily**, the opposite mechanism to a failed collection | Check what the words refer to. A word-match is not a theme |
| Nearly dropped two accounts because their reviews were quiet | **People who fail to pay do not write app reviews.** Run the drop test on VOC and the Step 8 ladder together, never on VOC alone |


---

# Climb the source ladder before you quote a number

_Part of the `abm-1to1` skill. The one-screen index is `../SKILL.md`._

## Step 8. Climb the source ladder before you quote a number. MANDATORY.

### The principle, which is the part that travels

Four rules. They hold for any company, in any country, whatever the signal is.

1. **One file is an anchor, not an edge.** Never build on the first artefact you find.
2. **Ask who else publishes this same claim, and whether they publish it better.**
3. **Ask what this account's regulator, owner or counterparty COMPELS it to publish.**
   That question, not a guess, is what tells you which ladder you are on.
4. **Write the reporting entity and the as-at date beside every figure.** Two sources that
   disagree are almost always two different entities.

Everything below rule 4 is **one instance** of those four rules.

### Which ladder you are on is decided at intake, not here

> **This file is the UK corporate-disclosure ladder.** It is the right ladder when the buying
> signal lives in what a company tells its investors, its regulator or its lenders. It is the
> **wrong** ladder when the signal lives somewhere else, and it will quietly find nothing rather
> than tell you so.
>
> The other ladders that this play has actually walked:
>
> | Ladder | The right one when | Where its rungs are written |
> |---|---|---|
> | **UK corporate disclosure** | the account is listed, bonded, regulated or foreign-owned | this file |
> | **UK public procurement** | the account is a public body and the signal is a contract | the section at the bottom of this file |
> | **The general access ladder** | you are not sure a source exists at all | `niche-engine/data-access/DATA-ACCESS-STRATEGY.md`, five rungs, never stop before four |
>
> A ladder that has never been walked is not on this list. Write it after the first client that
> needs it, never before.

### The UK corporate-disclosure ladder

For every account, walk all four rungs and record what exists on each. Then quote
from the highest rung available, not the first one you opened.

| Rung | Source | Why it beats the one below |
|---|---|---|
| 1 | **Regulatory news and trading updates** on the company's own IR site | The freshest thing that exists. Gym Group published a pre-close trading update on 8 July 2026, six weeks old, while its filed accounts were eight months old |
| 2 | **Quarterly and half-year investor reports, presentations and transcripts** | Text native, group level, and the transcript is management's own words to investors. PureGym publishes Q1 to Q4 because it issues public debt |
| 3 | **The annual report on the corporate site** | Same accounts as Companies House, but text native, group consolidated, and with the narrative sections the filing strips out |
| 4 | **Companies House filed accounts** | Always exists for a UK company. Scanned images with no text layer, single legal entity, and the staleness of the filing date. The floor, never the ceiling |

### Who has an IR site

Not only listed companies. **Anyone with public debt reports to bondholders**, and
that reporting is usually quarterly. PureGym is private equity owned and still
publishes Q1 results, because Pinnacle Bidco plc has listed bonds. Check for debt
before assuming a private company publishes nothing.

Find the site fast: try `corporate.{domain}`, `investors.{domain}`,
`{brand}plc.com`, then search `"{company} investor relations"` and
`"{company} results presentation pdf"`.

**Never stop at a page called /investors. Hunt the documents themselves.**
Domestic & General's `/investors` page carries complaints data and a supplier code
and no financials at all, which is what made me wrongly write the account off. The
FY26 annual report was one level down at **`/corporate/investors`**, and the PDF is
served from a CMS asset domain (`prod.domesticgeneral.magnolia-platform.io`) that no
URL guess would ever reach. Paths that hide documents: `/corporate/investors`,
`/corporate/financial-information`, `/about-us/results`, `/for-investors`,
`/investor-information/results-reports-presentations`, `/debt-information`.

When guessing fails, **search for the document, not the page**: the entity name plus
"annual report pdf", the bond issuer name (Galaxy Finco, Pinnacle Bidco, AA Bond Co,
RAC Bidco) plus "results", or the year plus "results for the year ended". A missing
IR page is never proof that a bonded company does not report.

### What UK companies actually publish, and what it is called

**Quarterly reporting is not compulsory in the UK.** The FCA abolished mandatory
interim management statements on 7 November 2014 (PS14/15). DTR 4 requires only an
**annual financial report** and a **half-yearly financial report**. Everything
between those two is voluntary, or contractual.

So do not go looking for "Q1 results" by default. Go looking for these names:

| What to search for | Who publishes it | Typical timing |
|---|---|---|
| **FY Results**, Full Year Results, Preliminary Results, Final Results | every listed company | 2 to 3 months after year end |
| **Annual Report and Accounts** | every listed company | with or just after FY results |
| **Interim Results**, Half Year Results, H1, Half-yearly report | every listed company, mandatory | ~2 months after the half year |
| **Trading update**, Trading Statement, **Pre-close** trading update, AGM Statement | voluntary, very common | Q1 and Q3, or just before each close |
| **Investor Report** (Q1, Q2, Q3, Q4) | **bond issuers**, because the indenture requires it | ~7 weeks after each quarter |
| **Results presentation** and **Transcript** | usually alongside FY and H1, and every quarter for bond issuers | same day |
| **Capital Markets Day**, Site Visit, Investor Day | occasional, and very rich | any time |
| **SFCR** | regulated insurers | annual, on their own site |
| **10-K** and **10-Q** | a US parent of a UK target | annual and quarterly, EDGAR |

**The bond issuer is the one people miss.** A private equity owned company with
listed high-yield debt reports **quarterly, with a transcript**, because its
bondholders contractually require it. That is why PureGym publishes Q1 to Q4 with a
management call while The Gym Group, which is listed, publishes only FY and H1 plus
two trading updates. Private does not mean quiet. **Check for bonds.**

Where they live: `/investors/`, `/investors/results-reports-and-presentations`,
`/investors/regulatory-news`, `/rns`, `/investors/financial-calendar`. The financial
calendar page tells you the next publication date, which is how you time a campaign.

### Why the narrative beats the balance sheet

The filed accounts give you a number. The **results announcement, the presentation
and the transcript give you what management says about the condition of the
business right now**, in their own words, in far more text than any filing carries.
That is where a buying signal lives.

Worked proof from this play: The Gym Group's payment failure programme is not in
the numbers anywhere. It sits in one paragraph of the FY25 strategic report and one
line on a capex slide. PureGym's 54,000 non-paying members sit in a footnote to a
Q1 presentation, and the Adyen migration sits only in a spoken transcript. **Three
of the strongest findings in the play came from narrative, none from a balance
sheet.**

So read in this order: transcript first, then presentation, then the results
announcement, then the accounts. Numbers last. The numbers only tell you the size
of what the narrative already told you.

### The reporting screen, and what it does and does not measure

Run this before building anything, because 1:1 ABM is expensive per account and
only pays at high ACV. Cannonball's tiering, in `cannonball-advanced-pvp`: under
$10K ACV use a segment-level PVP, $10K to $50K use contact-level, and **over $50K
is the tier that justifies full custom research per account.** 1:1 ABM lives in
that top tier. It is not for a client worth a few thousand a month.

Three separate gates, and they fail for different reasons. Do not merge them.

**Gate 1, size and ACV.** Is the account big enough that a bespoke page, creative
and ad set pay for themselves? The LinkedIn 300-member floor already forces this,
but check the deal size the client actually sells, not the account's revenue.

**Gate 2, disclosure depth.** How far up the ladder can you get? An account that
publishes quarterly with transcripts gives you narrative to write from. An account
with nothing above rung 4 gives you numbers only, and the copy will be thinner.
That is a known cost, not a blocker.

**Careful: disclosure depth measures listed-or-bonded, not size.** Gousto turns
over £342.9m and publishes no interim results at all, because it is private with no
listed debt. Do not read silence as smallness.

**Gate 3, does the pain exist in your product's area.** This is the one that
actually kills accounts. Bupa was dropped because 282 one-star reviews carried only
3 about a premium. Gousto fails the same test on financials: **zero trade
receivables**, because it charges at the order cut-off and ships only if it clears.
There is no uncollected billing to show it. Different failure from Bupa, same
verdict.

Write the three gates out per account before the build starts. An account that
fails Gate 3 is dropped. An account that fails Gate 2 is built anyway, with the
thinness declared.

### The IR page will not render for WebFetch

Most IR sites are Q4 Inc or Investis and load the document list by JavaScript.
WebFetch returns an empty shell. Drive headless Chrome instead, `domcontentloaded`
plus a wait, never `networkidle` (it times out on these sites). Q4 sites also expose
a machine readable index worth capturing:

```
https://{host}/feed/Event.svc/GetEventList?LanguageId=1&pageSize=-1&tagList=reports
```

PDFs sit on `s28.q4cdn.com/...` and are plain `curl`.

### Private companies with no IR site

Three moves, in this order, before writing anything off as unavailable.

1. **Find the group parent and pull its accounts.** A private group of any size
   files full audited group accounts somewhere. Gousto's FY25 group accounts,
   revenue £342.9m, were filed 24 June 2026 at the holding company.
2. **Check what the regulator compels.** Insurer, SFCR. Bank, Pillar 3. US parent,
   10-K and 10-Q on EDGAR.
3. **Then trade press.** Private results are announced by press release and picked
   up by the trade titles. Cite the article and the release, never the aggregator
   profile pages.

Note what you still do not get: a private company with no listed debt publishes no
interim narrative at all. You will have numbers and no management voice. Declare
that rather than writing thin copy and calling it research.

### Naming the reporting entity, every time

Two sources will disagree, and the reason is almost always that they are different
entities. Say which one.

- Pure Gym Limited, Companies House, 31 Dec 2025: trade debtors £5.1m, loss
  allowance £1.6m, **written off £nil**.
- Pinnacle Bidco plc group, FY25 annual report, same date: trade receivables £9.2m,
  loss allowance £1.8m, **written off £0.9m**.

Same year end, different entity, and the group number is the one that shows real
cash gone. Quoting the subsidiary would have understated it and been indefensible
when checked. **Write the entity name and the as-at date beside every figure.**

### The ladder for the five GoCardless accounts, walked 2026-08-18

| Account | Entity | Best rung reached | Freshest as-at |
|---|---|---|---|
| The Gym Group | The Gym Group plc 08528493 | **Rung 1.** Pre-close trading update, 8 July 2026 | 30 Jun 2026 |
| PureGym | Pure Gym Ltd 06690189 / Pinnacle Bidco plc | **Rung 2.** Q1 2026 report, presentation and transcript, 19 May 2026 | 31 Mar 2026 |
| Zego | Extracover Ltd 10128841 / Zego Insurance Ltd | **Rung 3.** Group SFCR 2025 on zego.com, text native. Companies House has no FY25 until 30 Sept 2026 | 31 Dec 2025 |
| Simply Business | Xbridge Ltd 03967717 | Rung 4 plus Travelers 10-Q. Not broken out in TRV | 31 Dec 2025 |
| Gousto | SCA Investments **Holdings** Ltd 15151622 | Rung 4. FY25 group accounts filed 24 June 2026 | 26 Dec 2025 |

Two of these were called wrong on the first pass and the ladder corrected both.
Gousto was written off as trade press only, and Zego as FY24 only. Full evidence
in `layer2/INVESTOR-EVIDENCE.md`.

### Two traps that hid a whole year of data

**"Audit exemption subsidiary" means the group accounts are somewhere else.**
Gousto's obvious entity, SCA Investments Ltd 08027386, files reduced accounts under
a parent guarantee. The audited group accounts sit at SCA Investments **Holdings**
Ltd 15151622. When a filing looks thin, walk up to the parent before concluding the
company publishes nothing.

**Regulated insurers publish an SFCR.** Any UK or Gibraltar insurer must publish a
Solvency and Financial Condition Report annually, on its own website, text native,
and it lands months before the Companies House filing. Zego's SFCR covered FY25
while Companies House still held FY24. An SFCR also carries a **credit risk**
section that states in the insurer's own words how it collects and what it worries
about. Check for one before ever calling an insurer stale.

The same logic generalises: ask what the account's **regulator** compels it to
publish. Insurers file SFCRs, banks file Pillar 3, listed companies file RNS, bond
issuers report to holders, US parents file 10-K and 10-Q. Search EDGAR full text
when a UK target has a US owner.

### Reading Companies House when rung 4 is all there is

Filed accounts are scanned images with no text layer, and there is no local OCR on
this machine. Route: pull the PDF from the document API, render pages at 140 dpi
with PyMuPDF, and read them with OpenAI vision. Scan in batches of six to locate the
notes, then transcribe the two or three pages that matter at 190 dpi. Roughly fifteen
pages per company and pennies per account. No script for this ships here: it is a short
PyMuPDF loop plus a vision call, and the parameters above are the part that took the time.

### The check that closes this step

Write one line per account: *source used, reporting entity, as-at date, publication
date, and what was on the rung above that you did not use and why.* If that last
clause is blank because you never looked, the step is not done.


### The second ladder, walked on a real client: UK public procurement

The rungs are different, the four rules are identical. WYN's entire account list came from
here, and **not one of the four corporate rungs above was touched.** That is the proof that
this file needed a scope line.

| Rung | Source | Why it beats the one below |
|---|---|---|
| 1 | **Find a Tender** | Carries the above-threshold awards, which is where the largest contracts sit |
| 2 | **Contracts Finder, bulk archive on data.gov.uk** | Daily CSVs back to 2014. **1,625 files in 449 seconds**, no wall, no rate limit |
| 3 | **Contracts Finder OCDS API** | Convenient, and **stops at four months**. Use it to learn the shape, never to build the list |
| 4 | **The buyer's own transparency pages** | Spend over £25k, and the organogram that names the buying committee with phone and email |

**Two traps found in the API within the first two minutes**, both of which would have produced
a confident wrong answer:

- **The `keyword` filter is silently ignored.** "Microsoft", a nonsense string, and no criteria
  at all returned identical rows. Filter client-side, and assume every server-side filter is a
  lie until an invariant proves otherwise.
- **`size: 500` returns 100.** Page with date windows or you will believe you have everything.

And the counting rule that cost the most: **establish what one row is before totalling anything.**
A framework ceiling is not a buyer's spend, a value belongs to the award and never to each
supplier named on it, and republished notices duplicate. Getting those three wrong put the first
total an order of magnitude high.

**The figure this play actually supports is £2,130,992,770 a year**, recomputed from the 557
rows of `accounts_merged.csv` and matching the client handover page, which is generated from the
same file. An earlier version of this paragraph quoted a corrected total of £1.77bn. That number
appears in no file in the run and was carried here from recollection rather than from the data.
**Recompute a total from the artefact before repeating it, including from your own notes.**

---

### Guardrail

| Failure, really happened | Fix |
|---|---|
| Built the whole exhibit off Companies House alone. Missed a **Q1 report published seven weeks after quarter end**, a management transcript, and a group write-off figure the subsidiary filing did not carry | Climb the ladder for every account, every time. Being told once is not enough |
| Stopped at a page called `/investors`. Domestic & General's real annual report was at `/corporate/investors`, served from a CMS asset domain no URL guess reaches | Hunt the document, not the page |
| Quoted a subsidiary's figure when the group's was materially different. £nil written off at the entity, **£0.9m at the group** | Write the reporting entity and the as-at date beside every figure |
| Called two accounts unavailable on the same run, right after being corrected once | Audit-exemption subsidiary means the parent has the group accounts. Regulated insurers publish an SFCR |


---

# Verify the signal today, then name the buying committee

## Step 4. Verify the signal, today

**The corpus `posted_date` is when the scraper saw it on LinkedIn, not the true
ATS date.** Roles that look 5 days old are routinely 30 days old on the
company's own board. Never trust the corpus date. Always re-fetch.

The gate itself is not in this repo, because it is three lines: fetch the canonical URL
today, assert the load-bearing claim is still on the page, and record the date you looked.
Do it however you like. What matters is that it happens per claim, not per company.

Pass the **canonical public ATS URL** (`job-boards.greenhouse.io/...`), not the
API URL. The API form makes the gate report a false `empty-ats` FAIL.

LinkedIn job URLs are unverifiable by design. Find the native ATS first:

| ATS | Endpoint |
|---|---|
| Greenhouse | `boards-api.greenhouse.io/v1/boards/{token}/jobs` |
| Ashby | `api.ashbyhq.com/posting-api/job-board/{token}` |
| Lever | `api.lever.co/v0/postings/{token}?mode=json` |
| Workable | `apply.workable.com/api/v1/widget/accounts/{token}?details=true` |
| SmartRecruiters | `api.smartrecruiters.com/v1/companies/{token}/postings` |

GATE FAIL on liveness stops the build. Pick another account. A delisted role
(Verda, 2026-08-14) and a stale-but-listed role (DeepL ABM Lead, 26 days) are
both disqualifying, for different reasons. Say which.

The gate always demands a **second independent source**. Satisfy it before the
claim anchors anything.

---

### Guardrail

| Failure, really happened | Fix |
|---|---|
| Trusted the corpus `posted_date`. Roles that looked 5 days old were 30 days old on the company's own board | Always re-fetch the native ATS |
| Passed the API URL to the gate, which reported a false `empty-ats` FAIL | Pass the canonical public ATS URL |


---

---

## Step 5. The account and the buying committee

One account. Resolve it, then map who actually decides.

- `tools/find_hiring_manager.py` for the committee
- `never-guess-an-email`, no invented addresses, ever
- `map-contacts` for the org shape
- The hiring manager named in the JD is usually the **buyer**, not the hire

---

**Do not guess the committee off LinkedIn titles until you have checked whether the
account publishes one.** A listed company's annual report carries a **risk ownership
table**, and it names which officer owns which risk. The Gym Group's names the Chief
Technology Officer as owner of the IT Dependency risk that its own payments programme
raised, and the Chief Financial Officer as owner of Reliance on Key Suppliers. It also
names the governance the programme runs through: a steering committee reporting to the
Executive Committee and the Board.

**The committee derived that way is evidence. The one guessed from titles is a
hypothesis.** Use the published one to choose the LinkedIn functions, not the reverse.

Where no risk table exists, walk this ladder and stop at the highest rung that answers:

1. **Companies House officers**, free and authoritative. It gives you the statutory board
   with appointment dates, and it dates the seat. `tools/ch_officers.py`. It will not give
   you a CTO, because a CTO is rarely a statutory director.
2. **The company's own leadership page.** Check the individual bio pages, not just the
   index: The Gym Group's index lists two executives and the CTO has his own page.
3. **The company's own press releases.** This is where a change of officer is announced,
   and it is the rung that catches a seat that moved. PureGym's CEO change was here and
   nowhere else.
4. **Regulated accounts publish more.** An SFCR names the key function holders, which
   hands you the Risk seat that a non-regulated account never discloses.
5. **Corroborated public search**, two independent sources minimum. Mark the rung on the
   row. A name that does not corroborate does not go in the list at all.

**Derive the seats from the offer BEFORE looking for names.** Economic buyer, technical
owner, champion, sponsor, and for a regulated account, the blocker. Then fill them.

**The champion is structurally not public.** Titles below the executive team are not in
filings and not on corporate websites. Public data will give you the C-suite on every
account and the champion on none, and the champion is the seat that feels the pain monthly
and builds the business case. That is the seat the enrichment spend exists to buy, and it
is the moment to ask rather than to spend.

**Every row carries its source and its rung, and the seats you could not fill stay in the
list, empty.** An open seat is a finding. A quietly dropped one is a lie about coverage.

### Guardrail

| Failure, really happened | Fix |
|---|---|
| Four of five accounts targeted "everyone non-junior" because the committee was never mapped | Map it. A function label LinkedIn will not confirm is not a committee |
| The committee was mapped off a stale evidence file. The account's CEO had left 65 days earlier and the CFO seat had gone interim | A committee is a dated fact. Re-run Step 4's liveness gate on the officers, not just on the signal. Companies House plus the company's press page is free |
| The C-suite came back on all four accounts and the champion on none | Expected, not a failure. Public data gives you the buyer and never the champion. Budget for the preview and ask before spending |


---

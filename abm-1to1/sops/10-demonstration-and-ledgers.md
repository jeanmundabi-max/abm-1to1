# The demonstration, and the three ledgers

_Part of the `abm-1to1` skill. The one-screen index is `../SKILL.md`._

## Step 13. The demonstration

The point of a demo build is not the campaign. It is the **proof that the whole
campaign was constructed from a terminal.**

### The two screens, and it is their agreement that proves it

**Screen one, the terminal.** The narrowing walk exactly as `narrow_audience.py`
prints it:

```
Base audience (employers + region): 3,800
Entry-level share: 31.6%  (target <=5%)
  base (employers + region)                        ->     3800
  strict geo (primary country)                     ->     3800
  job function + exclude junior seniority          ->      510
RECOMMENDATION: IN BAND (sweet spot) - 510
```

**Screen two, Campaign Manager.** The same ad set, the same number on screen.

The same figure in both places, and **the build never happened in Campaign Manager.**
That is what makes the demonstration unarguable rather than one more screenshot.

### What Campaign Manager is genuinely needed for, and it is only two things

Verified against Ivan's SOP 01. Name both in the walkthrough rather than overclaiming
that the API does everything.

1. The **per-company engagement report** on a company list, under Audiences.
2. **Company Engagement** dynamic exclusion lists, for impression capping.

Everything else in this pipeline is scripted.

### The walkthrough, in order

1. The intake and the derived gates. Why these accounts and not others.
2. The account list, with the OUT and BENCH verdicts and the reason for each.
3. One account's evidence trail, from the artefact to the quoted sentence.
4. The narrowing walk, terminal.
5. The same numbers in Campaign Manager.
6. The page.
7. The ad preview, live on LinkedIn.
8. The DRAFT status, and what activation would cost.

Close on the point: **nothing here was built in Campaign Manager.**

### Guardrail

| Failure, really happened | Fix |
|---|---|
| Reported "the pages are live" after opening a URL | Opening a URL is not evidence. Read the output |
| No walkthrough existed at all for the first build, so the work was invisible | This step |

---

---

## Step 14. Publish and the feedback loop

### Where it lands

Everything in `~/abm-runs/<slug>/abm-1to1/`. Shipped deliverables mirror
to `~/Clients/<slug>/`. Public versions to GitHub, with Ivan credited by name.

Every deliverable carries: _Strategy & GTM research by Jean Mundabi Fala_

### Three ledgers, because there are three kinds of mistake

A lesson from building the skill is not a lesson from running it, and neither is a
lesson from running it for a different client. They have different homes.

| Ledger | Errors from | Lives in |
|---|---|---|
| **CONSTRUCTION** | building this skill | the guardrail block of the step it belongs to |
| **RUN LOG** | executing it for one client | `<slug>/abm-1to1/RUN-LOG.md`, one per engagement |
| **TRANSFER** | changing client | the bottom of this file |

Format is Ivan's in all three: **the failure that really happened, then the fix.**
Never a theoretical risk.

### Transfer ledger

**First two entries, 2026-08-19, from moving between accounts inside one client.** Both
were assumptions the method carried without knowing it.

| Assumption that did not transfer | What actually happens |
|---|---|
| **The buying committee is published in a risk-ownership table** | That is an **equity-listed** disclosure practice. The Gym Group publishes a named Risk Owner per risk. **The AA does not**, because it is bonded rather than equity listed and its governance disclosure is lighter. Fall back to the named executive team plus function targeting, and say the committee is inferred rather than published |
| **A consumer app means a usable payer voice** | Volume is not the variable, **subject** is. The Gym Group: 144 of 500 reviews payment-related, 102 at 1-2 star. The AA: roughly 40 of 500, and the dominant one-star theme is **service delivery**, patrols not arriving, which is not the client's product area at all. An account can pass the financial gate and fail the voice gate. Build it financial-evidence-led and **declare the thin voice layer** rather than stretching quotes to fit |

The original question stands for a genuinely new client: **what broke because the client
changed?** Prime suspects, still untested:

- The four gates are derived. Did output 1d actually produce usable gates for the
  new client, or did they come out generic?
- Does the client have a payer whose voice is findable at all? GoCardless's accounts
  had consumer apps. A pure B2B client may have none.
- Does public evidence of the pain exist in that product's area, or was collection
  unusually well documented?

### The gate that closes the skill

**Can an operator who was not here run this cold and reach the same accounts, with
the same numbers and the same sources?**

If no, it is not publishable. That is the only test that matters for something going
on GitHub. Run it before every publish, not once.

---

---

## Open, carried forward

- The buying committee has never actually been mapped for any account.
- UTMs unset on every ad set. `adTrackingParameters` 500'd across three days.
- No conversions exist on the ad account.
- Hook variants and a second Big Swing, both still owed from Alisha's critique.

---

## The handover carries the ARGUMENT, not just the settings

Added 2026-09-08, on the operator's note that a client should never have to open Campaign
Manager to understand what was decided.

Campaign Manager shows what was set. It cannot show what else was on the table, or why this was
chosen over it, so a client reading it has to either trust the operator or re-litigate every
field. Section 03 of `scripts/build_handover.py` is the record of the argument.

**Two parts, and both are generated from the run rather than written by hand.**

**The narrowing funnel**, one per account, from `05-campaign/narrowing-walk.csv`: everyone at the
company, then the junior seniorities removed, then the buying functions only, with the 300 floor
marked. This is the answer to "why these departments", "why did you exclude those people" and
"why 300", drawn rather than argued. Where the walk holds a clone row and its final column is 0,
the number that actually built the ad set comes from `account_map.json` and the page says so
instead of hiding the gap.

**The ledger**, one row per decision, with five columns: the decision, what is set, **what else
was genuinely on the table**, why this one, and **whose call it is now**. The last two columns
are what makes it a handover rather than a settings dump. A row whose alternative is a strawman
teaches the client a false constraint, so if nothing was really considered, do not write the row.

Rows it must cover, because these are the ones clients ask about: one ad set per company against
a list upload, the objective and why not website visits, the excluded seniorities, the job
functions, the geography, the interface locale (a platform constraint, not a targeting choice),
the budget as a placeholder, why the image is a built card rather than a photograph, and that
nothing is live.

**Never print a facet URN on a client page.** `urn:li:function:10` tells them nothing and reads
as internal plumbing leaking out. `build_handover.py` carries a `FACET` map that renders them as
names, and a name is something a client can disagree with.

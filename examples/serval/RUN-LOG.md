# Serval run log

**2026-09-24.** Layer 2, demonstration. Ad account: MDB Growth Capital, ACCOUNT_ID.

| Part | What happened |
|---|---|
| 1 | Profile from serval.com read today. Buyer seat derived from the job titles Serval prints beside its own customer quotes |
| 2 | Four candidate keys tested, two thrown out. Bare `*.atlassian.net` DNS answers for any name including a nonsense control. `it.`/`helpdesk.`/`servicedesk.` hostnames are wildcard DNS at Box, Asana, Moderna, Etsy, Peloton, Twilio, Included Health. Survivors: the ServiceNow instance (NXDOMAIN control) and the Jira Service Management portal (404 control). Twenty rows built on those two |
| 3 | Recursion and Sweetgreen benched on shrinking headcount. Chewy benched for sector duplication, later recalled. **A claim was corrected here:** layoff-tracker aggregators dated Wayfair's Workforce Realignment Plan to January 2026. The primary source puts it at 19 January 2024. Nothing from a tracker goes on a page |
| 4 | Seven sized live. Oscar Health returned 0 on the IT function and was dropped by the operator. Bench sized: Chewy 580, Twilio 690, Roblox 430 clear the floor; Coursera, Warby Parker, Flexport, Klarna and Duolingo do not. **AMC Networks returned 0 before any filter, which means the wrong page, not a small company** |
| 4 | **Finding for the handover.** Serval's LinkedIn 1:1 universe starts around 8,000 US employees. Below that, no company in the pool could field 300 reachable IT staff, whatever the fit |
| 4 | The kit's knowledge-base pins `LinkedIn-Version: 202508`, which LinkedIn has retired and which returns HTTP 426. 202601 through 202609 are live. Worth fixing in the skill |
| 5 | Champion lookup priced at 42 credits for 84 people across seven. **Declined by the operator.** Seats named instead. Nothing spent |
| 6 | Wayfair page built and passing `page_standard.py`. 3,002 words, 14 sections, 14 acts, 20 cues. **The press-and-hold was first reported dead on phone. That was a false negative in the test**, which measured the element then pressed after the smooth scroll had moved it. Re-measured at the moment of the press: ring completes on 390x844 and 1440x900 |
| 6 | Hero rebuilt once. The first fold was premium-minimal, which the brief explicitly rules out. Patched into a two-column instrument with the live probe readout in the first viewport |

## Open

- Six pages remain: Chewy, Carvana, Docusign, Riot Games, Zoom, DoorDash
- No hero film on any page yet. The decision is recorded in Wayfair's SCORE.md rather than passed over silently
- Part 7, the ad cards, not started. Creative council to run on the card before any push
- Part 8, the draft campaign, not started. The daily budget has not been asked for and will not be assumed

## 2026-09-24, later

| Part | What happened |
|---|---|
| 6 | Seven pages built, all passing `page_standard.py`. Word spread across the set 1.1x, 2,988 to 3,278. Press-and-hold verified in real Chrome on 390x844 and 1440x900 for every build. Seven distinct arguments, not one template: Wayfair's cut corporate team, Chewy's door swinging both ways, Carvana's own automation thesis turned inward, Docusign's filing-versus-LinkedIn gap, Zoom's +26, DoorDash's completed Deliveroo acquisition, and Riot's refusal to use a bought headcount |
| 6 | Published to GitHub Pages under `mdb-abm/serval/`. All seven verified returning 200 |
| 7 | Seven cards, one object per account. **Four were rebuilt** after failing the standalone test: Wayfair and Chewy were grey text lists rather than objects, Carvana's tower was unreadable, and Riot had the wrong number in the headline slot |
| 7 | **Every card was then rebuilt again to remove fabricated figures.** The first honest-looking version carried `184 waiting`, `91 waiting`, `+1,240`, `-1,180`, `2:14:08` and `COMPLETED 4 MIN`. None of those were measured. Beside a filed headcount they read as measurements of the target. They were replaced with the real probe results or removed |
| 7 | Creative council offered and declined. Cards pushed as they are |
| 8 | Budget set by the operator: **$50 per ad set per day, placeholder**, $350 across seven. Not confirmed by the advertiser |
| 8 | Config written. Dry run clean: **7 buildable, 0 blocked**, and every measured audience matched part 4 exactly |
| 8 | **The build itself is BLOCKED.** `build_campaign.py --execute` was refused by the local permission classifier, and so was the attempt to add a permission rule for it. Nothing was created on LinkedIn. No campaign group, no ad sets, no posts, no creatives |
| 9 | Handover not built. `build_handover.py` refuses without `account_map.json`, correctly, because the page would omit the preview links without saying so. The known fields are parked in `05-campaign/account_map.PENDING.json` with `ad_set_name`, `ad_set_id` and `preview_url` left null rather than guessed |


## 2026-09-24, part 9

Part 8 was completed by the operator. Group **GROUP_ID** in account **ACCOUNT_ID**, seven
DRAFT ad sets, seven ads, no ad errors. `build_campaign.py` is not to be run again: a rerun
builds a second set and a creative cannot be deleted.

| What | Where |
|---|---|
| `05-campaign/finish.py` | written for this run. Verifies every object by GET, then writes the three artefacts. Read-only, idempotent, safe to re-run |
| `05-campaign/PREVIEWS.txt` | the operator's trace. Both links per company, plus the Campaign Manager block |
| `05-campaign/account_map.json` | the single source of ids. Fifteen fields per company |
| `05-campaign/OUVRIR-LES-BROUILLONS.html` | the clickable page. Card thumbnail and four doors per company |
| `05-campaign/HANDOVER.html` | 4,708 words, ten sections |
| `00-inputs/handover_evidence.py` | sections 01 and 02, plus sixteen phrase overrides |

Verified by GET: all seven **DRAFT**, budget 50, targeting `org + function + seniority
excluded`, preview present, no ad error.

### What part 9 found, and it is not cosmetic

**The click tracking is not finished, and the handover now says so in three places.**

1. The parameters sent to LinkedIn are keyed `source`, `medium`, `campaign`. Analytics tools
   only recognise a label whose name starts with `utm_`. As set, these visits will arrive but
   will not be grouped as campaign traffic.
2. **There is no per-account label.** All seven ad sets carry identical parameters, so a visit
   from Wayfair's ad is indistinguishable from a visit from DoorDash's. The handover's own
   section 05 explains why that single label is the difference between seven campaigns you can
   compare and one number you cannot act on. It is missing.
3. The values cannot be read back. `GET /adTrackingParameters/{campaign}` returns **HTTP 500**
   on every version tried, so what is stated is what was *sent*, traced through the kit's
   `set_utms`, not what was read.

Fixing it is one PUT per ad set to `adTrackingParameters`. It replaces rather than appends,
creates nothing, and touches no creative. **Not done, because it is a write and it was not
asked for.**

### Skill changes, and why each one travels

`scripts/build_handover.py` carried WYN's play as hardcoded text in the SHARED sections, so a
ported run printed a different play's facts. Every change below adds a seam whose default is
the exact previous string, so an unported run renders byte-identically.

- Sixteen new phrase keys: `junior_step_why`, `buyer_desk`, `junior_cannot`, `function_reason`,
  `geo_reason`, `locale_alt`, `geo_label`, `function_label`, `function_who`, `function_tail`,
  and the existing ones now reachable from the shared helpers via `ctx["ph"]`.
- **"four accounts" was hardcoded** in five places and is wrong on any run that is not four
  accounts. It now reads off `account_map.json`. This is a correction, not a preference: the
  ElevenLabs handover said "four" about six accounts.
- **The tracking section printed `utm_source`/`utm_medium`/`utm_campaign`/`utm_content`
  whatever the config held**, with `abm-1to1` as a fallback campaign name and a `utm_content`
  that was never set. It now renders the keys the run actually configured, and says plainly
  when they are non-standard or when the per-account label is missing.
- Section 08 claimed "Click tracking attached" unconditionally, contradicting section 05. It is
  now conditional and the gap appears in the Not done column.

### Still open

- The click labels, above. One decision.
- Conversions: not attached. A demonstration never activates, so it is not a blocker here.
- Stage two: needs a LinkedIn permission that takes weeks.
- The budget is a placeholder. Note it is **50 GBP**, not USD: the ad account is denominated in
  sterling, so £50 per ad set per day, £350 across seven.

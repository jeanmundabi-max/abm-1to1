---
name: abm-1to1
title: 1:1 ABM. One named account, one ad set, one page.
description: |
  Run a true 1:1 ABM play: onboard the client, research what they sell, derive the
  gates that select their target accounts, verify each signal is live today,
  resolve to LinkedIn org URNs, narrow to the 300-1,000 band, name the buying
  committee, build a page and a hero film per account, render a personalised
  creative, build the campaign in DRAFT at zero spend, and produce the walkthrough
  that demonstrates none of it touched Campaign Manager.
  Triggers, written: "1:1 ABM", "one-to-one ABM", "ABM ads", "named account campaign",
  "abm-1to1".
  Triggers, DICTATED, which is how this is usually started. A colon and a hyphen never
  survive speech, so these matter more than the written ones: "build an ABM campaign
  for [company]", "run the ABM play on [company]", "start a one to one ABM run for
  [company]", "new ABM client [company]", "let's do ABM for [company]", "one company at
  a time ads for [company]", "target [company] with LinkedIn ads".
  Triggers in French, because the operator dictates in French: "lance l'ABM sur
  [entreprise]", "campagne ABM pour [entreprise]", "nouveau client ABM [entreprise]",
  "on fait de l'ABM sur [entreprise]", "cible [entreprise] en un pour un".
  NOT for 1:few or 1:many list-upload campaigns, and NOT for email sequences,
  that is `abm-playbook`. This skill is the paid, single-account motion.
  It never activates a campaign and never spends.
---

# SKILL: 1:1 ABM on LinkedIn, one named account at a time

**Use this when:** you need to run **1:1 ABM ads on LinkedIn** — one ad set per named
company, each audience narrowed to the buyers, each ad pointing at a page built for that
one account and nothing else. The account list is **derived from the client's offer**, not
handed over. Self-contained; start here.

**Read `README.md` for the end-to-end walkthrough**, and
`knowledge-base/what-abm-is.md` before the first client conversation. This file is the
one-screen index.

**Read `RUNBOOK.md` first.** Eight legs, six stop points, each duration measured from a real
run. It tells the human when they are needed, which is the one thing the SOPs never said.

**Then, every session, before anything else:**

    python3 scripts/status.py --run <run>

It says which leg you are on and what it is waiting for. An untouched template does not count
as progress.


**Right after the layer and demo/live answers, before any research, print the path in plain words
and put it in front of the human:**

    python3 scripts/the_path.py --layer 2 --mode demo --client "<Client>" --product "<Product>"

Eight parts, what each produces, where they are needed. It is the opening of the recording as well.

## How to talk to the human, and this is a rule

Plain words, the way a colleague who knows the trade talks. In front of the human: **part one to
part eight**, never leg, gate, rung, lever, EDP, URN, facet, act, cue. Say "the list", "who we
can reach", "who decides", "the page", "the ad", "the budget". One sentence on what is about to
happen before it happens. When a decision is theirs, it is a box with the consequence and a yes
or no, and on yes it runs (`RUNBOOK.md`, "How a stop is asked"). Every creative is shown the
moment it exists: the card, a frame sheet of the film, the page fold. A line saying it passed a
gate is not a view of it. Added 2026-09-11 from the ElevenLabs review; the rest of that review is
`REFINE-SPRINT.md`.

**Start here, every time:**

    python3 scripts/new_run.py ~/abm-runs/<client>/abm-1to1
    export ABM_RUN_DIR=~/abm-runs/<client>/abm-1to1

That creates the run folder and drops every config template into the right place. After
that every script takes `--run` and defaults to `ABM_RUN_DIR`. `scripts/runpaths.py`
defines the folder shape.

## The pipeline

| # | Step | Do it with | Read |
|---|------|-----------|------|
| 0 | Preflight: run folder, token, guard, the rules | `scripts/new_run.py` | `sops/00-preflight-and-rules.md` |
| 1 | Onboard the client. The intake, then the research | — | `sops/01-onboarding.md`, `knowledge-base/what-abm-is.md`, `knowledge-base/linkedin-api-access.md` |
| 2 | Decide the layer, then derive the gates and build the account list | — | `sops/02-layers-and-account-list.md` |
| 3 | Verify each signal is live **today**, then name the buying committee | `scripts/ch_officers.py`, `scripts/preview_champions.py` | `sops/03-verify-and-committee.md`, `knowledge-base/buying-committee-ladder.md` |
| 4 | Resolve to org URNs, size, narrow to 300–1,000 | `scripts/narrowing_walk.py`, `scripts/resolve_and_size.py`, `scripts/narrow_audience.py` | `sops/04-size-and-narrow.md`, `knowledge-base/audience-api-behaviour.md` |
| 5 | Mind-Reader Survey. Mandatory, never skipped | — | `sops/05-mind-reader-survey.md` |
| 6 | Pick the right ladder, then climb it before quoting a single number | — | `sops/06-source-ladder.md` |
| 7 | Build the page, and the hero film in its first viewport | `scripts/build_page.py`, `scripts/build_vsl.py`, `scripts/vsl_render.js`, `scripts/vsl_motion_qa.js`, `scripts/patch_vsl_recut.py`, `scripts/qa_video_fold.py`, `scripts/publish_page.py` | **`sops/07b-the-page-from-the-buyers-seat.md` first**, then `sops/07-the-page-and-hero-film.md`, `knowledge-base/hero-film-format.md` |
| 7a | **Show it.** One picture per account, the fold, five film frames, the card, and it goes to the human before the next account is built. A gate result is not a view | `scripts/contact_sheet.py <build dir> --card <png>`, then SendUserFile | `sops/07b-the-page-from-the-buyers-seat.md`, last section |
| 7b | Decide which tool makes the moving picture and the page. **`scroll-craft` is a fourth tool and it OWNS the page: it will not restyle a generated one** | `npx hyperframes capture`, `scroll-craft` | `knowledge-base/pages-films-and-broll.md` |
| 8 | Write the creative. One idea and one format per ad. **Run the creative council on the CARD before the first push, not on the film alone** | `creative-council` skill, then build the card as HTML and screenshot it: `<run>/03-creative/cards/build.py`, one object per account | **`sops/08b-hooks.md` first**, then `sops/08-the-creative.md`, `knowledge-base/ad-copywriting.md` |
| 9 | Build the campaign to DRAFT, then QA the real ad preview. **Read `knowledge-base/linkedin-api-gotchas.md` first: four traps, each of which cost a build** | `scripts/build_campaign.py` (runs `scripts/ad_account_guard.py` itself) | `sops/09-build-qa-and-preview.md`, `knowledge-base/linkedin-api-gotchas.md` |
| 9a | **Les deux liens, jamais un seul.** L'apercu du fil (construit depuis les URN de l'API) ET Campaign Manager (compte, groupe en parametre, reglages, annonces). Dans `PREVIEWS.txt`, `account_map.json`, la remise, et une page cliquable `OUVRIR-LES-BROUILLONS.html` | `05-campaign/finish.py` | `sops/09-build-qa-and-preview.md`, derniere section |
| 9b | Say what stages two and three are, and hand the client the map. **The handover's sections 01 and 02 are the PLAY's argument: supply `00-inputs/handover_evidence.py` with `sections(ctx)` and `PHRASES`. With no module the WYN text renders unchanged** | `scripts/build_handover.py` | `knowledge-base/funnel-stages-and-orchestration.md` |
| 10 | The demonstration, and the three ledgers | — | `sops/10-demonstration-and-ledgers.md`, `knowledge-base/what-did-not-transfer.md` |

## Setup

Secrets live in `~/.config/abm-1to1/secrets.env` only, never in a repo. Keys needed are listed
in `scripts/.env.example`. The two node scripts need `NODE_PATH` set;
see `scripts/README-node.md`. Copy `config/*.example.*` into the run folder and fill them.

## The gate that decides "finished"

**`scripts/page_standard.py` runs before a page or a card can be called done. It exits 1.**

```
python3 scripts/page_standard.py page <build dir>     # the DIRECTORY, process artefacts count
python3 scripts/page_standard.py ad   <card.png>
```

It cannot tell you whether the work is good. It refuses work that is obviously thin, which is
the failure that actually happens. Floors are measured against the Hays build and set below it,
so the gate marks the bottom of acceptable rather than a copy of one page.

**Why it exists.** On 2026-09-08 a Revolut page and a WYN page were built hours apart by the
same operator. The first ran the play: interview, BRIEF, page grammar, a bespoke film, a
signature move, four rounds of rejection. The second was a one pass generator script. It came
out at 41% of the words, 50% of the sections, 13% of the interactive elements and no film.

The lessons from the first had been consigned into this skill **that same morning**, as prose.
An operator in a hurry does not open prose. **An instruction is not a mechanism.** The quality
of the first page came from a human rejecting the work four times, and that neither scales nor
travels. This gate is the part that travels.

## Rules that never bend

- Create everything **DRAFT**. Zero spend. Activation is separate and explicit.
- **Never delete** via the API without a fresh human "CONFIRM DELETE".
- **Ask before spending a credit.** Every time, including small runs. A name-only Ark
  preview is **not** free. `knowledge-base/spend-and-credits.md`.
- **There is more than one source ladder, and the intake picks it.** The corporate one
  reaches listed, bonded and regulated accounts. The procurement one reaches public bodies.
  A ladder you cannot name means the account is unresearched, not hard.
- **Never fabricate a number.** Every figure traces to a filing, and arithmetic on a filing
  says so on the frame that shows it.
- The account list is **derived from the offer**. A handed-over list is a different play.
- **Verify the signal is live today**, on every account, not just the pilot. A CEO left 65
  days before anyone noticed.
- Target band **>300**, ideal **300–1,000**. Entry-level **≤5%**. **A 0 from `audienceCounts` is never an
  answer**: it means under the floor, or no such org, or a clone page, or nobody in that
  geography, and the four are identical. Re-size after any lever change.
- **Ask about API access at intake, not on build day.** Approval takes weeks to months, and
  Development tier is enough for this play.
- **The objective is a FUNNEL-STAGE choice, and cold means ENGAGEMENT.** Never
  `WEBSITE_VISIT` on an account that has never heard of the client: you pay for a landing-page
  click before there is any intent. Traffic and conversion objectives belong to the WARM stage,
  after the retargeting pool exists. `knowledge-base/linkedin-ads-abm-guide.md`.
- **`locale` is the member's INTERFACE LANGUAGE, not the audience's country, and it must stay `en_US`.** LinkedIn injects this field into `targetingCriteria` server-side as `interfaceLocales` and then validates it: `{"country":"GB"}` returns HTTP 400 `INVALID_INTERFACE_LOCALE_CODE`. The audience's country is already carried by `profileLocations`. Verified live 2026-09-02 after it failed 3 of 3 ad sets. The earlier wording of this line, "set locale to the audience's country", is what caused that.
- **The name IS the report.** Ad set: `[Client] - [Region] - [Stage] - [Awareness] - [Type] -
  {Account}`. Without the stage in the name, cold and warm collide the moment stage 2 exists and
  no report can separate them. Campaign group carries the **shared intent**, not the client's
  initials: grouping by intent rolls more engagements up per group, which is what gets past
  LinkedIn's minimum before it obfuscates the data.
- **Renaming an ad set silently breaks the run.** `account_map.json` and `PREVIEWS.txt` are keyed
  by the ad set NAME, and `build_handover.py` drops the preview link without erroring. Rename all
  three together, then count the `Open the preview` links in the rebuilt page.
- **Conversions are mandatory even on an ENGAGEMENT objective.** If the account has no active
  campaign there is no convention to copy: say so rather than skipping silently.
- **Three tools make moving pictures and they are not interchangeable.** The house VSL pipeline
  carries a motion guard nothing else has, `scroll-craft` builds scroll-driven pages, and
  `hyperframes capture` is the only one that can point at a live URL and return footage.
  `knowledge-base/pages-films-and-broll.md`.
- **Patch the built pages, never regenerate them**, once a design pass has landed.
- **This play is COLD TRAFFIC, and the offer decides everything before the copy does.** A page
  that ends in "speak to sales" is a warm ask, and no copy saves a warm offer. Read
  `knowledge-base/cold-traffic-and-the-offer.md` before the page or the ad is written, and run
  `offer-temperature-check` on the offer. **Layer 1 is binary: if it fails, stop, and do not
  grade the copy.** On a demonstration the operator INFERS the offer and presents it as real,
  disclosing the inference in the footer and the handover, never on the call to action.
- **Something on the page has to receive the yes**, in the first viewport, matching the words on
  the button. A call to action that links to the client's homepage does not do what it says.
- **Open `knowledge-base/ad-copywriting.md` BEFORE writing a single line of ad copy**, and choose one of
  its six headline formulas per ad. Copy written without a formula reads flat, and flat was the
  exact word used. Write the image text FIRST and test it standalone: would this stop the scroll
  with no body copy.
- **Run the creative council on the CARD, before the first push.** Running it on the film idea
  alone is not enough. Its finding on the Revolut run: **the client's colour must stop being
  background paint and become the element that carries the meaning, inside the TARGET's own
  visual world.** A flat brand-coloured rectangle could be an ad for anything.
- **Every creative revision costs a post and a creative that cannot be removed.** The image is a
  create-only field, so it cannot be swapped on an existing post, and a creative whose
  `reviewStatus` is not APPROVED cannot be paused. Get the card right before the first push.

---

> Built on Ivan Falco's 1:1 ABM kit. What this adds, and what broke in the transfer, is in
> `sops/00-preflight-and-rules.md` and `knowledge-base/what-did-not-transfer.md`.
>
> _Strategy & GTM research by Jean Mundabi Fala_

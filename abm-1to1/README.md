# 1:1 ABM, end to end

`SKILL.md` is the one-screen index. This is the walkthrough: what a run actually looks
like, in order, with the commands.

Built on [Ivan Falco's 1:1 ABM kit](https://github.com/ivangfalco/curated-abm-skills),
MIT licensed. **The parts this skill uses are vendored into it**, so it clones and runs
with nothing else on disk. `NOTICE` lists exactly which files came from there and what
was changed.
His kit takes an account list and turns it into a LinkedIn campaign. **This skill starts
one step earlier and finishes two steps later**: it derives the account list from the
client's offer, verifies each signal is live today, names the buying committee, builds a
page and a hero film per account, and ends with a walkthrough that proves none of it
touched Campaign Manager.

## The shape of a run

A run folder is one client engagement. Create it once, and it comes with every config
template already in place:

    python3 scripts/new_run.py ~/abm-runs/<client>/abm-1to1
    export ABM_RUN_DIR=~/abm-runs/<client>/abm-1to1

    <run>/
      RUN-LOG.md          the failure ledger for this engagement
      00-inputs/          the offer, the config, the account list, deploy.json
      01-evidence/        source-ladder output, Mind-Reader surveys, the pilot write-up
      02-committee/       committee.csv and how it was built
      03-creative/        briefs and rendered ads
      04-pages/           content_<account>.py, live/ the built pages, vsl/ the films
      05-campaign/        LinkedIn ids and preview URLs
      _archive/           superseded generations, kept but out of the way

Fill the templates in. Nothing client-specific belongs in this skill folder; if you find
yourself editing a script to add an account, the account belongs in a config file instead.

## Phase 1. Before anything is built

Ask the four blocking questions and refuse to start until they are answered
(`sops/01-onboarding.md`). Three days went on the wrong offer once because they were not
asked. Then decide **which layer you are in**: are you pitching the client, or building
the campaign the client will run? The terms of layer 2 are the client's, never yours.

Derive the four gates from the offer, then screen candidates and record **three verdicts**,
IN, BENCH and OUT, with the evidence that killed each OUT. The rejections are what prove
the screen is real (`sops/02-layers-and-account-list.md`).

## Phase 2. Evidence, and it has to be alive

    python3 scripts/ch_officers.py "Company Name"          # search, free
    python3 scripts/ch_officers.py --number 08528493       # officers with appointment dates

Verify the signal is true **today**, on every account, not just the pilot
(`sops/03-verify-and-committee.md`). Then name the committee. Public sources give the
whole C-suite for nothing; the champion is structurally not public and is the only seat
worth paying for:

    python3 scripts/preview_champions.py                   # prices it and stops
    python3 scripts/preview_champions.py --confirm         # spends

Then climb the source ladder before quoting a single number
(`sops/06-source-ladder.md`). Rung 1 is a trading update, rung 4 is a scanned Companies
House PDF, and the entity you name is part of the claim.

## Phase 3. The page and the film

The page is the client's, in the client's brand, promoting the client's own products, in
the 13-section Mind-Reader structure. The hero film sits **in the first viewport**, 32
seconds, four beats, silent:

    python3 scripts/build_page.py                                  # one page per account
    python3 scripts/build_vsl.py                                   # HTML per account
    node scripts/vsl_motion_qa.js <run>/04-pages/vsl/<slug>-vsl.html   # 0 static frames or fix it
    node scripts/vsl_render.js    <run>/04-pages/vsl/<slug>-vsl.html <slug>
    python3 scripts/patch_vsl_recut.py                             # transcript into the pages
    python3 scripts/qa_video_fold.py                               # above the fold, measured
    python3 scripts/publish_page.py <slug> [<slug> ...]            # live

`vsl_motion_qa.js` is the guard that makes "more movement" a number instead of an
argument. See `knowledge-base/hero-film-format.md` for why it is 32 seconds and not 90.

**Once a design pass has landed on a page, patch it. Never re-run `build_page.py`**, or the
design is gone. The generator prints a guard saying so.

## Phase 4. Creative, campaign, proof

One idea **and** one format per ad, with a Direct-to-Offer control as the benchmark
(`sops/08-the-creative.md`). Build to DRAFT and QA the real rendered preview, not the
payload you sent (`sops/09-build-qa-and-preview.md`).

Then the demonstration: the narrowing walk in the terminal beside Campaign Manager showing
the same number, and the statement that **every account, every ad and every email came
from one list** (`sops/10-demonstration-and-ledgers.md`).

## The three ledgers

Because there are three kinds of mistake and they need different homes.

| Ledger | Where | What goes in it |
|---|---|---|
| **Construction** | the Guardrail block at the end of each SOP | the method was wrong |
| **Execution** | `RUN-LOG.md` in the run folder | the method was right and the run was wrong |
| **Transfer** | `knowledge-base/what-did-not-transfer.md` | the method was right for the last client and wrong for this one |

Nothing theoretical goes in any of them. If it did not cost time or ship wrong, leave it out.

## The gate that closes the skill

**Can an operator who was not here run this cold and reach the same accounts, with the
same numbers and the same sources?**

---

_Strategy & GTM research by Jean Mundabi Fala_

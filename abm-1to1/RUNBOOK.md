# RUNBOOK: what happens when you type `abm-1to1`, and when you are needed

> **On camera, and in every message to the operator, this is called PART 1 to PART 8, never
> "leg".** `scripts/the_path.py` prints the eight parts in plain words after the layer question,
> and `status.py` names them the same way. The word "leg" survives below because this file is
> the engineer's map, not the script. Added 2026-09-23.

_Part of the `abm-1to1` skill. The one-screen index is `SKILL.md`._

This file exists because the expensive part of this play was never the work. It was not knowing,
at the start, **where you would be interrupted and for how long**. Eight legs, six stop points.

**There are no durations in this file, on purpose.** A first attempt put them here, read off the
WYN run's file timestamps. Checking the arithmetic killed the number: of the 1,207 minutes between
the first and last file, **1,106 are gaps of fifteen minutes or more**. A gap is unattributable. It
could be an API call, a human absent, or thinking. File timestamps say when a file was written,
never how long the work took, and there is no clock in this system that measures the difference.

What is honest to say: **the number of times you are needed is six**, and it does not vary with the
client. How long a run takes does vary, mostly with how big the account list is and how hard the
evidence is to reach, and neither is knowable before leg 2.

    python3 scripts/status.py --run <run>

says which leg you are on and what it is waiting for. Run it first, every session. It reads the
folder and invents nothing: an untouched template is compared byte for byte against
`config/*.example.*` and does **not** count as progress.

---

## The eight legs

| # | Leg | You are needed for |
|---|-----|--------------------|
| 1 | Onboard, read what they sell | **Layer 1 or layer 2.** Who is doing the selling, you or them |
| 2 | Derive the gates, build the account list | **The first twenty rows.** Nothing gets built on a list you have not seen |
| 3 | Verify every signal is live today | nothing, unless a signal has died |
| 4 | Resolve, size, narrow to 300 to 1,000 | **The lever**, on any account that lands under 300 |
| 5 | Name the buying committee | **Permission**, and only if it needs a paid lookup |
| 6 | The page and the hero film | nothing, unless you want the creative council |
| 7 | The creative | **The council**, if you want to debate the idea |
| 8 | Campaign to DRAFT, previews, handover | **The daily budget.** Never assumed |

**Three legs always stop: 1, 2 and 8.** The layer, the list, and the money. Those are the three
where being wrong is expensive and unrecoverable.

**Three more stop only under a condition.** Leg 4 asks only if an account lands under 300, leg 5
only if the free routes are exhausted and a paid lookup is needed, and leg 7 only if you want to
debate the creative. Leg 7 is you choosing, not the run stopping.

**Legs 3 and 6 never stop.**

> An earlier version of this file said "six stop points" and a deck was built on it. Counting the
> conditional ones as stops inflates the number: three is the honest count, and it is the more
> useful one, because it says which three.

---

## What each stop point actually asks

**Leg 1, the layer.** Layer 1 is you pitching the client. Layer 2 is the client's own campaign to
their own targets. The terms of one never carry into the other, and getting this wrong wastes the
whole run. Asked first, before any research.

**Leg 2, the first twenty rows.** The list is derived from the offer, never handed over. Twenty
named rows with the reason each is on the list, shown before leg 3 spends time verifying them. If
the list is wrong, this is where it costs twenty minutes instead of three hours.

**Leg 4, the lever.** The targeting lever is chosen **per account**, not once for the campaign.
Finance-only gave 560 people at the Home Office and **0** at MHCLG. A `0` from `audienceCounts` is
never an answer: it means under the floor, or no such org, or a clone page, or nobody in that
geography, and the four are indistinguishable.

**Leg 5, permission.** The free routes come first: for UK public bodies the organogram names the
committee with phone and email. Only when those are exhausted does a paid lookup arise, and a
name-only preview is **not** free. Asked every time, no exceptions.

**Leg 7, the council.** Optional. Produces a written brief that records why the idea won.

**Leg 8, the budget.** Ivan's Phase 0 is explicit: ask, never default. A figure is set so the ad
set is complete, and it stays a **placeholder** until the client confirms it. `status.py` says so
until the config records the confirmation.

---

## How a stop is asked, and how it is not

**A stop is a box, never a command dump.** State what is about to happen in one or two plain
sentences, ask yes or no, and on yes run it. Never paste shell for the human to run in their own
terminal: the stop exists so that they DECIDE, not so that they type. If a permission classifier
blocks the write after the yes, the fix is a permission rule in settings, written by the operator
and said out loud, not a "run these two, in order".

Added 2026-09-11 after the ElevenLabs run, where the DRAFT push was blocked twice and the operator
answered by pasting the commands. Jean: *"you shouldn't ask me to do it... have a box, and ask me
a question about it. If I say yes, you go on with it."*

## The four things that block activation, checked every run

`status.py` prints these at the bottom whether or not you asked.

1. **The daily budget is confirmed by the client.** A placeholder is not a confirmation.
2. **The objective matches the funnel stage.** Cold accounts take `ENGAGEMENT`. `WEBSITE_VISIT`
   pays for a click before there is any intent. See `sops/09-build-qa-and-preview.md`, Step 10b.
3. **Conversions are attached.** Mandatory even on `ENGAGEMENT`. Blocked until the client says what
   counts as a result on their site.
4. **Everything is still DRAFT.** Verified against the API, never against the folder.

Activation is a separate, deliberate, human action. This skill never takes it.

---

## The demonstration, cold, in one command

Everything deterministic happens before the camera starts. `demo_start.py` creates the run,
records whether this is a demonstration or a live engagement, and prints the two questions that
have to be answered out loud.

    python3 scripts/demo_start.py <slug> --url https://... [--live]

Without `--live` the run is marked a demonstration, and that matters: **a demonstration never
activates, never needs conversions and never needs a real budget**, so three of the blockers that
stall a live build simply do not apply. The mode is written to `00-inputs/MODE.json` rather than
remembered.

Then, at any point:

    python3 scripts/status.py --run "$ABM_RUN_DIR"

### What to have on screen, and what to have ready off it

| Beat | What it proves | Runs live? |
|---|---|---|
| `demo_start.py` on a company nobody has seen | it starts from a bare URL | yes |
| The typeahead on a company name | **two dead pages come back and the real one is absent** | yes, and it is the best thirty seconds available |
| `status.py` on a finished run | the system knows where it is | yes |
| An account page and its 32 second film | what gets built per account | needs the pages published |
| The ad preview in a real feed | it is a real ad, not a mockup | needs a live token |

**Two things to check off camera first.** That the landing pages return 200, because GitHub Pages
switches off silently and does not redirect. And, by hovering the button on one ad preview, that
its destination is the current repository.

---

## What this skill still does not do

Stated plainly so nobody discovers it mid-run.

- **Stage two, retargeting, is not built.** It needs a LinkedIn permission that takes weeks, so it
  should be requested at intake rather than on build day.
  See `knowledge-base/funnel-stages-and-orchestration.md`.
- **Conversions have no route** while the token lacks the API and the account has no active
  campaign to copy a convention from.
- **Legs 1 and 5 have no script.** They are judgement, and their quality is not deterministic.
- **The demonstration has never been recorded.** `sops/10-demonstration-and-ledgers.md` describes
  it; nobody has filmed it.

---

> _Strategy & GTM research by Jean Mundabi Fala_

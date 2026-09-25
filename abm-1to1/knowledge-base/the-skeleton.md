# The skeleton: what never changes, and what must

_Part of the `abm-1to1` skill. Enforced by `scripts/page_standard.py`._

Written 2026-09-08, after a WYN page cleared every count in the gate and was still pale beside
the Revolut page the gate was built from. Counting words and sections was optimising the wrong
variable. The operator's note: *the quantity of the page is not the point.*

---

## Why a skeleton at all

Two failure modes, and they pull in opposite directions.

**Without a skeleton**, every account is improvised and the second one is worse than the first,
because the first was improvised by a human rejecting work four times and the second was not.

**With a template**, every account looks the same, and a page whose whole claim is "this was
built for you alone" that looks exactly like the last one has refuted itself before it is read.

So: **an invariant SPINE of things the page must DO, and a mandatory SKIN of axes that must
DIFFER.** Not a layout. A set of obligations and a set of obligations to be different.

---

## The SPINE. Nine things every page does, however it looks

1. **The page is scroll-driven, not a document.** At least four acts with declared spans, cues
   that fire on act progress, and at least one act pinned or scrubbed. The wheel is the
   instrument. **This is the single largest difference between the two builds that started this
   file**: the gold standard had five acts, eighteen cues and seven reads of the progress
   variable. The pale one had none of any, and was otherwise identical on every count.
2. **A bespoke silent film in the first viewport, and it is the ad card in motion.** The click
   resolves the still image into movement. Not a second idea, not a stock loop.
3. **One signature move**, coded in the page off the progress variable, that makes the argument
   physical. A recoloured kit device is not one.
4. **The account's own filed evidence, DRAWN.** Two figures minimum, built from the run's data
   file, never typed by hand and never merely quoted.
5. **The offer engine**: two routes at equal weight with the low-trust one leading, a button
   that says what it does, a conditional guarantee, and a form that receives the yes.
6. **The committee**, a seat each, what each asks first, and a paragraph written to be
   forwarded.
7. **Every objection**, including the ones that hurt. Twelve is the floor because eleven means
   the awkward one was left out.
8. **Computed dates**, and a disclosure in the footer away from the CTA.
9. **The page implements its own SCORE.** If `SCORE.md` declares seven acts and a signature
   move, the page has seven acts and that signature move. A score the page does not implement is
   a fiction, and writing one is worse than writing none.

---

## The SKIN. Six axes that MUST differ from every previous build

Checked as a fingerprint. A new build must differ from **every** existing row on at least four
of six. Not four in total: four against each row individually.

| Axis | What it means | Hays | HMRC |
|---|---|---|---|
| **Grammar** | One of the eight, chosen and justified | Split stage | Ruled ledger |
| **Chrome** | What replaces a nav bar | A vertical divider that IS the argument | A hairline left margin that fills |
| **Hero device** | How the film is held | Column-held scrub, film in one column | Held over a drawn register |
| **Act shape** | Count and where the peak sits | 5 acts, peak at 3 | 7 acts, peak at 4 |
| **Close** | How it resolves | The collapse, divider retires | The convergence, rules become the form rule |
| **Signature move** | The bespoke interaction | Drag the spread, never resolves | The held verdict, never takes a side |

**The world drawn is not on this list because it is not optional.** It always comes from the
account's own business: a placement board for a recruiter, a wall of screens for an electricals
retailer, a tolerance scale for a metrology firm, a published register for a government
department. Never a chart because a chart was convenient.

**The palette is not on this list either.** It is always the client's own, read from what they
publish. Revolut is white on black because their site is. WYN is ink on white because theirs is.
Inheriting the last client's ground is the fastest way to make a system look like a template.

---

## What the gold standard actually did, step by step

Reconstructed from the Hays build so it can be repeated rather than remembered.

| Step | Artefact it leaves | Skipped on the pale build? |
|---|---|---|
| Interview, or a self-authored brief marked as such | `BRIEF.md` with eight answers verbatim | Written, but after the fact |
| Feeling curve BEFORE the acts exist | The curve table in `BRIEF.md` | Written, never used |
| Grammar chosen from eight, seven rejections named | `SCORE.md` | Written, **never implemented** |
| Fingerprint gate against every prior row | The table in `SCORE.md` | Written, never checked in code |
| Council directs the film and the card | `COUNCIL-BRIEF.md`, the pitches summarised | **Skipped entirely on the first attempt** |
| The film built, motion QA on every frame | `hero.mp4`, a QA line | Skipped, then done |
| The page built to the acts in the score | `index.html` with `data-sc-act` | **Skipped** |
| Buyer walkthrough, would I hand over my data | A roast file | Skipped |
| The gate | exit 0 | Now enforced |

---

## The set, not the page. Added 2026-09-08

A page is not the unit. **The campaign is.**

On 3 September a clone script produced three Revolut pages from one thin source. On 7 September
one of the three was rebuilt, 486 words to 3,971 and five sections to sixteen, and the other two
were left. They stayed live at the old depth for five days, next to the good one, on the same
account, under the same claim: *this page was built for you alone.* At the same time all four
live WYN pages were still serving the superseded generator, while the rebuilt one sat unpublished
in a folder.

Neither is visible from inside the work. **The file you have just improved is the file you look
at**, and the gate you have just written you run on the thing you wrote it for.

So the gate has a third mode:

    python3 scripts/page_standard.py set <dir of builds>

It runs every build under one directory and then measures the **spread** between them. The three
Revolut pages that shipped together sit inside 1.1x of each other on word count; the failure this
catches was 8x. Anything past 2x means one member was raised and the others were not.

Two rules follow, and both are cheap:

- **Raising the standard on one member is not finished until every sibling passes.** Rebuild them
  in the same session or write down why one is exempt.
- **Check what is LIVE, not what is in the folder.** A rebuilt local file that was never published
  is the same defect wearing a different coat, and `curl` answers it in one line.

---

## The rule this file exists to state

**A count is not a quality.** The gate can refuse a thin page; it cannot make a good one. What
it CAN do is refuse a page that does not do what its own score says it does, and that is the
check that catches the failure this file records.

_Strategy & GTM research by Jean Mundabi Fala_

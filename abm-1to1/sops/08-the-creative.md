# The creative

## Step 10. The creative

**Build the card as HTML and screenshot it at 1200x1200.** One `build.py` in the run's
`03-creative/cards/`, one function per account, one object per account drawn from that
account's own visual world. It is deterministic, it costs nothing, it re-renders in a
second when a number changes, and it is what the Serval and ElevenLabs sets were built
with. The Serval file is the reference shape.

The account's own name and mark on the card is the entire point. The upstream kit reports 5-10x CTR
from that personalisation, and that figure is his, so attribute it if you repeat it.

**The image-model route is an option, not the default.** It costs money, it cannot be
re-rendered identically, and it puts a number you cannot control inside a picture. When
it earns its place, the technique is in `../knowledge-base/logo-accurate-image-ads.md`.
A skill script that did this for one agency's brand was deleted on 2026-09-24 after
`SKILL.md` had pointed at it as "the renderer" for weeks. It could not run: two dead
reference paths, someone else's five demo companies, and their brand baked into the
prompt. **A script nobody can run is worse than no script, because the index vouches for it.**

### Read these three vault notes before writing a single hook. Not optional.

`px-methodology` · `px-million-dollar-ads` · `alisha-conlin-hurd-leadgen`

They were in the vault the whole time and this step never pointed at them, which is how
five accounts shipped in one format. What they give you:

**Alisha's 5 Ad Types exist for format diversity, not variety for its own sake.**
Human/Relatable · Authority/Proof · Educational/Mechanism · Pattern-Interrupt ·
**Direct-to-Offer**. Pick the Big Swing from what the account's evidence actually IS: a
member quote is Human, a published table is Authority, a fee charged to a named person is
Story. **Direct-to-Offer is the one she says works on every account, so it is the control
that every account gets.** If a bespoke Big Swing cannot beat the generic direct offer,
the bespoke work was decoration.

**What makes a stranger think "this is for me", in order of force:**
1. **Their own words on the creative.** *"Whoever shows the market they understand it best
   wins."* A customer quote is not a claim, it is a mirror.
2. **Social proof with intent.** Proof must answer *"is this for me"*, not be a logo dump.
   One peer in their industry beats a processing volume.
3. **The Oh Sh*t moment in the first line.** Eight seconds. The image already stopped the
   scroll; the caption only has to earn the click.

**Ad to page message match, from `px-million-dollar-ads`.** Is the page headline a clear
extension of the ad hook? Do the first five seconds on the page validate the click? If the
ad says one thing and the page opens with another, the click is wasted however good both
are. Write the match into a table before shipping.

**Iteration versus Big Swing.** Iterate on what is winning, Big-Swing for discovery. Ten
near-identical variants teach nothing. The upstream kit's rule is one *idea* per ad; Alisha's is one
*format* per ad. Both, every time.

### Guardrail

| Failure, really happened | Fix |
|---|---|
| **All five accounts shipped as Educational/Mechanism.** One format, five times, and nobody noticed because each ad obeyed the one-idea rule | Map the 5 ad types across the play before writing. Name the Big Swing per account in the config |
| **Direct-to-Offer was never used**, and it is the format Alisha calls the low-lying fruit that works on every account. The client already published the direct offer and we walked past it | Every account gets a Direct-to-Offer control. It is the benchmark the bespoke work has to beat |
| The caption recited three facts in the analyst's first person | One idea, a turn in the second paragraph, and the advertiser's voice. See `layer2/AD-HOOKS-SYSTEM.md` |

**Three-layer copy, and they are not interchangeable:**

| Layer | Job |
|---|---|
| Creative (image) | The hook. One headline that signals "we built this for you." Carries no mechanics. |
| Commentary (feed text) | The enticement. Explains the hook, promises more exists, gives the reason to click. |
| Landing page | The substance. Real plays, proof, CTA. |

Second person, addressed to their employees. Never third person about them.

### Guardrail

| Failure, really happened | Fix |
|---|---|
| gpt-image-2 baked a C2PA Content Credentials manifest into the PNG. LinkedIn surfaced "Content Credentials - OpenAI Media Service API" beside the ad | Render from HTML via headless Chrome. No manifest, pixel-exact brand, free per account |
| One hook per account, so nothing could win | Alisha's critique, still open. Ship hook variants, one ad into five |

---

---

## Added 2026-09-03, after three rejected rounds on the Revolut run

### The order that was wrong, and the order that is right

The creative council was run on the FILM idea, and then the card was designed alone. Three
rounds of ad creative were rejected before the council was pointed at the card. **Run the
council on the card before the first push.**

### Open the copy library before writing copy

[the upstream ad-copywriting guide](https://github.com/swan-gtm/gtm-skills/blob/main/skills/ivan-falco/ad-copywriting/SKILL.md) is one click away, and it was not opened.
Two of its rules decide whether an ad reads flat:

- **Step 3, choose one of the six headline formulas.** Feeling, Conversation, Contrast, Shame,
  Stat Interrupt, Pain + Outcome. No formula chosen means no copywriting, and the client's
  word for the result was "flat".
- **Step 4, write the image text FIRST**, and test it standalone: *would this sentence stop the
  scroll with no body copy*. A quoted sentence from a filing is a citation, and it fails that
  test.
- **"The headline IS the creative."** The number belongs on the card as the largest element,
  not buried inside a paragraph.

### The council's finding, which is now the house rule for a 1:1 card

**The client's brand colour must stop being background paint and become the element that
carries the meaning, inside the TARGET account's own visual world.** A card that is a flat
brand-coloured rectangle with a number on it could be an ad for anything, and it does not
identify the account.

Worked, on the Revolut run:

| Account | Concept | Why the colour belongs there |
|---|---|---|
| Renishaw | Out of Tolerance | They build the instruments that measure drift. The card is one of their scales, and one tick in the client's blue sits outside the band |
| Currys | Wall of Screens | A wall of dark televisions. The lit ones glow the client's blue and spell the number. Their product becomes the brand colour |
| Hays | Placement Board | Person marks, the image of headcount. Grey is placed, blue is what nobody placed |

Ground stays the client's true brand colour, the accent is reserved for the one meaningful
element, the **target owns the top left** and the client owns the foot.

## Guardrail

| Failure, really happened | Fix |
|---|---|
| Three rounds of ad creative rejected as flat. The creative council had been run on the film and never on the card | Run the council on the CARD, before the first push |
| Ad copy written without opening [the upstream ad-copywriting guide](https://github.com/swan-gtm/gtm-skills/blob/main/skills/ivan-falco/ad-copywriting/SKILL.md), so none of the six headline formulas was chosen | Open it first. One formula per ad, named in the brief |
| The card carried the account's whole quoted sentence in grey. It reads as a citation and fails the standalone scroll test | Write the image text first and test it with no body copy |
| The brand colour was used as a background wash, so the card could have been an ad for anything | The colour carries the meaning, inside the target's visual world |
| Three creatives ended up on every ad set, and none can be removed | The image is a create-only field and an unreviewed creative cannot be paused. Every revision after the first push is permanent clutter |

## Added 2026-09-03: grade the AD on the same axis as the page

Most of this play's traffic is cold, so the ad is an ad **for the offer**, not for the
diagnosis. A card that carries only the account's own filed number is a strong scroll-stopper
and it asks for nothing.

- **The image can stay diagnosis-led.** It has one job, which is to survive two seconds in a
  feed, and a number the reader recognises as their own does that better than an offer does.
- **The body copy carries the offer**: what they send, what comes back, how long, and what it
  costs. Two or three sentences, which is what `atl-btl-messaging` allows a C-level reader.
- **The headline field carries neither.** It does not repeat the image, per
  [the upstream ad-copywriting guide](https://github.com/swan-gtm/gtm-skills/blob/main/skills/ivan-falco/ad-copywriting/SKILL.md), step 6, and it should differ per account.
- **Run `offer-temperature-check` on the ad as written**, not only on the page. An ad whose
  body copy asks for a meeting has quietly reintroduced the warm ask the page removed.

### And the reason to get it right before the first push

The image is a **create-only** field, so it cannot be swapped on an existing post, and a
creative whose `reviewStatus` is not APPROVED **cannot be paused**. Every revision after the
first push is a new post plus a new creative that only a deletion removes. Three rounds of
revision on the Revolut run left **nine creatives on three ad sets**, none of them removable
without a human CONFIRM DELETE. `../knowledge-base/linkedin-api-gotchas.md`.

---

## The body copy must not repeat the card

Added after the hook was judged insufficient and could not
say why. The reason was mechanical, not literary.

The Hays card carried, in grey under its headline: *"Hays call currency a significant Group
sensitivity. One cent on the euro is about £3.9m of net fees."* The body copy of the post read:
*"Your report calls currency a significant Group sensitivity and puts each 1 cent on the euro at
about £3.9 million of net fees."*

**The same sentence, twice, two seconds apart, on one screen.** This is the upstream kit's step 6 and
it is easy to violate because the card and the copy are written in different sittings and never
read side by side.

**The check, and it takes ten seconds.** Render the ad as it appears in the feed, card and copy
together, and read it as one object. If a phrase appears twice, one of them is wasted.

**The split that works.** The image carries the observation, which is the account's own filed
number in the account's own visual world. The body carries the offer, which is the only thing on
the screen that can be said yes to. Neither restates the other.

## One idea per ad, and the route choice is not part of the ad

The same rewrite found a second fault. The live copy carried the diagnosis, the offer, two
delivery routes and the terms, in four sentences. That is a funnel in an ad.

A cold ad has one job, the click. The choice between "send the file" and "twenty minutes on a
screen share" belongs on the page, where both routes carry equal weight and the reader has room
to weigh them. Putting it in the ad also puts the highest trust cost in the offer, the request
for data, in front of a reader who has not clicked anything yet.

If two ideas both deserve paid air, that is two ads, not a longer one. LinkedIn truncates a
sponsored post at roughly 140 characters on mobile, so a longer ad is not more reading, it is
more text behind a "see more" that may never be pressed.

## Grade the ad on the same axis as the page

Cold traffic means the ad is an ad for the OFFER. Run `offer-temperature-check` on the ad copy as
written, not only on the page, and run the Trust OS six gates over it: most ads pitch at gate 5,
"is it worth the hassle", while the reader is stuck at gate 3, "do you get me", or gate 4, "will
this hurt me". See `../knowledge-base/cold-traffic-and-the-offer.md`.

---

## Before you call a card finished

```
python3 ../scripts/page_standard.py ad <card.png>
```

Two artefacts, and both have to name THIS card. A council brief written no earlier than the day
the card was rendered, and a locked copy file. The first version of this gate accepted any file
named `*BRIEF*` in the folder and passed a card that never saw the council, on the strength of a
brief from another session. A gate that passes the wrong thing is worse than no gate.

Check the same card for fit, by eye or by script, on three things: aspect, ink clipped at the
canvas edge, and the contrast of the ink mass furthest from the measured ground. The tool that
did this is not in this repo; the three checks are the part worth keeping.

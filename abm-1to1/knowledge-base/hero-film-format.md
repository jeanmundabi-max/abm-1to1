# Creative Brief — the 1:1 hero film, re-cut

Run 2026-08-20. Creative Council, four directors: Apple, Beats by Dre, McDonald's,
Super Bowl Spectacle. This brief replaces the 90-second first cut, which the client
rejected on pacing: *"les bits de 18 secondes, c'est trop long, il n'y a pas de son,
il faut plus de mouvement."*

This is the format spec for all four accounts. Build it once here on The Gym Group,
then clone.

---

## What the room agreed on, unprompted

All four directors independently landed on the same three calls. That is the strongest
signal in the transcript, so all three are locked.

1. **The runtime is roughly a third of what was built.** Apple said 32s, Beats 34s,
   McDonald's 34s, Super Bowl 32s. Nobody argued for 90.
2. **One continuous line carries the whole film.** Not five devices that each appear
   and leave. One SVG rule that enters in frame one as the underline beneath their own
   quoted sentence and then never stops moving: it becomes the timeline axis, forks
   into the two layers, and falls into the baseline of the money bar. The beats change
   around it. The line *is* the film.
3. **The blue is withheld until the payoff.** Twenty-five seconds of ink and grey, then
   `#1A88FF` is spent on a sliver two pixels wide. Scale does the arguing.

Beats by Dre named the reason the first cut failed, and it is not the runtime:

> The problem was never duration. Each beat arrives, performs, and waits. Waiting is
> the enemy. Kill waiting, not seconds.

## Where the room disagreed, and the call

| Question | Positions | Call |
|---|---|---|
| Beat count | Apple 4, Beats 4, McDonald's 4, Super Bowl 3 | **4** |
| Which beat dies | Super Bowl and Beats cut the timeline. McDonald's cuts the calendar. | **The calendar.** McDonald's is right: the retry mechanism is a product demo and a product demo belongs below the fold, not in a silent hero. The date stays, because the date is the proof we read their filings. |
| Where the argument peaks | all four: the £2.6m sliver | **The sliver**, at true 1% scale, in blue, at 25s |

## The spec, as built

**Runtime 32.0s. 960 frames at 30fps. Four beats, every handover overlapped.**

Each beat runs exactly as long as its own device takes to draw. Nothing is padded to
fill a slot. There is no sound to carry a held frame, so there is no held frame.

| # | Window | On screen | What moves | Handover |
|---|---|---|---|---|
| 1 | 0.0 to 8.6 | A line the account published itself, one phrase boxed. | The sentence wipes on by clip-path. The rule draws underneath it, chasing the wipe. The box lands on the phrase at 4.6s. | From 7.2s the sentence greys and lifts while the rule is already stretching right. |
| 2 | 7.2 to 15.8 | The dated axis, and who owns it. | The rule becomes the axis. Ticks rise off it as its right edge clears them. The box shrinks into the marker sitting on the account's own date. | At 14.4s the axis forks while the dates are still settling. |
| 3 | 14.4 to 24.0 | Two lanes: what is being replaced, and what decides the month. | The one rule splits into two. The upper lane dims to wash from 20.4s while the lower is still holding. The box drops onto the lower rule. | At 23.0s the lower rule starts rising toward the bar. |
| 4 | 23.0 to 32.0 | The money. | The lower rule rises, thickens to 64px, gathers to nothing, then sweeps back out as the bar while a counter ticks. | The blue sweeps right to left back to the left margin the film opened on. |

**Hero moment: 28.4s, the snap.** The first bar takes three patient seconds to grow. The
proportion arrives in four frames. First and only blue in the film, and the progress bar
turns blue with it.

**The through-line, as built.** Two elements carry the whole 32 seconds and are moving in
every frame:
- `#ruleA` / `#ruleB` — one line until 14.6s, then two. It is the underline, the axis, the
  fork, and finally the bar itself.
- `#box` — four jobs. It boxes the phrase they published, shrinks into the marker on their
  own date, drops onto the collection lane, then becomes the proportion and hands over to
  the blue sliver at the snap.

**Verified, not asserted.** `vsl-motion-qa.js` steps all 960 frames, signs
the position, size, opacity and text of every element on the stage, and compares
consecutive frames. All four accounts: **0 frames identical to the one before, longest
static run 1 frame.** That is the fix for what was rejected, stated as a measurement.

**The $1M detail, taken from McDonald's:** under the second bar, in 21px muted, the
arithmetic is spelled out and labelled as arithmetic rather than as a claim about the
account's own rate. A CFO who catches you overclaiming stops watching. A CFO who catches
you refusing to overclaim starts listening.

## The four accounts, same format, own evidence

| Account | The line they published | The dated axis | The fork | The proportion |
|---|---|---|---|---|
| The Gym Group | *improve payment failure rates*, AR 2025 | 13 Mar 2026 to the 2026 completion, interims marked | member management software against a failed collection | £2.6m of £263m, 1% |
| The AA | note 21, sixty days or more overdue, £36m | 31 Jan 2025 to 31 Jan 2026 | £78m of insurance broking against a member's collection | £36m of £187m, 19% |
| PureGym | a member asking for Direct Debit, App Store | FY24 nil, FY25 £0.9m, the 54,000 published May 2026 | what note 22 says against what it leaves out | 54,000 of 2.3m members, 2.4% |
| Zego | checks around instalment collection, SFCR 2025 | 2024 £46.3m to 2025 £77.8m | the control they named against the wallet that ran out | £0.78m of £77.8m, 1% |

## Rules carried into every clone
- Runtime is declared once, as `window.DURATION` in the HTML. The renderer reads it.
- Every figure traces to a filing or to arithmetic on a filing, and arithmetic says so.
- The relative date is computed from a single `TODAY` constant at the top of the file,
  so a re-render is a one-line edit and never silently stale.

_Strategy & GTM research by Jean Mundabi Fala_

---

## Added 2026-09-03: the last beat is the OFFER, and the film is the ad card in motion

**The failure.** Every film on the Revolut run ended on more evidence. Hays' last beat was its
published sensitivity. Meanwhile the page had been rebuilt to ask for one month of statements,
so **the film and the page asked for different things** and nobody noticed until the pages were
audited.

**Beat 4 is the offer.** Not the best figure, not a summary. The thing the page wants.

**And the film is the ad card in motion, not a second idea.** The reader has just clicked a
still. Same ground, same world, same accent carrying the same meaning, so the click resolves
the image into movement. That is the ad-to-page message match `px-million-dollar-ads` requires:
*"Is the page headline a clear extension of the ad hook?"*

**The transition that made it work, and it generalises.** At 24.0s the account's own central
object **re-spaces into 31 marks, one per day of a month of statements, and the accent element
stops being an error and becomes a read head.** Same object, new meaning, no cut. The offer
then lands as the instrument arriving rather than as an ad break. Find that object in the
account's own world and the last beat writes itself.

**A fixed beat template cannot emit this.** `build_vsl.py` has a hardcoded shape of quote,
timeline, A-versus-B and count-up. When the council directs something outside it, write the
film bespoke and keep the harness: `vsl_render.js` and the QA only need `window.DURATION` and
`window.seek(0..1)`.

**And if the film is a canvas, the DOM motion QA cannot see it.** `vsl_motion_qa.js` reads
`.stage` children and `#pg`. Hash the rendered frame instead, which measures what actually
reaches the screen. That test caught a defect the DOM one would have missed: one film had **15
identical frames from 10.70s** because its world was the only one with nothing moving during
beat 2.

---

## Pacing: one beat every four seconds

**Recut 2026-09-07, after Jean watched the 32 second films at four beats.** Eight seconds
a beat reads as held frames. A silent film has no voice to carry a pause, so the reader
finishes the line at about three seconds and then waits five. Four seconds is the shortest
a line of this length can be read in and the longest it should hold.

**Eight beats of four seconds, not four beats of eight, and nothing gets cut to do it.**
Split each existing idea into a setup and a payoff: the number lands alone, then the
attribution arrives under it. That doubles the cut rate at the same duration, which matters
because the film is also the scroll scrubbed hero and its duration is tied to the act span.

Two traps found doing it, both created by the recut itself:

- **A beat that holds only the transition is a dead beat.** Moving the world transition so
  it opens a beat left that beat with no words, exactly where the ask should land. Start
  the offer on the transition and let it build across the last three.
- **Check what the world looks like after the transition.** Both grid worlds lit a single
  sweeping cell once re-columned, so the last third of the film was a near empty frame
  under the offer copy. The read head now leaves the ground lit behind it, which is also
  what the offer claims it does: every conversion read.

And check the config for authored copy that `seek()` never renders. `b4turn` existed for
every account from the first build and was never drawn. The recut had a beat waiting for it.

## Two harness traps that make a working film look broken

| Symptom | Cause |
|---|---|
| **`scripts/vsl_motion_qa.js` fails with "getComputedStyle: parameter 1 is not of type Element"** | It reads `.stage` children and computed styles, which is a DOM proxy for motion. A canvas film has nothing for it to read. Use the run's `motion_qa_canvas.py`, which hashes rendered frames, and is the stronger test anyway |
| **`scroll-craft`'s `encode.sh` exits silently, writes nothing, and returns 0 through a pipe** | It resolves `ffprobe` next to the ffmpeg it picked. `ffmpeg-static` ships ffmpeg and no ffprobe, so with none on PATH the assignment fails under `set -e`. Run ffmpeg directly with the same flags: `-an -vf scale=-2:1080:flags=lanczos,format=yuv420p -c:v libx264 -profile:v high -preset slow -crf 20 -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart`, and crf 24 / g 4 / 720p for the phone variant |

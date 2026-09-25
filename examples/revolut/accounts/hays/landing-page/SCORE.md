# Grammar, gate and score: Hays

## Grammar: Split stage

Chosen because the argument IS two sides. The rate you were given, and the interbank rate on
the same day. The comparison is the product.

**Why the other seven lost.**

| Grammar | Why not |
|---|---|
| Filmic one-shot | What all four prior builds used. Choosing it again needs a reason and there is none here |
| Chaptered editorial | Treats the argument as an article. This is a confrontation between two numbers |
| Live surface | Bans all marketing chrome and requires a real running product. We have a film and a filing, not a dashboard, and the honesty rule forbids painting one |
| Continuous world | The most expensive and most fragile grammar, and it exists to hide cuts between scenes. We have no cuts to hide |
| Typographic poster | Would throw away the film, which is the reader's own ad continuing |
| Gallery / catalog | Nothing to catalogue. One account, one argument |
| Rhythmic cutlist | Refuses the dwell that the proof film needs |

**What the grammar forbids, and we obey:** no full-bleed before the resolve, no centred copy,
no corner-anchored hero, no symmetric close. Both columns carry real content the whole way.
Bans `pan`, `spotlight`, `magnet`, more than one `scrub`, and `drift`.

## Signature move: the spread you cannot read

The divider is the spread. It is draggable, the reader can pull it to try to measure the gap
between the two rates, and a readout follows the cursor. **It never resolves to a number**,
because that number is exactly what the report produces. The page shows the space where their
figure goes and refuses to fill it in.

Coded in the page off `--sc-p` and a pointer handler. The engine is not touched.

## Fingerprint

| Dimension | This build |
|---|---|
| Grammar | Split stage |
| Nav treatment | No bar. The divider is the chrome and carries both labels and the progress |
| Hero device | `scrub` on the account's own ad card in motion, held in the left column, never full bleed |
| Act-sequence shape | 5 acts, quiet-loud-QUIET-loud, peak at act 3 |
| Close pattern | The collapse. Divider travels to one edge, the form takes the full width |
| Signature move | A draggable spread that never resolves to a number |

**Gate result: the registry is empty, so this build clears trivially.**

**One row is registered for the campaign, not three.** The three pages share a grammar and a
signature move by design, because they are one campaign for one client. The gate exists to stop
a studio repeating itself across clients, and registering three near-identical rows would make
the registry lie about how much variety exists. Hays, Currys and Hays differ in world,
content and act copy, not in grammar.

## Score

Total length 11 viewport-heights, which is inside 8 to 14 and outside the 6-to-7 acts at
13.6 to 13.8vh band that all four prior builds hit.

| # | Beat | Feeling | Device | Why this one | Span |
|---|---|---|---|---|---|
| 1 | Recognition | that is my ad, moving | `scrub` | The reader just clicked this exact still. The wheel scrubbing it is the strongest possible continuation | 2.5vh |
| 2 | Exposure | uneasy | `pin` + `kinetic` | The frame holds while their own filed sentence assembles. Authored silence | 1.5vh |
| 3 | **The gap** | **frustrated, then curious** | `reveal` + pointer | **A wipe is a change of state, and the state change is the two rates parting.** The pointer device is the signature move | **3.5vh** |
| 4 | Substance | relieved | `flow` + `in` | An ordinary section done well. The proof film is Revolut's, not ours, and it should not compete | 2vh |
| 5 | Commitment | decided | `pin` + the collapse | The page stops moving and starts responding | 1.5vh |

**Checks.** Five device families, none twice in a row, exactly one `scrub`, no two adjacent
acts share a feeling, act 3 has the largest span by 1vh and act 2 is the quietest thing before
it. The close resolves into a form rather than fading into a footer.

---

## 2026-09-03, v2: the page had no substance, and one house standard broke another

**The verdict that forced this.** Beautiful and empty. Confirmed against three house standards
and it failed all three.

| Standard | What it says | v1 |
|---|---|---|
| `aiden-vsl-framework` | "a VSL that has the emotional film but no offer engine reads as beautiful and empty" | moves 1 to 4 and a thin 8. The whole offer engine, 8 to 12, missing |
| `feedback-landing-longform-boxrich` | about 4,200 words, long-form and box-rich | **486 words** |
| `feedback-cold-page-must-name-the-fix` | show the problem, teach the mechanism, name the fix | diagnosed and stopped. **Not one Revolut product was ever named** |

Plus my own Mind-Reader Survey: **11 of the 14 dog-whistle terms I extracted appeared nowhere on
the page.** I did the language research and then wrote around it.

### What v2 adds

- **The advertiser is named above the fold.** v1 put Revolut in the footer, so the first screen
  was an accusation from nobody.
- **The mechanism is taught.** Why a spread is inside the rate rather than on a statement, so it
  is never approved, never questioned and never reported. Transactional against translational,
  and why constant currency reporting does not touch the cash.
- **The fix is named**: Multi-currency accounts, Exchange at the interbank rate, FX Forwards,
  with Revolut's own published prices and what each one removes.
- **The offer engine**: container, three-step process, a six-line deliverable stack, a
  **conditional guarantee that runs both ways** (under 10 basis points and there is nothing to
  sell), and the labour removed.
- **Seven objections**, the ones a treasurer actually asks before sending a file: who reads it,
  is it deleted, can I do it without sending anything, what if it is small.
- **486 to 1,801 words.**

### The signature move was inverted, and that is the important change

It used to be a divider that refused to give the number. On a cold page that reads as a game:
the buyer drags it, gets nothing, and asks why they are here. **It now gives.** The reader puts
in their own conversion volume and their own assumed spread and the page does the arithmetic.
Their inputs, their number, nothing attributed to the account. That is move 11, path-to-number
math, which the framework calls the single most believable line in a VSL.

### The deviation, declared rather than hidden

**The page is 16 viewport-heights and scroll-craft's cap is 8 to 14.** The two house standards
are in direct conflict: about 4,200 words of conversion copy cannot fit inside 14 viewport
heights of scrollytelling.

**Resolved by splitting the page rather than by picking a side.** Acts 1 to 3 and the close are
scrollytelling and keep the grammar: `pin > flow > reveal > flow > pin`, no family twice in a
row, one peak. **The body between them carries no `data-sc-act` at all**, because forcing
document sections into device acts is what produced `flow > flow > flow` on the first attempt.
The divider retires at the peak, since past there it is a line drawn through paragraphs.

The cap is therefore respected where it applies, to the scrollytelling, and the page is longer
than it because the conversion standard requires it. That is a deliberate deviation, not a miss.

## v3, same day: the headline was still diagnosis

Jean's read: *"ça ressemble encore à du diagnostic pur, rien que le headline."* Correct, and the
house standard already said so.

`feedback-highticket-page-formula`: **"LEAD the hero with a plain hard outcome guarantee in the
proven X outcome in Y days shape. Do NOT get clever with a hook."** The same memory records him
saying, about an earlier page, *"they all lead with a hard guarantee, what we're doing isn't
working, stop reinventing the wheel."*

**"Every conversion had a rate. Nobody placed that one."** is a pun on recruitment placements. It
is clever and it is not an outcome.

| | v2 | v3 |
|---|---|---|
| H1 | Every conversion had a rate. Nobody placed that one. | **Your FX spread, measured, in 14 days. No fee.** |
| Sub | explains what the page does | the method, then the guarantee, in the reader's terms |
| First thing on screen | a diagnosis | an outcome, a timeframe and a risk reversal |

The diagnosis did not disappear, it moved to where it belongs: **second**, as the reason this
particular company is being shown this particular page.

**Also added**, both because the page had neither: a **cost of inaction** section, on the argument
that a spread is not an event but a subscription nobody signed, and it cannot appear in any report
by construction. And the objections went from **7 to 13**, adding the ones a treasurer actually
raises: we already have a treasury policy and a bank panel, will our bank not just tell us, how
long does this take on our side, what if we do nothing with the answer.

**486 words in v1, 1,801 in v2, 2,341 in v3.** The standard is about 4,200 and this is still short
of it, which is stated rather than glossed.

## v4, the depth pass

Four sections added, none of them filler, each one answering a question the buyer's walkthrough
showed the page could not answer.

| Section | Why it exists |
|---|---|
| **Four routes already tried** | Q3 of the Mind-Reader Survey, researched in week one and never used until now. Forward contracts, constant currency reporting, natural hedging, a central treasury function. Each is sensible, most groups run two or three, and **none of them produces the number.** The gap is measurement, not judgement |
| **What the report actually looks like** | Move 10, proof of rigour. The seven columns of the workbook, and why matching to the hour rather than a daily average is the part a treasury function would insist on |
| **What happens after the fourteen days** | Three outcomes and **two of them end the conversation.** Under 10 basis points we write it down and stop. Material and you do nothing, you keep the workbook. Material and you want to act, it is a single currency pair first, not the whole treasury |
| **Fuller proof, honestly labelled** | Lyca Mobile is the only currency story on the page and it says so. Aer Lingus and Wizz Air are evidence of scale, not of FX, and the page says that too. A page that presents every logo as the same kind of evidence is not worth reading |

**486, 1,801, 2,341, now 3,316 words.** Still short of the ~4,200 standard and the structure is now
complete: outcome, diagnosis, mechanism, what was tried, cost of inaction, the arithmetic, the
named fix, proof, the offer engine, the report, what happens after, thirteen objections, the close.

**23.4 viewport-heights.** The scrollytelling acts remain `pin > flow > reveal > flow > pin` with
no family twice in a row. The body is long because the conversion standard requires it, and it
carries no acts, which is the split declared in v2.

## v5, the committee view, the pains, and the defect at the start

**The defect Jean felt on landing was real and it was mine.** The hero film was scrubbed from
scroll position only, so at the top of the page `--sc-p` is 0, `currentTime` stayed at 0, and the
film sat frozen on one frame until you scrolled. Diagnosed by reading the element rather than
guessing: `readyState 4`, duration 32s, `currentTime 0.00` at 0.3s, 1.0s and 2.5s. **It looked
exactly like a loading failure.** The film now plays on landing and hands control to the wheel at
the first scroll, which also teaches the interaction: it moves, then it responds.

### The two pains, named for Hays, and the third one disclaimed

Q1 of the Mind-Reader Survey found three bleeding-neck pains and **the page used one of them
lightly.** Now:

- **Pain 1, the number moves and nobody caused it**, drawn as a swing chart rather than written in
  a box: FY25 at −£23.1m, FY26 at +£14.9m, the £38.0m span marked and labelled as arithmetic on
  their own figures. With the emotional cost the survey recorded and the page never carried:
  *twice a year you present a number you did not earn and cannot defend.*
- **Pain 2, you report the same year twice**, as a two-column ledger: −7% reported against −8%
  like for like, one point apart on £905.5m, and the currency effect broken out by region from
  their own supplementary information.
- **Pain 3 is explicitly NOT theirs.** The hedge-became-the-volatility argument belongs to Currys
  and Renishaw. Saying so on the page proves we read this company rather than pattern-matched it,
  and a treasurer who spotted us claiming it would stop reading, correctly.

### The committee view

The page now says out loud that it has to survive three people, and gives each seat what it asks:
the **Treasurer** wants to know it is measured properly, so the timestamp method is the answer;
the **CFO** wants the risk, so it is one file, fourteen days, and it ends in writing under ten
basis points; the **Controller** wants to know the work, so it is one export and no project. Plus
**a paragraph written to be forwarded**, because on a committee sale the page's job is often to
arm the champion rather than to convert the buyer directly.

### Visual variety, because everything was arriving as another bordered rectangle

Added forms that are not boxes: an **SVG swing chart**, a **two-column ledger** with a rule rather
than a border, **pull-quotes** with an accent rail for the emotional costs, and a **three-column
table** for the committee. The divider also now retires over every full-width document section
rather than only past the peak, because before this it drew a line straight through the chart.
Found by looking; the fix needed geometry rather than hit testing, since `elementFromPoint`
returns the divider's own grip at the centre of the viewport.

**3,316 to 3,838 words.**

# Grammar, gate and score: Renishaw

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
the registry lie about how much variety exists. Renishaw, Currys and Hays differ in world,
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

## Addendum, 2026-09-08: rebuilt from the deep source

The version of this page that existed until today was cloned from the **thin** Renishaw build on
3 September, before the Hays page was rebuilt on 7 September. It cleared none of the page gate:
486 words against a floor of 2,800, five sections against twelve, no objections, no routes, no
committee and no computed date. **The score above was accurate about the grammar and false about
the page**, which is precisely the failure `page_standard.py` was written to catch.

Rebuilt by `build_deep.py`, which splices this account's evidence and world into the Hays
structure at fourteen named regions and asserts on every one of them, so a missed region stops
the build rather than shipping a page that still cites another company.

### What is shared with the other two, deliberately

Grammar, chrome, hero device, act shape, close and signature move. Three pages for one client
are one system, and `FINGERPRINTS.md` carries a single row for all three. A campaign whose three
pages used three grammars would make one client look like three suppliers.

### What is this account's alone

| Axis | This build |
|---|---|
| The world drawn | A calibration scale, because the account sells measurement. Two gauge marks a year apart on one rule, with the distance between them labelled as arithmetic. The second figure puts the £8.0m on its own. |
| The filed evidence | A different sentence from a different document, quoted whole |
| The inversion | Hays did not hedge, and the Hays page says in as many words that the hedging story is not theirs. Renishaw hedge across three currencies and say so, and their own sentence ranks forward contract income above the rate as the cause. So the third paragraph of act 2b says the opposite on this page. |
| The named seat | John Shipsey, Chief Financial Officer, appointed 13 April 2026, from Companies House 01106260 and Renishaw's own RNS on board changes. The Group Treasurer seat is not public and is left unnamed rather than inferred. |

### The figures, and where they come from

`renishaw_scale` and `renishaw_income` in `build_deep.py`. The only subtraction on the page, £466,120,539 minus £450,775,855, is drawn on the scale and labelled as arithmetic on two of Renishaw's own figures from the same statement.

### Acts, as implemented

Unchanged from the table above, and now actually present in the page: five `data-sc-act`
declarations, eighteen cues, six reads of `--sc-p`. The gate agrees: `acts vs SCORE 5, score
declares 5`.

_Strategy & GTM research by Jean Mundabi Fala_

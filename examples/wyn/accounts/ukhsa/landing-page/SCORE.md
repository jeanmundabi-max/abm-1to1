# SCORE — WYN × the UK Health Security Agency

## Page grammar: RULED LEDGER

**Shared with the HMRC build on purpose, and that is the whole of the reason.** Four pages for
one client are one system, not four studios. The Revolut run made the same call and logged one
fingerprint row for three accounts. A campaign whose four pages used four grammars would be
showing off a range nobody asked for and would make the client look like four different
suppliers.

So the fingerprint position of this build is stated plainly rather than inflated:

| Dimension | Hays (Revolut) | This build | Differs from Hays |
|---|---|---|---|
| Grammar | Split stage | Ruled ledger | yes |
| Nav | Vertical divider as chrome | Left hairline margin | yes |
| Hero device | Column-held scrub film | Held film over a drawn register | yes |
| Act shape | 5 acts, peak at 3 | 7 acts, peak at 4 | yes |
| Close | The collapse, divider retires | The convergence | yes |
| Signature | Drag the spread, never resolves | The held verdict, never takes a side | yes |

**6 of 6 against the other client. 0 of 6 against HMRC, by design.** What differs from HMRC is
the layer the skeleton says is not optional: the world drawn, the evidence, and the copy. This
register is not HMRC's register and the finding in it is not HMRC's finding.

- **Nav:** none. A running hairline down the left margin carrying the act's name.
- **Hero:** the film held in the upper band, this account's register drawn beneath it.
- **Close:** the rules converge into one, and the form sits on it.

## Signature move: THE HELD VERDICT

Two rails of identical stroke weight and identical type size carry 9 contracts ending 31 March 2027 at £23,022,463 and 11 contracts on 10 other dates at £8,754,220.
The reader drags a handle along the shared date axis and both rails travel together. **Whatever
the reader does, the page never marks one as better.** No colour on either figure, no arrow
between them, no label. The accent belongs to the date and to nothing else, ever.

Coded in the page off `--sc-p` and a pointer handler. The engine is untouched.

## The acts, as the page implements them

| # | Beat | Device | Feeling | Span | Why this device |
|---|---|---|---|---|---|
| 1 | The register | Held film + drawn SVG | Recognition | 2.4 | The film is the card in motion, so the click resolves the still into travel |
| 2 | The cliff | Kinetic figures on a rule | Unease | 1.8 | Numbers arriving on a line, not in boxes |
| 3 | The hinge | Flow, authored silence | Understanding | 1.2 | One sentence on white. No figure, no accent, nothing asked |
| 4 | Nine against eleven | **Pointer.** The held verdict | The peak | 3.0 | The largest span. An argument they perform rather than read |
| 5 | Two ways in | Two routes, a rule between | Relief | 1.8 | Equal weight, and the low trust one leads |
| 6 | The seats | Table + the forwarded paragraph | Permission | 1.6 | Three seats, three first questions |
| 7 | The published read | Convergence + form | Calm | 1.4 | The rules become the rule above the form |

Device families: scrub, kinetic, flow, pointer, table, form. **Six, floor four.** No family twice
in a row. Total 13.2 viewport heights, inside the 8 to 14 band.

**This table is the contract.** `page_standard.py` reads the row count out of this file and fails
the build if the page implements fewer acts than the score declares. The check exists because an
earlier WYN page declared seven acts and implemented none.

## The film

THE RAIL, 30 seconds, silent, white ground, one beat every four seconds. Same film as HMRC's,
because four films for one client are one campaign. What it carries is this account's own
published figures, read from `contracts_live.csv` by `build_account.py` and never typed by hand.

- The rail draws, ticks land on it, the ticks merge, the figures arrive, the rail splits at 16s.
- **The only accent in thirty seconds** lands at 24s on 31 March 2027 and on nothing else.
- **No countdown.** A rendered film cannot recompute itself, so the film carries dates and the
  page carries the arithmetic.
- Motion QA: 900 frames, longest static run 4 or fewer, floor 6. Pass.

## The card

The film paused at its own drop: the two rails, the accent on the date, the register ticks from
beat 2 underneath. Not a second idea, because the click has to resolve the still into movement.
`still_guard.py`: 4:5, no edge clipping, ink against ground 17.8:1 against a floor of 4.5.

_Strategy & GTM research by Jean Mundabi Fala_

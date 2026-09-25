# The page, and the hero film in its first viewport

_Part of the `abm-1to1` skill. The one-screen index is `../SKILL.md`._

## Step 9. The page

Ivan's kit takes a URL and does not build the page. This is that gap, and the page
is different in each layer. **Decide the layer before writing a word.**

### Layer 1 page. MDB pitching the client.

Shape follows Ivan's worked pattern, *"5 GTM plays, built for {Company}"*, not the
15-section acquisition mockup. It is the substance layer: the real plays, the proof,
one booking CTA. MDB's voice, MDB's credit, MDB's ask.

### Layer 2 page. The client's page, one per account.

This is the one the GoCardless build got structurally right and nearly wrote wrong.

- **Their brand, their product names, their proof, their CTA.** Jean's credit is one
  footer line.
- **It promotes the client's own products**, selected by the signal found at that
  account in Step 8. GoCardless sells Success+ and Pay by Bank; which of the two
  leads depends on whether the account's evidence is failed collection or card fees.
- **A cold page must name the fix, not just the problem.** Cold readers do not know
  the mechanism. Teach it, then name the product, then show attributed proof.
- **A diagnosis is not an offer.** Per `cold-vs-warm-offer-framework`, diagnosing
  someone's gaps is an improvement offer and it requires trusting the diagnosis. The
  diagnosis is the credibility layer that earns the right to make an offer. In a demo
  it does not need one. In a live build the client supplies it.

### Build procedure, both layers

1. `tools/scrape_hero_section.py <url> <outdir>` for the real palette and real logo
2. Put the palette, the vendor's logo and contact URL, and the slug-to-content map into
   `<run>/04-pages/pages.json`, then `python3 scripts/build_page.py --run <run>`.
   **Nothing client-specific belongs in the generator.** If adding an account means editing
   a `.py`, it is in the wrong place
3. Apply the design pass with the copy LOCKED, then diff the visible words to zero
3. `tools/qa_engineer.py --check-landing-page`, 90/100 hard floor. Check 15 rejects
   default Tailwind colours, so the scrape is not optional
4. Privacy scan, then host. Netlify credits are exhausted: use GitHub Pages via
   `GITHUB_TOKEN`, or the `SNEAK_PEEK_API_KEY` path

One action on the page. No nav exit-ramps.

### The hero film

Locked layout rule: **the film sits in the first viewport**, not below the fold. It
autoplays muted, so it has to survive with the sound off.

- **32 seconds, four beats, handovers overlapped by roughly 1.5s.** A beat ends when
  its own device has finished drawing. Nothing is padded to fill a slot.
- **One element carries the whole film** and changes job per beat: the underline of a
  line the account published, then the dated axis, then the fork between the two
  layers, then the bar itself. Devices that appear and leave produce slides, not a film.
- **Withhold the accent colour** until the last bar, then spend it on one proportion
  drawn at true scale.
- **Run `creative-council` before the beat map**, not after. It is what produced this
  format.
- **Prove the motion, do not assert it.** `vsl-motion-qa.js` steps every frame, signs
  the geometry, opacity and text of everything on stage and reports the longest run of
  identical frames. Ship at 0 repeats.
- The page prints the transcript with timecodes. **The film and the page rows are
  written by the same script** or they drift.

Reference build: see `examples/` in this repo for a finished set. The creative reasoning is
in `VSL-CREATIVE-BRIEF.md`, which is the durable artefact.

### Guardrail

| Failure, really happened | Fix |
|---|---|
| Five pages built as diagnoses. Jean's verdict: not saleable. The framework says why: a diagnosis is a warm offer wearing a number | Name the fix and the product, not just the problem |
| A misquoted client stat shipped on all five live pages | Step 1 output 4 |
| Pages built before the accounts were screened. Two later failed gate 4 | Step 3 before Step 9 |
| The layer 2 pages carried the client's brand while the ads posted from MDB's page | Step 2. Demo: say it in the walkthrough. Live: fix the advertiser identity |
| A 90 second hero film shipped with 18 second beats. Each device drew in five seconds and the frame then held for thirteen. With no sound, nothing carries a still picture | 32 seconds, four beats, overlapped. Cut the beat to its own animation, never to a narrated script's pacing |
| The first cut was defended as fine because the timeline looked full | Write the frame diff. "More movement" becomes a number or it gets argued about again |
| A timeline label never appeared in a film that had already been published, because only the opening frames of that beat were ever sampled | Sample the END of a beat, not just where it starts |
| The highlighted phrase was measured once, at parse time, before the webfont loaded, so the box landed around the wrong words | Any text measurement in a page with a webfont is taken every frame, never cached |
| Four pages had been published all week with no tool, no clone and no record of how | If a step ships to a live URL, it is a tool, not a memory. `publish_page.py` |

---

---

## Before you call a page finished

```
python3 ../scripts/page_standard.py page <build dir>
```

Ten counted floors plus two required artefacts, `BRIEF.md` and `SCORE.md`. It passes the Hays
build and fails a page that skipped the process, naming exactly which floor was missed. Do not
tune a floor because a page failed it. Raise the page.

The floors, and what each one is protecting:

| Floor | Protecting |
|---|---|
| 2,800 words | A cold page carries the whole argument. Under that it is a flyer |
| 12 sections | Hero, evidence, mechanism, cost of inaction, offer, proof, sample of the deliverable, what happens after, committee, objections, close |
| 2 drawn figures | The account's own numbers DRAWN. A page that only quotes is a document |
| 6 interactive | One object the reader can move. An argument they perform is one they keep |
| 12 objections | Under twelve, the awkward ones have been left out |
| 2 routes | Two ways in with equal weight, and the low trust one is not an afterthought |
| a form | Something has to receive the yes |
| a committee view | A seat each, plus a paragraph written to be forwarded |
| computed dates | A hardcoded countdown is wrong the next morning |
| a disclosure | In the footer, away from the CTA |

---

## Proof, and the rule about inventing it

**Look at the client's site before you write a proof section, and look properly.** WYN's homepage
carries the heading *What Our Clients Say* with nothing under it, so a first pass concluded they
publish no proof. Their blog, two clicks away, names **four UK institutions** with figures
attached: a Director of Procurement at Brighton with £1.5m over five months, Bath Spa
"fully compliant with governance and procurement rules", a 48% first project at Canterbury Christ
Church, and a named CFO at BIMM. The proof existed. The homepage was the wrong place to stop.

**Never invent a testimonial.** Not even a clearly labelled specimen one, and not even on a
demonstration. A page whose entire argument is that every figure on it can be checked cannot carry
one that cannot, and a reader who finds the fabricated one stops trusting the audited ones beside
it. If the client publishes nothing, the page says so plainly and the section becomes about what
they do publish instead.

**Attribute in the shape the source actually has.** WYN's blog describes what Julian Wood said. It
does not quote him. So the page says "WYN's account is that he walked into the process sceptical",
never a sentence in quotation marks he never wrote. The difference is invisible to a casual reader
and decisive to the one who checks.

**Every proof line carries its own limit.** The 48% has no named contract, so the base cannot be
checked and the page says so. The compliance claim is WYN's, not an audit, and the page says so.
A proof section that only carries the good half of each claim is an advertisement; one that
carries the limit is evidence.

## The rule of respite

**After a dense beat, a beat that asks nothing.** One sentence, no figure, no table, no accent.

A page that is loud the whole way is as flat as one that is quiet the whole way, and more
practically: a reader given four numbers in a row keeps none of them. The quiet act is where the
last dense one lands. On the Hays build it is the act that carries only *"A fee has to be argued
for. A spread does not."* On the HMRC build it is the hinge, one sentence on white with no figure
and no purple in the frame.

Enforced by `scripts/page_standard.py`, which counts acts whose whole content is short prose with
no table, figure, form or video. The floor is one and the gold standard has two.

## The film sizing rule

The film is the first thing on the page and it must not be a stamp. On the ledger grammar it sits
beside the drawn evidence at roughly 1.45 to 0.8 of the band, capped at 46vh so the copy above and
the figure beside it stay in the same screen. A film that fills the fold alone pushes the evidence
below it and the reader never learns what the film was about.

## Total page length

`scroll-craft` asks for 8 to 14 viewport heights. A 1:1 ABM page carries a long-form body under
its acts and will run over: the HMRC build is 17.3. That is a known and accepted departure, and it
is the reason the acts are the spine rather than the whole page. If a build runs past about 18,
cut the body, not the acts.

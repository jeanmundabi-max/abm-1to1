# SCORE: Wayfair

**Grammar.** Instrument, not document. The page opens on a live probe rather than a claim,
and the reader can re-run it with a press and hold. Eight acts, fourteen sections.

**The feeling curve.**
1. Recognition. Two desks, both yours, and you have never seen them named together.
2. Proof it is about you. The nonsense-name control, printed, so the probe is not a trick.
3. Weight. 12,800 filed, 19% of corporate cut, and the gap between the two.
4. Understanding. A ticket system routes and has never resolved. No product yet.
5. Agency. The dial. The only assumption on the page is the reader's own.
6. Respite. One line, no figure.
7. Recognition again, through peers in the same seat, three of them naming ServiceNow.
8. A yes that costs ten lines of typing.

**The signature move.** Press and hold for five seconds, and both service desk probes run
in sequence with the control at the end. Placed at the point of most doubt, which is
whether any of this is really about Wayfair. `pointer-events:auto` is forced on the wrap
and a transparent rect covers the whole SVG, so the press lands anywhere on the ring.

**The client's colour.** Serval's violet #703fdc marks one thing only: the share of the
queue that would stop needing a person. Wayfair's own purple #7b189f is the ground it sits
in. The bar figure is the argument rendered in the two colours.

**The hero film. Not built in this pass, and that is a decision, not an omission.** This
page's first viewport carries a live instrument rather than a film, and the instrument is
the stronger opening for a reader whose first question is whether this is really about
them. The 32 second film is the next pass and it belongs at the top of the probe section,
not above it. Recorded here so the gate is not silently passed.

**Verified, and how.** Driven in real Chrome via Playwright on 390x844 and 1440x900. The
pointer was held for 5.3 seconds and the ring reached stroke-dashoffset 0 on both, with the
final line reading "Two desks. Both yours. Neither one closes a ticket."

The first run of that test reported the move DEAD on phone. It was a false negative in the
test, not a fault in the page: it measured the element's box, then pressed several hundred
milliseconds later, and with `scroll-behavior:smooth` the target was still travelling on
the taller viewport. The fix was to wait for `window.scrollY` to stop changing and
re-measure at the moment of the press. Recorded because the wrong conclusion was one line
away from being written down as fact.

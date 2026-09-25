# Naming a buying committee from public data

The seats come from the offer. The names come from a ladder. Never the other way round.

**A committee derived from a filing is evidence. One guessed from LinkedIn titles is a
hypothesis.** Mark which one you have, on every row.

## Derive the seats first

| Seat | Who it is | Why they are on it |
|---|---|---|
| **Economic buyer** | CFO or Group CFO | Signs the spend. The loss lands on their statement |
| **Technical owner** | CTO or CIO | It runs inside their system, and they own the integration risk |
| **Champion** | The person who runs the process day to day | Feels it monthly. Builds the case. **Structurally not public** |
| **Sponsor** | CEO or COO | Only when it touches the customer, or already has board visibility |
| **Blocker** | Risk or Compliance | Regulated accounts only |

Champion first, economic buyer second, never the gatekeeper.

## Then climb for the names

Where no risk table exists, walk this ladder and stop at the highest rung that answers:

1. **Companies House officers**, free and authoritative. It gives you the statutory board
   with appointment dates, and it dates the seat. `tools/ch_officers.py`. It will not give
   you a CTO, because a CTO is rarely a statutory director.
2. **The company's own leadership page.** Check the individual bio pages, not just the
   index: The Gym Group's index lists two executives and the CTO has his own page.
3. **The company's own press releases.** This is where a change of officer is announced,
   and it is the rung that catches a seat that moved. PureGym's CEO change was here and
   nowhere else.
4. **Regulated accounts publish more.** An SFCR names the key function holders, which
   hands you the Risk seat that a non-regulated account never discloses.
5. **Corroborated public search**, two independent sources minimum. Mark the rung on the
   row. A name that does not corroborate does not go in the list at all.

**Derive the seats from the offer BEFORE looking for names.** Economic buyer, technical
owner, champion, sponsor, and for a regulated account, the blocker. Then fill them.

**The champion is structurally not public.** Titles below the executive team are not in
filings and not on corporate websites. Public data will give you the C-suite on every
account and the champion on none, and the champion is the seat that feels the pain monthly
and builds the business case. That is the seat the enrichment spend exists to buy, and it
is the moment to ask rather than to spend.

**Every row carries its source and its rung, and the seats you could not fill stay in the
list, empty.** An open seat is a finding. A quietly dropped one is a lie about coverage.

## Worked example

GoCardless, four accounts, 2026-08-20. Public sources alone gave **15 named executives
across four accounts with 12 LinkedIn URLs and zero champions**. One costed Ark preview
(8.5 credits, names and titles only) filled every champion seat and took it to **27 seats,
25 named, 22 URLs**. See `scripts/preview_champions.py` and
`knowledge-base/spend-and-credits.md`.

The two best finds were both invisible to filings: two Financial Controllers at the same
account whose two books are the exact split the landing page asks about, and a VP of
Finance for the region that IS the acquired estate the page quotes.

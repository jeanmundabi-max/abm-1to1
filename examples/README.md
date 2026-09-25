# Examples

Finished runs, with every artefact they produced. These exist so you can judge the work rather
than read a claim about it.

| Run | Target companies | What is here |
|---|---|---|
| [serval](serval/) | 7 | Wayfair, Chewy, Carvana, Docusign, Zoom, DoorDash, Riot Games. The most recently built and the most thoroughly checked |
| [elevenlabs](elevenlabs/) | 6 | BT, Monzo, British Gas, Admiral, easyJet, HMRC. Hero films, two ad crops each, and one disclosed invented figure per page |
| [wyn](wyn/) | 4 | HMRC, Home Office, MHCLG, UKHSA. Public sector, every figure from a statutory publication duty |
| [revolut](revolut/) | 3 | Hays, Currys, Renishaw. The pages that refuse to compute the number and hand the reader two sliders instead |

**20 target companies across 4 advertisers.** None of the four advertisers commissioned any of
this, and none of the twenty target companies was ever contacted. Every page says so in its own
footer.

Each run cleared the same checks before it went in: every page carries its disclosure, no figure
is unsourced, no live account identifier appears anywhere, and every page passes the repository's
own quality gate. `verify.sh` at the root re-runs those checks in one command.

## Why you cannot click through to a real LinkedIn ad

Every ad in these runs exists, as a **draft**, in a real LinkedIn ad account. None was ever
activated and nothing was spent.

A LinkedIn ad preview is only visible to someone signed in with access to the advertising
account it lives in. There is no public link, and sharing account access is not an option. So
instead of a link that would lead nowhere, each account has an `ad/ad.md` carrying the card at
full size and everything the ad was configured with: the body copy verbatim, the headline, the
button, the destination, and who it targets.

Account ids, campaign group ids and ad set ids are replaced with placeholders throughout.

## What these are not

They are **demonstrations**. Serval did not commission this, and neither did any of the seven
companies the pages are addressed to. Every page and every card says so in its own footer.

Every figure on every page traces to a filing, a regulatory notice, or a request made to a
public address on the day, and each one names which. Where an offer appears it was inferred
from the vendor's own published customer results, and the footer says that too.

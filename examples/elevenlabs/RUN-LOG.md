# Run log

Rebuild after the dry run of 2026-09-11. The research, the evidence and the committee carried
over unchanged. The pages, the films and the cards were rebuilt to `sops/07b` and `sops/08b`.

Six things went wrong. All six are here.

| # | Date | What really happened | The fix |
|---|---|---|---|
| 1 | 2026-09-23 | **The signature gesture did nothing.** A seven second press at the centre of the ring triggered nothing, on phone and on desktop. The scroll engine hands `pointer-events` back to a block only once that block is half visible, and it writes that inline | `.holdwrap, .holdwrap *{pointer-events:auto!important}`, plus a transparent hit surface over the whole SVG, because a circle with `fill="none"` is only sensitive along its stroke. Verified on all six pages |
| 2 | 2026-09-23 | **The top bar collapsed into unreadable mush on a phone**, and one full screen of empty black at the peak | Below 620px only the name and the one lit tile remain. The ring moved up and shrank to 220px |
| 3 | 2026-09-23 | **The ad copy was still the deleted version's**: "A flat line is a queue", already rejected, and one headline shared across all six accounts | Rewritten per account, each on its own figure, each headline naming its own object. Locked in `03-creative/copy/` |
| 4 | 2026-09-23 | **The demonstration terminal spoke in jargon**: "Levers, from the config", "URN", "0 UNNARROWED", "BELOW BAND, drop a lever" | 27 phrases rewritten in plain words, plus the cold-start screen |
| 5 | 2026-09-23 | **The handover described six drafts with no link to go and look at any of them**, and it was announced as finished without being put in front of anyone | Three Campaign Manager addresses written by `finish.py` into `PREVIEWS.txt` and `account_map.json`, rendered by `build_handover.py` at the top and in every account card. Now a rule in `sops/09` |
| 6 | 2026-09-23 | **The Campaign Manager address for a group was invented**: `/campaign-groups/{id}/campaigns`. Page not found. A user interface path cannot be deduced from an API identifier | The group is a **filter**, not a path segment: `/campaigns?campaignGroupIds=%5B{id}%5D`. Confirmed by clicking it, and recorded as verified and dated in `sops/09` |

Row 1 is the one worth reading twice. The gesture was the whole point of the page, it looked
correct in the markup, and it was dead to a press on every page. Nothing catches that except
pressing it.

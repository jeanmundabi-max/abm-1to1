# Three tools make moving pictures here, and they do different jobs

_Part of the `abm-1to1` skill. The one-screen index is `../SKILL.md`._

Every claim below was run on 2026-09-02, not read off a README.

## Which one, for what

| You want | Use | Why not the others |
|---|---|---|
| The **hero film inside an account's page**, 32 seconds, silent, autoplays in the fold | `scripts/build_vsl.py` then `scripts/vsl_render.js` | It already exists, it is deterministic, and `vsl_motion_qa.js` proves motion in every frame. Nothing else in this list has a motion guard |
| A **scroll-driven account page** where the page itself is the experience | `scroll-craft` (plugin `nateherk-design`) | The current pages are excellent documents. This is for when a page has to feel like a film |
| **B-roll of something that already exists on screen** | `hyperframes capture` | Neither of the others can point at a live URL and come back with usable footage |
| A **deck presented with audience sync** | `hyperframes present` | The house decks are scroll-snap HTML you drive by hand. This adds a presenter mode |

---

## The house film pipeline, which is already yours

`build_vsl.py` writes an HTML file exposing `window.DURATION` and `window.seek(t)`.
`vsl_render.js` steps it frame by frame in headless Chrome and pipes PNGs through ffmpeg.

**This is the same architecture Hyperframes packages.** The difference is that yours carries a
motion guard: `vsl_motion_qa.js` measures every frame and fails the build if anything holds still,
which is the rule that a silent film has no voice to carry a held frame. **Do not replace this
with Hyperframes to save code.** You would trade a tested guarantee for a dependency.

Both need the packages in `scripts/package.json` (`npm install` in `scripts/`) and Chrome from the Playwright
cache. See `scripts/README-node.md`.

---

## scroll-craft, and what it actually needs

Installed as a plugin, `nateherk-design@nateherk`, 3,227 lines across a SKILL and seven reference
files. It builds scroll-driven pages on a design floor: typography, spacing, depth, motion,
accessibility, then verifies itself by screenshotting its own scroll.

**Its own `doctor.mjs` is the gate, and it reports honestly.** Current state on this machine:

```
ok    node v24.13.1
ok    ffmpeg (full build)   486 filters, libwebp present
ok    Chrome
ok    playwright-core
ok    workspace             <your scrollcraft workspace>
warn  KIE_AI_API_KEY        not set
```

**ffmpeg is not on the PATH here.** The full build is the one inside `ffmpeg-static`, and
`SCROLLCRAFT_FFMPEG` in `~/.config/abm-1to1/secrets.env` points at it. That line is **exported**, unlike
every other line in that file, because a bare assignment is a shell variable and a child process
never sees it.

**The missing key only blocks generated imagery.** Its own words: *"Only needed to GENERATE
imagery. Building from your own photos and footage needs no key and no spend."* So it degrades,
which is what the install gate asks for.

**Where it collides with the house.** It picks a palette from an interview. The brand system is
locked and says never to invent a colour for an asset. **Answer the interview with the series
palette rather than letting it choose**: content engine is orange on warm dark, Growth Map is
magenta on light with navy structure.

---

## Hyperframes, and the one command that matters

`npm i hyperframes`, Apache-2.0, version 0.8.26. **It is a CLI, not a library.** The video skill in
`ai-audit/ad-audit-tool` documents `import { render } from "hyperframes"`, and that does not work:
`require('hyperframes')` throws. Use `npx hyperframes <command>`.

Commands: `init`, `add`, `capture`, `catalog`, `preview`, `present`, `publish`, `render`, `lint`,
`check`, `validate`, `beats`, `inspect`.

### `capture` is the one that earns its place

```
cd <your broll workspace>
npx hyperframes capture "<url>" -o <slug> --skip-vision --max-screenshots 8
```

Run against a live account page it returned **21 screenshots, 3 contact sheets, a full-page
render, the extracted sections, the fonts, and a generated `CLAUDE.md`** telling the next agent how
to turn the capture into a video. That is B-roll of a real artefact, which is the only kind worth
putting in a video about work you actually did.

`--skip-vision` skips AI captioning and costs nothing. `--max-screenshots` caps the sweep.

**One observed failure, and it is harmless:** *"animation catalog evaluate timed out; continuing
without animation catalog."* The capture completes.

### What to capture for a video about this skill

The artefacts, not the abstractions. An account page and its film. The ad preview in a real feed.
The terminal at the moment it stops and asks a question. **The typeahead returning two dead pages
for a company that employs thousands** is the best thirty seconds available, and it is a screen
recording rather than a capture.

---

> _Strategy & GTM research by Jean Mundabi Fala_

---

## Added 2026-09-03: scroll-craft is a fourth tool, and it owns the page

`nateherk-design:scroll-craft` builds a scroll-driven page: the wheel is a scrubber, the page
is a film with real text on it. It is the right tool when the generator's 14 uniform sections
read flat, which on the Revolut run they did, three times.

**It will not restyle an existing page, and it says so.** Its own words:

> *"A runtime that builds the page from a config object is exactly why every site built on one
> looks the same."*

That is a direct description of `build_page.py`. Its rule *"at most one eyebrow per three
sections"* is also incompatible with a page that has an eyebrow on all fourteen. **So using it
means leaving the generator behind for that run's pages, not layering it on top.** The
generator stays for the runs that already use it.

**What it needs, and what it does not.** Node, a full ffmpeg, Chrome, and a workspace. It does
**not** need an image-generation key when the build uses footage you already own, which is a
first-class route in the skill rather than a fallback. Two local gotchas: `ffmpeg-static` from
`scripts/node_modules` satisfies the full-build check, but **`encode.sh` also needs
`ffprobe`, which `ffmpeg-static` does not ship**, so do the dense-GOP encode directly with the
same settings. And encode for **scrubbing**, `-g 8 -sc_threshold 0`, because a normal web
encode plays perfectly and scrubs like mud.

**Its verification pass earns its keep and catches things looking does not.** On the first
Revolut page it reported contrast at **2.72:1** on the hero copy, a repeated device family, and
a page 0.7 viewport-heights under the floor. The contrast failure had a structural cause worth
remembering: **the kit's `scrub` act is full bleed by construction, and some grammars forbid
full bleed.** When the grammar and the kit device disagree, the grammar wins. Drive the video
yourself off `--sc-p`, which the skill explicitly allows.

#!/usr/bin/env python3
"""Prove the video really is inside the first viewport, on desktop and on mobile.

Measures the player's bounding box against the viewport height rather than
eyeballing a screenshot, then saves the fold shot for a human to look at.
"""
import argparse, asyncio, pathlib, sys
from playwright.async_api import async_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from runpaths import Run, add_run_arg

_ap = add_run_arg(argparse.ArgumentParser(description="prove the hero film is above the fold"))
_ap.add_argument("slugs", nargs="*", help="defaults to every page in <run>/04-pages/live")
_a = _ap.parse_args()
RUN = Run(_a.run)
PAGES = RUN.need(RUN.live)
SLUGS = _a.slugs or sorted(p.stem for p in PAGES.glob("*.html"))
VIEWPORTS = [("desktop", 1440, 900), ("mobile", 390, 844)]


async def main():
    fails = []
    qadir = RUN.root / "_qa"; qadir.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for slug in SLUGS:
            for name, w, h in VIEWPORTS:
                pg = await b.new_page(viewport={"width": w, "height": h})
                await pg.goto((PAGES / f"{slug}.html").as_uri())
                await pg.wait_for_timeout(700)
                box = await pg.locator("video.hvid").bounding_box()
                if box is None:
                    fails.append(f"{slug}/{name}: no hero video element")
                    await pg.close()
                    continue
                visible = max(0, min(box["y"] + box["height"], h) - max(box["y"], 0))
                pct = visible / box["height"] * 100
                print(f"{slug:15} {name:8} top={box['y']:6.0f} h={box['height']:5.0f} "
                      f"visible in first viewport: {pct:5.1f}%")
                if pct < 50:
                    fails.append(f"{slug}/{name}: only {pct:.0f}% of the player is above the fold")
                await pg.screenshot(path=str(qadir / f"fold-{slug}-{name}.png"))
                await pg.close()
        await b.close()
    if fails:
        print("\nFAIL")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("\nPASS. The video is in the first viewport on every page, both viewports.")


asyncio.run(main())

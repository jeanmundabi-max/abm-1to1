#!/usr/bin/env python3
"""One picture per account, to put in front of the human the moment the creative exists.

    python3 contact_sheet.py <build dir> [--card <png>]      -> <build dir>/contact-sheet.png

Left: the page fold at 1440x900. Right: five frames of the film (2s, 11s, 20s, 26s, 31s).
Bottom: the ad card if given. Added because there was no view of what the creative
will be." A gate result is not a view. This is. Send the PNG (SendUserFile) before moving on.
"""
import argparse, asyncio, subprocess, tempfile
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright
def _ffmpeg():
    """ffmpeg, from the environment, then the local node install, then PATH."""
    import os, shutil
    if os.environ.get("FFMPEG"):
        return os.environ["FFMPEG"]
    local = Path(__file__).resolve().parent / "node_modules/ffmpeg-static/ffmpeg"
    if local.exists():
        return str(local)
    found = shutil.which("ffmpeg")
    if found:
        return found
    raise SystemExit("ffmpeg not found. Set FFMPEG, or run `npm install` in scripts/, "
                     "or install ffmpeg on PATH. Only the film frames need it.")

FF = _ffmpeg()

async def fold(index, out):
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await pg.goto(index.as_uri()); await pg.wait_for_timeout(1500); await pg.screenshot(path=str(out)); await b.close()

def frames(mp4, tmp):
    out = []
    for t in (2, 11, 20, 26, 31):
        f = tmp / ("f%02d.png" % t)
        subprocess.run([str(FF), "-y", "-loglevel", "error", "-ss", str(t), "-i", str(mp4), "-frames:v", "1", "-vf", "scale=640:-1", str(f)], check=False)
        if f.exists(): out.append(Image.open(f))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("build"); ap.add_argument("--card", default=None); a = ap.parse_args()
    d = Path(a.build).resolve(); tmp = Path(tempfile.mkdtemp())
    index, mp4 = d / "index.html", d / "hero.mp4"
    if not index.exists(): raise SystemExit("no index.html in %s" % d)
    asyncio.run(fold(index, tmp / "fold.png"))
    fold_im = Image.open(tmp / "fold.png"); fold_im.thumbnail((960, 600))
    fr = frames(mp4, tmp) if mp4.exists() else []
    card = Image.open(a.card) if a.card and Path(a.card).exists() else None
    if card: card.thumbnail((420, 525))
    left = fold_im.size[1] + ((card.size[1] + 24) if card else 0)
    right = sum(im.size[1] + 12 for im in fr)
    W = 960 + (660 if fr else 0); H = max(left, right)
    sheet = Image.new("RGB", (W + 40, H + 40), "white")
    sheet.paste(fold_im, (20, 20))
    y = 20
    for im in fr: sheet.paste(im, (1000, y)); y += im.size[1] + 12
    if card: sheet.paste(card, (20, 20 + fold_im.size[1] + 24))
    out = d / "contact-sheet.png"; sheet.save(out); print("-> %s %dx%d" % (out, *sheet.size))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Put the hero film in the FIRST VIEWPORT of each built page.

    python3 insert_hero_film.py --run ~/path/to/client-run

The film in the first viewport is a locked layout rule. `build_page.py` does not emit the
player, on purpose: once a design pass has landed on a page you patch it, you never
regenerate it, and the player is part of the patch rather than part of the generator.

What this changes, and nothing else:
  1. One scoped CSS block appended before </style>.
  2. The hero becomes two columns, copy left and player right, with the checks and the
     buttons moved to a full-width row underneath.
  3. Nothing outside the first <section> is touched.

The video src is a bare filename so it resolves both locally, next to the page, and
deployed, at a/<slug>/index.html beside a/<slug>/<slug>.mp4.

Idempotent: a page that already carries the player is left alone.
"""
import argparse, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runpaths import Run, add_run_arg

CSS = """
/* Hero film, inserted by insert_hero_film.py. The film sits in the first viewport. */
.herogrid{display:grid;grid-template-columns:1.05fr .95fr;gap:44px;align-items:center}
.herogrid .hcopy{min-width:0}
.herovid{min-width:0}
.herovid video{width:100%;aspect-ratio:16/9;display:block;border-radius:16px;
 border:1px solid var(--rule);background:#000;box-shadow:0 18px 48px rgba(0,0,0,.10)}
.vidcap{margin-top:12px;font-size:.83rem;color:var(--muted);display:flex;align-items:center;
 gap:9px;line-height:1.45}
.vidcap .dot{width:7px;height:7px;border-radius:50%;background:var(--blue);flex:none}
.herofoot{margin-top:34px}
@media(max-width:900px){.herogrid{grid-template-columns:1fr;gap:26px}
 .herovid{order:-1}}
"""

PLAYER = ('<div class="herovid"><video class="hvid" src="{slug}.mp4" poster="{slug}-poster.jpg" '
          'controls autoplay muted loop playsinline></video>'
          '<div class="vidcap"><span class="dot"></span>{caption}</div></div>')

def patch(html, slug, caption):
    if 'class="hvid"' in html: return html, "deja present"
    if "</style>" not in html: return html, "pas de bloc style"
    html = html.replace("</style>", CSS + "</style>", 1)

    i = html.index('<section><div class="wrap">')
    j = html.index("</div></section>", i)
    hero = html[i:j]
    open_tag = '<section><div class="wrap">'
    inner = hero[len(open_tag):]

    # tout ce qui precede les puces reste a gauche, le reste passe dessous
    m = re.search(r'<div class="checks">', inner)
    if not m: return html, "pas de bloc checks, structure inattendue"
    left, below = inner[:m.start()], inner[m.start():]

    new = (open_tag + '<div class="herogrid"><div class="hcopy">' + left + "</div>"
           + PLAYER.format(slug=slug, caption=caption) + "</div>"
           + '<div class="herofoot">' + below + "</div>")
    return html[:i] + new + html[j:], "insere"

def main():
    ap = add_run_arg(argparse.ArgumentParser(description="put the film in the first viewport"))
    ap.add_argument("--caption", default="Thirty two seconds. Plays without sound, so nothing here "
                    "needs your speakers. The same thing is written out further down the page.")
    a = ap.parse_args()
    run = Run(a.run)
    for p in sorted(run.need(run.live).glob("*.html")):
        slug = p.stem
        if not (run.live / (slug + ".mp4")).exists():
            print("  %-16s pas de mp4, saute" % slug); continue
        out, why = patch(p.read_text(encoding="utf-8"), slug, a.caption)
        if why == "insere": p.write_text(out, encoding="utf-8")
        print("  %-16s %s" % (slug, why))

if __name__ == "__main__":
    main()

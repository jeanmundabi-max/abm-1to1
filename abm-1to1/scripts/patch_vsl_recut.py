#!/usr/bin/env python3
"""
Carry the 32 second re-cut through to the content files and the built pages.

The film is now four beats, not five, and its timecodes moved. The page prints the
transcript beside the player and the two have to agree, so this rewrites C["vsl"] in
each content file and patches the same four rows straight into pages-v3/<slug>.html.

The pages are patched rather than rebuilt on purpose: build_page_v3.py would overwrite
the design pass that is already in them.
"""
import argparse, html, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runpaths import Run, add_run_arg

def e(s): return html.escape(s, quote=False)

_ap = add_run_arg(argparse.ArgumentParser(description="carry the film's cut into the pages"))
_a = _ap.parse_args()
RUN = Run(_a.run)
CFG = json.loads(RUN.need(RUN.pages / "transcripts.json").read_text(encoding="utf-8"))
H2, NOTE, RUNTIME = CFG["h2"], CFG["note"], CFG["runtime_words"]
BEATS = {k: [tuple(r) for r in v] for k, v in CFG["beats"].items()}
CONTENT = CFG["content_files"]

# the transcript rows and the content-file map are the client's, so they live in
# <run>/04-pages/transcripts.json rather than in this file

def py_block(slug):
    rows = "".join('  ["%s", "%s", "%s"],\n' % b for b in BEATS[slug])
    # show_transcript survives the rewrite. Without this the flag was silently dropped every
    # time the transcript was recut, and the written-out section reappeared under the hero.
    # Absent from transcripts.json means absent here, so an unported run is byte identical.
    show = CFG.get("show_transcript")
    extra = "" if show is None else ' "show_transcript": %s,\n' % bool(show)
    return ('C["vsl"] = {\n "h2": "%s",\n "note": "%s",\n%s "beats": [\n%s ],\n}\n'
            % (H2, NOTE, extra, rows))

def html_block(slug):
    return '<div class="beats">' + "".join(
        '<div class="beat"><div class="tc">%s</div><div><h3>%s</h3>'
        '<p class="lede" style="margin-top:6px">%s</p></div></div>' % (tc, e(t), e(b))
        for tc, t, b in BEATS[slug]) + "</div>"

for slug, cf in CONTENT.items():
    # 1. the content file, the record of what the film says
    p = RUN.pages / cf
    src = p.read_text(encoding="utf-8")
    # les fichiers ecrits a la main utilisent des guillemets doubles, ceux generes des simples
    import re as _re
    m = _re.search(r'^C\[[\'"]vsl[\'"]\]', src, _re.M)
    if not m: raise SystemExit("pas de C[\"vsl\"] dans %s" % p)
    i = m.start()
    n = _re.search(r'^C\[[\'"]', src[i + 8:], _re.M)
    j = i + 8 + n.start() if n else len(src)
    p.write_text(src[:i] + py_block(slug) + "\n" + src[j:], encoding="utf-8")

    # 2. the page: runtime in the caption, loop on the hero, and the transcript rows
    q = RUN.live / (slug + ".html")
    h = q.read_text(encoding="utf-8")
    h = re.sub(r"(Ninety seconds|Thirty two seconds)(\. Plays without sound)",
               RUNTIME + r"\2", h)
    h = re.sub(r'(<video class="hvid"[^>]*?)\bcontrols autoplay muted playsinline',
               r'\1controls autoplay muted loop playsinline', h)
    a = h.index('<div class="beats">'); b = h.index("</div></div></div>", a) + len("</div></div></div>")
    h = h[:a] + html_block(slug) + h[b:]
    h = h.replace("The ninety second version", H2)
    q.write_text(h, encoding="utf-8")
    print("  %-16s content + page patched" % slug)

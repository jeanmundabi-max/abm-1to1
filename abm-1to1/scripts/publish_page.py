#!/usr/bin/env python3
"""
Push one account's page and its media to the GitHub Pages repo behind the previews.

    python3 publish_page.py --run ~/path/to/client-run the-gym-group [the-aa ...]

Target repo and path come from <run>/00-inputs/deploy.json. Repo layout is
a/<slug>/index.html plus the account's mp4 and poster beside it.
Idempotent: an unchanged file is skipped rather than committed again.
Written 2026-08-20 during the VSL re-cut, because the deploy had never been scripted.
"""
import argparse, base64, hashlib, json, os, sys, urllib.request, urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runpaths import Run, add_run_arg

ap = add_run_arg(argparse.ArgumentParser(description="publish pages and media to GitHub Pages"))
ap.add_argument("slugs", nargs="+")
ARGS = ap.parse_args()
RUN = Run(ARGS.run)
CFG = json.loads(RUN.need(RUN.inputs / "deploy.json").read_text(encoding="utf-8"))
REPO, PATH_TMPL = CFG["repo"], CFG.get("path", "a/{slug}")

def env():
    out = {}
    for line in Path.home().joinpath(".config/abm-1to1/secrets.env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out

E = env()
TOKEN, OWNER = E["GITHUB_TOKEN"], CFG.get("owner") or E["GITHUB_USERNAME"]
API = "https://api.github.com/repos/%s/%s/contents/" % (OWNER, REPO)

def call(path, method="GET", body=None):
    req = urllib.request.Request(API + path, method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json", "User-Agent": "mdb-publish"})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r)
    except urllib.error.HTTPError as ex:
        if ex.code == 404: return None
        raise SystemExit("%s %s -> %s %s" % (method, path, ex.code, ex.read()[:300].decode()))

def blob_sha(data):                       # git's own object id, so we can skip no-op writes
    h = hashlib.sha1(); h.update(b"blob %d\0" % len(data)); h.update(data); return h.hexdigest()

def put(local: Path, remote: str, msg: str):
    data = local.read_bytes()
    cur = call(remote)
    if cur and cur.get("sha") == blob_sha(data):
        print("  =  %-32s unchanged" % remote.rsplit("/", 1)[-1]); return
    body = {"message": msg, "content": base64.b64encode(data).decode()}
    if cur: body["sha"] = cur["sha"]
    call(remote, "PUT", body)
    print("  -> %-32s %s KB" % (remote.rsplit("/", 1)[-1], len(data) // 1024))

for slug in ARGS.slugs:
    src, base = RUN.live, PATH_TMPL.format(slug=slug)
    print(slug)
    put(src / (slug + ".html"), base + "/index.html", "%s: page" % slug)
    for extra in ((slug + ".mp4"), (slug + "-poster.jpg")):
        f = src / extra
        if f.exists(): put(f, "%s/%s" % (base, extra), "%s: %s" % (slug, extra))
    print("   https://%s.github.io/%s/%s/" % (OWNER, REPO, base))

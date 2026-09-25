#!/usr/bin/env python3
"""
Start a client engagement. Creates the run folder and drops the config templates in it.

    python3 new_run.py ~/abm-runs/<client>/abm-1to1

Then export ABM_RUN_DIR to it and every other script in this skill picks it up.
Nothing here talks to an API and nothing costs anything.
"""
import shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE.parent / "config"

DIRS = ["00-inputs", "01-evidence", "02-committee", "03-creative",
        "04-pages/live", "04-pages/vsl", "05-campaign", "_archive", "_qa"]

# example -> where it belongs, and what it is for
TEMPLATES = [
    ("account_list.example.csv",    "00-inputs/account_list.csv",        "the accounts, and why each is on the list"),
    ("narrow.example.json",         "00-inputs/narrow_uk.json",          "the targeting levers"),
    ("deploy.example.json",         "00-inputs/deploy.json",             "where the pages get published"),
    ("champion-search.example.json","02-committee/champion-search.json", "the titles to hunt for the champion seat"),
    ("pages.example.json",          "04-pages/pages.json",               "brand, vendor, and the slug to content map"),
    ("films.example.json",          "04-pages/vsl/films.json",           "one hero film spec per account"),
    ("transcripts.example.json",    "04-pages/transcripts.json",         "the film's beats, printed beside the player"),
]

def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    run = Path(sys.argv[1]).expanduser()
    if run.exists() and any(run.iterdir()):
        raise SystemExit("%s already exists and is not empty. Refusing to write into it." % run)
    for d in DIRS:
        (run / d).mkdir(parents=True, exist_ok=True)

    print("run folder: %s\n" % run)
    for src, dst, why in TEMPLATES:
        shutil.copy(CONFIG / src, run / dst)
        print("  %-34s %s" % (dst, why))

    (run / "RUN-LOG.md").write_text(
        "# RUN LOG\n\n"
        "The execution ledger for this engagement. One row per failure that really happened,\n"
        "and the fix beside it. Nothing theoretical. If it did not cost time or ship wrong,\n"
        "it does not go in.\n\n"
        "| # | Date | What really happened | The fix |\n|---|---|---|---|\n", encoding="utf-8")
    print("  %-34s the execution ledger, empty and waiting" % "RUN-LOG.md")

    print("""
Next:

    export ABM_RUN_DIR=%s

Then fill 00-inputs/account_list.csv and start at sops/01-onboarding.md.
The first command that does anything real is:

    python3 %s/narrowing_walk.py
""" % (run, HERE))

if __name__ == "__main__":
    main()

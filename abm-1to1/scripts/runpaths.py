"""One place that knows the shape of a run folder, so every script agrees.

A run folder is one client engagement. Layout:

    <run>/
      RUN-LOG.md          the failure ledger for this engagement
      00-inputs/          offer, config, account list
      01-evidence/        source-ladder output, Mind-Reader surveys, pilot write-ups
      02-committee/       committee.csv and how it was built
      03-creative/        briefs and rendered ads
      04-pages/           content_<account>.py, live/ (the built pages), vsl/ (the films)
      05-campaign/        LinkedIn ids, preview URLs
      _archive/           superseded generations, kept but out of the way

Every script takes --run. If it is omitted we use $ABM_RUN_DIR, then the cwd.
"""
import os
from pathlib import Path

def add_run_arg(parser):
    parser.add_argument("--run", default=os.environ.get("ABM_RUN_DIR", "."),
                        help="the client run folder. Defaults to $ABM_RUN_DIR, then the cwd")
    return parser

class Run:
    def __init__(self, root):
        self.root = Path(root).expanduser().resolve()
        if not self.root.is_dir():
            raise SystemExit("run folder not found: %s" % self.root)
    def __repr__(self): return "Run(%s)" % self.root
    @property
    def inputs(self):    return self.root / "00-inputs"
    @property
    def evidence(self):  return self.root / "01-evidence"
    @property
    def committee(self): return self.root / "02-committee"
    @property
    def creative(self):  return self.root / "03-creative"
    @property
    def pages(self):     return self.root / "04-pages"
    @property
    def live(self):      return self.root / "04-pages" / "live"
    @property
    def vsl(self):       return self.root / "04-pages" / "vsl"
    @property
    def campaign(self):  return self.root / "05-campaign"
    def need(self, p):
        if not p.exists(): raise SystemExit("expected %s and it is not there" % p)
        return p

#!/usr/bin/env python3
"""The path, in plain words. Print it right after the layer question is answered, before any work.

    python3 the_path.py --layer 2 --mode demo --client "ElevenLabs" --product "ElevenAgents"
    python3 the_path.py --layer 1 --mode live --client "Figure"

Eight parts. For each: what happens, what you get, and where you are needed. Written for
someone who has never opened Campaign Manager, so it can be read out on a recording as is.
No house words: no leg, gate, rung, lever, EDP, URN.

Added 2026-09-11 from Jean's review of the ElevenLabs dry run: "at the beginning, say this
is the step we will be going through, and the expectations."
"""
import argparse

def parts(layer, mode, client, product):
    demo = mode == "demo"
    who = ("you pitching %s" % client) if layer == 1 else ("%s selling %s to the companies it wants as customers" % (client, product or "its product"))
    P = [
     ("What they sell",
      "We read the %s site and write down what they sell, who pays for it, who uses it, and what proof they publish." % client,
      "A one-page profile, and the four tests a company has to pass to be worth a page.",
      "Nothing more. The layer question is already answered: this run is %s." % who),
     ("The list",
      "From what they sell we work out which companies have the problem today, find the public file that proves it, and read that file.",
      "Twenty named companies, with the reason each one is on the list and the file it came from.",
      "You look at the twenty and say yes, or change them. Nothing is built on a list you have not seen."),
     ("Is it still true today",
      "Every figure is read again from the source on the day. A company being bought, sold or broken up is put aside, because it will not choose a supplier while that is going on.",
      "The build set, usually five to seven, one per sector, and the reason any company was set aside.",
      "Nothing, unless a figure has died."),
     ("Who we can reach",
      "LinkedIn tells us how many people at each company we can put an ad in front of. We narrow that to the people who would decide: 300 to 1,000 per company.",
      "One number per company, and the choice that got it there.",
      "Only if a company comes out too small to reach. Then we choose together whether to widen or drop it."),
     ("Who decides",
      "The names: the boss, the person who owns the budget, the technical owner, and the person who feels the problem every month. From company filings and their own site first.",
      "A short table per company: seat, name, where the name came from.",
      "Only if a name has to be bought. That costs credits and we ask before spending one."),
     ("The page and the film",
      "One page per company, written from their seat: the problem they have now in their own numbers, then the fix, then what %s does about it, then proof from peers who already use it. A thirty-second silent film sits at the top." % (product or client),
      "One page and one film per company, live on the web.",
      "You see each page and film as it is made, and you say if it is right before the next one."),
     ("The ad",
      "One ad card per company, the same idea as the film, frozen. The company's own number is the biggest thing on it.",
      "The cards, and the words that go with them.",
      "You see every card before anything is pushed. Once pushed, an ad cannot be un-made."),
     ("The campaign",
      "Everything is built on LinkedIn as drafts. Nothing goes live, nothing is spent. Then a one-page handover says what was built and why, in plain words, with the previews.",
      "Six draft ad sets, the previews, the handover.",
      "The daily budget. We never guess it." + (" This is a demonstration, so it is a placeholder and nothing will ever run." if demo else " And the go to activate, which is a separate decision on another day.")),
    ]
    return P

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layer", type=int, choices=(1, 2), required=True)
    ap.add_argument("--mode", choices=("demo", "live"), required=True)
    ap.add_argument("--client", required=True)
    ap.add_argument("--product", default="")
    a = ap.parse_args()
    print("\n%s: the eight parts, and where you are needed\n" % a.client)
    for i, (name, what, get, you) in enumerate(parts(a.layer, a.mode, a.client, a.product), 1):
        print("Part %d. %s" % (i, name))
        print("  %s" % what)
        print("  You get: %s" % get)
        print("  You are needed for: %s\n" % you)
    print("Three of the eight always stop for you: the list, the ad, the budget. Everything else runs unless something is wrong.\n")

if __name__ == "__main__":
    main()

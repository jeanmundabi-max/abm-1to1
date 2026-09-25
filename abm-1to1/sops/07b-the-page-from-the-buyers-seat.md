# The page, written from the buyer's seat

_Part of the `abm-1to1` skill. Read with `07-the-page-and-hero-film.md`, which holds the
build mechanics. This file holds the SHAPE and the VOICE, and it overrides anything in 07
that contradicts it. Added 2026-09-11 from Jean's review of the ElevenLabs dry run._

## The one rule

**Nobody buys a product from the vendor's own wall.** They buy it from the people who already
use it, and they buy it for a problem they already have. So the page is written from the
buyer's seat, in the shape of a D100: the problem they have right now in their own numbers,
then why it happens, then the fix, then what people like them got from it, then what can be
done for them. The client appears as the thing the peers used, never as the narrator.

What the dry run did instead, so it is never done again: a section headed *"What an
ElevenAgent is, in ElevenLabs' own words"*, the vendor's three product lines listed, plan
pricing pasted from the vendor's page, and *"the mechanism, in one sentence"*. Jean: *"you
don't put yourself in the prospect's POV. Nobody buys ElevenLabs from its own words. It should
be from the peers, the people that use it."*

## The shape, in order

| # | Beat | From whose seat | What is on it |
|---|---|---|---|
| 1 | The ad continues | the reader who just clicked | The card they clicked, alive: the film, and their number. The headline is the ad's promise, not a restatement of the number |
| 2 | The problem they have now | theirs | Their figure, from their file, quoted whole with the period. Then the arithmetic of the next quarter in their own units. Nothing inferred, nothing borrowed |
| 3 | Why it happens | theirs, taught plainly | One beat, one sentence a stranger can check, no product yet. The reason the number sits where it sits. On a cold reader this is the beat that earns the right to name a fix |
| 4 | The fix, named | theirs | The client's product, by name, in one paragraph written as what changes for THEM. Not architecture, not a plan list, not a per-minute rate |
| 5 | People like them | the peers' | Named users, quoted in their own words, with the figure and the limit on it. A Director of CX at a bank speaking to a Director of CX at a bank. The vendor's aggregate stats (millions of conversations, thousands of voices) do not go here; they are the vendor's wall |
| 6 | What can be done for them | theirs | The offer: what arrives, what does not, what it costs them in trust. What receives the yes |
| 7 | Who decides | the committee's | A seat each, the first question each asks, the answer, and the paragraph to forward |
| 8 | Everything anyone has asked | theirs | The objections, the awkward ones included |
| 9 | The ask | theirs | One field, one button, the same sentence as the ad |

The film sits in beat 1, in the first viewport, per 07. The signature move sits where the
reader is most uneasy, usually beat 2 or 3. The rule of respite still applies: one quiet beat
after the densest one.

## Voice

- Second person, to the person in the seat. "Your callers are asked for 3:33." Never "the
  account", never "this page", never the operator's first person.
- The test on every paragraph: **would the Director of Customer Operations say this about her
  own problem, in these words?** If it reads like the vendor's brochure or the operator's
  notes, it is rewritten.
- Dog-whistle words from the Mind-Reader Survey (AHT, containment, abandonment, cost-to-serve)
  in the buyer's paragraphs; none of the vendor's marketing words anywhere.
- Every peer quotation is printed whole, attributed, with its qualifier. A described result is
  presented as the vendor's description, not as the peer's words.

## Banned on the page, and the gate checks for them

| Banned | Why |
|---|---|
| *"in [vendor]'s own words"* as a heading or a device | the vendor narrating itself |
| a list of the vendor's product lines ("sells three things") | the reader did not click for a catalogue |
| plan pricing pasted from the vendor's site | it is the vendor's wall, and on Enterprise it is wrong anyway |
| *"the mechanism, in one sentence"* or any architecture paragraph (CCaaS, CRM, ticketing stack) | that is beat 3 done as a spec sheet; teach the reason, not the plumbing |
| the vendor's aggregate stats as proof | a number about the vendor is not proof about the reader |

`scripts/page_standard.py` fails a page on the first two and on "Pricing is public".

## The visual floor

The Revolut builds (`revolut/abm-1to1/07-scrollcraft/builds/`) are the floor. Jean rejected
"flat" three times on that run and "pale" once on this one. Dense, instrument-like, the ad
continuing alive on the page, the client's colour on one meaningful element inside the
target's own world. A page that reads as a document beside Hays is rebuilt before it is shown.

Where the paleness came from on the dry run: the BRIEF's answer to "how far from premium minimal"
was *"Quiet. Monochrome."*, copied from the WYN brief for a civil-servant reader. The Hays
brief, after three rejections, answers the same question *"Not minimal. Dense and instrument-like,
closer to editorial."* That is the default answer now for a cold commercial buyer. Quiet is a
choice that has to be argued in the BRIEF, not inherited.


## Le geste doit repondre au doigt, et cela se verifie

Le moteur de defilement rend les evenements de pointeur a un bloc **seulement quand ce bloc est
a moitie visible**, et il ecrit cela en style direct sur l'element. Un geste signature place dans
un bloc porteur d'un `data-sc-cue` est donc **mort au toucher** pendant une bonne partie de son
acte. Trouve le 2026-09-23: un appui de sept secondes au centre de l'anneau ne declenchait rien,
ni sur telephone ni sur ordinateur, sur les six pages.

Deux lignes, obligatoires sur tout bloc interactif:

    .holdwrap, .holdwrap *{pointer-events:auto!important}

et une zone de clic transparente sur toute la surface du SVG, parce qu'un cercle en `fill="none"`
n'a de surface sensible que son trait:

    <rect x="0" y="0" width="320" height="320" fill="transparent"/>

**La verification fait partie du travail, pas de la relecture.** Avant de montrer une page:
appuyer reellement cinq secondes au centre du geste, sur un ecran de telephone et sur un ecran
d'ordinateur, et lire la phrase qui apparait. Un test qui mesure la position de l'element puis
appuie plus tard echoue tout seul, parce qu'un acte epingle bouge entre les deux: viser
l'element au moment de l'appui.

## Le telephone est la moitie du travail

Verifie a 390 pixels de large avant de montrer quoi que ce soit:

- **le bandeau fixe**: sous 620px il ne reste que le nom et la tuile qui s'allume. Quatre tuiles
  a 390px se chevauchent en bouillie illisible;
- **aucun ecran entierement vide**: un bloc sombre plus haut que l'ecran, avec la copie en haut
  et le geste sous la ligne de flottaison, donne un cran de defilement entierement noir, qui se
  lit comme un chargement rate. Le geste et sa phrase tiennent ensemble sur un ecran;
- **descendre toute la page en quatorze arrets** et regarder la planche: c'est la seule facon de
  voir un vide, une colonne coupee ou un titre orphelin.

## Show it as it is made

Beat 1 (the fold, with the film) and beat 5 (the proof) are shown to Jean as screenshots
before the rest of the page is written. He decides on the picture, not on a gate result.

_Strategy & GTM research by Jean Mundabi Fala_

# Spending money inside this skill

Three services in this pipeline cost real money: **AI Ark** for contacts, **OpenAI** for
generated creative, and **LinkedIn** the moment a campaign leaves DRAFT. This file is the
price list and the rule.

## The rule

**Ask before spending. Every time. Including small exploratory runs.**

Stated as absolute:

> *"Ce que je ne veux pas, c'est que tu gaspilles mes crédits d'Ark. En aucun cas tu
> dépenses des crédits d'Ark sans me demander."*

`guard()` in `niche-engine/plays/spend_guard.py` is the mechanism: it prints the
justification, refuses a run that has nothing to do or would breach the reserve floor, and
appends every run to `spend-ledger.jsonl`. But the mechanism is not the rule. The rule is
**say the number out loud first**.

## AI Ark, measured

| Call | Cost | Returns |
|---|---|---|
| `GET /payments/credits` | **free** | the balance |
| `POST /companies` | 0.1 per result | company profile |
| `POST /people` | **0.5 per result** | name, title, LinkedIn. **Never an email** |
| `POST /people/export/single` | 1 per **found** email | the email. Free when none is found |

**A name-only preview is not free.** This is the trap. The natural assumption is that names
are free and emails are paid, which is true of public sources and false of Ark. 48 results
of a people search costs 24 credits and returns no emails at all.

**You are charged per result RETURNED, not per result requested.** A search priced at 24
credits for 48 results cost 8.5 when only 17 people matched. Price the ceiling, report the
actual.

**Never trust a written balance, including one in a note like this.** Read it with the free
GET at the start of every run.

## What is genuinely free, and will get you most of the way

For a buying committee, public sources give the whole C-suite and cost nothing:

- Companies House officers, with appointment dates. `scripts/ch_officers.py`
- The company's own leadership page, **including the individual bio pages**
- The company's own press releases, which is where a seat that has changed hands is announced
- An annual report's risk-ownership table, for an equity-listed company
- An SFCR's key function holders, for a regulated insurer

Public data gives you the buyer and never the champion. Budget for the champion only.

## OpenAI

Image generation for personalised creative. `OPENAI_API_KEY` is the funded key; the
Anthropic and Gemini keys in the same file are empty.

## LinkedIn

Everything this skill builds is DRAFT and costs nothing. **Activation is a separate,
explicit step and it is never taken inside a build.** See `sops/09-build-qa-and-preview.md`.

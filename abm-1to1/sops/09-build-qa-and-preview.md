# Build to DRAFT, then QA the preview

## Step 10b. Decide three fields BEFORE you build. All three were got wrong once.

### The objective is a funnel stage, not a consequence of having a landing page

A 1:1 ABM account that has never heard of the client is **cold**, whatever else is true.
Cold gets `ENGAGEMENT`. [the upstream LinkedIn ABM guide](https://github.com/swan-gtm/gtm-skills/blob/main/skills/ivan-falco/linkedin-ads-abm-guide/SKILL.md):

> *"To warm up a cold audience, use an engagement objective, not a website-visits objective...
> you optimize (and pay) for a landing-page click before the account has any intent, so you burn
> budget. Move to traffic/conversion objectives only at the WARM stage."*

The landing page still exists and is still clicked. It is simply not what LinkedIn is told to buy.
`WEBSITE_VISIT` belongs to stage two, once the retargeting pool exists.

**How this was got wrong:** all four WYN ad sets were switched to `WEBSITE_VISIT` on the reasoning
that the ad's job is to reach a page. The change was made **while correcting a different mistake**,
and the guide sat in a folder that had never been opened.

### The name is the report

```
ad set : [Client] - [Region] - [Stage] - [Awareness] - [Type] - {Account}
         WYN - UK - Create - Unaware - 1to1 - Home Office
group  : [Shared intent]
         WYN - Software contract expiring
```

Without the stage in the ad set name, cold and warm collide the day stage two exists and no report
can separate them. The **group** carries the shared intent rather than the client's initials, and
that is mechanical rather than tidy. The upstream kit:

> *"Group by shared intent rather than persona... more engagements roll up at campaign-group level,
> easier to hit LinkedIn's 3-engagement minimum for API data."*

LinkedIn obfuscates engagement data below that floor, which bites hardest on 1:1 ABM because each
account is small by design. The group name is one of the free mitigations. The other is to read
engagement over **30 or 90 days, never 7**.

### `locale` is the audience's country

The upstream kit's config default is `en_US` with a note to adjust per client. A UK-only audience takes
`{"country":"GB","language":"en"}`. Nobody notices this one until a client does.

### If you rename any of the three later, three files move together

`account_map.json` and `PREVIEWS.txt` are keyed by the ad set **name**, and `build_handover.py`
does a `.get(name)` that **drops the client's preview links without erroring**. Rename LinkedIn,
the map and the previews in one pass, rebuild, then **count** the rendered `Open the preview` links
against the number of accounts. A silent drop of four client-facing links is the failure this
paragraph exists to prevent.

---

## Step 11. Build to DRAFT

```bash
cd "$HOME/.claude/skills/abm-1to1/scripts"
python3 build_campaign.py --config <run>/00-inputs/abm_config.json            # dry run
python3 build_campaign.py --config <run>/00-inputs/abm_config.json --execute  # DRAFT
```

`scripts/ad_account_guard.py` runs before Phase 1 on every invocation. It fails closed on
any ad account that is not on your own allowlist, which lives outside the repo at
`~/.config/abm-1to1/ad_accounts.json`. A token can come back able to see accounts you do not
own, and if one of those is runnable a wrong `account_id` spends somebody else's money. For a
period this SOP said the guard was wired into the build when it was not, so a wrong
`account_id` reached the API unchecked. Documenting a control is not the same as having one.

The same check refuses a required key that is present but null. `org_id: null` used to pass,
render as `urn:li:organization:None`, and fail once per company at Phase 6, after the group
and every ad set had already been created.

Easy to forget and mandatory: attach active **conversions** to every ad set, set
**UTMs at ad-set level** (never baked into ad URLs), and build the single-image link
ad as an **article** post or it loses its destination URL and CTA.

### Guardrail, all of these are the upstream kit's, recorded from real builds

| Failure | Fix |
|---|---|
| Built single-image ads as `content.media`, so no destination URL, no headline, no CTA | Always `content.article` |
| Treated the `createInline` 200 as a failure and stopped mid-build | A 200 with a `value.creative` body IS success |
| Hit a transient 500 and abandoned, leaving ad sets with no ad | Retry once, then two-step. Never leave an ad set empty |
| Forgot conversions and UTMs | Both mandatory, not optional |
| Claimed an ad was done without GET-verifying it | Every phase has a verify gate |

And one of ours:

| Failure, really happened | Fix |
|---|---|
| **`adTrackingParameters` 500'd on every UTM attempt across three days, and I wrote on a client-facing page that it was LinkedIn's bug.** It was not | Five things, all mine. The path needs the **restli key** `(adEntity:(sponsoredCampaign:{enc urn}))`, not a bare URN; the field is **`customValueParameters`** / **`dynamicValueParameters`** and both are **maps, not arrays**; `idempotencyToken` is a **query parameter**, not a body field; and **`adEntity` must ALSO appear in the body** as `{"sponsoredCampaign": "<urn>"}`. With all five it returns 201 and GET-verifies 200. **Never attribute a failure to the vendor on a page a client will read** |
| **The fix above was written here on 2026-09-08 and implemented nowhere.** Every build since 500'd on UTMs and the row was read as history rather than as a bug | Implemented in `set_utms()` on 2026-09-24, with `--utms-only` so a repair does not rebuild ad sets. **An instruction is not a mechanism.** When a guardrail row names a code fix, the row is not done until the code carries it |
| **All 7 ad sets 400'd: `Value USD of /Campaign/dailyBudget/currencyCode expected to match value GBP of /Account/currency`** | The ad account is **GBP**. The config said USD and the dry run cannot catch it, because Phase 1 only resolves and sizes. **Read the account's `currency` field before writing a budget**, and note the campaign group is created in Phase 2 *before* the first ad set fails, so a currency error leaves an orphan DRAFT group. Put its id in `existing_group_id` and re-run rather than making a second |
| **The image upload PUT returns 400 with only an `Authorization` header.** The upstream `upload_image()` sends exactly that, so the step fails on the upstream script | The signed upload URL needs **`Content-Type: application/octet-stream`** on the PUT. With it, 201. Do not edit the upstream script, wrap it |
| **A post's `content` is immutable too.** After a repo rename every ad destination was dead, and `content.article.source` refused every patch shape: nested restli, `$set` on the leaf, `$set` on the whole object, all **422** | Only the **top-level `contentLandingPage`** takes a `PARTIAL_UPDATE` (204). If the article's own source is what carries the click, the post must be **rebuilt**, not patched. Establish which one the ad actually uses **on the rendered preview** before rebuilding anything, because `GET /posts` is 403 on this token and there is no other way to know |
| Tried to repoint an existing creative at a new post | **A creative's `content.reference` is immutable.** Create a new creative on the ad set instead |
| Tried to pause the superseded creative | Refused: *"status transition is not allowed from ACTIVE to PAUSED if reviewStatus is not set to APPROVED"*. On a DRAFT ad set nothing has been reviewed, so both creatives sit ACTIVE. **Nothing serves while the ad set is DRAFT**, but say so out loud and resolve it before any activation |
| Reached for a copy of the operator's browser profile to capture an authenticated preview | Do not. Ask them to relaunch Chrome with `--remote-debugging-port=9222` and connect over CDP, or hand them the URL. A cookie store is not ours to copy |

---

---

## Step 12. QA and the ad preview

GET every object back. Confirm targeting, budget, **DRAFT status**, conversions,
UTMs, destination URL, CTA, headline.

**Then build the preview URL for every ad set. This is a deliverable, not a note.**

```
https://www.linkedin.com/feed/update/urn:li:sponsoredContentV2:({post URN},urn:li:sponsoredCreative:{id})/?actorCompanyId={org id}&viewContext=REVIEWER
```

Open every one. Screenshot every one. The preview is what proves the ad exists and
renders, and it is the single most convincing artefact in Step 13.

Then stop. State what activation would cost and hand the decision to the human.

### Guardrail

| Failure, really happened | Fix |
|---|---|
| Preview treated as a QA note and never opened | Open it, screenshot it, it is deliverable |
| No conversions exist on the ad account, so none were attached | Say it out loud. It needs the Insight Tag on a site we control. Not a blocker for DRAFT, but never skip it silently |
| Skipped conversions because the objective was ENGAGEMENT | The upstream kit's SOP: *"Engagement-objective campaigns still get conversions - do not skip."* And note his method is to **replicate an active campaign's conversion set**. On an account with no active campaign there is nothing to replicate, so name that as the reason instead of leaving the phase blank |
| Claimed Phase 6's verify gate passed | `GET /posts/{urn}` returns **403** on a token holding `w_organization_social` without `r_organization_social`. The gate cannot pass by the upstream method on this token. Close it on the **rendered preview** instead, and say which route was used |

---

---

## Ce que la camera lit, 2026-09-23

Tout ce qui s'affiche dans le terminal pendant une demonstration est un livrable, au meme titre
qu'une page. Un ecran qui dit `0 UNNARROWED`, `BELOW BAND, drop a lever` ou `urn:li:organization:`
apprend au spectateur que le systeme parle une langue qu'il ne parle pas.

Regle: **aucun mot de maison a l'ecran**. Ni leg, ni gate, ni lever, ni band, ni URN, ni facet.
`scripts/narrowing_walk.py` et `scripts/demo_start.py` ont ete reecrits sur ce principe; la sortie
dit maintenant "everyone who works there", "without junior roles", "only the buying teams",
"TOO FEW. LinkedIn will not run an ad below 300", "a copycat page, skipped".

Avant un enregistrement: lancer chaque commande filmee et **lire sa sortie a voix haute**. Si une
ligne demande une explication, elle est reecrite, pas expliquee.

---

## Un brouillon sans lien cliquable n'est pas livre, 2026-09-23

Un apercu montre **l'annonce**. Il ne montre pas le reglage: l'audience, le budget, le statut,
et le fait que rien ne tourne. Le client, ou l'operateur, doit pouvoir **ouvrir le brouillon la
ou il vit**, en un clic, sans chercher un identifiant dans un fichier.

**Les formes d'adresse, verifiees sur une session reelle le 2026-09-23.** La premiere version
de cette section inventait `/campaign-groups/{id}/campaigns`, qui n'existe pas: Campaign Manager
a repondu "The page you are looking for could not be found". Un chemin d'interface ne se deduit
pas, il se clique une fois.

| Quoi | Adresse | Verifie |
|---|---|---|
| Le compte | `https://www.linkedin.com/campaignmanager/accounts/{account_id}` | oui |
| Le groupe | `.../accounts/{account_id}/campaigns?campaignGroupIds=%5B{group_id}%5D` | **oui, 23 sept**. Le groupe est un FILTRE en parametre, pas un segment de chemin |
| Un ad set, ses reglages | `.../accounts/{account_id}/campaigns/{campaign_id}` | **oui, 23 sept** |
| Un ad set, ses annonces | `.../accounts/{account_id}/campaigns/{campaign_id}/creatives` | meme forme, meme session |

**Et l'apercu du fil, qui est l'autre moitie.** Celui-la se construit entierement depuis l'API,
avec les deux URN que la creation renvoie:

    https://www.linkedin.com/feed/update/urn:li:sponsoredContentV2:({post},{creative})/?actorCompanyId={org_id}&viewContext=REVIEWER

Les deux liens repondent a deux questions differentes et il faut les deux. L'apercu montre
**l'annonce telle qu'un humain la verra**. Campaign Manager montre **le reglage**: audience,
budget, statut, et qu'il ne tourne pas. Ne jamais livrer l'un sans l'autre.

Ou ils vont, et ce n'est pas au choix:

1. **`PREVIEWS.txt`**, sous les apercus, un bloc "Ouvrir dans Campaign Manager" avec le compte,
   le groupe et les six ad sets;
2. **`account_map.json`**, une cle `cm` par societe et une cle `_cm` pour le compte et le groupe;
3. **le document de remise**: un bandeau en tete, "See it yourself, on LinkedIn", et **dans la
   fiche de chaque societe une ligne "The draft itself, on LinkedIn"** a cote de l'apercu de
   l'annonce, avec le numero de l'ad set et ce qu'on y verra.

**Et une page cliquable, pas un fichier texte.** `05-campaign/OUVRIR-LES-BROUILLONS.html`: une
ligne par societe, la carte en vignette, puis les quatre liens cote a cote, l'annonce dans le
fil, les reglages, les annonces, la page d'atterrissage. Plus le groupe entier en haut. C'est
ce qu'on ouvre devant quelqu'un; `PREVIEWS.txt` reste la trace pour l'operateur.

`finish.py` ecrit les liens, `build_handover.py` les affiche, et la page cliquable se construit
dans la foulee. Une remise qui decrit un brouillon que
personne ne peut aller regarder demande au lecteur de croire sur parole, ce qui est exactement
ce que cette page existe pour eviter.

**Et le document de remise se montre, il ne se mentionne pas.** Le construire, l'ouvrir, et
donner son chemin. Le 23 septembre j'ai annonce huit parties terminees sans que la remise soit
devant Jean.

### Deux documents, pas un, et pourquoi

La question s'est posee le 2026-09-23: fondre la page cliquable dans la remise, ou la garder a part.
**A part**, et les deux se pointent l'un l'autre.

| | La remise | La page des brouillons |
|---|---|---|
| Combien de mots | ~4 500, dix sections | ~300 |
| Ce qu'elle fait | elle **argumente**: d'ou vient la liste, pourquoi ces six, qui voit l'annonce, ce qui n'est pas fait | elle **ouvre**: quatre portes par societe |
| Qui la lit | quelqu'un qui decide si le travail tient | quelqu'un qui veut regarder maintenant |
| Quand | une fois | a chaque fois |
| A l'ecran | on la lit | on la partage et on clique dedans |

Les fondre casse les deux: un tableau de bord noye dans un argumentaire ne sert plus de tableau de
bord, et un argumentaire qui commence par douze liens n'est plus lu. **Une seule source
d'identifiants** (`abm_config.results.json` et `account_map.json`), deux vues generees de la,
et un lien dans chaque sens en haut de chaque page. Les identifiants ne peuvent pas diverger,
parce qu'aucun des deux n'est ecrit a la main.

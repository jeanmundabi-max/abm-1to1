# Funnel stages, retargeting, and the channels around the ads

This skill builds **stage one only**. That is a deliberate scope, not an omission, but it is only
defensible if you can say what stages two and three are and hand the client the map. Everything
below is read from the upstream kit's own files, named beside each claim.

## The three stages, and why the order is not negotiable

`linkedin-ads/references/full-funnel-framework.md`:

> *"Only ~5% of your B2B market is 'in-market' at any given time. 90% of those prefer vendors they
> already know."*

| | Stage one, cold | Stage two, warm | Stage three, ready |
|---|---|---|---|
| Purpose | *"Get on the radar. Build retargeting audiences. NOT meant to drive direct conversions."* | Trust, through proof | Meetings |
| Objective | Engagement | Website Visits, Video Views | Conversions, Lead Gen |
| Budget share | 30 to 50% | 18 to 25% | 20 to 30% |
| Judged on | reach, engagement rate, **pool growth** | CTR, cost per engagement | cost per conversion |

## The retargeting pool is three groups, and two of them never clicked

The single most misread part of this. `full-funnel-framework.md`:

> *"Retargeting - video viewers (50%+) + website visitors + ad engagers from TOF"*

Somebody who watched half a video and scrolled on is warmer than most clickers, and is reachable.
Stage three narrows to **video viewers at 97%** and visitors of the pages only a serious buyer
opens. Windows, from `abm-retargeting-framework.md`: **90 days** nurture, **30 days** high intent,
**180 days** low-cost sustainer.

### The consequence for this skill's hero film

The 32-second film is built into the **landing page**, behind the click. The framework rates video
as *"High - builds retargeting pools efficiently"*. Behind the click it can only be seen by people
who already clicked, so it fills the smallest of the three pools. **Running the film as its own ad
set moves it in front of the click**, and everyone who watches half of it enters the pool without
clicking. Worth proposing on every build; it is not currently part of the default.

## Frequency and creative count, and do not mix the two sources up

`abm-retargeting-framework.md` gives **~4 impressions per person per week** at TOF and MOF, and
**3 to 4 rotating creatives** so that frequency stays productive. But read the scope: the variant
count is written for **retargeting and hot audiences**, and the rotation schedule is indexed by
audience temperature. The ABM fundamentals mandate **no creative count at cold**, only a frequency
ceiling, and put the weekly figure nearer **3**. The two documents differ slightly.

**So: one creative per account at cold is not a fault. Rotation becomes mandatory at stage two.**
Fatigue signals worth knowing: CTR down 20 to 30% from baseline, CPM up 30 to 40%, or roughly
**8 per week on a single creative**.

## The ads are one channel

`retargeting/ads-outbound-signaling-guide.md` describes ads as a **signal detection layer**:

> *"Ads create awareness -> Engagement reveals intent -> Intent triggers outbound -> Outbound is
> personalized by what they engaged with"*

His sequencing, which is the part clients get wrong:

| Weeks | What happens |
|---|---|
| 1 to 4 | **Ads only. No outbound at all.** Reaching an account that has only just seen your name is a cold approach with extra steps |
| 4 to 8 | Accounts reaching "Interested" get a person. Ads continue, now solution-oriented |
| 8 to 12 | Conversations. Ads turn to proof and case studies |

His handoff threshold is the **Interested** stage, roughly 5 clicks or 10 engagements, never
"Aware". And the rule that protects the relationship:

> *"Never say 'I saw you clicked our ad.' That's creepy. Reference the topic they showed interest
> in, not the channel."*

**Where this skill already has an advantage.** The hardest part of his pipeline is knowing who to
contact inside the account, which is why his architecture runs LinkedIn to Fibbler to HubSpot to
Slack. On UK public-sector accounts the **organogram names the buying committee for free**: name,
grade, title, unit, reporting line, phone, email. The outbound channel does not need buying, it
needs connecting. See `buying-committee-ladder.md`.

## The limit that bites this play hardest

> *"LinkedIn's API obfuscates engagement data if fewer than 3 members in an account engaged, or
> fewer than 3 total engagements/clicks in a timeframe."*

The upstream kit's claim, not independently verified against LinkedIn's documentation. If it holds it lands
directly on 1:1 ABM, where every audience is small on purpose. His three mitigations, all free:
group campaigns by **shared intent** so engagements roll up, read **30 or 90 day** windows rather
than 7, and aggregate at group level. Say this to the client **before** launch, not when the first
report looks thin.

---

> _Strategy & GTM research by Jean Mundabi Fala_

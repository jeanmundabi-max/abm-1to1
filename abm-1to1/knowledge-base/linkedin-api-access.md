# Getting LinkedIn API access

Everything this skill builds runs on the LinkedIn Marketing API. If the client has no
access, the play cannot start, and the wait is measured in weeks. **Ask at intake, on day
one, not when you are ready to build.**

## The one thing worth knowing first

**Development tier is enough to run 1:1 ABM. Do not wait for Standard.**

The Advertising API has two tiers. **Development** allows POST against **up to 5 ad
accounts** and GET against unlimited. A 1:1 ABM run uses **one** ad account with many ad
sets inside it, so Development covers it completely. **Standard** removes the account limit
and is what an ad-tech platform needs, not what this play needs.

That matters because Standard requires a screen recording of your platform creating and
optimising campaigns, and another review round. People wait months for access they did not
need.

## The path, in order

1. **A LinkedIn Page must exist.** The developer app has to be associated with one. If the
   client has no Page, that is step zero and it is quick.
2. **Create the app** at `linkedin.com/developers/apps/new`.
3. **Read the restricted use cases before applying.** Applications are rejected for a
   restricted use case, and a rejection costs another cycle. This is the step everyone skips.
4. **Apply to the product** under the app's **Products** tab. The one you want is the
   **Marketing Developer Platform**, and inside it the **Advertising API**.
5. **Complete the access form.** A clear use case, a privacy policy URL, and a description
   of the integration.
6. **Map the ad account to the app.** Copy the nine-digit **Account ID** from Campaign
   Manager, then in the Developer Portal go **Products → View Ad Accounts → Add Ad Account**.
   Missing this step is the most common reason a token that looks valid returns nothing.
7. **Generate a token** with the Token Generator in the Developer Portal, or the LinkedIn
   Marketing Solutions workspace on Postman. Check its life with the
   [Token Inspector](https://www.linkedin.com/developers/tools/oauth/token-inspector).

## How long it takes

**Approval is manual and LinkedIn does not publish a timeline.** Reported experience is
**four weeks at best, around four months on average**. Treat it as a lead time, not a task.

**So the intake question is not "do you have API access", it is "have you applied yet".**
If the answer is no and the engagement is live rather than a demo, that application is the
first thing that happens, in parallel with everything else. Nothing downstream is blocked
by it until the build step.

## Versioning will break you silently

The Marketing API is versioned by date, `li-lms-YYYY-MM`, and **old versions are sunset on
a published date**. Marketing version **202508 was sunset on 17 August 2026**. An
integration pinned to a dead version does not degrade, it stops.

Check the version in every request header at the start of a run, and check the migration
status page before assuming a 4xx is your bug.

## What to check on an inherited setup

Before trusting an account you did not set up:

- Token TTL and status, with the Token Inspector
- Which permissions the app actually holds, under the **Auth** tab
- Which ad accounts are mapped to the app, under **Products → View Ad Accounts**
- Which member roles exist on the ad account: `/adAccountUsers` answers this, and granting
  or revoking needs a token belonging to an `ACCOUNT_BILLING_ADMIN` or `ACCOUNT_MANAGER`
- The API version your code is pinned to, against the sunset schedule

## If they will not get access

Two honest options, and both should be said out loud rather than worked around:

- **Run it as a demonstration.** Everything except the build step works without API access:
  the account list, the evidence, the committee, the pages, the films, the creative. Only
  the DRAFT campaign needs the API. That is the whole of `sops/10-demonstration-and-ledgers.md`.
- **Run it on our ad account** and hand over the assets. This changes who the advertiser
  is, which is visible on the ad, and it is a layer question. See
  `sops/02-layers-and-account-list.md`.

Sources: LinkedIn's own [Marketing API quick start](https://learn.microsoft.com/en-us/linkedin/marketing/quick-start)
and [access tiers](https://learn.microsoft.com/en-us/linkedin/marketing/increasing-access),
read 2026-08-20, plus reported approval timelines from Phyllo's 2026 access guide.

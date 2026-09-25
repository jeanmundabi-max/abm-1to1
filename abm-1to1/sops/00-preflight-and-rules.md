# Preflight, and the rules that never bend

## What this skill adds to the upstream kit

The upstream kit assumes two things that do not exist at the start of a real engagement.
His README prerequisite 5 says it plainly: *"A landing page per account… you build
these separately; the pipeline just needs the URLs."* And his Step 1 starts from an
account list somebody already wrote.

So this skill supplies the front and the back that his kit does not:

| Missing in the upstream kit | Supplied here |
|---|---|
| Any onboarding or client intake | **Step 1** |
| Any way to decide which accounts belong | **Step 3**, gates derived from Step 1 |
| The landing pages | **Step 9** |
| A demonstrable output | **Step 13**, the walkthrough |
| A loop that stops mistakes repeating | **Step 14**, three ledgers |

Everything between Step 4 and Step 12 is the upstream kit's, wrapped.

---

---

## Rules that never bend

- **Everything DRAFT.** Never create ACTIVE. Never delete via API without a fresh
  human "CONFIRM DELETE".
- **Never fabricate.** Every word on the ad traces to a line on the landing page or
  to something the account published. This is the upstream kit's rule and the Observability
  Law saying the same thing.
- **Never sell an absence.** Not "they have no system", sell the screen you
  actually ran.
- **Never quote from the first source you find.** Walk the source ladder in Step 8
  and name the reporting entity and the as-at date beside every figure.
- **Band: >300 hard floor, 300-1,000 sweet spot**, <=1,200 fine, trim hard above
  2,000. Entry-level <=5%, ideally 0%.
- **No personalised name or logo ads in Germany.** Legal restriction, not policy.
  Check the account's geo before setting the ad set's.
- **Secrets only in `~/.config/abm-1to1/secrets.env`.**
- Copy: no em-dashes, no spaced hyphens, grade ~5, en-GB.
- **Every step carries a guardrail block.** The format is the upstream kit's: a failure that really
  happened, then the fix. Never a theoretical risk. If a step has no guardrail
  block, no one has run it yet, and that is worth saying out loud.

---

---

---

## Step 0. Preflight

**There is no minting script in this repo.** LinkedIn's OAuth flow is a browser
round-trip and a token is a credential, so this is deliberately a thing you do by hand
once. What you need:

1. A LinkedIn developer app with the **Advertising API** product granted. Approval is
   the long pole: four weeks at best, about four months typically. **Apply on day one of
   an engagement, not on build day.**
2. `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET` from that app, in secrets.env.
3. A redirect URL registered in the app's Auth tab, matching the one you authorise with.
4. Scopes `r_ads` and `rw_ads`. Without `rw_ads` everything up to part 7 still runs and
   only the campaign build defers.
5. The resulting token in `LINKEDIN_ACCESS_TOKEN`. It expires; check it before a build
   rather than halfway through one.

A two minute probe that tells you what the token can actually reach:

```bash
curl -s -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
     -H "LinkedIn-Version: 202609" -H "X-Restli-Protocol-Version: 2.0.0" \
     "https://api.linkedin.com/rest/adAccounts?q=search&count=10"
```

An HTTP 426 means the `LinkedIn-Version` you sent has been retired, not that the token
is dead. That distinction has cost a build.

The scripts read `~/.config/abm-1to1/secrets.env` directly. Nothing to symlink and
nothing to copy. A `.env` placed beside the scripts still wins if one exists, which
is the only way to point a single run at a different token.

`--check` reports what the token can reach. No ad account visible means the
research and page steps still run and only Step 11 defers. Say that out loud rather
than stalling.

### Guardrail

| Failure, really happened | Fix |
|---|---|
| A token came back able to see ad accounts it should not, one of them in a runnable state | `scripts/ad_account_guard.py` fails closed on any account that is not on your own allowlist, and it runs before Phase 1. **It was documented as wired into the build for a while before it actually was.** Ask whoever granted the access to remove it. The guard mitigates, it does not fix |
| A secret copied into a repo that has a public remote | Symlink `.env`, never copy |
| Token expiry not checked before a build | `--check` first, every time. A LinkedIn token expires and a build that starts on a dead one fails halfway |

---

---

# Four LinkedIn API traps, each of which cost a build

All four found live on the Revolut run, 2 and 3 September 2026. They were only in the
operator's private notes, which means they did not travel with the skill. They do now.

---

## 1. `locale` becomes `interfaceLocales`, server side, and must stay `en_US`

Setting the campaign's `locale` to the audience's country returns:

> `HTTP 400 INVALID_INTERFACE_LOCALE_CODE: Interface locale urn:li:locale:en_GB is not
> supported in Targeting Criteria`

**LinkedIn injects the campaign's `locale` field into `targetingCriteria` as
`interfaceLocales` and then validates it.** It is the member's **interface language**, not
their location. The location is already carried by `profileLocations`.

This failed **3 of 3 ad sets** on the first execute. SKILL.md previously said "set locale to
the audience's country", which is what caused it, and that line is now corrected.

## 2. The image upload URL is a different host, so strip the bearer token

`POST /images?action=initializeUpload` returns an `uploadUrl` on **`www.linkedin.com`** while
the API is on **`api.linkedin.com`**. Sending the API's `Authorization` header to that host
returns **HTTP 400 and an HTML error page**. Without the header: **201**, and the image
reaches `AVAILABLE`.

Same shape as any pre-signed URL: auth does not cross a host change.

## 3. `GET /posts` is 403 on a Development-tier token, so the verify is a false negative

`build_ad` creates the post, creates the creative, then reads the post back to confirm it
carries the destination, the CTA and the title. That read returns:

> `403 ACCESS_DENIED: Not enough permissions to access: partnerApiPostsExternal.GET`

The original code discarded the status code, so every post reported
`VERIFY FAILED - post missing fields: {all None}` **after the post and the creative had both
already been created**, and then returned `None` and threw their ids away. Three working ads
were recovered by listing creatives per campaign.

**A checker that cannot tell "unreadable" from "wrong" gets ignored.** It must say which.

## 5. The BODY COPY of a live post can be edited in place. The headline and the image cannot

Found 2026-09-08, and it changes the cost of every copy revision in this play.

Gotcha 4 says an unreviewed creative cannot be paused, so every revision is permanent. That is
true of a NEW creative. It is not true of the text.

```
POST /rest/posts/{urlencoded share urn}
X-RestLi-Method: PARTIAL_UPDATE
{"patch": {"$set": {"commentary": "the new body copy"}}}
                                                        -> 204 No Content
```

Three ad sets were rewritten this way and the creative count stayed at one each. No new
creative, nothing permanent, nothing to delete later.

**What is create-only, confirmed by a 422 on the same call:**

```
{"patch": {"content": {"media": {"$set": {"title": "..."}}}}}
  -> 422  /content/media/title :: CreateOnly field present in a partial_update request
```

So `content.media.title`, the headline bar under the image, and `content.media.id`, the image
itself, cannot be changed. Changing either means a new post and a new creative, which is
permanent.

**The rule that follows.** Get the headline and the image right before the first push, because
those two are the expensive fields. The body copy is cheap and can be iterated on a live draft
as many times as you like. Write the intake and the creative review around that asymmetry.

**And you cannot read your work back.** `GET /posts` is 403 on this tier, per gotcha 3, so a 204
is the only confirmation you get. Say that plainly rather than claiming the copy is verified: the
operator has to look at the preview.

## 4. An unreviewed creative cannot be paused, so every revision is permanent

> `/Creative/status transition is not allowed from ACTIVE to PAUSED if
> /Creative/review/reviewStatus is not set to APPROVED.`

Nothing has run, so nothing has been reviewed, so nothing can be paused. `DRAFT`, `PAUSED`
and `ARCHIVED` are all refused and `CANCELLED` is not an enum value. **The only route is
DELETE, which needs a fresh human CONFIRM DELETE.**

And the image cannot be swapped on an existing post either:

> `422: /content/article/thumbnail :: CreateOnly field present in a partial_update request`

**So every creative revision is a new post plus a new creative that can never be removed
without a deletion.** Three rounds of revision left nine creatives on three ad sets.

**The rule that follows: get the card right before the first push.** Run the creative council
on the card and the offer temperature check on the offer *before* anything is created, not
after the third rejection.

---

_Strategy & GTM research by Jean Mundabi Fala_

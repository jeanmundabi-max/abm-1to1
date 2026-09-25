# The two layers, and building the account list

## Step 2. The two layers. Everything downstream depends on this.

| | Layer 1 | Layer 2 |
|---|---|---|
| Who advertises | MDB | The client |
| Who is targeted | the client's staff | the client's target accounts |
| Whose brand is on the page | MDB's, or neutral | **the client's** |
| What the page sells | MDB's work | **the client's own products** |
| Whose commercial terms | MDB's | **the client's, and not ours to write** |
| Who signs off the copy | Jean | the client |

**The trap.** On the GoCardless build, layer 2 ad sets posted from MDB Growth
Capital's page, with commentary in our own first person, landing on pages branded as
GoCardless's. If those ever ran, a Gym Group employee would see MDB's name on the ad
and GoCardless's brand on the page.

In a **demo** that is fine, because nothing runs and the ad account is only a
sandbox. Say it out loud in the walkthrough: *in production this posts from the
client's page.* In a **live** layer 2 build it is not fine and the page must carry
the client's own advertiser identity.

**Never write a commercial offer for layer 2.** The price, the terms and the product
claims belong to the client. If a layer 2 page seems to need an offer, either the
client supplies it or the page carries a clearly marked specimen slot.

### Guardrail

| Failure, really happened | Fix |
|---|---|
| Spent three days trying to write GoCardless's offer to its own prospects | Layer 2 offers are the client's. Ours is layer 1 only |
| Built five layer 2 pages before anyone decided the layer | Step 1 question 1 |

---

---

## Step 3. Build the account list

The upstream kit starts from a list. On a real engagement there is none. Build it from the four
gates derived in Step 1d.

### The gates

1. **The client's product surface exists at this account, at scale.** Derived, not
   generic. For GoCardless: recurring collection in sterling, monthly.
2. **300+ addressable staff on LinkedIn**, or the ad set will not deliver at all.
   This is LinkedIn's floor, not a preference.
3. **The account publishes, and you know which ladder reaches it.** Listed, bonded,
   regulated or foreign-owned puts it on the corporate-disclosure ladder. A public body
   puts it on the procurement ladder. Neither is better; they are different rungs to
   climb, and Step 8 holds both. An account whose ladder you cannot name is not a hard
   account, it is an **unresearched** one. An account that reaches only the bottom rung
   gives numbers with no voice, which is a known cost, not a blocker.
4. **The pain is visible in public evidence: dated, named, and published by a party
   that had to publish it.** Not inferred. What that evidence looks like depends on the
   ladder, so do not go looking for one shape. On the corporate ladder it is a
   receivable, a provision, an ageing, a write-off, a named line or a funded programme.
   On the procurement ladder it is a contract, its value and its expiry date. **Write
   what it is for THIS client before you start looking**, or you will find the shape you
   already had in mind.

Plus one composition rule: **do not fill the list with one vertical.** Five accounts
in the same sector demonstrates one sector, not a method.

### Order of operations, cheapest first

Gate 2 is a single API call and kills candidates fastest. Gate 3 is a URL probe.
Gate 4 is the expensive one. Run them 2, 3, 4, 1.

```bash
cd "$HOME/.claude/skills/abm-1to1/scripts"
python3 resolve_and_size.py --in candidates.csv --out sized.csv --region urn:li:geo:101165590
```

### The three verdicts, and they are not the same

- **IN.** All four gates.
- **BENCH.** Gates 1 to 3 pass, gate 4 unscreened or the account has a blocking
  corporate event. Domestic & General cleared 1 to 3 and went to bench because its
  own FY26 report announced an acquisition by Asurion. **An in-flight acquisition
  freezes vendor decisions.**
- **OUT.** Gate 4 fails on evidence. Gousto has **zero trade receivables** because it
  charges at the order cut-off, so there is no uncollected billing to show, however
  large the company is.

Record all three. The bench is what you draw from when an account is dropped later,
and it will be.

### Guardrail

| Failure, really happened | Fix |
|---|---|
| Five accounts picked from intuition, then researched. Two failed gate 4 after their pages were already built and live | Gates before build, always. Cheapest gate first |
| An account written off as "publishes nothing" because its obvious entity files reduced accounts | Walk up to the group parent. Gousto's audited group accounts sit at a different company number |
| An account written off as stale on its Companies House filing | Check what the regulator compels. Zego's SFCR covered a year Companies House did not hold |
| Read `disclosure depth` as `company size` | Gousto turns over £342.9m and publishes no interims, because it is private with no listed debt. Silence is not smallness |
| Nearly shipped a five-account demo with three gyms in it | The composition rule. Five verticals demonstrate a method, one vertical demonstrates a sector |

---

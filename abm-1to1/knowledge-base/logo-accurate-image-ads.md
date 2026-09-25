# Getting a real logo into a generated ad

An image model asked for "the Chewy logo" draws something Chewy-shaped and wrong. On a 1:1
ABM card the target's mark is the whole personalisation, so wrong is worse than absent.

**The fix is the edit endpoint, not a better prompt.** Post the real PNGs as references and
tell the model to reproduce, not redraw.

```python
files = [
    ("image[]", ("advertiser-logo.png", open(LOGO, "rb"), "image/png")),
    ("image[]", ("account-icon.png",    open(ICON, "rb"), "image/png")),
]
data = {"model": "gpt-image-2", "prompt": PROMPT,
        "size": "1024x1024", "quality": "high", "n": "1"}
r = requests.post("https://api.openai.com/v1/images/edits",
                  headers={"Authorization": f"Bearer {KEY}"}, files=files, data=data,
                  timeout=1200)
out.write_bytes(base64.b64decode(r.json()["data"][0]["b64_json"]))
```

What makes it hold:

- **Number the references in the prompt** and say what each one is. "Image 1 is the
  advertiser logo. Image 2 is the {COMPANY} brand icon."
- **Say reproduce exactly, do NOT redraw, recolor, or restyle**, once per image. Without it
  the model restyles both to match the canvas.
- **Name the tiers by pixel height and give each a hex colour.** A layout described as prose
  comes back as one uniform block of text. Sizes are the hierarchy.
- **List what must not appear.** No badge, pill, watermark, chart, person, extra caption. The
  model fills whitespace unless told the whitespace is deliberate.
- Render accounts **in parallel**; each call is slow enough that serial is painful.

## When not to use it

This is the exception, not the route. The default is HTML plus a headless-Chrome screenshot
at 1200x1200, because it is free, deterministic, and re-renders in a second when a figure
changes. An image model cannot reproduce its own output, so a one-word copy change means a
new card that does not match the set.

**Never put a measured number inside a generated image.** You cannot diff it, and a figure
that drifted in generation reads to the buyer as a measurement of them. The Serval set had
every fabricated counter stripped for exactly this reason (`../sops/08-the-creative.md`).

Related: `../sops/08-the-creative.md`, and [the upstream ad-copywriting guide](https://github.com/swan-gtm/gtm-skills/blob/main/skills/ivan-falco/ad-copywriting/SKILL.md).

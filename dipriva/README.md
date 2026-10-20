# Dipriva standards for /brag

Everything a /brag run needs to produce a Dipriva-grade video. The rules mirror the `dipriva-brand` skill and the content gate in the private dipriva-social repository.

## Files

| File | Purpose |
|---|---|
| `brand.json` | Voice, palette, fonts, approved calls to action, allowed proof points, banned words, engagement bait and hedge words. |
| `check-copy.mjs` | Checks share copy, plans and composition HTML against `brand.json`. Exit code 1 on any error. |

```bash
node dipriva/check-copy.mjs showcase/dipriva-social
```

## Standard

| Area | Standard |
|---|---|
| Tone | Confident agency product demo. Understated and precise. No startup hype. |
| Headlines | Verb + object + strategic modifier. Title Case, no period. Example: "Eliminate Off-Brand Copy in Code". |
| Palette | Navy `#2F4059`, cream `#F5F5DC`, sand `#E8E4D9`. Brick `#C8553D` only for a rejection state. |
| Type | Playfair Display headlines, Inter body. Shipped locally under the SIL Open Font License. |
| Format | 1080 x 1920, 30 fps, 15 to 25 seconds, for Reels, TikTok and Shorts. Text stays inside the reel safe zone: 96 px left, 160 px right, 260 px top, 460 px bottom. |
| Proof | Show the real product: real renders, real tool output. Mockups of platform screens carry no platform logos and no invented counts. |
| Claims | Only the proof points in `brand.json`. Product facts (for example "12-hour veto window") must be true in the shipped product. |
| Call to action | One approved entry from `brand.json`, word for word, held on screen long enough to read the address. |
| Sound | Original synthesized music, no samples. Effects pitched to the key and mixed under the music. About -16 LUFS integrated, -1 dBTP peak. |
| Share copy | 1 to 3 sentences, declarative, ends with the call to action. No hashtags unless asked (max 3). |

## Pre-post checklist

- [ ] `node dipriva/check-copy.mjs <folder>` passes.
- [ ] Every figure is a proof point, an approved firm figure or a true product setting.
- [ ] Every platform named can actually do what the video shows today.
- [ ] Spanish copy read by a native speaker.
- [ ] Poster frame is a settled frame, baked in as frame 0.
- [ ] Posting with the platform's own AI label.

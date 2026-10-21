# Dipriva Social: brag plan

**Format:** 1080 x 1920, 30 fps, 25.0 s, no voiceover. Music and soft effects only.
**Tone:** confident agency product demo, understated and precise. Few scenes, long holds, clean wipes, no hype.

## Rubric

| Question | Answer |
|---|---|
| What is it | A content engine that turns one brief into gated, rendered, approved Facebook and Instagram posts and publishes them on schedule. |
| Who is it for | Owners of 10 to 500 person companies who want a steady social presence without handing their brand to a freelancer. |
| What sets it apart | Code rejects off-brand copy before a person sees it, and nothing publishes without a passing verdict. |
| Strongest claim | "Nothing Posts Without Approval." True in the shipped product. |
| Visual hook | An idea typed into a laptop, then a real `FAIL` from the real content gate. |
| Call to action | "Book a free 30-minute strategy session", dipriva.com/schedule (approved wording). |

## Source material

- Brief idea, post images and gate output come from the real product. The gate output on screen is verbatim from a run on a draft with one banned word and one em dash added on purpose.
- Spanish draft cards: written for this video in formal "usted" and passed by the same gate.
- Music: original, synthesized in Python on D, B minor, G, A at 96 BPM, the progression the product uses for its own Stories. No samples.
- Ledger rows and the veto-window bar are illustrative UI, not a real batch.
- No client names, numbers, logos or testimonials. No proof-point figures are used.

## Storyboard

| # | Time | Scene | On-screen copy | Sound |
|---|---|---|---|---|
| 1 | 0.0 to 3.75 | Navy. Laptop; the idea types into a "New brief" window, chips Facebook, Instagram, EN + ES. | "Brief One Idea" / "Type it once. The engine does the rest." | Pad, soft key ticks. |
| 2 | 3.75 to 7.5 | Cream. Four draft cards: Facebook and Instagram feed carousels and Stories. EN to ES toggle. | "Draft Every Meta Format" / "In English and Spanish." | Bass and marimba enter on the bar. |
| 3 | 7.5 to 12.5 | Navy. Real gate output, REJECTED stamp. | "Eliminate Off-Brand Copy in Code" | Arpeggio breathes out, low thud on the stamp. |
| 4 | 12.5 to 16.875 | Cream. Two phones: Dipriva's own Facebook Page post and Instagram post, real renders, "Published via Graph API". | "Publish to Facebook and Instagram" | Posts land, two soft chimes. |
| 5 | 16.875 to 20.625 | Navy. Checks, veto window bar, ledger with the duplicate skipped. | "Nothing Posts Without Approval" | Three chimes, ledger ticks. |
| 6 | 20.625 to 25.0 | Cream. Call to action card. | "Engineer Your Content System" / "Dipriva builds and runs this engine for your business." / "Book a free 30-minute strategy session" / "dipriva.com/schedule" / "Official Meta APIs only. No scraping." | D major resolve, bell on the card. |

Cuts land on the 96 BPM beat grid. Phone screens are neutral feed mockups: no Meta logos, Dipriva's own Page name, handle and profile image, no like or follower counts.

## Copy rules check

`node dipriva/check-copy.mjs showcase/dipriva-social` passes. Exception by design: the scene 3 draft line and the gate output quoting it contain a banned word and an em dash because they are the rejected example. They sit between brand-exempt markers in `composition/index.html` and appear struck through under a REJECTED stamp.

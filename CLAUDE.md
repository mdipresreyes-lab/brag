# brag (Dipriva fork): project context for Claude Code

Fork of [latent-spaces/brag](https://github.com/latent-spaces/brag), kept by Dipriva Consulting Group (owner: Manuel Dipres) to make launch and sales videos for Dipriva products. **This repository is public.** Never commit secrets, client data, lead data, internal hostnames or anything from a private Dipriva repo that is not already shown in a published video.

## How this fork is organized

| Path | Owner | Rule |
|---|---|---|
| `skills/`, `.claude/skills/`, `scripts/`, `docs/`, `examples/`, root `README.md` | Upstream | Keep verbatim so upstream updates merge cleanly. Do not apply Dipriva style edits here. |
| `CLAUDE.md`, `dipriva/` | Dipriva | The Dipriva standards. All Dipriva rules below apply. |
| `showcase/<product>/` | Dipriva | One folder per finished Dipriva video. All Dipriva rules below apply. |

## Running /brag for a Dipriva product

1. Read `dipriva/README.md` and `dipriva/brand.json` before planning. They override /brag's tone presets and visual defaults.
2. Plan with Dipriva voice: professional, direct, authoritative, strategic. Headlines follow verb + object + modifier, Title Case, no period.
3. Visuals: navy `#2F4059`, cream `#F5F5DC`, sand `#E8E4D9`. Playfair Display headlines, Inter body, fonts shipped locally (never a CDN). Brick `#C8553D` only for a rejection or failure state.
4. Claims: only the proof points in `dipriva/brand.json`. No invented numbers, logos, testimonials or client names.
5. End on an approved call to action from `brand.json` (`callsToAction`), word for word, with its page.
6. Before delivery, run `node dipriva/check-copy.mjs <output-dir>` and fix every error. A deliberate rejected example goes between `<!-- brand-exempt:start -->` and `<!-- brand-exempt:end -->`.
7. Save the finished video in `showcase/<product>/` (see the existing folder for the layout). `brag-output*/` and `renders/` stay ignored.

## Rules to always follow (Dipriva files)

- **No em dashes, ever.** In copy, docs, code comments and replies. Code that detects dashes writes them as unicode escapes.
<!-- brand-exempt:start (the rule list names the words it bans) -->
- **Banned words** (list in `dipriva/brand.json`): leverage, synergy, holistic, empower, journey, ecosystem, game-changer, innovative, cutting-edge, passionate, dynamic, solution provider, and their Spanish forms.
- **No engagement bait** ("DM me", "comment YES", "link in bio"). Max 3 hashtags. No emoji. Close with a statement.
<!-- brand-exempt:end -->
- **Official APIs only** is a selling point. Say it plainly.
- **No AI notice burned into a video.** Manuel uses each platform's own AI label when posting.
- **Languages:** social video copy is English. Spanish appears only as a shown product capability, in professional business Spanish (formal usted).
- **Commits:** stage files by explicit path, never `git add -A`. Push only when Manuel asks.

# Dipriva Social: sales video

A 25-second vertical video that shows prospective Dipriva clients the engine that would run their Facebook and Instagram content: brief, draft, gate, publish, approve. It ends on the approved call to action, "Book a free 30-minute strategy session" at dipriva.com/schedule.

| File | What it is |
|---|---|
| `brag.mp4` | Final video. 1080 x 1920, 30 fps, 25.0 s, H.264 and AAC, about -15 LUFS. Poster baked in as frame 0. |
| `brag.jpg` | Poster: the content gate rejecting a draft. |
| `share-copy.txt` | General share copy. |
| `caption-instagram.txt` | Instagram Reel caption. No link (Instagram captions are not clickable); the address is on the final frame. |
| `caption-facebook.txt` | Facebook Reel caption with the clickable booking link. |
| `brag-plan.md` | Angle, sources and storyboard. |
| `composition/` | Source: `index.html` (every frame is a pure function of time), `score.py` (original score), `capture.mjs` (frame capture), local fonts and media. |

## Rebuild

```bash
cd showcase/dipriva-social/composition
node capture.mjs frames                    # 750 PNG frames
python3 score.py score.wav                 # needs numpy
ffmpeg -framerate 30 -i frames/f%04d.png -i score.wav \
  -c:v libx264 -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest brag.mp4
```

To bake the poster, copy the chosen frame over `frames/f0000.png` before encoding (this cut uses `f0360.png`).

## Notes

- Real material: the brief text, the gate's error output and the post images come from the dipriva-social repository. The phone screens are neutral mockups of Dipriva's own Facebook Page and Instagram account.
- Publishing to a client's own Meta accounts needs Meta app review before it can be offered.

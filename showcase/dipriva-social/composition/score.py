# Original score for the Dipriva Social brag video. Same progression and tempo
# as the repo's "steady" Story bed (src/music/synth.ts): D, Bm, G, A at 96 BPM.
# Effects are pitched to the key and mixed under the music. No samples.
import numpy as np
import wave
import sys

SR = 48000
DUR = 25.0
BEAT = 60 / 96
BAR = BEAT * 4
N = int(DUR * SR)
rng = np.random.default_rng(7)
L = np.zeros(N)
R = np.zeros(N)

CHORDS = [[62, 66, 69], [59, 62, 66], [55, 59, 62], [57, 61, 64]]  # D, Bm, G, A
hz = lambda m: 440 * 2 ** ((m - 69) / 12)


def add(start, sig, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    l = np.cos((pan + 1) * np.pi / 4) * np.sqrt(2)
    r = np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
    L[i:i + len(sig)] += sig * gain * l
    R[i:i + len(sig)] += sig * gain * r


def env(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def pad_note(m, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(m)
    s = sum(np.sin(2 * np.pi * f * d * t + p) for d, p in [(1, 0), (1.003, 1.1), (0.997, 2.3)]) / 3
    s += 0.18 * np.sin(2 * np.pi * 2 * f * t)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.5)
    return s * np.clip(a, 0, 1)


def marimba(m, dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.18) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.03)
    return s * np.minimum(1, t / 0.003)


def bass(m, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * 2 * f * t)
    return s * np.minimum(1, t / 0.01) * np.exp(-t / 0.5) * np.minimum(1, (dur - t) / 0.05).clip(0, 1)


def bell(m, dur=2.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.9) + 0.35 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t / 0.25)
    return s * np.minimum(1, t / 0.004)


def noise_swell(dur, cutoff):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = lowpass(rng.standard_normal(n), cutoff)
    e = np.sin(np.pi * t / dur) ** 2
    return x * e / (np.abs(x).max() + 1e-9)


def tick(cutoff=4000, dur=0.025):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n) * np.exp(-t / 0.004)
    return lowpass(x, cutoff)


def chord_at(t):
    return CHORDS[int(t // BAR) % 4]


END = 20.625  # end card downbeat

# Pad: whole piece, chord per bar, resolves to D on the end card.
bar = 0
while bar * BAR < DUR:
    s = bar * BAR
    if s >= END:
        break
    for j, m in enumerate(chord_at(s)):
        add(s, pad_note(m - 12, BAR + 0.4), 0.055, (-0.4, 0.0, 0.4)[j])
    bar += 1
for j, m in enumerate([50, 57, 62, 66]):
    add(END, pad_note(m, DUR - END), 0.06, (-0.4, -0.1, 0.1, 0.4)[j])

# Bass from scene 2, on beats 1 and 3.
t = 3.75
while t < END - 1e-6:
    root = chord_at(t)[0] - 24
    add(t, bass(root, BEAT * 1.8), 0.16)
    t += BEAT * 2
add(END, bass(38, 3.0), 0.16)

# Marimba arpeggio in eighths from scene 2. It breathes out before the stamp.
t = 3.75
k = 0
while t < END - 1e-6:
    if not (9.4 <= t < 10.625):
        c = chord_at(t)
        pattern = [c[0], c[1], c[2], c[1] + 12, c[2], c[1], c[0] + 12, c[2]]
        g = 0.07 if k % 2 == 0 else 0.05
        add(t, marimba(pattern[k % 8]), g, -0.3 if k % 2 else 0.3)
    t += BEAT / 2
    k += 1

# Soft shaker on the off-beats from scene 3.
t = 7.5 + BEAT / 2
while t < END - 1e-6:
    if not (9.4 <= t < 10.625):
        add(t, tick(7000, 0.04), 0.03, 0.2)
    t += BEAT

# ---- effects, timed to the picture
# Scene 1: typing, very quiet.
t = 0.8
while t < 2.6:
    add(t, tick(3000), 0.035, rng.uniform(-0.2, 0.2))
    t += rng.uniform(0.05, 0.09)
for at, m in [(2.65, 74), (2.77, 78), (2.89, 81)]:
    add(at, marimba(m, 0.3), 0.05)
# Scene 2: cards deal, toggle.
for at in [4.25, 4.40, 4.55, 4.70]:
    add(at - 0.12, noise_swell(0.3, 1800), 0.03, rng.uniform(-0.3, 0.3))
add(5.6, tick(2500, 0.03), 0.08)
add(5.6, marimba(81, 0.3), 0.05)
# Scene 3: command typing, error lines, the stamp.
t = 8.1
while t < 8.6:
    add(t, tick(3000), 0.035)
    t += rng.uniform(0.04, 0.07)
for at in [9.45, 9.75, 10.05]:
    add(at, marimba(57, 0.25), 0.05)
thud_n = int(1.2 * SR)
tt = np.arange(thud_n) / SR
f = 73.4 * (1 + 0.6 * np.exp(-tt / 0.03))
thud = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.28) * np.minimum(1, tt / 0.002)
add(10.70, thud, 0.32)
add(10.70, lowpass(rng.standard_normal(int(0.12 * SR)) * np.exp(-np.arange(int(0.12 * SR)) / SR / 0.02), 900), 0.12)
# Scene 4: phones rise, posts land, published toasts.
for at in [12.9, 13.05]:
    add(at - 0.1, noise_swell(0.4, 2000), 0.03, rng.uniform(-0.3, 0.3))
for at, m in [(13.5, 74), (13.7, 78)]:
    add(at, marimba(m, 0.3), 0.05)
for at, m in [(14.1, 86), (14.3, 90)]:
    add(at, bell(m, 1.0), 0.03)
# Scene 5: three checks, ledger rows.
for at, m in [(17.35, 81), (17.57, 86), (17.79, 90)]:
    add(at + 0.1, bell(m, 1.2), 0.035)
for at, m in [(18.7, 74), (19.0, 74), (19.3, 69)]:
    add(at, marimba(m, 0.25), 0.04)
# End card.
for m in [74, 78, 81]:
    add(END + 0.2, bell(m, 3.0), 0.03)
for m in [86, 90]:
    add(21.45, bell(m, 2.0), 0.03)

# Master: fades, gentle saturation, normalize.
mix = np.stack([L, R], axis=1)
fade_in = np.minimum(1, np.arange(N) / (0.25 * SR))
fade_out = np.clip((DUR - np.arange(N) / SR) / 1.2, 0, 1)
mix *= (fade_in * fade_out)[:, None]
mix = np.tanh(mix * 1.4) / 1.4
mix /= np.abs(mix).max() / 0.89
out = (mix * 32767).astype(np.int16)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(out.tobytes())
print('ok', DUR)

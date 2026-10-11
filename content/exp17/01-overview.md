---
title: Overview
nav: Overview
lead: Turn the pipeline around. Take a video the model generated, pull its pose out, keep five keyframes, and let a motion model fill in between them. Is that better 3D animation than the video's own pose?
---

## The goal

Every experiment so far ended by lifting the video's pose with GVHMR. This one asks
whether a **motion model** can turn that into cleaner animation. It takes five keyframes
from the lifted pose and lets **CondMDI** generate the motion between them. No new video
is generated.

Two kinds of source video from Exp 15 are compared:

- **text-only video:** Exp 15's `text only`, the prompt with no control.
- **skeleton-controlled video:** Exp 15's `hand · trunk`, the full loop of MotionGPT3
  → video model → motion model.

For each prompt, the best of the three seeds was used, with the same seed for both
sources.

## Setup

- **Source:** 12 prompts × 2 source videos = 24 motions, lifted with GVHMR.
- **Keyframes:** five, evenly spaced (0·40·88·128·168), taken from the lift.
- **Motion model:** CondMDI. Every result is fitted to SMPL and rendered on the
  neutral body.

| method | what it does |
|---|---|
| `GVHMR lift` | the video's own pose on every frame — the baseline |
| `lift, smoothed` | the lift with light Savitzky–Golay smoothing (9 frames) |
| `blend` | a straight line between the 5 keyframes |
| `CondMDI` | the motion model fills in between the 5 keyframes, no text |
| `CondMDI + text` | the same, plus the prompt |

## What came out

::: key
- **CondMDI is not cleaner by the numbers.** Its foot skate is higher than the lift's
  (154 vs 122 mm/s) and its jerk is the same.
- **Light smoothing is cheaper and better.** It cuts jerk from 106 to 28 and stays
  within 1 mm of the lift.
- **CondMDI's value is robustness.** It looks natural on 24 of 24 motions against the
  lift's 22. It repairs broken lifts, though on `climb_ladder` it loses the climb
  itself. The blend is worst: natural on only 4 of 24.
- **Adding the prompt to CondMDI changes nothing.** What the motion means is decided
  by the source video: the action is there on 9 of 12 text-only sources and 5 of 12
  skeleton-controlled ones.
- **Best route:** text-only video → GVHMR lift → light smoothing.
:::

[Results →](results.html)

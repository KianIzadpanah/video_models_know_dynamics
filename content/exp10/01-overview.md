---
title: Overview
nav: Overview
lead: The first experiment with a genuinely broken input. Take a flawed text-to-motion clip, keep its skeleton on only K frames, and let the video model redraw the bad frames in between.
---

## The goal

Experiments 6–9 used clean motion capture as the input. Here the input is
**MotionGPT3's** output for a text prompt, with all of its natural errors.

The idea is that sparsity does not improve the frames that are kept. It **throws away
the bad frames in between** and lets the video prior redraw them. So the question is
whether what comes back is a better motion than what went in.

## Setup

- **Input:** MotionGPT3 (text-to-motion), fitted to SMPL, 169 frames @ 25 fps. Twelve
  prompts in three tiers: easy, medium, hard.
- **Control:** a DWPose skeleton on the K anchor frames, black elsewhere.
- **Video model:** LTX-2.3 22B distilled + Union-Control IC-LoRA, 768×768.
- **Recovery:** GVHMR, re-rendered on a neutral SMPL body.
- **Blend baseline:** straight-line interpolation between the same anchors, with no
  model.

| condition | anchor frames |
|---|---|
| `K = all` | all 22 latent frames — 0·8·16·…·168 |
| `K = 8` | 0·24·48·72·96·120·144·168 |
| `K = 5` | 0·40·88·128·168 |
| `K = 3` | 0·88·168 |
| `K = 2` | 0·168 — the two ends |

::: clips arms=input,ctrl_Kall,ctrl_K5,ctrl_K3,ctrl_K2 ids=jump seeds=1234
`jump`'s airborne frame is f24, and no uniform schedule at `K = 5` or below contains it.
:::

## What came out

::: key
- **Refinement in 8 of 12 motions, most often at `K = 5`.** `sit_down`, `stand_up`,
  `wave` and `walk` improve at every K.
- **The chair.** In the input, `sit_down` and `stand_up` sit on nothing. The video
  puts a real chair under the person at every K.
- **The model beats the blend** on jerk and foot skate at every K, and departs from
  the input smoothly as K drops. There is no sudden cliff.
- **`jump` is a sampling failure.** The anchors miss its airborne frame, so the jump
  disappears. `run` turns into a walk, and `throw` becomes a baseball swing with an
  invented bat.
:::

[Photoreal outputs →](photoreal.html) · [Recovered motion and blend →](recovered.html)

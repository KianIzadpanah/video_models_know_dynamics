---
title: Overview
nav: Overview
lead: Swap Experiment 6's depth map for a skeleton on every frame. A skeleton gives where the joints are and nothing about the surface, so the appearance has to come from the prompt. Then release the control part-way through denoising to see whether the model takes the extra freedom.
---

## The goal

Experiment 6 used a **depth render** as the control. This one asks two things:

1. Does a **DWPose skeleton** on every frame keep the pose as well as depth does, while
   leaving the look of the person to the prompt?
2. Does **releasing the control early** in denoising (timestep truncation) give the
   model room to change the motion while it keeps the pose?

Earlier experiments loosened control *in time* by keeping only some frames. This one
keeps every frame and loosens *how much* each frame specifies.

## Setup

- **Input:** nine AMASS/BABEL motion-capture clips, 169 frames @ 25 fps (the Exp 6 set).
- **Control:** a DWPose skeleton taken from a render of the input mesh. The `depth`
  column uses a depth render as the reference.
- **Video model:** LTX-2.3 22B distilled + Union-Control IC-LoRA, 768×768, 8 denoising
  steps where the control acts.
- **Recovery:** GVHMR, re-rendered on a neutral SMPL body.

| condition | what the model gets |
|---|---|
| `depth` | depth render on every frame, control on all 8 steps — reproduces Exp 6 |
| `skeleton 100%` | skeleton on every frame, control on all 8 steps |
| `skeleton 58%` | control released after step 7 of 8 (57.8% denoised) |
| `skeleton 28%` | control released after step 6 of 8 (27.5% denoised) |
| `skeleton 9%` | control released after step 5 of 8 (9.1% denoised) |

The two controls, for one clip:

::: clips arms=input,ctrl_skel,ctrl_depth ids=squat seeds=1234 size=lg
:::

## What came out

::: key
- **Every clip is photoreal, including `depth`.** The "mannequin" look from Exp 6 did
  not come back. Exp 6 paired a 19B adapter with a 22B base, while this run uses a
  matched adapter, so the mismatch was probably the cause.
- **Pose follows the skeleton at every cutoff, even 9%.** Releasing control earlier
  changes the picture more each time, but only at `9%` does the clip become a
  visibly different take.
- **`kick` is the one case where looser control was more faithful.** At `9%` it
  comes back closest to the input (713 mm against 1092 mm at `100%`).
- **`run` walks in every condition.** The input clip is itself a fast walk.
:::

[Photoreal outputs →](photoreal.html) · [Recovered motion →](recovered.html)

## Every clip

One page per motion, with every condition and every seed — the control, the photoreal output, the recovered motion:

[squat](clips-squat.html) · [walk](clips-walk.html) · [run](clips-run.html) · [jump](clips-jump.html) · [kick](clips-kick.html) · [stand_up](clips-stand-up.html) · [throw](clips-throw.html) · [turn](clips-turn.html) · [wave](clips-wave.html)

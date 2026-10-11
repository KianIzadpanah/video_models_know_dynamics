---
title: Overview
nav: Overview
lead: Exp 12's outputs followed their keyframes too loosely. Keep the same keyframes and change how the control video is drawn, so the model attends to it.
---

## The goal

There are two reasons why single keyframes on a black background are weak:

- **Black frames say "no person here"**, rather than "anything goes".
- **The video VAE packs 8 frames into one latent**, so a single-frame keyframe reaches
  the model at about ⅛ strength. That applies to `K = all` as well: a truly dense
  control, on all 169 frames, had never been run.

So this experiment changes **how the control is drawn, not which frames are chosen**.
Every condition uses Exp 12's entropy keyframes. The principle being tested is to
loosen *what* you specify rather than *how often* you specify it.

## Setup

- **Input:** the 24 MotionGPT3 clips from Exp 12, with Exp 12's entropy keyframes.
- **Video model:** LTX-2.3 22B distilled + Union-Control IC-LoRA, 768×768. Recovery
  with GVHMR.

| condition | what the control video holds |
|---|---|
| `text only` | nothing |
| `K5 single` | 5 single skeleton frames, black between (Exp 12's `entropy`) |
| `K5 hold` | each keyframe pose frozen across its whole 8-frame latent group |
| `K5 chunk` | the real poses across each keyframe's 8-frame group |
| `trunk + K5` | head, shoulders and hips on every frame, full skeleton on the 5 keyframes |
| `trunk only` | head, shoulders and hips on every frame, no keyframes |
| `K = all` | 22 grid frames, black between |
| `dense 1.0 / 0.6 / 0.4` | full skeleton on all 169 frames, at three strengths |
| `dense, early` | full skeleton on all frames, only in the first 3 of 8 steps |

How the control videos differ, for `jump`:

::: clips arms=ctrl_K5_single,ctrl_K5_hold,ctrl_K5_chunk,ctrl_trunk_K5,ctrl_dense_s10 ids=jump seeds=1234
:::

## What came out

::: key
- **Dense control is followed most closely.** Keyframe error is 64–69 mm, and
  lowering the strength barely loosens it. It also tends to move the person into a
  studio or onto a stage.
- **`trunk + K5` gives the best balance.** It has the least foot skate of any
  keyframed condition and natural motion between the keyframes. It struggles with
  free-limb actions: `kick` becomes a knee lift.
- **Holding the keyframe across its latent group helps a little.** `K5 hold` beats
  `K5 single` on 18 of 24 clips, but only by 8 mm, and it freezes the motion inside
  each group.
- **No control repairs a wrong movement.** On `push_door`, `step_up` and `run`,
  following more closely copies the input's error, and `text only` does better.
:::

[Photoreal outputs →](photoreal.html) · [More conditions →](more-conditions.html) · [Recovered motion →](recovered.html)

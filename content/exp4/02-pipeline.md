---
title: Pipeline
nav: Pipeline
lead: Five stages, and three settings that deliberately differ from the earlier experiments. The motions are reused unchanged, so the only thing that varies is how much of the pose is specified.
---

## The five stages

| stage | what happens | output |
|---|---|---|
| 1 | **Motion** — reused from Experiments 1–3, not regenerated | SMPL, resampled to 121 frames @ 25 fps |
| 2 | **Depth render** — the SMPL animation as a depth video | 121 frames, 704×704 — this is the *control*, never the appearance target |
| 3 | **Generation** — depth control + text prompt | a photorealistic video, 121 frames |
| 4 | **Recovery** — GVHMR on the photoreal video | SMPL-X, world-grounded, 25 fps |
| 5 | **Re-render** — recovered motion as the neutral body | comparable with stage 1 |

Stages 2 and 5 come out of **byte-identical render code**, hash-checked at run time
against [Experiment 1's](../exp1/provenance.html). Same neutral SMPL body with
`betas = 0`, same fixed camera, same grounding. If the two ends were rendered
differently the comparison would be between renderers rather than motions.

## The control track

The depth video is the whole mechanism, so it is worth being precise about it.

- On a **conditioned** frame it is the full-body depth render.
- On a frame left **free** it is blank mid-grey.

::: warn title="Frame indices are not free"
The video VAE compresses time by 8: frame 0 is latent 0, frames 1–8 are latent 1,
and so on. So the frames that sit on the latent grid are

```
0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120
```

— sixteen of them for a 121-frame clip. Anything off the grid snaps to the nearest
one and you end up conditioning on a frame you did not pick. Every condition below
is snapped to the grid in code before rendering.
:::

## The five conditions

Same motion, same appearance prompt, same seed. **Only the number of conditioned
frames changes.**

| condition | conditioned frames | count |
|---|---|---|
| `dense` | 0·8·16·24·32·40·48·56·64·72·80·88·96·104·112·120 | 16 |
| `K = 8` | 0·16·32·48·72·88·104·120 | 8 |
| `K = 5` | 0·32·64·88·120 | 5 |
| `K = 3` | 0·64·120 | 3 |
| `K = 2` | 0·120 | 2 |

`dense` is the control case the brief predicts: the pose is specified everywhere, so
the video model has nothing left to invent and should behave like a renderer.

## Appearance comes from text alone

::: key title="No reference image, no init frame"
The reason to use a depth IC-LoRA rather than a reference-image method is that **no
picture of a person is needed**. Appearance comes from the prompt, and the run
confirmed the pipeline accepts an empty image list — `images=[]`.

Each prompt names a person and a place and nothing else. No motion words: the
control carries the motion. All six end on the same three clauses, so lighting,
camera and framing are constant across them.
:::

| motion | appearance prompt |
|---|---|
| `box_heavy` | a muscular male warehouse worker in a warehouse, work trousers and a grey t-shirt, cardboard boxes and wooden pallets behind him, concrete floor |
| `barbell_heavy` | a muscular male weightlifter in a gym, athletic wear, loaded barbell rack and rubber flooring behind him |
| `push_heavy` | a muscular man on a suburban street beside a parked car, jeans and a dark t-shirt |
| `punch` | a lean male boxer in a boxing gym, shorts and hand wraps, bare torso, heavy bags and brick wall behind him |
| `squat` | a muscular man in a gym, athletic wear, rubber floor and racks behind him |
| `baseball` | a male baseball player on a baseball field, team uniform and cap |

Every one is followed by `natural lighting, static camera, full body in frame`.

::: note title="One prompt was changed mid-run"
`barbell_heavy` was originally the brief's own example verbatim — *"a muscular male
weightlifter in a gym, athletic wear"* — and it was the only one of the six that
named no scene. On seed 1234 at `dense` the model filled that gap by copying the
depth track's own flat mid-grey background instead of inventing a gym.

A scene clause was added so all six name their surroundings, and **all ten barbell
videos were regenerated with it**. Nothing else was re-rolled.
:::

## Settings that differ from the earlier experiments

::: warn title="Do not carry the old ones over"
| | Experiments 1–3 | This experiment |
|---|---|---|
| checkpoint | `dev` | **`distilled`** — the IC-LoRA requires it |
| pipeline | `TI2VidTwoStagesPipeline` | **`ICLoraPipeline`** |
| control parameter | `strength` on each conditioning image | **`ic-lora-strength`**, one value for the clip |
| what carries the pose | a list of keyframe images | **a depth video** |
:::

Held fixed across all 60 videos: control strength **1.0**,
`conditioning_attention_strength` **1.0**, no init frame, **121** frames at 25 fps,
**704×704**. Frame count must be `8n+1` and the dimensions divisible by 32.

The variable is how many frames are conditioned, not how strongly — so the strength
stays at 1.0 throughout.

## What each result page shows

Every motion gets its own page, in the same order:

1. **The input motion and the control tracks it became** — at `dense`, `K = 5` and
   `K = 2`, so you can see what was actually fed in before judging what came out.
2. **One grid per condition** — depth control, photoreal output, and recovered
   motion, side by side. The heading names the condition and its exact conditioned
   frames.
3. **Recovered motion across the sweep** — the five conditions in a row, which is
   the motion comparison proper.
4. **The timing strip** — control, photoreal and recovered against fixed frame
   times, as one image. Click to open it full size.

::: note title="The clips are synchronised"
Every clip here is 121 frames at 25 fps, so they can be compared frame against
frame — and the toolbar keeps them that way. **Sync** restarts every visible clip
together on a common loop rather than letting each drift on its own; the speed
buttons run the whole page at ¼×, ½×, 1× or 2×. Click any clip to open it and step
through a frame at a time.
:::

::: warn title="Read the photoreal row before the recovered row"
Pose recovery has a motion prior. It can return smooth, plausible motion from a
video that does not support it, and nothing in the output says so. Four of the
twelve `baseball` clips have distant background players; none contaminated a lift
here, but it is the failure mode to keep checking for, and it is why every grid
shows the video next to the motion taken from it.
:::

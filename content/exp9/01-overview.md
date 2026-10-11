---
title: Overview
nav: Overview
lead: Tell the model only where the body goes — a pelvis path, a few point tracks — and nothing about how it moves. The prompt and the video prior have to supply the action.
---

## The goal

Experiments 7 and 8 gave the model a skeleton. This one gives it a **trajectory**:
point tracks of the pelvis and, in some conditions, the hands and feet. The question
is whether the model can produce the right gait from *where* the body travels, with no
pose information.

There is no cheap interpolation baseline here, because a gait cannot be derived from a
path. `text only` is the lower bound and the full `skeleton` is the upper bound.

## Setup

- **Input:** the nine AMASS/BABEL clips from Exp 7, 169 frames @ 25 fps.
- **Control:** point tracks drawn the way ComfyUI's `LTXVDrawTracks` draws them, on
  every frame.
- **Video model:** LTX-2.3 22B distilled + Motion-Track-Control IC-LoRA (the
  `skeleton` column uses Union-Control), 768×768.
- **Recovery:** GVHMR, re-rendered on a neutral SMPL body.

| condition | what the model gets |
|---|---|
| `text only` | no control — lower bound |
| `root` | 1 track: the pelvis |
| `root + facing` | 2 tracks: pelvis and a point 0.5 m ahead of it |
| `root + limbs` | 5 tracks: pelvis, both wrists, both ankles |
| `skeleton` | full skeleton on every frame — upper bound |

The track controls for `run`:

::: clips arms=input,ctrl_root,ctrl_root_facing,ctrl_root_ee,ctrl_skeleton_dense ids=run seeds=1234
:::

## What came out

::: key
- **Headline, `run`:** the input is really a fast walk. Under `skeleton` the model
  walks, copying it faithfully. Under `root` it produces a real run: bent arms,
  airborne strides, a forward lean. That gait can only have come from the model's
  prior.
- **The track clearly reaches the model.** Pelvis error drops from 1223 px with
  `text only` to 337 px with `root`.
- **Gains appear only where the pelvis moves.** `walk` and `jump` improve. `wave`,
  `throw` and `kick` stay where they were.
- **Adding the facing point makes things worse**, while the wrist and ankle tracks
  rescue the arc of `throw`.
:::

[Photoreal outputs →](photoreal.html) · [Recovered motion →](recovered.html)

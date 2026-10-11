---
title: Overview
nav: Overview
lead: Give the skeleton on only K frames, leave the frames between them black, and find where the model stops copying the anchors and where the action stops being recognisable.
---

## The goal

Experiment 7 kept a skeleton on every frame. This one makes the skeleton **sparse in
time**: it is drawn on K anchor frames and the frames between are left black. The
model has to invent everything between the anchors.

Every K is compared against a **blend**: a straight-line interpolation between the same
anchor poses, with no model involved. The blend carries exactly the information the
model was given, so it shows what the video prior adds on top of that.

## Setup

- **Input:** the nine AMASS/BABEL clips from Exp 7, 169 frames @ 25 fps.
- **Control:** a DWPose skeleton on the anchor frames, black elsewhere. `K = all`
  reproduces Exp 7's `skeleton 100%`.
- **Video model:** LTX-2.3 22B distilled + Union-Control IC-LoRA, 768×768, strength 1.0.
- **Recovery:** GVHMR, re-rendered on a neutral SMPL body.

| condition | anchor frames |
|---|---|
| `K = all` | all 22 latent frames — 0·8·16·…·168 |
| `K = 8` | 0·24·48·72·96·120·144·168 |
| `K = 5` | 0·40·88·128·168 |
| `K = 3` | 0·88·168 |
| `K = 2` | 0·168 — the two ends |

What the control looks like as the anchors thin out:

::: clips arms=input,ctrl_Kall,ctrl_K5,ctrl_K3,ctrl_K2 ids=squat seeds=1234
:::

## What came out

::: key
- **The model never just interpolates.** In the gaps it sits 109–208 mm from the
  blend, and the distance grows as K drops.
- **It is far more physical than the blend.** Foot skate at `K = all` is, model
  against blend: walk 168 vs 956 mm/s, run 604 vs 1886 mm/s.
- **Whether the action stays recognisable depends on the motion.** `squat` and
  `walk` survive down to `K = 2`. `jump` and `stand_up` are lost between `K = 5`
  and `K = 3`. `kick` is lost by `K = 8`. From `K = 5`, `throw` turns into a
  badminton swing and a racquet appears.
:::

[Photoreal outputs →](photoreal.html) · [Model vs blend →](vs-blend.html)

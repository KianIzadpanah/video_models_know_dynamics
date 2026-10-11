---
title: Overview
nav: Overview
lead: Exp 13's best control was a trunk on every frame plus a full skeleton on keyframes, but it lost free-limb actions like kicks. Add wrist and ankle dots on every frame, and vary how many keyframes the limbs get.
---

## The goal

Two questions, building on Exp 13's `trunk + K5`:

1. Do **wrist and ankle dots on every frame** bring back the free-limb actions,
   `kick` and `throw`, that the trunk alone lost?
2. **How loose should the limbs be?** The full skeleton is given on 3, 5 or 8
   keyframes.

Every strength stays at 1.0, so all of the looseness comes from what is drawn. A
**gate** is also tested: fall back to `text only` when the input is badly broken.

## Setup

- **Input:** the 24 MotionGPT3 clips, with keyframes from Exp 12's entropy chooser.
- **Control:** head, shoulders and hips on every frame. The `+ dots` conditions add lone
  wrist and ankle points, with no elbows, knees or limb lines.
- **Video model:** LTX-2.3 22B distilled + Union-Control IC-LoRA, 768×768. Recovery
  with GVHMR.
- `text only`, `trunk + K5` and `dense 0.6` are reused from Exp 13.

| condition | what the control video holds |
|---|---|
| `trunk + K3 / K5 / K8` | trunk on every frame, full skeleton on 3 / 5 / 8 keyframes |
| `trunk + dots + K3 / K5 / K8` | the same, plus wrist and ankle dots on every frame |
| `dense 0.6` | full skeleton on all 169 frames, strength 0.6 |

How the controls differ, for `kick`:

::: clips arms=input,ctrl_trunk_K5,ctrl_trunk_ee_K3,ctrl_trunk_ee_K5,ctrl_trunk_ee_K8,ctrl_dense_s06 ids=kick seeds=1234
:::

## What came out

::: key
- **The dots bring the kick back at every K, even K3.** The ankle dot carries the
  foot's path. They do *not* fix `throw` on seed 1234: it stays a bat swing, and only
  `dense 0.6` throws on both seeds.
- **K barely matters overall.** Prompts that keep the action on both seeds: trunk
  15 / 15 / 16, trunk + dots 17 / 17 / 15 (K3 / K5 / K8). It matters only for
  limb-driven actions, where the dots do the job that more keyframes would.
- **The dots also carry the input's flawed limb paths.** On `heavy_box` the box is
  raised overhead or dropped, worst at K8.
- **Gating helps.** `text only` on the three badly broken inputs, plus
  `trunk + dots + K3` everywhere else, keeps the action on **20 of 24** prompts. The
  best single condition manages 17.
:::

[Photoreal outputs →](photoreal.html) · [How loose? →](looseness.html) · [Recovered motion →](recovered.html)

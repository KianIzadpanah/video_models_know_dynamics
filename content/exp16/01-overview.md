---
title: Overview
nav: Overview
lead: The same bad / uniform / hand-picked keyframe test as Exp 15, but on real motion capture. Now the true motion is known, so every clip can be scored against it.
---

## The goal

Exp 15's input was flawed, so "better" could only be judged by eye. Here the input is
**real AMASS motion capture**, which makes it the ground truth. The test of keyframe
choice is repeated (bad vs evenly spaced vs hand-picked, with black or a trunk between
them) on harder material: compound actions and out-of-distribution motions such as a
robot walk.

## Setup

- **Input:** twelve AMASS clips, 169 frames @ 25 fps, in tiers: simple, moderate,
  complex, compound and out of distribution.
- **Control:** five keyframes, drawn as in Exp 15. **black** is the skeleton on the
  keyframes and black between. **trunk** adds the trunk and wrist and ankle dots on
  every frame.
- **Video model:** LTX-2.3 22B distilled + Union-Control IC-LoRA, 768×768. Three seeds.
- **Scoring:** GVHMR, compared with the true mocap joints. The floor, GVHMR on a
  render of the mocap itself, is about 60 mm.

| condition | keyframes | between keyframes |
|---|---|---|
| `text only` | — | — |
| `bad / uniform / hand · black` | bad / evenly spaced / hand-picked | black |
| `bad / uniform / hand · trunk` | bad / evenly spaced / hand-picked | trunk + dots |

## What came out

::: key
- **Keyframe choice barely matters.** With black between, the action appears in 14 /
  17 / 18 of 36 clips (bad / uniform / hand). With the trunk it is 33 / 33 / 33.
- **The dense trunk is the big effect.** It takes action success from about 17 to 33
  of 36 and halves joint error (≈215 → ≈128 mm).
- **Black between fills the gaps with generic standing or walking.** `jumping_jacks`
  and `duck_walk` work on 0 of 9 clips; the trunk gets both on every seed.
- **Out of distribution:** text alone manages 0 of 9. The trunk does `robot_walk` and
  `airplane_run` on every seed. `walk_back_tiptoe` fails everywhere: the model turns
  around and walks forward, flat-footed.
:::

[Photoreal outputs →](photoreal.html) · [Recovered motion →](recovered.html)

---
title: Overview
nav: Overview
lead: Harder prompts, with objects, obstacles and several stages, where the text-to-motion input is clearly wrong. Does the video model supply what is missing, and does choosing the anchor frames smartly beat choosing them evenly?
---

## The goal

MotionGPT3 handled Exp 10's simple actions too well, so this run uses **harder
prompts**: boxes, shelves, doors, ladders, a pirate's bird. The input motion never
contains the object, because text-to-motion data has no world in it.

It asks three things:

1. Does the video model **add the missing object** and act on it?
2. Do **smarter anchor choices** beat evenly spaced ones? Two choosers are tried:
   *velmin*, the frames where the body is slowest, and *plaus*, the frames with the
   fewest physical errors.
3. How much comes from the **prompt alone**? `text only` uses no skeleton at all.

## Setup

- **Input:** MotionGPT3, fitted to SMPL, 169 frames @ 25 fps. Twelve prompts.
- **Control:** a DWPose skeleton on the anchor frames, black elsewhere. Every scheme
  keeps the first and last frame.
- **Video model:** LTX-2.3 22B distilled + Union-Control IC-LoRA, 768×768.
- **Recovery:** GVHMR, plus a straight-line blend baseline between the same anchors.

| condition | anchors |
|---|---|
| `text only` | none — prompt only |
| `K = all` | all 22 latent frames |
| `K = 5 / 3 uniform` | evenly spaced |
| `K = 5 / 3 velmin` | where the joints move slowest |
| `K = 5 / 3 plaus` | where ground penetration, foot skate, joint limits and floating are lowest |

## What came out

::: key
- **The missing object appears in 11 of 12 prompts**: box, shelf, door, tray,
  ladder, bar, steps, shoes, bench and wall, plus a pirate costume. Only `step_over`
  never gets its obstacle.
- **The anchor scheme barely matters.** The three choosers' outputs are visually
  indistinguishable. The failures are failures of content, not of sampling: there is
  no good frame to pick when the input is wrong throughout.
- **Control can hurt.** With `text only`, `climb_ladder` and `step_up` actually climb.
  Every skeleton-conditioned version stands still, copying the input's mistake.
- **The model beats the blend everywhere** on foot skate, by 2–3× (on `push_door`,
  33–169 vs 574–694 mm/s).
:::

[Photoreal outputs →](photoreal.html) · [Anchor schemes →](anchor-schemes.html) · [Recovered motion →](recovered.html)

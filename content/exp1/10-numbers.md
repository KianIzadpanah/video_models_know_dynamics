---
title: The numbers
nav: The numbers
lead: Joint error, jerk and foot-skate across all twelve conditions — and a careful account of why none of them settles whether the motion improved. They are here to size the floor and to flag lifts that should not be trusted.
---

## The table

Means over the 10 clips that lift correctly.
[`squat` is excluded](result-squat.html) — its `floor` already fails, so including it
would just move every column together.

| | input | floor | Kall | K9 | K5 | K3_1 | K3_2 | K3_3 | K3_4 | K2_1 | K2_2 | K2_3 | K2_4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint error vs input (mm) | — | 37 | 40 | 55 | 100 | 119 | 128 | 143 | 125 | 128 | 142 | 165 | 128 |
| jerk, relative to input | 1.00 | 0.72 | 0.75 | 0.79 | 1.47 | 1.01 | 2.08 | **2.51** | 1.71 | 0.81 | 1.16 | 1.82 | 1.37 |
| foot-skate planted (mm/s) | 158 | 144 | 142 | 133 | 224 | 175 | 252 | **394** | 223 | **114** | 170 | 280 | 182 |

## What the numbers do settle

### The round trip is not the source of the roughening

::: key title="The pipeline's own bias runs the other way"
`floor` and `K = all` come back **smoother** than the input — jerk 0.72 and 0.75
against the input's 1.00, foot-skate 144 and 142 against 158.

That is GVHMR's motion prior gently cleaning up whatever it is given. So the
pipeline's own bias runs in the **opposite** direction to what the loose columns
show. The extra jerk and skate in the loose columns come from the motion in those
videos, not from the trip.
:::

This is the single most useful thing the numbers contribute. Without it, every
"the returned motion is rougher" observation could be dismissed as recovery noise.

### Placement governs the outcome, not K

::: key title="Same K, opposite behaviour"
The sets that pin **no endpoint** are the worst on both roughness measures:
`K3_3` jerk 2.51 and skate 394 mm/s; `K2_3` jerk 1.82 and skate 280.

`K2_1` hands over **exactly the same two frames as `K2_3`** but puts them at the ends
— and it is the **calmest column in the whole table**: jerk 0.81, skate 114 mm/s,
below the input on both.

Same number of frames, opposite behaviour. This is
[Experiment 2's placement finding](../exp2/placement.html) reproduced by a completely
different measurement, on the other side of the pipeline.
:::

The full ordering of joint error follows the same rule: no endpoint pinned moves
furthest (`K2_3` 165, `K3_3` 143), one end free sits in the middle (`K3_2` 128,
`K3_4` 125, `K2_2` 142, `K2_4` 128), both ends anchored stays closest (`K5` 100,
`K3_1` 119).

## What the numbers do not settle

::: warn title="Smoothness is not the quantity of interest"
If naturalness meant smoothness and clean ground contact, this table would be a
straightforward negative result for the free-ended sets and a **positive** one for
`K2_1`.

But it does not. **Real human motion has impacts.**

- [`punch`](result-punch.html) has among the highest jerk ratios in the table, and
  its returned motion is the most convincingly physical thing in the experiment. A
  real punch *is* jerky.
- [`push_heavy`](result-push-heavy.html) comes back **smoother** than the input —
  jerk 0.47 to 0.82 — and no better. It is just a differently idle person.

A smoothness-based score would rank `push_heavy` above `punch`. Both would be
wrong.
:::

This is why the brief asks for eyes rather than metrics, and why the verdict on each
prompt page is a visual judgement. The numbers here have exactly two jobs:

1. **Size the floor**, so the loose columns can be read against real noise. See
   [The floor](floor.html).
2. **Flag lifts that should not be trusted** — a suspicious combination of clean
   output and a broken source, which is what sent us to look at
   [`box_heavy` s5678](result-box-heavy.html).

## Where the metrics came from

::: method title="Definitions"
**Joint error** — mean over 22 joints and 121 frames, root-relative, both motions
placed on the same neutral SMPL body with `betas = 0`. Root-relative because the
absolute world position is not comparable: GVHMR's world frame is arbitrary and the
clips are rotated onto their input's heading first.

**Jerk** — third derivative of joint position, reported as a ratio to the input
motion's jerk so that fast prompts and slow prompts are comparable.

**Foot-skate** — lateral velocity of a foot joint during frames where that foot is
classified as planted. In mm/s. A planted foot should not be moving.

All of it is in `results/analysis.json`, which opens with the note *"Supporting
numbers only; the verdict of this experiment is visual."*
:::

## Per-clip figures

The joint-error table for every clip and every condition is on
[The floor](floor.html#the-measurement), where it belongs — its main job is
establishing that the control column is clean.

Per-prompt tables pulled live from `analysis.json` are at the bottom of each result
page:
[box_heavy](result-box-heavy.html#the-numbers-for-this-prompt) ·
[barbell_heavy](result-barbell-heavy.html#the-numbers-for-this-prompt) ·
[push_heavy](result-push-heavy.html#the-numbers-for-this-prompt) ·
[punch](result-punch.html#the-numbers-for-this-prompt) ·
[squat](result-squat.html#the-numbers-for-this-prompt) ·
[baseball](result-baseball.html#the-numbers-for-this-prompt)

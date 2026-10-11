---
title: Overview
nav: Overview
lead: Exps 11 and 12 found that automatic keyframe choice rarely mattered. Test the best case and the worst case directly, with keyframes picked by hand and keyframes picked to be bad. Then ask whether a stage-by-stage prompt can act as control on its own.
---

## The goal

If keyframe choice matters at all, **hand-picked** keyframes should beat **evenly
spaced** ones, and **deliberately bad** picks (uninformative or broken poses) should be
worse. All picks were made in a picker tool and frozen before any video was generated.

The second question is about text. A **staged prompt** ("first…, then…, then…") is tried
on its own and together with keyframes. The idea being tested is that text supplies
meaning while keyframes supply timing.

## Setup

- **Input:** MotionGPT3 (flawed) on twelve prompts in tiers: simple, moderate,
  complex, plus three added later. Matching the input is not the goal.
- **Control:** five keyframes (0 and 168 always included), drawn two ways:
  - **black:** the full skeleton on the 5 keyframes, black between.
  - **trunk:** trunk plus wrist and ankle dots on every frame, full skeleton on the
    5 keyframes.
- **Video model:** LTX-2.3 22B distilled + Union-Control IC-LoRA, 768×768. Three seeds.
  Recovery with GVHMR.

| condition | prompt | keyframes | between keyframes |
|---|---|---|---|
| `text only` | short | — | — |
| `staged text` | staged | — | — |
| `bad / uniform / hand · black` | short | bad / evenly spaced / hand-picked | black |
| `bad / uniform / hand · trunk` | short | bad / evenly spaced / hand-picked | trunk + dots |
| `hand · trunk · staged` | staged | hand-picked | trunk + dots |

The three keyframe sets for one prompt:

::: clips arms=input,ctrl_single_bad,ctrl_single_uniform,ctrl_single_hand,ctrl_trunkee_hand ids=walk_stop_turn seeds=1234
:::

## What came out

::: key
- **Hand-picked does not beat uniform.** They tie in every tier. With trunk control
  there is no ordering at all: bad picks do as well as hand-picked ones.
- **Bad keyframes hurt only with black between**, and only where the prompt doesn't
  already name the action.
- **Staged prompt + hand-picked + trunk** is the only condition that does every
  stage in order on all 3 seeds of `walk_wave` and `walk_stop_turn`.
- **Some prompts fail everywhere.** `run_jump` never jumps (0 of 27 clips), the parrot
  is never petted, and `kneel_pick_stand` squats rather than kneels in 22 of 27,
  because the keyframes override the word "kneel".
- **The trunk halves foot skate** (229 → ~100 mm/s).
:::

[Photoreal outputs →](photoreal.html) · [Dense vs sparse →](dense-vs-sparse.html) · [Recovered motion →](recovered.html)

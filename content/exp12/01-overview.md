---
title: Overview
nav: Overview
lead: Exp 11 found that the way keyframes are chosen barely mattered. This one asks when it does matter, using a new chooser that picks the frames where the body moves in the most directions at once.
---

## The goal

Two new ways of choosing the five keyframes:

- **entropy** picks the frames where the joints move in the most different directions
  at once, which is where something is happening.
- **velent** works like an animator's keys and breakdowns: keys where the body pauses,
  breakdowns at the entropy peaks between them.

The prediction is that they help in **group A**, the prompts whose movement is roughly
right but where a brief key moment falls between evenly spaced frames (`jump`'s
airborne frame is f24). They should not help in **group B**, where every frame of the
input is wrong.

## Setup

- **Input:** the 24 MotionGPT3 clips of Exps 10 and 11. Group A comes from Exp 10 and
  group B from Exp 11.
- **Control:** a DWPose skeleton on five keyframes, black elsewhere. Frames 0 and 168
  are always kept.
- **Veto:** removes physically broken frames before choosing.
- **Video model:** LTX-2.3 22B distilled + Union-Control IC-LoRA, 768×768. Recovery
  with GVHMR, plus a straight-line blend baseline.

| condition | how the 5 keyframes are chosen |
|---|---|
| `text only` / `K = all` | references: no skeleton / all 22 grid frames |
| `uniform` | evenly spaced: 0·40·88·128·168 |
| `velmin` | where the body is slowest |
| `entropy` | where joint directions are most varied (`jump`: 0·24·40·136·168) |
| `entropy + veto` | entropy, with broken frames removed first |
| `velent` | pauses as keys, entropy peaks as breakdowns |

## What came out

::: key
- **`jump` comes back under `entropy`**, with a crouch, an arm swing, an airborne
  tuck and a landing. `uniform` and `velent` stand still. `velent` shares 4 of 5
  frames with `entropy` and differs only at f24, which shows that one missing frame
  was the whole cause.
- **Jitter is entropy's weak spot.** On a deliberately jittered clip it picked a
  jittered frame 52% of the time, against 12% on the clean clip.
- **The veto rarely changes anything.** It changes the picks on only 1 of 24 clips
  (`climb_ladder`).
- **Overall the outputs are loose.** The model follows the anchors only weakly, which
  is what Exp 13 sets out to fix.
:::

[Photoreal outputs →](photoreal.html) · [The jump →](jump.html)

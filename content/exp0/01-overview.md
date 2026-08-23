---
title: Overview
nav: Overview
lead: Three ways to turn the same sentence into human motion, run over nine prompts and three seeds, so that the arms can be compared clip by clip.
---

## The question

A text-to-motion model and a video model are given the same sentence. The motion
model has learned from mocap paired with captions; the video model has learned
from footage of the physical world. If a video model carries an implicit model of
dynamics, the place it should show up most plainly is **load** — the lean, the
brace, the slower and more controlled trajectory that a heavy object forces on a
body.

So the experiment asks: *given identical text, does the video model show the
weight where the motion model shows a generic version of the action?*

## The three arms

Every prompt is generated three ways. These are the three columns you will see in
every results grid.

| arm | what it is | why it's here |
|---|---|---|
| **T2M** | MotionGPT3 generates a HumanML3D joint sequence; that is fitted to SMPL and rendered as an untextured mesh | the motion-model baseline |
| **T2V** | LTX-2.5 generates video from the text alone | the video model, unconstrained |
| **I2V** | LTX-2.5 generates video conditioned on frame 0 of the T2M render | the video model, forced to start from the motion model's own pose |

The I2V arm is the interesting one. It starts the video model from the *same body,
same camera, same floor* as the T2M arm, which removes the "different person in a
different room" confound — at the cost of starting from a near-neutral standing
pose, since frame 0 of a MotionGPT3 clip usually is one.

::: diagram
The three arms: one prompt in, three generation paths, three clips out. T2V and I2V
share a video model; I2V is additionally seeded on frame 0 of the T2M render.
:::

::: stats
9: prompts
3: arms
3: seeds each
81: clips total
:::

## The prompt set

Nine prompts in three shapes:

- **Three matched pairs** — `box`, `barbell`, `push` — where the two members differ
  only in the load word (*heavy box* / *light box*, *car* / *cart*). These are the
  primary comparison.
- **Three unloaded actions** — `punch`, `squat`, `baseball` — fast or
  body-weight-only motions, as a control for "does the video model just always
  look more dynamic".

No effort or weight words were added anywhere beyond what the prompt text already
says. The load word in the prompt is the only thing that differs within a pair.

## What to look at, and in what order

::: method title="Suggested reading order"
1. **[Setup](setup.html)** — models, resolutions, seeds, the exact prompts.
2. **[Reading the clips](reading-the-clips.html)** — five facts about how the
   arms differ by construction. Worth reading *before* the results, because
   several of them look like findings if you don't know they were designed in.
3. **The three matched pairs** — [box](result-box.html),
   [barbell](result-barbell.html), [push](result-push.html). This is where the
   question is actually answered.
4. **The three unloaded controls** — [punch](result-punch.html),
   [squat](result-squat.html), [baseball](result-baseball.html).
5. **[Verdict](verdict.html)** — the pairs read against the controls.
6. **[Composed montages](montages.html)** — the same material pre-rendered into
   single files, for when you want to watch rather than click.
7. **[Fit quality](fit-quality.html)** and
   **[Provenance](provenance.html)** — how much the joints→SMPL step distorted
   the T2M arm, and where every file came from.
:::

::: warn title="What this experiment does not do"
There is no metric here and no human study. It produces matched clips and lays
them out so a difference — if there is one — can be seen. Any quantitative claim
about weight or effort would need a separate experiment with an actual estimator.
:::

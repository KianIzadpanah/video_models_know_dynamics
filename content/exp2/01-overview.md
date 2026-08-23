---
title: Overview
nav: Overview
lead: We take a motion model's output, render it as a plain blue character, and then hand a video model only some of those frames — making it invent the rest. The fewer frames it gets, the more of the motion is its own.
---

## The idea, in plain words

A text-to-motion model can already turn *"a person lifts a heavy box from the
floor"* into a moving skeleton. It usually looks stiff, and it often does not
really do the thing you asked for. The question is whether a **video** model —
which has watched enormous amounts of real footage — knows something about how
bodies actually move that the motion model does not.

To find out, we need to give the video model room to disagree. So:

1. Generate the motion with the motion model.
2. Render it as a **blue character** video — a plain, untextured body on a gray
   floor, fixed camera. Nothing distracting.
3. Hand the video model **only a few of those frames** and ask it to fill in
   everything between them.

If it only gets a handful of frames, it has to work out the *timing* on its own:
how fast the lift happens, where the pause at the bottom is, when the weight
shifts. That timing is precisely the physical knowledge we are testing for. Hand
over every frame and we never ask the question — the model just copies.

The knob is simply **how many frames we hand over**, and we call it **K**.

::: diagram
The pipeline: text becomes motion, motion becomes a blue character video, a few
of its frames become conditioning for the video model, and the video model
generates the rest.
:::

## What "K" means

The frames we hand over are called **pinned** frames, because the output is
forced to match them. Everything between two pinned frames is a **free run** —
the video model's own work.

| | |
|---|---|
| **K = all** | 16 frames pinned, every 8th one. Nothing is left free. This is **strong control**. |
| **K = 9** | every 16th frame. Still almost fully pinned. |
| **K = 5** | five frames: both ends plus three beats in the middle. |
| **K = 3** | three frames — and *where* those three sit turns out to matter enormously. |
| **K = 2** | two frames. The longest free runs in the sweep. This is **loose control**. |

For K = 3 and K = 2 we ran four different **placements** each, moving the pinned
frames around while holding everything else fixed. That turned out to be the most
important decision in the experiment — see [Placement, not
K](placement.html).

::: stats
6: prompts
11: conditioning sets
2: seeds each
132: generated videos
:::

## What we used

| step | model / tool | notes |
|---|---|---|
| Text → motion | **MotionGPT3** (`OpenMotionLab/MotionGPT3`) | HumanML3D format, 20 fps |
| Motion → body | **SMPL neutral**, `betas = 0` | resampled to 25 fps for the render |
| Render | matte blue body, gray floor, fixed 3/4 front-left camera | 121 frames, 25 fps, 512×512 |
| Video generation | **LTX-2.5 dev, 22B** | `TI2VidTwoStagesPipeline`, keyframe conditioning |

Two seeds throughout — **1234** and **5678** — fixed and logged. The same seed
drives the motion sampling *and* the video sampling, so within a row of clips the
only thing that changes is K.

## What came out of it

::: key title="The three findings, in short"
1. **At K = all and K = 9 the video model is a pure copier.** It adds slightly
   *less* motion than the input. No physical knowledge is expressed at all.
2. **There is a real window — K = 5 and K = 3_2 — where the video model visibly
   re-times the motion** instead of copying it. `squat` becomes repeated reps
   instead of one four-second hold; `punch` reaches full arm extension, which the
   input never does; `box_heavy` invents a cardboard box and performs an actual
   lift.
3. **But it is not a dial.** Handing over fewer frames does *not* reliably buy
   more motion. What actually governs it is **where the pinned frames sit** — and
   specifically whether the two ends of the clip are free.
:::

::: warn title="The failure mode was not the one we expected"
Going in, we expected that at low K the character would *morph* — smoothly melt
from one pinned pose to the next instead of performing the action. That never
happened, in any of the 132 clips. The actual failure at low K is
**under-moving**: given two distant pinned poses, the model often takes the
laziest path between them and the character goes nearly static.
:::

## Suggested reading order

::: method title="How to work through this"
1. **[How it was run](setup.html)** — the latent-grid constraint on which frames
   you are even allowed to pick, the eleven conditioning sets, and the settings.
2. **[Does it work?](does-it-work.html)** — three sanity checks that had to pass
   before any result here means anything. Read this before the results.
3. **The six prompts**, one page each. `box_heavy` is the most striking, `squat`
   is the clearest re-timing, and `barbell_heavy` is the clearest negative.
4. **[Placement, not K](placement.html)** — the cross-cutting result, and the
   most interesting thing in the experiment.
5. **[Verdict](verdict.html)** — what this means, and which two K values
   [Experiment 1](../exp1/overview.html) inherits from here.
:::

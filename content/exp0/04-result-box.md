---
title: Result 1 — box pair
nav: Result 1 · box (heavy/light)
lead: "A person lifts a heavy box from the floor" against "a person lifts a light box from the floor." One word differs, so anything that changes between the two rows is the model's response to that word.
---

This is the first of the three primary comparisons. The top row is the heavy
prompt, the bottom row its light counterpart; the columns are the three arms.

Compare **down a column** to see whether the load word changed anything, and
**across a row** to see how the three arms rendered the same sentence.

::: note title="Use the toolbar"
Each pair was generated at seeds 0, 1 and 2 — worth cycling through, because
MotionGPT3's clip length is seed-dependent (see
[Reading the clips](reading-the-clips.html)) and single-seed impressions of
generative output are unreliable. Slowing playback to ½× or ¼× is the fastest way
to judge the moment the object leaves the floor.
:::

## The clips

::: clips arms=t2m,t2v,i2v ids=box_heavy,box_light seeds=0,1,2
The `box` pair. Heavy above light. Click any clip to step through it frame by
frame — the moment the object leaves the floor is where a difference in load
should be most visible.
:::

::: todo title="Observations — box"
Write what you actually see here. Things worth stating explicitly if they hold:

- Does the **T2M** arm differ at all between the heavy and light rows, or is it
  the same generic pick-up twice?
- In **T2V**, is there a visible brace — hips back, torso angle, knee bend before
  the lift — and does it differ between rows?
- How long does the **I2V** arm spend in the idle pose before committing, and does
  the load word change the trajectory once it does?
- Does the effect survive across seeds 0, 1 and 2, or is it a one-seed
  coincidence?
:::

## Why this pair is the cleanest test

A box is the most generic possible load: no technique, no implement, no
stereotyped form. That means a difference between these two rows is hard to
attribute to anything except the load word itself.

It is also the prompt that turned out to matter most in the two later experiments.
In [Experiment 2](../exp2/result-box-heavy.html) it is the only prompt where the
video model invents the named object and performs the action, and in
[Experiment 1](../exp1/result-box-heavy.html) it is one of two prompts whose motion
comes back visibly more natural than it went in.

Next: [the barbell pair](result-barbell.html), where the same load contrast is
applied to an action with a stereotyped technique.

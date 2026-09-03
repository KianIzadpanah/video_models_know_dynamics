---
title: What fills the free run
nav: What fills the free run
lead: The cross-cutting result, and the clearest difference from Experiment 1. Where the earlier sweep filled its unpinned stretches with invented events, this one mostly fills them with whatever the person in the prompt would plausibly be doing — which is often very little.
---

## The finding

In [Experiment 1](../exp1/observations.html) the free stretches filled with invented
**events**: a cardboard box appeared and was carried off, a hand truck was pushed.

Here they mostly fill with **whatever the person in the prompt would plausibly be
doing**. And because the depth track's blank mid-grey frames say *"nothing in
particular is happening"*, plausible often means **idling**.

::: key title="The prompt supplies the content of the free run"
- The **boxer** keeps a real guard, steps, and throws the occasional punch, at every
  sparse condition — because the prompt put him in a boxing gym.
- The **warehouse worker** stands in a warehouse and shifts his weight. At `K = 2`
  seed 5678 he simply walks across the frame.
- The **man on the street** stands beside a car with one arm out and lowers it.

This changes what "loose control" buys you. In Experiment 1 the free run was an
opportunity for the video prior to supply an action. Here it is an opportunity for it
to supply a *person doing something reasonable* — and the two are only the same thing
when the reasonable thing happens to be the action you asked for.

[`punch`](result-punch.html) is exactly that case, and it is the one motion of six
that improves.
:::

## Props and roles, including at dense

The prompt also supplies objects, and it does so even when the pose is fully
specified:

- the **baseball player** picks up a bat and takes a stance in **seven of his ten
  clips**, including at `dense`
- in `s5678` at `K = 8` he is handed a **fielder's glove** instead, and catches and
  throws
- in the two loosest `s5678` clips he carries nothing and a bat lies on the ground
  beside him

None of it is in the control or in the input motion. None of it comes back through
pose recovery either — the lift returns a body and nothing else.

::: note title="Why it counts anyway"
A prop the recovery cannot see is worthless as *motion*. But it is visible evidence
that the video model is reasoning about the **action**, not only about pixels: it
decided a baseball player on a field should be holding a bat, and put one there.

That is the same faculty we want it to apply to timing and weight. Here it shows up
in the one channel that survives to the screen and not to the SMPL.
:::

## The one case where the free run supplied the missing action

::: key title="barbell_heavy, seed 1234, K = 2"
MotionGPT3 never produced a barbell lift for this motion, and neither
[Experiment 2](../exp2/result-barbell-heavy.html) nor
[Experiment 1's round trip](../exp1/result-barbell-heavy.html) could get one out of
it.

With **only frames 0 and 120 pinned**, a loaded barbell appears on the gym floor in
the last third of the clip and the man walks to it and folds into a deadlift setup,
hands to the bar — and the hip hinge comes back intact as SMPL.

One clip in sixty. It did not repeat on the other seed.
:::

::: clips arms=probe_deadlift width=980px
The photoreal row and the recovered motion underneath it.
:::

## Why this is less inventive than Experiment 1

The mechanism is visible in the control videos themselves.

::: warn title="A blank control frame is not permission"
A sparse condition hands the model a track that is blank mid-grey for around 90 % of
its frames. **A blank control frame is not "do what you like here" — it is a positive
statement that the reference has nothing in it.** The model answers it with a person
standing still.

Experiment 1's blue-character conditioning had no equivalent: between two pinned
frames there was simply no constraint, so the prior filled the gap with an action.
Here the gap is *specified as empty*.
:::

::: clips arms=probe_depthconds width=900px
The five control tracks. Read right to left and the question is not "how much freedom
does the model have" but "how much of the reference is blank".
:::

## The lever to try next

::: key title="conditioning_attention_mask"
The API already exposes a mask video over the reference, and it was deliberately left
unused here. It would let the free frames be **ignored** rather than read as empty —
which is the difference between "nothing is happening" and "no constraint".

**This is the first thing to try next.** It targets the exact mechanism this page
identifies, and it needs no new model, no new control signal and no re-rendering: the
same 60 depth tracks with a mask alongside them.
:::

## One thing the numbers do say, and it is not about smoothness

Averaged over the ten clips that lift correctly:

| | input | dense | K = 8 | K = 5 | K = 3 | K = 2 |
|---|---|---|---|---|---|---|
| jerk, relative to input | 1.00 | 0.87 | 0.93 | 0.75 | 0.78 | 0.78 |
| foot-skate, planted (mm/s) | **158** | 146 | **77** | **58** | 82 | 121 |

::: key title="The free runs come back with less than half the input's foot-skate"
Foot-skate is a planted foot sliding along the ground — a foot carrying weight that
is not staying put. The motion the video model invents **obeys the ground better than
the motion MotionGPT3 produced**: 58–82 mm/s against 158, while `dense`, which is
copying, inherits the input's 146.

That is a small, specific piece of evidence for the bet behind the project. A
plausible-looking person shot by a static camera plants their feet, and the video
prior knows it.
:::

::: warn title="But it is not a claim that the returned motion is better"
Jerk falls in every column, and
[Experiment 1 already made the point](../exp1/numbers.html) that smoothness is not
the quantity of interest — a real punch *is* jerky. These two rows are here to bound
the round trip, not to score it.
:::

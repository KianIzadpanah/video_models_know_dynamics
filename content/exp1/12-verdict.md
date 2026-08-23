---
title: Verdict
nav: Verdict
lead: Two of six prompts come back visibly more natural. The improvement is specific — the video model supplies a missing part of the action — and it is governed by where the free run sits, not by how many frames were withheld.
---

## The result

::: key title="Two of six prompts come back visibly more natural"
| prompt | verdict |
|---|---|
| [`box_heavy`](result-box-heavy.html) | **yes, clearly** — a purposeful kneel-and-reach replaces a vague flail |
| [`punch`](result-punch.html) | **yes, partially** — the guard becomes actual punches, with full extension |
| [`barbell_heavy`](result-barbell-heavy.html) | no — arm-waving variants, jerkier than the input |
| [`push_heavy`](result-push-heavy.html) | no — a differently idle person, and smoother |
| [`baseball`](result-baseball.html) | marginal — a stride, with doubled foot-skate |
| [`squat`](result-squat.html) | unusable — the lift fails in the control column |
:::

## What kind of improvement it is

::: key title="The video model supplies a missing part of the action"
Where it works, the mechanism is specific and identifiable:

- the **extension** of a punch, which the input never reaches
- a **kneel and reach** for an object the input never touches
- a **box picked up and carried off**, which the input does not contain

And pose recovery brings each of these back as motion intact.

It is **not** a general smoothing or physical-plausibility fix. Where the motion
model's output was simply wrong for the prompt, the round trip returns something
equally wrong.
:::

## The structural result

Running all eleven conditioning sets rather than only the two loose values adds one
clear finding:

::: key title="What the video model contributes is governed by where the free run sits, not by how many frames it is given"
`K2_1` and `K2_3` hand over **exactly two frames each**. The first comes back calmer
than the input and barely changed. The second comes back the furthest from the input
of any column, and the roughest.

On `box_heavy`, the free half decides whether the invented box shows up at the
**start** (`K3_2`, `K2_2`) or at the **end** (`K3_4`, `K2_4`) — the same action,
relocated.

That matches what [Experiment 2](../exp2/placement.html) found from the other side,
by a completely different measurement: **the video prior extends what it is given;
it does not correct it.**
:::

## Caveats worth carrying

::: warn title="1. The recovery prior is doing real work, and it is invisible in the output"
The [`box_heavy` s5678 `K3_2`](result-box-heavy.html) lift is smooth, plausible, and
drawn from a shot containing two different people — the blue character and a
photographic person in pink pushing a hand truck.

**Nothing about the returned motion signals that.** Every conclusion here was checked
against its source video, and any future conclusion has to be. This is why every
result page pairs the source with the return rather than showing the return alone.
:::

::: warn title="2. One clip in six failed to lift at all"
[`squat`](result-squat.html) is not an exotic pose — it is the second-most common
thing in a motion dataset. A folded crouch from a single fixed viewpoint is
genuinely front-back ambiguous, and pose recovery resolves it the wrong way every
time.

A second camera angle, or simply an off-axis camera, would probably fix it. **Worth
doing before running this at any scale.**
:::

::: warn title="3. The useful range is narrow, and placement sets it rather than K"
`K = 5` and `K = 3_2` were the only two sets in
[Experiment 2](../exp2/verdict.html) where every prompt moved more than its input.
Running all eleven sets through the round trip does not widen that:

- the sets that pin no endpoint (`K3_3`, `K2_3`) move furthest but come back with
  **2.5× the jerk and 2.5× the foot-skate**
- the sets that anchor both ends barely move at all — `K2_1` comes back *calmer*
  than the input

There is not much room between "the video model copies" and "the video model leaves
the clip". **That ceiling is a property of keyframe conditioning, not of the video
model** — which is the argument for moving to a control signal the model was trained
on.
:::

## What this project has established so far

Taking the two experiments together:

1. **Keyframe conditioning works mechanically.** Pinned frames land, full
   conditioning reproduces the input, and no morphing occurs.
   [(Experiment 2's checks)](../exp2/does-it-work.html)
2. **There is a real window where the video model re-times motion** rather than
   copying it, and it exists for every prompt.
3. **The round trip is essentially lossless**, so motion added in the video survives
   back into 3D. [(The floor)](floor.html)
4. **The video prior extends; it does not correct.** It can supply a missing part of
   an action, and it cannot fix an action that is wrong.
5. **The control is a placement puzzle, not a dial** — and that is the main obstacle
   to scaling any of this up.

::: note title="What would move this forward"
A per-frame control signal the model was actually trained on
(`LTX-2-19b-IC-LoRA-Pose-Control`) would replace the placement puzzle with a
monotone strength dial, and an off-axis or second camera would remove the recovery
failure that cost us `squat`. Both are cheap relative to what they unblock.

Neither changes the finding that matters: **the video model has actions available
that the motion model does not, and it will supply them when given room.**
:::

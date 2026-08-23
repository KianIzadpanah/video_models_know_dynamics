---
title: Verdict
nav: Verdict
lead: There is a real window where the video model re-times motion instead of copying it — and it exists for every prompt. But the mechanism is narrower than hoped, and it is a placement puzzle rather than a dial.
---

## The question the brief asked

> If the motion stays stiff right up until the action falls apart, write that down
> clearly. It means this control mechanism is not leaving the video prior room to
> work.

::: key title="It does not — but the mechanism is narrower than hoped"
There **is** a real window — `K = 5` and `K = 3_2` — where the video prior visibly
re-times the motion rather than copying it:

- [`squat`](result-squat.html) becomes repeated reps instead of a four-second hold
- [`punch`](result-punch.html) reaches full arm extension, which the input never does
- [`box_heavy`](result-box-heavy.html) performs an actual lift, with an invented box

That window exists for **every** prompt. So the mechanism does leave the prior room
to work.
:::

## Two limits to carry forward

::: warn title="1. The prior extends, it does not correct"
Where MotionGPT3's motion is simply wrong for the prompt —
[`barbell_heavy`](result-barbell-heavy.html),
[`push_heavy`](result-push-heavy.html),
[`baseball`](result-baseball.html) — **no K produces the named action.** The model
adds plausible movement of its own; it does not fix the semantics.

The comparison that establishes this is `box_heavy` against `barbell_heavy`. Both
name a concrete object the input lacks. The box gets drawn and lifted; the barbell
never appears. The difference is that the box input already resembled a crouch
closely enough to be developed into a lift.
:::

::: warn title="2. The control is not a dial"
Motion added is **not monotone in K**. `K = 2_1` is stiffer than `K = 5`. What
governs the outcome is *where* the pinned frames sit — specifically whether the
clip's two ends are free — and the two knobs are entangled.

See [Placement, not K](placement.html) for the evidence. This is the argument for
switching to a per-frame control signal the model was trained on
(`LTX-2-19b-IC-LoRA-Pose-Control`), which would give a monotone strength dial
instead.
:::

## The two K values Experiment 1 inherits

::: key title="K1 = 5 (0, 32, 64, 88, 120) and K2 = 3_2 (64, 88, 120)"
Chosen for three reasons:

1. **They are the only two sets where all six prompts move more than their blue
   input** — `K = 5`: 1.16–2.78; `K = 3_2`: 1.03–2.63. Everywhere else at least one
   prompt goes static, which would give the round trip a "loose" column that is
   really a frozen one.
2. **Both still anchor frame 120**, so the clip ends on the input's pose. The round
   trip then compares two motions that finish in the same place.
3. **They bracket the interesting range.** `5` keeps both ends plus three interior
   beats and never drifts (0/12 on both drift measures). `3_2` frees the entire
   first 64 frames — the longest genuinely unconstrained run that still ends
   anchored — at the cost of `box_heavy` drifting in 2 of 12 clips.
:::

### Why not the others

**`3_4` and `2_4`** (first half pinned) fail the same test the rest do: they do not
move every prompt. `barbell_heavy` drops to 0.81 at both, and `box_heavy` to 0.74 at
`2_4`. They are still worth watching in the round trip, which is why
[Experiment 1](../exp1/overview.html) carries **all eleven** sets rather than only
these two.

**`3_1`** (0, 64, 120) is clean on every drift measure but adds little motion — 1.10
mean, and below 1.0 for four of six prompts. As a second point it risks being
indistinguishable from the strong-control column.

**`3_3` and `2_3`** are not recommended for the round trip at all. They pin no
endpoint, so a lifted motion cannot be compared with the input at the boundaries,
and they occasionally open on an implausible pose — `box_heavy` s1234 at `K = 3_3`
starts with the character lying on the floor.

## Where this goes next

[Experiment 1](../exp1/overview.html) takes these videos and pulls motion back out
of them, which is the only way to ask whether the added movement is *better* motion
rather than just *more* of it. That experiment reuses this one's code, settings and
keyframe manifest directly, so the two cannot drift apart.

::: note title="What this experiment cannot tell us"
Everything on the six prompt pages is a visual judgement. The energy numbers size
the effect; they do not establish that the re-timed motion is more natural, because
"more silhouette change per frame" is not naturalness. `push_heavy` at `K = 2_3`
produces two and a half times the input's movement and none of it is pushing.

Naturalness needs the motion back in 3D, which is the next experiment.
:::

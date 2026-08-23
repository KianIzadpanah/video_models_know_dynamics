---
title: Result 3 — push_heavy
nav: Result 3 · push_heavy
lead: "A person pushes a car." No. The input is close to static, no car is ever pushed, and the returned motion is not more natural — it is just a differently idle person. This is also the one prompt that comes back smoother than it went in.
---

## What went in

The input is **close to static**: the character stands with one arm out and does
almost nothing. It was the lowest-energy input in
[Experiment 2](../exp2/result-push-heavy.html) as well.

Floor: 37 mm on both seeds — and `K = all` at 38/37 mm reproduces it exactly.

::: clips arms=blue,lift_floor,lift_Kall ids=push_heavy seeds=1234,5678 size=lg
Input, `floor`, `K = all`. There is very little here for the round trip to lose,
which is why this prompt has the tightest control column of the six.
:::

## The returned motion

::: clips arms=blue,lift_K5,lift_K3_2 ids=push_heavy seeds=1234,5678 size=lg
`K = 5` at 76 mm (s1234) and 61 mm (s5678) — the **smallest** loose-set deviations in
the experiment. `K = 3_2` at 112 mm and 79 mm.
:::

::: key title="What we observed — no"
`K = 5` adds a **slight forward lean**. `K = 3_2` adds **looking down and reaching**.

No car is ever pushed, and nothing about the returned motion is more natural. It is
a differently idle person.

**Jerk actually falls** — 0.47 to 0.82 — so the motion comes back *smoother* than it
went in, and no more meaningful. That combination is the cleanest counterexample in
the experiment to using smoothness as a proxy for naturalness.
:::

## Source video beside returned motion

::: clips arms=vid_K5,lift_K5,vid_K3_2,lift_K3_2 ids=push_heavy seeds=1234,5678
Source then return. The lean at `K = 5` and the reach at `K = 3_2` are both genuinely
in the source videos — they are just not pushing a car.
:::

## Placement variants

::: clips arms=lift_K3_1,lift_K3_2,lift_K3_3,lift_K3_4 ids=push_heavy seeds=1234,5678
`3_1` 85/78 mm · `3_2` 112/79 · `3_3` 98/88 · `3_4` 70/69. This prompt has the
flattest placement response of the six — an input with nothing in it gives the free
run nothing to extend.
:::

::: clips arms=lift_K2_1,lift_K2_2,lift_K2_3,lift_K2_4 ids=push_heavy seeds=1234,5678
`2_1` 104/114 · `2_2` 164/87 · `2_3` 142/108 · `2_4` 120/84.
:::

::: note title="The two experiments agree on this prompt from opposite directions"
[Experiment 2](../exp2/result-push-heavy.html) found that `2_3` produces two and a
half times the input's movement, none of which is pushing. Here the same prompt
comes back **smoother** than the input and no better.

More motion in the video, less jerk in the recovered motion, and no car in either.
Both measurements point the same way: this is the prompt where the video model has
nothing to work with, and neither measure of "more" corresponds to "better".
:::

## The numbers for this prompt

::: metrics src=results/analysis.json key=results where=prompt_id=push_heavy cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=mpjpe_root_rel_mm
Note how many `jerk_ratio` values sit below 1.00 — this is the prompt where the
round trip smooths rather than roughens.
:::

## Timing strip

::: clips arms=strip ids=push_heavy seeds=1234,5678 width=760px
The input above every returned motion, time-aligned. Very little changes down the
rows, which is the result.
:::

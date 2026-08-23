---
title: Result 6 — baseball
nav: Result 6 · baseball
lead: "A person hit a ball with baseball bat." Marginal. A leg lift and a torso rotation come back that read a little like a batting stride — but no bat, no ball, and foot-skate roughly doubles.
---

## What went in

Floor: 37 mm (s1234) and 34 mm (s5678) — the cleanest control column of the six. So
whatever comes back is genuinely attributable to the video model.

::: clips arms=blue,lift_floor,lift_Kall ids=baseball seeds=1234,5678 size=lg
Input, `floor`, `K = all`. 37/34 mm and 39/36 mm.
:::

## The returned motion

::: clips arms=blue,lift_K5,lift_K3_2 ids=baseball seeds=1234,5678 size=lg
`K = 5` at 118 mm (s1234) and 109 mm (s5678); `K = 3_2` at 128 mm and 150 mm.
:::

::: key title="What we observed — marginal"
`K = 5` and `K = 3_2` add **a leg lift and a torso rotation** that read a little like
a batting stride. The shape of the motion is right for the prompt.

But **no bat and no ball are ever present**, and **foot-skate roughly doubles** —
from 180 to 293 mm/s at `K = 5` on seed 1234.

Slightly more dynamic. Not obviously more natural.
:::

## Source video beside returned motion

::: clips arms=vid_K5,lift_K5,vid_K3_2,lift_K3_2 ids=baseball seeds=1234,5678
Source then return. The stride is really in the source videos — this is not a
recovery artefact. It is just a stride in empty space.
:::

## Placement variants

::: clips arms=lift_K3_1,lift_K3_2,lift_K3_3,lift_K3_4 ids=baseball seeds=1234,5678
`3_1` 122/176 mm · `3_2` 128/150 · `3_3` 155/110 · `3_4` 152/110. This prompt has the
noisiest seed-to-seed disagreement in the experiment — `3_1` is 122 on one seed and
176 on the other.
:::

::: clips arms=lift_K2_1,lift_K2_2,lift_K2_3,lift_K2_4 ids=baseball seeds=1234,5678
`2_1` 180/132 · `2_2` 161/190 · `2_3` 171/178 · `2_4` 122/103.
:::

::: note title="Why the foot-skate matters here specifically"
Foot-skate is a planted foot sliding along the ground — a foot that is supposed to be
carrying weight but is not staying put. For a batting stride, where the whole point
is loading onto the back foot, doubling the skate is the opposite of what "more
natural" should look like.

That is what separates this from [`punch`](result-punch.html), where the extra
roughness corresponds to a real physical impulse. Here the extra motion comes with
degraded ground contact, so the added dynamism does not buy plausibility.
:::

::: note title="Both experiments call this one marginal"
[Experiment 2](../exp2/result-baseball.html) found the stride and rotation appear at
`K = 5` and `K = 3_2` and nowhere else, with no bat ever drawn. The round trip agrees
from the other side: the motion that comes back is a stride, and it is a slightly
worse-grounded one.
:::

## The numbers for this prompt

::: metrics src=results/analysis.json key=results where=prompt_id=baseball cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-foot_skate_out_mm_s
Sorted by foot-skate, worst first. Compare the top rows against `floor` and
`K = all` near the bottom.
:::

## Timing strip

::: clips arms=strip ids=baseball seeds=1234,5678 width=760px
The input above every returned motion, time-aligned.
:::

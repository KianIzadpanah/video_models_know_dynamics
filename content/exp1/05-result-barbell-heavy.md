---
title: Result 2 — barbell_heavy
nav: Result 2 · barbell_heavy
lead: "A person lifts a heavy barbell from the ground." No. MotionGPT3 never produced a barbell lift to begin with, and the round trip cannot invent one — it returns arm-waving variants, jerkier than what went in.
---

## What went in

MotionGPT3's clip is **an arm-raise, not a barbell lift**.
[Experiment 2 established](../exp2/result-barbell-heavy.html) that no conditioning
set rescues this prompt: no barbell is ever drawn in the video, unlike the box in
`box_heavy`.

Floor: 42 mm (s1234) and 41 mm (s5678). Clean, so whatever comes back is real.

::: clips arms=blue,lift_floor,lift_Kall ids=barbell_heavy seeds=1234,5678 size=lg
Input, `floor`, `K = all`. 42/41 mm and 44/44 mm — the control and strong-control
columns behave exactly as they should.
:::

## The returned motion

::: clips arms=blue,lift_K5,lift_K3_2 ids=barbell_heavy seeds=1234,5678 size=lg
`K = 5` at 124 mm (s1234) and 74 mm (s5678); `K = 3_2` at 122 mm and 137 mm. The
motion genuinely changed — it just did not become a barbell lift.
:::

::: key title="What we observed — no"
The loose sets return **arm-waving variants at 74–204 mm from the input**. On seed
1234 the returned motion is far jerkier than what went in — jerk ratio **3.5** at
`K = 5` and **4.8** at `K = 3_3`.

Different, not better. There is no barbell in any source video, so there is no
barbell lift to recover.
:::

## Source video beside returned motion

::: clips arms=vid_K5,lift_K5,vid_K3_2,lift_K3_2 ids=barbell_heavy seeds=1234,5678
Source then return, at both loose values. The source videos are worth watching here
precisely because nothing appears in them — this is what "the prior extends what it
is given" looks like when what it was given is wrong.
:::

## Placement variants

::: clips arms=lift_K3_1,lift_K3_2,lift_K3_3,lift_K3_4 ids=barbell_heavy seeds=1234,5678
`3_1` 116/107 mm · `3_2` 122/137 · `3_3` **204/144** · `3_4` 134/126. `K3_3` produces
the single largest deviation from the input in the whole experiment on seed 1234 —
and none of it is a lift.
:::

::: clips arms=lift_K2_1,lift_K2_2,lift_K2_3,lift_K2_4 ids=barbell_heavy seeds=1234,5678
`2_1` 133/104 · `2_2` 128/126 · `2_3` 188/141 · `2_4` 156/150.
:::

::: note title="Why the negative result is load-bearing"
This prompt is what separates the two hypotheses about what the video model is
doing.

If it **corrected** bad motion, it would fix this one — an arm-raise labelled "lifts
a heavy barbell" is as wrong as the flail labelled "lifts a heavy box", and
[`box_heavy`](result-box-heavy.html) does get fixed.

If it **extends** what it is handed, it fixes only the case where the input already
resembled the action closely enough to be developed into it.

The second is what happens, in both directions of the pipeline. That is the single
most useful thing this prompt contributes, and it is
[carried forward as a limit](verdict.html) rather than treated as a failure of the
setup.
:::

## The numbers for this prompt

::: metrics src=results/analysis.json key=results where=prompt_id=barbell_heavy cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-jerk_ratio
Sorted by jerk ratio, worst first. The two rows above 3.0 are the seed-1234 loose
sets described above — large deviation, high roughness, no barbell.
:::

## Timing strip

::: clips arms=strip ids=barbell_heavy seeds=1234,5678 width=760px
The input above every returned motion, time-aligned.
:::

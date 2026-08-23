---
title: Result 4 — punch
nav: Result 4 · punch
lead: "A person throws right and left punches." Yes, partially. The video model extends a tentative guard into actual punches, and the round trip brings them back as motion — including full arm extension the input simply does not contain.
---

## What went in

The input is **a boxing guard with small arm movement that never reaches
extension**. It reads as tentative shadow-boxing.

Floor: 36 mm (s1234) and 37 mm (s5678). Clean.

::: clips arms=blue,lift_floor,lift_Kall ids=punch seeds=1234,5678 size=lg
Input, `floor`, `K = all`. Note `K = 9` on this prompt reaches 85/92 mm — the highest
`K = 9` figure in the experiment, because the input is the most energetic and nine
anchors leave real gaps between fast movements.
:::

## The returned motion

::: clips arms=blue,lift_K5,lift_K3_2 ids=punch seeds=1234,5678 size=lg
`K = 5` at 112 mm (s1234) and 128 mm (s5678); `K = 3_2` at 121 mm and 146 mm.
:::

::: key title="What we observed — yes, partially"
At `K = 5` and below, the video model **extends the guard into actual punches**, and
the round trip brings them back as motion.

The lifted rows track their sources pose for pose, **including the full arm
extension at frame 72 that the input simply does not contain.** That is the video
model supplying a missing part of the named action, recovered intact as 3D motion.
:::

## Source video beside returned motion

::: clips arms=vid_K5,lift_K5,vid_K3_2,lift_K3_2 ids=punch seeds=1234,5678
Source then return. This is the cleanest source-to-return correspondence in the
experiment — what is in the video is what comes back, with no invented content and
no second subject to confuse pose recovery.
:::

## The jerk question

::: key title="This is the prompt where jerk is not a defect"
The returned motion is **much jerkier than the input — jerk ratio 1.7 to 4.3.**
Everywhere else in this experiment that would be a warning sign.

Here it is not, because **a real punch *is* jerky.** The impulse at the end of an
extension is a genuine physical feature, and the input's smooth tentative guard is
the less physical of the two.

This is the single case in either experiment where higher jerk reads as more
physical rather than as noise — and it is the reason
[the numbers page](numbers.html) declines to use smoothness as a naturalness proxy.
:::

## Placement variants

::: clips arms=lift_K3_1,lift_K3_2,lift_K3_3,lift_K3_4 ids=punch seeds=1234,5678
`3_1` 121/146 mm · `3_2` 121/146 · `3_3` 162/155 · `3_4` 140/126.
:::

::: clips arms=lift_K2_1,lift_K2_2,lift_K2_3,lift_K2_4 ids=punch seeds=1234,5678
`2_1` 129/128 · `2_2` 153/150 · `2_3` 143/141 · `2_4` 151/126. Unusually flat across
placements — as in Experiment 2, an energetic input leaves placement less room to
matter.
:::

::: warn title="One thing to watch at K = 3_3"
[Experiment 2 noted](../exp2/result-punch.html) that at `K = 3_3` the video model
adds a **high kick at frame 96** — at which point the clip is no longer the prompt.
That kick is in the source video, so it is in the returned motion too. Worth seeing
in the grid above before treating `3_3` as a punch result.
:::

## The numbers for this prompt

::: metrics src=results/analysis.json key=results where=prompt_id=punch cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-jerk_ratio
Sorted by jerk ratio, highest first. Read the top rows against the clips above: the
roughest returns here are the ones with real punches in them.
:::

## Timing strip

::: clips arms=strip ids=punch seeds=1234,5678 width=760px
The input above every returned motion, time-aligned. Look along the rows for the
frames where the arm reaches full extension — present in the loose rows, absent in
the input and in `floor`.
:::

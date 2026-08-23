---
title: Result 5 — squat
nav: Result 5 · squat
lead: "A person squats down." Unusable. Pose recovery resolves this crouch front-to-back the wrong way, and it does so in the control column — before the video model is involved at all. Nothing in this row can be concluded from.
---

## The failure

::: warn title="This prompt fails in the floor column"
`squat` comes in at **353–356 mm — in `floor`**, the condition with no video model in
the loop at all. Every other clip's floor is 34–42 mm.

The input squats facing **away** from the camera, curled into a compact ball. Every
lifted row comes back squatting **towards** the camera.
:::

::: clips arms=blue,lift_floor,lift_Kall ids=squat seeds=1234,5678 size=lg
The input, `floor`, and `K = all`. The input faces away; both recoveries face
towards. No video model was involved in either of the right-hand cells.
:::

## Why it happens

A deeply folded crouch seen from **one fixed viewpoint** is close to front-back
ambiguous in silhouette. Curled into a ball, the shape you project is nearly the
same whichever way you are facing. GVHMR consistently resolves that ambiguity the
other way.

::: method title="It is not an alignment artefact"
Lifted clips are routinely rotated about the vertical axis onto their input's
heading, because GVHMR's absolute heading is arbitrary. So the obvious explanation
is a bad rotation.

It is not. A brute-force search over all rotations about the vertical axis finds
**no angle** that brings the two into agreement — the best is 277 mm at −90°, still
seven times any other clip's floor. **The recovered pose is genuinely a different
pose**, not the same pose viewed from elsewhere.

A yaw rotation cannot repair a front-to-back flip, which is why this clip stays
broken.
:::

## The consequence

::: key title="Every squat row must be discounted"
Because the floor already fails, **no column in this row says anything about the
video model.** The loose-set figures for `squat` (333–361 mm) are not "large
deviations caused by the video model" — they are the same front-back flip that
`floor` has, plus noise.

The yaw figure recorded for this clip in the manifest is meaningless, and `squat` is
excluded from every mean quoted in [The numbers](numbers.html). Including it would
just move every column together and hide the real spread.
:::

The clips below are included for completeness and for anyone who wants to confirm
the diagnosis. They should not be read as results.

::: clips arms=blue,lift_K5,lift_K3_2 ids=squat seeds=1234,5678 size=lg
`K = 5` (353/338 mm) and `K = 3_2` (336/351 mm). Compare each with `floor` above
rather than with the input — against `floor` they are barely different, which is the
tell that the video model is not what is causing the discrepancy.
:::

::: clips arms=vid_K5,lift_K5,vid_K3_2,lift_K3_2 ids=squat seeds=1234,5678
Source then return. **The source videos are fine.** Experiment 2 found this prompt
to be [its clearest re-timing result](../exp2/result-squat.html) — the video model
turns the four-second hold into repeated reps. All of that is visible on the left of
each pair, and all of it is lost on the right.
:::

::: note title="What was lost here is worth noting"
This is a genuinely annoying failure, because `squat` was Experiment 2's **best**
result. The video model turning a four-second static hold into two or three real
reps is exactly the kind of re-timing this project is looking for, and the round
trip cannot confirm it in 3D because the recovery step fails independently.
:::

## Why this matters beyond one clip

::: warn title="A squat is not an exotic pose"
It is the second-most common thing in a motion dataset. If a folded crouch from a
single fixed viewpoint cannot be recovered reliably, then **one clip in six failing
is a property of the capture setup, not bad luck.**

A second camera angle, or simply an off-axis camera, would very probably fix it.
That is worth doing before running this pipeline at any scale, and it is
[carried as the second caveat](verdict.html) on the verdict.
:::

## The numbers for this prompt

::: metrics src=results/analysis.json key=results where=prompt_id=squat cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=mpjpe_root_rel_mm
Every row sits in the 316–361 mm band, `floor` included. The **flatness** of this
column is the diagnosis: if the video model were responsible, `floor` would be low
and the loose sets high.
:::

## Timing strip

::: clips arms=strip ids=squat seeds=1234,5678 width=760px
The input above every returned motion. Click to open full size — the facing flip is
obvious across every row at once, which is the fastest way to see that the problem
is not condition-dependent.
:::

---
title: Fit quality
nav: Fit quality
lead: How much the joints-to-SMPL step distorted the T2M arm, per clip. Relevant because any artefact it introduces sits in the T2M column and nowhere else.
---

MotionGPT3 emits 22 HumanML3D joint positions. The T2M render needs SMPL
parameters — `poses`, `trans`, `betas` — so each joint sequence is fitted to a
neutral SMPL body with `betas = 0`. That fit is not exact, and its error is a
property of the T2M column alone.

## Why it is enforced this way

Because `betas = 0` is fixed, the body shape cannot absorb the mismatch between
the HumanML3D skeleton and SMPL's. Instead a single global scale is applied to the
target joints; it lands at approximately 0.96 for every clip. This keeps every
T2M clip on an identical body, so differences between T2M clips are differences in
motion and not in proportion.

## Residual per clip

Mean per-joint position error after fitting, and the worst single frame in each
clip.

::: metrics src=data/motions/manifest.json cols=prompt_id:prompt,seed:seed,generated_length:generated,length_fix:trim,target_scale:scale,fit_mpjpe_mm:MPJPE mm,fit_mpjpe_max_mm:worst frame mm sort=-fit_mpjpe_max_mm
All 27 T2M clips, sorted by worst-frame error. Mean residual runs roughly 9–17 mm
per clip; single-frame maxima run 27–95 mm, concentrated on the fast punch and
baseball motions where joint velocity is highest.
:::

## Reading these numbers

::: note title="Scale"
A 10 mm mean residual on a ~1.7 m body is well below the level at which pose
reads differently to the eye. A 95 mm single-frame maximum is not — that is
roughly a hand's width, and on a fast punch it is visible as a limb that snaps
slightly off-trajectory for a frame or two.
:::

::: warn title="Where this matters for the comparison"
The two prompts with the largest maxima are [`punch`](result-punch.html) and
[`baseball`](result-baseball.html) — both unloaded controls, and both fast. So the
arm that looks roughest on exactly the prompts where the T2M baseline is weakest is
partly a fitting artefact. Do not
score that against the motion model without checking the residual for the clip in
question.
:::

The `generated` and `trim` columns record MotionGPT3's own chosen sequence length
before it was cut to 80 frames — 128 frames on seed 0, 96 on seed 1, 84 on seed 2.
Nothing was time-warped; see
[Reading the clips](reading-the-clips.html) for why.

---
title: Reading the clips
nav: Reading the clips
lead: Five ways the three arms differ by construction rather than by finding. Each one is visible in the output and each one would be easy to mistake for a result.
---

The arms are not style-matched, length-matched or resolution-matched. That
follows from the pipeline, not from a choice made during analysis. Knowing which
differences were designed in is what makes the remaining differences readable.

## 1. Clip lengths differ between arms

The T2M arm is fixed at 80 frames @ 20 fps — exactly 4.00 s. The video arms are
5 s, and LTX-2.5 requires `num_frames = 8k + 1`, so they land at 121 frames
@ 24 fps = 5.04 s. The T2M clip is therefore about a second shorter than the
video clips beside it.

::: note
Every grid on the results pages loops all three arms independently, so they
drift out of phase within a few seconds. Use **▶ Replay in sync** in the toolbar
to restart everything from *t* = 0 when you want to compare timing rather than
pose.
:::

## 2. MotionGPT3 chooses its own clip length

The model generated 128 frames on seed 0, 96 on seed 1 and 84 on seed 2. The
length is drawn from the RNG, so it tracks the **seed**, not the prompt. Each
sequence was trimmed to its first 80 frames.

Nothing was time-warped. Resampling a motion to hit a target length changes how
fast the motion happens, and how fast it happens is the thing under observation.
The per-clip `generated_length` and `length_fix` fields record what each one
started at — see [Fit quality](fit-quality.html).

::: warn
Trimming to the first 80 frames means a motion that MotionGPT3 laid out over 128
frames is cut off partway. On seed 0 in particular, some clips end mid-action.
That is a truncation artefact, not the model stopping.
:::

## 3. The I2V seed frame is a neutral standing pose

Frame 0 of a MotionGPT3 clip is normally close to neutral standing. The I2V arm
is conditioned on frame 0, so it begins from an idle and has to invent the entire
action from the text — with the first frame pinning the body, camera and floor.

This was the specified setup rather than an accident, and it is the main thing to
watch in the I2V column: how long the model spends leaving the idle pose, and
whether it commits to the action at all.

## 4. The blue character survives into the video arms

The I2V arm is conditioned on a matte-blue untextured SMPL mesh standing on a
grey floor, and LTX-2.5 keeps that look rather than converting it to a
photographic person. The T2V arm, starting from text alone, produces photoreal
people.

So the two video columns are **not** style-matched to each other:

- **T2V vs. I2V** differ in appearance *and* in conditioning.
- **T2M vs. I2V** share an appearance, which makes pose and timing easier to
  compare directly.

::: clips arms=t2m,t2v,i2v ids=box_heavy seeds=0
One row, to make the point concretely: same prompt, three arms. The style gap
between the middle and right columns is a property of the conditioning image, not
a property of the motion.
:::

## 5. Audio is dropped

LTX-2.5 generates a soundtrack. It is discarded, so all three arms are silent and
nothing in the comparison depends on sound. The web transcodes on this site have
no audio track at all.

## Consequences for what can be claimed

::: method title="A fair comparison and an unfair one"
**Fair:** within one row of one grid, at one seed — same prompt, same seed,
arms side by side. And within one pair block — heavy row against light row, same
arm, same seed.

**Not fair:** across grids, across seeds, or "the video arms look more realistic
than the T2M arm". The last one is true and uninformative: one is a rendered mesh
and the others are generated video.
:::

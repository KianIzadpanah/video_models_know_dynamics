---
title: Result 5 — squat
nav: Result 5 · squat
lead: "A person squats down." The clearest re-timing in the sweep. MotionGPT3 drops into a squat and holds the bottom for four seconds; from K = 5 downward the video model refuses that and turns it into repeated reps.
---

## What went in

MotionGPT3 **drops into a squat and holds the bottom position for four seconds**.
Input energy 0.053 on both seeds — most of the clip is a static hold, so there is
very little frame-to-frame change.

A four-second hold at the bottom of a squat is not how people squat. It is a
plausible reading of the sentence and an implausible piece of human motion, which
makes it the ideal input for this question.

## Strong control

::: clips arms=blue,Kall,K9 ids=squat seeds=1234,5678 size=lg
`K = all` (0.89) and `K = 9` (0.87). The four-second hold is reproduced exactly.
This is also one of the pairs used for
[Test 2](does-it-work.html#test-2-k-all-reproduces-the-input).
:::

## The useful window

::: clips arms=blue,K5,K3_2 ids=squat seeds=1234,5678 size=lg
`K = 5` — ratio **2.78**, the highest single cell in the entire sweep — and
`K = 3_2` (2.63).
:::

::: key title="What we observed"
**From `K = 5` downward the video model refuses the hold and turns the clip into
repeated squat reps** — standing up and going back down two or three times within
the same 121 frames.

This is the cleanest re-timing result in the experiment. The model was handed five
poses and the freedom to decide what happens between them, and it chose to fill
the time with *more repetitions of the action* rather than with a static hold. That
is a decision about how the action is distributed in time, which is precisely the
kind of knowledge the experiment was built to look for.

**Stops looking stiff:** `K = 5`.

**Stops doing the action:** it never stops. Reps are still squatting — arguably a
more natural reading of "a person squats down" than a four-second hold at the
bottom.
:::

## Placement at K = 3

::: clips arms=K3_1,K3_2,K3_3,K3_4 ids=squat seeds=1234,5678
`3_1` 1.90 · `3_2` 2.63 · `3_3` 2.15 · `3_4` 2.40. **Every** placement more than
doubles the input here, including the ones that pin both ends — unique to this
prompt, and a direct consequence of the input containing so much dead time.
:::

## Placement at K = 2

::: clips arms=K2_1,K2_2,K2_3,K2_4 ids=squat seeds=1234,5678
`2_1` 1.72 · `2_2` 1.58 · `2_3` 2.01 · `2_4` 2.29.
:::

::: note title="Squat is also the off-grid test case"
This prompt at seed 1234 was re-run with a deliberately off-grid pinned index to
confirm the latent-grid constraint. See
[the off-grid negative control](does-it-work.html#extra-the-off-grid-negative-control).
:::

::: warn title="One thing squat does not survive"
In [Experiment 1](../exp1/result-squat.html) this prompt is the one clip that
**cannot be round-tripped at all** — pose recovery resolves the deeply folded
crouch front-to-back the wrong way, and the failure appears in the control column
before the video model is even involved. Nothing about that failure is visible
here; the videos on this page are fine.
:::

## The numbers for this prompt

::: metrics src=results/checks/energy.json key=results where=prompt_id=squat cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
Silhouette-change energy. This prompt has the highest ratios in the sweep because
its input has the most dead time to fill.
:::

## Timing strip

::: clips arms=strip ids=squat seeds=1234,5678 width=760px
Every condition, time-aligned. The reps are unmistakable here — count the descents
along each row.
:::

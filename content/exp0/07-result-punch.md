---
title: Result 4 — punch
nav: Result 4 · punch
lead: "A person throws right and left punches." The first of three unloaded controls — fast, repeated, ballistic motion where the interesting dynamics are inertial rather than gravitational.
---

## Why the unloaded prompts are here

If the video arms show more convincing dynamics on the loaded prompts, the obvious
objection is that they show more convincing dynamics on *everything* — that the
effect is about video realism, not about weight.

`punch`, [`squat`](result-squat.html) and [`baseball`](result-baseball.html) test
that. None involves carrying a load. A finding on the loaded pairs is only
interesting **relative to these three pages**.

::: note
There is no matched pair here, so this is a single row. Comparison is across the
row: same prompt, same seed, three arms.
:::

## The clips

::: clips arms=t2m,t2v,i2v ids=punch seeds=0,1,2 size=lg
`punch` — a fast, repeated, ballistic motion. This is also one of the two prompts
where the joints→SMPL fit residual is highest (see
[Fit quality](fit-quality.html)), so some of the roughness in the T2M column is
fitting error rather than model output.
:::

::: todo title="Observations — punch"
- Do the arms actually reach **extension**, in any of the three columns?
- Is the **alternation** right — left and right punches with recovery between, or
  undifferentiated flailing?
- Does hip rotation lead the arm, or does the arm move alone?
- Is the gap between T2M and the video arms **as large** as it was on the loaded
  pairs, smaller, or larger? This is the question the control prompts exist to
  answer.
:::

::: note title="What later experiments found on this prompt"
`punch` became one of the two positive results in
[Experiment 1](../exp1/result-punch.html): the video model extends a tentative guard
into actual punches with full arm extension, and the round trip brings them back as
motion. It is also the one case in the project where a *rougher* returned motion
reads as more physical rather than as noise — because a real punch is jerky.

If the T2M column here never reaches extension, that is precisely the gap the video
model later filled.
:::

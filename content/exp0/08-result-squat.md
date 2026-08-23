---
title: Result 5 — squat
nav: Result 5 · squat
lead: "A person squats down." Body weight only, slow, and highly stereotyped. Of the nine prompts this is the one a motion model should handle best — it is common in HumanML3D and needs no object.
---

## The clips

::: clips arms=t2m,t2v,i2v ids=squat seeds=0,1,2 size=lg
`squat` — no object, no implement, and a motion that appears constantly in motion
capture datasets. If the motion model is going to win anywhere, it should be here.
:::

::: todo title="Observations — squat"
- Is the **descent controlled**, or does the character drop?
- Is there a recognisable bottom position, and how long is it held?
- Is the drive back up present at all?
- **Does T2M actually win here?** This is the cleanest case for the motion model in
  the whole prompt set, so a loss on this prompt would be informative.
:::

::: note title="What later experiments found on this prompt"
`squat` produced the sharpest result and the sharpest failure in the project.

In [Experiment 2](../exp2/result-squat.html) MotionGPT3 drops into a squat and
**holds the bottom for four seconds** — a plausible reading of the sentence and an
implausible piece of human motion. From `K = 5` downward the video model refuses that
hold and turns it into repeated reps, the highest single re-timing effect in the
sweep.

In [Experiment 1](../exp1/result-squat.html) none of that could be confirmed in 3D,
because pose recovery resolves a deeply folded crouch front-to-back the wrong way —
and it does so in the control column, before the video model is involved.

If the T2M column here holds a long static bottom position, that is the input both
of those findings start from.
:::

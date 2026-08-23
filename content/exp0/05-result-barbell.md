---
title: Result 2 — barbell pair
nav: Result 2 · barbell (heavy/light)
lead: "A person lifts a heavy barbell from the ground" against "a person lifts a light barbell from the ground." Same single-word contrast as the box pair, but applied to an action with a learned, stereotyped form.
---

A barbell lift has a technique. That makes this pair a second, sharper question:
not just *does the model respond to the load word*, but *does it reproduce a
learned technique* rather than a generic bend-and-straighten.

## The clips

::: clips arms=t2m,t2v,i2v ids=barbell_heavy,barbell_light seeds=0,1,2
The `barbell` pair. Heavy above light.
:::

::: todo title="Observations — barbell"
As with the box pair, plus two things specific to this one:

- Does either video arm produce plausible **plate sizes** on the bar, and does
  plate size track the load word? That would be the model expressing weight
  through the *object* rather than through the body — a different mechanism
  entirely, and worth calling out separately if it happens.
- Is the bar path straight and close to the body, or does the model produce a
  generic lift with a barbell attached?
:::

## Cross-pair note

::: todo title="Do the two lift pairs agree?"
If the heavy/light contrast appears in one pair and not the other, say so and say
which. Two prompts is not enough to generalise from, but a disagreement between
them is more informative than either result alone.
:::

::: note title="What later experiments found on this prompt"
`barbell_heavy` became the clearest negative case in the project.
[Experiment 2](../exp2/result-barbell-heavy.html) found that MotionGPT3's clip is an
arm-raise rather than a lift, and that **no** conditioning set gets the video model
to draw a barbell — in direct contrast to the box. That comparison is what
established that the video prior *extends* what it is given rather than correcting
it.

Whatever you see in the T2M column here is the same output that finding rests on.
:::

Next: [the push pair](result-push.html), where the load difference is carried by
the noun rather than an adjective.

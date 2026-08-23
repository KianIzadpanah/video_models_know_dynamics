---
title: Result 6 — baseball
nav: Result 6 · baseball
lead: "A person hit a ball with baseball bat." Needs an implement, a target, and a full kinetic chain. The prompt's grammar is the specification's verbatim wording and was not corrected.
---

## The clips

::: clips arms=t2m,t2v,i2v ids=baseball seeds=0,1,2 size=lg
`baseball` — the most demanding of the three controls. It requires an object the
model has to place, a target it has to aim at, and a coordinated sequence from the
feet up.
:::

::: todo title="Observations — baseball"
- Is there a **weight shift onto the back foot** before the swing, and a pause?
- Do either video arm produce a **bat**? A ball?
- Is the rotation through contact fast relative to the wind-up, or is the whole
  motion one uniform speed?
- Like `punch`, this prompt has a high joints→SMPL fit residual (see
  [Fit quality](fit-quality.html)) — discount some of the T2M column's roughness
  accordingly.
:::

::: note title="What later experiments found on this prompt"
`baseball` came out **marginal** in both later experiments.
[Experiment 2](../exp2/result-baseball.html) found a leg lift and a rotation that
read as a batting stride at two conditioning sets and nowhere else, with no bat ever
drawn. [Experiment 1](../exp1/result-baseball.html) found the stride comes back as
motion, but with foot-skate roughly doubled — more dynamic, not more natural.
:::

---
title: The jump
nav: The jump
lead: The clip this experiment was built around. Uniform keyframes miss the airborne frame, entropy keyframes catch it, and the jump comes back.
---

## Control — the keyframes each chooser kept

::: clips arms=input,ctrl_K5_uniform,ctrl_K5_velmin,ctrl_K5_entropy,ctrl_K5_velent ids=jump seeds=1234,5678
:::

## Photoreal

::: clips arms=gen_K5_uniform,gen_K5_velmin,gen_K5_entropy,gen_K5_velent ids=jump seeds=1234,5678
Both seeds. Use the seed buttons in the toolbar to switch between them.
:::

## Recovered motion against the blend

::: clips arms=input,rec_K5_uniform,blend_K5_uniform,rec_K5_entropy,blend_K5_entropy ids=jump seeds=1234,5678
The blend interpolates in a straight line between the same keyframes. Under
`entropy` the model makes a jump of it, with a better countermovement beforehand than
the input had.
:::

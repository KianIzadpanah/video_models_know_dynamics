---
title: Photoreal outputs
nav: Photoreal outputs
lead: Eight of the 24 prompts, seed 1234, one row per prompt and one column per way of choosing the keyframes.
---

## Group A — movement roughly right

::: clips arms=input,gen_text_only,gen_K5_uniform,gen_K5_velmin,gen_K5_entropy,gen_K5_velent ids=jump,kick,throw,squat seeds=1234
:::

## Group B — movement wrong

::: clips arms=input,gen_text_only,gen_K5_uniform,gen_K5_velmin,gen_K5_entropy,gen_K5_velent ids=heavy_box,carry_tray,push_door,climb_ladder seeds=1234
Here no choice of frames can help, because every frame of the input is wrong.
:::

## The one clip where the veto changes the picks

::: clips arms=ctrl_K5_entropy,ctrl_K5_entropy_veto,gen_K5_entropy,gen_K5_entropy_veto ids=climb_ladder seeds=1234
:::

---
title: Photoreal outputs
nav: Photoreal outputs
lead: All 24 prompts, seed 1234, one column per way of choosing the five keyframes. Every condition and both seeds are on the per-motion pages.
---

## Group A — movement roughly right

::: clips arms=input,gen_text_only,gen_K5_uniform,gen_K5_velmin,gen_K5_entropy,gen_K5_velent ids=wave,raise_arm,sit_down,stand_up,walk,turn,squat,step_side,run,jump,kick,throw seeds=1234
:::

## Group B — movement wrong

::: clips arms=input,gen_text_only,gen_K5_uniform,gen_K5_velmin,gen_K5_entropy,gen_K5_velent ids=heavy_box,high_shelf,push_door,carry_tray,step_over,climb_ladder,crawl_under,step_up,tie_shoe,sit_cross,pirate_bird,lean_wall seeds=1234
In group B no choice of frames can help, because every frame of the input is wrong.
:::

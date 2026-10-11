---
title: Photoreal outputs
nav: Photoreal outputs
lead: All 24 prompts, seed 1234, under the six main ways of drawing the control. The other variants and both seeds are on the per-motion pages.
---

## Group A — movement roughly right

::: clips arms=input,gen_text_only,gen_K5_single,gen_K5_hold,gen_trunk_K5,gen_Kall,gen_dense_s06 ids=wave,raise_arm,sit_down,stand_up,walk,turn,squat,step_side,run,jump,kick,throw seeds=1234
:::

## Group B — movement wrong

::: clips arms=input,gen_text_only,gen_K5_single,gen_K5_hold,gen_trunk_K5,gen_Kall,gen_dense_s06 ids=heavy_box,high_shelf,push_door,carry_tray,step_over,climb_ladder,crawl_under,step_up,tie_shoe,sit_cross,pirate_bird,lean_wall seeds=1234
`heavy_box`: dense control copies the input's wrong hands-up gesture and tosses the box, while
`trunk + K5` carries it. `push_door`: no control pushes the door.
:::

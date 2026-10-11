---
title: Photoreal outputs
nav: Photoreal outputs
lead: All 24 prompts, seed 1234. `kick` is the clip the dots were meant to fix; `climb_ladder` is why the gate exists.
---

## Group A — movement roughly right

::: clips arms=input,gen_text_only,gen_trunk_K5,gen_trunk_ee_K3,gen_trunk_ee_K5,gen_trunk_ee_K8,gen_dense_s06 ids=wave,raise_arm,sit_down,stand_up,walk,turn,squat,step_side,run,jump,kick,throw seeds=1234
`kick`: a knee lift under `trunk + K5`, a real kick once the dots are added. `throw`: still a
bat swing on this seed.
:::

## Group B — movement wrong

::: clips arms=input,gen_text_only,gen_trunk_K5,gen_trunk_ee_K3,gen_trunk_ee_K5,gen_trunk_ee_K8,gen_dense_s06 ids=heavy_box,high_shelf,push_door,carry_tray,step_over,climb_ladder,crawl_under,step_up,tie_shoe,sit_cross,pirate_bird,lean_wall seeds=1234
`climb_ladder`: only `text only` climbs.
:::

---
title: Results
nav: Results
lead: Each row is one source video and the five ways of turning it into 3D animation. The source video is on the left.
---

## The cases that tell the story

::: clips arms=source,r_lift,r_lift_smooth,r_blend_uniform,r_inbetween_uniform,r_motion_text_uniform ids=climb_ladder__src_text,pirate_parrot__src_method,walk_jump__src_method,walk_wave__src_text,walk_wave__src_method seeds=best
`climb_ladder`: the lift climbs in place, and CondMDI looks natural but loses the climb.
`pirate_parrot`: a broken lift that CondMDI repairs. `walk_jump`: CondMDI recreates the
jump, and the blend drops it. `walk_wave`, both sources: the source video decides the
meaning.
:::

## Text-only source videos

::: clips arms=source,r_lift,r_lift_smooth,r_blend_uniform,r_inbetween_uniform,r_motion_text_uniform ids=run_jump__src_text,walk_stop_turn__src_text,pick_up__src_text,take_shelf__src_text,backpack_table__src_text,kneel_pick_stand__src_text seeds=best
:::

## Skeleton-controlled source videos

::: clips arms=source,r_lift,r_lift_smooth,r_blend_uniform,r_inbetween_uniform,r_motion_text_uniform ids=run_jump__src_method,walk_stop_turn__src_method,pick_up__src_method,take_shelf__src_method,backpack_table__src_method,kneel_pick_stand__src_method seeds=best
:::

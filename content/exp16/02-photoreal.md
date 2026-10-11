---
title: Photoreal outputs
nav: Photoreal outputs
lead: All twelve prompts, seed 1234. The mocap ground truth on the left, then text alone, the three keyframe sets with black between, and bad and hand-picked keyframes with the trunk.
---

## Simple, moderate, complex

::: clips arms=input,gen_text_only,gen_single_bad,gen_single_uniform,gen_single_hand,gen_trunkee_bad,gen_trunkee_hand ids=jump_obstacle,jumping_jacks,throw,getup_floor,lie_down_getup,cartwheels seeds=1234
:::

## Compound and out of distribution

::: clips arms=input,gen_text_only,gen_single_bad,gen_single_uniform,gen_single_hand,gen_trunkee_bad,gen_trunkee_hand ids=squats_run,walk_dribble,duck_walk,walk_back_tiptoe,robot_walk,airplane_run seeds=1234
`jumping_jacks` and `duck_walk`: the black-between columns stand or walk, and the trunk
columns do the action. `walk_back_tiptoe` fails in every column.
:::

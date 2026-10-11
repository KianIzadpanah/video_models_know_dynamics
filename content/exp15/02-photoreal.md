---
title: Photoreal outputs
nav: Photoreal outputs
lead: The nine original prompts, seed 1234. Text alone, then bad and hand-picked keyframes with black between, then with the trunk, then with the staged prompt added.
---

## Simple

::: clips arms=input,gen_text_only,gen_text_only_staged,gen_single_bad,gen_single_hand,gen_trunkee_hand,gen_trunkee_hand_staged ids=walk_wave,run_jump,walk_stop_turn seeds=1234
:::

## Moderate

::: clips arms=input,gen_text_only,gen_text_only_staged,gen_single_bad,gen_single_hand,gen_trunkee_hand,gen_trunkee_hand_staged ids=pick_up,climb_ladder,take_shelf seeds=1234
:::

## Complex

::: clips arms=input,gen_text_only,gen_text_only_staged,gen_single_bad,gen_single_hand,gen_trunkee_hand,gen_trunkee_hand_staged ids=pirate_parrot,backpack_table,kneel_pick_stand seeds=1234
`kneel_pick_stand`: the keyframes override "kneel", so most controlled clips squat.
:::

::: note
Uniform keyframes are left off these grids because they look the same as hand-picked
ones. They are on the [Dense vs sparse](dense-vs-sparse.html) page.
:::

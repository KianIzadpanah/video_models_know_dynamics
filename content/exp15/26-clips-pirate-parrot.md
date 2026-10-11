---
title: pirate_parrot — every clip
nav: Clips · pirate_parrot
lead: "a pirate pets the parrot sitting on his shoulder" — every condition, every seed. Use the seed buttons in the toolbar to switch seeds, or "all" to see them side by side.
---

## Control

::: clips arms=input,ctrl_single_bad,ctrl_single_uniform,ctrl_single_hand ids=pirate_parrot seeds=1234,5678,9012
:::

::: clips arms=ctrl_trunkee_bad,ctrl_trunkee_uniform,ctrl_trunkee_hand ids=pirate_parrot seeds=1234,5678,9012
:::

## Photoreal output

::: clips arms=gen_text_only,gen_text_only_staged,gen_single_bad,gen_single_uniform,gen_single_hand ids=pirate_parrot seeds=1234,5678,9012
:::

::: clips arms=gen_trunkee_bad,gen_trunkee_uniform,gen_trunkee_hand,gen_trunkee_hand_staged ids=pirate_parrot seeds=1234,5678,9012
:::

## Recovered motion

::: clips arms=rec_text_only,rec_text_only_staged,rec_single_bad,rec_single_uniform,rec_single_hand ids=pirate_parrot seeds=1234,5678,9012
:::

::: clips arms=rec_trunkee_bad,rec_trunkee_uniform,rec_trunkee_hand,rec_trunkee_hand_staged ids=pirate_parrot seeds=1234,5678,9012
:::

::: note
Seed 9012 has no recovered motion for `text only` and `staged text`: GVHMR found no person
in those two videos.
:::

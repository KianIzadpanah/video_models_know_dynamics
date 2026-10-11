---
title: tie_shoe — every clip
nav: Clips · tie_shoe
lead: "a person kneels down and ties a shoelace" — every condition, every seed. Use the seed buttons in the toolbar to switch seeds, or "all" to see them side by side.
---

## Control

::: clips arms=input,ctrl_Kall,ctrl_K5_uniform,ctrl_K5_velmin ids=tie_shoe seeds=1234,5678
:::

::: clips arms=ctrl_K5_plaus,ctrl_K5_entropy,ctrl_K5_entropy_veto,ctrl_K5_velent ids=tie_shoe seeds=1234,5678
:::

## Photoreal output

::: clips arms=gen_text_only,gen_Kall,gen_K5_uniform,gen_K5_velmin ids=tie_shoe seeds=1234,5678
:::

::: clips arms=gen_K5_plaus,gen_K5_entropy,gen_K5_entropy_veto,gen_K5_velent ids=tie_shoe seeds=1234,5678
:::

## Recovered motion

::: clips arms=rec_text_only,rec_Kall,rec_K5_uniform,rec_K5_velmin ids=tie_shoe seeds=1234,5678
:::

::: clips arms=rec_K5_plaus,rec_K5_entropy,rec_K5_entropy_veto,rec_K5_velent ids=tie_shoe seeds=1234,5678
:::

## Blend — no model

::: clips arms=blend_Kall,blend_K5_uniform,blend_K5_velmin,blend_K5_plaus ids=tie_shoe seeds=1234,5678
:::

::: clips arms=blend_K5_entropy,blend_K5_entropy_veto,blend_K5_velent ids=tie_shoe seeds=1234,5678
:::

---
title: step_over — every clip
nav: Clips · step_over
lead: "a person steps over an obstacle on the ground" — every condition, every seed. Use the seed buttons in the toolbar to switch seeds, or "all" to see them side by side.
---

## Control

::: clips arms=input,ctrl_Kall,ctrl_K5_uniform,ctrl_K5_velmin ids=step_over seeds=1234,5678
:::

::: clips arms=ctrl_K5_plaus,ctrl_K3_uniform,ctrl_K3_velmin,ctrl_K3_plaus ids=step_over seeds=1234,5678
:::

## Photoreal output

::: clips arms=gen_text_only,gen_Kall,gen_K5_uniform,gen_K5_velmin ids=step_over seeds=1234,5678
:::

::: clips arms=gen_K5_plaus,gen_K3_uniform,gen_K3_velmin,gen_K3_plaus ids=step_over seeds=1234,5678
:::

## Recovered motion

::: clips arms=rec_text_only,rec_Kall,rec_K5_uniform,rec_K5_velmin ids=step_over seeds=1234,5678
:::

::: clips arms=rec_K5_plaus,rec_K3_uniform,rec_K3_velmin,rec_K3_plaus ids=step_over seeds=1234,5678
:::

## Blend — no model

::: clips arms=blend_Kall,blend_K5_uniform,blend_K5_velmin,blend_K5_plaus ids=step_over seeds=1234,5678
:::

::: clips arms=blend_K3_uniform,blend_K3_velmin,blend_K3_plaus ids=step_over seeds=1234,5678
:::

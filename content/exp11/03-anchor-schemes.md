---
title: Anchor schemes
nav: Anchor schemes
lead: The same prompt under three ways of choosing the anchor frames. The result is negative — they look the same.
---

## K = 5

::: clips arms=gen_K5_uniform,gen_K5_velmin,gen_K5_plaus ids=heavy_box,carry_tray,high_shelf,climb_ladder seeds=1234
:::

## K = 3

::: clips arms=gen_K3_uniform,gen_K3_velmin,gen_K3_plaus ids=heavy_box,carry_tray,high_shelf,climb_ladder seeds=1234
Neither velmin nor plaus recovers anything that uniform lost.
:::

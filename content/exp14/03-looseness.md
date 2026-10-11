---
title: How loose?
nav: How loose?
lead: The full sweep — three keyframe counts, with and without the wrist and ankle dots — on four prompts.
---

## Trunk only

::: clips arms=gen_trunk_K3,gen_trunk_K5,gen_trunk_K8 ids=kick,throw,heavy_box,walk seeds=1234
:::

## Trunk + wrist and ankle dots

::: clips arms=gen_trunk_ee_K3,gen_trunk_ee_K5,gen_trunk_ee_K8 ids=kick,throw,heavy_box,walk seeds=1234
Compare `kick` row by row: the dots matter far more than the number of keyframes.
:::

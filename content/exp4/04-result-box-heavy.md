---
title: Result 1 — box_heavy
nav: Result 1 · box_heavy
lead: Motion "a person lifts a heavy box from the floor" as depth control; appearance "a muscular male warehouse worker in a warehouse". 121 frames @ 25 fps, 704×704, seeds 1234 and 5678, five conditions.
---

## Input motion, and the control tracks it became — dense, K = 5, K = 2

::: clips arms=input,depth_dense,depth_K5,depth_K2 ids=box_heavy seeds=1234,5678
:::

## dense — every latent frame, 0·8·16·…·120 (16 frames)

::: clips arms=depth_dense,vid_dense,lift_dense ids=box_heavy seeds=1234,5678 size=lg
:::

## K = 8 — 0·16·32·48·72·88·104·120

::: clips arms=depth_K8,vid_K8,lift_K8 ids=box_heavy seeds=1234,5678 size=lg
:::

## K = 5 — 0·32·64·88·120

::: clips arms=depth_K5,vid_K5,lift_K5 ids=box_heavy seeds=1234,5678 size=lg
:::

## K = 3 — 0·64·120

::: clips arms=depth_K3,vid_K3,lift_K3 ids=box_heavy seeds=1234,5678 size=lg
:::

## K = 2 — 0·120, the two ends

::: clips arms=depth_K2,vid_K2,lift_K2 ids=box_heavy seeds=1234,5678 size=lg
:::

## Recovered SMPL across the sweep — dense → K = 8 → K = 5 → K = 3 → K = 2

::: clips arms=lift_dense,lift_K8,lift_K5,lift_K3,lift_K2 ids=box_heavy seeds=1234,5678
:::

## Timing strip — control, photoreal and recovered, time-aligned

::: clips arms=strip ids=box_heavy seeds=1234,5678 width=1000px
:::

[Observations, numbers and caveats for this motion →](observations.html#box-heavy)

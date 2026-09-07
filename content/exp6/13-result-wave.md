---
title: Result 10 — wave
nav: Result 10 · wave
lead: "a man waving one arm" — 169 frames @ 25 fps, 1216×704, seed 1234, five conditioning densities. Essentially flat. K = 8 is marginally closer to the input than dense.
---

## The input clip, and the control tracks it became — dense, K = 5, K = 2

::: clips arms=input,depth_dense,depth_K5,depth_K2 ids=wave seeds=1234
:::

## dense — every latent frame, 0·8·16·…·168 (22 frames)

::: clips arms=depth_dense,vid_dense,lift_dense ids=wave seeds=1234 size=lg
:::

## K = 8 — 0·24·48·72·96·120·144·168

::: clips arms=depth_K8,vid_K8,lift_K8 ids=wave seeds=1234 size=lg
:::

## K = 5 — 0·40·88·128·168

::: clips arms=depth_K5,vid_K5,lift_K5 ids=wave seeds=1234 size=lg
:::

## K = 3 — 0·88·168

::: clips arms=depth_K3,vid_K3,lift_K3 ids=wave seeds=1234 size=lg
:::

## K = 2 — 0·168, the two ends

::: clips arms=depth_K2,vid_K2,lift_K2 ids=wave seeds=1234 size=lg
:::

## Photoreal across the sweep — dense → K = 8 → K = 5 → K = 3 → K = 2

::: clips arms=vid_dense,vid_K8,vid_K5,vid_K3,vid_K2 ids=wave seeds=1234
:::

## Recovered SMPL across the sweep — dense → K = 8 → K = 5 → K = 3 → K = 2

::: clips arms=lift_dense,lift_K8,lift_K5,lift_K3,lift_K2 ids=wave seeds=1234
:::

## Timing strip — control, photoreal and recovered, time-aligned

::: clips arms=strip ids=wave seeds=1234 width=1000px
:::

[Observations, numbers and caveats for this clip →](observations.html#wave)

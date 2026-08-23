---
title: Result 1 — box_heavy
nav: Result 1 · box_heavy
lead: "a person lifts a heavy box from the floor" — 121 frames @ 25 fps, 512×512, seeds 1234 and 5678, eleven conditioning sets.
---

## Strong control — every 8th frame, then every 16th

::: clips arms=blue,Kall,K9 ids=box_heavy seeds=1234,5678 size=lg
:::

## The useful window — 0·32·64·88·120, then 64·88·120

::: clips arms=blue,K5,K3_2 ids=box_heavy seeds=1234,5678 size=lg
:::

## Placement at K = 3 — 0·64·120 / 64·88·120 / 32·64·88 / 0·32·64

::: clips arms=K3_1,K3_2,K3_3,K3_4 ids=box_heavy seeds=1234,5678
:::

## Placement at K = 2 — 0·120 / 64·120 / 32·88 / 0·64

::: clips arms=K2_1,K2_2,K2_3,K2_4 ids=box_heavy seeds=1234,5678
:::

## Timing strip — all eleven sets, time-aligned

::: clips arms=strip ids=box_heavy seeds=1234,5678 width=760px
:::

[Observations, numbers and caveats for this prompt →](observations.html#box-heavy)

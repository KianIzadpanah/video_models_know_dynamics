---
title: Result 2 — barbell_heavy
nav: Result 2 · barbell_heavy
lead: "a person lifts a heavy barbell from the ground" — 121 frames @ 25 fps in and out, 512×512, seeds 1234 and 5678, twelve conditions.
---

## Control and strong control — floor, then every 8th frame

::: clips arms=blue,lift_floor,lift_Kall ids=barbell_heavy seeds=1234,5678 size=lg
:::

## The two loose values — 0·32·64·88·120, then 64·88·120

::: clips arms=blue,lift_K5,lift_K3_2 ids=barbell_heavy seeds=1234,5678 size=lg
:::

## Source video beside returned motion — K = 5 and K = 3_2

::: clips arms=vid_K5,lift_K5,vid_K3_2,lift_K3_2 ids=barbell_heavy seeds=1234,5678
:::

## Placement at K = 3 — returned motion, 0·64·120 / 64·88·120 / 32·64·88 / 0·32·64

::: clips arms=lift_K3_1,lift_K3_2,lift_K3_3,lift_K3_4 ids=barbell_heavy seeds=1234,5678
:::

## Placement at K = 2 — returned motion, 0·120 / 64·120 / 32·88 / 0·64

::: clips arms=lift_K2_1,lift_K2_2,lift_K2_3,lift_K2_4 ids=barbell_heavy seeds=1234,5678
:::

## Timing strip — input above every return, all twelve conditions

::: clips arms=strip ids=barbell_heavy seeds=1234,5678 width=1000px
:::

[Observations, numbers and caveats for this prompt →](observations.html#barbell-heavy)

---
title: Photoreal outputs
nav: Photoreal outputs
lead: All nine clips, seed 1234. The input motion on the left, then depth control, then the skeleton with its control released progressively earlier.
---

::: clips arms=input,gen_depth_dense,gen_skel_100,gen_skel_58,gen_skel_28,gen_skel_09 ids=squat,walk,run,jump,kick,stand_up,throw,turn,wave seeds=1234
Read across a row: `depth` and `skeleton 100%` differ only in the control signal; the
next three columns release that skeleton after 7, 6 and 5 of the 8 steps.
:::

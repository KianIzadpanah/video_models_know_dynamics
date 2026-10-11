---
title: Recovered motion and blend
nav: Recovered motion & blend
lead: The motion pulled back out of the video, next to a straight-line blend between the same anchors.
---

::: clips arms=input,rec_Kall,rec_K5,blend_K5,rec_K2,blend_K2 ids=sit_down,kick,wave,jump seeds=1234
`sit_down`: the person sits on a chair the input never had. `kick`: the cleanest
refinement, at `K = 5`. `wave` still waves at `K = 2`, carried by the text alone.
`jump`: once its airborne frame is missed, the jump is gone.
:::

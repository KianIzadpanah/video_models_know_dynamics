---
title: Model vs blend
nav: Model vs blend
lead: What the video model fills in between the anchors, against a straight-line blend between the same anchors. Both are shown as SMPL on the same neutral body.
---

## K = 3 and K = 2

::: clips arms=input,rec_K3,blend_K3,rec_K2,blend_K2 ids=squat,walk,kick,throw seeds=1234
`Recovered` is the motion pulled back out of the photoreal video, and `Blend` is the
interpolation with no model. In `squat` at `K = 3`, around frame 44, the blend is at a
half-crouch while the model reaches a full crouch. At `K = 2`, on `kick` and `squat`,
the model ends up closer to the input than the blend does.
:::

## Every density, one clip

::: clips arms=rec_Kall,rec_K8,rec_K5,rec_K3,rec_K2 ids=squat seeds=1234 heads=on
:::

::: clips arms=blend_Kall,blend_K8,blend_K5,blend_K3,blend_K2 ids=squat seeds=1234
Top: the model's motion at each K. Bottom: the blend for the same anchors.
:::

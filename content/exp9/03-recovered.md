---
title: Recovered motion
nav: Recovered motion
lead: The motion GVHMR pulls back out of each photoreal clip, for the four clips that tell the story.
---

::: clips arms=input,rec_text_only,rec_root,rec_root_facing,rec_root_ee,rec_skeleton_dense ids=run,walk,throw,wave seeds=1234
`run`: the trajectory produces a run. `walk`: under `root` the person crosses the frame
along the path. `throw`: the limb tracks recover the arc. `wave`: the pelvis does not
move, so a pelvis track adds nothing.
:::

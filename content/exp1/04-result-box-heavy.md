---
title: Result 1 — box_heavy
nav: Result 1 · box_heavy
lead: "A person lifts a heavy box from the floor." Yes, clearly. The motion that comes back is a purposeful kneel-and-reach where the input was a vague flail — and this is also the page that shows most sharply why the source video has to be looked at.
---

## What went in

MotionGPT3's clip is a **vague crouch-and-flail**. At frame 72 it puts both arms
over the head, in a pose no one lifting a box would produce. `floor` reproduces
that faithfully, arms and all — which is exactly what a good control column should
do.

Floor: 36 mm both seeds. Clean.

::: clips arms=blue,lift_floor,lift_Kall ids=box_heavy seeds=1234,5678 size=lg
Input, `floor`, `K = all`. The arms-overhead moment at f72 survives all three.
:::

## The returned motion

::: clips arms=blue,lift_K5,lift_K3_2 ids=box_heavy seeds=1234,5678 size=lg
Input against the two loose values. `K = 5` at 117 mm (s1234) and 80 mm (s5678);
`K = 3_2` at 139 mm and 143 mm.
:::

::: key title="What we observed — yes, clearly"
At **`K = 5`** what comes back is a calmer, plausible crouch-and-reach. **The
arms-overhead moment is gone.**

At **`K = 3_2` / `K = 2_2`, seed 1234**, the source video has the character kneel and
reach into an invented cardboard box, and GVHMR recovers that motion cleanly —
correctly excluding the box from the body. What comes back is a purposeful
kneel-and-reach: **a better rendition of "lifts a heavy box from the floor" than
anything that went in.**
:::

## Source video beside returned motion

This is the pairing that matters. Left cell of each pair is the video GVHMR was
given; right cell is the motion it gave back.

::: clips arms=vid_K5,lift_K5,vid_K3_2,lift_K3_2 ids=box_heavy seeds=1234,5678
`K = 5` and `K = 3_2`, source then return. On seed 1234 at `K = 3_2` you can watch the
kneel-and-reach into the invented box on the left, and the same motion cleanly
recovered on the right.
:::

::: warn title="Now look at seed 5678 at K = 3_2 — the most important clip in the experiment"
Its first half is **not the blue character at all**. The video model drew a
photographic person in pink pushing a hand truck alongside it. GVHMR tracked one
subject through a two-person scene and returned smooth, entirely plausible SMPL for
it.

**That lift is meaningless for the first ~60 frames, and it looks fine.** Nothing in
the returned motion signals the problem. Switch the seed selector above to 5678 and
compare the two cells.

It is the clearest example in the experiment of why the source video has to be
looked at, and it is the reason every page here shows both sides.
:::

## Where the action comes from

The placement variants answer this cleanly, because they move the free run around
while holding everything else fixed.

::: clips arms=lift_K3_1,lift_K3_2,lift_K3_3,lift_K3_4 ids=box_heavy seeds=1234,5678
Returned motion at all four `K = 3` placements. `3_1` 113/128 mm · `3_2` 139/143 ·
`3_3` 195/122 · `3_4` 168/151.
:::

::: clips arms=lift_K2_1,lift_K2_2,lift_K2_3,lift_K2_4 ids=box_heavy seeds=1234,5678
Returned motion at all four `K = 2` placements. `2_1` 139/114 · `2_2` 134/131 ·
`2_3` **233/208** · `2_4` 121/147.
:::

::: key title="The first-half sets show where the action comes from"
`K3_4` (0, 32, 64) and `K2_4` (0, 64) pin the **start** and leave the tail free. They
are the mirror image of `K3_2` / `K2_2`: the character stands normally through the
pinned first half, then from about frame 70 a large cardboard box appears, is picked
up, and is carried off — **and the round trip brings that carrying motion back
intact.**

Same prompt, same seed, same model. Only *which half was pinned* changed, and the
lift is a different, complete action each time.

**The video prior has the action available, and the conditioning decides *when* it
is allowed to happen.** That is the same conclusion
[Experiment 2 reached](../exp2/placement.html#where-the-invented-content-lands) from
the video side — confirmed here in recovered 3D motion.
:::

## Source video beside returned motion — the placement pairs

::: clips arms=vid_K3_2,lift_K3_2,vid_K3_4,lift_K3_4 ids=box_heavy seeds=1234,5678
Head free (left pair) against tail free (right pair). The box appears at the start
in one and at the end in the other, and comes back as motion both times.
:::

## The numbers for this prompt

::: metrics src=results/analysis.json key=results where=prompt_id=box_heavy cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=mpjpe_root_rel_mm
Joint error is root-relative, against the input motion. `jerk_ratio` above 1 means
the returned motion is rougher than the input. See
[The numbers](numbers.html) for why neither of those settles the question.
:::

## Timing strip

::: clips arms=strip ids=box_heavy seeds=1234,5678 width=760px
The input above every returned motion, time-aligned. Click to open full size — this
is where the pink-person passage on seed 5678 is unmistakable.
:::

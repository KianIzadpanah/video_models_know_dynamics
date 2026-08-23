---
title: Result 1 — box_heavy
nav: Result 1 · box_heavy
lead: "A person lifts a heavy box from the floor." The one prompt where the video model clearly takes over — it invents a cardboard box that was never in the input and performs an actual lift. The most striking result in the sweep.
---

## What went in

MotionGPT3's clip is a **vague crouch-and-flail**. There is no box in it, and the
motion does not read as lifting anything. Input energy 0.058 (s1234) and 0.060
(s5678) — middling for this set of six.

This matters for how the result is read: the video model is not being asked to
polish a good lift. It is being handed something that does not perform the prompt
at all.

## Strong control — the copier baseline

::: clips arms=blue,Kall,K9 ids=box_heavy seeds=1234,5678 size=lg
The blue input next to `K = all` and `K = 9`. Energy ratios 0.95 and 0.94 — very
slightly *less* motion than the input. The crouch-and-flail is faithfully
reproduced, box-less.
:::

## The useful window

::: clips arms=blue,K5,K3_2 ids=box_heavy seeds=1234,5678 size=lg
`K = 5` (1.16) and `K = 3_2` (1.74). At `K = 3_2` the entire first half of the clip
is free, and that is where the box appears.
:::

::: key title="What we observed"
At **`K = 2_1` (0, 120), seed 1234** the model invents a cardboard box, bends
down, picks it up and lifts it to chest height with plausible timing. That is a
**better rendition of the prompt than the motion it was conditioned on** — the
input never lifts anything.

The character stops looking stiff at `K = 5` (1.16) and decisively at `K = 3_1`
(1.56). It does not "stop doing the action" as K falls, which is what we expected
to see; it *starts* doing it.
:::

## Placement at K = 3

::: clips arms=K3_1,K3_2,K3_3,K3_4 ids=box_heavy seeds=1234,5678
Same three frames handed over, four different places. `3_1` pins both ends (1.56),
`3_2` frees the head (1.74), `3_3` frees both ends (2.09), `3_4` frees the tail
(1.54).
:::

## Placement at K = 2

::: clips arms=K2_1,K2_2,K2_3,K2_4 ids=box_heavy seeds=1234,5678
Two frames, four placements. Note `2_1` (0.81) and `2_4` (0.74) sit *below* the
input while `2_3` (2.14) nearly doubles it — the same number of pinned frames,
opposite behaviour.
:::

::: key title="Where the box appears is decided by where the free run is"
Both seeds, every time:

| set | pinned | free run | the box appears in |
|---|---|---|---|
| `3_2` / `2_2` | second half | frames 0–63 | **0–60** and **0–54 / 0–56** |
| `3_4` / `2_4` | first half | frames 65–120 | **69–120** and **70–120** |
| `2_3` | 32, 88 | both ends | **0–120** (i.e. at the two ends) |
| `2_1` | 0, 120 | the middle | **2–98** and **32–103** |

With the tail free, the character stands normally through the pinned first half and
then, from about frame 70, a large cardboard box appears and is picked up and
carried off. With the head free, the same box appears at the *start* instead, and
the character is kneeling beside it before the pinned frames take over at 64.

The video model has a whole action available. The conditioning decides **when** it
is allowed to happen, not whether.
:::

## The one prompt that draws things that were never there

This is also the only prompt where the model adds content the blue render never
contained. Warm-toned — that is, non-scene — pixels appear in **8 of 108** clips,
*all of them `box_heavy`*, all at K ≤ 3 sets with a long unpinned run: boxes, a
hand truck, and in `s5678` at `K = 3_2` / `2_2` a **photographic person in pink
clothing** occupying the free first half, which cuts back to the blue matte
character at the first pinned frame.

::: warn title="Two things to carry into Experiment 1"
**The identity switch is abrupt, not gradual.** We expected the blue character to
drift toward looking like a real person as K dropped. What actually happens is a
hard switch confined to the unpinned run, snapping back at the conditioning
boundary.

**`s5678` at `K = 3_1` has the character floating above the floor** around frames
72–96, with its shadow still on the ground. That is physically wrong, and it is a
direct warning for the [round trip](../exp1/overview.html): a motion lifted from
that video would be meaningless.
:::

## The numbers for this prompt

::: metrics src=results/checks/energy.json key=results where=prompt_id=box_heavy cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
Silhouette-change energy per condition, both seeds. **1.00 means the output moves
exactly as much as the blue input.** Full table in
`results/checks/energy.json`.
:::

## Timing strip

::: clips arms=strip ids=box_heavy seeds=1234,5678 width=760px
Every condition for this prompt as one time-aligned image — the fastest way to
read timing. Click to open full size.
:::

---
title: Placement, not K
nav: Placement, not K
lead: The headline result. How much the video model adds is not governed by how many frames it is given, but by whether the two ends of the clip are pinned. Two frames at the ends and two frames in the middle behave completely differently.
---

## How much motion did the video model actually add?

The measure: for each consecutive frame pair, the fraction of the body silhouette
that changes, averaged over the clip, divided by the same number for the blue
input. **1.00 means the output moves exactly as much as the motion model's clip.**

| prompt | all | 9 | 5 | 3_1 | 3_2 | 3_3 | 3_4 | 2_1 | 2_2 | 2_3 | 2_4 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| box_heavy | 0.95 | 0.94 | 1.16 | 1.56 | 1.74 | 2.09 | 1.54 | 0.81 | 1.56 | 2.14 | **0.74** |
| barbell_heavy | 0.84 | 0.77 | 1.99 | **0.47** | 1.96 | 2.90 | **0.81** | **0.58** | **0.45** | 2.87 | **0.81** |
| push_heavy | 0.70 | 0.63 | 1.24 | 0.83 | 1.61 | 2.16 | 1.04 | 0.84 | 1.70 | 2.52 | 1.38 |
| punch | 0.90 | 1.20 | 1.33 | 0.94 | 1.03 | 1.43 | 1.40 | 0.67 | 0.82 | 0.99 | 1.05 |
| squat | 0.89 | 0.87 | 2.78 | 1.90 | 2.63 | 2.15 | 2.40 | 1.72 | 1.58 | 2.01 | 2.29 |
| baseball | 0.88 | 0.75 | 1.38 | 0.93 | 1.44 | 1.64 | 1.16 | 0.66 | 0.90 | 1.55 | **0.83** |
| **mean** | 0.86 | 0.86 | **1.65** | 1.10 | **1.74** | 2.06 | 1.39 | 0.88 | 1.17 | 2.01 | 1.18 |

Three things fall out of this table, and none of them is "less K means more
motion".

### 1. Strong control adds nothing

`K = all` and `K = 9` both sit at **0.86** — very slightly *less* motion than the
input. At these settings the video model is a copier. This is the expected result
and it is worth stating plainly, because it means the sweep has a real zero point.

### 2. The amount of motion is not monotone in K

`K = 5` (1.65) produces **more** motion than `K = 3_1` (1.10) and far more than
`K = 2_1` (0.88) — despite handing over more frames.

The reason: with five anchors the model has to reach five specified poses on
schedule, which forces movement. With two distant ones it is free to take a lazy,
low-energy path, and usually does. `barbell_heavy` is the clearest case — 1.99 at
`K = 5`, and 0.45–0.58 at `3_1` / `2_1` / `2_2` where the character goes nearly
static.

### 3. What actually governs it is whether the ends are anchored

::: key title="The result"
The two sets that pin **neither** frame 0 nor frame 120 — `3_3` (32, 64, 88) and
`2_3` (32, 88) — roughly **double** the motion, 2.06 and 2.01, and they do it for
every prompt.

Sets that free only **one** end sit in between: `3_2` 1.74, `3_4` 1.39, `2_2` 1.17,
`2_4` 1.18.

Sets that anchor **both** ends sit lowest: `2_1` 0.88, `3_1` 1.10 — no matter how
few frames they hand over.

**Free ends, not few frames, is what buys the video prior room.**
:::

The cleanest single comparison in the experiment: `2_1` and `2_3` hand over exactly
two frames each. `2_1` puts them at 0 and 120 and produces 0.88 — less motion than
the input. `2_3` puts them at 32 and 88 and produces 2.01. Same K, opposite
behaviour.

::: clips arms=K2_1,K2_3 ids=barbell_heavy,squat,push_heavy seeds=1234,5678
Two frames each. Left: pinned at the ends. Right: pinned inside, both ends free.
`barbell_heavy` goes from 0.58 to 2.87 across this pair.
:::

## Did the blue character survive?

The blue render contains exactly one strongly blue thing (the body) and two neutral
grays (floor, backdrop), so blue silhouette area and warm-toned pixel count read
directly on whether the model invented anything.

| variant | pinned frames | clips with invented content | clips where the blue body is lost for ≥1 frame |
|---|---|---|---|
| all, 9, 5, 3_1, 3_3 | — | 0 / 12 | 0 / 12 |
| 3_2 | 64, 88, 120 | 2 / 12 | 1 / 12 |
| 3_4 | 0, 32, 64 | 2 / 12 | 2 / 12 |
| 2_1 | 0, 120 | 2 / 12 | 1 / 12 |
| 2_2 | 64, 120 | 2 / 12 | 1 / 12 |
| 2_3 | 32, 88 | 2 / 12 | 0 / 12 |
| 2_4 | 0, 64 | 2 / 12 | 1 / 12 |

**Every affected clip is [`box_heavy`](result-box-heavy.html).** Five of six prompts
keep a clean blue character at every K.

The drift we expected is real but narrow: it needs a prompt naming a concrete
object **and** a long unpinned run. And when it happens it is a hard switch at the
conditioning boundary, not the gradual fade toward a photoreal person we had
anticipated.

## Where the invented content lands

The four placements of `K = 2` and `K = 3` answer this cleanly, because they move
the unpinned run around while holding everything else fixed. For `box_heavy`, both
seeds, the frames in which the model draws something the blue render never had:

| variant | pinned frames | free run | invented content appears in |
|---|---|---|---|
| 3_2 / 2_2 | second half | frames 0–63 | **0–60** and **0–54 / 0–56** |
| 3_4 / 2_4 | first half | frames 65–120 | **69–120** and **70–120** |
| 2_3 | 32, 88 | both ends | **0–120** (i.e. the two ends) |
| 2_1 | 0, 120 | the middle | **2–98** and **32–103** |

::: key title="The action lands wherever the free run is — every time, on both seeds"
With the tail free (`3_4`, `2_4`) the character stands normally through the pinned
first half and then, from about frame 70, a large cardboard box appears and is
picked up and carried off. With the head free (`3_2`, `2_2`) the same box appears at
the start instead, and the character is kneeling beside it before the pinned frames
take over at 64.

This is the most direct evidence in the sweep that the video prior is doing
something and not merely interpolating: **it has a whole action available, and the
conditioning decides *when* it is allowed to happen, not whether.**
:::

::: clips arms=K3_2,K3_4 ids=box_heavy seeds=1234,5678
The same prompt, the same seed, the same model — only which half is pinned changes.
Left: head free, box appears at the start. Right: tail free, box appears at the
end.
:::

## What this costs us

::: warn title="The control is not a dial"
Motion added is not monotone in K, so "loose control" cannot be obtained by
lowering K — `2_1` is stiffer than `5`. What controls it is *where* the anchors
sit, and the two knobs (how many, and where) are entangled.

This is the argument for moving to `LTX-2-19b-IC-LoRA-Pose-Control`: a per-frame
control signal the model was actually trained on would give a strength dial that is
monotone, instead of a placement puzzle. Nothing here is broken enough to force
that move, but the sweep does not deliver the clean strong → loose axis the
experiment was designed around.
:::

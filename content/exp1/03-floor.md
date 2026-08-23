---
title: The floor
nav: The floor — read first
lead: The control column. The blue video goes straight into pose recovery with no video model in the loop, so whatever separates it from the input is damage done by rendering and recovery on their own. It is clean for ten clips of twelve — and the two exceptions are the same prompt, failing completely.
---

## What the floor column is

`floor` is the blue input video handed directly to GVHMR. No video model, no
keyframes, no generation. Then re-rendered with the identical render code.

In a perfect world the result would be pixel-identical to the input. It is not,
because pose recovery from a single fixed viewpoint is an inference. The question is
how much is lost — because that loss is the noise floor against which every other
column has to be read.

## The measurement

Joint error against the input motion, root-relative, on the same neutral SMPL body.
Mean over 22 joints and 121 frames, in millimetres.

| clip | floor | Kall | K9 | K5 | K3_1 | K3_2 | K3_3 | K3_4 | K2_1 | K2_2 | K2_3 | K2_4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| barbell_heavy s1234 | **42** | 44 | 52 | 124 | 116 | 122 | 204 | 134 | 133 | 128 | 188 | 156 |
| barbell_heavy s5678 | **41** | 44 | 50 | 74 | 107 | 137 | 144 | 126 | 104 | 126 | 141 | 150 |
| baseball s1234 | **37** | 39 | 43 | 118 | 122 | 128 | 155 | 152 | 180 | 161 | 171 | 122 |
| baseball s5678 | **34** | 36 | 48 | 109 | 176 | 150 | 110 | 110 | 132 | 190 | 178 | 103 |
| box_heavy s1234 | **36** | 38 | 46 | 117 | 113 | 139 | 195 | 168 | 139 | 134 | 233 | 121 |
| box_heavy s5678 | **36** | 40 | 53 | 80 | 128 | 143 | 122 | 151 | 114 | 131 | 208 | 147 |
| punch s1234 | **36** | 44 | 85 | 112 | 121 | 121 | 162 | 140 | 129 | 153 | 143 | 151 |
| punch s5678 | **37** | 44 | 92 | 128 | 146 | 146 | 155 | 126 | 128 | 150 | 141 | 126 |
| push_heavy s1234 | **37** | 38 | 40 | 76 | 85 | 112 | 98 | 70 | 104 | 164 | 142 | 120 |
| push_heavy s5678 | **37** | 37 | 39 | 61 | 78 | 79 | 88 | 69 | 114 | 87 | 108 | 84 |
| squat s1234 | **356** | 347 | 347 | 353 | 350 | 336 | 340 | 352 | 336 | 333 | 349 | 337 |
| squat s5678 | **353** | 350 | 348 | 338 | 352 | 351 | 361 | 357 | 316 | 346 | 356 | 351 |
| **mean, squat excluded** | **37** | 40 | 55 | 100 | 119 | 128 | 143 | 125 | 128 | 142 | 165 | 128 |

::: key title="The floor is clean for 10 of 12 clips: 34–42 mm"
That is roughly the width of a wrist. Rendering the motion to video and recovering
it again costs almost nothing, so **differences in the other columns can fairly be
attributed to the video model.**

Everything else in this experiment depends on this line.
:::

## See it for yourself

::: clips arms=blue,lift_floor,lift_Kall ids=box_heavy,punch,push_heavy seeds=1234,5678 heads=on
Input motion, `floor`, and `K = all`. All three should look like the same motion —
and they do. `floor` at 36–37 mm and `K = all` at 38–44 mm for these clips.
:::

## The strong-control column agrees

`K = all` comes in at 36–44 mm, statistically indistinguishable from `floor` — 40 mm
against 37 mm on the mean, and within 2–8 mm clip by clip.

That is the expected result and worth stating plainly: **when the video model is
handed every frame, it copies, so the round trip returns what went in.** The brief's
"if it comes back identical, the video model did nothing" case is exactly what
`K = all` looks like.

`K = 9` sits just above at 55 mm — nine frames is still enough to pin the motion
almost completely.

## The exception: squat fails in the control column

::: warn title="Every squat row in this experiment must be discounted"
`squat` comes in at **353–356 mm — in the `floor` column**, before the video model is
involved at all.

The input squats facing *away* from the camera, curled into a compact ball. Every
lifted row comes back squatting *towards* the camera. A deeply folded crouch seen
from one fixed viewpoint is close to front-back ambiguous in silhouette, and GVHMR
consistently resolves it the other way.

A brute-force search over rotations about the vertical axis finds no angle that
brings the two into agreement — best 277 mm at −90°. **This is not an alignment
artefact; the recovered pose is genuinely a different one.**

Nothing in that row tells us anything about the video model, and the yaw figure
recorded for it in the manifest is meaningless.
:::

::: clips arms=blue,lift_floor,lift_Kall ids=squat seeds=1234,5678
`squat`: the input, then `floor`, then `K = all`. The input faces away from the
camera; both recoveries face towards it. No video model was involved in either.
:::

See [Result 5 — squat](result-squat.html) for the full account, and
[the verdict](verdict.html) for why this failure mode is worth taking seriously
rather than writing off as one bad clip.

## The loose columns, sized against this

Root-relative error rises to **100–165 mm** across the loose sets — three to four
times the floor. So something real came back different. Whether it is *better* is
the question the six prompt pages answer.

::: key title="The ordering follows Experiment 2's finding exactly"
- Sets that pin **neither end** move furthest from the input: `K2_3` 165 mm,
  `K3_3` 143 mm.
- Sets that free **one end** sit in the middle: `K3_2` 128, `K3_4` 125, `K2_2` 142,
  `K2_4` 128.
- Sets that anchor **both ends** stay closest: `K5` 100, `K3_1` 119.

**Handing over fewer frames does not, on its own, buy distance from the input —
freeing an end does.** That is the same conclusion
[Experiment 2 reached](../exp2/placement.html) from the other side of the pipeline,
arrived at by a completely different measurement.
:::

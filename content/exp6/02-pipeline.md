---
title: Pipeline
nav: Pipeline
lead: Five stages, three virtualenvs, and five changes from Experiment 4 — two the brief asked for and three the pilots forced. None of them touches the one variable being swept.
---

## The five stages

| stage | code | what happens | output |
|---|---|---|---|
| 1 | `motions.py` | the ten AMASS/BABEL clips into the shape the renderer takes | `data/smpl/` |
| 2 | `render.py` | input SMPL preview, neutral body, fixed camera | `data/renders/` |
| 3 | `depth_render.py` | **depth map** of the clip, dense and sparse — *the control* | `data/depth/` |
| 4 | `generate.py` | LTX-2.3 22B + Depth IC-LoRA, appearance from text | `data/videos/` |
| 5 | `lift.py` → `rerender.py` | GVHMR to world-grounded SMPL-X, re-rendered on the same neutral body | `data/lifted_renders/` |

Then `analysis.py`, `strips.py` and `sheet.py` produce `results/`.

Each step reads the previous step's `manifest.json` rather than globbing, and writes
its own. Three virtualenvs, because the three models want different stacks: SMPL +
pyrender for the renders, LTX-2 for generation, GVHMR for the lift.

## The input clips

Ten clips from **AMASS/BABEL**, prepared in Experiment 5 and used here unmodified:

`walk` · `run` · `jump` · `kick` · `sit_down` · `stand_up` · `throw` · `turn` ·
`squat` · `wave`

Each is **169 frames at 25 fps — 6.76 s**, resampled with slerp on the joint
rotations and linear interpolation on the root translation. SMPL with `betas`
written as zeros, so every clip renders on the same neutral body. Y up, body facing
+Z.

::: key title="Why this matters more than it sounds"
These clips actually perform the actions they are labelled with. That is the whole
reason this experiment exists — in Experiments 1–4 the control motion was
MotionGPT3's, and it frequently did not.
:::

::: clips arms=prev_fitted,prev_depth ids=walk,kick,sit_down seeds=1234
The clip as the renderer takes it, and the dense depth control built from it. Worth
watching before anything else: if the control video is wrong, everything after it is
wasted.
:::

## The control track

- On a **conditioned** frame: the full-body depth render, camera-space depth mapped
  linearly through a fixed metric window, on a **flat mid-grey field**.
- On a frame left **free**: blank mid-grey — *and masked off*, see below.

::: warn title="Frame indices sit on the latent grid"
The causal VAE compresses time by 8, so for 169 frames the grid is
`0, 8, 16, … 160, 168` — twenty-two frames. Every condition is snapped to it in code
before rendering.
:::

| condition | conditioned frames | count | latent frames the mask leaves on |
|---|---|---|---|
| `dense` | 0·8·16·…·168 | 22 | all (no mask needed) |
| `K = 8` | 0·24·48·72·96·120·144·168 | 8 | 0·3·6·9·12·15·18·21 |
| `K = 5` | 0·40·88·128·168 | 5 | 0·5·11·16·21 |
| `K = 3` | 0·88·168 | 3 | 0·11·21 |
| `K = 2` | 0·168 | 2 | 0·21 |

## Appearance comes from text alone

No init frame, no reference image. Each prompt names a person and a place — and,
crucially, **what is actually behind the person**.

| clip | prompt |
|---|---|
| `walk` | a man walking along a city sidewalk, casual clothes, overcast daylight, **brick buildings and a row of parked cars along the street behind him** |
| `run` | a man running on an outdoor running track, athletic wear, bright daylight, **red track lanes and empty stands behind him** |
| `jump` | a man jumping upward, athletic wear, open gym interior, even lighting, **a wooden floor and a far wall with high windows behind him** |
| `kick` | a man performing a kick, martial arts clothing, plain training hall, even lighting, **a wooden floor and a mirrored wall behind him** |
| `sit_down` | a man lowering himself into a seated position, casual clothes, plain interior, soft daylight, **a wooden floor and a pale wall with a window behind him** |
| `stand_up` | a man rising to his feet from a seated position, casual clothes, plain interior, soft daylight, **a wooden floor and a pale wall with a window behind him** |
| `throw` | a man throwing with an overhand motion, athletic wear, outdoor field, bright daylight, **mown grass and a distant treeline behind him** |
| `turn` | a man turning around to face the other direction, casual clothes, plain interior, soft daylight, **a wooden floor and a pale wall behind him** |
| `squat` | a man performing a deep squat, athletic wear, gym interior, even lighting, **rubber flooring and equipment racks behind him** |
| `wave` | a man waving one arm, casual clothes, plain outdoor setting, soft daylight, **a paved path and a hedge in front of a house behind him** |

Every one ends `static camera, full body in frame`. The bold clause is what was
**added** to the brief's own prompt — and nothing added is an object the depth render
lacks. No chair, no ball: only walls, floors, treelines and buildings.

::: note title="Why every prompt says a man"
The clips render on neutral SMPL bodies with `betas = 0`, so a consistent subject
keeps the sheet comparable across rows.
:::

## What changed from Experiment 4

Two changes the brief asked for:

| | Experiment 4 | here |
|---|---|---|
| frames | 121 (4.84 s) | **169 (6.76 s)** |
| resolution | 704×704 | **1216×704** |

And three the pilots forced. Each is measured in
[What the pilots settled](pilots.html):

::: key title="1. The prompts name the background"
The brief's prompts name a place in two or three words. Each one here ends its scene
clause with what is actually behind the person. Experiment 4's own source records the
failure this fixes — its one prompt of six that named no surroundings was the one
where the model copied the depth track's grey background instead of inventing a
scene.
:::

::: key title="2. The depth control format was tested, not assumed"
A second format was built — the body on a ground plane receding to the horizon,
encoded as normalised inverse depth, which is what a real depth estimator outputs and
therefore the expected winner. **It lost.** Its empty background is *black*, i.e.
infinitely far, which an indoor prompt cannot satisfy; on `kick` the model drew a
black void instead of a training hall.

The run keeps the brief's own format: the body on a flat mid-grey field. Both are
implemented (`config.DEPTH_MODE`) and both are in `data/pilot/`.
:::

::: key title="3. Sparse conditions mask the reference off on their blank frames"
The control video is unchanged — body on the conditioned frames, blank between — but
the model is now **told not to attend to the blank frames**.

Without this it copies the control track itself into the unconditioned stretches,
which is exactly the background-free output this run existed to fix. It removes no
pose information: the latents carrying a conditioned frame are byte-identical either
way.
:::

None of the five changes the variable being swept: how many frames carry a pose.

## What each result page shows

Every clip gets its own page, in the same order:

1. **The input clip and the control tracks it became** — at `dense`, `K = 5` and
   `K = 2`, so you can see what was fed in before judging what came out.
2. **One grid per density** — depth control, photoreal output, recovered motion, side
   by side. The heading names the density and its exact conditioned frames.
3. **Photoreal across the sweep**, then **recovered SMPL across the sweep** — the
   appearance comparison and the motion comparison, each in one row.
4. **The timing strip** — control, photoreal and recovered against fixed frame times,
   as one image. Click to open it full size.

::: note title="The clips are synchronised"
Every clip here is 169 frames at 25 fps, so they can be compared frame against frame
— and the toolbar keeps them that way. **Sync** restarts every visible clip together
on a common loop rather than letting each drift; the speed buttons run the whole page
at ¼×, ½×, 1× or 2×. Click any clip to open it and step through a frame at a time.
:::

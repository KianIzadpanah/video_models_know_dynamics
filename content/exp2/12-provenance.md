---
title: Provenance
nav: Provenance
lead: Seeds, checkpoints, settings, and where every file came from. Enough to re-run the sweep exactly.
---

## Seeds

Seeds **1234** and **5678**, fixed and logged. The same seed drives the motion
sampling *and* the video sampling, so within a row of clips the only thing that
changes is the conditioning set.

## Models and checkpoints

| role | model | detail |
|---|---|---|
| Text to motion | **MotionGPT3** | `OpenMotionLab/MotionGPT3`. Text in via a txt file, motion out as `.npy` in HumanML3D format at 20 fps. Output folder set by `TEST.FOLDER` in `configs/assets.yaml`. |
| Motion to body | **SMPL neutral** | `betas = 0` enforced, so no body-shape variation between clips. Conversion from HumanML3D taken from MotionGPT3's own repository. |
| Video | **LTX-2.5 dev, 22B** | `TI2VidTwoStagesPipeline` with `combined_image_conditionings` — latent replacement at frame 0, keyframe conditioning after it. |

`KeyframeInterpolationPipeline` was **not used and not needed** — it was held in
reserve for the morphing failure mode, which
[never occurred](does-it-work.html#test-3-no-morphing-anywhere).

**SDEdit** — the optional second knob in the brief, controlling *how strongly* the
model follows the input rather than *which frames* it follows — was **not built**.

## Generation settings

Held fixed across all 132 videos:

```
cfg_scale        3.0
stg_scale        1.0
stg_blocks       [29]
rescale_scale    0.7
modality_scale   1.0
steps            40
frames           121 @ 25 fps
resolution       512 x 512
cond. strength   1.0
crf              33
```

## Render settings

SMPL neutral, `betas = 0`; matte blue body, gray floor with a soft shadow, flat
light-gray backdrop; fixed camera, 3/4 front-left; 121 frames, 25 fps, 512x512.
Motion resampled from 20 fps to 25 fps *before* rendering, so the video is never
retimed after the fact.

::: note title="Why these exact numbers"
LTX requires `num_frames % 8 == 1` and frame dimensions that are multiples of 32.
121 frames and 512x512 are the smallest values satisfying both that give a clip
just under five seconds. The same render code is reused byte-for-byte by
[Experiment 1](../exp1/provenance.html), which checks the hashes at runtime — if
the two sides of the round trip were rendered differently, that experiment would be
comparing rendering rather than motion.
:::

## Files

| path | what is in it |
|---|---|
| `src/prompts.py` | the six prompts and their physical beats |
| `src/config.py` | paths, geometry, the K sets |
| `src/motion.py` | MotionGPT3 driver |
| `src/smplfit.py` | HumanML3D to SMPL |
| `src/render.py` | the blue character render |
| `src/keyframes.py` | frame selection, plus `assert_on_latent_grid` |
| `src/generate.py` | LTX-2.5 generation |
| `src/energy.py` | silhouette-change energy |
| `src/checks.py` | tests 1 to 3 |
| `src/check_offgrid.py` | the off-grid negative control |
| `data/motions/` | MotionGPT3 output, HumanML3D `.npy` |
| `data/smpl/` | fitted SMPL, 12 files |
| `data/renders/` | the blue inputs, 12 files |
| `data/frames/` | every rendered frame as PNG, per clip |
| `data/keyframes/` | `manifest.json` — the single source of truth for the K sets |
| `data/videos/` | 132 generated videos |
| `data/videos_offgrid/` | the one off-grid control clip |
| `results/sweep.html` | the original contact sheet |
| `results/strips/` | 12 time-aligned strips |
| `results/checks/` | `checks.json`, `energy.json`, `offgrid.json`, 132 test images |
| `results/NOTES.md` | the written record this write-up is based on |

Every step writes a `manifest.json` with `prompt_id`, `condition`, `K`, `seed` and
`path`, and reads the previous step's manifest rather than globbing the filesystem.
The K sets are defined once, in `data/keyframes/manifest.json`, and
[Experiment 1](../exp1/provenance.html) reads them from there — so the two
experiments cannot disagree about what was generated.

## The prompts, verbatim

| id | text | the physical beat |
|---|---|---|
| `box_heavy` | a person lifts a heavy box from the floor | the load is taken up — pause at the bottom, then the slow rise under weight |
| `barbell_heavy` | a person lifts a heavy barbell from the ground | the break off the floor and the acceleration once the bar passes the knees |
| `push_heavy` | a person pushes a car | the lean into the load before anything moves |
| `punch` | a person throws right and left punches | the alternation — hip rotation leads each arm, recovery between punches |
| `squat` | a person squats down | controlled descent, bottom position, drive back up |
| `baseball` | a person hit a ball with baseball bat | load onto the back foot, pause, then the fast rotation through contact |

Every prompt contains a moment whose *timing* carries physical meaning. That timing
is exactly what a video model with physical knowledge would have to invent when only
a few keyframes are handed over.

## Clips on this site

The clips shown throughout are web-sized transcodes — H.264, audio stripped, capped
at 720 px wide. The 512x512 originals are unchanged in the experiment folder. The
timing strips are downscaled from about 2200 px; open one full-size to read it.

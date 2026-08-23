---
title: How it was run
nav: How it was run
lead: The frames you are allowed to pin are not free — the video model's compression of time snaps your choices to a grid. That constraint shapes every conditioning set in the sweep.
---

## Step 1 — the motion

MotionGPT3 generates a HumanML3D joint sequence from each prompt, at 20 fps, two
seeds per prompt. That sequence is converted to SMPL parameters using the
conversion in MotionGPT3's own repository.

## Step 2 — the blue character

The SMPL sequence is rendered deliberately plainly:

- SMPL **neutral** body, `betas = 0` — no body-shape variation between clips
- matte blue body, gray floor with a soft shadow, flat light-gray backdrop
- fixed camera, 3/4 front-left
- **121 frames, 25 fps, 512×512**

Those numbers are not arbitrary. LTX needs `num_frames % 8 == 1` and frame sizes
that are multiples of 32. The motion is 20 fps and the render is 25 fps, so the
motion is resampled *before* rendering rather than the video being retimed after.

The plainness is the point. One strongly blue thing (the body) and two neutral
grays (floor, backdrop) means that if the video model invents anything — an
object, a photographic person — it shows up immediately as
[warm-toned pixels that were never there](placement.html#where-the-invented-content-lands).

Every frame is saved as a PNG, and the pinned frames are selected from those.

## Step 3 — which frames you may pin

::: warn title="Frame indices are not free"
The video model's VAE compresses time. An index that does not sit on the latent
grid gets snapped to the nearest one that does — so you end up conditioning on a
frame you did not choose, without being told. For 121 frames the safe indices
are:

```
0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120
```

Frame 0 gets its own latent; the rest arrive in chunks of 8. "The middle frame"
is not a legal choice — 56 or 64 is. This is enforced in code by
`keyframes.assert_on_latent_grid`, and it is
[verified against a deliberate off-grid run](does-it-work.html#extra-the-off-grid-negative-control).
:::

## The eleven conditioning sets

| set | pinned frames | free run | what it isolates |
|---|---|---|---|
| `all` | every 8th, 0 → 120 | none | strong control: does conditioning work at all |
| `9` | 0, 16, 32, … 112, 120 | 15 frames at a time | still effectively pinned |
| `5` | 0, 32, 64, 88, 120 | ~31 frames | both ends plus three interior beats |
| `3_1` | 0, 64, 120 | two halves | both ends pinned |
| `3_2` | 64, 88, 120 | **frames 0–63** | the whole first half free |
| `3_3` | 32, 64, 88 | **both ends** | neither end pinned |
| `3_4` | 0, 32, 64 | **frames 65–120** | the whole second half free |
| `2_1` | 0, 120 | the entire middle | both ends pinned, longest interior run |
| `2_2` | 64, 120 | frames 0–63 | head free |
| `2_3` | 32, 88 | **both ends** | neither end pinned, only two frames |
| `2_4` | 0, 64 | frames 65–120 | tail free |

The four placements at K = 3 and the four at K = 2 exist so that *how many* frames
are pinned can be separated from *where* they sit. `2_1` and `2_3` hand over
exactly two frames each; the only difference is that `2_1` puts them at the ends
and `2_3` puts them inside. They behave completely differently, which is the
headline result.

## Step 4 — generation

Each pinned frame is passed as a conditioning image with its frame index, at
strength 1.0:

```python
images=[
    ImageConditioningInput("frame_000.png",   0, 1.0, 33),
    ImageConditioningInput("frame_064.png",  64, 1.0, 33),
    ImageConditioningInput("frame_120.png", 120, 1.0, 33),
]
```

::: method title="Sampler settings, held fixed across the whole sweep"
`cfg_scale 3.0` · `stg_scale 1.0` · `stg_blocks [29]` · `rescale_scale 0.7` ·
`modality_scale 1.0` · 40 steps · 121 frames @ 25 fps · 512×512 ·
conditioning strength 1.0 · crf 33.

Pipeline: `TI2VidTwoStagesPipeline` with `combined_image_conditionings` — latent
replacement at frame 0, keyframe conditioning after it.
`KeyframeInterpolationPipeline` was held in reserve for the morphing failure mode
and, since [that never occurred](does-it-work.html#test-3-no-morphing-anywhere),
was never needed. SDEdit — the optional second knob — was not built.
:::

## What each clip page shows

Every prompt gets its own page. On it, the same prompt appears in four grids:

- **Strong control** — the blue input next to `K = all` and `K = 9`. This is the
  baseline: the video model copying.
- **The useful window** — `K = 5` and `K = 3_2`, the two sets where something
  actually happens.
- **Placement at K = 3** and **at K = 2** — the four placements side by side, which
  is where the free-run effect is visible.

Then the per-prompt motion numbers, and a **timing strip**: every condition as one
time-aligned image. The strip is the fastest way to read timing — click it to open
it full size.

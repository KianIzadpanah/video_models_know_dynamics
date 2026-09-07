---
title: Provenance
nav: Provenance
lead: Seed, checkpoints, settings, the deviations from the brief, and where every file came from.
---

## Scope of this run

This is **Experiment 6, part 2 — Run C**, executed end to end: the ten clean
AMASS/BABEL clips from part 1, each generated at five conditioning densities, one
seed — **50 videos** — then lifted back to SMPL and re-rendered on the neutral body.

**Run A (does the prompt work) and Run B (which setting fixed it) were not run.** The
instruction for this pass was Run C only, so `results/exp6_prompt.html` — Run A's
four-video sheet — does not exist.

Nothing failed: pose recovery found and tracked a person in all fifty videos.

## Seed

Seed **1234**, single seed. This is the one experiment in the series without a second
seed, which is worth carrying: a per-clip observation here rests on one sample.

## Models and checkpoints

| role | model | detail |
|---|---|---|
| Input motion | **AMASS/BABEL** via Experiment 5 | ten clips, 169 frames @ 25 fps, unmodified |
| Motion to body | **SMPL** | `betas` written as zeros — the neutral body |
| Control | depth render, one fixed camera | flat mid-grey field, `config.DEPTH_MODE = "flat"` |
| Video | **LTX-2.3 22B distilled** + `LTX-2-19b-IC-LoRA-Depth-Control` | via `ICLoraPipeline` |
| Appearance | the text prompt alone | no init frame, no reference image |
| Video to motion | **GVHMR** | world-grounded SMPL-X |

## Generation settings

Identical across all fifty videos:

```
reference (ic-lora) strength        1.0
conditioning attention strength     1.0
resolution                          1216 x 704
frames                              169 @ 25 fps  (6.76 s)
seed                                1234
init frame                          none
```

Per-video settings are logged in `data/videos/manifest.json`.

Sparse conditions additionally use `conditioning_attention_mask`, built from the same
conditioned-frame list the depth video was rendered from. `dense` conditions every
latent frame and gets no mask.

## Conditioned frames

The latent grid for 169 frames is `0, 8, 16, … 160, 168` — twenty-two frames.

| condition | conditioned frames | count | latent frames left on |
|---|---|---|---|
| `dense` | 0·8·16·…·168 | 22 | all |
| `K = 8` | 0·24·48·72·96·120·144·168 | 8 | 0·3·6·9·12·15·18·21 |
| `K = 5` | 0·40·88·128·168 | 5 | 0·5·11·16·21 |
| `K = 3` | 0·88·168 | 3 | 0·11·21 |
| `K = 2` | 0·168 | 2 | 0·21 |

The downsampled mask was verified to be exactly binary and to land on exactly those
latents.

## The input clips

Built by Experiment 5's `amass_loader.py`:

- **169 frames at 25 fps** (6.72 s of source resampled to 6.76 s of clip)
- resampling: **slerp on joint rotations, linear on root translation**
- world frame: Y up, body faces +Z (AMASS Z-up rotated −90° about X)
- SMPL, 23 body joints with the last two zeroed; `betas` zeros so the neutral body
  renders
- stored as an npz archive under a `.npy` name, so `np.load` dispatches on magic
  bytes and yields the dict Experiment 4's renderer expects

## Deviations from the brief, all deliberate

::: note title="Five changes, and why each was made"
1. **Run A and Run B not executed** — instructed to run section C only.
2. **169 frames instead of 121, and 1216×704 instead of 704×704** — both asked for by
   the brief.
3. **Prompts extended with a background clause.** The brief's prompt is the head of
   each one; what was added is the surface *behind* the person. Nothing added is an
   object the depth render lacks — no chair, no ball — only walls, floors, treelines
   and buildings.
4. **Sparse conditions use `conditioning_attention_mask`.** The control video is
   exactly the brief's — body on conditioned frames, blank mid-grey between. The mask
   only stops the blank frames from instructing appearance, and removes no pose
   information: the latents carrying a conditioned frame are identical either way.
5. **The base is LTX-2.3 22B, not LTX-2 19B.** Experiment 4's own variant, and the
   only one reachable here that holds a 6.76 s clip without fading to black.

None of the five changes the variable Run C sweeps: how many frames carry a pose.
:::

## Environments

Three virtualenvs, because the three models want different stacks:

| env | what for |
|---|---|
| `/workspace/venvs/render` | SMPL + pyrender — depth control, previews, re-renders |
| `/workspace/vendor/LTX-2/.venv` | LTX-2 pipelines, torch 2.13 / cu132 |
| `/workspace/vendor/GVHMR/.venv` | GVHMR, torch 2.3 / cu121 / python 3.10 |

Model paths live in `src/config.py` and all point **outside** the experiment folder,
so no weights are in it. `bash src/run_all.sh` runs every step in order, about two
hours on one A100 80GB.

## Files

| path | what is in it |
|---|---|
| `src/motions.py` | the ten clips into the renderer's shape |
| `src/render.py` | input SMPL previews |
| `src/depth_render.py` | the depth control, dense and sparse, both formats |
| `src/generate.py` | LTX generation, and `sparse_attention_mask` |
| `src/lift.py` | GVHMR driver |
| `src/rerender.py` | recovered SMPL on the neutral body |
| `src/analysis.py`, `strips.py`, `sheet.py` | the numbers, the strips, the sheet |
| `src/config.py` | paths, geometry, the latent grid, `DEPTH_MODE` |
| `src/prompts.py` | the appearance prompts, and the brief's originals kept verbatim |
| `data/exp5_amass/` | the ten clean clips from part 1 — **the input, unmodified** |
| `data/smpl/` | the same clips in the renderer's shape |
| `data/renders/` | input SMPL previews |
| `data/depth/` | the 50 depth control videos — *what went in* |
| `data/videos/` | the 50 photoreal videos — *what LTX made* |
| `data/lifted/` | GVHMR output, SMPL-X params |
| `data/lifted_renders/` | the recovered motion on the neutral body |
| `data/preview/` | per-clip depth and fitted previews, plus `report.json` |
| `data/pilot/` | the four pilots: control formats, clip lengths, masked vs unmasked |
| `results/exp6.html` | the original contact sheet |
| `results/strips/` | each clip as one time-aligned PNG |
| `results/analysis.json` | joint error on pinned vs free frames, jerk, foot skate |
| `results/API_REPORT.md` | what the LTX IC-LoRA API actually is, and the four pilots |
| `results/NOTES.md` | the written record this write-up is based on |

Each step reads the previous step's `manifest.json` and writes its own. `data/frames/`
holds per-frame PNGs and is regenerable, so it is excluded from the packaged zip that
`src/package.sh` builds.

## What was not built

::: note title="Deliberate omissions"
There is **no metric that decides the verdict**. The numbers in
`results/analysis.json` describe what is on screen — same neutral body, same yaw
alignment, same grounding — and are used to locate *where* a clip stops copying and to
flag recoveries worth checking against their video.

There is **no human study**, and there is **one seed**. Ten clips at one seed is a
basis for deciding what to build next, not for a quantitative claim.
:::

## Clips on this site

Web-sized transcodes — H.264, audio stripped, capped at 720 px wide. The 1216×704
originals are unchanged in the experiment folder. Timing strips are downscaled; open
one full size to read it.

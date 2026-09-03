---
title: Provenance
nav: Provenance
lead: Seeds, checkpoints, settings, the render-code identity check, and where every file came from.
---

## Seeds

Seeds **1234** and **5678**, fixed. The same seed drove the motion (back in
Experiments 1–3), the video, and deterministically the lift. 60 clips: 6 motions x 5
conditions x 2 seeds.

## Models and checkpoints

| role | model | detail |
|---|---|---|
| Text to motion | **MotionGPT3** | reused from Experiments 1–3, **not regenerated**; resampled to 121 frames @ 25 fps |
| Motion to body | **SMPL neutral** | `betas = 0` |
| Control render | depth video of the SMPL animation | 121 frames, 704x704 |
| Video | **LTX-2.3 22B distilled** + `LTX-2-19b-IC-LoRA-Depth-Control` | via `ICLoraPipeline` |
| Appearance | the text prompt alone | no init frame, no reference image, `images=[]` |
| Video to motion | **GVHMR** | `gvhmr_siga24_release.ckpt`, world-grounded SMPL-X, `static_cam=True`, no DPVO |

121 frames in, 121 out, at 25 fps, for all 60 clips.

::: note title="Why LTX-2.3 distilled and not 2.5"
The depth IC-LoRA requires the `distilled` checkpoint, and the pipeline class and
control parameter both differ from the earlier experiments. The API was verified
against the installed package before anything was built, and the findings are
recorded in the run's `results/API_REPORT.md` — including that text-to-video with
control works with an empty image list, which is what makes the appearance split
possible without a reference photo.
:::

## Generation settings

Held fixed across all 60 videos:

```
control strength (ic-lora-strength)   1.0
conditioning_attention_strength       1.0
init frame                            none
frames                                121 @ 25 fps
resolution                            704 x 704
```

Frame count must be `8n+1` and both dimensions divisible by 32. The variable in this
experiment is **how many frames are conditioned**, not how strongly, so the strength
stays at 1.0 throughout.

`conditioning_attention_mask` — a mask video over the reference — exists in the API
and was **deliberately left unused**. It is the [first change to try next](verdict.html).

## Conditioned frames

Snapped to the latent grid before rendering. The grid for 121 frames is
`0, 8, 16, ... 112, 120`.

| condition | frames | count |
|---|---|---|
| `dense` | all 16 grid frames | 16 |
| `K = 8` | 0, 16, 32, 48, 72, 88, 104, 120 | 8 |
| `K = 5` | 0, 32, 64, 88, 120 | 5 |
| `K = 3` | 0, 64, 120 | 3 |
| `K = 2` | 0, 120 | 2 |

Sparse control videos use the brief's literal **impulse** encoding: the conditioned
pose on its own frame, blank mid-grey between. The alternative — **hold**, rendering
the pose across the whole latent frame it belongs to — was built, run and rejected on
the evidence; it would remove the
[end-frame blow-out](does-it-work.html#4-two-smaller-artefacts-both-bounded) but it
changes what the control means.

## The render-code identity check

::: method title="Both ends of the round trip are rendered by the same code"
The depth control, the input preview and the recovered re-render all come out of
**byte-identical render code**, sha256-checked at run time against
[Experiment 1's](../exp1/provenance.html). Digests are recorded in
`data/depth/manifest.json` and `data/lifted_renders/manifest.json`.

Same neutral SMPL body with `betas = 0`, same fixed camera, same grounding. If the
two ends were rendered differently, this experiment would be comparing renderers
rather than motions.
:::

## The heading rotation

Recovered clips are rotated about the vertical axis onto their own input's heading.
The offsets came out **−147° to −160°**, consistent with Experiment 1's ≈ −150°.

The rotation changes which way a clip points and nothing else. It cannot repair a
front-to-back flip, which is why [`squat`](result-squat.html) stays broken.

## Known artefacts

| artefact | scope | effect on the results |
|---|---|---|
| frames 119–120 blow out to near-white | 17 of the 48 sparse clips, all seed 5678, none `dense` | 2 frames in 121; moves none of the numbers |
| distant background people | 4 of the 12 `baseball` clips | no lift contaminated; the tracker took a single track |
| `barbell_heavy` prompt changed mid-run | its 10 clips regenerated | nothing else re-rolled |
| `squat` recovery flips front-to-back | all 10 `squat` clips | that row is excluded from every mean |

## Files

| path | what is in it |
|---|---|
| `src/prompts.py` | the six motion prompts and the six appearance prompts |
| `src/config.py` | paths, geometry, the latent grid, the five conditions |
| `src/motions.py` | reuse of the Experiments 1–3 motion files |
| `src/render.py` | the SMPL render — hash-checked against Experiment 1 |
| `src/depth_render.py` | the depth control render, dense and sparse |
| `src/generate.py` | the `ICLoraPipeline` wrapper |
| `src/lift.py` | GVHMR driver |
| `src/rerender.py` | re-render of the recovered motion |
| `src/analysis.py` | joint error split by pinned / free, jerk, foot-skate |
| `src/strips.py` | the time-aligned strips |
| `data/renders/` | input motion previews, 12 files |
| `data/depth/` | the 60 depth control tracks |
| `data/depth_hold/` | the rejected `hold` encoding, 8 files |
| `data/videos/` | the 60 photoreal videos |
| `data/lifted/` | GVHMR output, SMPL-X params |
| `data/lifted_renders/` | the 60 recovered motions, re-rendered |
| `data/probe*/` | the step-2 and step-3 verification runs |
| `results/exp4.html` | the original contact sheet |
| `results/strips/` | 12 time-aligned strips |
| `results/probe/` | the verification stills shown throughout |
| `results/analysis.json` | the supporting numbers |
| `results/API_REPORT.md` | what the installed LTX API actually exposes |
| `results/NOTES.md` | the written record this write-up is based on |

Each stage writes a `manifest.json` with `prompt_id`, `condition`, `seed` and `path`,
and reads the previous stage's manifest rather than globbing.

## What was not built

::: note title="Deliberate omissions"
There is **no metric that decides the verdict**. `results/analysis.json` opens with a
note saying so. The numbers are used for exactly two things: to say *where* a motion
stops copying its input, and to flag recoveries that should be checked against the
video they came from.

There is **no human study**. Six motions, two seeds and one pair of eyes is a basis
for deciding what to build next, not for a quantitative claim about naturalness.
:::

## Clips on this site

Web-sized transcodes — H.264, audio stripped, capped at 720 px wide. The 704x704
originals are unchanged in the experiment folder. Timing strips are downscaled from
about 2280 px wide; open one full size to read it.

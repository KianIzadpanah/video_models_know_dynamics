---
title: Provenance
nav: Provenance
lead: Seeds, checkpoints, the render-code identity check, and where every file came from.
---

## Seeds

Seeds **1234** and **5678**, fixed. The same seed drove the motion, the video, and
(deterministically) the lift. 144 clips: 6 prompts x 2 seeds x 12 conditions.

## Models and checkpoints

| role | model | detail |
|---|---|---|
| Text to motion | **MotionGPT3** | reused from Experiment 2, not regenerated |
| Motion to body | **SMPL neutral** | `betas = 0` |
| Video | **LTX-2.5 dev, 22B** | `TI2VidTwoStagesPipeline`, settings identical to Experiment 2 |
| Video to motion | **GVHMR** | `gvhmr_siga24_release.ckpt`, world-grounded SMPL-X, `static_cam=True`, no DPVO |

121 frames in, 121 frames out, at 25 fps, for every one of the 144 clips.

## The conditions

`floor` plus all eleven of Experiment 2's conditioning sets. The list is **read from
Experiment 2's keyframe manifest** at runtime, not restated here, so the two
experiments cannot drift apart about what was generated.

| condition | pinned frames |
|---|---|
| `floor` | none — the blue video goes straight to GVHMR |
| `Kall` | every 8th frame, 0 to 120 |
| `K9` | 0, 16, 32, 48, 64, 80, 96, 112, 120 |
| `K5` | 0, 32, 64, 88, 120 |
| `K3_1` | 0, 64, 120 |
| `K3_2` | 64, 88, 120 |
| `K3_3` | 32, 64, 88 |
| `K3_4` | 0, 32, 64 |
| `K2_1` | 0, 120 |
| `K2_2` | 64, 120 |
| `K2_3` | 32, 88 |
| `K2_4` | 0, 64 |

`K5` and `K3_2` are the two loose values
[chosen in Experiment 2](../exp2/verdict.html). `Kall` is the brief's `strong`
control.

## The render-code identity check

::: method title="Both sides are rendered by byte-identical code"
`src/render.py` and `src/smpl_neutral.py` are byte-identical copies of Experiment
2's. `assert_render_code_matches()` hashes both against Experiment 2's originals and
raises if they differ. The sha256 digests are recorded in
`data/lifted_renders/manifest.json`.

Same neutral SMPL body with `betas = 0`, same fixed camera, same lighting, same
grounding, on both sides of the round trip.

If the two sides were rendered differently, this experiment would be comparing
rendering rather than motion.
:::

## The heading rotation

Lifted clips are rotated about the vertical axis onto their own input's heading.
GVHMR's world frame came out at roughly −150° for most clips, and its absolute
heading is arbitrary, so this is a necessary normalisation.

The rotation changes which way the clip points and nothing else. It cannot repair a
front-to-back flip, which is why [`squat`](result-squat.html) stays broken — and a
brute-force search over all yaw angles confirms no rotation rescues it.

## Files

| path | what is in it |
|---|---|
| `src/config.py` | paths, geometry, the condition list read from Experiment 2 |
| `src/prompts.py` | the six prompts and their physical beats |
| `src/reuse.py` | copies Experiment 2's motions, fits and blue renders in |
| `src/render.py` | the blue character render — hash-checked against Experiment 2 |
| `src/smpl_neutral.py` | the neutral body — hash-checked against Experiment 2 |
| `src/lift.py` | GVHMR driver |
| `src/rerender.py` | re-render of the lifted motion, same code as `render.py` |
| `src/analysis.py` | joint error, jerk, foot-skate |
| `src/strips.py` | the time-aligned strips |
| `src/sheet.py` | the original contact sheet |
| `data/smpl/` | the input motions, 12 files, from Experiment 2 |
| `data/renders/` | the blue inputs (A), 12 files, from Experiment 2 |
| `data/videos/` | the 144 videos that go into GVHMR, `floor` included |
| `data/lifted/` | GVHMR output, SMPL-X params at 25 fps, 144 files |
| `data/lifted_renders/` | the re-rendered returned motions (B), 144 files |
| `results/roundtrip.html` | the original contact sheet |
| `results/strips/` | 12 time-aligned strips, input above every return |
| `results/analysis.json` | the supporting numbers |
| `results/NOTES.md` | the written record this write-up is based on |

Each step writes a `manifest.json` with `prompt_id`, `condition`, `K`, `seed` and
`path`, and reads it from the previous step. No globbing. Every seed fixed and
logged.

## What was not built

::: note title="Deliberate omissions"
There is **no metric that decides the verdict**, by design. `results/analysis.json`
opens with the line *"Supporting numbers only; the verdict of this experiment is
visual."* See [The numbers](numbers.html) for why the obvious candidates —
smoothness, ground contact — measure the wrong thing.

There is **no human study**. Six prompts, two seeds and one pair of eyes is not a
basis for a quantitative claim about naturalness; it is a basis for deciding whether
a larger experiment is worth running.
:::

## Clips on this site

Web-sized transcodes — H.264, audio stripped, capped at 720 px wide. The 512x512
originals are unchanged in the experiment folder. The timing strips are downscaled
from about 2100 x 4250; open one full-size to read it.

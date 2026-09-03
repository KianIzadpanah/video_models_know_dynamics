---
title: Overview
nav: Overview
lead: The earlier experiments asked the video model to do two jobs at once, and one of them was a mistake. Here the animation is only a control signal, the appearance comes from text, and the output is a photorealistic person.
---

## The idea, in plain words

A text-to-motion model learns from a few tens of hours of motion capture. A video
model learns from something closer to a million hours of footage of real people
moving. The bet behind this whole project is that all that footage leaves a video
model with a working sense of **how bodies actually move**, and that this is more
useful than its ability to make pretty pixels.

If that is right, a video model should not just be the last step in an animation
pipeline, rendering someone else's motion. It could be the thing that *improves*
the motion, with the motion model demoted to a rough sketch of intent.

## What was wrong with the earlier attempts

In [Experiments 1–3](../exp2/overview.html) the blue character did two jobs at
once. It told the video model **what motion to perform**, and it told the model
**what to look like**.

::: key title="The second job was the mistake"
An untextured blue mesh is nothing like the video model's training data. So the
model spent its capacity holding an appearance it has never seen, instead of using
what it knows about how bodies move.

At loose settings it gave up and did the thing that gives the game away: it drew a
**photoreal person in a pink shirt** instead — the prior pushing back toward its
own domain. That clip is
[still on Experiment 1's page](../exp1/observations.html#box-heavy), and it also
poisoned the pose recovery, which tracked the wrong person.
:::

## So the two jobs get split

| | Experiments 1–3 | This experiment |
|---|---|---|
| what to do | blue character video | **depth video, as a control signal** |
| what to look like | the same blue character | **a text prompt** |
| the output | a blue character | **a photorealistic human** |
| what gets recovered | blue video → SMPL | photoreal video → SMPL |

The recovery step benefits too. Pose recovery is trained on real and photorealistic
footage, so with a photoreal video it is finally operating **in its own domain**
rather than on an untextured mesh.

::: diagram
The pipeline: a motion becomes a depth video, the depth video plus a text prompt
becomes a photoreal video, and the photoreal video becomes motion again.
:::

## What we sweep

When the pose is specified at every frame, a video model behaves like a renderer —
it draws what you gave it, mistakes included. It can only contribute its own sense
of motion in the parts you **leave unspecified**.

So the one variable is how much of the motion we specify:

| condition | frames conditioned |
|---|---|
| `dense` | all 16 latent frames — 0·8·16·…·120 |
| `K = 8` | 0·16·32·48·72·88·104·120 |
| `K = 5` | 0·32·64·88·120 |
| `K = 3` | 0·64·120 |
| `K = 2` | 0·120 — the two ends |

On the frames left free, the depth track is blank mid-grey.

::: stats
6: motions
5: conditions
2: seeds
60: photoreal videos
:::

## What we used

| step | model / tool | notes |
|---|---|---|
| Motion | **MotionGPT3** | the same `.npy` files as Experiments 1–3, not regenerated |
| Control | depth render of the SMPL animation | 121 frames, 25 fps, 704×704 |
| Video | **LTX-2.3 22B distilled** + `LTX-2-19b-IC-LoRA-Depth-Control` | `ICLoraPipeline`, control strength 1.0, **no init frame** |
| Appearance | the text prompt alone | scene and person only, no motion words |
| Video → motion | **GVHMR** | world-grounded SMPL-X, `static_cam=True` |

## What came out of it

::: key title="Three findings"
1. **The split worked completely.** All 60 videos are photorealistic and every one
   is a single person. No blue mesh, no appearance drift, and none of Experiment
   1's second-person artefact. The premise is discharged.
2. **The control holds where you pin it, and only there.** Two frames pin their two
   poses as tightly as sixteen frames pin sixteen — 86 mm against 76 mm. What
   changes is the run in between, which walks away from the input steadily as pins
   are removed.
3. **What fills the free run is the *prompt*, not the motion.** In Experiment 1 the
   free stretches invented events. Here they mostly fill with whatever the person
   in the prompt would plausibly be doing — and because a blank control frame reads
   as "nothing is happening here", plausible often means *idling*.
:::

::: warn title="And the recovery is now the binding constraint"
[`squat`](result-squat.html) fails at every condition — including `dense`, where the
video is a pixel-accurate reproduction of the control. Experiment 1 saw the same
failure and left open whether the untextured blue body was confusing the recovery.

**It was not.** The video here is photorealistic and in the recovery model's own
domain, and it still flips the pose front-to-back. That rules out the domain gap and
points at the camera: one fixed viewpoint on a deeply folded crouch is genuinely
ambiguous.
:::

## Suggested reading order

::: method title="How to work through this"
1. **[Pipeline](pipeline.html)** — what was fed in, the models, and the settings
   that differ from the earlier experiments.
2. **[Did the split work?](does-it-work.html)** — read this before the results. It
   establishes that all 60 videos are usable and that the control does what it
   claims.
3. **The six motions**, one page each — just the clips, with the depth control, the
   photoreal output and the recovered motion side by side at every condition.
4. **[Observations](observations.html)** — what was actually seen in each motion,
   the per-motion numbers, and the caveats.
5. **[What fills the free run](free-run.html)** — the cross-cutting result, and the
   most interesting difference from Experiment 1.
6. **[Verdict](verdict.html)** — what this establishes and what to change next.
:::

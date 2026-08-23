---
title: How it was run
nav: How it was run
lead: Steps 1 to 3 are Experiment 2's, reused rather than regenerated. What is new here is pose recovery, the re-render, and the two control conditions that make the comparison legible.
---

## What is reused, and why that matters

The motions, the SMPL fits, the blue character videos and the keyframe sets all
come **directly from [Experiment 2](../exp2/overview.html)** — the same files, not a
re-run. The condition list is read out of that experiment's keyframe manifest at
runtime, so the two experiments cannot drift apart about what was generated.

::: method title="The render-code identity check"
`src/render.py` and `src/smpl_neutral.py` are byte-identical copies of Experiment
2's. `assert_render_code_matches()` hashes both and fails loudly if they differ.

Both sides of the round trip must be rendered by the same code. If they are not,
the comparison is between two renderers rather than two motions.
:::

## The pipeline

| step | what happens | output |
|---|---|---|
| 1 | MotionGPT3 generates motion from the prompt | HumanML3D `.npy`, 20 fps |
| 2 | fit to neutral SMPL, render the blue character | 121 frames, 25 fps, 512×512 — this is **A** |
| 3 | pick K frames on the latent grid | the conditioning set |
| 4 | LTX-2.5 generates the video from those frames | 121 frames, 25 fps |
| 5 | **GVHMR** recovers motion from the video | SMPL-X params, world-grounded, 25 fps |
| 6 | re-render with the identical render code | this is **B** |
| 7 | build the contact sheet and strips | `results/roundtrip.html`, `results/strips/` |

121 frames go in and 121 frames come out, at every condition. No drift accumulates
through render → generate → recover → render.

## Pose recovery

**GVHMR**, checkpoint `gvhmr_siga24_release.ckpt`. World-grounded SMPL-X output,
`static_cam=True`, no DPVO. The camera in these clips genuinely is static, so
telling GVHMR that is correct and removes a source of noise.

::: note title="The heading rotation"
GVHMR's world frame is arbitrary — it came out at roughly −150° for most clips. Each
lifted clip is rotated about the vertical axis onto its own input's heading before
comparison.

That rotation changes which way the clip points and nothing else. It **cannot**
repair a front-to-back flip, which is why [`squat`](result-squat.html) stays broken.
:::

## The two control conditions

Everything in this experiment rests on these two columns.

### `floor` — no video model at all

The blue video goes straight into GVHMR. Whatever separates `floor` from the input
is the cost of rendering and pose recovery *on their own*.

If `floor` is clean, differences in the other columns can fairly be attributed to
the video model. If it is not, they cannot. This is the first thing to look at on
every page, and it has [its own page](floor.html).

### `K = all` — the video model handed everything

Every 8th frame pinned. The video model has nothing left to invent, so the round
trip should return what went in. It does: 36–44 mm, statistically
indistinguishable from `floor`.

::: key title="Why a null result here is the point"
The brief put it plainly: *if it comes back identical, the video model did nothing.*
`K = all` is exactly what that looks like — and having it in the sweep means the
loose columns can be read against a real zero rather than against an assumption.
:::

## What each result page shows

Every prompt gets its own page, laid out in the same order:

1. **The floor and strong control** — the input next to `floor` and `K = all`. Both
   should be near-copies of the input. If they are not, stop reading.
2. **Source video beside returned motion** — the essential pairing. The left cell is
   the video GVHMR was given; the right cell is the motion it returned. This is the
   only way to catch a plausible-looking lift taken from a broken video.
3. **The two loose values** — `K = 5` and `K = 3_2`.
4. **Placement variants** — the returned motions for all four `K = 3` and all four
   `K = 2` placements.
5. **The numbers for that prompt**, and the **timing strip**: the input above every
   returned motion, time-aligned, as one image.

::: warn title="How to read the strip"
The strip is the fastest way to read timing, and it is also where a broken source
becomes obvious. Click it to open it full size — at grid scale these images are
2000 px tall and unreadable.
:::

## What is deliberately not here

::: note title="No metrics decide anything"
The verdict in this experiment is **visual**. The numbers in
[The numbers](numbers.html) exist for exactly two jobs: to size the `floor` column,
and to flag lifts that should not be trusted.

They are not used to decide whether the motion improved, because the obvious
candidates — smoothness, ground contact — measure the wrong thing. Real human motion
has impacts. [`punch`](result-punch.html) comes back among the *jerkiest* things in
the experiment and is also the most convincingly physical.
:::

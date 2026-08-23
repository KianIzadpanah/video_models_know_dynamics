---
title: Overview
nav: Overview
lead: Send a motion through the video model, then pull it back out as motion again. If the video model really knows how bodies move, what comes back should look more natural than what went in — not identical to it.
---

## The idea, in plain words

[Experiment 2](../exp2/overview.html) showed that when the video model is handed
only a few frames it adds real movement of its own. But "more movement" is not the
same as "better movement". A silhouette that changes faster per frame could be a
more convincing lift, or it could be noise.

The only way to settle that is to get the motion back into 3D and look at it as
motion. So this experiment closes the loop:

1. Generate a motion from text, exactly as before.
2. Render it as the blue character.
3. Hand a few of those frames to the video model, let it generate the rest.
4. Take that generated video and **run pose recovery on it** to get motion back out.
5. Render the recovered motion as the *same* blue character, with the *same* camera
   and lighting.

Now there are two videos of the same blue character: **A**, the motion we started
with, and **B**, the motion that came back. Put them side by side and ask whether
the motion improved.

::: diagram
The round trip: text becomes motion, motion becomes video, the video model
regenerates it from a few frames, and pose recovery turns it back into motion. Both
ends are rendered by identical code so that only the motion differs.
:::

## Why re-rendering both sides matters so much

::: warn title="If the two sides are rendered differently, you are comparing rendering, not motion"
Both A and B are rendered by **byte-identical code** — same neutral SMPL body with
`betas = 0`, same fixed camera, same lighting, same floor. The render scripts are
copies of Experiment 2's, and the pipeline hashes them at runtime and refuses to
run if they have drifted apart.

This is not a nicety. Any difference in body shape, camera or lighting between the
two sides would read as a difference in motion.
:::

## The control that decides whether any of this means anything

Pose recovery is not free. Rendering a motion to video and recovering it again
loses something even when no video model is involved at all. So there is a control
condition called **`floor`**: the blue video goes straight into pose recovery,
skipping the video model entirely.

::: key title="Read the floor column before anything else"
Whatever separates `floor` from the input is damage caused by rendering and pose
recovery on their own. If `floor` already looks different from the input, then
nothing in the other columns can be blamed on the video model.

It comes out at **34–42 mm for 10 of 12 clips** — roughly the width of a wrist. The
round trip is essentially lossless, so differences elsewhere are real.

**One clip fails completely**, and it fails in the control column. See
[The floor](floor.html).
:::

## What we used

| step | model / tool | notes |
|---|---|---|
| Text → motion | **MotionGPT3** | reused from Experiment 2, not regenerated |
| Render | blue character, fixed camera | 121 frames, 25 fps, 512×512 |
| Video generation | **LTX-2.5 dev, 22B** | all eleven of Experiment 2's conditioning sets |
| Video → motion | **GVHMR** | `gvhmr_siga24_release.ckpt`, world-grounded SMPL-X, 25 fps |
| Re-render | the same render code as step 2 | hash-checked at runtime |

::: stats
6: prompts
12: conditions
2: seeds
144: clips lifted and re-rendered
:::

## The conditions

`floor` plus all eleven conditioning sets from Experiment 2 — not just the two
"loose" values, so the **placement** variants can be read here too.

| condition | what it is |
|---|---|
| **`floor`** | the blue video straight into pose recovery. No video model. The control. |
| **`K = all`** | every 8th frame pinned. The video model has nothing to invent. |
| **`K = 9`** | every 16th frame. Still almost fully pinned. |
| **`K = 5`**, **`K = 3_2`** | the two loose values [chosen in Experiment 2](../exp2/verdict.html) |
| the other seven sets | the placement variants, carried through for the same reason |

## What came out of it

::: key title="Two of six prompts come back visibly more natural"
[`box_heavy`](result-box-heavy.html) and [`punch`](result-punch.html) improve.
Three come back different but no better —
[`barbell_heavy`](result-barbell-heavy.html),
[`push_heavy`](result-push-heavy.html),
[`baseball`](result-baseball.html). One,
[`squat`](result-squat.html), is unusable because the lift fails on its own.

**The improvement, where it happens, is specific.** The video model supplies a
*missing part of the action* — the extension of a punch, a kneel and reach for an
object, a box picked up and carried — and pose recovery brings it back as motion
intact. It is not a general smoothing or plausibility fix. Where the motion model's
output was simply wrong for the prompt, the round trip returns something equally
wrong.
:::

::: warn title="The one thing that must be checked every time"
Pose recovery has a motion prior built into it. It can output smooth, natural
looking motion **even when the video it was given was a mess**. Nothing in the
returned motion signals that this happened.

The clearest case: `box_heavy` s5678 at `K = 3_2`. Its source video contains a
photographic person in pink pushing a hand truck alongside the blue character. Pose
recovery tracked one subject through that two-person scene and returned smooth,
entirely plausible motion. **That lift is meaningless for its first ~60 frames, and
it looks fine.**

Every result page therefore shows the **source video next to the returned motion**.
Any conclusion drawn without looking at the source is worthless.
:::

## Suggested reading order

::: method title="How to work through this"
1. **[How it was run](setup.html)** — the pipeline, the models, and what is reused
   from Experiment 2.
2. **[The floor](floor.html)** — the control column. Read this before any result.
3. **The six prompts**, one page each.
4. **[The numbers](numbers.html)** — joint error, jerk and foot-skate, and a careful
   account of what they do *not* say.
5. **[Verdict](verdict.html)** — what this establishes, and the caveats to carry.
:::

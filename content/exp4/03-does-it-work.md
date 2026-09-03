---
title: Did the split work?
nav: Did the split work?
lead: Two things had to be true before any result here means anything: every video is a photorealistic single person, and the depth control actually holds the pose where it says it does. Both are true.
---

## 1. Sixty photoreal videos, sixty single people

::: key title="The premise is discharged"
**Every one of the 60 videos is a photorealistic human, and every one is a single
person.** No blue mesh, no untextured body, no drift to a different appearance
halfway through, and none of Experiment 1's worst artefact — a second photographic
person walking into the shot while pose recovery tracked the wrong one.

Appearance came from the text alone: no init frame, no reference image.
:::

::: clips arms=probe_all60 width=620px
Frame 76 of all sixty clips at a glance. Six motions down, ten clips each — five
conditions at two seeds.
:::

This matters because it removes a confound rather than producing a result. Nothing
on the pages that follow is muddled by the video model fighting an appearance it has
never seen.

## 2. The control holds where you pin it — and only there

Joint error against the input motion, root-relative, in millimetres, on the same
neutral body — split into the frames that were **conditioned** and the frames left
**free**:

| | dense | K = 8 | K = 5 | K = 3 | K = 2 |
|---|---|---|---|---|---|
| **on the conditioned frames** | 76 | 76 | 82 | 80 | 86 |
| **on the frames left free** | 77 | 85 | 101 | 117 | 132 |

*(means over the ten clips that lift correctly; [`squat` excluded](#3-and-one-thing-that-does-not-work))*

::: key title="This is the whole experiment in one table"
**Handing over fewer frames does not weaken the pose at the frames you hand over.**
Two frames pin their two poses as tightly as sixteen frames pin sixteen — 86 mm
against 76 mm, a difference of about a thumb's width. For scale,
[Experiment 1 measured](../exp1/floor.html) the cost of the round trip *alone* —
render, video, recover, re-render, with no video model in the loop — at 34–42 mm.

What changes is everything in between. The free run walks away from the input
steadily, **77 → 132 mm**, as the pins come out.
:::

::: clips arms=probe_depthconds width=900px
The five depth control tracks for one motion. Dense on the left, then progressively
blanker: on a free frame the track is mid-grey.
:::

### dense really is the renderer case

At 77 mm overall, with the pinned and free numbers identical, `dense` is copying
uniformly.

::: clips arms=probe_overlay width=900px
The control silhouette laid over the generated body at `dense` — pixel for pixel.
:::

::: clips arms=probe_dense_ctrl width=980px
`dense` output against its control, same frames side by side.
:::

It copies the mistakes too. `box_heavy`'s input puts **both arms over the head at
frame 72**, in a pose no one lifting a box would produce, and `dense` reproduces it
exactly. That is the brief's prediction confirmed: specify the pose everywhere and
the video model contributes nothing of its own.

### And the pins hold at the sparse conditions

::: clips arms=probe_pinned width=620px
A conditioned frame at a sparse condition, control over output. Even with two frames
in the whole clip, the two poses land.
:::

## 3. And one thing that does not work

::: warn title="squat fails at every condition, including dense"
[`squat`](result-squat.html) is **268–364 mm** from its input at every condition —
including `dense`, where the video is a pixel-accurate reproduction of the control.

The photoreal row is *right*: a man in a gym, squatting, seen from behind, exactly as
the control specifies. The **recovered** row is a different pose.

[Experiment 1 found the same failure](../exp1/result-squat.html) and left open
whether the untextured blue body was confusing the recovery. **It is not.** The video
here is photorealistic and in the recovery model's own training domain, and the pose
still flips front-to-back.

A deeply folded crouch seen from one fixed viewpoint is close to front-back ambiguous
in silhouette, and the recovery resolves it the other way regardless of how the pixels
look. **The fix is a camera, not a renderer.**
:::

Every `squat` row must be discounted. Note also that its error *falls* as
conditioning is removed — 350 → 291 mm — purely because the man squats less and
standing is easier to recover. That is not an improvement in anything.

## 4. Two smaller artefacts, both bounded

::: warn title="The last two frames blow out on 17 of the 48 sparse clips"
The person washes to a near-white silhouette at frames 119–120. Every affected clip
is seed 5678, none are `dense`, and it never reaches further back than frame 119.

The cause is legible: frame 120 is a conditioned frame whose seven neighbours in the
same latent frame are blank, so the latent carries a bright body mixed with mid-grey
and the model paints the mixture. It costs 2 frames in 121 and moves none of the
numbers above.
:::

::: clips arms=probe_blowout width=900px
The frame 119–120 blow-out.
:::

An alternative sparse encoding — holding the conditioned pose across the whole latent
frame it belongs to, rather than as a single-frame impulse — was **built, run and
rejected on the evidence**. It would remove the blow-out, but it was not what the
brief specified and it changes what the control means, so the production runs use the
literal impulse encoding.

::: clips arms=probe_impulse width=760px
The impulse encoding against the hold encoding.
:::

## What these checks license

::: note title="Read this before the results"
Passing means the mechanism works: appearance is text-driven and stable, the pose is
pinned to within about 80 mm at every conditioned frame regardless of how few there
are, and `dense` is a genuine copy so the sweep has a real zero point.

It does **not** mean the motion that comes back is good, or right for the prompt.
That is what the six motion pages and the [observations](observations.html) are for,
and it is judged by eye.
:::

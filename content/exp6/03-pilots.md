---
title: What the pilots settled
nav: What the pilots settled
lead: Four pilots, run before the sweep, and each one fixed something that would otherwise have made the sparse conditions unreadable. Two of them overturned the expected answer.
---

Experiment 4's output had photoreal people standing in **no background at all**.
Three things were wrong at once, and separating them took four pilots. All of the
material is in `data/pilot/`; the measurements are in `results/API_REPORT.md`.

## 1. The missing backgrounds — three candidate causes

1. **704×704 was off-distribution** for the IC-LoRA. The brief already changes this
   to 1216×704, and that change alone does most of the work.
2. **The prompts named a place in two or three words.** Experiment 4's own
   `prompts.py` records the failure directly: the one prompt of six that named no
   surroundings was the one where "the model filled the gap by copying the depth
   track's own flat mid-grey background instead of inventing a gym".
3. **The control video's own backdrop.** Every pixel of the control that is not the
   body says something about the frame, and the model will sometimes draw it.

::: key title="At 1216×704 with a background clause, the backgrounds come back"
Both control formats produce a full photoreal street on `walk` — brick buildings,
parked cars, a sidewalk, sky. So most of the missing background was **resolution and
prompt**, not the control.
:::

## 2. The control format — the expected winner lost

Two formats were built:

- **`flat`** — Experiment 4's, and the brief's: the body alone, camera-space depth
  through a fixed metric window, on a flat mid-grey field.
- **`scene`** — the body on a ground plane receding to the horizon, encoded as
  normalised inverse depth with the empty background at **black**. This is what a
  monocular depth estimator produces, so it is the form the IC-LoRA saw in training.
  It was the expected winner.

::: clips arms=p_flat_dense,p_scene_dense heads=on
The two control formats at `dense`, on `walk`. Left: flat mid-grey. Right: inverse
depth with a receding ground plane.
:::

::: clips arms=p_flat_K3,p_scene_K3 heads=on
The same two at `K = 3` — the body on the conditioned frames, and what fills the
frames between.
:::

::: warn title="scene fails on the clips the brief sets indoors"
Its empty background is black, i.e. **infinitely far** — which an indoor prompt
cannot satisfy. On `kick` ("plain training hall … a mirrored wall behind him") the
model resolved the contradiction by drawing **a black void** with a bare figure
standing on a grey gradient: the control's own appearance, straight through.

On `jump` the black read as a dark ceiling and got away with it. On `kick` it did
not.
:::

::: clips arms=p_kick_scene,p_kick_flat heads=on
`kick` at `dense`. Left: the `scene` control's output — a black void. Right: the
`flat` control's — a training hall with white walls, mirrors, a door and a wooden
floor, held for all 169 frames.
:::

**Flat mid-grey commits to nothing, so the prompt decides.** The run therefore keeps
the brief's own format unchanged. `scene` stays implemented and its output is kept —
it grounds an *outdoor* clip better, and it is the right starting point if the depth
render ever gains a room.

You can compare the two formats on any clip in the set:

::: clips arms=depth_dense,scene_ctrl_dense ids=kick,walk,squat seeds=1234
The production `flat` control against the rejected `scene` control, at `dense`.
:::

## 3. The fade to black — a clip-length property, not a control problem

The first 169-frame generation was correct for five seconds and then faded to black
over its last forty frames. Mean frame brightness, first quarter → last quarter →
last frame, on LTX-2 19B:

| | frames | first ¼ | last ¼ | last frame |
|---|---|---|---|---|
| scene control | 169 | 143.6 | 73.9 | **20.9** |
| flat control | 169 | 157.1 | 119.3 | **60.7** |
| **no control at all** | 169 | 122.0 | 41.6 | **12.5** |
| scene control | 121 | 149.0 | 147.6 | 148.1 |
| no control | 121 | 115.6 | 116.6 | 116.8 |

::: key title="The fade is there with no control at all, and gone at 121 frames"
So it is a property of the model's clip length, not of the depth track. LTX-2 19B's
default clip is 121 frames and it ends a shot at about five seconds — Lightricks'
own default negative prompt lists "transition to black", the same tendency.
:::

::: clips arms=p_none_121,p_none_169,p_scene_169 heads=on
No control at 121 frames (holds), no control at 169 (fades), and with control at 169
(still fades).
:::

Two fixes were measured:

| | frames | conditioned fps | reads as | last frame |
|---|---|---|---|---|
| LTX-2 19B | 169 | 30 | 5.63 s | 87.3 |
| LTX-2 19B | 169 | **33.6** | 5.03 s | **120.0** |
| **LTX-2.3 22B** | 169 | **25** | 6.76 s | **76.7** |

::: clips arms=p_fps34,p_ltx23_169 heads=on
Left: conditioning LTX-2 19B as 33.6 fps while still writing 25 fps — removes the
fade, at the cost of the clip reading as 5.03 s. Right: **LTX-2.3 22B holds the full
6.76 s at 25 fps with no workaround at all.**
:::

The run uses LTX-2.3 22B at 25 fps, which is also the variant Experiment 4 ran. The
frame-rate knob is kept in `generate.py` for anyone rerunning on the 19B base.

## 4. The sparse conditions — the attention mask

The first production pass produced good backgrounds at `dense` and `K = 8`, and then
broke at `K = 3`.

::: warn title="At K = 3 the model stopped rendering the scene and started rendering the control"
In `jump_K3` the stretch between conditioned frames — 0/88 and 88/168 — is not a gym
at all. It is **a grey figure standing on the depth track's own backdrop**.

The cause is structural, not a matter of prompt or format. The reference video is a
full-frame image on *every* frame, and at attention strength 1.0 a blank frame is an
instruction — "this is what the frame looks like" — not an absence of one. Whatever
the blank frame contains, the model will sometimes copy it.
:::

`ICLoraPipeline` has the parameter for exactly this.
`conditioning_attention_mask` is a pixel-space mask, area-downsampled spatially and
averaged temporally in groups of 8, that scales the reference's attention weight
**per latent frame**. It is built from the same conditioned-frame list the depth
video was rendered from, and verified to be exactly binary and to land on exactly
the right latents.

::: clips arms=p_unmasked_K3,p_masked_K3 heads=on
`jump` at `K = 3`. Left, unmasked: a gym for the first third, then the depth track's
grey figure on its own backdrop for the middle third. Right, masked: gym, floor,
windows and reflections held for all 169 frames.
:::

::: clips arms=p_unmasked_K2,p_masked_K2 heads=on
`jump` at `K = 2`. Left, unmasked: holds, but drifts pale and flat. Right, masked:
the scene stable throughout.
:::

::: key title="This removes no pose information"
The latents that carry a conditioned frame are **byte-identical either way**. The
mask only stops the *blank* latents from instructing the model. The number of frames
the condition specifies — the one variable of this sweep — is unchanged.

`dense` conditions every latent frame, so it gets no mask at all.
:::

## What the pilots license

::: note title="Read this before the results"
With all four fixes in place, **every one of the fifty outputs has a real
background** — city streets with brick terraces and parked cars, an athletics track
with lane markings and empty stands, gym interiors with racks and reflections on a
rubber floor, a training hall with mirrors, living rooms with windows and radiators,
a grass field with a treeline. No flat grey voids anywhere in the set.

That is what makes the sparse conditions readable at all. Without the mask in
particular, `K = 3` and `K = 2` would be measuring the model's tendency to copy its
own reference rather than anything about motion.
:::

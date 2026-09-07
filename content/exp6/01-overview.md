---
title: Overview
nav: Overview
lead: Experiment 4 fed the video model a motion that was already wrong. This one feeds it clean motion capture instead, and asks the only question left: how few conditioned frames still produce the right action, six seconds long, in a real place?
---

## The idea, in plain words

Every experiment before this one used **MotionGPT3's** motion as the control. That
was a problem we kept running into rather than a choice: half the time the motion
model had not produced the action in the prompt at all, so "did the video model
improve the motion?" collapsed into "can the video model rescue a motion that was
never right?"

[Experiment 4](../exp4/verdict.html) got the pipeline clean — photoreal output,
appearance from text, pose recovery in its own domain — and then ran into exactly
that. Its clearest positive was a single clip in sixty.

So this experiment changes the input, not the pipeline.

::: key title="Correct animation as control"
The control clips come from **AMASS/BABEL** — real motion capture, ten clips, each
one genuinely performing the action it is labelled with. Prepared in
Experiment 5 and used here unmodified.

That removes the confound. If the action is right going in, then everything the
sweep shows is about the *video model's* contribution, not about a broken input.
:::

::: diagram
The pipeline: a motion-capture clip becomes a depth video, the depth video plus a
text prompt becomes a photoreal video, and the photoreal video becomes motion again.
:::

## What we sweep

The one variable, exactly as in Experiment 4: **how many frames carry a pose.**

| condition | conditioned frames | count |
|---|---|---|
| `dense` | 0·8·16·…·168 | 22 |
| `K = 8` | 0·24·48·72·96·120·144·168 | 8 |
| `K = 5` | 0·40·88·128·168 | 5 |
| `K = 3` | 0·88·168 | 3 |
| `K = 2` | 0·168 | 2 |

On the frames left free, the depth track is blank mid-grey — **and the model is told
not to attend to those frames.** That last part is new here, and it matters: see
[What the pilots settled](pilots.html).

::: stats
10: clips
5: densities
1: seed
50: photoreal videos
:::

## What we used

| step | model / tool | notes |
|---|---|---|
| Motion | **AMASS/BABEL**, via Experiment 5 | ten clean clips, 169 frames @ 25 fps |
| Control | depth render, one fixed camera | body on a flat mid-grey field |
| Video | **LTX-2.3 22B distilled** + `LTX-2-19b-IC-LoRA-Depth-Control` | `ICLoraPipeline`, 1216×704 |
| Appearance | the text prompt alone | scene clause names what is *behind* the person |
| Video → motion | **GVHMR** | world-grounded SMPL-X |

Nothing failed: **pose recovery found and tracked a person in all fifty videos.**

## What came out of it

::: key title="Two frames plus a sentence is enough for the right action"
For **eight of the ten clips the action survives all the way down to two
conditioned frames.** What sparsity costs is not *what* the person does but *when
and where* — the input's trajectory, its timing, its specific stride.

Where copying breaks depends on the motion:
- **`K = 8`** for the fast, high-frequency clips — [jump](result-jump.html),
  [kick](result-kick.html), [throw](result-throw.html)
- **`K = 5`** for the locomotion clips — [walk](result-walk.html),
  [run](result-run.html), [stand up](result-stand-up.html)
- **never sharply** for the slow or near-static ones — [sit down](result-sit-down.html),
  [turn](result-turn.html), [squat](result-squat.html), [wave](result-wave.html).
  They just drift.

**Two frames plus a sentence is enough to produce the right action. It is not enough
to reproduce a particular performance.**
:::

::: key title="dense is the worst-looking condition of the five"
This inverts the obvious ordering, and it is the clearest thing on the whole sheet.

In all ten clips the `dense` output puts the person in **white or off-white clothing,
or bare skin** — the model is reproducing the near-white value of the depth
silhouette itself. Skin, fabric and lighting all come back at `K = 8` and get
*better* as the control gets sparser. By `K = 5` the person is properly dressed, lit
and shadowed.

That is the "video model behaves like a renderer when you specify every frame" point,
showing up in **appearance** rather than in motion.
:::

::: key title="And the model supplies physics the control does not have"
[`sit down`](result-sit-down.html) is the standout. The depth render is a body alone,
with **no chair in it** — and at every density the model puts a stool or a box under
him and sits him on it.

[`squat`](result-squat.html) at `K = 2` does something similar with timing: the input
holds one deep squat for six seconds, and given only the two ends the model performs
*repetitions* — down, up, down again — which is what a person in a gym would actually
do.
:::

::: warn title="Two clips where it goes wrong, and they are different kinds of wrong"
[`throw`](result-throw.html) — the only clip where the **prompt** loses. The overhand
throw reads to the model as a racket sport, so at *every* density, `dense` included,
it hands the man a tennis racket and turns the wind-up into a serve. The prompt names
no ball, and the caution about not naming objects the control lacks cuts both ways:
with nothing named, the model picks its own.

[`run`](result-run.html) — where the model invents fast motion between distant
anchors, it invents badly. Foot skate goes from 180 mm/s in the input to 900–1800
mm/s out.
:::

## Suggested reading order

::: method title="How to work through this"
1. **[Pipeline](pipeline.html)** — what was fed in, the models, and what changed from
   Experiment 4.
2. **[What the pilots settled](pilots.html)** — four pilots fixed the missing
   backgrounds, the fade to black and the sparse conditions. Read this before the
   results; without these fixes none of the sparse conditions would be readable.
3. **The ten clips**, one page each — just the clips, with the depth control, the
   photoreal output and the recovered motion side by side at every density.
4. **[Observations](observations.html)** — what was actually seen in each clip, the
   per-clip numbers and the caveats.
5. **[Where the sweep breaks](where-it-breaks.html)** — the cross-cutting result.
6. **[Verdict](verdict.html)** — what this establishes, and what it does not.
:::

::: warn title="One caution that applies to every row"
Pose recovery has a motion prior and will return smooth, plausible SMPL from a video
that was a mess. **No recovered motion means anything until the photoreal video above
it has been watched**, which is why every grid on every result page shows the two
next to each other.
:::

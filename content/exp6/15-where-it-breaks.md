---
title: Where the sweep breaks
nav: Where the sweep breaks
lead: The cross-cutting result. For eight of ten clips the action survives to two conditioned frames — what sparsity costs is the particular performance, not the action. And the condition that looks worst is the one that specifies most.
---

## The result, in one line

::: key title="What sparsity costs is not what the person does, but when and where"
For **eight of the ten clips the action survives all the way down to two conditioned
frames.** What goes is the input's *trajectory*, its *timing*, and its *specific
stride*.

Two frames plus a sentence is enough for this model to produce the **right action**,
six seconds long, in a real place. It is not enough to reproduce a **particular
performance**.
:::

That is the interesting answer for the project's actual question, and it is a
different answer from the one Experiments 1–4 kept producing. There the question was
always "can the video model rescue a bad motion?" Here the motion is good, so the
question becomes "how much of a good motion does it actually need?" — and the answer
is: much less than you would guess, as long as you only want the action.

## Where copying breaks depends on the motion's frequency

| break point | clips | what they have in common |
|---|---|---|
| **`K = 8`** | [jump](result-jump.html), [kick](result-kick.html), [throw](result-throw.html) | fast, high-frequency events |
| **`K = 5`** | [walk](result-walk.html), [run](result-run.html), [stand up](result-stand-up.html) | locomotion — a path through space |
| **never sharply** | [sit down](result-sit-down.html), [turn](result-turn.html), [squat](result-squat.html), [wave](result-wave.html) | slow or near-static; they just drift |

The pattern is not about how *much* the body moves — `jump` and `squat` are both large
motions — but about **how much information is in the frames you removed.**

A jump at 24-frame spacing has already lost the launch and the apex. A squat held for
six seconds has almost nothing between its endpoints to lose. A walk's path through
space is exactly the thing that only the intermediate frames record, which is why it
survives as an *action* and dies as a *trajectory*.

::: note title="Read squat and wave together to see the mechanism"
[`squat`](result-squat.html) is the cleanest monotone slope in the set — 51 → 168 mm —
and [`wave`](result-wave.html) is essentially flat — 61 → 78 mm, with `K = 8`
marginally *closer* to the input than `dense`.

Both are slow. The difference is that a squat has a definite bottom that only the
middle frames locate in time, and a wave does not have anything the endpoints do not
already imply.
:::

## The pinned frames hold regardless of how few there are

This is the same finding as [Experiment 4's](../exp4/does-it-work.html), reproduced
on clean motion. The per-clip tables in [Observations](observations.html) carry
`err on pinned mm` next to `err on free mm`: the pinned column stays roughly flat
across the sweep while the free column climbs.

**Removing frames does not weaken the frames you keep.** It only widens the gaps you
have not specified — and what fills those gaps is the video model's own idea of the
action.

## dense is the worst-looking condition of the five

::: key title="This inverts the obvious ordering, and it is the clearest thing on the sheet"
In **all ten clips** the `dense` output puts the person in white or off-white
clothing, or bare skin — **the model is reproducing the near-white value of the depth
silhouette itself.**

Skin, fabric and lighting all come back at `K = 8` and get *better* as the control
gets sparser. By `K = 5` the person is properly dressed, lit and shadowed.
:::

That is the brief's own point — a video model behaves like a renderer when the pose is
given at every frame — showing up in **appearance** rather than in motion. Specify
every frame and the model copies the reference, including the reference's greyscale
values, because a depth map is what it was shown.

::: clips arms=vid_dense,vid_K8,vid_K5,vid_K2 ids=walk,kick,squat seeds=1234
Left to right: `dense`, `K = 8`, `K = 5`, `K = 2`. The clothing and lighting get
*better* as the control gets sparser.
:::

It is worth being precise about what this does and does not mean. It is not evidence
that sparse conditioning produces better *motion* — it produces better *pictures*,
because the model is no longer being handed a greyscale image to match on every
frame. But it does say something about what dense control costs: you are spending the
model's capacity on reproducing a depth map.

## The model supplies physics the control does not have

Two clips, two different kinds:

::: key title="An object, and a timing"
[**`sit down`**](result-sit-down.html) — the depth render is a body alone with **no
chair**. At every density the model puts a stool or a box under him and sits him on
it, then keeps him in contact with it. A man lowering himself into a seated position
has to be sitting on *something*, and the model works that out.

[**`squat`**](result-squat.html) at `K = 2` — the input holds one deep squat for six
seconds. Given only the two ends, the model performs **repetitions**. Not a failure to
follow the control: a more plausible six seconds than the control described.
:::

Both are inferences about the physical world rather than about pixels, and both come
from the *unspecified* part of the clip. The `sit_down` chair is the strongest single
piece of evidence for the project's premise in any of the six experiments — and it
turns up on the easiest clip in the set, not the hardest.

## Where it invents badly

::: warn title="Fast motion between distant anchors"
[`run`](result-run.html) — foot skate goes from **180 mm/s in the input to 900–1800
mm/s out** at every sparse density. The model knows what running looks like and does
not know where this runner's feet were.

[`throw`](result-throw.html) at `K = 3` — **nine times the input's jerk**, and 548
mm/s of skate.

Both are clips where the model has to invent a fast, high-frequency gait or arc across
a long gap. That is exactly the case where "plausible" is not enough, because the
plausible version does not have to touch the ground in the same places.
:::

## And sometimes contact is better than the capture's

Against that, foot contact is often **cleaner** than the input's:

| clip | input skate | best output | at |
|---|---|---|---|
| [wave](result-wave.html) | 22.6 mm/s | **1.3** | `K = 2` |
| [squat](result-squat.html) | 39.8 | **10.4** | `K = 5` |
| [sit down](result-sit-down.html) | 40.8 | **13.7** | `K = 8` |
| [kick](result-kick.html) | 101.3 | **38.9** | `K = 2` |

Those are recoveries that stand **more solidly on the floor than the motion capture
did**. It is the same signal [Experiment 4 found](../exp4/free-run.html) — the free
runs there came back with less than half the input's foot skate — and it is the most
consistent quantitative evidence the project has that the video prior knows something
about ground contact.

::: warn title="But it is not a general claim of better motion"
`run` and `throw` go the other way, badly. And smoothness is not the quantity of
interest —
[Experiment 1 established that](../exp1/numbers.html) with `punch`, where the jerkier
motion was the more physical one.

The honest summary is narrower: **for slow and near-static motions, the recovered
contact is better than the capture's; for fast ones invented across long gaps, it is
much worse.**
:::

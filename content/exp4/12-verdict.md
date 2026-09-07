---
title: Verdict
nav: Verdict
lead: The appearance split is a clean win and the control does exactly what it claims. What the model does with the freedom is narrower than hoped — and the recovery step, not the generation, is now what limits the project.
---

## The result, per motion

| motion | verdict |
|---|---|
| [`punch`](result-punch.html) | **yes** — the free run holds a real guard and throws punches that reach extension, which the input never does |
| [`barbell_heavy`](result-barbell-heavy.html) | **once, and decisively** — s1234 at `K = 2` invents a barbell and a deadlift setup. One clip in sixty |
| [`baseball`](result-baseball.html) | **marginally** — a step and a rotation, and a bat the recovery cannot see |
| [`box_heavy`](result-box-heavy.html) | **no** — no box is ever lifted at any condition |
| [`push_heavy`](result-push-heavy.html) | **no** — nothing is ever pushed |
| [`squat`](result-squat.html) | **unusable** — the video is right and the recovery is wrong, at every condition |

## Three conclusions

::: key title="1. The control works exactly as specified, and the appearance split is a clean win"
Sixty photorealistic single-person videos. Pose pinned to within about **80 mm at
every conditioned frame regardless of how few there are** — two frames pin as tightly
as sixteen. And a recovery step that is finally operating in its own domain.

The mistake in [Experiments 1–3](../exp2/overview.html) was making one signal do two
jobs. Separating them removed the appearance drift, the pink-shirt failure, and the
second-person artefact that poisoned Experiment 1's best clip, all at once.
:::

::: warn title="2. What the model does with the freedom is narrower than hoped"
In **one clip of sixty** it supplied a whole missing action. In **one motion of six**
(`punch`) the free run is consistently more physical than the input. Everywhere else
the free run is a plausible person doing plausibly little.

The reason is mechanical, not a limit of the model: a blank control track reads as an
empty scene rather than as permission. See
[What fills the free run](free-run.html).
:::

::: warn title="3. The recovery is now the binding constraint, not the generation"
[`squat`](result-squat.html)'s video is correct at every condition and its lift is
wrong at every condition. One clip in six is lost to a single-viewpoint ambiguity
that **no amount of photorealism fixes** — which this experiment establishes, because
Experiment 1 could not separate the ambiguity from the domain gap and this one can.

Generation is no longer the weak link. Recovery is.
:::

## What to change next, in order

::: method title="Three changes, cheapest first"
1. **Mask the free frames instead of blanking them.** `conditioning_attention_mask`
   is already in the API and was left unused. It would let the unpinned frames be
   *ignored* rather than read as empty, which targets the exact mechanism behind
   finding 2. Same 60 depth tracks, plus a mask. This is the first thing to try.
2. **Add a second camera, or move the one there is off-axis.** That is the fix for
   `squat`, and `squat` is not an exotic pose — it is the second-most common thing in
   a motion dataset. One clip in six failing is a property of the capture setup, not
   bad luck.
3. **Then reconsider what the free run is asked to do.** With masking in place and
   the recovery unblocked, the interesting sweep is no longer "how many frames" but
   what the prompt is allowed to contribute — `punch` improved because the plausible
   idle behaviour for a boxer *is* the action, and that suggests the prompt and the
   control should be designed together rather than independently.
:::

## Where this leaves the project

Taking all four experiments together:

1. **[Exp 0](../exp0/overview.html)** compared a motion model against a video model
   on the same prompts, side by side.
2. **[Exp 2](../exp2/overview.html)** found a real window where a video model
   re-times motion instead of copying it, and that the window is governed by *where*
   the free run sits rather than by how many frames are withheld.
3. **[Exp 1](../exp1/overview.html)** closed the loop and showed the round trip is
   essentially lossless, so motion added in the video survives back into 3D — and
   that the prior **extends** what it is given rather than correcting it.
4. **This experiment** removed the appearance confound entirely, and in doing so moved
   the bottleneck. The generation side is now clean: text-driven appearance, a control
   that holds where you pin it, and sixty usable videos. What is left is a control
   encoding that says "empty" when it means "free", and a recovery step that cannot
   resolve a crouch from one viewpoint.

::: key title="What this experiment could not fix, and Experiment 6 did"
The input motion. MotionGPT3's clips frequently do not perform the action in the
prompt at all, so "did the video model improve the motion?" kept collapsing into "can
the video model rescue a motion that was never right?" — which is why the clearest
positive here is one clip in sixty.

[Experiment 6](../exp6/overview.html) keeps this pipeline and swaps the input for
clean AMASS/BABEL motion capture. With a correct animation as control, **two frames
and a sentence produce the right action** for eight clips of ten, and the model
supplies physics the control does not have. The experiment folders now record the
distinction in their names: *corrupted* animation as control here, *correct* animation
as control there.
:::

::: note title="The bet, and where it stands"
The bet was that a million hours of footage leaves a video model with a working sense
of how bodies move, and that this is more useful than its ability to make pretty
pixels.

The strongest evidence for it so far is small and specific: the invented deadlift in
one clip, `punch`'s extension in six more, and — quietly the most interesting number
in this experiment — **the free runs coming back with less than half the input's
foot-skate**. A plausible person shot by a static camera plants their feet, and the
prior knows it without being asked.

The evidence against a *strong* form of the bet is that none of this happens reliably
yet, and every mechanism tried so far has hit a ceiling that was a property of the
control scheme rather than of the model.
:::

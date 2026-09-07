---
title: Verdict
nav: Verdict
lead: With a correct animation as control, the answer to "how little pose is enough?" is: two frames, if you only want the action. The pipeline is now clean enough that the remaining limits are real ones rather than artefacts.
---

## What this establishes

::: key title="1. Two frames plus a sentence produces the right action"
For **eight of ten clips the action survives to two conditioned frames** — six
seconds of it, in a real place, with a photoreal person. Only
[`kick`](result-kick.html) loses the action, and only
[`throw`](result-throw.html) is mis-read by the prompt.

What sparsity costs is the *particular performance*: the input's trajectory, its
timing, its stride. See [Where the sweep breaks](where-it-breaks.html).
:::

::: key title="2. The video model supplies physical inferences the control lacks"
[`sit down`](result-sit-down.html) has no chair in its depth control and no chair in
its prompt, and at **every** density the model puts a stool under him and sits him on
it. [`squat`](result-squat.html) at `K = 2` turns a six-second static hold into
repetitions.

For slow and near-static motions the recovered foot contact is **better than the
motion capture's** — `wave` 22.6 → 1.3 mm/s, `squat` 39.8 → 10.4, `sit_down`
40.8 → 13.7.

This is the clearest evidence the project has produced for its own premise.
:::

::: key title="3. Dense control is not the good end of the sweep"
`dense` is the **worst-looking** condition of the five in all ten clips — the model
reproduces the near-white value of the depth silhouette and dresses the person in
white. Appearance improves monotonically as the control gets sparser.

Specify every frame and you spend the model's capacity making it match a greyscale
image.
:::

## What it does not establish

::: warn title="It is not enough to reproduce a performance"
[`walk`](result-walk.html) is the clean demonstration: from `K = 5` the model
substitutes a plain steady walk across frame and never makes the input's turn. The
action is right; the path is invented.

If the goal is "generate motion that looks natural", this is fine. If the goal is
"improve *this* motion", sparse control does not do it — it replaces the motion with
a generic one that happens to share the same label.
:::

::: warn title="Fast motion across long gaps is invented badly"
[`run`](result-run.html) skates 5–10× worse than its input at every sparse density.
[`throw`](result-throw.html) at `K = 3` has nine times the input's jerk. The model
knows what running looks like and does not know where this runner's feet were.
:::

::: warn title="The prompt can lose, and it does so silently"
[`throw`](result-throw.html) gets a tennis racket at every density, `dense` included.
The prompt named no ball, and an overhand arc in athletic wear on an outdoor field is
a serve as readily as a throw.

The caution about not naming objects the control lacks **cuts both ways**: name
nothing and the model picks its own. That is a prompt-design finding, not a model
limitation, and it is a one-word fix that was deliberately not made mid-sweep.
:::

::: warn title="Recovery still fails on floor-level poses"
[`stand up`](result-stand-up.html) starts prone, and even `dense` is 140 mm — the
highest `dense` error of the ten. That is pose recovery struggling, not the video
model.

It is the same failure as [Experiment 4's `squat`](../exp4/observations.html#squat)
and [Experiment 1's](../exp1/result-squat.html): one fixed viewpoint on a compact,
floor-level body. Three experiments have now hit it. **The fix is a second camera**,
and it has been the outstanding item since Experiment 1.
:::

## What the pilots contributed, separately from the sweep

Three of them overturned an expectation, which is worth recording:

1. **The expected best control format lost.** Inverse depth with a receding ground
   plane is what a real depth estimator outputs, so it should have been the
   in-distribution choice. Its black background means *infinitely far*, which an
   indoor prompt cannot satisfy — and on [`kick`](result-kick.html) the model drew a
   black void instead of a training hall. Flat mid-grey commits to nothing, so the
   prompt decides.
2. **The fade to black was not a control problem.** It appears with no control at all
   and vanishes at 121 frames: a clip-length property of LTX-2 19B. LTX-2.3 22B holds
   6.76 s with no workaround.
3. **A blank reference frame is an instruction, not an absence.** At attention
   strength 1.0 the model will draw whatever the blank frame contains — which at
   `K = 3` meant drawing the depth track itself into the free stretch.
   `conditioning_attention_mask` fixes it, and removes no pose information.

That third one is the change [Experiment 4's verdict](../exp4/verdict.html) named as
"the first thing to try next". It was tried, it worked, and it is what makes the
sparse conditions in this run readable at all.

## Where this leaves the project

::: note title="Six experiments, and what each settled"
1. **[Exp 0](../exp0/overview.html)** — motion model against video model, side by
   side, same prompts.
2. **[Exp 2](../exp2/overview.html)** — there is a window where a video model re-times
   motion instead of copying it, and it is governed by *where* the free run sits.
3. **[Exp 1](../exp1/overview.html)** — the round trip is essentially lossless, so
   motion added in the video survives back to 3D. The prior **extends**; it does not
   correct.
4. **[Exp 4](../exp4/overview.html)** — splitting "what to do" from "what to look
   like" removes the appearance confound entirely. But with MotionGPT3 motion as the
   input, one clip in sixty supplied a missing action.
5. **Exp 5** — ten clean AMASS/BABEL clips, prepared so this experiment could stop
   asking the wrong question.
6. **This experiment** — with a correct animation as control, two frames and a
   sentence produce the right action, and the model supplies physics the control does
   not have.
:::

::: key title="The bet, and where it stands now"
The bet was that a million hours of footage leaves a video model with a working sense
of how bodies move.

**The strongest evidence is no longer anecdotal.** A chair invented under a man who
has to sit on something, at every density. Squat repetitions replacing an implausible
six-second hold. Foot contact cleaner than the motion capture's on every slow clip.
And the right action from two frames, ten times out of ten in the clips where the
prompt did not misfire.

**What is still missing is control.** The model will give you the action; it will not
give you *your* action. Every experiment so far has hit a ceiling that was a property
of the control scheme — keyframe placement in Exp 2, blank-frame semantics in Exp 4,
and here the fact that the frames carrying a specific performance are exactly the ones
sparsity throws away. A control signal that is *dense but weak*, rather than sparse
and absolute, is the obvious thing this points at and none of the six experiments has
tried it.
:::

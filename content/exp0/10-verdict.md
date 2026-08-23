---
title: Verdict
nav: Verdict
lead: Pulling the six result pages together — the three matched pairs against the three unloaded controls. This is where the experiment's question actually gets answered, and the answer has to be stated as narrowly as the evidence allows.
---

## The question, restated

Given identical text, does the video model show the **weight** of an action — the
lean, the brace, the slow controlled lift — where the motion model shows a generic
version of it?

The design answers this by contrast in two directions at once:

- **Within a pair**, one word changes. A response to that word is a response to
  load.
- **Between the pairs and the controls**, the load is removed entirely. If the video
  arms lead by the same margin on `punch`, `squat` and `baseball` as they do on the
  pairs, then the effect is about video realism and not about weight.

## The matched pairs

::: todo title="Verdict on the loaded prompts"
Pull the three pairs together — [box](result-box.html),
[barbell](result-barbell.html), [push](result-push.html).

Was there a consistent heavy/light response in any arm? State it as narrowly as the
evidence allows: three pairs at three seeds, judged by eye, supports "we saw X in
these clips" and **not** "video models represent weight".

If the pairs disagree with each other, that is worth more than either result alone —
say which agreed and which did not.
:::

## The unloaded controls

::: todo title="Observations — unloaded prompts"
The question these answer is narrow, so answer it narrowly:

- On [punch](result-punch.html), [squat](result-squat.html) and
  [baseball](result-baseball.html), is the gap between the T2M and video arms **as
  large** as it was on the loaded prompts, smaller, or larger?
- If the gap is just as large here, the loaded-prompt result is about video realism
  in general rather than about weight specifically. Say so if that is what the clips
  show.
- `squat` is the cleanest case for the motion model. Does T2M actually win there?
:::

::: method title="Why the control page matters more than it looks"
A finding on the loaded pairs is only interesting relative to the controls. "The
video model showed the weight" requires that the video model **not** show an equal
advantage on prompts where there is no weight to show.
:::

## What this experiment licenses

::: warn title="The limits of this design"
There is no metric here and no human study. The experiment produces matched clips
and lays them out so a difference — if there is one — can be seen. Any quantitative
claim about weight or effort would need a separate experiment with an actual
estimator.

The three arms also differ in resolution, frame rate, clip length and visual style
**by construction**. Those differences are documented in
[Reading the clips](reading-the-clips.html) rather than normalised away, and several
of them look like findings if you do not know they were designed in.
:::

## Where the project went from here

This experiment compared the two model families side by side. The next two stopped
comparing them and started **combining** them — putting the motion model's output
*through* the video model, to ask what the video model adds:

- **[Experiment 2](../exp2/overview.html)** renders the motion as a blue character,
  hands the video model only some of those frames, and measures how much motion it
  adds. It found a real window where the video model re-times the action rather than
  copying it.
- **[Experiment 1](../exp1/overview.html)** closes the loop, pulling motion back out
  of those videos to ask whether the added movement is *better* motion rather than
  just more of it. Two of six prompts come back visibly more natural.

Six of the nine prompts on this page carry forward into both — `box_heavy`,
`barbell_heavy`, `push_heavy`, `punch`, `squat` and `baseball` — so the T2M clips
here are literally the inputs those experiments start from.

---
title: Observations
nav: Observations
lead: Everything the six result pages leave out — what each prompt is testing, what to look for in it, and where the observations still need writing. The result pages carry the clips; this page carries the reading of them.
---

::: warn title="Read the conventions first"
Several things that look like findings in these clips were designed in:
[Reading the clips](reading-the-clips.html) lists five of them. The clip lengths, frame
rates and visual styles differ between arms by construction, and the T2M arm's
roughness on the fast prompts is partly a
[joints-to-SMPL fitting artefact](fit-quality.html).
:::

This experiment's `NOTES.md` deliberately records only what was built and run, leaving
the visual read to the reader. So the observation blocks below are still open. Each one
lists the specific questions to answer, and the build counts them, so they cannot be
shipped by accident.

---

## Box pair

**"a person lifts a heavy box from the floor"** against **"a person lifts a light box
from the floor"** — the first of three primary comparisons.
[Clips →](result-box.html)

The top row is the heavy prompt, the bottom row its light counterpart; the columns are
the three arms. Compare **down a column** to see whether the load word changed anything,
and **across a row** to see how the three arms rendered the same sentence.

::: note title="Use the toolbar"
Each pair was generated at seeds 0, 1 and 2 — worth cycling through, because
MotionGPT3's clip length is seed-dependent and single-seed impressions of generative
output are unreliable. Slowing playback to ½× or ¼× is the fastest way to judge the
moment the object leaves the floor. Click any clip to step through it frame by frame.
:::

::: todo title="Observations — box"
Write what you actually see. Things worth stating explicitly if they hold:

- Does the **T2M** arm differ at all between the heavy and light rows, or is it the same
  generic pick-up twice?
- In **T2V**, is there a visible brace — hips back, torso angle, knee bend before the
  lift — and does it differ between rows?
- How long does the **I2V** arm spend in the idle pose before committing, and does the
  load word change the trajectory once it does?
- Does the effect survive across seeds 0, 1 and 2, or is it a one-seed coincidence?
:::

### Why this pair is the cleanest test

A box is the most generic possible load: no technique, no implement, no stereotyped
form. That means a difference between these two rows is hard to attribute to anything
except the load word itself.

It is also the prompt that turned out to matter most in the two later experiments. In
[Experiment 2](../exp2/result-box-heavy.html) it is the only prompt where the video
model invents the named object and performs the action, and in
[Experiment 1](../exp1/result-box-heavy.html) it is one of two prompts whose motion
comes back visibly more natural than it went in.

---

## Barbell pair

**"a person lifts a heavy barbell from the ground"** against **"a person lifts a light
barbell from the ground"** — the same single-word contrast, applied to an action with a
learned, stereotyped form. [Clips →](result-barbell.html)

A barbell lift has a technique. That makes this pair a second, sharper question: not
just *does the model respond to the load word*, but *does it reproduce a learned
technique* rather than a generic bend-and-straighten.

::: todo title="Observations — barbell"
As with the box pair, plus two things specific to this one:

- Does either video arm produce plausible **plate sizes** on the bar, and does plate size
  track the load word? That would be the model expressing weight through the *object*
  rather than through the body — a different mechanism entirely, and worth calling out
  separately if it happens.
- Is the bar path straight and close to the body, or does the model produce a generic
  lift with a barbell attached?
:::

::: todo title="Do the two lift pairs agree?"
If the heavy/light contrast appears in one pair and not the other, say so and say which.
Two prompts is not enough to generalise from, but a disagreement between them is more
informative than either result alone.
:::

::: note title="What later experiments found on this prompt"
`barbell_heavy` became the clearest negative case in the project.
[Experiment 2](../exp2/result-barbell-heavy.html) found that MotionGPT3's clip is an
arm-raise rather than a lift, and that **no** conditioning set gets the video model to
draw a barbell — in direct contrast to the box. That comparison is what established that
the video prior *extends* what it is given rather than correcting it.

Whatever you see in the T2M column here is the same output that finding rests on.
:::

---

## Push pair

**"a person pushes a car"** against **"a person pushes a cart"** — the third matched
pair, where the load difference is carried by the noun rather than by an adjective.
[Clips →](result-push.html)

The `push` pair is structurally different from the two lift pairs. There is no *heavy* or
*light* in either prompt; the weight is implied entirely by the object. A model that only
reacts to explicit effort adjectives should fail here while still passing the box and
barbell pairs, which makes this a useful separator.

Pushing has a distinctive signature under load — forward lean, straight arms, low body
line, small steps — so it is fairly legible even in the untextured T2M render.

::: todo title="Observations — push"
Write what you see. Specific things to check:

- Does **T2M** produce a lean at all? A pushing motion without an object is ambiguous in
  mocap, so it may render as walking with arms out.
- Does **T2V** put an actual car and an actual cart in frame, and does the body posture
  differ between them?
- Does **I2V** ever produce the object, given that its conditioning frame shows an empty
  grey floor?
- Is the car/cart contrast stronger or weaker than the explicit heavy/light contrast in
  the [box](#box-pair) and [barbell](#barbell-pair) pairs?
:::

::: warn title="A confound specific to this pair"
*Car* and *cart* differ by more than weight — they differ in size, in what the hands
contact, and in how common each is in video training data. A difference between these two
rows is **not** cleanly attributable to weight the way the box and barbell pairs are,
where a single adjective is the only thing that changed.
:::

::: note title="What later experiments found on this prompt"
`push_heavy` turned out to be the lowest-energy input of the six prompts carried forward.
[Experiment 2](../exp2/result-push-heavy.html) found no car is ever drawn at any
conditioning set, and [Experiment 1](../exp1/result-push-heavy.html) found the motion
comes back *smoother* than it went in and no better.

If the T2M column here already looks close to static, that is the same output those
findings rest on.
:::

---

## punch

**"a person throws right and left punches"** — the first of three unloaded controls.
Fast, repeated, ballistic motion where the interesting dynamics are inertial rather than
gravitational. [Clips →](result-punch.html)

### Why the unloaded prompts are here

If the video arms show more convincing dynamics on the loaded prompts, the obvious
objection is that they show more convincing dynamics on *everything* — that the effect is
about video realism, not about weight.

`punch`, [`squat`](#squat) and [`baseball`](#baseball) test that. None involves carrying a
load. A finding on the loaded pairs is only interesting **relative to these three**.

::: todo title="Observations — punch"
- Do the arms actually reach **extension**, in any of the three columns?
- Is the **alternation** right — left and right punches with recovery between, or
  undifferentiated flailing?
- Does hip rotation lead the arm, or does the arm move alone?
- Is the gap between T2M and the video arms **as large** as it was on the loaded pairs,
  smaller, or larger? This is the question the control prompts exist to answer.
:::

This is also one of the two prompts where the joints-to-SMPL fit residual is highest (see
[Fit quality](fit-quality.html)), so some of the roughness in the T2M column is fitting
error rather than model output.

::: note title="What later experiments found on this prompt"
`punch` became one of the two positive results in
[Experiment 1](../exp1/result-punch.html): the video model extends a tentative guard into
actual punches with full arm extension, and the round trip brings them back as motion. It
is also the one case in the project where a *rougher* returned motion reads as more
physical rather than as noise — because a real punch is jerky.

If the T2M column here never reaches extension, that is precisely the gap the video model
later filled.
:::

---

## squat

**"a person squats down"** — body weight only, slow, and highly stereotyped. Of the nine
prompts this is the one a motion model should handle best: it is common in HumanML3D and
needs no object. [Clips →](result-squat.html)

If the motion model is going to win anywhere, it should be here.

::: todo title="Observations — squat"
- Is the **descent controlled**, or does the character drop?
- Is there a recognisable bottom position, and how long is it held?
- Is the drive back up present at all?
- **Does T2M actually win here?** This is the cleanest case for the motion model in the
  whole prompt set, so a loss on this prompt would be informative.
:::

::: note title="What later experiments found on this prompt"
`squat` produced the sharpest result and the sharpest failure in the project.

In [Experiment 2](../exp2/result-squat.html) MotionGPT3 drops into a squat and **holds the
bottom for four seconds** — a plausible reading of the sentence and an implausible piece
of human motion. From `K = 5` downward the video model refuses that hold and turns it into
repeated reps, the highest single re-timing effect in the sweep.

In [Experiment 1](../exp1/result-squat.html) none of that could be confirmed in 3D,
because pose recovery resolves a deeply folded crouch front-to-back the wrong way — and it
does so in the control column, before the video model is involved.

If the T2M column here holds a long static bottom position, that is the input both of
those findings start from.
:::

---

## baseball

**"a person hit a ball with baseball bat"** — needs an implement, a target, and a full
kinetic chain. The most demanding of the three controls. The prompt's grammar is the
specification's verbatim wording and was not corrected. [Clips →](result-baseball.html)

::: todo title="Observations — baseball"
- Is there a **weight shift onto the back foot** before the swing, and a pause?
- Does either video arm produce a **bat**? A ball?
- Is the rotation through contact fast relative to the wind-up, or is the whole motion one
  uniform speed?
- Like `punch`, this prompt has a high joints-to-SMPL fit residual (see
  [Fit quality](fit-quality.html)) — discount some of the T2M column's roughness
  accordingly.
:::

::: note title="What later experiments found on this prompt"
`baseball` came out **marginal** in both later experiments.
[Experiment 2](../exp2/result-baseball.html) found a leg lift and a rotation that read as a
batting stride at two conditioning sets and nowhere else, with no bat ever drawn.
[Experiment 1](../exp1/result-baseball.html) found the stride comes back as motion, but
with foot-skate roughly doubled — more dynamic, not more natural.
:::

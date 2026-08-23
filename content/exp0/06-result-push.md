---
title: Result 3 — push pair
nav: Result 3 · push (car/cart)
lead: "A person pushes a car" against "a person pushes a cart." The third matched pair, where the load difference is carried by the noun rather than by an adjective.
---

The `push` pair is structurally different from the two lift pairs. There is no
*heavy* or *light* in either prompt; the weight is implied entirely by the object. A
model that only reacts to explicit effort adjectives should fail here while still
passing the box and barbell pairs, which makes this a useful separator.

## The clips

::: clips arms=t2m,t2v,i2v ids=push_heavy,push_light seeds=0,1,2
The `push` pair. Car above cart. Pushing has a distinctive signature under load —
forward lean, straight arms, low body line, small steps — so it is fairly legible
even in the untextured T2M render.
:::

::: todo title="Observations — push"
Write what you see. Specific things to check:

- Does **T2M** produce a lean at all? A pushing motion without an object is
  ambiguous in mocap, so it may render as walking with arms out.
- Does **T2V** put an actual car and an actual cart in frame, and does the body
  posture differ between them?
- Does **I2V** ever produce the object, given that its conditioning frame shows an
  empty grey floor?
- Is the car/cart contrast stronger or weaker than the explicit heavy/light
  contrast in the [box](result-box.html) and [barbell](result-barbell.html) pairs?
:::

::: warn title="A confound specific to this pair"
*Car* and *cart* differ by more than weight — they differ in size, in what the hands
contact, and in how common each is in video training data. A difference between
these two rows is **not** cleanly attributable to weight the way the box and barbell
pairs are, where a single adjective is the only thing that changed.
:::

::: note title="What later experiments found on this prompt"
`push_heavy` turned out to be the lowest-energy input of the six prompts carried
forward. [Experiment 2](../exp2/result-push-heavy.html) found no car is ever drawn
at any conditioning set, and [Experiment 1](../exp1/result-push-heavy.html) found
the motion comes back *smoother* than it went in and no better.

If the T2M column here already looks close to static, that is the same output those
findings rest on.
:::

Next: the three [unloaded controls](result-punch.html), starting with `punch`.

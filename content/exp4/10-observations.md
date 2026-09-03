---
title: Observations
nav: Observations
lead: Everything the six motion pages leave out — what was actually seen in each, the per-motion numbers, and the caveats. The motion pages carry the clips; this page carries the reading of them.
---

The question below is always asked **of the motion, not of the picture**. The picture
is better everywhere, trivially, because one side is a photograph and the other is an
untextured mesh.

Joint error is root-relative against the input motion, in millimetres. Read
[Did the split work?](does-it-work.html) first — it establishes that all 60 videos are
usable and that `dense` is a genuine copy.

::: warn title="The check that applies to every section below"
Pose recovery has a motion prior. It can return smooth, plausible motion from a video
that does not support it, and nothing in the output says so. Every conclusion here was
read off the **photoreal row** before the recovered row.
:::

---

## box_heavy

**"a person lifts a heavy box from the floor"** · warehouse worker in a warehouse —
**no.** No box is ever lifted, at any condition. [Clips →](result-box-heavy.html)

### What we observed

`dense` (65/59 mm) and `K = 8` (74/68 mm) faithfully copy the input's
crouch-and-flail, **including the arms-overhead moment at frame 72** that no one
lifting a box would produce. That is the renderer case working as advertised.

`K = 5` (80/74 mm) gives one crouch and then stands. `K = 3` (140/110 mm) and
`K = 2` (110/150 mm) stand or walk. At `K = 2` seed 5678 the man simply walks across
the frame.

::: warn title="This is weaker than Experiment 1, and the reason matters"
[Experiment 1's loose conditions on this same motion](../exp1/result-box-heavy.html)
invented a cardboard box and carried it off. Here nothing is invented — the free run
fills with a warehouse worker standing in a warehouse, shifting his weight.

The mechanism is the blank control track. See
[What fills the free run](free-run.html).
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=box_heavy cols=seed:seed,condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,foot_skate_out_mm_s:skate mm/s sort=num_conditioned
The two error columns are the whole story: the pinned column barely moves, the free
column climbs as pins come out.
:::

---

## barbell_heavy

**"a person lifts a heavy barbell from the ground"** · weightlifter in a gym —
**once, and decisively.** [Clips →](result-barbell-heavy.html)

### What we observed

Everywhere except one clip this is arm-waving in a gym, which is what went in.
`dense` 61/64 mm, rising to `K = 2` at 169/132 mm.

::: key title="The best single result in the experiment — seed 1234 at K = 2"
MotionGPT3 never produced a barbell lift for this motion.
[Experiment 2 established](../exp2/result-barbell-heavy.html) that no conditioning
set rescues it, and [Experiment 1's round trip](../exp1/result-barbell-heavy.html)
could not invent one.

Here, with **only frames 0 and 120 pinned**, a loaded barbell appears on the gym
floor in the last third of the clip, and the man walks to it and folds into a
deadlift setup, hands to the bar. **Pose recovery brings that hip hinge back intact
as SMPL.**

It is the single clearest case in this experiment of the video model contributing an
action the motion model could not produce.
:::

::: clips arms=probe_deadlift width=980px
`barbell_heavy` s1234 at `K = 2` — the photoreal row, and the recovered motion
underneath it.
:::

It did not repeat on seed 5678, which gestured instead. One clip in sixty.

::: note title="This motion's prompt was changed mid-run"
It was the only one of the six naming no scene, and at `dense` on seed 1234 the model
copied the depth track's flat grey background instead of inventing a gym. A scene
clause was added and all ten barbell videos were regenerated. See
[Pipeline](pipeline.html#appearance-comes-from-text-alone).
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=barbell_heavy cols=seed:seed,condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,foot_skate_out_mm_s:skate mm/s sort=num_conditioned
:::

---

## push_heavy

**"a person pushes a car"** · man on a suburban street beside a parked car —
**no.** [Clips →](result-push-heavy.html)

### What we observed

The input is close to static and so is every output: a man stands on a street beside
a parked car with one arm out, and lowers it. **No car is ever pushed, at any
condition.**

These are the **lowest errors in the whole run** — 46 to 109 mm — simply because
there is so little motion to get wrong. On seed 5678 at `K = 8` the error is 46 mm,
below `dense`'s 69 mm, which says nothing about quality and everything about the
input being nearly still.

::: note title="Consistent with both earlier experiments"
[Experiment 2](../exp2/result-push-heavy.html) found no car is ever drawn at any
conditioning set. [Experiment 1](../exp1/result-push-heavy.html) found the motion
comes back smoother than it went in and no better. Three experiments, three ways of
asking, same answer: there is nothing in this input for the video model to develop.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=push_heavy cols=seed:seed,condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,foot_skate_out_mm_s:skate mm/s sort=num_conditioned
:::

---

## punch

**"a person throws right and left punches"** · boxer in a boxing gym — **yes.** The
one motion where the free run reads as more physical rather than just different.
[Clips →](result-punch.html)

### What we observed

::: key title="Yes"
The input is a boxing guard with small arm movement that **never reaches
extension**. `dense` (83/99 mm) copies exactly that.

From `K = 8` down the man holds a **real guard, moves his feet, and throws punches
that reach extension** — and the recovered SMPL brings them back as a more definite,
better-organised guard than the input carried.

This is the one motion where the free run is consistently more physical rather than
merely different. It is also
[where Experiment 1 landed](../exp1/result-punch.html), from the other direction.
:::

The prompt is doing part of the work here, and that is the point: the boxer keeps a
guard, steps and throws the occasional punch **at every sparse condition**, because
the prompt put him in a boxing gym. When the plausible idle behaviour for the person
in the prompt *is* the action you asked for, a blank control track costs you nothing.

Errors run 83/99 mm at `dense` to 125/117 mm at `K = 2` — the flattest sweep of the
six after `push_heavy`, on a motion that is genuinely moving.

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=punch cols=seed:seed,condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,foot_skate_out_mm_s:skate mm/s sort=num_conditioned
:::

---

## squat

**"a person squats down"** · man in a gym — **unusable.** The video is right at every
condition and the recovery is wrong at every condition.
[Clips →](result-squat.html)

### The failure

::: warn title="268–364 mm from its input at every condition, including dense"
The photoreal row is **correct**: a man in a gym, squatting, seen from behind,
exactly as the control specifies. The recovered row is a different pose.

At `dense` the video is a pixel-accurate reproduction of the control, so there is
nothing left to blame on the generation.
:::

### Why this result is worth more than one lost clip

[Experiment 1 found the same failure](../exp1/result-squat.html) and could not tell
whether the untextured blue body was confusing pose recovery. **This experiment
settles it.**

::: key title="The domain gap is ruled out"
The video here is photorealistic, is in the recovery model's own training domain, and
the pose still flips front-to-back. A deeply folded crouch seen from **one fixed
viewpoint** is close to front-back ambiguous in silhouette, and the recovery resolves
it the other way regardless of how the pixels look.

So it is not the renderer, and it is not the appearance. **It is the camera.** A
second angle, or an off-axis camera, before running this at any scale.
:::

Note that the error *falls* as conditioning is removed — 350 → 291 mm on seed 1234 —
purely because the man squats less and standing is easier to recover. That is not an
improvement in anything, and it is a good example of why a single error number cannot
be read as quality.

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=squat cols=seed:seed,condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,foot_skate_out_mm_s:skate mm/s sort=num_conditioned
The flatness of this column across conditions is the diagnosis: if the generation
were at fault, `dense` would be low and the sparse conditions high.
:::

---

## baseball

**"a person hit a ball with baseball bat"** · baseball player on a field —
**marginally.** [Clips →](result-baseball.html)

### What we observed

`dense` (98/94 mm) copies the input's arm-raise-and-twist, **with a bat in hand**.
`K = 8` and `K = 5` add a step and a rotation that read more like a batting stride.

But no contact is ever made with anything, **the implement varies from clip to
clip** — bat, fielder's glove, or nothing — and a prop is something the recovery
cannot see. So what comes back as *motion* is only slightly more dynamic. The same
verdict as [Experiment 1](../exp1/result-baseball.html).

::: key title="The props are evidence, even though they do not survive the lift"
The baseball player picks up a bat and takes a stance in **seven of his ten clips**,
including at `dense`, and in `s5678` at `K = 8` he is handed a fielder's glove
instead and catches and throws. Neither the bat nor the glove is in the control or in
the input motion.

The recovery returns a body and nothing else, so none of it comes back as motion. But
it is visible evidence that the video model is **reasoning about the action**, not
only about pixels. In the two loosest `s5678` clips he carries nothing at all and a
bat lies on the ground beside him.
:::

::: warn title="Distant background people"
Four of the twelve `baseball` clips put other players out on the field, forty or more
metres back and a few dozen pixels tall. The subject dominates every frame and the
tracker takes a single track, so **no lift here was contaminated** the way
[Experiment 1's `box_heavy` s5678 was](../exp1/observations.html#box-heavy) — but it
is the failure mode to keep checking for.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=baseball cols=seed:seed,condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,foot_skate_out_mm_s:skate mm/s sort=num_conditioned
:::

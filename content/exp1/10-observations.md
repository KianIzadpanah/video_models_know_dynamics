---
title: Observations
nav: Observations
lead: Everything the six result pages leave out — what was actually seen in each prompt, the per-prompt numbers, and the caveats. The result pages carry the clips; this page carries the reading of them.
---

Joint error is quoted root-relative against the input motion, in millimetres, mean
over 22 joints and 121 frames. The **floor** figure is the control: the blue video
lifted with no video model in the loop. Read [The floor](floor.html) before any of
this, and [The numbers](numbers.html) for why smoothness is not used to decide
anything.

::: warn title="The check that applies to every section below"
Pose recovery has a motion prior built into it. It can output smooth, natural-looking
motion **even when the video it was given was a mess**, and nothing in the returned
motion signals that this happened.

Every conclusion here was checked against its source video. The `box_heavy` s5678
`K = 3_2` case below is why.
:::

---

## box_heavy

**"a person lifts a heavy box from the floor"** — **yes, clearly.** The motion that
comes back is a purposeful kneel-and-reach where the input was a vague flail.
[Clips →](result-box-heavy.html)

### What went in

MotionGPT3's clip is a **vague crouch-and-flail**. At frame 72 it puts both arms over
the head, in a pose no one lifting a box would produce. `floor` reproduces that
faithfully, arms and all — which is exactly what a good control column should do.

Floor: 36 mm on both seeds. Clean.

### What we observed

::: key title="Yes, clearly"
At **`K = 5`** what comes back is a calmer, plausible crouch-and-reach. **The
arms-overhead moment is gone.**

At **`K = 3_2` / `K = 2_2`, seed 1234**, the source video has the character kneel and
reach into an invented cardboard box, and GVHMR recovers that motion cleanly —
correctly excluding the box from the body. What comes back is a purposeful
kneel-and-reach: **a better rendition of "lifts a heavy box from the floor" than
anything that went in.**
:::

`K = 5` sits at 117 mm (s1234) and 80 mm (s5678); `K = 3_2` at 139 mm and 143 mm.

::: warn title="Seed 5678 at K = 3_2 — the most important clip in the experiment"
Its first half is **not the blue character at all**. The video model drew a
photographic person in pink pushing a hand truck alongside it. GVHMR tracked one
subject through a two-person scene and returned smooth, entirely plausible SMPL for
it.

**That lift is meaningless for the first ~60 frames, and it looks fine.** Nothing in
the returned motion signals the problem. On the
[result page](result-box-heavy.html#source-video-beside-returned-motion-k-5-and-k-3-2)
switch the seed selector to 5678 and compare the two cells.

It is the clearest example in the experiment of why the source video has to be looked
at, and the reason every result page shows both sides.
:::

### Where the action comes from

::: key title="The first-half sets show where the action comes from"
`K3_4` (0, 32, 64) and `K2_4` (0, 64) pin the **start** and leave the tail free. They
are the mirror image of `K3_2` / `K2_2`: the character stands normally through the
pinned first half, then from about frame 70 a large cardboard box appears, is picked
up, and is carried off — **and the round trip brings that carrying motion back
intact.**

Same prompt, same seed, same model. Only *which half was pinned* changed, and the lift
is a different, complete action each time.

**The video prior has the action available, and the conditioning decides *when* it is
allowed to happen.** That is the same conclusion
[Experiment 2 reached](../exp2/placement.html#where-the-invented-content-lands) from
the video side — confirmed here in recovered 3D motion.
:::

Placements at K = 3: `3_1` 113/128 mm · `3_2` 139/143 · `3_3` 195/122 · `3_4` 168/151.
At K = 2: `2_1` 139/114 · `2_2` 134/131 · `2_3` **233/208** · `2_4` 121/147.

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=box_heavy cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=mpjpe_root_rel_mm
`jerk_ratio` above 1 means the returned motion is rougher than the input.
:::

---

## barbell_heavy

**"a person lifts a heavy barbell from the ground"** — **no.** MotionGPT3 never
produced a barbell lift to begin with, and the round trip cannot invent one.
[Clips →](result-barbell-heavy.html)

### What went in

MotionGPT3's clip is **an arm-raise, not a barbell lift**.
[Experiment 2 established](../exp2/result-barbell-heavy.html) that no conditioning set
rescues this prompt: no barbell is ever drawn in the video, unlike the box in
`box_heavy`.

Floor: 42 mm (s1234) and 41 mm (s5678). Clean, so whatever comes back is real.

### What we observed

::: key title="No"
The loose sets return **arm-waving variants at 74–204 mm from the input**. On seed 1234
the returned motion is far jerkier than what went in — jerk ratio **3.5** at `K = 5`
and **4.8** at `K = 3_3`.

Different, not better. There is no barbell in any source video, so there is no barbell
lift to recover.
:::

`K = 5` at 124/74 mm; `K = 3_2` at 122/137. Placements at K = 3: `3_1` 116/107 ·
`3_2` 122/137 · `3_3` **204/144** · `3_4` 134/126 — `K3_3` produces the single largest
deviation from the input in the whole experiment on seed 1234, and none of it is a
lift. At K = 2: `2_1` 133/104 · `2_2` 128/126 · `2_3` 188/141 · `2_4` 156/150.

::: note title="Why the negative result is load-bearing"
This prompt is what separates the two hypotheses about what the video model is doing.

If it **corrected** bad motion, it would fix this one — an arm-raise labelled "lifts a
heavy barbell" is as wrong as the flail labelled "lifts a heavy box", and `box_heavy`
does get fixed.

If it **extends** what it is handed, it fixes only the case where the input already
resembled the action closely enough to be developed into it.

The second is what happens, in both directions of the pipeline. That is the most
useful thing this prompt contributes, and it is [carried forward as a limit](verdict.html)
rather than treated as a failure of the setup.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=barbell_heavy cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-jerk_ratio
Sorted by jerk ratio, worst first. The two rows above 3.0 are the seed-1234 loose sets
described above — large deviation, high roughness, no barbell.
:::

---

## push_heavy

**"a person pushes a car"** — **no.** No car is ever pushed, and the returned motion is
just a differently idle person. This is the one prompt that comes back *smoother* than
it went in. [Clips →](result-push-heavy.html)

### What went in

The input is **close to static**: the character stands with one arm out and does almost
nothing. It was the lowest-energy input in
[Experiment 2](../exp2/result-push-heavy.html) as well.

Floor: 37 mm on both seeds — and `K = all` at 38/37 mm reproduces it exactly. There is
very little here for the round trip to lose, which is why this prompt has the tightest
control column of the six.

### What we observed

::: key title="No"
`K = 5` adds a **slight forward lean**. `K = 3_2` adds **looking down and reaching**.

No car is ever pushed, and nothing about the returned motion is more natural. It is a
differently idle person.

**Jerk actually falls** — 0.47 to 0.82 — so the motion comes back *smoother* than it
went in, and no more meaningful. That combination is the cleanest counterexample in
the experiment to using smoothness as a proxy for naturalness.
:::

`K = 5` at 76/61 mm — the **smallest** loose-set deviations in the experiment; `K = 3_2`
at 112/79. Placements at K = 3: `3_1` 85/78 · `3_2` 112/79 · `3_3` 98/88 · `3_4` 70/69 —
the flattest placement response of the six, because an input with nothing in it gives
the free run nothing to extend. At K = 2: `2_1` 104/114 · `2_2` 164/87 · `2_3` 142/108 ·
`2_4` 120/84.

::: note title="The two experiments agree from opposite directions"
[Experiment 2](../exp2/result-push-heavy.html) found that `2_3` produces two and a half
times the input's movement, none of which is pushing. Here the same prompt comes back
**smoother** than the input and no better.

More motion in the video, less jerk in the recovered motion, and no car in either. Both
measurements point the same way: this is the prompt where the video model has nothing
to work with, and neither measure of "more" corresponds to "better".
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=push_heavy cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=mpjpe_root_rel_mm
Note how many `jerk_ratio` values sit below 1.00 — this is the prompt where the round
trip smooths rather than roughens.
:::

---

## punch

**"a person throws right and left punches"** — **yes, partially.** The video model
extends a tentative guard into actual punches, and the round trip brings them back as
motion. [Clips →](result-punch.html)

### What went in

The input is **a boxing guard with small arm movement that never reaches extension**.
It reads as tentative shadow-boxing.

Floor: 36 mm (s1234) and 37 mm (s5678). Clean. Note `K = 9` on this prompt reaches
85/92 mm — the highest `K = 9` figure in the experiment, because the input is the most
energetic and nine anchors leave real gaps between fast movements.

### What we observed

::: key title="Yes, partially"
At `K = 5` and below, the video model **extends the guard into actual punches**, and the
round trip brings them back as motion.

The lifted rows track their sources pose for pose, **including the full arm extension
at frame 72 that the input simply does not contain.** That is the video model supplying
a missing part of the named action, recovered intact as 3D motion.
:::

This is also the cleanest source-to-return correspondence in the experiment — what is
in the video is what comes back, with no invented content and no second subject to
confuse pose recovery.

`K = 5` at 112/128 mm; `K = 3_2` at 121/146. Placements are unusually flat, as in
Experiment 2: at K = 3, `3_1` 121/146 · `3_2` 121/146 · `3_3` 162/155 · `3_4` 140/126;
at K = 2, `2_1` 129/128 · `2_2` 153/150 · `2_3` 143/141 · `2_4` 151/126.

### The jerk question

::: key title="This is the prompt where jerk is not a defect"
The returned motion is **much jerkier than the input — jerk ratio 1.7 to 4.3.**
Everywhere else in this experiment that would be a warning sign.

Here it is not, because **a real punch *is* jerky.** The impulse at the end of an
extension is a genuine physical feature, and the input's smooth tentative guard is the
less physical of the two.

This is the single case in either experiment where higher jerk reads as more physical
rather than as noise — and the reason [the numbers page](numbers.html) declines to use
smoothness as a naturalness proxy.
:::

::: warn title="One thing to watch at K = 3_3"
[Experiment 2 noted](../exp2/result-punch.html) that at `K = 3_3` the video model adds a
**high kick at frame 96** — at which point the clip is no longer the prompt. That kick
is in the source video, so it is in the returned motion too. Worth seeing before
treating `3_3` as a punch result.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=punch cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-jerk_ratio
Sorted by jerk ratio, highest first. The roughest returns here are the ones with real
punches in them.
:::

---

## squat

**"a person squats down"** — **unusable.** Pose recovery resolves this crouch
front-to-back the wrong way, and it does so in the control column, before the video
model is involved at all. [Clips →](result-squat.html)

### The failure

::: warn title="This prompt fails in the floor column"
`squat` comes in at **353–356 mm — in `floor`**, the condition with no video model in
the loop at all. Every other clip's floor is 34–42 mm.

The input squats facing **away** from the camera, curled into a compact ball. Every
lifted row comes back squatting **towards** the camera.
:::

### Why it happens

A deeply folded crouch seen from **one fixed viewpoint** is close to front-back
ambiguous in silhouette. Curled into a ball, the shape you project is nearly the same
whichever way you are facing. GVHMR consistently resolves that ambiguity the other way.

::: method title="It is not an alignment artefact"
Lifted clips are routinely rotated about the vertical axis onto their input's heading,
because GVHMR's absolute heading is arbitrary. So the obvious explanation is a bad
rotation.

It is not. A brute-force search over all rotations about the vertical axis finds **no
angle** that brings the two into agreement — the best is 277 mm at −90°, still seven
times any other clip's floor. **The recovered pose is genuinely a different pose**, not
the same pose viewed from elsewhere.

A yaw rotation cannot repair a front-to-back flip, which is why this clip stays broken.
:::

### The consequence

::: key title="Every squat row must be discounted"
Because the floor already fails, **no column in this row says anything about the video
model.** The loose-set figures for `squat` (333–361 mm) are not "large deviations caused
by the video model" — they are the same front-back flip that `floor` has, plus noise.

The yaw figure recorded for this clip in the manifest is meaningless, and `squat` is
excluded from every mean quoted in [The numbers](numbers.html). Including it would just
move every column together and hide the real spread.
:::

The clips on the result page are there for completeness and for anyone who wants to
confirm the diagnosis. Compare each with `floor` rather than with the input — against
`floor` they are barely different, which is the tell that the video model is not what
is causing the discrepancy.

::: note title="What was lost here is worth noting"
This is a genuinely annoying failure, because `squat` was Experiment 2's **best**
result. **The source videos are fine** — the video model turns the four-second hold into
[repeated reps](../exp2/result-squat.html), exactly the kind of re-timing this project
is looking for, and the round trip cannot confirm it in 3D because the recovery step
fails independently.
:::

### Why this matters beyond one clip

::: warn title="A squat is not an exotic pose"
It is the second-most common thing in a motion dataset. If a folded crouch from a
single fixed viewpoint cannot be recovered reliably, then **one clip in six failing is
a property of the capture setup, not bad luck.**

A second camera angle, or simply an off-axis camera, would very probably fix it. That
is worth doing before running this pipeline at any scale, and it is
[carried as the second caveat](verdict.html) on the verdict.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=squat cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=mpjpe_root_rel_mm
Every row sits in the 316–361 mm band, `floor` included. The **flatness** of this column
is the diagnosis: if the video model were responsible, `floor` would be low and the
loose sets high.
:::

---

## baseball

**"a person hit a ball with baseball bat"** — **marginal.** A leg lift and a torso
rotation come back that read a little like a batting stride, but no bat, no ball, and
foot-skate roughly doubles. [Clips →](result-baseball.html)

### What went in

Floor: 37 mm (s1234) and 34 mm (s5678) — the cleanest control column of the six. So
whatever comes back is genuinely attributable to the video model.

### What we observed

::: key title="Marginal"
`K = 5` and `K = 3_2` add **a leg lift and a torso rotation** that read a little like a
batting stride. The shape of the motion is right for the prompt.

But **no bat and no ball are ever present**, and **foot-skate roughly doubles** — from
180 to 293 mm/s at `K = 5` on seed 1234.

Slightly more dynamic. Not obviously more natural.
:::

The stride is really in the source videos — this is not a recovery artefact. It is just
a stride in empty space.

`K = 5` at 118/109 mm; `K = 3_2` at 128/150. Placements at K = 3: `3_1` 122/176 ·
`3_2` 128/150 · `3_3` 155/110 · `3_4` 152/110 — the noisiest seed-to-seed disagreement in
the experiment. At K = 2: `2_1` 180/132 · `2_2` 161/190 · `2_3` 171/178 · `2_4` 122/103.

::: note title="Why the foot-skate matters here specifically"
Foot-skate is a planted foot sliding along the ground — a foot that is supposed to be
carrying weight but is not staying put. For a batting stride, where the whole point is
loading onto the back foot, doubling the skate is the opposite of what "more natural"
should look like.

That is what separates this from [`punch`](#punch), where the extra roughness
corresponds to a real physical impulse. Here the extra motion comes with degraded
ground contact, so the added dynamism does not buy plausibility.
:::

::: note title="Both experiments call this one marginal"
[Experiment 2](../exp2/result-baseball.html) found the stride and rotation appear at
`K = 5` and `K = 3_2` and nowhere else, with no bat ever drawn. The round trip agrees
from the other side: the motion that comes back is a stride, and it is a slightly
worse-grounded one.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=baseball cols=seed:seed,condition:condition,mpjpe_root_rel_mm:joint err mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-foot_skate_out_mm_s
Sorted by foot-skate, worst first. Compare the top rows against `floor` and `K = all`
near the bottom.
:::

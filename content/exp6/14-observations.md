---
title: Observations
nav: Observations
lead: Everything the ten clip pages leave out — what was actually seen in each, the per-clip numbers, and the caveats. The clip pages carry the clips; this page carries the reading of them.
---

Numbers are mean **root-relative joint error against the input motion, in mm**, on the
same neutral body after the same yaw alignment and grounding — so they describe
exactly what is on screen. `results/analysis.json` has the rest.

::: warn title="The caution that applies to every row below"
Pose recovery has a motion prior and will return smooth, plausible SMPL from a video
that was a mess. **No recovered motion means anything until the photoreal video above
it has been watched.** Every conclusion here was read off the photoreal row first.
:::

## The whole sweep in one table

| clip | dense | K8 | K5 | K3 | K2 | stops copying | stops doing the action |
|---|---|---|---|---|---|---|---|
| [walk](result-walk.html) | 48 | 84 | 184 | 177 | 170 | **K5** | never |
| [run](result-run.html) | 78 | 126 | 230 | 220 | 219 | **K5** | never |
| [jump](result-jump.html) | 73 | 149 | 148 | 147 | 162 | **K8** | never |
| [kick](result-kick.html) | 74 | 156 | 172 | 241 | 154 | **K8** | **K3** |
| [sit down](result-sit-down.html) | 67 | 69 | 85 | 99 | 79 | never sharply | never |
| [stand up](result-stand-up.html) | 140 | 136 | 301 | 279 | 270 | **K5** | never |
| [throw](result-throw.html) | 113 | 166 | 193 | 244 | 252 | **K8** | mis-read at every density |
| [turn](result-turn.html) | 56 | 92 | 108 | 98 | 117 | never sharply | never |
| [squat](result-squat.html) | 51 | 76 | 102 | 137 | 168 | gradually, from K8 | never |
| [wave](result-wave.html) | 61 | 56 | 75 | 92 | 78 | never | never |

---

## walk

**"a man walking along a city sidewalk"** — the action survives to two frames; the
*trajectory* does not. [Clips →](result-walk.html)

`dense` (48 mm) and `K = 8` (84 mm) follow the input's **actual path**: approach the
camera, pass, turn away. From `K = 5` the model substitutes a plain steady walk
straight across frame and never turns.

So the action is intact all the way down to two frames, and the specific performance
is gone from `K = 5`. That split — *what* survives, *where and when* does not — is
[the result of the whole experiment](where-it-breaks.html), and `walk` is the
clearest single case of it.

::: warn title="A second pedestrian appears at K = 5 and K = 3"
The model adds another person walking in frame. Pose recovery does not track them, so
the recovered column ignores it — but it is the failure mode
[Experiment 1 was poisoned by](../exp1/observations.html#box-heavy), and worth
knowing is present.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=walk cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
:::

---

## run

**"a man running on an outdoor running track"** — same threshold as `walk`, sharper.
[Clips →](result-run.html)

`dense` (78 mm) and `K = 8` (126 mm) hold the input's stride. `K = 5` and below are a
**generic run**.

::: warn title="This is where the model invents fast motion badly"
Foot skate goes from **180 mm/s in the input to 900–1800 mm/s out** — 1812 mm/s at
`K = 5`, ten times the input.

**The model knows what running looks like and does not know where this runner's feet
were.** Between distant anchors it has to invent a fast, high-frequency gait, and it
invents one that does not stay on the ground.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=run cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
:::

---

## jump

**"a man jumping upward"** — the only clip whose error jumps immediately and then
never gets worse. [Clips →](result-jump.html)

`K = 8` is already at **twice `dense`** — 149 against 73 mm — and `K = 5`, `K = 3`
and `K = 2` sit at 148, 147 and 162. The curve is a step, not a slope.

The **crouch-and-launch survives at every density including two frames**. A jump is a
large, unambiguous, ballistic motion: pin its start and its end and the model knows
what has to happen in between.

::: note title="And at K = 8 and below it adds a basketball"
Which the depth control never contained. Like Experiment 4's bat and glove, it does
not come back through pose recovery — but it is the model reasoning about the
*action*, not only the pixels: a man jumping upward in a gym is, plausibly, going for
a rebound.
:::

This clip is also the one the [attention-mask pilot](pilots.html#4-the-sparse-conditions-the-attention-mask)
was diagnosed on.

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=jump cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
:::

---

## kick

**"a man performing a kick"** — **the only clip where the action itself does not
survive.** [Clips →](result-kick.html)

Copies at `dense` (74 mm), loses the input at `K = 8` (156 mm), and at `K = 3` and
`K = 2` **the kick itself goes**: what is left is footwork with one late leg raise.

::: warn title="Why kick and not jump"
Both are fast. The difference is that a jump is one large ballistic event that two
endpoints effectively specify, while a kick is a *short, high-frequency* event that
can happen anywhere in six seconds. Given frames 0 and 168 of a man in a training
hall, "footwork" is a perfectly plausible six seconds — and the one moment that made
it a kick is not pinned by either end.
:::

`kick` is also the clip that
[decided the control format](pilots.html#2-the-control-format-the-expected-winner-lost):
its indoor prompt is what the `scene` format could not satisfy.

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=kick cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
Note the skate at `K = 2`: 39 mm/s against the input's 101. The motion is wrong for
the prompt and yet stands on the floor better than the capture did.
:::

---

## sit_down

**"a man lowering himself into a seated position"** — the flattest curve in the set,
and **the clearest case of the video model supplying physics the control does not
have.** [Clips →](result-sit-down.html)

67 → 69 → 85 → 99 → 79 mm. It never sharply stops copying.

::: key title="The depth render is a body alone with no chair — and LTX puts one there"
At **every density** the model puts a stool or a box under him and sits him on it.

The control contains no chair. The prompt names no chair. But a man lowering himself
into a seated position in a plain interior has to be sitting *on* something, and the
model supplies it — then keeps him in contact with it for the rest of the clip.

That is the video prior contributing an inference about the physical world, not just
about pixels. It is the single best example of the project's premise in any of the
six experiments, and it happens on the *easiest* clip rather than the hardest.
:::

Foot contact also improves: input skate 40.8 mm/s, down to **13.7 at `K = 8`**.

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=sit_down cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
:::

---

## stand_up

**"a man rising to his feet from a seated position"** — read this one from the
photoreal video, not the recovered SMPL. [Clips →](result-stand-up.html)

::: warn title="The input starts prone on the floor, which is hard for pose recovery"
Even `dense` is **140 mm** — the highest `dense` error of the ten. That is not the
video model; it is the recovery struggling with a body lying on the ground at frame
0.

So the numbers in this row describe the recovery's difficulty as much as the
generation's. Visually, **the rise off the floor survives to `K = 2`.**
:::

Copying breaks at `K = 5`, where the error goes 136 → 301 mm.

This is the same lesson as [Experiment 4's `squat`](../exp4/observations.html#squat)
and [Experiment 1's](../exp1/result-squat.html): a single fixed viewpoint on a
compact, floor-level pose is where recovery fails, and no amount of photorealism
fixes it.

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=stand_up cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
:::

---

## throw

**"a man throwing with an overhand motion"** — **the only clip where the *prompt*
loses.** [Clips →](result-throw.html)

::: warn title="At every density, dense included, the model hands him a racket"
The overhand throw reads to the model as a **racket sport**: it gives the man a
tennis or badminton racket and turns the wind-up into a serve.

The prompt says "throwing with an overhand motion" and **names no ball**. The caution
about not naming objects the control does not contain cuts both ways — with nothing
named, the model picks its own, and an overhand arm arc plus athletic wear on an
outdoor field is a serve as readily as it is a throw.
:::

Copying breaks at `K = 8`. And this is the worst-behaved clip in the set at `K = 3`:
**nine times the input's jerk** (ratio 9.07) and 548 mm/s of foot skate against the
input's 112. Like [`run`](#run), it is inventing fast motion between distant anchors,
and it invents badly.

::: note title="The fix is a one-word prompt change, and it was not made"
Naming the ball would very likely resolve it. It was left alone deliberately: the
run's variable is conditioning density, and changing a prompt mid-sweep would have
made this row incomparable with the other nine. It is the first thing to change if
this clip is rerun.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=throw cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
:::

---

## turn

**"a man turning around to face the other direction"** — degrades gently and never
breaks. [Clips →](result-turn.html)

56 → 92 → 108 → 98 → 117 mm. **Turning around is a large, unambiguous motion, and two
frames at the ends are enough to specify it** — the start faces one way, the end faces
the other, and there is only one reasonable way to get between them.

The input's own foot skate is 363 mm/s, the highest of the ten, so this is one row
where the recovered motion standing *less* solidly than the input would be hard to
achieve.

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=turn cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
:::

---

## squat

**"a man performing a deep squat"** — the cleanest monotone degradation of the ten,
which makes it **the best single row for reading the sweep.**
[Clips →](result-squat.html)

51 → 76 → 102 → 137 → 168 mm, and the action never goes.

::: key title="At K = 2 the model does something interesting rather than wrong"
The input **holds one deep squat for six seconds.** Given only the two ends, the model
performs *repetitions* — down, up, down again — which is what a person in a gym would
actually do.

That is not a failure to follow the control; it is a more plausible six seconds than
the control described. And it is the same behaviour
[Experiment 2 found on its own `squat`](../exp2/result-squat.html), arrived at through
a completely different mechanism — there by withholding keyframes from a blue-character
video, here by withholding depth frames from a photoreal one.
:::

Foot contact is also the best in the set: input 39.8 mm/s, down to **10.4 at
`K = 5`** — and every density is at or under 28.

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=squat cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
The jerk ratio sits at 0.94–1.13 across the whole sweep — this row is as clean as the
set gets.
:::

---

## wave

**"a man waving one arm"** — essentially flat. [Clips →](result-wave.html)

61 → 56 → 75 → 92 → 78 mm. **`K = 8` is marginally *closer* to the input than
`dense`.**

A small, near-static motion is fully specified by its endpoints. There is nothing for
sparsity to cost, because there was never much information in the frames it removed.

Foot contact is the cleanest in the experiment: input 22.6 mm/s, **1.3 at `K = 2`** —
the recovered motion stands almost perfectly still on the floor, where the motion
capture drifted.

::: note title="Why a flat row is worth having"
It is the control for the whole sweep. If sparsity degraded everything uniformly,
`wave` would degrade too. It does not, which means what the other rows lose is
specific to the information their motion carried in the removed frames — not an
artefact of conditioning fewer frames.
:::

### The numbers

::: metrics src=results/analysis.json key=results where=prompt_id=wave cols=condition:condition,num_conditioned:frames pinned,mpjpe_on_conditioned_mm:err on pinned mm,mpjpe_on_free_mm:err on free mm,jerk_ratio:jerk vs. input,foot_skate_out_mm_s:skate mm/s sort=-num_conditioned
:::

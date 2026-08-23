---
title: Observations
nav: Observations
lead: Everything the six result pages leave out — what was actually seen in each prompt, the per-prompt numbers, and the caveats. The result pages carry the clips; this page carries the reading of them.
---

The measure quoted throughout is **silhouette-change energy**: for each consecutive
frame pair, the fraction of the body silhouette that changes, averaged over the clip,
divided by the same number for the blue input. **1.00 means the output moves exactly
as much as the motion model's clip.** The full table is in
[Placement, not K](placement.html); `results/checks/energy.json` has every cell.

---

## box_heavy

**"a person lifts a heavy box from the floor"** — the one prompt where the video
prior clearly takes over, and the most striking result in the sweep.
[Clips →](result-box-heavy.html)

### What went in

MotionGPT3's clip is a **vague crouch-and-flail**. There is no box in it, and the
motion does not read as lifting anything. Input energy 0.058 (s1234) and 0.060
(s5678) — middling for this set of six.

This matters for how the result is read: the video model is not being asked to polish
a good lift. It is being handed something that does not perform the prompt at all.

### What we observed

::: key title="It starts doing the action as K falls"
At **`K = 2_1` (0, 120), seed 1234** the model invents a cardboard box, bends down,
picks it up and lifts it to chest height with plausible timing. That is a **better
rendition of the prompt than the motion it was conditioned on** — the input never
lifts anything.

The character stops looking stiff at `K = 5` (1.16) and decisively at `K = 3_1`
(1.56). It does not "stop doing the action" as K falls, which is what we expected to
see; it *starts* doing it.
:::

Strong control is a pure copy: `K = all` 0.95 and `K = 9` 0.94 — very slightly *less*
motion than the input, crouch-and-flail faithfully reproduced, box-less.

At K = 3 the placements run `3_1` 1.56 · `3_2` 1.74 · `3_3` 2.09 · `3_4` 1.54. At
K = 2 they run `2_1` 0.81 · `2_2` 1.56 · `2_3` 2.14 · `2_4` 0.74 — note that `2_1` and
`2_4` sit *below* the input while `2_3` nearly doubles it, on the same number of
pinned frames.

### Where the box appears is decided by where the free run is

::: key title="Both seeds, every time"
| set | pinned | free run | the box appears in |
|---|---|---|---|
| `3_2` / `2_2` | second half | frames 0–63 | **0–60** and **0–54 / 0–56** |
| `3_4` / `2_4` | first half | frames 65–120 | **69–120** and **70–120** |
| `2_3` | 32, 88 | both ends | **0–120** (i.e. at the two ends) |
| `2_1` | 0, 120 | the middle | **2–98** and **32–103** |

With the tail free, the character stands normally through the pinned first half and
then, from about frame 70, a large cardboard box appears and is picked up and carried
off. With the head free, the same box appears at the *start* instead, and the
character is kneeling beside it before the pinned frames take over at 64.

The video model has a whole action available. The conditioning decides **when** it is
allowed to happen, not whether.
:::

### The one prompt that draws things that were never there

This is also the only prompt where the model adds content the blue render never
contained. Warm-toned — that is, non-scene — pixels appear in **8 of 108** clips,
*all of them `box_heavy`*, all at K ≤ 3 sets with a long unpinned run: boxes, a hand
truck, and in `s5678` at `K = 3_2` / `2_2` a **photographic person in pink clothing**
occupying the free first half, which cuts back to the blue matte character at the
first pinned frame.

::: warn title="Two things to carry into Experiment 1"
**The identity switch is abrupt, not gradual.** We expected the blue character to
drift toward looking like a real person as K dropped. What actually happens is a hard
switch confined to the unpinned run, snapping back at the conditioning boundary.

**`s5678` at `K = 3_1` has the character floating above the floor** around frames
72–96, with its shadow still on the ground. That is physically wrong, and it is a
direct warning for the [round trip](../exp1/overview.html): a motion lifted from that
video would be meaningless.
:::

### The numbers

::: metrics src=results/checks/energy.json key=results where=prompt_id=box_heavy cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
:::

---

## barbell_heavy

**"a person lifts a heavy barbell from the ground"** — the clearest negative in the
sweep. No barbell is ever drawn, at any K.
[Clips →](result-barbell-heavy.html)

### What went in

MotionGPT3's clip is **an arm-raise, not a barbell lift**. Input energy 0.072 (s1234)
and 0.078 (s5678).

The contrast with `box_heavy` is the point. Both prompts name a concrete object the
input does not contain. In one case the model draws the object and performs the
action; here it never does.

### What we observed

::: key title="It never does the action"
**Stops looking stiff:** at `K = 5` (1.99) and `K = 3_2` (1.96) only. Everywhere else
this prompt moves *less* than its input.

**Stops doing the action:** it never does it. No barbell is ever drawn, at any K —
unlike the box. The video model extends the arm-raise it was given into larger
arm-waving; it does not replace it with a lift.

**Goes the other way at three sets:** `K = 3_1` (0.47), `K = 2_1` (0.58) and `K = 2_2`
(0.45). The character nearly *freezes*. Given two distant pinned poses it takes the
cheapest path between them rather than performing anything.
:::

The placement spread here is the widest of any prompt. At K = 3: `3_1` 0.47 · `3_2`
1.96 · `3_3` 2.90 · `3_4` 0.81 — pinning both ends nearly halts the clip, freeing both
ends nearly triples it. At K = 2: `2_1` 0.58 · `2_2` 0.45 · `2_3` **2.87** · `2_4` 0.81.
`2_1` and `2_3` hand over the same *number* of frames; `2_3` produces five times the
motion because neither end is pinned.

::: warn title="This prompt holds the sweep's lowest crossfade ratio"
`K = 2_2` frames 64 → 120 scores 0.38 on the
[morphing check](does-it-work.html#test-3-no-morphing-anywhere) — the lowest anywhere.
On inspection it is the near-freeze described above, not a dissolve. The check is
measuring "close to a linear blend", and a character that barely moves is trivially
close to one.
:::

### Why this prompt matters more than it looks

::: key title="The prior extends, it does not correct"
`box_heavy` and `barbell_heavy` differ in exactly the way that separates the two
hypotheses:

- If the video model **corrected** bad motion, it would fix both — an arm-raise
  labelled "lifts a heavy barbell" is as wrong as a flail labelled "lifts a heavy
  box".
- If the video model **extends** what it is handed, it fixes only the one where the
  input already resembles the action closely enough to be developed into it.

The second is what happens. This is the single clearest piece of evidence for that
reading in the experiment, and it is [carried forward as a limit](verdict.html) rather
than treated as a failure.
:::

### The numbers

::: metrics src=results/checks/energy.json key=results where=prompt_id=barbell_heavy cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
Note how many rows sit **below 1.00** — this prompt under-moves at most sets.
:::

---

## push_heavy

**"a person pushes a car"** — the input barely moves at all, and no car is ever drawn
at any K. What the video model adds here is motion without meaning.
[Clips →](result-push-heavy.html)

### What went in

The blue input is **close to static**: the character just stands with one arm out.
Input energy 0.036 (s1234) and 0.034 (s5678) — the lowest of the six prompts by a
clear margin.

The physical beat this prompt was chosen for is *the lean into the load before
anything moves*. Nothing in the input leans.

### What we observed

::: key title="Motion is added; meaning is not"
**Stops looking stiff:** `K = 5` (1.24), strongly at `3_2` / `3_3` / `2_2` (1.6–2.2).

**Stops doing the action:** it never starts. **No car is ever drawn and nothing is
ever pushed, at any K.**

**What gets added instead is arbitrary.** At `2_2` and `2_3` the extra motion is leg
raises and a crouch — movement that has nothing to do with pushing. Given a
near-empty input and a long free run, the model fills the time with generic plausible
human movement rather than with the named action.
:::

Strong control is the lowest in the sweep — `K = all` 0.70 and `K = 9` 0.63 — because
there is so little to copy. Placements: at K = 3, `3_1` 0.83 · `3_2` 1.61 · `3_3` 2.16 ·
`3_4` 1.04; at K = 2, `2_1` 0.84 · `2_2` 1.70 · `2_3` **2.52** · `2_4` 1.38.

::: note title="A useful control, precisely because it fails"
`push_heavy` is the cleanest demonstration that added motion is not the same as added
*meaning*. `2_3` produces two and a half times the input's movement and none of it is
pushing. Any measure that scored this experiment on motion quantity alone would call
this a success.

It also sets up the [round trip](../exp1/result-push-heavy.html), where this prompt
comes back **smoother** than it went in and no better — the mirror image of the same
finding.
:::

### The numbers

::: metrics src=results/checks/energy.json key=results where=prompt_id=push_heavy cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
Read the absolute `energy` column as well as the ratio here — the input is so nearly
static that a large ratio still means a small amount of movement.
:::

---

## punch

**"a person throws right and left punches"** — the highest-energy input of the six and
the most stable across the sweep. The one prompt where the video model completes an
action the input only gestures at. [Clips →](result-punch.html)

### What went in

MotionGPT3 produces **a boxing guard with small arm movement that never reaches
extension**. It reads as someone shadow-boxing tentatively rather than punching. Input
energy 0.148 (s1234) and 0.146 (s5678) — the highest of the six by a wide margin.

Because the input is already energetic, this prompt is the most stable across the
sweep: ratios stay between 0.67 and 1.43 everywhere, with none of the freezes or
doublings the other prompts show.

### What we observed

::: key title="The model completes the action"
**Stops looking stiff:** already at `K = 9` (1.20) — **the only prompt in the sweep
where K = 9 adds anything at all.**

**From `K = 5` downward the model extends the guard into full punches, with the arm
actually reaching extension.** The input never does this. It is not adding generic
movement; it is completing the specific action named in the prompt.

**Stops doing the action:** the boxing stance survives all the way to the loosest
sets. The one departure is at `K = 3_3`, where the model adds a **high kick at frame
96** — at which point it is no longer the prompt.
:::

Placements are the narrowest of any prompt — an energetic input leaves less room for
placement to matter. At K = 3: `3_1` 0.94 · `3_2` 1.03 · `3_3` 1.43 · `3_4` 1.40. At
K = 2: `2_1` 0.67 · `2_2` 0.82 · `2_3` 0.99 · `2_4` 1.05. Note that `2_3` — which nearly
doubles or triples every other prompt — does almost nothing here.

::: note title="Why punch reads differently from the rest"
For every other prompt, "more motion" is ambiguous evidence. Here it is not, because
the *kind* of motion added is exactly the missing part of the named action: the
extension at the end of a punch.

That is also why this prompt carries the most weight in the
[round trip](../exp1/result-punch.html), where the returned motion is much jerkier
than the input — and a real punch *is* jerky. It is the one case in either experiment
where higher jerk reads as more physical rather than as noise.
:::

### The numbers

::: metrics src=results/checks/energy.json key=results where=prompt_id=punch cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
The tightest range in the sweep.
:::

---

## squat

**"a person squats down"** — the clearest re-timing in the sweep. A four-second static
hold becomes repeated reps. [Clips →](result-squat.html)

### What went in

MotionGPT3 **drops into a squat and holds the bottom position for four seconds**.
Input energy 0.053 on both seeds — most of the clip is a static hold, so there is very
little frame-to-frame change.

A four-second hold at the bottom of a squat is not how people squat. It is a plausible
reading of the sentence and an implausible piece of human motion, which makes it the
ideal input for this question.

### What we observed

::: key title="The model refuses the hold"
**From `K = 5` downward the video model turns the clip into repeated squat reps** —
standing up and going back down two or three times within the same 121 frames.
`K = 5` scores **2.78**, the highest single cell in the entire sweep.

This is the cleanest re-timing result in the experiment. The model was handed five
poses and the freedom to decide what happens between them, and it chose to fill the
time with *more repetitions of the action* rather than with a static hold. That is a
decision about how the action is distributed in time, which is precisely the kind of
knowledge the experiment was built to look for.

**Stops looking stiff:** `K = 5`. **Stops doing the action:** it never stops. Reps are
still squatting — arguably a more natural reading of "a person squats down" than a
four-second hold at the bottom.
:::

**Every** placement more than doubles the input here, including the ones that pin both
ends — unique to this prompt, and a direct consequence of the input containing so much
dead time. At K = 3: `3_1` 1.90 · `3_2` 2.63 · `3_3` 2.15 · `3_4` 2.40. At K = 2: `2_1`
1.72 · `2_2` 1.58 · `2_3` 2.01 · `2_4` 2.29.

Strong control copies the hold faithfully: `K = all` 0.89, `K = 9` 0.87. This prompt is
also one of the pairs used for
[Test 2](does-it-work.html#test-2-k-all-reproduces-the-input), and the one re-run with
a deliberately off-grid pinned index for
[the off-grid control](does-it-work.html#extra-the-off-grid-negative-control).

::: warn title="One thing squat does not survive"
In [Experiment 1](../exp1/result-squat.html) this prompt is the one clip that **cannot
be round-tripped at all** — pose recovery resolves the deeply folded crouch
front-to-back the wrong way, and the failure appears in the control column before the
video model is even involved. Nothing about that failure is visible here; the videos
on the result page are fine.
:::

### The numbers

::: metrics src=results/checks/energy.json key=results where=prompt_id=squat cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
The highest ratios in the sweep, because this input has the most dead time to fill.
:::

---

## baseball

**"a person hit a ball with baseball bat"** — a stride and a rotation get added that
read a little like batting, but no bat and no ball ever appear. The marginal case of
the six. [Clips →](result-baseball.html)

### What went in

Input energy 0.089 (s1234) and 0.120 (s5678) — second-highest of the six, and the one
prompt where the two seeds differ substantially from each other.

The beat this prompt was chosen for is *load onto the back foot, pause, then the fast
rotation through contact*. It is a timing signature that is very specific and hard to
fake.

### What we observed

::: key title="Right shape of motion, missing object, does not hold"
**Stops looking stiff:** `K = 5` (1.38).

**At `K = 5` and `K = 3_2` (1.44) the model adds a leg lift and a rotation that read as
a batting stride.** That is genuinely the right *shape* of motion for the prompt —
weight onto the back foot, then rotation.

**But no bat and no ball are ever drawn, at any K.** Unlike `box_heavy`, the model
never places the named object in the scene, so what is added is the body mechanics of
batting without the thing being batted.

**And it does not hold at looser sets.** At `2_1` (0.66) and `2_2` (0.90) it settles
back to near-input energy, and at `2_3` it wanders into unrelated arm movement.
:::

Placements at K = 3: `3_1` 0.93 · `3_2` 1.44 · `3_3` 1.64 · `3_4` 1.16. At K = 2: `2_1`
0.66 · `2_2` 0.90 · `2_3` 1.55 · `2_4` 0.83 — three of four sit at or below the input.

::: note title="Why this one is called marginal rather than positive"
The added motion is in the right direction, which `push_heavy` and `barbell_heavy`
cannot claim. But it is a stride and a rotation in empty space, present at two
conditioning sets and absent at the rest.

In the [round trip](../exp1/result-baseball.html) the same verdict holds from the other
side: the returned motion is slightly more dynamic, and foot-skate roughly doubles,
which is the opposite of what "more natural" should look like.
:::

### The numbers

::: metrics src=results/checks/energy.json key=results where=prompt_id=baseball cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
Worth comparing the two seeds directly here — this is the prompt where they diverge
most.
:::

---
title: Video Models Know Dynamics
lead: An experiment log. Each experiment asks one question about whether video generation models carry an implicit model of physical dynamics, and shows the clips it produced so the claim can be checked rather than taken on trust.
---

## The question behind the log

A text-to-motion model learns from motion-capture sequences paired with captions. A
video generation model learns from footage of the physical world. Both can be asked
for "a person lifts a heavy box" — but only one of them has ever had to predict what
light does to a body under load, how a torso braces, or how long a heavy thing takes
to leave the ground.

The experiments here probe whether that difference in training signal shows up in the
output: whether a video model's samples carry **dynamics** — weight, inertia, effort,
contact — that a motion model's samples do not.

## Experiments

<div class="cards">
<a class="card" href="exp0/overview.html">
  <div class="card-c">Exp 0</div>
  <div class="card-t">Generating motion with video models vs. a text-to-motion model</div>
  <div class="card-q">Given the same prompt, does a video model show the weight of an action where a text-to-motion model shows a generic version of it?</div>
  <div class="card-m">
    <span class="status s-complete">complete</span>
    <span class="meta-chip">2026-08-21</span>
    <span class="meta-chip tag">81 clips</span>
  </div>
</a>
<a class="card" href="exp2/overview.html">
  <div class="card-c">Exp 2</div>
  <div class="card-t">Strong vs. loose control — how much motion does the video model add?</div>
  <div class="card-q">If we render a motion model's output as video and hand the video model only some of those frames, at what point does it stop copying and start inventing the motion itself?</div>
  <div class="card-m">
    <span class="status s-complete">complete</span>
    <span class="meta-chip">2026-08-23</span>
    <span class="meta-chip tag">132 clips</span>
  </div>
</a>
<a class="card" href="exp1/overview.html">
  <div class="card-c">Exp 1</div>
  <div class="card-t">The round trip — does motion come back more natural than it went in?</div>
  <div class="card-q">Send a motion through the video model and pull it back out as motion. If the video model knows how bodies move, what comes back should look more natural than what went in — not identical to it.</div>
  <div class="card-m">
    <span class="status s-complete">complete</span>
    <span class="meta-chip">2026-08-23</span>
    <span class="meta-chip tag">144 clips</span>
  </div>
</a>
<a class="card" href="exp4/overview.html">
  <div class="card-c">Exp 4</div>
  <div class="card-t">Photoreal output, animation as control</div>
  <div class="card-q">Earlier experiments made the video model hold an appearance it had never seen. If the animation is control only and the appearance comes from text, does the model spend its capacity on motion instead?</div>
  <div class="card-m">
    <span class="status s-complete">complete</span>
    <span class="meta-chip">2026-09-03</span>
    <span class="meta-chip tag">60 clips</span>
  </div>
</a>
<a class="card" href="exp6/overview.html">
  <div class="card-c">Exp 6</div>
  <div class="card-t">Photoreal output, correct animation as control</div>
  <div class="card-q">Given a clean motion-capture clip as depth control and a sentence for appearance, how few conditioned frames still produce the right action, six seconds long, in a real place?</div>
  <div class="card-m">
    <span class="status s-complete">complete</span>
    <span class="meta-chip">2026-09-07</span>
    <span class="meta-chip tag">50 clips</span>
  </div>
</a>
</div>

::: note title="Why the numbering is out of order"
They were numbered by when they were designed, not by when they run. Experiment 2
builds and validates the keyframe-conditioning machinery and chooses the two control
settings; Experiment 1 then reuses that code, those settings and those files to close
the loop. Reading 2 before 1 is much easier than the reverse.

Experiment 4 identified what was wrong with 1–3 — the blue character was doing two
jobs at once — and fixed it. Experiment 6 then fixed the *other* problem those
experiments shared: the control motion itself was often wrong, so it swaps
MotionGPT3's output for clean motion capture. Experiments 3 and 5 are not written up
here; 5 is the data-preparation step Experiment 6 consumes.
:::

## What the experiments add up to

::: key title="The state of the argument"
1. **Keyframe conditioning works mechanically** — pinned frames land where asked,
   full conditioning reproduces the input, and no morphing occurs.
   [(Exp 2's checks)](exp2/does-it-work.html)
2. **There is a real window where the video model re-times motion** rather than
   copying it, and it exists for every prompt.
   [(Exp 2's verdict)](exp2/verdict.html)
3. **The round trip is essentially lossless**, so motion added in the video survives
   back into 3D. [(Exp 1's floor)](exp1/floor.html)
4. **The video prior extends; it does not correct.** It can supply a missing part of
   an action — the extension of a punch, a box picked up and carried — and it cannot
   fix an action that is simply wrong for the prompt.
   [(Exp 1's verdict)](exp1/verdict.html)
5. **The control is a placement puzzle, not a dial.** What the video model
   contributes is governed by *where* the free run sits, not by how many frames were
   withheld. [(Exp 2)](exp2/placement.html)
6. **Separating "what to do" from "what to look like" removes the whole appearance
   confound.** Feed the animation in as depth control and take appearance from text,
   and every output is a photoreal single person with the pose pinned to within about
   80 mm wherever it is specified. [(Exp 4)](exp4/does-it-work.html)
7. **With a correct animation as control, two frames and a sentence produce the right
   action** — six seconds of it, in a real place, for eight clips of ten. What
   sparsity costs is the *particular performance*, not the action.
   [(Exp 6)](exp6/where-it-breaks.html)
8. **And the model supplies physics the control does not have** — a chair invented
   under a man who has to sit on something, squat repetitions replacing an
   implausible six-second hold, and foot contact cleaner than the motion capture's on
   every slow clip. [(Exp 6's verdict)](exp6/verdict.html)
:::

::: warn title="What is still missing"
Control. The model will give you the action; it will not give you *your* action.
Every experiment so far has hit a ceiling that was a property of the control scheme
rather than of the model — keyframe placement in Exp 2, blank-frame semantics in
Exp 4, and in Exp 6 the fact that the frames carrying a specific performance are
exactly the ones sparsity throws away.

Two concrete items are outstanding across the series: a control signal that is
**dense but weak** rather than sparse and absolute, and **a second camera** — three
experiments have now lost a clip to a single fixed viewpoint on a floor-level pose.
:::

## How to read these pages

::: note title="Conventions used throughout"
Every experiment is split into short pages: what the question was, how it was set
up, what to watch for, then **one page per prompt** carrying nothing but that prompt's
clips, then an **Observations** page holding the discussion and the numbers, then a
verdict and provenance.

The split is deliberate. A result page is meant to go on a projector — headings that
name the conditioning set and the frame indices, and the clips underneath. Everything
that needs reading rather than watching lives on the Observations page.

**Picking a page hides the sidebar**, so the clips get the whole window. The button at
the top left, or `n`, brings it back.

Clips autoplay muted. **They loop in lockstep rather than independently** — one
timer restarts every visible clip together, so a comparison stays frame-aligned
instead of drifting apart after a few seconds. Where the arms differ in length, the
shorter one holds on its last frame until the group comes round again.

The toolbar at the top of a results page switches seed, runs the whole page at ¼×,
½×, 1× or 2×, restarts everything from *t = 0*, and turns the lockstep off if you
want it. Click any clip to open it full-size and step through it a frame at a time.
Click a timing strip to open it full-size and scroll it.
:::

Comparisons are always laid out so that the thing being compared sits **inside one
block**. Where a prompt has a matched heavy/light counterpart, the two are adjacent
rows of the same grid; where a returned motion has a source video, they are adjacent
cells. Comparing across blocks is not meaningful: the arms differ in resolution,
frame rate, clip length and visual style by construction, and those differences are
documented per experiment rather than normalised away.

::: method title="Keyboard shortcuts"
`n` show or hide the sidebar · `/` focus the sidebar filter · `r` replay all visible
clips in sync · `p` pause or play all · click a clip to open it · `←` `→` step one
frame · `space` play/pause · `Esc` close.
:::

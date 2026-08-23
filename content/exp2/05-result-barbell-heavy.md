---
title: Result 2 — barbell_heavy
nav: Result 2 · barbell_heavy
lead: "A person lifts a heavy barbell from the ground." The clearest negative in the sweep. No barbell is ever drawn, at any K — and this is the prompt that shows the video prior extends what it is given rather than replacing it.
---

## What went in

MotionGPT3's clip is **an arm-raise, not a barbell lift**. Input energy 0.072
(s1234) and 0.078 (s5678).

The contrast with [`box_heavy`](result-box-heavy.html) is the point of this page.
Both prompts name a concrete object the input does not contain. In one case the
model draws the object and performs the action; here it never does.

## Strong control

::: clips arms=blue,Kall,K9 ids=barbell_heavy seeds=1234,5678 size=lg
`K = all` (0.84) and `K = 9` (0.77) copy the arm-raise, adding slightly less motion
than the input.
:::

## The useful window

::: clips arms=blue,K5,K3_2 ids=barbell_heavy seeds=1234,5678 size=lg
`K = 5` (1.99) and `K = 3_2` (1.96) are the only two sets where this prompt moves
substantially more than its input. Everywhere else it moves *less*.
:::

::: key title="What we observed"
**Stops looking stiff:** at `K = 5` and `K = 3_2` only.

**Stops doing the action:** it never does the action. No barbell is ever drawn, at
any K — unlike the box in `box_heavy`. The video model extends the arm-raise it
was given into larger arm-waving; it does not replace it with a lift.

**Goes the other way at three sets:** `K = 3_1` (0.47), `K = 2_1` (0.58) and
`K = 2_2` (0.45). The character nearly *freezes*. Given two distant pinned poses it
takes the cheapest path between them rather than performing anything.
:::

## Placement at K = 3

::: clips arms=K3_1,K3_2,K3_3,K3_4 ids=barbell_heavy seeds=1234,5678
`3_1` 0.47 · `3_2` 1.96 · `3_3` 2.90 · `3_4` 0.81. The spread here is the widest of
any prompt: pinning both ends nearly halts the clip, freeing both ends nearly
triples it.
:::

## Placement at K = 2

::: clips arms=K2_1,K2_2,K2_3,K2_4 ids=barbell_heavy seeds=1234,5678
`2_1` 0.58 · `2_2` 0.45 · `2_3` **2.87** · `2_4` 0.81. `2_1` and `2_3` hand over the
same *number* of frames; `2_3` produces five times the motion because neither end
is pinned.
:::

::: warn title="This prompt holds the sweep's lowest crossfade ratio"
`K = 2_2` frames 64 → 120 scores 0.38 on the
[morphing check](does-it-work.html#test-3-no-morphing-anywhere) — the lowest
anywhere. On inspection it is the near-freeze described above, not a dissolve.
The check is measuring "close to a linear blend", and a character that barely
moves is trivially close to one.
:::

## Why this prompt matters more than it looks

::: key title="The prior extends, it does not correct"
`box_heavy` and `barbell_heavy` differ in exactly the way that separates the two
hypotheses:

- If the video model **corrected** bad motion, it would fix both — an arm-raise
  labelled "lifts a heavy barbell" is as wrong as a flail labelled "lifts a heavy
  box".
- If the video model **extends** what it is handed, it fixes only the one where
  the input already resembles the action closely enough to be developed into it.

The second is what happens. This is the single clearest piece of evidence for that
reading in the experiment, and it is
[carried forward as a limit](verdict.html) rather than treated as a failure.
:::

## The numbers for this prompt

::: metrics src=results/checks/energy.json key=results where=prompt_id=barbell_heavy cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
Silhouette-change energy. Note how many rows sit **below 1.00** — this prompt
under-moves at most conditioning sets.
:::

## Timing strip

::: clips arms=strip ids=barbell_heavy seeds=1234,5678 width=760px
Every condition, time-aligned. The near-frozen rows (`3_1`, `2_1`, `2_2`) are
obvious here in a way they are not in the video grid.
:::

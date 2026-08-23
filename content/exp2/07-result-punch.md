---
title: Result 4 — punch
nav: Result 4 · punch
lead: "A person throws right and left punches." The highest-energy input of the six, and the most stable across the sweep. This is the one prompt where the video model completes an action the input only gestures at.
---

## What went in

MotionGPT3 produces **a boxing guard with small arm movement that never reaches
extension**. It reads as someone shadow-boxing tentatively rather than punching.
Input energy 0.148 (s1234) and 0.146 (s5678) — the highest of the six by a wide
margin.

Because the input is already energetic, this prompt is also the most stable across
the sweep: ratios stay between 0.67 and 1.43 everywhere, with none of the freezes
or doublings the other prompts show.

## Strong control

::: clips arms=blue,Kall,K9 ids=punch seeds=1234,5678 size=lg
`K = all` (0.90) copies. `K = 9` (1.20) is the interesting cell: **this is the only
prompt in the sweep where K = 9 adds anything at all.**
:::

## The useful window

::: clips arms=blue,K5,K3_2 ids=punch seeds=1234,5678 size=lg
`K = 5` (1.33) and `K = 3_2` (1.03).
:::

::: key title="What we observed"
**Stops looking stiff:** already at `K = 9` (1.20) — unique to this prompt.

**From `K = 5` downward the model extends the guard into full punches, with the arm
actually reaching extension.** The input never does this. It is not adding generic
movement; it is completing the specific action named in the prompt.

**Stops doing the action:** the boxing stance survives all the way to the loosest
sets. The one departure is at `K = 3_3`, where the model adds a **high kick at
frame 96** — at which point it is no longer the prompt.
:::

## Placement at K = 3

::: clips arms=K3_1,K3_2,K3_3,K3_4 ids=punch seeds=1234,5678
`3_1` 0.94 · `3_2` 1.03 · `3_3` 1.43 · `3_4` 1.40. The narrowest spread of any
prompt — an energetic input leaves less room for placement to matter.
:::

## Placement at K = 2

::: clips arms=K2_1,K2_2,K2_3,K2_4 ids=punch seeds=1234,5678
`2_1` 0.67 · `2_2` 0.82 · `2_3` 0.99 · `2_4` 1.05. Note that `2_3` — which nearly
doubles or triples every other prompt — does almost nothing here.
:::

::: note title="Why punch reads differently from the rest"
For every other prompt, "more motion" is ambiguous evidence. Here it is not,
because the *kind* of motion added is exactly the missing part of the named action:
the extension at the end of a punch.

That is also why this prompt carries the most weight in the
[round trip](../exp1/result-punch.html), where the returned motion is much jerkier
than the input — and a real punch *is* jerky. It is the one case in either
experiment where higher jerk reads as more physical rather than as noise.
:::

## The numbers for this prompt

::: metrics src=results/checks/energy.json key=results where=prompt_id=punch cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
Silhouette-change energy. The tightest range in the sweep.
:::

## Timing strip

::: clips arms=strip ids=punch seeds=1234,5678 width=760px
Every condition, time-aligned. Look along the rows for the frames where the arm
reaches full extension — they appear from `K = 5` down and not above it.
:::

---
title: Result 3 — push_heavy
nav: Result 3 · push_heavy
lead: "A person pushes a car." The input barely moves at all — the lowest-energy clip of the six — and no car is ever drawn at any K. What the video model adds here is motion without meaning.
---

## What went in

The blue input is **close to static**: the character just stands with one arm out.
Input energy 0.036 (s1234) and 0.034 (s5678) — the lowest of the six prompts by a
clear margin.

The physical beat this prompt was chosen for is *the lean into the load before
anything moves*. Nothing in the input leans.

## Strong control

::: clips arms=blue,Kall,K9 ids=push_heavy seeds=1234,5678 size=lg
`K = all` (0.70) and `K = 9` (0.63) copy the near-static stance faithfully. These
are the lowest strong-control ratios in the sweep, because there is so little to
copy.
:::

## The useful window

::: clips arms=blue,K5,K3_2 ids=push_heavy seeds=1234,5678 size=lg
`K = 5` (1.24) and `K = 3_2` (1.61). Real movement is added — but see below for
what kind.
:::

::: key title="What we observed"
**Stops looking stiff:** `K = 5` (1.24), strongly at `3_2` / `3_3` / `2_2`
(1.6–2.2).

**Stops doing the action:** it never starts. **No car is ever drawn and nothing is
ever pushed, at any K.**

**What gets added instead is arbitrary.** At `2_2` and `2_3` the extra motion is
leg raises and a crouch — movement that has nothing to do with pushing. Given a
near-empty input and a long free run, the model fills the time with generic
plausible human movement rather than with the named action.
:::

## Placement at K = 3

::: clips arms=K3_1,K3_2,K3_3,K3_4 ids=push_heavy seeds=1234,5678
`3_1` 0.83 · `3_2` 1.61 · `3_3` 2.16 · `3_4` 1.04. The same ordering as everywhere
else: free ends buy motion, pinned ends do not.
:::

## Placement at K = 2

::: clips arms=K2_1,K2_2,K2_3,K2_4 ids=push_heavy seeds=1234,5678
`2_1` 0.84 · `2_2` 1.70 · `2_3` **2.52** · `2_4` 1.38.
:::

::: note title="A useful control, precisely because it fails"
`push_heavy` is the cleanest demonstration that added motion is not the same as
added *meaning*. `2_3` produces two and a half times the input's movement and none
of it is pushing. Any measure that scored this experiment on motion quantity alone
would call this a success.

It also sets up the [round trip](../exp1/result-push-heavy.html), where this
prompt comes back **smoother** than it went in and no better — the mirror image of
the same finding.
:::

## The numbers for this prompt

::: metrics src=results/checks/energy.json key=results where=prompt_id=push_heavy cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
Silhouette-change energy. The absolute `energy` column is worth reading here as
well as the ratio — the input is so nearly static that a large ratio still means a
small amount of movement.
:::

## Timing strip

::: clips arms=strip ids=push_heavy seeds=1234,5678 width=760px
Every condition, time-aligned.
:::

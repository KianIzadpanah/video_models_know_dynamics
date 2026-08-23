---
title: Result 6 — baseball
nav: Result 6 · baseball
lead: "A person hit a ball with baseball bat." A stride and a rotation get added that read a little like batting — but no bat and no ball ever appear, at any K. The marginal case of the six.
---

## What went in

Input energy 0.089 (s1234) and 0.120 (s5678) — second-highest of the six, and the
one prompt where the two seeds differ substantially from each other.

The beat this prompt was chosen for is *load onto the back foot, pause, then the
fast rotation through contact*. It is a timing signature that is very specific and
hard to fake.

## Strong control

::: clips arms=blue,Kall,K9 ids=baseball seeds=1234,5678 size=lg
`K = all` (0.88) and `K = 9` (0.75).
:::

## The useful window

::: clips arms=blue,K5,K3_2 ids=baseball seeds=1234,5678 size=lg
`K = 5` (1.38) and `K = 3_2` (1.44).
:::

::: key title="What we observed"
**Stops looking stiff:** `K = 5` (1.38).

**At `K = 5` and `K = 3_2` the model adds a leg lift and a rotation that read as a
batting stride.** That is genuinely the right *shape* of motion for the prompt —
weight onto the back foot, then rotation.

**But no bat and no ball are ever drawn, at any K.** Unlike `box_heavy`, the model
never places the named object in the scene, so what is added is the body mechanics
of batting without the thing being batted.

**And it does not hold at looser sets.** At `2_1` (0.66) and `2_2` (0.90) it
settles back to near-input energy, and at `2_3` it wanders into unrelated arm
movement.
:::

## Placement at K = 3

::: clips arms=K3_1,K3_2,K3_3,K3_4 ids=baseball seeds=1234,5678
`3_1` 0.93 · `3_2` 1.44 · `3_3` 1.64 · `3_4` 1.16.
:::

## Placement at K = 2

::: clips arms=K2_1,K2_2,K2_3,K2_4 ids=baseball seeds=1234,5678
`2_1` 0.66 · `2_2` 0.90 · `2_3` 1.55 · `2_4` 0.83. Three of four sit at or below the
input.
:::

::: note title="Why this one is called marginal rather than positive"
The added motion is in the right direction, which `push_heavy` and
`barbell_heavy` cannot claim. But it is a stride and a rotation in empty space,
present at two conditioning sets and absent at the rest.

In the [round trip](../exp1/result-baseball.html) the same verdict holds from the
other side: the returned motion is slightly more dynamic, and foot-skate roughly
doubles, which is the opposite of what "more natural" should look like.
:::

## The numbers for this prompt

::: metrics src=results/checks/energy.json key=results where=prompt_id=baseball cols=seed:seed,K:set,energy:energy,energy_ratio:vs. input sort=-energy_ratio
Silhouette-change energy. Worth comparing the two seeds directly here — this is
the prompt where they diverge most.
:::

## Timing strip

::: clips arms=strip ids=baseball seeds=1234,5678 width=760px
Every condition, time-aligned.
:::

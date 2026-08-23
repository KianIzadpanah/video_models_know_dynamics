---
title: Composed montages
nav: Montages
lead: The same material pre-rendered into single video files — three arms side by side, matched pairs stacked, and everything in one clip. For watching rather than clicking.
---

The grids on the results pages are built from individual clips, which makes them
filterable but leaves the arms free to drift out of phase as they loop. The
montages below are composed with ffmpeg into one file per view, so the arms are
locked in sync and stay that way.

All montages are 24 fps with a tile height of 300 px. The T2M tile is 4.00 s and
the video tiles are 5.04 s, so the T2M tile freezes on its last frame for the
final second of each montage.

## Everything in one clip

::: clips arms=all seeds=0,1,2 size=lg width=620px
`all_s{seed}.mp4` — one row per prompt with matched pairs adjacent, all nine
prompts and all three arms in a single file. The fastest way to get an overall
impression before looking at anything closely.
:::

## Three arms side by side

One file per prompt: T2M, T2V and I2V in a labelled row.

::: clips arms=3up seeds=0,1,2 ids=box_heavy,box_light,barbell_heavy,barbell_light
The lift prompts, composed. Heavy and light alternate.
:::

::: clips arms=3up seeds=0,1,2 ids=push_heavy,push_light,punch,squat,baseball
The push pair and the three unloaded controls, composed.
:::

## Matched pairs stacked

One file per pair, heavy above light, across all three arms.

::: clips arms=pair seeds=0,1,2 ids=box,barbell,push size=lg width=900px
`pair_{pair}_s{seed}.mp4` — the cleanest single-file view of the central
comparison. Each file holds six tiles: two prompts × three arms.
:::

::: note title="Original files"
These montages exist in the experiment folder at full resolution under
`results/montage/`. The versions on this page are web-sized transcodes; see
[Provenance](provenance.html) for the mapping between the two.
:::

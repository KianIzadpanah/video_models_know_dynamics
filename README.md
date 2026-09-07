# Video Models Know Dynamics — experiment log site

A zero-dependency static site generator for the experiment log. You write
Markdown; `build.py` pulls the result clips straight out of the experiment
folders, transcodes them to web-sized copies, and emits a complete static site
into `docs/` that GitHub Pages can serve as-is.

```
python build.py            # full build
python build.py --serve    # build, then http://localhost:8000
```

Requirements: **Python 3.9+** (standard library only — no pip install) and
**ffmpeg** + **ffprobe** on `PATH`.

---

## 1. How it fits together

```
Experiments/
  Exp 00 - Generate motions ... /        <- untouched inputs
  Exp 01 - Comparing 3D motions ... /
  Exp 02 - Comparing animations ... /
  site/                                  <- THIS IS THE GIT REPO
    build.py            the generator
    site.json           global config: title, experiment order, encode settings
    content/
      index.md          the home page
      exp0/ exp1/ exp2/
        exp.json        where this experiment's media lives + how it is named
        01-overview.md  one file per page, ordered by the number prefix
        02-setup.md
        ...
    theme/
      base.html         the page shell
      assets/site.css   assets/site.js
    docs/               <- BUILD OUTPUT. Committed. Served by Pages.
```

Each experiment's `source_dir` in `exp.json` points at its folder by name, so
**renaming an experiment folder breaks the build until you update that field.**
The build reports it as `source_dir not found`.

Two things worth internalising:

- **The experiment folders are read-only inputs.** `build.py` never writes into
  them. Your originals are never touched, moved or re-encoded in place.
- **`docs/` is generated.** Never hand-edit it; it is overwritten on every build.
  It *is* committed, because GitHub Pages serves it directly.

### Why the build runs locally and not in CI

The generator needs the experiment folders and ffmpeg. The experiment folders
hold ~80 MB of originals each and are not in the repo, so a GitHub Action could
not reproduce the build. You run `build.py` on your machine and commit the
resulting `docs/`. That also means the site is exactly what you last saw locally.

---

## 2. Everyday workflow

```bash
cd site

python build.py --no-media       # prose-only: instant, reuses existing clips
python build.py                  # full: transcodes anything new or changed
python build.py --serve          # build then serve on :8000
python build.py --clean          # nuke docs/ and rebuild everything
```

`--no-media` is the one you want while writing. It skips ffmpeg entirely and
finishes in under a second.

Transcodes are cached in `.build-cache.json` (gitignored) keyed on source
mtime + size + encode settings, so a full rebuild only re-encodes what actually
changed. A cold build of all three experiments is ~2 min for 469 files;
subsequent builds are instant. `--no-media` finishes in under a second.

**Renaming an experiment folder invalidates the whole cache**, because the cache is
keyed on absolute source paths. The next build re-encodes everything. Harmless, just
slow.

### What the build tells you

Every run ends with a report. Pay attention to three parts of it:

- **`N unwritten section(s) marked :::todo`** — every `:::todo` block you left in
  the Markdown, with its file. This is your to-do list; ship with zero.
- **`N warning(s)`** — missing media, unknown directives, broken internal links,
  broken `#anchors`. Should always be zero.
- **`docs/media is N MB`** — keep an eye on this as experiments accumulate. See
  §6.
- **`pruned N stale file(s)`** — output that no longer corresponds to anything in
  `content/`, deleted. You see this after renaming or splitting a page, or after
  dropping a set from an `exp.json`. A stale page is worse than a missing one: it
  stays reachable and shows content you have since rewritten elsewhere, so the build
  removes it rather than leaving it. Nothing else is ever deleted from `docs/`.

---

## 3. Authoring a page

A page is one `.md` file in `content/<exp>/`. The number prefix sets the order
and is stripped from the URL: `04-loaded-lifting.md` → `exp0/loaded-lifting.html`.

```markdown
---
title: Loaded actions — lifting
nav: Lifting (box, barbell)
lead: One or two sentences under the title, setting up what this page shows.
---

## A section

Normal Markdown. **Bold**, *italic*, `code`, [links](setup.html), lists,
tables, fenced code blocks, blockquotes. Raw HTML passes through untouched if
you need something the parser doesn't cover.
```

Front matter keys: `title` (page title), `nav` (short sidebar label — defaults to
`title`), `lead` (the deck under the title).

`##` and `###` headings automatically get anchors and populate the "On this page"
rail on the right.

### The page convention

All three experiments follow the same shape, and new ones should too — it is what
makes the sidebar navigable when there are ten of them:

```
01-overview.md        what this asks, what we used, what came out. Has a :::diagram slot.
02-setup.md           how it was run: settings, constraints, what is reused
03-…                  any checks or controls that must be read before the results
04-result-<prompt>.md  ─┐
05-result-<prompt>.md   │ ONE PAGE PER PROMPT. This is the important part.
…                      ─┘
NN-verdict.md         what it establishes, stated narrowly
NN-provenance.md      seeds, checkpoints, files
```

One page per prompt is deliberate. It means a result is a single screen you can put
on a projector, and two prompts can be compared by flipping between two pages rather
than scrolling one long one. `tools/new-experiment.py --prompts a,b,c` scaffolds it.

Each result page then repeats the same internal order — what went in, the clips, what
we observed, the numbers, the timing strip — so that a reader who has read one page
knows where to look on all the others.

### Directives

Blocks fenced with `:::`. Attributes go on the opening line, content in the body.

An unquoted attribute value runs to the next ` key=` or to the end of the line, so
**labels may contain spaces without quoting**: `cols=a:Joint error mm,b:Jerk` works.
Quote the value if it needs to contain something that looks like ` key=`.

#### `:::clips` — the video grid

The workhorse. Rows are prompts, columns are arms, and each cell holds one clip
per seed.

```
::: clips arms=t2m,t2v,i2v ids=box_heavy,box_light seeds=0,1,2
Optional caption in Markdown.
:::
```

| attribute | meaning |
|---|---|
| `arms=` | comma-separated set names from `exp.json` → the columns. **Required.** |
| `ids=` | comma-separated item ids → the rows. Omit for sets whose filename pattern has no `{id}` (e.g. a whole-run montage). |
| `seeds=` | which seeds to emit. Defaults to `media.default_seeds` in `exp.json`. Emit all of them — the page toolbar filters between them at runtime. |
| `heads=off` | drop the column header row |
| `size=lg` | wider row-label column, for grids with few columns |
| `width=` | CSS max-width for the whole figure, e.g. `620px`. Use it on tall composites so they don't fill the content column. |

The page's seed/speed/sync toolbar appears automatically on any page containing a
`:::clips` block, and its seed buttons are the union of every `seeds=` on the page.
It also carries the speed buttons (¼×, ½×, 1×, 2×), the **Sync** toggle, a manual
restart, and pause-all.

#### `:::metrics` — a table from a manifest

```
::: metrics src=data/motions/manifest.json cols=prompt_id:prompt,seed:seed,fit_mpjpe_mm:MPJPE mm sort=-fit_mpjpe_mm limit=12
Optional caption.
:::
```

| attribute | meaning |
|---|---|
| `src=` | path to a JSON file, **relative to the experiment's `source_dir`** |
| `key=` | which key holds the array (default `entries`) |
| `cols=` | `field:Label` pairs, comma-separated. Omit for all fields. |
| `where=` | `field=value` filters, comma-separated |
| `sort=` | field name; prefix `-` to reverse |
| `limit=` | keep only the first N rows |

Numbers are right-aligned in a tabular figure automatically.

#### `:::stats` — a KPI strip

```
::: stats
9: prompts
81: clips total
:::
```
One `value: label` per line.

#### Callouts

`:::note`, `:::key`, `:::warn`, `:::method`, `:::todo` — each takes an optional
`title="…"` and a Markdown body.

- **`note`** — a neutral aside.
- **`key`** — "What we observed". Use for actual findings.
- **`warn`** — a caveat or confound the reader must know.
- **`method`** — how something was done.
- **`todo`** — an unwritten section. Renders as a visibly-unfinished dashed box
  *and* gets counted in the build report, so you cannot ship it by accident.

#### `:::diagram` — the diagram slot

A figure that is *allowed to be missing*. Every experiment overview has one.

```
::: diagram
Optional caption.
:::
```

If `diagram.png` exists either next to the page's `.md` or at the root of the
experiment folder, it is rendered as a figure. If it does not, the page shows a
calm dashed placeholder naming both paths you can drop the file at. It is **not**
a build warning either way — an empty slot is a valid state.

| attribute | meaning |
|---|---|
| `src=` | filename to look for. Default `diagram.png`. |
| `width=` | CSS max-width. Default `760px`. |
| `alt=` | alt text when the image is present. |

So: draw a pipeline diagram whenever you get round to it, save it as
`content/exp2/diagram.png`, rebuild, and it appears. Nothing else to change.

#### `:::figure` — a single image

```
::: figure src=diagram.png width=680px
Caption.
:::
```
`src` is resolved next to the `.md` file first, then inside the experiment
folder, and the file is copied into `docs/static/`.

---

## 4. Adding a new experiment

Say the next one lives in `Exp 03 - Optical flow under load`.

**Step 1 — scaffold.** Pass the prompt ids and you get one result page per prompt,
which is [the convention](#the-page-convention) the rest of the site follows.

```bash
cd site
python tools/new-experiment.py exp3 "Exp 03 - Optical flow under load"        --prompts box_heavy,barbell_heavy,punch
```

That creates `content/exp3/` with an `exp.json`, an overview (with a `:::diagram`
slot), a setup page, one result page per prompt, a verdict and a provenance page —
and adds `"exp3"` to `site.json`'s `experiments` list, which controls sidebar order.

**Step 2 — describe the media in `content/exp3/exp.json`.**

This is the only conceptually new part. A **set** is one column of a clip grid: a
directory plus a filename pattern with `{id}` and `{seed}` placeholders.

```json
"sets": {
  "flow": {
    "dir": "data/flow",
    "pattern": "{id}_s{seed}_flow.mp4",
    "label": "Optical flow",
    "sublabel": "RAFT, colour-wheel encoded",
    "max_width": 1440
  }
}
```

`max_width` is optional and overrides the global cap — use it for composites that
pack several tiles into one frame, which need more pixels than a single clip.
Add `"kind": "image"` for stills.

One set per column. Where an experiment has a *condition* axis rather than a model
axis — as Exp 1 and Exp 2 do — give each condition its own set and let the columns be
conditions:

```json
"K5":   { "dir": "data/videos", "pattern": "{id}_s{seed}_K5.mp4",
          "label": "K = 5", "sublabel": "0 · 32 · 64 · 88 · 120" },
"K3_2": { "dir": "data/videos", "pattern": "{id}_s{seed}_K3_2.mp4",
          "label": "K = 3_2", "sublabel": "64 · 88 · 120 — head free" }
```

Put the meaning in `sublabel`. A column headed `K = 3_2` tells the reader nothing;
one subtitled *"64 · 88 · 120 — head free"* tells them what the comparison is.

**Items** are the rows. Either list them inline:

```json
"items": {
  "box_heavy": { "text": "a person lifts a heavy box from the floor",
                 "verdict": "improved",
                 "meta": { "the beat": "the pause at the bottom, then the slow rise" } }
}
```

or pull them from a JSON file you already have:

```json
"items_from": { "path": "configs/prompts.json", "key": "prompts", "id_field": "id" }
```

Each item's fields are then available: `text` becomes the row label, `meta` renders
as small key/value lines under it, and any field can be turned into a coloured chip
via `media.chips`. The chip classes `improved`, `partial`, `marginal`, `no-change`
and `unusable` are already styled.

**Step 3 — sanity-check the paths before writing prose.** Cheapest possible check
that `exp.json` describes reality:

```bash
python build.py --no-media 2>&1 | grep "missing media"
```

Silence means every set × item × seed combination resolves to a real file. Do this
first; it is much less annoying than discovering a wrong `pattern` after writing ten
pages.

**Step 4 — write the pages, and build.**

```bash
python build.py
```

Missing files, bad set names, unknown directives, broken links and broken `#anchors`
all surface as warnings rather than silently producing an empty grid.

---

## 4b. Slide decks

An experiment gets a deck by dropping a `slides.json` next to its `exp.json`.

> **Decks are not part of the website.**

Each one is written **one level up, next to the experiment folders** — outside this
repo — as a single self-contained `.html` with its clips inlined as data URIs:

```bash
python build.py
#   deck: exp6-slides.html (14 slides, 160 clips, 24.3 MB) -> …/Experiments
#         local only, not part of docs/ and never published
```

That means a deck

- **never appears at a public URL.** Nothing in `docs/` links to one, and because
  the file lands outside the repo, git never sees it — there is nothing to
  accidentally commit. If a previous build left one in `docs/`, the
  [pruner](#what-the-build-tells-you) deletes it.
- **works from disk.** Double-click it, or copy it to a laptop or a USB stick. It
  carries its own clips, so it needs no repo, no server and no network.
- **costs nothing to rebuild.** It reuses the transcodes the site pages already
  produced, so no extra ffmpeg work.

The price is size: inlining 160 clips makes a ~24 MB file. That is the right trade
for something you present from and hand around, and the wrong one for something you
serve, which is the other reason it is not on the site.

`site.json`'s `url` is used for the deck's "← write-up" link, so a local deck can
still point back at the published pages.

`content/exp6/slides.json` is the worked example. Its shape:

| key | what it is |
|---|---|
| `title`, `subtitle`, `footer` | the title slide's text and the bar along the bottom |
| `intro` | `question`, `bullets`, `stats`, and `pipeline` / `pipeline_side` — the boxes and arrows are **drawn from that list**, so there is no diagram asset to keep in sync |
| `conditions` | one entry per column: `key` (matches the set names), `label`, `count`, `frames`. The frame list is drawn as a tick timeline. |
| `rows` | one entry per row of the matrix: `set` (with `{cond}` substituted), `label`, `sub` |
| `input_set` | an optional single clip shown beside each result's heading |
| `clips` | per item: `prompt`, `headline`, `errors` (one per condition), `breaks`, `action` |
| `slides` | the running order. Types: `intro`, `conditions`, `clip` (needs `id`), `row` (a single set across conditions for several `ids`), `closing`. |
| `closing` | `title`, `headline`, `columns` (each `kind` `good`/`bad`, `title`, `items`), `punchline` |

Missing media and unknown set names surface as build warnings, exactly as they do
for a page, so a deck cannot silently ship an empty cell.

### The PowerPoint version

```bash
python tools/make_pptx.py exp6      # -> ../exp6-slides.pptx
```

Same `slides.json`, same running order, rendered as a **static, light-theme
`.pptx`** next to the HTML deck. Requires `python-pptx`, `Pillow` and ffmpeg.

PowerPoint cannot play the HTML deck's synchronised video grids, so the motion
becomes *frames*: every clip is sampled at **f0 · f56 · f112 · f168** and laid out
conditions-down, time-across — the one arrangement that shows both what changed
with K and what happened over the six seconds. Each result slide carries two of
those grids side by side, *what the model made* and *what came back as motion*,
with the joint error beside each row and the best value in green.

Nothing on a slide is a video, an animation, a SmartArt or an embedded object —
just pictures and text boxes. It opens anywhere, prints, and is ~4 MB. The
pipeline diagram and the K timelines are drawn from `slides.json` with Pillow, so
there is no diagram asset to keep in sync.

Extracted frames are cached in `.pptx-frames/` (gitignored); the second build is
fast.

### Presenting

| key | action |
|---|---|
| `→` `space` `PageDown` / click | next slide |
| `←` `PageUp` | previous |
| `Home` `End` | first / last |
| `f` | full screen |
| `r` | restart the clips on this slide |

The clips on a slide **loop in lockstep**, on a period set by the longest of them,
and only the current slide and its neighbour hold a loaded video — a fourteen-slide
deck carries ~160 clips, and attaching them all would stall the tab mid-demo.

---

## 5. Deploying to GitHub Pages

Target URL: **`https://kianizadpanah.github.io/video_models_know_dynamics/`**

That URL is determined by two things: your account name (`kianizadpanah`) and the
**repository name**, which must be exactly `video_models_know_dynamics`.

### One-time setup

**1. Create the repo on GitHub.** Public, named exactly
`video_models_know_dynamics`. Do **not** let GitHub add a README or `.gitignore` —
this folder already has both.

**2. Push this folder.** Run these from inside `site/`:

```bash
cd site
git init -b main
git add .
git commit -m "Experiment log site: generator, theme, and write-ups for Exp 0, 1, 2"
git remote add origin https://github.com/kianizadpanah/video_models_know_dynamics.git
git push -u origin main
```

**3. Turn on Pages.** In the repo on GitHub: **Settings -> Pages**.

- **Source:** `Deploy from a branch`
- **Branch:** `main`, folder **`/docs`**
- Save.

The first deploy takes 1-2 minutes. The site is then live at
`https://kianizadpanah.github.io/video_models_know_dynamics/`.

### Nothing to configure for the subpath

Every internal link, script, stylesheet and clip URL the generator emits is
**relative**. That means the identical `docs/` works at a domain root, at the
`/video_models_know_dynamics/` subpath, and by opening `docs/index.html` straight
off your filesystem. There is no base-URL setting to get wrong.

`docs/.nojekyll` is written on every build. It matters: without it GitHub runs
Jekyll over the output and silently drops files it does not like.

### Every update after that

```bash
cd site
python build.py
git add -A
git commit -m "Exp 0: wrote up the box pair observations"
git push
```

Pages redeploys within a minute or two. Hard-refresh (Ctrl-Shift-R) if you see a
stale page — GitHub caches assets aggressively.

### Checking a build before you push

```bash
python build.py --serve
```

Then open <http://localhost:8000/>. This serves `docs/` exactly as Pages will,
which is worth doing before a meeting.

### A custom domain, later

Put a `CNAME` file in `theme/assets/` — everything there is copied to `docs/` on
every build — containing just your domain. Then point a `CNAME` DNS record at
`kianizadpanah.github.io` and set the domain in Settings -> Pages.

## 6. Size and bandwidth

GitHub's limits: **100 MB per file** (hard), **1 GB per repo** (recommended), and
**100 GB/month** bandwidth (soft). The transcoding step is what keeps you inside
them.

The three current experiments reference ~400 MB of originals and produce
**46.5 MB** of web clips across 469 files. At that ratio you have room for roughly
15–20 more experiments before the repo gets uncomfortable. Levers in `site.json` if
it ever gets tight:

```json
"media": { "video_max_width": 720, "video_crf": 28, "video_preset": "medium" }
```

Raise `video_crf` to 30–32 for smaller files, lower it to 24–26 for better
quality. Change either and the whole cache invalidates, so the next build
re-encodes everything.

If a single experiment is genuinely enormous, keep its clips out of the repo and
point the set's `dir` at a host you control — but the current numbers are nowhere
near needing that.

---

## 7. Design notes

Things that were deliberate, in case you want to change them:

- **Real multi-page HTML, no client-side router.** Every page is a real file at a
  real URL, so deep links, browser history, print and search engines all just
  work. The sidebar is rendered into every page server-side, which means the nav
  is visible even with JavaScript disabled.
- **The sidebar collapses on navigation, and the state is persisted.** Picking a
  page hides the sidebar so the clips get the whole window; the burger in the top
  bar (or `n`) brings it back. Because this is a real multi-page site, the state
  *has* to live in `localStorage` — an in-memory flag would reset on every
  navigation and the sidebar would spring open again on each page. It is applied
  by an inline script in `<head>`, before first paint, so nothing flashes. Below
  940 px the same state drives an overlay drawer instead of a column, so opening
  it never squeezes the clips.
- **There is no "on this page" rail.** It cost ~230 px of width on every page and
  earned it on almost none: the result pages are five or six headings long and the
  headings are visible anyway. Headings keep their `id`s and their `#` anchor
  links, so cross-page deep links still work. The width went to the clip grids.
- **All internal paths are relative.** The site works at any subpath, at a domain
  root, and by opening `docs/index.html` off the filesystem. Nothing needs a
  configured base URL.
- **Clips are lazy.** A `<video>` gets no `src` until it is within 350 px of the
  viewport, and pauses when it scrolls away. This is what makes a 54-clip page
  usable. Posters are grabbed from ~40 % into each clip rather than frame 0,
  because frame 0 of these clips is often a neutral standing pose.
- **Clips loop in lockstep, not independently.** The point of these pages is
  frame-against-frame comparison, and clips left to their own `loop` attribute
  drift apart immediately: each one starts whenever the observer attaches it, and
  within an experiment the arms can differ in length. So `loop` is turned off and
  a single timer restarts every visible clip together, on a period set by the
  longest of them; a shorter clip holds on its last frame until the group comes
  round again, exactly as the pre-composed montages do. The toolbar's **Sync**
  button turns it off if you want independent looping. Two details worth keeping
  if you touch this: the timer only ever touches clips that are *already
  attached*, because force-loading the rest would defeat the lazy loading; and a
  clip revealed mid-cycle is seeked to the group's elapsed time so scrolling does
  not knock it out of step.
- **Seed filtering is client-side.** All seeds are in the HTML; the toolbar hides
  the ones you aren't looking at, so switching seeds is instant and hidden clips
  cost nothing until shown.
- **Audio is stripped from every transcode.** These comparisons never depend on
  sound, and it saves bytes.
- **Dark mode has three states** — system, forced light, forced dark — handled by
  defining the palette on `:root` and overriding it in both a
  `prefers-color-scheme` block and a `[data-theme]` block, so the toggle wins in
  either direction.

### Keyboard shortcuts

| key | action |
|---|---|
| `n` | show / hide the sidebar |
| `/` | focus the sidebar filter |
| `r` | replay all visible clips in sync |
| `p` | pause / play all |
| click a clip | open the frame-stepper |
| `←` `→` or `,` `.` | step one frame (in the frame-stepper) |
| `space` | play / pause (in the frame-stepper) |
| `Esc` | close the frame-stepper, or the sidebar |

#!/usr/bin/env python3
"""
Scaffold a new experiment: content/<id>/ with an exp.json and starter pages,
and register it in site.json so it appears in the sidebar.

    python tools/new-experiment.py exp1 "Exp1-optical-flow-under-load"
    python tools/new-experiment.py exp1 "Exp1-..." --title "Optical flow under load"

The second argument is the experiment's folder name as it sits next to site/.
Nothing is overwritten: if content/<id>/ already exists the script stops.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXP_JSON = {
    "id": None,
    "nav": None,
    "title": None,
    "question": "One sentence: what does this experiment actually ask?",
    "status": "in progress",
    "date": "",
    "tags": [],
    "source_dir": None,
    "media": {
        "seeds": ["0", "1", "2"],
        "default_seeds": ["0"],
        "_items_note": [
            "Rows of a clip grid. Either list them inline as {\"id\": {\"text\": \"...\"}},",
            "or pull them from a JSON file you already have with items_from."
        ],
        "items": {
            "example_id": {"text": "the label shown beside the row", "load": "heavy"}
        },
        "chips": [
            {"field": "load", "labels": {"heavy": "heavy load", "light": "light load"}}
        ],
        "_sets_note": [
            "One set = one column of a clip grid. dir is relative to source_dir;",
            "pattern may use {id} and {seed}. Add \"kind\": \"image\" for stills,",
            "and \"max_width\": 1440 for composites that pack several tiles per frame."
        ],
        "sets": {
            "example_arm": {
                "dir": "data/videos",
                "pattern": "{id}_s{seed}.mp4",
                "label": "Column heading",
                "sublabel": "smaller text under it"
            }
        }
    }
}

OVERVIEW = """---
title: Overview
nav: Overview
lead: One or two sentences in plain language: what this experiment does and why it is worth reading.
---

## The idea, in plain words

What is being asked, why it is worth asking, and what would count as an answer.
Write this for someone seeing the project for the first time.

::: diagram
The pipeline. Drop a `diagram.png` next to this file, or at the root of the
experiment folder, and it appears here. Until then this slot shows a placeholder.
:::

## What we used

| step | model / tool | notes |
|---|---|---|
|  |  |  |

::: stats
0: prompts
0: clips
:::

## What came out of it

::: todo title="The findings, in short"
Two or three numbered points. Write this last, but put it here, because it is what
a reader wants before the detail.
:::

## Suggested reading order

::: method title="How to work through this"
1. **[How it was run](setup.html)** - settings, constraints, what is reused.
2. **The prompts**, one page each.
3. **[Verdict](verdict.html)** - what this establishes and what it does not.
:::
"""

SETUP = """---
title: How it was run
nav: How it was run
lead: The settings, the constraints, and anything reused from another experiment.
---

## The pipeline

| step | what happens | output |
|---|---|---|
| 1 |  |  |

## Settings

::: method title="Held fixed across every clip"
Seeds, checkpoints, resolutions, sampler settings. Enough to re-run it.
:::

## What each result page shows

Every prompt gets its own page, laid out in the same order, so two prompts can be
compared by flipping between two pages rather than scrolling one.

::: todo title="Describe the per-page layout"
Which grids appear, in what order, and what each one isolates.
:::
"""

RESULT = """---
title: Result {n} - {pid}
nav: Result {n} · {pid}
lead: The prompt text, then a one-line verdict.
---

## What went in

What the input looked like, and any number that sizes it.

## The clips

::: clips arms=example_arm ids={pid} seeds=0,1,2 size=lg
Caption. Say what to look at and what would count as a difference.
:::

::: todo title="What we observed"
Write what you actually see. Be specific about which clips support it, and say
explicitly whether it survives across seeds.
:::
"""

VERDICT = """---
title: Verdict
nav: Verdict
lead: What this experiment establishes, stated as narrowly as the evidence allows.
---

## The result

::: todo title="Per-prompt verdict table"
One row per prompt, one short verdict each. Link each row to its page.
:::

## Caveats worth carrying

::: todo title="What could undermine this"
Confounds, failure modes, and anything a later experiment has to check.
:::
"""

PROVENANCE = """---
title: Provenance
nav: Provenance
lead: Seeds, checkpoints, settings, and where every file came from.
---

## Seeds

## Models and checkpoints

| role | model | detail |
|---|---|---|
|  |  |  |

## Files

| path | what is in it |
|---|---|
|  |  |
"""

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id", help="short id, e.g. exp1 (becomes the URL folder)")
    ap.add_argument("source_dir", help="experiment folder name, as it sits next to site/")
    ap.add_argument("--title", default=None, help="human title (default: derived from source_dir)")
    ap.add_argument("--nav", default=None, help="short sidebar label (default: 'Exp N')")
    ap.add_argument("--prompts", default="",
                    help="comma-separated prompt ids; scaffolds one result page per id, "
                         "which is the convention the rest of the site follows")
    a = ap.parse_args()

    dest = ROOT / "content" / a.id
    if dest.exists():
        print(f"error: {dest.relative_to(ROOT)} already exists — nothing written.", file=sys.stderr)
        return 1

    src = ROOT.parent / a.source_dir
    if not src.is_dir():
        print(f"warning: ../{a.source_dir} does not exist yet. Writing the config anyway;\n"
              f"         the build will warn until the folder is there.")

    nav = a.nav or (a.id[:3].title() + " " + a.id[3:] if a.id.startswith("exp") else a.id)
    title = a.title or a.source_dir.split("-", 1)[-1].replace("-", " ").strip().capitalize()

    cfg = json.loads(json.dumps(EXP_JSON))          # deep copy
    cfg["id"] = a.id
    cfg["nav"] = nav
    cfg["title"] = title
    cfg["source_dir"] = f"../{a.source_dir}"

    pids = [x.strip() for x in a.prompts.split(",") if x.strip()]
    if pids:
        cfg["media"]["items"] = {pid: {"text": f"the prompt text for {pid}"} for pid in pids}

    dest.mkdir(parents=True)
    (dest / "exp.json").write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")

    written = ["exp.json"]

    def emit(name: str, text: str) -> None:
        (dest / name).write_text(text, encoding="utf-8")
        written.append(name)

    emit("01-overview.md", OVERVIEW)
    emit("02-setup.md", SETUP)
    # One result page per prompt, numbered from 03 so the tail pages stay last.
    for i, pid in enumerate(pids or ["example_id"], start=1):
        emit(f"{i + 2:02d}-result-{pid.replace('_', '-')}.md", RESULT.format(n=i, pid=pid))
    tail = len(pids or ["x"]) + 3
    emit(f"{tail:02d}-verdict.md", VERDICT)
    emit(f"{tail + 1:02d}-provenance.md", PROVENANCE)

    site_file = ROOT / "site.json"
    site = json.loads(site_file.read_text(encoding="utf-8"))
    if a.id not in site.get("experiments", []):
        site.setdefault("experiments", []).append(a.id)
        site_file.write_text(json.dumps(site, indent=2) + "\n", encoding="utf-8")

    print(f"created content/{a.id}/")
    for name in written:
        note = "   <- point media.sets at your real files" if name == "exp.json" else ""
        print(f"  {name}{note}")
    print(f"registered '{a.id}' in site.json (sidebar order = the 'experiments' list)")
    print(f"\nnext: edit content/{a.id}/exp.json, then  python build.py --serve")
    return 0


if __name__ == "__main__":
    sys.exit(main())

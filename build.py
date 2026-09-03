#!/usr/bin/env python3
"""
Static site generator for the "Video Models Know Dynamics" experiment log.

Reads Markdown write-ups from content/, pulls result media straight out of the
sibling experiment folders, transcodes it to web-sized copies, and emits a
complete static site into docs/ ready for GitHub Pages.

Dependencies: Python 3.9+ (standard library only) and ffmpeg/ffprobe on PATH.

    python build.py              # full build (transcodes new/changed media)
    python build.py --no-media   # prose only, reuse existing media  (fast)
    python build.py --serve      # build, then serve docs/ on :8000
    python build.py --clean      # wipe docs/ first

See README.md for the authoring guide.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:  # Windows consoles default to cp1252; page titles here are not ASCII
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
THEME = ROOT / "theme"
OUT = ROOT / "docs"

WARNINGS: list[str] = []
STATIC_USED: set[str] = set()
TODOS: list[str] = []


def warn(msg: str) -> None:
    WARNINGS.append(msg)


# ---------------------------------------------------------------------------
# tiny front-matter parser (flat YAML subset: scalars, [inline, lists], - lists)
# ---------------------------------------------------------------------------

def _scalar(raw: str):
    s = raw.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_scalar(p) for p in inner.split(",") if p.strip()] if inner else []
    low = s.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "~", ""):
        return None
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d*\.\d+", s):
        return float(s)
    return s


def split_front_matter(text: str) -> tuple[dict, str]:
    """Return (front_matter_dict, body). Front matter is a leading --- block."""
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    meta: dict = {}
    key = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("- ") and key:
            meta.setdefault(key, [])
            if isinstance(meta[key], list):
                meta[key].append(_scalar(line.lstrip()[2:]))
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            key = k.strip()
            meta[key] = _scalar(v) if v.strip() else []
    return meta, "\n".join(lines[end + 1:])


# ---------------------------------------------------------------------------
# markdown -> html  (deliberate subset; raw HTML passes through untouched)
# ---------------------------------------------------------------------------

_BLOCK_TAGS = (
    "div", "table", "figure", "section", "details", "p", "ul", "ol", "pre",
    "blockquote", "h1", "h2", "h3", "h4", "iframe", "video", "img", "aside",
)


def slugify(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s or "section"


def inline(text: str) -> str:
    """Inline markdown. Raw inline HTML is intentionally left alone."""
    stash: list[str] = []

    def keep(rendered: str) -> str:
        """Park finished HTML so later inline passes cannot touch it."""
        stash.append(rendered)
        return f"\x00{len(stash) - 1}\x00"

    # code spans first so their contents are never re-processed
    text = re.sub(r"``(.+?)``|`([^`]+?)`", lambda m: keep_code(m, stash), text, flags=re.S)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)",
                  lambda m: keep(_img(m)), text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: keep(_link(m)), text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text, flags=re.S)
    text = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w_])_([^_\n]+?)_(?![\w_])", r"<em>\1</em>", text)
    text = text.replace("\\*", "*").replace("\\_", "_")
    # Restore high indices first: a link or image may hold a code-span
    # placeholder, and code spans always occupy the lower indices.
    for i in range(len(stash) - 1, -1, -1):
        text = text.replace(f"\x00{i}\x00", stash[i])
    return text


def keep_code(m, stash: list[str]) -> str:
    body = m.group(1) if m.group(1) is not None else m.group(2)
    body = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    stash.append(f"<code>{body}</code>")
    return f"\x00{len(stash) - 1}\x00"


def _img(m) -> str:
    alt, src, title = m.group(1), m.group(2), m.group(3)
    t = f' title="{title}"' if title else ""
    return f'<img src="{src}" alt="{alt}"{t} loading="lazy">'


def _link(m) -> str:
    label, href = m.group(1), m.group(2)
    ext = ' target="_blank" rel="noopener"' if re.match(r"https?://", href) else ""
    return f'<a href="{href}"{ext}>{inline(label)}</a>'


class Renderer:
    """Block-level markdown renderer with ::: directive support."""

    def __init__(self, ctx: "PageCtx"):
        self.ctx = ctx
        self.headings: list[tuple[int, str, str]] = []
        self._ids: dict[str, int] = {}

    def uid(self, text: str) -> str:
        base = slugify(text)
        n = self._ids.get(base, 0)
        self._ids[base] = n + 1
        return base if n == 0 else f"{base}-{n + 1}"

    def render(self, text: str) -> str:
        lines = text.replace("\r\n", "\n").split("\n")
        out: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            # ::: directive block
            if stripped.startswith(":::"):
                name_attrs = stripped[3:].strip()
                body, i = self._collect(lines, i + 1, lambda s: s.strip() == ":::")
                out.append(self.directive(name_attrs, body))
                continue

            # fenced code
            if stripped.startswith("```"):
                lang = stripped[3:].strip()
                body, i = self._collect(lines, i + 1, lambda s: s.strip().startswith("```"))
                esc = "\n".join(body).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                cls = f' class="language-{lang}"' if lang else ""
                out.append(f"<pre><code{cls}>{esc}</code></pre>")
                continue

            # heading
            m = re.match(r"(#{1,4})\s+(.*)", stripped)
            if m:
                level = len(m.group(1))
                body = inline(m.group(2).strip())
                hid = self.uid(m.group(2))
                if level in (2, 3):
                    self.headings.append((level, hid, re.sub(r"<[^>]+>", "", body)))
                out.append(
                    f'<h{level} id="{hid}">{body}'
                    f'<a class="anchor" href="#{hid}" aria-label="link to this section">#</a></h{level}>'
                )
                i += 1
                continue

            # horizontal rule
            if re.fullmatch(r"(\*\s*){3,}|(-\s*){3,}", stripped):
                out.append("<hr>")
                i += 1
                continue

            # table
            if "|" in stripped and i + 1 < len(lines) and re.fullmatch(
                    r"\|?[\s:|-]+\|[\s:|-]*", lines[i + 1].strip()):
                block, i = self._take_while(lines, i, lambda s: "|" in s.strip())
                out.append(self._table(block))
                continue

            # blockquote
            if stripped.startswith(">"):
                block, i = self._take_while(lines, i, lambda s: s.strip().startswith(">"))
                inner = "\n".join(re.sub(r"^\s*>\s?", "", b) for b in block)
                out.append(f"<blockquote>{Renderer(self.ctx).render(inner)}</blockquote>")
                continue

            # lists
            if re.match(r"[-*+]\s+", stripped) or re.match(r"\d+[.)]\s+", stripped):
                block, i = self._take_while(
                    lines, i,
                    lambda s: bool(s.strip()) and (
                        re.match(r"\s*([-*+]|\d+[.)])\s+", s) or s.startswith(("  ", "\t"))))
                out.append(self._list(block))
                continue

            # raw html block
            if stripped.startswith("<") and re.match(
                    r"<\s*/?\s*(" + "|".join(_BLOCK_TAGS) + r")\b", stripped, re.I):
                block, i = self._take_while(lines, i, lambda s: bool(s.strip()))
                out.append("\n".join(block))
                continue

            # paragraph
            block, i = self._take_while(
                lines, i,
                lambda s: bool(s.strip()) and not s.strip().startswith((":::", "```", "#", ">"))
                and not re.match(r"\s*([-*+]|\d+[.)])\s+", s))
            out.append(f"<p>{inline(' '.join(b.strip() for b in block))}</p>")
        return "\n".join(out)

    @staticmethod
    def _collect(lines, start, is_end):
        body = []
        i = start
        while i < len(lines) and not is_end(lines[i]):
            body.append(lines[i])
            i += 1
        return body, i + 1

    @staticmethod
    def _take_while(lines, start, pred):
        block = []
        i = start
        while i < len(lines) and pred(lines[i]):
            block.append(lines[i])
            i += 1
        return block, i

    @staticmethod
    def _cells(row: str) -> list[str]:
        row = row.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return [c.strip() for c in row.split("|")]

    def _table(self, block: list[str]) -> str:
        head = self._cells(block[0])
        aligns = []
        for spec in self._cells(block[1]):
            if spec.startswith(":") and spec.endswith(":"):
                aligns.append("center")
            elif spec.endswith(":"):
                aligns.append("right")
            else:
                aligns.append("left")
        rows = [self._cells(r) for r in block[2:]]
        th = "".join(
            f'<th style="text-align:{aligns[i] if i < len(aligns) else "left"}">{inline(c)}</th>'
            for i, c in enumerate(head))
        body = []
        for r in rows:
            tds = "".join(
                f'<td style="text-align:{aligns[i] if i < len(aligns) else "left"}">{inline(c)}</td>'
                for i, c in enumerate(r))
            body.append(f"<tr>{tds}</tr>")
        return ('<div class="table-wrap"><table><thead><tr>' + th + "</tr></thead><tbody>"
                + "".join(body) + "</tbody></table></div>")

    def _list(self, block: list[str]) -> str:
        ordered = bool(re.match(r"\s*\d+[.)]\s+", block[0]))
        items: list[list[str]] = []
        for line in block:
            m = re.match(r"\s*([-*+]|\d+[.)])\s+(.*)", line)
            if m and not line.startswith(("    ", "\t")):
                items.append([m.group(2)])
            elif items:
                items[-1].append(line.strip())
            else:
                items.append([line.strip()])
        tag = "ol" if ordered else "ul"
        lis = "".join(f"<li>{inline(' '.join(it))}</li>" for it in items)
        return f"<{tag}>{lis}</{tag}>"

    # -- directives ---------------------------------------------------------

    def directive(self, head: str, body: list[str]) -> str:
        parts = head.split(None, 1)
        name = parts[0].lower() if parts else ""
        attrs = parse_attrs(parts[1] if len(parts) > 1 else "")
        text = "\n".join(body)
        fn = getattr(self, f"d_{name}", None)
        if fn is None:
            warn(f"{self.ctx.src}: unknown directive ':::{name}'")
            return f'<div class="callout warn"><p>unknown directive <code>:::{name}</code></p></div>'
        return fn(attrs, text)

    def d_note(self, a, text):
        return self._callout("note", a.get("title", "Note"), text)

    def d_warn(self, a, text):
        return self._callout("warn", a.get("title", "Watch out"), text)

    def d_key(self, a, text):
        return self._callout("key", a.get("title", "What we observed"), text)

    def d_method(self, a, text):
        return self._callout("method", a.get("title", "How it was done"), text)

    def d_todo(self, a, text):
        TODOS.append(f"{self.ctx.src}: {a.get('title', 'unwritten')}")
        return self._callout("todo", a.get("title", "To write"), text)

    def _callout(self, kind, title, text):
        inner = Renderer(self.ctx).render(text)
        return (f'<aside class="callout {kind}"><div class="callout-title">{inline(title)}</div>'
                f'<div class="callout-body">{inner}</div></aside>')

    def d_figure(self, a, text):
        src = a.get("src", "")
        if src and not re.match(r"https?://|/", src):
            resolved = self.ctx.static_asset(src)
            if resolved:
                src = resolved
        cap = inline(text.strip()) if text.strip() else ""
        w = f' style="max-width:{a["width"]}"' if a.get("width") else ""
        return (f'<figure class="figure"{w}><img src="{src}" alt="{a.get("alt", cap and "figure" or "")}" '
                f'loading="lazy">' + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")

    def d_diagram(self, a, text):
        """A diagram slot that is allowed to be empty.

        Drop ``diagram.png`` next to the page's .md (or at the root of the
        experiment folder) and it appears here. Until then the slot renders a
        placeholder naming the exact path to drop the file at, so the page keeps
        its shape in a presentation and nobody has to remember where it goes."""
        name = a.get("src", "diagram.png")
        found = self.ctx.static_asset(name, quiet=True)
        cap = inline(text.strip()) if text.strip() else ""
        w = a.get("width", "760px")
        if found:
            return (f'<figure class="figure diagram" style="max-width:{w}">'
                    f'<img src="{found}" alt="{a.get("alt", "experiment diagram")}" loading="lazy">'
                    + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")
        # Show the drop location relative to the repo, not an absolute path.
        where = []
        for base in self.ctx.search_dirs():
            try:
                where.append((base / name).resolve().relative_to(ROOT.parent).as_posix())
            except ValueError:
                where.append((base / name).as_posix())
        return (f'<figure class="diagram-slot" style="max-width:{w}">'
                f'<div class="ds-box"><div class="ds-icon" aria-hidden="true">'
                f'<svg viewBox="0 0 48 34" width="46" height="33">'
                f'<rect x="1.6" y="1.6" width="18" height="12" rx="2.4" fill="none" '
                f'stroke="currentColor" stroke-width="1.6"/>'
                f'<rect x="28.4" y="20.4" width="18" height="12" rx="2.4" fill="none" '
                f'stroke="currentColor" stroke-width="1.6"/>'
                f'<path d="M19.6 7.6h6a3 3 0 0 1 3 3v12.8" fill="none" stroke="currentColor" '
                f'stroke-width="1.6" stroke-linecap="round"/>'
                f'<path d="M25.6 23.4l2.8 3 2.8-3" fill="none" stroke="currentColor" '
                f'stroke-width="1.6" stroke-linejoin="round"/></svg></div>'
                f'<div class="ds-t">Diagram slot &mdash; empty</div>'
                f'<div class="ds-s">Save a pipeline diagram as <code>{name}</code> at either of '
                f'these paths and it appears here on the next build:</div>'
                f'<ul class="ds-p">' + "".join(f"<li><code>{x}</code></li>" for x in where) + "</ul>"
                f'</div>' + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")

    def d_stats(self, a, text):
        cells = []
        for line in text.splitlines():
            if ":" not in line:
                continue
            val, _, label = line.partition(":")
            cells.append(f'<div class="stat"><div class="stat-v">{inline(val.strip())}</div>'
                         f'<div class="stat-l">{inline(label.strip())}</div></div>')
        return f'<div class="stats">{"".join(cells)}</div>'

    def d_metrics(self, a, text):
        exp = self.ctx.exp
        if not exp:
            warn(f"{self.ctx.src}: :::metrics is only available inside an experiment")
            return ""
        src = exp.source_dir / a.get("src", "")
        if not src.is_file():
            warn(f"{self.ctx.src}: :::metrics source not found: {src}")
            return ""
        data = json.loads(src.read_text(encoding="utf-8"))
        rows = data.get(a.get("key", "entries"), data if isinstance(data, list) else [])
        for f in [x for x in a.get("where", "").split(",") if x.strip()]:
            k, _, v = f.partition("=")
            rows = [r for r in rows if str(r.get(k.strip(), "")) == v.strip()]
        if a.get("sort"):
            key = a["sort"].lstrip("-")
            rows = sorted(rows, key=lambda r: (r.get(key) is None, r.get(key)),
                          reverse=a["sort"].startswith("-"))
        if a.get("limit"):
            rows = rows[: int(a["limit"])]
        specs = [c.strip() for c in a.get("cols", "").split(",") if c.strip()]
        if not specs:
            specs = list(rows[0].keys()) if rows else []
        fields, labels = [], []
        for s in specs:
            f, _, lab = s.partition(":")
            fields.append(f.strip())
            labels.append(lab.strip() or f.strip())
        th = "".join(f"<th>{inline(l)}</th>" for l in labels)
        body = []
        for r in rows:
            tds = []
            for f in fields:
                v = r.get(f, "")
                num = isinstance(v, (int, float)) and not isinstance(v, bool)
                tds.append(f'<td class="{"num" if num else ""}">{v if v is not None else ""}</td>')
            body.append(f"<tr>{''.join(tds)}</tr>")
        cap = inline(text.strip())
        return ('<figure class="metrics"><div class="table-wrap"><table><thead><tr>' + th
                + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>"
                + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")

    def d_clips(self, a, text):
        exp = self.ctx.exp
        if not exp:
            warn(f"{self.ctx.src}: :::clips is only available inside an experiment")
            return ""
        arms = [s.strip() for s in a.get("arms", "").split(",") if s.strip()]
        if not arms:
            warn(f"{self.ctx.src}: :::clips needs arms=")
            return ""
        ids = [s.strip() for s in a.get("ids", "").split(",") if s.strip()]
        seeds = [s.strip() for s in a.get("seeds", "").split(",") if s.strip()] or exp.default_seeds
        heads = a.get("heads", "on") != "off"
        size = a.get("size", "md")
        self.ctx.seeds.update(seeds)
        self.ctx.has_clips = True

        cols = len(arms)
        rowheads = bool(ids)
        grid = [f'<div class="clips-grid size-{size}'
                f'{" no-rowhead" if not rowheads else ""}" style="--cols:{cols}">']
        if heads:
            if rowheads:
                grid.append('<div class="ch corner"></div>')
            for arm in arms:
                lab = exp.sets.get(arm, {}).get("label", arm)
                sub = exp.sets.get(arm, {}).get("sublabel", "")
                grid.append(f'<div class="ch"><span class="ch-t">{inline(lab)}</span>'
                            + (f'<span class="ch-s">{inline(sub)}</span>' if sub else "") + "</div>")
        for item_id in (ids or [None]):
            if rowheads:
                grid.append(self._rowhead(exp, item_id))
            for arm in arms:
                grid.append(self._cell(exp, arm, item_id, seeds))
        grid.append("</div>")
        cap = inline(text.strip())
        # width= caps the figure: a tall composite (many stacked rows) is
        # unreadable if it is allowed to fill the full content column.
        style = f' style="max-width:{a["width"]}"' if a.get("width") else ""
        return (f'<figure class="clips" data-clips{style}>' + "".join(grid)
                + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")

    def _rowhead(self, exp, item_id):
        it = exp.items.get(item_id, {})
        bits = [f'<div class="rh-t">{inline(it.get("text", item_id))}</div>',
                f'<div class="rh-id">{item_id}</div>']
        for chip in exp.chips_for(item_id):
            bits.append(f'<span class="chip chip-{chip[0]}">{chip[1]}</span>')
        for k, v in (it.get("meta") or {}).items():
            bits.append(f'<div class="rh-m"><span>{k}</span> {v}</div>')
        return f'<div class="rh">{"".join(bits)}</div>'

    def _cell(self, exp, arm, item_id, seeds):
        spec = exp.sets.get(arm)
        if spec is None:
            warn(f"{self.ctx.src}: unknown arm '{arm}' (not in exp.json media.sets)")
            return '<div class="cc"><div class="missing">unknown arm</div></div>'
        clips = []
        for seed in seeds:
            src = exp.resolve(arm, item_id, seed)
            if src is None or not src.is_file():
                warn(f"{self.ctx.src}: missing media {arm}/{item_id}/s{seed} -> {src}")
                clips.append(f'<div class="clip miss" data-seed="{seed}">'
                             f'<div class="missing">no file<br><small>seed {seed}</small></div></div>')
                continue
            asset = MEDIA.request(src, exp, kind=spec.get("kind", "video"),
                                  max_width=spec.get("max_width"))
            label = f'{exp.sets[arm].get("label", arm)} · {item_id or ""} · seed {seed}'.strip(" ·")
            clips.append(self._clip_html(asset, seed, label))
        return f'<div class="cc">{"".join(clips)}</div>'

    def _clip_html(self, asset: "Asset", seed, label):
        rel = self.ctx.rel
        ar = f"{asset.w}/{asset.h}" if asset.w and asset.h else "16/9"
        if asset.kind == "image":
            # data-img (not data-src) so the lightbox knows to show a still and
            # hide the transport controls. Strips are 2000px+ tall composites and
            # are unreadable at grid size, so opening them full-size matters.
            return (f'<div class="clip is-img" data-seed="{seed}" style="--ar:{ar}" '
                    f'data-label="{label}" data-img="{rel}{asset.url}">'
                    f'<img src="{rel}{asset.url}" alt="{label}" loading="lazy">'
                    f'<span class="sd">s{seed}</span>'
                    f'<button class="zoom" type="button" aria-label="expand image">⤢</button></div>')
        return (f'<div class="clip" data-seed="{seed}" style="--ar:{ar}" '
                f'data-label="{label}" data-src="{rel}{asset.url}">'
                f'<video muted loop playsinline preload="none" '
                f'poster="{rel}{asset.poster}" data-src="{rel}{asset.url}"></video>'
                f'<span class="sd">s{seed}</span>'
                f'<button class="zoom" type="button" aria-label="expand clip">⤢</button></div>')


# An unquoted value runs to the next ` key=` or to end of line, NOT to the next
# space. Without that, `cols=a:Joint error mm,b:Jerk` silently truncated the first
# label at the space and dropped every column after it -- a wrong table, with no
# warning. Quoting still works and is clearer for values containing ` key=`.
_ATTR_RE = re.compile(r"""([\w-]+)=(?:"([^"]*)"|'([^']*)'|(.+?))(?=\s+[\w-]+=|$)""")


def parse_attrs(s: str) -> dict:
    out = {}
    for m in _ATTR_RE.finditer(s.strip()):
        dq, sq, bare = m.group(2), m.group(3), m.group(4)
        v = dq if dq is not None else sq if sq is not None else (bare or "").strip()
        out[m.group(1)] = v
    return out


# ---------------------------------------------------------------------------
# media pipeline
# ---------------------------------------------------------------------------

class Asset:
    __slots__ = ("url", "poster", "w", "h", "dur", "kind", "src", "out", "max_width")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


class MediaPipeline:
    def __init__(self):
        self.cfg = {}
        self.requests: dict[Path, Asset] = {}
        self.cache: dict = {}
        self.cache_file = ROOT / ".build-cache.json"
        self.made = 0
        self.reused = 0

    def configure(self, cfg: dict):
        self.cfg = cfg
        if self.cache_file.is_file():
            try:
                self.cache = json.loads(self.cache_file.read_text(encoding="utf-8"))
            except Exception:
                self.cache = {}

    def request(self, src: Path, exp: "Experiment", kind: str = "video",
                max_width: int | None = None) -> Asset:
        src = src.resolve()
        if src in self.requests:
            return self.requests[src]
        rel = src.relative_to(exp.source_dir.resolve())
        ext = ".jpg" if kind == "image" else ".mp4"
        out = OUT / "media" / exp.id / rel.with_suffix(ext)
        url = f"media/{exp.id}/{rel.with_suffix(ext).as_posix()}"
        poster = "" if kind == "image" else f"media/{exp.id}/{rel.with_suffix('.poster.jpg').as_posix()}"
        c = self.cache.get(str(src), {})
        a = Asset(url=url, poster=poster, w=c.get("w"), h=c.get("h"), dur=c.get("dur"),
                  kind=kind, src=src, out=out, max_width=max_width)
        self.requests[src] = a
        return a

    def _sig(self, src: Path, a: Asset) -> str:
        st = src.stat()
        key = json.dumps([st.st_mtime_ns, st.st_size, self.cfg, a.max_width], sort_keys=True)
        return hashlib.sha1(key.encode()).hexdigest()[:16]

    def _width(self, a: Asset) -> int:
        """Per-set override wins; composites need more pixels than single clips."""
        if a.max_width:
            return int(a.max_width)
        return self.cfg.get("image_max_width" if a.kind == "image" else "video_max_width", 720)

    def run(self, skip: bool = False) -> None:
        if not self.requests:
            return
        todo = []
        for src, a in self.requests.items():
            sig = self._sig(src, a)
            c = self.cache.get(str(src))
            fresh = (c and c.get("sig") == sig and (OUT / a.url).is_file()
                     and (not a.poster or (OUT / a.poster).is_file()))
            if fresh:
                a.w, a.h, a.dur = c.get("w"), c.get("h"), c.get("dur")
                self.reused += 1
            else:
                todo.append((src, a, sig))
        if skip:
            for src, a, _ in todo:
                if not (OUT / a.url).is_file():
                    warn(f"--no-media: {a.url} has never been built; page will show a broken clip")
                a.w = a.w or 16
                a.h = a.h or 9
            print(f"  media: {self.reused} cached, {len(todo)} skipped (--no-media)")
            return
        if not todo:
            print(f"  media: {self.reused} cached, nothing to transcode")
            return
        print(f"  media: {self.reused} cached, transcoding {len(todo)} ...")
        workers = max(2, min(8, (os.cpu_count() or 4) - 1))
        t0 = time.time()
        done = [0]

        def work(job):
            src, a, sig = job
            try:
                info = self._transcode(src, a)
                info["sig"] = sig
                self.cache[str(src)] = info
                a.w, a.h, a.dur = info.get("w"), info.get("h"), info.get("dur")
            except Exception as e:  # noqa: BLE001 - keep building, report at the end
                warn(f"transcode failed for {src.name}: {e}")
                a.w, a.h = 16, 9
            done[0] += 1
            if done[0] % 10 == 0 or done[0] == len(todo):
                print(f"    {done[0]}/{len(todo)}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, todo))
        self.made = len(todo)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(json.dumps(self.cache, indent=0), encoding="utf-8")
        print(f"  media: done in {time.time() - t0:.0f}s")

    def _probe(self, src: Path) -> dict:
        cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height:format=duration", "-of", "json", str(src)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            st = (d.get("streams") or [{}])[0]
            dur = float((d.get("format") or {}).get("duration") or 0) or None
            return {"w": st.get("width"), "h": st.get("height"), "dur": dur}
        except Exception:
            return {"w": None, "h": None, "dur": None}

    def _transcode(self, src: Path, a: Asset) -> dict:
        info = self._probe(src)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        mw = self._width(a)
        if a.kind == "image":
            run_ff(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                    "-vf", f"scale='min({mw},iw)':-2:flags=lanczos",
                    "-q:v", str(self.cfg.get("image_quality", 4)), str(a.out)])
        else:
            run_ff(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-an", "-sn", "-dn",
                    "-vf", f"scale='min({mw},iw)':-2:flags=lanczos",
                    "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-crf", str(self.cfg.get("video_crf", 28)),
                    "-preset", self.cfg.get("video_preset", "medium"),
                    "-movflags", "+faststart", str(a.out)])
            # poster from ~40% in: more representative of the action than frame 0
            at = round((info.get("dur") or 2.0) * 0.4, 2)
            pout = OUT / a.poster
            pout.parent.mkdir(parents=True, exist_ok=True)
            base = ["ffmpeg", "-y", "-v", "error"]
            vf = f"scale='min({mw},iw)':-2:flags=lanczos"
            try:
                run_ff(base + ["-ss", str(at), "-i", str(a.out), "-frames:v", "1",
                               "-vf", vf, "-q:v", "5", str(pout)])
            except Exception:
                run_ff(base + ["-i", str(a.out), "-frames:v", "1", "-vf", vf,
                               "-q:v", "5", str(pout)])
        out_info = self._probe(a.out)
        return {"w": out_info.get("w") or info.get("w"),
                "h": out_info.get("h") or info.get("h"),
                "dur": info.get("dur")}


def run_ff(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or "").strip().splitlines()[-1] if r.stderr else "ffmpeg failed")


MEDIA = MediaPipeline()


# ---------------------------------------------------------------------------
# model
# ---------------------------------------------------------------------------

class Experiment:
    def __init__(self, d: Path, site: dict):
        self.dir = d
        self.id = d.name
        cfg = json.loads((d / "exp.json").read_text(encoding="utf-8"))
        self.cfg = cfg
        self.title = cfg.get("title", self.id)
        self.nav = cfg.get("nav", self.id)
        self.question = cfg.get("question", "")
        self.status = cfg.get("status", "")
        self.date = cfg.get("date", "")
        self.tags = cfg.get("tags", [])
        raw = cfg.get("source_dir", "")
        self.source_dir = (ROOT / raw) if raw else d
        if raw and not self.source_dir.is_dir():
            warn(f"{self.id}: source_dir not found: {self.source_dir}")
        media = cfg.get("media", {})
        self.sets: dict = media.get("sets", {})
        self.default_seeds = [str(s) for s in media.get("default_seeds", ["0"])]
        self.all_seeds = [str(s) for s in media.get("seeds", self.default_seeds)]
        self.items: dict = {}
        self._load_items(media)
        self.pages: list[Page] = []

    def _load_items(self, media: dict):
        """Items are the rows of a clip grid. Either inline, or pulled from a JSON file."""
        inline_items = media.get("items")
        if isinstance(inline_items, dict):
            self.items = inline_items
            return
        src = media.get("items_from")
        if not src:
            return
        p = self.source_dir / src.get("path", "")
        if not p.is_file():
            warn(f"{self.id}: items_from path not found: {p}")
            return
        data = json.loads(p.read_text(encoding="utf-8"))
        for k in (src.get("key") or "").split("."):
            if k:
                data = data.get(k, []) if isinstance(data, dict) else data
        idf = src.get("id_field", "id")
        for row in data or []:
            if isinstance(row, dict) and row.get(idf):
                self.items[str(row[idf])] = row

    def chips_for(self, item_id) -> list[tuple[str, str]]:
        it = self.items.get(item_id, {})
        out = []
        for spec in self.cfg.get("media", {}).get("chips", []):
            f = spec.get("field")
            val = it.get(f)
            if val in (None, "", "none") and not spec.get("show_empty"):
                continue
            label = (spec.get("labels") or {}).get(str(val), f"{val}")
            out.append((slugify(str(val)) or "x", label))
        return out

    def resolve(self, arm: str, item_id, seed) -> Path | None:
        spec = self.sets.get(arm)
        if not spec:
            return None
        try:
            name = spec["pattern"].format(id=item_id or "", seed=seed)
        except Exception:
            return None
        return self.source_dir / spec.get("dir", "") / name


class Page:
    def __init__(self, src: Path, exp: Experiment | None, site: dict):
        self.src = src
        self.exp = exp
        raw = src.read_text(encoding="utf-8")
        self.meta, self.body = split_front_matter(raw)
        stem = src.stem
        m = re.match(r"(\d+)[-_](.*)", stem)
        self.order = int(m.group(1)) if m else 999
        self.slug = (m.group(2) if m else stem)
        if src.name in ("index.md",):
            self.slug = "index"
            self.order = -1
        self.title = self.meta.get("title") or self.slug.replace("-", " ").title()
        self.nav = self.meta.get("nav") or self.title
        self.lead = self.meta.get("lead") or ""
        self.out_rel = (f"{exp.id}/{self.slug}.html" if exp else
                        ("index.html" if self.slug == "index" else f"{self.slug}.html"))
        self.url = self.out_rel
        self.html = ""
        self.headings: list = []


class PageCtx:
    def __init__(self, page: Page, rel: str):
        self.page = page
        self.src = page.src.relative_to(ROOT).as_posix()
        self.exp = page.exp
        self.rel = rel
        self.seeds: set[str] = set()
        self.has_clips = False

    def search_dirs(self) -> list[Path]:
        """Where a page-local asset may live: next to the .md, then the experiment."""
        return [self.page.src.parent] + ([self.exp.source_dir] if self.exp else [])

    def static_asset(self, src: str, quiet: bool = False) -> str | None:
        """Copy a file that sits next to the .md (or in the experiment) into docs/.

        ``quiet`` suppresses the warning, for slots that are *allowed* to be
        empty and render a placeholder instead (see :::diagram)."""
        for base in self.search_dirs():
            p = (base / src)
            if p.is_file():
                sub = f"static/{self.exp.id if self.exp else 'site'}/{p.name}"
                dst = OUT / sub
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dst)
                STATIC_USED.add(sub)
                return f"{self.rel}{sub}"
        if not quiet:
            warn(f"{self.src}: figure src not found: {src}")
        return None


# ---------------------------------------------------------------------------
# chrome
# ---------------------------------------------------------------------------

def sidebar_html(site, exps, current: Page | None, rel: str) -> str:
    home_on = current is not None and current.exp is None and current.slug == "index"
    out = [f'<a class="side-home{" on" if home_on else ""}" href="{rel}index.html">'
           f'<span class="sh-t">{site.get("title", "Experiments")}</span>'
           f'<span class="sh-s">{site.get("subtitle", "")}</span></a>',
           '<div class="side-filter"><input type="search" id="navfilter" '
           'placeholder="Filter pages…" autocomplete="off" spellcheck="false"></div>',
           '<nav class="side-nav" aria-label="Experiments">']
    for e in exps:
        active = current is not None and current.exp is e
        out.append(f'<div class="exp{" open" if active else ""}" data-exp>')
        out.append(f'<button class="exp-h" type="button" aria-expanded="{str(active).lower()}">'
                   f'<span class="exp-c">{e.nav}</span>'
                   f'<span class="exp-t">{e.title}</span>'
                   f'<svg class="caret" viewBox="0 0 10 6" aria-hidden="true">'
                   f'<path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
                   f"</button>")
        out.append('<ul class="exp-pages">')
        for p in e.pages:
            on = " on" if current is p else ""
            out.append(f'<li><a class="{on.strip()}" href="{rel}{p.url}">'
                       f'<span class="pn">{p.nav}</span></a></li>')
        out.append("</ul></div>")
    out.append("</nav>")
    extra = site.get("links", [])
    if extra:
        out.append('<div class="side-links">')
        for l in extra:
            out.append(f'<a href="{l["href"]}" target="_blank" rel="noopener">{l["label"]} ↗</a>')
        out.append("</div>")
    return "\n".join(out)


def toolbar_html(seeds: list[str]) -> str:
    if not seeds:
        return ""
    btns = "".join(f'<button type="button" data-seed="{s}">{s}</button>' for s in seeds)
    allb = '<button type="button" data-seed="all">all</button>' if len(seeds) > 1 else ""
    return f"""<div class="toolbar" data-toolbar>
  <div class="tb-g"><span class="tb-l">seed</span><div class="seg">{btns}{allb}</div></div>
  <div class="tb-g"><span class="tb-l">speed</span><div class="seg">
    <button type="button" data-rate="0.25">&frac14;&times;</button>
    <button type="button" data-rate="0.5">&frac12;&times;</button>
    <button type="button" data-rate="1">1&times;</button>
    <button type="button" data-rate="2">2&times;</button></div></div>
  <div class="tb-g"><button type="button" class="btn" data-autosync aria-pressed="true">Sync: on</button>
    <button type="button" class="btn" data-sync>&#9654; Restart now</button>
    <button type="button" class="btn" data-toggleplay>Pause all</button></div>
  <div class="tb-hint">Click any clip to open it frame-by-frame</div>
</div>"""


def pagenav_html(page: Page, flat: list[Page], rel: str) -> str:
    try:
        i = flat.index(page)
    except ValueError:
        return ""
    prev = flat[i - 1] if i > 0 else None
    nxt = flat[i + 1] if i + 1 < len(flat) else None
    bits = []
    if prev:
        bits.append(f'<a class="pg prev" href="{rel}{prev.url}"><span>Previous</span>'
                    f'<strong>{prev.nav}</strong></a>')
    else:
        bits.append('<span class="pg"></span>')
    if nxt:
        bits.append(f'<a class="pg next" href="{rel}{nxt.url}"><span>Next</span>'
                    f'<strong>{nxt.nav}</strong></a>')
    else:
        bits.append('<span class="pg"></span>')
    return f'<nav class="pagenav">{"".join(bits)}</nav>'


def status_chip(status: str) -> str:
    if not status:
        return ""
    return f'<span class="status s-{slugify(status)}">{status}</span>'


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

def build(args) -> int:
    site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    MEDIA.configure(site.get("media", {}))

    if args.clean and OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    order = site.get("experiments")
    dirs = sorted([d for d in CONTENT.iterdir() if d.is_dir() and (d / "exp.json").is_file()],
                  key=lambda d: (order.index(d.name) if order and d.name in order else 999, d.name))
    if order:
        for name in order:
            if not (CONTENT / name / "exp.json").is_file():
                warn(f"site.json lists '{name}' but content/{name}/exp.json is missing")

    exps = [Experiment(d, site) for d in dirs]
    for e in exps:
        pages = sorted([p for p in e.dir.glob("*.md")], key=lambda p: p.name)
        e.pages = sorted([Page(p, e, site) for p in pages], key=lambda p: (p.order, p.slug))
        if not e.pages:
            warn(f"{e.id}: no .md pages found")

    home_src = CONTENT / "index.md"
    home = Page(home_src, None, site) if home_src.is_file() else None
    loose = [Page(p, None, site) for p in sorted(CONTENT.glob("*.md")) if p.name != "index.md"]

    flat = [p for e in exps for p in e.pages]
    all_pages = ([home] if home else []) + loose + flat

    # pass 1: render markdown (this also registers every media file we need)
    print("building pages ...")
    for p in all_pages:
        rel = "../" * (len(Path(p.out_rel).parts) - 1)
        ctx = PageCtx(p, rel)
        r = Renderer(ctx)
        p.html = r.render(p.body)
        p.headings = r.headings
        p.ctx = ctx
        p.rel = rel

    MEDIA.run(skip=args.no_media)

    # pass 2: media dimensions are known now, so patch aspect ratios and emit
    template = (THEME / "base.html").read_text(encoding="utf-8")
    for p in all_pages:
        p.html = patch_ratios(p.html)

    for p in all_pages:
        write_page(p, template, site, exps, flat)

    if home:
        pass
    else:
        warn("content/index.md is missing; the site has no home page")

    # theme assets + Pages housekeeping
    dst = OUT / "assets"
    dst.mkdir(parents=True, exist_ok=True)
    for f in (THEME / "assets").iterdir():
        if f.is_file():
            shutil.copy2(f, dst / f.name)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    write_404(template, site, exps, flat)
    write_search_index(all_pages, exps)
    prune(all_pages, STATIC_USED)
    check_links()

    # report
    n_media = len(MEDIA.requests)
    size = sum(f.stat().st_size for f in (OUT / "media").rglob("*") if f.is_file()) if (OUT / "media").exists() else 0
    print(f"\n  {len(all_pages)} pages, {len(exps)} experiments, {n_media} media files")
    print(f"  docs/media is {size / 1e6:.1f} MB")
    if TODOS:
        print(f"\n  {len(TODOS)} unwritten section(s) marked :::todo")
        for t in TODOS[:12]:
            print(f"    - {t}")
        if len(TODOS) > 12:
            print(f"    ... and {len(TODOS) - 12} more")
    if WARNINGS:
        print(f"\n  {len(WARNINGS)} warning(s):")
        seen = set()
        for w in WARNINGS:
            if w in seen:
                continue
            seen.add(w)
            print(f"    ! {w}")
    print(f"\n  output: {OUT}")
    return 0


_AR_RE = re.compile(r'--ar:16/9;?" data-label="[^"]*" data-src="([^"]+)"')


def patch_ratios(html_text: str) -> str:
    """Fill in real aspect ratios now that ffprobe has run."""
    by_url = {}
    for a in MEDIA.requests.values():
        if a.w and a.h:
            by_url[a.url] = f"{a.w}/{a.h}"

    def fix(m):
        url = m.group(2)
        key = url.split("media/", 1)[-1]
        for u, ar in by_url.items():
            if u.endswith(key):
                return m.group(0).replace("--ar:16/9", f"--ar:{ar}")
        return m.group(0)

    return re.sub(r'--ar:16/9(.*?)(?:data-src|src)="([^"]+)"', fix, html_text)


def prune(all_pages, static_used: set[str]) -> int:
    """Delete output that no longer corresponds to anything in content/.

    Renaming or splitting a page leaves its old .html behind, and a stale page is
    worse than a missing one: it stays reachable, stays in search results, and
    shows content that has since been rewritten elsewhere. Same for media whose
    experiment or set has gone away, which otherwise just accumulates in the repo.
    """
    keep = {(OUT / p.out_rel).resolve() for p in all_pages}
    keep.add((OUT / "404.html").resolve())
    for a in MEDIA.requests.values():
        keep.add((OUT / a.url).resolve())
        if a.poster:
            keep.add((OUT / a.poster).resolve())
    keep |= {(OUT / rel).resolve() for rel in static_used}
    for f in (THEME / "assets").iterdir():
        if f.is_file():
            keep.add((OUT / "assets" / f.name).resolve())
    for name in (".nojekyll", "search.json"):
        keep.add((OUT / name).resolve())

    removed = []
    for sub in ("", "media", "static"):
        base = OUT / sub if sub else OUT
        if not base.is_dir():
            continue
        pattern = "**/*" if sub else "**/*.html"
        for f in base.glob(pattern):
            if f.is_file() and f.resolve() not in keep:
                f.unlink()
                removed.append(f.relative_to(OUT).as_posix())
    # also drop directories left empty by the above
    for d in sorted((q for q in OUT.rglob("*") if q.is_dir()),
                    key=lambda q: len(q.parts), reverse=True):
        try:
            next(d.iterdir())
        except StopIteration:
            d.rmdir()
    if removed:
        print(f"  pruned {len(removed)} stale file(s)")
        for r in removed[:8]:
            print(f"    - {r}")
        if len(removed) > 8:
            print(f"    ... and {len(removed) - 8} more")
    return len(removed)


def write_page(p: Page, template: str, site, exps, flat) -> None:
    rel = p.rel
    exp = p.exp
    crumbs = [f'<a href="{rel}index.html">{site.get("short_title", "Home")}</a>']
    if exp:
        crumbs.append(f'<a href="{rel}{exp.pages[0].url}">{exp.nav}</a>')
    crumbs.append(f"<span>{p.nav}</span>")

    head_bits = []
    if exp:
        head_bits.append(f'<div class="ph-kicker">{exp.nav} · {exp.title}</div>')
    head_bits.append(f"<h1>{inline(p.title)}</h1>")
    if p.lead:
        head_bits.append(f'<p class="lead">{inline(p.lead)}</p>')
    if exp and p is exp.pages[0]:
        chips = [status_chip(exp.status)]
        if exp.date:
            chips.append(f'<span class="meta-chip">{exp.date}</span>')
        for t in exp.tags:
            chips.append(f'<span class="meta-chip tag">{t}</span>')
        head_bits.append(f'<div class="ph-meta">{"".join(c for c in chips if c)}</div>')

    seeds = sorted(p.ctx.seeds, key=lambda s: (len(s), s))
    body = template
    subs = {
        "REL": rel,
        "LANG": site.get("lang", "en"),
        "TITLE": f"{p.title} · {site.get('short_title', site.get('title', ''))}",
        "DESC": (p.lead or site.get("description", "")).replace('"', "&quot;"),
        "SIDEBAR": sidebar_html(site, exps, p, rel),
        "BREADCRUMB": '<span class="sep">/</span>'.join(crumbs),
        "PAGEHEAD": "".join(b for b in head_bits if b),
        "TOOLBAR": toolbar_html(seeds if p.ctx.has_clips else []),
        "CONTENT": p.html,
        "PAGENAV": pagenav_html(p, flat, rel) if exp else "",
        "FOOTER": site.get("footer", ""),
    }
    for k, v in subs.items():
        body = body.replace(f"{{{{{k}}}}}", v or "")
    dst = OUT / p.out_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(body, encoding="utf-8")


def write_404(template, site, exps, flat) -> None:
    body = template
    subs = {
        "REL": "", "LANG": site.get("lang", "en"),
        "TITLE": f"Not found · {site.get('short_title', '')}", "DESC": "",
        "SIDEBAR": sidebar_html(site, exps, None, ""),
        "BREADCRUMB": '<span>404</span>',
        "PAGEHEAD": '<h1>Page not found</h1><p class="lead">That page moved or never existed.</p>',
        "TOOLBAR": "",
        "CONTENT": '<p><a href="index.html">Back to the experiment index</a>.</p>',
        "PAGENAV": "", "FOOTER": site.get("footer", ""),
    }
    for k, v in subs.items():
        body = body.replace(f"{{{{{k}}}}}", v or "")
    (OUT / "404.html").write_text(body, encoding="utf-8")


def check_links() -> None:
    """Every internal href/src in the emitted site must resolve to a real file,
    and every #anchor must exist on its page. Cheap, and catches page renames."""
    pages = list(OUT.rglob("*.html"))
    for html in pages:
        text = html.read_text(encoding="utf-8")
        ids = set(re.findall(r'id="([^"]+)"', text))
        here = html.relative_to(OUT).as_posix()
        for ref in re.findall(r'(?:href|src|poster|data-src)="([^"]+)"', text):
            if ref.startswith(("http://", "https://", "mailto:", "data:", "//")):
                continue
            if ref.startswith("#"):
                if ref[1:] not in ids:
                    warn(f"{here}: link to missing anchor {ref}")
                continue
            path, _, frag = ref.partition("#")
            if not path:
                continue
            target = (html.parent / path).resolve()
            if not target.exists():
                warn(f"{here}: broken link -> {ref}")
            elif frag and target.suffix == ".html":
                tids = set(re.findall(r'id="([^"]+)"',
                                      target.read_text(encoding="utf-8")))
                if frag not in tids:
                    warn(f"{here}: link to missing anchor {ref}")


def write_search_index(pages, exps) -> None:
    idx = []
    for p in pages:
        text = re.sub(r"<[^>]+>", " ", p.html)
        text = re.sub(r"\s+", " ", text).strip()
        idx.append({"t": p.title, "u": p.url, "e": p.exp.nav if p.exp else "",
                    "s": text[:400]})
    (OUT / "search.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")


def serve() -> None:
    import http.server
    import socketserver
    os.chdir(OUT)
    handler = http.server.SimpleHTTPRequestHandler
    handler.extensions_map[".mp4"] = "video/mp4"
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        print("\n  serving http://localhost:8000/   (ctrl-c to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-media", action="store_true",
                    help="skip ffmpeg entirely and reuse whatever is already in docs/media")
    ap.add_argument("--clean", action="store_true", help="delete docs/ before building")
    ap.add_argument("--serve", action="store_true", help="serve docs/ on :8000 after building")
    args = ap.parse_args()
    if not args.no_media and not shutil.which("ffmpeg"):
        print("error: ffmpeg not found on PATH. Install it, or run with --no-media.", file=sys.stderr)
        return 2
    rc = build(args)
    if args.serve:
        serve()
    return rc


if __name__ == "__main__":
    sys.exit(main())

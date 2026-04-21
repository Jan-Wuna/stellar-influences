from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class WikiPage:
    path: Path
    meta: dict
    body: str


def load_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    _, raw, body = text.split("---\n", 2)
    return yaml.safe_load(raw) or {}, body


def load_page(path: Path) -> WikiPage:
    text = path.read_text(encoding="utf-8")
    meta, body = load_frontmatter(text)
    return WikiPage(path=path, meta=meta, body=body)


def iter_wiki_pages(root: Path) -> list[WikiPage]:
    pages: list[WikiPage] = []
    for path in sorted(root.rglob("*.md")):
        if "_templates" in path.parts:
            continue
        pages.append(load_page(path))
    return pages


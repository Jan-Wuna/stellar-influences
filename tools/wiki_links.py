from __future__ import annotations

import os
from pathlib import Path


DERIVED_SYNTHESIS_ANCHOR = "derived-synthesis"


def explicit_anchor(anchor: str) -> str:
    return f'<a id="{anchor}"></a>'


def derived_synthesis_heading() -> str:
    return f"{explicit_anchor(DERIVED_SYNTHESIS_ANCHOR)}\n\n## Derived Synthesis"


def relative_link_target(current_path: Path, target_path: Path, anchor: str | None = None) -> str:
    relative = Path(os.path.relpath(target_path, start=current_path.parent)).as_posix()
    if anchor:
        return f"{relative}#{anchor}"
    return relative

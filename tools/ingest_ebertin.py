from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.ebertin_source import (
    generate_models,
    normalize_activation,
    render_source_page,
    _activation_page_text,
    _axis_page_text,
    _factor_page_text,
    _triad_page_text,
)
from tools.rebuild_index import build_index


UPDATED_AT = "2026-04-21"
SOURCE_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _clear_markdown_files(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for file_path in path.glob("*.md"):
        file_path.unlink()


def main() -> None:
    root = Path.cwd()
    pdf_path = root / "Stellar Influences Vault" / "planetary expressions - Reinhold Ebertin - The Combination Of Stellar Influences.pdf"
    wiki_root = root / "wiki"

    factor_blocks, axis_blocks = generate_models(pdf_path)

    factor_dir = wiki_root / "factors"
    axis_dir = wiki_root / "axes"
    activation_dir = wiki_root / "activations"
    triad_dir = wiki_root / "triads"
    source_dir = wiki_root / "sources"

    for directory in [factor_dir, axis_dir, activation_dir, triad_dir, source_dir]:
        _clear_markdown_files(directory)

    activation_index: dict[str, int] = defaultdict(int)
    triads: dict[tuple[str, str, str], list] = defaultdict(list)
    for axis in axis_blocks:
        for entry in axis.activation_entries:
            identity = normalize_activation(axis.factor_a, axis.factor_b, entry.activated_by)
            activation_index[entry.activated_by] += 1
            activation_index[axis.factor_a] += 1
            activation_index[axis.factor_b] += 1
            triads[identity.triad_set].append((axis, entry))
            _write(activation_dir / f"{identity.slug}.md", _activation_page_text(axis, entry, UPDATED_AT))

    for axis in axis_blocks:
        identity = normalize_activation(axis.factor_a, axis.factor_b, axis.activation_entries[0].activated_by).axis
        _write(axis_dir / f"{identity.slug}.md", _axis_page_text(axis, UPDATED_AT))

    for factor in factor_blocks:
        _write(
            factor_dir / f"{factor.factor.lower()}.md",
            _factor_page_text(factor, axis_blocks, activation_index[factor.factor], UPDATED_AT),
        )

    for triad_set, orientation_entries in triads.items():
        slug = "-".join(name.lower() for name in triad_set)
        _write(triad_dir / f"{slug}.md", _triad_page_text(orientation_entries, UPDATED_AT))

    _write(
        source_dir / f"{SOURCE_SLUG}.md",
        render_source_page(
            factor_blocks,
            axis_blocks,
            triad_count=len(triads),
            activation_count=sum(len(axis.activation_entries) for axis in axis_blocks),
            updated_at=UPDATED_AT,
        ),
    )

    index_path = wiki_root / "index.md"
    index_path.write_text(build_index(wiki_root), encoding="utf-8")


if __name__ == "__main__":
    main()

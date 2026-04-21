from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.wiki_identity import normalize_activation
from tools.wiki_pages import iter_wiki_pages


REQUIRED_FIELDS = {
    "activation": {"title", "page_type", "slug", "axis", "activated_by", "triad_set"},
}


def _check_required_fields(meta: dict) -> list[str]:
    page_type = meta.get("page_type")
    required = REQUIRED_FIELDS.get(page_type, set())
    missing = []
    for field in sorted(required):
        if field not in meta:
            missing.append(f"missing required field '{field}'")
    return missing


def _parse_activation_formula(formula: str):
    left, right = formula.split("=")
    factor_a, factor_b = [part.strip() for part in left.split("/")]
    activated_by = right.strip()
    return normalize_activation(factor_a, factor_b, activated_by)


def _check_activation_aliases(meta: dict) -> list[str]:
    if meta.get("page_type") != "activation":
        return []
    normalized = meta.get("normalized_formula")
    triad = tuple(sorted(meta.get("triad_set", []), key=str.casefold))
    problems: list[str] = []
    for alias in meta.get("aliases", []) or []:
        if "/" not in alias or "=" not in alias:
            continue
        alias_identity = _parse_activation_formula(alias)
        if tuple(sorted(alias_identity.triad_set, key=str.casefold)) == triad and alias != normalized:
            problems.append("aliases must not collapse distinct orientations")
            break
    return problems


def lint_wiki(root: Path) -> list[str]:
    problems: list[str] = []
    for page in iter_wiki_pages(root):
        page_problems = _check_required_fields(page.meta)
        page_problems.extend(_check_activation_aliases(page.meta))
        for problem in page_problems:
            problems.append(f"{page.path}: {problem}")
    return problems


def main() -> None:
    root = Path("wiki")
    problems = lint_wiki(root)
    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    print("Lint passed")


if __name__ == "__main__":
    main()

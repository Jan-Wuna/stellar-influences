from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.wiki_identity import normalize_activation, normalize_axis, normalize_factor, normalize_triad
from tools.wiki_links import DERIVED_SYNTHESIS_ANCHOR, explicit_anchor
from tools.wiki_pages import iter_wiki_pages


REQUIRED_FIELDS = {
    "factor": {
        "title",
        "page_type",
        "slug",
        "status",
        "framework_scope",
        "factors",
        "aliases",
        "source_pages",
        "updated_at",
    },
    "axis": {
        "title",
        "page_type",
        "slug",
        "status",
        "framework_scope",
        "factors",
        "normalized_axis",
        "factor_a",
        "factor_b",
        "related_activations",
        "related_triad_hubs",
        "aliases",
        "source_pages",
        "updated_at",
    },
    "activation": {
        "title",
        "page_type",
        "slug",
        "status",
        "framework_scope",
        "factors",
        "normalized_formula",
        "axis",
        "activated_by",
        "triad_set",
        "aliases",
        "source_pages",
        "updated_at",
    },
    "triad_hub": {
        "title",
        "page_type",
        "slug",
        "status",
        "framework_scope",
        "factors",
        "triad_set",
        "orientations",
        "aliases",
        "source_pages",
        "updated_at",
    },
    "source": {
        "title",
        "page_type",
        "slug",
        "status",
        "framework_scope",
        "factors",
        "aliases",
        "source_pages",
        "updated_at",
    },
    "derived": {
        "title",
        "page_type",
        "slug",
        "status",
        "framework_scope",
        "source_pages",
        "updated_at",
    },
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


def _check_factor_identity(meta: dict) -> list[str]:
    if meta.get("page_type") != "factor":
        return []
    factors = meta.get("factors", []) or []
    if len(factors) != 1:
        return ["factor pages must list exactly one factor"]
    identity = normalize_factor(factors[0])
    problems: list[str] = []
    if normalize_factor(meta.get("title", "")).display != identity.display:
        problems.append("factor title and factors[0] must match canonically")
    if meta.get("title") != identity.display:
        problems.append("factor title must use the canonical factor name")
    if meta.get("slug") != identity.slug:
        problems.append("factor slug must match canonical factor title")
    return problems


def _check_axis_identity(meta: dict) -> list[str]:
    if meta.get("page_type") != "axis":
        return []
    factors = tuple(meta.get("factors", []) or [])
    if len(factors) != 2:
        return ["axis pages must list exactly two factors"]
    identity = normalize_axis(meta.get("factor_a", ""), meta.get("factor_b", ""))
    problems: list[str] = []
    if meta.get("title") != identity.display:
        problems.append("axis title must match canonical normalized axis")
    if meta.get("normalized_axis") != identity.display:
        problems.append("normalized_axis must match canonical normalized axis")
    if meta.get("slug") != identity.slug:
        problems.append("axis slug must match canonical normalized axis")
    if factors != identity.factors:
        problems.append("axis factors must match canonical axis order")
    return problems


def _check_activation_identity(meta: dict) -> list[str]:
    if meta.get("page_type") != "activation":
        return []
    axis_text = meta.get("axis", "")
    if "/" not in axis_text:
        return []
    factor_a, factor_b = [part.strip() for part in axis_text.split("/")]
    identity = normalize_activation(factor_a, factor_b, meta.get("activated_by", ""))
    problems: list[str] = []
    if meta.get("title") != identity.display:
        problems.append("activation title must match canonical normalized formula")
    if meta.get("normalized_formula") != identity.display:
        problems.append("normalized_formula must match canonical normalized formula")
    if meta.get("axis") != identity.axis.display:
        problems.append("activation axis must match canonical normalized axis")
    if meta.get("slug") != identity.slug:
        problems.append("activation slug must match canonical normalized formula")
    if tuple(meta.get("triad_set", []) or []) != identity.triad_set:
        problems.append("activation triad_set must match canonical normalized formula")
    return problems


def _check_triad_identity(meta: dict) -> list[str]:
    if meta.get("page_type") != "triad_hub":
        return []
    try:
        identity = normalize_triad(meta.get("triad_set", []) or [])
    except ValueError:
        return ["triad hubs must list exactly three distinct factors"]
    problems: list[str] = []
    if tuple(meta.get("factors", []) or []) != identity.factors:
        problems.append("triad factors must match canonical triad order")
    if tuple(meta.get("triad_set", []) or []) != identity.factors:
        problems.append("triad_set must match canonical triad order")
    if meta.get("title") != identity.display:
        problems.append("triad title must match canonical triad order")
    if meta.get("slug") != identity.slug:
        problems.append("triad slug must match canonical triad order")
    if tuple(meta.get("orientations", []) or []) != identity.orientations:
        problems.append("triad orientations must list the canonical three distinct orientations")
    return problems


def _check_canonical_anchors(page_type: str, body: str) -> list[str]:
    if page_type not in {"factor", "axis", "activation"}:
        return []
    if explicit_anchor(DERIVED_SYNTHESIS_ANCHOR) not in body:
        return ["canonical pages must include an explicit derived-synthesis anchor"]
    return []


def lint_wiki(root: Path) -> list[str]:
    problems: list[str] = []
    for page in iter_wiki_pages(root):
        page_problems = _check_required_fields(page.meta)
        page_problems.extend(_check_factor_identity(page.meta))
        page_problems.extend(_check_axis_identity(page.meta))
        page_problems.extend(_check_activation_identity(page.meta))
        page_problems.extend(_check_activation_aliases(page.meta))
        page_problems.extend(_check_triad_identity(page.meta))
        page_problems.extend(_check_canonical_anchors(str(page.meta.get("page_type", "")), page.body))
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

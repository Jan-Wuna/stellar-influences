from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


CHECKS = [
    {
        "id": "factor-sun",
        "path": "wiki/factors/sun.md",
        "contains": [
            "page_type: factor",
            "title: Sun",
            "## Source Entries",
            "### Manly P. Hall - Astrological Keywords",
            '<a id="derived-synthesis"></a>',
        ],
    },
    {
        "id": "axis-sun-moon",
        "path": "wiki/axes/sun-moon.md",
        "contains": [
            "page_type: axis",
            "normalized_axis: Sun/Moon",
            "aliases:",
            "  - Moon/Sun",
            "### Michael Harding and Charles Harvey - Working with Astrology",
            "### Zane B. Stein - The Quadrant Midpoints: The Chart's Backbone",
            '<a id="derived-synthesis"></a>',
        ],
    },
    {
        "id": "axis-jupiter-uranus",
        "path": "wiki/axes/jupiter-uranus.md",
        "contains": [
            "page_type: axis",
            "normalized_axis: Jupiter/Uranus",
            "aliases:",
            "  - Uranus/Jupiter",
            "### Aren Ober - Midpoint Interpretation Simplified",
            '<a id="derived-synthesis"></a>',
        ],
    },
    {
        "id": "activation-jupiter-uranus-equals-sun",
        "path": "wiki/activations/jupiter-uranus-equals-sun.md",
        "contains": [
            "page_type: activation",
            "normalized_formula: Jupiter/Uranus = Sun",
            "axis: Jupiter/Uranus",
            "activated_by: Sun",
            "#### Ober Entry",
            '<a id="derived-synthesis"></a>',
        ],
    },
    {
        "id": "activation-sun-jupiter-equals-moon",
        "path": "wiki/activations/sun-jupiter-equals-moon.md",
        "contains": [
            "page_type: activation",
            "normalized_formula: Sun/Jupiter = Moon",
            "axis: Sun/Jupiter",
            "activated_by: Moon",
            "Source notation: `Moon equals Sun/Jupiter` / `Mo = So/Ju`",
            '<a id="derived-synthesis"></a>',
        ],
    },
    {
        "id": "triad-sun-jupiter-uranus",
        "path": "wiki/triads/sun-jupiter-uranus.md",
        "contains": [
            "page_type: triad_hub",
            "triad_set:",
            "  - Sun",
            "  - Jupiter",
            "  - Uranus",
            "This page is structural only. It does not merge the meanings of its orientations.",
            "- [Jupiter/Uranus = Sun]",
            "- [Sun/Jupiter = Uranus]",
            "- [Sun/Uranus = Jupiter]",
        ],
    },
]


ADVERSARIAL = [
    {
        "id": "axis-unordered-alias",
        "path": "wiki/axes/jupiter-uranus.md",
        "expected": "Axis keeps Uranus/Jupiter as alias while canonical normalized_axis remains Jupiter/Uranus.",
        "pass_if": lambda text: "normalized_axis: Jupiter/Uranus" in text and "  - Uranus/Jupiter" in text,
    },
    {
        "id": "activation-no-alias-collapse",
        "path": "wiki/activations/jupiter-uranus-equals-sun.md",
        "expected": "Activation has no aliases and preserves activated_by: Sun.",
        "pass_if": lambda text: "aliases:\n  []" in text and "activated_by: Sun" in text,
    },
    {
        "id": "triad-no-merged-doctrine",
        "path": "wiki/triads/sun-jupiter-uranus.md",
        "expected": "Triad hub remains structural and lists orientations instead of a Derived Synthesis.",
        "pass_if": lambda text: "This page is structural only" in text and "## Derived Synthesis" not in text,
    },
]


def main() -> int:
    results = []
    ok = True
    for check in CHECKS:
        path = ROOT / check["path"]
        text = path.read_text(encoding="utf-8")
        missing = [needle for needle in check["contains"] if needle not in text]
        passed = not missing
        ok = ok and passed
        results.append(
            {
                "scenario": check["id"],
                "path": check["path"],
                "verdict": "PASS" if passed else "FAIL",
                "missing": missing,
            }
        )

    adversarial_results = []
    for case in ADVERSARIAL:
        path = ROOT / case["path"]
        text = path.read_text(encoding="utf-8")
        passed = bool(case["pass_if"](text))
        ok = ok and passed
        adversarial_results.append(
            {
                "scenario": case["id"],
                "path": case["path"],
                "expected": case["expected"],
                "verdict": "PASS" if passed else "FAIL",
            }
        )

    output = {
        "surfaceEvidence": results,
        "adversarialCases": adversarial_results,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

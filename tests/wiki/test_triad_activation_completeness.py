from pathlib import Path

from tools.wiki_identity import normalize_activation
from tools.wiki_pages import iter_wiki_pages


def test_every_triad_orientation_has_a_live_activation_page():
    missing = []
    for page in iter_wiki_pages(Path("wiki/triads")):
        for orientation in page.meta.get("orientations", []) or []:
            left, right = orientation.split("=")
            factor_a, factor_b = [part.strip() for part in left.split("/")]
            activation = normalize_activation(factor_a, factor_b, right.strip())
            activation_path = Path("wiki/activations") / f"{activation.slug}.md"
            if not activation_path.exists():
                missing.append(f"{page.path.as_posix()} -> {orientation}")

    assert not missing, "\n".join(missing)

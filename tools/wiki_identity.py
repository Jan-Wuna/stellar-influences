from __future__ import annotations

from dataclasses import dataclass


FACTOR_ORDER = {
    "Sun": 10,
    "Moon": 20,
    "Mercury": 30,
    "Venus": 40,
    "Mars": 50,
    "Jupiter": 60,
    "Saturn": 70,
    "Uranus": 80,
    "Neptune": 90,
    "Pluto": 100,
    "Node": 110,
    "Asc": 120,
    "MC": 130,
}


def _clean_factor(name: str) -> str:
    return " ".join(name.strip().split()).title()


def _slug_part(name: str) -> str:
    return _clean_factor(name).lower().replace(" ", "-")


def _sort_key(name: str) -> tuple[int, str]:
    clean = _clean_factor(name)
    return (FACTOR_ORDER.get(clean, 10_000), clean.casefold())


@dataclass(frozen=True)
class AxisIdentity:
    display: str
    slug: str
    factors: tuple[str, str]


@dataclass(frozen=True)
class ActivationIdentity:
    display: str
    slug: str
    axis: AxisIdentity
    activated_by: str
    triad_set: tuple[str, str, str]


def normalize_axis(a: str, b: str) -> AxisIdentity:
    left, right = sorted((_clean_factor(a), _clean_factor(b)), key=_sort_key)
    return AxisIdentity(
        display=f"{left}/{right}",
        slug=f"{_slug_part(left)}-{_slug_part(right)}",
        factors=(left, right),
    )


def normalize_activation(a: str, b: str, activated_by: str) -> ActivationIdentity:
    axis = normalize_axis(a, b)
    right = _clean_factor(activated_by)
    triad = tuple(sorted({axis.factors[0], axis.factors[1], right}, key=_sort_key))
    return ActivationIdentity(
        display=f"{axis.display} = {right}",
        slug=f"{axis.slug}-equals-{_slug_part(right)}",
        axis=axis,
        activated_by=right,
        triad_set=triad,
    )


def triad_orientations(factors: list[str] | tuple[str, ...]) -> list[str]:
    unique = tuple(sorted({_clean_factor(name) for name in factors}, key=_sort_key))
    if len(unique) != 3:
        raise ValueError("triad_orientations requires exactly three distinct factors")
    orientations = [
        normalize_activation(unique[1], unique[2], unique[0]).display,
        normalize_activation(unique[0], unique[1], unique[2]).display,
        normalize_activation(unique[0], unique[2], unique[1]).display,
    ]
    return sorted(orientations)

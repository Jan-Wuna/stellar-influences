from __future__ import annotations

from dataclasses import dataclass


CANONICAL_FACTORS = (
    "Vernal Point",
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Chiron",
    "Uranus",
    "Neptune",
    "Pluto",
    "Node",
    "Asc",
    "MC",
    "Cupido",
    "Hades",
    "Zeus",
    "Kronos",
    "Apollon",
    "Admetos",
    "Vulcanus",
    "Poseidon",
)

FACTOR_ORDER = {name: index for index, name in enumerate(CANONICAL_FACTORS)}

FACTOR_ALIASES = {
    "Vernal Point": {
        "ar",
        "aries",
        "aries point",
        "vp",
        "vernal point",
        "vernal point (aries point)",
        "vernal point (representing all the cardinal points)",
    },
    "MC": {"m", "mc", "medium coeli", "meridian"},
    "Asc": {"a", "as", "asc", "ascendant"},
    "Sun": {"0", "o", "sun", "su"},
    "Moon": {"))", "])", "d", "j)", "moon", "mo"},
    "Node": {"g", "n", "q", "node", "nodes", "lunar node", "lunar nodes", "dragon's head", "no"},
    "Mercury": {"mercury", "me"},
    "Venus": {"venus", "ve"},
    "Mars": {"cf", "mars", "ma"},
    "Jupiter": {"if", "1|.", "jupiter", "ju"},
    "Saturn": {"f)", "saturn", "sa"},
    "Chiron": {"ch", "chiron"},
    "Uranus": {"uranus", "ur"},
    "Neptune": {"neptune", "ne"},
    "Pluto": {"pluto", "pl"},
    "Cupido": {"cupido", "cu"},
    "Hades": {"hades", "ha"},
    "Zeus": {"zeus", "ze"},
    "Kronos": {"kronos", "kr"},
    "Apollon": {"apollon", "ap"},
    "Admetos": {"admetos", "ad"},
    "Vulcanus": {"vulcanus", "vulkanus", "vu"},
    "Poseidon": {"poseidon", "po"},
}

FACTOR_NAME_LOOKUP = {
    alias.casefold(): canonical
    for canonical, aliases in FACTOR_ALIASES.items()
    for alias in aliases | {canonical}
}

ASTRONOMICON_TOKENS = {
    "Vernal Point": "VP",
    "Sun": "S",
    "Moon": "R",
    "Mercury": "T",
    "Venus": "Q",
    "Mars": "U",
    "Jupiter": "V",
    "Saturn": "W",
    "Uranus": "X",
    "Neptune": "Y",
    "Pluto": "Z",
    "Node": "g",
    "Cupido": "\u00a1",
    "Hades": "\u00a2",
    "Zeus": "\u00a3",
    "Kronos": "\u00a4",
    "Apollon": "\u00a5",
    "Admetos": "\u00a6",
    "Vulcanus": "\u00a7",
    "Poseidon": "\u00a8",
}


def _clean_factor(name: str) -> str:
    compact = " ".join(name.strip().split())
    if not compact:
        raise ValueError("factor name cannot be empty")
    canonical = FACTOR_NAME_LOOKUP.get(compact.casefold())
    if canonical is not None:
        return canonical
    return compact.title()


def _slug_part(name: str) -> str:
    return _clean_factor(name).lower().replace(" ", "-")


def _sort_key(name: str) -> tuple[int, str]:
    clean = _clean_factor(name)
    return (FACTOR_ORDER.get(clean, 10_000), clean.casefold())


def astronomicon_token(name: str) -> str:
    canonical = _clean_factor(name)
    return ASTRONOMICON_TOKENS.get(canonical, canonical)


@dataclass(frozen=True)
class AxisIdentity:
    display: str
    slug: str
    factors: tuple[str, str]


@dataclass(frozen=True)
class FactorIdentity:
    display: str
    slug: str


@dataclass(frozen=True)
class ActivationIdentity:
    display: str
    slug: str
    axis: AxisIdentity
    activated_by: str
    triad_set: tuple[str, ...]

    @property
    def has_distinct_triad(self) -> bool:
        return len(self.triad_set) == 3


@dataclass(frozen=True)
class TriadIdentity:
    display: str
    slug: str
    factors: tuple[str, str, str]
    orientations: tuple[str, str, str]


def normalize_factor(name: str) -> FactorIdentity:
    canonical = _clean_factor(name)
    return FactorIdentity(
        display=canonical,
        slug=_slug_part(canonical),
    )


def factor_slug(name: str) -> str:
    return normalize_factor(name).slug


def normalize_axis(a: str, b: str) -> AxisIdentity:
    left = _clean_factor(a)
    right = _clean_factor(b)
    if _sort_key(left) <= _sort_key(right):
        ordered = (left, right)
    else:
        ordered = (right, left)
    return AxisIdentity(
        display=f"{ordered[0]}/{ordered[1]}",
        slug=f"{_slug_part(ordered[0])}-{_slug_part(ordered[1])}",
        factors=ordered,
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


def _normalize_triad_factors(factors: list[str] | tuple[str, ...]) -> tuple[str, str, str]:
    unique = tuple(sorted({_clean_factor(name) for name in factors}, key=_sort_key))
    if len(unique) != 3:
        raise ValueError("triad_orientations requires exactly three distinct factors")
    return unique


def normalize_triad(factors: list[str] | tuple[str, ...]) -> TriadIdentity:
    unique = _normalize_triad_factors(factors)
    orientations = (
        normalize_activation(unique[1], unique[2], unique[0]).display,
        normalize_activation(unique[0], unique[1], unique[2]).display,
        normalize_activation(unique[0], unique[2], unique[1]).display,
    )
    return TriadIdentity(
        display=" ".join(unique),
        slug="-".join(_slug_part(name) for name in unique),
        factors=unique,
        orientations=tuple(sorted(orientations)),
    )


def triad_slug(factors: list[str] | tuple[str, ...]) -> str:
    return normalize_triad(factors).slug


def triad_orientations(factors: list[str] | tuple[str, ...]) -> list[str]:
    return list(normalize_triad(factors).orientations)

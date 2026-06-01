from pathlib import Path

from tools.query_manifest import build_query_manifest


_MANIFEST = None
_BY_SLUG = None


def manifest_pages():
    global _MANIFEST
    if _MANIFEST is None:
        _MANIFEST = build_query_manifest(Path("wiki"))
    return _MANIFEST["pages"]


def manifest_by_slug():
    global _BY_SLUG
    if _BY_SLUG is None:
        _BY_SLUG = {page["slug"]: page for page in manifest_pages()}
    return _BY_SLUG


def is_deferred_answer_surface(page):
    factors = page.get("factors") or []
    if "Chiron" in factors:
        return True
    if page.get("page_type") == "activation" and len(set(factors)) < len(factors):
        return True
    return False


SEEDED_RELATIONSHIP_CLUSTER = {
    "sun-moon",
    "sun-venus",
    "moon-venus",
    "sun-moon-equals-venus",
    "sun-venus-equals-moon",
    "moon-venus-equals-sun",
}

SEEDED_GROWTH_CLUSTER = {
    "sun-jupiter",
    "moon-jupiter",
    "mars-jupiter",
    "jupiter-asc",
    "asc-mc",
    "asc-mc-equals-jupiter",
}

SEEDED_EXPANSION_PRESSURE_CLUSTER = {
    "jupiter-neptune",
    "jupiter-saturn",
    "jupiter-uranus",
    "mars-neptune",
    "mars-saturn",
    "mars-uranus",
}

SEEDED_MERCURY_CLUSTER = {
    "sun-mercury",
    "moon-mercury",
    "mercury-venus",
    "mercury-mars",
    "mercury-saturn",
    "mercury-uranus",
    "mercury-neptune",
}

SEEDED_LUMINARY_PRESSURE_CLUSTER = {
    "sun-mars",
    "sun-neptune",
    "sun-saturn",
    "sun-uranus",
    "moon-mars",
    "moon-neptune",
    "moon-saturn",
    "moon-uranus",
}

SEEDED_VENUS_AND_OUTER_CLUSTER = {
    "saturn-neptune",
    "saturn-uranus",
    "uranus-neptune",
    "venus-jupiter",
    "venus-mars",
    "venus-neptune",
    "venus-saturn",
    "venus-uranus",
}

SEEDED_PLUTO_AND_MERCURY_JUPITER_CLUSTER = {
    "jupiter-pluto",
    "mars-pluto",
    "mercury-jupiter",
    "mercury-pluto",
    "moon-pluto",
    "neptune-pluto",
    "saturn-pluto",
    "sun-pluto",
    "uranus-pluto",
    "venus-pluto",
}

SEEDED_ANGLE_NODE_CLUSTER = {
    "jupiter-mc",
    "jupiter-node",
    "mars-asc",
    "mars-mc",
    "mars-node",
    "mercury-asc",
    "mercury-mc",
    "mercury-node",
    "moon-mc",
    "moon-node",
    "neptune-asc",
    "neptune-mc",
    "neptune-node",
    "node-asc",
    "node-mc",
}

SEEDED_SUN_VENUS_SATURN_URANUS_PLUTO_PERSONAL_POINT_CLUSTER = {
    "pluto-asc",
    "pluto-mc",
    "pluto-node",
    "saturn-asc",
    "saturn-mc",
    "saturn-node",
    "sun-asc",
    "sun-mc",
    "sun-node",
    "uranus-asc",
    "uranus-mc",
    "uranus-node",
    "venus-asc",
    "venus-mc",
    "venus-node",
}

SEEDED_MOON_ASC_AND_MERCURY_ACTIVATION_CLUSTER = {
    "moon-asc",
    "asc-mc-equals-mercury",
    "sun-moon-equals-mercury",
}

SEEDED_MOON_ASC_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-asc-equals-admetos",
    "moon-asc-equals-apollon",
    "moon-asc-equals-chiron",
    "moon-asc-equals-cupido",
    "moon-asc-equals-hades",
    "moon-asc-equals-kronos",
    "moon-asc-equals-poseidon",
    "moon-asc-equals-vernal-point",
    "moon-asc-equals-vulcanus",
    "moon-asc-equals-zeus",
}

SEEDED_MOON_JUPITER_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-jupiter-equals-admetos",
    "moon-jupiter-equals-apollon",
    "moon-jupiter-equals-chiron",
    "moon-jupiter-equals-cupido",
    "moon-jupiter-equals-hades",
    "moon-jupiter-equals-kronos",
    "moon-jupiter-equals-poseidon",
    "moon-jupiter-equals-vernal-point",
    "moon-jupiter-equals-vulcanus",
    "moon-jupiter-equals-zeus",
}

SEEDED_MOON_MARS_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-mars-equals-admetos",
    "moon-mars-equals-apollon",
    "moon-mars-equals-chiron",
    "moon-mars-equals-cupido",
    "moon-mars-equals-hades",
    "moon-mars-equals-kronos",
    "moon-mars-equals-poseidon",
    "moon-mars-equals-vernal-point",
    "moon-mars-equals-vulcanus",
    "moon-mars-equals-zeus",
}

SEEDED_MOON_MC_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-mc-equals-admetos",
    "moon-mc-equals-apollon",
    "moon-mc-equals-chiron",
    "moon-mc-equals-cupido",
    "moon-mc-equals-hades",
    "moon-mc-equals-kronos",
    "moon-mc-equals-poseidon",
    "moon-mc-equals-vernal-point",
    "moon-mc-equals-vulcanus",
    "moon-mc-equals-zeus",
}

SEEDED_MOON_MERCURY_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-mercury-equals-admetos",
    "moon-mercury-equals-apollon",
    "moon-mercury-equals-chiron",
    "moon-mercury-equals-cupido",
    "moon-mercury-equals-hades",
    "moon-mercury-equals-kronos",
    "moon-mercury-equals-poseidon",
    "moon-mercury-equals-vernal-point",
    "moon-mercury-equals-vulcanus",
    "moon-mercury-equals-zeus",
}

SEEDED_MOON_MOON_INITIAL_CLUSTER = {
    "moon-moon",
    "moon-moon-equals-admetos",
    "moon-moon-equals-apollon",
    "moon-moon-equals-asc",
    "moon-moon-equals-cupido",
    "moon-moon-equals-hades",
    "moon-moon-equals-jupiter",
    "moon-moon-equals-kronos",
    "moon-moon-equals-mars",
    "moon-moon-equals-mc",
}

SEEDED_MOON_MOON_COMPLETION_CLUSTER = {
    "moon-moon-equals-mercury",
    "moon-moon-equals-neptune",
    "moon-moon-equals-node",
    "moon-moon-equals-pluto",
    "moon-moon-equals-poseidon",
    "moon-moon-equals-saturn",
    "moon-moon-equals-sun",
    "moon-moon-equals-uranus",
    "moon-moon-equals-venus",
    "moon-moon-equals-vernal-point",
    "moon-moon-equals-vulcanus",
    "moon-moon-equals-zeus",
}

SEEDED_MOON_NEPTUNE_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-neptune-equals-admetos",
    "moon-neptune-equals-apollon",
    "moon-neptune-equals-chiron",
    "moon-neptune-equals-cupido",
    "moon-neptune-equals-hades",
    "moon-neptune-equals-kronos",
    "moon-neptune-equals-poseidon",
    "moon-neptune-equals-vernal-point",
    "moon-neptune-equals-vulcanus",
    "moon-neptune-equals-zeus",
}

SEEDED_MOON_NODE_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-node-equals-admetos",
    "moon-node-equals-apollon",
    "moon-node-equals-chiron",
    "moon-node-equals-cupido",
    "moon-node-equals-hades",
    "moon-node-equals-kronos",
    "moon-node-equals-poseidon",
    "moon-node-equals-vernal-point",
    "moon-node-equals-vulcanus",
    "moon-node-equals-zeus",
}

SEEDED_MOON_PLUTO_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-pluto-equals-admetos",
    "moon-pluto-equals-apollon",
    "moon-pluto-equals-chiron",
    "moon-pluto-equals-cupido",
    "moon-pluto-equals-hades",
    "moon-pluto-equals-kronos",
    "moon-pluto-equals-poseidon",
    "moon-pluto-equals-vernal-point",
    "moon-pluto-equals-vulcanus",
    "moon-pluto-equals-zeus",
}

SEEDED_MOON_SATURN_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-saturn-equals-admetos",
    "moon-saturn-equals-apollon",
    "moon-saturn-equals-chiron",
    "moon-saturn-equals-cupido",
    "moon-saturn-equals-hades",
    "moon-saturn-equals-kronos",
    "moon-saturn-equals-poseidon",
    "moon-saturn-equals-vernal-point",
    "moon-saturn-equals-vulcanus",
    "moon-saturn-equals-zeus",
}

SEEDED_MOON_URANUS_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-uranus-equals-admetos",
    "moon-uranus-equals-apollon",
    "moon-uranus-equals-chiron",
    "moon-uranus-equals-cupido",
    "moon-uranus-equals-hades",
    "moon-uranus-equals-kronos",
    "moon-uranus-equals-poseidon",
    "moon-uranus-equals-vernal-point",
    "moon-uranus-equals-vulcanus",
    "moon-uranus-equals-zeus",
}

SEEDED_MOON_VENUS_ADDITIONAL_ACTIVATION_CLUSTER = {
    "moon-venus-equals-admetos",
    "moon-venus-equals-apollon",
    "moon-venus-equals-chiron",
    "moon-venus-equals-cupido",
    "moon-venus-equals-hades",
    "moon-venus-equals-kronos",
    "moon-venus-equals-poseidon",
    "moon-venus-equals-vernal-point",
    "moon-venus-equals-vulcanus",
    "moon-venus-equals-zeus",
}

SEEDED_NEPTUNE_ADMETOS_INITIAL_CLUSTER = {
    "neptune-admetos",
    "neptune-admetos-equals-apollon",
    "neptune-admetos-equals-asc",
    "neptune-admetos-equals-cupido",
    "neptune-admetos-equals-hades",
    "neptune-admetos-equals-jupiter",
    "neptune-admetos-equals-kronos",
    "neptune-admetos-equals-mars",
    "neptune-admetos-equals-mc",
    "neptune-admetos-equals-mercury",
    "neptune-admetos-equals-moon",
    "neptune-admetos-equals-node",
}

SEEDED_NEPTUNE_ADMETOS_COMPLETION_CLUSTER = {
    "neptune-admetos-equals-pluto",
    "neptune-admetos-equals-poseidon",
    "neptune-admetos-equals-saturn",
    "neptune-admetos-equals-sun",
    "neptune-admetos-equals-uranus",
    "neptune-admetos-equals-venus",
    "neptune-admetos-equals-vernal-point",
    "neptune-admetos-equals-vulcanus",
    "neptune-admetos-equals-zeus",
}

SEEDED_NEPTUNE_APOLLON_INITIAL_CLUSTER = {
    "neptune-apollon",
    "neptune-apollon-equals-admetos",
    "neptune-apollon-equals-asc",
    "neptune-apollon-equals-cupido",
    "neptune-apollon-equals-hades",
    "neptune-apollon-equals-jupiter",
    "neptune-apollon-equals-kronos",
    "neptune-apollon-equals-mars",
    "neptune-apollon-equals-mc",
    "neptune-apollon-equals-mercury",
    "neptune-apollon-equals-moon",
    "neptune-apollon-equals-node",
}

SEEDED_NEPTUNE_APOLLON_COMPLETION_CLUSTER = {
    "neptune-apollon-equals-pluto",
    "neptune-apollon-equals-poseidon",
    "neptune-apollon-equals-saturn",
    "neptune-apollon-equals-sun",
    "neptune-apollon-equals-uranus",
    "neptune-apollon-equals-venus",
    "neptune-apollon-equals-vernal-point",
    "neptune-apollon-equals-vulcanus",
    "neptune-apollon-equals-zeus",
}

SEEDED_ASC_MC_ACTIVATION_CLUSTER = {
    "asc-mc-equals-admetos",
    "asc-mc-equals-apollon",
    "asc-mc-equals-chiron",
    "asc-mc-equals-cupido",
    "asc-mc-equals-hades",
    "asc-mc-equals-kronos",
    "asc-mc-equals-mars",
    "asc-mc-equals-moon",
    "asc-mc-equals-neptune",
    "asc-mc-equals-node",
    "asc-mc-equals-pluto",
    "asc-mc-equals-poseidon",
    "asc-mc-equals-saturn",
    "asc-mc-equals-sun",
    "asc-mc-equals-uranus",
    "asc-mc-equals-venus",
    "asc-mc-equals-vernal-point",
    "asc-mc-equals-vulcanus",
    "asc-mc-equals-zeus",
}

SEEDED_JUPITER_ASC_ACTIVATION_CLUSTER = {
    "jupiter-asc-equals-mars",
    "jupiter-asc-equals-mc",
    "jupiter-asc-equals-mercury",
    "jupiter-asc-equals-moon",
    "jupiter-asc-equals-neptune",
    "jupiter-asc-equals-node",
    "jupiter-asc-equals-pluto",
    "jupiter-asc-equals-saturn",
    "jupiter-asc-equals-sun",
    "jupiter-asc-equals-uranus",
    "jupiter-asc-equals-venus",
}

SEEDED_ASC_JUPITER_FACTOR_CLUSTER = {
    "asc",
    "jupiter",
}

SEEDED_JUPITER_MC_ACTIVATION_CLUSTER = {
    "jupiter-mc-equals-asc",
    "jupiter-mc-equals-mars",
    "jupiter-mc-equals-mercury",
    "jupiter-mc-equals-moon",
    "jupiter-mc-equals-neptune",
    "jupiter-mc-equals-node",
    "jupiter-mc-equals-pluto",
    "jupiter-mc-equals-saturn",
    "jupiter-mc-equals-sun",
    "jupiter-mc-equals-uranus",
    "jupiter-mc-equals-venus",
}

SEEDED_JUPITER_NEPTUNE_ACTIVATION_CLUSTER = {
    "jupiter-neptune-equals-asc",
    "jupiter-neptune-equals-mars",
    "jupiter-neptune-equals-mc",
    "jupiter-neptune-equals-mercury",
    "jupiter-neptune-equals-moon",
    "jupiter-neptune-equals-node",
    "jupiter-neptune-equals-pluto",
    "jupiter-neptune-equals-saturn",
    "jupiter-neptune-equals-sun",
    "jupiter-neptune-equals-uranus",
    "jupiter-neptune-equals-venus",
}

SEEDED_JUPITER_MC_ADDITIONAL_ACTIVATION_CLUSTER = {
    "jupiter-mc-equals-admetos",
    "jupiter-mc-equals-apollon",
    "jupiter-mc-equals-chiron",
    "jupiter-mc-equals-cupido",
    "jupiter-mc-equals-hades",
    "jupiter-mc-equals-kronos",
    "jupiter-mc-equals-poseidon",
    "jupiter-mc-equals-vernal-point",
    "jupiter-mc-equals-vulcanus",
    "jupiter-mc-equals-zeus",
}

SEEDED_JUPITER_NEPTUNE_ADDITIONAL_ACTIVATION_CLUSTER = {
    "jupiter-neptune-equals-admetos",
    "jupiter-neptune-equals-apollon",
    "jupiter-neptune-equals-chiron",
    "jupiter-neptune-equals-cupido",
    "jupiter-neptune-equals-hades",
    "jupiter-neptune-equals-kronos",
    "jupiter-neptune-equals-poseidon",
    "jupiter-neptune-equals-vernal-point",
    "jupiter-neptune-equals-vulcanus",
    "jupiter-neptune-equals-zeus",
}

SEEDED_JUPITER_NODE_ACTIVATION_CLUSTER = {
    "jupiter-node-equals-asc",
    "jupiter-node-equals-mars",
    "jupiter-node-equals-mc",
    "jupiter-node-equals-mercury",
    "jupiter-node-equals-moon",
    "jupiter-node-equals-neptune",
    "jupiter-node-equals-pluto",
    "jupiter-node-equals-saturn",
    "jupiter-node-equals-sun",
    "jupiter-node-equals-uranus",
    "jupiter-node-equals-venus",
}

SEEDED_JUPITER_PLUTO_ACTIVATION_CLUSTER = {
    "jupiter-pluto-equals-asc",
    "jupiter-pluto-equals-mars",
    "jupiter-pluto-equals-mc",
    "jupiter-pluto-equals-mercury",
    "jupiter-pluto-equals-moon",
    "jupiter-pluto-equals-neptune",
    "jupiter-pluto-equals-node",
    "jupiter-pluto-equals-saturn",
    "jupiter-pluto-equals-sun",
    "jupiter-pluto-equals-uranus",
    "jupiter-pluto-equals-venus",
}

SEEDED_JUPITER_NODE_ADDITIONAL_ACTIVATION_CLUSTER = {
    "jupiter-node-equals-admetos",
    "jupiter-node-equals-apollon",
    "jupiter-node-equals-chiron",
    "jupiter-node-equals-cupido",
    "jupiter-node-equals-hades",
    "jupiter-node-equals-kronos",
    "jupiter-node-equals-poseidon",
    "jupiter-node-equals-vernal-point",
    "jupiter-node-equals-vulcanus",
    "jupiter-node-equals-zeus",
}

SEEDED_JUPITER_PLUTO_ADDITIONAL_ACTIVATION_CLUSTER = {
    "jupiter-pluto-equals-admetos",
    "jupiter-pluto-equals-apollon",
    "jupiter-pluto-equals-chiron",
    "jupiter-pluto-equals-cupido",
    "jupiter-pluto-equals-hades",
    "jupiter-pluto-equals-kronos",
    "jupiter-pluto-equals-poseidon",
    "jupiter-pluto-equals-vernal-point",
    "jupiter-pluto-equals-vulcanus",
    "jupiter-pluto-equals-zeus",
}

SEEDED_JUPITER_SATURN_ACTIVATION_CLUSTER = {
    "jupiter-saturn-equals-asc",
    "jupiter-saturn-equals-mars",
    "jupiter-saturn-equals-mc",
    "jupiter-saturn-equals-mercury",
    "jupiter-saturn-equals-moon",
    "jupiter-saturn-equals-neptune",
    "jupiter-saturn-equals-node",
    "jupiter-saturn-equals-pluto",
    "jupiter-saturn-equals-sun",
    "jupiter-saturn-equals-uranus",
    "jupiter-saturn-equals-venus",
}

SEEDED_MARS_FACTOR_CLUSTER = {
    "mars",
}

SEEDED_JUPITER_URANUS_ACTIVATION_CLUSTER = {
    "jupiter-uranus-equals-asc",
    "jupiter-uranus-equals-mars",
    "jupiter-uranus-equals-mc",
    "jupiter-uranus-equals-mercury",
    "jupiter-uranus-equals-moon",
    "jupiter-uranus-equals-neptune",
    "jupiter-uranus-equals-node",
    "jupiter-uranus-equals-pluto",
    "jupiter-uranus-equals-saturn",
    "jupiter-uranus-equals-sun",
    "jupiter-uranus-equals-venus",
}

SEEDED_JUPITER_SATURN_ADDITIONAL_ACTIVATION_CLUSTER = {
    "jupiter-saturn-equals-admetos",
    "jupiter-saturn-equals-apollon",
    "jupiter-saturn-equals-chiron",
    "jupiter-saturn-equals-cupido",
    "jupiter-saturn-equals-hades",
    "jupiter-saturn-equals-kronos",
    "jupiter-saturn-equals-poseidon",
    "jupiter-saturn-equals-vernal-point",
    "jupiter-saturn-equals-vulcanus",
    "jupiter-saturn-equals-zeus",
}

SEEDED_JUPITER_URANUS_ADDITIONAL_ACTIVATION_CLUSTER = {
    "jupiter-uranus-equals-admetos",
    "jupiter-uranus-equals-apollon",
    "jupiter-uranus-equals-chiron",
    "jupiter-uranus-equals-cupido",
    "jupiter-uranus-equals-hades",
    "jupiter-uranus-equals-kronos",
    "jupiter-uranus-equals-poseidon",
    "jupiter-uranus-equals-vernal-point",
    "jupiter-uranus-equals-vulcanus",
    "jupiter-uranus-equals-zeus",
}

SEEDED_MARS_ASC_ACTIVATION_CLUSTER = {
    "mars-asc-equals-jupiter",
    "mars-asc-equals-mc",
    "mars-asc-equals-mercury",
    "mars-asc-equals-moon",
    "mars-asc-equals-neptune",
    "mars-asc-equals-node",
    "mars-asc-equals-pluto",
    "mars-asc-equals-saturn",
    "mars-asc-equals-sun",
    "mars-asc-equals-uranus",
    "mars-asc-equals-venus",
}

SEEDED_MARS_ASC_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mars-asc-equals-admetos",
    "mars-asc-equals-apollon",
    "mars-asc-equals-chiron",
    "mars-asc-equals-cupido",
    "mars-asc-equals-hades",
    "mars-asc-equals-kronos",
    "mars-asc-equals-poseidon",
    "mars-asc-equals-vernal-point",
    "mars-asc-equals-vulcanus",
    "mars-asc-equals-zeus",
}

SEEDED_MARS_JUPITER_ACTIVATION_CLUSTER = {
    "mars-jupiter-equals-asc",
    "mars-jupiter-equals-mc",
    "mars-jupiter-equals-mercury",
    "mars-jupiter-equals-moon",
    "mars-jupiter-equals-neptune",
    "mars-jupiter-equals-node",
    "mars-jupiter-equals-pluto",
    "mars-jupiter-equals-saturn",
    "mars-jupiter-equals-sun",
    "mars-jupiter-equals-uranus",
    "mars-jupiter-equals-venus",
}

SEEDED_MARS_JUPITER_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mars-jupiter-equals-admetos",
    "mars-jupiter-equals-apollon",
    "mars-jupiter-equals-chiron",
    "mars-jupiter-equals-cupido",
    "mars-jupiter-equals-hades",
    "mars-jupiter-equals-kronos",
    "mars-jupiter-equals-poseidon",
    "mars-jupiter-equals-vernal-point",
    "mars-jupiter-equals-vulcanus",
    "mars-jupiter-equals-zeus",
}

SEEDED_MARS_MC_ACTIVATION_CLUSTER = {
    "mars-mc-equals-asc",
    "mars-mc-equals-jupiter",
    "mars-mc-equals-mercury",
    "mars-mc-equals-moon",
    "mars-mc-equals-neptune",
    "mars-mc-equals-node",
    "mars-mc-equals-pluto",
    "mars-mc-equals-saturn",
    "mars-mc-equals-sun",
    "mars-mc-equals-uranus",
    "mars-mc-equals-venus",
}

SEEDED_MARS_NEPTUNE_ACTIVATION_CLUSTER = {
    "mars-neptune-equals-asc",
    "mars-neptune-equals-jupiter",
    "mars-neptune-equals-mc",
    "mars-neptune-equals-mercury",
    "mars-neptune-equals-moon",
    "mars-neptune-equals-node",
    "mars-neptune-equals-pluto",
    "mars-neptune-equals-saturn",
    "mars-neptune-equals-sun",
    "mars-neptune-equals-uranus",
    "mars-neptune-equals-venus",
}

SEEDED_MARS_NODE_ACTIVATION_CLUSTER = {
    "mars-node-equals-asc",
    "mars-node-equals-jupiter",
    "mars-node-equals-mc",
    "mars-node-equals-mercury",
    "mars-node-equals-moon",
    "mars-node-equals-neptune",
    "mars-node-equals-pluto",
    "mars-node-equals-saturn",
    "mars-node-equals-sun",
    "mars-node-equals-uranus",
    "mars-node-equals-venus",
}

SEEDED_MARS_PLUTO_ACTIVATION_CLUSTER = {
    "mars-pluto-equals-asc",
    "mars-pluto-equals-jupiter",
    "mars-pluto-equals-mc",
    "mars-pluto-equals-mercury",
    "mars-pluto-equals-moon",
    "mars-pluto-equals-neptune",
    "mars-pluto-equals-node",
    "mars-pluto-equals-saturn",
    "mars-pluto-equals-sun",
    "mars-pluto-equals-uranus",
    "mars-pluto-equals-venus",
}

SEEDED_MARS_SATURN_ACTIVATION_CLUSTER = {
    "mars-saturn-equals-asc",
    "mars-saturn-equals-jupiter",
    "mars-saturn-equals-mc",
    "mars-saturn-equals-mercury",
    "mars-saturn-equals-moon",
    "mars-saturn-equals-neptune",
    "mars-saturn-equals-node",
    "mars-saturn-equals-pluto",
    "mars-saturn-equals-sun",
    "mars-saturn-equals-uranus",
    "mars-saturn-equals-venus",
}

SEEDED_MARS_URANUS_ACTIVATION_CLUSTER = {
    "mars-uranus-equals-asc",
    "mars-uranus-equals-jupiter",
    "mars-uranus-equals-mc",
    "mars-uranus-equals-mercury",
    "mars-uranus-equals-moon",
    "mars-uranus-equals-neptune",
    "mars-uranus-equals-node",
    "mars-uranus-equals-pluto",
    "mars-uranus-equals-saturn",
    "mars-uranus-equals-sun",
    "mars-uranus-equals-venus",
}

SEEDED_MC_MERCURY_FACTOR_CLUSTER = {
    "mc",
    "mercury",
}

SEEDED_MERCURY_ASC_ACTIVATION_CLUSTER = {
    "mercury-asc-equals-jupiter",
    "mercury-asc-equals-mars",
    "mercury-asc-equals-mc",
    "mercury-asc-equals-moon",
    "mercury-asc-equals-neptune",
    "mercury-asc-equals-node",
    "mercury-asc-equals-pluto",
    "mercury-asc-equals-saturn",
    "mercury-asc-equals-sun",
    "mercury-asc-equals-uranus",
    "mercury-asc-equals-venus",
}

SEEDED_MERCURY_MARS_ACTIVATION_CLUSTER = {
    "mercury-mars-equals-asc",
    "mercury-mars-equals-jupiter",
    "mercury-mars-equals-mc",
    "mercury-mars-equals-moon",
    "mercury-mars-equals-neptune",
    "mercury-mars-equals-node",
    "mercury-mars-equals-pluto",
    "mercury-mars-equals-saturn",
    "mercury-mars-equals-sun",
    "mercury-mars-equals-uranus",
    "mercury-mars-equals-venus",
}

SEEDED_MERCURY_MC_ACTIVATION_CLUSTER = {
    "mercury-mc-equals-asc",
    "mercury-mc-equals-jupiter",
    "mercury-mc-equals-mars",
    "mercury-mc-equals-moon",
    "mercury-mc-equals-neptune",
    "mercury-mc-equals-node",
    "mercury-mc-equals-pluto",
    "mercury-mc-equals-saturn",
    "mercury-mc-equals-sun",
    "mercury-mc-equals-uranus",
    "mercury-mc-equals-venus",
}

SEEDED_SUN_NODE_ACTIVATION_CLUSTER = {
    "sun-node-equals-asc",
    "sun-node-equals-jupiter",
    "sun-node-equals-mars",
    "sun-node-equals-mc",
    "sun-node-equals-mercury",
    "sun-node-equals-moon",
    "sun-node-equals-neptune",
    "sun-node-equals-pluto",
    "sun-node-equals-saturn",
    "sun-node-equals-uranus",
    "sun-node-equals-venus",
}

SEEDED_SUN_NEPTUNE_ACTIVATION_CLUSTER = {
    "sun-neptune-equals-asc",
    "sun-neptune-equals-jupiter",
    "sun-neptune-equals-mars",
    "sun-neptune-equals-mc",
    "sun-neptune-equals-mercury",
    "sun-neptune-equals-moon",
    "sun-neptune-equals-node",
    "sun-neptune-equals-pluto",
    "sun-neptune-equals-saturn",
    "sun-neptune-equals-uranus",
    "sun-neptune-equals-venus",
}

SEEDED_SUN_MERCURY_ACTIVATION_CLUSTER = {
    "sun-mercury-equals-asc",
    "sun-mercury-equals-jupiter",
    "sun-mercury-equals-mars",
    "sun-mercury-equals-mc",
    "sun-mercury-equals-moon",
    "sun-mercury-equals-neptune",
    "sun-mercury-equals-node",
    "sun-mercury-equals-pluto",
    "sun-mercury-equals-saturn",
    "sun-mercury-equals-uranus",
    "sun-mercury-equals-venus",
}

SEEDED_SUN_PLUTO_ACTIVATION_CLUSTER = {
    "sun-pluto-equals-asc",
    "sun-pluto-equals-jupiter",
    "sun-pluto-equals-mars",
    "sun-pluto-equals-mc",
    "sun-pluto-equals-mercury",
    "sun-pluto-equals-moon",
    "sun-pluto-equals-neptune",
    "sun-pluto-equals-node",
    "sun-pluto-equals-saturn",
    "sun-pluto-equals-uranus",
    "sun-pluto-equals-venus",
}

SEEDED_SUN_MC_ACTIVATION_CLUSTER = {
    "sun-mc-equals-asc",
    "sun-mc-equals-jupiter",
    "sun-mc-equals-mars",
    "sun-mc-equals-mercury",
    "sun-mc-equals-moon",
    "sun-mc-equals-neptune",
    "sun-mc-equals-node",
    "sun-mc-equals-pluto",
    "sun-mc-equals-saturn",
    "sun-mc-equals-uranus",
    "sun-mc-equals-venus",
}

SEEDED_SUN_MARS_ACTIVATION_CLUSTER = {
    "sun-mars-equals-asc",
    "sun-mars-equals-jupiter",
    "sun-mars-equals-mc",
    "sun-mars-equals-mercury",
    "sun-mars-equals-moon",
    "sun-mars-equals-neptune",
    "sun-mars-equals-node",
    "sun-mars-equals-pluto",
    "sun-mars-equals-saturn",
    "sun-mars-equals-uranus",
    "sun-mars-equals-venus",
}

SEEDED_SUN_SATURN_ACTIVATION_CLUSTER = {
    "sun-saturn-equals-asc",
    "sun-saturn-equals-jupiter",
    "sun-saturn-equals-mars",
    "sun-saturn-equals-mc",
    "sun-saturn-equals-mercury",
    "sun-saturn-equals-moon",
    "sun-saturn-equals-neptune",
    "sun-saturn-equals-node",
    "sun-saturn-equals-pluto",
    "sun-saturn-equals-uranus",
    "sun-saturn-equals-venus",
}

SEEDED_SUN_JUPITER_ACTIVATION_CLUSTER = {
    "sun-jupiter-equals-asc",
    "sun-jupiter-equals-mars",
    "sun-jupiter-equals-mc",
    "sun-jupiter-equals-mercury",
    "sun-jupiter-equals-moon",
    "sun-jupiter-equals-neptune",
    "sun-jupiter-equals-node",
    "sun-jupiter-equals-pluto",
    "sun-jupiter-equals-saturn",
    "sun-jupiter-equals-uranus",
    "sun-jupiter-equals-venus",
}

SEEDED_SUN_ASC_ACTIVATION_CLUSTER = {
    "sun-asc-equals-jupiter",
    "sun-asc-equals-mars",
    "sun-asc-equals-mc",
    "sun-asc-equals-mercury",
    "sun-asc-equals-moon",
    "sun-asc-equals-neptune",
    "sun-asc-equals-node",
    "sun-asc-equals-pluto",
    "sun-asc-equals-saturn",
    "sun-asc-equals-uranus",
    "sun-asc-equals-venus",
}

SEEDED_SUN_URANUS_ACTIVATION_CLUSTER = {
    "sun-uranus-equals-asc",
    "sun-uranus-equals-jupiter",
    "sun-uranus-equals-mars",
    "sun-uranus-equals-mc",
    "sun-uranus-equals-mercury",
    "sun-uranus-equals-moon",
    "sun-uranus-equals-neptune",
    "sun-uranus-equals-node",
    "sun-uranus-equals-pluto",
    "sun-uranus-equals-saturn",
    "sun-uranus-equals-venus",
}

SEEDED_URANUS_MC_ACTIVATION_CLUSTER = {
    "uranus-mc-equals-asc",
    "uranus-mc-equals-jupiter",
    "uranus-mc-equals-mars",
    "uranus-mc-equals-mercury",
    "uranus-mc-equals-moon",
    "uranus-mc-equals-neptune",
    "uranus-mc-equals-node",
    "uranus-mc-equals-pluto",
    "uranus-mc-equals-saturn",
    "uranus-mc-equals-sun",
    "uranus-mc-equals-venus",
}

SEEDED_URANUS_ASC_ACTIVATION_CLUSTER = {
    "uranus-asc-equals-jupiter",
    "uranus-asc-equals-mars",
    "uranus-asc-equals-mc",
    "uranus-asc-equals-mercury",
    "uranus-asc-equals-moon",
    "uranus-asc-equals-neptune",
    "uranus-asc-equals-node",
    "uranus-asc-equals-pluto",
    "uranus-asc-equals-saturn",
    "uranus-asc-equals-sun",
    "uranus-asc-equals-venus",
}

SEEDED_SATURN_NEPTUNE_ACTIVATION_CLUSTER = {
    "saturn-neptune-equals-asc",
    "saturn-neptune-equals-jupiter",
    "saturn-neptune-equals-mars",
    "saturn-neptune-equals-mc",
    "saturn-neptune-equals-mercury",
    "saturn-neptune-equals-moon",
    "saturn-neptune-equals-node",
    "saturn-neptune-equals-pluto",
    "saturn-neptune-equals-sun",
    "saturn-neptune-equals-uranus",
    "saturn-neptune-equals-venus",
}

SEEDED_SATURN_MC_ACTIVATION_CLUSTER = {
    "saturn-mc-equals-asc",
    "saturn-mc-equals-jupiter",
    "saturn-mc-equals-mars",
    "saturn-mc-equals-mercury",
    "saturn-mc-equals-moon",
    "saturn-mc-equals-neptune",
    "saturn-mc-equals-node",
    "saturn-mc-equals-pluto",
    "saturn-mc-equals-sun",
    "saturn-mc-equals-uranus",
    "saturn-mc-equals-venus",
}

SEEDED_SATURN_ASC_ACTIVATION_CLUSTER = {
    "saturn-asc-equals-jupiter",
    "saturn-asc-equals-mars",
    "saturn-asc-equals-mc",
    "saturn-asc-equals-mercury",
    "saturn-asc-equals-moon",
    "saturn-asc-equals-neptune",
    "saturn-asc-equals-node",
    "saturn-asc-equals-pluto",
    "saturn-asc-equals-sun",
    "saturn-asc-equals-uranus",
    "saturn-asc-equals-venus",
}

SEEDED_SATURN_URANUS_ACTIVATION_CLUSTER = {
    "saturn-uranus-equals-asc",
    "saturn-uranus-equals-jupiter",
    "saturn-uranus-equals-mars",
    "saturn-uranus-equals-mc",
    "saturn-uranus-equals-mercury",
    "saturn-uranus-equals-moon",
    "saturn-uranus-equals-neptune",
    "saturn-uranus-equals-node",
    "saturn-uranus-equals-pluto",
    "saturn-uranus-equals-sun",
    "saturn-uranus-equals-venus",
}

SEEDED_SATURN_PLUTO_ACTIVATION_CLUSTER = {
    "saturn-pluto-equals-asc",
    "saturn-pluto-equals-jupiter",
    "saturn-pluto-equals-mars",
    "saturn-pluto-equals-mc",
    "saturn-pluto-equals-mercury",
    "saturn-pluto-equals-moon",
    "saturn-pluto-equals-neptune",
    "saturn-pluto-equals-node",
    "saturn-pluto-equals-sun",
    "saturn-pluto-equals-uranus",
    "saturn-pluto-equals-venus",
}

SEEDED_SATURN_NODE_ACTIVATION_CLUSTER = {
    "saturn-node-equals-asc",
    "saturn-node-equals-jupiter",
    "saturn-node-equals-mars",
    "saturn-node-equals-mc",
    "saturn-node-equals-mercury",
    "saturn-node-equals-moon",
    "saturn-node-equals-neptune",
    "saturn-node-equals-pluto",
    "saturn-node-equals-sun",
    "saturn-node-equals-uranus",
    "saturn-node-equals-venus",
}

SEEDED_VENUS_NODE_ACTIVATION_CLUSTER = {
    "venus-node-equals-asc",
    "venus-node-equals-jupiter",
    "venus-node-equals-mars",
    "venus-node-equals-mc",
    "venus-node-equals-mercury",
    "venus-node-equals-moon",
    "venus-node-equals-neptune",
    "venus-node-equals-pluto",
    "venus-node-equals-saturn",
    "venus-node-equals-sun",
    "venus-node-equals-uranus",
}

SEEDED_VENUS_NEPTUNE_ACTIVATION_CLUSTER = {
    "venus-neptune-equals-asc",
    "venus-neptune-equals-jupiter",
    "venus-neptune-equals-mars",
    "venus-neptune-equals-mc",
    "venus-neptune-equals-mercury",
    "venus-neptune-equals-moon",
    "venus-neptune-equals-node",
    "venus-neptune-equals-pluto",
    "venus-neptune-equals-saturn",
    "venus-neptune-equals-sun",
    "venus-neptune-equals-uranus",
}

SEEDED_VENUS_MC_ACTIVATION_CLUSTER = {
    "venus-mc-equals-asc",
    "venus-mc-equals-jupiter",
    "venus-mc-equals-mars",
    "venus-mc-equals-mercury",
    "venus-mc-equals-moon",
    "venus-mc-equals-neptune",
    "venus-mc-equals-node",
    "venus-mc-equals-pluto",
    "venus-mc-equals-saturn",
    "venus-mc-equals-sun",
    "venus-mc-equals-uranus",
}

SEEDED_URANUS_NODE_ACTIVATION_CLUSTER = {
    "uranus-node-equals-asc",
    "uranus-node-equals-jupiter",
    "uranus-node-equals-mars",
    "uranus-node-equals-mc",
    "uranus-node-equals-mercury",
    "uranus-node-equals-moon",
    "uranus-node-equals-neptune",
    "uranus-node-equals-pluto",
    "uranus-node-equals-saturn",
    "uranus-node-equals-sun",
    "uranus-node-equals-venus",
}

SEEDED_URANUS_NEPTUNE_ACTIVATION_CLUSTER = {
    "uranus-neptune-equals-asc",
    "uranus-neptune-equals-jupiter",
    "uranus-neptune-equals-mars",
    "uranus-neptune-equals-mc",
    "uranus-neptune-equals-mercury",
    "uranus-neptune-equals-moon",
    "uranus-neptune-equals-node",
    "uranus-neptune-equals-pluto",
    "uranus-neptune-equals-saturn",
    "uranus-neptune-equals-sun",
    "uranus-neptune-equals-venus",
}

SEEDED_VENUS_ASC_ACTIVATION_CLUSTER = {
    "venus-asc-equals-jupiter",
    "venus-asc-equals-mars",
    "venus-asc-equals-mc",
    "venus-asc-equals-mercury",
    "venus-asc-equals-moon",
    "venus-asc-equals-neptune",
    "venus-asc-equals-node",
    "venus-asc-equals-pluto",
    "venus-asc-equals-saturn",
    "venus-asc-equals-sun",
    "venus-asc-equals-uranus",
}

SEEDED_MOON_ASC_ACTIVATION_CLUSTER = {
    "moon-asc-equals-jupiter",
    "moon-asc-equals-mars",
    "moon-asc-equals-mc",
    "moon-asc-equals-mercury",
    "moon-asc-equals-neptune",
    "moon-asc-equals-node",
    "moon-asc-equals-pluto",
    "moon-asc-equals-saturn",
    "moon-asc-equals-sun",
    "moon-asc-equals-uranus",
    "moon-asc-equals-venus",
}

SEEDED_MOON_JUPITER_ACTIVATION_CLUSTER = {
    "moon-jupiter-equals-asc",
    "moon-jupiter-equals-mars",
    "moon-jupiter-equals-mc",
    "moon-jupiter-equals-mercury",
    "moon-jupiter-equals-neptune",
    "moon-jupiter-equals-node",
    "moon-jupiter-equals-pluto",
    "moon-jupiter-equals-saturn",
    "moon-jupiter-equals-sun",
    "moon-jupiter-equals-uranus",
    "moon-jupiter-equals-venus",
}

SEEDED_MOON_MARS_ACTIVATION_CLUSTER = {
    "moon-mars-equals-asc",
    "moon-mars-equals-jupiter",
    "moon-mars-equals-mc",
    "moon-mars-equals-mercury",
    "moon-mars-equals-neptune",
    "moon-mars-equals-node",
    "moon-mars-equals-pluto",
    "moon-mars-equals-saturn",
    "moon-mars-equals-sun",
    "moon-mars-equals-uranus",
    "moon-mars-equals-venus",
}

SEEDED_MOON_MC_ACTIVATION_CLUSTER = {
    "moon-mc-equals-asc",
    "moon-mc-equals-jupiter",
    "moon-mc-equals-mars",
    "moon-mc-equals-mercury",
    "moon-mc-equals-neptune",
    "moon-mc-equals-node",
    "moon-mc-equals-pluto",
    "moon-mc-equals-saturn",
    "moon-mc-equals-sun",
    "moon-mc-equals-uranus",
    "moon-mc-equals-venus",
}

SEEDED_MOON_MERCURY_ACTIVATION_CLUSTER = {
    "moon-mercury-equals-asc",
    "moon-mercury-equals-jupiter",
    "moon-mercury-equals-mars",
    "moon-mercury-equals-mc",
    "moon-mercury-equals-neptune",
    "moon-mercury-equals-node",
    "moon-mercury-equals-pluto",
    "moon-mercury-equals-saturn",
    "moon-mercury-equals-sun",
    "moon-mercury-equals-uranus",
    "moon-mercury-equals-venus",
}

SEEDED_MOON_NEPTUNE_ACTIVATION_CLUSTER = {
    "moon-neptune-equals-asc",
    "moon-neptune-equals-jupiter",
    "moon-neptune-equals-mars",
    "moon-neptune-equals-mc",
    "moon-neptune-equals-mercury",
    "moon-neptune-equals-node",
    "moon-neptune-equals-pluto",
    "moon-neptune-equals-saturn",
    "moon-neptune-equals-sun",
    "moon-neptune-equals-uranus",
    "moon-neptune-equals-venus",
}

SEEDED_MOON_NODE_ACTIVATION_CLUSTER = {
    "moon-node-equals-asc",
    "moon-node-equals-jupiter",
    "moon-node-equals-mars",
    "moon-node-equals-mc",
    "moon-node-equals-mercury",
    "moon-node-equals-neptune",
    "moon-node-equals-pluto",
    "moon-node-equals-saturn",
    "moon-node-equals-sun",
    "moon-node-equals-uranus",
    "moon-node-equals-venus",
}

SEEDED_MOON_PLUTO_ACTIVATION_CLUSTER = {
    "moon-pluto-equals-asc",
    "moon-pluto-equals-jupiter",
    "moon-pluto-equals-mars",
    "moon-pluto-equals-mc",
    "moon-pluto-equals-mercury",
    "moon-pluto-equals-neptune",
    "moon-pluto-equals-node",
    "moon-pluto-equals-saturn",
    "moon-pluto-equals-sun",
    "moon-pluto-equals-uranus",
    "moon-pluto-equals-venus",
}

SEEDED_MOON_SATURN_ACTIVATION_CLUSTER = {
    "moon-saturn-equals-asc",
    "moon-saturn-equals-jupiter",
    "moon-saturn-equals-mars",
    "moon-saturn-equals-mc",
    "moon-saturn-equals-mercury",
    "moon-saturn-equals-neptune",
    "moon-saturn-equals-node",
    "moon-saturn-equals-pluto",
    "moon-saturn-equals-sun",
    "moon-saturn-equals-uranus",
    "moon-saturn-equals-venus",
}

SEEDED_MOON_URANUS_ACTIVATION_CLUSTER = {
    "moon-uranus-equals-asc",
    "moon-uranus-equals-jupiter",
    "moon-uranus-equals-mars",
    "moon-uranus-equals-mc",
    "moon-uranus-equals-mercury",
    "moon-uranus-equals-neptune",
    "moon-uranus-equals-node",
    "moon-uranus-equals-pluto",
    "moon-uranus-equals-saturn",
    "moon-uranus-equals-sun",
    "moon-uranus-equals-venus",
}

SEEDED_SUN_MOON_ACTIVATION_CLUSTER = {
    "sun-moon-equals-asc",
    "sun-moon-equals-jupiter",
    "sun-moon-equals-mars",
    "sun-moon-equals-mc",
    "sun-moon-equals-mercury",
    "sun-moon-equals-neptune",
    "sun-moon-equals-node",
    "sun-moon-equals-pluto",
    "sun-moon-equals-saturn",
    "sun-moon-equals-uranus",
    "sun-moon-equals-venus",
}

SEEDED_SUN_VENUS_ACTIVATION_CLUSTER = {
    "sun-venus-equals-asc",
    "sun-venus-equals-jupiter",
    "sun-venus-equals-mars",
    "sun-venus-equals-mc",
    "sun-venus-equals-mercury",
    "sun-venus-equals-moon",
    "sun-venus-equals-neptune",
    "sun-venus-equals-node",
    "sun-venus-equals-pluto",
    "sun-venus-equals-saturn",
    "sun-venus-equals-uranus",
}

SEEDED_MOON_VENUS_ACTIVATION_CLUSTER = {
    "moon-venus-equals-asc",
    "moon-venus-equals-jupiter",
    "moon-venus-equals-mars",
    "moon-venus-equals-mc",
    "moon-venus-equals-mercury",
    "moon-venus-equals-neptune",
    "moon-venus-equals-node",
    "moon-venus-equals-pluto",
    "moon-venus-equals-saturn",
    "moon-venus-equals-sun",
    "moon-venus-equals-uranus",
}

SEEDED_MERCURY_JUPITER_ACTIVATION_CLUSTER = {
    "mercury-jupiter-equals-asc",
    "mercury-jupiter-equals-mars",
    "mercury-jupiter-equals-mc",
    "mercury-jupiter-equals-moon",
    "mercury-jupiter-equals-neptune",
    "mercury-jupiter-equals-node",
    "mercury-jupiter-equals-pluto",
    "mercury-jupiter-equals-saturn",
    "mercury-jupiter-equals-sun",
    "mercury-jupiter-equals-uranus",
    "mercury-jupiter-equals-venus",
}

SEEDED_MERCURY_NEPTUNE_ACTIVATION_CLUSTER = {
    "mercury-neptune-equals-asc",
    "mercury-neptune-equals-jupiter",
    "mercury-neptune-equals-mars",
    "mercury-neptune-equals-mc",
    "mercury-neptune-equals-moon",
    "mercury-neptune-equals-node",
    "mercury-neptune-equals-pluto",
    "mercury-neptune-equals-saturn",
    "mercury-neptune-equals-sun",
    "mercury-neptune-equals-uranus",
    "mercury-neptune-equals-venus",
}

SEEDED_MERCURY_NODE_ACTIVATION_CLUSTER = {
    "mercury-node-equals-asc",
    "mercury-node-equals-jupiter",
    "mercury-node-equals-mars",
    "mercury-node-equals-mc",
    "mercury-node-equals-moon",
    "mercury-node-equals-neptune",
    "mercury-node-equals-pluto",
    "mercury-node-equals-saturn",
    "mercury-node-equals-sun",
    "mercury-node-equals-uranus",
    "mercury-node-equals-venus",
}

SEEDED_MERCURY_PLUTO_ACTIVATION_CLUSTER = {
    "mercury-pluto-equals-asc",
    "mercury-pluto-equals-jupiter",
    "mercury-pluto-equals-mars",
    "mercury-pluto-equals-mc",
    "mercury-pluto-equals-moon",
    "mercury-pluto-equals-neptune",
    "mercury-pluto-equals-node",
    "mercury-pluto-equals-saturn",
    "mercury-pluto-equals-sun",
    "mercury-pluto-equals-uranus",
    "mercury-pluto-equals-venus",
}

SEEDED_MERCURY_PLUTO_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-pluto-equals-admetos",
    "mercury-pluto-equals-apollon",
    "mercury-pluto-equals-chiron",
    "mercury-pluto-equals-cupido",
    "mercury-pluto-equals-hades",
    "mercury-pluto-equals-kronos",
    "mercury-pluto-equals-poseidon",
    "mercury-pluto-equals-vernal-point",
    "mercury-pluto-equals-vulcanus",
    "mercury-pluto-equals-zeus",
}

SEEDED_MERCURY_POSEIDON_FAMILY_CLUSTER = {
    "mercury-poseidon",
    "mercury-poseidon-equals-admetos",
    "mercury-poseidon-equals-apollon",
    "mercury-poseidon-equals-asc",
    "mercury-poseidon-equals-cupido",
    "mercury-poseidon-equals-hades",
    "mercury-poseidon-equals-jupiter",
    "mercury-poseidon-equals-kronos",
    "mercury-poseidon-equals-mars",
    "mercury-poseidon-equals-mc",
    "mercury-poseidon-equals-moon",
    "mercury-poseidon-equals-neptune",
    "mercury-poseidon-equals-node",
    "mercury-poseidon-equals-pluto",
    "mercury-poseidon-equals-saturn",
    "mercury-poseidon-equals-sun",
    "mercury-poseidon-equals-uranus",
    "mercury-poseidon-equals-venus",
    "mercury-poseidon-equals-vernal-point",
    "mercury-poseidon-equals-vulcanus",
    "mercury-poseidon-equals-zeus",
}

SEEDED_MERCURY_SATURN_ACTIVATION_CLUSTER = {
    "mercury-saturn-equals-asc",
    "mercury-saturn-equals-jupiter",
    "mercury-saturn-equals-mars",
    "mercury-saturn-equals-mc",
    "mercury-saturn-equals-moon",
    "mercury-saturn-equals-neptune",
    "mercury-saturn-equals-node",
    "mercury-saturn-equals-pluto",
    "mercury-saturn-equals-sun",
    "mercury-saturn-equals-uranus",
    "mercury-saturn-equals-venus",
}

SEEDED_MERCURY_SATURN_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-saturn-equals-admetos",
    "mercury-saturn-equals-apollon",
    "mercury-saturn-equals-chiron",
    "mercury-saturn-equals-cupido",
    "mercury-saturn-equals-hades",
    "mercury-saturn-equals-kronos",
    "mercury-saturn-equals-poseidon",
    "mercury-saturn-equals-vernal-point",
    "mercury-saturn-equals-vulcanus",
    "mercury-saturn-equals-zeus",
}

SEEDED_MERCURY_URANUS_ACTIVATION_CLUSTER = {
    "mercury-uranus-equals-asc",
    "mercury-uranus-equals-jupiter",
    "mercury-uranus-equals-mars",
    "mercury-uranus-equals-mc",
    "mercury-uranus-equals-moon",
    "mercury-uranus-equals-neptune",
    "mercury-uranus-equals-node",
    "mercury-uranus-equals-pluto",
    "mercury-uranus-equals-saturn",
    "mercury-uranus-equals-sun",
    "mercury-uranus-equals-venus",
}

SEEDED_MERCURY_URANUS_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-uranus-equals-admetos",
    "mercury-uranus-equals-apollon",
    "mercury-uranus-equals-chiron",
    "mercury-uranus-equals-cupido",
    "mercury-uranus-equals-hades",
    "mercury-uranus-equals-kronos",
    "mercury-uranus-equals-poseidon",
    "mercury-uranus-equals-vernal-point",
    "mercury-uranus-equals-vulcanus",
    "mercury-uranus-equals-zeus",
}

SEEDED_MERCURY_VENUS_ACTIVATION_CLUSTER = {
    "mercury-venus-equals-asc",
    "mercury-venus-equals-jupiter",
    "mercury-venus-equals-mars",
    "mercury-venus-equals-mc",
    "mercury-venus-equals-moon",
    "mercury-venus-equals-neptune",
    "mercury-venus-equals-node",
    "mercury-venus-equals-pluto",
    "mercury-venus-equals-saturn",
    "mercury-venus-equals-sun",
    "mercury-venus-equals-uranus",
}

SEEDED_MERCURY_VENUS_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-venus-equals-admetos",
    "mercury-venus-equals-apollon",
    "mercury-venus-equals-chiron",
    "mercury-venus-equals-cupido",
    "mercury-venus-equals-hades",
    "mercury-venus-equals-kronos",
    "mercury-venus-equals-poseidon",
    "mercury-venus-equals-vernal-point",
    "mercury-venus-equals-vulcanus",
    "mercury-venus-equals-zeus",
}

SEEDED_MERCURY_VULCANUS_FAMILY_CLUSTER = {
    "mercury-vulcanus",
    "mercury-vulcanus-equals-admetos",
    "mercury-vulcanus-equals-apollon",
    "mercury-vulcanus-equals-asc",
    "mercury-vulcanus-equals-cupido",
    "mercury-vulcanus-equals-hades",
    "mercury-vulcanus-equals-jupiter",
    "mercury-vulcanus-equals-kronos",
    "mercury-vulcanus-equals-mars",
    "mercury-vulcanus-equals-mc",
    "mercury-vulcanus-equals-moon",
    "mercury-vulcanus-equals-neptune",
    "mercury-vulcanus-equals-node",
    "mercury-vulcanus-equals-pluto",
    "mercury-vulcanus-equals-poseidon",
    "mercury-vulcanus-equals-saturn",
    "mercury-vulcanus-equals-sun",
    "mercury-vulcanus-equals-uranus",
    "mercury-vulcanus-equals-venus",
    "mercury-vulcanus-equals-vernal-point",
    "mercury-vulcanus-equals-zeus",
}

SEEDED_MERCURY_ZEUS_FAMILY_CLUSTER = {
    "mercury-zeus",
    "mercury-zeus-equals-admetos",
    "mercury-zeus-equals-apollon",
    "mercury-zeus-equals-asc",
    "mercury-zeus-equals-cupido",
    "mercury-zeus-equals-hades",
    "mercury-zeus-equals-jupiter",
    "mercury-zeus-equals-kronos",
    "mercury-zeus-equals-mars",
    "mercury-zeus-equals-mc",
    "mercury-zeus-equals-moon",
    "mercury-zeus-equals-neptune",
    "mercury-zeus-equals-node",
    "mercury-zeus-equals-pluto",
    "mercury-zeus-equals-poseidon",
    "mercury-zeus-equals-saturn",
    "mercury-zeus-equals-sun",
    "mercury-zeus-equals-uranus",
    "mercury-zeus-equals-venus",
    "mercury-zeus-equals-vernal-point",
    "mercury-zeus-equals-vulcanus",
}

SEEDED_MOON_ADMETOS_FAMILY_CLUSTER = {
    "moon-admetos",
    "moon-admetos-equals-apollon",
    "moon-admetos-equals-asc",
    "moon-admetos-equals-cupido",
    "moon-admetos-equals-hades",
    "moon-admetos-equals-jupiter",
    "moon-admetos-equals-kronos",
    "moon-admetos-equals-mars",
    "moon-admetos-equals-mc",
    "moon-admetos-equals-mercury",
    "moon-admetos-equals-neptune",
    "moon-admetos-equals-node",
    "moon-admetos-equals-pluto",
    "moon-admetos-equals-poseidon",
    "moon-admetos-equals-saturn",
    "moon-admetos-equals-sun",
    "moon-admetos-equals-uranus",
    "moon-admetos-equals-venus",
    "moon-admetos-equals-vernal-point",
    "moon-admetos-equals-vulcanus",
    "moon-admetos-equals-zeus",
}

SEEDED_MOON_APOLLON_FAMILY_CLUSTER = {
    "moon-apollon",
    "moon-apollon-equals-admetos",
    "moon-apollon-equals-asc",
    "moon-apollon-equals-cupido",
    "moon-apollon-equals-hades",
    "moon-apollon-equals-jupiter",
    "moon-apollon-equals-kronos",
    "moon-apollon-equals-mars",
    "moon-apollon-equals-mc",
    "moon-apollon-equals-mercury",
    "moon-apollon-equals-neptune",
    "moon-apollon-equals-node",
    "moon-apollon-equals-pluto",
    "moon-apollon-equals-poseidon",
    "moon-apollon-equals-saturn",
    "moon-apollon-equals-sun",
    "moon-apollon-equals-uranus",
    "moon-apollon-equals-venus",
    "moon-apollon-equals-vernal-point",
    "moon-apollon-equals-vulcanus",
    "moon-apollon-equals-zeus",
}

SEEDED_MOON_CUPIDO_FAMILY_CLUSTER = {
    "moon-cupido",
    "moon-cupido-equals-admetos",
    "moon-cupido-equals-apollon",
    "moon-cupido-equals-asc",
    "moon-cupido-equals-hades",
    "moon-cupido-equals-jupiter",
    "moon-cupido-equals-kronos",
    "moon-cupido-equals-mars",
    "moon-cupido-equals-mc",
    "moon-cupido-equals-mercury",
    "moon-cupido-equals-neptune",
    "moon-cupido-equals-node",
    "moon-cupido-equals-pluto",
    "moon-cupido-equals-poseidon",
    "moon-cupido-equals-saturn",
    "moon-cupido-equals-sun",
    "moon-cupido-equals-uranus",
    "moon-cupido-equals-venus",
    "moon-cupido-equals-vernal-point",
    "moon-cupido-equals-vulcanus",
    "moon-cupido-equals-zeus",
}

SEEDED_MOON_HADES_FAMILY_CLUSTER = {
    "moon-hades",
    "moon-hades-equals-admetos",
    "moon-hades-equals-apollon",
    "moon-hades-equals-asc",
    "moon-hades-equals-cupido",
    "moon-hades-equals-jupiter",
    "moon-hades-equals-kronos",
    "moon-hades-equals-mars",
    "moon-hades-equals-mc",
    "moon-hades-equals-mercury",
    "moon-hades-equals-neptune",
    "moon-hades-equals-node",
    "moon-hades-equals-pluto",
    "moon-hades-equals-poseidon",
    "moon-hades-equals-saturn",
    "moon-hades-equals-sun",
    "moon-hades-equals-uranus",
    "moon-hades-equals-venus",
    "moon-hades-equals-vernal-point",
    "moon-hades-equals-vulcanus",
    "moon-hades-equals-zeus",
}

SEEDED_MOON_KRONOS_FAMILY_CLUSTER = {
    "moon-kronos",
    "moon-kronos-equals-admetos",
    "moon-kronos-equals-apollon",
    "moon-kronos-equals-asc",
    "moon-kronos-equals-cupido",
    "moon-kronos-equals-hades",
    "moon-kronos-equals-jupiter",
    "moon-kronos-equals-mars",
    "moon-kronos-equals-mc",
    "moon-kronos-equals-mercury",
    "moon-kronos-equals-neptune",
    "moon-kronos-equals-node",
    "moon-kronos-equals-pluto",
    "moon-kronos-equals-poseidon",
    "moon-kronos-equals-saturn",
    "moon-kronos-equals-sun",
    "moon-kronos-equals-uranus",
    "moon-kronos-equals-venus",
    "moon-kronos-equals-vernal-point",
    "moon-kronos-equals-vulcanus",
    "moon-kronos-equals-zeus",
}

SEEDED_MOON_POSEIDON_FAMILY_CLUSTER = {
    "moon-poseidon",
    "moon-poseidon-equals-admetos",
    "moon-poseidon-equals-apollon",
    "moon-poseidon-equals-asc",
    "moon-poseidon-equals-cupido",
    "moon-poseidon-equals-hades",
    "moon-poseidon-equals-jupiter",
    "moon-poseidon-equals-kronos",
    "moon-poseidon-equals-mars",
    "moon-poseidon-equals-mc",
    "moon-poseidon-equals-mercury",
    "moon-poseidon-equals-neptune",
    "moon-poseidon-equals-node",
    "moon-poseidon-equals-pluto",
    "moon-poseidon-equals-saturn",
    "moon-poseidon-equals-sun",
    "moon-poseidon-equals-uranus",
    "moon-poseidon-equals-venus",
    "moon-poseidon-equals-vernal-point",
    "moon-poseidon-equals-vulcanus",
    "moon-poseidon-equals-zeus",
}

SEEDED_MOON_VULCANUS_FAMILY_CLUSTER = {
    "moon-vulcanus",
    "moon-vulcanus-equals-admetos",
    "moon-vulcanus-equals-apollon",
    "moon-vulcanus-equals-asc",
    "moon-vulcanus-equals-cupido",
    "moon-vulcanus-equals-hades",
    "moon-vulcanus-equals-jupiter",
    "moon-vulcanus-equals-kronos",
    "moon-vulcanus-equals-mars",
    "moon-vulcanus-equals-mc",
    "moon-vulcanus-equals-mercury",
    "moon-vulcanus-equals-neptune",
    "moon-vulcanus-equals-node",
    "moon-vulcanus-equals-pluto",
    "moon-vulcanus-equals-poseidon",
    "moon-vulcanus-equals-saturn",
    "moon-vulcanus-equals-sun",
    "moon-vulcanus-equals-uranus",
    "moon-vulcanus-equals-venus",
    "moon-vulcanus-equals-vernal-point",
    "moon-vulcanus-equals-zeus",
}

SEEDED_MOON_ZEUS_FAMILY_CLUSTER = {
    "moon-zeus",
    "moon-zeus-equals-admetos",
    "moon-zeus-equals-apollon",
    "moon-zeus-equals-asc",
    "moon-zeus-equals-cupido",
    "moon-zeus-equals-hades",
    "moon-zeus-equals-jupiter",
    "moon-zeus-equals-kronos",
    "moon-zeus-equals-mars",
    "moon-zeus-equals-mc",
    "moon-zeus-equals-mercury",
    "moon-zeus-equals-neptune",
    "moon-zeus-equals-node",
    "moon-zeus-equals-pluto",
    "moon-zeus-equals-poseidon",
    "moon-zeus-equals-saturn",
    "moon-zeus-equals-sun",
    "moon-zeus-equals-uranus",
    "moon-zeus-equals-venus",
    "moon-zeus-equals-vernal-point",
    "moon-zeus-equals-vulcanus",
}

SEEDED_MOON_CHIRON_FAMILY_CLUSTER = {
    "moon-chiron",
    "moon-chiron-equals-asc",
    "moon-chiron-equals-jupiter",
    "moon-chiron-equals-mars",
    "moon-chiron-equals-mc",
    "moon-chiron-equals-mercury",
    "moon-chiron-equals-neptune",
    "moon-chiron-equals-node",
    "moon-chiron-equals-pluto",
    "moon-chiron-equals-saturn",
    "moon-chiron-equals-sun",
    "moon-chiron-equals-uranus",
    "moon-chiron-equals-venus",
}

SEEDED_MOON_NEPTUNE_FACTOR_CLUSTER = {
    "moon",
    "neptune",
}

SEEDED_NEPTUNE_ASC_ACTIVATION_CLUSTER = {
    "neptune-asc-equals-admetos",
    "neptune-asc-equals-apollon",
    "neptune-asc-equals-chiron",
    "neptune-asc-equals-cupido",
    "neptune-asc-equals-hades",
    "neptune-asc-equals-jupiter",
    "neptune-asc-equals-kronos",
    "neptune-asc-equals-mars",
    "neptune-asc-equals-mc",
    "neptune-asc-equals-mercury",
    "neptune-asc-equals-moon",
    "neptune-asc-equals-node",
    "neptune-asc-equals-poseidon",
    "neptune-asc-equals-pluto",
    "neptune-asc-equals-saturn",
    "neptune-asc-equals-sun",
    "neptune-asc-equals-uranus",
    "neptune-asc-equals-venus",
    "neptune-asc-equals-vernal-point",
    "neptune-asc-equals-vulcanus",
    "neptune-asc-equals-zeus",
}

SEEDED_NEPTUNE_CUPIDO_CLUSTER = {
    "neptune-cupido",
    "neptune-cupido-equals-admetos",
    "neptune-cupido-equals-apollon",
    "neptune-cupido-equals-asc",
    "neptune-cupido-equals-hades",
    "neptune-cupido-equals-jupiter",
    "neptune-cupido-equals-kronos",
    "neptune-cupido-equals-mars",
    "neptune-cupido-equals-mc",
    "neptune-cupido-equals-mercury",
    "neptune-cupido-equals-moon",
    "neptune-cupido-equals-node",
    "neptune-cupido-equals-pluto",
    "neptune-cupido-equals-poseidon",
    "neptune-cupido-equals-saturn",
    "neptune-cupido-equals-sun",
    "neptune-cupido-equals-uranus",
    "neptune-cupido-equals-venus",
    "neptune-cupido-equals-vernal-point",
    "neptune-cupido-equals-vulcanus",
    "neptune-cupido-equals-zeus",
}

SEEDED_NEPTUNE_HADES_CLUSTER = {
    "neptune-hades",
    "neptune-hades-equals-admetos",
    "neptune-hades-equals-apollon",
    "neptune-hades-equals-asc",
    "neptune-hades-equals-cupido",
    "neptune-hades-equals-jupiter",
    "neptune-hades-equals-kronos",
    "neptune-hades-equals-mars",
    "neptune-hades-equals-mc",
    "neptune-hades-equals-mercury",
    "neptune-hades-equals-moon",
    "neptune-hades-equals-node",
    "neptune-hades-equals-pluto",
    "neptune-hades-equals-poseidon",
    "neptune-hades-equals-saturn",
    "neptune-hades-equals-sun",
    "neptune-hades-equals-uranus",
    "neptune-hades-equals-venus",
    "neptune-hades-equals-vernal-point",
    "neptune-hades-equals-vulcanus",
    "neptune-hades-equals-zeus",
}

SEEDED_NEPTUNE_MIXED_MAY02_CLUSTER = {
    "neptune-kronos",
    "neptune-pluto-equals-poseidon",
    "neptune-poseidon",
    "neptune-poseidon-equals-sun",
    "neptune-vulcanus",
    "neptune-vulcanus-equals-admetos",
    "neptune-vulcanus-equals-venus",
    "neptune-zeus",
}

SEEDED_NEPTUNE_KRONOS_RESIDUAL_CLUSTER = {
    "neptune-kronos-equals-admetos",
    "neptune-kronos-equals-apollon",
    "neptune-kronos-equals-asc",
    "neptune-kronos-equals-cupido",
    "neptune-kronos-equals-hades",
    "neptune-kronos-equals-jupiter",
    "neptune-kronos-equals-mars",
    "neptune-kronos-equals-mc",
    "neptune-kronos-equals-mercury",
    "neptune-kronos-equals-moon",
    "neptune-kronos-equals-node",
    "neptune-kronos-equals-pluto",
    "neptune-kronos-equals-poseidon",
    "neptune-kronos-equals-saturn",
    "neptune-kronos-equals-sun",
    "neptune-kronos-equals-uranus",
    "neptune-kronos-equals-venus",
    "neptune-kronos-equals-vernal-point",
    "neptune-kronos-equals-vulcanus",
    "neptune-kronos-equals-zeus",
}

SEEDED_NEPTUNE_MC_ACTIVATION_CLUSTER = {
    "neptune-mc-equals-admetos",
    "neptune-mc-equals-apollon",
    "neptune-mc-equals-asc",
    "neptune-mc-equals-chiron",
    "neptune-mc-equals-cupido",
    "neptune-mc-equals-hades",
    "neptune-mc-equals-jupiter",
    "neptune-mc-equals-kronos",
    "neptune-mc-equals-mars",
    "neptune-mc-equals-mercury",
    "neptune-mc-equals-moon",
    "neptune-mc-equals-node",
    "neptune-mc-equals-poseidon",
    "neptune-mc-equals-pluto",
    "neptune-mc-equals-saturn",
    "neptune-mc-equals-sun",
    "neptune-mc-equals-uranus",
    "neptune-mc-equals-venus",
    "neptune-mc-equals-vernal-point",
    "neptune-mc-equals-vulcanus",
    "neptune-mc-equals-zeus",
}

SEEDED_NEPTUNE_NEPTUNE_INITIAL_CLUSTER = {
    "neptune-neptune",
    "neptune-neptune-equals-admetos",
    "neptune-neptune-equals-apollon",
    "neptune-neptune-equals-asc",
    "neptune-neptune-equals-cupido",
    "neptune-neptune-equals-hades",
    "neptune-neptune-equals-jupiter",
    "neptune-neptune-equals-kronos",
    "neptune-neptune-equals-mars",
    "neptune-neptune-equals-mc",
    "neptune-neptune-equals-mercury",
    "neptune-neptune-equals-moon",
    "neptune-neptune-equals-node",
    "neptune-neptune-equals-pluto",
    "neptune-neptune-equals-poseidon",
    "neptune-neptune-equals-saturn",
    "neptune-neptune-equals-sun",
    "neptune-neptune-equals-uranus",
    "neptune-neptune-equals-venus",
    "neptune-neptune-equals-vernal-point",
    "neptune-neptune-equals-vulcanus",
    "neptune-neptune-equals-zeus",
}

SEEDED_NEPTUNE_NODE_ACTIVATION_CLUSTER = {
    "neptune-node-equals-admetos",
    "neptune-node-equals-apollon",
    "neptune-node-equals-asc",
    "neptune-node-equals-chiron",
    "neptune-node-equals-cupido",
    "neptune-node-equals-hades",
    "neptune-node-equals-jupiter",
    "neptune-node-equals-kronos",
    "neptune-node-equals-mars",
    "neptune-node-equals-mc",
    "neptune-node-equals-mercury",
    "neptune-node-equals-moon",
    "neptune-node-equals-poseidon",
    "neptune-node-equals-pluto",
    "neptune-node-equals-saturn",
    "neptune-node-equals-sun",
    "neptune-node-equals-uranus",
    "neptune-node-equals-venus",
    "neptune-node-equals-vernal-point",
    "neptune-node-equals-vulcanus",
    "neptune-node-equals-zeus",
}

SEEDED_NODE_FACTOR_CLUSTER = {
    "node",
}

SEEDED_NEPTUNE_PLUTO_ACTIVATION_CLUSTER = {
    "neptune-pluto-equals-admetos",
    "neptune-pluto-equals-apollon",
    "neptune-pluto-equals-asc",
    "neptune-pluto-equals-chiron",
    "neptune-pluto-equals-cupido",
    "neptune-pluto-equals-hades",
    "neptune-pluto-equals-jupiter",
    "neptune-pluto-equals-kronos",
    "neptune-pluto-equals-mars",
    "neptune-pluto-equals-mc",
    "neptune-pluto-equals-mercury",
    "neptune-pluto-equals-moon",
    "neptune-pluto-equals-node",
    "neptune-pluto-equals-saturn",
    "neptune-pluto-equals-sun",
    "neptune-pluto-equals-uranus",
    "neptune-pluto-equals-venus",
    "neptune-pluto-equals-vernal-point",
    "neptune-pluto-equals-vulcanus",
    "neptune-pluto-equals-zeus",
}

SEEDED_NEPTUNE_POSEIDON_ACTIVATION_CLUSTER = {
    "neptune-poseidon-equals-admetos",
    "neptune-poseidon-equals-apollon",
    "neptune-poseidon-equals-asc",
    "neptune-poseidon-equals-cupido",
    "neptune-poseidon-equals-hades",
    "neptune-poseidon-equals-jupiter",
    "neptune-poseidon-equals-kronos",
    "neptune-poseidon-equals-mars",
    "neptune-poseidon-equals-mc",
    "neptune-poseidon-equals-mercury",
    "neptune-poseidon-equals-moon",
    "neptune-poseidon-equals-node",
    "neptune-poseidon-equals-pluto",
    "neptune-poseidon-equals-saturn",
    "neptune-poseidon-equals-uranus",
    "neptune-poseidon-equals-venus",
    "neptune-poseidon-equals-vernal-point",
    "neptune-poseidon-equals-vulcanus",
    "neptune-poseidon-equals-zeus",
}

SEEDED_NEPTUNE_VULCANUS_RESIDUAL_CLUSTER = {
    "neptune-vulcanus-equals-apollon",
    "neptune-vulcanus-equals-asc",
    "neptune-vulcanus-equals-cupido",
    "neptune-vulcanus-equals-hades",
    "neptune-vulcanus-equals-jupiter",
}

SEEDED_NODE_ASC_ACTIVATION_CLUSTER = {
    "node-asc-equals-jupiter",
    "node-asc-equals-mars",
    "node-asc-equals-mc",
    "node-asc-equals-mercury",
    "node-asc-equals-moon",
    "node-asc-equals-neptune",
    "node-asc-equals-pluto",
    "node-asc-equals-saturn",
    "node-asc-equals-sun",
    "node-asc-equals-uranus",
    "node-asc-equals-venus",
}

SEEDED_NODE_MC_ACTIVATION_CLUSTER = {
    "node-mc-equals-asc",
    "node-mc-equals-jupiter",
    "node-mc-equals-mars",
    "node-mc-equals-mercury",
    "node-mc-equals-moon",
    "node-mc-equals-neptune",
    "node-mc-equals-pluto",
    "node-mc-equals-saturn",
    "node-mc-equals-sun",
    "node-mc-equals-uranus",
    "node-mc-equals-venus",
}

SEEDED_PLUTO_FACTOR_CLUSTER = {
    "pluto",
}

SEEDED_PLUTO_ASC_ACTIVATION_CLUSTER = {
    "pluto-asc-equals-jupiter",
    "pluto-asc-equals-mars",
    "pluto-asc-equals-mc",
    "pluto-asc-equals-mercury",
    "pluto-asc-equals-moon",
    "pluto-asc-equals-neptune",
    "pluto-asc-equals-node",
    "pluto-asc-equals-saturn",
    "pluto-asc-equals-sun",
    "pluto-asc-equals-uranus",
    "pluto-asc-equals-venus",
}

SEEDED_PLUTO_MC_ACTIVATION_CLUSTER = {
    "pluto-mc-equals-asc",
    "pluto-mc-equals-jupiter",
    "pluto-mc-equals-mars",
    "pluto-mc-equals-mercury",
    "pluto-mc-equals-moon",
    "pluto-mc-equals-neptune",
    "pluto-mc-equals-node",
    "pluto-mc-equals-saturn",
    "pluto-mc-equals-sun",
    "pluto-mc-equals-uranus",
    "pluto-mc-equals-venus",
}

SEEDED_PLUTO_NODE_ACTIVATION_CLUSTER = {
    "pluto-node-equals-asc",
    "pluto-node-equals-jupiter",
    "pluto-node-equals-mars",
    "pluto-node-equals-mc",
    "pluto-node-equals-mercury",
    "pluto-node-equals-moon",
    "pluto-node-equals-neptune",
    "pluto-node-equals-saturn",
    "pluto-node-equals-sun",
    "pluto-node-equals-uranus",
    "pluto-node-equals-venus",
}

SEEDED_SATURN_SUN_URANUS_FACTOR_CLUSTER = {
    "saturn",
    "sun",
    "uranus",
}

SEEDED_URANUS_PLUTO_ACTIVATION_CLUSTER = {
    "uranus-pluto-equals-asc",
    "uranus-pluto-equals-jupiter",
    "uranus-pluto-equals-mars",
    "uranus-pluto-equals-mc",
    "uranus-pluto-equals-mercury",
    "uranus-pluto-equals-moon",
    "uranus-pluto-equals-neptune",
    "uranus-pluto-equals-node",
    "uranus-pluto-equals-saturn",
    "uranus-pluto-equals-sun",
    "uranus-pluto-equals-venus",
}

SEEDED_VENUS_JUPITER_ACTIVATION_CLUSTER = {
    "venus-jupiter-equals-asc",
    "venus-jupiter-equals-mars",
    "venus-jupiter-equals-mc",
    "venus-jupiter-equals-mercury",
    "venus-jupiter-equals-moon",
    "venus-jupiter-equals-neptune",
    "venus-jupiter-equals-node",
    "venus-jupiter-equals-pluto",
    "venus-jupiter-equals-saturn",
    "venus-jupiter-equals-sun",
    "venus-jupiter-equals-uranus",
}

SEEDED_VENUS_MARS_ACTIVATION_CLUSTER = {
    "venus-mars-equals-asc",
    "venus-mars-equals-jupiter",
    "venus-mars-equals-mc",
    "venus-mars-equals-mercury",
    "venus-mars-equals-moon",
    "venus-mars-equals-neptune",
    "venus-mars-equals-node",
    "venus-mars-equals-pluto",
    "venus-mars-equals-saturn",
    "venus-mars-equals-sun",
    "venus-mars-equals-uranus",
}

SEEDED_VENUS_FACTOR_CLUSTER = {
    "venus",
}

SEEDED_VENUS_PLUTO_ACTIVATION_CLUSTER = {
    "venus-pluto-equals-asc",
    "venus-pluto-equals-jupiter",
    "venus-pluto-equals-mars",
    "venus-pluto-equals-mc",
    "venus-pluto-equals-mercury",
    "venus-pluto-equals-moon",
    "venus-pluto-equals-neptune",
    "venus-pluto-equals-node",
    "venus-pluto-equals-saturn",
    "venus-pluto-equals-sun",
    "venus-pluto-equals-uranus",
}

SEEDED_VENUS_SATURN_ACTIVATION_CLUSTER = {
    "venus-saturn-equals-asc",
    "venus-saturn-equals-jupiter",
    "venus-saturn-equals-mars",
    "venus-saturn-equals-mc",
    "venus-saturn-equals-mercury",
    "venus-saturn-equals-moon",
    "venus-saturn-equals-neptune",
    "venus-saturn-equals-node",
    "venus-saturn-equals-pluto",
    "venus-saturn-equals-sun",
    "venus-saturn-equals-uranus",
}

SEEDED_VENUS_URANUS_ACTIVATION_CLUSTER = {
    "venus-uranus-equals-asc",
    "venus-uranus-equals-jupiter",
    "venus-uranus-equals-mars",
    "venus-uranus-equals-mc",
    "venus-uranus-equals-mercury",
    "venus-uranus-equals-moon",
    "venus-uranus-equals-neptune",
    "venus-uranus-equals-node",
    "venus-uranus-equals-pluto",
    "venus-uranus-equals-saturn",
    "venus-uranus-equals-sun",
}

SEEDED_VERNAL_POINT_FACTOR_CLUSTER = {
    "vernal-point",
}

SEEDED_VERNAL_POINT_AXIS_CLUSTER = {
    "vernal-point-asc",
    "vernal-point-jupiter",
    "vernal-point-mars",
    "vernal-point-mc",
    "vernal-point-mercury",
    "vernal-point-moon",
    "vernal-point-neptune",
    "vernal-point-node",
    "vernal-point-pluto",
    "vernal-point-saturn",
    "vernal-point-sun",
    "vernal-point-uranus",
    "vernal-point-venus",
}

SEEDED_ADMETOS_FACTOR_CLUSTER = {
    "admetos",
}

SEEDED_ADMETOS_ADMETOS_AXIS_CLUSTER = {
    "admetos-admetos",
}

SEEDED_ADMETOS_ADMETOS_ACTIVATION_CLUSTER = {
    "admetos-admetos-equals-apollon",
    "admetos-admetos-equals-asc",
    "admetos-admetos-equals-cupido",
    "admetos-admetos-equals-hades",
    "admetos-admetos-equals-jupiter",
    "admetos-admetos-equals-kronos",
    "admetos-admetos-equals-mars",
    "admetos-admetos-equals-mc",
    "admetos-admetos-equals-mercury",
    "admetos-admetos-equals-moon",
    "admetos-admetos-equals-neptune",
    "admetos-admetos-equals-node",
    "admetos-admetos-equals-pluto",
    "admetos-admetos-equals-poseidon",
    "admetos-admetos-equals-saturn",
    "admetos-admetos-equals-sun",
    "admetos-admetos-equals-uranus",
    "admetos-admetos-equals-venus",
    "admetos-admetos-equals-vernal-point",
    "admetos-admetos-equals-vulcanus",
    "admetos-admetos-equals-zeus",
}

SEEDED_ADMETOS_POSEIDON_AXIS_CLUSTER = {
    "admetos-poseidon",
}

SEEDED_ADMETOS_POSEIDON_ACTIVATION_CLUSTER = {
    "admetos-poseidon-equals-apollon",
    "admetos-poseidon-equals-asc",
    "admetos-poseidon-equals-cupido",
    "admetos-poseidon-equals-hades",
    "admetos-poseidon-equals-jupiter",
    "admetos-poseidon-equals-kronos",
    "admetos-poseidon-equals-mars",
    "admetos-poseidon-equals-mc",
    "admetos-poseidon-equals-mercury",
    "admetos-poseidon-equals-moon",
    "admetos-poseidon-equals-neptune",
    "admetos-poseidon-equals-node",
    "admetos-poseidon-equals-pluto",
    "admetos-poseidon-equals-saturn",
    "admetos-poseidon-equals-sun",
    "admetos-poseidon-equals-uranus",
    "admetos-poseidon-equals-venus",
    "admetos-poseidon-equals-vernal-point",
    "admetos-poseidon-equals-vulcanus",
    "admetos-poseidon-equals-zeus",
}

SEEDED_ADMETOS_VULCANUS_AXIS_CLUSTER = {
    "admetos-vulcanus",
}

SEEDED_ADMETOS_VULCANUS_ACTIVATION_CLUSTER = {
    "admetos-vulcanus-equals-apollon",
    "admetos-vulcanus-equals-asc",
    "admetos-vulcanus-equals-cupido",
    "admetos-vulcanus-equals-hades",
    "admetos-vulcanus-equals-jupiter",
    "admetos-vulcanus-equals-kronos",
    "admetos-vulcanus-equals-mars",
    "admetos-vulcanus-equals-mc",
    "admetos-vulcanus-equals-mercury",
    "admetos-vulcanus-equals-moon",
    "admetos-vulcanus-equals-neptune",
    "admetos-vulcanus-equals-node",
    "admetos-vulcanus-equals-pluto",
    "admetos-vulcanus-equals-poseidon",
    "admetos-vulcanus-equals-saturn",
    "admetos-vulcanus-equals-sun",
    "admetos-vulcanus-equals-uranus",
    "admetos-vulcanus-equals-venus",
    "admetos-vulcanus-equals-vernal-point",
    "admetos-vulcanus-equals-zeus",
}

SEEDED_APOLLON_FACTOR_CLUSTER = {
    "apollon",
}

SEEDED_CUPIDO_FACTOR_CLUSTER = {
    "cupido",
}

SEEDED_HADES_FACTOR_CLUSTER = {
    "hades",
}

SEEDED_KRONOS_FACTOR_CLUSTER = {
    "kronos",
}

SEEDED_APOLLON_ADMETOS_AXIS_CLUSTER = {
    "apollon-admetos",
}

SEEDED_APOLLON_ADMETOS_ACTIVATION_CLUSTER = {
    "apollon-admetos-equals-asc",
    "apollon-admetos-equals-cupido",
    "apollon-admetos-equals-hades",
    "apollon-admetos-equals-jupiter",
    "apollon-admetos-equals-kronos",
    "apollon-admetos-equals-mars",
    "apollon-admetos-equals-mc",
    "apollon-admetos-equals-mercury",
    "apollon-admetos-equals-moon",
    "apollon-admetos-equals-neptune",
    "apollon-admetos-equals-node",
    "apollon-admetos-equals-pluto",
    "apollon-admetos-equals-poseidon",
    "apollon-admetos-equals-saturn",
    "apollon-admetos-equals-sun",
    "apollon-admetos-equals-uranus",
    "apollon-admetos-equals-venus",
    "apollon-admetos-equals-vernal-point",
    "apollon-admetos-equals-vulcanus",
    "apollon-admetos-equals-zeus",
}

SEEDED_APOLLON_APOLLON_AXIS_CLUSTER = {
    "apollon-apollon",
}

SEEDED_APOLLON_APOLLON_ACTIVATION_CLUSTER = {
    "apollon-apollon-equals-admetos",
    "apollon-apollon-equals-asc",
    "apollon-apollon-equals-cupido",
    "apollon-apollon-equals-hades",
    "apollon-apollon-equals-jupiter",
    "apollon-apollon-equals-kronos",
    "apollon-apollon-equals-mars",
    "apollon-apollon-equals-mc",
    "apollon-apollon-equals-mercury",
    "apollon-apollon-equals-moon",
    "apollon-apollon-equals-neptune",
    "apollon-apollon-equals-node",
    "apollon-apollon-equals-pluto",
    "apollon-apollon-equals-poseidon",
    "apollon-apollon-equals-saturn",
    "apollon-apollon-equals-sun",
    "apollon-apollon-equals-uranus",
    "apollon-apollon-equals-venus",
    "apollon-apollon-equals-vernal-point",
    "apollon-apollon-equals-vulcanus",
    "apollon-apollon-equals-zeus",
}

SEEDED_APOLLON_POSEIDON_AXIS_CLUSTER = {
    "apollon-poseidon",
}

SEEDED_APOLLON_POSEIDON_ACTIVATION_CLUSTER = {
    "apollon-poseidon-equals-admetos",
    "apollon-poseidon-equals-asc",
    "apollon-poseidon-equals-cupido",
    "apollon-poseidon-equals-hades",
    "apollon-poseidon-equals-jupiter",
    "apollon-poseidon-equals-kronos",
    "apollon-poseidon-equals-mars",
    "apollon-poseidon-equals-mc",
    "apollon-poseidon-equals-mercury",
    "apollon-poseidon-equals-moon",
    "apollon-poseidon-equals-neptune",
    "apollon-poseidon-equals-node",
    "apollon-poseidon-equals-pluto",
    "apollon-poseidon-equals-saturn",
    "apollon-poseidon-equals-sun",
    "apollon-poseidon-equals-uranus",
    "apollon-poseidon-equals-venus",
    "apollon-poseidon-equals-vernal-point",
    "apollon-poseidon-equals-vulcanus",
    "apollon-poseidon-equals-zeus",
}

SEEDED_APOLLON_VULCANUS_AXIS_CLUSTER = {
    "apollon-vulcanus",
}

SEEDED_APOLLON_VULCANUS_ACTIVATION_CLUSTER = {
    "apollon-vulcanus-equals-admetos",
    "apollon-vulcanus-equals-asc",
    "apollon-vulcanus-equals-cupido",
    "apollon-vulcanus-equals-hades",
    "apollon-vulcanus-equals-jupiter",
    "apollon-vulcanus-equals-kronos",
    "apollon-vulcanus-equals-mars",
    "apollon-vulcanus-equals-mc",
    "apollon-vulcanus-equals-mercury",
    "apollon-vulcanus-equals-moon",
    "apollon-vulcanus-equals-neptune",
    "apollon-vulcanus-equals-node",
    "apollon-vulcanus-equals-pluto",
    "apollon-vulcanus-equals-poseidon",
    "apollon-vulcanus-equals-saturn",
    "apollon-vulcanus-equals-sun",
    "apollon-vulcanus-equals-uranus",
    "apollon-vulcanus-equals-venus",
    "apollon-vulcanus-equals-vernal-point",
    "apollon-vulcanus-equals-zeus",
}

SEEDED_ASC_ADMETOS_AXIS_CLUSTER = {
    "asc-admetos",
}

SEEDED_ASC_ADMETOS_ACTIVATION_CLUSTER = {
    "asc-admetos-equals-apollon",
    "asc-admetos-equals-cupido",
    "asc-admetos-equals-hades",
    "asc-admetos-equals-jupiter",
    "asc-admetos-equals-kronos",
    "asc-admetos-equals-mars",
    "asc-admetos-equals-mc",
    "asc-admetos-equals-mercury",
    "asc-admetos-equals-moon",
    "asc-admetos-equals-neptune",
    "asc-admetos-equals-node",
    "asc-admetos-equals-pluto",
    "asc-admetos-equals-poseidon",
    "asc-admetos-equals-saturn",
    "asc-admetos-equals-sun",
    "asc-admetos-equals-uranus",
    "asc-admetos-equals-venus",
    "asc-admetos-equals-vernal-point",
    "asc-admetos-equals-vulcanus",
    "asc-admetos-equals-zeus",
}

SEEDED_ASC_APOLLON_AXIS_CLUSTER = {
    "asc-apollon",
}

SEEDED_ASC_APOLLON_ACTIVATION_CLUSTER = {
    "asc-apollon-equals-admetos",
    "asc-apollon-equals-cupido",
    "asc-apollon-equals-hades",
    "asc-apollon-equals-jupiter",
    "asc-apollon-equals-kronos",
    "asc-apollon-equals-mars",
    "asc-apollon-equals-mc",
    "asc-apollon-equals-mercury",
    "asc-apollon-equals-moon",
    "asc-apollon-equals-neptune",
    "asc-apollon-equals-node",
    "asc-apollon-equals-pluto",
    "asc-apollon-equals-poseidon",
    "asc-apollon-equals-saturn",
    "asc-apollon-equals-sun",
    "asc-apollon-equals-uranus",
    "asc-apollon-equals-venus",
    "asc-apollon-equals-vernal-point",
    "asc-apollon-equals-vulcanus",
    "asc-apollon-equals-zeus",
}

SEEDED_ASC_ASC_AXIS_CLUSTER = {
    "asc-asc",
}

SEEDED_ASC_ASC_ACTIVATION_CLUSTER = {
    "asc-asc-equals-admetos",
    "asc-asc-equals-apollon",
    "asc-asc-equals-cupido",
    "asc-asc-equals-hades",
    "asc-asc-equals-jupiter",
    "asc-asc-equals-kronos",
    "asc-asc-equals-mars",
    "asc-asc-equals-mc",
    "asc-asc-equals-mercury",
    "asc-asc-equals-moon",
    "asc-asc-equals-neptune",
    "asc-asc-equals-node",
    "asc-asc-equals-pluto",
    "asc-asc-equals-poseidon",
    "asc-asc-equals-saturn",
    "asc-asc-equals-sun",
    "asc-asc-equals-uranus",
    "asc-asc-equals-venus",
    "asc-asc-equals-vernal-point",
    "asc-asc-equals-vulcanus",
    "asc-asc-equals-zeus",
}

SEEDED_ASC_CUPIDO_AXIS_CLUSTER = {
    "asc-cupido",
}

SEEDED_ASC_CUPIDO_ACTIVATION_CLUSTER = {
    "asc-cupido-equals-admetos",
    "asc-cupido-equals-apollon",
    "asc-cupido-equals-hades",
    "asc-cupido-equals-jupiter",
    "asc-cupido-equals-kronos",
    "asc-cupido-equals-mars",
    "asc-cupido-equals-mc",
    "asc-cupido-equals-mercury",
    "asc-cupido-equals-moon",
    "asc-cupido-equals-neptune",
    "asc-cupido-equals-node",
    "asc-cupido-equals-pluto",
    "asc-cupido-equals-poseidon",
    "asc-cupido-equals-saturn",
    "asc-cupido-equals-sun",
    "asc-cupido-equals-uranus",
    "asc-cupido-equals-venus",
    "asc-cupido-equals-vernal-point",
    "asc-cupido-equals-vulcanus",
    "asc-cupido-equals-zeus",
}

SEEDED_ASC_HADES_AXIS_CLUSTER = {
    "asc-hades",
}

SEEDED_ASC_HADES_ACTIVATION_CLUSTER = {
    "asc-hades-equals-admetos",
    "asc-hades-equals-apollon",
    "asc-hades-equals-cupido",
    "asc-hades-equals-jupiter",
    "asc-hades-equals-kronos",
    "asc-hades-equals-mars",
    "asc-hades-equals-mc",
    "asc-hades-equals-mercury",
    "asc-hades-equals-moon",
    "asc-hades-equals-neptune",
    "asc-hades-equals-node",
    "asc-hades-equals-pluto",
    "asc-hades-equals-poseidon",
    "asc-hades-equals-saturn",
    "asc-hades-equals-sun",
    "asc-hades-equals-uranus",
    "asc-hades-equals-venus",
    "asc-hades-equals-vernal-point",
    "asc-hades-equals-vulcanus",
    "asc-hades-equals-zeus",
}

SEEDED_ASC_KRONOS_AXIS_CLUSTER = {
    "asc-kronos",
}

SEEDED_ASC_KRONOS_ACTIVATION_CLUSTER = {
    "asc-kronos-equals-admetos",
    "asc-kronos-equals-apollon",
    "asc-kronos-equals-cupido",
    "asc-kronos-equals-hades",
    "asc-kronos-equals-jupiter",
    "asc-kronos-equals-mars",
    "asc-kronos-equals-mc",
    "asc-kronos-equals-mercury",
    "asc-kronos-equals-moon",
    "asc-kronos-equals-neptune",
    "asc-kronos-equals-node",
    "asc-kronos-equals-pluto",
    "asc-kronos-equals-poseidon",
    "asc-kronos-equals-saturn",
    "asc-kronos-equals-sun",
    "asc-kronos-equals-uranus",
    "asc-kronos-equals-venus",
    "asc-kronos-equals-vernal-point",
    "asc-kronos-equals-vulcanus",
    "asc-kronos-equals-zeus",
}

SEEDED_ASC_POSEIDON_AXIS_CLUSTER = {
    "asc-poseidon",
}

SEEDED_ASC_POSEIDON_ACTIVATION_CLUSTER = {
    "asc-poseidon-equals-admetos",
    "asc-poseidon-equals-apollon",
    "asc-poseidon-equals-cupido",
    "asc-poseidon-equals-hades",
    "asc-poseidon-equals-jupiter",
    "asc-poseidon-equals-kronos",
    "asc-poseidon-equals-mars",
    "asc-poseidon-equals-mc",
    "asc-poseidon-equals-mercury",
    "asc-poseidon-equals-moon",
    "asc-poseidon-equals-neptune",
    "asc-poseidon-equals-node",
    "asc-poseidon-equals-pluto",
    "asc-poseidon-equals-saturn",
    "asc-poseidon-equals-sun",
    "asc-poseidon-equals-uranus",
    "asc-poseidon-equals-venus",
    "asc-poseidon-equals-vernal-point",
    "asc-poseidon-equals-vulcanus",
    "asc-poseidon-equals-zeus",
}

SEEDED_ASC_VULCANUS_AXIS_CLUSTER = {
    "asc-vulcanus",
}

SEEDED_ASC_VULCANUS_ACTIVATION_CLUSTER = {
    "asc-vulcanus-equals-admetos",
    "asc-vulcanus-equals-apollon",
    "asc-vulcanus-equals-cupido",
    "asc-vulcanus-equals-hades",
    "asc-vulcanus-equals-jupiter",
    "asc-vulcanus-equals-kronos",
    "asc-vulcanus-equals-mars",
    "asc-vulcanus-equals-mc",
    "asc-vulcanus-equals-mercury",
    "asc-vulcanus-equals-moon",
    "asc-vulcanus-equals-neptune",
    "asc-vulcanus-equals-node",
    "asc-vulcanus-equals-pluto",
    "asc-vulcanus-equals-poseidon",
    "asc-vulcanus-equals-saturn",
    "asc-vulcanus-equals-sun",
    "asc-vulcanus-equals-uranus",
    "asc-vulcanus-equals-venus",
    "asc-vulcanus-equals-vernal-point",
    "asc-vulcanus-equals-zeus",
}

SEEDED_ASC_ZEUS_AXIS_CLUSTER = {
    "asc-zeus",
}

SEEDED_ASC_ZEUS_ACTIVATION_CLUSTER = {
    "asc-zeus-equals-admetos",
    "asc-zeus-equals-apollon",
    "asc-zeus-equals-cupido",
    "asc-zeus-equals-hades",
    "asc-zeus-equals-jupiter",
    "asc-zeus-equals-kronos",
    "asc-zeus-equals-mars",
    "asc-zeus-equals-mc",
    "asc-zeus-equals-mercury",
    "asc-zeus-equals-moon",
    "asc-zeus-equals-neptune",
    "asc-zeus-equals-node",
    "asc-zeus-equals-pluto",
    "asc-zeus-equals-poseidon",
    "asc-zeus-equals-saturn",
    "asc-zeus-equals-sun",
    "asc-zeus-equals-uranus",
    "asc-zeus-equals-venus",
    "asc-zeus-equals-vernal-point",
    "asc-zeus-equals-vulcanus",
}

SEEDED_CHIRON_ASC_AXIS_CLUSTER = {
    "chiron-asc",
}

SEEDED_CHIRON_ASC_ACTIVATION_CLUSTER = {
    "chiron-asc-equals-jupiter",
    "chiron-asc-equals-mars",
    "chiron-asc-equals-mc",
    "chiron-asc-equals-mercury",
    "chiron-asc-equals-moon",
    "chiron-asc-equals-neptune",
    "chiron-asc-equals-node",
    "chiron-asc-equals-pluto",
    "chiron-asc-equals-saturn",
    "chiron-asc-equals-sun",
    "chiron-asc-equals-uranus",
    "chiron-asc-equals-venus",
}

SEEDED_CHIRON_MC_AXIS_CLUSTER = {
    "chiron-mc",
}

SEEDED_CHIRON_MC_ACTIVATION_CLUSTER = {
    "chiron-mc-equals-asc",
    "chiron-mc-equals-jupiter",
    "chiron-mc-equals-mars",
    "chiron-mc-equals-mercury",
    "chiron-mc-equals-moon",
    "chiron-mc-equals-neptune",
    "chiron-mc-equals-node",
    "chiron-mc-equals-pluto",
    "chiron-mc-equals-saturn",
    "chiron-mc-equals-sun",
    "chiron-mc-equals-uranus",
    "chiron-mc-equals-venus",
}

SEEDED_CHIRON_NEPTUNE_AXIS_CLUSTER = {
    "chiron-neptune",
}

SEEDED_CHIRON_NEPTUNE_ACTIVATION_CLUSTER = {
    "chiron-neptune-equals-asc",
    "chiron-neptune-equals-jupiter",
    "chiron-neptune-equals-mars",
    "chiron-neptune-equals-mc",
    "chiron-neptune-equals-mercury",
    "chiron-neptune-equals-moon",
    "chiron-neptune-equals-node",
    "chiron-neptune-equals-pluto",
    "chiron-neptune-equals-saturn",
    "chiron-neptune-equals-sun",
    "chiron-neptune-equals-uranus",
    "chiron-neptune-equals-venus",
}

SEEDED_CHIRON_NODE_AXIS_CLUSTER = {
    "chiron-node",
}

SEEDED_CHIRON_NODE_ACTIVATION_CLUSTER = {
    "chiron-node-equals-asc",
    "chiron-node-equals-jupiter",
    "chiron-node-equals-mars",
    "chiron-node-equals-mc",
    "chiron-node-equals-mercury",
    "chiron-node-equals-moon",
    "chiron-node-equals-neptune",
    "chiron-node-equals-pluto",
    "chiron-node-equals-saturn",
    "chiron-node-equals-sun",
    "chiron-node-equals-uranus",
    "chiron-node-equals-venus",
}

SEEDED_CHIRON_PLUTO_AXIS_CLUSTER = {
    "chiron-pluto",
}

SEEDED_CHIRON_PLUTO_ACTIVATION_CLUSTER = {
    "chiron-pluto-equals-asc",
    "chiron-pluto-equals-jupiter",
    "chiron-pluto-equals-mars",
    "chiron-pluto-equals-mc",
    "chiron-pluto-equals-mercury",
    "chiron-pluto-equals-moon",
    "chiron-pluto-equals-neptune",
    "chiron-pluto-equals-node",
    "chiron-pluto-equals-saturn",
    "chiron-pluto-equals-sun",
    "chiron-pluto-equals-uranus",
    "chiron-pluto-equals-venus",
}

SEEDED_CHIRON_URANUS_AXIS_CLUSTER = {
    "chiron-uranus",
}

SEEDED_CHIRON_URANUS_ACTIVATION_CLUSTER = {
    "chiron-uranus-equals-asc",
    "chiron-uranus-equals-jupiter",
    "chiron-uranus-equals-mars",
    "chiron-uranus-equals-mc",
    "chiron-uranus-equals-mercury",
    "chiron-uranus-equals-moon",
    "chiron-uranus-equals-neptune",
    "chiron-uranus-equals-node",
    "chiron-uranus-equals-pluto",
    "chiron-uranus-equals-saturn",
    "chiron-uranus-equals-sun",
    "chiron-uranus-equals-venus",
}

SEEDED_CUPIDO_ADMETOS_AXIS_CLUSTER = {
    "cupido-admetos",
}

SEEDED_CUPIDO_ADMETOS_ACTIVATION_CLUSTER = {
    "cupido-admetos-equals-apollon",
    "cupido-admetos-equals-asc",
    "cupido-admetos-equals-hades",
    "cupido-admetos-equals-jupiter",
    "cupido-admetos-equals-kronos",
    "cupido-admetos-equals-mars",
    "cupido-admetos-equals-mc",
    "cupido-admetos-equals-mercury",
    "cupido-admetos-equals-moon",
    "cupido-admetos-equals-neptune",
    "cupido-admetos-equals-node",
    "cupido-admetos-equals-pluto",
    "cupido-admetos-equals-poseidon",
    "cupido-admetos-equals-saturn",
    "cupido-admetos-equals-sun",
    "cupido-admetos-equals-uranus",
    "cupido-admetos-equals-venus",
    "cupido-admetos-equals-vernal-point",
    "cupido-admetos-equals-vulcanus",
    "cupido-admetos-equals-zeus",
}

SEEDED_CUPIDO_APOLLON_AXIS_CLUSTER = {
    "cupido-apollon",
}

SEEDED_CUPIDO_APOLLON_ACTIVATION_CLUSTER = {
    "cupido-apollon-equals-admetos",
    "cupido-apollon-equals-asc",
    "cupido-apollon-equals-hades",
    "cupido-apollon-equals-jupiter",
    "cupido-apollon-equals-kronos",
    "cupido-apollon-equals-mars",
    "cupido-apollon-equals-mc",
    "cupido-apollon-equals-mercury",
    "cupido-apollon-equals-moon",
    "cupido-apollon-equals-neptune",
    "cupido-apollon-equals-node",
    "cupido-apollon-equals-pluto",
    "cupido-apollon-equals-poseidon",
    "cupido-apollon-equals-saturn",
    "cupido-apollon-equals-sun",
    "cupido-apollon-equals-uranus",
    "cupido-apollon-equals-venus",
    "cupido-apollon-equals-vernal-point",
    "cupido-apollon-equals-vulcanus",
    "cupido-apollon-equals-zeus",
}

SEEDED_CUPIDO_CUPIDO_AXIS_CLUSTER = {
    "cupido-cupido",
}

SEEDED_CUPIDO_CUPIDO_ACTIVATION_CLUSTER = {
    "cupido-cupido-equals-admetos",
    "cupido-cupido-equals-apollon",
    "cupido-cupido-equals-asc",
    "cupido-cupido-equals-hades",
    "cupido-cupido-equals-jupiter",
    "cupido-cupido-equals-kronos",
    "cupido-cupido-equals-mars",
    "cupido-cupido-equals-mc",
    "cupido-cupido-equals-mercury",
    "cupido-cupido-equals-moon",
    "cupido-cupido-equals-neptune",
    "cupido-cupido-equals-node",
    "cupido-cupido-equals-pluto",
    "cupido-cupido-equals-poseidon",
    "cupido-cupido-equals-saturn",
    "cupido-cupido-equals-sun",
    "cupido-cupido-equals-uranus",
    "cupido-cupido-equals-venus",
    "cupido-cupido-equals-vernal-point",
    "cupido-cupido-equals-vulcanus",
    "cupido-cupido-equals-zeus",
}

SEEDED_CUPIDO_HADES_AXIS_CLUSTER = {
    "cupido-hades",
}

SEEDED_CUPIDO_HADES_ACTIVATION_CLUSTER = {
    "cupido-hades-equals-admetos",
    "cupido-hades-equals-apollon",
    "cupido-hades-equals-asc",
    "cupido-hades-equals-jupiter",
    "cupido-hades-equals-kronos",
    "cupido-hades-equals-mars",
    "cupido-hades-equals-mc",
    "cupido-hades-equals-mercury",
    "cupido-hades-equals-moon",
    "cupido-hades-equals-neptune",
    "cupido-hades-equals-node",
    "cupido-hades-equals-pluto",
    "cupido-hades-equals-poseidon",
    "cupido-hades-equals-saturn",
    "cupido-hades-equals-sun",
    "cupido-hades-equals-uranus",
    "cupido-hades-equals-venus",
    "cupido-hades-equals-vernal-point",
    "cupido-hades-equals-vulcanus",
    "cupido-hades-equals-zeus",
}

SEEDED_CUPIDO_KRONOS_AXIS_CLUSTER = {
    "cupido-kronos",
}

SEEDED_CUPIDO_KRONOS_ACTIVATION_CLUSTER = {
    "cupido-kronos-equals-admetos",
    "cupido-kronos-equals-apollon",
    "cupido-kronos-equals-asc",
    "cupido-kronos-equals-hades",
    "cupido-kronos-equals-jupiter",
    "cupido-kronos-equals-mars",
    "cupido-kronos-equals-mc",
    "cupido-kronos-equals-mercury",
    "cupido-kronos-equals-moon",
    "cupido-kronos-equals-neptune",
    "cupido-kronos-equals-node",
    "cupido-kronos-equals-pluto",
    "cupido-kronos-equals-poseidon",
    "cupido-kronos-equals-saturn",
    "cupido-kronos-equals-sun",
    "cupido-kronos-equals-uranus",
    "cupido-kronos-equals-venus",
    "cupido-kronos-equals-vernal-point",
    "cupido-kronos-equals-vulcanus",
    "cupido-kronos-equals-zeus",
}

SEEDED_CUPIDO_POSEIDON_AXIS_CLUSTER = {
    "cupido-poseidon",
}

SEEDED_CUPIDO_POSEIDON_ACTIVATION_CLUSTER = {
    "cupido-poseidon-equals-admetos",
    "cupido-poseidon-equals-apollon",
    "cupido-poseidon-equals-asc",
    "cupido-poseidon-equals-hades",
    "cupido-poseidon-equals-jupiter",
    "cupido-poseidon-equals-kronos",
    "cupido-poseidon-equals-mars",
    "cupido-poseidon-equals-mc",
    "cupido-poseidon-equals-mercury",
    "cupido-poseidon-equals-moon",
    "cupido-poseidon-equals-neptune",
    "cupido-poseidon-equals-node",
    "cupido-poseidon-equals-pluto",
    "cupido-poseidon-equals-saturn",
    "cupido-poseidon-equals-sun",
    "cupido-poseidon-equals-uranus",
    "cupido-poseidon-equals-venus",
    "cupido-poseidon-equals-vernal-point",
    "cupido-poseidon-equals-vulcanus",
    "cupido-poseidon-equals-zeus",
}

SEEDED_CUPIDO_VULCANUS_AXIS_CLUSTER = {
    "cupido-vulcanus",
}

SEEDED_CUPIDO_VULCANUS_ACTIVATION_CLUSTER = {
    "cupido-vulcanus-equals-admetos",
    "cupido-vulcanus-equals-apollon",
    "cupido-vulcanus-equals-asc",
    "cupido-vulcanus-equals-hades",
    "cupido-vulcanus-equals-jupiter",
    "cupido-vulcanus-equals-kronos",
    "cupido-vulcanus-equals-mars",
    "cupido-vulcanus-equals-mc",
    "cupido-vulcanus-equals-mercury",
    "cupido-vulcanus-equals-moon",
    "cupido-vulcanus-equals-neptune",
    "cupido-vulcanus-equals-node",
    "cupido-vulcanus-equals-pluto",
    "cupido-vulcanus-equals-poseidon",
    "cupido-vulcanus-equals-saturn",
    "cupido-vulcanus-equals-sun",
    "cupido-vulcanus-equals-uranus",
    "cupido-vulcanus-equals-venus",
    "cupido-vulcanus-equals-vernal-point",
    "cupido-vulcanus-equals-zeus",
}

SEEDED_CUPIDO_ZEUS_AXIS_CLUSTER = {
    "cupido-zeus",
}

SEEDED_CUPIDO_ZEUS_ACTIVATION_CLUSTER = {
    "cupido-zeus-equals-admetos",
    "cupido-zeus-equals-apollon",
    "cupido-zeus-equals-asc",
    "cupido-zeus-equals-hades",
    "cupido-zeus-equals-jupiter",
    "cupido-zeus-equals-kronos",
    "cupido-zeus-equals-mars",
    "cupido-zeus-equals-mc",
    "cupido-zeus-equals-mercury",
    "cupido-zeus-equals-moon",
    "cupido-zeus-equals-neptune",
    "cupido-zeus-equals-node",
    "cupido-zeus-equals-pluto",
    "cupido-zeus-equals-poseidon",
    "cupido-zeus-equals-saturn",
    "cupido-zeus-equals-sun",
    "cupido-zeus-equals-uranus",
    "cupido-zeus-equals-venus",
    "cupido-zeus-equals-vernal-point",
    "cupido-zeus-equals-vulcanus",
}

SEEDED_HADES_ADMETOS_AXIS_CLUSTER = {
    "hades-admetos",
}

SEEDED_HADES_ADMETOS_ACTIVATION_CLUSTER = {
    "hades-admetos-equals-apollon",
    "hades-admetos-equals-asc",
    "hades-admetos-equals-cupido",
    "hades-admetos-equals-jupiter",
    "hades-admetos-equals-kronos",
    "hades-admetos-equals-mars",
    "hades-admetos-equals-mc",
    "hades-admetos-equals-mercury",
    "hades-admetos-equals-moon",
    "hades-admetos-equals-neptune",
    "hades-admetos-equals-node",
    "hades-admetos-equals-pluto",
    "hades-admetos-equals-poseidon",
    "hades-admetos-equals-saturn",
    "hades-admetos-equals-sun",
    "hades-admetos-equals-uranus",
    "hades-admetos-equals-venus",
    "hades-admetos-equals-vernal-point",
    "hades-admetos-equals-vulcanus",
    "hades-admetos-equals-zeus",
}

SEEDED_HADES_APOLLON_AXIS_CLUSTER = {
    "hades-apollon",
}

SEEDED_HADES_APOLLON_ACTIVATION_CLUSTER = {
    "hades-apollon-equals-admetos",
    "hades-apollon-equals-asc",
    "hades-apollon-equals-cupido",
    "hades-apollon-equals-jupiter",
    "hades-apollon-equals-kronos",
    "hades-apollon-equals-mars",
    "hades-apollon-equals-mc",
    "hades-apollon-equals-mercury",
    "hades-apollon-equals-moon",
    "hades-apollon-equals-neptune",
    "hades-apollon-equals-node",
    "hades-apollon-equals-pluto",
    "hades-apollon-equals-poseidon",
    "hades-apollon-equals-saturn",
    "hades-apollon-equals-sun",
    "hades-apollon-equals-uranus",
    "hades-apollon-equals-venus",
    "hades-apollon-equals-vernal-point",
    "hades-apollon-equals-vulcanus",
    "hades-apollon-equals-zeus",
}

SEEDED_HADES_HADES_AXIS_CLUSTER = {
    "hades-hades",
}

SEEDED_HADES_HADES_ACTIVATION_CLUSTER = {
    "hades-hades-equals-admetos",
    "hades-hades-equals-apollon",
    "hades-hades-equals-asc",
    "hades-hades-equals-cupido",
    "hades-hades-equals-jupiter",
    "hades-hades-equals-kronos",
    "hades-hades-equals-mars",
    "hades-hades-equals-mc",
    "hades-hades-equals-mercury",
    "hades-hades-equals-moon",
    "hades-hades-equals-neptune",
    "hades-hades-equals-node",
    "hades-hades-equals-pluto",
    "hades-hades-equals-poseidon",
    "hades-hades-equals-saturn",
    "hades-hades-equals-sun",
    "hades-hades-equals-uranus",
    "hades-hades-equals-venus",
    "hades-hades-equals-vernal-point",
    "hades-hades-equals-vulcanus",
    "hades-hades-equals-zeus",
}

SEEDED_HADES_KRONOS_AXIS_CLUSTER = {
    "hades-kronos",
}

SEEDED_HADES_KRONOS_ACTIVATION_CLUSTER = {
    "hades-kronos-equals-admetos",
    "hades-kronos-equals-apollon",
    "hades-kronos-equals-asc",
    "hades-kronos-equals-cupido",
    "hades-kronos-equals-jupiter",
    "hades-kronos-equals-mars",
    "hades-kronos-equals-mc",
    "hades-kronos-equals-mercury",
    "hades-kronos-equals-moon",
    "hades-kronos-equals-neptune",
    "hades-kronos-equals-node",
    "hades-kronos-equals-pluto",
    "hades-kronos-equals-poseidon",
    "hades-kronos-equals-saturn",
    "hades-kronos-equals-sun",
    "hades-kronos-equals-uranus",
    "hades-kronos-equals-venus",
    "hades-kronos-equals-vernal-point",
    "hades-kronos-equals-vulcanus",
    "hades-kronos-equals-zeus",
}

SEEDED_HADES_POSEIDON_AXIS_CLUSTER = {
    "hades-poseidon",
}

SEEDED_HADES_POSEIDON_ACTIVATION_CLUSTER = {
    "hades-poseidon-equals-admetos",
    "hades-poseidon-equals-apollon",
    "hades-poseidon-equals-asc",
    "hades-poseidon-equals-cupido",
    "hades-poseidon-equals-jupiter",
    "hades-poseidon-equals-kronos",
    "hades-poseidon-equals-mars",
    "hades-poseidon-equals-mc",
    "hades-poseidon-equals-mercury",
    "hades-poseidon-equals-moon",
    "hades-poseidon-equals-neptune",
    "hades-poseidon-equals-node",
    "hades-poseidon-equals-pluto",
    "hades-poseidon-equals-saturn",
    "hades-poseidon-equals-sun",
    "hades-poseidon-equals-uranus",
    "hades-poseidon-equals-venus",
    "hades-poseidon-equals-vernal-point",
    "hades-poseidon-equals-vulcanus",
    "hades-poseidon-equals-zeus",
}

SEEDED_HADES_VULCANUS_AXIS_CLUSTER = {
    "hades-vulcanus",
}

SEEDED_HADES_VULCANUS_ACTIVATION_CLUSTER = {
    "hades-vulcanus-equals-admetos",
    "hades-vulcanus-equals-apollon",
    "hades-vulcanus-equals-asc",
    "hades-vulcanus-equals-cupido",
    "hades-vulcanus-equals-jupiter",
    "hades-vulcanus-equals-kronos",
    "hades-vulcanus-equals-mars",
    "hades-vulcanus-equals-mc",
    "hades-vulcanus-equals-mercury",
    "hades-vulcanus-equals-moon",
    "hades-vulcanus-equals-neptune",
    "hades-vulcanus-equals-node",
    "hades-vulcanus-equals-pluto",
    "hades-vulcanus-equals-poseidon",
    "hades-vulcanus-equals-saturn",
    "hades-vulcanus-equals-sun",
    "hades-vulcanus-equals-uranus",
    "hades-vulcanus-equals-venus",
    "hades-vulcanus-equals-vernal-point",
    "hades-vulcanus-equals-zeus",
}

SEEDED_HADES_ZEUS_AXIS_CLUSTER = {
    "hades-zeus",
}

SEEDED_HADES_ZEUS_ACTIVATION_CLUSTER = {
    "hades-zeus-equals-admetos",
    "hades-zeus-equals-apollon",
    "hades-zeus-equals-asc",
    "hades-zeus-equals-cupido",
    "hades-zeus-equals-jupiter",
    "hades-zeus-equals-kronos",
    "hades-zeus-equals-mars",
    "hades-zeus-equals-mc",
    "hades-zeus-equals-mercury",
    "hades-zeus-equals-moon",
    "hades-zeus-equals-neptune",
    "hades-zeus-equals-node",
    "hades-zeus-equals-pluto",
    "hades-zeus-equals-poseidon",
    "hades-zeus-equals-saturn",
    "hades-zeus-equals-sun",
    "hades-zeus-equals-uranus",
    "hades-zeus-equals-venus",
    "hades-zeus-equals-vernal-point",
    "hades-zeus-equals-vulcanus",
}

SEEDED_JUPITER_ADMETOS_AXIS_CLUSTER = {
    "jupiter-admetos",
}

SEEDED_JUPITER_ADMETOS_ACTIVATION_CLUSTER = {
    "jupiter-admetos-equals-apollon",
    "jupiter-admetos-equals-asc",
    "jupiter-admetos-equals-cupido",
    "jupiter-admetos-equals-hades",
    "jupiter-admetos-equals-kronos",
    "jupiter-admetos-equals-mars",
    "jupiter-admetos-equals-mc",
    "jupiter-admetos-equals-mercury",
    "jupiter-admetos-equals-moon",
    "jupiter-admetos-equals-neptune",
    "jupiter-admetos-equals-node",
    "jupiter-admetos-equals-pluto",
    "jupiter-admetos-equals-poseidon",
    "jupiter-admetos-equals-saturn",
    "jupiter-admetos-equals-sun",
    "jupiter-admetos-equals-uranus",
    "jupiter-admetos-equals-venus",
    "jupiter-admetos-equals-vernal-point",
    "jupiter-admetos-equals-vulcanus",
    "jupiter-admetos-equals-zeus",
}

SEEDED_JUPITER_APOLLON_AXIS_CLUSTER = {
    "jupiter-apollon",
}

SEEDED_JUPITER_APOLLON_ACTIVATION_CLUSTER = {
    "jupiter-apollon-equals-admetos",
    "jupiter-apollon-equals-asc",
    "jupiter-apollon-equals-cupido",
    "jupiter-apollon-equals-hades",
    "jupiter-apollon-equals-kronos",
    "jupiter-apollon-equals-mars",
    "jupiter-apollon-equals-mc",
    "jupiter-apollon-equals-mercury",
    "jupiter-apollon-equals-moon",
    "jupiter-apollon-equals-neptune",
    "jupiter-apollon-equals-node",
    "jupiter-apollon-equals-pluto",
    "jupiter-apollon-equals-poseidon",
    "jupiter-apollon-equals-saturn",
    "jupiter-apollon-equals-sun",
    "jupiter-apollon-equals-uranus",
    "jupiter-apollon-equals-venus",
    "jupiter-apollon-equals-vernal-point",
    "jupiter-apollon-equals-vulcanus",
    "jupiter-apollon-equals-zeus",
}

SEEDED_JUPITER_ASC_ADDITIONAL_ACTIVATION_CLUSTER = {
    "jupiter-asc-equals-admetos",
    "jupiter-asc-equals-apollon",
    "jupiter-asc-equals-chiron",
    "jupiter-asc-equals-cupido",
    "jupiter-asc-equals-hades",
    "jupiter-asc-equals-kronos",
    "jupiter-asc-equals-poseidon",
    "jupiter-asc-equals-vernal-point",
    "jupiter-asc-equals-vulcanus",
    "jupiter-asc-equals-zeus",
}

SEEDED_JUPITER_CHIRON_AXIS_CLUSTER = {
    "jupiter-chiron",
}

SEEDED_JUPITER_CHIRON_ACTIVATION_CLUSTER = {
    "jupiter-chiron-equals-asc",
    "jupiter-chiron-equals-mars",
    "jupiter-chiron-equals-mc",
    "jupiter-chiron-equals-mercury",
    "jupiter-chiron-equals-moon",
    "jupiter-chiron-equals-neptune",
    "jupiter-chiron-equals-node",
    "jupiter-chiron-equals-pluto",
    "jupiter-chiron-equals-saturn",
    "jupiter-chiron-equals-sun",
    "jupiter-chiron-equals-uranus",
    "jupiter-chiron-equals-venus",
}

SEEDED_JUPITER_CUPIDO_AXIS_CLUSTER = {
    "jupiter-cupido",
}

SEEDED_JUPITER_CUPIDO_ACTIVATION_CLUSTER = {
    "jupiter-cupido-equals-admetos",
    "jupiter-cupido-equals-apollon",
    "jupiter-cupido-equals-asc",
    "jupiter-cupido-equals-hades",
    "jupiter-cupido-equals-kronos",
    "jupiter-cupido-equals-mars",
    "jupiter-cupido-equals-mc",
    "jupiter-cupido-equals-mercury",
    "jupiter-cupido-equals-moon",
    "jupiter-cupido-equals-neptune",
    "jupiter-cupido-equals-node",
    "jupiter-cupido-equals-pluto",
    "jupiter-cupido-equals-poseidon",
    "jupiter-cupido-equals-saturn",
    "jupiter-cupido-equals-sun",
    "jupiter-cupido-equals-uranus",
    "jupiter-cupido-equals-venus",
    "jupiter-cupido-equals-vernal-point",
    "jupiter-cupido-equals-vulcanus",
    "jupiter-cupido-equals-zeus",
}

SEEDED_JUPITER_HADES_AXIS_CLUSTER = {
    "jupiter-hades",
}

SEEDED_JUPITER_HADES_ACTIVATION_CLUSTER = {
    "jupiter-hades-equals-admetos",
    "jupiter-hades-equals-apollon",
    "jupiter-hades-equals-asc",
    "jupiter-hades-equals-cupido",
    "jupiter-hades-equals-kronos",
    "jupiter-hades-equals-mars",
    "jupiter-hades-equals-mc",
    "jupiter-hades-equals-mercury",
    "jupiter-hades-equals-moon",
    "jupiter-hades-equals-neptune",
    "jupiter-hades-equals-node",
    "jupiter-hades-equals-pluto",
    "jupiter-hades-equals-poseidon",
    "jupiter-hades-equals-saturn",
    "jupiter-hades-equals-sun",
    "jupiter-hades-equals-uranus",
    "jupiter-hades-equals-venus",
    "jupiter-hades-equals-vernal-point",
    "jupiter-hades-equals-vulcanus",
    "jupiter-hades-equals-zeus",
}

SEEDED_JUPITER_JUPITER_AXIS_CLUSTER = {
    "jupiter-jupiter",
}

SEEDED_JUPITER_JUPITER_ACTIVATION_CLUSTER = {
    "jupiter-jupiter-equals-admetos",
    "jupiter-jupiter-equals-apollon",
    "jupiter-jupiter-equals-asc",
    "jupiter-jupiter-equals-cupido",
    "jupiter-jupiter-equals-hades",
    "jupiter-jupiter-equals-kronos",
    "jupiter-jupiter-equals-mars",
    "jupiter-jupiter-equals-mc",
    "jupiter-jupiter-equals-mercury",
    "jupiter-jupiter-equals-moon",
    "jupiter-jupiter-equals-neptune",
    "jupiter-jupiter-equals-node",
    "jupiter-jupiter-equals-pluto",
    "jupiter-jupiter-equals-poseidon",
    "jupiter-jupiter-equals-saturn",
    "jupiter-jupiter-equals-sun",
    "jupiter-jupiter-equals-uranus",
    "jupiter-jupiter-equals-venus",
    "jupiter-jupiter-equals-vernal-point",
    "jupiter-jupiter-equals-vulcanus",
    "jupiter-jupiter-equals-zeus",
}

SEEDED_JUPITER_KRONOS_AXIS_CLUSTER = {
    "jupiter-kronos",
}

SEEDED_JUPITER_KRONOS_ACTIVATION_CLUSTER = {
    "jupiter-kronos-equals-admetos",
    "jupiter-kronos-equals-apollon",
    "jupiter-kronos-equals-asc",
    "jupiter-kronos-equals-cupido",
    "jupiter-kronos-equals-hades",
    "jupiter-kronos-equals-mars",
    "jupiter-kronos-equals-mc",
    "jupiter-kronos-equals-mercury",
    "jupiter-kronos-equals-moon",
    "jupiter-kronos-equals-neptune",
    "jupiter-kronos-equals-node",
    "jupiter-kronos-equals-pluto",
    "jupiter-kronos-equals-poseidon",
    "jupiter-kronos-equals-saturn",
    "jupiter-kronos-equals-sun",
    "jupiter-kronos-equals-uranus",
    "jupiter-kronos-equals-venus",
    "jupiter-kronos-equals-vernal-point",
    "jupiter-kronos-equals-vulcanus",
    "jupiter-kronos-equals-zeus",
}

SEEDED_JUPITER_POSEIDON_AXIS_CLUSTER = {
    "jupiter-poseidon",
}

SEEDED_JUPITER_POSEIDON_ACTIVATION_CLUSTER = {
    "jupiter-poseidon-equals-admetos",
    "jupiter-poseidon-equals-apollon",
    "jupiter-poseidon-equals-asc",
    "jupiter-poseidon-equals-cupido",
    "jupiter-poseidon-equals-hades",
    "jupiter-poseidon-equals-kronos",
    "jupiter-poseidon-equals-mars",
    "jupiter-poseidon-equals-mc",
    "jupiter-poseidon-equals-mercury",
    "jupiter-poseidon-equals-moon",
    "jupiter-poseidon-equals-neptune",
    "jupiter-poseidon-equals-node",
    "jupiter-poseidon-equals-pluto",
    "jupiter-poseidon-equals-saturn",
    "jupiter-poseidon-equals-sun",
    "jupiter-poseidon-equals-uranus",
    "jupiter-poseidon-equals-venus",
    "jupiter-poseidon-equals-vernal-point",
    "jupiter-poseidon-equals-vulcanus",
    "jupiter-poseidon-equals-zeus",
}

SEEDED_JUPITER_VULCANUS_AXIS_CLUSTER = {
    "jupiter-vulcanus",
}

SEEDED_JUPITER_VULCANUS_ACTIVATION_CLUSTER = {
    "jupiter-vulcanus-equals-admetos",
    "jupiter-vulcanus-equals-apollon",
    "jupiter-vulcanus-equals-asc",
    "jupiter-vulcanus-equals-cupido",
    "jupiter-vulcanus-equals-hades",
    "jupiter-vulcanus-equals-kronos",
    "jupiter-vulcanus-equals-mars",
    "jupiter-vulcanus-equals-mc",
    "jupiter-vulcanus-equals-mercury",
    "jupiter-vulcanus-equals-moon",
    "jupiter-vulcanus-equals-neptune",
    "jupiter-vulcanus-equals-node",
    "jupiter-vulcanus-equals-pluto",
    "jupiter-vulcanus-equals-poseidon",
    "jupiter-vulcanus-equals-saturn",
    "jupiter-vulcanus-equals-sun",
    "jupiter-vulcanus-equals-uranus",
    "jupiter-vulcanus-equals-venus",
    "jupiter-vulcanus-equals-vernal-point",
    "jupiter-vulcanus-equals-zeus",
}

SEEDED_JUPITER_ZEUS_AXIS_CLUSTER = {
    "jupiter-zeus",
}

SEEDED_JUPITER_ZEUS_ACTIVATION_CLUSTER = {
    "jupiter-zeus-equals-admetos",
    "jupiter-zeus-equals-apollon",
    "jupiter-zeus-equals-asc",
    "jupiter-zeus-equals-cupido",
    "jupiter-zeus-equals-hades",
    "jupiter-zeus-equals-kronos",
    "jupiter-zeus-equals-mars",
    "jupiter-zeus-equals-mc",
    "jupiter-zeus-equals-mercury",
    "jupiter-zeus-equals-moon",
    "jupiter-zeus-equals-neptune",
    "jupiter-zeus-equals-node",
    "jupiter-zeus-equals-pluto",
    "jupiter-zeus-equals-poseidon",
    "jupiter-zeus-equals-saturn",
    "jupiter-zeus-equals-sun",
    "jupiter-zeus-equals-uranus",
    "jupiter-zeus-equals-venus",
    "jupiter-zeus-equals-vernal-point",
    "jupiter-zeus-equals-vulcanus",
}

SEEDED_KRONOS_ADMETOS_AXIS_CLUSTER = {
    "kronos-admetos",
}

SEEDED_KRONOS_ADMETOS_ACTIVATION_CLUSTER = {
    "kronos-admetos-equals-apollon",
    "kronos-admetos-equals-asc",
    "kronos-admetos-equals-cupido",
    "kronos-admetos-equals-hades",
    "kronos-admetos-equals-jupiter",
    "kronos-admetos-equals-mars",
    "kronos-admetos-equals-mc",
    "kronos-admetos-equals-mercury",
    "kronos-admetos-equals-moon",
    "kronos-admetos-equals-neptune",
    "kronos-admetos-equals-node",
    "kronos-admetos-equals-pluto",
    "kronos-admetos-equals-poseidon",
    "kronos-admetos-equals-saturn",
    "kronos-admetos-equals-sun",
    "kronos-admetos-equals-uranus",
    "kronos-admetos-equals-venus",
    "kronos-admetos-equals-vernal-point",
    "kronos-admetos-equals-vulcanus",
    "kronos-admetos-equals-zeus",
}

SEEDED_KRONOS_APOLLON_AXIS_CLUSTER = {
    "kronos-apollon",
}

SEEDED_KRONOS_APOLLON_ACTIVATION_CLUSTER = {
    "kronos-apollon-equals-admetos",
    "kronos-apollon-equals-asc",
    "kronos-apollon-equals-cupido",
    "kronos-apollon-equals-hades",
    "kronos-apollon-equals-jupiter",
    "kronos-apollon-equals-mars",
    "kronos-apollon-equals-mc",
    "kronos-apollon-equals-mercury",
    "kronos-apollon-equals-moon",
    "kronos-apollon-equals-neptune",
    "kronos-apollon-equals-node",
    "kronos-apollon-equals-pluto",
    "kronos-apollon-equals-poseidon",
    "kronos-apollon-equals-saturn",
    "kronos-apollon-equals-sun",
    "kronos-apollon-equals-uranus",
    "kronos-apollon-equals-venus",
    "kronos-apollon-equals-vernal-point",
    "kronos-apollon-equals-vulcanus",
    "kronos-apollon-equals-zeus",
}

SEEDED_KRONOS_KRONOS_AXIS_CLUSTER = {
    "kronos-kronos",
}

SEEDED_KRONOS_KRONOS_ACTIVATION_CLUSTER = {
    "kronos-kronos-equals-admetos",
    "kronos-kronos-equals-apollon",
    "kronos-kronos-equals-asc",
    "kronos-kronos-equals-cupido",
    "kronos-kronos-equals-hades",
    "kronos-kronos-equals-jupiter",
    "kronos-kronos-equals-mars",
    "kronos-kronos-equals-mc",
    "kronos-kronos-equals-mercury",
    "kronos-kronos-equals-moon",
    "kronos-kronos-equals-neptune",
    "kronos-kronos-equals-node",
    "kronos-kronos-equals-pluto",
    "kronos-kronos-equals-poseidon",
    "kronos-kronos-equals-saturn",
    "kronos-kronos-equals-sun",
    "kronos-kronos-equals-uranus",
    "kronos-kronos-equals-venus",
    "kronos-kronos-equals-vernal-point",
    "kronos-kronos-equals-vulcanus",
    "kronos-kronos-equals-zeus",
}

SEEDED_KRONOS_POSEIDON_AXIS_CLUSTER = {
    "kronos-poseidon",
}

SEEDED_KRONOS_POSEIDON_ACTIVATION_CLUSTER = {
    "kronos-poseidon-equals-admetos",
    "kronos-poseidon-equals-apollon",
    "kronos-poseidon-equals-asc",
    "kronos-poseidon-equals-cupido",
    "kronos-poseidon-equals-hades",
    "kronos-poseidon-equals-jupiter",
    "kronos-poseidon-equals-mars",
    "kronos-poseidon-equals-mc",
    "kronos-poseidon-equals-mercury",
    "kronos-poseidon-equals-moon",
    "kronos-poseidon-equals-neptune",
    "kronos-poseidon-equals-node",
    "kronos-poseidon-equals-pluto",
    "kronos-poseidon-equals-saturn",
    "kronos-poseidon-equals-sun",
    "kronos-poseidon-equals-uranus",
    "kronos-poseidon-equals-venus",
    "kronos-poseidon-equals-vernal-point",
    "kronos-poseidon-equals-vulcanus",
    "kronos-poseidon-equals-zeus",
}

SEEDED_KRONOS_VULCANUS_AXIS_CLUSTER = {
    "kronos-vulcanus",
}

SEEDED_KRONOS_VULCANUS_ACTIVATION_CLUSTER = {
    "kronos-vulcanus-equals-admetos",
    "kronos-vulcanus-equals-apollon",
    "kronos-vulcanus-equals-asc",
    "kronos-vulcanus-equals-cupido",
    "kronos-vulcanus-equals-hades",
    "kronos-vulcanus-equals-jupiter",
    "kronos-vulcanus-equals-mars",
    "kronos-vulcanus-equals-mc",
    "kronos-vulcanus-equals-mercury",
    "kronos-vulcanus-equals-moon",
    "kronos-vulcanus-equals-neptune",
    "kronos-vulcanus-equals-node",
    "kronos-vulcanus-equals-pluto",
    "kronos-vulcanus-equals-poseidon",
    "kronos-vulcanus-equals-saturn",
    "kronos-vulcanus-equals-sun",
    "kronos-vulcanus-equals-uranus",
    "kronos-vulcanus-equals-venus",
    "kronos-vulcanus-equals-vernal-point",
    "kronos-vulcanus-equals-zeus",
}

SEEDED_MARS_ADMETOS_AXIS_CLUSTER = {
    "mars-admetos",
}

SEEDED_MARS_ADMETOS_ACTIVATION_CLUSTER = {
    "mars-admetos-equals-apollon",
    "mars-admetos-equals-asc",
    "mars-admetos-equals-cupido",
    "mars-admetos-equals-hades",
    "mars-admetos-equals-jupiter",
    "mars-admetos-equals-kronos",
    "mars-admetos-equals-mc",
    "mars-admetos-equals-mercury",
    "mars-admetos-equals-moon",
    "mars-admetos-equals-neptune",
    "mars-admetos-equals-node",
    "mars-admetos-equals-pluto",
    "mars-admetos-equals-poseidon",
    "mars-admetos-equals-saturn",
    "mars-admetos-equals-sun",
    "mars-admetos-equals-uranus",
    "mars-admetos-equals-venus",
    "mars-admetos-equals-vernal-point",
    "mars-admetos-equals-vulcanus",
    "mars-admetos-equals-zeus",
}

SEEDED_MARS_APOLLON_AXIS_CLUSTER = {
    "mars-apollon",
}

SEEDED_MARS_APOLLON_ACTIVATION_CLUSTER = {
    "mars-apollon-equals-admetos",
    "mars-apollon-equals-asc",
    "mars-apollon-equals-cupido",
    "mars-apollon-equals-hades",
    "mars-apollon-equals-jupiter",
    "mars-apollon-equals-kronos",
    "mars-apollon-equals-mc",
    "mars-apollon-equals-mercury",
    "mars-apollon-equals-moon",
    "mars-apollon-equals-neptune",
    "mars-apollon-equals-node",
    "mars-apollon-equals-pluto",
    "mars-apollon-equals-poseidon",
    "mars-apollon-equals-saturn",
    "mars-apollon-equals-sun",
    "mars-apollon-equals-uranus",
    "mars-apollon-equals-venus",
    "mars-apollon-equals-vernal-point",
    "mars-apollon-equals-vulcanus",
    "mars-apollon-equals-zeus",
}

SEEDED_MARS_CHIRON_AXIS_CLUSTER = {
    "mars-chiron",
}

SEEDED_MARS_CHIRON_ACTIVATION_CLUSTER = {
    "mars-chiron-equals-asc",
    "mars-chiron-equals-jupiter",
    "mars-chiron-equals-mc",
    "mars-chiron-equals-mercury",
    "mars-chiron-equals-moon",
    "mars-chiron-equals-neptune",
    "mars-chiron-equals-node",
    "mars-chiron-equals-pluto",
    "mars-chiron-equals-saturn",
    "mars-chiron-equals-sun",
    "mars-chiron-equals-uranus",
    "mars-chiron-equals-venus",
}

SEEDED_MARS_CUPIDO_AXIS_CLUSTER = {
    "mars-cupido",
}

SEEDED_MARS_CUPIDO_ACTIVATION_CLUSTER = {
    "mars-cupido-equals-admetos",
    "mars-cupido-equals-apollon",
    "mars-cupido-equals-asc",
    "mars-cupido-equals-hades",
    "mars-cupido-equals-jupiter",
    "mars-cupido-equals-kronos",
    "mars-cupido-equals-mc",
    "mars-cupido-equals-mercury",
    "mars-cupido-equals-moon",
    "mars-cupido-equals-neptune",
    "mars-cupido-equals-node",
    "mars-cupido-equals-pluto",
    "mars-cupido-equals-poseidon",
    "mars-cupido-equals-saturn",
    "mars-cupido-equals-sun",
    "mars-cupido-equals-uranus",
    "mars-cupido-equals-venus",
    "mars-cupido-equals-vernal-point",
    "mars-cupido-equals-vulcanus",
    "mars-cupido-equals-zeus",
}

SEEDED_MARS_HADES_AXIS_CLUSTER = {
    "mars-hades",
}

SEEDED_MARS_HADES_ACTIVATION_CLUSTER = {
    "mars-hades-equals-admetos",
    "mars-hades-equals-apollon",
    "mars-hades-equals-asc",
    "mars-hades-equals-cupido",
    "mars-hades-equals-jupiter",
    "mars-hades-equals-kronos",
    "mars-hades-equals-mc",
    "mars-hades-equals-mercury",
    "mars-hades-equals-moon",
    "mars-hades-equals-neptune",
    "mars-hades-equals-node",
    "mars-hades-equals-pluto",
    "mars-hades-equals-poseidon",
    "mars-hades-equals-saturn",
    "mars-hades-equals-sun",
    "mars-hades-equals-uranus",
    "mars-hades-equals-venus",
    "mars-hades-equals-vernal-point",
    "mars-hades-equals-vulcanus",
    "mars-hades-equals-zeus",
}

SEEDED_MARS_KRONOS_AXIS_CLUSTER = {
    "mars-kronos",
}

SEEDED_MARS_KRONOS_ACTIVATION_CLUSTER = {
    "mars-kronos-equals-admetos",
    "mars-kronos-equals-apollon",
    "mars-kronos-equals-asc",
    "mars-kronos-equals-cupido",
    "mars-kronos-equals-hades",
    "mars-kronos-equals-jupiter",
    "mars-kronos-equals-mc",
    "mars-kronos-equals-mercury",
    "mars-kronos-equals-moon",
    "mars-kronos-equals-neptune",
    "mars-kronos-equals-node",
    "mars-kronos-equals-pluto",
    "mars-kronos-equals-poseidon",
    "mars-kronos-equals-saturn",
    "mars-kronos-equals-sun",
    "mars-kronos-equals-uranus",
    "mars-kronos-equals-venus",
    "mars-kronos-equals-vernal-point",
    "mars-kronos-equals-vulcanus",
    "mars-kronos-equals-zeus",
}

SEEDED_MARS_MARS_AXIS_CLUSTER = {
    "mars-mars",
}

SEEDED_MARS_MARS_ACTIVATION_CLUSTER = {
    "mars-mars-equals-admetos",
    "mars-mars-equals-apollon",
    "mars-mars-equals-asc",
    "mars-mars-equals-cupido",
    "mars-mars-equals-hades",
    "mars-mars-equals-jupiter",
    "mars-mars-equals-kronos",
    "mars-mars-equals-mc",
    "mars-mars-equals-mercury",
    "mars-mars-equals-moon",
    "mars-mars-equals-neptune",
    "mars-mars-equals-node",
    "mars-mars-equals-pluto",
    "mars-mars-equals-poseidon",
    "mars-mars-equals-saturn",
    "mars-mars-equals-sun",
    "mars-mars-equals-uranus",
    "mars-mars-equals-venus",
    "mars-mars-equals-vernal-point",
    "mars-mars-equals-vulcanus",
    "mars-mars-equals-zeus",
}

SEEDED_MARS_MC_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mars-mc-equals-admetos",
    "mars-mc-equals-apollon",
    "mars-mc-equals-chiron",
    "mars-mc-equals-cupido",
    "mars-mc-equals-hades",
    "mars-mc-equals-kronos",
    "mars-mc-equals-poseidon",
    "mars-mc-equals-vernal-point",
    "mars-mc-equals-vulcanus",
    "mars-mc-equals-zeus",
}

SEEDED_MARS_NEPTUNE_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mars-neptune-equals-admetos",
    "mars-neptune-equals-apollon",
    "mars-neptune-equals-chiron",
    "mars-neptune-equals-cupido",
    "mars-neptune-equals-hades",
    "mars-neptune-equals-kronos",
    "mars-neptune-equals-poseidon",
    "mars-neptune-equals-vernal-point",
    "mars-neptune-equals-vulcanus",
    "mars-neptune-equals-zeus",
}

SEEDED_MARS_NODE_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mars-node-equals-admetos",
    "mars-node-equals-apollon",
    "mars-node-equals-chiron",
    "mars-node-equals-cupido",
    "mars-node-equals-hades",
    "mars-node-equals-kronos",
    "mars-node-equals-poseidon",
    "mars-node-equals-vernal-point",
    "mars-node-equals-vulcanus",
    "mars-node-equals-zeus",
}

SEEDED_MARS_PLUTO_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mars-pluto-equals-admetos",
    "mars-pluto-equals-apollon",
    "mars-pluto-equals-chiron",
    "mars-pluto-equals-cupido",
    "mars-pluto-equals-hades",
    "mars-pluto-equals-kronos",
    "mars-pluto-equals-poseidon",
    "mars-pluto-equals-vernal-point",
    "mars-pluto-equals-vulcanus",
    "mars-pluto-equals-zeus",
}

SEEDED_MARS_POSEIDON_AXIS_CLUSTER = {
    "mars-poseidon",
}

SEEDED_MARS_POSEIDON_ACTIVATION_CLUSTER = {
    "mars-poseidon-equals-admetos",
    "mars-poseidon-equals-apollon",
    "mars-poseidon-equals-asc",
    "mars-poseidon-equals-cupido",
    "mars-poseidon-equals-hades",
    "mars-poseidon-equals-jupiter",
    "mars-poseidon-equals-kronos",
    "mars-poseidon-equals-mc",
    "mars-poseidon-equals-mercury",
    "mars-poseidon-equals-moon",
    "mars-poseidon-equals-neptune",
    "mars-poseidon-equals-node",
    "mars-poseidon-equals-pluto",
    "mars-poseidon-equals-saturn",
    "mars-poseidon-equals-sun",
    "mars-poseidon-equals-uranus",
    "mars-poseidon-equals-venus",
    "mars-poseidon-equals-vernal-point",
    "mars-poseidon-equals-vulcanus",
    "mars-poseidon-equals-zeus",
}

SEEDED_MARS_SATURN_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mars-saturn-equals-admetos",
    "mars-saturn-equals-apollon",
    "mars-saturn-equals-chiron",
    "mars-saturn-equals-cupido",
    "mars-saturn-equals-hades",
    "mars-saturn-equals-kronos",
    "mars-saturn-equals-poseidon",
    "mars-saturn-equals-vernal-point",
    "mars-saturn-equals-vulcanus",
    "mars-saturn-equals-zeus",
}

SEEDED_MARS_URANUS_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mars-uranus-equals-admetos",
    "mars-uranus-equals-apollon",
    "mars-uranus-equals-chiron",
    "mars-uranus-equals-cupido",
    "mars-uranus-equals-hades",
    "mars-uranus-equals-kronos",
    "mars-uranus-equals-poseidon",
    "mars-uranus-equals-vernal-point",
    "mars-uranus-equals-vulcanus",
    "mars-uranus-equals-zeus",
}

SEEDED_MARS_VULCANUS_AXIS_CLUSTER = {
    "mars-vulcanus",
}

SEEDED_MARS_VULCANUS_ACTIVATION_CLUSTER = {
    "mars-vulcanus-equals-admetos",
    "mars-vulcanus-equals-apollon",
    "mars-vulcanus-equals-asc",
    "mars-vulcanus-equals-cupido",
    "mars-vulcanus-equals-hades",
    "mars-vulcanus-equals-jupiter",
    "mars-vulcanus-equals-kronos",
    "mars-vulcanus-equals-mc",
    "mars-vulcanus-equals-mercury",
    "mars-vulcanus-equals-moon",
    "mars-vulcanus-equals-neptune",
    "mars-vulcanus-equals-node",
    "mars-vulcanus-equals-pluto",
    "mars-vulcanus-equals-poseidon",
    "mars-vulcanus-equals-saturn",
    "mars-vulcanus-equals-sun",
    "mars-vulcanus-equals-uranus",
    "mars-vulcanus-equals-venus",
    "mars-vulcanus-equals-vernal-point",
    "mars-vulcanus-equals-zeus",
}

SEEDED_MARS_ZEUS_AXIS_CLUSTER = {
    "mars-zeus",
}

SEEDED_MARS_ZEUS_ACTIVATION_CLUSTER = {
    "mars-zeus-equals-admetos",
    "mars-zeus-equals-apollon",
    "mars-zeus-equals-asc",
    "mars-zeus-equals-cupido",
    "mars-zeus-equals-hades",
    "mars-zeus-equals-jupiter",
    "mars-zeus-equals-kronos",
    "mars-zeus-equals-mc",
    "mars-zeus-equals-mercury",
    "mars-zeus-equals-moon",
    "mars-zeus-equals-neptune",
    "mars-zeus-equals-node",
    "mars-zeus-equals-pluto",
    "mars-zeus-equals-poseidon",
    "mars-zeus-equals-saturn",
    "mars-zeus-equals-sun",
    "mars-zeus-equals-uranus",
    "mars-zeus-equals-venus",
    "mars-zeus-equals-vernal-point",
    "mars-zeus-equals-vulcanus",
}

SEEDED_MC_ADMETOS_AXIS_CLUSTER = {
    "mc-admetos",
}

SEEDED_MC_ADMETOS_ACTIVATION_CLUSTER = {
    "mc-admetos-equals-apollon",
    "mc-admetos-equals-asc",
    "mc-admetos-equals-cupido",
    "mc-admetos-equals-hades",
    "mc-admetos-equals-jupiter",
    "mc-admetos-equals-kronos",
    "mc-admetos-equals-mars",
    "mc-admetos-equals-mercury",
    "mc-admetos-equals-moon",
    "mc-admetos-equals-neptune",
    "mc-admetos-equals-node",
    "mc-admetos-equals-pluto",
    "mc-admetos-equals-poseidon",
    "mc-admetos-equals-saturn",
    "mc-admetos-equals-sun",
    "mc-admetos-equals-uranus",
    "mc-admetos-equals-venus",
    "mc-admetos-equals-vernal-point",
    "mc-admetos-equals-vulcanus",
    "mc-admetos-equals-zeus",
}

SEEDED_MC_APOLLON_AXIS_CLUSTER = {
    "mc-apollon",
}

SEEDED_MC_APOLLON_ACTIVATION_CLUSTER = {
    "mc-apollon-equals-admetos",
    "mc-apollon-equals-asc",
    "mc-apollon-equals-cupido",
    "mc-apollon-equals-hades",
    "mc-apollon-equals-jupiter",
    "mc-apollon-equals-kronos",
    "mc-apollon-equals-mars",
    "mc-apollon-equals-mercury",
    "mc-apollon-equals-moon",
    "mc-apollon-equals-neptune",
    "mc-apollon-equals-node",
    "mc-apollon-equals-pluto",
    "mc-apollon-equals-poseidon",
    "mc-apollon-equals-saturn",
    "mc-apollon-equals-sun",
    "mc-apollon-equals-uranus",
    "mc-apollon-equals-venus",
    "mc-apollon-equals-vernal-point",
    "mc-apollon-equals-vulcanus",
    "mc-apollon-equals-zeus",
}

SEEDED_MC_CUPIDO_AXIS_CLUSTER = {
    "mc-cupido",
}

SEEDED_MC_CUPIDO_ACTIVATION_CLUSTER = {
    "mc-cupido-equals-admetos",
    "mc-cupido-equals-apollon",
    "mc-cupido-equals-asc",
    "mc-cupido-equals-hades",
    "mc-cupido-equals-jupiter",
    "mc-cupido-equals-kronos",
    "mc-cupido-equals-mars",
    "mc-cupido-equals-mercury",
    "mc-cupido-equals-moon",
    "mc-cupido-equals-neptune",
    "mc-cupido-equals-node",
    "mc-cupido-equals-pluto",
    "mc-cupido-equals-poseidon",
    "mc-cupido-equals-saturn",
    "mc-cupido-equals-sun",
    "mc-cupido-equals-uranus",
    "mc-cupido-equals-venus",
    "mc-cupido-equals-vernal-point",
    "mc-cupido-equals-vulcanus",
    "mc-cupido-equals-zeus",
}

SEEDED_MC_HADES_AXIS_CLUSTER = {
    "mc-hades",
}

SEEDED_MC_HADES_ACTIVATION_CLUSTER = {
    "mc-hades-equals-admetos",
    "mc-hades-equals-apollon",
    "mc-hades-equals-asc",
    "mc-hades-equals-cupido",
    "mc-hades-equals-jupiter",
    "mc-hades-equals-kronos",
    "mc-hades-equals-mars",
    "mc-hades-equals-mercury",
    "mc-hades-equals-moon",
    "mc-hades-equals-neptune",
    "mc-hades-equals-node",
    "mc-hades-equals-pluto",
    "mc-hades-equals-poseidon",
    "mc-hades-equals-saturn",
    "mc-hades-equals-sun",
    "mc-hades-equals-uranus",
    "mc-hades-equals-venus",
    "mc-hades-equals-vernal-point",
    "mc-hades-equals-vulcanus",
    "mc-hades-equals-zeus",
}

SEEDED_MC_KRONOS_AXIS_CLUSTER = {
    "mc-kronos",
}

SEEDED_MC_KRONOS_ACTIVATION_CLUSTER = {
    "mc-kronos-equals-admetos",
    "mc-kronos-equals-apollon",
    "mc-kronos-equals-asc",
    "mc-kronos-equals-cupido",
    "mc-kronos-equals-hades",
    "mc-kronos-equals-jupiter",
    "mc-kronos-equals-mars",
    "mc-kronos-equals-mercury",
    "mc-kronos-equals-moon",
    "mc-kronos-equals-neptune",
    "mc-kronos-equals-node",
    "mc-kronos-equals-pluto",
    "mc-kronos-equals-poseidon",
    "mc-kronos-equals-saturn",
    "mc-kronos-equals-sun",
    "mc-kronos-equals-uranus",
    "mc-kronos-equals-venus",
    "mc-kronos-equals-vernal-point",
    "mc-kronos-equals-vulcanus",
    "mc-kronos-equals-zeus",
}

SEEDED_MC_MC_AXIS_CLUSTER = {
    "mc-mc",
}

SEEDED_MC_MC_ACTIVATION_CLUSTER = {
    "mc-mc-equals-admetos",
    "mc-mc-equals-apollon",
    "mc-mc-equals-asc",
    "mc-mc-equals-cupido",
    "mc-mc-equals-hades",
    "mc-mc-equals-jupiter",
    "mc-mc-equals-kronos",
    "mc-mc-equals-mars",
    "mc-mc-equals-mercury",
    "mc-mc-equals-moon",
    "mc-mc-equals-neptune",
    "mc-mc-equals-node",
    "mc-mc-equals-pluto",
    "mc-mc-equals-poseidon",
    "mc-mc-equals-saturn",
    "mc-mc-equals-sun",
    "mc-mc-equals-uranus",
    "mc-mc-equals-venus",
    "mc-mc-equals-vernal-point",
    "mc-mc-equals-vulcanus",
    "mc-mc-equals-zeus",
}

SEEDED_MC_POSEIDON_AXIS_CLUSTER = {
    "mc-poseidon",
}

SEEDED_MC_POSEIDON_ACTIVATION_CLUSTER = {
    "mc-poseidon-equals-admetos",
    "mc-poseidon-equals-apollon",
    "mc-poseidon-equals-asc",
    "mc-poseidon-equals-cupido",
    "mc-poseidon-equals-hades",
    "mc-poseidon-equals-jupiter",
    "mc-poseidon-equals-kronos",
    "mc-poseidon-equals-mars",
    "mc-poseidon-equals-mercury",
    "mc-poseidon-equals-moon",
    "mc-poseidon-equals-neptune",
    "mc-poseidon-equals-node",
    "mc-poseidon-equals-pluto",
    "mc-poseidon-equals-saturn",
    "mc-poseidon-equals-sun",
    "mc-poseidon-equals-uranus",
    "mc-poseidon-equals-venus",
    "mc-poseidon-equals-vernal-point",
    "mc-poseidon-equals-vulcanus",
    "mc-poseidon-equals-zeus",
}

SEEDED_MC_VULCANUS_AXIS_CLUSTER = {
    "mc-vulcanus",
}

SEEDED_MC_VULCANUS_ACTIVATION_CLUSTER = {
    "mc-vulcanus-equals-admetos",
    "mc-vulcanus-equals-apollon",
    "mc-vulcanus-equals-asc",
    "mc-vulcanus-equals-cupido",
    "mc-vulcanus-equals-hades",
    "mc-vulcanus-equals-jupiter",
    "mc-vulcanus-equals-kronos",
    "mc-vulcanus-equals-mars",
    "mc-vulcanus-equals-mercury",
    "mc-vulcanus-equals-moon",
    "mc-vulcanus-equals-neptune",
    "mc-vulcanus-equals-node",
    "mc-vulcanus-equals-pluto",
    "mc-vulcanus-equals-poseidon",
    "mc-vulcanus-equals-saturn",
    "mc-vulcanus-equals-sun",
    "mc-vulcanus-equals-uranus",
    "mc-vulcanus-equals-venus",
    "mc-vulcanus-equals-vernal-point",
    "mc-vulcanus-equals-zeus",
}

SEEDED_MC_ZEUS_AXIS_CLUSTER = {
    "mc-zeus",
}

SEEDED_MC_ZEUS_ACTIVATION_CLUSTER = {
    "mc-zeus-equals-admetos",
    "mc-zeus-equals-apollon",
    "mc-zeus-equals-asc",
    "mc-zeus-equals-cupido",
    "mc-zeus-equals-hades",
    "mc-zeus-equals-jupiter",
    "mc-zeus-equals-kronos",
    "mc-zeus-equals-mars",
    "mc-zeus-equals-mercury",
    "mc-zeus-equals-moon",
    "mc-zeus-equals-neptune",
    "mc-zeus-equals-node",
    "mc-zeus-equals-pluto",
    "mc-zeus-equals-poseidon",
    "mc-zeus-equals-saturn",
    "mc-zeus-equals-sun",
    "mc-zeus-equals-uranus",
    "mc-zeus-equals-venus",
    "mc-zeus-equals-vernal-point",
    "mc-zeus-equals-vulcanus",
}

SEEDED_MERCURY_ADMETOS_AXIS_CLUSTER = {
    "mercury-admetos",
}

SEEDED_MERCURY_ADMETOS_ACTIVATION_CLUSTER = {
    "mercury-admetos-equals-apollon",
    "mercury-admetos-equals-asc",
    "mercury-admetos-equals-cupido",
    "mercury-admetos-equals-hades",
    "mercury-admetos-equals-jupiter",
    "mercury-admetos-equals-kronos",
    "mercury-admetos-equals-mars",
    "mercury-admetos-equals-mc",
    "mercury-admetos-equals-moon",
    "mercury-admetos-equals-neptune",
    "mercury-admetos-equals-node",
    "mercury-admetos-equals-pluto",
    "mercury-admetos-equals-poseidon",
    "mercury-admetos-equals-saturn",
    "mercury-admetos-equals-sun",
    "mercury-admetos-equals-uranus",
    "mercury-admetos-equals-venus",
    "mercury-admetos-equals-vernal-point",
    "mercury-admetos-equals-vulcanus",
    "mercury-admetos-equals-zeus",
}

SEEDED_MERCURY_APOLLON_AXIS_CLUSTER = {
    "mercury-apollon",
}

SEEDED_MERCURY_APOLLON_ACTIVATION_CLUSTER = {
    "mercury-apollon-equals-admetos",
    "mercury-apollon-equals-asc",
    "mercury-apollon-equals-cupido",
    "mercury-apollon-equals-hades",
    "mercury-apollon-equals-jupiter",
    "mercury-apollon-equals-kronos",
    "mercury-apollon-equals-mars",
    "mercury-apollon-equals-mc",
    "mercury-apollon-equals-moon",
    "mercury-apollon-equals-neptune",
    "mercury-apollon-equals-node",
    "mercury-apollon-equals-pluto",
    "mercury-apollon-equals-poseidon",
    "mercury-apollon-equals-saturn",
    "mercury-apollon-equals-sun",
    "mercury-apollon-equals-uranus",
    "mercury-apollon-equals-venus",
    "mercury-apollon-equals-vernal-point",
    "mercury-apollon-equals-vulcanus",
    "mercury-apollon-equals-zeus",
}

SEEDED_MERCURY_ASC_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-asc-equals-admetos",
    "mercury-asc-equals-apollon",
    "mercury-asc-equals-chiron",
    "mercury-asc-equals-cupido",
    "mercury-asc-equals-hades",
    "mercury-asc-equals-kronos",
    "mercury-asc-equals-poseidon",
    "mercury-asc-equals-vernal-point",
    "mercury-asc-equals-vulcanus",
    "mercury-asc-equals-zeus",
}

SEEDED_MERCURY_CHIRON_AXIS_CLUSTER = {
    "mercury-chiron",
}

SEEDED_MERCURY_CHIRON_ACTIVATION_CLUSTER = {
    "mercury-chiron-equals-asc",
    "mercury-chiron-equals-jupiter",
    "mercury-chiron-equals-mars",
    "mercury-chiron-equals-mc",
    "mercury-chiron-equals-moon",
    "mercury-chiron-equals-neptune",
    "mercury-chiron-equals-node",
    "mercury-chiron-equals-pluto",
    "mercury-chiron-equals-saturn",
    "mercury-chiron-equals-sun",
    "mercury-chiron-equals-uranus",
    "mercury-chiron-equals-venus",
}

SEEDED_MERCURY_CUPIDO_AXIS_CLUSTER = {
    "mercury-cupido",
}

SEEDED_MERCURY_CUPIDO_ACTIVATION_CLUSTER = {
    "mercury-cupido-equals-admetos",
    "mercury-cupido-equals-apollon",
    "mercury-cupido-equals-asc",
    "mercury-cupido-equals-hades",
    "mercury-cupido-equals-jupiter",
    "mercury-cupido-equals-kronos",
    "mercury-cupido-equals-mars",
    "mercury-cupido-equals-mc",
    "mercury-cupido-equals-moon",
    "mercury-cupido-equals-neptune",
    "mercury-cupido-equals-node",
    "mercury-cupido-equals-pluto",
    "mercury-cupido-equals-poseidon",
    "mercury-cupido-equals-saturn",
    "mercury-cupido-equals-sun",
    "mercury-cupido-equals-uranus",
    "mercury-cupido-equals-venus",
    "mercury-cupido-equals-vernal-point",
    "mercury-cupido-equals-vulcanus",
    "mercury-cupido-equals-zeus",
}

SEEDED_MERCURY_HADES_AXIS_CLUSTER = {
    "mercury-hades",
}

SEEDED_MERCURY_HADES_ACTIVATION_CLUSTER = {
    "mercury-hades-equals-admetos",
    "mercury-hades-equals-apollon",
    "mercury-hades-equals-asc",
    "mercury-hades-equals-cupido",
    "mercury-hades-equals-jupiter",
    "mercury-hades-equals-kronos",
    "mercury-hades-equals-mars",
    "mercury-hades-equals-mc",
    "mercury-hades-equals-moon",
    "mercury-hades-equals-neptune",
    "mercury-hades-equals-node",
    "mercury-hades-equals-pluto",
    "mercury-hades-equals-poseidon",
    "mercury-hades-equals-saturn",
    "mercury-hades-equals-sun",
    "mercury-hades-equals-uranus",
    "mercury-hades-equals-venus",
    "mercury-hades-equals-vernal-point",
    "mercury-hades-equals-vulcanus",
    "mercury-hades-equals-zeus",
}

SEEDED_MERCURY_JUPITER_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-jupiter-equals-admetos",
    "mercury-jupiter-equals-apollon",
    "mercury-jupiter-equals-chiron",
    "mercury-jupiter-equals-cupido",
    "mercury-jupiter-equals-hades",
    "mercury-jupiter-equals-kronos",
    "mercury-jupiter-equals-poseidon",
    "mercury-jupiter-equals-vernal-point",
    "mercury-jupiter-equals-vulcanus",
    "mercury-jupiter-equals-zeus",
}

SEEDED_MERCURY_MARS_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-mars-equals-admetos",
    "mercury-mars-equals-apollon",
    "mercury-mars-equals-chiron",
    "mercury-mars-equals-cupido",
    "mercury-mars-equals-hades",
    "mercury-mars-equals-kronos",
    "mercury-mars-equals-poseidon",
    "mercury-mars-equals-vernal-point",
    "mercury-mars-equals-vulcanus",
    "mercury-mars-equals-zeus",
}

SEEDED_MERCURY_MC_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-mc-equals-admetos",
    "mercury-mc-equals-apollon",
    "mercury-mc-equals-chiron",
    "mercury-mc-equals-cupido",
    "mercury-mc-equals-hades",
    "mercury-mc-equals-kronos",
    "mercury-mc-equals-poseidon",
    "mercury-mc-equals-vernal-point",
    "mercury-mc-equals-vulcanus",
    "mercury-mc-equals-zeus",
}

SEEDED_MERCURY_KRONOS_AXIS_CLUSTER = {
    "mercury-kronos",
}

SEEDED_MERCURY_KRONOS_ACTIVATION_CLUSTER = {
    "mercury-kronos-equals-admetos",
    "mercury-kronos-equals-apollon",
    "mercury-kronos-equals-asc",
    "mercury-kronos-equals-cupido",
    "mercury-kronos-equals-hades",
    "mercury-kronos-equals-jupiter",
    "mercury-kronos-equals-mars",
    "mercury-kronos-equals-mc",
    "mercury-kronos-equals-moon",
    "mercury-kronos-equals-neptune",
    "mercury-kronos-equals-node",
    "mercury-kronos-equals-pluto",
    "mercury-kronos-equals-poseidon",
    "mercury-kronos-equals-saturn",
    "mercury-kronos-equals-sun",
    "mercury-kronos-equals-uranus",
    "mercury-kronos-equals-venus",
    "mercury-kronos-equals-vernal-point",
    "mercury-kronos-equals-vulcanus",
    "mercury-kronos-equals-zeus",
}

SEEDED_MERCURY_MERCURY_AXIS_CLUSTER = {
    "mercury-mercury",
}

SEEDED_MERCURY_MERCURY_ACTIVATION_CLUSTER = {
    "mercury-mercury-equals-admetos",
    "mercury-mercury-equals-apollon",
    "mercury-mercury-equals-asc",
    "mercury-mercury-equals-cupido",
    "mercury-mercury-equals-hades",
    "mercury-mercury-equals-jupiter",
    "mercury-mercury-equals-kronos",
    "mercury-mercury-equals-mars",
    "mercury-mercury-equals-mc",
    "mercury-mercury-equals-moon",
    "mercury-mercury-equals-neptune",
    "mercury-mercury-equals-node",
    "mercury-mercury-equals-pluto",
    "mercury-mercury-equals-poseidon",
    "mercury-mercury-equals-saturn",
    "mercury-mercury-equals-sun",
    "mercury-mercury-equals-uranus",
    "mercury-mercury-equals-venus",
    "mercury-mercury-equals-vernal-point",
    "mercury-mercury-equals-vulcanus",
    "mercury-mercury-equals-zeus",
}

SEEDED_MERCURY_NEPTUNE_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-neptune-equals-admetos",
    "mercury-neptune-equals-apollon",
    "mercury-neptune-equals-chiron",
    "mercury-neptune-equals-cupido",
    "mercury-neptune-equals-hades",
    "mercury-neptune-equals-kronos",
    "mercury-neptune-equals-poseidon",
    "mercury-neptune-equals-vernal-point",
    "mercury-neptune-equals-vulcanus",
    "mercury-neptune-equals-zeus",
}

SEEDED_MERCURY_NODE_ADDITIONAL_ACTIVATION_CLUSTER = {
    "mercury-node-equals-admetos",
    "mercury-node-equals-apollon",
    "mercury-node-equals-chiron",
    "mercury-node-equals-cupido",
    "mercury-node-equals-hades",
    "mercury-node-equals-kronos",
    "mercury-node-equals-poseidon",
    "mercury-node-equals-vernal-point",
    "mercury-node-equals-vulcanus",
    "mercury-node-equals-zeus",
}


def test_seeded_relationship_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_RELATIONSHIP_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_growth_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_GROWTH_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_expansion_pressure_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_EXPANSION_PRESSURE_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_luminary_pressure_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_LUMINARY_PRESSURE_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_and_outer_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_AND_OUTER_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_pluto_and_mercury_jupiter_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_PLUTO_AND_MERCURY_JUPITER_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_angle_node_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ANGLE_NODE_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_venus_saturn_uranus_pluto_personal_point_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_VENUS_SATURN_URANUS_PLUTO_PERSONAL_POINT_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_asc_and_mercury_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_ASC_AND_MERCURY_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_asc_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_ASC_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_jupiter_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_JUPITER_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_mars_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_MARS_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_mc_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_MC_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_mercury_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_MERCURY_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_moon_initial_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_MOON_INITIAL_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_moon_completion_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_MOON_COMPLETION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_neptune_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_NEPTUNE_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_node_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_NODE_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_pluto_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_PLUTO_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_saturn_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_SATURN_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_uranus_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_URANUS_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_venus_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_VENUS_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_admetos_initial_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_ADMETOS_INITIAL_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_admetos_completion_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_ADMETOS_COMPLETION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_apollon_initial_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_APOLLON_INITIAL_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_apollon_completion_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_APOLLON_COMPLETION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_jupiter_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_JUPITER_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_neptune_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_NEPTUNE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_mc_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_MC_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_neptune_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_NEPTUNE_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_node_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_NODE_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_pluto_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_PLUTO_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_saturn_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_SATURN_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_uranus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_URANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_saturn_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_SATURN_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_uranus_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_URANUS_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_asc_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_ASC_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_jupiter_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_JUPITER_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_jupiter_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_JUPITER_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_neptune_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_NEPTUNE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_saturn_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_SATURN_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_uranus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_URANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_mercury_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_MERCURY_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_mars_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_MARS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_neptune_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_NEPTUNE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_mercury_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_MERCURY_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_mars_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_MARS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_saturn_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_SATURN_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_jupiter_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_JUPITER_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_uranus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_URANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_uranus_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_URANUS_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_uranus_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_URANUS_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_saturn_neptune_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SATURN_NEPTUNE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_saturn_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SATURN_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_saturn_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SATURN_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_saturn_uranus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SATURN_URANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_saturn_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SATURN_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_saturn_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SATURN_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_neptune_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_NEPTUNE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_uranus_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_URANUS_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_uranus_neptune_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_URANUS_NEPTUNE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_jupiter_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_JUPITER_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_mars_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_MARS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_mercury_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_MERCURY_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_neptune_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_NEPTUNE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_saturn_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_SATURN_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_uranus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_URANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_moon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_MOON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_sun_venus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SUN_VENUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_venus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_VENUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_jupiter_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_JUPITER_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_neptune_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_NEPTUNE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_pluto_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_PLUTO_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_poseidon_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_POSEIDON_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_saturn_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_SATURN_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_saturn_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_SATURN_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_uranus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_URANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_uranus_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_URANUS_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_venus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_VENUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_venus_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_VENUS_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_vulcanus_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_VULCANUS_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_zeus_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_ZEUS_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_admetos_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_ADMETOS_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_apollon_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_APOLLON_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_cupido_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_CUPIDO_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_hades_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_HADES_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_kronos_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_KRONOS_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_poseidon_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_POSEIDON_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_vulcanus_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_VULCANUS_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_zeus_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_ZEUS_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_chiron_family_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_CHIRON_FAMILY_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_moon_neptune_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MOON_NEPTUNE_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_cupido_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_CUPIDO_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_hades_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_HADES_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_mixed_may02_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_MIXED_MAY02_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_kronos_residual_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_KRONOS_RESIDUAL_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_neptune_initial_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_NEPTUNE_INITIAL_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_node_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NODE_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_neptune_vulcanus_residual_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NEPTUNE_VULCANUS_RESIDUAL_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_node_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NODE_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_node_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_NODE_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_pluto_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_PLUTO_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_pluto_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_PLUTO_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_pluto_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_PLUTO_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_pluto_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_PLUTO_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_saturn_sun_uranus_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_SATURN_SUN_URANUS_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_uranus_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_URANUS_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_jupiter_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_JUPITER_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_mars_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_MARS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_saturn_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_SATURN_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_venus_uranus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VENUS_URANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_vernal_point_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VERNAL_POINT_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_vernal_point_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_VERNAL_POINT_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_admetos_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ADMETOS_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_admetos_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ADMETOS_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_admetos_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ADMETOS_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_admetos_poseidon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ADMETOS_POSEIDON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_admetos_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ADMETOS_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_admetos_vulcanus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ADMETOS_VULCANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_admetos_vulcanus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ADMETOS_VULCANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_apollon_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_APOLLON_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_factor_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_FACTOR_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_apollon_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_APOLLON_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_apollon_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_APOLLON_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_apollon_apollon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_APOLLON_APOLLON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_apollon_apollon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_APOLLON_APOLLON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_apollon_poseidon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_APOLLON_POSEIDON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_apollon_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_APOLLON_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_apollon_vulcanus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_APOLLON_VULCANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_apollon_vulcanus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_APOLLON_VULCANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_apollon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_APOLLON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_apollon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_APOLLON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_asc_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_ASC_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_cupido_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_CUPIDO_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_cupido_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_CUPIDO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_hades_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_HADES_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_hades_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_HADES_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_kronos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_KRONOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_kronos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_KRONOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_poseidon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_POSEIDON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_vulcanus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_VULCANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_vulcanus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_VULCANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_zeus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_ZEUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_asc_zeus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_ASC_ZEUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_asc_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_ASC_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_asc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_ASC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_mc_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_MC_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_neptune_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_NEPTUNE_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_neptune_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_NEPTUNE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_node_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_NODE_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_node_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_NODE_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_pluto_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_PLUTO_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_pluto_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_PLUTO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_uranus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_URANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_chiron_uranus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CHIRON_URANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_apollon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_APOLLON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_apollon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_APOLLON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_cupido_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_CUPIDO_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_cupido_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_CUPIDO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_hades_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_HADES_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_hades_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_HADES_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_kronos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_KRONOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_kronos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_KRONOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_poseidon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_POSEIDON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_vulcanus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_VULCANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_vulcanus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_VULCANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_zeus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_ZEUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_cupido_zeus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_CUPIDO_ZEUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_apollon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_APOLLON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_apollon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_APOLLON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_hades_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_HADES_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_hades_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_HADES_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_kronos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_KRONOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_kronos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_KRONOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_poseidon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_POSEIDON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_vulcanus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_VULCANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_vulcanus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_VULCANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_zeus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_ZEUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_hades_zeus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_HADES_ZEUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_apollon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_APOLLON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_apollon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_APOLLON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_asc_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_ASC_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_chiron_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_CHIRON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_chiron_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_CHIRON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_cupido_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_CUPIDO_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_cupido_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_CUPIDO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_hades_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_HADES_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_hades_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_HADES_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_jupiter_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_JUPITER_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_jupiter_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_JUPITER_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_kronos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_KRONOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_kronos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_KRONOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_poseidon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_POSEIDON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_vulcanus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_VULCANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_vulcanus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_VULCANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_zeus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_ZEUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_jupiter_zeus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_JUPITER_ZEUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_apollon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_APOLLON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_apollon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_APOLLON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_kronos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_KRONOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_kronos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_KRONOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_poseidon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_POSEIDON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_vulcanus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_VULCANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_kronos_vulcanus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_KRONOS_VULCANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_apollon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_APOLLON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_apollon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_APOLLON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_chiron_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_CHIRON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_chiron_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_CHIRON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_cupido_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_CUPIDO_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_cupido_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_CUPIDO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_hades_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_HADES_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_hades_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_HADES_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_kronos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_KRONOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_kronos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_KRONOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_mars_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_MARS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_mars_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_MARS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_mc_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_MC_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_neptune_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_NEPTUNE_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_node_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_NODE_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_pluto_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_PLUTO_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_poseidon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_POSEIDON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_saturn_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_SATURN_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_uranus_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_URANUS_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_vulcanus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_VULCANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_vulcanus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_VULCANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_zeus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_ZEUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mars_zeus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MARS_ZEUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_apollon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_APOLLON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_apollon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_APOLLON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_cupido_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_CUPIDO_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_cupido_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_CUPIDO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_hades_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_HADES_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_hades_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_HADES_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_kronos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_KRONOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_kronos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_KRONOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_mc_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_MC_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_mc_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_MC_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_poseidon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_POSEIDON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_poseidon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_POSEIDON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_vulcanus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_VULCANUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_vulcanus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_VULCANUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_zeus_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_ZEUS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mc_zeus_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MC_ZEUS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_admetos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_ADMETOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_admetos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_ADMETOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_apollon_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_APOLLON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_apollon_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_APOLLON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_asc_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_ASC_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_chiron_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_CHIRON_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_chiron_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_CHIRON_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_cupido_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_CUPIDO_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_cupido_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_CUPIDO_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_hades_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_HADES_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_hades_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_HADES_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_jupiter_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_JUPITER_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_mars_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_MARS_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_mc_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_MC_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_kronos_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_KRONOS_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_kronos_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_KRONOS_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_mercury_axis_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_MERCURY_AXIS_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_mercury_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_MERCURY_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_neptune_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_NEPTUNE_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_seeded_mercury_node_additional_activation_cluster_has_real_derived_synthesis():
    by_slug = manifest_by_slug()

    for slug in SEEDED_MERCURY_NODE_ADDITIONAL_ACTIVATION_CLUSTER:
        record = by_slug[slug]
        assert record["retrieval_role"] == "canonical_answer"
        assert record["has_real_derived_synthesis"] is True or is_deferred_answer_surface(record)
        assert record["answer_surface"] is True


def test_all_answer_surfaces_have_real_derived_synthesis():
    missing = sorted(
        page["slug"]
        for page in manifest_pages()
        if page.get("answer_surface")
        and not page.get("has_real_derived_synthesis", False)
        and not is_deferred_answer_surface(page)
    )
    assert missing == []

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
import json
from pathlib import Path
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.query_manifest import write_query_artifacts
from tools.rebuild_index import build_index
from tools.udo_rudolph_abc_source import (
    FACTOR_SEQUENCE,
    ActivationEntry,
    AxisBlock,
    FactorBlock,
    generate_models,
)
from tools.wiki_identity import (
    astronomicon_token,
    factor_slug,
    normalize_activation,
    normalize_axis,
    normalize_factor,
    normalize_triad,
)
from tools.wiki_links import DERIVED_SYNTHESIS_ANCHOR, explicit_anchor
from tools.wiki_pages import load_page


UPDATED_AT = "2026-05-04"
SOURCE_SLUG = "udo-rudolph-abc-fur-planetenbilder"
SOURCE_TITLE = "Udo Rudolph - ABC für Planetenbilder"
LEGACY_SOURCE_TITLES = {"Udo Rudolph - ABC fĂĽr Planetenbilder"}
SOURCE_FILE = "Udo-Rudolph_ABC-fur-Planetenbilder.pdf"
TRANSLATION_CACHE_FILE = "udo_rudolph_abc_translations.json"
SOURCE_FRAMEWORK_SCOPE = "hamburg_school"
LEGACY_SOURCE_TITLES = LEGACY_SOURCE_TITLES | {SOURCE_TITLE}
SOURCE_TITLE = "Udo Rudolph - ABC for Planetary Pictures"
ENGLISH_ONLY_REPLACEMENTS = (
    (r"\bOff(?:en|cnt|t|ent!|ent\?|ont|f?r\.nicht|fentlich|fentliche|fentlichkeits|tlichkeit|entlichkcit|entkcit|klichkcit|tlichkcit|fentlichkcit|fentlichkeit)\w*\b", "public"),
    (r"\b[Mm][fl]?entliche[nr]?\b", "public"),
    (r"\bÖffentlich\w*\b", "public"),
    (r"\böftlich\w*\b", "public"),
    (r"\b(Jffr:lichkcit|Ofklichkcit|Openlichkeit)\b", "public"),
    (r"\bder\b|\bdie\b|\bdas\b|\bden\b|\bdem\b|\bdes\b", "the"),
    (r"\bin der\b|\bim\b|\bin dcr\b|\bin einer\b|\bin einem\b", "in the"),
    (r"\bzur\b|\bzum\b", "to the"),
    (r"\bUber\b|\bOber\b|\büber\b", "about"),
    (r"<lurch|\blurch\b|\bdurch\b|\bdurcb\b", "through"),
    (r"\b(fur|für|flir|ft\.ir|f\.ir)\b", "for"),
    (r"\bHannon(?:ie|y|ia|ic|ian|ischen|izing)\b", "harmony"),
    (r"\bHarmonie\b", "harmony"),
    (r"\bHarmonie-Verlust\b", "harmony loss"),
    (r"\bHannonie-Verlust\b", "harmony loss"),
    (r"\bLiebe(?:s)?\b", "love"),
    (r"\bLiebes-?([A-Za-z]+)\b", r"love \1"),
    (r"\bLiebcs-?([A-Za-z]+)\b", r"love \1"),
    (r"\bKunst\b", "art"),
    (r"\bKunst-?([A-Za-z]+)\b", r"art \1"),
    (r"\bKünst(?:[-A-Za-z0-9]*)?\b", "art"),
    (r"\bktinstlerical\b", "artistic"),
    (r"\bKtinstler\b|\bktinstler\b", "artist"),
    (r"\bktinstleric\b", "artistic"),
    (r"\b[Kk](?:[IiUü]|il)nstler(?:ische|ischer|isches|isch|n|m)?\b", "artistic"),
    (r"\bkOnstler(?:ische|ischer|isches|isch|n|m)?\b", "artistic"),
    (r"\bkülnstlerische\b", "artistic"),
    (r"\bMensch(?:en)?\b", "people"),
    (r"\bMenschcn\b", "people"),
    (r"\bPersonen\b", "persons"),
    (r"\bManner\b", "men"),
    (r"\bMann(?:es)?\b", "man"),
    (r"\bFrau(?:en)?\b", "women"),
    (r"\bFraucn\b", "women"),
    (r"\bGemeinschaft(?:en)?\b", "community"),
    (r"\bCemeinschaft(?:en)?\b|\bGemcinschaft\b|\bGcmeinschaft\b|\bGcmeinschafl\b|\bGcminähl\b|\bFrauengemeinschaft\b", "community"),
    (r"\bGemeinschafts\b", "community"),
    (r"\bgemeinsame\b|\bgemeinsamer\b|\bgemeinsames\b", "common"),
    (r"\bgemeinsamen\b", "common"),
    (r"\bGcmeinsamer\b", "common"),
    (r"\bGcmeinschafts\b", "community"),
    (r"\bGemi\.?its-Gemeinschaften\b", "emotional communities"),
    (r"\bVolk(?:es|er|ers)?\b|\bYolk(?:es|er|ers)?\b|\bY\s?olks\b", "people"),
    (r"\bVolkcs\b|\bVolks\b", "people"),
    (r"\bVerbindung(?:en)?\b|\bYerbindung(?:en)?\b|\bYerbindungen\b|\bVerbund\b|\bYerbund\b", "connection"),
    (r"\bVerbindigung\b|\bYerbindigung\b", "connection"),
    (r"\bBeziehungen\b|\bBeziehung\b", "relationships"),
    (r"\bKontakt(?:e)?\b", "contact"),
    (r"\bVermittlung(?:s)?\b|\bYermittlungs\b", "mediation"),
    (r"\bVereinigung\b|\bVereindungen\b", "union"),
    (r"\bVergangenheit\b|\bYergangenheit\b", "past"),
    (r"\bVerlust(?:e)?\b|\bYerlust(?:e)?\b", "loss"),
    (r"\bVerzicht\b|\bYerzicht\b", "renunciation"),
    (r"\bVeranderungen\b|\bYeranderings\b|\bYeranderung\b|\bVcranderungen\b|\bVeränderungen\b|\bVerande-\b|\bY erandep\.mg\b", "changes"),
    (r"\bVerandcrung\b|\bVerandcrungen\b", "changes"),
    (r"\boffentliche\b|\boffentlichen\b", "public"),
    (r"\bVorliebe\b|\bYorliebe\b|\bOrliebe\b|\bV orliebe\b", "preference"),
    (r"\bTatigkeit\b|\bTätigkeit\b|\bBitigkeit\b|\bFatigkeit\b", "activity"),
    (r"\bAktivität\b", "activity"),
    (r"\bHandlungen\b", "actions"),
    (r"\bArbeit\b", "work"),
    (r"\bArbeits\b|\brbeits\b", "work"),
    (r"\bFreude\b", "joy"),
    (r"\bFrcudc\b", "joy"),
    (r"\bWunsch(?:e)?\b|\bWilnsche\b|\bWiinsche\b|\bVtinsche\b", "wishes"),
    (r"\bGeist(?:es|liche|licher|igen)?\b", "spirit"),
    (r"\bgeistige\b", "spiritual"),
    (r"\bSeele\b|\bSee le\b|\bSeelc\b|\bSeelcn\b", "soul"),
    (r"\bSeelen-?([A-Za-z]+)\b", r"soul \1"),
    (r"\bBcseelte\b|\bBeseltc\b|\bbeselte\b|\bbeseelte\b|\bbcseelte\b|\bbcscelter\b|\bbzzeelte\b|\bbesekler\b", "soulful"),
    (r"\blkscelte\b|\bbesceltcs\b", "soulful"),
    (r"\bKorper\b|\bKarper\b|\bkarper\b|\bkoper\b|\bKörper\b", "body"),
    (r"\bkorperliche\b|\bkarperliche\b|\bkoperliche\b", "physical"),
    (r"\bStaat(?:s)?\b|\bStaal\b", "state"),
    (r"\bBehorden\b", "authorities"),
    (r"\bMacht\b", "power"),
    (r"\bGewalt\b", "force"),
    (r"\bEinfluf3\b|\bEinfiuflrciche\b|\bInfluf3\b|\bEintluB\b|\bEinfluB\b", "influence"),
    (r"\bFührung\b|\bFiihrung\b|\bFOhrung\b|\bfLihrung\b", "leadership"),
    (r"\bfli?ehrend\b|\bfLihrend\b|\bflihrende\b|\bflirende\b|\bführend\b", "leading"),
    (r"\bGefihl\b|\bGefilhl\b|\bGefehl\b|\bGcfLihl\b", "feeling"),
    (r"\bGedanken\b|\bGcdanken\b", "thoughts"),
    (r"\bBcwegliche\b", "mobile"),
    (r"\bGemiits Bewegung\b", "emotional movement"),
    (r"\bGesprach(?:e|en)?\b|\bGcsprachc\b|\bGespri:iche\b|\bGeprache\b", "conversation"),
    (r"\bNachrichten\b", "reports"),
    (r"\bMedien\b|\bMcdien\b", "media"),
    (r"\bRechts-?([A-Za-z]+)?\b", "legal"),
    (r"\bRecht(?:es|0)?\b|\bRightes\b", "legal"),
    (r"\bGeld(?:es)?\b", "money"),
    (r"\bGdd\b|\bCield\b", "money"),
    (r"\bGlUck\b|\bGli\.?ick\b|\bGHick\b|\bGIUck\b|\bGlilck\b|\bglicklich\b", "happiness"),
    (r"\bGlück\b|\bgltickliche\b|\bg!Umliche\b|\bGli\.icks-Gefähigkeit\b", "happiness"),
    (r"\bSchonheit\b|\bschonheit\b|\bSchönheit\b", "beauty"),
    (r"\bSchaffen\b|\bschopferisch(?:en|er|es|e)?\b|\bschaferisch(?:en|er|es|e)?\b", "creative"),
    (r"\bGri\.indliche Seelen-!3ekritik\b", "thorough soul criticism"),
    (r"\bgrundlich\b", "thoroughly"),
    (r"\bunderdriicking\b", "suppressing"),
    (r"\bWahrheit\b|\bWhrheit\b|\bWahrhcit\b|\bwürheit\b", "truth"),
    (r"\bKlarheit\b|\bKlarhcit\b|\bKlarität\b", "clarity"),
    (r"\bVemunft\b|\bVcmunn\b", "reason"),
    (r"\bAufgaben\b|\bAufgabe\b", "tasks"),
    (r"\bufgabe\b", "task"),
    (r"\bProblem(?:e|s)?\b|\bProbleme\b", "problems"),
    (r"\bStorung(?:en)?\b|\bStörung(?:en)?\b|\bSteorte\b|\bstorte\b|\bgeorte\b|\bgesWrtc\b", "disturbance"),
    (r"\bemste\b|\bEmste\b", "serious"),
    (r"\bErnste\b|\bernste\b", "serious"),
    (r"\bErschwerte\b", "difficult"),
    (r"\bAuflösung\b", "dissolution"),
    (r"\bAlter\b|\bAlters\b", "old age"),
    (r"\bOrt(?:s)?\b", "place"),
    (r"\bOr1\b", "place"),
    (r"\bPlatzen\b", "places"),
    (r"\bPlatz\b", "place"),
    (r"\bUmwelt\b|\bUmwclt\b", "environment"),
    (r"\bUmgebung\b", "environment"),
    (r"\bUm world\b", "environment"),
    (r"\bWelt\b", "world"),
    (r"\bLeeben\b|\bLeben\b", "life"),
    (r"\bTag\b", "day"),
    (r"\bZentrum\b", "center"),
    (r"\bJugend\b|\bJugendliche\b", "youth"),
    (r"\bWasser\b", "water"),
    (r"\bLuft\b", "air"),
    (r"\bFeuer\b", "fire"),
    (r"\bMetaphysik\b", "metaphysics"),
    (r"\bKultur\b", "culture"),
    (r"\bErkenntnisse\b|\bErkenntnis\b", "insight"),
    (r"\bklare\b", "clear"),
    (r"\bZukunfts\b|\bZukunft\b", "future"),
    (r"\bmctaphysischcn\b", "metaphysical"),
    (r"\bFcingefLihl\b", "subtle feeling"),
    (r"\bEntwicklung\b", "development"),
    (r"\bentwickeln\b", "developing"),
    (r"\bEntfaltung\b", "development"),
    (r"\bMeinungs\b", "opinion"),
    (r"\bMeinung\b", "opinion"),
    (r"\bAnderungen\b", "changes"),
    (r"\bSprach\b", "language"),
    (r"\bWort\b", "word"),
    (r"\bWechsel\b", "exchange"),
    (r"\bwachsender\b", "growing"),
    (r"\bVerkehr\b", "traffic"),
    (r"\bDenken\b", "thinking"),
    (r"\bJugend\b", "youth"),
    (r"\bStunde\b", "hour"),
    (r"\bMutter\b", "mother"),
    (r"\bGefahrdeter\b", "endangered"),
    (r"\bHandlungcn\b", "actions"),
    (r"\bGesprache\b|\bGespraeche\b", "conversations"),
    (r"\(\)ffentlichkeit\b|\bOeffentlichkeit\b|\bOffentlichkeit\b", "public"),
    (r"\bGestaltung\b", "design"),
    (r"\bErfolg\b|\bErfolgreicher\b|\berfolgreicher\b", "success"),
    (r"\bErweiterung\b", "expansion"),
    (r"\bFriedens\b|\bFried ens\b", "peace"),
    (r"\bVenn utlung\b", "mediation"),
    (r"\bmehrende\b", "increasing"),
    (r"\bGrolles\b|\bgroßes\b|\bgrof3e\b|\bFroß\b|\bGroß\b", "great"),
    (r"\bAndauemde\b", "enduring"),
    (r"\bEinschränkungen\b", "restrictions"),
    (r"\bblokkiert\b", "blocked"),
    (r"\bBclastung\b", "burden"),
    (r"\bmcin\b|\brnein\b", "my"),
    (r"\bmcine\b|\brncine\b", "my"),
    (r"\bmeinc\b|\bmciner\b|\bmeiner\b|\bmein(?:e|er|es)?\b", "my"),
    (r"\bpersanliche\b|\bpersanelicher\b|\bpersönliche\b", "personal"),
    (r"\bpersonliche\b", "personal"),
    (r"\bandercr\b|\banderer\b", "others"),
    (r"\bcincr\b", "a"),
    (r"\bHerstellung\b", "production"),
    (r"\bWille\b", "will"),
    (r"\bvie!\b", "much"),
    (r"\bRaum\b", "space"),
    (r"\beineste\b|\beinemste\b|\bemster\b", "serious"),
    (r"\bSelbstandig\b|\bself-andy\b", "independent"),
    (r"\bAutoritat\b", "authority"),
    (r"\bDominanz\b", "dominance"),
    (r"\bHierarchie\b|\bHierarchy\b", "hierarchy"),
    (r"\bvon\b", "of"),
    (r"\bund\b", "and"),
    (r"\bam\b", "at the"),
    (r"\bmit\b", "with"),
    (r"\bgegen\b", "against"),
    (r"\bzu\b", "to"),
    (r"\baus\b", "from"),
    (r"\bciner\b|\beiner\b|\beinem\b|\beines\b|\bdcm\b", "a"),
    (r"\bde2\b", "of"),
    (r"\bfiber\b|\btiber\b|\bi\.iber\b", "about"),
    (r"\bF\s?eur\b", "fire"),
    (r"\bflühle\b|\bgefLühle\b|\bGeft\.ihls\b|\bgemUts\b", "feelings"),
    (r"\bGefiihle\b|\bGefiiM\b|\bGefuhlc\b|\bGefUhle\b|\bGefLihle\b|\bGefilhls\b|\bGeftihls\b|\bGcfuhls\b|\bGcfuhl\b|\bCefiihle\b|\bCefi\.ihle\b", "feelings"),
    (r"\bGeflihl\b|\bGeflihls\b", "feeling"),
    (r"\bGemUt\b|\bGemUts\b|\bCemiit\b|\bCern i\.its\b", "emotional"),
    (r"\bGemiitsGcmeinschaft\b|\bGemuts-Gemeinschat1\b", "emotional community"),
    (r"\bGemeinschat1\b", "community"),
    (r"\bsoul-\s+and feelings community\b", "soul and emotional community"),
    (r"\bSynthcse\b", "synthesis"),
    (r"\bFables\b", "feelings"),
    (r"\bailments\b", "feelings"),
    (r"\bPeople's Corps\b", "people's body"),
    (r"\bCorps\b", "body"),
    (r"\bFtille\b", "fullness"),
    (r"\bMediaDevelopment\b", "media development"),
    (r"\biiber\b|\bUber\b", "about"),
    (r"\bueber\b", "about"),
    (r"\bOeffentlichkeit\b", "public"),
    (r"\bGespraeche\b", "conversations"),
    (r"\bde\.-", "of the"),
    (r"\bLanguage about Evolution\b", "conversations about evolution"),
    (r"\bWord change\b", "word exchange"),
    (r"\bdevelopment the\b", "development of the"),
    (r"\bchanges the\b", "changes in the"),
    (r"\bpeople the\b", "people in the"),
    (r"\bpersons community\b", "community of persons"),
    (r"\bmen community\b", "men's community"),
    (r"\b([A-Za-z]+) a community\b", r"\1 of a community"),
    (r"\bof of a\b", "of a"),
    (r"\binsight a metaphysical community\b", "insight into a metaphysical community"),
    (r"\bart and culture the future\b", "art and culture of the future"),
    (r"\b([A-Za-z]+) the women\b", r"\1 of women"),
    (r"\binsight community\b", "community insight"),
    (r"\bPartner\b", "partner"),
    (r"\bMedi en\b", "media"),
)
TRANSLATION_SOURCE_REPLACEMENTS = (
    (r"\biiber\b", "ueber"),
    (r"\bY er", "Ver"),
    (r"\bV cr", "Ver"),
    (r"\bGcsprache\b|\bGcsprachc\b", "Gespraeche"),
    (r"\bJugcnd\b", "Jugend"),
    (r"\bDcnkcn\b", "Denken"),
    (r"\bWcchsel\b", "Wechsel"),
    (r"\bdcr\b|\bdcs\b|\bdcn\b", "der"),
    (r"\bMfcntlichcn\b|\boffcntlichcn\b|\bOffcntlichkeit\b|\bOncntlichkcit\b|\bOtkntlichkcit\b|\b\(\)ffentlichkeit\b", "Oeffentlichkeit"),
    (r"\bOff(?:en|cnt|t|ent!|fentlich|entlichkcit|entkcit|klichkcit|tlichkcit|fentlichkcit|fentlichkeit)\w*\b", "Öffentlichkeit"),
    (r"\b[Mm][fl]?entliche[nr]?\b", "öffentlichen"),
    (r"\bOber\b|\bUber\b", "über"),
    (r"\bflir\b|\bf\.ir\b|\bft\.ir\b|\bfur\b", "für"),
    (r"\bfLihr|\bflihr|\bfiihr|\bFOhr", "führ"),
    (r"\bHannon", "Harmon"),
    (r"\bKUnst|\bKiinst|\bKilnst|\bkOnst|\bkünst", "Künst"),
    (r"\bKorper\b|\bKarper\b|\bkarper\b|\bkoper\b", "Körper"),
    (r"\bTatigkeit\b|\bFatigkeit\b|\bBitigkeit\b", "Tätigkeit"),
    (r"\bYer", "Ver"),
    (r"\bYor", "Vor"),
    (r"\bGlUck\b|\bGHick\b|\bGIUck\b|\bGlilck\b", "Glück"),
    (r"\bWiinsche\b|\bWilnsche\b|\bVtinsche\b", "Wünsche"),
    (r"\bSchonheit\b|\bschonheit\b", "Schönheit"),
    (r"\bschopfer|\bschafer", "schöpfer"),
    (r"\bWhrheit\b|\bWahrhcit\b", "Wahrheit"),
    (r"\bKlarhcit\b", "Klarheit"),
    (r"\bVcmunn\b", "Vernunft"),
    (r"\bBcseelte\b|\bBcschelte\b|\bBeseltc\b|\bbeselte\b|\bbcseelte\b|\bbcscelter\b|\bbzzeelte\b|\bbesekler\b", "beseelte"),
    (r"\bBclastung\b", "Belastung"),
    (r"\bmcin\b|\brnein\b", "mein"),
    (r"\bmcine\b|\brncine\b", "meine"),
    (r"\bpersanlich", "persönlich"),
    (r"\bemste\b|\bEmste\b", "ernste"),
    (r"\bStaal\b", "Staat"),
    (r"\bEinfluf3\b|\bInfluf3\b|\bEintluB\b|\bEinfluB\b", "Einfluss"),
    (r"<lurch|\blurch\b", "durch"),
)

WITTE_SLUG = "alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures"
WITTE_TITLE = "Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures"
EBERTIN_SLUG = "reinhold-ebertin-the-combination-of-stellar-influences"
EBERTIN_TITLE = "Reinhold Ebertin - The Combination of Stellar Influences"
FALIS_SLUG = "michelle-falis-planet-combinations-astrological-brainstorms"
FALIS_TITLE = "Michelle Falis - Planet Combinations: Astrological Brainstorms"
CARTER_SLUG = "charles-carter-the-astrological-aspects"
CARTER_TITLE = "Charles Carter - The Astrological Aspects"
SANDBACH_SLUG = "john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints"
SANDBACH_TITLE = "John Sandbach - Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints"
HAND_SLUG = "robert-hand-horoscope-symbols"
HAND_TITLE = "Robert Hand - Horoscope Symbols"
MCBROOM_SLUG = "don-mcbroom-midpoints"
MCBROOM_TITLE = "Don McBroom - Midpoints"
MUNKASEY_SLUG = "michael-munkasey-midpoints-unleashing-the-power-of-the-planets"
MUNKASEY_TITLE = "Michael Munkasey - Midpoints: Unleashing the Power of the Planets"

SOURCE_ORDER = [
    WITTE_SLUG,
    SOURCE_SLUG,
    EBERTIN_SLUG,
    FALIS_SLUG,
    CARTER_SLUG,
    SANDBACH_SLUG,
    HAND_SLUG,
    MCBROOM_SLUG,
    MUNKASEY_SLUG,
]

SOURCE_TITLES = {
    WITTE_SLUG: WITTE_TITLE,
    SOURCE_SLUG: SOURCE_TITLE,
    EBERTIN_SLUG: EBERTIN_TITLE,
    FALIS_SLUG: FALIS_TITLE,
    CARTER_SLUG: CARTER_TITLE,
    SANDBACH_SLUG: SANDBACH_TITLE,
    HAND_SLUG: HAND_TITLE,
    MCBROOM_SLUG: MCBROOM_TITLE,
    MUNKASEY_SLUG: MUNKASEY_TITLE,
}

SOURCE_SLUGS_BY_TITLE = {title: slug for slug, title in SOURCE_TITLES.items()}
SOURCE_SLUGS_BY_TITLE.update({title: SOURCE_SLUG for title in LEGACY_SOURCE_TITLES})

SCHEMA_CUES = {
    "psychology": (
        "seel",
        "gefuhl",
        "gefühl",
        "denken",
        "gedank",
        "meinung",
        "bewusstsein",
        "nervos",
        "freude",
        "wunsch",
        "erkenntnis",
        "wahrheit",
        "geist",
        "animated",
        "opinion",
        "soul",
        "feeling",
        "thought",
        "mind",
        "joy",
        "wish",
        "truth",
        "spirit",
    ),
    "body/health": (
        "korper",
        "körper",
        "krank",
        "gesund",
        "schmerz",
        "tod",
        "mensch",
        "person",
        "mann",
        "frau",
        "body",
        "physical",
        "health",
        "pain",
        "person",
        "man",
        "woman",
    ),
    "social/relationship": (
        "partner",
        "verbindung",
        "kontakt",
        "gemeinschaft",
        "volk",
        "umwelt",
        "liebe",
        "ehe",
        "familie",
        "ort",
        "partner",
        "relationship",
        "connection",
        "contact",
        "community",
        "people",
        "love",
        "affection",
        "family",
        "place",
    ),
    "events/manifestations": (
        "ereignis",
        "arbeit",
        "tatigkeit",
        "tätigkeit",
        "handlung",
        "geld",
        "finanz",
        "recht",
        "staat",
        "nachricht",
        "erfolg",
        "verlust",
        "gefahr",
        "entwicklung",
        "reform",
        "macht",
        "kultur",
        "event",
        "work",
        "activity",
        "action",
        "money",
        "financial",
        "law",
        "state",
        "news",
        "success",
        "loss",
        "danger",
        "development",
        "reform",
        "power",
        "culture",
    ),
}

DEFAULT_DERIVED_TEXT = ""
DEFAULT_FACTOR_CONTRADICTIONS = (
    "- Source differences on this factor page are preserved as framework emphasis rather than forced contradiction.\n"
    "- This page keeps the contributing source entries side by side instead of treating one as a gloss on the other."
)
DEFAULT_AXIS_CONTRADICTIONS = (
    "- No direct contradiction is recorded yet among the ingested source entries on this axis.\n"
    "- Differences are preserved as distinct source voices and framework emphases rather than flattened into one wording."
)
DEFAULT_ACTIVATION_CONTRADICTIONS = "- No direct contradiction is recorded yet among the ingested source entries on this activation."
UDO_DERIVED_HEADING = "### Udo Rudolph Deepening"


def _yaml_list(items: list[str], indent: int = 0) -> str:
    padding = " " * indent
    return "\n".join(f"{padding}- {item}" for item in items) if items else f"{padding}[]"


def _ordered_source_pages(items: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item not in seen:
            unique.append(item)
            seen.add(item)
    return sorted(unique, key=lambda slug: (SOURCE_ORDER.index(slug) if slug in SOURCE_ORDER else 999, slug))


def _framework_scope_for_sources(source_pages: list[str]) -> str:
    if len(_ordered_source_pages(source_pages)) > 1:
        return "comparative"
    return SOURCE_FRAMEWORK_SCOPE


def _section_body(body: str, heading: str) -> str:
    normalized = body.replace("\r\n", "\n")
    marker = f"## {heading}\n"
    if marker not in normalized:
        return ""
    section = normalized.split(marker, 1)[1]
    extracted = re.split(r"\n## ", section, maxsplit=1)[0].strip()
    derived_anchor = explicit_anchor(DERIVED_SYNTHESIS_ANCHOR)
    cleaned_lines = [line for line in extracted.splitlines() if line.strip() != derived_anchor]
    return "\n".join(cleaned_lines).strip()


def _source_entry_blocks(body: str) -> list[str]:
    section = _section_body(body, "Source Entries")
    if not section:
        return []
    return [block.strip() for block in re.split(r"(?m)(?=^### )", section.strip()) if block.strip()]


def _entry_title(block: str) -> str:
    match = re.match(r"^### ([^\n]+)", block)
    if match is None:
        raise ValueError("source entry block is missing a title heading")
    return match.group(1).strip()


def _canonical_source_title(title: str) -> str:
    if title in LEGACY_SOURCE_TITLES:
        return SOURCE_TITLE
    return title


def _with_source_title(block: str, title: str) -> str:
    return re.sub(r"^### [^\n]+", f"### {title}", block, count=1)


def _merge_source_entries(body: str, addition: str, title: str) -> str:
    blocks = _source_entry_blocks(body)
    existing_index = {
        _canonical_source_title(_entry_title(block)): index
        for index, block in enumerate(blocks)
    }
    by_title = {
        _canonical_source_title(_entry_title(block)): _with_source_title(
            block,
            _canonical_source_title(_entry_title(block)),
        )
        for block in blocks
    }
    canonical_title = _canonical_source_title(title)
    by_title[canonical_title] = _with_source_title(addition.strip(), canonical_title)
    ordered_titles = sorted(
        by_title,
        key=lambda item: (
            SOURCE_ORDER.index(SOURCE_SLUGS_BY_TITLE[item])
            if item in SOURCE_SLUGS_BY_TITLE and SOURCE_SLUGS_BY_TITLE[item] in SOURCE_ORDER
            else 999,
            existing_index.get(item, len(existing_index)),
            item.casefold(),
        ),
    )
    return "\n\n".join(by_title[item] for item in ordered_titles)


def _source_page_refs(body: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    for block in _source_entry_blocks(body):
        title = _canonical_source_title(_entry_title(block))
        page_match = re.search(r"- Source page: `([^`]+)`", block)
        if page_match:
            refs.append((title, page_match.group(1)))
        pages_match = re.search(r"- Source pages: `([^`]+)`", block)
        if pages_match:
            refs.append((title, pages_match.group(1)))
    return refs


def _factor_link(name: str) -> str:
    factor = normalize_factor(name)
    return f"- [{factor.display}](../factors/{factor.slug}.md)"


def _source_links(source_pages: list[str]) -> str:
    return "\n".join(
        f"- [{SOURCE_TITLES.get(slug, slug)}](../sources/{slug}.md)"
        for slug in _ordered_source_pages(source_pages)
    )


def _activation_identity_from_display(display: str):
    left, right = display.split("=")
    factor_a, factor_b = [part.strip() for part in left.split("/")]
    activated_by = right.strip()
    return normalize_activation(factor_a, factor_b, activated_by)


def _activation_link(display: str) -> str:
    identity = _activation_identity_from_display(display)
    return f"- [{identity.display}](../activations/{identity.slug}.md)"


def _triad_names_from_activations(activations: list[str]) -> list[str]:
    names = {
        " ".join(_activation_identity_from_display(display).triad_set)
        for display in activations
        if _activation_identity_from_display(display).has_distinct_triad
    }
    return sorted(names, key=str.casefold)


def _astronomicon_axis(factor_a: str, factor_b: str) -> str:
    return f"{astronomicon_token(factor_a)}/{astronomicon_token(factor_b)}"


def _load_translation_cache(root: Path) -> dict[str, str]:
    path = root / "tools" / TRANSLATION_CACHE_FILE
    return json.loads(path.read_text(encoding="utf-8"))


def _apply_text_replacements(text: str, replacements: tuple[tuple[str, str], ...]) -> str:
    cleaned = text
    for pattern, replacement in replacements:
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s+([,.;:])", r"\1", cleaned)
    cleaned = re.sub(r"\bthe the\b", "the", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def _normalize_translation_source_text(text: str) -> str:
    return _apply_text_replacements(text, TRANSLATION_SOURCE_REPLACEMENTS)


def _clean_english_translation(text: str) -> str:
    cleaned = _apply_text_replacements(text, ENGLISH_ONLY_REPLACEMENTS)
    cleaned = cleaned.replace("' '", ",")
    cleaned = re.sub(r"\b([A-Za-z]+)-([A-Za-z]+)\b", r"\1 \2", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" ,")


def _translate_text(text: str, translation_lookup: Mapping[str, str] | None) -> str:
    if translation_lookup is None:
        return text
    try:
        return _clean_english_translation(translation_lookup[text])
    except KeyError as error:
        raise KeyError(f"missing Udo Rudolph English translation for: {text}") from error


def _required_translation_texts(
    factor_blocks: tuple[FactorBlock, ...],
    axis_blocks: tuple[AxisBlock, ...],
) -> list[str]:
    texts: list[str] = []
    for block in factor_blocks:
        texts.append(block.text)
    for block in axis_blocks:
        texts.append(block.summary)
        texts.extend(entry.text for entry in block.activation_entries)
    unique: list[str] = []
    seen: set[str] = set()
    for text in texts:
        if text not in seen:
            unique.append(text)
            seen.add(text)
    return unique


def _assert_translation_coverage(
    factor_blocks: tuple[FactorBlock, ...],
    axis_blocks: tuple[AxisBlock, ...],
    translation_lookup: Mapping[str, str],
) -> None:
    missing = [
        text
        for text in _required_translation_texts(factor_blocks, axis_blocks)
        if text not in translation_lookup or not translation_lookup[text].strip()
    ]
    if missing:
        preview = "\n".join(f"- {text}" for text in missing[:10])
        remainder = "" if len(missing) <= 10 else f"\n... and {len(missing) - 10} more"
        raise ValueError(f"missing Udo Rudolph English translations:\n{preview}{remainder}")


def _split_claims(text: str) -> list[str]:
    return [
        claim.strip(" .;:")
        for claim in re.split(r",\s*", text)
        if claim.strip(" .;:")
    ]


def _schema_claims(text: str, category: str) -> list[str]:
    cues = SCHEMA_CUES[category]
    matches: list[str] = []
    for claim in _split_claims(text):
        folded = claim.casefold()
        if any(cue in folded for cue in cues):
            matches.append(claim)
        if len(matches) == 3:
            break
    return matches


def _format_schema_mapping(text: str) -> str:
    claims = _split_claims(text)
    core = claims[0] if claims else "No source-native claim text extracted."
    lines = ["#### ABC Schema Mapping", "", f"- core meaning: {core}"]
    for category in ("psychology", "body/health", "social/relationship", "events/manifestations"):
        matches = _schema_claims(text, category)
        value = "; ".join(matches) if matches else "no explicit cue detected in this entry."
        lines.append(f"- {category}: {value}")
    lines.append("- conflicts/notes: English clauses are mapped by lexical cue only; German source wording is not rendered on this page.")
    return "\n".join(lines)


def _derived_schema_theme_line(text: str) -> str:
    parts: list[str] = []
    for category in ("psychology", "body/health", "social/relationship", "events/manifestations"):
        matches = _schema_claims(text, category)
        if matches:
            parts.append(f"{category}: {'; '.join(matches)}")
    if not parts:
        return "- Retrieval themes: no category-specific cue detected; use the source entry wording as the governing evidence."
    return f"- Retrieval themes: {'; '.join(parts)}."


def _query_anchor_line(
    factor: str | None = None,
    axis: AxisBlock | None = None,
    entry: ActivationEntry | None = None,
) -> str:
    if axis is not None and entry is not None:
        identity = normalize_activation(axis.factor_a, axis.factor_b, entry.activated_by)
        triad = " ".join(identity.triad_set) if identity.has_distinct_triad else "repeated-pair identity"
        return (
            f"- Query anchors: formula `{identity.display}`; axis `{identity.axis.display}`; "
            f"activator `{identity.activated_by}`; orientation-specific activation; triad hub `{triad}`."
        )
    if axis is not None:
        identity = normalize_axis(axis.factor_a, axis.factor_b)
        return (
            f"- Query anchors: axis `{identity.display}`; factors `{identity.factors[0]}`, `{identity.factors[1]}`; "
            "unordered midpoint pair; use linked activations for third-factor specification."
        )
    if factor is None:
        raise ValueError("query anchor line requires a factor, axis, or activation entry")
    identity = normalize_factor(factor)
    return (
        f"- Query anchors: factor `{identity.display}`; source `Udo Rudolph`; "
        "use as factor keyword field, not as a merged formula."
    )


def _sibling_orientation_line(axis: AxisBlock, entry: ActivationEntry) -> str:
    identity = normalize_activation(axis.factor_a, axis.factor_b, entry.activated_by)
    if not identity.has_distinct_triad:
        return "- Sibling orientations: repeated-pair activation; no distinct three-factor sibling pages exist."
    siblings = [
        normalize_activation(a, b, c).display
        for a, b, c in (
            (identity.axis.factors[0], identity.activated_by, identity.axis.factors[1]),
            (identity.axis.factors[1], identity.activated_by, identity.axis.factors[0]),
        )
    ]
    return (
        f"- Sibling orientations: compare `{siblings[0]}` and `{siblings[1]}` as separate pages "
        "for the same triad; these are lookup neighbors, not merged meanings."
    )


def _as_sentence(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""
    return cleaned if cleaned.endswith((".", "!", "?")) else f"{cleaned}."


def _keyword_preview(text: str, limit: int = 12) -> str:
    claims = _split_claims(text)
    if not claims:
        return text.strip()
    preview = claims[:limit]
    suffix = "" if len(claims) <= limit else ", and related keywords"
    return ", ".join(preview) + suffix


OCR_DERIVED_CLAIM_MARKERS = (
    "translation qa",
    "cached wording",
    "ec court",
    "court of first instance",
    "free movement",
    "community law",
    "treaty",
    "president in office",
    "ladies and gentlemen",
    "cern",
    "cefi",
    "gefi",
    "gcf",
    "geft",
    "fius",
    "mcmn",
    "refons",
    "influence13",
    "influence3",
    "inyoung",
    "dcr",
    "dcs",
    "dcn",
    "jugcnd",
    "dcnkcn",
    "handlungcn",
    "offcnt",
    "oncnt",
    "otknt",
    "mfcnt",
    "korpcr",
    "karpcr",
    "pcrs",
    "rncin",
    "meincs",
    "gemeinsame",
    "gcmeinschaf",
    "gemiits",
    "geflihl",
    "gefl",
    "menschcn",
    "personliche",
    "andercr",
    "cincr",
    "mctaph",
    "fcingef",
)


def _claim_has_ocr_artifacts(claim: str) -> bool:
    folded = claim.casefold()
    if any(marker in folded for marker in OCR_DERIVED_CLAIM_MARKERS):
        return True
    if re.search(r"[~<>\\]|[A-Za-z]\.[A-Za-z]|[A-Za-z][0-9]", claim):
        return True
    if re.search(r"\b[A-Za-z]{1,2}\.-\b", claim):
        return True
    return False


def _has_runaway_repetition(text: str) -> bool:
    words = [word.casefold() for word in re.findall(r"[A-Za-z']{3,}", text)]
    if len(words) < 6:
        return False
    run_word = ""
    run_length = 0
    counts: dict[str, int] = defaultdict(int)
    for word in words:
        counts[word] += 1
        if word == run_word:
            run_length += 1
        else:
            run_word = word
            run_length = 1
        if run_length >= 4:
            return True
    most_common = max(counts.values(), default=0)
    return most_common >= 12 and most_common / len(words) >= 0.35


def _usable_delineation_claims(
    source_text: str,
    translated_text: str,
    limit: int = 8,
) -> list[str]:
    translated_claims: list[str] = []
    if not _translation_preview_is_suspicious(translated_text):
        translated_claims = _usable_claims_from_text(translated_text, limit)
        if translated_claims:
            return translated_claims
    return _usable_claims_from_text(
        _clean_english_translation(_normalize_translation_source_text(source_text)),
        limit,
    )


def _usable_claims_from_text(text: str, limit: int) -> list[str]:
    claims: list[str] = []
    seen: set[str] = set()
    for raw_claim in _split_claims(text):
        claim = _clean_english_translation(raw_claim).strip(" .;:")
        if not claim or _translation_preview_is_suspicious(claim) or _claim_has_ocr_artifacts(claim):
            continue
        folded = claim.casefold()
        if folded in seen:
            continue
        claims.append(claim)
        seen.add(folded)
        if len(claims) == limit:
            break
    return claims


def _claim_series(claims: list[str]) -> str:
    if not claims:
        return ""
    if len(claims) == 1:
        return claims[0]
    if len(claims) == 2:
        return f"{claims[0]} and {claims[1]}"
    return f"{', '.join(claims[:-1])}, and {claims[-1]}"


def _delineation_text(
    source_text: str,
    translated_text: str,
    limit: int = 8,
) -> str:
    claims = _usable_delineation_claims(source_text, translated_text, limit=limit)
    return _claim_series(claims)


def _delineation_theme_line(source_text: str, translated_text: str) -> str:
    claims = _usable_delineation_claims(source_text, translated_text, limit=12)
    if not claims:
        return "- Retrieval themes: translation QA pending; no stable English clauses are available for derived use yet."
    return _derived_schema_theme_line(", ".join(claims))


def _merge_derived_synthesis(existing: str, rudolph_synthesis: str) -> str:
    cleaned = re.sub(
        rf"(?:\n{{0,2}}){re.escape(UDO_DERIVED_HEADING)}\n.*?(?=\n### |\Z)",
        "",
        existing.strip(),
        flags=re.S,
    ).strip()
    rudolph_block = f"{UDO_DERIVED_HEADING}\n\n{rudolph_synthesis.strip()}"
    return f"{cleaned}\n\n{rudolph_block}" if cleaned else rudolph_block


def _source_subsection_body(block: str, heading: str) -> str:
    marker = f"#### {heading}\n"
    if marker not in block:
        return ""
    section = block.split(marker, 1)[1]
    return re.split(r"\n#### |\n### |\n## ", section, maxsplit=1)[0].strip()


def _udo_abc_entry_preview(body: str) -> str:
    for block in _source_entry_blocks(body):
        if _canonical_source_title(_entry_title(block)) != SOURCE_TITLE:
            continue
        text = _source_subsection_body(block, "ABC Entry")
        if text:
            claims = _usable_delineation_claims(text, re.sub(r"\s+", " ", text), limit=4)
            return _as_sentence(_claim_series(claims)) if claims else TRANSLATION_QA_ENTRY_TEXT
    return ""


SUSPICIOUS_TRANSLATION_PREVIEW_MARKERS = (
    "ec court",
    "court of first instance",
    "free movement of persons",
    "research programme",
    "economic statistics",
    "commission's proposal",
    "member states",
    "translation flagged for qa",
    "cached wording is not rendered",
    "unbekannt",
    "sensibilitat",
    "sensibi",
    "fius",
    "fiuss",
    "flill",
    "kifrper",
    "corpedic",
    "gestaltloses",
    "verneinigung",
    "ladies and gentlemen",
    "president in office",
    "mcmn",
    "\\vesen",
    "manjiche",
    "geft",
    "gemut",
    "yolk",
    "kc)",
    "korpcr",
    "corpcr",
    "krcislau",
    "j\\",
    "refons",
    "influence13",
    "influence3",
    "inyoung",
)


def _translation_preview_is_suspicious(text: str) -> bool:
    folded = text.casefold()
    return _has_runaway_repetition(text) or any(marker in folded for marker in SUSPICIOUS_TRANSLATION_PREVIEW_MARKERS)


TRANSLATION_QA_ENTRY_TEXT = (
    "English-only translation flagged for QA; cached wording is not rendered until reviewed."
)


def _source_entry_text(source_text: str, text: str) -> str:
    claims = _usable_delineation_claims(source_text, text, limit=12)
    if not claims:
        return TRANSLATION_QA_ENTRY_TEXT
    return _claim_series(claims)


def _translation_qa_section(source_text: str, text: str) -> str:
    if _usable_delineation_claims(source_text, text, limit=1):
        return ""
    return "\n\n".join(
        [
            "#### Translation QA",
            (
                "- cached English translation is flagged for QA; no German original is rendered on this page, "
                "and this entry should not be used as synthesis evidence until reviewed."
            ),
        ]
    )


def _format_schema_mapping_for_source(source_text: str, text: str) -> str:
    claims = _usable_delineation_claims(source_text, text, limit=12)
    if claims:
        return _format_schema_mapping(", ".join(claims))
    return "\n".join(
        [
            "#### ABC Schema Mapping",
            "",
            "- core meaning: translation QA pending; cached English text is not treated as schema evidence until reviewed.",
            "- psychology: translation QA pending.",
            "- body/health: translation QA pending.",
            "- social/relationship: translation QA pending.",
            "- events/manifestations: translation QA pending.",
            "- conflicts/notes: English-only QA placeholder is rendered because the cached translation matched artifact patterns; German source wording is not rendered on this page.",
        ]
    )


def _translation_qa_retrieval_line() -> str:
    return "- Retrieval themes: translation QA pending; cached English text is not treated as retrieval evidence until reviewed."


def _triad_derived_synthesis(triad_factors: tuple[str, str, str], activation_dir: Path) -> str:
    identity = normalize_triad(triad_factors)
    lines = [
        "### Udo Rudolph Orientation Map",
        "",
        (
            f"- Triad role: `{identity.display}` is a structural lookup hub; keep sibling formula meanings "
            "on their orientation-specific activation pages."
        ),
    ]
    for orientation in identity.orientations:
        activation_path = activation_dir / f"{_activation_identity_from_display(orientation).slug}.md"
        if not activation_path.exists():
            lines.append(f"- Orientation `{orientation}`: activation page not available.")
            continue
        preview = _udo_abc_entry_preview(load_page(activation_path).body)
        if preview and _translation_preview_is_suspicious(preview):
            lines.append(f"- Orientation `{orientation}`: ABC entry present; cached English preview is flagged for translation QA.")
        elif preview:
            lines.append(f"- Orientation `{orientation}`: {preview}")
        else:
            lines.append(
                f"- Orientation `{orientation}`: no Udo Rudolph ABC entry is currently available on the activation page."
            )
    lines.append(
        f"- Query anchors: triad hub `{identity.display}`; source `Udo Rudolph`; "
        "compare sibling activation pages without merging their meanings."
    )
    return "\n".join(lines)


def _derived_factor_synthesis(
    block: FactorBlock,
    translation_lookup: Mapping[str, str] | None,
    activation_count: int,
) -> str:
    text = _translate_text(block.text, translation_lookup)
    delineation = _delineation_text(block.text, text, limit=10)
    if not delineation:
        return "\n".join(
            [
                (
                    f"- Rudolph deepening: `{block.factor}` English-only keyword field is flagged for "
                    "Translation QA; do not use the cached wording as derived doctrine until reviewed."
                ),
                _query_anchor_line(factor=block.factor),
                _translation_qa_retrieval_line(),
                (
                    f"- Formula use: Rudolph contributes {activation_count} orientation-specific activation pages for "
                    f"`{block.factor}`; keep those activation pages orientation-specific while this keyword field is reviewed."
                ),
            ]
        )
    return "\n".join(
        [
            f"- Rudolph delineation: `{block.factor}` carries {delineation}.",
            _delineation_theme_line(block.text, text),
            (
                f"- Formula use: Rudolph contributes {activation_count} orientation-specific activation pages for "
                f"`{block.factor}`; read the factor through the active axis and third factor instead of using the factor page as a merged formula."
            ),
        ]
    )


def _factor_context_phrase(
    factor: str,
    factor_lookup: Mapping[str, FactorBlock] | None,
    translation_lookup: Mapping[str, str] | None,
) -> str | None:
    if not factor_lookup:
        return None
    block = factor_lookup.get(factor)
    if block is None:
        return None
    text = _translate_text(block.text, translation_lookup)
    if _translation_preview_is_suspicious(text):
        return f"{factor} contributes an English-only keyword field flagged for translation QA"
    return f"{factor} contributes {_keyword_preview(text, limit=8)}"


def _derived_axis_synthesis(
    block: AxisBlock,
    factor_lookup: Mapping[str, FactorBlock] | None,
    translation_lookup: Mapping[str, str] | None,
) -> str:
    axis = normalize_axis(block.factor_a, block.factor_b)
    summary_text = _translate_text(block.summary, translation_lookup)
    delineation = _delineation_text(block.summary, summary_text, limit=8)
    if not delineation:
        return "\n".join(
            [
                (
                    f"- Rudolph deepening: `{axis.display}` ABC pair summary is flagged for Translation QA; "
                    "do not use the cached wording as derived doctrine until reviewed."
                ),
                _query_anchor_line(axis=block),
                _translation_qa_retrieval_line(),
                "- Activation use: read the related activation pages as third-factor specifications of this unordered axis; do not collapse those oriented statements back into the pair.",
            ]
        )
    return "\n".join(
        [
            f"- Rudolph delineation: `{axis.display}` centers on {delineation}.",
            _delineation_theme_line(block.summary, summary_text),
            "- Activation use: read the related activation pages as third-factor specifications of this unordered axis; do not collapse those oriented statements back into the pair.",
        ]
    )


def _derived_activation_synthesis(
    block: AxisBlock,
    entry: ActivationEntry,
    factor_lookup: Mapping[str, FactorBlock] | None,
    translation_lookup: Mapping[str, str] | None,
) -> str:
    identity = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
    raw_entry_text = _translate_text(entry.text, translation_lookup)
    raw_axis_text = _translate_text(block.summary, translation_lookup)
    entry_delineation = _delineation_text(entry.text, raw_entry_text, limit=8)
    axis_delineation = _delineation_text(block.summary, raw_axis_text, limit=4)
    entry_flagged = not entry_delineation
    axis_flagged = _translation_preview_is_suspicious(raw_axis_text)
    if entry_flagged:
        first_line = (
            f"- Rudolph deepening: `{identity.display}` ABC entry is flagged for Translation QA; this page keeps "
            "the orientation-specific source reference but does not use the cached wording as derived doctrine until reviewed."
        )
    else:
        axis_clause = (
            " The underlying axis summary is flagged for Translation QA."
            if axis_flagged and not axis_delineation
            else f" The underlying `{identity.axis.display}` axis contributes {axis_delineation}."
        )
        first_line = f"- Rudolph delineation: `{identity.display}` indicates {entry_delineation}.{axis_clause}"
    return "\n".join(
        [
            first_line,
            _sibling_orientation_line(block, entry),
            (
                _translation_qa_retrieval_line()
                if entry_flagged
                else _delineation_theme_line(entry.text, raw_entry_text)
            ),
            f"- Orientation note: {entry.activated_by} specifies the axis as the third factor; do not merge it with sibling orientations of the same triad.",
        ]
    )


def _axis_formula_display(block: AxisBlock) -> str:
    return normalize_axis(block.factor_a, block.factor_b).display


def _activation_formula_display(block: AxisBlock, activated_by: str) -> str:
    return normalize_activation(block.factor_a, block.factor_b, activated_by).display


def _factor_context_line(
    role: str,
    factor: str,
    factor_lookup: Mapping[str, FactorBlock],
    translation_lookup: Mapping[str, str] | None,
) -> str | None:
    block = factor_lookup.get(factor)
    if block is None:
        return None
    text = _translate_text(block.text, translation_lookup)
    if _translation_preview_is_suspicious(text):
        text = "English-only keyword field flagged for translation QA; review before using as synthesis evidence."
    return f"- {role} `{factor}` (source keyword page `{block.page}`): {text}"


def _format_factor_context(
    axis_factors: tuple[str, str],
    factor_lookup: Mapping[str, FactorBlock] | None,
    translation_lookup: Mapping[str, str] | None,
    activated_by: str | None = None,
) -> str:
    if not factor_lookup:
        return ""
    lines = [
        line
        for line in (
            _factor_context_line("Axis factor", axis_factors[0], factor_lookup, translation_lookup),
            _factor_context_line("Axis factor", axis_factors[1], factor_lookup, translation_lookup),
            _factor_context_line("Activator", activated_by, factor_lookup, translation_lookup) if activated_by else None,
        )
        if line is not None
    ]
    if not lines:
        return ""
    return "\n".join(["#### ABC Factor Context", "", *lines])


def _factor_source_entry(block: FactorBlock, translation_lookup: Mapping[str, str] | None = None) -> str:
    text = _translate_text(block.text, translation_lookup)
    qa_section = _translation_qa_section(block.text, text)
    qa_section = f"\n\n{qa_section}" if qa_section else ""
    return f"""### {SOURCE_TITLE}

- Source factor: `{block.factor}`
- Source page: `{block.page}`

#### ABC Keyword Entry

{_source_entry_text(block.text, text)}
{qa_section}

{_format_schema_mapping_for_source(block.text, text)}""".strip()


def _axis_source_entry(
    block: AxisBlock,
    factor_lookup: Mapping[str, FactorBlock] | None = None,
    translation_lookup: Mapping[str, str] | None = None,
) -> str:
    text = _translate_text(block.summary, translation_lookup)
    factor_context = _format_factor_context((block.factor_a, block.factor_b), factor_lookup, translation_lookup)
    factor_context_section = f"\n\n{factor_context}" if factor_context else ""
    qa_section = _translation_qa_section(block.summary, text)
    qa_section = f"\n\n{qa_section}" if qa_section else ""
    return f"""### {SOURCE_TITLE}

- Source axis: `{_axis_formula_display(block)}`
- Source pages: `{block.page_range}`
- PDF page: `{block.pdf_page}`

#### ABC Pair Summary

{_source_entry_text(block.summary, text)}
{qa_section}
{factor_context_section}

{_format_schema_mapping_for_source(block.summary, text)}""".strip()


def _activation_source_entry(
    block: AxisBlock,
    entry: ActivationEntry,
    factor_lookup: Mapping[str, FactorBlock] | None = None,
    translation_lookup: Mapping[str, str] | None = None,
) -> str:
    text = _translate_text(entry.text, translation_lookup)
    factor_context = _format_factor_context((block.factor_a, block.factor_b), factor_lookup, translation_lookup, entry.activated_by)
    factor_context_section = f"\n\n{factor_context}" if factor_context else ""
    qa_section = _translation_qa_section(entry.text, text)
    qa_section = f"\n\n{qa_section}" if qa_section else ""
    return f"""### {SOURCE_TITLE}

- Source formula: `{_activation_formula_display(block, entry.activated_by)}`
- Source page: `{entry.page}`
- PDF page: `{block.pdf_page}`
- Source marker: `{entry.token}`

#### ABC Entry

{_source_entry_text(entry.text, text)}
{qa_section}
{factor_context_section}

{_format_schema_mapping_for_source(entry.text, text)}""".strip()


def _render_factor_page(
    path: Path,
    block: FactorBlock,
    activation_count: int,
    translation_lookup: Mapping[str, str] | None = None,
) -> str:
    if path.exists():
        page = load_page(path)
        aliases = list(page.meta.get("aliases", []) or [])
        source_pages = _ordered_source_pages(list(page.meta.get("source_pages", []) or []) + [SOURCE_SLUG])
        source_entries = _merge_source_entries(page.body, _factor_source_entry(block, translation_lookup), SOURCE_TITLE)
        contradictions = _section_body(page.body, "Contradictions and Framework Notes") or DEFAULT_FACTOR_CONTRADICTIONS
        derived = _merge_derived_synthesis(
            _section_body(page.body, "Derived Synthesis") or DEFAULT_DERIVED_TEXT,
            _derived_factor_synthesis(block, translation_lookup, activation_count),
        )
        related_axes = _section_body(page.body, "Related Axes") or "- None generated."
        related_activations = _section_body(page.body, "Related Activations") or "- None."
        open_questions = _section_body(page.body, "Open Questions") or "- None recorded yet."
    else:
        aliases = []
        source_pages = [SOURCE_SLUG]
        source_entries = _factor_source_entry(block, translation_lookup)
        contradictions = DEFAULT_FACTOR_CONTRADICTIONS
        derived = _merge_derived_synthesis(
            DEFAULT_DERIVED_TEXT,
            _derived_factor_synthesis(block, translation_lookup, activation_count),
        )
        related_axes = "- None generated."
        related_activations = f"- Generated activation pages involving `{block.factor}`: `{activation_count}`."
        open_questions = "- None recorded yet."

    factor = normalize_factor(block.factor)
    framework_scope = _framework_scope_for_sources(source_pages)
    astronomicon = astronomicon_token(factor.display)
    astronomicon_line = (
        f"- Astronomicon token: `{astronomicon}`\n"
        if astronomicon != factor.display
        else ""
    )

    return f"""---
title: {factor.display}
page_type: factor
slug: {factor.slug}
status: source_ingested
framework_scope: {framework_scope}
factors:
{_yaml_list([factor.display], indent=2)}
aliases:
{_yaml_list(aliases, indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Factor: {factor.display}
{astronomicon_line}- Canonical page type: comparative factor page grounded in standalone source entries.

## Source Entries

{source_entries}

## Comparative Schema

- core meaning: source-native factor entries are preserved side by side above.
- psychology: source-specific psychological and doctrinal emphases remain attached to their own source blocks instead of being flattened.
- body/health: bodily wording remains inside each contributing source block when present.
- social/relationship: interpersonal implications remain attached to each source's own phrasing.
- events/manifestations: source-specific extensions remain attached to the source entry that states them.
- conflicts/notes: this page preserves distinct source voices and frameworks side by side instead of collapsing them into one wording.

## Contradictions and Framework Notes

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived}

## Related Axes

{related_axes}

## Related Activations

{related_activations}

## Related Sources

{_source_links(source_pages)}

## Open Questions

{open_questions}
"""


def _render_axis_page(
    path: Path,
    block: AxisBlock,
    factor_lookup: Mapping[str, FactorBlock] | None = None,
    translation_lookup: Mapping[str, str] | None = None,
) -> str:
    axis = normalize_axis(block.factor_a, block.factor_b)
    new_activations = [
        normalize_activation(block.factor_a, block.factor_b, entry.activated_by).display
        for entry in block.activation_entries
    ]
    default_aliases = [f"{axis.factors[1]}/{axis.factors[0]}"]

    if path.exists():
        page = load_page(path)
        aliases = list(page.meta.get("aliases", []) or default_aliases)
        source_pages = _ordered_source_pages(list(page.meta.get("source_pages", []) or []) + [SOURCE_SLUG])
        source_entries = _merge_source_entries(page.body, _axis_source_entry(block, factor_lookup, translation_lookup), SOURCE_TITLE)
        existing_related = list(page.meta.get("related_activations", []) or [])
        contradictions = _section_body(page.body, "Contradictions") or DEFAULT_AXIS_CONTRADICTIONS
        derived = _merge_derived_synthesis(
            _section_body(page.body, "Derived Synthesis") or DEFAULT_DERIVED_TEXT,
            _derived_axis_synthesis(block, factor_lookup, translation_lookup),
        )
    else:
        aliases = default_aliases
        source_pages = [SOURCE_SLUG]
        source_entries = _axis_source_entry(block, factor_lookup, translation_lookup)
        existing_related = []
        contradictions = DEFAULT_AXIS_CONTRADICTIONS
        derived = _merge_derived_synthesis(
            DEFAULT_DERIVED_TEXT,
            _derived_axis_synthesis(block, factor_lookup, translation_lookup),
        )

    related_activations = sorted(set(existing_related) | set(new_activations), key=str.casefold)
    related_triad_hubs = _triad_names_from_activations(related_activations)
    related_links = "\n".join(_activation_link(item) for item in related_activations)
    framework_scope = _framework_scope_for_sources(source_pages)
    astronomicon_axis = _astronomicon_axis(axis.factors[0], axis.factors[1])
    astronomicon_line = (
        f"- Astronomicon axis: `{astronomicon_axis}`\n"
        if astronomicon_axis != axis.display
        else ""
    )

    return f"""---
title: {axis.display}
page_type: axis
slug: {axis.slug}
status: source_ingested
framework_scope: {framework_scope}
factors:
{_yaml_list(list(axis.factors), indent=2)}
normalized_axis: {axis.display}
factor_a: {axis.factors[0]}
factor_b: {axis.factors[1]}
related_activations:
{_yaml_list(related_activations, indent=2)}
related_triad_hubs:
{_yaml_list(related_triad_hubs, indent=2)}
aliases:
{_yaml_list(aliases, indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Axis: `{axis.display}`
{astronomicon_line}- Canonical page type: comparative axis page grounded in source-native pair entries.

## Source Entries

{source_entries}

## Comparative Schema

- core meaning: source-native pair entries are preserved side by side above.
- psychology: source-specific psychological and doctrinal emphases remain attached to their own source blocks instead of being flattened together.
- body/health: bodily wording remains inside each contributing source block when present.
- social/relationship: interpersonal implications remain attached to each source's own phrasing.
- events/manifestations: see the source entries above and the orientation-specific activation pages linked below.
- conflicts/notes: source `+` headings are normalized as midpoint-axis identities, and orientation-specific activation pages stay separate.

## Related Activations

{related_links}

## Contradictions

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived}

## Links

{_factor_link(axis.factors[0])}
{_factor_link(axis.factors[1])}
{_source_links(source_pages)}
"""


def _render_activation_page(
    path: Path,
    block: AxisBlock,
    entry: ActivationEntry,
    factor_lookup: Mapping[str, FactorBlock] | None = None,
    translation_lookup: Mapping[str, str] | None = None,
) -> str:
    identity = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)

    if path.exists():
        page = load_page(path)
        aliases = list(page.meta.get("aliases", []) or [])
        source_pages = _ordered_source_pages(list(page.meta.get("source_pages", []) or []) + [SOURCE_SLUG])
        source_entries = _merge_source_entries(
            page.body,
            _activation_source_entry(block, entry, factor_lookup, translation_lookup),
            SOURCE_TITLE,
        )
        contradictions = _section_body(page.body, "Contradictions") or DEFAULT_ACTIVATION_CONTRADICTIONS
        derived = _merge_derived_synthesis(
            _section_body(page.body, "Derived Synthesis") or DEFAULT_DERIVED_TEXT,
            _derived_activation_synthesis(block, entry, factor_lookup, translation_lookup),
        )
    else:
        aliases = []
        source_pages = [SOURCE_SLUG]
        source_entries = _activation_source_entry(block, entry, factor_lookup, translation_lookup)
        contradictions = DEFAULT_ACTIVATION_CONTRADICTIONS
        derived = _merge_derived_synthesis(
            DEFAULT_DERIVED_TEXT,
            _derived_activation_synthesis(block, entry, factor_lookup, translation_lookup),
        )

    framework_scope = _framework_scope_for_sources(source_pages)
    astronomicon_formula = (
        f"{_astronomicon_axis(identity.axis.factors[0], identity.axis.factors[1])} = "
        f"{astronomicon_token(identity.activated_by)}"
    )
    astronomicon_line = (
        f"- Astronomicon formula: `{astronomicon_formula}`\n"
        if astronomicon_formula != identity.display
        else ""
    )
    triad_line = (
        f"- Triad hub: [{' '.join(identity.triad_set)}](../triads/{normalize_triad(identity.triad_set).slug}.md)\n"
        if identity.has_distinct_triad
        else "- Repeated-pair identity: no distinct triad hub exists for this activation.\n"
    )

    return f"""---
title: {identity.display}
page_type: activation
slug: {identity.slug}
status: source_ingested
framework_scope: {framework_scope}
factors:
{_yaml_list([identity.axis.factors[0], identity.axis.factors[1], identity.activated_by], indent=2)}
normalized_formula: {identity.display}
axis: {identity.axis.display}
activated_by: {identity.activated_by}
triad_set:
{_yaml_list(list(identity.triad_set), indent=2)}
aliases:
{_yaml_list(aliases, indent=2)}
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Formula: `{identity.display}`
{astronomicon_line}- Axis page: [{identity.axis.display}](../axes/{identity.axis.slug}.md)
{triad_line}
## Source Entries

{source_entries}

## Comparative Schema

- core meaning: source-native activation entries are preserved side by side above.
- psychology: each source keeps its own phrasing and emphasis for the same orientation-specific formula.
- body/health: bodily implications remain embedded inside the source-native entry when present.
- social/relationship: interpersonal implications remain attached to each source entry instead of being collapsed.
- events/manifestations: this page preserves the activation as an orientation-specific formula with source-backed statements only.
- conflicts/notes: orientation-specific meaning is preserved on its own page and not merged into the triad hub.

## Contradictions

{contradictions}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived}

## Links

{_factor_link(identity.axis.factors[0])}
{_factor_link(identity.axis.factors[1])}
{_factor_link(identity.activated_by)}
- [{identity.axis.display}](../axes/{identity.axis.slug}.md)
{_source_links(source_pages)}
"""


def _render_triad_page(triad_factors: tuple[str, str, str], activation_dir: Path) -> str:
    identity = normalize_triad(triad_factors)
    activation_pages = []
    orientation_lines: list[str] = []
    for orientation in identity.orientations:
        activation_path = activation_dir / f"{_activation_identity_from_display(orientation).slug}.md"
        if activation_path.exists():
            activation_pages.append(load_page(activation_path))
            orientation_lines.append(_activation_link(orientation))
        else:
            orientation_lines.append(f"- `{orientation}` (activation page not available)")

    source_pages = _ordered_source_pages(
        [source for page in activation_pages for source in list(page.meta.get("source_pages", []) or [])]
    )
    framework_scope = _framework_scope_for_sources(source_pages)
    coverage_lines: list[str] = []
    for orientation in identity.orientations:
        activation_path = activation_dir / f"{_activation_identity_from_display(orientation).slug}.md"
        if not activation_path.exists():
            coverage_lines.append(f"- `{orientation}`: no activation page is currently available.")
            continue
        page = load_page(activation_path)
        for title, source_page in _source_page_refs(page.body):
            coverage_lines.append(f"- `{orientation}`: {title}, page `{source_page}`")

    astronomicon_triad = " ".join(astronomicon_token(factor) for factor in identity.factors)
    astronomicon_line = (
        f"- Astronomicon triad-set: `{astronomicon_triad}`\n"
        if astronomicon_triad != identity.display
        else ""
    )
    derived = _triad_derived_synthesis(triad_factors, activation_dir)

    return f"""---
title: {identity.display}
page_type: triad_hub
slug: {identity.slug}
status: source_ingested
framework_scope: {framework_scope}
factors:
{_yaml_list(list(identity.factors), indent=2)}
triad_set:
{_yaml_list(list(identity.factors), indent=2)}
orientations:
{_yaml_list(list(identity.orientations), indent=2)}
aliases: []
source_pages:
{_yaml_list(source_pages, indent=2)}
updated_at: {UPDATED_AT}
---

## Identity

- Triad-set: `{identity.display}`
{astronomicon_line}- This page is structural only. It does not merge the meanings of its orientations.

## Orientation Map

{chr(10).join(orientation_lines)}

## Source Coverage

{chr(10).join(coverage_lines)}

<a id="derived-synthesis"></a>

## Derived Synthesis

{derived}

## Contradictions Across Orientations

- None recorded yet.
- Distinct meanings across orientations are preserved as orientation differences, not collapsed into one interpretation.

## Links

{chr(10).join(_factor_link(factor) for factor in identity.factors)}
{_source_links(source_pages)}
"""


def _translation_qa_counts(
    factor_blocks: tuple[FactorBlock, ...],
    axis_blocks: tuple[AxisBlock, ...],
    translation_lookup: Mapping[str, str],
) -> dict[str, int]:
    factor_count = sum(
        1
        for block in factor_blocks
        if _translation_preview_is_suspicious(_translate_text(block.text, translation_lookup))
    )
    axis_count = sum(
        1
        for block in axis_blocks
        if _translation_preview_is_suspicious(_translate_text(block.summary, translation_lookup))
    )
    activation_count = sum(
        1
        for block in axis_blocks
        for entry in block.activation_entries
        if _translation_preview_is_suspicious(_translate_text(entry.text, translation_lookup))
    )
    return {
        "factor": factor_count,
        "axis": axis_count,
        "activation": activation_count,
        "total": factor_count + axis_count + activation_count,
    }


def _translation_qa_factor_lines(
    factor_blocks: tuple[FactorBlock, ...],
    translation_lookup: Mapping[str, str],
) -> list[str]:
    lines: list[str] = []
    for block in factor_blocks:
        if not _translation_preview_is_suspicious(_translate_text(block.text, translation_lookup)):
            continue
        factor = normalize_factor(block.factor)
        lines.append(f"- [{factor.display}](../factors/{factor.slug}.md): factor keyword page `{block.page}`.")
    return lines


def _translation_qa_axis_lines(
    axis_blocks: tuple[AxisBlock, ...],
    translation_lookup: Mapping[str, str],
) -> list[str]:
    lines: list[str] = []
    for block in axis_blocks:
        if not _translation_preview_is_suspicious(_translate_text(block.summary, translation_lookup)):
            continue
        axis = normalize_axis(block.factor_a, block.factor_b)
        lines.append(
            f"- [{axis.display}](../axes/{axis.slug}.md): ABC pair summary pages `{block.page_range}`; PDF page `{block.pdf_page}`."
        )
    return lines


def _translation_qa_activation_lines(
    axis_blocks: tuple[AxisBlock, ...],
    translation_lookup: Mapping[str, str],
) -> list[str]:
    lines: list[str] = []
    for block in axis_blocks:
        for entry in block.activation_entries:
            if not _translation_preview_is_suspicious(_translate_text(entry.text, translation_lookup)):
                continue
            activation = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
            lines.append(
                f"- [{activation.display}](../activations/{activation.slug}.md): source page `{entry.page}`; PDF page `{block.pdf_page}`."
            )
    return lines


def _review_lines_or_none(lines: list[str]) -> str:
    return "\n".join(lines) if lines else "- None."


def _render_translation_qa_page(
    factor_blocks: tuple[FactorBlock, ...],
    axis_blocks: tuple[AxisBlock, ...],
    translation_lookup: Mapping[str, str],
) -> str:
    counts = _translation_qa_counts(factor_blocks, axis_blocks, translation_lookup)
    factor_lines = _translation_qa_factor_lines(factor_blocks, translation_lookup)
    axis_lines = _translation_qa_axis_lines(axis_blocks, translation_lookup)
    activation_lines = _translation_qa_activation_lines(axis_blocks, translation_lookup)
    return f"""---
title: Udo Rudolph ABC Translation QA
page_type: derived
slug: udo-rudolph-abc-translation-qa
status: source_ingested
framework_scope: {SOURCE_FRAMEWORK_SCOPE}
factors:
{_yaml_list(list(FACTOR_SEQUENCE), indent=2)}
aliases: []
source_pages:
  - {SOURCE_SLUG}
updated_at: {UPDATED_AT}
---

## Purpose

- This page lists Udo Rudolph ABC entries whose cached English translation was withheld from source, schema, retrieval, and derived synthesis because it matched translation-artifact patterns.
- No German original or suspect cached English wording is rendered here; use the source page references and linked canonical pages for review.
- The review list is a QA surface only, not a doctrine page and not a merged interpretation layer.

## Status

- Flagged factor keyword entries: `{counts["factor"]}`.
- Flagged axis pair summaries: `{counts["axis"]}`.
- Flagged activation entries: `{counts["activation"]}`.
- Total flagged source entries: `{counts["total"]}`.

## Factor Keyword Entries

{_review_lines_or_none(factor_lines)}

## Axis Pair Summaries

{_review_lines_or_none(axis_lines)}

## Activation Entries

{_review_lines_or_none(activation_lines)}

## Links

- [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)
"""


def _coverage_factor_lines(
    factor_blocks: tuple[FactorBlock, ...],
    axis_blocks: tuple[AxisBlock, ...],
) -> list[str]:
    factor_names = [block.factor for block in factor_blocks]
    axis_counts = {factor: 0 for factor in factor_names}
    activator_counts = {factor: 0 for factor in factor_names}
    activation_involving_counts = {factor: 0 for factor in factor_names}
    triads_by_factor = {factor: set() for factor in factor_names}

    for block in axis_blocks:
        axis = normalize_axis(block.factor_a, block.factor_b)
        for factor in axis.factors:
            if factor in axis_counts:
                axis_counts[factor] += 1
        for entry in block.activation_entries:
            activation = normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
            if entry.activated_by in activator_counts:
                activator_counts[entry.activated_by] += 1
            for factor in activation.triad_set:
                if factor in activation_involving_counts:
                    activation_involving_counts[factor] += 1
                if activation.has_distinct_triad and factor in triads_by_factor:
                    triads_by_factor[factor].add(activation.triad_set)

    lines: list[str] = []
    for block in factor_blocks:
        factor = normalize_factor(block.factor)
        lines.append(
            f"- [{factor.display}](../factors/{factor.slug}.md): axes `{axis_counts[block.factor]}`; "
            f"activation pages involving factor `{activation_involving_counts[block.factor]}`; "
            f"activator entries `{activator_counts[block.factor]}`; "
            f"triad hubs involving factor `{len(triads_by_factor[block.factor])}`."
        )
    return lines


def _render_coverage_map_page(
    factor_blocks: tuple[FactorBlock, ...],
    axis_blocks: tuple[AxisBlock, ...],
) -> str:
    activation_entries = [
        normalize_activation(block.factor_a, block.factor_b, entry.activated_by)
        for block in axis_blocks
        for entry in block.activation_entries
    ]
    triads = {activation.triad_set for activation in activation_entries if activation.has_distinct_triad}
    factor_lines = _coverage_factor_lines(factor_blocks, axis_blocks)
    return f"""---
title: Udo Rudolph ABC Coverage Map
page_type: derived
slug: udo-rudolph-abc-coverage-map
status: source_ingested
framework_scope: {SOURCE_FRAMEWORK_SCOPE}
factors:
{_yaml_list([block.factor for block in factor_blocks], indent=2)}
aliases: []
source_pages:
  - {SOURCE_SLUG}
updated_at: {UPDATED_AT}
---

## Purpose

- This page summarizes the canonical coverage geometry generated from Udo Rudolph's ABC source model.
- It is a navigation and audit surface only; it does not merge sibling activation meanings into triad doctrine.
- Triad hubs are structural only, and each `A/B = C` activation remains orientation-specific.

## Coverage Summary

- Factor keyword pages: `{len(factor_blocks)}`.
- Distinct unordered axes: `{len(axis_blocks)}`.
- Orientation-specific activation entries: `{len(activation_entries)}`.
- Distinct triad hubs: `{len(triads)}`.

## Factor Coverage Index

{chr(10).join(factor_lines)}

## Links

- [{SOURCE_TITLE}](../sources/{SOURCE_SLUG}.md)
- [Udo Rudolph ABC Translation QA](udo-rudolph-abc-translation-qa.md)
"""


def _render_source_page(
    factor_blocks: tuple[FactorBlock, ...],
    axis_count: int,
    activation_count: int,
    triad_count: int,
    translation_qa_count: int = 0,
) -> str:
    factor_links = "\n".join(f"- [{factor.factor}](../factors/{factor_slug(factor.factor)}.md)" for factor in factor_blocks)
    return f"""---
title: {SOURCE_TITLE}
page_type: source
slug: {SOURCE_SLUG}
status: source_ingested
framework_scope: {SOURCE_FRAMEWORK_SCOPE}
factors:
{_yaml_list(list(FACTOR_SEQUENCE), indent=2)}
aliases: []
source_pages: []
updated_at: {UPDATED_AT}
---

## Bibliographic Metadata

- Author: Udo Rudolph
- Title: *ABC for Planetary Pictures*
- Vault file: `Stellar Influences Vault/{SOURCE_FILE}`

## Scope Notes

- This ingest contributes the source's factor keyword spread plus every explicit distinct-factor axis spread in the ABC table.
- The PDF table begins at PDF page `8`; each scanned spread is mapped to one unordered axis pair in the source's factor sequence.
- Source pair headings are normalized into unordered midpoint-axis pages `A/B`.
- Source cross-reference markers for the two axis factors are treated as pair-summary references and are not ingested as separate activation pages.
- Triad hubs remain structural pages; activation orientations are kept separate.

## ABC Schema Mapping Notes

- The deepened ingest maps source-native clauses into the shared comparative schema by conservative lexical cues.
- The mapping is added beneath each ABC keyword, pair summary, and activation entry as `ABC Schema Mapping`.
- Schema lines are retrieval aids, not rewritten doctrine; the generated wiki keeps only the English translation of each delineation.
- German OCR text is retained only in `tools/{TRANSLATION_CACHE_FILE}` as translation cache input, not on rendered wiki pages.
- Empty category matches are reported as missing cues instead of inferred meaning.

## Factors Covered

{factor_links}

## Axes Covered

- Canonical axis pages updated or created: `{axis_count}`.
- Browse [Index](../index.md) or `wiki/axes/` for the full set.

## Activations Covered

- Canonical activation pages updated or created: `{activation_count}`.
- Canonical triad hubs updated or created: `{triad_count}`.
- Browse [Index](../index.md), `wiki/activations/`, and `wiki/triads/` for the full set.

## Coverage Map

- Coverage artifact: [Udo Rudolph ABC Coverage Map](../derived/udo-rudolph-abc-coverage-map.md)
- The coverage map summarizes factor, axis, activation, and triad counts without merging orientation-specific meanings.

## Translation QA

- Flagged English-only entries withheld from synthesis: `{translation_qa_count}`.
- Review artifact: [Udo Rudolph ABC Translation QA](../derived/udo-rudolph-abc-translation-qa.md)

## Ingestion History

- {UPDATED_AT}: Ingested Udo Rudolph's ABC factor keywords, 231 distinct-factor axis spreads, and 4,620 orientation-specific activation entries into the live comparative wiki.
"""


def _append_log_entry(log_path: Path, axis_count: int, activation_count: int, triad_count: int) -> None:
    text = log_path.read_text(encoding="utf-8").replace("ABC fĂĽr Planetenbilder", "ABC for Planetary Pictures").replace("ABC für Planetenbilder", "ABC for Planetary Pictures").rstrip()
    entry = (
        f"- {UPDATED_AT}: Ingested Udo Rudolph's `ABC for Planetary Pictures`, merging {axis_count} axis spreads, "
        f"{activation_count} orientation-specific activation entries, and {triad_count} triad hubs into the live wiki."
    )
    if entry not in text:
        log_path.write_text(f"{text}\n{entry}\n", encoding="utf-8")


def main() -> None:
    root = Path.cwd()
    wiki_root = root / "wiki"
    factor_dir = wiki_root / "factors"
    axis_dir = wiki_root / "axes"
    activation_dir = wiki_root / "activations"
    triad_dir = wiki_root / "triads"
    source_dir = wiki_root / "sources"
    derived_dir = wiki_root / "derived"

    factor_blocks, axis_blocks = generate_models(root / "Stellar Influences Vault" / SOURCE_FILE)
    translation_lookup = _load_translation_cache(root)
    _assert_translation_coverage(factor_blocks, axis_blocks, translation_lookup)
    factor_lookup = {block.factor: block for block in factor_blocks}
    translation_qa_counts = _translation_qa_counts(factor_blocks, axis_blocks, translation_lookup)

    activation_index: dict[str, int] = defaultdict(int)
    triads_touched: set[tuple[str, str, str]] = set()
    activation_count = 0

    for axis in axis_blocks:
        axis_identity = normalize_axis(axis.factor_a, axis.factor_b)
        (axis_dir / f"{axis_identity.slug}.md").write_text(
            _render_axis_page(axis_dir / f"{axis_identity.slug}.md", axis, factor_lookup, translation_lookup),
            encoding="utf-8",
        )

        for entry in axis.activation_entries:
            activation_identity = normalize_activation(axis.factor_a, axis.factor_b, entry.activated_by)
            (activation_dir / f"{activation_identity.slug}.md").write_text(
                _render_activation_page(
                    activation_dir / f"{activation_identity.slug}.md",
                    axis,
                    entry,
                    factor_lookup,
                    translation_lookup,
                ),
                encoding="utf-8",
            )
            for factor in activation_identity.triad_set:
                activation_index[factor] += 1
            if activation_identity.has_distinct_triad:
                triads_touched.add(activation_identity.triad_set)
            activation_count += 1

    for factor in factor_blocks:
        factor_identity = normalize_factor(factor.factor)
        (factor_dir / f"{factor_identity.slug}.md").write_text(
            _render_factor_page(
                factor_dir / f"{factor_identity.slug}.md",
                factor,
                activation_index[factor.factor],
                translation_lookup,
            ),
            encoding="utf-8",
        )

    for triad in sorted(triads_touched, key=lambda item: tuple(name.casefold() for name in item)):
        triad_identity = normalize_triad(triad)
        (triad_dir / f"{triad_identity.slug}.md").write_text(
            _render_triad_page(triad, activation_dir),
            encoding="utf-8",
        )

    (source_dir / f"{SOURCE_SLUG}.md").write_text(
        _render_source_page(
            factor_blocks,
            axis_count=len(axis_blocks),
            activation_count=activation_count,
            triad_count=len(triads_touched),
            translation_qa_count=translation_qa_counts["total"],
        ),
        encoding="utf-8",
    )
    (derived_dir / "udo-rudolph-abc-translation-qa.md").write_text(
        _render_translation_qa_page(factor_blocks, axis_blocks, translation_lookup),
        encoding="utf-8",
    )
    (derived_dir / "udo-rudolph-abc-coverage-map.md").write_text(
        _render_coverage_map_page(factor_blocks, axis_blocks),
        encoding="utf-8",
    )

    _append_log_entry(wiki_root / "log.md", len(axis_blocks), activation_count, len(triads_touched))
    (wiki_root / "index.md").write_text(build_index(wiki_root), encoding="utf-8")
    write_query_artifacts(wiki_root)


if __name__ == "__main__":
    main()

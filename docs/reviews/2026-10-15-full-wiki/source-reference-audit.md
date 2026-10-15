# Source-reference audit, 2026-10-15

This investigation changes review artifacts only. It does not reingest sources or edit the wiki, parsers, tests, or vault. Parser output is an evidence aid: its formula labels, paragraph boundaries, and OCR are not certified by having a page number.

## Review data

- `source-evidence.jsonl`: initially 13,626 unique `(path, source_slug)` records from nine existing parsers. Each record retains `native_text`, `parser_passage`, `source_heading`, a typed `locator`, the source file, and `verified_visually: false`. Udo records also retain the matching cached English translation. Supplementary raw-page records are added separately and merged atomically.
- `source-evidence-timings.jsonl`: actual extraction times and record counts. Udo took 56.808 s; Witte 71.660 s. Ebertin 2.122 s; Sandbach 2.396 s; Falis 1.122 s; Carter 0.983 s; Hand 8.239 s; Munkasey 1.298 s; McBroom 0.214 s.
- `source-evidence-factors.jsonl`: compact factor subset. All 22 Witte factor models are present: Vernal Point through Venus on PDF 27, Mars through Pluto on PDF 28, Cupido through Poseidon on PDF 29.
- `source-evidence-known-issues.jsonl`: separate scan findings and pending source checks. The parser map remains unchanged so it can reproduce the defects.
- `source-reference-counts.json`: inventory against the protected `before/wiki` snapshot. It counts blocks with explicit third-level source headings, not unheaded Witte-only entries or structural omission sections. It distinguishes missing numeric locator bullets from absence of any provenance.

The map contains parser-normalized source text, not an independent transcription. `verified_visually: false` applies even when the parser has an exact-looking number. Consult the issue index and the owning reviewer's scan-backed ledger before applying a substantive correction.

## Reference convention and reusable APIs

Frontmatter `source_pages` contains source-catalog slugs, not page numbers. Pagination belongs inside the relevant source subentry. Existing renderers use `Source page`, `Source pages`, and `PDF page`; later source slices use `PDF page(s)`. Keep the numbering system explicit. Do not infer that two equal numeric values belong to the same edition or pagination.

| Source | Existing read-only API | Locator actually retained | Limitation |
|---|---|---|---|
| Witte | `tools/witte_source.py:933` `generate_models`; `tools/ingest_witte.py:54` `_canonical_factor_blocks`; `:87` `_coalesce_pair_blocks` | One-based PDF page on factor, pair, and activation models | `LineRecord.page` comes from PDF index + 1 (`witte_source.py:312`). Entry starts and merged continuations can be wrong. Two duplicate pair blocks are coalesced by existing ingest rules. |
| Ebertin | `tools/ebertin_source.py:955` `generate_models`; `:239` `extract_page_records`; `:273` `page_lookup` | Printed page on chapters and coded entries | `page_lookup` keeps the first occurrence of a four-digit code anywhere in the book. A code reused in earlier introductory material can supply the wrong page. Preserve the entry code and verify suspicious outliers. |
| Sandbach | `tools/sandbach_source.py:321` `generate_models` | One-based PDF chapter start | Activations have no page field (`:53`); their inherited chapter start is not an exact entry locator. Seven expected entries remain source omissions, with no invented parser passage. |
| Udo Rudolph ABC | `tools/udo_rudolph_abc_source.py:543` `generate_models` | Printed factor/activation page, printed pair range, and one-based PDF spread | Printed pages are read from footers with arithmetic fallback (`:201`). Fixed factor-order assignment can shift rows after OCR merges or drops markers. `tools/udo_rudolph_abc_translations.json` retains German OCR keys and English cache values. |
| Falis | `tools/falis_source.py:188` `generate_models`; `:43` `SECTION_START_PAGES` | One-based PDF section start | End range can be reconstructed from the next section start, but the model keeps only the start. |
| Carter | `tools/carter_source.py:301` `generate_models` | Printed chapter start when detected, otherwise one-based PDF page (`:146`) | Mixed fallback must be checked before labeling it printed. Sections/examples can extend beyond that start. |
| Hand | `tools/hand_source.py:205` `generate_models`; `:266` `generate_factor_models`; `:84` `FACTOR_SECTION_SPECS` | One-based PDF page; factor specs retain ranges | Pair model is an entry start. The shared Asc/MC factor section remains attached to both factors. |
| Munkasey | `tools/munkasey_source.py:307` `generate_models`; `:297` `generate_factor_models` | Printed factor, axis, activation, concepts, and With Itself pages | Distinct pages have separate fields. Keep source-native Thesis/Anti categories separate. Existing PDF is present in the vault even though an ignore-aware `rg --files` omitted it. |
| McBroom | `tools/mcbroom_source.py:147` `generate_models`; `:25` `SECTION_SPECS` | One-based PDF excerpt start and explicit extraction range | Four bounded excerpts only; do not expand this pilot to the rest of the methodology book. |

`tools/wiki_pages.py` supplies `load_page` and `iter_wiki_pages`. `tools/ingest_udo_rudolph_abc.py:501` supplies source-block splitting, and `:553` reads both singular and plural Source page bullets. These helpers can locate source sections without running an ingest writer. Whole-corpus YAML parsing is relatively expensive here; load the assignment's paths or use the already generated evidence subsets.

Banzhaf/Haebler, Johndro, Hall, Harding/Harvey, Ober, and Stein have no existing parser module. Their canonical subentries already retain explicit `PDF page(s)` and their source catalogs identify external reference PDFs under `W:/books references etc/!master list astro`. Supplementary evidence preserves those admitted PDF pages and the original canonical entry with `granularity: admitted_pdf_page_span`; it does not pretend that the full-page text is an exact segmented passage. Hall's admitted PDF 104–121 correspond to printed 102–119. Ober's admitted examples are PDF 126–131; Stein's admitted pages are PDF 2, 9, and 11. Harding/Harvey's 61–80 is a chapter span, not a claim-level page.

## Observed risk and verification

ABC presents two independent risks: German OCR damage and English translation damage. A third risk is assigning the correct paragraph to the wrong activator. Witte has glyph, continuation, and page-boundary risks. Ebertin additionally has footnote and code-lookup risks. Carter, Hand, Falis, and McBroom retain useful starts/ranges but do not retain claim-level locations throughout long chapters. Parserless table sources require row/column inspection: adjacent factor or aspect categories can bleed into one another.

I personally rendered and inspected Udo PDF 68, printed 138–139 (`udo-pdf-0068.png`). The Sun/Moon = Venus row clearly contains `Körper-Gefühle`, `Kunst-Zentrum des Volkes`, `Schönheit des Frauen-Körpers`, and `Liebes-Gefühle des Mannes`. The cached/rendered English expressions “body flies,” “artificial center,” “shame,” and “love flies” are therefore corrupt. The Venus glyph ownership is correct on this scan. This bounded visual check contradicts treating the old ABC QA artifact's zero flags as certification of clean translations.

I also inspected the supplied Witte PDF 309 image: Admetos/Admetos = Mars owns the continuation beginning “To throttle”; Jupiter begins “Rest. Happy in straitened circumstances.” The parser incorrectly moves the Mars continuation into Jupiter. Scan-confirmed shifts reported by the activation owners also affect Udo Moon/Neptune on PDF 93, Witte Zeus/Zeus on PDF 287–288, and Witte Moon/Vulcanus on PDF 136–137. The issue index records exact paths and verification status, including pending observations that have not yet been checked against a scan.

Existing Witte axis pagination is also contaminated on sample pages: Sun/Moon labels the Witte entry page 55, but its Witte model points to PDF 101; Asc/MC labels it page 363, but Witte points to PDF 58. Both existing values and headings match the Munkasey entries on those pages. Do not copy these pre-existing bullets forward as verified Witte references. The owner should verify the Witte page before replacing the metadata; the source text and source metadata are separate checks.

## Maintenance and tests

`tools/lint_wiki.py` checks required frontmatter, canonical identity/orientation, aliases, and presence of the synthesis anchor. It does not verify source citations, source text, paragraph boundaries, English translation quality, or anchor adjacency. `tests/tools/test_wiki_links.py:27` currently expects a blank line between the anchor and heading, whereas the current editorial standard requires immediate adjacency; this is a test/helper contract to resolve deliberately, not proof that all current pages comply.

`tests/wiki/test_source_page_coverage_claims.py` compares claimed axis/activation/triad counts with live frontmatter attribution. It checks representation, not passage fidelity. Source-specific ingest tests pin source order, native headings, scope exclusions, and historical wording: `test_carter_axis_ingest.py`, `test_hand_axis_ingest.py`, `test_mcbroom_ingest.py`, `test_munkasey_concepts_ingest.py`, `test_sandbach_ingest.py`, and `test_ebertin_full_ingest.py`. The Ebertin test explicitly preserves the existing Position in Houses and Signs material; do not remove historical source sections while improving interpretation. The many Udo repair tests pin reviewed phrases and old zero-flag QA counts. A new scan-backed repair can legitimately require updating those expectations, but a green old phrase assertion is not a new source check.

I read these contracts and the corresponding parser tests; I did not run the test suite or any generator as part of this read-only investigation. The root reviewer owns whole-corpus validation.

## Exact commands

From the repository root in Git Bash:

```bash
PYTHONDONTWRITEBYTECODE=1 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' tools/tmp_inspect_witte_pdf.py --page 309
PYTHONDONTWRITEBYTECODE=1 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' tools/tmp_inspect_witte_pdf.py --lines 309
PYTHONDONTWRITEBYTECODE=1 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' tools/tmp_inspect_witte_pdf.py --ocr-lines 309
pdftoppm -f 68 -l 68 -scale-to 2400 -png -singlefile 'Stellar Influences Vault/Udo-Rudolph_ABC-fur-Planetenbilder.pdf' 'docs/reviews/2026-10-15-full-wiki/udo-pdf-0068'
PYTHONDONTWRITEBYTECODE=1 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' -m pytest -q tests/tools/test_lint_wiki.py tests/tools/test_wiki_links.py tests/tools/test_query_manifest.py tests/wiki/test_source_page_coverage_claims.py
PYTHONDONTWRITEBYTECODE=1 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' -m pytest -q tests/tools/test_witte_source.py tests/tools/test_ebertin_source.py tests/tools/test_udo_rudolph_abc_source.py tests/tools/test_carter_source.py tests/tools/test_falis_source.py tests/tools/test_hand_source.py tests/tools/test_munkasey_source.py
```

The Witte inspection helper is source-specific; its flags are text/span/OCR inspection, not a general PNG export. `pdftoppm` is available from the bundled Poppler runtime. Generators `tools/rebuild_index.py` and `tools/query_manifest.py` write generated wiki navigation; run them only in the root integration phase. Preserve all source prose unless the actual source and oriented row have been checked.

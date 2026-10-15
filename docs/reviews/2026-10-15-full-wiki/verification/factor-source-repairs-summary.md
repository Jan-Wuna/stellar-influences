# Targeted factor source repairs

This continuation resumes specific unresolved defects in the existing factor ledgers. It does not repeat their completed whole-page reviews or create additional review rows. Seventeen canonical pages received targeted changes; Poseidon's existing ledger additionally records a verified ABC glyph without a page edit. All 23 original factor records remain unique.

## Repairs and direct evidence

All listed PNGs are renders of the immutable local source PDFs and were personally viewed. Filenames below are in this directory.

| Pages | Actual repair | Original passage and render |
| --- | --- | --- |
| Sun | Separate swallowed Gemini 0016; correct subsequent labels through Pisces 0025. Restore Hand's “shaper of the will, particularly the will” and paragraph boundary. | Ebertin printed 45–47 / PDF 47–49, `factor-source-repairs-ebertin-pdf47.png` through `49.png`; Hand PDF 56, `factor-source-repairs-robert-hand-pdf56.png`. |
| Jupiter, Venus, Uranus, Neptune | Remove twelve conditional placements from each sociological paragraph into its native section. Preserve claims, sign glyph identities, entry codes, house markers, and old section fragments. | Ebertin printed 57–58 / PDF 59–60; 53–54 / 55–56; 61–63 / 63–65; 64–66 / 66–68. Corresponding `factor-source-repairs-ebertin-pdfN.png` files. |
| Pluto | Separate Gemini 0133; correct following signs through Pisces 0142 and Capricorn 0140 locator. | Ebertin printed 67–68 / PDF 69–70. |
| MC | Rejoin Taurus around a footnote; retain footnote separately as historical argument; correct Gemini–Aquarius labels and recover Pisces 0181; correct Scorpio 0177 locator. | Ebertin printed 74–76 / PDF 76–78. |
| Asc, Node, Moon | Asc Taurus is 0158, printed 71; Node Leo is 0148, printed 69. Moon's trailing TIJ is the following Virgo glyph. Asc's Virgo/Libra repetition is genuinely printed and remains visible. | Ebertin PDF 73–75, 71–72, and 50–51 respectively. |
| Admetos, Apollon, Asc, Mercury, Neptune, Node, Saturn, Uranus | Correct mistranslations and omitted tails within their admitted ABC keyword lines; retain the German quotation beside a labeled editorial translation. Examples: thoroughness rather than gravity, multiplication rather than veneration, mediation rather than veins, suddenness rather than plotting. | ABC printed 16–17 / PDF 7, `factor-source-repairs-abc-pdf7.png`. Venus, Moon and Poseidon parser glyph concerns were also checked against this scan. |
| Mercury, Venus, Saturn, Uranus, Neptune | Complete the specific broken sentence or paragraph; correct Saturn/Uranus boundary contamination. Label short excerpts explicitly rather than claiming complete Hand chapter coverage. | Hand PDF 64, 67, 84–85, 91; corresponding `factor-source-repairs-hand-pdfN.png`. |
| Node, Pluto, Asc, MC | Recover Node's printed 1°45′ token as historical text only; remove Pluto's next-chapter number; restore Asc/MC's chapter 9 reference and damaged closing words. | Hand PDF 107, 99–100, and 104. |
| Vernal Point, Mars | Verify cardinal glyph names and “making”; Hand's “widest” rather than “oddest,” Aries and 1920s, and related OCR; Mars/Ares and “own integrity” restored. | Witte PDF 27, Hand PDF 108–109 and 72–73. |
| Chiron | Consolidate three repeated Identity exclusions into one scope sentence. | Existing structural identity and source-scope entry; `structural_only: true` retained. |

## Verification

- Actual revised Ebertin source blocks and their surrounding notes were read after editing and checked against the viewed scans. Each of the seven extensively rebuilt blocks has exactly twelve correctly sequenced sign/code rows.
- Scoped required-environment Python checks passed for all 23 factor pages: unique original ledger record, preserved canonical metadata (apart from the already authorized Chiron structural flag and review date), adjacent synthesis anchor, six schema categories, local file targets, and changed/unchanged outcomes against the original captured pages.
- `git diff --check -- wiki/factors docs/reviews/2026-10-15-full-wiki/ledgers/factors-*.jsonl` passed; Git reported only its existing LF/CRLF conversion notices.
- Source repair acceptance is independently owned by `source_integrity_gate`; this report is implementation evidence, not blanket approval of source changes.

## Remaining limits

The Asc Virgo/Libra duplication is an apparent source problem whose authorial intent cannot be settled from this edition. It is retained rather than silently corrected. PDF-only sources often lack visible printed folios. Uninspected inherited Hand OCR outside the targeted boundary pages remains identified in the original records; no complete raw-book proofread is claimed. These limitations do not restore the repaired mislabeled rows or broken endings to unresolved status.

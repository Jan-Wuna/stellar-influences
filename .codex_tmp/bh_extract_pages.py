# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# --- How to run ---
# C:/pyMADMAX2/miniconda3/envs/deep11/python.exe .codex_tmp/bh_extract_pages.py <pdf> <first-page> <last-page> <output>
from __future__ import annotations

import sys
from pathlib import Path

import fitz


def main() -> int:
    pdf_path = Path(sys.argv[1])
    first_page = int(sys.argv[2])
    last_page = int(sys.argv[3])
    output_path = Path(sys.argv[4])

    chunks: list[str] = []
    with fitz.open(pdf_path) as doc:
        for page_number in range(first_page, last_page + 1):
            page = doc.load_page(page_number - 1)
            chunks.append(f"\n\n=== PDF page {page_number} ===\n")
            chunks.append(page.get_text("text"))

    output_path.write_text("".join(chunks), encoding="utf-8")
    print(f"WROTE {output_path} bytes={output_path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

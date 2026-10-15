#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pymupdf",
# ]
# ///

# --- How to run ---
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run extract_hall_pdf_pages.py [PDF_PATH] [FIRST_PAGE] [LAST_PAGE]
# 3. Or run with the project interpreter:
#      C:/pyMADMAX2/miniconda3/envs/deep11/python.exe extract_hall_pdf_pages.py [PDF_PATH] [FIRST_PAGE] [LAST_PAGE]
# ------------------

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf

DEFAULT_PDF_PATH = Path("W:/books references etc/!master list astro/varia - Manly P Hall - Astrological Keywords.pdf")
DEFAULT_FIRST_PAGE = 104
DEFAULT_LAST_PAGE = 121


def page_arg(index: int, default: int) -> int:
    if len(sys.argv) <= index:
        return default
    return int(sys.argv[index])


def main() -> None:
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF_PATH
    first_page = page_arg(2, DEFAULT_FIRST_PAGE)
    last_page = page_arg(3, DEFAULT_LAST_PAGE)

    with pymupdf.open(pdf_path) as document:
        for page_number in range(first_page, last_page + 1):
            page = document[page_number - 1]
            print(f"\n===== PDF PAGE {page_number} =====")
            print(page.get_text("text"))


if __name__ == "__main__":
    main()

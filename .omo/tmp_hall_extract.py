from __future__ import annotations

import sys
from pathlib import Path


PDF = Path("W:/books references etc/!master list astro/varia - Manly P Hall - Astrological Keywords.pdf")


def extract_pages(start: int, end: int) -> None:
    from PyPDF2 import PdfReader

    reader = PdfReader(str(PDF))
    print(f"PDF page count: {len(reader.pages)}")
    for page_number in range(start, end + 1):
        page = reader.pages[page_number - 1]
        text = page.extract_text() or ""
        print(f"\n===== PDF PAGE {page_number} =====")
        print(text)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: tmp_hall_extract.py START_PAGE END_PAGE")
    extract_pages(int(sys.argv[1]), int(sys.argv[2]))


if __name__ == "__main__":
    main()

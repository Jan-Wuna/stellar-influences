from __future__ import annotations

from pathlib import Path
import sys

import fitz
import numpy as np

from tools.witte_source import _extract_ocr_line_records


def _pdf_path(root: Path) -> Path:
    return next(
        (root / "Stellar Influences Vault").glob(
            "planetary expressions - Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures 2020.pdf"
        )
    )


def print_font_summary(doc: fitz.Document) -> None:
    pages_by_font: dict[str, set[int]] = {}
    for page_number in range(doc.page_count):
        for _, _, _, basefont, *_ in doc[page_number].get_fonts():
            pages_by_font.setdefault(basefont, set()).add(page_number + 1)
    print("Fonts:")
    for font, pages in sorted(pages_by_font.items()):
        first_pages = ", ".join(str(page) for page in sorted(pages)[:12])
        print(f"  {font}: {len(pages)} pages (first pages: {first_pages})")


def print_search_hits(doc: fitz.Document, needle: str) -> None:
    print(f"Search hits for {needle!r}:")
    found = False
    for page_number in range(doc.page_count):
        text = doc[page_number].get_text("text")
        if needle.lower() in text.lower():
            found = True
            print(f"\n=== PAGE {page_number + 1} ===")
            print(text[:2500].replace("\x0c", " "))
    if not found:
        print("  none")


def print_page_dump(doc: fitz.Document, page_number: int) -> None:
    page = doc[page_number - 1]
    text = page.get_text("text")
    print(f"\n=== PAGE {page_number} ===")
    print(text[:4000].replace("\x0c", " "))
    data = page.get_text("dict")
    for block in data["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span["text"].strip():
                    print(f"FONT={span['font']!r} TEXT={span['text']!r}")


def print_line_dump(doc: fitz.Document, page_number: int) -> None:
    page = doc[page_number - 1]
    data = page.get_text("dict")
    print(f"\n=== PAGE {page_number} LINES ===")
    for block in data["blocks"]:
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            text = "".join(span["text"] for span in spans).rstrip()
            if not text.strip():
                continue
            x0 = min(span["bbox"][0] for span in spans)
            x1 = max(span["bbox"][2] for span in spans)
            print(f"x0={x0:6.1f} x1={x1:6.1f} text={text!r}")


def print_ocr_line_dump(pdf_path: Path, page_number: int) -> None:
    print(f"\n=== PAGE {page_number} OCR LINES ===")
    for record in _extract_ocr_line_records(pdf_path, page_number):
        print(f"x0={record.x0:6.1f} y0={record.y0:6.1f} text={record.text!r}")


def print_line_ink_dump(doc: fitz.Document, page_number: int) -> None:
    page = doc[page_number - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    gray = image.mean(axis=2)
    data = page.get_text("dict")
    print(f"\n=== PAGE {page_number} LINE INK ===")
    for block in data["blocks"]:
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            text = "".join(span["text"] for span in spans).rstrip()
            if not text.strip():
                continue
            x0 = min(span["bbox"][0] for span in spans)
            y0 = min(span["bbox"][1] for span in spans)
            y1 = max(span["bbox"][3] for span in spans)
            sx0 = 0
            sx1 = min(int(90 * 2), gray.shape[1])
            sy0 = max(0, int(y0 * 2) - 2)
            sy1 = min(gray.shape[0], int(y1 * 2) + 2)
            crop = gray[sy0:sy1, sx0:sx1]
            dark = int((crop < 230).sum())
            col_dark = (crop < 230).sum(axis=0)
            nonzero = np.where(col_dark > 0)[0]
            if nonzero.size:
                first = int(nonzero[0])
                last = int(nonzero[-1])
            else:
                first = -1
                last = -1
            print(
                f"x0={x0:6.1f} dark={dark:5d} first={first:3d} last={last:3d} text={text!r}"
            )


def main() -> None:
    root = Path.cwd()
    pdf_path = _pdf_path(root)
    doc = fitz.open(pdf_path)
    print(f"PDF: {pdf_path}")
    print(f"Pages: {doc.page_count}")
    if len(sys.argv) == 1:
        print_font_summary(doc)
        return
    if sys.argv[1] == "--search":
        print_search_hits(doc, sys.argv[2])
        return
    if sys.argv[1] == "--page":
        print_page_dump(doc, int(sys.argv[2]))
        return
    if sys.argv[1] == "--lines":
        print_line_dump(doc, int(sys.argv[2]))
        return
    if sys.argv[1] == "--ocr-lines":
        print_ocr_line_dump(pdf_path, int(sys.argv[2]))
        return
    if sys.argv[1] == "--lineink":
        print_line_ink_dump(doc, int(sys.argv[2]))
        return
    raise SystemExit(
        "Usage: tmp_inspect_witte_pdf.py [--search TEXT | --page N | --lines N | --ocr-lines N | --lineink N]"
    )


if __name__ == "__main__":
    main()

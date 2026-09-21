#!/usr/bin/env python3
"""
extract_pdf.py — Extract PDF/PPTX pages as high-res PNG images for multimodal reading.

Uses PyMuPDF (fitz) to convert each page to a PNG image at 2x zoom,
enabling Claude's multimodal vision to read tables, charts, images,
and complex layouts that text-only extractors (Docling, pdfplumber) miss.

Usage:
  python scripts/extract_pdf.py <input.pdf> <output_dir> [--pages 1-10] [--zoom 2.0]
  python scripts/extract_pdf.py <input.pptx> <output_dir> [--pages 1-10] [--zoom 2.0]

Output:
  <output_dir>/page-001.png
  <output_dir>/page-002.png
  ...

Requires: pip install pymupdf
"""

import sys
import os
import argparse

# Windows UTF-8 fix
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def parse_page_range(page_str: str, total_pages: int) -> list[int]:
    """Parse a page range string like '1-10' or '5' or '1-5,8,10-12' into 0-indexed list."""
    pages = []
    for part in page_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = max(1, int(start))
            end = min(total_pages, int(end))
            pages.extend(range(start - 1, end))
        else:
            p = int(part) - 1
            if 0 <= p < total_pages:
                pages.append(p)
    return sorted(set(pages))


def extract_pages(input_path: str, output_dir: str, pages: list[int] | None = None, zoom: float = 2.0):
    """Extract PDF/PPTX pages as PNG images."""
    try:
        import fitz
    except ImportError:
        print("ERROR: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(input_path):
        print(f"ERROR: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(input_path)
    total = doc.page_count

    if pages is None:
        pages = list(range(total))

    mat = fitz.Matrix(zoom, zoom)
    extracted = []

    for page_num in pages:
        if page_num >= total:
            continue
        page = doc[page_num]
        pix = page.get_pixmap(matrix=mat)
        filename = f"page-{page_num + 1:03d}.png"
        filepath = os.path.join(output_dir, filename)
        pix.save(filepath)
        extracted.append({
            "page": page_num + 1,
            "file": filepath,
            "width": pix.width,
            "height": pix.height
        })

    doc.close()
    return extracted


def main():
    parser = argparse.ArgumentParser(description="Extract PDF/PPTX pages as PNG images")
    parser.add_argument("input", help="Path to PDF or PPTX file")
    parser.add_argument("output_dir", help="Directory to save PNG images")
    parser.add_argument("--pages", help="Page range (e.g., '1-10', '5', '1-5,8,10-12'). Default: all pages", default=None)
    parser.add_argument("--zoom", type=float, default=2.0, help="Zoom factor for image quality (default: 2.0)")

    args = parser.parse_args()

    # Detect total pages first
    try:
        import fitz
    except ImportError:
        print("ERROR: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(args.input)
    total = doc.page_count
    doc.close()

    # Parse page range
    pages = None
    if args.pages:
        pages = parse_page_range(args.pages, total)

    # Extract
    results = extract_pages(args.input, args.output_dir, pages, args.zoom)

    # Report
    print(f"Extracted {len(results)} pages from {os.path.basename(args.input)}")
    print(f"Output: {args.output_dir}")
    print(f"Total pages in document: {total}")
    for r in results:
        print(f"  page-{r['page']:03d}.png ({r['width']}x{r['height']})")


if __name__ == "__main__":
    main()

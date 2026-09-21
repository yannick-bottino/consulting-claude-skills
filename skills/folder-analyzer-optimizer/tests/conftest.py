import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

"""Shared pytest fixtures for tree_builder tests."""
from pathlib import Path
import pymupdf
import pytest


@pytest.fixture
def fixtures_dir():
    """Path to tests/fixtures/."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def make_pdf_with_toc(tmp_path):
    """
    Factory: builds a PDF with N pages and a custom TOC.
    Usage: pdf_path = make_pdf_with_toc(60, [[1,"Chap 1",1],[2,"Sec 1.1",2],[1,"Chap 2",30]])
    """
    def _build(page_count: int, toc: list, filename: str = "test.pdf") -> Path:
        doc = pymupdf.open()
        for i in range(page_count):
            page = doc.new_page()
            page.insert_text((72, 72), f"Body of page {i + 1}")
        if toc:
            doc.set_toc(toc)
        path = tmp_path / filename
        doc.save(str(path))
        doc.close()
        return path
    return _build


@pytest.fixture
def sample_md_with_anchors():
    """A .md text containing `## Page N` anchors and headings, for preview/regex tests."""
    return (
        "# document.pdf\n"
        "<!-- Parsed: ... -->\n\n"
        "## Page 1\n\n"
        "# Definitions and Interpretation\n\n"
        "In this Agreement, unless the context otherwise requires, the following terms shall have the meanings set forth in this section. References to clauses, schedules and annexes are to clauses, schedules and annexes of this Agreement.\n\n"
        "## Page 2\n\n"
        "Body text continues here on page two with more content.\n\n"
        "## Page 19\n\n"
        "# Sale and Purchase\n\n"
        "Subject to the terms and conditions of this Agreement, the Seller agrees to sell and the Purchaser agrees to purchase the Sale Shares.\n\n"
        "## Page 26\n\n"
        "## Earn-Out\n\n"
        "An additional amount of up to EUR 5,000,000 (the Earn-Out Amount) shall be payable subject to achievement of EBITDA targets.\n\n"
        "## Page 35\n\n"
        "# Representations and Warranties\n\n"
        "Each Party makes the following representations.\n"
    )

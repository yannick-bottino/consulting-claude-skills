"""Tests for tree_builder."""
import pytest
from tree_builder import nest_headings, compute_end_pages, assess_tree_quality, extract_preview, extract_headings_pymupdf_toc, extract_headings_markdown_regex


def test_nest_headings_flat_single_level():
    headings = [
        {"level": 1, "title": "A", "page": 1},
        {"level": 1, "title": "B", "page": 10},
        {"level": 1, "title": "C", "page": 20},
    ]
    tree = nest_headings(headings)
    assert len(tree) == 3
    assert tree[0]["node_id"] == "n1"
    assert tree[1]["node_id"] == "n2"
    assert tree[2]["node_id"] == "n3"
    assert all(node["nodes"] == [] for node in tree)


def test_nest_headings_two_levels():
    headings = [
        {"level": 1, "title": "A", "page": 1},
        {"level": 2, "title": "A.1", "page": 2},
        {"level": 2, "title": "A.2", "page": 5},
        {"level": 1, "title": "B", "page": 10},
        {"level": 2, "title": "B.1", "page": 11},
    ]
    tree = nest_headings(headings)
    assert len(tree) == 2
    assert tree[0]["title"] == "A"
    assert tree[0]["node_id"] == "n1"
    assert len(tree[0]["nodes"]) == 2
    assert tree[0]["nodes"][0]["node_id"] == "n1.1"
    assert tree[0]["nodes"][1]["node_id"] == "n1.2"
    assert tree[1]["node_id"] == "n2"
    assert tree[1]["nodes"][0]["node_id"] == "n2.1"


def test_nest_headings_skip_level():
    """A level-3 right after a level-1 attaches to the level-1 (no synthetic level-2)."""
    headings = [
        {"level": 1, "title": "A", "page": 1},
        {"level": 3, "title": "A.x", "page": 2},
        {"level": 1, "title": "B", "page": 10},
    ]
    tree = nest_headings(headings)
    assert len(tree) == 2
    assert len(tree[0]["nodes"]) == 1
    assert tree[0]["nodes"][0]["node_id"] == "n1.1"
    assert tree[0]["nodes"][0]["level"] == 3
    assert tree[0]["nodes"][0]["title"] == "A.x"


def test_nest_headings_empty():
    assert nest_headings([]) == []


def test_nest_headings_preserves_page():
    headings = [
        {"level": 1, "title": "A", "page": 5},
        {"level": 2, "title": "A.1", "page": 7},
    ]
    tree = nest_headings(headings)
    assert tree[0]["start_page"] == 5
    assert tree[0]["nodes"][0]["start_page"] == 7


def test_compute_end_pages_single_node():
    tree = [{"node_id": "n1", "title": "A", "level": 1, "start_page": 1, "nodes": []}]
    compute_end_pages(tree, page_count=20)
    assert tree[0]["end_page"] == 20


def test_compute_end_pages_two_siblings():
    tree = [
        {"node_id": "n1", "title": "A", "level": 1, "start_page": 1, "nodes": []},
        {"node_id": "n2", "title": "B", "level": 1, "start_page": 10, "nodes": []},
    ]
    compute_end_pages(tree, page_count=20)
    assert tree[0]["end_page"] == 9
    assert tree[1]["end_page"] == 20


def test_compute_end_pages_nested():
    tree = [
        {
            "node_id": "n1", "title": "A", "level": 1, "start_page": 1,
            "nodes": [
                {"node_id": "n1.1", "title": "A.1", "level": 2, "start_page": 2, "nodes": []},
                {"node_id": "n1.2", "title": "A.2", "level": 2, "start_page": 5, "nodes": []},
            ],
        },
        {"node_id": "n2", "title": "B", "level": 1, "start_page": 10, "nodes": []},
    ]
    compute_end_pages(tree, page_count=20)
    assert tree[0]["end_page"] == 9
    assert tree[0]["nodes"][0]["end_page"] == 4
    assert tree[0]["nodes"][1]["end_page"] == 9
    assert tree[1]["end_page"] == 20


def test_compute_end_pages_clamps_pathological():
    """If two headings sit on the same page, end_page = start_page (no negative range)."""
    tree = [
        {"node_id": "n1", "title": "A", "level": 1, "start_page": 5, "nodes": []},
        {"node_id": "n2", "title": "B", "level": 1, "start_page": 5, "nodes": []},
    ]
    compute_end_pages(tree, page_count=20)
    assert tree[0]["end_page"] == 5
    assert tree[1]["end_page"] == 20


def test_quality_insufficient_too_few_headings():
    headings = [{"level": 1, "title": "A", "page": 1}] * 4
    assert assess_tree_quality(headings, page_count=100) == "INSUFFICIENT"


def test_quality_ok_two_levels_good_coverage():
    """8 headings, 2 levels, 8 unique pages => 8/80 = 10% coverage."""
    headings = [
        {"level": 1, "title": "A", "page": 1},
        {"level": 2, "title": "A.1", "page": 5},
        {"level": 1, "title": "B", "page": 15},
        {"level": 2, "title": "B.1", "page": 20},
        {"level": 1, "title": "C", "page": 35},
        {"level": 2, "title": "C.1", "page": 40},
        {"level": 1, "title": "D", "page": 55},
        {"level": 2, "title": "D.1", "page": 60},
    ]
    assert assess_tree_quality(headings, page_count=80) == "OK"


def test_quality_degraded_flat_but_present():
    """5 headings, single level, decent coverage → DEGRADED."""
    headings = [{"level": 1, "title": f"H{i}", "page": i * 10 + 1} for i in range(6)]
    assert assess_tree_quality(headings, page_count=100) == "DEGRADED"


def test_quality_insufficient_clustered():
    """8 headings but all on page 1 → coverage too low."""
    headings = [{"level": 1, "title": f"H{i}", "page": 1} for i in range(8)]
    headings.append({"level": 2, "title": "X", "page": 1})
    assert assess_tree_quality(headings, page_count=200) == "INSUFFICIENT"


def test_extract_preview_first_section(sample_md_with_anchors):
    preview = extract_preview(sample_md_with_anchors, start_page=1, end_page=18, max_chars=120)
    assert preview.startswith("In this Agreement")
    assert len(preview) <= 121  # +1 for ellipsis
    assert preview.endswith("…")


def test_extract_preview_strips_headings(sample_md_with_anchors):
    """Heading lines like '# Sale and Purchase' must be excluded from preview."""
    preview = extract_preview(sample_md_with_anchors, start_page=19, end_page=25, max_chars=300)
    assert "Sale and Purchase" not in preview
    assert preview.startswith("Subject to the terms")


def test_extract_preview_missing_anchor():
    md = "## Page 5\n\nSome text on page five.\n"
    preview = extract_preview(md, start_page=99, end_page=100)
    assert preview == ""


def test_extract_preview_no_truncation_needed():
    md = "## Page 1\n\nShort body.\n"
    preview = extract_preview(md, start_page=1, end_page=1, max_chars=300)
    assert preview == "Short body."
    assert not preview.endswith("…")


def test_pymupdf_toc_extracts_known_outline(make_pdf_with_toc):
    pdf_path = make_pdf_with_toc(
        60,
        [
            [1, "Chapter 1", 1],
            [2, "Section 1.1", 2],
            [2, "Section 1.2", 5],
            [1, "Chapter 2", 30],
            [2, "Section 2.1", 31],
        ],
    )
    headings = extract_headings_pymupdf_toc(pdf_path)
    assert len(headings) == 5
    assert headings[0] == {"level": 1, "title": "Chapter 1", "page": 1}
    assert headings[3] == {"level": 1, "title": "Chapter 2", "page": 30}


def test_pymupdf_toc_returns_empty_when_no_outline(make_pdf_with_toc):
    pdf_path = make_pdf_with_toc(60, [])
    headings = extract_headings_pymupdf_toc(pdf_path)
    assert headings == []


def test_pymupdf_toc_handles_unreadable_file(tmp_path):
    bad = tmp_path / "not_a_pdf.pdf"
    bad.write_text("this is not a PDF")
    headings = extract_headings_pymupdf_toc(bad)
    assert headings == []


def test_markdown_regex_uses_nearest_page_anchor(sample_md_with_anchors):
    headings = extract_headings_markdown_regex(sample_md_with_anchors)
    titles = [(h["level"], h["title"], h["page"]) for h in headings]
    assert (1, "Definitions and Interpretation", 1) in titles
    assert (1, "Sale and Purchase", 19) in titles
    assert (2, "Earn-Out", 26) in titles
    assert (1, "Representations and Warranties", 35) in titles


def test_markdown_regex_ignores_page_anchors_themselves(sample_md_with_anchors):
    """`## Page N` lines must NOT be returned as headings."""
    headings = extract_headings_markdown_regex(sample_md_with_anchors)
    for h in headings:
        assert not h["title"].startswith("Page ")


def test_markdown_regex_empty_doc_returns_empty():
    assert extract_headings_markdown_regex("") == []


def test_markdown_regex_no_anchors_defaults_to_page_1():
    md = "# A\n\nbody\n\n## B\n\nbody\n"
    headings = extract_headings_markdown_regex(md)
    assert headings[0]["page"] == 1
    assert headings[1]["page"] == 1


from tree_builder import build_chunked_tree


def test_chunked_tree_divides_evenly():
    tree = build_chunked_tree(page_count=30, chunk_pages=10, md_text="")
    assert len(tree) == 3
    assert tree[0]["start_page"] == 1
    assert tree[0]["end_page"] == 10
    assert tree[0]["title"] == "Pages 1-10"
    assert tree[0]["node_id"] == "n1"
    assert tree[2]["start_page"] == 21
    assert tree[2]["end_page"] == 30


def test_chunked_tree_handles_remainder():
    tree = build_chunked_tree(page_count=25, chunk_pages=10, md_text="")
    assert len(tree) == 3
    assert tree[2]["start_page"] == 21
    assert tree[2]["end_page"] == 25
    assert tree[2]["title"] == "Pages 21-25"


def test_chunked_tree_attaches_preview_when_md_available(sample_md_with_anchors):
    tree = build_chunked_tree(page_count=2, chunk_pages=1, md_text=sample_md_with_anchors)
    assert tree[0]["preview"].startswith("In this Agreement")


def test_chunked_tree_short_doc_single_node():
    tree = build_chunked_tree(page_count=5, chunk_pages=10, md_text="")
    assert len(tree) == 1
    assert tree[0]["start_page"] == 1
    assert tree[0]["end_page"] == 5


import json
from tree_builder import build_tree_for_file, DEFAULT_TREE_CONFIG


def _make_md_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_build_tree_skipped_too_short(tmp_path, make_pdf_with_toc):
    pdf = make_pdf_with_toc(30, [[1, "X", 1], [1, "Y", 15]])
    md = tmp_path / "out" / "x.md"
    _make_md_file(md, "## Page 1\n\nbody\n")
    status = build_tree_for_file(
        source_path=pdf,
        md_path=md,
        page_count=30,
        output_root=tmp_path / "out",
        config=DEFAULT_TREE_CONFIG,
    )
    assert status == "SKIPPED_TOO_SHORT"
    assert not (tmp_path / "out" / "x.tree.json").exists()


def test_build_tree_ok_uses_pymupdf_toc(tmp_path, make_pdf_with_toc):
    toc = [
        [1, "Chapter 1", 1],
        [2, "Section 1.1", 5],
        [1, "Chapter 2", 20],
        [2, "Section 2.1", 25],
        [1, "Chapter 3", 35],
        [2, "Section 3.1", 40],
        [1, "Chapter 4", 50],
        [2, "Section 4.1", 55],
    ]
    pdf = make_pdf_with_toc(60, toc, filename="long.pdf")
    md = tmp_path / "out" / "long.md"
    _make_md_file(md, "## Page 1\n\nBody.\n## Page 20\n\nMore body.\n")
    status = build_tree_for_file(
        source_path=pdf,
        md_path=md,
        page_count=60,
        output_root=tmp_path / "out",
        config=DEFAULT_TREE_CONFIG,
    )
    assert status == "OK"
    sidecar = tmp_path / "out" / "long.tree.json"
    assert sidecar.exists()
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    assert data["heading_extraction"] == "pymupdf_toc"
    assert data["quality"] == "OK"
    assert data["page_count"] == 60
    assert len(data["tree"]) == 4  # 4 chapters
    assert data["tree"][0]["nodes"][0]["title"] == "Section 1.1"


def test_build_tree_skipped_no_structure(tmp_path, make_pdf_with_toc):
    pdf = make_pdf_with_toc(80, [], filename="flat.pdf")
    md = tmp_path / "out" / "flat.md"
    _make_md_file(md, "## Page 1\n\nbody\n## Page 2\n\nbody\n")
    status = build_tree_for_file(
        source_path=pdf,
        md_path=md,
        page_count=80,
        output_root=tmp_path / "out",
        config=DEFAULT_TREE_CONFIG,
    )
    assert status == "SKIPPED_NO_STRUCTURE"
    assert not (tmp_path / "out" / "flat.tree.json").exists()


def test_build_tree_forced_chunked(tmp_path, make_pdf_with_toc):
    pdf = make_pdf_with_toc(80, [], filename="trans.pdf")
    md = tmp_path / "out" / "trans.md"
    _make_md_file(md, "## Page 1\n\nbody\n")
    cfg = {**DEFAULT_TREE_CONFIG, "force_chunked_tree": True, "chunk_pages": 20}
    status = build_tree_for_file(
        source_path=pdf,
        md_path=md,
        page_count=80,
        output_root=tmp_path / "out",
        config=cfg,
    )
    assert status == "FORCED_CHUNKED"
    sidecar = tmp_path / "out" / "trans.tree.json"
    assert sidecar.exists()
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    assert data["heading_extraction"] == "chunked"
    assert len(data["tree"]) == 4


def test_build_tree_disabled(tmp_path, make_pdf_with_toc):
    toc = [[1, f"H{i}", i * 5 + 1] for i in range(10)]
    pdf = make_pdf_with_toc(60, toc)
    md = tmp_path / "out" / "x.md"
    _make_md_file(md, "## Page 1\n\nbody\n")
    cfg = {**DEFAULT_TREE_CONFIG, "enabled": False}
    status = build_tree_for_file(
        source_path=pdf,
        md_path=md,
        page_count=60,
        output_root=tmp_path / "out",
        config=cfg,
    )
    assert status == "SKIPPED_DISABLED"


from tree_builder import render_structured_documents_section


def _sample_tree_payload():
    return {
        "source_path": "Contrats/SPA_v3.pdf",
        "md_path": "Contrats/SPA_v3.md",
        "page_count": 187,
        "heading_extraction": "pymupdf_toc",
        "quality": "OK",
        "generated_at": "2026-05-13T14:42:00",
        "tree": [
            {
                "node_id": "n1", "title": "Definitions", "level": 1,
                "start_page": 5, "end_page": 18,
                "preview": "In this Agreement, unless the context otherwise requires…",
                "nodes": [],
            },
            {
                "node_id": "n2", "title": "Sale and Purchase", "level": 1,
                "start_page": 19, "end_page": 34,
                "preview": "Subject to the terms and conditions…",
                "nodes": [
                    {
                        "node_id": "n2.1", "title": "Purchase Price", "level": 2,
                        "start_page": 19, "end_page": 25,
                        "preview": "The aggregate consideration…", "nodes": [],
                    },
                    {
                        "node_id": "n2.2", "title": "Earn-Out", "level": 2,
                        "start_page": 26, "end_page": 34,
                        "preview": "An additional amount of up to EUR 5,000,000…",
                        "nodes": [],
                    },
                ],
            },
        ],
    }


def test_render_empty_when_no_trees():
    assert render_structured_documents_section([], max_depth=2) == ""


def test_render_includes_doc_header_and_links():
    md = render_structured_documents_section(
        [(_sample_tree_payload(), "SPA_v3.pdf", 42800)],
        max_depth=2,
    )
    assert "## Documents structurés" in md
    assert "SPA_v3.pdf" in md
    assert "[doc complet](SPA_v3.md)" in md
    assert "[arbre](SPA_v3.tree.json)" in md
    assert "187 p." in md
    assert "structure pymupdf_toc" in md


def test_render_shows_level1_with_preview_inline():
    md = render_structured_documents_section(
        [(_sample_tree_payload(), "SPA_v3.pdf", 42800)],
        max_depth=2,
    )
    assert "**1. Definitions**" in md or "**Definitions**" in md
    assert "*(p. 5-18)*" in md
    assert "In this Agreement" in md


def test_render_shows_level2_without_preview_when_max_depth_2():
    md = render_structured_documents_section(
        [(_sample_tree_payload(), "SPA_v3.pdf", 42800)],
        max_depth=2,
    )
    assert "Purchase Price" in md
    assert "Earn-Out" in md


def test_render_degraded_adds_badge():
    payload = _sample_tree_payload()
    payload["quality"] = "DEGRADED"
    md = render_structured_documents_section(
        [(payload, "x.pdf", 1000)],
        max_depth=2,
    )
    assert "*(structure partielle)*" in md


def test_render_forced_chunked_adds_badge():
    payload = _sample_tree_payload()
    payload["heading_extraction"] = "chunked"
    md = render_structured_documents_section(
        [(payload, "x.pdf", 1000)],
        max_depth=2,
    )
    assert "*(découpage par plages de pages)*" in md

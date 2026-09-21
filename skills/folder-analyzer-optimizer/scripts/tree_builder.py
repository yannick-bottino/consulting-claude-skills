"""
Tree builder for folder-analyzer-optimizer Step 6.5.

Zero-token PageIndex-like indexing of long documents (>= 50 pages).
See references/tree-builder.md.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

# Default configuration. Overridable via CLAUDE.md or runtime kwargs.
DEFAULT_TREE_CONFIG = {
    "enabled": True,
    "tree_threshold_pages": 50,
    "min_headings": 5,
    "max_depth_in_index_md": 2,
    "preview_chars": 300,
    "force_chunked_tree": False,
    "chunk_pages": 10,
}


def nest_headings(headings: list[dict]) -> list[dict]:
    """
    Convert a flat list of {level, title, page} into a nested tree.

    Each node:
        {
            "node_id": "n1.2.1",
            "title": str,
            "level": int,
            "start_page": int,
            "nodes": [child_node, ...]
        }

    Nesting rule: a heading attaches to the most recent ancestor with level <
    its own. If no such ancestor exists, it becomes a top-level node.
    """
    root_nodes: list[dict] = []
    # Stack entries: (node, level)
    stack: list[tuple[dict, int]] = []

    def make_node_id(parent_id: str | None, index_among_siblings: int) -> str:
        if parent_id is None:
            return f"n{index_among_siblings}"
        return f"{parent_id}.{index_among_siblings}"

    for h in headings:
        level = h["level"]
        # Pop ancestors with level >= current
        while stack and stack[-1][1] >= level:
            stack.pop()

        if stack:
            parent_node = stack[-1][0]
            siblings = parent_node["nodes"]
            node_id = make_node_id(parent_node["node_id"], len(siblings) + 1)
        else:
            siblings = root_nodes
            node_id = make_node_id(None, len(siblings) + 1)

        node = {
            "node_id": node_id,
            "title": h["title"],
            "level": level,
            "start_page": h["page"],
            "nodes": [],
        }
        siblings.append(node)
        stack.append((node, level))

    return root_nodes


def compute_end_pages(tree: list[dict], page_count: int) -> None:
    """
    Mutate every node in-place to add `end_page`.

    Rule: end_page = (next sibling at same level).start_page - 1,
          or (next ancestor sibling).start_page - 1,
          or page_count if no such sibling exists.
    Clamped to >= start_page.
    """
    # Flatten depth-first with parent linkage, then post-process.
    flat: list[dict] = []

    def walk(nodes: list[dict]) -> None:
        for n in nodes:
            flat.append(n)
            walk(n["nodes"])

    walk(tree)

    # Build a list of "next boundary page" candidates by walking the flat list:
    # end_page of node i = min(start_page of any later node whose level <= i.level) - 1
    for i, node in enumerate(flat):
        boundary = page_count
        for later in flat[i + 1 :]:
            if later["level"] <= node["level"]:
                boundary = later["start_page"] - 1
                break
        # A nested child's range also ends when the parent's range ends.
        # Already covered: a sibling of the parent has level <= parent.level <= node.level.
        end_page = max(node["start_page"], boundary)
        node["end_page"] = end_page


def assess_tree_quality(headings: list[dict], page_count: int) -> str:
    """
    Return 'OK', 'DEGRADED', or 'INSUFFICIENT'.

    OK         : >= 2 distinct levels AND >= 8 headings AND coverage >= 10%
    DEGRADED   : >= 5 headings AND coverage >= 5%
    INSUFFICIENT: anything else
    """
    n = len(headings)
    if n < 5:
        return "INSUFFICIENT"

    levels = {h["level"] for h in headings}
    covered_pages = {h["page"] for h in headings}
    coverage = len(covered_pages) / page_count if page_count else 0.0

    if len(levels) >= 2 and n >= 8 and coverage >= 0.10:
        return "OK"
    if n >= 5 and coverage >= 0.05:
        return "DEGRADED"
    return "INSUFFICIENT"


_PAGE_ANCHOR_RE = re.compile(r"^## Page \d+\s*\n", flags=re.MULTILINE)
_ANY_HEADING_RE = re.compile(r"^#{1,6}\s.*\n", flags=re.MULTILINE)


def extract_preview(
    md_text: str,
    start_page: int,
    end_page: int,
    max_chars: int = 300,
) -> str:
    """
    Return the first `max_chars` characters of body content found between
    `## Page {start_page}` and `## Page {end_page + 1}` anchors in `md_text`.
    Page anchors and any markdown heading lines are stripped before truncation.

    Returns "" if the start anchor cannot be located.
    """
    start_marker = f"## Page {start_page}\n"
    start = md_text.find(start_marker)
    if start < 0:
        return ""

    end_marker = f"## Page {end_page + 1}\n"
    end = md_text.find(end_marker, start)
    slice_text = md_text[start:end] if end > 0 else md_text[start:]

    clean = _PAGE_ANCHOR_RE.sub("", slice_text)
    clean = _ANY_HEADING_RE.sub("", clean)
    clean = re.sub(r"\s+", " ", clean).strip()

    if len(clean) <= max_chars:
        return clean
    return clean[:max_chars].rstrip() + "…"


def extract_headings_pymupdf_toc(pdf_path) -> list[dict]:
    """
    Use PyMuPDF's native get_toc() to read the embedded PDF outline.

    Returns a list of {level, title, page} dicts (page is 1-indexed).
    Returns [] if the file has no outline, cannot be opened, or raises any error.
    """
    try:
        import pymupdf
    except ImportError:
        return []
    try:
        doc = pymupdf.open(str(pdf_path))
    except Exception:
        return []
    try:
        toc = doc.get_toc(simple=True)
    except Exception:
        doc.close()
        return []
    doc.close()
    return [
        {"level": int(level), "title": str(title).strip(), "page": int(page)}
        for level, title, page in toc
        if str(title).strip()
    ]


_PAGE_ANCHOR_LINE_RE = re.compile(r"^## Page (\d+)\s*$")
_HEADING_LINE_RE = re.compile(r"^(#{1,4})\s+(.+?)\s*$")


def extract_headings_markdown_regex(md_text: str) -> list[dict]:
    """
    Scan a `.md` file produced by Step 2 of the skill. Return headings as
    {level, title, page}, where page is the page number of the most recent
    `## Page N` anchor seen above the heading (or 1 if no anchor yet).

    `## Page N` lines are NOT returned as headings.
    """
    current_page = 1
    headings: list[dict] = []
    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()
        page_match = _PAGE_ANCHOR_LINE_RE.match(line)
        if page_match:
            current_page = int(page_match.group(1))
            continue
        head_match = _HEADING_LINE_RE.match(line)
        if head_match:
            level = len(head_match.group(1))
            title = head_match.group(2).strip()
            if not title:
                continue
            headings.append({"level": level, "title": title, "page": current_page})
    return headings


def build_chunked_tree(page_count: int, chunk_pages: int, md_text: str) -> list[dict]:
    """
    Build a flat tree of N nodes, each spanning `chunk_pages` pages
    (last node may be shorter). Used as the FORCED_CHUNKED fallback.

    Each node gets a `preview` extracted from `md_text` if anchors are present.
    """
    nodes: list[dict] = []
    start = 1
    index = 1
    while start <= page_count:
        end = min(start + chunk_pages - 1, page_count)
        node = {
            "node_id": f"n{index}",
            "title": f"Pages {start}-{end}",
            "level": 1,
            "start_page": start,
            "end_page": end,
            "preview": extract_preview(md_text, start, end) if md_text else "",
            "nodes": [],
        }
        nodes.append(node)
        start = end + 1
        index += 1
    return nodes


def _inject_previews(nodes: list[dict], md_text: str, max_chars: int) -> None:
    """Walk tree, attach `preview` to every node."""
    for node in nodes:
        node["preview"] = extract_preview(md_text, node["start_page"], node["end_page"], max_chars)
        _inject_previews(node["nodes"], md_text, max_chars)


def _write_sidecar(
    sidecar_path: Path,
    source_path: Path,
    md_path: Path,
    page_count: int,
    heading_extraction: str,
    quality: str,
    tree: list[dict],
) -> None:
    payload = {
        "source_path": str(source_path),
        "md_path": str(md_path),
        "page_count": page_count,
        "heading_extraction": heading_extraction,
        "quality": quality,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "tree": tree,
    }
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    sidecar_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_tree_for_file(
    *,
    source_path: Path,
    md_path: Path,
    page_count: int,
    output_root: Path,
    config: dict,
) -> str:
    """
    Orchestrate the tree-building pipeline for one document.

    Returns one of:
      OK, DEGRADED, FORCED_CHUNKED,
      SKIPPED_DISABLED, SKIPPED_TOO_SHORT,
      SKIPPED_NO_STRUCTURE, SKIPPED_LOW_QUALITY, FAILED
    """
    if not config.get("enabled", True):
        return "SKIPPED_DISABLED"

    if page_count < config["tree_threshold_pages"]:
        return "SKIPPED_TOO_SHORT"

    source_path = Path(source_path)
    md_path = Path(md_path)
    sidecar_path = md_path.with_suffix(".tree.json")

    # --- Heading cascade ---
    headings = extract_headings_pymupdf_toc(source_path)
    heading_extraction = "pymupdf_toc"

    if len(headings) < config["min_headings"]:
        try:
            md_text = md_path.read_text(encoding="utf-8")
        except Exception:
            return "FAILED"
        headings = extract_headings_markdown_regex(md_text)
        heading_extraction = "markdown_regex_headings"
    else:
        try:
            md_text = md_path.read_text(encoding="utf-8")
        except Exception:
            md_text = ""

    if len(headings) < config["min_headings"]:
        if config.get("force_chunked_tree"):
            tree = build_chunked_tree(page_count, config["chunk_pages"], md_text)
            try:
                _write_sidecar(
                    sidecar_path, source_path, md_path, page_count,
                    "chunked", "FORCED_CHUNKED", tree,
                )
            except Exception:
                return "FAILED"
            return "FORCED_CHUNKED"
        return "SKIPPED_NO_STRUCTURE"

    quality = assess_tree_quality(headings, page_count)
    if quality == "INSUFFICIENT":
        return "SKIPPED_LOW_QUALITY"

    tree = nest_headings(headings)
    compute_end_pages(tree, page_count)
    _inject_previews(tree, md_text, config["preview_chars"])

    try:
        _write_sidecar(
            sidecar_path, source_path, md_path, page_count,
            heading_extraction, quality, tree,
        )
    except Exception:
        return "FAILED"
    return quality


def _format_inline_preview(preview: str, max_chars: int = 80) -> str:
    """Format a preview for inline display in markdown."""
    if not preview:
        return ""
    clean = preview.replace("\n", " ").strip()
    if len(clean) <= max_chars:
        return f" — {clean}"
    return f" — {clean[:max_chars].rstrip()}…"


def _render_node(node: dict, depth: int, max_depth: int, indent: str = "") -> list[str]:
    """
    Recursive render of a single node and its children.
    Returns a list of markdown lines.
    """
    lines: list[str] = []
    title = node["title"]
    pages = f"*(p. {node['start_page']}-{node['end_page']})*"
    # Only show preview for level-1 nodes
    preview_str = _format_inline_preview(node.get("preview", "")) if depth == 1 else ""
    # Bold only level-1 nodes
    bold = "**" if depth == 1 else ""
    lines.append(f"{indent}- {bold}{title}{bold} {pages}{preview_str}")
    # Recurse only if depth < max_depth
    if depth < max_depth:
        for child in node["nodes"]:
            lines.extend(_render_node(child, depth + 1, max_depth, indent + "  "))
    return lines


def render_structured_documents_section(
    trees: list[tuple[dict, str, int]],
    max_depth: int = 2,
    max_top_level_shown: int = 6,
) -> str:
    """
    Build the "Documents structurés" markdown block for a folder _index.md.

    Args:
        trees: List of (tree_payload, source_filename, word_count) tuples,
               where tree_payload is the JSON dict written by build_tree_for_file.
        max_depth: Maximum nesting depth to render (default 2).
        max_top_level_shown: Max top-level nodes to expand (default 6).

    Returns:
        Markdown string, or "" if trees is empty.
    """
    if not trees:
        return ""

    BADGE = {
        "DEGRADED": " *(structure partielle)*",
        "chunked": " *(découpage par plages de pages)*",
    }

    out: list[str] = ["## Documents structurés", ""]
    for payload, src_filename, word_count in trees:
        md_filename = Path(payload["md_path"]).name
        tree_filename = Path(payload["md_path"]).with_suffix(".tree.json").name
        page_count = payload["page_count"]
        extraction = payload["heading_extraction"]
        quality = payload["quality"]

        # Select badge: chunked extraction gets its badge, otherwise use quality badge
        badge = ""
        if extraction == "chunked":
            badge = BADGE.get("chunked", "")
        else:
            badge = BADGE.get(quality, "")

        out.append(
            f"### {src_filename} — [doc complet]({md_filename}) · [arbre]({tree_filename}){badge}"
        )
        out.append(f"*{page_count} p. | {word_count:,} mots | structure {extraction}*")
        out.append("")

        nodes = payload["tree"]
        for node in nodes[:max_top_level_shown]:
            out.extend(_render_node(node, depth=1, max_depth=max_depth))
        if len(nodes) > max_top_level_shown:
            out.append(f"- *(+ {len(nodes) - max_top_level_shown} sections de niveau 1)*")
        out.append("")

    out.append("---")
    out.append("")
    return "\n".join(out)

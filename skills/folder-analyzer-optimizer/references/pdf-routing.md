# PDF Extraction Routing
<!-- Loaded on demand by SKILL.md Step 2 -->

## Step 2: Extraction routing

Based on classification from Step 1, route each file to the appropriate extractor.

### Routing matrix

| Classification | Extractor                                      | Tokens                        | Speed      |
| -------------- | ---------------------------------------------- | ----------------------------- | ---------- |
| SCANNED        | Read tool vision (all pages)                   | ~700 x N_pages                | ~2s/page   |
| TEXT-HEAVY     | PyMuPDF (text extraction)                      | 0                             | ~0.1s/doc  |
| MIXED          | PyMuPDF (text) + Read tool (visual-dominant pages) | ~700 x N_visual_pages     | varies     |
| DOCX           | python-docx                                    | 0                             | ~0.5s      |
| PPTX           | python-pptx                                    | 0                             | ~0.5s      |

**Decision rule**: Route to SCANNED first (avg_words < 10), before attempting any free extractor. Running PyMuPDF text extraction on a scanned PDF wastes time and produces PARTIAL status with 0 words — a silent failure.

### 2a. SCANNED route (vision, all pages)

For PDFs with `avg_words < 10`: skip text extraction entirely. Convert every page to PNG and use Claude's native Read tool (multimodal vision).

```python
import pymupdf, os

def extract_scanned_pdf(file_path, output_root):
    """Convert all pages to PNG and return list of paths for Read tool processing."""
    doc = pymupdf.open(str(file_path))
    png_dir = output_root / "_vision_queue" / safe_folder_name(str(file_path))
    png_dir.mkdir(parents=True, exist_ok=True)

    png_paths = []
    for page_num in range(len(doc)):
        png_path = png_dir / f"page_{page_num+1:03d}.png"
        if not png_path.exists():
            pix = doc[page_num].get_pixmap(dpi=150)
            pix.save(str(png_path))
        png_paths.append(png_path)

    doc.close()
    return png_paths
```

Then, for each PNG, use the Read tool with this instruction:
> Transcribe ALL text visible on this page: titles, body text, tables, lists, dates, names, numbers, amounts, signatures, stamps, logos. For tables use Markdown table format. For charts/diagrams describe type, axes, values, trends. Do not summarize — transcribe faithfully.

Merge all page transcriptions into the final .md, with `## Page N` headers.

**Parallelization**: For large batches of scanned PDFs, group files into batches of ~15-20 pages and process in parallel subagents. Each subagent reads its assigned PNGs and writes the .md files directly.

### 2b. PyMuPDF text route (TEXT-HEAVY)

Adaptation note (2026-07-28 source cleanup): this route previously used a third-party PDF-to-markdown extractor. PyMuPDF is now the sole PDF text extractor, so this route uses the same full text+table extraction shown in the Fallback route below (2d): what was a fallback for that extractor's failures is now the primary implementation.

```python
import pymupdf

doc = pymupdf.open(str(file_path))
md_parts = []

for page_num in range(len(doc)):
    page = doc[page_num]
    md_parts.append(f"## Page {page_num + 1}\n\n")

    tables = page.find_tables()
    if tables.tables:
        for tab in tables.tables:
            rows = tab.extract()
            if rows:
                header = rows[0]
                md_parts.append("| " + " | ".join(str(c) if c else "" for c in header) + " |\n")
                md_parts.append("| " + " | ".join("---" for _ in header) + " |\n")
                for row in rows[1:]:
                    md_parts.append("| " + " | ".join(str(c) if c else "" for c in row) + " |\n")
                md_parts.append("\n")

    text = page.get_text("text")
    md_parts.append(text + "\n")

doc.close()
md = "\n".join(md_parts)
```

Output: markdown with tables, page anchors, and body text. Zero tokens consumed.

### 2c. Smart MIXED route (MIXED)

This is the primary route for documents with both text and images. It maximizes free text extraction via PyMuPDF and uses Read tool only where images carry information not captured in text.

1. Run PyMuPDF text+table extraction on the full document (get text + tables — zero tokens)
2. Identify **visual-dominant pages** from pre-analysis: `image_heavy_pages` (pages with >= 3 images AND < 150 words)
3. For those pages only, convert to PNG and use Read tool:
   
   ```python
   import pymupdf
   doc = pymupdf.open(str(file_path))
   page = doc[page_num]
   pix = page.get_pixmap(dpi=150)
   pix.save(f"_temp_page_{page_num}.png")
   ```

4. Read the PNG with Claude's native Read tool (multimodal vision)

5. Instruction for image description: describe every image, chart, graph, and diagram in detail. Include:
   
   - Type (bar chart, pie chart, line graph, table, photo, logo, diagram)
   - Content (what it shows: axes, labels, categories)
   - Values (numerical data points if readable)
   - Trends (increasing, decreasing, stable)
   - Legends (color coding, series names)

6. Merge: replace PyMuPDF text for visual-dominant pages with Read tool descriptions

### 2d. Fallback route

Adaptation note (2026-07-28 source cleanup): this section previously documented the fallback used when the prior third-party extractor raised an exception. It is retained as the reference implementation for PyMuPDF's own text+table extraction (now shared by 2b and 2c above), and still applies verbatim if PyMuPDF itself raises an exception on a specific PDF:

```python
import pymupdf

doc = pymupdf.open(str(file_path))
md_parts = []

for page_num in range(len(doc)):
    page = doc[page_num]
    md_parts.append(f"## Page {page_num + 1}\n\n")

    # Tables
    tables = page.find_tables()
    if tables.tables:
        for tab in tables.tables:
            rows = tab.extract()
            # Format as markdown table
            if rows:
                header = rows[0]
                md_parts.append("| " + " | ".join(str(c) if c else "" for c in header) + " |\n")
                md_parts.append("| " + " | ".join("---" for _ in header) + " |\n")
                for row in rows[1:]:
                    md_parts.append("| " + " | ".join(str(c) if c else "" for c in row) + " |\n")
                md_parts.append("\n")

    # Text
    text = page.get_text("text")
    md_parts.append(text + "\n")

    # Images (detect only, cannot describe without Read tool)
    images = page.get_images()
    if images:
        md_parts.append(f"\n[{len(images)} image(s) detected on this page - use Read tool for descriptions]\n\n")

doc.close()
md = "\n".join(md_parts)
```

### 2e. DOCX extraction

```python
from docx import Document

doc = Document(str(file_path))
md_parts = []

for para in doc.paragraphs:
    if para.style.name.startswith("Heading"):
        level = int(para.style.name[-1]) if para.style.name[-1].isdigit() else 2
        md_parts.append(f"{'#' * level} {para.text}\n\n")
    elif para.text.strip():
        md_parts.append(f"{para.text}\n\n")

for table in doc.tables:
    rows = []
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
        rows.append(cells)
    if rows:
        md_parts.append("| " + " | ".join(rows[0]) + " |\n")
        md_parts.append("| " + " | ".join("---" for _ in rows[0]) + " |\n")
        for row in rows[1:]:
            md_parts.append("| " + " | ".join(row) + " |\n")
        md_parts.append("\n")

md = "\n".join(md_parts)
```

### 2f. PPTX extraction

```python
from pptx import Presentation

prs = Presentation(str(file_path))
md_parts = []

for slide_num, slide in enumerate(prs.slides, 1):
    md_parts.append(f"## Slide {slide_num}\n\n")

    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                if para.text.strip():
                    md_parts.append(f"{para.text}\n\n")
        if shape.has_table:
            table = shape.table
            rows = []
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                rows.append(cells)
            if rows:
                md_parts.append("| " + " | ".join(rows[0]) + " |\n")
                md_parts.append("| " + " | ".join("---" for _ in rows[0]) + " |\n")
                for row in rows[1:]:
                    md_parts.append("| " + " | ".join(row) + " |\n")
                md_parts.append("\n")

    # Speaker notes
    if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
        notes = slide.notes_slide.notes_text_frame.text.strip()
        if notes:
            md_parts.append(f"**Speaker notes**: {notes}\n\n")

md = "\n".join(md_parts)
```

### Output format (.md files)

Every generated .md file starts with a metadata header:

```markdown
# [Original filename]
<!-- Parsed: [ISO date] | Extractor: [pymupdf/read_tool/python-docx/python-pptx] | Pages: [N] | Words: [N] | Classification: [TEXT-HEAVY/IMAGE-HEAVY/MIXED/SCANNED/N/A] -->
<!-- Source: [full original path] -->

## Page 1
[Content...]
```

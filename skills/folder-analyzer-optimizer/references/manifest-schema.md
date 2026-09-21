# Manifest Schema
<!-- Loaded on demand by SKILL.md Step 3 -->

## Step 3: Manifest management

The manifest file `_parsed/_parse_manifest.json` is the single source of truth for parsing state. It tracks every file, its status, extractor used, classification, and cache metadata.

### Manifest schema

See `examples/sample_manifest.json` for a complete example.

Key fields per file entry:

| Field                    | Type   | Description                                                                                  |
| ------------------------ | ------ | -------------------------------------------------------------------------------------------- |
| `source_path`            | string | Full absolute path to source file                                                            |
| `output_path`            | string | Relative path to generated .md file                                                          |
| `mtime`                  | float  | `os.path.getmtime()` of source at parse time                                                 |
| `parsed_at`              | string | ISO 8601 timestamp                                                                           |
| `page_count`             | int    | Number of pages (PDF/PPTX) or sections (DOCX)                                                |
| `word_count`             | int    | Total word count in generated .md                                                            |
| `status`                 | string | OK, PARTIAL, FAILED, SKIP_EXCEL, SKIP_IMAGE, SKIP_LEGACY_FORMAT, SKIP_UNSUPPORTED            |
| `extractor`              | string | pymupdf, pymupdf+read_tool, read_tool_vision, python_docx, python_pptx                        |
| `routing_classification` | string | SCANNED, TEXT-HEAVY, MIXED, N/A                                                              |
| `preanalysis`            | object | Pre-analysis metrics (total_images, avg_images_per_page, avg_words_per_page)                 |
| `error`                  | string | Error message if status=FAILED                                                               |
| `tree_status`            | string | OK, DEGRADED, FORCED_CHUNKED, SKIPPED_TOO_SHORT, SKIPPED_NO_STRUCTURE, SKIPPED_LOW_QUALITY, SKIPPED_DISABLED, FAILED. Absence = legacy entry (triggers lazy upgrade) |
| `tree_path`              | string | Relative path to the `.tree.json` sidecar, or null if no tree was generated                  |
| `tree_generated_at`      | string | ISO 8601 timestamp of the last tree generation, or null                                      |

### Crash resilience

Save the manifest after EACH file is parsed. If the process is interrupted, already-parsed files are cached and will not be re-parsed on next run.

### Cache invalidation

```python
import os, json

manifest_path = os.path.join(output_root, "_parse_manifest.json")
manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {"files": {}}

for file_key, entry in manifest["files"].items():
    current_mtime = os.path.getmtime(entry["source_path"])
    if current_mtime == entry["mtime"]:
        # File unchanged, skip parsing
        continue
    else:
        # File modified, re-parse
        pass
```

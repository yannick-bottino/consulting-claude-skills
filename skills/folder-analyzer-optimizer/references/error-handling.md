# Error Handling
<!-- Loaded on demand by SKILL.md -->

## Error handling

| Error                                           | Impact    | Action                                                              |
| ----------------------------------------------- | --------- | ------------------------------------------------------------------- |
| PyMuPDF extraction exception on a specific page | One file  | Log partial result for that page, continue with remaining pages. Do NOT mark as FAILED |
| PyMuPDF cannot open file (encrypted, corrupted) | One file  | Log as FAILED in manifest with error message. Continue to next file |
| Read tool fails on a PNG page                   | One page  | Log warning. Use PyMuPDF text for that page instead                 |
| python-docx/pptx exception                      | One file  | Log as FAILED in manifest. Continue                                 |
| pip install fails                               | All files | Stop and ask user to install manually                               |
| Disk full                                       | All files | Stop with clear error message                                       |
| File locked (OneDrive/SharePoint)               | One file  | Log as FAILED with "file locked" message. Suggest closing the file  |
| `pymupdf.get_toc()` exception                   | One file (tree) | Fallback to markdown regex headings. Continue                      |
| Markdown regex headings illisibles              | One file (tree) | Mark `tree_status = SKIPPED_NO_STRUCTURE`. Continue                  |
| Écriture `.tree.json` échoue (disque, lock)     | One file (tree) | Mark `tree_status = FAILED` with error message. Continue             |
| `.md` source manquant pour build_tree           | One file (tree) | Mark `tree_status = FAILED`. Log warning. Continue                   |
| Heading title vide / unicode invalide           | One node        | Use `title = "(untitled section {node_id})"`                         |
| `start_page > page_count`                       | One node        | Clamp to `page_count`. Log warning                                   |

**Principle**: Never let a single file failure block the entire pipeline. Log the error, continue, report at the end.

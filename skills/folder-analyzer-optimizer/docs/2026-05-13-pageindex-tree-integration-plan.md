# PageIndex Tree Integration Implementation Plan (superseded)

**Removed 2026-07-28** as part of the EQ_LIB source cleanup ahead of vendoring this skill into the ESG DD plugin.

This implementation plan (2026-05-13) walked through building `scripts/tree_builder.py` and its tests task-by-task. Several tasks and code samples referenced the third-party PDF extractor in use at the time (e.g. the heading-extraction function, then named after it), which has since been replaced by PyMuPDF (2026-07-28 source cleanup, phase-2 Arbitrage 4): the function is now `extract_headings_markdown_regex`. Rather than rewrite dozens of task descriptions and code blocks to retroactively claim a different tool was used (which would fabricate the historical record), the content has been removed. The shipped result of this plan is preserved verbatim in `scripts/tree_builder.py`, `tests/test_tree_builder.py`, and `references/tree-builder.md`.

Full original content remains available in the EQ_LIB git history for this folder (see `git log -- folder-analyzer-optimizer/docs`).

Audit the provided Markdown for accessibility and usability issues.

Return a JSON list:
- issue_type (heading_hierarchy, link_text, missing_alt_text, pdf_only, long_paragraphs, ambiguous_instructions)
- severity (low/med/high)
- location (quote the problematic snippet)
- fix (specific edit instruction)

Do not rewrite the whole page; produce actionable fixes.

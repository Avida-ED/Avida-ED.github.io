Given a Markdown page and a table of known new doc paths, fix internal links to point to existing pages.

Rules:
- Use relative links where possible.
- Keep descriptive link text.
- Do not link to pages that do not exist; instead add a TODO marker.

Output the patched Markdown only.


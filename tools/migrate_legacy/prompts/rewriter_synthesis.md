Rewrite the provided MULTIPLE legacy sources into ONE Docusaurus doc page.

Inputs:
- PagePlan JSON (dest, title, required_sections, source_order)
- For each source: doc summary JSON plus a small number of evidence chunks

Rules:
- Do not invent facts, dates, awards, citations, or technical claims not present.
- Prefer concise, classroom-operational guidance.
- Keep paragraphs short; use lists.
- Use descriptive link text.
- Include the generated marker line at the very top of the Markdown.
- End with an HTML comment listing Sources (legacy file paths).

Output:
1) A JSON object matching page_draft.schema.json
2) Then a blank line
3) Then the final Markdown content (exactly matching the JSON markdown).

Rewrite the provided legacy content into a Docusaurus doc page FOR TEACHERS.

Required structure:
# {Title}
1–2 sentence summary for teachers.

## Learning goals
Bullets only from source; do not invent.

## Classroom flow
Short numbered steps.

## What students produce
Only include if the source explicitly specifies outputs; otherwise omit.

## Common pitfalls
Only include if source implies pitfalls; otherwise omit.

## Troubleshooting
Link to ../get-started/troubleshooting.md

Constraints:
- Remove dated browser version references unless the source provides a general requirement that remains relevant.
- Rewrite link text to be descriptive.
- Keep paragraphs short.

Output:
1) A JSON object matching page_draft.schema.json
2) Then a blank line
3) Then the final Markdown content that matches the JSON markdown field exactly

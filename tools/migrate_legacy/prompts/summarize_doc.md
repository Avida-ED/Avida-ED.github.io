You will be given multiple chunk summaries (JSON) from one legacy document.

Task:
- Produce a single compact document summary suitable for planning and rewriting.

Hard rules:
- Do not invent facts.
- Consolidate duplicates.
- Identify if this document is primarily: teachers, students, support, about, announcement, or unknown.

Output JSON only:
{
  "doc_title_guess": "...",
  "audience": "teachers|students|general|unknown",
  "content_type": "how_to|lesson|faq|announcement|about|support|unknown",
  "best_use": "suggest where this belongs in the new IA",
  "key_points": ["..."],
  "still_relevant": ["..."],
  "likely_outdated": ["..."],
  "notable_links": ["..."]
}

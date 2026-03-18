{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ChunkSummary",
  "type": "object",
  "required": ["key_points", "audience", "content_type", "notable_links", "outdated_signals", "quotes_to_preserve"],
  "properties": {
    "key_points": { "type": "array", "items": { "type": "string" } },
    "audience": { "type": "string", "enum": ["teachers", "students", "general", "unknown"] },
    "content_type": {
      "type": "string",
      "enum": ["how_to", "lesson", "faq", "announcement", "about", "support", "unknown"]
    },
    "notable_links": { "type": "array", "items": { "type": "string" } },
    "outdated_signals": { "type": "array", "items": { "type": "string" } },
    "quotes_to_preserve": { "type": "array", "items": { "type": "string" } }
  },
  "additionalProperties": false
}


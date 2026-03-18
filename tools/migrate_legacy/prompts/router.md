Given: (1) site IA categories and destination paths, (2) extracted legacy text and metadata.
Task: classify and route this content into exactly one destination doc path.
Return JSON matching mapping.schema.json.

IA categories:
- get_started
- teachers
- students
- curriculum
- support
- about

Routing rules:
- Prefer teachers/students/get-started unless the content is purely institutional/history/citation.
- Do not create new categories.
- If content is outdated or purely news/announcements, route to support or archive bucket and flag for human review.

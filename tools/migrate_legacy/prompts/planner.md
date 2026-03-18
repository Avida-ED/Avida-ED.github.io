You are planning the migration of legacy website content into a fixed Docusaurus structure.

Task:
- Create a PagePlan for the specified page_type and destination.
- Select MULTIPLE relevant legacy source files from the provided candidate list.
- Provide source_order (most important first).
- Provide required_sections appropriate for the page_type.
- Provide link_intents for legacy internal refs that should become links to other new docs.

Hard rules:
- Only use provided candidate sources.
- Do not invent facts; plan only.
- Favor teacher/student usability and accessibility.
- If a candidate is an announcement/news item, generally avoid it unless it is still essential.

Return JSON only matching page_plan.schema.json.


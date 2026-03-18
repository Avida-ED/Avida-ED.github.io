# Legacy site migration tool (agentic, local LLM)

This tool migrates legacy Avida-ED site content into the new Docusaurus structure using:
- deterministic extraction (pandoc, pdftotext)
- a local LLM for routing + rewriting (Ollama, vLLM, or llamafile in OpenAI-compat mode)
- cache-backed calls for reproducibility

## Setup

From repo root:

```bash
cd tools/migrate_legacy
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


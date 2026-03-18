# Avida-ED Project Site (Docusaurus)

This repository contains the public Avida-ED project website built with Docusaurus.

## Local development

Prerequisites: Node.js 20+

```bash
npm ci
npm run start

Build

npm run build
npm run serve

Editing content

Most content is in docs/ as Markdown. Edit via GitHub web UI or a local editor and submit a pull request.
Deployment

The site deploys to GitHub Pages via .github/workflows/deploy.yml on pushes to main.
Accessibility

    Prefer HTML pages over PDFs.

    Provide alt text for meaningful images.

    Provide captions and transcripts for videos.

    PRs run an accessibility smoke test (pa11y) against key pages.


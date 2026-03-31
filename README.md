# Avida-ED-Test3

This repository is the current `Avida-ED-Test3` site prototype and migration
workspace. It uses Docusaurus as the site engine, but the site is being shaped
away from default Docusaurus "docs" presentation and toward a simpler public
website for learners and instructors.

The current site includes:

- a custom landing page with logo, overview video, and audience-first entry
  points
- public pages for app access, support, downloads, archive/news, and project
  background
- page-based curriculum content under `src/pages/curriculum/`
- student, support, and video content under `docs/`, including transcript-first
  migration work
- local scripts and process documents for media transcription and transcript
  publication

## Requirements

- Node.js 18+

## Install

```bash
npm install
```

## Build

```bash
npm run build
```

## Site structure

- `src/pages/`
  public site pages and the active page-based curriculum content
- `docs/`
  selected docs-rendered content, including student/support/video sections and
  a reduced instructor comparison example
- `static/`
  public assets copied directly into the built site
- `scripts/`
  local transcription and publication tooling plus process notes

## Transcript workflow

For media-to-transcript migration work, see
[scripts/README.md](/mnt/CIFS/pengolodh/Docs/Projects/genai/codex-projects/web-avida-ed-codex/Avida-ED-Test3/scripts/README.md).

The detailed remaining process document is at
[scripts/VIDEO_PROCESS.md](/mnt/CIFS/pengolodh/Docs/Projects/genai/codex-projects/web-avida-ed-codex/Avida-ED-Test3/scripts/VIDEO_PROCESS.md).

For repo promotion and GitHub setup steps, see
[REPO_PROMOTION_PROCESS.md](/mnt/CIFS/pengolodh/Docs/Projects/genai/codex-projects/web-avida-ed-codex/Avida-ED-Test3/REPO_PROMOTION_PROCESS.md).

## Hosting large assets

GitHub rejects files larger than 95 MB, so installers, videos, or archives that
exceed that limit should reside under `staging/` instead of `static/`. Document
each staging asset inside `staging/README.md`, noting the intended permanent
host (cloud storage, external archive, mirror repo, etc.) and which page(s) need
their URLs updated once the host is ready. After you publish the file at that
host, switch the content links from `staging/...` to the final location and
remove the staging copy so the repo stays within GitHub’s size limit.

The local workflow now has two stages:

- `scripts/transcribe_media.py` for media-to-draft transcript generation
- `scripts/publish_transcript.py` for promoting reviewed drafts into
  `docs/videos/`

## Repo process

For the repo promotion history and ongoing repo/process notes, see
[REPO_PROMOTION_PROCESS.md](/mnt/CIFS/pengolodh/Docs/Projects/genai/codex-projects/web-avida-ed-codex/Avida-ED-Test3/REPO_PROMOTION_PROCESS.md).

# Video Processing Workflow

This document describes the remaining process for turning Avida-ED video
material into published site content.

It is an internal workflow document for the migration work, not a public site
page.

## Goal

For each video that matters to students or instructors:

1. obtain a local media file
2. generate a draft transcript
3. review and correct the text
4. publish a transcript page into the site
5. link that page from the appropriate video, student, or support pages

## Directory conventions

Use these locations consistently inside `Avida-ED-Test3`:

- `transcripts/source-media/`
  Local copies of acquired video files that are being processed for transcript
  work. This is the preferred landing area when the source is not already
  present elsewhere in the repo.
- `transcripts/`
  Working directory for generated transcript drafts and optional normalized WAV
  files.
- `docs/videos/`
  Published transcript pages that are part of the site.

## What goes where

### Source media

Put newly acquired local video files in:

`Avida-ED-Test3/transcripts/source-media/`

Examples:

- `transcripts/source-media/project-overview.mp4`
- `transcripts/source-media/lab-bench-tutorial.mov`

If a video already exists elsewhere in the workspace, such as the scraped legacy
site under `../avida-ed-static-site-2024/...`, you can transcribe it directly
from there instead of copying it.

### Draft outputs

`transcribe_media.py` writes working files to `transcripts/` by default:

- `slug.txt`
- `slug.md`
- optionally `slug.wav`

These are working artifacts, not final published content.

### Published site pages

Final transcript pages belong in:

`Avida-ED-Test3/docs/videos/`

Examples:

- `docs/videos/intro-to-lab-bench.md`
- `docs/videos/project-overview.md`

## Step-by-step process

### 1. Acquire the source media

Use one of these approaches:

- transcribe directly from an existing local file in the scraped legacy site
- copy a newly obtained video into `transcripts/source-media/`
- export a hosted video to a local file and place it in `transcripts/source-media/`

Current known unresolved acquisition target:

- `Avida-ED Project Overview`
  Kaltura metadata is documented in `docs/videos/project-overview.md`, but the
  actual media file is not yet local.

### 2. Generate the draft transcript

Run:

```bash
python3 scripts/transcribe_media.py \
  transcripts/source-media/<video-file>.ext \
  --output-dir transcripts \
  --slug <slug> \
  --title "<Human Title>"
```

Example:

```bash
python3 scripts/transcribe_media.py \
  transcripts/source-media/project-overview.mp4 \
  --output-dir transcripts \
  --slug project-overview \
  --title "Avida-ED Project Overview"
```

If the source already exists elsewhere locally, you can point at that path
instead.

### 3. Review and correct the draft

Review the generated file in:

- `transcripts/<slug>.md`
  or
- `transcripts/<slug>.txt`

Correct:

- `Avida-ED` terminology
- names of interface areas
- obvious word recognition errors
- punctuation and line breaks where needed for readability

Do not try to make it read like marketing copy. Keep it a transcript, but make
it accurate and usable.

### 4. Publish the reviewed page

Run:

```bash
python3 scripts/publish_transcript.py \
  transcripts/<slug>.md \
  --slug <slug> \
  --title "<Human Title>" \
  --summary "<One-sentence summary>"
```

This writes:

- `docs/videos/<slug>.md`

The published page is the version that should be linked from the site.

### 5. Update site navigation

After publishing a transcript page:

- add or update the entry in `docs/videos/index.md`
- add links from student or support pages if the video is relevant there
- keep `sidebars.js` in sync if a new videos page should appear in the docs
  sidebar

Typical touchpoints:

- `docs/videos/index.md`
- `docs/students/videos.md`
- `docs/support/*.md`
- `sidebars.js`

### 6. Verify the site build

Run:

```bash
npm run build
```

Fix any broken links before treating the page as finished.

## Current completion state

### Done

- `Intro to Lab Bench`
  Published at `docs/videos/intro-to-lab-bench.md`

### Not done

- `Avida-ED Project Overview`
  Needs local media acquisition, transcript generation, review, publication,
  and final linking

## Working-file policy

The `transcripts/` tree is for working files, including:

- source media placed in `transcripts/source-media/`
- generated drafts
- optional normalized audio files

These should not be treated as public site content.

The repo still needs this `.gitignore` entry:

```gitignore
transcripts/
```

That line would cover both `transcripts/source-media/` and generated transcript
artifacts.

## Minimum checklist for each video

- local media file available
- draft transcript generated
- transcript reviewed by a human
- published page written to `docs/videos/`
- videos index updated
- relevant student/support links updated
- `npm run build` passes

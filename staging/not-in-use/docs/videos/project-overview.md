---
title: Avida-ED Project Overview Transcript
---

This page tracks the Avida-ED project overview video that is embedded on the
home page and appeared throughout the legacy site as a general introduction to
the software and its classroom purpose.

## Current status

A reviewed transcript is not available yet. The video is still important enough
to keep in the site structure because it serves as the broadest orientation
video for new visitors.

Until the source media is available for local transcription, this page serves
as the text-first record of what the video is for, where it appears, and how it
should be migrated.

## What this video is for

Use or reference this video when a visitor needs:

- a short orientation to what Avida-ED is
- a quick explanation of how the software supports evolution learning
- a general introduction before moving into student or instructor materials

The more task-specific video support should continue to live in tutorial pages
such as [Intro to Lab Bench](./intro-to-lab-bench.md).

## What should appear here later

When the media file is available and transcribed, this page should include:

- a reviewed transcript
- a short summary of the video's main teaching points
- terminology cleanup where the automatic transcript mishears Avida-ED terms
- notes if the narration reflects an older interface or earlier project framing

## Known source metadata

The local site consistently embeds this video through Kaltura with:

- `partner_id`: `811482`
- `uiconf_id`: `27551951`
- `entry_id`: `1_rdyd9cnv`

The same embedded player appears in the legacy site sidebar and on the current
home page implementation.

## Where the video is used

This overview video is used as broad orientation material rather than a lesson-
specific walkthrough. In the current redesign it is most relevant from:

- the home page
- student-facing launch guidance
- support and FAQ-style pages that need a quick project introduction

That means a transcript here helps both accessibility and site navigation,
because readers can learn what Avida-ED is without depending on the embedded
player.

## Interim text summary

Based on its repeated placement across the legacy site and the current home page
use, this video functions as the concise, general-purpose introduction to
Avida-ED. It should explain the software's role in teaching digital evolution,
orient new users to the project, and direct them toward more detailed student
and instructor materials.

## Planned follow-up

When the source media is available locally or through an approved acquisition
workflow, run the transcript pipeline below and replace this summary page with a
reviewed transcript.

## Transcript workflow once media is local

After a local copy of the video is obtained, use:

```bash
python3 scripts/transcribe_media.py /path/to/project-overview-video.ext \
  --output-dir transcripts \
  --slug project-overview \
  --title "Avida-ED Project Overview"
```

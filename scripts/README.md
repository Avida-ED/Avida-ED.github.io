# Transcript Scripts

`transcribe_media.py` extracts mono 16 kHz WAV audio with `ffmpeg`, runs the
local `whisperfile` speech-to-text engine, and writes:

- a plain text transcript
- a markdown transcript page

`publish_transcript.py` takes a reviewed transcript draft and promotes it into
`docs/videos/` as a site page with a consistent transcript-first layout.

For the full remaining process, local file placement, and per-video checklist,
see [VIDEO_PROCESS.md](/mnt/CIFS/pengolodh/Docs/Projects/genai/codex-projects/web-avida-ed-codex/Avida-ED-Test3/scripts/VIDEO_PROCESS.md).

Default dependencies expected on this machine:

- `ffmpeg`
- `/home/netuser/bin/whisperfile`
- `/home/netuser/programs/AGiXT/models/whispercpp/ggml-base.en.bin`

Example:

```bash
python3 scripts/transcribe_media.py \
  ../avida-ed-static-site-2024/avida-ed.msu.edu/html/files/curricula/tutorials/GUI_Intro_full_test14_050123.mov \
  --output-dir transcripts \
  --slug intro-to-lab-bench \
  --title "Intro to Lab Bench"
```

Outputs go into the chosen output directory. By default the intermediate WAV
file is deleted unless `--keep-wav` is passed.

## Publish reviewed transcript pages

After reviewing and correcting a transcript draft in `transcripts/`, publish it
into the site with:

```bash
python3 scripts/publish_transcript.py \
  transcripts/intro-to-lab-bench.md \
  --slug intro-to-lab-bench \
  --title "Intro to Lab Bench" \
  --summary "Introductory walkthrough of the Avida-ED 4 lab bench interface."
```

This writes a page under `docs/videos/`. The helper accepts either a reviewed
`.md` draft from `transcribe_media.py` or a plain `.txt` transcript.

## Recommended workflow

1. Run `transcribe_media.py` on a local video file.
2. Review and correct the generated text in `transcripts/`.
3. Run `publish_transcript.py` to create the public page in `docs/videos/`.
4. Link the new page from `docs/videos/index.md` and any relevant student or
   support pages.

## Current Avida-ED video targets

- `Intro to Lab Bench`
  Source media is already local in the scraped legacy site and has been used to
  generate the first published transcript.
- `Avida-ED Project Overview`
  The site has the Kaltura embed metadata locally, but not the media file
  itself. Known identifiers:
  - `partner_id=811482`
  - `uiconf_id=27551951`
  - `entry_id=1_rdyd9cnv`

Once the source media is downloaded or exported locally, it can be processed
with the same `transcribe_media.py` workflow and then published with
`publish_transcript.py`.

## Repo note

The local working directory `transcripts/` is intended for generated
intermediate artifacts and should be ignored by git. The repository currently
needs this `.gitignore` addition:

```gitignore
transcripts/
```

That change was identified during transcript migration work but could not be
written automatically in the current checkout.

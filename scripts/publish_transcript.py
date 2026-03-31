#!/usr/bin/env python3
"""
Promote a reviewed transcript draft into docs/videos/.

This script is intended for the second stage of the local video workflow:
1. transcribe media into transcripts/
2. review and correct the draft text
3. publish a cleaned page into docs/videos/
"""

from __future__ import annotations

import argparse
import pathlib
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish a reviewed transcript into docs/videos/."
    )
    parser.add_argument(
        "input",
        type=pathlib.Path,
        help="Reviewed transcript source (.md or .txt)",
    )
    parser.add_argument(
        "--slug",
        required=True,
        help="Output slug under docs/videos/",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Page title without the trailing 'Transcript'",
    )
    parser.add_argument(
        "--summary",
        default="",
        help="Optional short summary sentence for the page",
    )
    parser.add_argument(
        "--status-note",
        default=(
            "This transcript was generated locally and then reviewed for obvious "
            "Avida-ED terminology and clarity."
        ),
        help="Short status note shown near the top of the published page",
    )
    parser.add_argument(
        "--source-note",
        default="This transcript corresponds to a published Avida-ED support video.",
        help="Short source note shown above the transcript body",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=pathlib.Path("docs/videos"),
        help="Destination directory for published video pages",
    )
    return parser.parse_args()


def read_transcript_text(path: pathlib.Path) -> str:
    if not path.exists():
        raise SystemExit(f"Input file does not exist: {path}")

    text = path.read_text(encoding="utf-8").strip()
    if path.suffix.lower() != ".md":
        return text

    lines = text.splitlines()
    idx = 0
    if lines and lines[0].strip() == "---":
        idx = 1
        while idx < len(lines) and lines[idx].strip() != "---":
            idx += 1
        if idx < len(lines):
            idx += 1

    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    if idx < len(lines) and lines[idx].startswith("# "):
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    if idx < len(lines) and lines[idx].strip() == "## Transcript":
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    transcript = "\n".join(lines[idx:]).strip()
    if not transcript:
        raise SystemExit(f"No transcript body found in: {path}")
    return transcript


def build_page(
    title: str,
    summary: str,
    status_note: str,
    source_note: str,
    transcript: str,
) -> str:
    page_title = f"{title} Transcript"
    lines = [
        "---",
        f'title: "{page_title}"',
        "---",
        "",
        f"This page is the transcript home for the Avida-ED video \"{title}.\"",
        "",
    ]

    if summary:
        lines.extend(
            [
                "## Summary",
                "",
                summary.strip(),
                "",
            ]
        )

    lines.extend(
        [
            "## Status",
            "",
            status_note.strip(),
            "",
            "## Transcript",
            "",
            source_note.strip(),
            "",
            transcript.rstrip(),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    transcript = read_transcript_text(args.input)

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{args.slug}.md"

    page = build_page(
        title=args.title,
        summary=args.summary,
        status_note=args.status_note,
        source_note=args.source_note,
        transcript=transcript,
    )
    output_path.write_text(page, encoding="utf-8")
    print(f"Wrote published transcript page: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

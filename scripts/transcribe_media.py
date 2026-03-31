#!/usr/bin/env python3
"""
Extract audio from media and create transcript outputs with whisperfile.

Default model path points at a local English Whisper model already present on
this machine. Outputs:
  - normalized wav file
  - plain text transcript
  - markdown transcript page
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys


DEFAULT_MODEL = pathlib.Path(
    "/home/netuser/programs/AGiXT/models/whispercpp/ggml-base.en.bin"
)
DEFAULT_WHISPERFILE = pathlib.Path("/home/netuser/bin/whisperfile")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract audio from media and transcribe it with whisperfile."
    )
    parser.add_argument("input", type=pathlib.Path, help="Input media file")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=pathlib.Path,
        default=pathlib.Path("transcripts"),
        help="Directory for generated outputs",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Optional human-readable title for the markdown transcript",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="Optional output slug; defaults to the input filename stem",
    )
    parser.add_argument(
        "--model",
        type=pathlib.Path,
        default=DEFAULT_MODEL,
        help=f"Whisper model path (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--whisperfile",
        type=pathlib.Path,
        default=DEFAULT_WHISPERFILE,
        help=f"whisperfile binary path (default: {DEFAULT_WHISPERFILE})",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=8,
        help="Number of threads for whisperfile",
    )
    parser.add_argument(
        "--keep-wav",
        action="store_true",
        help="Keep the intermediate normalized wav file",
    )
    return parser.parse_args()


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required command not found on PATH: {name}")


def run_command(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def transcribe(args: argparse.Namespace) -> int:
    if not args.input.exists():
        raise SystemExit(f"Input file does not exist: {args.input}")
    if not args.model.exists():
        raise SystemExit(f"Whisper model does not exist: {args.model}")
    if not args.whisperfile.exists():
        raise SystemExit(f"whisperfile binary does not exist: {args.whisperfile}")

    require_command("ffmpeg")

    slug = args.slug or args.input.stem
    title = args.title or slug.replace("-", " ").replace("_", " ").title()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    wav_path = output_dir / f"{slug}.wav"
    txt_path = output_dir / f"{slug}.txt"
    md_path = output_dir / f"{slug}.md"

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(args.input),
        "-ar",
        "16000",
        "-ac",
        "1",
        str(wav_path),
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    whisper_cmd = [
        str(args.whisperfile),
        "-m",
        str(args.model),
        "-f",
        str(wav_path),
        "-t",
        str(args.threads),
        "-np",
    ]
    whisper_result = run_command(whisper_cmd)
    transcript = whisper_result.stdout.strip()

    txt_path.write_text(transcript + "\n", encoding="utf-8")

    md_lines = [
        "---",
        f'title: "{title}"',
        f"source_media: {args.input}",
        f"source_audio: {wav_path.name}",
        "generated_by: scripts/transcribe_media.py",
        "---",
        "",
        f"# {title}",
        "",
        "## Transcript",
        "",
        transcript,
        "",
    ]
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    if not args.keep_wav:
        wav_path.unlink(missing_ok=True)

    print(f"Wrote transcript text: {txt_path}")
    print(f"Wrote transcript markdown: {md_path}")
    if args.keep_wav:
        print(f"Kept normalized audio: {wav_path}")
    return 0


def main() -> int:
    args = parse_args()
    return transcribe(args)


if __name__ == "__main__":
    sys.exit(main())

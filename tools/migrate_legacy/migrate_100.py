#!/usr/bin/env python3
"""
tools/migrate_legacy/migrate.py

A deterministic, cache-backed pipeline to migrate legacy site content into a
Docusaurus repo structure using a local LLM (Ollama or OpenAI-compatible servers).

Usage examples:
  python tools/migrate_legacy/migrate.py run --dry-run
  python tools/migrate_legacy/migrate.py inventory
  python tools/migrate_legacy/migrate.py extract
  python tools/migrate_legacy/migrate.py map --max-items 30
  python tools/migrate_legacy/migrate.py draft --max-items 30
  python tools/migrate_legacy/migrate.py apply --dry-run=false
  python tools/migrate_legacy/migrate.py qa
"""

from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
import yaml
from jsonschema import validate as jsonschema_validate

HERE = Path(__file__).resolve().parent


# ----------------------------
# Utilities
# ----------------------------

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_text(s: str) -> str:
    return sha256_bytes(s.encode("utf-8", errors="replace"))

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")

def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def run_cmd(cmd: List[str], cwd: Optional[Path] = None, timeout: int = 300) -> Tuple[int, str, str]:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout, proc.stderr


# ----------------------------
# Config / Data structures
# ----------------------------

@dataclasses.dataclass
class AppConfig:
    project_root: Path
    legacy_root: Path
    target_repo_root: Path
    output_dir: Path
    cache_dir: Path
    docs_root: Path
    static_img_root: Path
    allowed_dest_prefixes: List[str]
    include_globs: List[str]
    exclude_globs: List[str]
    tools: Dict[str, str]
    llm: Dict[str, Any]
    pipeline: Dict[str, Any]
    first_wave: Dict[str, Any]

def load_config(config_path: Path) -> AppConfig:
    raw = yaml.safe_load(read_text(config_path))
    project_root = (config_path.parent / raw["project_root"]).resolve()
    legacy_root = (config_path.parent / raw["legacy_root"]).resolve()
    target_repo_root = (config_path.parent / raw["target_repo_root"]).resolve()

    output_dir = (config_path.parent / raw["output_dir"]).resolve()
    cache_dir = (config_path.parent / raw["cache_dir"]).resolve()

    docs_root = target_repo_root / raw["docs_root"]
    static_img_root = target_repo_root / raw["static_img_root"]

    return AppConfig(
        project_root=project_root,
        legacy_root=legacy_root,
        target_repo_root=target_repo_root,
        output_dir=output_dir,
        cache_dir=cache_dir,
        docs_root=docs_root,
        static_img_root=static_img_root,
        allowed_dest_prefixes=raw["allowed_dest_prefixes"],
        include_globs=raw["include_globs"],
        exclude_globs=raw["exclude_globs"],
        tools=raw["tools"],
        llm=raw["llm"],
        pipeline=raw["pipeline"],
        first_wave=raw["first_wave"],
    )

@dataclasses.dataclass
class InventoryItem:
    path: str
    relpath: str
    ext: str
    size_bytes: int
    mtime: float

@dataclasses.dataclass
class ExtractedItem:
    source_relpath: str
    extracted_relpath: str
    text_hash: str
    title_guess: str
    links: List[str]


# ----------------------------
# File discovery
# ----------------------------

def should_exclude(relpath: str, exclude_globs: List[str]) -> bool:
    for pat in exclude_globs:
        if fnmatch.fnmatch(relpath, pat):
            return True
    return False

def matches_include(relpath: str, include_globs: List[str]) -> bool:
    for pat in include_globs:
        if fnmatch.fnmatch(relpath, pat):
            return True
    return False

def inventory_legacy(cfg: AppConfig, max_items: int = 0) -> List[InventoryItem]:
    items: List[InventoryItem] = []
    root = cfg.legacy_root
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            p = Path(dirpath) / fn
            rel = str(p.relative_to(root)).replace("\\", "/")
            if should_exclude(rel, cfg.exclude_globs):
                continue
            if not matches_include(rel, cfg.include_globs):
                continue
            st = p.stat()
            items.append(InventoryItem(
                path=str(p),
                relpath=rel,
                ext=p.suffix.lower(),
                size_bytes=st.st_size,
                mtime=st.st_mtime,
            ))
            if max_items and len(items) >= max_items:
                return items
    return items


# ----------------------------
# Extraction
# ----------------------------

def guess_title_from_text(text: str, fallback: str) -> str:
    # very simple: first markdown-ish heading or first non-empty line
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            return s.lstrip("#").strip()[:120] or fallback
        # HTML title might survive pandoc; also accept plain text
        return s[:120]
    return fallback

_LINK_RE = re.compile(r"https?://[^\s\)]+", re.IGNORECASE)

def extract_links(text: str) -> List[str]:
    return sorted(set(_LINK_RE.findall(text)))

def pandoc_to_markdown(cfg: AppConfig, src: Path, dest: Path) -> str:
    # Convert to Markdown. Use --wrap=none to preserve layout.
    cmd = [
        cfg.tools["pandoc"],
        str(src),
        "-t", "gfm",
        "--wrap=none",
        "--extract-media", str(dest.parent / "media"),
    ]
    rc, out, err = run_cmd(cmd, cwd=cfg.legacy_root, timeout=300)
    if rc != 0:
        raise RuntimeError(f"pandoc failed ({rc}) for {src}:\n{err}")
    return out

def pdftotext_extract(cfg: AppConfig, src: Path) -> str:
    cmd = [cfg.tools["pdftotext"], "-layout", str(src), "-"]
    rc, out, err = run_cmd(cmd, cwd=cfg.legacy_root, timeout=300)
    if rc != 0:
        raise RuntimeError(f"pdftotext failed ({rc}) for {src}:\n{err}")
    return out

def extract_one(cfg: AppConfig, item: InventoryItem) -> ExtractedItem:
    src = cfg.legacy_root / item.relpath
    extracted_dir = cfg.output_dir / "extracted"
    extracted_path = extracted_dir / (item.relpath.replace("/", "__") + ".md")

    # cache key: source file hash + extractor version string
    data = src.read_bytes()
    src_hash = sha256_bytes(data)
    cache_key = sha256_text(f"extract:v1:{item.relpath}:{src_hash}")
    cache_file = cfg.cache_dir / "extract" / f"{cache_key}.json"

    if cache_file.exists():
        cached = json.loads(read_text(cache_file))
        return ExtractedItem(**cached)

    extracted_dir.mkdir(parents=True, exist_ok=True)
    extracted_path.parent.mkdir(parents=True, exist_ok=True)

    if item.ext in [".html", ".htm", ".docx", ".odt", ".rtf"]:
        md = pandoc_to_markdown(cfg, src, extracted_path)
    elif item.ext in [".md", ".txt"]:
        md = read_text(src)
    elif item.ext == ".pdf":
        md = pdftotext_extract(cfg, src)
    else:
        md = read_text(src)

    title_guess = guess_title_from_text(md, fallback=Path(item.relpath).stem)
    links = extract_links(md)
    text_hash = sha256_text(md)

    write_text(extracted_path, md)

    extracted_relpath = str(extracted_path.relative_to(cfg.output_dir)).replace("\\", "/")
    result = ExtractedItem(
        source_relpath=item.relpath,
        extracted_relpath=extracted_relpath,
        text_hash=text_hash,
        title_guess=title_guess,
        links=links,
    )

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    write_text(cache_file, json.dumps(dataclasses.asdict(result), indent=2))
    return result


# ----------------------------
# LLM Backends
# ----------------------------

class LLMClient:
    def chat(self, system: str, user: str, temperature: float, max_tokens: int, timeout_s: int) -> str:
        raise NotImplementedError

class OllamaClient(LLMClient):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def chat(self, system: str, user: str, temperature: float, max_tokens: int, timeout_s: int) -> str:
        # Ollama /api/chat
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "options": {
                "temperature": temperature,
                # Ollama uses num_predict
                "num_predict": max_tokens,
            },
            "stream": False,
        }
        r = requests.post(url, json=payload, timeout=timeout_s)
        r.raise_for_status()
        data = r.json()
        return data["message"]["content"]

class OpenAICompatClient(LLMClient):
    """
    For vLLM or llamafile running an OpenAI-compatible server:
      POST /v1/chat/completions
    """
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def chat(self, system: str, user: str, temperature: float, max_tokens: int, timeout_s: int) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        r = requests.post(url, headers=headers, json=payload, timeout=timeout_s)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]


def make_llm_client(cfg: AppConfig) -> LLMClient:
    llm = cfg.llm
    backend = llm["backend"]
    model = llm["model"]
    if backend == "ollama":
        return OllamaClient(llm["ollama_url"], model=model)
    if backend == "openai_compat":
        return OpenAICompatClient(llm["openai_compat_url"], api_key=llm["openai_compat_api_key"], model=model)
    raise ValueError(f"Unknown LLM backend: {backend}")


# ----------------------------
# Prompt loading and caching
# ----------------------------

def load_prompt(name: str) -> str:
    p = HERE / "prompts" / name
    if not p.exists():
        raise FileNotFoundError(p)
    return read_text(p)

def load_schema(name: str) -> Dict[str, Any]:
    p = HERE / "schemas" / name
    if not p.exists():
        raise FileNotFoundError(p)
    return json.loads(read_text(p))

def cached_llm_call(cfg: AppConfig, cache_namespace: str, key_material: str, call_fn) -> str:
    key = sha256_text(key_material)
    cache_file = cfg.cache_dir / "llm" / cache_namespace / f"{key}.txt"
    if cache_file.exists():
        return read_text(cache_file)
    out = call_fn()
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    write_text(cache_file, out)
    return out


# ----------------------------
# Mapping and drafting
# ----------------------------

def canonical_destinations(cfg: AppConfig) -> Dict[str, str]:
    # Flatten cfg.first_wave into a dict of page_type->dest
    fw = cfg.first_wave
    out: Dict[str, str] = {}
    out["get_started.index"] = fw["get_started"]["index"]
    out["get_started.choose_version"] = fw["get_started"]["choose_version"]
    out["get_started.system_requirements"] = fw["get_started"]["system_requirements"]
    out["get_started.first_experiment"] = fw["get_started"]["first_experiment"]
    out["get_started.troubleshooting"] = fw["get_started"]["troubleshooting"]
    out["teachers.index"] = fw["teachers"]["index"]
    out["teachers.quick_start"] = fw["teachers"]["quick_start"]
    out["students.index"] = fw["students"]["index"]
    out["students.first_steps"] = fw["students"]["first_steps"]
    out["support.index"] = fw["support"]["index"]
    out["support.accessibility"] = fw["support"]["accessibility"]
    out["about.index"] = fw["about"]["index"]
    out["about.how_to_cite"] = fw["about"]["how_to_cite"]
    return out

def validate_dest(cfg: AppConfig, dest: str) -> bool:
    # dest is repo-relative path
    for prefix in cfg.allowed_dest_prefixes:
        if dest.startswith(prefix):
            return True
    return False

def parse_first_json_object(text: str) -> Dict[str, Any]:
    """
    Extract the first JSON object from the LLM output robustly.
    Assumes the LLM returns a JSON object at the start or near the start.
    """
    # Try direct parse
    s = text.strip()
    if s.startswith("{"):
        # Find matching braces by simple stack
        depth = 0
        for i, ch in enumerate(s):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    obj = s[: i + 1]
                    return json.loads(obj)
    # Fallback: locate first '{'
    idx = s.find("{")
    if idx >= 0:
        return parse_first_json_object(s[idx:])
    raise ValueError("Could not find JSON object in LLM output")

def router_map_one(cfg: AppConfig, llm: LLMClient, extracted: ExtractedItem) -> Dict[str, Any]:
    sys_prompt = load_prompt("system.md")
    router_prompt = load_prompt("router.md")
    schema = load_schema("mapping.schema.json")

    canon = canonical_destinations(cfg)
    extracted_text = read_text(cfg.output_dir / extracted.extracted_relpath)

    user = (
        f"{router_prompt}\n\n"
        f"Canonical destinations (page_type -> dest path):\n{json.dumps(canon, indent=2)}\n\n"
        f"Legacy source path: {extracted.source_relpath}\n"
        f"Legacy title guess: {extracted.title_guess}\n\n"
        f"Extracted content:\n---\n{extracted_text[:20000]}\n---\n"
        f"Return JSON only."
    )

    key_material = f"router:v1:{cfg.llm['model']}:{sha256_text(sys_prompt)}:{sha256_text(router_prompt)}:{extracted.text_hash}"
    raw = cached_llm_call(cfg, "router", key_material, lambda: llm.chat(
        system=sys_prompt,
        user=user,
        temperature=cfg.llm["temperature"],
        max_tokens=min(cfg.llm["max_tokens"], 1200),
        timeout_s=cfg.llm["timeout_s"],
    ))

    obj = parse_first_json_object(raw)
    jsonschema_validate(instance=obj, schema=schema)

    # Enforce canonical dests unless archive.review
    if obj["page_type"] != "archive.review":
        if obj["page_type"] in canon:
            obj["dest"] = canon[obj["page_type"]]
        if not validate_dest(cfg, obj["dest"]):
            raise ValueError(f"Router produced invalid dest: {obj['dest']} for {extracted.source_relpath}")
    else:
        obj["dest"] = f"out/archive_review/{extracted.source_relpath.replace('/', '__')}.md"

    return obj

def rewriter_prompt_for_page_type(page_type: str) -> str:
    if page_type.startswith("get_started."):
        return "rewriter_get_started.md"
    if page_type.startswith("teachers."):
        return "rewriter_teacher.md"
    if page_type.startswith("students."):
        return "rewriter_student.md"
    if page_type.startswith("support."):
        return "rewriter_support.md"
    if page_type.startswith("about."):
        return "rewriter_about.md"
    return "rewriter_support.md"

def draft_one(cfg: AppConfig, llm: LLMClient, mapping: Dict[str, Any], extracted: ExtractedItem) -> Dict[str, Any]:
    sys_prompt = load_prompt("system.md")
    prompt_name = rewriter_prompt_for_page_type(mapping["page_type"])
    rw_prompt = load_prompt(prompt_name)
    schema = load_schema("page_draft.schema.json")

    extracted_text = read_text(cfg.output_dir / extracted.extracted_relpath)

    user = (
        f"{rw_prompt}\n\n"
        f"Destination path (repo-relative): {mapping['dest']}\n"
        f"Page type: {mapping['page_type']}\n"
        f"Legacy source: {extracted.source_relpath}\n"
        f"Legacy title guess: {extracted.title_guess}\n\n"
        f"Extracted content:\n---\n{extracted_text[:28000]}\n---\n"
        f"Return the JSON object first, then the exact Markdown."
    )

    key_material = (
        f"draft:v1:{cfg.llm['model']}:{mapping['page_type']}:"
        f"{sha256_text(sys_prompt)}:{sha256_text(rw_prompt)}:{extracted.text_hash}"
    )
    raw = cached_llm_call(cfg, "draft", key_material, lambda: llm.chat(
        system=sys_prompt,
        user=user,
        temperature=cfg.llm["temperature"],
        max_tokens=cfg.llm["max_tokens"],
        timeout_s=cfg.llm["timeout_s"],
    ))

    obj = parse_first_json_object(raw)
    jsonschema_validate(instance=obj, schema=schema)

    # Enforce dest and source_files
    obj["dest"] = mapping["dest"]
    if "source_files" not in obj or not obj["source_files"]:
        obj["source_files"] = [extracted.source_relpath]
    if extracted.source_relpath not in obj["source_files"]:
        obj["source_files"].append(extracted.source_relpath)

    # Ensure traceability comment exists
    if "<!-- Sources:" not in obj["markdown"]:
        sources = "; ".join(obj["source_files"])
        obj["markdown"] = obj["markdown"].rstrip() + f"\n\n<!-- Sources: {sources} -->\n"

    return obj


# ----------------------------
# Apply / write outputs
# ----------------------------

def ensure_frontmatter(md: str, title: str) -> str:
    # If it already has frontmatter, leave it.
    if md.lstrip().startswith("---"):
        return md
    fm = f"---\ntitle: {title}\n---\n\n"
    return fm + md

def write_draft_outputs(cfg: AppConfig, page_draft: Dict[str, Any]) -> Tuple[Path, Path]:
    drafts_dir = cfg.output_dir / "drafts"
    md_dir = cfg.output_dir / "rendered_markdown"

    dest_rel = page_draft["dest"].replace("/", "__")
    draft_json_path = drafts_dir / f"{dest_rel}.json"
    draft_md_path = md_dir / f"{dest_rel}.md"

    drafts_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)

    write_text(draft_json_path, json.dumps(page_draft, indent=2))
    write_text(draft_md_path, page_draft["markdown"])
    return draft_json_path, draft_md_path

def apply_to_repo(cfg: AppConfig, page_draft: Dict[str, Any], dry_run: bool, overwrite: bool) -> Path:
    dest = cfg.target_repo_root / page_draft["dest"]
    title = page_draft["frontmatter"]["title"]
    content = ensure_frontmatter(page_draft["markdown"], title=title)

    if dest.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {dest}")

    if dry_run:
        return dest

    write_text(dest, content)
    return dest


# ----------------------------
# QA
# ----------------------------

def run_qa(cfg: AppConfig) -> None:
    cmds = cfg.pipeline.get("qa_commands", [])
    for cmd in cmds:
        rc, out, err = run_cmd(cmd, cwd=cfg.target_repo_root, timeout=900)
        if rc != 0:
            raise RuntimeError(f"QA command failed: {cmd}\nSTDOUT:\n{out}\nSTDERR:\n{err}")


# ----------------------------
# Reporting
# ----------------------------

def write_report(cfg: AppConfig, inventory: List[InventoryItem], extracted: List[ExtractedItem],
                 mappings: List[Dict[str, Any]], drafts: List[Dict[str, Any]], notes: List[str]) -> Path:
    report_path = cfg.output_dir / "report.md"
    lines: List[str] = []
    lines.append(f"# Migration report\n")
    lines.append(f"- Generated: `{now_iso()}`\n")
    lines.append(f"- Legacy root: `{cfg.legacy_root}`\n")
    lines.append(f"- Target repo root: `{cfg.target_repo_root}`\n\n")

    lines.append("## Summary\n")
    lines.append(f"- Inventory items: **{len(inventory)}**\n")
    lines.append(f"- Extracted items: **{len(extracted)}**\n")
    lines.append(f"- Mapped items: **{len(mappings)}**\n")
    lines.append(f"- Drafted pages: **{len(drafts)}**\n\n")

    if notes:
        lines.append("## Notes / flags\n")
        for n in notes:
            lines.append(f"- {n}\n")
        lines.append("\n")

    # Show mapping table
    lines.append("## Mappings\n")
    lines.append("| legacy source | page_type | dest | confidence |\n")
    lines.append("|---|---|---|---:|\n")
    for m in mappings:
        lines.append(f"| `{m['source']}` | `{m['page_type']}` | `{m['dest']}` | {m['confidence']:.2f} |\n")
    lines.append("\n")

    write_text(report_path, "".join(lines))
    return report_path


# ----------------------------
# Main pipeline
# ----------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(HERE / "config.yaml"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_inv = sub.add_parser("inventory")
    p_inv.add_argument("--max-items", type=int, default=0)

    p_ext = sub.add_parser("extract")
    p_ext.add_argument("--max-items", type=int, default=0)

    p_map = sub.add_parser("map")
    p_map.add_argument("--max-items", type=int, default=0)

    p_draft = sub.add_parser("draft")
    p_draft.add_argument("--max-items", type=int, default=0)

    p_apply = sub.add_parser("apply")
    p_apply.add_argument("--dry-run", type=str, default="true")
    p_apply.add_argument("--overwrite", type=str, default="false")

    p_qa = sub.add_parser("qa")

    p_run = sub.add_parser("run")
    p_run.add_argument("--dry-run", type=str, default="true")
    p_run.add_argument("--max-items", type=int, default=0)
    p_run.add_argument("--overwrite", type=str, default="false")

    args = parser.parse_args()
    cfg = load_config(Path(args.config))

    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    cfg.cache_dir.mkdir(parents=True, exist_ok=True)

    max_items = getattr(args, "max_items", 0) or cfg.pipeline.get("max_items", 0) or 0

    # Load previous stage outputs if present
    inventory_path = cfg.output_dir / "inventory.jsonl"
    extracted_path = cfg.output_dir / "extracted_index.jsonl"
    mapping_path = cfg.output_dir / "mapping.jsonl"
    drafts_index_path = cfg.output_dir / "drafts_index.jsonl"

    notes: List[str] = []

    if args.cmd in ("inventory", "run"):
        inv = inventory_legacy(cfg, max_items=max_items)
        write_text(
            inventory_path,
            "\n".join(json.dumps(dataclasses.asdict(i)) for i in inv) + ("\n" if inv else "")
        )
    else:
        inv = [InventoryItem(**json.loads(line)) for line in read_text(inventory_path).splitlines() if line.strip()]

    if args.cmd in ("extract", "run"):
        extracted_items: List[ExtractedItem] = []
        for i in inv:
            try:
                extracted_items.append(extract_one(cfg, i))
            except Exception as e:
                notes.append(f"EXTRACT FAIL: {i.relpath}: {e}")
        write_text(
            extracted_path,
            "\n".join(json.dumps(dataclasses.asdict(ei)) for ei in extracted_items) + ("\n" if extracted_items else "")
        )
    else:
        extracted_items = [ExtractedItem(**json.loads(line)) for line in read_text(extracted_path).splitlines() if line.strip()]

    llm = make_llm_client(cfg)

    if args.cmd in ("map", "run"):
        schema = load_schema("mapping.schema.json")
        mappings: List[Dict[str, Any]] = []
        # naive: map each extracted item independently
        for ei in extracted_items[: max_items or len(extracted_items)]:
            try:
                m = router_map_one(cfg, llm, ei)
                jsonschema_validate(instance=m, schema=schema)
                mappings.append(m)
            except Exception as e:
                notes.append(f"MAP FAIL: {ei.source_relpath}: {e}")
        write_text(mapping_path, "\n".join(json.dumps(m) for m in mappings) + ("\n" if mappings else ""))
    else:
        mappings = [json.loads(line) for line in read_text(mapping_path).splitlines() if line.strip()]

    if args.cmd in ("draft", "run"):
        schema = load_schema("page_draft.schema.json")
        drafts: List[Dict[str, Any]] = []
        # join mapping with extracted by source_relpath
        extracted_by_src = {ei.source_relpath: ei for ei in extracted_items}
        for m in mappings[: max_items or len(mappings)]:
            src = m["source"]
            if src not in extracted_by_src:
                notes.append(f"DRAFT SKIP: missing extracted source: {src}")
                continue
            try:
                d = draft_one(cfg, llm, m, extracted_by_src[src])
                jsonschema_validate(instance=d, schema=schema)
                drafts.append(d)
                if cfg.pipeline.get("write_drafts_json", True) or cfg.pipeline.get("write_markdown", True):
                    write_draft_outputs(cfg, d)
            except Exception as e:
                notes.append(f"DRAFT FAIL: {src}: {e}")
        write_text(drafts_index_path, "\n".join(json.dumps(d) for d in drafts) + ("\n" if drafts else ""))
    else:
        drafts = [json.loads(line) for line in read_text(drafts_index_path).splitlines() if line.strip()]

    if args.cmd in ("apply", "run"):
        dry_run = (getattr(args, "dry_run", "true").lower() == "true")
        overwrite = (getattr(args, "overwrite", "false").lower() == "true")
        if args.cmd == "run":
            # default to dry-run unless user set otherwise
            dry_run = (args.dry_run.lower() == "true")

        applied: List[str] = []
        for d in drafts[: max_items or len(drafts)]:
            try:
                dest = apply_to_repo(cfg, d, dry_run=dry_run, overwrite=overwrite)
                applied.append(str(dest))
            except Exception as e:
                notes.append(f"APPLY FAIL: {d.get('dest')}: {e}")
        if dry_run:
            notes.append(f"Dry run: {len(applied)} pages would be written. No repo files modified.")
        else:
            notes.append(f"Wrote {len(applied)} pages into repo.")

        if cfg.pipeline.get("run_qa", False) and not dry_run:
            run_qa(cfg)

    if args.cmd == "qa":
        run_qa(cfg)

    # Always write a report at the end of any command (helps visibility)
    report = write_report(cfg, inv, extracted_items, mappings, drafts, notes)
    print(f"[ok] report: {report}")

if __name__ == "__main__":
    main()

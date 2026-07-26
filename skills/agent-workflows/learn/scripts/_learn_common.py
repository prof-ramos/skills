"""Shared helpers for the learn_*.py scripts.

Not a script itself (no CLI). Everything the learn_* tools have in common lives
here: the on-disk layout under .agents/learn/, atomic ID allocation, index.json
read/write, and a minimal frontmatter parser for learning-entry.md files.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

LEARN_DIRNAME = ".agents/learn"
INDEX_SCHEMA_VERSION = 1


def learn_dir(project_root: Path) -> Path:
    return project_root / LEARN_DIRNAME


def ensure_scaffold(project_root: Path) -> Path:
    """Create .agents/learn/ and its subdirectories + an empty index.json if missing.

    This is infrastructure for the learning system itself, not domain
    knowledge, so it does not require the approval gate described in SKILL.md.
    """
    base = learn_dir(project_root)
    for sub in ("learnings", "proposals", "history", "snapshots"):
        (base / sub).mkdir(parents=True, exist_ok=True)

    index_path = base / "index.json"
    if not index_path.exists():
        save_index(project_root, {"schema_version": INDEX_SCHEMA_VERSION, "learnings": []})

    counter_path = base / ".counter"
    if not counter_path.exists():
        counter_path.write_text("0\n", encoding="utf-8")

    return base


def load_index(project_root: Path) -> dict:
    ensure_scaffold(project_root)
    index_path = learn_dir(project_root) / "index.json"
    return json.loads(index_path.read_text(encoding="utf-8"))


def save_index(project_root: Path, data: dict) -> None:
    base = learn_dir(project_root)
    base.mkdir(parents=True, exist_ok=True)
    index_path = base / "index.json"
    tmp_path = index_path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp_path.replace(index_path)


def find_learning(index: dict, learning_id: str) -> dict | None:
    for entry in index.get("learnings", []):
        if entry.get("id") == learning_id:
            return entry
    return None


def next_id(project_root: Path) -> str:
    """Allocate the next LP-XXXXXX id via a locked counter file.

    IDs are monotonic but may have gaps (an id allocated for a candidate that
    is later dropped before being proposed is never reused) -- see
    references/id-and-versioning.md for why that trade-off is acceptable.
    """
    counter_path = ensure_scaffold(project_root) / ".counter"
    with counter_path.open("r+", encoding="utf-8") as fh:
        try:
            import fcntl

            fcntl.flock(fh, fcntl.LOCK_EX)
        except ImportError:
            pass  # non-POSIX platform: best-effort, not race-safe
        try:
            current = int(fh.read().strip() or "0")
            new_value = current + 1
            fh.seek(0)
            fh.write(str(new_value) + "\n")
            fh.truncate()
        finally:
            try:
                import fcntl

                fcntl.flock(fh, fcntl.LOCK_UN)
            except ImportError:
                pass
    return f"LP-{new_value:06d}"


def append_history(project_root: Path, event: dict) -> None:
    history_dir = ensure_scaffold(project_root) / "history"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_path = history_dir / f"{today}.jsonl"
    record = {"ts": datetime.now(timezone.utc).isoformat(), **event}
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


_FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def parse_learning_entry(text: str) -> tuple[dict, str]:
    """Parse a learning-entry.md file: (frontmatter dict, markdown body).

    Deliberately minimal (no external YAML dependency, per this repo's
    convention that scripts be self-contained). Supports scalars, quoted
    strings, and simple flow lists like `depends_on: [LP-000001, LP-000002]`.
    Anything more elaborate belongs in the markdown body, not the frontmatter.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("learning entry missing opening '---' frontmatter marker")

    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        raise ValueError("learning entry missing closing '---' frontmatter marker")

    data: dict = {}
    for line in lines[1:end]:
        match = _FRONTMATTER_KEY_RE.match(line)
        if not match:
            continue
        key, raw = match.groups()
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            data[key] = [item.strip().strip("\"'") for item in inner.split(",") if item.strip()]
        elif raw.lower() in {"null", "~", ""}:
            data[key] = None
        elif raw.lower() in {"true", "false"}:
            data[key] = raw.lower() == "true"
        else:
            data[key] = raw.strip("\"'")

    body = "\n".join(lines[end + 1 :])
    return data, body


_DIFF_BLOCK_RE = re.compile(r"```diff\n(.*?)\n```", re.DOTALL)


def extract_diff_block(body: str) -> str:
    match = _DIFF_BLOCK_RE.search(body)
    if not match:
        raise ValueError("no ```diff ... ``` block found in learning entry body")
    return match.group(1) + "\n"


def learning_path(project_root: Path, learning_id: str) -> Path:
    return learn_dir(project_root) / "learnings" / f"{learning_id}.md"


def snapshot_path(project_root: Path, learning_id: str) -> Path:
    return learn_dir(project_root) / "snapshots" / f"{learning_id}.pre.diff"


def resolve_target(project_root: Path, target_file: str) -> Path:
    """Resolve a learning's target_file to an absolute path.

    A leading "~" means global scope (e.g. ~/.codex/AGENTS.md); anything else
    is relative to the project root. This is scope semantics, not patch
    mechanics, which is why it lives here rather than in _learn_patch.py.
    """
    if target_file.startswith("~"):
        return Path(target_file).expanduser()
    return (project_root / target_file).resolve()

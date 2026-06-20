#!/usr/bin/env python3
"""PR Analyzer — parses git diffs and produces a structured change summary."""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


RISK_EXTENSIONS = {
    "high": {".sql", ".sh", ".bash", ".tf", ".yaml", ".yml", ".env", ".pem", ".key"},
    "medium": {".py", ".ts", ".js", ".go", ".rs", ".java", ".kt", ".swift"},
    "low": {".md", ".txt", ".json", ".toml", ".ini", ".css", ".html"},
}

SENSITIVE_PATTERNS = [
    (re.compile(r"(password|secret|token|api_?key|auth)\s*=\s*['\"][^'\"]+['\"]", re.I), "hardcoded secret"),
    (re.compile(r"(TODO|FIXME|HACK|XXX)\b", re.I), "unresolved marker"),
    (re.compile(r"eval\s*\(", re.I), "eval() usage"),
    (re.compile(r"exec\s*\(", re.I), "exec() usage"),
    (re.compile(r"subprocess\.call\([^)]*shell\s*=\s*True"), "shell=True injection risk"),
    (re.compile(r"console\.log|print\s*\(.*password|print\s*\(.*token", re.I), "credential logging"),
]


@dataclass
class FileStat:
    path: str
    additions: int = 0
    deletions: int = 0
    risk_level: str = "low"
    flags: list[str] = field(default_factory=list)


@dataclass
class PRSummary:
    base: str
    head: str
    total_files: int = 0
    total_additions: int = 0
    total_deletions: int = 0
    file_stats: list[FileStat] = field(default_factory=list)
    high_risk_files: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)


def run(cmd: list[str], cwd: Optional[str] = None) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"[warn] {' '.join(cmd)}: {result.stderr.strip()}", file=sys.stderr)
    return result.stdout


def classify_risk(path: str) -> str:
    ext = Path(path).suffix.lower()
    for level, exts in RISK_EXTENSIONS.items():
        if ext in exts:
            return level
    return "medium"


def scan_flags(diff_chunk: str) -> list[str]:
    found = []
    for pattern, label in SENSITIVE_PATTERNS:
        if pattern.search(diff_chunk):
            found.append(label)
    return found


def parse_diff(raw_diff: str) -> list[FileStat]:
    stats: list[FileStat] = []
    current: Optional[FileStat] = None
    chunk: list[str] = []

    for line in raw_diff.splitlines():
        if line.startswith("diff --git"):
            if current:
                current.flags = scan_flags("\n".join(chunk))
                stats.append(current)
            # extract b/ path
            m = re.search(r"b/(.+)$", line)
            path = m.group(1) if m else "unknown"
            current = FileStat(path=path, risk_level=classify_risk(path))
            chunk = []
        elif line.startswith("+") and not line.startswith("+++"):
            current and chunk.append(line[1:])
            if current:
                current.additions += 1
        elif line.startswith("-") and not line.startswith("---"):
            if current:
                current.deletions += 1

    if current:
        current.flags = scan_flags("\n".join(chunk))
        stats.append(current)

    return stats


def analyze(repo_path: str, base: str, head: str, output_format: str) -> PRSummary:
    summary = PRSummary(base=base, head=head)

    raw_diff = run(["git", "diff", f"{base}...{head}"], cwd=repo_path)
    file_stats = parse_diff(raw_diff)

    for fs in file_stats:
        summary.total_files += 1
        summary.total_additions += fs.additions
        summary.total_deletions += fs.deletions
        summary.file_stats.append(fs)
        if fs.risk_level == "high" or fs.flags:
            summary.high_risk_files.append(fs.path)
        summary.flags.extend(f"{fs.path}: {flag}" for flag in fs.flags)

    return summary


def print_report(s: PRSummary, fmt: str) -> None:
    if fmt == "json":
        import dataclasses
        print(json.dumps(dataclasses.asdict(s), indent=2))
        return

    print(f"\n{'='*60}")
    print(f"PR Analysis: {s.base}...{s.head}")
    print(f"{'='*60}")
    print(f"Files changed : {s.total_files}")
    print(f"Lines added   : {s.total_additions}")
    print(f"Lines removed : {s.total_deletions}")

    if s.high_risk_files:
        print(f"\n[!] High-risk files ({len(s.high_risk_files)}):")
        for f in s.high_risk_files:
            print(f"    - {f}")

    if s.flags:
        print(f"\n[!] Flags found ({len(s.flags)}):")
        for flag in s.flags:
            print(f"    - {flag}")

    print(f"\nFile breakdown:")
    for fs in sorted(s.file_stats, key=lambda x: x.additions + x.deletions, reverse=True)[:20]:
        indicator = {"high": "!!!", "medium": " ! ", "low": "   "}[fs.risk_level]
        print(f"  {indicator} +{fs.additions:-4} -{fs.deletions:-4}  {fs.path}")

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Analyze a PR diff for risk and statistics.")
    parser.add_argument("repo_path", nargs="?", default=".", help="Path to git repository")
    parser.add_argument("--base", default="main", help="Base branch/commit (default: main)")
    parser.add_argument("--head", default="HEAD", help="Head branch/commit (default: HEAD)")
    parser.add_argument("--format", choices=["text", "json"], default="text", dest="fmt")
    args = parser.parse_args()

    repo = os.path.abspath(args.repo_path)
    if not os.path.isdir(os.path.join(repo, ".git")):
        # walk up to find git root
        p = Path(repo)
        while p != p.parent:
            if (p / ".git").exists():
                repo = str(p)
                break
            p = p.parent
        else:
            print(f"Error: no git repository found at {repo}", file=sys.stderr)
            sys.exit(1)

    summary = analyze(repo, args.base, args.head, args.fmt)
    print_report(summary, args.fmt)


if __name__ == "__main__":
    main()

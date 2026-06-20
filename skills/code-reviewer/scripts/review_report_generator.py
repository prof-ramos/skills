#!/usr/bin/env python3
"""Review Report Generator — combines PR analysis and quality checks into a markdown review report."""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(cmd: list[str], cwd: str | None = None) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return r.stdout.strip()


def script_dir() -> Path:
    return Path(__file__).parent


def repo_root(path: str) -> str | None:
    p = Path(path)
    while p != p.parent:
        if (p / ".git").exists():
            return str(p)
        p = p.parent
    return None


# ── Data collection ───────────────────────────────────────────────────────────

def collect_pr_data(repo: str, base: str, head: str) -> dict:
    script = script_dir() / "pr_analyzer.py"
    result = subprocess.run(
        [sys.executable, str(script), repo, "--base", base, "--head", head, "--format", "json"],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


def collect_quality_data(path: str) -> dict:
    script = script_dir() / "code_quality_checker.py"
    result = subprocess.run(
        [sys.executable, str(script), path, "--format", "json", "--min-severity", "info"],
        capture_output=True, text=True,
    )
    if not result.stdout.strip():
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


def git_log(repo: str, base: str, head: str) -> list[dict]:
    raw = run(
        ["git", "log", f"{base}...{head}", "--pretty=format:%H|%s|%an|%ad", "--date=short"],
        cwd=repo,
    )
    commits = []
    for line in raw.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({"hash": parts[0][:8], "subject": parts[1], "author": parts[2], "date": parts[3]})
    return commits


def git_branch_name(repo: str) -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo)


# ── Markdown builder ──────────────────────────────────────────────────────────

SEVERITY_EMOJI = {"error": "🔴", "warning": "🟡", "info": "🔵"}


def build_report(
    repo: str,
    base: str,
    head: str,
    pr_data: dict,
    quality_data: dict,
    commits: list[dict],
    branch: str,
    title: str,
) -> str:
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []

    def h(level: int, text: str):
        lines.append(f"\n{'#' * level} {text}\n")

    def li(text: str, indent: int = 0):
        lines.append(f"{'  ' * indent}- {text}")

    def code(block: str, lang: str = ""):
        lines.append(f"```{lang}\n{block}\n```")

    # Header
    lines.append(f"# {title}")
    lines.append(f"\n_Generated {now}_  \n_Branch: `{branch}`_\n")

    # Summary table
    h(2, "Summary")
    pr_files = pr_data.get("total_files", "—")
    pr_add = pr_data.get("total_additions", "—")
    pr_del = pr_data.get("total_deletions", "—")
    q_errors = quality_data.get("summary", {}).get("errors", "—")
    q_warn = quality_data.get("summary", {}).get("warnings", "—")
    q_info = quality_data.get("summary", {}).get("infos", "—")
    q_files = quality_data.get("files_checked", "—")

    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Base → Head | `{base}` → `{head}` |")
    lines.append(f"| Files changed | {pr_files} |")
    lines.append(f"| Lines added | {pr_add} |")
    lines.append(f"| Lines removed | {pr_del} |")
    lines.append(f"| Files analyzed | {q_files} |")
    lines.append(f"| Errors | {q_errors} |")
    lines.append(f"| Warnings | {q_warn} |")
    lines.append(f"| Info | {q_info} |")

    # Commits
    if commits:
        h(2, "Commits")
        for c in commits:
            lines.append(f"- `{c['hash']}` {c['subject']} _{c['author']}, {c['date']}_")

    # High-risk files
    high_risk = pr_data.get("high_risk_files", [])
    if high_risk:
        h(2, "High-Risk Files")
        lines.append("> These files warrant extra scrutiny during review.\n")
        for f in high_risk:
            li(f"`{f}`")

    # PR flags
    pr_flags = pr_data.get("flags", [])
    if pr_flags:
        h(2, "PR Flags")
        lines.append("> Patterns detected in changed lines.\n")
        for flag in pr_flags:
            li(flag)

    # Quality issues
    issues = quality_data.get("issues", [])
    if issues:
        h(2, "Quality Issues")

        for sev in ("error", "warning", "info"):
            sev_issues = [i for i in issues if i.get("severity") == sev]
            if not sev_issues:
                continue
            emoji = SEVERITY_EMOJI.get(sev, "")
            h(3, f"{emoji} {sev.capitalize()}s ({len(sev_issues)})")
            for i in sev_issues:
                lines.append(f"- **{i['code']}** `{i['file']}:{i['line']}` — {i['message']}")
    else:
        h(2, "Quality Issues")
        lines.append("_No issues detected._")

    # Complexity warnings
    complexity = quality_data.get("complexity_warnings", [])
    if complexity:
        h(2, "Complexity Warnings")
        lines.append("> Files with estimated cyclomatic complexity > 20.\n")
        for w in complexity:
            li(f"`{w}`")

    # Checklist
    h(2, "Review Checklist")
    checklist = [
        ("Correctness", [
            "Logic matches the stated intent of the change",
            "Edge cases (empty, null, overflow) are handled",
            "No off-by-one errors in loops or slices",
        ]),
        ("Security", [
            "No hardcoded credentials or secrets",
            "All user input is validated before use",
            "SQL/shell injection vectors are closed",
            "Auth/authz checks are not bypassed",
        ]),
        ("Performance", [
            "No N+1 query patterns introduced",
            "Large allocations inside hot loops avoided",
            "Caching is appropriate and doesn't stale",
        ]),
        ("Maintainability", [
            "Functions are small and single-purpose",
            "Naming is clear and consistent with the codebase",
            "No dead or commented-out code left behind",
            "TODOs are tracked in issues, not inline",
        ]),
        ("Tests", [
            "Changed logic is covered by tests",
            "New tests are meaningful (not just coverage padding)",
            "Tests are deterministic (no time/random dependencies)",
        ]),
    ]
    for section, items in checklist:
        h(3, section)
        for item in items:
            lines.append(f"- [ ] {item}")

    # Footer
    lines.append("\n---")
    lines.append("_Generated by `review_report_generator.py`_")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate a markdown code review report.")
    parser.add_argument("repo_path", nargs="?", default=".", help="Path to git repository (default: .)")
    parser.add_argument("--base", default="main", help="Base branch/commit (default: main)")
    parser.add_argument("--head", default="HEAD", help="Head branch/commit (default: HEAD)")
    parser.add_argument("--title", default="Code Review Report", help="Report title")
    parser.add_argument("--output", "-o", help="Write report to this file instead of stdout")
    parser.add_argument("--analyze", action="store_true", help="Alias: run full analysis (default behaviour)")
    args = parser.parse_args()

    repo = os.path.abspath(args.repo_path)
    root = repo_root(repo) or repo

    branch = git_branch_name(root)
    commits = git_log(root, args.base, args.head)
    pr_data = collect_pr_data(root, args.base, args.head)
    quality_data = collect_quality_data(root)

    report = build_report(
        repo=root,
        base=args.base,
        head=args.head,
        pr_data=pr_data,
        quality_data=quality_data,
        commits=commits,
        branch=branch,
        title=args.title,
    )

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()

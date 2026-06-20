#!/usr/bin/env python3
"""Code Quality Checker — static analysis across TypeScript, JavaScript, Python, Go, Swift, Kotlin."""

import argparse
import ast
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator


# ── Issue severity ────────────────────────────────────────────────────────────

SEVERITY = {"error": 0, "warning": 1, "info": 2}


@dataclass
class Issue:
    file: str
    line: int
    severity: str  # error | warning | info
    code: str      # short rule id
    message: str

    def __str__(self):
        return f"{self.file}:{self.line}  [{self.severity.upper():7}] {self.code}  {self.message}"


# ── Generic pattern-based checker ────────────────────────────────────────────

PATTERN_RULES: list[tuple[set[str], str, str, str, re.Pattern]] = [
    # (extensions, severity, code, message, pattern)
    (
        {".py", ".js", ".ts", ".go", ".swift", ".kt"},
        "warning", "SEC001", "Hardcoded secret candidate",
        re.compile(r'(password|secret|api_?key|token)\s*=\s*["\'][^"\']{4,}["\']', re.I),
    ),
    (
        {".py", ".js", ".ts"},
        "warning", "SEC002", "eval() — arbitrary code execution risk",
        re.compile(r'\beval\s*\('),
    ),
    (
        {".py"},
        "warning", "SEC003", "exec() — arbitrary code execution risk",
        re.compile(r'\bexec\s*\('),
    ),
    (
        {".py"},
        "error", "SEC004", "shell=True subprocess call",
        re.compile(r'subprocess\.(call|run|Popen)\s*\([^)]*shell\s*=\s*True'),
    ),
    (
        {".py", ".js", ".ts", ".go", ".swift", ".kt"},
        "info", "MAINT001", "TODO / FIXME left in code",
        re.compile(r'\b(TODO|FIXME|HACK|XXX)\b', re.I),
    ),
    (
        {".js", ".ts"},
        "warning", "MAINT002", "console.log left in production code",
        re.compile(r'\bconsole\.(log|debug|warn|error)\s*\('),
    ),
    (
        {".py"},
        "warning", "MAINT003", "Bare except clause",
        re.compile(r'^\s*except\s*:'),
    ),
    (
        {".py", ".js", ".ts"},
        "info", "PERF001", "Synchronous sleep in async context",
        re.compile(r'\btime\.sleep\s*\(|\bsleep\s*\(\d'),
    ),
    (
        {".ts", ".js"},
        "warning", "TYPE001", "any type annotation",
        re.compile(r':\s*any\b'),
    ),
    (
        {".go"},
        "error", "GO001", "Unhandled error (_)",
        re.compile(r',\s*_\s*:?=\s*\w+\('),
    ),
    (
        {".py", ".js", ".ts"},
        "warning", "SEC005", "MD5 / SHA1 — weak hash algorithm",
        re.compile(r'\b(md5|sha1)\b', re.I),
    ),
    (
        {".py", ".js", ".ts", ".go"},
        "warning", "SEC006", "SQL string concatenation — injection risk",
        re.compile(r'(SELECT|INSERT|UPDATE|DELETE).{0,60}\+\s*\w', re.I),
    ),
]


def pattern_check(path: Path, lines: list[str]) -> Iterator[Issue]:
    ext = path.suffix.lower()
    for exts, severity, code, message, pattern in PATTERN_RULES:
        if ext not in exts:
            continue
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                yield Issue(str(path), i, severity, code, message)


# ── Python AST checker ────────────────────────────────────────────────────────

def py_ast_check(path: Path, source: str) -> Iterator[Issue]:
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as e:
        yield Issue(str(path), e.lineno or 0, "error", "PY001", f"Syntax error: {e.msg}")
        return

    for node in ast.walk(tree):
        # functions with too many arguments (>7)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            nargs = len(node.args.args) + len(node.args.posonlyargs)
            if nargs > 7:
                yield Issue(str(path), node.lineno, "warning", "COMP001",
                            f"Function '{node.name}' has {nargs} parameters (>7)")
            # very long function body
            body_lines = (node.end_lineno or node.lineno) - node.lineno
            if body_lines > 80:
                yield Issue(str(path), node.lineno, "info", "COMP002",
                            f"Function '{node.name}' is {body_lines} lines (>80)")

        # global variable mutation
        if isinstance(node, ast.Global):
            yield Issue(str(path), node.lineno, "info", "MAINT004",
                        f"global statement: {', '.join(node.names)}")

        # mutable default argument
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    yield Issue(str(path), node.lineno, "warning", "PY002",
                                f"Mutable default argument in '{node.name}'")
                    break


# ── Complexity estimator ──────────────────────────────────────────────────────

BRANCH_PATTERN = re.compile(
    r'\b(if|elif|else|for|while|case|catch|except|&&|\|\|)\b'
)


def cyclomatic_estimate(lines: list[str]) -> int:
    count = 1
    for line in lines:
        count += len(BRANCH_PATTERN.findall(line))
    return count


# ── File walker ───────────────────────────────────────────────────────────────

SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build", ".next"}
SUPPORTED_EXTS = {".py", ".ts", ".js", ".go", ".swift", ".kt"}


def walk_files(root: str) -> Iterator[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            p = Path(dirpath) / fname
            if p.suffix.lower() in SUPPORTED_EXTS:
                yield p


# ── Main analysis ─────────────────────────────────────────────────────────────

@dataclass
class QualityReport:
    root: str
    files_checked: int = 0
    issues: list[Issue] = field(default_factory=list)
    complexity_warnings: list[str] = field(default_factory=list)

    @property
    def errors(self):
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self):
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def infos(self):
        return [i for i in self.issues if i.severity == "info"]


def analyze(root: str, verbose: bool) -> QualityReport:
    report = QualityReport(root=root)

    for path in walk_files(root):
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        lines = source.splitlines()
        report.files_checked += 1

        if verbose:
            print(f"  checking {path}", file=sys.stderr)

        for issue in pattern_check(path, lines):
            report.issues.append(issue)

        if path.suffix == ".py":
            for issue in py_ast_check(path, source):
                report.issues.append(issue)

        cc = cyclomatic_estimate(lines)
        if cc > 20:
            report.complexity_warnings.append(f"{path}  CC≈{cc}")

    return report


def print_report(r: QualityReport, fmt: str, min_severity: str) -> None:
    min_level = SEVERITY.get(min_severity, 1)
    filtered = [i for i in r.issues if SEVERITY.get(i.severity, 99) <= min_level]

    if fmt == "json":
        import dataclasses
        data = {
            "root": r.root,
            "files_checked": r.files_checked,
            "summary": {
                "errors": len(r.errors),
                "warnings": len(r.warnings),
                "infos": len(r.infos),
            },
            "issues": [dataclasses.asdict(i) for i in filtered],
            "complexity_warnings": r.complexity_warnings,
        }
        print(json.dumps(data, indent=2))
        return

    print(f"\n{'='*60}")
    print(f"Code Quality Report: {r.root}")
    print(f"{'='*60}")
    print(f"Files checked : {r.files_checked}")
    print(f"Errors        : {len(r.errors)}")
    print(f"Warnings      : {len(r.warnings)}")
    print(f"Info          : {len(r.infos)}")

    if filtered:
        print(f"\nIssues (severity >= {min_severity}):")
        for issue in sorted(filtered, key=lambda x: (SEVERITY.get(x.severity, 9), x.file, x.line)):
            print(f"  {issue}")
    else:
        print("\nNo issues found.")

    if r.complexity_warnings:
        print(f"\nHigh complexity files ({len(r.complexity_warnings)}):")
        for w in r.complexity_warnings[:20]:
            print(f"  {w}")

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Static quality analysis for multi-language codebases.")
    parser.add_argument("target_path", nargs="?", default=".", help="Directory to analyze")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--format", choices=["text", "json"], default="text", dest="fmt")
    parser.add_argument("--min-severity", choices=["error", "warning", "info"], default="warning",
                        help="Minimum severity to show (default: warning)")
    args = parser.parse_args()

    root = os.path.abspath(args.target_path)
    report = analyze(root, args.verbose)
    print_report(report, args.fmt, args.min_severity)

    # exit non-zero if errors found
    sys.exit(1 if report.errors else 0)


if __name__ == "__main__":
    main()

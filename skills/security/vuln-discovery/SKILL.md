---
name: vuln-discovery
description: "Multi-phase vulnerability discovery pipeline for codebases. Orchestrates 8 phases — Recon, Hunt, Validate, Gapfill, Dedup, Trace, Feedback, Report — to find, validate, deduplicate, and trace security vulnerabilities. Use for security audits, vulnerability hunting, attack surface analysis, exploitation risk checks, or identifying injection, auth bypass, SSRF, race conditions, hardcoded secrets in source code. Triggers on: 'find vulnerabilities', 'security audit this repo', 'hunt security bugs', 'analyze attack surface', 'check for SQL injection', 'is this repo secure?', 'can attackers exploit anything?', 'find hardcoded secrets', 'pentest this service'. Does NOT trigger on general bugs, features, refactoring, perf, or docs."
---

# Vuln-Discovery

Orchestrate a multi-agent vulnerability discovery pipeline across a codebase. Eight sequential phases progressively narrow findings from broad reconnaissance to a validated, deduplicated, traced report.

## Pipeline

```
Recon → Hunt → Validate → Gapfill → Dedup → Trace → Feedback → Report
```

Each phase produces structured output consumed by the next. Never skip or reorder phases.

## Phase 1 — Recon

Produce an architecture document that drives all later phases.

1. Identify scope from the user's request. Default to the entire repository if unspecified.
2. Enumerate files with `rg --files`. Read key entry points, config, and module boundaries.
3. Fill in the architecture document template from `references/recon-checklist.md`.
4. Store the document for all later phases.

## Phase 2 — Hunt

Fan out specialized agents across 7 hunting trails. Each trail targets a vulnerability class. Agents are scoped to code segments identified in Recon.

### Trail definitions

| Trail | Scope | Reference |
|-------|-------|-----------|
| TRAIL-INJECT | Input and injection vulnerabilities | `references/hunt-trails.md` |
| TRAIL-AUTH | Authentication and authorization flaws | `references/hunt-trails.md` |
| TRAIL-DATAFLOW | Source-to-sink data flow issues | `references/hunt-trails.md` |
| TRAIL-FILEIO | File I/O and parsing vulnerabilities | `references/hunt-trails.md` |
| TRAIL-SECRETS | Hardcoded secrets and misconfigurations | `references/hunt-trails.md` |
| TRAIL-NETWORK | SSRF, CORS, and network-level flaws | `references/hunt-trails.md` |
| TRAIL-CONCURRENCY | Race conditions and state corruption | `references/hunt-trails.md` |

### Allocation

Use the matrix in `references/hunt-trails.md` to assign agents. Prioritize high-risk intersections (entry points + injection, auth modules + bypass). Spawn each agent with the prompt template from that file.

### Finding format

Every finding must conform to the schema in `references/finding-schema.md`. Required fields: `finding_id`, `title`, `category`, `severity`, `confidence`, `reachability`, `locations`, `description`, `root_cause`, `root_cause_id`, `attack_scenario`, `attack_path`, `evidence`, `sanitization_checkpoints`, `impact`, `remediation`.

## Phase 3 — Validate

Spawn independent agents to refute each finding. Validation is adversarial — agents try to disprove, not confirm.

- Use the prompt template in `references/validate-rules.md`.
- Rate each finding: `confirmed`, `plausible`, `unlikely`, or `false_positive`.
- Apply promotion rules from that file. Discard `false_positive` findings.
- Retain `confirmed` and `plausible` findings with validation notes attached.

## Phase 4 — Gapfill

Identify code areas with insufficient coverage and re-analyze them.

1. Map findings to modules in the architecture document.
2. Apply the gap heuristics from `references/gapfill-criteria.md`.
3. Spawn 1–3 focused Hunt agents per identified gap.
4. Run Validate on each gapfill finding before merging.

## Phase 5 — Dedup

Merge findings that share a root cause. Follow the policy in `references/dedup-policy.md`.

- Group by proximity (same file/function/data flow).
- Apply the single-fix, dependency, and cause-isolation tests.
- Merge groups into single findings with union of locations, attack scenarios, and the highest severity.
- Assign `root_cause_id` per the format in `references/dedup-policy.md`.

## Phase 6 — Trace

Confirm whether attacker input reaches each vulnerable code path. Follow the methodology in `references/trace-methodology.md`.

- For each finding, spawn a Trace agent with the prompt template from that file.
- Classify: `reachable`, `partially_reachable`, or `unreachable`.
- Adjust severity per the reachability rules in `references/severity-criteria.md`.

## Phase 7 — Feedback

For reachable and partially reachable findings, expand the hunt along confirmed attack paths.

- For each reachable finding, spawn 1–2 Hunt agents targeting adjacent code and similar patterns along the same data flow.
- For partially reachable findings, spawn agents to investigate whether the gating condition can be satisfied.
- Run Validate on new findings. Merge into the deduplicated list (re-run Dedup if overlaps appear).

## Phase 8 — Report

Write the final report using the template in `references/report-schema.md`.

1. Collect all validated, deduplicated, traced findings.
2. Sort by severity (Critical → Info), then by reachability (reachable → unreachable).
3. Fill in the report schema for each finding.
4. Write to the working directory: `vuln-report-[YYYY-MM-DD].md`

## Agent Orchestration

This skill uses `spawn_agent` for parallel work in phases 2, 3, 4, 6, and 7. Key constraints:

- **Hunt phase**: Spawn up to 7 trail agents in parallel. Each agent covers one trail across its assigned segment. Do not exceed 7 concurrent Hunt agents per code segment.
- **Validate phase**: Spawn one agent per finding. Batch into groups if there are many findings.
- **Gapfill phase**: Spawn 1–3 agents per identified gap.
- **Trace phase**: Spawn one agent per finding.
- **Feedback phase**: Spawn 1–2 agents per reachable finding.
- Each spawned agent receives the minimum context needed: the relevant architecture section, trail definition, and any prior findings.

## Resource Files

- `references/recon-checklist.md` — Architecture document template and segmentation strategy
- `references/hunt-trails.md` — Trail definitions, grep patterns, agent prompt templates, allocation strategy
- `references/bug-taxonomy.md` — Full vulnerability category taxonomy for trail assignment
- `references/validate-rules.md` — Validation prompt template, checklist, and promotion rules
- `references/gapfill-criteria.md` — Gap heuristics and re-analysis strategy
- `references/dedup-policy.md` — Deduplication rules, root-cause identification, and merge procedures
- `references/trace-methodology.md` — Source-to-sink tracing, sanitization assessment, and confidence scoring
- `references/finding-schema.md` — Canonical data model for findings
- `references/severity-criteria.md` — Severity matrix, category floors, and reachability adjustments
- `references/report-schema.md` — Final report template and formatting rules
- `examples/sample-report.md` — Example output demonstrating the expected report format
- `examples/example-finding.md` — Example validated finding with all schema fields
- `examples/example-recon-output.md` — Example Phase 1 architecture document output
- `examples/example-report-fragment.md` — Example report fragment with multiple findings

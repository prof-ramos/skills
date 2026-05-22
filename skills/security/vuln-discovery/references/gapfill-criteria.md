# Gapfill Criteria

## Overview

Gapfilling is a targeted re-analysis triggered when the initial discovery pass leaves under-analyzed areas. This document defines how to detect coverage gaps, when to trigger a gapfill pass, how to route it, and when to stop.

---

## Coverage Assessment

After each discovery trail completes, assess coverage by asking:

1. **Did every module with a trust boundary produce at least one finding?** If not, that module may be under-analyzed.
2. **Did every module that processes untrusted input produce injection-type findings?** If not, the input validation surface may have been missed.
3. **Did every module with privileged operations produce access-control findings?** If not, the authorization surface may be under-explored.
4. **Is the ratio of findings to module size reasonable?** A 2,000-line module with only one Info-level finding likely has undiscovered issues.

### Module Coverage Score

For each module, compute a rough coverage score:

```
coverage = findings_count / max(expected_findings, 1)
```

Where `expected_findings` is estimated from:
- Lines of code / 500 (baseline expectation of ~1 finding per 500 LOC for security-sensitive code)
- Adjusted upward if the module has trust boundaries (+3), processes untrusted input (+3), or has privileged operations (+2)

A module with `coverage < 0.3` is considered **under-analyzed**.

---

## Signals of Insufficient Coverage

Any of the following signals should flag a module or area for gapfilling:

### Signal 1: Trust boundary with zero findings
A module sits at a trust boundary (e.g., receives requests from an external system, bridges two privilege levels) but produced zero findings.

**Why it matters**: Trust boundaries are high-value targets. No findings likely means the analysis didn't probe the boundary, not that it's secure.

### Signal 2: Privileged operations with few findings
A module performs privileged operations (e.g., admin actions, database writes, file system access, secret handling) but has fewer than 2 findings.

**Why it matters**: Privileged code is inherently riskier. Few findings suggest the analysis didn't explore privilege escalation or misuse paths.

### Signal 3: Untrusted input processing with no injection findings
A module accepts, parses, or transforms untrusted input (e.g., HTTP request bodies, file uploads, user-controlled URLs, message queue payloads) but has zero injection-type findings (SQLi, XSS, command injection, path traversal, SSRF, deserialization).

**Why it matters**: Untrusted input is the primary vector for injection. No injection findings in an input-processing module is a strong signal of under-analysis.

### Signal 4: Large module with only low-severity findings
A module with ≥500 LOC that produced only 1–2 findings, all Low or Info severity.

**Why it matters**: Large modules have more attack surface. Only trivial findings suggests the deep analysis didn't reach the interesting parts.

### Signal 5: Disconnected trust zones
Two modules that interact across a trust boundary (e.g., a public API calling an internal service) where findings exist in only one side.

**Why it matters**: The boundary itself and the receiving side may not have been analyzed.

### Signal 6: Orthogonal category gap
All findings from a module fall into one vulnerability category (e.g., only auth issues, only injection issues), leaving other categories unexplored.

**Why it matters**: Real-world modules often have issues spanning multiple categories. A single-category cluster may indicate the analysis was too narrowly scoped.

---

## Gapfill Trigger Thresholds

A gapfill re-analysis is triggered when **any** of the following conditions are met:

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Under-analyzed module (coverage < 0.3) | 1+ modules | Trigger gapfill for those modules |
| Trust boundary with zero findings | 1+ boundaries | Trigger gapfill focusing on that boundary |
| Privileged ops with < 2 findings | 1+ modules | Trigger gapfill with access-control focus |
| Untrusted input with zero injection findings | 1+ modules | Trigger gapfill with injection focus |
| Large module (≥500 LOC) with only Low/Info | 1+ modules | Trigger gapfill with deeper analysis focus |
| Orthogonal category gap | 1+ modules | Trigger gapfill for missing categories |

**Maximum gapfill rounds**: 2 per module. After 2 rounds, accept diminishing returns and stop.

---

## How to Route Gapfill

Gapfill is not a generic re-scan. It must be **targeted** based on the specific signal that triggered it.

### Routing by Signal

| Trigger Signal | Trail Focus | Additional Context for Re-analysis |
|---------------|-------------|-------------------------------------|
| Trust boundary, zero findings | Authentication & authorization trail | Emphasize: "Analyze every entry point crossing this boundary. Look for auth bypass, missing validation, and privilege escalation." |
| Privileged ops, few findings | Access control & privilege trail | Emphasize: "Map all privileged operations. For each, test whether a lower-privilege user can invoke or tamper with it." |
| Untrusted input, no injection | Input validation & injection trail | Emphasize: "Trace every untrusted input to its sink. Test SQLi, XSS, command injection, path traversal, SSRF, and deserialization for each input-to-sink path." |
| Large module, low severity only | Deep variant analysis trail | Emphasize: "Re-analyze with focus on complex logic, state mutations, race conditions, and chaining opportunities." |
| Disconnected trust zones | Inter-service boundary trail | Emphasize: "Trace the communication between the two zones. Look for missing auth, data leakage, and request forgery at the boundary." |
| Orthogonal category gap | Missing category trail | Emphasize: "This module has only [existing category] findings. Systematically check for: [missing categories]." |

### Gapfill Prompt Structure

When invoking a gapfill re-analysis, include:

```markdown
## Gapfill Re-analysis Request

- **Module**: [module path/name]
- **Trigger signal**: [which signal triggered this gapfill]
- **Round**: [1 or 2]
- **Focus**: [specific trail/route from table above]
- **Prior findings in this module**: [list of finding IDs and categories, so the re-analysis avoids duplicating them]
- **Emphasis**: [the specific emphasis text from the routing table]

## Instructions

Analyze this module with the specified focus. Do not re-report findings already identified. Look specifically for vulnerabilities in the emphasized categories and patterns. Report new findings using the standard finding format.
```

---

## Gapfill Finding Handling

All findings from a gapfill pass must go through the **standard validation pipeline** before being merged into the active findings set.

### Process

1. **Gapfill pass completes** → produces a set of candidate findings.
2. **Each candidate enters validation** → uses the same validation rubric and levels (Confirmed, Plausible, Possible, Unlikely, False positive).
3. **Validation results are applied** → same promotion/demotion rules as primary findings.
4. **Deduplication** → before merging, check whether any validated gapfill finding duplicates an existing finding. If so, merge by keeping the more severe / better-validated version.
5. **Merge into active findings** → only after validation and deduplication.

### Anti-Patterns to Avoid

- **Do not** skip validation for gapfill findings because "they came from a targeted analysis."
- **Do not** merge gapfill findings directly into the active set without deduplication.
- **Do not** allow more than 2 gapfill rounds per module (see diminishing returns below).

---

## When to Stop Gapfilling

### Diminishing Returns Rule

Stop gapfilling when **either** condition is met:

1. **Quantitative threshold**: The gapfill round produces fewer than 3 new validated findings (after deduplication) for the targeted module.
2. **Round limit**: 2 gapfill rounds have been completed for a given module, regardless of yield.

### Rationale

- The first gapfill round addresses the most obvious gaps. The second round catches what the first missed.
- Beyond 2 rounds, the analysis is increasingly unlikely to produce novel findings and more likely to produce low-quality or duplicate results.
- Time spent on additional rounds is better spent on other modules or on validation depth.

### Exceptions

The only exception to the 2-round limit is if a **new code path or module** is discovered during gapfill that was not analyzed at all in prior passes. In that case, treat it as a fresh module (with its own gapfill budget) rather than an additional round on the existing module.

---

## Quick Reference: Gapfill Decision Flow

```
Discovery trail completes
  │
  ├─ Assess module coverage scores
  │
  ├─ Check trigger signals
  │    ├─ Trust boundary + 0 findings → trigger
  │    ├─ Privileged ops + < 2 findings → trigger
  │    ├─ Untrusted input + 0 injection → trigger
  │    ├─ Large module + only Low/Info → trigger
  │    ├─ Disconnected trust zones → trigger
  │    └─ Category gap → trigger
  │
  ├─ Route gapfill by signal type
  │    └─ Use focused trail + emphasis prompt
  │
  ├─ Validate all gapfill findings
  │    └─ Same rubric as primary findings
  │
  ├─ Deduplicate against existing findings
  │
  ├─ Merge validated, deduplicated findings
  │
  └─ Check stop conditions:
       ├─ < 3 new validated findings → stop
       └─ 2 rounds completed → stop
           └─ Unless new code path discovered → fresh module budget
```

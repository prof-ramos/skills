# Vulnerability Report Schema

Use this schema for the final report produced in Phase 8.

## Report Structure

```markdown
# Vulnerability Assessment Report

**Target**: [repository or module path]
**Date**: [YYYY-MM-DD]
**Scope**: [scope description from Phase 1]
**Total Findings**: [count]
**Critical**: [count] | **High**: [count] | **Medium**: [count] | **Low**: [count] | **Info**: [count]

---

## Executive Summary

[2–4 sentence summary of the most impactful findings and overall risk posture.]

## Severity Distribution

| Severity | Count | Reachable | Partially Reachable | Unreachable |
|----------|-------|-----------|--------------------|-------------|
| Critical |   —   |     —     |         —          |      —      |
| High     |   —   |     —     |         —          |      —      |
| Medium   |   —   |     —     |         —          |      —      |
| Low      |   —   |     —     |         —          |      —      |
| Info     |   —   |     —     |         —          |      —      |

## Findings

[Repeat the following block for each finding, ordered by severity then reachability.]

### [FINDING-ID]: [Title]

- **Severity**: Critical | High | Medium | Low | Info
- **Category**: [taxonomy ID, e.g. INJ-01]
- **Confidence**: confirmed | plausible | possible
- **Reachability**: reachable | partially_reachable | unreachable
- **Locations**:
  - `[file:line]`
  - `[file:line]` (if multiple)

**Description**:

[1–3 sentences describing the vulnerability.]

**Root Cause**:

[The underlying code-level defect, not the symptom.]
Root cause ID: `[RC-{category}-{hash}]`

**Attack Scenario**:

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Attack Path**:

1. [Entry point]
2. [Intermediate transformation]
3. [Vulnerable code / sink]

**Evidence**:

```[lang]
[relevant code snippet]
```

**Sanitization Checkpoints**:

| Checkpoint | Type | Bypassable? |
|------------|------|-------------|
| `[file:line]` | validation / encoding / sanitize | Yes / No |

**Impact**:

[What the attacker achieves: data theft, RCE, privilege escalation, etc.]

**Remediation**:

[Concrete fix recommendation with code-level direction.]

**Validation Notes**:

[Caveats or observations from the Validate phase.]

**Dedup Notes**:

[Reasoning for root_cause_id assignment, if applicable.]

**Trace Notes**:

[Provenance notes: how the taint trace was discovered, any assumptions.]

---

## Defense-in-Depth Issues

[List findings marked `unreachable` here with brief descriptions. These are not exploitable via current attack paths but represent hardening opportunities.]

---

## Coverage Gaps

[List areas identified in Gapfill that remain under-analyzed or could not be fully assessed.]
```

## Finding IDs

Use sequential IDs: `F-001`, `F-002`, etc. Assign in order of severity (Critical first).

## Timestamp Format

Use ISO 8601 date in the filename: `vuln-report-YYYY-MM-DD.md`

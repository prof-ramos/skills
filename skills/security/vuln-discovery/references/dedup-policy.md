# Vulnerability Deduplication Policy

## Purpose

When multiple findings point to the same root cause, merge them into a single finding. Dedup reduces noise, preserves severity accuracy, and ensures remediation targets the actual flaw—not its symptoms.

---

## Dedup Triggers

Consider merging when any of these conditions hold between two findings:

| Trigger | Description |
|---|---|
| Same file/function | Both findings occur in the same function or tightly coupled code |
| Same data flow | Untrusted input travels the same path to reach both sinks |
| Same missing validation | The same validation gap enables both findings |
| Same vulnerable pattern at multiple call sites | A single insecure pattern (e.g., string interpolation into SQL) is called from multiple locations |

If none of these triggers apply, findings are independent—keep them separate.

---

## Root Cause Identification

Two findings share a root cause when fixing one defect eliminates the other. Ask:

1. **Single-fix test**: Would one code change resolve both findings?
2. **Dependency test**: Does one finding only exist because the other exists (e.g., both rely on the same unsanitized variable)?
3. **Cause-isolation test**: If you rewrote the vulnerable function with correct validation, would both findings disappear?

If the answer is **yes** to at least two of these tests, the findings share a root cause and should be merged. If only one test is positive or the findings survive independently after the fix, keep them separate.

---

## Dedup Rules with Examples

### Rule 1 — Same vulnerable pattern at multiple call sites → single finding with multiple locations

**Scenario**: An application builds SQL queries via string concatenation in `getUser()`, `getOrders()`, and `searchProducts()`.

**Action**: One finding: "SQL Injection via string concatenation." Locations list all three call sites.

**Rationale**: One fix (parameterized queries) eliminates all three. The pattern is the root cause; the call sites are manifestations.

### Rule 2 — Different symptoms from same missing validation → single finding with multiple manifestations

**Scenario**: A JSON parser lacks input validation. This causes:
- Finding A: Denial of service via crafted deeply-nested JSON
- Finding B: Prototype pollution via `__proto__` key

**Action**: One finding: "Missing input validation in JSON parser." Manifestations list both DoS and prototype pollution.

**Rationale**: Adding schema validation fixes both. The missing validation is the root cause; DoS and pollution are symptoms.

### Rule 3 — Independent vulns in same file → keep separate

**Scenario**: `auth.js` contains:
- Finding A: Hardcoded API key on line 10
- Finding B: Timing attack on password comparison on line 45

**Action**: Two separate findings. They have different root causes (credential management vs. comparison logic), different fixes, and different severity profiles.

**Rationale**: Proximity in the same file does not imply shared root cause.

---

## Merging Procedure

When merging findings, apply these rules:

| Field | Merge Rule |
|---|---|
| **Severity** | Take the **highest** severity among merged findings |
| **Description** | Combine into a single narrative: root cause first, then enumerate manifestations |
| **Attack scenarios** | **Union** — include all distinct scenarios from each original finding |
| **Locations** | **Union** — list all file:line references |
| **Confidence** | Take the **highest** confidence (strongest evidence lifts the group) |
| **Root cause ID** | Assign a single `root_cause_id` (see format below) |

### Merge Example

```
Before merge:
  F-001  High   SQLi in getUser()       at db.js:22
  F-002  High   SQLi in getOrders()     at db.js:58
  F-003  Medium SQLi in searchProducts() at db.js:91

After merge:
  F-001  High   SQL Injection via string concatenation in db.js
         Locations: db.js:22, db.js:58, db.js:91
         Attack scenarios: auth bypass (from F-001), data exfiltration (from F-002), 
                           search manipulation (from F-003)
         root_cause_id: RC-inject-a3f1c2
```

---

## Root Cause ID Format

```
RC-{category}-{hash}
```

- **category**: One of `inject`, `xss`, `auth`, `crypto`, `config`, `logic`, `dos`, `access`, `other`
- **hash**: First 6 characters of SHA-256 of the canonical root-cause description (e.g., "string concat in SQL query builder" → `a3f1c2`)

The ID groups findings without depending on file paths or line numbers (which shift during refactoring).

### Generation Steps

1. Write a one-sentence canonical description of the root cause (e.g., "Unsanitized user input passed to OS command execution via exec()")
2. Normalize: lowercase, trim whitespace, collapse spaces
3. Compute `SHA-256(normalized)`, take first 6 hex characters
4. Prefix with `RC-` and the category

### Examples

| Root Cause | Category | Hash | ID |
|---|---|---|---|
| Unsanitized user input in SQL string concat | inject | `a3f1c2` | `RC-inject-a3f1c2` |
| Missing CSRF token on state-changing endpoints | auth | `b7e4d9` | `RC-auth-b7e4d9` |
| Hardcoded encryption key in source | crypto | `f2a081` | `RC-crypto-f2a081` |

---

## Edge Cases

### Ambiguous dedup — overlapping but not identical root causes

When two findings share some but not all root-cause tests (e.g., same data flow but different sinks with different validation gaps):

- **Default**: Keep separate. Over-merging hides distinct fixes.
- **Exception**: If the shared component is the **primary** enabler and the sinks differ only in which output is affected, merge with multiple manifestations.
- **Document the ambiguity**: Note in the finding description why the merge decision was non-obvious.

### Severity disagreement after merge

If merged findings disagree on severity (e.g., one is Critical, another is Low):

- Always take the highest severity.
- Include a note: "Merged finding spans multiple impact profiles; Critical severity reflects the worst-case scenario."

### One finding is unreachable

If one of the candidate findings is `unreachable` but shares a root cause with a `reachable` finding:

- Merge. The reachable finding establishes exploitability; the unreachable call site is a defense-in-depth note within the same finding.
- The merged finding retains `reachable` status.

### Findings discovered in different hunt cycles

Merge across cycles if the `root_cause_id` matches. Reference both cycle numbers in the finding metadata. This prevents the same defect from appearing as "new" in later reports.

---

## Summary Decision Tree

```
Two findings candidate for dedup?
  │
  ├─ Pass single-fix test? ── Pass dependency test? ──→ MERGE
  │
  ├─ Fail single-fix, pass dependency only ──→ KEEP SEPARATE (note overlap)
  │
  ├─ Same file, no shared cause ──→ KEEP SEPARATE
  │
  └─ Ambiguous ──→ Default: KEEP SEPARATE, document ambiguity
```

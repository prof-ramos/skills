# Finding Data Model

Canonical schema for vulnerability discovery findings. Every finding produced by this skill **must** conform to this model.

---

## 1. Field Definitions

| # | Field | Type | Required | Description |
|---|-------|------|----------|-------------|
| 1 | `finding_id` | `string` | ✅ | Unique identifier in `F-NNN` format (zero-padded, e.g. `F-001`, `F-042`). Incremented per-session. |
| 2 | `title` | `string` | ✅ | Concise, human-readable summary (imperative mood, ≤ 80 chars). E.g. "SQL injection in user search endpoint". |
| 3 | `category` | `string` | ✅ | Bug-taxonomy identifier. See § Category IDs. E.g. `INJ-01`, `AUTH-02`. |
| 4 | `severity` | `enum` | ✅ | One of: `Critical`, `High`, `Medium`, `Low`, `Info`. Determined by the severity matrix (§ 3). |
| 5 | `confidence` | `enum` | ✅ | One of: `confirmed`, `plausible`, `possible`. See § 4 for criteria. |
| 6 | `reachability` | `enum` | ✅ | One of: `reachable`, `partially_reachable`, `unreachable`. See § 5 for criteria. |
| 7 | `locations` | `list[string]` | ✅ | File paths with optional line numbers in `file:line` format. At least one entry required. |
| 8 | `description` | `string` | ✅ | Full narrative of the vulnerability: what it is, how it manifests, and why it matters. |
| 9 | `root_cause` | `string` | ✅ | The minimal code-level defect enabling the vulnerability. Not the consequence — the *cause*. |
| 10 | `root_cause_id` | `string` | ✅ | Deterministic key for dedup grouping. Composed as `{category}::{normalized_location}`. E.g. `INJ-01::UserController.search`. |
| 11 | `attack_scenario` | `list[string]` | ✅ | Step-by-step attack narrative. Each step is a single imperative sentence. |
| 12 | `attack_path` | `object` | ✅ | Structured path with three fields (see below). |
| 13 | `evidence` | `string` | ✅ | Minimal code snippet demonstrating the vulnerability. Trimmed to relevant lines only. |
| 14 | `sanitization_checkpoints` | `list[object]` | ✅ | Each entry has `checkpoint` (location), `type` (validation/encoding/sanitize), and `bypassable` (bool). May be empty `[]`. |
| 15 | `impact` | `string` | ✅ | Concrete business/technical impact if exploited. Not generic — tie to the specific asset and data at risk. |
| 16 | `remediation` | `string` | ✅ | Specific, actionable fix guidance. Prefer code-level direction over vague advice. |
| 17 | `validation_notes` | `string` | ⬜ | Observations from attempted validation (e.g. "Confirmed via crafted curl — DB error exfiltrated"). |
| 18 | `dedup_notes` | `string` | ⬜ | Reasoning for `root_cause_id` assignment. Explain why this is or is not a duplicate. |
| 19 | `trace_notes` | `string` | ⬜ | Provenance notes: how the taint trace was discovered, tools used, any assumptions. |

### `attack_path` structure

```yaml
attack_path:
  entry_point: "string   # Where untrusted data enters (file:line)"
  intermediates: "list[string]  # Propagation steps (file:line)"
  sink: "string   # Where the dangerous operation occurs (file:line)"
```

### `sanitization_checkpoints` item structure

```yaml
- checkpoint: "string   # File:line of the validation"
  type: "enum     # validation | encoding | sanitize"
  bypassable: bool      # Whether an attacker can circumvent this check
```

---

## 2. Category IDs

| ID | Category | Examples |
|----|----------|----------|
| `INJ-01` | Injection (SQL) | SQL injection, NoSQL injection |
| `INJ-02` | Injection (Command) | OS command injection, shell metacharacter abuse |
| `INJ-03` | Injection (Code) | `eval()`, deserialization, template injection |
| `INJ-04` | Injection (LDAP/XPath/Other) | LDAP injection, XPath injection, header injection |
| `AUTH-01` | Authentication (Broken) | Missing auth, weak credentials, brute-force |
| `AUTH-02` | Authorization (Broken) | IDOR, privilege escalation, missing RBAC check |
| `AUTH-03` | Session Management | Session fixation, missing session invalidation |
| `CRYPTO-01` | Weak Cryptography | Hardcoded keys, weak algorithms, insufficient key length |
| `CRYPTO-02` | Transport Security | Missing TLS, weak TLS config, mixed content |
| `DATA-01` | Data Exposure (Sensitive) | PII leakage, verbose errors, information disclosure |
| `DATA-02` | Data Exposure (Misconfigured) | CORS misconfig, directory listing, default credentials |
| `ERR-01` | Error Handling | Unhandled exceptions, stack trace leakage, swallow-and-continue |
| `FS-01` | File Handling | Path traversal, unrestricted upload, insecure temp files |
| `MEM-01` | Memory Safety | Buffer overflow, use-after-free, integer overflow |
| `RACE-01` | Race Condition | TOCTOU, concurrent access without locks |
| `SSRF-01` | Server-Side Request Forgery | Internal network scanning, cloud metadata access |
| `XSS-01` | Cross-Site Scripting (Reflected) | Unescaped user input in HTML response |
| `XSS-02` | Cross-Site Scripting (Stored) | Persisted malicious content rendered to other users |
| `CSRF-01` | Cross-Site Request Forgery | Missing anti-CSRF token, relying solely on cookies |
| `CONFIG-01` | Security Misconfiguration | Default configs, missing security headers, verbose logging |
| `DEP-01` | Vulnerable Dependency | Known CVE in third-party package |
| `LOGIC-01` | Business Logic Flaw | Workflow bypass, price manipulation, state corruption |

---

## 3. Severity Matrix

Severity is determined by crossing **impact** (rows) with **exploitability** (columns).

| Impact \ Exploitability | Easy | Moderate | Difficult |
|--------------------------|------|----------|-----------|
| **System Compromise / Data Breach** | Critical | Critical | High |
| **Significant Data Exposure** | Critical | High | Medium |
| **Limited Data Exposure** | High | Medium | Low |
| **Minimal / Informational** | Medium | Low | Info |

### Definitions

- **Easy** — Unauthenticated, single request, no special conditions.
- **Moderate** — Requires authentication, specific state, or chained steps.
- **Difficult** — Requires privileged access, race conditions, or exotic configurations.

- **System Compromise / Data Breach** — RCE, full DB dump, admin takeover.
- **Significant Data Exposure** — Partial data leak, privilege escalation to non-admin.
- **Limited Data Exposure** — Info disclosure, non-sensitive data leak.
- **Minimal / Informational** — Verbose errors, version disclosure, best-practice violations.

> **Special rule:** If `reachability` is `unreachable`, downgrade severity by one level (floor at `Info`). If `confidence` is `possible`, downgrade by one level (floor at `Info`).

---

## 4. Confidence Levels

| Level | Criteria |
|-------|----------|
| `confirmed` | Vulnerability is **exploitable** as described. One or more of: live reproduction, automated exploit proof, or verified taint trace from source to sink with no intact sanitization. |
| `plausible` | Vulnerability is **likely exploitable** based on static analysis. A complete taint trace exists from entry point to sink, but some sanitization checkpoints are present — and at least one is marked `bypassable`. No live reproduction attempted. |
| `possible` | Vulnerability is **suspected** but not fully traced. Entry point and sink are identified, but the propagation path is incomplete or sanitization status is unknown. Requires manual investigation. |

### Downgrade rules

- If the trace has **gaps** (unresolved intermediates) → max `possible`.
- If **all** sanitization checkpoints are marked `bypassable: false` → max `possible` unless an alternative bypass path exists.
- If `reachability` is `unreachable` → max `possible`.

---

## 5. Reachability Levels

| Level | Criteria |
|-------|----------|
| `reachable` | Entry point is **exposed to untrusted input** (network endpoint, CLI argument, file input, environment variable) and there are **no unconditional barriers** (auth gates, feature flags, network segmentation) blocking the path. |
| `partially_reachable` | Entry point exists but is gated by **one condition** an attacker can realistically satisfy (e.g. valid low-privilege account, specific feature flag enabled, same-origin policy). The path is reachable but not by any anonymous requester. |
| `unreachable` | Entry point is **not externally accessible** (internal-only endpoint, dead code path, development-only configuration) **or** the path is fully blocked by an unconditional barrier (e.g. mandatory admin auth with MFA that cannot be bypassed within this finding). |

### Notes

- Reachability is assessed **independently** of exploitability. A path may be reachable but hard to exploit (difficult exploitability + reachable → High severity).
- When in doubt, default to `partially_reachable` and document the uncertainty in `trace_notes`.

---

## 6. Example Finding

```yaml
finding_id: F-001
title: "SQL injection in user search endpoint"
category: INJ-01
severity: Critical
confidence: confirmed
reachability: reachable
locations:
  - "src/routes/users.ts:47"
  - "src/db/queries.ts:112"
description: |
  The /api/users/search endpoint accepts a `q` query parameter that is
  interpolated directly into a raw SQL WHERE clause without parameterization.
  An attacker can inject arbitrary SQL to read, modify, or delete data from
  the application database.
root_cause: |
  String interpolation of user-supplied `q` parameter into a raw SQL query
  string at src/db/queries.ts:112 — the value is used inside a template
  literal passed to `pool.query()` instead of using parameterized bindings.
root_cause_id: "INJ-01::UserSearch.query"
attack_scenario:
  - "Attacker sends GET /api/users/search?q=' UNION SELECT credit_card FROM payments--"
  - "Server interpolates the payload into SQL: SELECT ... WHERE name LIKE '%' UNION SELECT credit_card FROM payments--%'"
  - "Database executes the UNION query and returns payment data in the API response"
  - "Attacker extracts credit card numbers from the JSON response"
attack_path:
  entry_point: "src/routes/users.ts:47"
  intermediates:
    - "src/routes/users.ts:52"
    - "src/services/userService.ts:31"
  sink: "src/db/queries.ts:112"
evidence: |
  // src/routes/users.ts:47
  router.get('/search', async (req, res) => {
    const results = await searchUsers(req.query.q);  // unsanitized
  });

  // src/db/queries.ts:112
  const { rows } = await pool.query(
    `SELECT * FROM users WHERE name LIKE '%${query}%'`  // direct interpolation
  );
sanitization_checkpoints:
  - checkpoint: "src/routes/users.ts:48"
    type: validation
    bypassable: true
  - checkpoint: "src/middleware/rateLimit.ts:15"
    type: validation
    bypassable: true
impact: |
  Full read access to the application database. An attacker can exfiltrate
  all tables including PII (emails, addresses) and payment data (credit card
  numbers). Under the PostgreSQL superuser role used by the app, write access
  and OS command execution via COPY/lo_export may also be possible.
remediation: |
  Replace string interpolation with parameterized queries:

    // Before (vulnerable):
    pool.query(`SELECT * FROM users WHERE name LIKE '%${query}%'`);

    // After (safe):
    pool.query(`SELECT * FROM users WHERE name LIKE '%' || $1 || '%'`, [query]);

  Additionally, apply input validation on `q` (alphanumeric + spaces only,
  max 100 chars) as defense-in-depth. Restrict the database user to
  least-privilege permissions.
validation_notes: |
  Confirmed via curl: `curl 'http://localhost:3000/api/users/search?q=%27%20UNION%20SELECT%201--'`
  returned a 200 with unexpected column count, proving the UNION executes.
dedup_notes: |
  The similar finding in admin panel search (src/routes/admin.ts:88) shares
  the same root cause (interpolation in queries.ts) and is grouped under
  the same root_cause_id. Not a duplicate — different entry point, different
  auth requirements.
trace_notes: |
  Discovered via static taint analysis: req.query.q flows through
  searchUsers() → userService.search() → queries.ts with no effective
  sanitization. The rate limiter does not prevent the injection. Manual curl
  test confirmed exploitability.
```

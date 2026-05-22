# Trace Methodology — Reachability Confirmation

## Purpose

A vulnerability hypothesis is only as strong as its reachability. This methodology defines how to confirm whether attacker-controlled input can reach a vulnerable code path (sink). Unreachable findings waste remediation effort; confirmed reachability sharpens priorities.

---

## Source Identification

An attacker-controlled source is any entry point where untrusted data enters the application. Classify sources by type:

| Source Type | Examples | Trust Level |
|---|---|---|
| HTTP parameters | Query strings, headers, cookies, request body fields, path parameters | Untrusted |
| CLI arguments | `argv`, environment-driven flags | Context-dependent |
| File input | Uploaded files, config files parsed at runtime, imported data | Untrusted |
| Network data | API responses from third parties, WebSocket messages, gRPC payloads | Untrusted |
| Environment variables | Config injected by deployment, secrets managers | Context-dependent |
| Database values | Data read from DB that was previously written by users | Untrusted (tainted) |
| Inter-service messages | Messages from other microservices, queue payloads | Context-dependent |

### Rules for source classification

1. **Default to untrusted** unless the source is provably controlled only by the application itself (e.g., a constant defined in code).
2. **Transitive trust**: If a trusted source reads from an untrusted source (e.g., config file editable by another service), treat it as untrusted.
3. **Authenticated ≠ trusted**: Authentication limits *who* can send data, not *what* data they send. An authenticated user is still an attacker-controlled source.

---

## Path Tracing Methodology

Trace data flow from source to sink in four stages:

```
SOURCE → TRANSFORMATIONS → VALIDATIONS/SANITIZATION → SINK
```

### Step 1 — Start at the source

Identify the exact variable, parameter, or data field that is attacker-controlled. Record:
- Variable name
- Entry point (function, endpoint, handler)
- Data type and expected format

### Step 2 — Follow transformations

Track every operation applied to the data on its path to the sink:

| Transformation | Effect on taint |
|---|---|
| String concatenation / interpolation | Preserved — taint flows through |
| Encoding (URL, Base64, HTML entity) | Preserved — encoding is reversible |
| Type casting (int(), float(), bool()) | May narrow taint — but coercion edge cases exist |
| Serialization / deserialization | Preserved — round-trip restores original data |
| Hashing / encryption | Breaks taint — output is not attacker-controlled (unless key is known) |
| Array indexing `data[key]` | Preserved if `key` is attacker-controlled; breaks if `key` is constant |

**Rule**: Taint is preserved unless the transformation is **cryptographic or one-way**. Encoding and escaping do not remove taint.

### Step 3 — Evaluate validations and sanitization

At each validation or sanitization checkpoint, assess whether it **effectively blocks** the attack. See the Sanitization Assessment section below.

### Step 4 — Reach the sink

Confirm the data arrives at the vulnerable operation (e.g., `eval()`, `exec()`, SQL query builder, file write path). If taint survives all intermediate steps, the path is reachable.

### Tracing conventions

- Trace **one path per finding**. If multiple paths reach the same sink, document each as a separate trace but reference the shared sink.
- Record the trace as a sequence: `source:funcA → transform:funcB → validate:funcC → sink:funcD`
- Note branch conditions: if the path requires a specific branch (e.g., `if mode == "admin"`), record it as a **condition** on reachability.

---

## Sanitization Assessment

### When sanitization is effective

| Sanitizer | Effective against | Condition |
|---|---|---|
| Parameterized queries / prepared statements | SQL injection | Always — data never enters query structure |
| Allowlist validation (strict type + value check) | Injection, path traversal | Effective when allowlist is exhaustive and enforced before use |
| Context-aware output encoding | XSS | Effective when encoding matches the output context (HTML, JS, URL, CSS) |
| CSP headers | XSS | Effective as a mitigation; does not sanitize input itself |
| Path canonicalization + allowlist prefix check | Path traversal | Effective when canonicalized path is checked against allowlist |
| Signed tokens (HMAC) | Parameter tampering | Effective when signature is verified before use |

### When sanitization is bypassable

| Sanitizer | Why it fails | Common bypass |
|---|---|---|
| Blocklist / denylist filtering | Incomplete coverage; encoding bypasses | Unicode normalization, double-encoding, null bytes |
| `escape()` for HTML context used in JS context | Wrong encoding context | `</script><script>alert(1)</script>` |
| Type casting as sole validation | Coercion edge cases | `"0e12345" == 0` in PHP, `NaN` comparisons |
| Regex validation without anchors | Partial match accepted | `^admin` without `$` matches `adminEVIL` |
| Truncation | Data survives partial truncation | Long payloads where the dangerous fragment falls after the cut |
| Client-side-only validation | Not enforced server-side | Direct API requests bypass browser checks |

### Assessment rule

A sanitizer is **effective** only if it is:
1. Applied **before** the sink (not after)
2. **Context-appropriate** for the attack type
3. **Unbypassable** under the threat model (no known encoding, normalization, or logic bypass)

If any of these conditions are not met, the sanitizer is **bypassable** and does not block reachability.

---

## Reachability Levels

### `reachable`

- Clear path from attacker-controlled source to sink
- No effective sanitization blocks exploitation
- The attacker can craft input that reaches the sink in its malicious form

**Action**: Findings at this level are confirmed vulnerabilities. Proceed to impact assessment and remediation.

### `partially_reachable`

A path exists but exploitation requires one or more of:

| Condition | Example |
|---|---|
| Authentication | Only authenticated users can reach the endpoint, but any user account qualifies |
| Specific configuration | Feature flag, debug mode, or environment setting must be enabled |
| Race window | Exploitation requires winning a timing window (TOCTOU) |
| Low-probability branch | Code path is reachable but only under unusual input conditions |
| Privilege escalation prerequisite | Normal user can reach path; admin privileges at sink require separate escalation |

**Action**: Findings are confirmed with caveats. Document the required conditions. Severity may be adjusted downward depending on likelihood of conditions being met in production.

### `unreachable`

- No path from any attacker-controlled source to the sink, **or**
- Effective sanitization blocks all known exploitation paths

**Action**: Demote to defense-in-depth. Document as a hardening recommendation, not a vulnerability. See the Unreachable Findings section below.

---

## Confidence Scoring

Assign a confidence level to each trace based on the strength of evidence:

| Confidence | Criteria | Score Range |
|---|---|---|
| **High** | Complete trace from source to sink verified; sanitization assessed and bypassable or absent; code path confirmed by static analysis or test | 0.8–1.0 |
| **Medium** | Trace is plausible but involves an indirect data flow (e.g., through a shared state, callback, or event system); sanitization status uncertain | 0.5–0.79 |
| **Low** | Trace is speculative; source-to-sink path inferred but not directly observed; heavy reliance on assumptions about runtime behavior | 0.2–0.49 |
| **None** | No trace found; finding is hypothetical | 0.0–0.19 |

### Scoring adjustments

- **+0.1** if the trace has been confirmed by a proof-of-concept or test case
- **-0.1** if the trace crosses a trust boundary that may have undocumented validation
- **-0.2** if the trace relies on a race condition or timing assumption
- **-0.3** if the source is environment variables and the deployment environment is unknown

### Confidence and severity interaction

Confidence does not reduce severity directly. Instead:
- `High` confidence: severity stands as assessed
- `Medium` confidence: severity stands, but flag for manual verification
- `Low` confidence: demote severity by one level for prioritization purposes
- `None` confidence: demote to informational / defense-in-depth

---

## Unreachable Findings

When a trace concludes `unreachable`:

1. **Demote severity to informational** — the code is not exploitable under current conditions
2. **Label as defense-in-depth** — the finding represents a missing safeguard that would matter *if* conditions change
3. **Record why it is unreachable** — document the specific sanitization, configuration, or architectural reason
4. **Note potential for future reachability** — flag conditions under which the finding could become reachable (e.g., "if the authentication check on endpoint `/api/upload` is removed, this becomes reachable")

Unreachable findings still have value:
- They document assumptions about the threat model
- They surface latent risks that configuration changes could activate
- They provide guidance for future code audits when the codebase evolves

---

## How Traces Feed into the Feedback Phase

Reachability traces directly drive the next hunt cycle:

### Reachable findings → Generate new hunt tasks

Each confirmed `reachable` finding expands the attack surface map and suggests adjacent targets:

| Trace Result | Feedback Action |
|---|---|
| Reachable SQL injection in query builder | Hunt for other sinks that use the same query builder (same data flow, new sinks) |
| Reachable XSS via reflected parameter | Hunt for other reflections of the same parameter (same source, new sinks) |
| Reachable path traversal via file upload | Hunt for other file operations that consume the stored path (new source-to-sink chain) |

### Partially reachable findings → Generate condition-research tasks

- Investigate how likely the required condition is in production
- Hunt for ways an attacker could satisfy the condition (e.g., default credentials, feature flags exposed to users)

### Unreachable findings → Generate hardening tasks

- Document as defense-in-depth recommendations
- If the unreachable reason is a single sanitizer, hunt for bypasses against that sanitizer
- If the unreachable reason is a configuration, verify the configuration is enforced in all environments

### Trace reuse

Completed traces are reusable assets:
- A confirmed source-to-sink path can be parameterized for other data flowing the same route
- Sanitization assessments for a given function apply to all findings that pass through it
- When new code is introduced, existing traces can be extended instead of rebuilt from scratch

---

## Summary

```
SOURCE ──→ TRANSFORMATIONS ──→ VALIDATIONS/SANITIZATION ──→ SINK
  │              │                      │                      │
  │  taint preserved unless             │  effective?           │
  │  cryptographic/one-way              │  ├─ yes → UNREACHABLE │
  │                                     │  └─ no/bypassable →  │
  │                                     │                       │
  └─────────────────────────────────────┴───────────────────────┘
                                    │
                          REACHABLE / PARTIALLY REACHABLE / UNREACHABLE
                                    │
                          CONFIDENCE SCORE (0.0–1.0)
                                    │
                          FEEDBACK → new hunt tasks
```

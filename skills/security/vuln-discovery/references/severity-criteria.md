# Vulnerability Severity Criteria

## Overview

Severity is determined by intersecting **Impact** (what happens if exploited) with **Exploitability** (how easy it is to exploit). The resulting cell in the matrix gives the base severity, which is then adjusted by category-specific guidance and reachability.

---

## Impact Axis

| Level | Impact | Description |
|-------|--------|-------------|
| I5 | Data breach / RCE | Attacker reads/writes arbitrary data or executes arbitrary code |
| I4 | Privilege escalation | Attacker gains elevated privileges (e.g., user → admin, tenant → org) |
| I3 | Denial of service | Service becomes unavailable or data integrity is destroyed |
| I2 | Information disclosure | Sensitive data leaked (secrets, PII, internal state) but no write/exec |
| I1 | None / minimal | No direct confidentiality/integrity/availability impact |

## Exploitability Axis

| Level | Exploitability | Description |
|-------|---------------|-------------|
| E5 | Trivial | No authentication required; single HTTP request or CLI command |
| E4 | Easy | Auth required but easy to obtain; simple payload construction |
| E3 | Moderate | Specific preconditions (particular config, user role, timing) |
| E2 | Difficult | Race window, multi-step chain, or unusual environment needed |
| E1 | Theoretical | No known exploit path; requires future discovery to become practical |

---

## Severity Matrix

| Impact \ Exploitability | E5 Trivial | E4 Easy | E3 Moderate | E2 Difficult | E1 Theoretical |
|--------------------------|:----------:|:-------:|:------------:|:------------:|:--------------:|
| I5 Data breach / RCE    | Critical   | Critical | High         | Medium       | Low            |
| I4 Privilege escalation  | Critical   | High     | High         | Medium       | Low            |
| I3 DoS                   | High       | High     | Medium       | Low          | Info           |
| I2 Info disclosure       | Medium     | Medium   | Low          | Info         | Info           |
| I1 None / minimal        | Info       | Info     | Info         | Info         | Info           |

---

## Category-Specific Severity Guidance

The matrix gives a base rating. Apply category-specific floors or adjustments **after** looking up the matrix value, taking the **higher** of the two.

| Category | Minimum Severity | Rationale |
|----------|:----------------:|-----------|
| SQL injection | High | Proven data exfiltration class; even moderate-exploitability SQLi is High |
| Command injection / RCE | Critical | Full server takeover; no scenario below High |
| Path traversal | Medium-High | Can lead to config/secret read; downgrade to Medium only if sandboxed |
| XSS (reflected) | Medium | Browser-context escape; upgrade to High if auth cookies are accessible |
| XSS (stored) | Medium-High | Persistent, hits all viewers; at least Medium-High |
| CSRF | Medium | Depends on target action; High if targets privileged state change |
| SSRF | High | Internal network pivot; at least High unless cloud metadata is blocked |
| Auth bypass | Critical | Eliminates exploitability barrier; always Critical |
| Broken access control | High | Horizontal/vertical privilege escalation floor is High |
| Information disclosure | Low–Info | No integrity/availability impact; Low for sensitive data, Info otherwise |
| DoS (amplification) | Medium-High | One request causing disproportionate resource consumption |
| DoS (resource exhaustion) | Medium | Requires sustained effort; Medium floor unless single-request trigger |
| Race condition | Medium | Exploitability is inherently moderate; never below Medium if impact ≥ I3 |
| Cryptographic weakness | Low–Medium | Depends on context; Medium if secrets are directly recoverable |
| Misconfiguration | Low–Medium | Low if defense-in-depth; Medium if directly exploitable |

### Applying the Floor

1. Look up the matrix value using impact × exploitability.
2. Look up the category floor.
3. The final base severity is `max(matrix_value, category_floor)`.

---

## Reachability Adjustment

After computing the base severity, adjust based on how reachable the vulnerability is from an attacker's entry point.

| Reachability | Adjustment | Example |
|--------------|------------|---------|
| **Reachable** | No change. Severity stays as computed. | An unauthenticated endpoint calls the vulnerable function directly. |
| **Partially reachable** | Lower by one level (e.g., High → Medium). | The vulnerable path exists behind an internal API not directly exposed, but could be reached via SSRF or another vulnerability. |
| **Unreachable** | Cap at **Info** (defense-in-depth). | The vulnerable code exists in an unused code path or a dead route with no caller. Document for hardening, but do not inflate the finding. |

### Reachability Assessment Rules

- A path is **reachable** if an external request can trigger it without chaining through another vulnerability.
- A path is **partially reachable** if it requires chaining through one other finding to reach.
- A path is **unreachable** if no reasonable request flow reaches it, even when considering other confirmed findings.

---

## Severity Level Definitions & Examples

### Critical
- **Definition**: Immediate, severe impact with trivial-to-easy exploitation. Unauthenticated RCE, data breach, or auth bypass.
- **Examples**:
  - Unauthenticated SQL injection on a login endpoint returning all user records.
  - Unauthenticated command injection via a webhook handler.
  - Auth bypass allowing any user to access admin endpoints without credentials.

### High
- **Definition**: Significant impact with reachable exploitation. Privilege escalation, authenticated RCE, or serious SSRF.
- **Examples**:
  - Authenticated SSRF hitting cloud metadata endpoint (169.254.169.254).
  - Horizontal privilege escalation letting user A read user B's private data.
  - Stored XSS in an admin panel that steals admin session cookies.

### Medium
- **Definition**: Moderate impact or moderate exploitability. Information disclosure of sensitive data, DoS with moderate effort.
- **Examples**:
  - Reflected XSS requiring user interaction on a non-privileged page.
  - Verbose error messages leaking stack traces and internal paths on failed requests.
  - Denial of service via resource exhaustion requiring sustained requests.

### Low
- **Definition**: Limited impact or difficult exploitation. Theoretical chains, minor info leaks, or defense-in-depth gaps.
- **Examples**:
  - Theoretical timing side-channel on a password comparison (difficult exploitation).
  - Internal IP address disclosure in debug headers (minimal security impact).
  - Race condition requiring a narrow window and authenticated access.

### Info
- **Definition**: No direct security impact under current conditions. Useful for hardening recommendations.
- **Examples**:
  - Missing security header (e.g., X-Content-Type-Options) with no known exploit path.
  - Unreachable code path containing a deprecated crypto call.
  - Verbose 404 page revealing framework version with no other impact.

---

## Quick Reference: Final Severity Algorithm

```
1. impact    ← determine_impact(finding)
2. exploit   ← determine_exploitability(finding)
3. base      ← MATRIX[impact][exploit]
4. floor     ← CATEGORY_FLOOR[finding.category]
5. severity  ← max(base, floor)
6. severity  ← adjust_for_reachability(severity, finding.reachability)
7. return severity
```

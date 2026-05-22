# Finding: F-001

## Core Fields

| Field            | Value                                                                 |
|------------------|-----------------------------------------------------------------------|
| **finding_id**   | F-001                                                                 |
| **title**        | SQL Injection in task search endpoint                                 |
| **category**     | INJ-01 (SQL Injection)                                                |
| **severity**     | Critical                                                              |
| **confidence**   | confirmed                                                             |
| **reachability** | reachable                                                             |

---

## Locations

- Primary: `src/routes/tasks.js:47`

---

## Description

The `GET /api/tasks/search` endpoint accepts a `q` query parameter and interpolates it directly into a raw SQL `LIKE` clause without parameterization or escaping. An authenticated user can inject arbitrary SQL, enabling data exfiltration from the `tasks` and `users` tables, and potentially escalating to full database compromise via PostgreSQL superuser capabilities (e.g., `COPY TO`, `pg_dump`).

---

## Root Cause

String concatenation is used to build the SQL query instead of parameterized placeholders. The developer used `$1` for `userId` but failed to apply the same pattern to the `q` parameter.

**root_cause_id:** RC-INJ-001 — Direct string interpolation of user input into SQL query

```js
// src/routes/tasks.js:47
const result = await db.query(
  `SELECT * FROM tasks WHERE title LIKE '%${q}%' AND user_id = $1`,
  [userId]
);
```

The `$1` placeholder is correctly used for `userId`, but `q` is embedded via template literal — a classic parameterization gap.

---

## Attack Scenario

1. Attacker authenticates as any valid user (standard registration is open).
2. Attacker sends: `GET /api/tasks/search?q=%25'%20UNION%20SELECT%20id,username,password_hash,email,null,null%20FROM%20users--`
3. The server executes:
   ```sql
   SELECT * FROM tasks WHERE title LIKE '%%' UNION SELECT id,username,password_hash,email,null,null FROM users--%' AND user_id = $1
   ```
4. The `--` comment discards the trailing `AND user_id = $1`, bypassing the ownership filter.
5. The response contains every user's `password_hash` and `email`.
6. Attacker cracks bcrypt hashes offline or pivots to credential-stuffing.

---

## Attack Path

```
Entry Point:      GET /api/tasks/search?q=...  (authenticated route)
Intermediate:      authGuard middleware (valid JWT required — low barrier, open registration)
Sink:              db.query() — PostgreSQL execution with app-level DB user
Impact Zone:       Full read access to all tables; potential RCE via COPY/lo_export
```

---

## Evidence

```js
// src/routes/tasks.js:45-49
router.get('/search', authGuard, async (req, res) => {
  const { q } = req.query;
  const userId = req.user.id;
  const result = await db.query(
    `SELECT * FROM tasks WHERE title LIKE '%${q}%' AND user_id = $1`,
    [userId]
  );
  res.json(result.rows);
});
```

No sanitization, validation, or allow-list is applied to `q` before interpolation.

---

## Sanitization Checkpoints

| Checkpoint                          | Present? | Effective? |
|-------------------------------------|----------|------------|
| Input validation (allow-list)       | No       | —          |
| Input sanitization (escape)         | No       | —          |
| Parameterized query for `q`         | No       | —          |
| ORM / query builder abstraction     | No       | —          |
| WAF / SQL-injection rule            | Unknown  | N/A        |

---

## Impact

| Dimension       | Assessment                                                           |
|-----------------|----------------------------------------------------------------------|
| Confidentiality | Full DB read — all tables accessible via UNION-based injection        |
| Integrity       | Potential DB writes via stacked queries if multi-statement is enabled|
| Availability    | Denial-of-service via expensive queries (e.g., `pg_sleep`)          |
| Privilege       | Authenticated user → full database read; possible RCE via PostgreSQL|
| Scope           | All tenant data in the same PostgreSQL database                       |

---

## Remediation

1. **Parameterize the search query** — use a placeholder for `q`:
   ```js
   const result = await db.query(
     "SELECT * FROM tasks WHERE title LIKE $1 AND user_id = $2",
     [`%${q}%`, userId]
   );
   ```
2. **Validate input length and characters** — reject queries longer than 200 chars or containing non-printable characters.
3. **Grant least-privilege DB roles** — the app's PostgreSQL user should not own `users.password_hash` if not needed by this query.
4. **Add integration tests** — cover search with single-quote, `UNION`, and `;` inputs to confirm parameterization.

---

## Validation Notes

- Confirmed by code inspection: `q` is interpolated at line 47 with zero sanitization.
- Confirmed by dynamic test: sent `q=' OR 1=1--` and received rows belonging to other users.
- The `db.query()` function in `src/db/index.js:8` delegates directly to `pg.Pool.query` — no central sanitization hook.

---

## Dedup Notes

- No other finding covers SQL injection in `tasks.js`. The `INSERT` at line 38 and `DELETE` at line 131 use parameterized queries and are not vulnerable.
- This is the sole injection point in the task search flow.

---

## Trace Notes

- Discovered during Phase 2 (Hunt) via string-interpolation trail on `db.query` calls.
- Cross-referenced against Recon data flow D1 — task search was marked P0.
- Confirmed reachable: the route requires only a valid JWT, obtainable via open registration.

# Phase 1 — Recon Output: TaskFlow

## Target Scope

| Property      | Value                                        |
|---------------|----------------------------------------------|
| Application   | TaskFlow — project task management platform  |
| Stack         | Express.js 4.18 / PostgreSQL 15 / Node 20  |
| Repo root     | `/opt/taskflow`                              |
| Auth model    | JWT (jsonwebtokton) + bcrypt password hashing|
| Scope         | Full codebase — all HTTP handlers, middleware, DB queries |

---

## Entry Points

### HTTP Handlers (`src/routes/`)

| Route                   | Method | Handler File          | Auth Required |
|-------------------------|--------|-----------------------|---------------|
| `/api/auth/register`   | POST   | `auth.js:12`          | No            |
| `/api/auth/login`      | POST   | `auth.js:58`          | No            |
| `/api/tasks`            | GET    | `tasks.js:15`         | Yes           |
| `/api/tasks`            | POST   | `tasks.js:34`         | Yes           |
| `/api/tasks/search`     | GET    | `tasks.js:47`         | Yes           |
| `/api/tasks/:id`        | PUT    | `tasks.js:89`         | Yes (owner)   |
| `/api/tasks/:id`        | DELETE | `tasks.js:124`        | Yes (admin)   |
| `/api/admin/users`      | GET    | `admin.js:10`         | Yes (admin)   |
| `/api/admin/export`     | POST   | `admin.js:45`         | Yes (admin)   |

### Middleware (`src/middleware/`)

| Middleware        | File              | Notes                                |
|-------------------|-------------------|--------------------------------------|
| `authGuard`       | `auth.js:5`       | Verifies JWT, attaches `req.user`    |
| `adminOnly`       | `admin.js:3`      | Checks `req.user.role === 'admin'`   |
| `errorHandler`    | `errors.js:1`     | Catches unhandled errors, returns 500|
| `requestLogger`   | `logger.js:1`     | Logs method + path (no body logging)  |

---

## Data Flows

### D1 — Task Search (⚠️ priority trail)

```
User input (query param "q")
  → GET /api/tasks/search
  → authGuard (verifies JWT)
  → tasks.js:47  const result = await db.query(`SELECT * FROM tasks WHERE title LIKE '%${q}%' AND user_id = $1`, [userId])
  → PostgreSQL
  → JSON response
```

**Note:** `q` is interpolated directly into the SQL string before `$1` binding is used for `userId`. Classic string-concat injection surface.

### D2 — Admin CSV Export

```
Admin input (body: { format, filters })
  → POST /api/admin/export
  → authGuard → adminOnly
  → admin.js:45  execSync(`python3 export.py --format ${format} --filter '${filters.status}'`)
  → Shell subprocess
  → File written to /tmp, streamed back
```

**Note:** `format` and `filters.status` are passed unsanitized to `execSync`. Command injection possible.

### D3 — User Registration

```
User input (body: { email, password, name })
  → POST /api/auth/register
  → auth.js:12  bcrypt.hash(password, 10)
  → db.query('INSERT INTO users ...', [email, hash, name])
  → PostgreSQL
```

**Note:** Password is hashed before storage. Email validation is minimal (`includes('@')`).

### D4 — JWT Issuance

```
User input (body: { email, password })
  → POST /api/auth/login
  → auth.js:58  bcrypt.compare(password, storedHash)
  → jwt.sign({ id, role }, process.env.JWT_SECRET, { expiresIn: '24h' })
  → Response with token
```

**Note:** `JWT_SECRET` loaded from `.env` via dotenv. If `.env` is committed or default is used, secret is predictable.

---

## Trust Boundaries

```
┌─────────────────────────────────────────────────────────┐
│  Internet (Untrusted)                                    │
│    │                                                     │
│    ▼                                                     │
│  [Express HTTP Layer]  ← authGuard / adminOnly gate     │
│    │                                                     │
│    ├── Auth routes (public)  ← NO auth boundary          │
│    │                                                     │
│    ├── Task routes (authenticated)  ← JWT boundary       │
│    │                                                     │
│    └── Admin routes (admin-only)  ← role boundary       │
│         │                                                │
│         ▼                                                │
│  [Node.js Runtime]                                       │
│    │                                                     │
│    ├── pg.query()  ← SQL boundary (parameterized?)       │
│    │                                                     │
│    └── execSync()  ← OS command boundary (sanitized?)    │
│                                                          │
│    ▼                                                     │
│  [PostgreSQL / OS]  ← High-privilege zone                │
└─────────────────────────────────────────────────────────┘
```

---

## Module Map

```
src/
├── app.js              # Express app setup, middleware registration
├── routes/
│   ├── auth.js         # Register, login, token refresh
│   ├── tasks.js        # CRUD + search for tasks
│   └── admin.js        # User management, CSV export
├── middleware/
│   ├── auth.js         # authGuard (JWT verify)
│   ├── admin.js        # adminOnly role check
│   ├── errors.js       # Central error handler
│   └── logger.js       # Request logging
├── db/
│   └── index.js        # pg Pool singleton, exposes .query()
├── utils/
│   ├── validators.js   # Input validation helpers
│   └── export.py        # Python script for CSV/PDF export
├── config/
│   └── index.js        # Loads dotenv, exports config object
└── tests/
    └── ...             # Unit + integration tests (sparse)
```

---

## Dependencies

| Package        | Version | Known Issues                            |
|----------------|---------|------------------------------------------|
| express        | 4.18.2  | None critical                            |
| pg             | 8.11.3  | Safe if parameterized queries used        |
| bcrypt         | 5.1.1   | None                                     |
| jsonwebtoken   | 9.0.2   | None (but depends on secret strength)    |
| dotenv         | 16.3.1  | Config risk if `.env` is committed        |
| morgan         | 1.10.0  | None                                     |

---

## Privileged Operations

| Operation                 | File              | Line | Risk          |
|---------------------------|-------------------|------|---------------|
| SQL query (SELECT)        | `tasks.js`        | 47   | Injection     |
| SQL query (INSERT/UPDATE) | `tasks.js`        | 38   | Injection     |
| SQL query (DELETE)        | `tasks.js`        | 131  | Injection     |
| OS command (execSync)     | `admin.js`        | 48   | Cmd injection |
| File read (stream)        | `admin.js`        | 52   | Path traversal|

---

## Hunt Planning — Priority Trails

| Priority | Trail                                       | Rationale                                              |
|----------|---------------------------------------------|--------------------------------------------------------|
| 🔴 P0    | SQL injection in task search                | Direct string interpolation into `db.query()` — confirmed pattern |
| 🔴 P0    | Command injection in admin export            | `execSync` with unsanitized user input                |
| 🟡 P1    | Hardcoded/default JWT secret                | Check `.env.example` and `config/index.js` fallbacks |
| 🟡 P1    | IDOR on task PUT/DELETE                      | Owner checks may be bypassable via `:id` parameter   |
| 🟢 P2    | Email validation bypass on registration     | Weak check (`includes('@')`) allows malformed emails |
| 🟢 P2    | Error information leakage                    | Stack traces in production error responses            |

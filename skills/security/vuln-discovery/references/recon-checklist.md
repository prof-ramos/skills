# Recon Phase Checklist

## Scope Definition

1. Default to the entire repository if the user does not specify scope.
2. If the user specifies a directory, module, or file, restrict scope accordingly.
3. Record the scope boundary explicitly (which directories are in/out of scope).

## File Enumeration

1. Run `rg --files` to list source files. Exclude generated, vendored, and dependency directories (`node_modules/`, `vendor/`, `dist/`, `build/`, `__pycache__/`, `.git/`).
2. Identify the technology stack from manifest files:
   - `package.json` → Node.js
   - `requirements.txt` / `pyproject.toml` / `setup.py` → Python
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `pom.xml` / `build.gradle` → Java
   - `Gemfile` → Ruby
   - `composer.json` → PHP
3. Identify framework from imports/dependencies:
   - Express, NestJS, Fastify → Node.js web
   - Django, Flask, FastAPI → Python web
   - Spring Boot → Java web
   - Rails → Ruby web
   - Laravel → PHP web
   - Gin, Echo → Go web
   - Actix, Axum → Rust web

## Architecture Document Template

Fill in every section. Mark sections as N/A only if the codebase genuinely does not contain the relevant surface.

```markdown
# Architecture Document — [Target Name]

## 1. Technology Stack
- Language(s):
- Framework(s):
- Database(s):
- Build system:
- Key dependencies (with versions):

## 2. Entry Points
| Entry Point | Type | File | Auth Required? |
|------------|------|------|---------------|
| /api/users | HTTP GET | src/routes/users.ts | Yes |

## 3. Data Flows
For each data flow, trace from entry point to sink:
- Source → [transformations] → Sink

## 4. Trust Boundaries
| Boundary | Location | Type |
|----------|----------|------|
| Auth middleware | src/middleware/auth.ts | Authentication gate |
| RBAC check | src/utils/permissions.ts | Authorization gate |

## 5. Module Map
| Module/Directory | Responsibility | LOC (approx) | Risk Level |
|-----------------|---------------|-------------|------------|
| src/routes/ | HTTP handlers | ~800 | High |
| src/db/ | Database queries | ~400 | High |
| src/utils/ | Utility functions | ~200 | Low |

## 6. Dependencies
| Dependency | Version | Known Issues |
|-----------|---------|-------------|
| express | 4.17.1 | No critical CVEs |

## 7. Privileged Operations
| Operation | File | Risk |
|-----------|------|------|
| SQL queries | src/db/queries.ts | Injection |
| File writes | src/services/upload.ts | Path traversal |
| Command execution | src/utils/shell.ts | Command injection |

## 8. Attack Surface Summary
Ranked list of highest-risk areas for hunting focus:
1. [Highest risk area] — [reason]
2. [Next highest] — [reason]
3. ...
```

## Language-Specific Recon

### Python/Flask/Django
- Check `app.route` decorators, URL patterns, middleware
- Look for `eval()`, `exec()`, `pickle.loads()`, `subprocess.call()`
- Identify ORM usage (SQLAlchemy, Django ORM) vs raw SQL

### Node.js/Express
- Check `router.get/post/put/delete`, middleware chain
- Look for `eval()`, `child_process.exec()`, template engines
- Identify input sources: `req.query`, `req.params`, `req.body`, `req.headers`

### Java/Spring
- Check `@RequestMapping`, `@GetMapping`, `@PostMapping`
- Look for `Runtime.exec()`, `ProcessBuilder`, JPA native queries
- Identify Spring Security filters and method-level security

### Go
- Check `http.HandleFunc`, `mux.HandleFunc`, Gin/Echo routes
- Look for `os/exec.Command()`, `fmt.Sprintf` in SQL
- Identify middleware chain and auth checks

### Rust
- Check route handlers in web frameworks (Actix, Axum, Rocket)
- Look for `unsafe` blocks, raw pointer operations
- Identify `unwrap()` calls on user-controlled data

## Segmentation Strategy

Divide the codebase into segments for parallel Hunt agents:

### By module (preferred)
- Group by directory/module (e.g., `src/auth/`, `src/api/`, `src/db/`)
- Each segment should be 200–2000 LOC ideally
- Merge very small modules; split very large ones

### By entry point (for API-heavy codebases)
- Group by API endpoint prefix (e.g., `/api/users/*`, `/api/admin/*`)
- Each segment covers all handlers for one prefix

### By data flow (for complex pipelines)
- Group by data flow path (e.g., "upload pipeline", "payment pipeline")
- Each segment covers the full path from entry to sink

### Allocation rules
- Each segment should be assigned to at least one trail
- High-risk segments (entry points, privileged operations) should be covered by all 7 trails
- Low-risk segments (utilities, config) need only 1–2 trails
- Target total: segment_count × avg_trails_per_segment ≈ 40–60 agent-scopes

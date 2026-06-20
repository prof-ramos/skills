# Coding Standards

Team-wide coding standards covering style, structure, tooling, and workflow across all supported languages.

---

## General Principles

1. **Clarity over cleverness.** Code is read far more than it is written. A clear, slightly verbose solution beats a terse, opaque one.
2. **Explicit over implicit.** Avoid magic values, hidden conventions, and surprising side effects.
3. **Small units.** Functions under 40 lines, files under 400 lines, PRs under 400 changed lines.
4. **No premature abstraction.** Duplicate three times, then extract. A wrong abstraction is worse than repetition.
5. **Fail loudly.** Return errors or throw exceptions immediately when invariants are violated; don't silently swallow failures.

---

## Naming Conventions

| Construct | TypeScript/JS | Python | Go | Swift | Kotlin |
|-----------|--------------|--------|----|-------|--------|
| Variables | `camelCase` | `snake_case` | `camelCase` | `camelCase` | `camelCase` |
| Functions | `camelCase` | `snake_case` | `camelCase` | `camelCase` | `camelCase` |
| Classes/Types | `PascalCase` | `PascalCase` | `PascalCase` | `PascalCase` | `PascalCase` |
| Constants | `SCREAMING_SNAKE` | `SCREAMING_SNAKE` | `CamelCase` (exported) | `camelCase` | `SCREAMING_SNAKE` |
| Files | `kebab-case.ts` | `snake_case.py` | `snake_case.go` | `PascalCase.swift` | `PascalCase.kt` |

**Rule:** names should explain intent, not implementation. `userAccountBalance` not `uab` or `value`.

---

## File & Module Structure

```
src/
  domain/          # business logic — no framework imports
  application/     # use cases / services
  infrastructure/  # DB, HTTP, external APIs
  interfaces/      # controllers, CLI handlers, GraphQL resolvers
tests/
  unit/
  integration/
  e2e/
```

- One exported symbol per file (classes, large interfaces)
- Group related small utilities in a single file (`date-utils.ts`, `string_helpers.py`)
- Never mix domain logic and infrastructure in the same file

---

## TypeScript Standards

```typescript
// ✅ Explicit return types on public APIs
export function parseUserId(raw: string): number {
  const id = parseInt(raw, 10);
  if (Number.isNaN(id)) throw new Error(`Invalid user id: ${raw}`);
  return id;
}

// ✅ Readonly where mutation is unexpected
type Config = Readonly<{
  apiUrl: string;
  timeout: number;
}>;

// ✅ Discriminated unions for state
type RequestState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: User }
  | { status: "error"; error: Error };

// ❌ Avoid
const result: any = await fetch(url);  // loses type safety
```

**Tooling:**
- `tsc --strict` (no exceptions)
- `eslint` with `@typescript-eslint/recommended`
- `prettier` for formatting (no debates)
- `vitest` or `jest` for tests

---

## Python Standards

```python
# ✅ Type annotations everywhere
def get_user(user_id: int, db: Session) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

# ✅ Dataclasses for plain data
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

# ✅ Context managers for resources
with open(path, encoding="utf-8") as f:
    data = f.read()

# ❌ Avoid
def append_item(item, lst=[]):  # mutable default — shared across calls
    lst.append(item)
    return lst
```

**Tooling:**
- `ruff` for linting + formatting
- `mypy --strict` for type checking
- `pytest` for tests
- `pip-audit` for dependency CVE scanning

---

## Go Standards

```go
// ✅ Always handle errors explicitly
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doSomething: %w", err)
}

// ✅ Table-driven tests
tests := []struct {
    name     string
    input    string
    expected int
}{
    {"empty", "", 0},
    {"single digit", "5", 5},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got := parse(tt.input)
        require.Equal(t, tt.expected, got)
    })
}

// ✅ Context for cancellation
func Fetch(ctx context.Context, url string) ([]byte, error) {
    req, _ := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    // ...
}
```

**Tooling:**
- `golangci-lint` (with `errcheck`, `govet`, `staticcheck`)
- `govulncheck` for dependency scanning
- `testify` for assertions

---

## React / Next.js Standards

```tsx
// ✅ Prefer server components by default; opt-in to client
"use client"; // only when needed (event handlers, hooks, browser APIs)

// ✅ Co-locate types with the component
type ButtonProps = {
  label: string;
  onClick: () => void;
  disabled?: boolean;
};

export function Button({ label, onClick, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled} type="button">
      {label}
    </button>
  );
}

// ❌ Avoid index.ts barrel re-exports for large modules — they break tree-shaking
```

---

## API Design

- Use `camelCase` for JSON keys in REST APIs
- Return 400 for client errors with a structured body: `{ "error": "message", "code": "VALIDATION_ERROR" }`
- Return 500 only for unexpected server errors; never expose stack traces
- Version APIs under `/v1/` from the start — retrofitting is painful
- Paginate any list endpoint from day one (`limit`, `cursor`)
- Use ISO 8601 (`2024-01-15T12:00:00Z`) for all datetime fields

---

## Database

- All schema changes go through migration files (no manual `ALTER TABLE`)
- Add indexes before the column is queried in production
- Avoid `SELECT *` — list columns explicitly
- Use transactions for multi-step writes; never leave partial state
- Soft-delete over hard-delete when audit trails matter (`deleted_at TIMESTAMPTZ`)
- Store passwords as bcrypt/argon2 hashes — never plain text or MD5/SHA1

---

## Git Workflow

```
main          # always deployable
└── feat/TICKET-123-short-description
└── fix/TICKET-456-what-was-broken
└── chore/upgrade-dependencies
```

**Commit message format (Conventional Commits):**
```
<type>(<scope>): <short summary>

[optional body explaining WHY, not WHAT]

[optional footer: Closes #123]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`

**Rules:**
- Commits must build and pass tests in isolation
- Squash or rebase before merging — no merge commits on `main`
- PR title = first line of the squashed commit message
- Every PR needs at least one reviewer approval before merge

---

## CI/CD Gates (all must pass before merge)

- [ ] Type checker (`tsc`, `mypy`, `go vet`)
- [ ] Linter (`eslint`, `ruff`, `golangci-lint`)
- [ ] Unit tests (≥ 80 % coverage on changed lines)
- [ ] Security scan (`npm audit`, `pip-audit`, `govulncheck`)
- [ ] Build succeeds

---

## Secrets Management

| ❌ Never | ✅ Instead |
|---------|-----------|
| `.env` committed to git | `.env.example` with placeholder values; real secrets in CI/CD variables |
| Hardcoded API keys in source | Environment variables loaded at runtime |
| Secrets in log output | Redact with `***` or structured logging filters |
| Secrets in URL query params | POST body or Authorization header |

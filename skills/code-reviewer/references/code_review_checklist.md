# Code Review Checklist

A practical, language-agnostic checklist for reviewing pull requests. Work through each section before approving.

---

## 1. Correctness

| Check | Guidance |
|-------|----------|
| Logic matches intent | Read the PR description, then verify the code does exactly that — nothing more, nothing less. |
| Edge cases handled | Empty collections, `null`/`nil`/`undefined`, zero, negative numbers, very large inputs. |
| Off-by-one errors | Verify loop bounds, slice indices, and pagination math manually. |
| Concurrency safety | Shared state accessed from multiple goroutines/threads must be guarded. |
| Return values checked | Especially error returns in Go; unhandled errors hide bugs. |
| State machines valid | Every state transition should be reachable and every terminal state defined. |

**Red flags:**
- Functions longer than 50–80 lines without clear sub-operations
- Nested conditionals deeper than 3 levels
- Magic numbers with no explanation

---

## 2. Security

| Check | Guidance |
|-------|----------|
| No hardcoded secrets | Credentials belong in environment variables or a secrets manager — never in source. |
| Input validation | All data arriving from outside the process boundary (HTTP, CLI, files, queues) must be validated before use. |
| Parameterized queries | Never concatenate user input into SQL strings. Use prepared statements or ORM query builders. |
| Shell injection | Avoid `shell=True` / `exec()` / `eval()` with user-supplied data. Prefer `subprocess` with a list arg. |
| Auth not bypassed | New routes, endpoints, or file handlers must go through the same auth/authz middleware as existing ones. |
| Dependency versions | New packages should be pinned; check for known CVEs with `pip audit`, `npm audit`, or `govulncheck`. |
| Sensitive data in logs | PII, tokens, and passwords must never appear in log output. |

**Patterns to reject:**
```python
# BAD — SQL injection
query = "SELECT * FROM users WHERE id = " + user_id

# GOOD — parameterized
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

```bash
# BAD — shell injection
subprocess.call(f"ls {user_path}", shell=True)

# GOOD — list form
subprocess.run(["ls", user_path])
```

---

## 3. Performance

| Check | Guidance |
|-------|----------|
| N+1 queries | A query inside a loop that iterates over DB results is almost always wrong. |
| Unbounded fetches | Queries without `LIMIT` will explode on large tables. |
| Unnecessary allocations | Creating large objects inside hot loops drives GC pressure. |
| Caching correctness | Cache TTLs must be short enough that stale data doesn't cause user-visible bugs. |
| Async vs sync | Blocking I/O on an async thread kills throughput; use async clients or thread pools. |

**Benchmark before optimizing:** only optimize when a profiler identifies the hot path. Premature micro-optimization makes code harder to read.

---

## 4. Maintainability

| Check | Guidance |
|-------|----------|
| Naming clarity | Variables, functions, and types should explain their purpose without comments. |
| Single responsibility | Each function does one thing; each module owns one concern. |
| No dead code | Commented-out blocks and unused variables should be deleted, not committed. |
| TODOs tracked | A `TODO` is only acceptable if there is a linked issue tracking it. |
| Cyclomatic complexity | Keep functions below CC 10; anything above 20 is a refactor candidate. |
| Magic strings/numbers | Extract constants with descriptive names. |

---

## 5. Tests

| Check | Guidance |
|-------|----------|
| Coverage of changed logic | Every new branch in the diff should have at least one test exercising it. |
| Tests are meaningful | A test that always passes regardless of implementation is not a test. |
| Deterministic | No `time.Now()`, `rand.Intn()`, or external network calls in unit tests. |
| Fast | Unit tests must run in milliseconds; slow tests belong in an integration suite. |
| Descriptive names | `test_user_login_fails_with_wrong_password` beats `test_login_2`. |
| Test isolation | Tests must not depend on execution order or shared mutable state. |

---

## 6. Documentation

| Check | Guidance |
|-------|----------|
| Public API documented | Exported functions, types, and constants need at least one-line doc comments. |
| Complex logic explained | The *why* (not the what) should be captured in a comment where a future reader would be confused. |
| README updated | If the change affects setup, configuration, or usage, update the README. |
| Changelog entry | Breaking changes and new features should have a changelog entry. |

---

## 7. Language-Specific Notes

### TypeScript / JavaScript
- Prefer `unknown` over `any`; use type guards to narrow
- `async`/`await` over raw `.then()` chains
- `const` by default, `let` only when reassignment is needed
- Avoid `!` non-null assertions without a comment explaining why it's safe

### Python
- Use type hints (`def foo(x: int) -> str`)
- Never use mutable default arguments (`def f(lst=[])`)
- Prefer explicit exception types over bare `except:`
- Use context managers (`with open(...)`) for resource cleanup

### Go
- Always handle returned errors — no `_` for error values
- Prefer table-driven tests
- Avoid `init()` for business logic
- Use `context.Context` for cancellation propagation

### Swift / Kotlin
- Prefer value types (structs / data classes) over reference types for pure data
- Force-unwrap (`!` / `!!`) requires a justification comment
- Use `Result` / `sealed class` over unchecked exceptions for expected failure modes

---

## Quick Approval Criteria

A PR is ready to approve when:

1. It does what it says in the description
2. No security red flags remain
3. Changed logic has test coverage
4. No obvious performance regressions
5. The checklist above has no unchecked blockers

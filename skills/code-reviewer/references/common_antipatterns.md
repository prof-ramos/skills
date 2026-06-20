# Common Antipatterns

A catalogue of recurring mistakes across TypeScript, JavaScript, Python, Go, Swift, and Kotlin — with explanations and corrected examples.

---

## Security Antipatterns

### AP-SEC-001 — Hardcoded Credentials

**Languages:** All

```python
# ❌ Antipattern
DATABASE_URL = "postgresql://admin:hunter2@prod-db.example.com/app"
API_KEY = "sk-prod-abc123xyz"
```

**Why it's wrong:** Credentials committed to git are permanently exposed — even after deletion, they remain in history. Attackers routinely scan public repos for leaked secrets.

**Fix:**
```python
# ✅ Load from environment
import os
DATABASE_URL = os.environ["DATABASE_URL"]
API_KEY = os.environ["API_KEY"]
```

Use a secrets manager (AWS Secrets Manager, HashiCorp Vault, Doppler) for production.

---

### AP-SEC-002 — SQL Injection via String Concatenation

**Languages:** Python, TypeScript/JS, Go

```python
# ❌ Antipattern
def get_user(username: str) -> User:
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)
```

**Why it's wrong:** A `username` of `'; DROP TABLE users; --` deletes your database.

**Fix:**
```python
# ✅ Parameterized query
def get_user(username: str) -> User | None:
    return db.execute("SELECT * FROM users WHERE username = %s", (username,)).fetchone()
```

---

### AP-SEC-003 — Shell Injection

**Languages:** Python, Node.js

```python
# ❌ Antipattern
import subprocess
filename = request.args.get("file")
subprocess.call(f"convert {filename} output.pdf", shell=True)
```

**Why it's wrong:** `filename = "x; rm -rf /"` runs arbitrary commands.

**Fix:**
```python
# ✅ List form — no shell interpolation
import subprocess, shlex, pathlib

filename = request.args.get("file", "")
safe_path = pathlib.Path(filename).resolve()
subprocess.run(["convert", str(safe_path), "output.pdf"], check=True)
```

---

### AP-SEC-004 — eval() / exec() on User Input

**Languages:** Python, JavaScript/TypeScript

```javascript
// ❌ Antipattern
const formula = req.query.formula;
const result = eval(formula);  // executes arbitrary JS
```

**Fix:** Use a sandboxed expression evaluator library (`mathjs`, `expr-eval`) or a restricted DSL parser. Never pass user data to `eval`.

---

### AP-SEC-005 — Weak Hashing for Passwords

**Languages:** All

```python
# ❌ Antipattern
import hashlib
stored = hashlib.md5(password.encode()).hexdigest()
```

**Why it's wrong:** MD5 and SHA1 are not password hashing algorithms. They are fast by design; attackers can crack billions of hashes per second with GPUs.

**Fix:**
```python
# ✅ bcrypt or argon2
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
```

---

## Correctness Antipatterns

### AP-COR-001 — Mutable Default Argument (Python)

```python
# ❌ Antipattern — the list is shared across ALL calls
def append(item, lst=[]):
    lst.append(item)
    return lst

append(1)  # [1]
append(2)  # [1, 2] — unexpected!
```

**Fix:**
```python
# ✅ Use None sentinel
def append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

---

### AP-COR-002 — Ignoring Errors (Go)

```go
// ❌ Antipattern
data, _ := ioutil.ReadFile(path)
process(data)  // data is nil if the file didn't exist
```

**Fix:**
```go
// ✅ Always check errors
data, err := os.ReadFile(path)
if err != nil {
    return fmt.Errorf("reading %s: %w", path, err)
}
process(data)
```

---

### AP-COR-003 — Race Condition on Shared State

**Languages:** Go, Swift, Kotlin

```go
// ❌ Antipattern — concurrent map writes panic at runtime
var cache = map[string]int{}

func increment(key string) {
    cache[key]++ // data race
}
```

**Fix:**
```go
// ✅ Protect with sync.Mutex or use sync.Map
var (
    mu    sync.Mutex
    cache = map[string]int{}
)

func increment(key string) {
    mu.Lock()
    defer mu.Unlock()
    cache[key]++
}
```

---

### AP-COR-004 — Floating-Point for Money

```typescript
// ❌ Antipattern
const total = 0.1 + 0.2;  // 0.30000000000000004
```

**Fix:** Represent money as integer cents, or use a decimal library (`decimal.js`, Python's `decimal.Decimal`).

---

## Performance Antipatterns

### AP-PERF-001 — N+1 Query

**Languages:** All ORMs

```python
# ❌ Antipattern — 1 query for orders + N queries for users
orders = Order.objects.all()
for order in orders:
    print(order.user.name)  # triggers a new SELECT per iteration
```

**Fix:**
```python
# ✅ Eager-load with select_related / JOIN
orders = Order.objects.select_related("user").all()
for order in orders:
    print(order.user.name)  # no extra queries
```

---

### AP-PERF-002 — Unbounded Queries

```typescript
// ❌ Antipattern
const users = await db.user.findMany();  // fetches entire table
```

**Fix:**
```typescript
// ✅ Always paginate
const users = await db.user.findMany({
  take: 100,
  cursor: cursor ? { id: cursor } : undefined,
  orderBy: { id: "asc" },
});
```

---

### AP-PERF-003 — Blocking I/O in Async Context

```typescript
// ❌ Antipattern — blocks the event loop
import fs from "fs";
const data = fs.readFileSync("large-file.txt");
```

**Fix:**
```typescript
// ✅ Async I/O
import { readFile } from "fs/promises";
const data = await readFile("large-file.txt", "utf-8");
```

---

### AP-PERF-004 — String Concatenation in a Loop

```python
# ❌ Antipattern — O(n²) copies
result = ""
for item in large_list:
    result += str(item)  # allocates a new string each iteration
```

**Fix:**
```python
# ✅ join() — single allocation
result = "".join(str(item) for item in large_list)
```

---

## Maintainability Antipatterns

### AP-MAINT-001 — God Function

```python
# ❌ Antipattern — 300-line function doing everything
def process_order(order_id):
    # fetch from DB
    # validate inventory
    # calculate pricing
    # apply discount codes
    # charge payment
    # send confirmation email
    # update analytics
    ...
```

**Fix:** Extract each responsibility into its own function. Aim for functions that fit on one screen (~40 lines).

---

### AP-MAINT-002 — Boolean Trap

```typescript
// ❌ Antipattern — what does true mean?
updateUser(user, true, false, true);
```

**Fix:**
```typescript
// ✅ Named options object
updateUser(user, { notify: true, sendEmail: false, audit: true });
```

---

### AP-MAINT-003 — Primitive Obsession

```python
# ❌ Antipattern — what unit is duration? what range is valid?
def schedule_job(job_id: int, duration: int, retries: int) -> None: ...
```

**Fix:** Wrap primitives in domain types that encode invariants:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Duration:
    seconds: int

    def __post_init__(self):
        if self.seconds <= 0:
            raise ValueError("Duration must be positive")
```

---

### AP-MAINT-004 — Deep Callback / Promise Nesting

```javascript
// ❌ Antipattern — "callback hell"
fetchUser(id, function(user) {
  fetchOrders(user.id, function(orders) {
    fetchItems(orders[0].id, function(items) {
      render(user, orders, items);
    });
  });
});
```

**Fix:**
```typescript
// ✅ async/await
const user = await fetchUser(id);
const orders = await fetchOrders(user.id);
const items = await fetchItems(orders[0].id);
render(user, orders, items);
```

---

### AP-MAINT-005 — Magic Numbers and Strings

```go
// ❌ Antipattern
if status == 3 {
    retry()
}
if role == "adm" {
    grantAccess()
}
```

**Fix:**
```go
// ✅ Named constants
const StatusRetryable = 3

type Role string
const RoleAdmin Role = "admin"

if status == StatusRetryable {
    retry()
}
if role == RoleAdmin {
    grantAccess()
}
```

---

## Testing Antipatterns

### AP-TEST-001 — Testing Implementation Instead of Behaviour

```python
# ❌ Antipattern — testing private internals
def test_cache_key_format():
    svc = UserService()
    assert svc._build_cache_key(42) == "user:42"  # implementation detail
```

**Fix:** Test observable output — what the function returns or what side effects it produces — not how it works internally.

---

### AP-TEST-002 — Flaky Time-Dependent Tests

```python
# ❌ Antipattern — fails at midnight, on slow CI, etc.
def test_token_not_expired():
    token = create_token(expires_in=3600)
    time.sleep(1)
    assert not token.is_expired()
```

**Fix:** Inject a clock dependency and control it in tests:
```python
def test_token_not_expired():
    now = datetime(2024, 1, 1, 12, 0, 0)
    token = create_token(expires_in=3600, issued_at=now)
    assert not token.is_expired(at=now + timedelta(seconds=100))
```

---

### AP-TEST-003 — Coverage Padding

```python
# ❌ Antipattern — assertion never fails, but coverage shows 100 %
def test_divide():
    result = divide(10, 2)
    assert result is not None  # doesn't verify correctness
```

**Fix:**
```python
def test_divide():
    assert divide(10, 2) == 5.0
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

---

## Quick Reference — Rule IDs

| ID | Antipattern |
|----|-------------|
| AP-SEC-001 | Hardcoded credentials |
| AP-SEC-002 | SQL injection via string concat |
| AP-SEC-003 | Shell injection via shell=True |
| AP-SEC-004 | eval/exec on user input |
| AP-SEC-005 | Weak password hashing |
| AP-COR-001 | Mutable default argument |
| AP-COR-002 | Ignored errors (Go) |
| AP-COR-003 | Race condition on shared state |
| AP-COR-004 | Float arithmetic for money |
| AP-PERF-001 | N+1 database query |
| AP-PERF-002 | Unbounded query |
| AP-PERF-003 | Blocking I/O in async |
| AP-PERF-004 | String concat in loop |
| AP-MAINT-001 | God function |
| AP-MAINT-002 | Boolean trap |
| AP-MAINT-003 | Primitive obsession |
| AP-MAINT-004 | Deep callback nesting |
| AP-MAINT-005 | Magic numbers/strings |
| AP-TEST-001 | Testing implementation not behaviour |
| AP-TEST-002 | Time-dependent flaky tests |
| AP-TEST-003 | Coverage padding |

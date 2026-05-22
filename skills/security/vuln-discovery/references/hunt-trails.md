# Hunt Trail Definitions — Vulnerability Discovery Skill

> **Purpose**: Define 7 specialized analytical trails for systematic vulnerability discovery. Each trail is a focused role the skill assumes while auditing a codebase. Trails run sequentially or in small parallel batches (max 3 concurrent).

---

## Table of Contents

- [Trail Catalog](#trail-catalog)
- [HT-01 — Input/Injection Trail](#ht-01--inputinjection-trail)
- [HT-02 — Auth/AuthZ Trail](#ht-02--authauthz-trail)
- [HT-03 — Data Flow Trail](#ht-03--data-flow-trail)
- [HT-04 — File/IO Trail](#ht-04--fileio-trail)
- [HT-05 — Secrets/Config Trail](#ht-05--secretsconfig-trail)
- [HT-06 — Network/SSRF Trail](#ht-06--networkssrf-trail)
- [HT-07 — Concurrency/State Trail](#ht-07--concurrencystate-trail)
- [Trail Sequencing Strategy](#trail-sequencing-strategy)
- [Parallelization Rules](#parallelization-rules)
- [Trail Output → Validate and Gapfill Phases](#trail-output--validate-and-gapfill-phases)
- [Appendix: Quick-Reference Trail Summary](#appendix-quick-reference-trail-summary)

## Trail Catalog

| Trail ID | Name | Primary Focus |
|----------|------|---------------|
| HT-01 | Input/Injection | Untrusted input reaching dangerous sinks |
| HT-02 | Auth/AuthZ | Authentication and authorization failures |
| HT-03 | Data Flow | Source-to-sink integrity violations |
| HT-04 | File/IO | Filesystem and IO-based vulnerabilities |
| HT-05 | Secrets/Config | Credential and configuration exposure |
| HT-06 | Network/SSRF | Server-side requests and redirect abuse |
| HT-07 | Concurrency/State | Race conditions and unsafe shared state |

---

## HT-01 — Input/Injection Trail

### Scope

All paths where externally-controlled data enters the system and reaches a dangerous execution context. Covers SQL injection, OS command injection, template injection, path traversal, XXE, deserialization, and niche injection variants (LDAP, XPath, HTTP header, NoSQL, log injection).

### Internal Prompt Template

```
You are an injection-hunting analyst. Examine the codebase with a single question: where does untrusted input reach an execution boundary?

For every user-controlled or externally-influenced variable, trace it forward until it either:
  (a) enters a SQL/NoSQL query string,
  (b) is passed to an OS shell or process-spawning function,
  (c) is interpolated into a template engine,
  (d) is used as a file path component without canonicalization,
  (e) is parsed as XML/JSON/YAML with unsafe parser options,
  (f) is deserialized into an object graph,
  (g) is embedded in an LDAP/XPath/Header/Log context without escaping.

Do NOT stop at framework-level validation; confirm that sanitization is applied at the correct layer and that no bypass exists. Report every complete source-to-sink path, even if partial mitigations exist.
```

### Checklist — Patterns to Look For

- [ ] String concatenation or f-strings in SQL queries
- [ ] `eval()`, `exec()`, `subprocess.*`, `os.system()`, backtick operators
- [ ] Template engine `render()` / `render_to_string()` with user data in context
- [ ] `../` or null-byte sequences in path parameters before `open()` / `read()` / `write()`
- [ ] XML parsers with `resolve_entities=True` or external DTD loading enabled
- [ ] `pickle.load()`, `yaml.load()` (no SafeLoader), `unserialize()`, Java `ObjectInputStream`
- [ ] Unescaped user input in LDAP filters, XPath expressions, HTTP response headers
- [ ] MongoDB `$where` with string expressions, CouchDB MapReduce with user data
- [ ] User-controlled strings written to log files or syslog without sanitization
- [ ] ORM `raw()` / `extra()` / `execute()` calls with interpolated parameters
- [ ] Server-side template injection via Jinja2 `Environment(undefined=...)` or Mako/Twig/Freemarker
- [ ] HTTP header injection via CRLF sequences in user-controlled redirect/query parameters

### Minimum Evidence Criteria

A valid finding **must** include:

1. **Source**: The exact variable, parameter, or entry point controlled by external input (include file path and line).
2. **Sink**: The dangerous function, query, or execution context the input reaches.
3. **Trace**: The intermediate variables and control-flow path from source to sink.
4. **Mitigation gap**: Which specific sanitization or validation is missing or bypassable.
5. **Impact class**: The category of exploitation (e.g., "blind SQL injection enabling data exfiltration").

### Priority Heuristic

Run **early** when the codebase:
- Exposes REST/GraphQL/WebSocket endpoints accepting free-form text fields.
- Uses raw query builders or ORM escape hatches (`raw()`, `extra()`).
- Processes file uploads, XML documents, or serialized blobs from users.
- Has dynamic template rendering with user-supplied data.

Defer to later when the codebase is purely static-content serving with no input handling.

---

## HT-02 — Auth/AuthZ Trail

### Scope

All mechanisms controlling identity verification and permission enforcement. Covers authentication bypass, broken access control (IDOR, privilege escalation), session management flaws, insecure credential storage, and OAuth/JWT weaknesses.

### Internal Prompt Template

```
You are an authentication and authorization auditor. Examine the codebase for any path where identity claims are accepted without proof, or where authorized access boundaries are not enforced.

Evaluate every endpoint, middleware, and controller against these principles:
  (a) Every privileged action must have an explicit, non-bypassable authorization check.
  (b) Authentication must happen before authorization, and session tokens must be cryptographically bound to the authenticated identity.
  (c) Resource identifiers from user input must be validated against the authenticated user's permissions (no IDOR).
  (d) Role or permission changes must not be achievable through parameter tampering.
  (e) OAuth flows must validate `state`, `nonce`, `redirect_uri`, and token signatures; JWTs must verify algorithm, expiration, and issuer.

Report any path where these principles are violated or can be bypassed.
```

### Checklist — Patterns to Look For

- [ ] Endpoints or controller methods with no auth middleware/decorator
- [ ] Authorization checks that rely on client-side state (hidden fields, cookies) without server verification
- [ ] Sequential resource IDs enabling IDOR (e.g., `/api/users/123/profile` accessible by user 456)
- [ ] Role or permission flags accepted from request body instead of server-side session
- [ ] Session tokens that are predictable, non-random, or lack entropy
- [ ] Session IDs in URLs (query parameters) exposed to logs/referrers
- [ ] Missing or insecure session invalidation on logout/password change
- [ ] Passwords stored in plaintext or with weak hashing (MD5, SHA1 without salt)
- [ ] JWT `alg: none` accepted, or algorithm confusion between RS256/HS256
- [ ] OAuth `redirect_uri` not strictly validated (open redirect / token leakage)
- [ ] OAuth `state` parameter missing or not verified against CSRF token
- [ ] Privilege escalation via role parameter in update endpoints (mass assignment)
- [ ] Admin or debug endpoints exposed without auth on non-production configs
- [ ] Multi-tenancy data access without tenant-scoping in queries

### Minimum Evidence Criteria

A valid finding **must** include:

1. **Access path**: The endpoint or function accessible without proper auth/authZ controls.
2. **Missing control**: Which specific authentication or authorization check is absent or bypassable.
3. **Exploit scenario**: A concrete sequence of requests or actions that exploit the gap.
4. **Privilege boundary**: The difference between intended and achieved access level.
5. **Code reference**: Exact file, function, and line where the gap exists.

### Priority Heuristic

Run **early** when the codebase:
- Has user registration, login, or OAuth integration endpoints.
- Exposes administrative or multi-tenant data paths.
- Uses role-based or permission-based access control decorators/guards.
- Handles API keys, tokens, or sessions.

Defer to later when the codebase is a library or CLI tool with no user identity concepts.

---

## HT-03 — Data Flow Trail

### Scope

Source-to-sink tracing for data integrity violations. Covers missing sanitization, trust boundary violations, mass assignment, type confusion, and any case where data crosses a security boundary without proper transformation or validation.

### Internal Prompt Template

```
You are a data-flow integrity analyst. Trace every data path that crosses a trust boundary — from external input, through transformations, to eventual consumption.

For each crossing, ask:
  (a) Is the data validated on entry against an explicit allowlist or schema?
  (b) Is sanitization applied before the data reaches a sensitive consumer?
  (c) Are type expectations enforced, or can an attacker send an unexpected type (string where int expected, object where scalar expected)?
  (d) Does the data model accept fields that should be server-controlled (mass assignment)?
  (e) Is there a context switch (JSON → SQL, string → command, text → HTML) where escaping is required but missing?

Map every complete source-to-sink path that lacks a required transformation. Flag every trust boundary crossing without validation.
```

### Checklist — Patterns to Look For

- [ ] Request body or query parameters bound directly to model objects (mass assignment)
- [ ] Type coercion in dynamically-typed languages without explicit checks (e.g., `==` vs `===`, truthy/falsy abuse)
- [ ] JSON/XML parsing that accepts unexpected types (array where object expected, number where string expected)
- [ ] Data flowing from one subsystem to another without re-validation (e.g., queue message → DB write)
- [ ] Missing output encoding when switching contexts (data → HTML, data → JS, data → SQL)
- [ ] Implicit type conversions in comparisons (`0 == "0"`, `null == undefined`)
- [ ] API endpoints accepting arbitrary additional properties beyond the documented schema
- [ ] Internal service calls that implicitly trust data because "it came from our own backend"
- [ ] Protobuf/Avro/thrift deserialization without schema enforcement
- [ ] Form data parsed without Content-Type validation (e.g., JSON accepted as form-urlencoded)
- [ ] Integer overflow or underflow in financial or permission calculations
- [ ] Default values in models that bypass validation when fields are omitted

### Minimum Evidence Criteria

A valid finding **must** include:

1. **Source boundary**: Where data enters the system or crosses from a lower-trust to higher-trust zone.
2. **Sink boundary**: Where the untrusted or improperly transformed data is consumed with security implications.
3. **Missing transformation**: The specific validation, sanitization, encoding, or type check absent.
4. **Consequence**: What an attacker achieves by exploiting the gap (e.g., privilege escalation via role field injection).
5. **Trace**: Key intermediate variables and function calls in the data path.

### Priority Heuristic

Run **early** when the codebase:
- Uses ORM or model binding from request parameters.
- Has microservice boundaries where data crosses process/network lines.
- Performs context-switching (data flows from JSON input → SQL query → HTML output).
- Accepts dynamic or polymorphic data structures from external sources.

Defer to later when the codebase has simple, static data paths with minimal transformation.

---

## HT-04 — File/IO Trail

### Scope

All filesystem and IO-based attack surfaces. Covers insecure file upload, insecure parsing of file contents, file inclusion (LFI/RFI), symlink abuse, and path traversal outside designated directories.

### Internal Prompt Template

```
You are a filesystem and IO security analyst. Identify every path where the application interacts with the filesystem or processes file-like content.

For each interaction, verify:
  (a) Upload: Is the filename sanitized? Is the content type verified beyond the header? Is the file stored outside the web root or in a non-executable location? Are upload size and type restrictions enforced server-side?
  (b) Parsing: Are parsers configured to prevent entity expansion (XXE), zip bombs, billion laughs, or resource exhaustion? Are there fallback parsers that might be less strict?
  (c) Inclusion: Does the application use user input to construct file paths for `include`, `require`, `import`, or dynamic loading? Is path canonicalization applied before access checks?
  (d) Symlinks: Are there operations that follow symlinks without verification, enabling reads/writes outside intended directories?
  (e) Path traversal: Is `../`, encoded traversal, or null-byte injection possible in any path parameter?

Report every instance where file IO operations accept user-influenced paths or content without proper restriction.
```

### Checklist — Patterns to Look For

- [ ] `open()`, `read()`, `write()`, `unlink()`, `rename()` with user-influenced path components
- [ ] `os.path.join()` or equivalent where the second argument is absolute and overrides the base
- [ ] Upload handlers that rely solely on client-provided `Content-Type` or file extension
- [ ] Double extensions (e.g., `shell.php.jpg`) bypassing extension allowlists
- [ ] Magic byte validation that can be spoofed (file content starts with allowed bytes but contains malicious payload)
- [ ] Zip/archive extraction without checking for path traversal in member filenames
- [ ] XML/HTML parsers with external entity resolution enabled
- [ ] `include()`, `require()`, `import` with dynamically constructed paths
- [ ] Symlink-following file operations (`os.path.realpath()` not called before access check)
- [ ] Temporary file creation with predictable names (race condition on creation)
- [ ] Sensitive files served directly from a public directory (`.env`, `config.yml`, `.git`)
- [ ] Image/video processing pipelines that invoke external tools (ImageMagick, FFmpeg) with user-controlled parameters
- [ ] File download endpoints that accept relative paths without canonicalization

### Minimum Evidence Criteria

A valid finding **must** include:

1. **Entry point**: The specific function, endpoint, or handler that accepts file-related user input.
2. **Filesystem operation**: The exact IO call that can be influenced (include path, write destination, etc.).
3. **Escalation path**: How the attacker progresses from the IO vulnerability to impact (e.g., path traversal → config read, upload → RCE).
4. **Missing safeguard**: Which specific protection (canonicalization, extension allowlist, content verification) is absent.
5. **Reachability**: That the code path is exercisable via an external interface (not dead code).

### Priority Heuristic

Run **early** when the codebase:
- Has file upload endpoints or media processing pipelines.
- Uses dynamic `include`/`require`/`import` based on request parameters.
- Serves files from user-controlled paths (download, export, attachment endpoints).
- Processes XML, YAML, or archive files from external sources.

Defer to later when the codebase has minimal file IO beyond static asset serving.

---

## HT-05 — Secrets/Config Trail

### Scope

All hardcoded and improperly managed secrets, weak cryptographic configurations, insecure defaults, debug exposure, environment variable leakage, and missing security headers. Covers both application-level and infrastructure-level configuration security.

### Internal Prompt Template

```
You are a secrets and configuration security auditor. Systematically search the codebase for sensitive data exposure through configuration.

Examine:
  (a) Hardcoded credentials: API keys, passwords, tokens, certificates embedded in source code, config files, or VCS history.
  (b) Cryptographic weaknesses: weak algorithms (MD5, SHA1 for security, DES, RC4), insufficient key lengths, hardcoded IVs, ECB mode usage, custom crypto.
  (c) Insecure defaults: debug mode enabled, verbose error messages in production, default admin credentials, CORS set to `*`.
  (d) Debug/test exposure: Swagger/UI endpoints, `/debug`, `/metrics`, `/healthz` leaking internal data, stack traces in responses.
  (e) Environment leakage: `.env` files committed, secrets in CI/CD configs, secrets in Dockerfiles or docker-compose, secrets in logs.
  (f) Security headers: missing HSTS, CSP, X-Content-Type-Options, X-Frame-Options; misconfigured CORS or CSP policies.

Report every instance where secrets are exposed or security-relevant configurations are insecure.
```

### Checklist — Patterns to Look For

- [ ] Hardcoded passwords, API keys, or tokens in source files (search for common patterns: `password=`, `api_key=`, `secret=`, `token=`)
- [ ] Private keys or certificates committed to VCS (`.pem`, `.key`, `.p12`, `.jks`)
- [ ] Weak hashing algorithms used for security purposes (MD5, SHA1)
- [ ] Weak encryption algorithms (DES, 3DES, RC4, Blowfish) or insufficient key sizes (<256 bits for symmetric, <2048 for RSA)
- [ ] ECB mode usage, hardcoded IVs or salts
- [ ] Custom or homegrown cryptographic implementations
- [ ] `DEBUG=True` or equivalent in production configs
- [ ] Verbose error pages leaking stack traces or internal paths
- [ ] CORS configuration with `Access-Control-Allow-Origin: *` combined with credential-bearing endpoints
- [ ] Missing security headers: `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`
- [ ] `.env`, `.env.production`, or similar files containing real secrets in VCS
- [ ] Secrets in Dockerfiles (`ENV SECRET=...`), docker-compose.yml, or CI/CD YAML
- [ ] Default or well-known credentials (admin/admin, root/root) in configs
- [ ] Logging of sensitive data (passwords, tokens, PII) in application logs
- [ ] Exposed debug/admin routes (`/admin`, `/debug`, `/swagger`, `/graphql`, `/metrics`) without auth
- [ ] Sensitive data in URL query parameters (tokens, passwords in GET requests)

### Minimum Evidence Criteria

A valid finding **must** include:

1. **Secret or config item**: The exact string, file, or setting that is exposed or misconfigured.
2. **Location**: File path, line number, and context (source code, config file, Dockerfile, etc.).
3. **Exposure scope**: Who can access this — public repo, deployed endpoint, internal network, local file.
4. **Remediation direction**: What should replace the current insecure practice (e.g., "use env variable", "rotate to 256-bit key", "add CSP header").
5. **Severity factor**: Whether the finding is exploitable directly (e.g., public API key) vs. requires additional access (e.g., hardcoded password in an internal service).

### Priority Heuristic

Run **very early** (often first) when the codebase:
- Is a new codebase being assessed for the first time (quick wins).
- Has public-facing endpoints (secrets in client-accessible code are critical).
- Contains configuration files, Dockerfiles, or CI/CD pipelines.
- Has a history of credential leaks (check git history).

Always run, but can be parallelized with HT-01 since it operates on different code patterns.

---

## HT-06 — Network/SSRF Trail

### Scope

Server-side request forgery, insecure outbound callbacks, URL fetch abuse, internal network pivoting, and open redirects. Covers any path where the application makes network requests influenced by user input.

### Internal Prompt Template

```
You are a network-level vulnerability analyst. Identify every path where the application initiates outbound network requests, especially where URLs, hostnames, or IP addresses are influenced by external input.

For each outbound request path, verify:
  (a) SSRF: Can a user-controlled URL cause the server to fetch from internal hosts, cloud metadata endpoints (169.254.169.254), or localhost services?
  (b) URL validation: Is the scheme, host, and port validated against an allowlist? Are DNS rebinding or IP-based bypasses (decimal/octal IP representations, IPv6 mapping) handled?
  (c) Redirect following: Does the HTTP client follow redirects? If so, can a 302 redirect to an internal host bypass initial URL validation?
  (d) Open redirect: Can user-controlled input cause the application to issue a 302/301 to an arbitrary external domain, enabling phishing or token theft?
  (e) Callback URLs: Does the application call back to URLs provided in webhooks, OAuth redirect URIs, or API integrations without strict validation?

Report every instance where user input influences network requests without sufficient allowlist validation.
```

### Checklist — Patterns to Look For

- [ ] `requests.get()`, `fetch()`, `http.Get()`, `URL.open()`, `curl` with user-controlled URLs
- [ ] URL validation that only checks domain suffix or scheme but allows internal IPs
- [ ] Missing validation for `169.254.169.254`, `metadata.google.internal`, `100.100.100.200` (cloud metadata)
- [ ] HTTP clients configured to follow redirects where initial URL passes validation but redirect target does not
- [ ] Webhook URLs stored in DB and called without validation
- [ ] Open redirect via `?redirect=`, `?next=`, `?return_to=` parameters
- [ ] DNS rebinding potential: domain that resolves to external IP on first lookup, internal IP on subsequent
- [ ] URL parsing inconsistencies (e.g., `http://evil.com@good.com` parsed differently by different libraries)
- [ ] IPv6 mapped addresses bypassing IPv4 denylists (`::ffff:127.0.0.1`, `::ffff:10.0.0.1`)
- [ ] Decimal/octal IP representations bypassing host denylists (`2130706433` = `127.0.0.1`, `0177.0.0.1`)
- [ ] PDF generators, image processors, or importers that fetch external resources
- [ ] SSRF via file:// or gopher:// scheme handlers
- [ ] Partial SSRF: ability to scan internal ports or hosts (port scanning, service enumeration)

### Minimum Evidence Criteria

A valid finding **must** include:

1. **Request initiation point**: The function or endpoint where user input triggers an outbound network request.
2. **User-controlled parameter**: Which specific input field influences the URL, host, or port.
3. **Validation gap**: What specific validation is missing (scheme allowlist, IP denylist, redirect-following, etc.).
4. **Internal reachability**: Which internal resources become accessible (cloud metadata, internal APIs, localhost services).
5. **Exploit chain**: How the SSRF or redirect can be leveraged (data exfiltration, internal service access, credential theft).

### Priority Heuristic

Run **early** when the codebase:
- Has URL-fetching features (webhooks, URL preview, link unfurling, image import from URL).
- Integrates with OAuth providers (callback URLs).
- Generates PDFs, screenshots, or renders external content server-side.
- Has open redirect patterns in login/logout flows.

Defer to later when the codebase makes no outbound network requests influenced by user input.

---

## HT-07 — Concurrency/State Trail

### Scope

Race conditions, time-of-check-to-time-of-use (TOCTOU) vulnerabilities, session confusion, cache poisoning, and unsafe shared state. Covers any vulnerability that arises from the interaction of concurrent or asynchronous operations.

### Internal Prompt Template

```
You are a concurrency and state integrity analyst. Identify every path where the correctness of security-relevant operations depends on atomic execution but is not guaranteed by the implementation.

Examine:
  (a) TOCTOU: Are there sequences where a check (e.g., "balance sufficient?") and the subsequent action ("deduct balance") are not atomic, allowing a window for exploitation?
  (b) Race conditions: Can concurrent requests cause double-spending, duplicate account creation, or circumvent rate limits by hitting non-atomic operations?
  (c) Session confusion: Can one user's session state be observed or modified by another through shared objects, caching, or session fixation?
  (d) Cache poisoning: Can an attacker influence cached responses that other users receive, injecting malicious content?
  (e) Unsafe shared state: Are global or module-level mutable objects used for request-scoped data (e.g., class-level dict instead of per-request dict)?

Report every instance where non-atomic operations on security-critical state can be exploited by concurrent or interleaved requests.
```

### Checklist — Patterns to Look For

- [ ] Check-then-act patterns on shared resources without database-level locking (`SELECT ... WHERE balance >= X` then `UPDATE ... SET balance = balance - X` in separate queries)
- [ ] `balance -= amount` without `SELECT FOR UPDATE` or equivalent atomic operation
- [ ] Rate limiting implemented in application code without atomic increment (e.g., `count = cache.get(); if count < limit: count += 1; cache.set()`)
- [ ] One-time tokens (password reset, email verification) that are not atomically consumed
- [ ] Session data stored in global or class-level mutable objects rather than per-request stores
- [ ] Filesystem TOCTOU: `os.path.exists()` check followed by `open()` or `os.unlink()` in separate calls
- [ ] Shared cache keys that include user-influenced data, enabling cache poisoning for other users
- [ ] Double-submit patterns (e.g., payment, account creation) without idempotency keys
- [ ] Lazy initialization of singletons without proper locking (DCLP issues)
- [ ] Race in OAuth/OIDC state parameter: state stored after redirect, or not verified atomically with token exchange
- [ ] Inventory/stock deduction without atomic reserve-and-confirm pattern
- [ ] Async/await patterns where shared mutable state is modified across await points without synchronization
- [ ] CSRF tokens stored in a way that one request can override another's token before validation

### Minimum Evidence Criteria

A valid finding **must** include:

1. **Shared resource**: The specific state, record, or object that is accessed concurrently.
2. **Non-atomic sequence**: The exact check-then-act or multi-step operation that lacks atomicity.
3. **Race window**: The concrete sequence of interleaved requests that exploits the gap.
4. **Security impact**: What the attacker gains (double spend, bypass rate limit, access another user's data).
5. **Reproducibility**: Assessment of whether the race window is practically exploitable (microsecond window vs. second window).

### Priority Heuristic

Run **early** when the codebase:
- Handles financial transactions, inventory, or balance operations.
- Implements rate limiting or one-time token mechanisms in application code.
- Uses in-memory caches (Redis, Memcached) for security-relevant data.
- Has async/await or multi-threaded request handling with shared mutable state.

Defer to later when the codebase is stateless or uses database-level atomic operations for all critical paths.

---

## Trail Sequencing Strategy

### Decision Matrix

Trail order should adapt to the codebase type. Use the following decision matrix to determine initial sequencing:

| Codebase Characteristic | Run First | Run Second | Run Third |
|---|---|---|---|
| **Web API with auth** | HT-02 (Auth/AuthZ) | HT-01 (Input/Injection) | HT-03 (Data Flow) |
| **Web API without auth** | HT-01 (Input/Injection) | HT-03 (Data Flow) | HT-06 (Network/SSRF) |
| **Library / SDK** | HT-03 (Data Flow) | HT-01 (Input/Injection) | HT-05 (Secrets/Config) |
| **CLI tool** | HT-01 (Input/Injection) | HT-04 (File/IO) | HT-05 (Secrets/Config) |
| **Microservice with callbacks** | HT-06 (Network/SSRF) | HT-02 (Auth/AuthZ) | HT-01 (Input/Injection) |
| **Financial / transactional** | HT-07 (Concurrency/State) | HT-02 (Auth/AuthZ) | HT-03 (Data Flow) |
| **File-processing pipeline** | HT-04 (File/IO) | HT-01 (Input/Injection) | HT-05 (Secrets/Config) |
| **Unknown / general** | HT-05 (Secrets/Config) | HT-01 (Input/Injection) | HT-02 (Auth/AuthZ) |

### Default Sequence

When no clear codebase type is identified, use this default order:

1. **HT-05** (Secrets/Config) — Fast, high-signal, finds quick wins regardless of codebase type.
2. **HT-01** (Input/Injection) — Broadest attack surface, most common vulnerability class.
3. **HT-02** (Auth/AuthZ) — Critical impact, present in most applications with user concepts.
4. **HT-03** (Data Flow) — Connects findings from earlier trails, discovers systemic issues.
5. **HT-06** (Network/SSRF) — Narrower surface but high impact when present.
6. **HT-04** (File/IO) — Important for specific codebases, less universal.
7. **HT-07** (Concurrency/State) — Requires deep understanding of application flow; benefits from context gathered by earlier trails.

---

## Parallelization Rules

### Constraints

- **Maximum 3 trails running simultaneously** — controlled fan-out to maintain analysis quality and avoid cognitive overload.
- **No overlapping scope within a batch** — trails in the same parallel batch should target different code paths and different vulnerability classes.
- **Sequential dependencies are respected** — some trails benefit from context gathered by earlier trails.

### Batching Strategy

**Batch 1 (3 trails, parallel):**
- HT-05 (Secrets/Config) — scans config files, env vars, headers; does not need code flow context.
- HT-01 (Input/Injection) — scans entry points and sinks; independent of auth logic.
- HT-02 (Auth/AuthZ) — scans auth middleware and access control; independent of data flow.

These three trails are independent — they examine different code patterns and can run in parallel without cross-contamination.

**Batch 2 (2 trails, parallel):**
- HT-03 (Data Flow) — benefits from HT-01 findings (known sinks) and HT-02 findings (known auth boundaries).
- HT-06 (Network/SSRF) — benefits from HT-01 findings (known URL input points); examines different code.

**Batch 3 (2 trails, sequential or parallel):**
- HT-04 (File/IO) — benefits from HT-01 context (known file-handling paths) and HT-03 context (known data flows).
- HT-07 (Concurrency/State) — benefits from all prior context; identifies race windows in known critical paths.

### Re-batching Rules

- If Batch 1 findings reveal the codebase has no auth layer, skip HT-02 and promote HT-03 to Batch 1.
- If Batch 1 findings reveal extensive file processing, promote HT-04 to Batch 2.
- If Batch 1 findings reveal no outbound network requests, skip HT-06.
- **Skip condition**: Any trail can be skipped if Batch 1 analysis shows the attack surface is entirely absent (e.g., no file uploads → skip HT-04).

---

## Trail Output → Validate and Gapfill Phases

### Trail Output Format

Each trail produces findings in this canonical structure:

```yaml
finding:
  id: "HT-XX-NNN"           # Trail ID + sequential number
  title: "Short description"
  severity: "critical|high|medium|low|info"
  trail: "HT-XX"
  source:
    file: "path/to/file"
    line: 42
    function: "handler"
  evidence:
    source: "Description of the user-controlled input"
    sink: "Description of the dangerous execution point"
    trace: ["step1", "step2", "step3"]
    mitigation_gap: "What specific protection is missing"
  impact: "What an attacker can achieve"
  confidence: "confirmed|likely|possible|unverified"
```

### Feeding into Validate Phase

After all trails complete, the **Validate** phase:

1. **Deduplication**: Merge findings from different trails that identify the same vulnerability from different angles (e.g., HT-01 and HT-03 both flagging a SQL injection path).
2. **Confidence upgrade**: For each finding, confirm minimum evidence criteria are met. Downgrade or discard findings where evidence is incomplete.
3. **Exploitability assessment**: For each remaining finding, evaluate whether a concrete exploit path exists. Mark as `confirmed` if reachable, `theoretical` if code path exists but is not externally reachable.
4. **Severity calibration**: Adjust severity based on real-world exploitability, not theoretical maximum impact. A SQL injection in an internal-only endpoint is `high`, not `critical`.
5. **Cross-reference**: Check if a finding from one trail enables or worsens a finding from another (e.g., HT-05 finds exposed debug endpoint → HT-02 confirms no auth on that endpoint → combined finding is `critical`).

### Feeding into Gapfill Phase

After validation, the **Gapfill** phase:

1. **Coverage audit**: For each trail, verify that all code paths within scope were examined. If a trail reported "no findings" for a large module, re-examine with a narrower focus.
2. **Blind spot identification**: List code areas that were not covered by any trail (e.g., third-party dependencies, generated code, configuration files outside the main repo).
3. **Trail re-run**: If gaps are found in specific areas, re-run the relevant trail with narrowed scope targeting only the uncovered areas.
4. **Edge case hunting**: Based on validated findings, look for similar patterns in adjacent code that may have the same vulnerability class but were not flagged (variant hunting).
5. **Final coverage report**: Produce a summary of which code areas were examined by which trails, and which areas remain unexamined.

### Flow Diagram

```
┌─────────────┐
│  HT-05/01/02 │  ← Batch 1 (parallel)
└──────┬──────┘
       │ findings
       ▼
┌─────────────┐
│  HT-03/06   │  ← Batch 2 (parallel, uses Batch 1 context)
└──────┬──────┘
       │ findings
       ▼
┌─────────────┐
│  HT-04/07   │  ← Batch 3 (uses all prior context)
└──────┬──────┘
       │ all findings
       ▼
┌─────────────┐
│  VALIDATE   │  ← Deduplicate, confirm, calibrate
└──────┬──────┘
       │ validated findings
       ▼
┌─────────────┐
│  GAPFILL    │  ← Coverage audit, re-run, variant hunt
└──────┬──────┘
       │ final findings
       ▼
┌─────────────┐
│  REPORT     │  ← Structured vulnerability report
└─────────────┘
```

---

## Appendix: Quick-Reference Trail Summary

| Trail | Focus | Key Signal | Skip If |
|-------|-------|------------|---------|
| HT-01 | Input/Injection | String concat in queries, `eval()`, template rendering | No user input handling |
| HT-02 | Auth/AuthZ | Missing auth decorators, IDOR, JWT flaws | No auth system |
| HT-03 | Data Flow | Unvalidated model binding, missing encoding, type confusion | Simple static data paths |
| HT-04 | File/IO | Upload handlers, dynamic `include`, path params | No file IO |
| HT-05 | Secrets/Config | Hardcoded keys, weak crypto, missing headers | Always run |
| HT-06 | Network/SSRF | URL fetch with user input, webhooks, open redirects | No outbound requests |
| HT-07 | Concurrency/State | Check-then-act, shared mutable state, rate limits | Stateless or DB-atomic |

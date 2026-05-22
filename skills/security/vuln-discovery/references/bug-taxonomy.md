# Bug Taxonomy

Vulnerability categories for Hunt trail assignment. Select categories relevant to the target codebase's language, framework, and domain.

## Injection

| ID | Category | Description |
|----|----------|-------------|
| INJ-01 | SQL Injection | Untrusted input concatenated into SQL queries |
| INJ-02 | Command Injection | Untrusted input passed to shell/exec |
| INJ-03 | LDAP Injection | Untrusted input in LDAP queries |
| INJ-04 | XPath Injection | Untrusted input in XPath expressions |
| INJ-05 | Header Injection | Untrusted input in HTTP headers (CRLF) |
| INJ-06 | Template Injection | Untrusted input in template engines (SSTI/Jinja2/etc.) |
| INJ-07 | NoSQL Injection | Untrusted input in NoSQL query constructors |
| INJ-08 | Log Injection | Untrusted input written to logs without sanitization |

## Authentication & Authorization

| ID | Category | Description |
|----|----------|-------------|
| AUTH-01 | Authentication Bypass | Logic errors allowing auth skip |
| AUTH-02 | Broken Access Control | IDOR, missing permission checks, privilege escalation |
| AUTH-03 | Session Management | Session fixation, insecure cookie flags, missing rotation |
| AUTH-04 | Credential Storage | Plaintext passwords, weak hashing, hardcoded credentials |
| AUTH-05 | Privilege Escalation | Vertical or horizontal escalation via parameter tampering |
| AUTH-06 | OAuth/JWT Flaws | Token forgery, algorithm confusion, missing validation |

## Data Handling

| ID | Category | Description |
|----|----------|-------------|
| DATA-01 | Buffer Overflow | Unbounded reads/writes in memory-unsafe languages |
| DATA-02 | Integer Overflow | Arithmetic overflow leading to memory corruption or logic errors |
| DATA-03 | Type Confusion | Incorrect type assumptions leading to bypass |
| DATA-04 | Deserialization | Insecure deserialization of untrusted data |
| DATA-05 | Mass Assignment | Unintended model binding from user input |
| DATA-06 | Improper Input Validation | Missing or insufficient validation on user input |

## Cryptography

| ID | Category | Description |
|----|----------|-------------|
| CRYPTO-01 | Weak Cryptography | Use of broken algorithms (MD5, SHA1, DES, RC4) |
| CRYPTO-02 | Hardcoded Secrets | API keys, tokens, passwords in source code |
| CRYPTO-03 | Insecure Random | Predictable RNG for security-sensitive operations |
| CRYPTO-04 | Certificate Issues | Improper TLS validation, self-signed cert acceptance |

## Web-Specific

| ID | Category | Description |
|----|----------|-------------|
| WEB-01 | Cross-Site Scripting (XSS) | Reflected, stored, or DOM-based XSS |
| WEB-02 | Cross-Site Request Forgery (CSRF) | Missing anti-CSRF tokens |
| WEB-03 | Open Redirect | Untrusted redirect targets |
| WEB-04 | Server-Side Request Forgery (SSRF) | User-controlled URLs for outbound requests |
| WEB-05 | File Upload | Unrestricted file upload leading to code execution |
| WEB-06 | Path Traversal | Directory traversal via `../` or symlink |
| WEB-07 | Race Condition | TOCTOU issues in concurrent operations |
| WEB-08 | Clickjacking | Missing X-Frame-Options or CSP frame-ancestors |

## API & Service

| ID | Category | Description |
|----|----------|-------------|
| API-01 | Broken Object-Level Auth | API endpoints exposing object properties without authorization |
| API-02 | Broken Function-Level Auth | API functions callable without proper role checks |
| API-03 | Unrestricted Resource Consumption | No rate limiting, pagination, or resource caps |
| API-04 | Broken Object Property Limits | Excessive data exposure in API responses |
| API-05 | Security Misconfiguration | Default credentials, verbose errors, missing hardening |

## Concurrency & State

| ID | Category | Description |
|----|----------|-------------|
| CONC-01 | Race Condition | TOCTOU, check-then-act without locks |
| CONC-02 | Deadlock | Improper lock ordering |
| CONC-03 | Unsafe Shared State | Global mutable state without synchronization |

## Error Handling & Logging

| ID | Category | Description |
|----|----------|-------------|
| ERR-01 | Information Disclosure | Stack traces, internal paths, or secrets in error responses |
| ERR-02 | Missing Error Handling | Uncaught exceptions crashing the service |
| ERR-03 | Swallowed Errors | Catch blocks that silently ignore errors |

## Configuration & Infrastructure

| ID | Category | Description |
|----|----------|-------------|
| CONFIG-01 | Insecure Defaults | Default passwords, unnecessary features enabled |
| CONFIG-02 | Exposed Debug Interfaces | Debug endpoints, admin panels, Swagger UI in production |
| CONFIG-03 | Dependency Vulnerabilities | Known CVEs in third-party packages |
| CONFIG-04 | Missing Security Headers | Absent CSP, HSTS, X-Content-Type-Options |
| CONFIG-05 | Environment Leakage | Secrets in env vars exposed to client, .env committed |

## Memory Safety (C/C++/Rust)

| ID | Category | Description |
|----|----------|-------------|
| MEM-01 | Use After Free | Dereferencing freed memory |
| MEM-02 | Double Free | Freeing the same allocation twice |
| MEM-03 | Out-of-Bounds Read/Write | Array indexing beyond bounds |
| MEM-04 | Null Pointer Dereference | Dereferencing NULL or uninitialized pointers |
| MEM-05 | Uninitialized Memory | Using memory before initialization |

## Selection Guidance

When assigning Hunt trails, prioritize categories based on:

- **Language**: Memory safety for C/C++/Rust; injection for SQL-using languages; deserialization for Java/Python
- **Framework**: Web frameworks → XSS/CSRF/injection; ORMs → SQL injection, mass assignment
- **Domain**: Financial apps → race conditions, authorization; IoT → buffer overflows, command injection
- **Entry points**: APIs → API-*; web forms → WEB-* and INJ-*; CLI tools → INJ-02, WEB-06

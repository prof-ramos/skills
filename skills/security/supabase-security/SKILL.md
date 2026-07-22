---
name: supabase-security
description: >-
  Audits Supabase security on authorized bug bounty and pentest targets,
  focusing on misconfigurations common in vibe-coded and production apps:
  missing/broken RLS, USING(true)/WITH CHECK(true), JWT user_metadata privilege
  escalation, anon write policies, SECURITY DEFINER RPCs, storage buckets,
  exposed service_role keys, and PostgREST surface. Guides running the bundled
  SQL audit scripts, interpreting red flags, validating client-side exposure,
  and writing severity-ranked findings with PoC steps and remediations. Use when
  the user runs /supabase-security, or asks to audit Supabase, check RLS, review
  Supabase policies, hunt Supabase misconfigs, test anon key access, or secure
  a Supabase backend on a bug bounty target. Requires written authorization
  before any active testing.
license: MIT
metadata:
  author: prof-ramos
  version: "1.0.0"
  compatibility: >-
    Authorized bug bounty / pentest only. Prefer read-only catalog SQL and
    client-side checks with the public anon key. Never use service_role keys
    found in the wild without program rules allowing credential use.
---

# Supabase Security Audit (Bug Bounty)

Full security verification of a target's Supabase stack. Vibe-coded and many production apps share the same failure modes: RLS off, open policies, JWT metadata for roles, open Storage, and SECURITY DEFINER RPCs.

> **Authorization gate**
> Use only on targets with written authorization (bug bounty program, pentest SOW, or owned project).
> Confirm in-scope assets (domains, project refs, APIs) before any active test.
> Prefer non-destructive checks. Do not mass-exfiltrate PII; minimize evidence to PoC rows/fields.
> If a `service_role` key is found, treat as Critical secret exposure — do **not** abuse it beyond program-allowed proof unless rules explicitly allow.

## When to run

- User runs `/supabase-security`
- Target uses Supabase (`.supabase.co`, `createClient`, `NEXT_PUBLIC_SUPABASE_*`, PostgREST `/rest/v1`)
- Need RLS / anon-key / Storage / RPC review for bug bounty or hardening

## Inputs to collect

Ask only for what is missing:

| Input | Why |
|-------|-----|
| Target URL / app URL | JS recon, key harvesting |
| Program scope / auth proof | Legal boundary |
| Supabase project URL (`https://<ref>.supabase.co`) | API surface |
| `anon` public key (from frontend) | Authenticated-as-anon tests |
| Optional: SQL Editor / `psql` access | Full catalog audit (when authorized & available) |
| Optional: two test accounts | IDOR / horizontal privilege checks |

## Pipeline

```
0 Auth gate → 1 Recon → 2 Client surface → 3 Catalog SQL (if possible)
→ 4 Abuse validation → 5 Severity + report
```

Do not skip 0–2. Phase 3 requires DB access (Dashboard SQL Editor or `psql`); if unavailable, deepen 2 and 4 from the outside.

---

## Phase 0 — Authorization

1. Confirm target is in scope and testing is authorized.
2. Note program rules on automated scanning, account creation, and credential use.
3. If authorization is unclear, stop and ask the user.

---

## Phase 1 — Recon

Map how the app talks to Supabase.

1. **Frontend / mobile bundle**
   - Search for: `supabase.co`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `service_role`, `eyJ` JWTs, `createClient(`.
   - Extract project ref, anon key, any leaked service_role or DB URLs.
2. **OpenAPI / PostgREST**
   - `GET {SUPABASE_URL}/rest/v1/` with headers:
     - `apikey: <anon>`
     - `Authorization: Bearer <anon>`
   - Note exposed tables, views, RPC names if schema is open or errors leak names.
3. **Auth methods in UI**: email/password, magic link, OAuth, phone, anonymous sign-in.
4. **Storage / Realtime / Edge** usage in network tab or source.
5. Produce a short attack-surface note: project ref, keys found (redact in reports as needed), tables/RPCs suspected, auth model.

---

## Phase 2 — Client-side surface (anon / user JWT)

All tests use only **public** credentials (`anon` key + attacker-controlled accounts) unless rules say otherwise.

### 2A. REST data access

For each suspected table `T`:

```http
GET /rest/v1/T?select=*&limit=5
apikey: <anon>
Authorization: Bearer <anon_or_user_jwt>
```

Check:

| Check | Red flag |
|-------|----------|
| Anon SELECT returns rows | Public data leak / missing RLS |
| Authenticated user reads other users' rows | IDOR / weak USING clause |
| INSERT/UPDATE/DELETE as anon | Anon write |
| INSERT as user A with `user_id` of B | Missing WITH CHECK |
| PATCH role/is_admin/plan columns | Mass assignment / broken column grants |

Prefer `Prefer: count=exact` and small `limit` — enough for PoC, not dumps.

### 2B. RPC / functions

```http
POST /rest/v1/rpc/<fn>
```

Probe discovered function names. SECURITY DEFINER without auth checks often = privilege escalation.

### 2C. Auth / JWT

- Sign up two accounts; compare access to the same resources.
- If policies use roles from JWT: try `updateUser({ data: { role: 'admin' } })` (user_metadata is user-writable).
- Confirm whether admin/premium flags live in `user_metadata` (Critical) vs `app_metadata` / server table.

### 2D. Storage

```http
GET /storage/v1/bucket
GET /storage/v1/object/list/<bucket>
```

- Public buckets with sensitive objects
- Upload to buckets as anon/authenticated when not intended
- Path traversal / predictable object names / IDOR on object paths

### 2E. Realtime

- Subscribe to sensitive tables/channels as anon or low-priv user.
- Presence of unrestricted channels for private data.

### 2F. Edge Functions

- Call `/functions/v1/<name>` with anon key.
- Missing JWT verification, SSRF, secrets in responses, IDOR in function logic.

### 2G. Secrets in client

- `service_role` in JS/mobile → Critical.
- Database password / connection string in client → Critical.
- Long-lived user tokens in logs → High/Medium depending on impact.

---

## Phase 3 — Catalog SQL audit (when DB access exists)

**Read-only.** Do not run DDL/DML "fixes" during bounty unless asked for remediation on owned projects.

| Access | Script |
|--------|--------|
| Supabase SQL Editor | `references/audit-dashboard.sql` (no `\echo`) |
| `psql` | `references/audit-psql.sql` |
| Deep pass / PT-BR red flags | `references/audit-complete.sql` |

Run sections in order. Capture scorecard + every CRITICAL/WARN row.

Interpret with `references/misconfig-catalog.md`.

---

## Phase 4 — Abuse validation

For each candidate finding, prove impact with a minimal PoC:

1. **Precondition** (keys, account state)
2. **Request(s)** (HTTP or SQL) — redact secrets in final writeup if required
3. **Observed result** (status, sample fields, row counts — not full dumps)
4. **Impact** (confidentiality / integrity / privilege)
5. **False-positive check** (public-by-design marketing data? documented public bucket?)

Prioritize:

1. service_role leak, RLS off on tenant tables, USING(true) on private data  
2. user_metadata authorization, anon write, SECURITY DEFINER without checks  
3. Storage IDOR, missing WITH CHECK, horizontal IDOR  
4. Info disclosure (schema, enums, error messages), missing FORCE RLS  

---

## Phase 5 — Report

Write `supabase-security-report-YYYY-MM-DD.md` using `references/report-template.md`.

Severity guide (adjust to program CVSS):

| Severity | Examples |
|----------|----------|
| Critical | service_role in client; RLS off + PII/tenant data; USING(true) private tables; user_metadata → admin |
| High | Anon write on sensitive tables; DEFINER RPC priv-esc; Storage full read of private files |
| Medium | IDOR on non-critical objects; missing WITH CHECK; app_metadata misuse if settable |
| Low | Verbose errors; enum/role name leak; RLS perf anti-patterns |
| Info | Hardening notes (FORCE RLS, indexes, Security Advisor) |

Each finding: title, severity, asset, evidence, PoC, impact, remediation, references (Supabase docs / OWASP).

---

## Common vibe-coder failure modes (hunt these first)

1. **RLS never enabled** on `public` tables exposed via PostgREST  
2. **`CREATE POLICY ... USING (true)`** "so the app works"  
3. **Authorization via `auth.jwt() -> user_metadata` / `raw_user_meta_data`**  
4. **No WITH CHECK** on INSERT/UPDATE (owner spoofing)  
5. **Anon policies for write** left from prototypes  
6. **SECURITY DEFINER** RPCs granted to `anon`/`authenticated` without `auth.uid()` checks or pinned `search_path`  
7. **Storage buckets public** with user uploads  
8. **service_role** in Next.js `NEXT_PUBLIC_*` or mobile apps  
9. **Views** without `security_invoker` bypassing RLS  
10. **Realtime** on tables that REST already protects poorly  

Full catalog: `references/misconfig-catalog.md`.

---

## Remediation patterns (for owned projects or report "fix")

```sql
-- Enable + force RLS
ALTER TABLE public.t ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.t FORCE ROW LEVEL SECURITY;

-- Owner-only pattern
CREATE POLICY t_select_own ON public.t
  FOR SELECT TO authenticated
  USING (user_id = (SELECT auth.uid()));

CREATE POLICY t_insert_own ON public.t
  FOR INSERT TO authenticated
  WITH CHECK (user_id = (SELECT auth.uid()));
```

- Roles: table `user_roles` with its own RLS, or `app_metadata` set **only** by service_role / Auth Hook — never `user_metadata` for authz.
- DEFINER functions: `SET search_path = public, pg_temp`, explicit authz, minimal GRANT.
- Re-run Supabase Dashboard → Database → **Security Advisor** after fixes.

---

## Resource files

| Path | Use |
|------|-----|
| `references/audit-dashboard.sql` | Catalog audit in SQL Editor |
| `references/audit-psql.sql` | Catalog audit via psql (`\echo` sections) |
| `references/audit-complete.sql` | Extended PT-BR checklist + executive summary query |
| `references/misconfig-catalog.md` | Red flags, severity, PoC hints |
| `references/report-template.md` | Report skeleton |

## Constraints

- Read-only preference; no destructive tests without explicit user request.
- Minimize data access; PoC-sized evidence only.
- Do not commit real keys, JWTs, or PII into git.
- Coordinate with `ethical-redteam` / `vuln-discovery` when the engagement is broader than Supabase.

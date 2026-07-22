# Supabase Misconfiguration Catalog

Quick reference for red flags during bug bounty audits. Map each hit to a finding with PoC.

## Critical

| ID | Pattern | Why | External PoC hint | SQL signal |
|----|---------|-----|-------------------|------------|
| C1 | RLS disabled on multi-tenant / PII table | PostgREST exposes full table to roles with GRANT | `GET /rest/v1/t?select=*` as anon/auth | `rls_enabled = false` |
| C2 | `USING (true)` / `WITH CHECK (true)` on private data | Any role in policy sees/writes all rows | Same as C1 with policy role | `qual`/`with_check` = `true` |
| C3 | Authz on `user_metadata` / `raw_user_meta_data` | User can set metadata via signup/`updateUser` | Set `role=admin` in user metadata; re-access | policies ILIKE `%user_metadata%` |
| C4 | `service_role` key in client bundle | Full bypass of RLS | Key in JS/source maps | N/A (client recon) |
| C5 | SECURITY DEFINER RPC, no auth check, granted to anon/auth | Runs as owner; privilege escalation | `POST /rest/v1/rpc/fn` | `prosecdef` + grants + body lacks `auth.uid` |
| C6 | DEFINER without pinned `search_path` | Search-path hijack risk | Code review of function | `proconfig` missing `search_path=` |

## High

| ID | Pattern | Why | External PoC hint | SQL signal |
|----|---------|-----|-------------------|------------|
| H1 | Anon INSERT/UPDATE/DELETE policies | Anyone with anon key mutates data | Write as anon | policies `roles @> {anon}` + write cmd |
| H2 | Missing WITH CHECK on INSERT/UPDATE | Create/update rows as another user | Insert `user_id` of victim | `with_check` null on INSERT/UPDATE |
| H3 | Horizontal IDOR (USING only partial) | e.g. filter by `org_id` spoofable | Swap IDs between two accounts | Review policy expressions |
| H4 | Public Storage bucket with private files | Objects world-readable | List/download without auth | Storage API |
| H5 | Authenticated read-all on tenant table | "Logged in users see everything" | Two accounts, cross-read | open SELECT for `authenticated` |
| H6 | Edge Function without JWT verify + sensitive action | Unauthenticated backend logic | Call function with only anon key | Source / behavior |

## Medium

| ID | Pattern | Why | External PoC hint | SQL signal |
|----|---------|-----|-------------------|------------|
| M1 | RLS on, zero policies | Deny-all for non-owner; often broken app or incomplete setup | 401/empty; still flag incomplete security model | RLS true, no pg_policies |
| M2 | Views without `security_invoker` | May run as owner and bypass RLS | `GET /rest/v1/view` | `relkind = v`, reloptions |
| M3 | `app_metadata` in policies if client can set it | Usually safe if only service_role sets it | Confirm update paths | policies reference app_metadata |
| M4 | Predictable Storage paths (`userId/doc.pdf`) without ACL | Object IDOR | Guess paths | Storage |
| M5 | Realtime on sensitive tables | Leak via subscription | Subscribe as low-priv | Client code |
| M6 | Column-level mass assignment | User sets `is_admin`, `balance` | PATCH elevated fields | grants + policies |

## Low / Info

| ID | Pattern | Why | Notes |
|----|---------|-----|-------|
| L1 | Verbose PostgREST errors | Schema/column enumeration | Helpful for attackers |
| L2 | Public enums of roles | Reveals privilege model | `pg_enum` |
| L3 | `auth.uid()` not wrapped as `(select auth.uid())` | Perf / rare edge cases | Optimize |
| L4 | Missing indexes on RLS filter columns | DoS/perf, incomplete hardening | indexes section |
| L5 | RLS on but not FORCE | Table owner bypasses | `relforcerowsecurity = false` |
| I1 | Open marketing/public content tables | May be intentional | Confirm business intent before filing |

## Client recon checklist

```text
[ ] Project URL + anon key from frontend
[ ] service_role / DB URL absent from client
[ ] OpenAPI or error-based table discovery
[ ] Sign-up / anonymous auth available
[ ] Storage buckets listable
[ ] Edge functions enumerated from JS
[ ] Realtime channels in source
[ ] Admin UI talking to same project with weak policies
```

## JWT notes

- **anon key**: public by design; security = RLS + grants + Storage policies.
- **user JWT**: `role=authenticated`; still constrained by RLS.
- **service_role**: bypasses RLS — never ship to browsers/mobile.
- **user_metadata**: end-user writable → never use for authorization.
- **app_metadata**: only trusted if set exclusively server-side.

## Suggested severity mapping for reports

Use program CVSS when required. Default narrative:

- **Critical**: unauthenticated or trivial auth → full tenant/PII read/write, or full project compromise (service_role).
- **High**: authenticated low-priv → cross-tenant or privilege escalation with clear impact.
- **Medium**: limited data exposure, harder prerequisites, or integrity issues on non-critical data.
- **Low/Info**: defense-in-depth, enumeration, hardening.

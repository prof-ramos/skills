# Supabase Security Report — {{TARGET}}

- **Date:** {{YYYY-MM-DD}}
- **Auditor:** {{NAME}}
- **Authorization:** {{PROGRAM / SOW / OWNED}}
- **Project ref:** {{REF}} (redact if needed)
- **Access mode:** Client-only | Client + SQL Editor | Client + psql
- **Keys used:** anon only | + test users | (never paste service_role)

## Executive summary

{{2–5 sentences: overall risk, worst finding, data at risk}}

| Severity | Count |
|----------|------:|
| Critical | |
| High | |
| Medium | |
| Low | |
| Info | |

## Scope

- In-scope assets:
- Out of scope:
- Accounts used:
- Testing window:

## Attack surface

| Component | Observed |
|-----------|----------|
| Supabase URL | |
| Anon key present in client | yes/no |
| service_role in client | yes/no |
| Auth methods | |
| Tables/views hit via REST | |
| RPCs | |
| Storage buckets | |
| Edge Functions | |
| Realtime | |
| SQL catalog audit run | yes/no |

## Scorecard (if SQL audit run)

| Metric | Value |
|--------|------:|
| tables_rls_off | |
| tables_rls_on_no_policies | |
| policies_using_user_metadata | |
| security_definer_public | |
| policies_total | |
| anon write policies | |
| policies USING/CHECK true | |

## Findings

### F-001 — {{Title}}

| Field | Value |
|-------|-------|
| Severity | Critical / High / Medium / Low / Info |
| Asset | table / rpc / storage / edge / secret |
| CWE / category | e.g. Broken Access Control |
| Catalog ID | e.g. C2, H1 (from misconfig-catalog) |

**Description**

{{What is wrong and why it matters}}

**Evidence**

```http
{{minimal request/response or SQL result snippet — no PII dumps}}
```

**PoC steps**

1.
2.
3.

**Impact**

{{confidentiality / integrity / availability / privilege}}

**Remediation**

```sql
-- suggested fix (owned projects) or guidance for the vendor
```

**References**

- Supabase RLS: https://supabase.com/docs/guides/database/postgres/row-level-security
- …

---

### F-002 — …

## Negative results / hardening notes

- Checked X: no issue found because …
- Recommended follow-ups: Security Advisor, FORCE RLS, …

## Appendix

- Tools:
- Scripts used: `audit-dashboard.sql` / `audit-psql.sql` / `audit-complete.sql`
- Timeline:
- Disclosure status:

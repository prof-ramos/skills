---
name: cloudflare-workers
description: Build and operate Cloudflare Workers applications end-to-end, including bootstrap, Wrangler setup, bindings (KV, R2, D1, Durable Objects, Queues, Workers AI, Vectorize), runtime APIs, framework integrations, testing, deployment, and observability. Use when users ask for Cloudflare Workers, Wrangler, edge functions, or Cloudflare Developer Platform integrations.
---

# Cloudflare Workers

Use this skill to deliver Cloudflare Workers tasks with production-safe defaults and minimal setup churn.

## Execute the workflow

1. Classify the request.
2. Bootstrap or inspect the project.
3. Configure `wrangler.jsonc` and bindings.
4. Implement handlers and business logic.
5. Validate locally and with tests.
6. Deploy and verify in logs.

## Classify the request

Identify the primary task before making changes:

- New project or scaffold
- Binding configuration or migration
- Runtime API usage
- Framework integration
- Deployment or CI/CD
- Debugging and observability

Use the routing table below to load only the needed reference file.

## Route to references on demand

Load only one file at a time unless the task clearly spans multiple domains.

- `references/bindings.md`: KV, R2, D1, Durable Objects, Queues, AI, Vectorize, Service Bindings, Browser Rendering, Hyperdrive, Analytics
- `references/runtime-apis.md`: `fetch`, `scheduled`, `queue`, Cache API, HTMLRewriter, WebSockets, Streams, Crypto, Node compatibility
- `references/frameworks.md`: React/Vite, Vue/Vite, Next.js, Astro, SvelteKit, Hono, React Router, Nuxt, Solid Start, Express adapters
- `references/patterns.md`: API patterns, caching, auth, rate limiting, validation, repository patterns, RAG, performance, security

## Bootstrap quickly

Prefer the bundled scaffold when the user wants a starter project:

```bash
bash scripts/scaffold-worker.sh <project-name> [api|spa|fullstack|hono]
```

Then run:

```bash
cd <project-name>
npm install
npx wrangler dev
```

Use `npm create cloudflare@latest` when the user explicitly asks for official templates.

## Configure Wrangler correctly

Use `wrangler.jsonc` and always set:

- `name`
- `main`
- `compatibility_date`

Apply these rules:

- Keep non-sensitive config in `vars`
- Store secrets with `wrangler secret put`
- Keep bindings in `wrangler.jsonc` aligned with the `Env` interface in code
- Regenerate bindings types after changes with `npx wrangler types`

## Implement handlers with clear boundaries

Start with `fetch`; add `scheduled` and `queue` only if needed.

- Keep routing thin
- Move logic to modules/services
- Use `ctx.waitUntil` for non-blocking async work
- Use prepared statements for D1
- Return explicit status codes and content types

## Validate before deploy

Run a tight verification loop:

```bash
npx wrangler dev
npm test
npx wrangler deploy --dry-run
```

If bindings depend on remote resources, test with remote mode when necessary.

## Deploy safely

Follow staged deployment:

1. Deploy to staging environment.
2. Run smoke checks on key routes.
3. Deploy to production.
4. Tail logs and confirm no regression.

Useful commands:

```bash
npx wrangler deploy
npx wrangler deploy -e staging
npx wrangler tail
```

## Debug systematically

When debugging, execute this order:

1. Confirm request path and method handling.
2. Confirm binding names and IDs in `wrangler.jsonc`.
3. Confirm `Env` interface matches configured bindings.
4. Confirm secrets and environment-specific config.
5. Re-run type generation and restart dev server.
6. Tail logs and inspect failing requests.

## Use production guardrails

- Never store secrets in `vars`.
- Validate external input before use.
- Keep queue consumers idempotent.
- Define cache behavior intentionally.
- Limit per-request work and parallelize I/O with care.

## Return useful outputs

When responding to users, provide concrete artifacts:

- Minimal patch-ready config snippets
- Exact command sequence for local run and deploy
- Clear list of required bindings and secrets
- Verification checklist (what to test and where to look)

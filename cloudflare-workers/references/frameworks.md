# Framework Integration Guide

Complete guides for deploying popular frameworks on Cloudflare Workers.

## Table of Contents

1. [React (Vite)](#react-vite)
2. [Vue (Vite)](#vue-vite)
3. [Next.js](#nextjs)
4. [Astro](#astro)
5. [SvelteKit](#sveltekit)
6. [Hono](#hono)
7. [React Router (Remix)](#react-router-remix)
8. [Nuxt](#nuxt)
9. [Solid Start](#solid-start)
10. [Express.js](#expressjs)

---

## React (Vite)

Full-stack React SPA with API routes using Cloudflare Vite Plugin.

### Quick Start

```bash
npm create cloudflare@latest my-react-app -- --framework=react
cd my-react-app
npm run dev
```

### Manual Setup

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @cloudflare/vite-plugin wrangler --save-dev
```

### Configuration

```typescript
// vite.config.ts
import { cloudflare } from '@cloudflare/vite-plugin';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    react(),
    cloudflare()
  ]
});
```

```jsonc
// wrangler.jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-react-app",
  "main": "src/worker.ts",
  "compatibility_date": "2025-01-01",
  "assets": {
    "directory": "./dist",
    "binding": "ASSETS",
    "not_found_handling": "single-page-application"
  }
}
```

### Worker with API Routes

```typescript
// src/worker.ts
export interface Env {
  ASSETS: Fetcher;
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    // API routes
    if (url.pathname.startsWith('/api/')) {
      return handleApi(request, env);
    }
    
    // Serve React SPA
    return env.ASSETS.fetch(request);
  }
};

async function handleApi(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  
  if (url.pathname === '/api/users' && request.method === 'GET') {
    const users = await env.DB.prepare('SELECT * FROM users').all();
    return Response.json(users.results);
  }
  
  return Response.json({ error: 'Not found' }, { status: 404 });
}
```

### Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "deploy": "npm run build && wrangler deploy"
  }
}
```

---

## Vue (Vite)

Vue 3 SPA with Cloudflare Workers backend.

### Quick Start

```bash
npm create cloudflare@latest my-vue-app -- --framework=vue
```

### Manual Setup

```typescript
// vite.config.ts
import { cloudflare } from '@cloudflare/vite-plugin';
import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    vue(),
    cloudflare()
  ]
});
```

### Configuration

```jsonc
// wrangler.jsonc
{
  "name": "my-vue-app",
  "main": "src/worker.ts",
  "compatibility_date": "2025-01-01",
  "assets": {
    "directory": "./dist",
    "binding": "ASSETS",
    "not_found_handling": "single-page-application"
  }
}
```

---

## Next.js

Next.js on Cloudflare Workers using `@cloudflare/next-on-pages`.

### Quick Start

```bash
npm create cloudflare@latest my-next-app -- --framework=next
```

### Manual Setup

```bash
npx create-next-app@latest my-app
cd my-app
npm install @cloudflare/next-on-pages wrangler --save-dev
```

### Configuration

```javascript
// next.config.mjs
import { setupDevPlatform } from '@cloudflare/next-on-pages/next-dev';

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Required for Workers deployment
};

if (process.env.NODE_ENV === 'development') {
  await setupDevPlatform();
}

export default nextConfig;
```

```jsonc
// wrangler.jsonc
{
  "name": "my-next-app",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "pages_build_output_dir": ".vercel/output/static"
}
```

### Accessing Bindings

```typescript
// app/api/data/route.ts
import { getRequestContext } from '@cloudflare/next-on-pages';

export const runtime = 'edge';

export async function GET() {
  const { env } = getRequestContext();
  const data = await env.DB.prepare('SELECT * FROM items').all();
  return Response.json(data.results);
}
```

### Build & Deploy

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "npx @cloudflare/next-on-pages",
    "preview": "npx wrangler pages dev .vercel/output/static",
    "deploy": "npm run build && npx wrangler pages deploy .vercel/output/static"
  }
}
```

### Limitations

- Server Actions require `runtime = 'edge'`
- Middleware runs at the edge
- API routes need edge runtime
- Some Node.js APIs not available

---

## Astro

Static site generation and server-side rendering with Astro.

### Quick Start

```bash
npm create cloudflare@latest my-astro-app -- --framework=astro
```

### Manual Setup

```bash
npm create astro@latest my-app
cd my-app
npx astro add cloudflare
```

### Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'server',  // or 'hybrid' for mixed static/dynamic
  adapter: cloudflare({
    imageService: 'passthrough',
    platformProxy: {
      enabled: true
    }
  })
});
```

```jsonc
// wrangler.jsonc
{
  "name": "my-astro-app",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "assets": {
    "directory": "./dist/client"
  }
}
```

### Accessing Bindings

```astro
---
// src/pages/index.astro
const runtime = Astro.locals.runtime;
const { env } = runtime;
const items = await env.DB.prepare('SELECT * FROM items').all();
---

<html>
  <body>
    <ul>
      {items.results.map(item => <li>{item.name}</li>)}
    </ul>
  </body>
</html>
```

### API Routes

```typescript
// src/pages/api/items.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ locals }) => {
  const { env } = locals.runtime;
  const items = await env.DB.prepare('SELECT * FROM items').all();
  return Response.json(items.results);
};

export const POST: APIRoute = async ({ request, locals }) => {
  const { env } = locals.runtime;
  const data = await request.json();
  await env.DB.prepare('INSERT INTO items (name) VALUES (?)').bind(data.name).run();
  return Response.json({ success: true });
};
```

---

## SvelteKit

Full-stack Svelte applications with SvelteKit adapter.

### Quick Start

```bash
npm create cloudflare@latest my-svelte-app -- --framework=svelte
```

### Manual Setup

```bash
npm create svelte@latest my-app
cd my-app
npm install @sveltejs/adapter-cloudflare wrangler --save-dev
```

### Configuration

```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-cloudflare';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      routes: {
        include: ['/*'],
        exclude: ['<all>']
      }
    })
  }
};
```

```jsonc
// wrangler.jsonc
{
  "name": "my-svelte-app",
  "compatibility_date": "2025-01-01",
  "assets": {
    "directory": "./.svelte-kit/cloudflare"
  }
}
```

### Accessing Bindings

```typescript
// src/routes/+page.server.ts
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ platform }) => {
  const items = await platform?.env.DB.prepare('SELECT * FROM items').all();
  return { items: items?.results ?? [] };
};
```

```typescript
// src/routes/api/items/+server.ts
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ platform }) => {
  const items = await platform?.env.DB.prepare('SELECT * FROM items').all();
  return Response.json(items?.results);
};
```

### Type Definitions

```typescript
// src/app.d.ts
declare global {
  namespace App {
    interface Platform {
      env: {
        DB: D1Database;
        KV: KVNamespace;
      };
      context: ExecutionContext;
      caches: CacheStorage;
    }
  }
}

export {};
```

---

## Hono

Lightweight web framework optimized for edge computing.

### Quick Start

```bash
npm create cloudflare@latest my-hono-app -- --framework=hono
```

### Manual Setup

```bash
npm create hono@latest my-app
# Select "cloudflare-workers" template
```

### Basic Application

```typescript
// src/index.ts
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { prettyJSON } from 'hono/pretty-json';

type Bindings = {
  DB: D1Database;
  KV: KVNamespace;
};

const app = new Hono<{ Bindings: Bindings }>();

// Middleware
app.use('*', logger());
app.use('*', prettyJSON());
app.use('/api/*', cors());

// Routes
app.get('/', (c) => c.text('Hello Hono!'));

app.get('/api/users', async (c) => {
  const users = await c.env.DB.prepare('SELECT * FROM users').all();
  return c.json(users.results);
});

app.post('/api/users', async (c) => {
  const body = await c.req.json();
  await c.env.DB.prepare('INSERT INTO users (name) VALUES (?)').bind(body.name).run();
  return c.json({ success: true }, 201);
});

app.get('/api/users/:id', async (c) => {
  const id = c.req.param('id');
  const user = await c.env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(id).first();
  if (!user) return c.json({ error: 'Not found' }, 404);
  return c.json(user);
});

// Error handling
app.onError((err, c) => {
  console.error(err);
  return c.json({ error: 'Internal server error' }, 500);
});

app.notFound((c) => c.json({ error: 'Not found' }, 404));

export default app;
```

### Middleware

```typescript
import { Hono } from 'hono';
import { jwt } from 'hono/jwt';
import { rateLimiter } from 'hono/rate-limiter';

const app = new Hono();

// JWT authentication
app.use('/api/*', jwt({ secret: 'your-secret' }));

// Custom middleware
app.use('*', async (c, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  c.res.headers.set('X-Response-Time', `${ms}ms`);
});

// Rate limiting (with KV)
app.use('/api/*', async (c, next) => {
  const ip = c.req.header('CF-Connecting-IP') || 'unknown';
  const key = `rate:${ip}`;
  const count = parseInt(await c.env.KV.get(key) || '0');
  
  if (count > 100) {
    return c.json({ error: 'Rate limited' }, 429);
  }
  
  await c.env.KV.put(key, String(count + 1), { expirationTtl: 60 });
  await next();
});
```

### File Upload with R2

```typescript
app.post('/upload', async (c) => {
  const body = await c.req.parseBody();
  const file = body['file'];
  
  if (!(file instanceof File)) {
    return c.json({ error: 'No file uploaded' }, 400);
  }
  
  const key = `uploads/${crypto.randomUUID()}-${file.name}`;
  await c.env.R2.put(key, file.stream(), {
    httpMetadata: { contentType: file.type }
  });
  
  return c.json({ key });
});
```

---

## React Router (Remix)

React Router v7 with Cloudflare Workers.

### Quick Start

```bash
npx create-react-router@latest --template cloudflare
```

### Configuration

```typescript
// react-router.config.ts
import type { Config } from '@react-router/dev/config';

export default {
  serverBuildFile: 'index.js',
  serverModuleFormat: 'esm',
} satisfies Config;
```

```jsonc
// wrangler.jsonc
{
  "name": "my-remix-app",
  "main": "./build/server/index.js",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "assets": {
    "directory": "./build/client"
  }
}
```

### Loader with Bindings

```typescript
// app/routes/_index.tsx
import type { LoaderFunctionArgs } from 'react-router';
import { useLoaderData } from 'react-router';

export async function loader({ context }: LoaderFunctionArgs) {
  const { env } = context.cloudflare;
  const items = await env.DB.prepare('SELECT * FROM items').all();
  return { items: items.results };
}

export default function Index() {
  const { items } = useLoaderData<typeof loader>();
  return (
    <ul>
      {items.map(item => <li key={item.id}>{item.name}</li>)}
    </ul>
  );
}
```

---

## Nuxt

Vue-based full-stack framework with Nuxt 3.

### Quick Start

```bash
npx nuxi@latest init my-nuxt-app
cd my-nuxt-app
npm install --save-dev wrangler nitro-preset-cloudflare-module
```

### Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  nitro: {
    preset: 'cloudflare-module'
  }
});
```

```jsonc
// wrangler.jsonc
{
  "name": "my-nuxt-app",
  "main": "./.output/server/index.mjs",
  "compatibility_date": "2025-01-01",
  "assets": {
    "directory": "./.output/public"
  }
}
```

### Accessing Bindings

```typescript
// server/api/items.get.ts
export default defineEventHandler(async (event) => {
  const { DB } = event.context.cloudflare.env;
  const items = await DB.prepare('SELECT * FROM items').all();
  return items.results;
});
```

---

## Solid Start

SolidJS full-stack framework.

### Quick Start

```bash
npm create solid@latest my-app
# Select "with-solid-start" and "Cloudflare Workers"
```

### Configuration

```typescript
// app.config.ts
import { defineConfig } from '@solidjs/start/config';

export default defineConfig({
  server: {
    preset: 'cloudflare-module'
  }
});
```

---

## Express.js

Express applications on Cloudflare Workers.

### Setup

```bash
npm install express express-cloudflare
```

### Application

```typescript
// src/index.ts
import express from 'express';
import { createServer } from 'express-cloudflare';

const app = express();

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Hello from Express on Workers!' });
});

app.get('/api/data', async (req, res) => {
  const env = req.cloudflare?.env;
  const data = await env?.DB.prepare('SELECT * FROM items').all();
  res.json(data?.results);
});

export default createServer(app);
```

### Limitations

- Not all Express middleware is compatible
- File system operations not available
- Session storage needs KV or Durable Objects
- WebSocket handling differs

---

## Framework Comparison

| Framework | SSR | SSG | API Routes | Best For |
|-----------|-----|-----|------------|----------|
| React (Vite) | No | Yes | Worker | SPAs with API |
| Vue (Vite) | No | Yes | Worker | SPAs with API |
| Next.js | Yes | Yes | Yes | Full-stack React |
| Astro | Yes | Yes | Yes | Content sites |
| SvelteKit | Yes | Yes | Yes | Full-stack Svelte |
| Hono | N/A | N/A | Yes | APIs, microservices |
| React Router | Yes | Yes | Yes | Full-stack React |
| Nuxt | Yes | Yes | Yes | Full-stack Vue |

## Common Patterns

### Environment Variables

```typescript
// Type-safe env access
interface Env {
  DB: D1Database;
  KV: KVNamespace;
  API_KEY: string;
}

// Access in framework
const env = platform?.env;  // SvelteKit
const env = context.cloudflare.env;  // React Router
const env = Astro.locals.runtime.env;  // Astro
const env = c.env;  // Hono
```

### Development vs Production

```jsonc
// wrangler.jsonc
{
  "name": "my-app",
  "env": {
    "production": {
      "vars": { "ENVIRONMENT": "production" },
      "d1_databases": [{ "binding": "DB", "database_id": "prod-id" }]
    },
    "staging": {
      "vars": { "ENVIRONMENT": "staging" },
      "d1_databases": [{ "binding": "DB", "database_id": "staging-id" }]
    }
  }
}
```

### Error Handling

```typescript
// Global error boundary
try {
  const response = await handleRequest(request, env);
  return response;
} catch (error) {
  console.error('Unhandled error:', error);
  return new Response('Internal Server Error', { status: 500 });
}
```

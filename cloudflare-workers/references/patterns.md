# Cloudflare Workers Architectural Patterns

Common patterns, best practices, and solutions for building applications on Cloudflare Workers.

## Table of Contents

1. [API Design Patterns](#api-design-patterns)
2. [Caching Strategies](#caching-strategies)
3. [Authentication & Authorization](#authentication--authorization)
4. [Rate Limiting](#rate-limiting)
5. [Error Handling](#error-handling)
6. [Database Patterns](#database-patterns)
7. [File Upload Patterns](#file-upload-patterns)
8. [Real-time Applications](#real-time-applications)
9. [AI/ML Patterns](#aiml-patterns)
10. [Testing Patterns](#testing-patterns)
11. [Performance Optimization](#performance-optimization)
12. [Security Best Practices](#security-best-practices)

---

## API Design Patterns

### Router Pattern

```typescript
type RouteHandler = (request: Request, env: Env, ctx: ExecutionContext) => Promise<Response>;

class Router {
  private routes: Map<string, Map<string, RouteHandler>> = new Map();
  
  on(method: string, path: string, handler: RouteHandler) {
    if (!this.routes.has(method)) {
      this.routes.set(method, new Map());
    }
    this.routes.get(method)!.set(path, handler);
    return this;
  }
  
  get(path: string, handler: RouteHandler) { return this.on('GET', path, handler); }
  post(path: string, handler: RouteHandler) { return this.on('POST', path, handler); }
  put(path: string, handler: RouteHandler) { return this.on('PUT', path, handler); }
  delete(path: string, handler: RouteHandler) { return this.on('DELETE', path, handler); }
  
  async handle(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const method = request.method;
    const methodRoutes = this.routes.get(method);
    
    if (methodRoutes) {
      // Exact match
      const handler = methodRoutes.get(url.pathname);
      if (handler) return handler(request, env, ctx);
      
      // Pattern matching (simple)
      for (const [pattern, handler] of methodRoutes) {
        if (this.matchPattern(pattern, url.pathname)) {
          return handler(request, env, ctx);
        }
      }
    }
    
    return new Response('Not Found', { status: 404 });
  }
  
  private matchPattern(pattern: string, path: string): boolean {
    const regex = new RegExp('^' + pattern.replace(/:\w+/g, '([^/]+)') + '$');
    return regex.test(path);
  }
}

// Usage
const router = new Router();

router
  .get('/api/users', listUsers)
  .get('/api/users/:id', getUser)
  .post('/api/users', createUser)
  .put('/api/users/:id', updateUser)
  .delete('/api/users/:id', deleteUser);

export default {
  fetch: (request, env, ctx) => router.handle(request, env, ctx)
};
```

### Middleware Pattern

```typescript
type Middleware = (
  request: Request,
  env: Env,
  ctx: ExecutionContext,
  next: () => Promise<Response>
) => Promise<Response>;

function compose(middlewares: Middleware[]): Middleware {
  return async (request, env, ctx, next) => {
    let index = -1;
    
    async function dispatch(i: number): Promise<Response> {
      if (i <= index) throw new Error('next() called multiple times');
      index = i;
      
      const middleware = middlewares[i];
      if (!middleware) return next();
      
      return middleware(request, env, ctx, () => dispatch(i + 1));
    }
    
    return dispatch(0);
  };
}

// Middleware examples
const logger: Middleware = async (request, env, ctx, next) => {
  const start = Date.now();
  const response = await next();
  console.log(`${request.method} ${request.url} - ${Date.now() - start}ms`);
  return response;
};

const cors: Middleware = async (request, env, ctx, next) => {
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      }
    });
  }
  
  const response = await next();
  response.headers.set('Access-Control-Allow-Origin', '*');
  return response;
};

const auth: Middleware = async (request, env, ctx, next) => {
  const token = request.headers.get('Authorization')?.replace('Bearer ', '');
  if (!token) return new Response('Unauthorized', { status: 401 });
  
  // Verify token...
  return next();
};

// Usage
const middlewareStack = compose([logger, cors, auth]);
```

### RESTful Resource Pattern

```typescript
interface Resource<T> {
  list(env: Env): Promise<T[]>;
  get(id: string, env: Env): Promise<T | null>;
  create(data: Partial<T>, env: Env): Promise<T>;
  update(id: string, data: Partial<T>, env: Env): Promise<T | null>;
  delete(id: string, env: Env): Promise<boolean>;
}

class UserResource implements Resource<User> {
  async list(env: Env) {
    const result = await env.DB.prepare('SELECT * FROM users').all();
    return result.results as User[];
  }
  
  async get(id: string, env: Env) {
    return env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(id).first<User>();
  }
  
  async create(data: Partial<User>, env: Env) {
    const id = crypto.randomUUID();
    await env.DB.prepare('INSERT INTO users (id, name, email) VALUES (?, ?, ?)')
      .bind(id, data.name, data.email)
      .run();
    return this.get(id, env) as Promise<User>;
  }
  
  async update(id: string, data: Partial<User>, env: Env) {
    const sets = Object.keys(data).map(k => `${k} = ?`).join(', ');
    await env.DB.prepare(`UPDATE users SET ${sets} WHERE id = ?`)
      .bind(...Object.values(data), id)
      .run();
    return this.get(id, env);
  }
  
  async delete(id: string, env: Env) {
    const result = await env.DB.prepare('DELETE FROM users WHERE id = ?').bind(id).run();
    return result.meta.changes > 0;
  }
}

// Generic REST handler
function createResourceHandler<T>(resource: Resource<T>) {
  return async (request: Request, env: Env): Promise<Response> => {
    const url = new URL(request.url);
    const pathParts = url.pathname.split('/').filter(Boolean);
    const id = pathParts[pathParts.length - 1];
    
    switch (request.method) {
      case 'GET':
        if (id && id !== pathParts[pathParts.length - 2]) {
          const item = await resource.get(id, env);
          if (!item) return Response.json({ error: 'Not found' }, { status: 404 });
          return Response.json(item);
        }
        return Response.json(await resource.list(env));
        
      case 'POST':
        const createData = await request.json();
        return Response.json(await resource.create(createData, env), { status: 201 });
        
      case 'PUT':
        const updateData = await request.json();
        const updated = await resource.update(id, updateData, env);
        if (!updated) return Response.json({ error: 'Not found' }, { status: 404 });
        return Response.json(updated);
        
      case 'DELETE':
        const deleted = await resource.delete(id, env);
        if (!deleted) return Response.json({ error: 'Not found' }, { status: 404 });
        return new Response(null, { status: 204 });
        
      default:
        return Response.json({ error: 'Method not allowed' }, { status: 405 });
    }
  };
}
```

---

## Caching Strategies

### Cache-Aside Pattern

```typescript
async function getCachedData<T>(
  key: string,
  env: Env,
  fetchFn: () => Promise<T>,
  ttl = 3600
): Promise<T> {
  // Try KV cache first
  const cached = await env.KV.get(key, 'json');
  if (cached) return cached as T;
  
  // Fetch fresh data
  const data = await fetchFn();
  
  // Store in cache
  await env.KV.put(key, JSON.stringify(data), { expirationTtl: ttl });
  
  return data;
}

// Usage
const users = await getCachedData(
  'users:all',
  env,
  () => env.DB.prepare('SELECT * FROM users').all().then(r => r.results),
  300  // 5 minutes
);
```

### Stale-While-Revalidate

```typescript
async function staleWhileRevalidate<T>(
  key: string,
  env: Env,
  ctx: ExecutionContext,
  fetchFn: () => Promise<T>,
  staleTtl = 60,
  maxAge = 3600
): Promise<T> {
  const cacheKey = `swr:${key}`;
  const metaKey = `swr-meta:${key}`;
  
  const [cached, meta] = await Promise.all([
    env.KV.get(cacheKey, 'json'),
    env.KV.get(metaKey, 'json') as Promise<{ timestamp: number } | null>
  ]);
  
  const now = Date.now();
  const isStale = meta && (now - meta.timestamp) > staleTtl * 1000;
  const isExpired = meta && (now - meta.timestamp) > maxAge * 1000;
  
  if (cached && !isExpired) {
    if (isStale) {
      // Revalidate in background
      ctx.waitUntil((async () => {
        const fresh = await fetchFn();
        await Promise.all([
          env.KV.put(cacheKey, JSON.stringify(fresh)),
          env.KV.put(metaKey, JSON.stringify({ timestamp: Date.now() }))
        ]);
      })());
    }
    return cached as T;
  }
  
  // Fetch fresh
  const fresh = await fetchFn();
  await Promise.all([
    env.KV.put(cacheKey, JSON.stringify(fresh)),
    env.KV.put(metaKey, JSON.stringify({ timestamp: Date.now() }))
  ]);
  
  return fresh;
}
```

### Edge Cache with Cache API

```typescript
async function edgeCachedFetch(
  request: Request,
  ctx: ExecutionContext,
  ttl = 3600
): Promise<Response> {
  const cache = caches.default;
  const cacheKey = new Request(request.url, { method: 'GET' });
  
  let response = await cache.match(cacheKey);
  
  if (!response) {
    response = await fetch(request);
    response = new Response(response.body, response);
    response.headers.set('Cache-Control', `public, max-age=${ttl}`);
    
    ctx.waitUntil(cache.put(cacheKey, response.clone()));
  }
  
  return response;
}
```

---

## Authentication & Authorization

### JWT Authentication

```typescript
import { SignJWT, jwtVerify } from 'jose';

const JWT_SECRET = new TextEncoder().encode('your-secret-key');

async function createToken(payload: Record<string, unknown>): Promise<string> {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('24h')
    .sign(JWT_SECRET);
}

async function verifyToken(token: string): Promise<Record<string, unknown> | null> {
  try {
    const { payload } = await jwtVerify(token, JWT_SECRET);
    return payload as Record<string, unknown>;
  } catch {
    return null;
  }
}

// Middleware
async function authMiddleware(request: Request, env: Env): Promise<{ user: User } | Response> {
  const token = request.headers.get('Authorization')?.replace('Bearer ', '');
  
  if (!token) {
    return Response.json({ error: 'No token provided' }, { status: 401 });
  }
  
  const payload = await verifyToken(token);
  if (!payload) {
    return Response.json({ error: 'Invalid token' }, { status: 401 });
  }
  
  const user = await env.DB.prepare('SELECT * FROM users WHERE id = ?')
    .bind(payload.userId)
    .first<User>();
    
  if (!user) {
    return Response.json({ error: 'User not found' }, { status: 401 });
  }
  
  return { user };
}
```

### API Key Authentication

```typescript
async function apiKeyAuth(request: Request, env: Env): Promise<{ client: Client } | Response> {
  const apiKey = request.headers.get('X-API-Key');
  
  if (!apiKey) {
    return Response.json({ error: 'API key required' }, { status: 401 });
  }
  
  // Hash the key for lookup
  const keyHash = await crypto.subtle.digest(
    'SHA-256',
    new TextEncoder().encode(apiKey)
  );
  const keyHashHex = [...new Uint8Array(keyHash)]
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
  
  const client = await env.DB.prepare('SELECT * FROM api_clients WHERE key_hash = ?')
    .bind(keyHashHex)
    .first<Client>();
    
  if (!client) {
    return Response.json({ error: 'Invalid API key' }, { status: 401 });
  }
  
  return { client };
}
```

### OAuth 2.0 Flow

```typescript
// OAuth redirect
async function handleOAuthRedirect(request: Request, env: Env): Promise<Response> {
  const state = crypto.randomUUID();
  await env.KV.put(`oauth:state:${state}`, '1', { expirationTtl: 600 });
  
  const authUrl = new URL('https://github.com/login/oauth/authorize');
  authUrl.searchParams.set('client_id', env.GITHUB_CLIENT_ID);
  authUrl.searchParams.set('redirect_uri', `${env.APP_URL}/auth/callback`);
  authUrl.searchParams.set('scope', 'user:email');
  authUrl.searchParams.set('state', state);
  
  return Response.redirect(authUrl.toString());
}

// OAuth callback
async function handleOAuthCallback(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  
  // Verify state
  const storedState = await env.KV.get(`oauth:state:${state}`);
  if (!storedState) {
    return Response.json({ error: 'Invalid state' }, { status: 400 });
  }
  await env.KV.delete(`oauth:state:${state}`);
  
  // Exchange code for token
  const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify({
      client_id: env.GITHUB_CLIENT_ID,
      client_secret: env.GITHUB_CLIENT_SECRET,
      code
    })
  });
  
  const { access_token } = await tokenResponse.json();
  
  // Get user info
  const userResponse = await fetch('https://api.github.com/user', {
    headers: { 'Authorization': `Bearer ${access_token}` }
  });
  
  const githubUser = await userResponse.json();
  
  // Create or update user...
  const token = await createToken({ userId: user.id });
  
  return Response.redirect(`${env.APP_URL}?token=${token}`);
}
```

---

## Rate Limiting

### Sliding Window Rate Limiter

```typescript
async function rateLimitRequest(
  identifier: string,
  env: Env,
  limit: number,
  windowSeconds: number
): Promise<{ allowed: boolean; remaining: number; resetAt: number }> {
  const now = Date.now();
  const windowStart = now - (windowSeconds * 1000);
  const key = `ratelimit:${identifier}`;
  
  // Get current timestamps
  const stored = await env.KV.get(key, 'json') as number[] | null;
  const timestamps = (stored || []).filter(ts => ts > windowStart);
  
  if (timestamps.length >= limit) {
    return {
      allowed: false,
      remaining: 0,
      resetAt: Math.ceil((timestamps[0] + windowSeconds * 1000) / 1000)
    };
  }
  
  // Add current timestamp
  timestamps.push(now);
  await env.KV.put(key, JSON.stringify(timestamps), { expirationTtl: windowSeconds * 2 });
  
  return {
    allowed: true,
    remaining: limit - timestamps.length,
    resetAt: Math.ceil((now + windowSeconds * 1000) / 1000)
  };
}

// Middleware
async function rateLimitMiddleware(request: Request, env: Env): Promise<Response | null> {
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const result = await rateLimitRequest(ip, env, 100, 60);  // 100 requests per minute
  
  if (!result.allowed) {
    return new Response('Too Many Requests', {
      status: 429,
      headers: {
        'X-RateLimit-Remaining': '0',
        'X-RateLimit-Reset': result.resetAt.toString(),
        'Retry-After': String(result.resetAt - Math.floor(Date.now() / 1000))
      }
    });
  }
  
  return null;  // Continue
}
```

### Token Bucket with Durable Objects

```typescript
export class RateLimiter implements DurableObject {
  private tokens: number;
  private lastRefill: number;
  private readonly maxTokens: number = 100;
  private readonly refillRate: number = 10;  // tokens per second
  
  constructor(state: DurableObjectState) {
    this.tokens = this.maxTokens;
    this.lastRefill = Date.now();
  }
  
  private refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(this.maxTokens, this.tokens + elapsed * this.refillRate);
    this.lastRefill = now;
  }
  
  async fetch(request: Request): Promise<Response> {
    this.refill();
    
    if (this.tokens < 1) {
      return Response.json({ allowed: false, tokens: 0 }, { status: 429 });
    }
    
    this.tokens -= 1;
    return Response.json({ allowed: true, tokens: Math.floor(this.tokens) });
  }
}
```

---

## Error Handling

### Global Error Handler

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR'
  ) {
    super(message);
    this.name = 'AppError';
  }
}

function errorHandler(error: unknown): Response {
  console.error('Error:', error);
  
  if (error instanceof AppError) {
    return Response.json({
      error: {
        code: error.code,
        message: error.message
      }
    }, { status: error.statusCode });
  }
  
  if (error instanceof SyntaxError) {
    return Response.json({
      error: {
        code: 'INVALID_JSON',
        message: 'Invalid JSON in request body'
      }
    }, { status: 400 });
  }
  
  return Response.json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  }, { status: 500 });
}

// Wrapper
function withErrorHandling(handler: (request: Request, env: Env, ctx: ExecutionContext) => Promise<Response>) {
  return async (request: Request, env: Env, ctx: ExecutionContext): Promise<Response> => {
    try {
      return await handler(request, env, ctx);
    } catch (error) {
      return errorHandler(error);
    }
  };
}

// Usage
export default {
  fetch: withErrorHandling(async (request, env, ctx) => {
    // Your handler code
    throw new AppError('User not found', 404, 'USER_NOT_FOUND');
  })
};
```

### Validation with Zod

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().positive().optional()
});

async function validateBody<T>(request: Request, schema: z.ZodSchema<T>): Promise<T> {
  const body = await request.json();
  const result = schema.safeParse(body);
  
  if (!result.success) {
    throw new AppError(
      `Validation error: ${result.error.issues.map(i => i.message).join(', ')}`,
      400,
      'VALIDATION_ERROR'
    );
  }
  
  return result.data;
}

// Usage
const userData = await validateBody(request, CreateUserSchema);
```

---

## Database Patterns

### Repository Pattern

```typescript
abstract class Repository<T extends { id: string }> {
  constructor(protected db: D1Database, protected table: string) {}
  
  async findAll(options?: { limit?: number; offset?: number }): Promise<T[]> {
    let query = `SELECT * FROM ${this.table}`;
    if (options?.limit) query += ` LIMIT ${options.limit}`;
    if (options?.offset) query += ` OFFSET ${options.offset}`;
    const result = await this.db.prepare(query).all();
    return result.results as T[];
  }
  
  async findById(id: string): Promise<T | null> {
    return this.db.prepare(`SELECT * FROM ${this.table} WHERE id = ?`).bind(id).first<T>();
  }
  
  async create(data: Omit<T, 'id'>): Promise<T> {
    const id = crypto.randomUUID();
    const keys = Object.keys(data);
    const values = Object.values(data);
    const placeholders = keys.map(() => '?').join(', ');
    
    await this.db.prepare(
      `INSERT INTO ${this.table} (id, ${keys.join(', ')}) VALUES (?, ${placeholders})`
    ).bind(id, ...values).run();
    
    return { id, ...data } as T;
  }
  
  async update(id: string, data: Partial<T>): Promise<T | null> {
    const keys = Object.keys(data);
    const values = Object.values(data);
    const sets = keys.map(k => `${k} = ?`).join(', ');
    
    await this.db.prepare(`UPDATE ${this.table} SET ${sets} WHERE id = ?`)
      .bind(...values, id)
      .run();
    
    return this.findById(id);
  }
  
  async delete(id: string): Promise<boolean> {
    const result = await this.db.prepare(`DELETE FROM ${this.table} WHERE id = ?`)
      .bind(id)
      .run();
    return result.meta.changes > 0;
  }
}

class UserRepository extends Repository<User> {
  constructor(db: D1Database) {
    super(db, 'users');
  }
  
  async findByEmail(email: string): Promise<User | null> {
    return this.db.prepare('SELECT * FROM users WHERE email = ?').bind(email).first<User>();
  }
}
```

### Unit of Work Pattern

```typescript
class UnitOfWork {
  private statements: D1PreparedStatement[] = [];
  
  constructor(private db: D1Database) {}
  
  addStatement(statement: D1PreparedStatement) {
    this.statements.push(statement);
  }
  
  async commit(): Promise<D1Result[]> {
    const results = await this.db.batch(this.statements);
    this.statements = [];
    return results;
  }
}

// Usage
const uow = new UnitOfWork(env.DB);

uow.addStatement(
  env.DB.prepare('INSERT INTO orders (id, user_id, total) VALUES (?, ?, ?)')
    .bind(orderId, userId, total)
);

uow.addStatement(
  env.DB.prepare('UPDATE inventory SET quantity = quantity - ? WHERE product_id = ?')
    .bind(quantity, productId)
);

uow.addStatement(
  env.DB.prepare('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)')
    .bind(orderId, productId, quantity)
);

await uow.commit();  // All or nothing
```

---

## AI/ML Patterns

### RAG (Retrieval-Augmented Generation)

```typescript
async function ragQuery(query: string, env: Env): Promise<string> {
  // 1. Generate query embedding
  const { data: embeddings } = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
    text: [query]
  });
  
  // 2. Search vector database
  const searchResults = await env.VECTORIZE.query(embeddings[0], {
    topK: 5,
    returnMetadata: 'all'
  });
  
  // 3. Build context from results
  const context = searchResults.matches
    .filter(m => m.score > 0.7)
    .map(m => m.metadata?.content)
    .join('\n\n---\n\n');
  
  if (!context) {
    return "I don't have enough information to answer that question.";
  }
  
  // 4. Generate response with context
  const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [
      {
        role: 'system',
        content: `You are a helpful assistant. Answer questions based only on the following context. If the answer is not in the context, say so.

Context:
${context}`
      },
      { role: 'user', content: query }
    ]
  });
  
  return response.response;
}
```

### Document Indexing Pipeline

```typescript
async function indexDocument(
  document: { id: string; title: string; content: string },
  env: Env
): Promise<void> {
  // Split into chunks
  const chunks = splitIntoChunks(document.content, 500);
  
  // Generate embeddings for all chunks
  const { data: embeddings } = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
    text: chunks
  });
  
  // Upsert vectors
  const vectors = chunks.map((chunk, i) => ({
    id: `${document.id}-${i}`,
    values: embeddings[i],
    metadata: {
      documentId: document.id,
      title: document.title,
      content: chunk,
      chunkIndex: i
    }
  }));
  
  await env.VECTORIZE.upsert(vectors);
}

function splitIntoChunks(text: string, maxWords: number): string[] {
  const words = text.split(/\s+/);
  const chunks: string[] = [];
  
  for (let i = 0; i < words.length; i += maxWords) {
    chunks.push(words.slice(i, i + maxWords).join(' '));
  }
  
  return chunks;
}
```

---

## Performance Optimization

### Request Coalescing

```typescript
const inflightRequests = new Map<string, Promise<Response>>();

async function coalescedFetch(url: string): Promise<Response> {
  const existing = inflightRequests.get(url);
  if (existing) return existing.then(r => r.clone());
  
  const promise = fetch(url);
  inflightRequests.set(url, promise);
  
  try {
    const response = await promise;
    return response;
  } finally {
    inflightRequests.delete(url);
  }
}
```

### Parallel Processing

```typescript
async function processInParallel<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  concurrency: number = 5
): Promise<R[]> {
  const results: R[] = [];
  const executing: Promise<void>[] = [];
  
  for (const item of items) {
    const promise = processor(item).then(result => {
      results.push(result);
    });
    
    executing.push(promise);
    
    if (executing.length >= concurrency) {
      await Promise.race(executing);
      executing.splice(0, executing.findIndex(p => p !== promise) + 1);
    }
  }
  
  await Promise.all(executing);
  return results;
}

// Usage
const urls = ['url1', 'url2', 'url3', ...];
const responses = await processInParallel(urls, url => fetch(url), 10);
```

### Response Streaming

```typescript
function streamJsonArray<T>(items: AsyncIterable<T>): Response {
  const { readable, writable } = new TransformStream();
  const writer = writable.getWriter();
  const encoder = new TextEncoder();
  
  (async () => {
    await writer.write(encoder.encode('['));
    let first = true;
    
    for await (const item of items) {
      if (!first) await writer.write(encoder.encode(','));
      await writer.write(encoder.encode(JSON.stringify(item)));
      first = false;
    }
    
    await writer.write(encoder.encode(']'));
    await writer.close();
  })();
  
  return new Response(readable, {
    headers: { 'Content-Type': 'application/json' }
  });
}
```

---

## Security Best Practices

### Input Sanitization

```typescript
function sanitizeHtml(html: string): string {
  return html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

function sanitizeSql(input: string): string {
  // Always use parameterized queries instead!
  // This is just for display purposes
  return input.replace(/'/g, "''");
}
```

### CORS Configuration

```typescript
function corsHeaders(origin: string, allowedOrigins: string[]): Headers {
  const headers = new Headers();
  
  if (allowedOrigins.includes(origin) || allowedOrigins.includes('*')) {
    headers.set('Access-Control-Allow-Origin', origin);
    headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    headers.set('Access-Control-Max-Age', '86400');
  }
  
  return headers;
}
```

### Content Security Policy

```typescript
function addSecurityHeaders(response: Response): Response {
  const newResponse = new Response(response.body, response);
  
  newResponse.headers.set('Content-Security-Policy', 
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
  );
  newResponse.headers.set('X-Content-Type-Options', 'nosniff');
  newResponse.headers.set('X-Frame-Options', 'DENY');
  newResponse.headers.set('X-XSS-Protection', '1; mode=block');
  newResponse.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  newResponse.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  
  return newResponse;
}
```

# Cloudflare Workers Bindings Reference

Complete configuration and usage guide for all Cloudflare Workers bindings.

## Table of Contents

1. [KV Namespaces](#kv-namespaces)
2. [R2 Buckets](#r2-buckets)
3. [D1 Databases](#d1-databases)
4. [Durable Objects](#durable-objects)
5. [Queues](#queues)
6. [Workers AI](#workers-ai)
7. [Vectorize](#vectorize)
8. [Hyperdrive](#hyperdrive)
9. [Service Bindings](#service-bindings)
10. [Browser Rendering](#browser-rendering)
11. [Analytics Engine](#analytics-engine)
12. [Rate Limiting](#rate-limiting)
13. [mTLS Certificates](#mtls-certificates)

---

## KV Namespaces

Low-latency key-value storage optimized for read-heavy workloads with edge caching.

### Configuration

```jsonc
// wrangler.jsonc
{
  "kv_namespaces": [
    {
      "binding": "CACHE",           // Variable name in code
      "id": "abc123def456",         // Namespace ID (production)
      "preview_id": "preview123"    // Namespace ID (wrangler dev)
    }
  ]
}
```

### TypeScript Interface

```typescript
interface Env {
  CACHE: KVNamespace;
}
```

### API Methods

```typescript
// PUT - Write value
await env.CACHE.put(key: string, value: string | ArrayBuffer | ReadableStream, options?: {
  expiration?: number;      // Unix timestamp (seconds)
  expirationTtl?: number;   // Seconds from now
  metadata?: object;        // JSON-serializable metadata
});

// GET - Read value
const value = await env.CACHE.get(key: string, options?: {
  type?: 'text' | 'json' | 'arrayBuffer' | 'stream';
  cacheTtl?: number;        // Override cache TTL
});

// GET with metadata
const { value, metadata } = await env.CACHE.getWithMetadata(key, { type: 'json' });

// DELETE
await env.CACHE.delete(key: string);

// LIST - Enumerate keys
const result = await env.CACHE.list({
  prefix?: string;
  limit?: number;           // Max 1000
  cursor?: string;          // Pagination cursor
});
// Returns: { keys: [{name, expiration?, metadata?}], list_complete, cursor? }
```

### Usage Patterns

```typescript
// Caching with TTL
async function getCachedData(env: Env, key: string) {
  const cached = await env.CACHE.get(key, 'json');
  if (cached) return cached;
  
  const fresh = await fetchFromOrigin(key);
  await env.CACHE.put(key, JSON.stringify(fresh), { expirationTtl: 3600 });
  return fresh;
}

// Session storage with metadata
await env.CACHE.put(`session:${sessionId}`, JSON.stringify(userData), {
  expirationTtl: 86400,
  metadata: { userId: user.id, createdAt: Date.now() }
});
```

---

## R2 Buckets

S3-compatible object storage with zero egress fees.

### Configuration

```jsonc
{
  "r2_buckets": [
    {
      "binding": "STORAGE",
      "bucket_name": "my-bucket",
      "preview_bucket_name": "my-bucket-dev",  // Optional
      "jurisdiction": "eu"                      // Optional: "eu" for EU-only storage
    }
  ]
}
```

### TypeScript Interface

```typescript
interface Env {
  STORAGE: R2Bucket;
}

interface R2Object {
  key: string;
  version: string;
  size: number;
  etag: string;
  httpEtag: string;
  uploaded: Date;
  httpMetadata?: R2HTTPMetadata;
  customMetadata?: Record<string, string>;
  body: ReadableStream;       // Only on get()
  bodyUsed: boolean;
  arrayBuffer(): Promise<ArrayBuffer>;
  text(): Promise<string>;
  json<T>(): Promise<T>;
  blob(): Promise<Blob>;
}
```

### API Methods

```typescript
// PUT - Upload object
const object = await env.STORAGE.put(key: string, value: ReadableStream | ArrayBuffer | string | Blob, {
  httpMetadata?: {
    contentType?: string;
    contentLanguage?: string;
    contentDisposition?: string;
    contentEncoding?: string;
    cacheControl?: string;
    cacheExpiry?: Date;
  };
  customMetadata?: Record<string, string>;
  md5?: ArrayBuffer | string;  // Verify integrity
  sha1?: ArrayBuffer | string;
  sha256?: ArrayBuffer | string;
  sha384?: ArrayBuffer | string;
  sha512?: ArrayBuffer | string;
});

// GET - Download object
const object = await env.STORAGE.get(key: string, {
  onlyIf?: {
    etagMatches?: string;
    etagDoesNotMatch?: string;
    uploadedBefore?: Date;
    uploadedAfter?: Date;
  };
  range?: { offset?: number; length?: number; suffix?: number };
});

// HEAD - Get metadata without body
const head = await env.STORAGE.head(key: string);

// DELETE - Single or multiple
await env.STORAGE.delete(key: string);
await env.STORAGE.delete(keys: string[]);  // Batch delete

// LIST - Enumerate objects
const result = await env.STORAGE.list({
  prefix?: string;
  delimiter?: string;         // For "folder" simulation
  cursor?: string;
  limit?: number;             // Max 1000
  include?: ('httpMetadata' | 'customMetadata')[];
});
// Returns: { objects, truncated, cursor?, delimitedPrefixes }

// Multipart uploads (large files)
const upload = await env.STORAGE.createMultipartUpload(key, { httpMetadata, customMetadata });
const part = await upload.uploadPart(partNumber, data);
const object = await upload.complete([part1, part2, ...]);
await upload.abort();  // Cancel upload
```

### Usage Patterns

```typescript
// File upload endpoint
async function handleUpload(request: Request, env: Env) {
  const formData = await request.formData();
  const file = formData.get('file') as File;
  
  const key = `uploads/${crypto.randomUUID()}/${file.name}`;
  await env.STORAGE.put(key, file.stream(), {
    httpMetadata: { contentType: file.type }
  });
  
  return Response.json({ key });
}

// Presigned URL pattern (via Worker)
async function servePrivateFile(request: Request, env: Env) {
  const url = new URL(request.url);
  const key = url.pathname.slice(1);
  
  const object = await env.STORAGE.get(key);
  if (!object) return new Response('Not Found', { status: 404 });
  
  return new Response(object.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
      'Cache-Control': 'private, max-age=3600'
    }
  });
}
```

---

## D1 Databases

Serverless SQLite database with automatic replication.

### Configuration

```jsonc
{
  "d1_databases": [
    {
      "binding": "DB",
      "database_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "database_name": "my-database"
    }
  ]
}
```

### CLI Commands

```bash
# Create database
npx wrangler d1 create my-database

# Execute SQL
npx wrangler d1 execute my-database --command "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"

# Execute from file
npx wrangler d1 execute my-database --file schema.sql

# Local development (uses local SQLite)
npx wrangler d1 execute my-database --local --command "SELECT * FROM users"
```

### TypeScript Interface

```typescript
interface Env {
  DB: D1Database;
}

interface D1Database {
  prepare(query: string): D1PreparedStatement;
  batch<T = unknown>(statements: D1PreparedStatement[]): Promise<D1Result<T>[]>;
  exec(query: string): Promise<D1ExecResult>;  // Raw SQL (no binding)
  dump(): Promise<ArrayBuffer>;  // Export database
}

interface D1PreparedStatement {
  bind(...values: unknown[]): D1PreparedStatement;
  first<T = unknown>(colName?: string): Promise<T | null>;
  all<T = unknown>(): Promise<D1Result<T>>;
  run(): Promise<D1Result>;
  raw<T = unknown[]>(): Promise<T[]>;  // Array of arrays
}

interface D1Result<T = unknown> {
  results: T[];
  success: boolean;
  meta: {
    duration: number;
    rows_read: number;
    rows_written: number;
    last_row_id: number;
    changed_db: boolean;
    size_after: number;
    changes: number;
  };
}
```

### API Methods

```typescript
// Prepared statements (ALWAYS use for user input)
const user = await env.DB
  .prepare('SELECT * FROM users WHERE id = ?')
  .bind(userId)
  .first();

// Multiple bindings
const results = await env.DB
  .prepare('SELECT * FROM users WHERE status = ? AND created_at > ?')
  .bind('active', '2024-01-01')
  .all();

// Insert/Update/Delete
const result = await env.DB
  .prepare('INSERT INTO users (name, email) VALUES (?, ?)')
  .bind(name, email)
  .run();
console.log(result.meta.last_row_id);

// Batch operations (transactional)
const results = await env.DB.batch([
  env.DB.prepare('INSERT INTO users (name) VALUES (?)').bind('Alice'),
  env.DB.prepare('INSERT INTO users (name) VALUES (?)').bind('Bob'),
  env.DB.prepare('UPDATE stats SET user_count = user_count + 2')
]);

// Raw query (avoid for user input)
await env.DB.exec('PRAGMA table_info(users)');
```

### Usage Patterns

```typescript
// Repository pattern
class UserRepository {
  constructor(private db: D1Database) {}
  
  async findById(id: number) {
    return this.db.prepare('SELECT * FROM users WHERE id = ?').bind(id).first();
  }
  
  async create(data: { name: string; email: string }) {
    const result = await this.db
      .prepare('INSERT INTO users (name, email) VALUES (?, ?) RETURNING *')
      .bind(data.name, data.email)
      .first();
    return result;
  }
  
  async search(query: string, limit = 10) {
    return this.db
      .prepare('SELECT * FROM users WHERE name LIKE ? LIMIT ?')
      .bind(`%${query}%`, limit)
      .all();
  }
}
```

---

## Durable Objects

Globally distributed stateful objects for coordination and WebSockets.

### Configuration

```jsonc
{
  "durable_objects": {
    "bindings": [
      {
        "name": "COUNTER",           // Binding name
        "class_name": "Counter"      // Class name in code
      },
      {
        "name": "ROOMS",
        "class_name": "ChatRoom",
        "script_name": "chat-worker"  // Optional: different Worker
      }
    ]
  },
  "migrations": [
    { "tag": "v1", "new_classes": ["Counter", "ChatRoom"] }
  ]
}
```

### TypeScript Implementation

```typescript
// Durable Object class
export class Counter implements DurableObject {
  private state: DurableObjectState;
  private value: number = 0;
  
  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    // Restore state from storage
    this.state.blockConcurrencyWhile(async () => {
      this.value = await this.state.storage.get('value') || 0;
    });
  }
  
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    switch (url.pathname) {
      case '/increment':
        this.value++;
        await this.state.storage.put('value', this.value);
        return Response.json({ value: this.value });
      
      case '/get':
        return Response.json({ value: this.value });
      
      default:
        return new Response('Not Found', { status: 404 });
    }
  }
}

// Export in main Worker
export { Counter };
export default {
  async fetch(request: Request, env: Env) {
    const id = env.COUNTER.idFromName('global-counter');
    const stub = env.COUNTER.get(id);
    return stub.fetch(request);
  }
};
```

### Durable Object with WebSockets

```typescript
export class ChatRoom implements DurableObject {
  private sessions: Map<WebSocket, { name: string }> = new Map();
  
  constructor(private state: DurableObjectState, private env: Env) {
    this.state.getWebSockets().forEach(ws => {
      this.sessions.set(ws, ws.deserializeAttachment());
    });
  }
  
  async fetch(request: Request): Promise<Response> {
    if (request.headers.get('Upgrade') === 'websocket') {
      const [client, server] = Object.values(new WebSocketPair());
      
      const name = new URL(request.url).searchParams.get('name') || 'Anonymous';
      server.serializeAttachment({ name });
      this.state.acceptWebSocket(server);
      this.sessions.set(server, { name });
      
      this.broadcast(`${name} joined the chat`);
      
      return new Response(null, { status: 101, webSocket: client });
    }
    
    return new Response('Expected WebSocket', { status: 400 });
  }
  
  async webSocketMessage(ws: WebSocket, message: string) {
    const session = this.sessions.get(ws);
    this.broadcast(`${session?.name}: ${message}`);
  }
  
  async webSocketClose(ws: WebSocket) {
    const session = this.sessions.get(ws);
    this.sessions.delete(ws);
    this.broadcast(`${session?.name} left the chat`);
  }
  
  private broadcast(message: string) {
    for (const ws of this.sessions.keys()) {
      ws.send(message);
    }
  }
}
```

### Storage API

```typescript
// In Durable Object class
async storeData() {
  // Single value
  await this.state.storage.put('key', value);
  const value = await this.state.storage.get('key');
  
  // Multiple values (transactional)
  await this.state.storage.put({ key1: value1, key2: value2 });
  const values = await this.state.storage.get(['key1', 'key2']);
  
  // List keys
  const map = await this.state.storage.list({ prefix: 'user:', limit: 100 });
  
  // Delete
  await this.state.storage.delete('key');
  await this.state.storage.deleteAll();  // Clear everything
  
  // SQL (Durable Objects SQLite)
  const cursor = this.state.storage.sql.exec('SELECT * FROM data WHERE id = ?', id);
  const rows = [...cursor];
}
```

---

## Queues

Message queues with guaranteed delivery and automatic retries.

### Configuration

```jsonc
{
  "queues": {
    "producers": [
      {
        "binding": "TASK_QUEUE",
        "queue": "background-tasks"
      }
    ],
    "consumers": [
      {
        "queue": "background-tasks",
        "max_batch_size": 10,
        "max_batch_timeout": 30,
        "max_retries": 3,
        "dead_letter_queue": "failed-tasks",
        "max_concurrency": 10
      }
    ]
  }
}
```

### Producer (Sending Messages)

```typescript
interface Env {
  TASK_QUEUE: Queue;
}

// Send single message
await env.TASK_QUEUE.send({
  type: 'email',
  to: 'user@example.com',
  subject: 'Hello'
});

// Send with options
await env.TASK_QUEUE.send(payload, {
  contentType: 'json',           // 'json' | 'text' | 'bytes' | 'v8'
  delaySeconds: 60               // Delay delivery
});

// Batch send (up to 100 messages)
await env.TASK_QUEUE.sendBatch([
  { body: { task: 1 } },
  { body: { task: 2 }, delaySeconds: 30 }
]);
```

### Consumer (Processing Messages)

```typescript
export default {
  async queue(batch: MessageBatch<{ type: string; [key: string]: unknown }>, env: Env) {
    for (const message of batch.messages) {
      try {
        await processMessage(message.body, env);
        message.ack();  // Mark as processed
      } catch (error) {
        message.retry({ delaySeconds: 60 });  // Retry later
        // Or: message.ack() to discard
      }
    }
  }
};

// Message interface
interface Message<T> {
  id: string;
  timestamp: Date;
  body: T;
  attempts: number;
  ack(): void;
  retry(options?: { delaySeconds?: number }): void;
}
```

---

## Workers AI

Serverless AI inference with multiple model types.

### Configuration

```jsonc
{
  "ai": {
    "binding": "AI"
  }
}
```

### Available Model Categories

| Category | Models | Use Case |
|----------|--------|----------|
| Text Generation | `@cf/meta/llama-3.1-8b-instruct`, `@cf/mistral/mistral-7b-instruct-v0.2` | Chat, completion |
| Text Embeddings | `@cf/baai/bge-base-en-v1.5`, `@cf/baai/bge-large-en-v1.5` | Semantic search, RAG |
| Image Generation | `@cf/black-forest-labs/flux-1-schnell`, `@cf/stabilityai/stable-diffusion-xl-base-1.0` | Image creation |
| Speech to Text | `@cf/openai/whisper` | Transcription |
| Text Classification | `@cf/huggingface/distilbert-sst-2-int8` | Sentiment analysis |
| Translation | `@cf/meta/m2m100-1.2b` | Language translation |
| Summarization | `@cf/facebook/bart-large-cnn` | Text summarization |
| Object Detection | `@cf/facebook/detr-resnet-50` | Image analysis |

### API Usage

```typescript
interface Env {
  AI: Ai;
}

// Text generation (chat)
const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'What is serverless computing?' }
  ],
  max_tokens: 500,
  temperature: 0.7
});
// response.response contains the text

// Streaming response
const stream = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [...],
  stream: true
});
return new Response(stream, {
  headers: { 'Content-Type': 'text/event-stream' }
});

// Text embeddings
const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
  text: ['Document text to embed', 'Another document']
});
// embeddings.data[0] contains the vector

// Image generation
const image = await env.AI.run('@cf/black-forest-labs/flux-1-schnell', {
  prompt: 'A serene mountain landscape at sunset',
  num_steps: 4
});
return new Response(image, {
  headers: { 'Content-Type': 'image/png' }
});

// Speech to text
const audioData = await request.arrayBuffer();
const transcript = await env.AI.run('@cf/openai/whisper', {
  audio: [...new Uint8Array(audioData)]
});
```

---

## Vectorize

Vector database for semantic search and RAG applications.

### Configuration

```jsonc
{
  "vectorize": [
    {
      "binding": "VECTORS",
      "index_name": "my-index"
    }
  ]
}
```

### CLI Commands

```bash
# Create index
npx wrangler vectorize create my-index --dimensions 768 --metric cosine

# List indexes
npx wrangler vectorize list

# Delete index
npx wrangler vectorize delete my-index
```

### API Usage

```typescript
interface Env {
  VECTORS: VectorizeIndex;
  AI: Ai;
}

// Insert vectors
await env.VECTORS.upsert([
  {
    id: 'doc-1',
    values: [0.1, 0.2, ...],  // 768 dimensions for bge-base
    metadata: { title: 'Document 1', category: 'tech' }
  }
]);

// Insert with AI-generated embeddings
async function indexDocument(text: string, id: string, metadata: object) {
  const { data } = await env.AI.run('@cf/baai/bge-base-en-v1.5', { text: [text] });
  await env.VECTORS.upsert([{
    id,
    values: data[0],
    metadata
  }]);
}

// Query vectors
const { data } = await env.AI.run('@cf/baai/bge-base-en-v1.5', {
  text: ['search query']
});
const results = await env.VECTORS.query(data[0], {
  topK: 5,
  returnMetadata: 'all',
  filter: { category: 'tech' }
});
// results.matches[0] = { id, score, metadata }

// Delete vectors
await env.VECTORS.deleteByIds(['doc-1', 'doc-2']);
```

### RAG Pattern

```typescript
async function ragQuery(query: string, env: Env) {
  // 1. Generate query embedding
  const { data } = await env.AI.run('@cf/baai/bge-base-en-v1.5', { text: [query] });
  
  // 2. Find similar documents
  const results = await env.VECTORS.query(data[0], { topK: 3, returnMetadata: 'all' });
  
  // 3. Build context from results
  const context = results.matches
    .map(m => m.metadata?.content)
    .join('\n\n');
  
  // 4. Generate response with context
  const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [
      { role: 'system', content: `Answer based on this context:\n${context}` },
      { role: 'user', content: query }
    ]
  });
  
  return response.response;
}
```

---

## Hyperdrive

Connection pooling and caching for external PostgreSQL databases.

### Configuration

```jsonc
{
  "hyperdrive": [
    {
      "binding": "HYPERDRIVE",
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  ]
}
```

### CLI Setup

```bash
# Create Hyperdrive config
npx wrangler hyperdrive create my-hyperdrive \
  --connection-string "postgres://user:pass@host:5432/database"
```

### Usage

```typescript
import { Client } from 'pg';

interface Env {
  HYPERDRIVE: Hyperdrive;
}

export default {
  async fetch(request: Request, env: Env) {
    const client = new Client({
      connectionString: env.HYPERDRIVE.connectionString
    });
    
    await client.connect();
    const result = await client.query('SELECT * FROM users LIMIT 10');
    await client.end();
    
    return Response.json(result.rows);
  }
};
```

---

## Service Bindings

Direct Worker-to-Worker communication without HTTP overhead.

### Configuration

```jsonc
{
  "services": [
    {
      "binding": "AUTH_SERVICE",
      "service": "auth-worker",
      "entrypoint": "AuthHandler"  // Optional: named entrypoint
    }
  ]
}
```

### Basic RPC

```typescript
// auth-worker
export default {
  async fetch(request: Request) {
    const { action, token } = await request.json();
    if (action === 'verify') {
      const user = verifyToken(token);
      return Response.json({ valid: true, user });
    }
  }
};

// main-worker
interface Env {
  AUTH_SERVICE: Fetcher;
}

export default {
  async fetch(request: Request, env: Env) {
    const token = request.headers.get('Authorization')?.replace('Bearer ', '');
    
    const authResponse = await env.AUTH_SERVICE.fetch('http://auth/', {
      method: 'POST',
      body: JSON.stringify({ action: 'verify', token })
    });
    
    const { valid, user } = await authResponse.json();
    if (!valid) return new Response('Unauthorized', { status: 401 });
    
    // Continue with authenticated user
  }
};
```

### Named Entrypoints (RPC)

```typescript
// auth-worker with named entrypoints
export class AuthHandler extends WorkerEntrypoint {
  async verifyToken(token: string) {
    return { valid: true, user: { id: 1, name: 'Alice' } };
  }
  
  async createSession(userId: number) {
    return { sessionId: crypto.randomUUID() };
  }
}

// main-worker using RPC
export default {
  async fetch(request: Request, env: Env) {
    const result = await env.AUTH_SERVICE.verifyToken('token123');
    // Direct method call, no fetch() needed
  }
};
```

---

## Browser Rendering

Headless browser automation using Puppeteer.

### Configuration

```jsonc
{
  "browser": {
    "binding": "BROWSER"
  }
}
```

### Usage

```typescript
import puppeteer from '@cloudflare/puppeteer';

interface Env {
  BROWSER: BrowserWorker;
}

export default {
  async fetch(request: Request, env: Env) {
    const browser = await puppeteer.launch(env.BROWSER);
    const page = await browser.newPage();
    
    await page.goto('https://example.com');
    await page.waitForSelector('h1');
    
    const screenshot = await page.screenshot({ type: 'png' });
    const title = await page.title();
    const content = await page.$eval('h1', el => el.textContent);
    
    await browser.close();
    
    return new Response(screenshot, {
      headers: { 'Content-Type': 'image/png' }
    });
  }
};
```

---

## Analytics Engine

High-cardinality time-series analytics.

### Configuration

```jsonc
{
  "analytics_engine_datasets": [
    {
      "binding": "ANALYTICS",
      "dataset": "my-analytics"
    }
  ]
}
```

### Usage

```typescript
interface Env {
  ANALYTICS: AnalyticsEngineDataset;
}

export default {
  async fetch(request: Request, env: Env) {
    // Write data point
    env.ANALYTICS.writeDataPoint({
      blobs: ['user-agent', request.headers.get('User-Agent') || ''],
      doubles: [1],  // Count
      indexes: [request.cf?.country || 'unknown']
    });
    
    return new Response('OK');
  }
};

// Query via GraphQL API (external)
```

---

## Rate Limiting

Built-in rate limiting binding.

### Configuration

```jsonc
{
  "unsafe": {
    "bindings": [
      {
        "name": "RATE_LIMITER",
        "type": "ratelimit",
        "namespace_id": "1234",
        "simple": {
          "limit": 100,
          "period": 60
        }
      }
    ]
  }
}
```

### Usage

```typescript
interface Env {
  RATE_LIMITER: RateLimit;
}

export default {
  async fetch(request: Request, env: Env) {
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const { success } = await env.RATE_LIMITER.limit({ key: ip });
    
    if (!success) {
      return new Response('Rate limited', { status: 429 });
    }
    
    return new Response('OK');
  }
};
```

---

## mTLS Certificates

Mutual TLS for secure service-to-service communication.

### Configuration

```jsonc
{
  "mtls_certificates": [
    {
      "binding": "CLIENT_CERT",
      "certificate_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  ]
}
```

### Usage

```typescript
interface Env {
  CLIENT_CERT: Fetcher;
}

export default {
  async fetch(request: Request, env: Env) {
    // Requests through this fetcher include the mTLS certificate
    const response = await env.CLIENT_CERT.fetch('https://secure-api.example.com/data');
    return response;
  }
};
```

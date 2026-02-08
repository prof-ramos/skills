# Cloudflare Workers Runtime APIs Reference

Complete reference for Workers runtime APIs, handlers, and web standard implementations.

## Table of Contents

1. [Handlers](#handlers)
2. [Request Object](#request-object)
3. [Response Object](#response-object)
4. [Fetch API](#fetch-api)
5. [Cache API](#cache-api)
6. [HTMLRewriter](#htmlrewriter)
7. [WebSockets](#websockets)
8. [Streams](#streams)
9. [Web Crypto](#web-crypto)
10. [Encoding](#encoding)
11. [Performance & Timers](#performance--timers)
12. [Node.js Compatibility](#nodejs-compatibility)

---

## Handlers

### Fetch Handler (HTTP Requests)

```typescript
export default {
  async fetch(
    request: Request,      // Incoming HTTP request
    env: Env,              // Bindings (KV, R2, etc.)
    ctx: ExecutionContext  // Context for background tasks
  ): Promise<Response> {
    return new Response('Hello World');
  }
};

// ExecutionContext methods
interface ExecutionContext {
  waitUntil(promise: Promise<unknown>): void;  // Run after response
  passThroughOnException(): void;              // Pass to origin on error
}
```

### Scheduled Handler (Cron Triggers)

```typescript
export default {
  async scheduled(
    event: ScheduledEvent,
    env: Env,
    ctx: ExecutionContext
  ) {
    // event.cron = "0 * * * *"
    // event.scheduledTime = timestamp
    ctx.waitUntil(performTask(env));
  }
};
```

### Queue Handler (Message Processing)

```typescript
export default {
  async queue(
    batch: MessageBatch<T>,
    env: Env,
    ctx: ExecutionContext
  ) {
    for (const message of batch.messages) {
      // message.body, message.id, message.timestamp
      message.ack();  // or message.retry()
    }
  }
};
```

### Tail Handler (Log Processing)

```typescript
export default {
  async tail(events: TailEvent[]) {
    for (const event of events) {
      // event.logs, event.exceptions, event.outcome
      await sendToLogService(event);
    }
  }
};
```

### Email Handler

```typescript
export default {
  async email(
    message: EmailMessage,
    env: Env,
    ctx: ExecutionContext
  ) {
    const { from, to, subject, raw } = message;
    // Forward, process, or store email
    await message.forward('admin@example.com');
  }
};
```

---

## Request Object

### Properties

```typescript
interface Request {
  // Standard properties
  method: string;                    // "GET", "POST", etc.
  url: string;                       // Full URL
  headers: Headers;                  // Request headers
  body: ReadableStream | null;       // Request body
  bodyUsed: boolean;
  
  // Cloudflare-specific
  cf?: IncomingRequestCfProperties;  // Cloudflare properties
}

interface IncomingRequestCfProperties {
  // Geolocation
  country?: string;          // "US"
  city?: string;             // "San Francisco"
  continent?: string;        // "NA"
  latitude?: string;
  longitude?: string;
  postalCode?: string;
  region?: string;           // "California"
  regionCode?: string;       // "CA"
  timezone?: string;         // "America/Los_Angeles"
  
  // Network
  asn?: number;              // 13335
  asOrganization?: string;   // "CLOUDFLARENET"
  colo?: string;             // "SFO"
  
  // Security
  tlsVersion?: string;       // "TLSv1.3"
  tlsCipher?: string;
  tlsClientAuth?: {
    certPresented: '0' | '1';
    certVerified: 'SUCCESS' | 'FAILED';
    certRevoked?: '0' | '1';
    certIssuerDN?: string;
    certSubjectDN?: string;
    certNotBefore?: string;
    certNotAfter?: string;
    certSerial?: string;
    certFingerprintSHA1?: string;
    certFingerprintSHA256?: string;
  };
  
  // Bot detection
  botManagement?: {
    score: number;           // 0-99 (lower = more likely bot)
    verifiedBot: boolean;
    staticResource: boolean;
    ja3Hash?: string;
  };
  
  // Request properties
  httpProtocol?: string;     // "HTTP/2"
  requestPriority?: string;
}
```

### Body Methods

```typescript
const request = new Request('https://example.com', {
  method: 'POST',
  body: JSON.stringify({ name: 'Alice' })
});

// Read body (can only be read once)
const json = await request.json();
const text = await request.text();
const formData = await request.formData();
const arrayBuffer = await request.arrayBuffer();
const blob = await request.blob();

// Clone to read multiple times
const clone = request.clone();
```

### Creating Requests

```typescript
// Basic request
const request = new Request('https://api.example.com/data');

// With options
const request = new Request('https://api.example.com/data', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token123'
  },
  body: JSON.stringify({ key: 'value' }),
  redirect: 'follow',  // 'follow' | 'error' | 'manual'
  
  // Cloudflare-specific options
  cf: {
    cacheTtl: 300,
    cacheEverything: true,
    scrapeShield: false,
    apps: false,
    image: { fit: 'cover', width: 100, height: 100 },
    resolveOverride: 'origin.example.com'
  }
});
```

---

## Response Object

### Creating Responses

```typescript
// Basic responses
new Response('Hello World');
new Response(null, { status: 204 });

// JSON response
Response.json({ success: true });
Response.json({ error: 'Not found' }, { status: 404 });

// With headers
new Response(body, {
  status: 200,
  statusText: 'OK',
  headers: {
    'Content-Type': 'application/json',
    'Cache-Control': 'max-age=3600',
    'X-Custom-Header': 'value'
  }
});

// Redirect
Response.redirect('https://example.com', 301);

// Stream response
new Response(readableStream, {
  headers: { 'Content-Type': 'application/octet-stream' }
});
```

### Properties

```typescript
interface Response {
  ok: boolean;              // status 200-299
  status: number;           // HTTP status code
  statusText: string;
  headers: Headers;
  body: ReadableStream | null;
  bodyUsed: boolean;
  url: string;
  redirected: boolean;
  type: ResponseType;       // 'basic' | 'cors' | 'error' | 'opaque'
  
  // Cloudflare-specific
  webSocket?: WebSocket;    // For WebSocket upgrade responses
  cf?: { cacheStatus?: string };
}
```

### Body Methods

```typescript
const response = await fetch('https://api.example.com');

const json = await response.json();
const text = await response.text();
const arrayBuffer = await response.arrayBuffer();
const blob = await response.blob();
const formData = await response.formData();

// Clone to read multiple times
const clone = response.clone();
```

---

## Fetch API

### Basic Usage

```typescript
// GET request
const response = await fetch('https://api.example.com/data');
const data = await response.json();

// POST request
const response = await fetch('https://api.example.com/data', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Alice' })
});

// With timeout (using AbortController)
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch(url, { signal: controller.signal });
  clearTimeout(timeoutId);
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Request timed out');
  }
}
```

### Cloudflare-specific Options

```typescript
const response = await fetch('https://example.com/image.jpg', {
  cf: {
    // Caching
    cacheTtl: 300,                    // Cache TTL in seconds
    cacheEverything: true,            // Cache all content types
    cacheKey: 'custom-cache-key',     // Custom cache key
    cacheTtlByStatus: {
      '200-299': 86400,
      '404': 1,
      '500-599': 0
    },
    
    // Image optimization
    image: {
      fit: 'cover',                   // 'scale-down' | 'contain' | 'cover' | 'crop' | 'pad'
      width: 800,
      height: 600,
      quality: 80,
      format: 'webp'                  // 'webp' | 'avif' | 'json'
    },
    
    // Polish (image optimization)
    polish: 'lossy',                  // 'lossless' | 'lossy' | 'off'
    
    // Mirage (image lazy loading)
    mirage: true,
    
    // Security features
    scrapeShield: false,              // Disable email obfuscation
    apps: false,                      // Disable Cloudflare apps
    minify: { javascript: true, css: true, html: true },
    
    // Origin resolution
    resolveOverride: 'custom-origin.example.com'
  }
});
```

### Subrequest Limits

- Free plan: 50 subrequests per request
- Paid plan: 1,000 subrequests per request
- Recursive Worker calls count against limits

---

## Cache API

### Default Cache

```typescript
const cache = caches.default;

// Match request in cache
const response = await cache.match(request);

// Store in cache
await cache.put(request, response);

// Delete from cache
await cache.delete(request);
```

### Custom Cache Keys

```typescript
async function handleRequest(request: Request, ctx: ExecutionContext) {
  const url = new URL(request.url);
  
  // Create custom cache key (ignore query params)
  const cacheKey = new Request(url.origin + url.pathname, request);
  
  const cache = caches.default;
  let response = await cache.match(cacheKey);
  
  if (!response) {
    response = await fetch(request);
    response = new Response(response.body, response);
    response.headers.set('Cache-Control', 'public, max-age=3600');
    
    // Store in cache (non-blocking)
    ctx.waitUntil(cache.put(cacheKey, response.clone()));
  }
  
  return response;
}
```

### Named Caches

```typescript
// Open named cache (isolated namespace)
const myCache = await caches.open('my-cache');

await myCache.put(key, response);
const cached = await myCache.match(key);
await myCache.delete(key);
```

### Cache API with POST Requests

```typescript
async function cachePostRequest(request: Request, ctx: ExecutionContext) {
  const body = await request.clone().text();
  const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(body));
  const hashHex = [...new Uint8Array(hash)].map(b => b.toString(16).padStart(2, '0')).join('');
  
  const cacheKey = new Request(`${request.url}?hash=${hashHex}`, {
    method: 'GET',
    headers: request.headers
  });
  
  const cache = caches.default;
  let response = await cache.match(cacheKey);
  
  if (!response) {
    response = await fetch(request);
    ctx.waitUntil(cache.put(cacheKey, response.clone()));
  }
  
  return response;
}
```

---

## HTMLRewriter

Streaming HTML parser and transformer for modifying HTML on the fly.

### Element Handlers

```typescript
class ElementHandler {
  element(element: Element) {
    // Modify element
    element.setInnerContent('New content');
    element.setAttribute('class', 'modified');
    element.removeAttribute('onclick');
    element.prepend('<span>Before</span>', { html: true });
    element.append('<span>After</span>', { html: true });
    element.remove();
    element.removeAndKeepContent();
    
    // Read element
    const tag = element.tagName;
    const attr = element.getAttribute('href');
    const hasAttr = element.hasAttribute('class');
  }
  
  comments(comment: Comment) {
    comment.text;  // Comment content
    comment.remove();
  }
  
  text(text: Text) {
    text.text;      // Text content
    text.lastInTextNode;  // Is last chunk
    text.remove();
    text.replace('new text');
  }
}
```

### Document Handlers

```typescript
class DocumentHandler {
  doctype(doctype: Doctype) {
    // doctype.name, doctype.publicId, doctype.systemId
  }
  
  comments(comment: Comment) {
    // Top-level comments
  }
  
  text(text: Text) {
    // Text outside elements
  }
  
  end(end: DocumentEnd) {
    end.append('<script>console.log("loaded")</script>', { html: true });
  }
}
```

### Usage Example

```typescript
async function transformHTML(request: Request) {
  const response = await fetch(request);
  
  return new HTMLRewriter()
    // Transform specific elements
    .on('title', {
      element(el) { el.setInnerContent('Modified Title'); }
    })
    
    // Transform by CSS selector
    .on('a[href^="/"]', {
      element(el) {
        const href = el.getAttribute('href');
        el.setAttribute('href', `https://example.com${href}`);
      }
    })
    
    // Remove elements
    .on('script[src*="analytics"]', {
      element(el) { el.remove(); }
    })
    
    // Modify text content
    .on('p.description', {
      text(text) {
        if (text.text.includes('OLD')) {
          text.replace(text.text.replace('OLD', 'NEW'));
        }
      }
    })
    
    // Add content to document
    .onDocument({
      end(end) {
        end.append('<!-- Modified by Workers -->', { html: true });
      }
    })
    
    .transform(response);
}
```

---

## WebSockets

### Server (Worker as WebSocket endpoint)

```typescript
export default {
  async fetch(request: Request) {
    const upgradeHeader = request.headers.get('Upgrade');
    
    if (upgradeHeader !== 'websocket') {
      return new Response('Expected WebSocket', { status: 426 });
    }
    
    const [client, server] = Object.values(new WebSocketPair());
    
    server.accept();
    
    server.addEventListener('message', (event) => {
      console.log('Received:', event.data);
      server.send(`Echo: ${event.data}`);
    });
    
    server.addEventListener('close', (event) => {
      console.log('Closed:', event.code, event.reason);
    });
    
    server.addEventListener('error', (event) => {
      console.error('Error:', event);
    });
    
    return new Response(null, {
      status: 101,
      webSocket: client
    });
  }
};
```

### Client (Worker connecting to external WebSocket)

```typescript
async function connectWebSocket() {
  const response = await fetch('wss://echo.websocket.org', {
    headers: { 'Upgrade': 'websocket' }
  });
  
  const webSocket = response.webSocket;
  if (!webSocket) {
    throw new Error('WebSocket upgrade failed');
  }
  
  webSocket.accept();
  
  webSocket.addEventListener('message', (event) => {
    console.log('Received:', event.data);
  });
  
  webSocket.send('Hello, WebSocket!');
  
  // Close after some time
  setTimeout(() => webSocket.close(1000, 'Done'), 5000);
}
```

---

## Streams

### ReadableStream

```typescript
// Create readable stream
const stream = new ReadableStream({
  start(controller) {
    controller.enqueue('Hello ');
    controller.enqueue('World');
    controller.close();
  }
});

// From array
const stream = new ReadableStream({
  start(controller) {
    ['a', 'b', 'c'].forEach(chunk => controller.enqueue(chunk));
    controller.close();
  }
});

// Read stream
const reader = stream.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(value);
}
```

### TransformStream

```typescript
// Text encoder stream
const { readable, writable } = new TransformStream({
  transform(chunk, controller) {
    controller.enqueue(chunk.toUpperCase());
  }
});

// Pipe through transform
const response = await fetch('https://example.com');
const upperCased = response.body.pipeThrough(new TransformStream({
  transform(chunk, controller) {
    const text = new TextDecoder().decode(chunk);
    controller.enqueue(new TextEncoder().encode(text.toUpperCase()));
  }
}));
```

### WritableStream

```typescript
const chunks: Uint8Array[] = [];

const writable = new WritableStream({
  write(chunk) {
    chunks.push(chunk);
  },
  close() {
    console.log('Stream closed, total chunks:', chunks.length);
  }
});

const writer = writable.getWriter();
await writer.write(new TextEncoder().encode('Hello'));
await writer.close();
```

### Streaming Response

```typescript
function streamingResponse() {
  const { readable, writable } = new TransformStream();
  const writer = writable.getWriter();
  
  // Write chunks asynchronously
  (async () => {
    for (let i = 0; i < 10; i++) {
      await writer.write(new TextEncoder().encode(`Chunk ${i}\n`));
      await new Promise(r => setTimeout(r, 100));
    }
    await writer.close();
  })();
  
  return new Response(readable, {
    headers: { 'Content-Type': 'text/plain' }
  });
}
```

---

## Web Crypto

### Random Values

```typescript
// Random bytes
const bytes = new Uint8Array(16);
crypto.getRandomValues(bytes);

// UUID
const uuid = crypto.randomUUID();
```

### Hashing

```typescript
async function hash(data: string, algorithm = 'SHA-256') {
  const encoder = new TextEncoder();
  const hashBuffer = await crypto.subtle.digest(algorithm, encoder.encode(data));
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Usage
const sha256 = await hash('Hello World');           // SHA-256 (default)
const sha1 = await hash('Hello World', 'SHA-1');    // SHA-1
const md5 = await hash('Hello World', 'MD5');       // MD5
```

### HMAC

```typescript
async function hmacSign(key: string, data: string) {
  const encoder = new TextEncoder();
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    encoder.encode(key),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  
  const signature = await crypto.subtle.sign('HMAC', cryptoKey, encoder.encode(data));
  return btoa(String.fromCharCode(...new Uint8Array(signature)));
}

async function hmacVerify(key: string, data: string, signature: string) {
  const encoder = new TextEncoder();
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    encoder.encode(key),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['verify']
  );
  
  const sigBytes = Uint8Array.from(atob(signature), c => c.charCodeAt(0));
  return crypto.subtle.verify('HMAC', cryptoKey, sigBytes, encoder.encode(data));
}
```

### AES Encryption

```typescript
async function aesEncrypt(plaintext: string, key: string) {
  const encoder = new TextEncoder();
  const iv = crypto.getRandomValues(new Uint8Array(12));
  
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    await crypto.subtle.digest('SHA-256', encoder.encode(key)),
    'AES-GCM',
    false,
    ['encrypt']
  );
  
  const ciphertext = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    cryptoKey,
    encoder.encode(plaintext)
  );
  
  // Return IV + ciphertext as base64
  const combined = new Uint8Array(iv.length + ciphertext.byteLength);
  combined.set(iv);
  combined.set(new Uint8Array(ciphertext), iv.length);
  return btoa(String.fromCharCode(...combined));
}

async function aesDecrypt(encrypted: string, key: string) {
  const encoder = new TextEncoder();
  const combined = Uint8Array.from(atob(encrypted), c => c.charCodeAt(0));
  
  const iv = combined.slice(0, 12);
  const ciphertext = combined.slice(12);
  
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    await crypto.subtle.digest('SHA-256', encoder.encode(key)),
    'AES-GCM',
    false,
    ['decrypt']
  );
  
  const plaintext = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv },
    cryptoKey,
    ciphertext
  );
  
  return new TextDecoder().decode(plaintext);
}
```

### Timing-Safe Comparison

```typescript
function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  
  const encoder = new TextEncoder();
  const aBytes = encoder.encode(a);
  const bBytes = encoder.encode(b);
  
  return crypto.subtle.timingSafeEqual(aBytes, bBytes);
}
```

---

## Encoding

### TextEncoder/TextDecoder

```typescript
// String to bytes
const encoder = new TextEncoder();
const bytes = encoder.encode('Hello World');

// Bytes to string
const decoder = new TextDecoder();
const text = decoder.decode(bytes);

// With encoding
const decoder = new TextDecoder('utf-8', { fatal: true });
```

### Base64

```typescript
// Encode
const base64 = btoa('Hello World');

// Decode
const text = atob(base64);

// Binary-safe base64
function base64Encode(buffer: ArrayBuffer): string {
  return btoa(String.fromCharCode(...new Uint8Array(buffer)));
}

function base64Decode(base64: string): ArrayBuffer {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
}
```

### URL Encoding

```typescript
// Encode/decode component
const encoded = encodeURIComponent('hello world');  // "hello%20world"
const decoded = decodeURIComponent('hello%20world'); // "hello world"

// Encode/decode full URL
const url = encodeURI('https://example.com/path with spaces');
const original = decodeURI(url);

// URLSearchParams
const params = new URLSearchParams({ name: 'Alice', age: '30' });
params.toString();  // "name=Alice&age=30"
params.get('name'); // "Alice"
params.append('city', 'NYC');
```

---

## Performance & Timers

### Timing

```typescript
// High-resolution time
const start = performance.now();
await doWork();
const duration = performance.now() - start;

// Date (wall clock)
const timestamp = Date.now();
const date = new Date();
```

### Timers

```typescript
// setTimeout/setInterval (limited in Workers)
const timeoutId = setTimeout(() => {
  console.log('Executed after delay');
}, 1000);

clearTimeout(timeoutId);

// Note: Timers don't keep the Worker alive
// Use ctx.waitUntil() for background tasks
```

### Scheduler API

```typescript
// scheduler.wait() - async sleep
await scheduler.wait(1000);  // Wait 1 second

// In loops
for (let i = 0; i < 10; i++) {
  await doWork();
  await scheduler.wait(100);  // Rate limiting
}
```

---

## Node.js Compatibility

Workers support a subset of Node.js APIs. Enable with compatibility flags.

### Configuration

```jsonc
{
  "compatibility_flags": ["nodejs_compat"]
}
```

### Supported Modules

```typescript
// Buffer
import { Buffer } from 'node:buffer';
const buf = Buffer.from('Hello');
const base64 = buf.toString('base64');

// Crypto
import { createHash, createHmac, randomBytes } from 'node:crypto';
const hash = createHash('sha256').update('data').digest('hex');

// Util
import { promisify } from 'node:util';

// Path
import { join, dirname, basename } from 'node:path';

// Stream
import { Readable, Writable, Transform } from 'node:stream';

// Assert
import assert from 'node:assert';

// Process (limited)
import { env } from 'node:process';
```

### AsyncLocalStorage

```typescript
import { AsyncLocalStorage } from 'node:async_hooks';

const requestContext = new AsyncLocalStorage<{ requestId: string }>();

export default {
  async fetch(request: Request, env: Env) {
    const requestId = crypto.randomUUID();
    
    return requestContext.run({ requestId }, async () => {
      // Access context anywhere in call stack
      const ctx = requestContext.getStore();
      console.log('Request ID:', ctx?.requestId);
      
      return new Response('OK');
    });
  }
};
```

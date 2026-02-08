#!/bin/bash
#
# Cloudflare Workers Project Scaffolding Script
# Usage: ./scaffold-worker.sh <project-name> [template]
#
# Templates: api, spa, fullstack, hono
#

set -e

PROJECT_NAME="${1:-my-worker}"
TEMPLATE="${2:-api}"

echo "🚀 Creating Cloudflare Workers project: $PROJECT_NAME"
echo "   Template: $TEMPLATE"
echo ""

# Create project directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Initialize package.json
cat > package.json << 'EOF'
{
  "name": "PROJECT_NAME",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "test": "vitest run",
    "test:watch": "vitest",
    "types": "wrangler types"
  },
  "devDependencies": {
    "@cloudflare/vitest-pool-workers": "^0.5.0",
    "@cloudflare/workers-types": "^4.0.0",
    "typescript": "^5.0.0",
    "vitest": "^2.0.0",
    "wrangler": "^3.0.0"
  }
}
EOF
sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" package.json

# Create wrangler.jsonc
cat > wrangler.jsonc << 'EOF'
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "PROJECT_NAME",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  
  // Uncomment and configure bindings as needed:
  
  // "kv_namespaces": [
  //   { "binding": "KV", "id": "your-kv-namespace-id" }
  // ],
  
  // "d1_databases": [
  //   { "binding": "DB", "database_id": "your-database-id", "database_name": "your-db-name" }
  // ],
  
  // "r2_buckets": [
  //   { "binding": "STORAGE", "bucket_name": "your-bucket-name" }
  // ],
  
  // "ai": { "binding": "AI" },
  
  // "vars": {
  //   "ENVIRONMENT": "development"
  // }
}
EOF
sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" wrangler.jsonc

# Create tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "lib": ["ES2022"],
    "types": ["@cloudflare/workers-types/2023-07-01", "@cloudflare/vitest-pool-workers"],
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true,
    "isolatedModules": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*", "test/**/*"],
  "exclude": ["node_modules"]
}
EOF

# Create vitest.config.ts
cat > vitest.config.ts << 'EOF'
import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config';

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.jsonc' }
      }
    }
  }
});
EOF

# Create source directory
mkdir -p src

# Template: API
if [ "$TEMPLATE" = "api" ]; then
cat > src/index.ts << 'EOF'
export interface Env {
  // Add your bindings here
  // KV: KVNamespace;
  // DB: D1Database;
  // STORAGE: R2Bucket;
  // AI: Ai;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // Health check
    if (url.pathname === '/health') {
      return Response.json({ status: 'ok', timestamp: new Date().toISOString() });
    }
    
    // API routes
    if (url.pathname === '/api/hello') {
      return Response.json({ message: 'Hello from Cloudflare Workers!' });
    }
    
    if (url.pathname === '/api/echo' && request.method === 'POST') {
      const body = await request.json();
      return Response.json({ echo: body });
    }
    
    // 404 for unknown routes
    return Response.json({ error: 'Not found' }, { status: 404 });
  }
};
EOF
fi

# Template: SPA
if [ "$TEMPLATE" = "spa" ]; then
# Update wrangler.jsonc for SPA
cat > wrangler.jsonc << 'EOF'
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "PROJECT_NAME",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "assets": {
    "directory": "./dist",
    "binding": "ASSETS",
    "not_found_handling": "single-page-application"
  }
}
EOF
sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" wrangler.jsonc

cat > src/index.ts << 'EOF'
export interface Env {
  ASSETS: Fetcher;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // API routes handled by Worker
    if (url.pathname.startsWith('/api/')) {
      return handleApi(request, env);
    }
    
    // Serve static assets (SPA)
    return env.ASSETS.fetch(request);
  }
};

async function handleApi(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  
  if (url.pathname === '/api/hello') {
    return Response.json({ message: 'Hello from API!' });
  }
  
  return Response.json({ error: 'Not found' }, { status: 404 });
}
EOF

mkdir -p dist
cat > dist/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My SPA</title>
</head>
<body>
  <h1>Hello from SPA!</h1>
  <script>
    fetch('/api/hello')
      .then(r => r.json())
      .then(data => console.log(data));
  </script>
</body>
</html>
EOF
fi

# Template: Full-stack
if [ "$TEMPLATE" = "fullstack" ]; then
# Update wrangler.jsonc
cat > wrangler.jsonc << 'EOF'
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "PROJECT_NAME",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "assets": {
    "directory": "./dist",
    "binding": "ASSETS",
    "not_found_handling": "single-page-application",
    "run_worker_first": ["/api/*"]
  },
  "d1_databases": [
    { "binding": "DB", "database_id": "YOUR_DATABASE_ID", "database_name": "mydb" }
  ]
}
EOF
sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" wrangler.jsonc

cat > src/index.ts << 'EOF'
export interface Env {
  ASSETS: Fetcher;
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // API routes
    if (url.pathname.startsWith('/api/')) {
      return handleApi(request, env);
    }
    
    // Serve static assets
    return env.ASSETS.fetch(request);
  }
};

async function handleApi(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  
  try {
    // GET /api/items - List items
    if (url.pathname === '/api/items' && request.method === 'GET') {
      const result = await env.DB.prepare('SELECT * FROM items').all();
      return Response.json(result.results);
    }
    
    // POST /api/items - Create item
    if (url.pathname === '/api/items' && request.method === 'POST') {
      const body = await request.json() as { name: string };
      const id = crypto.randomUUID();
      await env.DB.prepare('INSERT INTO items (id, name) VALUES (?, ?)')
        .bind(id, body.name)
        .run();
      return Response.json({ id, name: body.name }, { status: 201 });
    }
    
    // GET /api/items/:id - Get item
    const itemMatch = url.pathname.match(/^\/api\/items\/([^/]+)$/);
    if (itemMatch && request.method === 'GET') {
      const item = await env.DB.prepare('SELECT * FROM items WHERE id = ?')
        .bind(itemMatch[1])
        .first();
      if (!item) return Response.json({ error: 'Not found' }, { status: 404 });
      return Response.json(item);
    }
    
    // DELETE /api/items/:id - Delete item
    if (itemMatch && request.method === 'DELETE') {
      await env.DB.prepare('DELETE FROM items WHERE id = ?')
        .bind(itemMatch[1])
        .run();
      return new Response(null, { status: 204 });
    }
    
    return Response.json({ error: 'Not found' }, { status: 404 });
  } catch (error) {
    console.error('API Error:', error);
    return Response.json({ error: 'Internal server error' }, { status: 500 });
  }
}
EOF

mkdir -p dist
cat > dist/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Full-Stack App</title>
</head>
<body>
  <h1>Items</h1>
  <ul id="items"></ul>
  <input type="text" id="newItem" placeholder="New item name">
  <button onclick="addItem()">Add</button>
  
  <script>
    async function loadItems() {
      const response = await fetch('/api/items');
      const items = await response.json();
      const ul = document.getElementById('items');
      ul.innerHTML = items.map(item => `<li>${item.name}</li>`).join('');
    }
    
    async function addItem() {
      const input = document.getElementById('newItem');
      await fetch('/api/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: input.value })
      });
      input.value = '';
      loadItems();
    }
    
    loadItems();
  </script>
</body>
</html>
EOF

# Create schema file
cat > schema.sql << 'EOF'
CREATE TABLE IF NOT EXISTS items (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now'))
);
EOF
fi

# Template: Hono
if [ "$TEMPLATE" = "hono" ]; then
cat >> package.json << 'EOF'
EOF
# Add hono dependency (simplified - would need proper JSON manipulation)

cat > src/index.ts << 'EOF'
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';

type Bindings = {
  // Add your bindings here
  // DB: D1Database;
  // KV: KVNamespace;
};

const app = new Hono<{ Bindings: Bindings }>();

// Middleware
app.use('*', logger());
app.use('/api/*', cors());

// Routes
app.get('/', (c) => c.text('Hello Hono!'));

app.get('/api/hello', (c) => c.json({ message: 'Hello from Hono!' }));

app.post('/api/echo', async (c) => {
  const body = await c.req.json();
  return c.json({ echo: body });
});

// 404 handler
app.notFound((c) => c.json({ error: 'Not found' }, 404));

// Error handler
app.onError((err, c) => {
  console.error('Error:', err);
  return c.json({ error: 'Internal server error' }, 500);
});

export default app;
EOF

# Update package.json to include hono
node -e "
const pkg = require('./package.json');
pkg.dependencies = pkg.dependencies || {};
pkg.dependencies.hono = '^4.0.0';
require('fs').writeFileSync('package.json', JSON.stringify(pkg, null, 2));
"
fi

# Create test directory and sample test
mkdir -p test

cat > test/index.test.ts << 'EOF'
import { env, createExecutionContext, waitOnExecutionContext } from 'cloudflare:test';
import { describe, it, expect } from 'vitest';
import worker from '../src/index';

describe('Worker', () => {
  it('responds to health check', async () => {
    const request = new Request('http://localhost/health');
    const ctx = createExecutionContext();
    const response = await worker.fetch(request, env, ctx);
    await waitOnExecutionContext(ctx);
    
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data).toHaveProperty('status', 'ok');
  });
  
  it('responds to /api/hello', async () => {
    const request = new Request('http://localhost/api/hello');
    const ctx = createExecutionContext();
    const response = await worker.fetch(request, env, ctx);
    await waitOnExecutionContext(ctx);
    
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data).toHaveProperty('message');
  });
  
  it('returns 404 for unknown routes', async () => {
    const request = new Request('http://localhost/unknown');
    const ctx = createExecutionContext();
    const response = await worker.fetch(request, env, ctx);
    await waitOnExecutionContext(ctx);
    
    expect(response.status).toBe(404);
  });
});
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
node_modules/
.wrangler/
.dev.vars
dist/
*.log
EOF

# Create README
cat > README.md << EOF
# $PROJECT_NAME

Cloudflare Workers project created with template: $TEMPLATE

## Development

\`\`\`bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Deploy
npm run deploy
\`\`\`

## Configuration

Edit \`wrangler.jsonc\` to configure bindings (KV, D1, R2, etc.)

## Resources

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
EOF

echo ""
echo "✅ Project created successfully!"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  npm install"
echo "  npm run dev"
echo ""

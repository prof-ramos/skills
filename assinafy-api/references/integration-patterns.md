# Padrões de Integração Assinafy

Referência baseada em `prof-ramos/intranet` (`src/lib/assinafy/`).

## Estrutura de módulos recomendada

```
lib/assinafy/
├── client.ts       # HTTP client — upload, signers, assignments
├── types.ts        # Enums de status, tipos de webhook
├── service.ts      # Lógica de negócio — mapeamento de eventos
├── repository.ts   # Persistência local (document ID ↔ entidade do app)
└── client.test.ts  # Testes unitários do client
```

## Client HTTP

Princípios do `AssinafyClient`:

- Constructor recebe `{ apiKey, accountId?, baseUrl? }`
- Default base URL: `https://sandbox.assinafy.com.br/v1`
- Timeout de 30s com `AbortController`
- Header fixo: `X-Api-Key`
- Parse JSON obrigatório; lançar erro tipado se `status >= 400` no body ou HTTP

```typescript
export class AssinafyError extends Error {
  constructor(
    message: string,
    public readonly statusCode?: number,
    public readonly responseBody?: string,
  ) {
    super(message);
    this.name = 'AssinafyError';
  }
}

// Upload — multipart/form-data, campo "file"
async uploadDocument(pdf: Buffer, filename: string) {
  const form = new FormData();
  form.set('file', new Blob([pdf], { type: 'application/pdf' }), filename);
  return this.request(`/accounts/${this.accountId}/documents`, {
    method: 'POST',
    body: form,
  });
}

// Signer — JSON body
async createSigner(fullName: string, email: string) {
  const resp = await this.request(`/accounts/${this.accountId}/signers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ full_name: fullName, email }),
  });
  return resp.data; // { id, full_name, email }
}

// Assignment — method "virtual" ou "collect"
async createAssignment(documentId: string, options: AssignmentOptions) {
  return this.request(`/documents/${documentId}/assignments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(options),
  });
}
```

## Tipos de webhook

```typescript
export interface AssinafyWebhookEvent {
  id: number;
  event: string;
  message: string | null;
  payload: Record<string, unknown>;
  origin: { ip: string; 'user-agent': string };
  created_at: number;
  subject: { id: string; full_name: string; email: string; type: string };
  object: { id: string; status: string; type: string };
  account_id: string;
}
```

## Service — mapeamento de eventos

```typescript
const EVENT_STATUS_MAP: Record<string, string> = {
  signer_signed_document: 'partially_signed',
  document_ready: 'certificated',
  signer_rejected_document: 'rejected_by_signer',
  user_rejected_document: 'rejected_by_user',
  document_processing_failed: 'failed',
};

export async function handleWebhookEvent(event: AssinafyWebhookEvent) {
  const mappedStatus = EVENT_STATUS_MAP[event.event];
  if (!mappedStatus) return null; // evento desconhecido — ignorar

  const entity = await findByAssinafyDocumentId(event.object.id);
  if (!entity) return null;

  // Atualizar status local + campos adicionais conforme evento
  return updateStatus(entity.id, mappedStatus, buildAdditionalFields(event));
}
```

## Route handler (Next.js / API)

```typescript
export const POST = createWebhookHandler({
  authenticate: (request) =>
    requireSecretHeader({
      request,
      secret: process.env.ASSINAFY_WEBHOOK_SECRET,
      headerName: 'X-Webhook-Secret',
    }),
  parse: parseJsonWebhook,
  handle: async (event) => {
    if (!event.event || !event.object?.id) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }
    try {
      await handleWebhookEvent(event);
    } catch (error) {
      // Logar mas ainda retornar 200 para evitar retries desnecessários
    }
    return NextResponse.json({ received: true });
  },
});
```

## Persistência local

Salve o `document.id` retornado pelo upload para correlacionar webhooks:

```typescript
// No upload bem-sucedido
await saveEntity({
  assinafyDocumentId: response.id,
  assinafyStatus: 'uploaded',
});

// No webhook
const entity = await findByAssinafyDocumentId(event.object.id);
```

## Checklist de implementação

- [ ] Variáveis de ambiente configuradas e validadas na inicialização
- [ ] Client com timeout e tratamento de erro tipado
- [ ] Upload via multipart (não base64 em JSON)
- [ ] IDs do Assinafy persistidos localmente
- [ ] Webhook com validação de secret
- [ ] Handler idempotente (reprocessar mesmo evento não causa duplicata)
- [ ] Logs sem API keys, emails ou signer-access-codes
- [ ] Sandbox testado antes de trocar `ASSINAFY_BASE_URL` para produção
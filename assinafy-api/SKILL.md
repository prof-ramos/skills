---
name: assinafy-api
description: >
  Especialista na API Assinafy para assinatura digital. Use SEMPRE que o usuário mencionar
  Assinafy, assinatura eletrônica/digital, upload de documento para assinar, signers, assignments,
  webhooks de documento, templates, field definitions, API key da Assinafy, sandbox Assinafy,
  ou integração com plataforma de assinatura — mesmo que não cite "API" explicitamente.
  Orienta upload, signers, assignments (virtual/collect), webhooks e autenticação.
  Consulta assinafy/assinafy-api-docs/ antes de buscar na web. Use com /assinafy-api.
---

# Assinafy API

Assinafy é uma plataforma de assinatura digital com API REST.

## Antes de implementar

1. Identifique a tarefa (upload, assignment, webhook, template, etc.)
2. Leia o arquivo de doc local indicado no Decision Tree abaixo
3. Se for código, leia também `references/integration-patterns.md`
4. Confirme o ambiente (sandbox em dev, produção só quando o usuário pedir)

**Fonte primária:** `assinafy/assinafy-api-docs/`. Consulte https://api.assinafy.com.br/v1/docs apenas se a doc local não cobrir o caso.

## Regras importantes

| Regra | Por quê |
|-------|---------|
| Use sandbox (`https://sandbox.assinafy.com.br/v1`) em desenvolvimento | Evita cobranças e afeta documentos reais |
| API Key só no backend | Chave exposta no frontend permite abuso da conta |
| Header `X-Api-Key` (ou Bearer token) | Forma documentada de autenticação server-side |
| Trate `status` no body **e** HTTP status | A API retorna erros em ambos os níveis |
| Upload via multipart, campo `file` | Endpoint de upload não aceita JSON com base64 |
| `virtual` = sem campos; `collect` = com field definitions | Escolha errada quebra o fluxo de assinatura |
| Webhook: validar secret, responder 200, processar idempotente | Retries do provedor reenviam o mesmo evento |

Variáveis de ambiente padrão: `ASSINAFY_API_KEY`, `ASSINAFY_ACCOUNT_ID`, `ASSINAFY_BASE_URL`, `ASSINAFY_WEBHOOK_SECRET`. Detalhes em `references/integration-patterns.md`.

## Decision Tree — qual doc ler

| Tarefa | Arquivo |
|--------|---------|
| Primeira integração | `assinafy/assinafy-api-docs/README.md`, `quick-start.md` |
| Autenticação / API keys | `authentication.md` |
| Documentos (upload, download, status) | `documents.md` + `schemas/document.md` |
| Signatários | `signers.md` + `schemas/signer.md` |
| Solicitar assinatura | `assignments.md` + `schemas/assignment.md` |
| Campos no PDF (collect) | `field-definitions.md` |
| Templates | `templates.md` |
| Tags | `tags.md` |
| Fluxo do signatário | `signer-documents.md` |
| Webhooks | `webhooks.md` + `references/webhook-events.md` |
| Paginação, erros, ambientes | `basics.md` |
| Padrões de código | `references/integration-patterns.md` |

Todos os caminhos são relativos a `assinafy/assinafy-api-docs/` exceto `references/`.

## Fluxo típico

```
Credenciais → Upload PDF → Criar signers → Assignment → Webhooks → Download certificated
```

**Exemplo — assignment virtual:**

```json
{
  "method": "virtual",
  "signerIds": ["<signer_id>"],
  "expires_at": "2026-12-31T23:59:59Z",
  "message": "Por favor, assine o documento."
}
```

Para `collect`, leia `assignments.md` seção "Create with Input" antes de implementar.

## Referências externas

- Coleção Postman: https://www.postman.com/devassinafy/dev-assinafy-s-workspace/collection/tqqxlsd/assinafy-api-collection
- Códigos de erro HTTP: `assinafy/assinafy-api-docs/basics.md`
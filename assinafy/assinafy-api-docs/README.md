# Assinafy API — Documentação Local

> Documentação técnica extraída de [https://api.assinafy.com.br/v1/docs](https://api.assinafy.com.br/v1/docs)

## Visão Geral

A **Assinafy API** é uma API RESTful que permite gerenciar documentos, usuários, workspaces e signatários (signers). A autenticação pode ser feita via **API Key** (recomendado para integrações server-side) ou **Access Token** (JWT obtido via login).

### Características principais

- API REST com verbos HTTP padrão (GET, POST, PUT, DELETE)
- Formato padrão JSON (XML também suportado)
- Respostas padronizadas com `status`, `message` e `data`
- Paginação, busca e ordenação em endpoints de listagem
- Ambientes separados para desenvolvimento (sandbox) e produção

### Formato de resposta

```json
{
  "status": 200,
  "message": "",
  "data": { }
}
```

## Como Começar (Quick Start)

1. **Crie uma conta** no ambiente sandbox: [https://app-sandbox.assinafy.com.br](https://app-sandbox.assinafy.com.br)
2. **Gere uma API Key** em *My Account → API*
3. **Obtenha o Workspace Account ID** em *My Account → Workspaces*
4. **Faça upload de um documento**: `POST /accounts/{account_id}/documents`
5. **Crie signatários**: `POST /accounts/{account_id}/signers`
6. **Solicite assinaturas**: `POST /documents/{document_id}/assignments`

Consulte o guia completo em [quick-start.md](./quick-start.md).

## Ambientes

| Ambiente | API Base URL | App URL |
| --- | --- | --- |
| **Sandbox (Test)** | `https://sandbox.assinafy.com.br/v1` | `https://app-sandbox.assinafy.com.br` |
| **Produção** | `https://api.assinafy.com.br/v1` | `https://app.assinafy.com.br` |

> Durante o desenvolvimento, use sempre o ambiente sandbox. Para compras de plano/créditos no sandbox, use o cartão de teste: `5510 3647 0363 3414`.

## Autenticação

| Método | Header / Parâmetro |
| --- | --- |
| API Key (recomendado) | `X-Api-Key: {api-key}` |
| Bearer Token | `Authorization: Bearer {access-token}` |
| Token na URL | `?access-token={access-token}` |

Detalhes em [authentication.md](./authentication.md).

## Coleção Postman

Explore os endpoints com a coleção pública do Postman:

1. Acesse a [Assinafy Postman Collection](https://www.postman.com/devassinafy/dev-assinafy-s-workspace/collection/tqqxlsd/assinafy-api-collection)
2. Selecione a coleção **Assinafy Collection** no painel esquerdo
3. Clique em **Fork** para copiar a coleção para seu workspace

## Índice da Documentação

### Fundamentos

| Documento | Descrição |
| --- | --- |
| [basics.md](./basics.md) | Conceitos REST, paginação, erros, ambientes |
| [quick-start.md](./quick-start.md) | Guia rápido: upload, signers, assinaturas |
| [authentication.md](./authentication.md) | Login, API keys, reset de senha |

### Recursos

| Documento | Descrição |
| --- | --- |
| [signers.md](./signers.md) | CRUD de signatários, verificação, assinatura |
| [documents.md](./documents.md) | Upload, listagem, download, status |
| [templates.md](./templates.md) | Modelos de documentos reutilizáveis |
| [tags.md](./tags.md) | Tags para organização de documentos |
| [assignments.md](./assignments.md) | Solicitação e gestão de assinaturas |
| [signer-documents.md](./signer-documents.md) | Fluxo do signatário (lado signer) |
| [field-definitions.md](./field-definitions.md) | Campos de formulário em documentos |
| [webhooks.md](./webhooks.md) | Notificações de eventos via webhook |

### Schemas (Objetos)

| Schema | Descrição |
| --- | --- |
| [schemas/signer.md](./schemas/signer.md) | Objeto Signer |
| [schemas/document.md](./schemas/document.md) | Objeto Document |
| [schemas/template.md](./schemas/template.md) | Objeto Template |
| [schemas/tag.md](./schemas/tag.md) | Objeto Tag |
| [schemas/assignment.md](./schemas/assignment.md) | Objeto Assignment |
| [schemas/field-definition.md](./schemas/field-definition.md) | Objeto Field Definition |
| [schemas/webhook.md](./schemas/webhook.md) | Objetos Webhook |

## Códigos de Erro

| Código | Tipo |
| --- | --- |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 415 | Unsupported Media Type |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

## Estrutura de Arquivos

```
assinafy-api-docs/
├── README.md
├── basics.md
├── quick-start.md
├── authentication.md
├── signers.md
├── documents.md
├── assignments.md
├── templates.md
├── tags.md
├── field-definitions.md
├── signer-documents.md
├── webhooks.md
└── schemas/
    ├── signer.md
    ├── document.md
    ├── template.md
    ├── tag.md
    ├── assignment.md
    ├── field-definition.md
    └── webhook.md
```

---

*Documentação gerada em 2026-06-08 a partir da API Reference oficial da Assinafy.*

# Webhook Events — Assinafy

Mapeamento comum para integrações (referência: `prof-ramos/intranet`).

| Evento Assinafy | Status típico local | Campos adicionais |
|-----------------|---------------------|-------------------|
| `signer_signed_document` | `partially_signed` | `assinafySignedAt` |
| `document_ready` | `certificated` | `assinafySignedAt` |
| `signer_rejected_document` | `rejected_by_signer` | `assinafyError` (decline_reason) |
| `user_rejected_document` | `rejected_by_user` | `assinafyError` |
| `document_processing_failed` | `failed` | `assinafyError` (error_message) |

Eventos desconhecidos: logar e ignorar — não falhar o handler.

Payload completo e catálogo de eventos: `assinafy/assinafy-api-docs/webhooks.md`
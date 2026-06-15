# Document Schema

> Schema reutilizável — documentação completa em [`documents.md`](../documents.md)

### Document Objects

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for document-related objects returned by the API.

#### Document Object

Returned by document endpoints such as `GET /documents`, `GET /documents/{document_id}`, `POST /documents`, and `POST /accounts/{account_id}/templates/{template_id}/create-document`.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `document`. |
| `id` | string | Document ID. |
| `account_id` | string | Workspace ID that owns the document. |
| `template_id` | string|null | Template ID used to create the document, when applicable. |
| `name` | string | Document file name. |
| `status` | string | Document status code. |
| `artifacts` | object | Artifact download URLs keyed by artifact name, such as `original` or `certificated`. |
| `is_closed` | boolean | Indicates whether the document is in a closed terminal state. |
| `signing_url` | string | URL that opens the document signing flow. |
| `decline_reason` | string|null | Reason provided when the document was declined, when available. |
| `declined_by` | object|null | Signer object for the signer who declined the document, when available. |
| `tags` | array[object] | Tags attached to the document. Each entry has `id` and `name`. Always present, possibly empty. |
| `created_at` | string | Creation timestamp in ISO 8601 format. |
| `updated_at` | string | Last update timestamp in ISO 8601 format. |
| `assignment` | object|null | Expanded assignment data when included by the endpoint. |
| `pages` | array[object] | Expanded document pages when included by the endpoint. |

The `assignment` field uses the [Assignment Object](#assignment-objects) shape. The `pages` field uses the page shape below.

#### Document Page Object

Returned inside `document.pages`.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Page ID. |
| `number` | integer | Page number, starting at `1`. |
| `height` | integer | Page height in pixels. |
| `width` | integer | Page width in pixels. |
| `download_url` | string | URL to download the rendered page image. |

#### Document Status

A document will be in one of the following status:

| Status | Deletable | Description |
| --- | --- | --- |
| uploading | no | The document upload is in process. |
| uploaded | no | The document has been uploaded. |
| metadata\_processing | no | The initial processing is under way. |
| metadata\_ready | yes | The initial processing has been completed. |
| expired | yes | The signature deadline has been reached. |
| certificating | no | The document has been signed and is being certificated. |
| certificated | no | The document is certificated. |
| rejected\_by\_signer | yes | A signer declined signing the document. |
| pending\_signature | yes | The document is waiting for signatures. |
| rejected\_by\_user | yes | The signature process was cancelled by a user. |
| failed | yes | The document processing has failed. |
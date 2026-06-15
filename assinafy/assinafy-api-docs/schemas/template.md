# Template Schema

> Schema reutilizável — documentação completa em [`templates.md`](../templates.md)

### Template Objects

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for template-related objects returned by the API.

#### Template Object

Returned by endpoints such as `GET /accounts/{account_id}/templates`, `GET /accounts/{account_id}/templates/{template_id}`, `POST /accounts/{account_id}/templates`, and `PUT /accounts/{account_id}/templates/{template_id}`.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `template`. |
| `id` | string | Template ID. |
| `name` | string | Template file name. |
| `document_name` | string|null | Default document name used when creating documents from this template. |
| `message` | string|null | Default invitation message configured on the template. |
| `status` | string | Template status code. |
| `pages` | array[object] | Template pages. |
| `roles` | array[object] | Template roles. |
| `tags` | array[object] | Tags attached to the template (own tags). Each entry has `id` and `name`. Always present, possibly empty. |
| `default_document_tags` | array[object] | Tags automatically applied to every document created from this template. Each entry has `id` and `name`. Returned only by the single-template endpoint (`GET /accounts/{account_id}/templates/{template_id}`); omitted from the list endpoint to keep responses compact. |
| `created_at` | string | Creation timestamp in ISO 8601 format. |
| `updated_at` | string | Last update timestamp in ISO 8601 format. |

#### Template Page Object

Returned inside `template.pages`.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Template page ID. |
| `number` | integer | Page number, starting at `1`. |
| `height` | integer | Page height in pixels. |
| `width` | integer | Page width in pixels. |
| `download_url` | string | URL to download the rendered template page image. |
| `fields` | array[object] | Field placements configured on that page. |

#### Template Field Placement Object

Returned inside `template.pages[].fields`.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Field placement ID. |
| `field_id` | string | Field definition ID linked to the placement. |
| `role_id` | string | Template role ID responsible for the placement. |
| `label` | string | Label displayed for the field placement. |
| `display_settings` | object|array|string|null | Rendering metadata for the field placement. |
| `created_at` | string | Creation timestamp in ISO 8601 format. |
| `updated_at` | string | Last update timestamp in ISO 8601 format. |

#### Template Status

A template will be in one of the following status:

| Status | Description |
| --- | --- |
| uploading | The template upload is being uploaded. |
| uploaded | The template has been uploaded. |
| processing | The template is being processed. |
| ready | The template is ready to use. |
| failed | The template processing has failed. |
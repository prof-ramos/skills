# Tag Schema

> Schema reutilizável — documentação completa em [`tags.md`](../tags.md)

### Tag Object

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for tag objects returned by the API.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `tag`. |
| `id` | string | Tag ID. |
| `name` | string | Tag display name. |
| `color` | string | Optional 6-character hex color (without the leading `#`) for UI display. `null` when not set. |
| `created_at` | string | Creation timestamp in ISO 8601 format. |
| `updated_at` | string | Last update timestamp in ISO 8601 format. |

Tag names are unique per workspace, case-insensitive (`"Contracts"` and `"contracts"` collide). Leading/trailing whitespace is trimmed and internal whitespace is collapsed to single spaces before storage.

When a tag attached to a document or template appears inline in those resources (under the `tags` or `default_document_tags` field), only `id`, `name`, and `color` are returned.
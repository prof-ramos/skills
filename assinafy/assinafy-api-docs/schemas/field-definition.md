# Field Definition Schema

> Schema reutilizável — documentação completa em [`field-definitions.md`](../field-definitions.md)

### Field Definition Object

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for field definition objects returned by the API.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `field_definition`. |
| `id` | string | Field definition ID. |
| `name` | string | Field display name. |
| `type` | string | Field type code, such as `text`, `date`, `signature`, `initial`, or `virtual`. |
| `regex` | string|null | Regular expression used to validate the field value, when configured. |
| `is_pre_defined` | boolean | Indicates whether the field is predefined by the platform. |
| `is_active` | boolean | Indicates whether the field is active and available for use. |
| `is_required` | boolean | Indicates whether the field requires a value. |
| `is_standard` | boolean | Indicates whether the field belongs to the standard built-in field set. |
| `is_read_only` | boolean | Indicates whether the field value is read-only from the signer's perspective. |
| `is_visible` | boolean | Indicates whether the field is visible to signers and users. |
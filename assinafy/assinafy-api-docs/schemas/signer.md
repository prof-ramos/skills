# Signer Schema

> Schema reutilizável — documentação completa em [`signers.md`](../signers.md)

### Signer Object

The signer endpoints return a base signer object, plus a few signer-session fields in signer-facing flows.

#### Base Signer Fields

These fields are returned by the account-scoped signer endpoints such as:

- `GET /accounts/{account_id}/signers`
- `GET /accounts/{account_id}/signers/{signer_id}`
- `POST /accounts/{account_id}/signers`
- `PUT /accounts/{account_id}/signers/{signer_id}`

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `signer`. |
| `id` | string | Signer custom ID. |
| `full_name` | string | Signer's full name. |
| `email` | string|null | Signer's email address. Used for email-based verification and notifications when configured. |
| `whatsapp_phone_number` | string|null | Signer's WhatsApp phone number in E.164 format (for example, `+5548999990000`). Used for WhatsApp-based verification and notifications when configured. |
| `has_accepted_terms` | boolean | Indicates whether the signer has accepted the terms of use. |

#### Additional Fields In `GET /signers/self`

The signer self endpoint returns the base signer fields above and also includes:

| Field | Type | Description |
| --- | --- | --- |
| `has_signature` | boolean | Indicates whether the signer already has an uploaded signature image stored for reuse. |
| `has_initial` | boolean | Indicates whether the signer already has an uploaded initials image stored for reuse. |
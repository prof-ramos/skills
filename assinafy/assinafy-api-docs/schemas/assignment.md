# Assignment Schema

> Schema reutilizável — documentação completa em [`assignments.md`](../assignments.md)

### Assignment Objects

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for assignment-related objects returned by the API.

#### Assignment Object

Returned by endpoints such as `POST /documents/{documentId}/assignments` and `PUT /documents/{documentId}/assignments/{assignmentId}/reset-expiration`. The same shape is also embedded inside expanded document responses.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `assignment`. |
| `id` | string | Assignment ID. |
| `sender_email` | string | Email address of the user who created the assignment. |
| `method` | string | Assignment method, such as `virtual` or `collect`. |
| `expires_at` | string|null | Expiration timestamp in ISO 8601 format, or `null` when the assignment does not expire. |
| `message` | string|null | Optional invitation message configured for the assignment. |
| `signers` | array[object] | Signers in the assignment, including verification details and tracked notification history when available. |
| `copy_receivers` | array[object] | Signers who only receive a copy of the document. |
| `items` | array[object] | Assignment items to be completed. |
| `summary` | object | Aggregate completion summary for the assignment. |
| `signing_urls` | array[object] | Direct signing URLs generated for each signer. |

#### Assignment Signer Object

Returned inside `assignment.signers`.

| Field | Type | Description |
| --- | --- | --- |
| Base signer fields | object | All fields documented in the [Signer Object](#signer-object) reference. |
| `verification_method` | string|null | Verification method configured for this signer in this assignment. |
| `notification_methods` | array[string]|null | Notification methods configured for this signer in this assignment. |
| `step` | integer|null | Step the signer belongs to in the sequential signing flow. Signers in the same step sign in parallel; the next step is activated once every signer in the previous step has signed. `null` only for legacy records; new assignments always populate it (defaults to `1`). |
| `notified` | boolean|null | `true` once the signature-request notification has been dispatched to this signer. `false` for signers in steps that have not been activated yet. `null` only for legacy records. |
| `completed` | boolean|null | Indicates whether this signer has completed all of their assignment items, or `null` when the signer has no assignment items yet. This completion state is independent from notification delivery failures. **Only present in account-owner contexts.** |
| `notification_history` | array[object] | Tracked notification delivery history for this signer in this assignment. Can be an empty array when the configured channel does not persist delivery history. See Assignment Signer Notification Object. **Only present in account-owner contexts.** |

#### Assignment Signer Notification Object

Returned inside `assignment.signers[].notification_history`.

| Field | Type | Description |
| --- | --- | --- |
| `event` | string | Normalized API event value for the tracked notification record. |
| `status` | string | Normalized delivery status for this endpoint. Returns `failed` when there was a delivery problem; otherwise returns `sent`. |
| `error_code` | string|null | Provider error code when the notification fails. |
| `error_message` | string|null | Provider error message when the notification fails. |
| `sent_at` | string|null | Timestamp in ISO 8601 format when the notification was sent. |
| `failed_at` | string|null | Timestamp in ISO 8601 format when the notification failed. |

Supported `event` values currently include `signature_request`, `document_about_to_expire`, `document_expired`, `document_canceled`, `document_declined`, `signed_delivery`, and `unknown` for unmapped legacy/provider data.

#### Assignment Item Object

Returned inside `assignment.items`.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Assignment item ID. |
| `page` | object|null | Page object where the field is placed, when applicable. |
| `signer` | object | Signer responsible for this item. |
| `field` | object|null | Field definition object associated with this item. |
| `display_settings` | object|array|string|null | Rendering metadata for the item position and appearance. |
| `value` | mixed | Value captured for the item, when completed. |
| `completed` | boolean | Indicates whether the item has been completed. |

#### Assignment Summary Object

Returned inside `assignment.summary`.

| Field | Type | Description |
| --- | --- | --- |
| `signer_count` | integer | Total number of signers represented in the assignment items. |
| `completed_count` | integer | Number of signers who have completed all required items. |
| `signers` | array[object] | Signers included in the summary, each with an additional `completed` boolean flag. |

#### Signing URL Object

Returned inside `assignment.signing_urls`.

| Field | Type | Description |
| --- | --- | --- |
| `signer_id` | string | Signer ID associated with the URL. |
| `url` | string | Direct URL that opens the signing flow for that signer. |
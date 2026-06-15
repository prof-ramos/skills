> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#assignment)

# Assignment

## Índice

- [Assignment Objects](#assignment-objects)
  - [Assignment Object](#assignment-object)
  - [Assignment Signer Object](#assignment-signer-object)
  - [Assignment Signer Notification Object](#assignment-signer-notification-object)
  - [Assignment Item Object](#assignment-item-object)
  - [Assignment Summary Object](#assignment-summary-object)
  - [Signing URL Object](#signing-url-object)
- [Estimate Cost](#estimate-cost)
  - [Header Parameters](#header-parameters)
  - [Body Parameters](#body-parameters)
  - [Response Fields](#response-fields)
  - [Notification Costs](#notification-costs)
  - [Default Behavior](#default-behavior)
  - [Notification Timing and Sequential Signing](#notification-timing-and-sequential-signing)
- [Create without Input](#create-without-input)
  - [Header Parameters](#header-parameters)
  - [Body Parameters](#body-parameters)
- [Create with Input](#create-with-input)
  - [Header Parameters](#header-parameters)
  - [Body Parameters](#body-parameters)
- [Resend](#resend)
  - [Notification Costs](#notification-costs)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Estimate Resend Cost](#estimate-resend-cost)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Response Fields](#response-fields)
- [Reset Expiration](#reset-expiration)
  - [URL Parameters](#url-parameters)
  - [Request Parameters](#request-parameters)
- [Get](#get)
  - [Header Parameters](#header-parameters)
  - [Request Parameters](#request-parameters)
  - [Error Responses](#error-responses)
- [Sign](#sign)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
  - [Error Responses](#error-responses)
- [Decline](#decline)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [WhatsApp Notifications](#whatsapp-notifications)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Response Fields](#response-fields)

---



An assignment represent a request for signees to sign a document.

## Assignment Objects

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for assignment-related objects returned by the API.

### Assignment Object

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

### Assignment Signer Object

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

### Assignment Signer Notification Object

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

### Assignment Item Object

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

### Assignment Summary Object

Returned inside `assignment.summary`.

| Field | Type | Description |
| --- | --- | --- |
| `signer_count` | integer | Total number of signers represented in the assignment items. |
| `completed_count` | integer | Number of signers who have completed all required items. |
| `signers` | array[object] | Signers included in the summary, each with an additional `completed` boolean flag. |

### Signing URL Object

Returned inside `assignment.signing_urls`.

| Field | Type | Description |
| --- | --- | --- |
| `signer_id` | string | Signer ID associated with the URL. |
| `url` | string | Direct URL that opens the signing flow for that signer. |

## Estimate Cost

> Request (Email notification — default, no methods specified)

```
curl -X POST https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/assignments/estimate-cost \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
-d '
{
  "signers": [{}],
  "method": "virtual"
}
'
```

> Request (Whatsapp notification — inferred from verification\_method)

```
curl -X POST https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/assignments/estimate-cost \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
-d '
{
  "signers": [
    {
      "verification_method": "Whatsapp"
    },
    {
      "verification_method": "Whatsapp"
    }
  ],
  "method": "virtual"
}
'
```

> Request (Collect Method)

```
curl -X POST https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/assignments/estimate-cost \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
-d '
{
  "method": "collect",
  "signers": [
    {
      "notification_methods": ["Email"]
    }
  ],
  "entries": [
    {
      "page_id": "615213ed81b071f4293b2fc2",
      "fields": [
        {
          "signer_id": "615605f50e968054a5b7c9b8",
          "field_id": "6152120297080d55bdd13197",
          "display_settings": {
            "top": 285,
            "left": 639,
            "width": 501,
            "height": 27.34,
            "fontSize": 18,
            "fontFamily": "Arial",
            "backgroundColor": "rgb(195, 230, 203)"
          }
        }
      ]
    }
  ]
}
'
```

> 200 OK (Email notification - 0 credits for notifications)

```
{
  "status": 200,
  "message": "",
  "data": {
    "documents": 1,
    "credits": 0,
    "needs_extra_document": false,
    "extra_document_cost": 0,
    "total_credits": 0,
    "breakdown": [],
    "document_balance": 100,
    "credit_balance": 0,
    "has_sufficient_resources": true,
    "blocking_reason": null,
    "message": null
  }
}
```

> 200 OK (Whatsapp notification - 0.45 credits each)

```
{
  "status": 200,
  "message": "",
  "data": {
    "documents": 1,
    "credits": 0.9,
    "needs_extra_document": false,
    "extra_document_cost": 0,
    "total_credits": 0.9,
    "breakdown": [
      {
        "code": "NotificationWhatsapp",
        "name": "Whatsapp Notification",
        "cost": 0.9,
        "quantity": 2,
        "unit_cost": 0.45
      }
    ],
    "document_balance": 100,
    "credit_balance": 0,
    "has_sufficient_resources": false,
    "blocking_reason": "InsufficientCredits",
    "message": null
  }
}
```

> 200 OK (Pending subscription payment - balances preserved, usage blocked)

```
{
  "status": 200,
  "message": "",
  "data": {
    "documents": 1,
    "credits": 0,
    "needs_extra_document": false,
    "extra_document_cost": 0,
    "total_credits": 0,
    "breakdown": [],
    "document_balance": 100,
    "credit_balance": 50,
    "has_sufficient_resources": false,
    "blocking_reason": "PendingPayment",
    "message": "Subscription payment is pending. Complete payment before using documents or credits."
  }
}
```

> 200 OK (No documents remaining and not enough credits for an extra document)

```
{
  "status": 200,
  "message": "",
  "data": {
    "documents": 1,
    "credits": 0,
    "needs_extra_document": true,
    "extra_document_cost": 1,
    "total_credits": 1,
    "breakdown": [],
    "document_balance": 0,
    "credit_balance": 0,
    "has_sufficient_resources": false,
    "blocking_reason": "InsufficientDocuments",
    "message": "Account does not have enough documents."
  }
}
```

`POST /documents/{documentId}/assignments/estimate-cost`

Estimates the cost of creating an assignment without actually creating it. Returns a detailed cost breakdown along with the current account balances. Signer IDs are not required — only the verification or notification method matters for cost calculation.

Each assignment always consumes **1 document** from the plan's monthly document allowance. If the plan documents are exhausted, the `ExtraDocument` cost will be charged from credits instead (`needs_extra_document` will be `true`).

The cost breakdown includes notification costs only (items with cost > 0):

- **Email**: 0 credits (not shown in breakdown)
- **Whatsapp**: 0.45 credits each

Use this endpoint to check if the account has sufficient resources before creating an assignment.

Possible blocking reasons currently returned by this endpoint:

- `PendingPayment`
- `InsufficientDocuments`
- `InsufficientCredits`

If the current subscription is pending payment, the endpoint still returns the real `document_balance` and `credit_balance`, but `has_sufficient_resources` is `false` and `blocking_reason` is `PendingPayment`.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| method | false | Assignment method: `virtual` (default) or `collect`. |
| signers[] | true\* | List of signers. Required for `virtual` method. Each entry can be an empty object `{}` to default to Email. |
| signers[].id | false | Signer ID. Not required for cost estimation. |
| signers[].verification\_method | false | Verification method code. If provided without `notification_methods`, the notification method is inferred. Defaults to `Email`. See [Verification and Notification Methods](#verification-and-notification-methods). |
| signers[].notification\_methods[] | false | List of notification method codes. If provided without `verification_method`, the verification method is inferred. Defaults to `Email`. See [Notification Methods](#verification-and-notification-methods). |
| entries | true\* | A list of page entries with fields. Required for `collect` method. |
| expires\_at | false | Expiration date (ignored for cost calculation). |
| copy\_receivers | false | A list of signer IDs for copy receivers. |
| signer\_ids | false | **(Legacy)** A list of signer IDs. Defaults to Email notification. Use `signers` instead. |

### Response Fields

| Field | Type | Description |
| --- | --- | --- |
| documents | number | Number of documents this assignment will consume (always 1). |
| credits | number | Total notification credits needed. |
| needs\_extra\_document | boolean | Whether the plan document allowance is exhausted and an extra document must be purchased from credits. |
| extra\_document\_cost | number | Cost in credits for the extra document (0 if plan documents are available). |
| total\_credits | number | Total credits needed (notification credits + extra document cost if applicable). |
| breakdown | array | Itemized list of notification costs (only items with cost > 0). |
| breakdown[].code | string | Cost type code (e.g., `NotificationWhatsapp`). |
| breakdown[].name | string | Human-readable cost type name. |
| breakdown[].cost | number | Total cost in credits for this item (unit\_cost x quantity). |
| breakdown[].quantity | number | Number of notifications. |
| breakdown[].unit\_cost | number | Cost per notification. |
| document\_balance | number | Current account document balance. |
| credit\_balance | number | Current account credit balance. |
| has\_sufficient\_resources | boolean | Whether the account has enough documents and credits for this operation. |
| blocking\_reason | string | Block reason when the operation cannot proceed. Currently `PendingPayment`, `InsufficientDocuments`, or `InsufficientCredits` may be returned. Otherwise `null`. |
| message | string | Explanation for the current block state. For example, pending-payment estimates instruct the user to complete payment, while resource-related estimates explain whether documents or credits are missing. Otherwise `null`. |

**Note:** Only one notification method is allowed per signer.

Invalid combinations will return a `400 Bad Request` error with a descriptive message.

### Notification Costs

Each notification method has an associated credit cost that is charged when creating an assignment or resending notifications:

- **Email**: 0 credits per notification
- **Whatsapp**: 0.45 credits per notification

The cost is charged per signer. For example:

- 2 signers with Email notification = 0 credits
- 2 signers with Whatsapp notification = 0.9 credits

Use the [Estimate Cost](#estimate-cost) endpoint to preview the total cost before creating an assignment.

### Default Behavior

The system infers the missing method based on what is provided:

- **Neither specified**: both default to `Email`.
- **Only `verification_method` specified**: `notification_methods` is inferred from the verification method (e.g., `Whatsapp` verification → `Whatsapp` notification).
- **Only `notification_methods` specified**: `verification_method` is inferred from the notification method (e.g., `Whatsapp` notification → `Whatsapp` verification).
- **Both specified**: used as-is (must follow [Coupling Rules](#coupling-rules)).

### Notification Timing and Sequential Signing

By default, every signer is notified as soon as the assignment is created. When the optional `signers[].step` field is used to define a signing order, the notification for each signer is delayed until that signer's step is activated:

- Step 1 signers are notified at creation, exactly as before.
- A higher step is activated — and its signers notified — only after every signer in the previous step has completed signing.

See [Create without Input](#create-without-input) and [Create with Inputs](#create-with-inputs) for the `step` field reference.

## Create without Input

> Request

```
curl -X POST https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/assignments \
-H 'Content-Type: application/json' \
-d '
{
  "signers": [
    {
      "id": "615605f50e968054a5b7c9b8",
      "verification_method": "Email",
      "notification_methods": ["Email"],
      "step": 1
    },
    {
      "id": "615605f50e968054a5b7c9b9",
      "verification_method": "Whatsapp",
      "notification_methods": ["Whatsapp"],
      "step": 2
    }
  ],
  "method": "virtual",
  "expiration": "2021-09-30"
}
'
```

> 200 OK

```
{
  "id": "615605f8f0cc742d680c62c5",
  "expiration": "2021-09-30",
  "signers": [
    {
      "id": "615605f50e968054a5b7c9b8",
      "full_name": "John Dove",
      "email": "[email protected]"
    },
    {
      "id": "615605f50e968054a5b7c9b9",
      "full_name": "Jane Doe",
      "email": "[email protected]"
    }
  ],
  "method": "virtual",
  "items": [
    {
      "id": "615605f8e4a097c44247bd8e",
      "page": null,
      "signer": {
        "id": "615605f50e968054a5b7c9b8",
        "full_name": "John Dove",
        "email": "[email protected]"
      },
      "field": {
        "id": "61521202f2f86152752c6a1b",
        "name": "Virtual",
        "type": "virtual"
      },
      "display_settings": [],
      "value": null,
      "completed": false
    }
  ],
  "signing_urls": [
    {
      "signer_id": "615605f50e968054a5b7c9b8",
      "url": "https://api.assinafy.com.br/v1/sign/[email protected]"
    },
    {
      "signer_id": "615605f50e968054a5b7c9b9",
      "url": "https://api.assinafy.com.br/v1/sign/[email protected]"
    }
  ]
}
```

`POST /documents/{documentId}/assignments`

Create assignments without fields (method: 'virtual').

The document may be in `uploaded`, `metadata_processing`, or `metadata_ready` status when
the virtual assignment is created. When the document has not finished metadata processing,
it remains in its current status and is promoted to `pending_signature` automatically once
metadata processing completes. Signers can be notified immediately but cannot view or sign
the document until it reaches `pending_signature`.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| method | true | Should be `virtual`. |
| signers[] | true | List of signers configuration. |
| signers[].id | true | Signer ID. |
| signers[].step | false | Positive integer that controls signing order. Signers sharing the same step number sign in parallel; a step is activated (its signers are notified) only after every signer in the previous step has signed. If supplied, every signer must supply it, and the values must form a contiguous sequence starting at 1 (e.g. `1, 1, 2, 3` is valid; `1, 3` is not). Omitting `step` from every signer keeps the previous behavior of notifying all signers at once. |
| message | false | Text to be included in the invitation email. |
| expires\_at | false | Expiration date for the assignment in the ISO 8601 format. Default the default is no expiration. |
| copy\_receivers | false | A list of signer IDs that should only receive a copy of the document. |
| signer\_ids | false | **(Legacy)** A list of signer IDs. Defaults to `Email` verification and notification. Use `signers` instead. |

## Create with Input

> Request

```
curl -X POST https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/assignments \
-H 'Content-Type: application/json' \
-d '
{
  "method": "collect",
  "signers": [
    {
      "id": "61521202f665dffcef5f6b24",
      "verification_method": "Email",
      "notification_methods": ["Email"],
      "step": 1
    },
    {
      "id": "615212039529a822e24b6913",
      "verification_method": "Whatsapp",
      "notification_methods": ["Whatsapp"],
      "step": 2
    }
  ],
  "entries": [
    {
      "page_id": "615213ed81b071f4293b2fc2",
      "fields": [
        {
          "signer_id": "61521202f665dffcef5f6b24",
          "field_id": "6152120297080d55bdd13197",
          "display_settings": {
            "left": 69,
            "top": 282,
            "fontFamily": "Arial",
            "fontSize": 18,
            "backgroundColor": "rgb(185, 218, 255)"
          }
        },
        {
          "signer_id": "615212039529a822e24b6913",
          "field_id": "6152120297080d55bdd13197",
          "display_settings": {
            "left": 639,
            "top": 285,
            "fontFamily": "Arial",
            "fontSize": 18,
            "backgroundColor": "rgb(195, 230, 203)"
          }
        }
      ]
    }
  ],
  "expires_at": "2021-09-30T21:00:00Z"
}
'
```

> 200 OK

```
{
  "id": "615606ef81d199996981dbce",
  "expiration": "2021-09-30",
  "signers": [
    {
      "id": "61521202f665dffcef5f6b24",
      "full_name": "Kennith Kuphal",
      "email": "[email protected]"
    },
    {
      "id": "615212039529a822e24b6913",
      "full_name": "Sonny Bayer",
      "email": "[email protected]"
    }
  ],
  "method": null,
  "items": [
    {
      "id": "615606efbb67641186c12330",
      "page": {
        "id": "615213ed81b071f4293b2fc2",
        "number": 1,
        "height": 2100,
        "width": 1275,
        "download_url": "https://api.assinafy.com.br/v1/documents/615213edf8a58f132e1b2384/pages/615213ed81b071f4293b2fc2/download"
      },
      "signer": {
        "id": "61521202f665dffcef5f6b24",
        "full_name": "Kennith Kuphal",
        "email": "[email protected]"
      },
      "field": {
        "id": "6152120297080d55bdd13197",
        "name": "Signature",
        "type": "signature"
      },
      "display_settings": {
        "top": 282,
        "left": 69,
        "fontSize": 18,
        "fontFamily": "Arial",
        "backgroundColor": "rgb(185, 218, 255)"
      },
      "value": null,
      "completed": false
    },
    {
      "id": "615606efcde1a39c9d21e30e",
      "page": {
        "id": "615213ed81b071f4293b2fc2",
        "number": 1,
        "height": 2100,
        "width": 1275,
        "download_url": "https://api.assinafy.com.br/v1/documents/615213edf8a58f132e1b2384/pages/615213ed81b071f4293b2fc2/download"
      },
      "signer": {
        "id": "615212039529a822e24b6913",
        "full_name": "Sonny Bayer",
        "email": "[email protected]"
      },
      "field": {
        "id": "6152120297080d55bdd13197",
        "name": "Signature",
        "type": "signature"
      },
      "display_settings": {
        "top": 285,
        "left": 639,
        "fontSize": 18,
        "fontFamily": "Arial",
        "backgroundColor": "rgb(195, 230, 203)"
      },
      "value": null,
      "completed": false
    }
  ],
  "signing_urls": [
    {
      "signer_id": "61521202f665dffcef5f6b24",
      "url": "https://api.assinafy.com.br/v1/sign/[email protected]"
    },
    {
      "signer_id": "615212039529a822e24b6913",
      "url": "https://api.assinafy.com.br/v1/sign/[email protected]"
    }
  ]
}
```

`POST /documents/{documentId}/assignments`

Create assignments with input fields.

The document must be in `metadata_ready` status when creating a collect assignment —
input fields reference specific pages, so metadata processing must be complete.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| method | true | Should be `collect`. |
| signers[] | false | List of signers configuration. |
| signers[].id | true | Signer ID. References a signer defined in the `signers` array. |
| signers[].step | false | Positive integer that controls signing order. Signers sharing the same step number sign in parallel; a step is activated (its signers are notified) only after every signer in the previous step has signed. If supplied, every signer must supply it, and the values must form a contiguous sequence starting at 1 (e.g. `1, 1, 2, 3` is valid; `1, 3` is not). Omitting `step` from every signer keeps the previous behavior of notifying all signers at once. |
| entries[] | true | List of assignment items. |
| entries[].page\_id | true | Page ID. |
| entries[].fields | true | List of fields in the page. |
| entries[].fields[].signer\_id | true | Signer ID. References a signer defined in the `signers` array. |
| entries[].fields[].field\_id | true | Field ID. |
| entries[].fields[].display\_settings | true | Field positioning and font information. |
| message | false | Text to be included in the invitation email. |
| expires\_at | false | Expiration date for the assignment in the ISO 8601 format. Default the default is no expiration. |
| copy\_receivers[] | false | A list of signer IDs that should only receive a copy of the document. |

## Resend

> Request

```
curl -X PUT "https://api.assinafy.com.br/v1/documents/c57d51eaad68a7/assignments/d51edaee68a7/signers/a51edaee68a7/resend"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "is_sent": true,
    "document_id": "c57d51eaad68a7",
    "signer_id": "a51edaee68a7"
  }
}
```

> 400 Bad Request (Insufficient Credits)

```
{
  "status": 400,
  "message": "Account does not have enough credits.",
  "data": null
}
```

> 400 Bad Request (Signer in a pending step)

```
{
  "status": 400,
  "message": "This signer is in a pending step and has not been notified yet.",
  "data": null
}
```

`PUT /documents/{documentId}/assignments/{assignmentId}/signers/{signerId}/resend`

Resend assignment input request message to a signer. This is used in case it is necessary to resend the notification with the link to sign a document.

The notification will be resent using the same notification methods configured when the assignment was created.

If the assignment uses sequential signing and the target signer belongs to a step that has not been activated yet (no signature-request notification has been sent), the resend request is rejected with a 400 — wait until every signer in the previous step has signed, which automatically activates the next step.

### Notification Costs

Resending notifications may incur credit costs depending on the notification methods used:

- **Email**: 0 credits per resend
- **Whatsapp**: 0.2 credits per resend

If the account does not have sufficient credits, the request will fail with a 400 error.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| documentId | true | The document ID. |
| assignmentId | true | The assignment ID. |
| signerId | true | The signer ID. |

## Estimate Resend Cost

> Request

```
curl -X POST https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/assignments/61f720572d7fecf7c16c8464/signers/615605f50e968054a5b7c9b8/estimate-resend-cost \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK (Email notification - 0 credits)

```
{
  "status": 200,
  "message": "",
  "data": {
    "total": 0,
    "breakdown": [
      {
        "code": "NotificationEmailResend",
        "name": "Email Notification Resend",
        "cost": 0
      }
    ],
    "credit_balance": 100,
    "has_sufficient_credits": true
  }
}
```

> 200 OK (WhatsApp notification - 0.2 credits)

```
{
  "status": 200,
  "message": "",
  "data": {
    "total": 0.2,
    "breakdown": [
      {
        "code": "NotificationWhatsappResend",
        "name": "Whatsapp Notification Resend",
        "cost": 0.2
      }
    ],
    "credit_balance": 100,
    "has_sufficient_credits": true
  }
}
```

> 404 Not Found (Signer not found)

```
{
  "status": 404,
  "message": "Signer not found.",
  "data": null
}
```

`POST /documents/{documentId}/assignments/{assignmentId}/signers/{signerId}/estimate-resend-cost`

Estimates the cost of resending a notification to a signer without actually resending it. This endpoint returns a detailed cost breakdown along with the current account credit balance.

The cost depends on the notification method configured for the signer when the assignment was created:

- **Email**: 0 credits per resend
- **WhatsApp**: 0.2 credits per resend

Use this endpoint to check if the account has sufficient credits before calling the [Resend](#resend) endpoint.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| documentId | true | The document ID. |
| assignmentId | true | The assignment ID. |
| signerId | true | The signer ID. |

### Response Fields

| Field | Type | Description |
| --- | --- | --- |
| total | number | Total cost in credits for resending the notification. |
| breakdown | array | Itemized list of costs by notification method. |
| breakdown[].code | string | Cost type code (e.g., `NotificationEmailResend`, `NotificationWhatsappResend`). |
| breakdown[].name | string | Human-readable cost type name. |
| breakdown[].cost | number | Cost in credits for this notification method resend. |
| credit\_balance | number | Current account credit balance. |
| has\_sufficient\_credits | boolean | Whether the account has enough credits for this operation. |

## Reset Expiration

> Request example

```
curl -X PUT "https://api.assinafy.com.br/v1/documents/c57d51eaad68a7/assignments/d51edaee68a7/reset-expiration" -d
'{
  "expires_at": "2030-08-03T21:00:00Z"
}'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "assignment",
    "id": "1",
    "expires_at": "2030-08-03T21:00:00Z",
    "signers": [
      {
        "id": "customid1",
        "full_name": "Signer 1",
        "email": "[email protected]",
        "has_accepted_terms": false
      },
      {
        "id": "customid2",
        "full_name": "Signer 2",
        "email": "[email protected]",
        "has_accepted_terms": false
      }
    ],
    "method": "virtual",
    "items": [
      {
        "id": "1",
        "page": {
          "id": "1",
          "number": 1,
          "height": 1,
          "width": 1,
          "download_url": "https://api.assinafy.com.br/v1/documents/1/pages/1/download"
        },
        "signer": {
          "id": "customid1",
          "full_name": "Signer 1",
          "email": "[email protected]",
          "has_accepted_terms": false
        },
        "field": null,
        "display_settings": "",
        "value": "",
        "completed": true
      },
      {
        "id": "2",
        "page": {
          "id": "1",
          "number": 1,
          "height": 1,
          "width": 1,
          "download_url": "https://api.assinafy.com.br/v1/documents/1/pages/1/download"
        },
        "signer": {
          "id": "customid2",
          "full_name": "Signer 2",
          "email": "[email protected]",
          "has_accepted_terms": false
        },
        "field": null,
        "display_settings": "",
        "value": "",
        "completed": false
      },
      {
        "id": "3",
        "page": {
          "id": "1",
          "number": 1,
          "height": 1,
          "width": 1,
          "download_url": "https://api.assinafy.com.br/v1/documents/1/pages/1/download"
        },
        "signer": {
          "id": "customid1",
          "full_name": "Signer 1",
          "email": "[email protected]",
          "has_accepted_terms": false
        },
        "field": null,
        "display_settings": "",
        "value": "",
        "completed": true
      }
    ],
    "summary": {
      "signer_count": 2,
      "completed_count": 1,
      "signers": [
        {
          "id": "customid1",
          "full_name": "Signer 1",
          "email": "[email protected]",
          "has_accepted_terms": false,
          "completed": true
        },
        {
          "id": "customid2",
          "full_name": "Signer 2",
          "email": "[email protected]",
          "has_accepted_terms": false,
          "completed": false
        }
      ]
    }
  }
}
```

`PUT /documents/{documentId}/assignments/{assignmentId}/reset-expiration`

Reset assignment expiration. This endpoint can be used to set a new expiration
date for an assignment. A null value is accepted and means no expiration date.

**Headers**:

- `Content-Type` - `application/json`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| documentId | true | The document ID. |
| assignmentId | true | The assignment ID. |

### Request Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| expires\_at | true | The new date and time to be set in the ISO 8601 format. A null value means no expiration. |

## Get

> Request

```
curl 'https://api.assinafy.com.br/v1/sign?signer-access-code=9uAWyOXx9hgzCKdCuahkinwvg8tWJ2RC-n6hhxyLS1QfMhqWSw-PnwQlSs2oPNea'
```

> 200 OK

```
{
  "id": "615213edf8a58f132e1b2384",
  "account_id": "d199996981dbd199996981db",
  "name": "sample-contract-one-page.pdf",
  "status": "pending",
  "assignment": {
    "id": "615606ef81d199996981dbce",
    "expiration": "2021-09-30",
    "method": "collect",
    "signers": [
      {
        "id": "customid1",
        "full_name": "Signer 1",
        "email": "[email protected]",
        "has_accepted_terms": true,
        "verification_method": "Email",
        "notification_methods": ["Email"]
      },
      {
        "id": "customid2",
        "full_name": "Signer 2",
        "email": "[email protected]",
        "has_accepted_terms": false,
        "verification_method": "Email",
        "notification_methods": ["Email"]
      }
    ],
    "items": [
      {
        "id": "615606efcde1a39c9d21e30e",
        "page": {
          "id": "615213ed81b071f4293b2fc2",
          "number": 1,
          "height": 2100,
          "width": 1275,
          "download_url": "https://api.assinafy.com.br/v1/documents/615213edf8a58f132e1b2384/pages/615213ed81b071f4293b2fc2/download"
        },
        "signer": {
          "id": "615212039529a822e24b6913",
          "full_name": "Sonny Bayer",
          "email": "[email protected]",
          "has_accepted_terms": true
        },
        "field": {
          "id": "6152120297080d55bdd13197",
          "name": "Signature",
          "type": "signature"
        },
        "display_settings": {
          "top": 285,
          "left": 639,
          "width": 501,
          "height": 27.340000000000032,
          "fontSize": 18,
          "fontFamily": "Arial",
          "backgroundColor": "rgb(195, 230, 203)"
        },
        "value": null,
        "completed": false
      }
    ],
    "summary": {
      "signer_count": 2,
      "completed_count": 1,
      "signers": [
        {
          "id": "customid1",
          "full_name": "Signer 1",
          "email": "[email protected]",
          "has_accepted_terms": true,
          "completed": true
        },
        {
          "id": "customid2",
          "full_name": "Signer 2",
          "email": "[email protected]",
          "has_accepted_terms": false,
          "completed": false
        }
      ]
    },
    "signing_urls": [
      {
        "signer_id": "customid1",
        "url": "https://api.assinafy.com.br/v1/sign/[email protected]",
      },
      {
        "signer_id": "customid2",
        "url": "https://api.assinafy.com.br/v1/sign/[email protected]",
      }
    ]
  },
   "artifacts": {
    "original": "https://api.assinafy.com.br/v1/documents/3/download/original",
    "certificated": "https://api.assinafy.com.br/v1/documents/3/download/certificated",
    "certificate-page": "https://api.assinafy.com.br/v1/documents/3/download/certificate-page",
    "bundle": "https://api.assinafy.com.br/v1/documents/3/download/bundle"
  },
  "pages": [
    {
      "id": "615213ed81b071f4293b2fc2",
      "number": 1,
      "height": 2100,
      "width": 1275,
      "download_url": "https://api.assinafy.com.br/v1/documents/615213edf8a58f132e1b2384/pages/615213ed81b071f4293b2fc2/download"
    }
  ],
  "created_at": 1632769005,
  "updated_at": 1632769005,
  "current_signer": {
    "id": "615212039529a822e24b6913",
    "full_name": "Till Man",
    "email": "[email protected]",
    "has_accepted_terms": true,
    "verification_method": "Email",
    "notification_methods": ["Email"]
  }
}
```

`GET /sign`

Retrieve document assignment details as a signer. It requires the signer access code
with verification code.

The response is the document data that the signer have access to.
The embedded `assignment.signers` entries follow the Assignment Signer Object reference.
The `completed` and `notification_history` fields are omitted in this signer-facing context.

### Header Parameters

- `Content-Type` - `application/json`

### Request Parameters

| Parameter | Default | Required | Description |
| --- | --- | --- | --- |
| `signer-access-code` |  | true | Signer access code. |
| `has_accepted_terms` | false | false | Indicates whether signer has accepted the terms. |

### Error Responses

**409 Conflict** — Returned when the signer attempts to view a document that has not
yet reached a viewable status. Typically happens during the brief window when a virtual
assignment was created before metadata processing finished. Clients should retry with
exponential backoff and surface a "preparing document" state to the user while retrying.

```
{
  "status": 409,
  "data": null,
  "message": "The document is not ready to be viewed yet."
}
```

## Sign

> Request

```
curl -X POST 'https://api.assinafy.com.br/v1/documents/c57d51eaad68a7/assignments/d51edaee68a7?signer-access-code=9uAWyOXx9hgzCKdCuahkinwvg8tWJ2RC-n6hhxyLS1QfMhqWSw-PnwQlSs2oPNea' -d '
[
  {
    "itemId": "615606efcde1a39c9d21e30e",
    "fieldId": "6152120297080d55bdd13197",
    "pageId": "615213ed81b071f4293b2fc2",
    "value": "Signed by Sonny Bayer"
  }
]
'
```

`POST /documents/{documentId}/assignments/{assignmentId}`

Allow a signer to sign a document with input fields (collect method).

**Important:** For virtual assignments, signers must confirm their data via `PUT /documents/{documentId}/signers/confirm-data` before signing. Attempting to sign without confirming data will result in a 400 error: "Signer data must be confirmed before signing."

**Headers**:

- `Content-Type` - `application/json`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signer-access-code` | true | Signer access code as query string parameter. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `[].itemId` | true | The item id. |
| `[].fieldId` | true | Field it associated to the item. |
| `[].pageId` | true | The page id. |
| `[].value` | true | String representation of the value. |

### Error Responses

**400 Bad Request** - If attempting to sign without confirming data (for virtual assignments):

```
{
  "name": "Bad Request",
  "message": "Signer data must be confirmed before signing.",
  "code": 0,
  "status": 400
}
```

**409 Conflict** — Returned when the signer attempts to sign a document that has not
yet reached `pending_signature`. Typically happens during the window between virtual
assignment creation and metadata processing completion. Clients should retry with
exponential backoff while showing a "preparing document" state.

```
{
  "status": 409,
  "data": null,
  "message": "The document is not ready to be signed yet."
}
```

## Decline

> Request

```
curl -X PUT "https://api.assinafy.com.br/v1/documents/c57d51eaad68a7/assignments/d51edaee68a7/reject?signer-access-code=1e7d51e68a7" \
-H 'Content-Type: application/json' \
-d '{
  "decline_reason": "I do not agree with clause 2."
}'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": []
}
```

`PUT /documents/{documentId}/assignments/{assignmentId}/reject?signer-access-code={accessCode}`

Allows a signer to decline an assignment.

### Header Parameters

- `Content-Type: application/json`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| documentId | true | The document ID. |
| assignmentId | true | The assignment ID. |
| accessCode | true | Signer access code. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| decline\_reason | true | Descriptive reason for declining the invitation. |

## WhatsApp Notifications

> Request

```
curl -X GET "https://api.assinafy.com.br/v1/documents/c57d51eaad68a7/assignments/d51edaee68a7/whatsapp-notifications"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "sent_at": 1710000000,
      "header": "Documento para assinatura: Contrato de Servico",
      "body": "Oi, Maria.\n\nJoao Silva enviou um documento para voce revisar e assinar.\n\nMensagem:\nPor favor assine o contrato\n\nPara acessar o documento, toque em \"Abrir documento\".",
      "buttons": [
        {
          "text": "Abrir documento"
        }
      ],
      "phone_number": "+5511999990001",
      "signer_id": "a51edaee68a7"
    }
  ]
}
```

`GET /documents/{documentId}/assignments/{assignmentId}/whatsapp-notifications`

List all WhatsApp notification messages sent for a specific assignment.

The response includes the rendered template text split into `header`, `body`, and `buttons` — showing exactly what the signer would see on their phone.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| documentId | true | The document ID. |
| assignmentId | true | The assignment ID. |

### Response Fields

| Field | Type | Description |
| --- | --- | --- |
| sent\_at | integer | Unix timestamp when the message was sent. |
| header | string | Rendered header text of the WhatsApp message. |
| body | string | Rendered body text of the WhatsApp message. |
| buttons | array | List of button objects with `text` and optionally `url`. |
| buttons[].text | string | The button label shown to the signer. |
| phone\_number | string | Recipient phone number (E.164 format). |
| signer\_id | string | The signer's ID. |
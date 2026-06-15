> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#webhooks)

# Webhooks

## Índice

- [Webhook Objects](#webhook-objects)
  - [Webhook Subscription Object](#webhook-subscription-object)
  - [Webhook Dispatch Object](#webhook-dispatch-object)
  - [How it works](#how-it-works)
- [Get Subscription](#get-subscription)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Update Subscription](#update-subscription)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Inactivate](#inactivate)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Payload Reference](#payload-reference)
  - [Delivery Contract](#delivery-contract)
  - [Common Envelope](#common-envelope)
  - [Event Catalog](#event-catalog)
  - [Sample Payloads](#sample-payloads)
- [List Types](#list-types)
  - [Header Parameters](#header-parameters)
- [List Webhook Dispaches](#list-webhook-dispaches)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Query Parameters](#query-parameters)
  - [Response Headers](#response-headers)
  - [Response Fields](#response-fields)
- [Retry Webhook Dispatch](#retry-webhook-dispatch)
  - [URL Parameters](#url-parameters)
  - [Response Fields](#response-fields)
  - [Error Responses](#error-responses)

---



> Example of payload:

```
{
  "id":987,
  "event":"document_ready",
  "object":{
    "id": "efo39340da030af0g",
    "name":"document.pdf",
    "type":"document"
  },
  "subject":{
    "id": "efo39340da030af0g",
    "name":"John Doe",
    "type":"user"
  },
  "account_id":"o39340do39340d"
}
```

Webhooks allow your application to **receive real-time notifications** whenever specific events occur in our system.
Instead of periodically polling our API, you can subscribe to events and automatically receive an HTTP request containing event data.

Using the Webhooks API, you can:

- **Subscribe** to one or more event types;
- **Inactivate** when you no longer need updates;
- **Receive notifications** at your configured endpoint whenever those events happen.

## Webhook Objects

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for webhook configuration and delivery-history objects returned by the API.

### Webhook Subscription Object

Returned by:

- `GET /accounts/{account_id}/webhooks/subscriptions`
- `PUT /accounts/{account_id}/webhooks/subscriptions`
- `DELETE /accounts/{account_id}/webhooks/subscriptions`

| Field | Type | Description |
| --- | --- | --- |
| `events` | array[string] | Event types currently subscribed for delivery. |
| `is_active` | boolean | Indicates whether webhook delivery is active. |
| `url` | string|null | Webhook endpoint URL. |
| `email` | string|null | Contact email associated with the subscription. |
| `updated_at` | string|null | Last update timestamp in ISO 8601 format. |

### Webhook Dispatch Object

Returned by `GET /accounts/{account_id}/webhooks` and `POST /accounts/{account_id}/webhooks/{dispatch_id}/retry`.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `activity_dispatching_history`. |
| `id` | string | Dispatch entry ID. |
| `event` | string | Event type that triggered the dispatch. |
| `activity_id` | integer | Internal activity ID associated with the dispatch. |
| `endpoint` | string|null | URL that received the webhook request. |
| `payload` | object|null | JSON payload sent to the webhook endpoint. |
| `delivered` | boolean | Indicates whether the webhook was delivered successfully. |
| `http_status` | integer|null | HTTP status code returned by the endpoint, when available. |
| `response_body` | string|null | Response body captured from the endpoint, truncated when necessary. |
| `error` | string|null | Delivery error message, when applicable. |
| `created_at` | string | Creation timestamp in ISO 8601 format. |
| `updated_at` | string | Last update timestamp in ISO 8601 format. |

### How it works

1. You register your webhook URL via the **subscription endpoint**.
2. Whenever an event occurs (e.g., `document_ready`), our system sends a `POST` request with a JSON payload to your endpoint.
3. Your server acknowledges the event with an HTTP `200 OK` response.
4. You can later **unsubscribe** by inactivating webhook settings at any time.

## Get Subscription

> Request

```
curl -X GET "https://api.assinafy.com.br/v1/accounts/Avmvk6Urzus3byLD2/webhooks/subscriptions" \
-H "Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "events": [
      "document_ready",
      "document_prepared"
    ],
    "is_active": true,
    "url": "http://example.com?test=1",
    "email": "[email protected]",
    "updated_at": "2023-05-10T14:58:24Z"
  }
}
```

`GET /accounts/{account_id}/webhooks/subscriptions`

Retrieves the current webhook subscription status for a specific account.
Use this endpoint to check which events the account is currently subscribed to and verify the delivery configuration.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | The ID of the account which is related to the events. |

## Update Subscription

> Request

```
curl -X PUT "https://api.assinafy.com.br/v1/accounts/Avmvk6Urzus3byLD2/webhooks/subscriptions" \
-H "Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg" \
-H "Content-Type: application/json" \
-d '
{
  "events": [
    "document_ready",
    "document_prepared"
  ],
  "is_active": true,
  "url": "http://example.com?test=1",
  "email": "[email protected]"
}'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "events": [
      "document_ready",
      "document_prepared"
    ],
    "is_active": true,
    "url": "http://example.com?test=1",
    "email": "[email protected]",
    "updated_at": "2023-05-10T14:58:24Z"
  }
}
```

`PUT /accounts/{account_id}/webhooks/subscriptions`

Updates the webhook subscription settings for a specific account.
Use this endpoint to modify which events are being monitored, enable or disable notifications, and update the delivery or contact details.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | Unique identifier of the account whose webhook subscription you want to update. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| events | true | Array with list of events to subscribe to. |
| is\_active | true | Boolean indicating whether events should be notified to webhook. |
| url | true | The URL which will receive events. |
| email | true | The email address that will receive important information related to webhook communication. |

## Inactivate

> Request

```
curl -X PUT "https://api.assinafy.com.br/v1/accounts/Avmvk6Urzus3byLD2/webhooks/inactivate" \
-H "Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "events": [
      "document_ready",
      "document_prepared"
    ],
    "is_active": false,
    "url": "http://example.com?myparam=value",
    "email": "[email protected]",
    "updated_at": "2023-05-10T14:58:24Z"
  }
}
```

`PUT /accounts/{account_id}/webhooks/inactivate`

Deactivates the webhook integration for a specific account.
While the integration is inactive, no events will be sent to the configured webhook endpoint.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | Unique identifier of the account whose webhook integration should be deactivated. |

## Payload Reference

This section documents the HTTP request your endpoint will receive whenever a subscribed event is triggered, and the shape of the JSON body we send for each event type.

> Sample top level structure:

```
{
  "id": 987,
  "event": "document_ready",
  "message": null,
  "payload": null,
  "origin": {
    "ip": "189.12.34.56",
    "user-agent": "Mozilla/5.0 ..."
  },
  "created_at": 1705312200,
  "subject": {
    "id": "...",
    "type": "User"
  },
  "object": {
    "id": "...",
    "type": "Document"
  },
  "account_id": "Avmvk6Urzus3byLD2"
}
```

### Delivery Contract

When an event occurs, we send an HTTP `POST` request to the endpoint configured in your webhook subscription.

| Property | Value |
| --- | --- |
| Method | `POST` |
| Content-Type | `application/json` |
| Connection header | `close` |
| Success criteria | Any `2xx` response |
| Attempts | Up to 2 per event (initial attempt + 1 retry) |
| Retry wait | 3 seconds between attempts |
| Circuit breaker | After 10 consecutive failed events, delivery is paused and only ~5% of events are probed until one succeeds. Use the **Retry Webhook Dispatch** endpoint to force redelivery. |
| Response capture | We store the first 2000 characters of your response body for debugging (see **List Webhook Dispatches**). |

Your endpoint must respond within a reasonable time and return a `2xx` status code. Non-`2xx` responses, connection errors, and timeouts are all treated as failed deliveries and counted toward the circuit breaker.

### Common Envelope

> `document_uploaded` — User uploaded a new document

```
{
  "id": 6,
  "event": "document_uploaded",
  "message": "document uploaded",
  "payload": null,
  "origin": {
    "ip": "172.19.0.1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
  },
  "created_at": 1705312200,
  "subject": {
    "id": "d6zqpbyog2v3xvxerwn8la94",
    "name": "John Smith",
    "email": "[email protected]",
    "telephone": "+5548999999999",
    "government_id": "86861345059",
    "is_email_verified": false,
    "has_accepted_terms": true,
    "is_password_set": true,
    "created_at": 1705312200,
    "to_be_deleted_at": null,
    "type": "User"
  },
  "object": {
    "id": "doc5",
    "account_id": "1a",
    "template_id": null,
    "name": "5.pdf",
    "status": "uploaded",
    "artifacts": {
      "original": "https://app.assinafy.com.br/v1/documents/doc5/download/original"
    },
    "is_closed": false,
    "signing_url": "https://app.assinafy.com.br/sign/doc5",
    "decline_reason": null,
    "declined_by": null,
    "created_at": 1705312199,
    "updated_at": 1705312199,
    "assignment": null,
    "pages": [],
    "type": "Document"
  },
  "account_id": "1a"
}
```

> `assignment_created` — User created an assignment for the document

```
{
  "id": 8,
  "event": "assignment_created",
  "message": null,
  "payload": {
    "user_name": "John Smith",
    "user_email": "[email protected]",
    "user_telephone": "+5548999999999"
  },
  "origin": {
    "ip": "172.19.0.1",
    "user-agent": "Mozilla/5.0 ..."
  },
  "created_at": 1705312250,
  "subject": {
    "id": "d6zqpbyog2v3xvxerwn8la94",
    "name": "John Smith",
    "email": "[email protected]",
    "telephone": "+5548999999999",
    "government_id": "86861345059",
    "is_email_verified": false,
    "has_accepted_terms": true,
    "is_password_set": true,
    "created_at": 1705312200,
    "to_be_deleted_at": null,
    "type": "User"
  },
  "object": {
    "id": "doc2",
    "account_id": "1a",
    "template_id": null,
    "name": "2.pdf",
    "status": "pending_signatures",
    "artifacts": {
      "original": "https://app.assinafy.com.br/v1/documents/doc2/download/original"
    },
    "is_closed": false,
    "signing_url": "https://app.assinafy.com.br/sign/doc2",
    "decline_reason": null,
    "declined_by": null,
    "created_at": 1705312199,
    "updated_at": 1705312250,
    "assignment": {
      "id": "2",
      "sender_email": "[email protected]",
      "method": "virtual",
      "expires_at": null,
      "message": null,
      "signers": [
        {
          "id": "customid1",
          "full_name": "Signer 1",
          "email": "[email protected]",
          "whatsapp_phone_number": "+5548999999999",
          "has_accepted_terms": false
        }
      ],
      "copy_receivers": [],
      "items": [],
      "summary": {
        "signer_count": 1,
        "completed_count": 0,
        "signers": []
      },
      "signing_urls": []
    },
    "pages": [],
    "type": "Document"
  },
  "account_id": "1a"
}
```

> `signature_requested` — User requested a signer to sign the document

```
{
  "id": 1,
  "event": "signature_requested",
  "message": null,
  "payload": {
    "signer_email": "[email protected]",
    "signer_full_name": "John Signer"
  },
  "origin": {
    "ip": "172.19.0.1",
    "user-agent": "Mozilla/5.0 ..."
  },
  "created_at": 1705312200,
  "subject": {
    "id": "d6zqpbyog2v3xvxerwn8la94",
    "name": "John Smith",
    "email": "[email protected]",
    "telephone": "+5548999999999",
    "government_id": "86861345059",
    "is_email_verified": false,
    "has_accepted_terms": true,
    "is_password_set": true,
    "created_at": 1705312200,
    "to_be_deleted_at": null,
    "type": "User"
  },
  "object": {
    "id": "doc2",
    "account_id": "1a",
    "template_id": null,
    "name": "2.pdf",
    "status": "pending_signatures",
    "artifacts": {
      "original": "https://app.assinafy.com.br/v1/documents/doc2/download/original"
    },
    "is_closed": false,
    "signing_url": "https://app.assinafy.com.br/sign/doc2",
    "decline_reason": null,
    "declined_by": null,
    "created_at": 1705312199,
    "updated_at": 1705312199,
    "assignment": {
      "id": "2",
      "sender_email": "[email protected]",
      "method": "virtual",
      "expires_at": null,
      "message": null,
      "signers": [
        {
          "id": "customid1",
          "full_name": "Signer 1",
          "email": "[email protected]",
          "whatsapp_phone_number": "+5548999999999",
          "has_accepted_terms": false
        },
        {
          "id": "customid2",
          "full_name": "Signer 2",
          "email": "[email protected]",
          "whatsapp_phone_number": null,
          "has_accepted_terms": false
        }
      ],
      "copy_receivers": [],
      "items": [],
      "summary": {
        "signer_count": 0,
        "completed_count": 0,
        "signers": []
      },
      "signing_urls": []
    },
    "pages": [],
    "type": "Document"
  },
  "account_id": "1a"
}
```

> `signer_signed_document` — Signer signed the document

```
{
  "id": 7,
  "event": "signer_signed_document",
  "message": null,
  "payload": {
    "signer_full_name": "Signer 1"
  },
  "origin": {
    "ip": "172.19.0.1",
    "user-agent": "Mozilla/5.0 ..."
  },
  "created_at": 1705312200,
  "subject": {
    "id": "customid1",
    "full_name": "Signer 1",
    "email": "[email protected]",
    "whatsapp_phone_number": "+5548999999999",
    "has_accepted_terms": false,
    "type": "Signer"
  },
  "object": {
    "id": "doc2",
    "account_id": "1a",
    "template_id": null,
    "name": "2.pdf",
    "status": "partially_signed",
    "artifacts": {
      "original": "https://app.assinafy.com.br/v1/documents/doc2/download/original"
    },
    "is_closed": false,
    "signing_url": "https://app.assinafy.com.br/sign/doc2",
    "decline_reason": null,
    "declined_by": null,
    "created_at": 1705312199,
    "updated_at": 1705315800,
    "assignment": {
      "id": "2",
      "sender_email": "[email protected]",
      "method": "virtual",
      "expires_at": null,
      "message": null,
      "signers": [
        {
          "id": "customid1",
          "full_name": "Signer 1",
          "email": "[email protected]",
          "whatsapp_phone_number": "+5548999999999",
          "has_accepted_terms": false
        }
      ],
      "copy_receivers": [],
      "items": [],
      "summary": {
        "signer_count": 1,
        "completed_count": 1,
        "signers": []
      },
      "signing_urls": []
    },
    "pages": [],
    "type": "Document"
  },
  "account_id": "1a"
}
```

> `document_ready` — Last signer signed, document is now ready

```
{
  "id": 50,
  "event": "document_ready",
  "message": null,
  "payload": null,
  "origin": null,
  "created_at": 1705316400,
  "subject": {
    "id": "1a",
    "name": "Acme Inc.",
    "primary_color": "aabbcc",
    "secondary_color": null,
    "created_at": 1690000000,
    "users": [
      {
        "id": "d6zqpbyog2v3xvxerwn8la94",
        "name": "John Smith",
        "email": "[email protected]",
        "telephone": "+5548999999999",
        "government_id": "86861345059",
        "is_email_verified": false,
        "has_accepted_terms": true,
        "is_password_set": true,
        "created_at": 1705312200,
        "to_be_deleted_at": null
      }
    ],
    "type": "Account"
  },
  "object": {
    "id": "doc5",
    "account_id": "1a",
    "template_id": null,
    "name": "5.pdf",
    "status": "certificated",
    "artifacts": {
      "original": "https://app.assinafy.com.br/v1/documents/doc5/download/original",
      "certificated": "https://app.assinafy.com.br/v1/documents/doc5/download/certificated",
      "certificate-page": "https://app.assinafy.com.br/v1/documents/doc5/download/certificate-page",
      "bundle": "https://app.assinafy.com.br/v1/documents/doc5/download/bundle"
    },
    "is_closed": true,
    "signing_url": "https://app.assinafy.com.br/sign/doc5",
    "decline_reason": null,
    "declined_by": null,
    "created_at": 1705312199,
    "updated_at": 1705316400,
    "assignment": null,
    "pages": [],
    "type": "Document"
  },
  "account_id": "1a"
}
```

Every webhook body shares the same top-level structure

| Field | Type | Description |
| --- | --- | --- |
| id | integer | Internal activity ID that produced this event. Useful for deduplication on your side. |
| event | string | Event type identifier. See the [event catalog](#event-catalog) below and the **List Types** endpoint for the full list. |
| message | string | null | A human-readable message describing the event. May contain token placeholders like `signer_signed_document {signer_full_name}`. Can be `null`. |
| payload | object | null | Event-specific parameters. Keys vary per event — see each entry in the catalog. Can be `null` when the event carries no extra parameters. |
| origin | object | null | Where the action was triggered from (when available). Shape: `{ "ip": "string", "user-agent": "string" }`. |
| created\_at | integer | Unix timestamp (seconds) when the event was recorded. |
| subject | object | The entity that performed the action. Polymorphic — see below. |
| object | object | The entity the action was performed on. Polymorphic — see below. |
| account\_id | string | The `custom_id` of the account that owns this event. Always present. |

#### About `subject` and `object`

Both `subject` and `object` are **polymorphic**: their shape depends on which entity they represent for a given event. We always add a `type` property with the entity class name, which is one of:

- `User`
- `Signer`
- `Account`
- `Document`
- `Template`

The remaining properties correspond to the same fields returned by the REST API for that resource. The `object` is additionally serialized with its extra relationships expanded (for example a `Document` object includes `assignment` and `pages`). The `subject` is serialized with its base fields only.

To keep payloads from growing unbounded, whenever `subject` or `object` is an `Account`, the `integration` property (which includes the dispatch history) is removed before sending.

The subject/object pairing is fixed per event. The table below lists every event we dispatch, what the subject and object represent, and which extra keys you can expect inside `payload`.

### Event Catalog

| Event | Subject type | Object type | `payload` keys | Description |
| --- | --- | --- | --- | --- |
| `document_uploaded` | User | Document | — | The user uploaded a new document. |
| `document_metadata_ready` | User | Document | — | The document was normalized to PDF and its pages are available. |
| `document_prepared` | User | Document | — | The user prepared a document (fields assigned to signers). |
| `assignment_created` | User | Document | `user_name`, `user_email`, `user_telephone` | The user created an assignment for the document. The payload includes a snapshot of the creator profile. |
| `document_ready` | Account | Document | — | The last signer of the assignment signed the document. The document status is now `ready`. |
| `document_processing_failed` | Account | Document | `error_message` | The document could not be processed. |
| `signature_requested` | User | Document | `signer_email` *or* `signer_full_name` *or* `signer_whatsapp_phone_number` (depending on the notification method used) | The user requested a signer to sign the document. |
| `signer_created` | User | Signer | `signer_full_name` | The user created a new signer. |
| `signer_email_verified` | Signer | Document | `signer_email` | The signer's email was verified through a code linked to the document. |
| `signer_whatsapp_verified` | Signer | Document | `signer_whatsapp_phone_number` | The signer's WhatsApp number was verified through a code linked to the document. |
| `signer_data_confirmed` | Signer | Document | `signer_email` | The signer confirmed their data before signing. |
| `signer_viewed_document` | Signer | Document | `signer_full_name` | The signer opened the document for the first time. |
| `signer_signed_document` | Signer | Document | `signer_full_name` | The signer signed the document. |
| `signer_rejected_document` | Signer | Document | `signer_full_name` | The signer refused to sign the document. |
| `user_rejected_document` | User | Document | `user_name` | The document was cancelled by a user of the account. |
| `template_created` | User | Template | — | The user created a new template. |
| `template_processed` | User | Template | — | A template's metadata has been processed and is ready for use. |
| `template_processing_failed` | Account | Template | `error_message` | A template could not be processed. |

### Sample Payloads

Field-level details for embedded entities follow the same schema returned by the corresponding REST endpoints. See the [Document Object](#document-object), [Signer Object](#signer-object), [User Object](#user-object), [Template Object](#template-object), and [Workspace Account Object](#workspace-account-object) references. Treat any unknown field as a forward-compatible addition.

Notice that for `document_ready` the `subject` is the `Account` itself: this event is emitted by the system when the document finishes being certificated, not by any particular user. The same applies to `document_processing_failed` and `template_processing_failed`.

## List Types

> Request

```
curl -X GET "https://api.assinafy.com.br/v1/webhooks/event-types" \
-H "Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "id": "document_prepared",
      "description": "Triggered when the User as subject prepares a Document."
    },
    {
      "id": "assignment_created",
      "description": "Triggered when the User created an assignment for a Document. Includes a snapshot of the creator profile (name, email, telephone) and origin IP/user-agent. When a virtual assignment is created before metadata processing finishes, this event may arrive before `document_metadata_ready`. Subscribers should not assume an ordering between the two."
    },
    {
      "id": "document_metadata_ready",
      "description": "Triggered when the document is ready to be prepared. The document has been normalized to PDF and its pages are available. Under the virtual pre-metadata flow, `assignment_created` may already have fired for this document before this event — do not rely on an ordering between them."
    },
    {
      "id": "document_ready",
      "description": "Triggered when the last Signer of the assignment signs the Document, as a result, the document status becomes ready."
    },
    {
      "id": "document_uploaded",
      "description": "Triggered when the User has uploaded a Document"
    },
    {
      "id": "signature_requested",
      "description": "Triggered when the User requested signature of a Document"
    },
    {
      "id": "signer_created",
      "description": "Triggered when the User created a Signer"
    },
    {
      "id": "signer_email_verified",
      "description": "Triggered when Signer's email has been verified by a verification code linked to a Document"
    },
    {
      "id": "signer_signed_document",
      "description": "Triggered when the Signer signed a Document"
    },
    {
      "id": "signer_rejected_document",
      "description": "Triggered when the Signer rejected signing a Document"
    },
    {
      "id": "signer_viewed_document",
      "description": "Triggered when the Signer viewed a Document for the first time"
    },
    {
      "id": "document_processing_failed",
      "description": "Unprocessable document, either invalid or the system couldn't process it"
    }
  ]
}
```

`GET /webhooks/event-types`

Retrieves the list of all available event types that can be subscribed to via webhooks.
Use this endpoint to discover which events your application can receive notifications for.

### Header Parameters

- `Authorization: Bearer {access_token}`

## List Webhook Dispaches

> Request

```
curl -X GET "https://api.assinafy.com.br/v1/accounts/Avmvk6Urzus3byLD2/webhooks" \
-H "Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
      "event": "document_ready",
      "activity_id": 456,
      "endpoint": "https://example.com/webhook",
      "payload": {
        "event": "document_ready",
        "id": 456,
        "object": {
          "id": "abc123",
          "name": "contract.pdf",
          "type": "document"
        },
        "subject": {
          "id": "def456",
          "name": "John Doe",
          "type": "user"
        },
        "account_id": "Avmvk6Urzus3byLD2"
      },
      "delivered": true,
      "http_status": 200,
      "response_body": "OK",
      "error": null,
      "created_at": 1705312200,
      "updated_at": 1705312200
    }
  ]
}
```

`GET /accounts/{account_id}/webhooks`

Retrieves the delivery history for webhooks sent to this account's configured endpoint.
Use this endpoint to monitor webhook delivery status, debug failed deliveries, and verify payload contents.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | The ID of the account. |

### Query Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| event | string | Filter by event type (e.g., `document_ready`) |
| delivered | string | Filter by delivery status: `true` or `false` |
| from | integer | Unix timestamp - filter data after this time |
| to | integer | Unix timestamp - filter data before this time |
| page | integer | Page number for pagination |
| per-page | integer | Items per page (default: 20) |

### Response Headers

| Header | Description |
| --- | --- |
| X-Pagination-Current-Page | Current returned page |
| X-Pagination-Total-Count | Total count of records |
| X-Pagination-Page-Count | Count of pages |
| X-Pagination-Per-Page | Count of records per page |

### Response Fields

| Field | Type | Description |
| --- | --- | --- |
| id | string | Unique entry custom ID (hex string) |
| event | string | The event type that triggered this webhook |
| activity\_id | integer | The associated activity ID |
| endpoint | string | The URL the webhook was sent to |
| payload | object | The JSON payload that was sent |
| delivered | boolean | Whether the delivery was successful |
| http\_status | integer | HTTP status code returned (null if connection failed) |
| response\_body | string | Response body from the endpoint (truncated to 2000 chars) |
| error | string | Error message if delivery failed |
| created\_at | integer | Unix timestamp when the delivery was attempted |
| updated\_at | integer | Unix timestamp of last update |

## Retry Webhook Dispatch

> Request

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/Avmvk6Urzus3byLD2/webhooks/{id}/retry" \
-H "Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "activity_dispatching_history",
    "id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "event": "document_ready",
    "activity_id": 456,
    "endpoint": "https://example.com/webhook",
    "payload": {
      "event": "document_ready",
      "id": 456,
      "object": {
        "id": "abc123",
        "name": "contract.pdf",
        "type": "document"
      },
      "subject": {
        "id": "def456",
        "name": "John Doe",
        "type": "user"
      },
      "account_id": "Avmvk6Urzus3byLD2"
    },
    "delivered": true,
    "http_status": 200,
    "response_body": "OK",
    "error": null,
    "created_at": 1705312200,
    "updated_at": 1705312200
  }
}
```

`POST /accounts/{account_id}/webhooks/{dispatch_id}/retry`

Retries dispatching a webhook for a specific entry. This endpoint allows you to manually retry a failed webhook delivery without waiting for automatic retries. Returns the newly created webhook entry.

%default\_post\_headers%

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | The ID of the account. |
| dispatch\_id | true | The ID of the webhook entry to retry. |

### Response Fields

The response returns a webhook entry with the same fields as the list endpoint:

| Field | Type | Description |
| --- | --- | --- |
| id | string | Unique entry custom ID (hex string) |
| event | string | The event type that triggered this webhook |
| activity\_id | integer | The associated activity ID |
| endpoint | string | The URL the webhook was sent to |
| payload | object | The JSON payload that was sent |
| delivered | boolean | Whether the delivery was successful |
| http\_status | integer | HTTP status code returned (null if connection failed) |
| response\_body | string | Response body from the endpoint (truncated to 2000 chars) |
| error | string | Error message if delivery failed |
| created\_at | integer | Unix timestamp when the delivery was attempted |
| updated\_at | integer | Unix timestamp of last update |

### Error Responses

- `404 Not Found`: The webhook entry was not found or does not belong to this account.
- `400 Bad Request`: The webhook subscription is inactive or the event type is not subscribed.
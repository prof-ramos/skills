# Webhook Schema

> Schema reutilizável — documentação completa em [`webhooks.md`](../webhooks.md)

### Webhook Objects

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for webhook configuration and delivery-history objects returned by the API.

#### Webhook Subscription Object

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

#### Webhook Dispatch Object

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

#### How it works

1. You register your webhook URL via the **subscription endpoint**.
2. Whenever an event occurs (e.g., `document_ready`), our system sends a `POST` request with a JSON payload to your endpoint.
3. Your server acknowledges the event with an HTTP `200 OK` response.
4. You can later **unsubscribe** by inactivating webhook settings at any time.
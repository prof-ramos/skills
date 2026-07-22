# Resend REST API Reference

Comprehensive technical documentation for Resend REST API endpoints, HTTP methods, headers, request/response payload schemas, and pagination mechanics.

Base URL: `https://api.resend.com`

---

## 1. Authentication & Common Headers

All HTTP requests to Resend REST API require an Authorization Bearer token header containing a valid Resend API key.

```http
Authorization: Bearer RESEND_API_KEY
Content-Type: application/json
User-Agent: resend-api-skill/1.0
```

---

## 2. Emails API

### 2.1 Send Single Email
- **Method & Path:** `POST /emails`
- **Description:** Dispatches a single transactional email message.

#### Request Payload Schema
```json
{
  "from": "Acme Team <onboarding@resend.dev>",
  "to": ["user@example.com"],
  "subject": "Welcome to Acme!",
  "html": "<p>Hi <strong>Alice</strong>, welcome aboard!</p>",
  "text": "Hi Alice, welcome aboard!",
  "cc": ["manager@example.com"],
  "bcc": ["audit@example.com"],
  "reply_to": ["support@example.com"],
  "headers": {
    "X-Entity-Ref-ID": "inv_987654321"
  },
  "tags": [
    { "name": "category", "value": "welcome" }
  ],
  "attachments": [
    {
      "content": "SGVsbG8gV29ybGQh",
      "filename": "hello.txt",
      "content_type": "text/plain"
    }
  ]
}
```

#### Response Payload (200 OK)
```json
{
  "id": "49bf7fff-9b12-4716-9d8a-9040716a4959"
}
```

### 2.2 Send Batch Emails
- **Method & Path:** `POST /emails/batch`
- **Description:** Sends up to 100 emails in a single HTTP request payload.

#### Request Payload Schema
```json
[
  {
    "from": "Acme <news@yourdomain.com>",
    "to": ["user1@example.com"],
    "subject": "July Updates",
    "html": "<h1>Update 1</h1>"
  },
  {
    "from": "Acme <news@yourdomain.com>",
    "to": ["user2@example.com"],
    "subject": "July Updates",
    "html": "<h1>Update 2</h1>"
  }
]
```

#### Response Payload (200 OK)
```json
{
  "data": [
    { "id": "e1654877-22f3-4217-a068-07e0aa812f62" },
    { "id": "670c538e-0f4b-4b10-8b4e-e179e8631b52" }
  ]
}
```

### 2.3 Get Single Email
- **Method & Path:** `GET /emails/{email_id}`
- **Description:** Retrieves metadata and status of a sent email by ID.

#### Response Payload (200 OK)
```json
{
  "object": "email",
  "id": "49bf7fff-9b12-4716-9d8a-9040716a4959",
  "to": ["user@example.com"],
  "from": "Acme Team <onboarding@resend.dev>",
  "created_at": "2026-07-22T08:00:00.000Z",
  "subject": "Welcome to Acme!",
  "html": "<p>Hi <strong>Alice</strong>, welcome aboard!</p>",
  "text": "Hi Alice, welcome aboard!",
  "last_event": "delivered"
}
```

---

## 3. Domains API

### 3.1 Create Domain
- **Method & Path:** `POST /domains`
- **Request Body:**
  ```json
  {
    "name": "mail.yourdomain.com",
    "region": "us-east-1"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": "d91cd95f-6947-4a6f-a964-00c401be29c6",
    "name": "mail.yourdomain.com",
    "status": "not_started",
    "created_at": "2026-07-22T08:00:00.000Z",
    "region": "us-east-1",
    "records": [
      {
        "record": "DKIM",
        "name": "resend._domainkey",
        "type": "CNAME",
        "value": "dkim.resend.com",
        "status": "not_started"
      },
      {
        "record": "SPF",
        "name": "bounces",
        "type": "MX",
        "value": "feedback-smtp.us-east-1.amazonses.com",
        "status": "not_started"
      },
      {
        "record": "SPF",
        "name": "bounces",
        "type": "TXT",
        "value": "v=spf1 include:amazonses.com ~all",
        "status": "not_started"
      }
    ]
  }
  ```

### 3.2 Verify Domain
- **Method & Path:** `POST /domains/{domain_id}/verify`
- **Description:** Triggers DNS record verification on Resend infrastructure.
- **Response (200 OK):**
  ```json
  {
    "object": "domain",
    "id": "d91cd95f-6947-4a6f-a964-00c401be29c6",
    "status": "pending"
  }
  ```

### 3.3 List Domains & Get Domain Details
- **List Method & Path:** `GET /domains`
- **Get Method & Path:** `GET /domains/{domain_id}`

### 3.4 Delete Domain
- **Method & Path:** `DELETE /domains/{domain_id}`
- **Response (200 OK):**
  ```json
  {
    "object": "domain",
    "id": "d91cd95f-6947-4a6f-a964-00c401be29c6",
    "deleted": true
  }
  ```

---

## 4. API Keys API

### 4.1 Create API Key
- **Method & Path:** `POST /api-keys`
- **Request Body:**
  ```json
  {
    "name": "Production Sending Key",
    "permission": "sending_access",
    "domain_id": "d91cd95f-6947-4a6f-a964-00c401be29c6"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": "36ef9159-8664-4bf8-b677-2e0618037b5c",
    "token": "re_123456789_abcdefghijklmnopqrstuvwxyz"
  }
  ```

### 4.2 List API Keys
- **Method & Path:** `GET /api-keys`
- **Response (200 OK):**
  ```json
  {
    "data": [
      {
        "id": "36ef9159-8664-4bf8-b677-2e0618037b5c",
        "name": "Production Sending Key",
        "created_at": "2026-07-22T08:00:00.000Z"
      }
    ]
  }
  ```

### 4.3 Delete API Key
- **Method & Path:** `DELETE /api-keys/{api_key_id}`

---

## 5. Audiences & Contacts API

### 5.1 Audiences
- `POST /audiences` — Body: `{"name": "Newsletter"}`
- `GET /audiences` — Returns array of audience objects.
- `GET /audiences/{audience_id}` — Returns audience object.
- `DELETE /audiences/{audience_id}` — Deletes specified audience.

### 5.2 Contacts
- `POST /audiences/{audience_id}/contacts` — Body:
  ```json
  {
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "unsubscribed": false
  }
  ```
- `GET /audiences/{audience_id}/contacts` — Returns subscriber list.
- `GET /audiences/{audience_id}/contacts/{contact_id}` — Retrieves single contact profile.
- `PATCH /audiences/{audience_id}/contacts/{contact_id}` — Body:
  ```json
  {
    "first_name": "Jonathan",
    "unsubscribed": true
  }
  ```
- `DELETE /audiences/{audience_id}/contacts/{contact_id}` — Removes contact from audience.

---

## 6. Raw Curl Examples

```bash
# Send Email via Raw Curl
curl -X POST "https://api.resend.com/emails" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Acme <onboarding@resend.dev>",
    "to": ["user@example.com"],
    "subject": "Testing Resend REST API",
    "html": "<p>Hello from cURL!</p>"
  }'
```

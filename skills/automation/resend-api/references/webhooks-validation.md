# Webhook Verification & Event Payload Specification

Complete guide to receiving Resend webhook notifications, enforcing Svix signature verification, preventing replay attacks, and handling event lifecycle payloads.

---

## 1. Webhook Overview & Architecture

Resend uses [Svix](https://www.svix.com/) for reliable, secure webhook event delivery. When events occur in your Resend account (such as email delivery, bounce, or click), Resend sends an HTTP `POST` request to your configured webhook endpoint URL.

### Security Headers Delivered by Resend
Every incoming HTTP POST request from Resend carries three critical Svix verification headers:

| Header Name | Format Example | Purpose |
|-------------|----------------|---------|
| `svix-id` | `msg_2DRX9h1Vp5k6W87vK1Y` | Unique message identifier for deduplication/idempotency. |
| `svix-timestamp` | `1721635200` | UNIX timestamp (seconds) when signature was generated. |
| `svix-signature` | `v1,g0hM9SsE+... v1,49bf7fff...` | Space-separated list of signatures (`v1,<base64_hmac>`). |

---

## 2. Svix Signature Verification Algorithm

To verify that an incoming request genuinely originated from Resend and was not tampered with:

1. **Extract Headers:** Read `svix-id`, `svix-timestamp`, and `svix-signature` from the HTTP request headers.
2. **Read Raw Body:** Capture the raw unparsed HTTP body string/bytes. (Do NOT use parsed JSON).
3. **Check Timestamp Freshness:** Calculate `abs(current_unix_time - svix_timestamp)`. If the difference is > 300 seconds (5 minutes), reject the request as a potential replay attack.
4. **Construct Signed Payload:** Concatenate `${svix-id}.${svix-timestamp}.${raw_body}`.
5. **Compute HMAC SHA-256:**
   - Extract the base64 portion of your secret key after `whsec_` (e.g. if `RESEND_WEBHOOK_SECRET="whsec_dGVzdF9zZWNyZXQ="`, base64 decode `dGVzdF9zZWNyZXQ=`).
   - Calculate HMAC SHA-256 digest over the signed payload string using the decoded secret key.
   - Base64 encode the resulting digest.
6. **Compare Signatures:** Ensure `v1,<computed_base64_digest>` matches at least one signature entry in the `svix-signature` header list using constant-time comparison.

---

## 3. Implementation Code Examples

### 3.1 Python Verification (Native standard library - 0 dependencies)
```python
import base64
import hmac
import hashlib
import time

def verify_svix_signature(
    raw_body: bytes,
    headers: dict,
    secret: str,
    tolerance_seconds: int = 300
) -> bool:
    msg_id = headers.get("svix-id")
    msg_timestamp = headers.get("svix-timestamp")
    msg_signature = headers.get("svix-signature")

    if not msg_id or not msg_timestamp or not msg_signature:
        raise ValueError("Missing mandatory Svix headers")

    # Timestamp tolerance check
    try:
        ts = int(msg_timestamp)
    except ValueError:
        raise ValueError("Invalid svix-timestamp format")

    if abs(time.time() - ts) > tolerance_seconds:
        raise ValueError("Webhook timestamp outside tolerance window (replay attack prevention)")

    # Prepare secret key bytes
    clean_secret = secret.replace("whsec_", "")
    secret_bytes = base64.b64decode(clean_secret)

    # Construct signed payload: id.timestamp.body
    signed_payload = f"{msg_id}.{msg_timestamp}.".encode("utf-8") + raw_body

    # Compute HMAC SHA-256
    expected_digest = hmac.new(secret_bytes, signed_payload, hashlib.sha256).digest()
    expected_b64 = base64.b64encode(expected_digest).decode("utf-8")
    expected_sig = f"v1,{expected_b64}"

    # Verify against space-separated signature list
    passed_signatures = msg_signature.split(" ")
    for sig in passed_signatures:
        if hmac.compare_digest(sig, expected_sig):
            return True

    raise ValueError("No matching valid signature found")
```

### 3.2 Node.js Verification (Using `svix` package)
```javascript
import { Webhook } from 'svix';

export function handleResendWebhook(rawBodyBuffer, headers, secret) {
  const wh = new Webhook(secret);
  
  try {
    const payload = wh.verify(rawBodyBuffer, {
      'svix-id': headers['svix-id'],
      'svix-timestamp': headers['svix-timestamp'],
      'svix-signature': headers['svix-signature'],
    });
    return payload; // Returns parsed JSON object if valid
  } catch (err) {
    console.error('Svix signature verification failed:', err.message);
    throw new Error('Invalid webhook signature');
  }
}
```

---

## 4. Webhook Event Payload Examples

### 4.1 `email.sent`
Triggered when Resend accepts the email for delivery.
```json
{
  "created_at": "2026-07-22T08:30:00.000Z",
  "data": {
    "created_at": "2026-07-22T08:29:58.000Z",
    "email_id": "49bf7fff-9b12-4716-9d8a-9040716a4959",
    "from": "Acme Team <onboarding@resend.dev>",
    "subject": "Welcome to Acme!",
    "to": ["user@example.com"]
  },
  "type": "email.sent"
}
```

### 4.2 `email.delivered`
Triggered when the recipient's mail server confirms delivery.
```json
{
  "created_at": "2026-07-22T08:30:05.000Z",
  "data": {
    "created_at": "2026-07-22T08:29:58.000Z",
    "email_id": "49bf7fff-9b12-4716-9d8a-9040716a4959",
    "from": "Acme Team <onboarding@resend.dev>",
    "subject": "Welcome to Acme!",
    "to": ["user@example.com"]
  },
  "type": "email.delivered"
}
```

### 4.3 `email.bounced`
Triggered when a hard or soft bounce occurs.
```json
{
  "created_at": "2026-07-22T08:30:10.000Z",
  "data": {
    "created_at": "2026-07-22T08:29:58.000Z",
    "email_id": "49bf7fff-9b12-4716-9d8a-9040716a4959",
    "from": "Acme Team <onboarding@resend.dev>",
    "subject": "Welcome to Acme!",
    "to": ["invalid-user@example.com"],
    "bounce_type": "Permanent",
    "message": "550 5.1.1 User unknown"
  },
  "type": "email.bounced"
}
```

### 4.4 `email.clicked`
Triggered when recipient clicks a link in an open-tracked email.
```json
{
  "created_at": "2026-07-22T08:35:00.000Z",
  "data": {
    "click": {
      "ipAddress": "192.0.2.1",
      "link": "https://example.com/activate?token=abc",
      "timestamp": "2026-07-22T08:34:59.000Z",
      "userAgent": "Mozilla/5.0..."
    },
    "created_at": "2026-07-22T08:29:58.000Z",
    "email_id": "49bf7fff-9b12-4716-9d8a-9040716a4959",
    "from": "Acme Team <onboarding@resend.dev>",
    "subject": "Welcome to Acme!",
    "to": ["user@example.com"]
  },
  "type": "email.clicked"
}
```

---

## 5. Webhook Operational Best Practices

1. **Return HTTP 200 Fast:** Always send back HTTP 200 OK immediately after signature verification. Enqueue heavy background processing asynchronously.
2. **Idempotency via `svix-id`:** Track `svix-id` in Redis or SQL to prevent duplicate processing if Svix retries a webhook delivery.
3. **Secure Secret Storage:** Keep `RESEND_WEBHOOK_SECRET` in environment variables or secret vaults. Never commit secrets to git repositories.

---
name: resend-api
description: >-
  Always use when the user asks to send transactional or batch emails, configure custom email domains, manage API keys, verify Svix webhooks, handle email templates (HTML/React Email), or manage audiences and contacts using Resend API or SDKs (Node.js, Python). Trigger phrases include: 'resend', 'send email resend', 'enviar email resend', 'resend api key', 'resend domain', 'resend webhook', 'resend email template', 'resend audiences', 'resend contacts', 'gerenciar dominio resend', 'verificar webhook resend'.
license: MIT
metadata:
  author: prof-ramos
  version: "1.0.0"
  topic: automation
---

# Resend API Specialist

Expert Agent Skill for integrating, building, and operating transactional email workflows, domain DNS management, API key configuration, Svix webhook signature verification, email templates, and audience contacts using the Resend platform via REST API and official Node.js/Python SDKs.

---

## 1. Overview

Resend is a developer-first email platform for transactional email sending, domain authentication (DKIM, SPF, DMARC), template rendering (HTML/React Email), webhook processing, and contact audience management.

### Key Capabilities
- **Transactional & Batch Email Dispatch:** Send single emails or bulk batches (up to 100 per call) with HTML, plain text, custom headers, tags, and base64 attachments up to 40 MB.
- **Domain Authentication:** Register domains, retrieve required DKIM/SPF CNAME/TXT records, and trigger verification status checks.
- **API Key Lifecycle:** Generate scoped API keys (`full_access` vs. `sending_access`) and revoke compromised credentials.
- **Webhook Security:** Verify inbound Svix webhook signatures (`svix-id`, `svix-timestamp`, `svix-signature`) to prevent tampering and replay attacks.
- **Audiences & Contacts:** Programmatically add, update, unsubscribe, list, and delete contacts in subscriber audiences.

---

## 2. Reference Routing & Documentation Map

To preserve prompt budget, consult the granular reference documentation under `references/` based on the active sub-task:

| Objective / Sub-Task | Reference Document | Key Topics Covered |
|----------------------|-------------------|-------------------|
| REST Endpoints, HTTP Headers, JSON Payloads | `references/rest-api.md` | Base URL (`https://api.resend.com`), Auth headers, raw curl examples for all resources. |
| Node.js & Python SDK Usage | `references/sdks-nodejs-python.md` | `@resend/node` and `resend` Python packages, async patterns, exception handling. |
| Webhook Setup & Signature Verification | `references/webhooks-validation.md` | Svix HMAC SHA-256 verification algorithm, timestamp windows, payload schemas. |
| HTML & React Email Templates | `references/email-templates.md` | Inline CSS, `@react-email/render`, responsive layout, variable substitution, attachments. |
| Audiences, Contacts & GDPR Compliance | `references/audiences-contacts.md` | Audience CRUD, contact suppression/unsubscribes, consent tracking, GDPR tips. |

---

## 3. Core Rules & Safety Guardrails

1. **Authentication:** All requests MUST include `Authorization: Bearer <RESEND_API_KEY>` header.
2. **Domain Verification Required:** E-mails sent from unverified custom domains will be rejected with HTTP `422 Unprocessable Entity`. Use `onboarding@resend.dev` only for testing.
3. **Payload Limits:** Maximum single email body + attachments payload size is **40 MB**. Maximum batch sending limit is **100 emails per request**.
4. **API Key Principle of Least Privilege:** Use `sending_access` keys bound to a specific domain in production application servers; keep `full_access` keys restricted to CI/CD or admin tooling.
5. **Webhook Raw Body Retention:** Webhook verification MUST parse the raw unparsed HTTP body string/bytes. Do NOT verify signatures using parsed JSON objects.
6. **Rate Limit Handling:** Standard account rate limits apply (2 requests/sec for emails). Implement exponential backoff when encountering `429 Too Many Requests`.

---

## 4. Environment Setup & Configuration

Configure the following environment variables across deployment environments:

```bash
# Primary API Key (Required)
export RESEND_API_KEY="re_123456789_abcdefghijklmnopqrstuvwxyz"

# Default Sender Address (Optional, e.g. "Acme Team <onboarding@resend.dev>" or "app@yourdomain.com")
export RESEND_DEFAULT_FROM="Acme <onboarding@resend.dev>"

# Webhook Secret for Svix Verification (Starts with whsec_)
export RESEND_WEBHOOK_SECRET="whsec_dGVzdF9zZWNyZXRfa2V5XzEyMzQ1Njc4OQ=="
```

---

## 5. Quick Starts

### Node.js SDK (`@resend/node`)
```javascript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

async function sendWelcomeEmail() {
  const { data, error } = await resend.emails.send({
    from: 'Acme <onboarding@resend.dev>',
    to: ['user@example.com'],
    subject: 'Welcome to Acme!',
    html: '<strong>Hello World!</strong>',
  });

  if (error) {
    console.error('Failed to send email:', error);
    return;
  }
  console.log('Email sent successfully. ID:', data.id);
}
```

### Python SDK (`resend`)
```python
import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

params = {
    "from": "Acme <onboarding@resend.dev>",
    "to": ["user@example.com"],
    "subject": "Welcome to Acme!",
    "html": "<strong>Hello World!</strong>",
}

try:
    email = resend.Emails.send(params)
    print(f"Email sent successfully. ID: {email['id']}")
except Exception as e:
    print(f"Failed to send email: {e}")
```

---

## 6. Operational Guides

### 6.1 Transactional Email & Batch Sending
- **Single Email:** Call `POST https://api.resend.com/emails` with `from`, `to` (array), `subject`, and either `html` or `text`.
- **Batch Sending:** Call `POST https://api.resend.com/emails/batch` passing a JSON array of up to 100 email objects.
- **Attachments:** Pass `attachments: [{ filename: 'doc.pdf', content: '<base64>' }]`.

### 6.2 Domain Management
- Add domain via `POST /domains` with `name` (e.g. `mail.example.com`) and region (`us-east-1`, `eu-west-1`, `ap-southeast-1`).
- Extract returned DKIM (CNAME) and SPF/MX records and publish them to your DNS provider.
- Trigger verification via `POST /domains/{domain_id}/verify`.

### 6.3 API Keys Management
- Create API key via `POST /api-keys` with `name`, `permission` (`full_access` or `sending_access`), and optional `domain_id`.
- Note: The returned secret `token` is shown ONLY ONCE.

### 6.4 Webhook Signature Verification
- Inbound webhooks carry `svix-id`, `svix-timestamp`, and `svix-signature` headers.
- Reconstruct signature payload: `${svix_id}.${svix_timestamp}.${raw_body}`.
- Compute HMAC SHA-256 with decoded base64 key from `RESEND_WEBHOOK_SECRET`.
- Reject requests if timestamp is older than 300 seconds (5 minutes).

### 6.5 Email Templates
- Use responsive HTML with inline CSS or React Email (`@react-email/components`).
- Ensure plain-text fallback (`text`) is supplied alongside `html` for deliverability.

### 6.6 Audiences & Contacts
- Create audience via `POST /audiences`.
- Create contact via `POST /audiences/{audience_id}/contacts` with `email`, `first_name`, `last_name`, `unsubscribed`.

---

## 7. Error Handling & HTTP Status Codes

| Status Code | Meaning | Common Cause & Resolution |
|-------------|---------|---------------------------|
| `400 Bad Request` | Missing required fields / syntax error | Verify `from`, `to`, `subject` parameters and JSON structure. |
| `401 Unauthorized` | Invalid/missing API Key | Ensure `Authorization: Bearer <RESEND_API_KEY>` is set. |
| `403 Forbidden` | Key lacks permission | Key with `sending_access` cannot perform admin/domain operations. |
| `404 Not Found` | Resource missing | Check specified ID for email, domain, audience, or contact. |
| `422 Unprocessable Entity` | Domain not verified / Invalid domain | Complete DKIM/SPF DNS verification before sending. |
| `429 Too Many Requests` | Rate limit reached (2 req/s) | Implement exponential backoff using `Retry-After` header. |
| `500 Server Error` | Resend infrastructure error | Retry request with exponential backoff. |

---

## 8. Verification Checklist

Before deploying any Resend integration:
- [ ] Environment variable `RESEND_API_KEY` is loaded securely.
- [ ] Sending domain is verified (`status: verified`) with valid DKIM & SPF records.
- [ ] Raw body is preserved for Svix webhook signature validation.
- [ ] Batch email payloads do not exceed 100 emails per HTTP request.
- [ ] Attachments are base64 encoded and total payload is < 40 MB.
- [ ] Unsubscribe headers (`List-Unsubscribe`) and contact compliance are enforced.
- [ ] All helper scripts pass syntax check (`make check`).

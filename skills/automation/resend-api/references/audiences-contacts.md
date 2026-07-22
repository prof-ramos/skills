# Audiences & Contacts API Reference & Compliance Guide

Complete documentation for managing Resend subscriber lists (Audiences), individual contacts, unsubscribe preferences, and privacy compliance (GDPR/CAN-SPAM/LGPD).

---

## 1. Concepts & Data Architecture

- **Audience:** A named list or segment of subscriber contact profiles (e.g., "Newsletter Subscribers", "Beta Testers", "Customers").
- **Contact:** An individual subscriber record containing `email`, `first_name`, `last_name`, `unsubscribed` status flag, and metadata.
- **Unsubscribe Compliance:** Contacts marked `unsubscribed: true` are automatically suppressed from future audience dispatches by Resend.

---

## 2. Audiences Endpoints & Operations

### 2.1 Create Audience
- **Endpoint:** `POST https://api.resend.com/audiences`
- **Request Body:**
  ```json
  {
    "name": "Beta Testers"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "object": "audience",
    "id": "78261ee2-911b-491a-a107-164e26210f92",
    "name": "Beta Testers"
  }
  ```

### 2.2 List Audiences
- **Endpoint:** `GET https://api.resend.com/audiences`
- **Response (200 OK):**
  ```json
  {
    "object": "list",
    "data": [
      {
        "id": "78261ee2-911b-491a-a107-164e26210f92",
        "name": "Beta Testers",
        "created_at": "2026-07-22T08:00:00.000Z"
      }
    ]
  }
  ```

### 2.3 Get Single Audience
- **Endpoint:** `GET https://api.resend.com/audiences/{audience_id}`

### 2.4 Delete Audience
- **Endpoint:** `DELETE https://api.resend.com/audiences/{audience_id}`
- **Response (200 OK):**
  ```json
  {
    "object": "audience",
    "id": "78261ee2-911b-491a-a107-164e26210f92",
    "deleted": true
  }
  ```

---

## 3. Contacts Endpoints & Operations

### 3.1 Create Contact
- **Endpoint:** `POST https://api.resend.com/audiences/{audience_id}/contacts`
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "unsubscribed": false
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "object": "contact",
    "id": "e1654877-22f3-4217-a068-07e0aa812f62"
  }
  ```

### 3.2 Update Contact Profile or Subscription Status
- **Endpoint:** `PATCH https://api.resend.com/audiences/{audience_id}/contacts/{contact_id}`
- **Request Body:**
  ```json
  {
    "first_name": "Alicia",
    "unsubscribed": true
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "object": "contact",
    "id": "e1654877-22f3-4217-a068-07e0aa812f62",
    "unsubscribed": true
  }
  ```

### 3.3 List Contacts in Audience
- **Endpoint:** `GET https://api.resend.com/audiences/{audience_id}/contacts`
- **Response (200 OK):**
  ```json
  {
    "object": "list",
    "data": [
      {
        "id": "e1654877-22f3-4217-a068-07e0aa812f62",
        "email": "user@example.com",
        "first_name": "Alicia",
        "last_name": "Smith",
        "created_at": "2026-07-22T08:00:00.000Z",
        "unsubscribed": true
      }
    ]
  }
  ```

### 3.4 Delete Contact
- **Endpoint:** `DELETE https://api.resend.com/audiences/{audience_id}/contacts/{contact_id}`
- **Response (200 OK):**
  ```json
  {
    "object": "contact",
    "id": "e1654877-22f3-4217-a068-07e0aa812f62",
    "deleted": true
  }
  ```

---

## 4. Privacy & Regulatory Compliance (GDPR, CAN-SPAM, LGPD)

When building email campaigns and managing contacts via Resend API:

1. **Explicit Opt-in Consent:** Record explicit consent timestamp and IP address in your user database prior to adding contacts to marketing audiences.
2. **List-Unsubscribe Header:** Include RFC 8058 `List-Unsubscribe` headers in marketing broadcasts:
   ```json
   "headers": {
     "List-Unsubscribe": "<https://yourdomain.com/unsubscribe?email=user@example.com>, <mailto:unsubscribe@yourdomain.com>",
     "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"
   }
   ```
3. **Right to be Forgotten (Deletion):** Immediately call `DELETE /audiences/{audience_id}/contacts/{contact_id}` when a user requests data deletion under GDPR Article 17 or LGPD Article 18.
4. **Physical Mailing Address:** Commercial emails must contain a valid physical postal address of the sender in the HTML footer to comply with CAN-SPAM regulations.

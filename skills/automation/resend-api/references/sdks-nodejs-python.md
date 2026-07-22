# Official SDK Guide: Node.js & Python

Detailed usage, code samples, initialization patterns, and error handling for the official Resend SDKs in Node.js (`@resend/node` / `resend`) and Python (`resend`).

---

## 1. Node.js SDK (`@resend/node` or `resend`)

### 1.1 Installation
```bash
npm install resend
# or
pnpm add resend
# or
yarn add resend
```

### 1.2 Initialization
```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);
```

### 1.3 Sending Single Email (TypeScript/JavaScript)
```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

async function sendTransactional() {
  const { data, error } = await resend.emails.send({
    from: 'Acme <onboarding@resend.dev>',
    to: ['user@example.com'],
    subject: 'Order Confirmation #1092',
    html: '<h1>Thank you for your order!</h1>',
    tags: [{ name: 'category', value: 'receipt' }],
    headers: { 'X-Entity-Ref-ID': 'order_1092' },
  });

  if (error) {
    console.error('Error sending email:', error.name, error.message);
    return;
  }

  console.log('Successfully dispatched email ID:', data.id);
}
```

### 1.4 Sending Batch Emails (Node.js)
```typescript
async function sendBatchNotifications(users: { email: string; name: string }[]) {
  const payload = users.map(user => ({
    from: 'Acme <onboarding@resend.dev>',
    to: [user.email],
    subject: 'System Maintenance Scheduled',
    html: `<p>Hi ${user.name}, system maintenance is scheduled tonight at 02:00 UTC.</p>`,
  }));

  const { data, error } = await resend.batch.send(payload);

  if (error) {
    console.error('Batch send failed:', error);
    return;
  }

  console.log('Batch response count:', data.data.length);
}
```

### 1.5 Domain Verification (Node.js)
```typescript
async function setupDomain(domainName: string) {
  // 1. Create domain
  const { data: newDomain, error: createErr } = await resend.domains.create({
    name: domainName,
    region: 'us-east-1',
  });
  if (createErr) throw createErr;

  console.log('Created domain ID:', newDomain.id);
  console.log('DNS Records to configure:', newDomain.records);

  // 2. Trigger verification
  const { data: verifyData, error: verifyErr } = await resend.domains.verify(newDomain.id);
  if (verifyErr) throw verifyErr;

  console.log('Domain verification state:', verifyData.status);
}
```

### 1.6 Contacts Management (Node.js)
```typescript
async function addSubscriberToAudience(audienceId: string, email: string, firstName: string) {
  const { data, error } = await resend.contacts.create({
    email,
    firstName,
    audienceId,
    unsubscribed: false,
  });

  if (error) {
    console.error('Failed to add contact:', error);
    return;
  }

  console.log('Created contact ID:', data.id);
}
```

---

## 2. Python SDK (`resend`)

### 2.1 Installation
```bash
pip install resend
```

### 2.2 Initialization
```python
import os
import resend

resend.api_key = os.environ.get("RESEND_API_KEY")
```

### 2.3 Sending Single Email (Python)
```python
import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

def send_welcome_email(user_email: str, user_name: str) -> str:
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": [user_email],
        "subject": f"Welcome aboard, {user_name}!",
        "html": f"<p>Hi <strong>{user_name}</strong>, glad to have you!</p>",
        "text": f"Hi {user_name}, glad to have you!",
        "tags": [{"name": "onboarding", "value": "v1"}],
    }

    try:
        response = resend.Emails.send(params)
        return response["id"]
    except Exception as e:
        print(f"Failed to dispatch email: {e}")
        raise
```

### 2.4 Sending Batch Emails (Python)
```python
import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

def send_batch_emails():
    params = [
        {
            "from": "Acme <onboarding@resend.dev>",
            "to": ["user1@example.com"],
            "subject": "Weekly Newsletter",
            "html": "<h1>Newsletter Issue #1</h1>",
        },
        {
            "from": "Acme <onboarding@resend.dev>",
            "to": ["user2@example.com"],
            "subject": "Weekly Newsletter",
            "html": "<h1>Newsletter Issue #1</h1>",
        },
    ]

    try:
        batch_res = resend.Batch.send(params)
        print("Sent batch IDs:", [item["id"] for item in batch_res["data"]])
    except Exception as e:
        print(f"Batch sending failed: {e}")
```

### 2.5 Domain Management (Python)
```python
import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

def register_and_verify_domain(domain_name: str):
    # Create Domain
    domain = resend.Domains.create({"name": domain_name, "region": "us-east-1"})
    domain_id = domain["id"]
    print(f"Domain Created ({domain_id}). DNS Records:")
    for rec in domain.get("records", []):
        print(f" - [{rec['record']}] {rec['name']} -> {rec['value']}")

    # Verify Domain
    verify_res = resend.Domains.verify(domain_id=domain_id)
    print(f"Verification Triggered. Status: {verify_res.get('status')}")
```

### 2.6 Contacts Management (Python)
```python
import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

def create_and_unsubscribe_contact(audience_id: str, email: str):
    # Add contact
    contact = resend.Contacts.create({
        "audience_id": audience_id,
        "email": email,
        "first_name": "Jane",
        "last_name": "Doe",
        "unsubscribed": False,
    })
    contact_id = contact["id"]
    print(f"Contact Created ID: {contact_id}")

    # Mark unsubscribed
    updated = resend.Contacts.update({
        "audience_id": audience_id,
        "id": contact_id,
        "unsubscribed": True,
    })
    print(f"Contact Updated. Unsubscribed: {updated.get('unsubscribed')}")
```

---

## 3. SDK Comparison Matrix

| Feature | Node.js (`@resend/node`) | Python (`resend`) |
|---------|-------------------------|------------------|
| Import Style | `import { Resend } from 'resend';` | `import resend` |
| Auth Config | `const resend = new Resend(apiKey);` | `resend.api_key = "re_..."` |
| Return Pattern | Tuple `{ data, error }` | Dictionary or raises Exception |
| TypeScript Types | Native export (`CreateEmailOptions`, etc.) | Type hints in PyPI package |
| Async Support | Native Promises / async-await | Synchronous + Async client helpers |

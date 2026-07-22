# HTML Email Templates & React Email Guide

Best practices for designing, building, inline-styling, and rendering HTML email layouts and React Email components for Resend API delivery.

---

## 1. HTML Email Architecture & Best Practices

Email client rendering engines (Outlook, Gmail, Apple Mail, Yahoo) have fragmented CSS support. Adhere to these fundamental rules when drafting raw HTML email strings for Resend:

### Core Rules
1. **Layout Strategy:** Use `<table>` structures instead of `<div>` flexbox/grid for robust multi-client layout compatibility.
2. **Inline Styling:** All CSS styles MUST be inlined directly onto element `style="..."` attributes.
3. **Fonts & Fallbacks:** Rely on universal web-safe font stacks: `font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;`.
4. **Widths & Max-Widths:** Set fixed container widths (e.g. `width="600" style="max-width: 600px;"`) centered with `margin: 0 auto;`.
5. **Plain Text Fallback:** ALWAYS provide a plain text `text` string alongside your `html` payload to maximize deliverability and accessibility scores.

---

## 2. Production HTML Email Template Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to Acme</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f5f7; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
  <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f5f7; padding: 20px 0;">
    <tr>
      <td align="center">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
          <!-- Header -->
          <tr>
            <td style="background-color: #000000; padding: 24px; text-align: center;">
              <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 700;">Acme Corp</h1>
            </td>
          </tr>
          <!-- Body Content -->
          <tr>
            <td style="padding: 32px; color: #333333; line-height: 1.6; font-size: 16px;">
              <h2 style="color: #111111; font-size: 20px; margin-top: 0;">Welcome, {{FIRST_NAME}}!</h2>
              <p>Thank you for signing up for Acme. We are thrilled to have you join our developer platform.</p>
              <p>Click the button below to complete your email verification:</p>
              <!-- CTA Button -->
              <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="margin: 28px 0;">
                <tr>
                  <td align="center" style="background-color: #0066cc; border-radius: 6px;">
                    <a href="{{VERIFICATION_URL}}" target="_blank" style="display: inline-block; padding: 12px 24px; color: #ffffff; text-decoration: none; font-weight: 600; border-radius: 6px;">Verify Email Address</a>
                  </td>
                </tr>
              </table>
              <p style="font-size: 14px; color: #666666;">If you didn't create an account, you can safely ignore this message.</p>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb; font-size: 12px; color: #9ca3af;">
              <p style="margin: 0;">© 2026 Acme Inc. 123 Innovation Way, San Francisco, CA 94105</p>
              <p style="margin: 4px 0 0 0;"><a href="{{UNSUBSCRIBE_URL}}" style="color: #6b7280; text-decoration: underline;">Unsubscribe</a></p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

---

## 3. React Email Integration (`@react-email/components`)

Resend was created by the team behind [React Email](https://react.email/). You can render React components directly to clean HTML strings for Resend dispatch.

### 3.1 Component Definition (`WelcomeEmail.tsx`)
```tsx
import React from 'react';
import {
  Html,
  Head,
  Body,
  Container,
  Heading,
  Text,
  Button,
  Section,
  Hr,
} from '@react-email/components';

interface WelcomeEmailProps {
  firstName: string;
  actionUrl: string;
}

export const WelcomeEmail = ({ firstName, actionUrl }: WelcomeEmailProps) => (
  <Html lang="en">
    <Head />
    <Body style={{ backgroundColor: '#f4f5f7', fontFamily: 'sans-serif' }}>
      <Container style={{ backgroundColor: '#ffffff', padding: '32px', borderRadius: '8px' }}>
        <Heading style={{ color: '#111827', fontSize: '24px' }}>Welcome, {firstName}!</Heading>
        <Text style={{ color: '#374151', fontSize: '16px', lineHeight: '1.5' }}>
          Welcome to the platform. Click below to activate your account.
        </Text>
        <Section style={{ textAlign: 'center', margin: '24px 0' }}>
          <Button
            href={actionUrl}
            style={{
              backgroundColor: '#2563eb',
              color: '#ffffff',
              padding: '12px 24px',
              borderRadius: '6px',
              textDecoration: 'none',
              fontWeight: 'bold',
            }}
          >
            Activate Account
          </Button>
        </Section>
        <Hr style={{ borderColor: '#e5e7eb' }} />
        <Text style={{ color: '#9ca3af', fontSize: '12px' }}>
          © 2026 Acme Inc. All rights reserved.
        </Text>
      </Container>
    </Body>
  </Html>
);

export default WelcomeEmail;
```

### 3.2 Dispatching React Email with Resend SDK
```typescript
import { Resend } from 'resend';
import { renderAsync } from '@react-email/render';
import { WelcomeEmail } from './WelcomeEmail';

const resend = new Resend(process.env.RESEND_API_KEY);

async function sendReactEmail(userEmail: string, name: string, token: string) {
  // Option A: Pass component directly to resend.emails.send ({ react: <WelcomeEmail ... /> })
  // Option B: Explicitly render to html string with renderAsync
  const html = await renderAsync(
    WelcomeEmail({ firstName: name, actionUrl: `https://example.com/verify?token=${token}` })
  );

  const { data, error } = await resend.emails.send({
    from: 'Acme <onboarding@resend.dev>',
    to: [userEmail],
    subject: `Welcome to Acme, ${name}!`,
    html,
    text: `Welcome, ${name}! Activate your account here: https://example.com/verify?token=${token}`,
  });

  if (error) throw error;
  return data.id;
}
```

---

## 4. Attachments & Inline Images

### 4.1 Base64 Attachment Encoding
Attachments are passed as array objects containing `content` (base64 string) and `filename`.

```javascript
import fs from 'fs';

const pdfBuffer = fs.readFileSync('./invoice_1092.pdf');
const base64Pdf = pdfBuffer.toString('base64');

await resend.emails.send({
  from: 'Billing <billing@yourdomain.com>',
  to: ['client@example.com'],
  subject: 'Invoice #1092',
  html: '<p>Please find your attached invoice.</p>',
  attachments: [
    {
      filename: 'invoice_1092.pdf',
      content: base64Pdf,
      content_type: 'application/pdf',
    },
  ],
});
```

### 4.2 Dynamic Variables Substitution Strategy
When working with stored HTML strings in Node/Python, use standard template string replacements or regex substitution:

```python
def fill_template(template_str: str, context: dict) -> str:
    rendered = template_str
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered
```

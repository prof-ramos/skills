> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#signer)

# Signer

## Índice

- [Signer Object](#signer-object)
  - [Base Signer Fields](#base-signer-fields)
  - [Additional Fields In `GET /signers/self`](#additional-fields-in-get-signersself)
- [Create](#create)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [List](#list)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Get](#get)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Update](#update)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Delete](#delete)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Get Self](#get-self)
  - [Body Parameters](#body-parameters)
- [Accept Terms](#accept-terms)
  - [Body Parameters](#body-parameters)
- [Verify Email](#verify-email)
  - [Header Parameters](#header-parameters)
  - [Body Parameters](#body-parameters)
- [Confirm Signer Data](#confirm-signer-data)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
  - [Error Responses](#error-responses)
- [Upload Signature](#upload-signature)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Download Signature](#download-signature)
  - [URL Parameters](#url-parameters)

---



## Signer Object

The signer endpoints return a base signer object, plus a few signer-session fields in signer-facing flows.

### Base Signer Fields

These fields are returned by the account-scoped signer endpoints such as:

- `GET /accounts/{account_id}/signers`
- `GET /accounts/{account_id}/signers/{signer_id}`
- `POST /accounts/{account_id}/signers`
- `PUT /accounts/{account_id}/signers/{signer_id}`

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `signer`. |
| `id` | string | Signer custom ID. |
| `full_name` | string | Signer's full name. |
| `email` | string|null | Signer's email address. Used for email-based verification and notifications when configured. |
| `whatsapp_phone_number` | string|null | Signer's WhatsApp phone number in E.164 format (for example, `+5548999990000`). Used for WhatsApp-based verification and notifications when configured. |
| `has_accepted_terms` | boolean | Indicates whether the signer has accepted the terms of use. |

### Additional Fields In `GET /signers/self`

The signer self endpoint returns the base signer fields above and also includes:

| Field | Type | Description |
| --- | --- | --- |
| `has_signature` | boolean | Indicates whether the signer already has an uploaded signature image stored for reuse. |
| `has_initial` | boolean | Indicates whether the signer already has an uploaded initials image stored for reuse. |

## Create

> Request

```
curl "https://api.assinafy.com.br/v1/accounts/e2d6ee35c7741ca4006b9e1a/signers" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -H 'Content-Type: application/json' \
  -d '
{
  "full_name": "John Dove",
  "email": "[email protected]",
  "whatsapp_phone_number": "+5548999990000"
}
'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "signer",
    "id": "62d6ee35c7741ca4006b9e11",
    "full_name": "John Signer",
    "email": "[email protected]",
    "whatsapp_phone_number": "+5548999990000",
    "has_accepted_terms": false
  }
}
```

`POST /accounts/{account_id}/signers`

Create a signer.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| full\_name | true | Signer full name. |
| email | false | Signer Email. |
| whatsapp\_phone\_number | false | Signer's WhatsApp phone number. Format: E.164 (e.g., +5548999990000). Numbers are automatically normalized to E.164 format on save. |

## List

> Request

```
curl "https://api.assinafy.com.br/v1/accounts/60f720577e30d2047d4f385f/signers" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "id": "60f720577e30d2047d4f385f",
      "full_name": "Joan Signer",
      "email": "[email protected]",
      "whatsapp_phone_number": "+5548999990000",
      "has_accepted_terms": false
    },
    {
      "id": "60f72057b865123687d56c3c",
      "full_name": "Mary Signer",
      "email": "[email protected]",
      "whatsapp_phone_number": null,
      "has_accepted_terms": true
    }
  ]
}
```

`GET /accounts/{account_id}/signers`

List signers of the workspace.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | The account ID. |
| search | false | Search term to filter by full\_name or email. |

## Get

> Request

```
curl -X GET "https://api.assinafy.com.br/v1/accounts/35c7741ca4006b9e11/signers/62d6ee35c7741ca4006b9e11" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "signer",
    "id": "62d6ee35c7741ca4006b9e11",
    "full_name": "John Signer",
    "email": "[email protected]",
    "whatsapp_phone_number": "+5548999990000",
    "has_accepted_terms": false
  }
}
```

`GET /accounts/{account_id}/signers/{signer_id}`

Retrieve a signer's information.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |
| signer\_id | true | The signer ID. |

## Update

> Request

```
curl -X PUT "https://api.assinafy.com.br/v1/accounts/35c7741ca4006b9e11/signers/62d6ee35c7741ca4006b9e11" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '
{
  "full_name": "John Dove",
  "email": "[email protected]",
  "whatsapp_phone_number": "+5548999990000"
}
'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "signer",
    "id": "62d6ee35c7741ca4006b9e11",
    "full_name": "John Signer",
    "email": "[email protected]",
    "whatsapp_phone_number": "+5548999990000",
    "has_accepted_terms": false
  }
}
```

`PUT /accounts/{account_id}/signers/{signer_id}`

Update signer's account information.

**Verification integrity rules:**

- `email` cannot be updated if the signer has already verified an email-based
  access code on at least one document that has not yet been certificated
  (i.e. the document is still in-flight: uploading, processing, pending
  signature, or currently being certificated). The response will be `400 Bad Request` with a message naming the offending document(s). To proceed, the
  affected document(s) must first be cancelled, rejected, allowed to expire,
  or fully certificated.
- `whatsapp_phone_number` follows the same rule for WhatsApp-based access
  codes.
- Documents already in `certificated` state do **not** block the update: the
  certificate PDF has already been rendered with the signer data in effect at
  the time of signing, and subsequent updates cannot retroactively alter that
  issued certificate.
- `full_name` can always be updated.
- When `email` or `whatsapp_phone_number` is updated while the signer has
  *unverified* in-flight documents that use the corresponding verification
  method, the access code and verification code on those unverified requests
  are rotated so the previously delivered link and OTP become invalid. The new
  tokens are not automatically re-sent — use the resend endpoint to deliver
  them to the updated address or number.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | The account ID. |
| signer\_id | true | The signer ID. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| full\_name | false | Signer full name. |
| email | false | Signer Email. |
| whatsapp\_phone\_number | false | Signer's WhatsApp phone number. Format: E.164 (e.g., +5548999990000). Numbers are automatically normalized to E.164 format on save. |

## Delete

> Request

```
curl -X DELETE "https://api.assinafy.com.br/v1/accounts/5c7741ca4006b9e1/signers/62d6ee35c7741ca4006b9e11" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": []
}
```

`DELETE /accounts/{account_id}/signers/{signer_id}`

Delete a signer.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | The account ID. |
| signer\_id | true | The signer ID. |

## Get Self

> Request

```
curl -X GET 'https://api.assinafy.com.br/v1/signers/self?signer-access-code=9uAWyOXx9hgzCKdCuahkinwvg8tWJ2RC'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "signer",
    "id": "uahkinwvg8tWJ2RC",
    "full_name": "Signer Name",
    "email": "[email protected]",
    "whatsapp_phone_number": "+5548999990000",
    "has_accepted_terms": false,
    "has_signature": false,
    "has_initial": false
  }
}
```

`GET /signers/self`

Allows a signer to obtain his/her own information.

**Headers**:

- `Content-Type` - `application/json`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signer-access-code` | true | Signer access code. |

## Accept Terms

> Request

```
curl -X PUT 'https://api.assinafy.com.br/v1/signers/accept-terms' -d '
{
  "signer-access-code": "9uAWyOXx9hgzCKdCuahkinwvg8tWJ2RC-n6hhxyLS1QfMhqWSw-PnwQlSs2oPNea"
}
'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "full_name": "Signer Name",
    "email": "[email protected]",
    "has_accepted_terms": true
  }
}
```

`PUT /signers/accept-terms`

This endpoint allows a signer to accept terms of use.

**Alternative:** Terms can also be accepted via the [Confirm Signer Data](#confirm-signer-data) endpoint by including `has_accepted_terms: true` in the request body. This allows confirming data and accepting terms in a single API call.

**Headers**:

- `Content-Type` - `application/json`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signer-access-code` | true | Signer access code. |

## Verify Email

> Request

```
curl -XPOST 'https://api.assinafy.com.br/v1/verify' -d '
{
  "verification-code": "123456",
  "signer-access-code": "9uAWyOXx9hgzCKdCuahkinwvg8tWJ2RC-n6hhxyLS1QfMhqWSw-PnwQlSs2oPNea"
}
'
```

> 200 OK

```
{
  "message": "Code verified successfully"
}
```

`POST /verify`

Verify the signer email that received a link to access a document.

### Header Parameters

- `Content-Type` - `application/json`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signer-access-code` | true | Signer access code. |
| `verification-code` | true | Verification code. |

## Confirm Signer Data

> Request

```
curl -X PUT 'https://api.assinafy.com.br/v1/documents/c57d51eaad68a7/signers/confirm-data?signer-access-code=9uAWyOXx9hgzCKdCuahkinwvg8tWJ2RC-n6hhxyLS1QfMhqWSw-PnwQlSs2oPNea' \
-H 'Content-Type: application/json' \
-d '
{
  "email": "[email protected]",
  "whatsapp_phone_number": "+5548999990000",
  "has_accepted_terms": true
}
'
```

> 200 OK

```
{}
```

`PUT /documents/{documentId}/signers/confirm-data`

Confirm signer data for virtual assignments. Signers must confirm their data before they can sign the document.

**Important:**

- Which fields are required depends on the signer's **verification method** and **notification methods**:
  - `email` is required when the signer uses **email verification** or **email notification**.
  - `whatsapp_phone_number` is required when the signer uses **WhatsApp verification** or **WhatsApp notification**.
  - If the signer uses both channels (e.g., email verification with WhatsApp notification), both fields are required.
- **Email validation:**
  - If the signer already has an email, the provided email **must match** the existing email exactly.
  - If the signer doesn't have an email, the provided email will be saved to the signer's record.
- **WhatsApp phone number validation:**
  - Phone numbers are normalized to E.164 format before comparison (e.g., `5548999990000` and `+5548999990000` are treated as equivalent).
  - If the signer already has a WhatsApp phone number, the provided phone number **must match** the existing phone number after normalization.
  - If the signer doesn't have a phone number, the provided phone number will be saved to the signer's record in E.164 format.
- Terms acceptance can be done in this same request by setting `has_accepted_terms` to `true`, allowing you to confirm data and accept terms in a single API call.

### Header Parameters

- `Content-Type` - `application/json`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `documentId` | true | Document custom ID. |
| `signer-access-code` | true | Signer access code. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `email` | conditional | Signer's email address. **Required** when signer uses email verification or email notification. Must match the existing email if already set, or will be saved if not set. Must be a valid email format. |
| `whatsapp_phone_number` | conditional | Signer's WhatsApp phone number. **Required** when signer uses WhatsApp verification or WhatsApp notification. Must match the existing phone number if already set, or will be saved if not set. Format: E.164 (e.g., +5548999990000). |
| `has_accepted_terms` | false | Set to `true` to accept terms of use. This allows accepting terms and confirming data in a single request. |

### Error Responses

**400 Bad Request** - If email is missing:

```
{
  "name": "Bad Request",
  "message": "Email is required.",
  "code": 0,
  "status": 400
}
```

**400 Bad Request** - If email is empty:

```
{
  "name": "Bad Request",
  "message": "Email cannot be empty.",
  "code": 0,
  "status": 400
}
```

**400 Bad Request** - If email format is invalid:

```
{
  "name": "Bad Request",
  "message": "Invalid email.",
  "code": 0,
  "status": 400
}
```

**400 Bad Request** - If email doesn't match existing email:

```
{
  "name": "Bad Request",
  "message": "The provided email does not match the signer's email.",
  "code": 0,
  "status": 400
}
```

**400 Bad Request** - If WhatsApp phone number is missing:

```
{
  "name": "Bad Request",
  "message": "WhatsApp phone number is required.",
  "code": 0,
  "status": 400
}
```

**400 Bad Request** - If WhatsApp phone number is empty:

```
{
  "name": "Bad Request",
  "message": "WhatsApp phone number cannot be empty.",
  "code": 0,
  "status": 400
}
```

**400 Bad Request** - If WhatsApp phone number doesn't match existing phone number:

```
{
  "name": "Bad Request",
  "message": "The provided phone number does not match the signer's phone number.",
  "code": 0,
  "status": 400
}
```

**400 Bad Request** - If attempting to sign without confirming data first:

```
{
  "name": "Bad Request",
  "message": "Signer data must be confirmed before signing.",
  "code": 0,
  "status": 400
}
```

## Upload Signature

> Request

```
curl 'https://api.assinafy.com.br/v1/signature?signer-access-code=9uAWyOXx9hgzCKdCuea&type=signature' \
-H 'Content-Type: image/png' \
-d '{<Binary Here>}'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": []
}
```

`POST /signature?signer-access-code={signer_access_code}&type={type}`

Upload the signer's signature or intial image.

### Header Parameters

- `Content-Type` - `image/{png|jpeg}`

### URL Parameters

| Parameter | Default | Required | Description |
| --- | --- | --- | --- |
| signer-access-code |  | true | The signer access code. |
| type | *signature* |  | Should be *signature* or *initial*. |

## Download Signature

> Request

```
curl 'https://api.assinafy.com.br/v1/signature/signature?signer-access-code=9uAWyOXx9hgzCKdCuea
```

> 200 OK

```
Content-Type: image/png

[PNG binary]
```

`GET /signature/{type}?signer-access-code={signer_access_code}`

Download the signer's signature or initial image.

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| signer\_access\_code | true | The signer access code. |
| type | true | Should be *signature* or *initial*. |
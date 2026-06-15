> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#document)

# Document

## Índice

- [Document Objects](#document-objects)
  - [Document Object](#document-object)
  - [Document Page Object](#document-page-object)
  - [Document Status](#document-status)
- [Statuses](#statuses)
  - [Header Parameters](#header-parameters)
- [List](#list)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Document Status](#document-status)
- [Upload and Create](#upload-and-create)
  - [URL Parameters](#url-parameters)
  - [Limits](#limits)
- [Create from Template](#create-from-template)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Estimate Cost from Template](#estimate-cost-from-template)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
  - [Response Fields](#response-fields)
- [Get](#get)
  - [Header Parameters](#header-parameters)
- [Delete](#delete)
  - [Header Parameters](#header-parameters)
- [Download](#download)
  - [Header Parameters](#header-parameters)
  - [URL Paramenters](#url-paramenters)
- [Download Thumbnail](#download-thumbnail)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Download Page](#download-page)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Verify](#verify)
  - [URL Parameters](#url-parameters)
- [List Activities](#list-activities)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Response Fields](#response-fields)
  - [Event Payloads](#event-payloads)
- [Public: Get Basic Info](#public-get-basic-info)
  - [URL Parameters](#url-parameters)
- [Signer: Send Token](#signer-send-token)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Params](#body-params)
- [List Document Tags](#list-document-tags)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
- [Replace Document Tags](#replace-document-tags)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Append Document Tags](#append-document-tags)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Detach Tag From Document](#detach-tag-from-document)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)

---



This is the documents management service. The endpoints of this area allow us
to create, list, download and delete documents.

## Document Objects

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for document-related objects returned by the API.

### Document Object

Returned by document endpoints such as `GET /documents`, `GET /documents/{document_id}`, `POST /documents`, and `POST /accounts/{account_id}/templates/{template_id}/create-document`.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `document`. |
| `id` | string | Document ID. |
| `account_id` | string | Workspace ID that owns the document. |
| `template_id` | string|null | Template ID used to create the document, when applicable. |
| `name` | string | Document file name. |
| `status` | string | Document status code. |
| `artifacts` | object | Artifact download URLs keyed by artifact name, such as `original` or `certificated`. |
| `is_closed` | boolean | Indicates whether the document is in a closed terminal state. |
| `signing_url` | string | URL that opens the document signing flow. |
| `decline_reason` | string|null | Reason provided when the document was declined, when available. |
| `declined_by` | object|null | Signer object for the signer who declined the document, when available. |
| `tags` | array[object] | Tags attached to the document. Each entry has `id` and `name`. Always present, possibly empty. |
| `created_at` | string | Creation timestamp in ISO 8601 format. |
| `updated_at` | string | Last update timestamp in ISO 8601 format. |
| `assignment` | object|null | Expanded assignment data when included by the endpoint. |
| `pages` | array[object] | Expanded document pages when included by the endpoint. |

The `assignment` field uses the [Assignment Object](#assignment-objects) shape. The `pages` field uses the page shape below.

### Document Page Object

Returned inside `document.pages`.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Page ID. |
| `number` | integer | Page number, starting at `1`. |
| `height` | integer | Page height in pixels. |
| `width` | integer | Page width in pixels. |
| `download_url` | string | URL to download the rendered page image. |

### Document Status

A document will be in one of the following status:

| Status | Deletable | Description |
| --- | --- | --- |
| uploading | no | The document upload is in process. |
| uploaded | no | The document has been uploaded. |
| metadata\_processing | no | The initial processing is under way. |
| metadata\_ready | yes | The initial processing has been completed. |
| expired | yes | The signature deadline has been reached. |
| certificating | no | The document has been signed and is being certificated. |
| certificated | no | The document is certificated. |
| rejected\_by\_signer | yes | A signer declined signing the document. |
| pending\_signature | yes | The document is waiting for signatures. |
| rejected\_by\_user | yes | The signature process was cancelled by a user. |
| failed | yes | The document processing has failed. |

## Statuses

> Request

```
curl -X GET "https://api.assinafy.com.br/v1/documents/statuses" \
  -H "Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "code": "uploading",
      "deletable": false
    },
    {
      "code": "uploaded",
      "deletable": false
    },
    {
      "code": "metadata_processing",
      "deletable": false
    },
    {
      "code": "metadata_ready",
      "deletable": true
    },
    {
      "code": "certificating",
      "deletable": false
    }
  ]
}
```

`GET /documents/statuses`

Returns the list of supported document statuses and their properties (such as whether a document in that status can be deleted).

### Header Parameters

- `Authorization: Bearer {access_token}`

## List

> Request

```
curl "https://api.assinafy.com.br/v1/accounts/d199996981dbd199996981db/documents" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrghAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "id": "6981dbd199996981d",
      "account_id": "1a",
      "name": "my_document.pdf",
      "status": "metadata_ready",
      "assignment": {
        "id": "1",
        "sender_email": "[email protected]",
        "method": "virtual",
        "expires_at": null,
        "message": null,
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
        "items": [
          {
            "id": "dbd199996981d",
            "page": {
              "id": "dbd199996981d",
              "number": 1,
              "height": 1,
              "width": 1,
              "download_url": "https://api.assinafy.com.br/v1/documents/doc1/pages/1a/download"
            },
            "signer": {
              "id": "dbd199996981d",
              "full_name": "Signer Name",
              "email": "[email protected]",
              "has_accepted_terms": false
            },
            "field": {
              "id": "dbd199996981d",
              "name": "Assinatura",
              "type": "virtual",
              "regex": null,
              "is_pre_defined": false,
              "is_active": true,
              "is_required": true,
              "is_standard": false,
              "is_read_only": false,
              "is_visible": true
            },
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
              "id": "dbd199996981d",
              "full_name": "Signer 1",
              "email": "[email protected]",
              "has_accepted_terms": false,
              "completed": true
            },
            {
              "id": "dbd199996981d",
              "full_name": "Signer 2",
              "email": "[email protected]",
              "has_accepted_terms": false,
              "completed": false
            }
          ]
        }
      },
      "artifacts": {
        "original": "https://api.assinafy.com.br/v1/documents/doc1/download/original",
        "thumbnail": "https://api.assinafy.com.br/v1/documents/doc1/thumbnail"
      },
      "pages": [
        {
          "id": "dbd199996981d",
          "number": 1,
          "height": 1,
          "width": 1,
          "download_url": "https://api.assinafy.com.br/v1/documents/doc1/pages/1a/download"
        }
      ],
      "created_at": "2023-07-21T13:43:17Z",
      "updated_at": "2023-07-21T13:43:17Z",
      "is_closed": false,
      "decline_reason": null,
      "declined_by": null,
      "tags": [
        { "id": "fa8c09f3e709a8a1c82d69b1454", "name": "Contracts", "color": "#FF0000" }
      ]
    },
  ]
}
```

`GET /accounts/{account_id}/documents`

This endpoint will list documents of the workspace.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | ID of the workspace account. |
| status | false | Status filter. Ex.: `?status=pending_signature`. |
| method | false | Signature method filter. Ex.: `?method=virtual`. Possible values: `virtual` or `collect`. |
| search | false | Search term that will be used for partial matching on the following attributes: `document.name`, `signer.full_name` and `signer.email`. |
| tags | false | Comma-separated list of tag IDs. Returns only documents that have **all** the listed tags (AND semantics). Unknown tag IDs yield an empty result. Example: `?tags=tagId1,tagId2`. |
| sort | false | Allows sorting by: `name` and `updated_at`. |

### Document Status

These are the possible document status:

| Status | Deletable | Description |
| --- | --- | --- |
| uploading | no | The document upload is in process. |
| uploaded | no | The document has been uploaded. |
| metadata\_processing | no | The initial processing is under way. |
| metadata\_ready | yes | The initial processing has been completed. |
| expired | yes | The signature deadline has been reached. |
| certificating | no | The document has been signed and is being certificated. |
| certificated | no | The document is certificated. |
| rejected\_by\_signer | yes | A signer declined signing the document. |
| pending\_signature | yes | The document is waiting for signatures. |
| rejected\_by\_user | yes | The signature process was cancelled by a user. |
| failed | yes | The document processing has failed. |

## Upload and Create

> Request

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/documents" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'\
  -F 'file=@/tmp/document.pdf'
```

> 200 OK

```
{
  "id": "615601fab04c0a3147bb1246",
  "name": "document.pdf",
  "status": "uploaded",
  "assignment": null,
  "artifacts": {
    "original": "https://api.assinafy.com.br/v1/documents/615601fab04c0a3147bb1246/download/original"
  },
  "pages": [
    {
      "id": "615601faf166d6d1d8e7dc30",
      "number": 1,
      "height": 2100,
      "width": 1275,
      "download_url": "https://api.assinafy.com.br/v1/documents/615601fab04c0a3147bb1246/pages/615601faf166d6d1d8e7dc30/download"
    }
  ],
  "created_at": 1633026554,
  "updated_at": 1633026554,
  "is_closed": false
}
```

`POST /accounts/{account_id}/documents`

Create a document from an uploaded file.

**Headers**:

- `Content-Type` - `multipart/form-data`
- `Authorization` - `Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The ID of the workspace. |

### Limits

- **Maximum file size**: 25MB
- **Maximum pages**: 2000

## Create from Template

> Request

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/35c7741ca4006b9e11/templates/60f720572d7fecf7c16c8463/documents" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '
    {
      "name": "sample-contract-one-page.pdf",
      "message": "Message to the signers",
      "editor_fields": [
        {
          "field_id": "fa8c14f3af99d2846d1789de4ba",
          "value": "Field value"
        }
      ],
      "signers": [
        {
          "role_id": "fa8c14f32d732271e071998246e",
          "id": "fa8c140cb49b79f940aab95fddd"
        },
        {
          "role_id": "fa8c14f3964a362e3230f2283d1",
          "id": "fa8c140cbce705c1a080346cb39"
        }
      ],
      "expires_at": "2024-07-30T23:59:00Z"
    }
'
```

> Request (with explicit verification and notification methods)

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/35c7741ca4006b9e11/templates/60f720572d7fecf7c16c8463/documents" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '
    {
      "name": "sample-contract-one-page.pdf",
      "message": "Message to the signers",
      "signers": [
        {
          "role_id": "fa8c14f32d732271e071998246e",
          "id": "fa8c140cb49b79f940aab95fddd",
          "verification_method": "Email",
          "notification_methods": ["Email"],
          "step": 1
        },
        {
          "role_id": "fa8c14f3964a362e3230f2283d1",
          "id": "fa8c140cbce705c1a080346cb39",
          "verification_method": "Whatsapp",
          "notification_methods": ["Whatsapp"],
          "step": 2
        }
      ],
      "expires_at": "2024-07-30T23:59:00Z"
    }
'
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": {
        "resource": "document",
        "id": "fa8c140c614c928f7e7efa086b2",
        "account_id": "1a",
        "template_id": "fa8c140b5ee344f8e48236ed284",
        "name": "sample-contract-one-page.pdf",
        "status": "uploaded",
        "assignment": {
            "id": "fa8c140ccd5781b079738d19e95",
            "sender_email": "[email protected]",
            "method": "virtual",
            "expires_at": "2024-07-30T23:59:00Z",
            "message": "669fc6accda22",
            "signers": [
                {
                    "id": "fa8c140cb49b79f940aab95fddd",
                    "full_name": "Suzana Stephany Cordeiro",
                    "email": "[email protected]",
                    "has_accepted_terms": false
                }
            ],
            "copy_receivers": [
                {
                    "id": "fa8c140cbce705c1a080346cb39",
                    "full_name": "Eric Flores Filho",
                    "email": "[email protected]",
                    "has_accepted_terms": false
                }
            ],
            "items": [
                {
                    "id": "fa8c140cd99a0b9dcb40e7ef29e",
                    "page": null,
                    "signer": {
                        "id": "fa8c140cb49b79f940aab95fddd",
                        "full_name": "Suzana Stephany Cordeiro",
                        "email": "[email protected]",
                        "has_accepted_terms": false
                    },
                    "field": {
                        "id": "field1",
                        "name": "signature",
                        "type": "virtual",
                        "regex": null,
                        "is_pre_defined": false,
                        "is_active": true,
                        "is_required": true,
                        "is_standard": false,
                        "is_read_only": false,
                        "is_visible": true
                    },
                    "display_settings": [],
                    "value": null,
                    "completed": false
                }
            ],
            "summary": {
                "signer_count": 1,
                "completed_count": 0,
                "signers": [
                    {
                        "id": "fa8c140cb49b79f940aab95fddd",
                        "full_name": "Suzana Stephany Cordeiro",
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
            "original": "https://api.assinafy.com.br/v1/v1/documents/fa8c140c614c928f7e7efa086b2/download/original",
            "thumbnail": "https://api.assinafy.com.br/v1/v1/documents/fa8c140c614c928f7e7efa086b2/thumbnail"
        },
        "pages": [
            {
                "id": "fa8c140c9617a07be842995d4a1",
                "number": 1,
                "height": 2100,
                "width": 1275,
                "download_url": "https://api.assinafy.com.br/v1/v1/documents/fa8c140c614c928f7e7efa086b2/pages/fa8c140c9617a07be842995d4a1/download"
            }
        ],
        "created_at": "2024-07-23T15:05:17Z",
        "updated_at": "2024-07-23T15:05:17Z",
        "is_closed": false,
        "decline_reason": null,
        "declined_by": null,
        "tags": [
            { "id": "ab12cd34ef56gh78ij90kl12mn3", "name": "Onboarding" },
            { "id": "fa8c09f3e709a8a1c82d69b1454", "name": "Q2-Renewal" }
        ]
    }
}
```

`POST /accounts/{account_id}/templates/{template_id}/documents`

Create a document from a template.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |
| template\_id | True | The template ID. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signers[]` | true | A list of signers for the document. One entry per template role. |
| `signers[].role_id` | true | The template role ID associated with the signer. |
| `signers[].id` | true | The signer ID. The signer must already exist in the account and is used directly for the selected role. |
| `signers[].verification_method` | false | The verification method for this signer. If provided without `notification_methods`, the notification method is inferred. Defaults to `Email`. Only applies to signers (not copy receivers). See [Verification and Notification Methods](#verification-and-notification-methods). |
| `signers[].notification_methods[]` | false | List of notification method codes for this signer. If provided without `verification_method`, the verification method is inferred. Defaults to `Email`. Only one method allowed per signer. See [Verification and Notification Methods](#verification-and-notification-methods). |
| `signers[].step` | false | Positive integer that controls signing order. Signers sharing the same step number sign in parallel; a step is activated only after every signer in the previous step has signed. If supplied for any signer role, it must be supplied for every signer role, and the values must form a contiguous sequence starting at `1`. Copy receivers ignore this field. |
| `editor_fields[]` | false | A list of editor fields and values. |
| `editor_fields[].field_id` | true | The unique identifier of a field, matching the `field_id` provided in the template data. |
| `editor_fields[].value` | true | The value to assign to the corresponding field. |
| `name` | false | The title or name for the document being created. The default is the template name. |
| `message` | false | An optional message to be sent to signers. |
| `expires_at` | false | The expiration date for the assignment in **ISO 8601** format. By default, there is no expiration. |
| `tags[]` | false | List of tag names to attach to the new document. Names that don't exist yet are auto-created. Tags configured on the template as default-document-tags are always applied; values supplied here are merged on top (duplicates are removed). |

## Estimate Cost from Template

> Request (Email notification — default, role\_id only)

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/35c7741ca4006b9e11/templates/60f720572d7fecf7c16c8463/documents/estimate-cost" \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '
    {
      "signers": [
        {
          "role_id": "fa8c14f32d732271e071998246e"
        }
      ]
    }
  '
```

> Request (Whatsapp notification — inferred from verification\_method)

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/35c7741ca4006b9e11/templates/60f720572d7fecf7c16c8463/documents/estimate-cost" \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '
    {
      "signers": [
        {
          "role_id": "fa8c14f32d732271e071998246e",
          "verification_method": "Whatsapp"
        }
      ]
    }
  '
```

> Request (Whatsapp — explicit notification\_method only)

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/35c7741ca4006b9e11/templates/60f720572d7fecf7c16c8463/documents/estimate-cost" \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '
    {
      "signers": [
        {
          "role_id": "fa8c14f32d732271e071998246e",
          "notification_methods": ["Whatsapp"]
        }
      ]
    }
  '
```

> 200 OK (Email notification — 0 credits for notifications)

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
    "has_sufficient_resources": true,
    "blocking_reason": null,
    "message": null
  }
}
```

> 200 OK (Whatsapp notification — 0.45 credits each)

```
{
  "status": 200,
  "message": "",
  "data": {
    "documents": 1,
    "credits": 0.45,
    "needs_extra_document": false,
    "extra_document_cost": 0,
    "total_credits": 0.45,
    "breakdown": [
      {
        "code": "NotificationWhatsapp",
        "name": "Whatsapp Notification",
        "cost": 0.45,
        "quantity": 1,
        "unit_cost": 0.45
      }
    ],
    "document_balance": 100,
    "credit_balance": 50,
    "has_sufficient_resources": true,
    "blocking_reason": null,
    "message": null
  }
}
```

> 200 OK (Pending subscription payment — balances preserved, usage blocked)

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

`POST /accounts/{account_id}/templates/{template_id}/documents/estimate-cost`

Estimates the cost of creating a document from a template without actually creating it. Contact information is **not required** — only the `role_id` and optionally the verification or notification method are needed for cost calculation. The signer list is validated against the template roles.

Each document created from a template always consumes **1 document** from the plan's monthly document allowance. If the plan documents are exhausted, the `ExtraDocument` cost will be charged from credits instead (`needs_extra_document` will be `true`).

The cost breakdown includes notification costs only (items with cost > 0):

- **Email**: 0 credits (not shown in breakdown)
- **Whatsapp**: 0.45 credits per signer

Use this endpoint to check if the account has sufficient resources before creating a document from a template.

Possible blocking reasons currently returned by this endpoint:

- `PendingPayment`
- `InsufficientDocuments`
- `InsufficientCredits`

If the current subscription is pending payment, the endpoint still returns the real `document_balance` and `credit_balance`, but `has_sufficient_resources` is `false` and `blocking_reason` is `PendingPayment`.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |
| template\_id | True | The template ID. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signers[]` | true | A list of signers. One entry per template role (editor roles are ignored for cost calculation). |
| `signers[].role_id` | true | The template role ID associated with the signer. |
| `signers[].id` | false | The signer ID. Accepted for payload compatibility with Create from Template, but not required for cost estimation. |
| `signers[].verification_method` | false | Verification method for this signer. If provided without `notification_methods`, the notification method is inferred. Defaults to `Email`. See [Verification and Notification Methods](#verification-and-notification-methods). |
| `signers[].notification_methods[]` | false | Notification methods for this signer. If provided without `verification_method`, the verification method is inferred. Defaults to `Email`. See [Verification and Notification Methods](#verification-and-notification-methods). |
| `signers[].step` | false | Accepted for payload compatibility with Create from Template, but ignored for cost estimation. |
| `name` | false | Ignored. Included for payload compatibility with Create from Template. |
| `message` | false | Ignored. Included for payload compatibility with Create from Template. |
| `editor_fields[]` | false | Ignored. Included for payload compatibility with Create from Template. |
| `expires_at` | false | Ignored. Included for payload compatibility with Create from Template. |

### Response Fields

| Field | Type | Description |
| --- | --- | --- |
| documents | number | Number of documents this operation will consume (always 1). |
| credits | number | Total notification credits needed. |
| needs\_extra\_document | boolean | Whether the plan document allowance is exhausted and an extra document must be purchased from credits. |
| extra\_document\_cost | number | Cost in credits for the extra document (0 if plan documents are available). |
| total\_credits | number | Total credits needed (notification credits + extra document cost if applicable). |
| breakdown | array | Itemized list of notification costs (only items with cost > 0). |
| breakdown[].code | string | Cost type code (e.g., `NotificationWhatsapp`). |
| breakdown[].name | string | Human-readable cost type name. |
| breakdown[].cost | number | Total cost in credits for this item (unit\_cost × quantity). |
| breakdown[].quantity | number | Number of notifications. |
| breakdown[].unit\_cost | number | Cost per notification. |
| document\_balance | number | Current account document balance. |
| credit\_balance | number | Current account credit balance. |
| has\_sufficient\_resources | boolean | Whether the account has enough documents and credits for this operation. |
| blocking\_reason | string | Block reason when the operation cannot proceed. Currently `PendingPayment`, `InsufficientDocuments`, or `InsufficientCredits` may be returned. Otherwise `null`. |
| message | string | Explanation for the current block state. For example, pending-payment estimates instruct the user to complete payment, while resource-related estimates explain whether documents or credits are missing. Otherwise `null`. |

## Get

> Request

```
curl "https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463" \
-H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "document",
    "id": "1016d5795af62e28c2161efcb7a6",
    "account_id": "d199996981dbd199996981db",
    "name": "3.pdf",
    "status": "rejected_by_signer",
    "assignment": {
      "id": "1016d5a650dcb1e056eddd367bbd",
      "sender_email": "[email protected]",
      "expiration": "2038-01-01",
      "signers": [
        {
          "id": "customid1",
          "full_name": "Signer 1",
          "email": "[email protected]",
          "verification_method": "Whatsapp",
          "notification_methods": ["Whatsapp"],
          "completed": true,
          "notification_history": [
            {
              "event": "signature_request",
              "status": "sent",
              "error_code": null,
              "error_message": null,
              "sent_at": "2026-05-04T15:00:00Z",
              "failed_at": null
            }
          ]
        },
        {
          "id": "customid2",
          "full_name": "Signer 2",
          "email": "[email protected]",
          "verification_method": "Email",
          "notification_methods": ["Email"],
          "completed": false,
          "notification_history": []
        }
      ],
      "method": "virtual",
      "items": [],
      "summary": {
        "signer_count": 0,
        "completed_count": 0,
        "signers": []
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
    "download_url": "https://api.assinafy.com.br/v1/documents/3/download",
    "download_final_url": null,
    "pages": [],
    "is_closed": true,
    "signing_url": "http://app.assinafy.test/sign/doc1",
    "tags": [
      { "id": "fa8c09f3e709a8a1c82d69b1454", "name": "Contracts", "color": "#FF0000" }
    ],
    "created_at": "2022-07-19 18:14:29",
    "updated_at": "2022-07-19 18:14:29"
  }
}
```

> 200 OK | Document declined by a signer

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "document",
    "id": "1016d5795af62e28c2161efcb7a6",
    "name": "2.pdf",
    "status": "rejected_by_signer",
    "assignment": {
      "id": "1016d5a650dcb1e056eddd367bbd",
      "sender_email": "[email protected]",
      "expiration": "2038-01-01",
      "signers": [
        {
          "id": "customid1",
          "full_name": "Signer 1",
          "email": "[email protected]",
          "verification_method": "Whatsapp",
          "notification_methods": ["Whatsapp"],
          "completed": true,
          "notification_history": [
            {
              "event": "document_declined",
              "status": "sent",
              "error_code": null,
              "error_message": null,
              "sent_at": "2026-05-04T15:00:00Z",
              "failed_at": null
            }
          ]
        },
        {
          "id": "customid2",
          "full_name": "Signer 2",
          "email": "[email protected]",
          "verification_method": "Email",
          "notification_methods": ["Email"],
          "completed": false,
          "notification_history": []
        }
      ],
      "method": "virtual",
      "items": [],
      "summary": {
        "signer_count": 0,
        "completed_count": 0,
        "signers": []
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

    "pages": [],
    "created_at": "2022-07-19 17:53:37",
    "updated_at": "2022-07-19 17:53:37",
    "decline_reason": "I regretted.",
    "activities": [
      {
        "id": 1,
        "event": "signer_rejected_document",
        "message": "Signer 1 decline doc 2",
        "origin": "",
        "created_at": "2022-07-19 17:53:36"
      }
    ]
  }
}
```

`GET /documents/{document_id}`

Get the document data by its ID.

### Header Parameters

- `Authorization: Bearer {access_token}`

**Important:** The attribute *declined\_reason* in the result, is only available
when the the access token is from the user who created the document.

## Delete

> Request

```
curl -X DELETE "https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463" \
  -H "Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": []
}
```

`DELETE /documents/{documentId}`

Delete a document by its ID.

### Header Parameters

- `Authorization: Bearer {access_token}`

## Download

> Request

```
curl "https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/download/original" \
-H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
Content-Type: application/pdf

[PDF binary]
```

`GET /documents/{document_id}/download/{artifact_name}`

Download a document artifact.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Paramenters

| Name | Required | Description |
| --- | --- | --- |
| document\_id | True | The document ID. |
| artifact\_name | True | The type of artifact to download. |

**Artifact types**: original, certificated, certificate-page, bundle.

## Download Thumbnail

> Request

```
curl "https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/thumbnail" \
    -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
Content-Type: image/jpeg

[JPEG binary]
```

`GET /documents/{document_id}/thumbnail`

Download the document thumbnail.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| document\_id | True | The ID of the document to retrieve the thumbnail. |

## Download Page

> Request

```
curl "https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/pages/60f7205883c2fc57d51e68a7/download" \
    -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
Content-Type: application/jpeg

[JPEG binary]
```

`GET /documents/{document_id}/pages/{page_id}/download`

Download a document page as JPEG content.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| document\_id | True | The ID of the document to be downloaded. |
| page\_id | True | The ID of the page to be downloaded. |

## Verify

> Request

```
curl "https://api.assinafy.com.br/v1/documents/FE32EDDADE7CBDDCBB934E7402047450B0E59C02/verify"
```

> 200 OK | Verified

```
{
  "status": 200,
  "message": "",
  "data": {
    "hash": "FE32EDDADE7CBDDCBB934E7402047450B0E59C02",
    "id": "63ddb172402799bfc991d10d",
    "status": "certificated",
    "page_count": "1",
    "signer_count": "1",
    "completed_count": 1,
    "completed_at": "2023-01-27T19:27:44Z",
    "verified_at": "2023-01-27T19:27:46Z",
    "is_valid": true,
    "message": ""
  }
}
```

> 200 OK | Not Verified

```
{
  "status": 200,
  "message": "",
  "data": {
    "hash": "INVALIDHASHEXAMPLE",
    "id": null,
    "status": null,
    "page_count": null,
    "signer_count": null,
    "completed_count": null,
    "completed_at": null,
    "verified_at": "2023-01-27T19:30:15Z",
    "is_valid": false,
    "message": "Document not signed or not found."
  }
}
```

`GET /documents/{signature_hash}/verify`

Verify a document through its signature hash.

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| signature\_hash | True | The signature hash. It can be found on a signed document. |

## List Activities

> Request

```
curl "https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/activities" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "id": 4,
      "event": "assignment_created",
      "message": "Assignment created by John Smith.",
      "payload": {
        "user_name": "John Smith",
        "user_email": "[email protected]",
        "user_telephone": "+5511999999999"
      },
      "origin": {
        "ip": "172.19.0.1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
      },
      "created_at": "2022-07-19 19:28:13"
    },
    {
      "id": 3,
      "event": "signer_rejected_document",
      "message": "Signer 1 decline doc 2",
      "payload": {
        "signer_full_name": "Signer 1"
      },
      "origin": {
        "ip": "172.19.0.1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
      },
      "created_at": "2022-07-19 19:28:16"
    },
    {
      "id": 1,
      "event": "signature_requested",
      "message": "Signature requested to Nicole Bergstrom <+5511999999999>.",
      "payload": {
        "signer_full_name": "Nicole Bergstrom",
        "signer_email": "[email protected]",
        "signer_whatsapp_phone_number": "+5511999999999",
        "notification_method": "whatsapp"
      },
      "origin": {
        "ip": "172.19.0.1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
      },
      "created_at": "2022-07-19 19:28:14"
    }
  ]
}
```

`GET /documents/{documentId}/activities`

List document activities.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| documentId | true | The document ID. |

### Response Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | integer | Activity ID |
| `event` | string | Event type code |
| `message` | string | Human-readable event description |
| `payload` | object|array | Event-specific payload snapshot |
| `origin` | object|null | Request origin with `ip` and `user-agent` when available |
| `created_at` | string | ISO 8601 timestamp |

### Event Payloads

`assignment_created`

| Field | Type | Description |
| --- | --- | --- |
| `user_name` | string | Assignment creator name captured at record time |
| `user_email` | string | Assignment creator email captured at record time |
| `user_telephone` | string|null | Assignment creator telephone captured at record time |

`signature_requested`

| Field | Type | Description |
| --- | --- | --- |
| `signer_full_name` | string | Signer full name |
| `signer_email` | string|null | Signer email snapshot |
| `signer_whatsapp_phone_number` | string|null | Signer WhatsApp phone snapshot |
| `notification_method` | string | Notification channel used for this event: `email`, `whatsapp`, or `bypass` |

`signer_data_confirmed`

| Field | Type | Description |
| --- | --- | --- |
| `signer_full_name` | string | Signer full name |
| `signer_email` | string|null | Signer email snapshot |
| `signer_whatsapp_phone_number` | string|null | Signer WhatsApp phone snapshot |
| `verification_method` | string | Verification channel used for this event: `email`, `whatsapp`, or `bypass` |

## Public: Get Basic Info

> Request

```
curl "https://api.assinafy.com.br/v1/public/documents/39adfe3r5a3a"
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "document",
    "id": "doc1",
    "name": "1.pdf",
    "page_count": "1",
    "created_by": "John Smith"
  }
}
```

`GET /public/documents/{document_id}`

Get public information about a document by its ID. This endpoint does not require authentication and returns basic document details.

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| document\_id | True | The ID of the document. |

## Signer: Send Token

> Request

```
curl -X PUT "https://api.assinafy.com.br/v1/public/documents/39adfe3r5a3a/send-token" \
  -H "Content-Type: application/json" \
  -d '
{
  "recipient": "[email protected]",
  "channel": "email"
}
'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "document": {
      "resource": "document",
      "id": "doc1",
      "name": "1.pdf",
      "page_count": "1",
      "created_by": "John Smith"
    },
    "channel": "email",
    "recipient": "[email protected]"
  }
}
```

`PUT /public/documents/{document_id}/send-token`

Send the 6-digit token to the specified email for signing the document. This endpoint
does not require authentication and allows the token to be sent to a signer.

### Header Parameters

- `Content-Type: application/json`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| document\_id | True | The ID of the document. |

### Body Params

| Parameter | Required | Description |
| --- | --- | --- |
| recipient | True | Email of the signer. |
| channel | True | Channel to send the token. |

## List Document Tags

> Request

```
curl "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/documents/60f720572d7fecf7c16c8463/tags" \
  -H "Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg"
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": [
        {
            "id": "fa8c09f3e709a8a1c82d69b1454",
            "name": "Contracts",
            "color": "#FF0000",
            "created_at": "2026-05-14T12:00:00Z",
            "updated_at": "2026-05-14T12:00:00Z"
        }
    ]
}
```

`GET /accounts/{account_id}/documents/{document_id}/tags`

List the tags currently attached to a document.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |
| document\_id | True | The document ID. |

## Replace Document Tags

> Request

```
curl -X PUT "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/documents/60f720572d7fecf7c16c8463/tags" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '{ "tags": ["Contracts", "2026-Q1"] }'
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": [
        { "id": "fa8c...", "name": "2026-Q1", "color": null, "created_at": "...", "updated_at": "..." },
        { "id": "ab12...", "name": "Contracts", "color": null, "created_at": "...", "updated_at": "..." }
    ]
}
```

`PUT /accounts/{account_id}/documents/{document_id}/tags`

Replace the document's tag set with the provided list. Tags whose names do not yet exist in the workspace are created automatically (case-insensitive lookup).

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |
| document\_id | True | The document ID. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| tags | true | Array of tag names. An empty array detaches all tags from the document. |

## Append Document Tags

> Request

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/documents/60f720572d7fecf7c16c8463/tags" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '{ "tags": ["Urgent"] }'
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": [
        { "id": "ab12c09f3e709a8a1c82d69b145", "name": "Contracts", "color": "#FF0000", "created_at": "2026-05-14T12:00:00Z", "updated_at": "2026-05-14T12:00:00Z" },
        { "id": "fa8c09f3e709a8a1c82d69b1454", "name": "Urgent", "color": null, "created_at": "2026-05-14T13:00:00Z", "updated_at": "2026-05-14T13:00:00Z" }
    ]
}
```

`POST /accounts/{account_id}/documents/{document_id}/tags`

Attach additional tags to a document without removing existing ones. Idempotent: re-attaching a tag that is already present is a no-op. Unknown names are auto-created.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |
| document\_id | True | The document ID. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| tags | true | Array of tag names. |

## Detach Tag From Document

> Request

```
curl -X DELETE "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/documents/60f720572d7fecf7c16c8463/tags/fa8c09f3e709a8a1c82d69b1454" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": {
        "detached": true
    }
}
```

`DELETE /accounts/{account_id}/documents/{document_id}/tags/{tag_id}`

Detach a single tag from a document. The tag itself is not deleted. Detaching a tag that was not attached is a no-op.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |
| document\_id | True | The document ID. |
| tag\_id | True | The tag ID. |
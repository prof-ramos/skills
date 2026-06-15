> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#signer-documents)

# Signer Documents

## Índice

- [Get Current Document](#get-current-document)
  - [Authorization](#authorization)
  - [URL Parameters](#url-parameters)
  - [Response](#response)
- [List](#list)
  - [Authorization](#authorization)
  - [URL Parameters](#url-parameters)
  - [Document Status](#document-status)
- [Sign Multiple](#sign-multiple)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Decline Multiple](#decline-multiple)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Download](#download)
  - [URL Parameters](#url-parameters)

---



## Get Current Document

> Request

```
curl -X GET 'https://api.assinafy.com.br/v1/signers/62d6ee35c7741ca4006b9e11/document?signer-access-code=1ca4006b9e111ca4006b9e11'
```

`GET /signers/{signer_id}/document?signer-access-code=1ca4006b9e111ca4006b9e11`

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "id": "6981dbd199996981d",
    "account_id": "1a",
    "name": "my_document.pdf",
    "status": "metadata_ready",
    "artifacts": {
      "original": "https://api.assinafy.com.br/v1/documents/doc1/download/original",
      "thumbnail": "https://api.assinafy.com.br/v1/documents/doc1/thumbnail"
    },
    "is_closed": false,
    "signing_url": "%ui_base_url%/sign/doc1",
    "decline_reason": null,
    "declined_by": null,
    "created_at": "2023-07-21T13:43:17Z",
    "updated_at": "2023-07-21T13:43:17Z",
    "current_signer": {
      "id": "62d6ee35c7741ca4006b9e11",
      "full_name": "Signer Name",
      "email": "[email protected]",
      "has_accepted_terms": false,
      "verification_method": "Email",
      "notification_methods": ["Email"]
    },
    "assignment": {
      "id": "1",
      "sender_email": "[email protected]",
      "method": "virtual",
      "expires_at": null,
      "message": null,
      "items": [
        {
          "id": "dbd199996981d",
          "signer": {
            "id": "62d6ee35c7741ca4006b9e11",
            "full_name": "Signer Name",
            "email": "[email protected]",
            "has_accepted_terms": false
          },
          "field": {
            "id": "dbd199996981d",
            "name": "Assinatura",
            "type": "virtual"
          },
          "display_settings": "",
          "value": "",
          "completed": false
        }
      ]
    }
  }
}
```

Retrieves the document associated with the current signer access code,
without exposing page content. Useful right after the signer opens the link
received by email or WhatsApp, so the frontend can display which document
is about to be signed before asking the signer to verify their code.

This endpoint does not require the signer to have completed code
verification or data confirmation. It resolves the document, assignment,
and current signer data directly from the `signer-access-code`.

### Authorization

The `signer-access-code` URL parameter is required.

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signer_id` | true | The signer ID (must match the one bound to the access code). |
| `signer-access-code` | true | Signer access code as query string parameter. |

### Response

The response mirrors the document shape returned by the signing endpoints,
but omits the `pages` array. The `assignment.items` array is filtered to
only include the items assigned to the current signer.

## List

> Request

```
curl -X GET https://api.assinafy.com.br/v1/signers/62d6ee35c7741ca4006b9e11/documents?signer-access-code=1ca4006b9e111ca4006b9e11
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
      "declined_by": null
    },
  ]
}
```

`GET /signers/{signer_id}/documents?signer-access-code=1ca4006b9e111ca4006b9e11`

List signer's documents.

### Authorization

Either the `authorization` header or the `signer_access_code` URL parameter
can be used for authorization.

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| signer\_id | true | The signer ID. |
| signer\_access\_code | true | The signer access code. |
| status | false | Status code to filter results. Ex.: `pending_signature`. |
| method | false | Signature method filter. Ex.: `?method=virtual`. Possible values: `virtual` or `collect`. |
| search | false | Search term that will be used for partial matching on the following attributes: `document.name`, `signer.full_name` and `signer.email`. |
| sort | false | Allows sorting by: `name` and `updated_at`. |

When present, the `search` URL parameter will be used for a partial search
on the following attributes: `document.name`, `signer.full_name` and `signer.email`.

Possible sort attributes are `name` and `updated_at`.

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

## Sign Multiple

> Request

```
curl -X PUT 'https://api.assinafy.com.br/v1/signers/documents/sign-multiple?signer-access-code=9uAWyOXx9hgzCKhkinwvg8tWJ2RC' \
-d '{
  "document_ids": ["documentid1", "documentid2"]
}'
```

`PUT /signers/documents/sign-multiple`

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": []
}
```

Allow a signer to sign multiple documents at once.

Each document should be prepared for the "virtual" signature method.

**Headers**:

- `Content-Type` - `application/json`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signer-access-code` | true | Signer access code as query string parameter. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `document_ids` | true | Array of document IDs to be signed. |

## Decline Multiple

> Request

```
curl -X PUT 'https://api.assinafy.com.br/v1/signers/documents/decline-multiple?signer-access-code=9uAWyOXx9hgzCKhkinwvg8tWJ2RC' \
-d '{
  "document_ids": ["documentid1", "documentid2"],
  "decline_reason": "Unfavorable terms."
}'
```

`PUT /signers/documents/decline-multiple`

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": []
}
```

Allow a signer to decline multiple documents at once.

**Headers**:

- `Content-Type` - `application/json`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signer-access-code` | true | Signer access code as query string parameter. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `document_ids` | true | Array of document IDs to be declined. |
| `decline_reason` | true | Text explaining the reason for the decline. |

## Download

> Request

```
curl -X GET "https://api.assinafy.com.br/v1/signers/62d6ee35c7741ca4006b9e11/documents/62d6ee35c7741ca4006b9e11/download/original?signer-access-code=1ca4006b9e111ca4006b9e11"
```

> 200 OK

```
Content-Type: application/pdf

[PDF binary]
```

`GET /signers/{signer_id}/documents/{document_id}/download/{artifact_name}?signer-access-code=1ca4006b9e111ca4006b9e11`

Download a signer's document.

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| signer\_id | true | The signer ID. |
| document\_id | true | The document ID. |
| artifact\_name | True | The type of artifact to download. |
| signer-access-code | True | The signer's access code. |

**Artifact types**: original, certificated, certificate-page, bundle.
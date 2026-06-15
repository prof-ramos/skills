> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#template)

# Template

## Índice

- [Template Objects](#template-objects)
  - [Template Object](#template-object)
  - [Template Page Object](#template-page-object)
  - [Template Field Placement Object](#template-field-placement-object)
  - [Template Status](#template-status)
- [List](#list)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Template Status](#template-status)

---



This is the templates management service. The endpoints of this area allow us
to create, list, download and delete templates.

## Template Objects

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for template-related objects returned by the API.

### Template Object

Returned by endpoints such as `GET /accounts/{account_id}/templates`, `GET /accounts/{account_id}/templates/{template_id}`, `POST /accounts/{account_id}/templates`, and `PUT /accounts/{account_id}/templates/{template_id}`.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `template`. |
| `id` | string | Template ID. |
| `name` | string | Template file name. |
| `document_name` | string|null | Default document name used when creating documents from this template. |
| `message` | string|null | Default invitation message configured on the template. |
| `status` | string | Template status code. |
| `pages` | array[object] | Template pages. |
| `roles` | array[object] | Template roles. |
| `tags` | array[object] | Tags attached to the template (own tags). Each entry has `id` and `name`. Always present, possibly empty. |
| `default_document_tags` | array[object] | Tags automatically applied to every document created from this template. Each entry has `id` and `name`. Returned only by the single-template endpoint (`GET /accounts/{account_id}/templates/{template_id}`); omitted from the list endpoint to keep responses compact. |
| `created_at` | string | Creation timestamp in ISO 8601 format. |
| `updated_at` | string | Last update timestamp in ISO 8601 format. |

### Template Page Object

Returned inside `template.pages`.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Template page ID. |
| `number` | integer | Page number, starting at `1`. |
| `height` | integer | Page height in pixels. |
| `width` | integer | Page width in pixels. |
| `download_url` | string | URL to download the rendered template page image. |
| `fields` | array[object] | Field placements configured on that page. |

### Template Field Placement Object

Returned inside `template.pages[].fields`.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Field placement ID. |
| `field_id` | string | Field definition ID linked to the placement. |
| `role_id` | string | Template role ID responsible for the placement. |
| `label` | string | Label displayed for the field placement. |
| `display_settings` | object|array|string|null | Rendering metadata for the field placement. |
| `created_at` | string | Creation timestamp in ISO 8601 format. |
| `updated_at` | string | Last update timestamp in ISO 8601 format. |

### Template Status

A template will be in one of the following status:

| Status | Description |
| --- | --- |
| uploading | The template upload is being uploaded. |
| uploaded | The template has been uploaded. |
| processing | The template is being processed. |
| ready | The template is ready to use. |
| failed | The template processing has failed. |

## List

> Request

```
curl "https://api.assinafy.com.br/v1/accounts/{account_id}/templates" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrghAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": [
        {
            "id": "fa7f3e524f3a2cc00a5ea4325e2",
            "name": "sample-contract-one-page.pdf",
            "document_name": "sample-contract-one-page.pdf",
            "message": null,
            "status": "Ready",
            "pages": [
                {
                    "id": "fa7f3e528d77f2b3ed786df2ce0",
                    "number": 1,
                    "height": 2100,
                    "width": 1275,
                    "download_url": "https://api.assinafy.com.br/v1/accounts/1a/templates/fa7f3e524f3a2cc00a5ea4325e2/pages/fa7f3e528d77f2b3ed786df2ce0/download",
                    "fields": []
                }
            ],
            "roles": [
                {
                    "id": "fa7f3e525bfefc71df3701eac6f",
                    "name": "Editor",
                    "assignment_type": "Editor",
                    "created_at": "2024-07-19T15:23:03Z",
                    "updated_at": "2024-07-19T15:23:03Z"
                }
            ],
            "tags": [
                { "id": "fa8c09f3e709a8a1c82d69b1454", "name": "HR" }
            ],
            "created_at": "2024-07-19T15:23:03Z",
            "updated_at": "2024-07-19T15:23:03Z"
        }
    ]
}
```

`GET /accounts/{account_id}/templates`

This endpoint will list templates of the workspace.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | true | ID of the workspace account. |
| status | false | Status filter. Ex.: `?status=ready`. |
| search | false | Search term that will be used for partial matching on the template name. |
| tags | false | Comma-separated list of tag IDs. Returns only templates that have **all** the listed tags (AND semantics). Unknown tag IDs yield an empty result. Example: `?tags=tagId1,tagId2`. |
| sort | false | Allows sorting by: `name` and `updated_at`. |

### Template Status

These are the possible template status:

| Status | Description |
| --- | --- |
| uploading | The template upload is being uploaded. |
| uploaded | The template has been uploaded. |
| processing | The template is being processed. |
| ready | The template is ready to use. |
| failed | The template processing has failed. |
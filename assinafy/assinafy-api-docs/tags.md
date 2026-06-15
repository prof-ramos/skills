> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#tag)

# Tag

## Índice

- [Tag Object](#tag-object)
- [List Tags](#list-tags)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Query Parameters](#query-parameters)
- [Create Tag](#create-tag)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Rename Tag](#rename-tag)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Delete Tag](#delete-tag)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Query Parameters](#query-parameters)

---



This is the tags management service. Tags are workspace-scoped labels that can be
attached to documents and templates to make them easier to find. Templates also
carry a separate set of "default document tags" that are automatically applied to
documents generated from them.

## Tag Object

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for tag objects returned by the API.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `tag`. |
| `id` | string | Tag ID. |
| `name` | string | Tag display name. |
| `color` | string | Optional 6-character hex color (without the leading `#`) for UI display. `null` when not set. |
| `created_at` | string | Creation timestamp in ISO 8601 format. |
| `updated_at` | string | Last update timestamp in ISO 8601 format. |

Tag names are unique per workspace, case-insensitive (`"Contracts"` and `"contracts"` collide). Leading/trailing whitespace is trimmed and internal whitespace is collapsed to single spaces before storage.

When a tag attached to a document or template appears inline in those resources (under the `tags` or `default_document_tags` field), only `id`, `name`, and `color` are returned.

## List Tags

> Request

```
curl "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/tags?search=contract" \
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
            "color": "ff8800",
            "created_at": "2026-05-14T12:00:00Z",
            "updated_at": "2026-05-14T12:00:00Z"
        }
    ]
}
```

`GET /accounts/{account_id}/tags`

List the tags of a workspace, ordered alphabetically by name.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |

### Query Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| search | False | Case-insensitive substring filter applied to tag name. |

## Create Tag

> Request

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/tags" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '{ "name": "Contracts", "color": "ff8800" }'
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": {
        "resource": "tag",
        "id": "fa8c09f3e709a8a1c82d69b1454",
        "name": "Contracts",
        "color": "ff8800",
        "created_at": "2026-05-14T12:00:00Z",
        "updated_at": "2026-05-14T12:00:00Z"
    }
}
```

`POST /accounts/{account_id}/tags`

Create a new tag in the workspace.

Returns `409 Conflict` if a tag with the same name (case-insensitive) already exists.

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
| name | true | Tag display name. Trimmed; whitespace is collapsed; max 64 characters. |
| color | false | 6-character hex color (with or without leading `#`) used for UI display. Omit or pass `null` for no color. |

## Rename Tag

> Request

```
curl -X PUT "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/tags/fa8c09f3e709a8a1c82d69b1454" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -d '{ "name": "Sales Contracts", "color": "112233" }'
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": {
        "resource": "tag",
        "id": "fa8c09f3e709a8a1c82d69b1454",
        "name": "Sales Contracts",
        "color": "112233",
        "created_at": "2026-05-14T12:00:00Z",
        "updated_at": "2026-05-14T13:00:00Z"
    }
}
```

`PUT /accounts/{account_id}/tags/{tag_id}`

Update a tag's name and/or color. All documents and templates already attached to the tag keep their relationship — only the tag's own attributes change. Either parameter may be omitted to leave it untouched; passing `color: null` clears the color.

Returns `409 Conflict` if another tag in the workspace already uses the new name (case-insensitive). Renaming the same tag to a different casing of its current name is allowed.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |
| tag\_id | True | The tag ID. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| name | false | New tag name. Omit to leave unchanged. |
| color | false | New 6-character hex color (with or without leading `#`). Pass `null` to clear. Omit to leave unchanged. |

## Delete Tag

> Request

```
curl -X DELETE "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/tags/fa8c09f3e709a8a1c82d69b1454" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": {
        "deleted": true
    }
}
```

> 409 Conflict (tag in use, no force)

```
{
    "status": 409,
    "message": "Tag is in use. Pass force=true to detach and delete.",
    "data": null
}
```

`DELETE /accounts/{account_id}/tags/{tag_id}`

Delete a tag. By default, deletion fails with `409 Conflict` if the tag is attached to any document, template, or template default-document-tag set. Pass `force=true` to detach the tag from everything and delete it; the affected documents and templates themselves are **not** deleted.

### Header Parameters

- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| account\_id | True | The account ID. |
| tag\_id | True | The tag ID. |

### Query Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| force | False | When `true`, detach the tag from all documents and templates before deleting it. Defaults to `false`. |
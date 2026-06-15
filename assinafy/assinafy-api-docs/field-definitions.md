> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#field-definition)

# Field Definition

## Índice

- [Field Definition Object](#field-definition-object)
- [Create](#create)
  - [Body Parameters](#body-parameters)
- [List](#list)
- [Get](#get)
- [Update](#update)
  - [Header Parameters](#header-parameters)
  - [Body Parameters](#body-parameters)
- [Delete](#delete)
  - [Header Parameters](#header-parameters)
- [Validate](#validate)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [Validate Multiple](#validate-multiple)
  - [Header Parameters](#header-parameters)
  - [URL Parameters](#url-parameters)
  - [Body Parameters](#body-parameters)
- [List Types](#list-types)
  - [Header Parameters](#header-parameters)

---



## Field Definition Object

Examples in this section may omit fields for brevity. Use this reference as the canonical shape for field definition objects returned by the API.

| Field | Type | Description |
| --- | --- | --- |
| `resource` | string | Resource type. Present in single-resource responses. Always `field_definition`. |
| `id` | string | Field definition ID. |
| `name` | string | Field display name. |
| `type` | string | Field type code, such as `text`, `date`, `signature`, `initial`, or `virtual`. |
| `regex` | string|null | Regular expression used to validate the field value, when configured. |
| `is_pre_defined` | boolean | Indicates whether the field is predefined by the platform. |
| `is_active` | boolean | Indicates whether the field is active and available for use. |
| `is_required` | boolean | Indicates whether the field requires a value. |
| `is_standard` | boolean | Indicates whether the field belongs to the standard built-in field set. |
| `is_read_only` | boolean | Indicates whether the field value is read-only from the signer's perspective. |
| `is_visible` | boolean | Indicates whether the field is visible to signers and users. |

## Create

> Request

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/2120297080d55bdd13197/fields" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -H 'Content-Type: application/json' \
  -d '{ "type: "text", "name": "Field Name" }'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "field_definition",
    "id": "63cfe15556a99a147bdd304b",
    "name": "CPF",
    "type": "cpf",
    "regex": null,
    "is_active": true,
    "is_required": true,
    "is_standard": false,
    "is_read_only": false,
    "is_visible": true
  }
}
```

`POST /accounts/{accountId}/fields`

Create a field definition.

**Headers**:

- `Content-Type` - `application/json`
- `Authorization` - `Bearer {access_token}`

### Body Parameters

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `type` | true |  | The input type. |
| `name` | true |  | The label for the input field. |
| `regex` | false |  | REGEX pattern to be used for validation. Ex.: "/[0-9]{2}-[0-9]{4}/". It is effective only for *text* input types. |
| `is_required` | false | true | Indicate if an input value is required. |
| `is_active` | false | true | Indicate if the field definition is active. |

**Note:** the */input-types* endpoint can be used to list allowed types.

## List

> Request

```
curl "https://api.assinafy.com.br/v1/accounts/2120297080d55bdd13197/fields" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "id": "64a7584106d7e3ded274da11",
      "name": "Name",
      "type": "personName",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    },
    {
      "id": "64a758410c5a5df8d07256b5",
      "name": "CPF",
      "type": "cpf",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    },
    {
      "id": "64a75841255d055eba653c6b",
      "name": "Phone Number",
      "type": "phoneNumber",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    },
    {
      "id": "64a758412201552421d7f60d",
      "name": "Postal Code",
      "type": "postalCode",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    },
    {
      "id": "64a75841ce1def29916e3d23",
      "name": "E-mail",
      "type": "email",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    },
    {
      "id": "64a758411a3fbc679ef91a55",
      "name": "CNPJ",
      "type": "cnpj",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    },
    {
      "id": "64a75841851209fc930db912",
      "name": "Company Name",
      "type": "companyName",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    },
    {
      "id": "64a75841090c4807361996b4",
      "name": "Text Field",
      "type": "text",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    },
    {
      "id": "64a758413ac706942c065035",
      "name": "Number",
      "type": "number",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    },
    {
      "id": "64a7584139987d891d5820df",
      "name": "Date",
      "type": "date",
      "regex": null,
      "is_pre_defined": true,
      "is_active": true,
      "is_required": false,
      "is_standard": false,
      "is_read_only": false,
      "is_visible": true
    }
  ]
}
```

`GET /accounts/{accountId}/fields`

List field definitions.

**Headers**:

- `Content-Type` - `application/json`
- `Authorization` - `Bearer {access_token}`

###### URL Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `include_inactive` | false | Indicate if inactive records should be returned. Possible values: *true*, *false*. |
| `include_standard` | false | Indicate if standard fields types should be returned. Possible values: *true*, *false*. |

When indicating standard fields to be returned, records of type *signature*, *initial*
and *signatureDate* will also be in the result.

## Get

> Request

```
curl "https://api.assinafy.com.br/v1/accounts/2120297080d55bdd13197/fields/7080d55bdd13197" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "field_definition",
    "id": "63cfe123880b1ba571a97916",
    "name": "Field Name",
    "type": "text",
    "regex": null,
    "is_active": true,
    "is_required": true,
    "is_standard": false,
    "is_read_only": false,
    "is_visible": true
  }
}
```

`GET /accounts/{accountId}/fields/{field_id}`

Get single field definition.

**Headers**:

- `Content-Type` - `application/json`
- `Authorization` - `Bearer {access_token}`

## Update

> Request

```
curl -X PUT "https://api.assinafy.com.br/v1/accounts/2120297080d55bdd13197/fields/63345ba3255f24a5bc7c75f0" \
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
  -H 'Content-Type: application/json' \
  -d '{ "name": "New Field Name" }'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "field_definition",
    "id": "63cfe0e0fdc4e3aeb74783d7",
    "name": "New Field Name",
    "type": "text",
    "regex": null,
    "is_active": true,
    "is_required": true,
    "is_standard": false,
    "is_read_only": false,
    "is_visible": true
  }
}
```

`PUT /accounts/{account_id}/fields/{field_id}`

Update a field definition.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### Body Parameters

| Parameter | Description |
| --- | --- |
| `type` | The input type. |
| `name` | The label for the input field. |
| `regex` | REGEX pattern to be used for validation. Ex.: "/[0-9]{2}-[0-9]{4}/". It is effective only for *text* input types. |
| `is_required` | Indicate if an input value is required. |
| `is_active` | Indicate if it is active. |

Note: the */input-types* endpoint can be used to list allowed types.

## Delete

> Request

```
curl -X DELETE "https://api.assinafy.com.br/v1/accounts/2120297080d55bdd13197/fields/63345ba3255f24a5bc7c75f0" \
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

`DELETE /accounts/{account_id}/fields/{field_id}`

Delete a field definition.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

A field definition that has been used in a document cannot be
deleted.

## Validate

> Request

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/2120297080d55bdd13197/fields/63345ba3255f24a5bc7c75f0/validate?signer-access-code=hAvmvk6Urzus3byLD2qOWrghAvmvk6Urzus3byLD2qOWrg" \
  -H 'Content-Type: application/json' \
  -d '{"value":"400.676.228-36"}'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "type": "cpf",
    "success": true,
    "error_message": ""
  }
}
```

`POST /accounts/{accountId}/fields/{field_id}/validate`

Validate an input value against a field definition.

**Important:** The *Authorization* header is used only when accessing as an
authenticated user. When accessing as a signer, use the *signer-access-code* URL parameter.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signer-access-code` | true | Signer access code. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `value` | true | The input value to be validated. |

## Validate Multiple

> Request

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/2120297080d55bdd13197/fields/validate-multiple?signer-access-code=hAvmvk6Urzus3byLD2qOWrghAvmvk6Urzus3byLD2qOWrg" \
  -H 'Content-Type: application/json' \
  -d '
[
  {
    "field_id": "63488ffb7adf435aba319787",
    "value": "1111111111111"
  },
  {
    "field_id": "63488ffb0461cebb70775497",
    "value": "[email protected]"
  }
]
'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "field_id": "63488ffb7adf435aba319787",
      "type": "cpf",
      "success": false,
      "error_message": "Invalid CPF."
    },
    {
      "field_id": "63488ffb0461cebb70775497",
      "type": "email",
      "success": true,
      "error_message": ""
    }
  ]
}
```

`POST /accounts/{accountId}/fields/validate-multiple`

Validate multiple input values at once.

**Important:** The *Authorization* header is used only when accessing as an
authenticated user. When accessing as a signer, use the *signer-access-code* URL parameter.

### Header Parameters

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### URL Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `signer-access-code` | true | Signer access code. |

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `[].field_id` | true | The field definition ID. |
| `[].value` | true | The input value to be validated. |

## List Types

> Request

```
curl "https://api.assinafy.com.br/v1/field-types"
  -H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": [
    {
      "type": "personName",
      "name": "Name"
    },
    {
      "type": "cpf",
      "name": "CPF"
    },
    {
      "type": "phoneNumber",
      "name": "Phone Number"
    },
    {
      "type": "postalCode",
      "name": "Postal Code"
    },
    {
      "type": "email",
      "name": "E-mail"
    },
    {
      "type": "cnpj",
      "name": "CNPJ"
    },
    {
      "type": "companyName",
      "name": "Company Name"
    },
    {
      "type": "email",
      "name": "E-mail"
    },
    {
      "type": "text",
      "name": "Text"
    },
    {
      "type": "number",
      "name": "Number"
    },
    {
      "type": "date",
      "name": "Date"
    }
  ]
}
```

`GET /field-types`

List possible field types.

The `cpf` field type expects 11 digits. The `cnpj` field type accepts 14-character values; as of the Receita Federal `CNPJ Alfanumérico` rule, letters `A-Z` are accepted in positions 1–12 (check digits 13–14 remain numeric). Punctuation is ignored during validation.

### Header Parameters

- `Authorization: Bearer {access_token}`
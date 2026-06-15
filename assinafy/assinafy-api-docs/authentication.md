> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#authentication)

# Authentication

## Índice

- [Login](#login)
  - [Headers](#headers)
  - [Body Parameters](#body-parameters)
- [Social Login](#social-login)
  - [Headers](#headers)
  - [Body Parameters](#body-parameters)
- [Create API Key](#create-api-key)
  - [Headers](#headers)
  - [Body Parameters](#body-parameters)
- [Get API Key](#get-api-key)
  - [Header Parameters](#header-parameters)
- [Delete API Key](#delete-api-key)
  - [Headers](#headers)
- [Change Password](#change-password)
  - [Headers](#headers)
  - [Body Parameters](#body-parameters)
- [Request Password Reset](#request-password-reset)
  - [Headers](#headers)
  - [Request Body](#request-body)
- [Reset Password](#reset-password)
  - [Headers](#headers)
  - [Body Parameters](#body-parameters)

---



A authentication can be done through these methods:

- API key in the header `X-Api-Key`:  
  `X-Api-Key: {api-key}`
- Access token in the `Authorization` header:  
  `Authorization: Bearer {access-token}`
- Access token as URL parameter:  
  `?access-token={access-token}`

The recommended way to authenticate is throgh an API key. You can create a key
from the settings page, in the Assinafy app.

if however, you want to use an access token, it is obtained through the login
process using user email and password. It is a JWT token and usually
it expires in one hour.

## Login

> Request

```
curl -X POST https://api.assinafy.com.br/v1/login \
-H 'Content-Type: application/json' \
-d '{ "email": "[email protected]", "password": "password" }'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImp0aSI6IjY0MDFkZjQ3NWNkYzgxLjc2MTkwODgxIn0.eyJpc3MiOiJBc3NpbmFmeSIsImF1ZCI6IkFzc2luYWZ5IiwianRpIjoiNjQwMWRmNDc1Y2RjODEuNzYxOTA4ODEiLCJpYXQiOjE2Nzc4NDQyOTUsImV4cCI6MTY3OTY1ODY5NSwic3ViIjoiYmdqYXplbzVyOXYybHE3bDM2ZHg0OG5wIiwibmFtZSI6IkZcdTAwZTFiaW8gQ3Jpc3RpYW5vIExvdmF0byBKci4iLCJlbWFpbCI6ImRpcmNlLm9saXZlaXJhQGdtYWlsLmNvbSJ9.sHpe608nPwb5gMUMn-REy7TOxq7mxTPpPwE-bak6hz4",
    "user": {
      "id": "bgjazeo5r9v2lq7l36dx48np",
      "name": "John Smith",
      "email": "[email protected]",
      "telephone": "17989206641",
      "government_id": "15774136604",
      "is_email_verified": false,
      "has_accepted_terms": true,
      "created_at": "2023-03-03T11:51:34Z",
      "to_be_deleted_at": null
    },
    "accounts": [
      {
        "id": "6401df46d6a6b0c692d9ec49",
        "name": "JS",
        "roles": [
          "owner"
        ],
        "is_delete_allowed": true,
        "created_at": "2023-03-03T11:51:34Z"
      }
    ]
  }
}
```

`POST /login`

Login and create an access token.

### Headers

- `Content-Type: application/json`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| email | true | User's email. |
| password | true | User's password. |

## Social Login

> Request

```
curl -X POST https://api.assinafy.com.br/v1/authentication/social-login \
-H 'Content-Type: application/json' \
-d '{
    "provider": "google",
    "token": "yOTUvImV4cCI6MTY3OTY1ODY5NSwic3ViIjoiYmdqYXplbzVyOXYybHE3bDM2ZHg0",
    "has_accepted_terms": true
}'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImp0aSI6IjY0MDFkZjQ3NWNkYzgxLjc2MTkwODgxIn0.eyJpc3MiOiJBc3NpbmFmeSIsImF1ZCI6IkFzc2luYWZ5IivianRpIjoiNjQwMWRmNDc1Y2RjODEuNzYxOTA4ODEiLCJpYXQiOjE2Nzc4NDQyOTUvImV4cCI6MTY3OTY1ODY5NSwic3ViIjoiYmdqYXplbzVyOXYybHE3bDM2ZHg0OG5wIiwibmFtZSI6IkZcdTAwZTFiaW8gQ3Jpc3RpYW5vIExvdmF0byBKci4iLCJlbWFpbCI6ImRpcmNlLm9saXZlaXJhQGdtYWlsLmNvbSJ9.sHpe608nPwb5gMUMn-REy7TOxq7mxTPpPwE-bak6hz4",
    "user": {
      "id": "bgjazeo5r9v2lq7l36dx48np",
      "name": "John Smith",
      "email": "[email protected]",
      "telephone": "17989206641",
      "government_id": "15774136604",
      "is_email_verified": false,
      "has_accepted_terms": true,
      "created_at": "2023-03-03T11:51:34Z",
      "to_be_deleted_at": null
    },
    "accounts": [
      {
        "id": "6401df46d6a6b0c692d9ec49",
        "name": "JS",
        "roles": [
          "owner"
        ],
        "is_delete_allowed": true,
        "created_at": "2023-03-03T11:51:34Z"
      }
    ]
  }
}
```

`POST /authentication/social-login`

Receive an access token or an ID token obtained throught a social login
provider and return an Assinafy access token.

### Headers

- `Content-Type: application/json`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| provider | true | The provider type. |
| token | true | The access token or ID token obtained from the social login provider. |
| has\_accepted\_terms | true | Boolean value indicating if user has accepted terms. Example: *true*. |

Currently, the only possible provider type is *google*.

## Create API Key

> Request

```
curl -X POST https://api.assinafy.com.br/v1/users/api-keys \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer 62b3a62b3a62b3ac64d6c55c64d6c55c64d6c55' \
-d '
{
  "password": "password"
}
'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "api_key": "mIpe_zdJfKUpMK9Va3XuYgzPXMxz49fIaRCWXseVkpVAX608A9j3i_D67qU5qW3M"
  }
}
```

`POST /users/api-keys`

Generate an API key for the user. The generated API key should be used
through the header X-Api-Key.

Important: when generating a new key, the previous one will be deleted.

Never use your API key from a frontend application.

### Headers

- `Content-Type: application/json`
- `Authorization: Bearer {access_token}`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| password | true | User's password. |

## Get API Key

> Request

```
curl -X GET https://api.assinafy.com.br/v1/users/api-keys \
-H 'Authorization: Bearer 62b3a62b3a62b3ac64d6c55c64d6c55c64d6c55'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "api_key": "************************************************************9Jdr"
  }
}
```

`GET /users/api-keys`

Retrieve a masked version of existing API key. For security reasons, your existing
API key cannot be retrieved fully.

While an API key was not generated yet, a null value is returned.

### Header Parameters

- `Authorization: Bearer {access_token}`

## Delete API Key

> Request

```
curl -X DELETE https://api.assinafy.com.br/v1/users/api-keys \
-H 'Authorization: Bearer 62b3a62b3a62b3ac64d6c55c64d6c55c64d6c55'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": []
}
```

`DELETE /users/api-keys`

Delete an existing API key.

### Headers

- `Authorization: Bearer {access_token}`

## Change Password

> Request

```
curl -X PUT https://api.assinafy.com.br/v1/authentication/change-password \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrg' \
-d '
{
  "email": "[email protected]",
  "password": "X3$_!456aTa",
  "new_password": "X3$_!456aT"
}'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "email": "[email protected]"
  }
}
```

`PUT /authentication/change-password`

Change user's password.

### Headers

- `Authorization Bearer {access_token}`
- `Content-Type application/json`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| email | true | User's email. |
| password | true | The current password. |
| new\_password | true | The new password to be set. |

## Request Password Reset

> Request

```
curl -X PUT https://api.assinafy.com.br/v1/authentication/request-password-reset \
-H 'Content-Type: application/json' \
-d '{
  "email": "[email protected]"
}'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "email": "[email protected]"
  }
}
```

`PUT /authentication/request-password-reset`

Request a password reset. An email with instructions will be sent to the user
to continue the process. This is request is typically used when the user
forgot his password or when it was not set yet.

### Headers

- `Content-Type` - `application/json`

### Request Body

| Parameter | Required | Description |
| --- | --- | --- |
| email | true | User's email. |

## Reset Password

> Request

```
curl -X PUT https://api.assinafy.com.br/v1/authentication/reset-password \
-H 'Content-Type: application/json' \
-d '{
  "email": "[email protected]",
  "token": "b3ac64d6c55b3ac64d6c55b3ac64d6c55b3ac64d6c55",
  "new_password": "62b3ac64d6c55"
}'
```

> 200 OK

```
{
  "status": 200,
  "message": "",
  "data": {
    "email": "[email protected]"
  }
}
```

`PUT /authentication/reset-password`

Reset the user's password using instructions received by email.

### Headers

- `Content-Type` - `application/json`

### Body Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| email | true | User's email. |
| token | false | Token received by email as an URL parameter. |
| new\_password | true | The new password to be set. |
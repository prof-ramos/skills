> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#basics)

# Basics

## Índice

- [REST API](#rest-api)
  - [Content Type](#content-type)
  - [Status Code](#status-code)
  - [Authentication](#authentication)
- [Searching, Paginating and Sorting](#searching-paginating-and-sorting)
  - [URL Parameters](#url-parameters)
  - [Response Headers](#response-headers)
- [Test and Production Environments](#test-and-production-environments)
- [Errors](#errors)
  - [Error Codes](#error-codes)
- [Postman Collection](#postman-collection)

---



The Assinafy API is RESTful and allows access to documents, users, workspaces
and signers, using an access token or a permanent key.

## REST API

> Request Example

```
curl -X GET "https://api.assinafy.com.br/v1/some-end-point" \
  -H 'X-Api-Key: hAvmvk6Urzus3byLD2qOWrghAvmvk6Urzus3byLD2qOWrg'
```

> Success Response Example

```
{
    "status": 200,
    "message": "",
    "data": {
        "attribute_1": "value 1",
        "attribute_2": "value 2",
    }
}
```

> Error Response example

```
{
    "status": 400,
    "message": "Some error message.",
    "data": []
}
```

As a RESTful API, HTTP verbs are used according to the request type.

- GET to retrieve data;
- POST to create;
- PUT to update;
- DELETE to remove.

### Content Type

The default request and response data format is JSON. The XML format is also
supported.

### Status Code

Every response will return the status attribute. The value of 200 indicates the
request was successful. Otherwise another HTTP code will indicate the result. The
status attribute will reflect the status code in HTTP headers.

### Authentication

Most endpoints require authentication. There two options:

- A fixed API key;
- An access token.

## Searching, Paginating and Sorting

> Request

```
curl -X GET 'https://api.assinafy.com.br/v1/accounts/631606b068b6cd6709f448bc/documents?page=1&per-page=25&search=name' \
-H 'Authorization: Bearer hAvmvk6Urzus3byLD2qOWrghAvmvk6Urzus3byLD2qOWrghAvmvk6'
```

> 200 OK

```
{
    "status": 200,
    "message": "",
    "data": [
        { "id": "1zus3byLD2qOWrghAvmvk6", "name 1" },
        { "id": "2zus3byLD2qOWrghAvmvk6", "name 2" }
    ]
}
```

### URL Parameters

| Parameter | Description |
| --- | --- |
| search | Search term. |
| page | Page number. |
| per-page | Desired count of records per page. A maximum of 100 is allowed. |
| sort | Sort order for results. Example.: `?sort=name, ?sort=-created_at` |

### Response Headers

| Header | Description |
| --- | --- |
| X-Pagination-Current-Page | Current returned page. |
| X-Pagination-Total-Count | Total count of records. |
| X-Pagination-Page-Count | Count of pages. |
| X-Pagination-Per-Page | Count of records per page. |

## Test and Production Environments

During development stage, use the sandbox base URL:  
API: <https://sandbox.assinafy.com.br/v1>  
APP: <https://app-sandbox.assinafy.com.br>

When development is completed, use the production base URL:  
API: <https://api.assinafy.com.br/v1>  
APP: <https://app.assinafy.com.br>

## Errors

It is important do consider responses resulting in a error. That can occur,
for example, when a field is sent with an invalid value.

> 400 Bad Request

```
{
    "status": 400,
    "message": "The 'email' attribute cannot be empty.",
    "data": []
}
```

### Error Codes

The error code is returned in the *status* attribute.

| Code | Type |
| --- | --- |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 415 | Unsupported Media Type |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

## Postman Collection

This a public Postman collection to explore Assinafy endpoints. Here is how
to use it:

1. Access the [Assinafy Postman collection](https://www.postman.com/devassinafy/dev-assinafy-s-workspace/collection/tqqxlsd/assinafy-api-collection).
2. At the left, select the Assinafy Collection.
3. At the right side, click on *fork* button to make a copy of the collection
   into your own workspace.
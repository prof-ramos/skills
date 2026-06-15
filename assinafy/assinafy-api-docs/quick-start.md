> Documentação extraída de [Assinafy API Reference](https://api.assinafy.com.br/v1/docs#quick-start)

# Quick Start

## Índice

- [Creating a User Account](#creating-a-user-account)
- [Setting Up Credentials](#setting-up-credentials)
  - [API Key](#api-key)
  - [Workspace Account ID](#workspace-account-id)
- [Uploading a Document](#uploading-a-document)
- [Creating Signers](#creating-signers)
- [Requesting Signatures](#requesting-signatures)
  - [Parameters](#parameters)

---



These are steps to quickly start using the API. At the end of it you will be
able to create a document and send signature invitation to signers.

## Creating a User Account

During the development of your application, we recommend creating a user account in our sandbox environment. To do this, please go to <https://app-sandbox.assinafy.com.br>.

Once your application is complete, use your user account from the production environment (<https://app.assinafy.com.br>).

For integrations using an API key, it is advisable to create a separate user account. For instance, you can create a user account named *My App*. This practice enables us to configure the minimum access necessary for the integration.

For enhanced security, create a separate user account for your integration, and assign a role accordingly.

## Setting Up Credentials

### API Key

To authenticate your application and gain access to Assinafy's API, you will need to generate an API key. Follow these steps to create your key:

1. Log in to your Assinafy account and navigate to the "My Account" page.
2. Select the "API" tab.
3. Follow the on-screen instructions to generate your unique API key.

- Assinafy app sandbox URL: <https://app-sandbox.assinafy.com.br>
- Assinafy app production URL: <https://app.assinafy.com.br>

Your API key should be used only from a back-end system. Avoid storing it in the
source code.
For any plans or credit purchase at the sandbox environment, please use the following credit card: `5510 3647 0363 3414`

### Workspace Account ID

To find the workspace account ID, go to the "My Account" page and look for the "Workspaces" tab.

## Uploading a Document

> Document Upload Request Using Curl

```
curl -X POST "https://api.assinafy.com.br/v1/accounts/615601fab04c0a31/documents" \
  -H 'X-Api-Key: hAvmvk6Urzus3byLD2qOWrghAvmvk6Urzus3byLD2qOWrg'\
  -F 'file=@/tmp/document.pdf'
```

> Document Upload Request Using PHP

```
<?php
// To install requirements:
// composer require guzzlehttp/guzzle

require 'vendor/autoload.php';

use GuzzleHttp\Client;

// Credentials
$workspace_account_id = 'YOUR_WORKSPACE_ACCOUNT_ID';
$api_key = 'YOUR_API_KEY';

$file_path = '/tmp/document.pdf';
$url = 'https://api.main.stage.assinafy.com.br/v1/accounts/' . $workspace_account_id . '/documents';

$client = new Client([
    'headers' => [
        'X-Api-Key' => $api_key,
    ]
]);

$response = $client->request('POST', $url, [
    'multipart' => [
        [
            'name' => 'file',
            'contents' => file_get_contents($file_path),
            'filename' => 'document.pdf'
        ]
    ]
]);

echo $response->getStatusCode() . "\n";
echo $response->getBody()->getContents() . "\n";
```

> Document Upload Request Using Python

```
# To install requirements:
# pip install requests

import requests

# Credentials
workspace_account_id = 'YOUR_WORKSPACE_ACCOUNT_ID'
api_key = 'YOUR_API_KEY'

file_path = '/tmp/document.pdf'
url = 'https://api-staging.assinafy.com.br/v1/accounts/' + workspace_account_id + '/documents'

with open(file_path, 'rb') as file:
    files = {'file': file}
    headers = {'X-Api-Key': api_key}
    response = requests.post(url, headers=headers, files=files)

print(response.status_code)
print(response.json())
```

> 200 OK - Document Upload Response

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

Upload a document from a local file and save the resulted ID to be used later.

`POST /accounts/{account_id}/documents`

| Parameter | Type | Description |
| --- | --- | --- |
| X-Api-Key | Header | The API key. |
| account\_id | URL | The workspace account ID. |

Both *account\_id* URL parameter and *X-APU-Key* header parameter are obtained
as shown in previous steps.

Please follow the examples here to create a document from an uploaded file.

You may find more information in the [document](#document) session.

## Creating Signers

> Create Signer

```
curl "https://api.assinafy.com.br/v1/accounts/e2d6ee35c7741ca4006b9e1a/signers" \
  -H 'X-Api-Key: hAvmvk6Urzus3byLD2qOWrghAvmvk6Urzus3byLD2qOWrg'\
  -H 'Content-Type: application/json' \
  -d '
{
  "full_name": "John Dove",
  "email": "[email protected]"
}
'
```

> 200 OK - Signer Creation Response

```
{
  "status": 200,
  "message": "",
  "data": {
    "resource": "signer",
    "id": "62d6ee35c7741ca4006b9e11",
    "full_name": "John Signer",
    "email": "[email protected]"
  }
}
```

Create signers and save the resulted IDs to be used later.

`POST /accounts/{account_id}/signers`

Find more information in the [signer](#signer) session.

## Requesting Signatures

> Curl Request - Invitation to Sign a Document

```
curl -X POST https://api.assinafy.com.br/v1/documents/60f720572d7fecf7c16c8463/assignments
  -H 'X-Api-Key: f720572d7fecf7c16c8463f720572d7fecf7c16c8463f72' \
  -H 'Content-Type: application/json' \
  -d '
{
  "method": "virtual",
  "signerIds": [
    "615605f50e968054a5b7c9b8"
  ]
}'
```

Invite signers to sign a document using the *virtual* method.

`POST /documents/{document_id}/assignments`

### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| X-Api-Key | Header | The API Key. |
| document\_id | URL | The document ID from the upload request. |
| method | Body | Should be *virtual*. |
| signerIds[] | Body | Array with of signers IDs. |

The *virtual* method will not require any input from the signer. To request
signatures with input fields, the *collect* method should be used. For further
details on how to implement this method, please refer to the
[assignment](#assignment) section.
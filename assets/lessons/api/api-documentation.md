---
title: Documenting Your API
summary: Make your API easy for app developers (and future you) to use.
minutes: 6
---
An undocumented API is a broken API. Developers need to know every endpoint, what to send and what comes back.

## What good docs include

- Base URL and versioning
- How to authenticate (getting and sending tokens)
- Every endpoint: method, URL, parameters, an example request and response
- Error format and error codes
- Rate limits

## Generate docs automatically

Popular packages read your routes, form requests and resources:

- **Scramble** (`dedoc/scramble`): generates an OpenAPI spec and a docs UI with zero annotations
- **Scribe** (`knuckleswtf/scribe`): docs plus Postman and OpenAPI exports

```bash
composer require dedoc/scramble
# visit /docs/api
```

## OpenAPI

OpenAPI (formerly Swagger) is the standard format for describing APIs. Tools turn it into interactive docs, client SDKs (including Dart for Flutter) and tests.

:::tip
Give app developers a **Postman/Bruno collection** or an **OpenAPI file**. They can then try every endpoint in minutes.
:::

```quiz
[
 {"q": "What is OpenAPI?", "options": ["A PHP framework", "A standard format for describing HTTP APIs", "A database", "A hosting company"], "answer": 1, "why": "OpenAPI specs describe endpoints, inputs and outputs."}
]
```

---
title: HTTP Methods, Status Codes & JSON
summary: The vocabulary every API developer must know.
minutes: 9
---
## Methods (verbs)

| Method | Meaning | Example |
|---|---|---|
| GET | Read | `GET /api/books` |
| POST | Create | `POST /api/books` |
| PUT | Replace | `PUT /api/books/1` |
| PATCH | Update some fields | `PATCH /api/books/1` |
| DELETE | Remove | `DELETE /api/books/1` |

GET, PUT and DELETE are **idempotent**: repeating them has the same effect as doing it once. POST is not, because each call creates something new.

## Status codes

| Code | Meaning | When |
|---|---|---|
| 200 | OK | Successful read or update |
| 201 | Created | POST created something |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Malformed request |
| 401 | Unauthenticated | Missing or invalid token |
| 403 | Forbidden | Logged in but not allowed |
| 404 | Not Found | No such resource |
| 405 | Method Not Allowed | Wrong verb for this URL |
| 422 | Unprocessable Content | Validation failed |
| 429 | Too Many Requests | Rate limit hit |
| 500 | Server Error | A bug on the server |

:::tip
Remember the families: **2xx** success, **4xx** the client made a mistake, **5xx** the server made a mistake.
:::

## JSON

```json
{
  "id": 7,
  "title": "Clean Code",
  "price": 19.99,
  "in_stock": true,
  "tags": ["programming", "classic"],
  "author": { "name": "Robert C. Martin" },
  "isbn": null
}
```

JSON has strings, numbers, booleans, `null`, arrays and objects. Keys are always double-quoted strings.

## Important headers

- `Accept: application/json`: "please reply with JSON". Laravel then returns JSON errors instead of HTML pages.
- `Content-Type: application/json`: "my request body is JSON".
- `Authorization: Bearer <token>`: who I am.

```quiz
[
 {"q": "Which status code means validation failed?", "options": ["400", "404", "422", "500"], "answer": 2, "why": "Laravel returns 422 Unprocessable Content for validation errors."},
 {"q": "Which code should a successful POST that created a resource return?", "options": ["200", "201", "204", "302"], "answer": 1, "why": "201 Created."},
 {"q": "What does 401 mean?", "options": ["Not found", "Not authenticated", "Forbidden", "Rate limited"], "answer": 1, "why": "401 means the request lacks valid credentials."},
 {"q": "Why send Accept: application/json to Laravel?", "options": ["Faster responses", "Errors come back as JSON instead of HTML", "Required for GET", "It enables CORS"], "answer": 1, "why": "Laravel renders JSON responses when the client expects JSON."}
]
```

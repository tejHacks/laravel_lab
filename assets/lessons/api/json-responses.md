---
title: JSON Responses
summary: Control status codes, headers and the shape of your responses.
minutes: 7
---
```php
// Arrays and models are converted automatically (status 200)
return ['message' => 'Hello'];
return $book;

// Full control
return response()->json(['message' => 'Created'], 201);
return response()->json($book, 201, ['X-Request-Id' => $id]);

// No body
return response()->noContent();          // 204

// Errors
abort(404, 'Book not found');            // {"message": "Book not found"}
abort_if(! $book->published, 403, 'Not published yet.');
```

## A consistent envelope

Pick one shape and use it everywhere. Laravel's API Resources use a `data` key:

```json
{
  "data": { "id": 1, "title": "..." },
  "meta": { "request_id": "..." }
}
```

Errors from Laravel look like this:

```json
{
  "message": "The title field is required.",
  "errors": {
    "title": ["The title field is required."]
  }
}
```

:::tip
In Laravel 13, `bootstrap/app.php` already makes every `api/*` URL (and any request sending `Accept: application/json`) render errors as JSON, so mobile apps never receive HTML error pages.
:::

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->shouldRenderJsonWhen(
        fn (Request $request) => $request->is('api/*') || $request->expectsJson(),
    );
})
```

```quiz
[
 {"q": "What does response()->noContent() return?", "options": ["200 with {}", "204 with no body", "404", "null"], "answer": 1, "why": "noContent() sends 204 No Content."},
 {"q": "What shape does Laravel use for validation errors?", "options": ["{error: ''}", "{message: ..., errors: {field: [...]}}", "A plain string", "HTML"], "answer": 1, "why": "A message plus an errors object keyed by field name."}
]
```

---
title: Your First API Routes
summary: install:api, routes/api.php and returning JSON.
minutes: 8
---
New Laravel apps don't include API routes until you ask:

```bash
php artisan install:api
```

This installs **Laravel Sanctum** (token auth), creates `routes/api.php` and adds the `personal_access_tokens` migration. Every route in `routes/api.php` is automatically prefixed with **`/api`**.

```php
// routes/api.php
use Illuminate\Support\Facades\Route;

Route::get('/ping', fn () => ['pong' => true, 'time' => now()->toIso8601String()]);

Route::get('/books', fn () => \App\Models\Book::all());

Route::get('/books/{book}', fn (\App\Models\Book $book) => $book);
```

```bash
curl http://localhost:8000/api/ping
# {"pong":true,"time":"2026-11-19T10:00:00+00:00"}
```

## API routes vs web routes

| | `routes/web.php` | `routes/api.php` |
|---|---|---|
| URL prefix | none | `/api` |
| Sessions and cookies | yes | no (stateless) |
| CSRF protection | yes | no |
| Auth | session login | tokens (Sanctum) |

## Testing your API by hand

- **curl** in the terminal
- **Postman**, **Insomnia**, **Bruno** or **HTTPie** desktop apps
- The VS Code **REST Client** extension
- This app's **API Playground** page

```bash
curl -X POST http://localhost:8000/api/v1/books \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"title": "Purple Hibiscus", "author": "Chimamanda Ngozi Adichie"}'
```

```quiz
[
 {"q": "What prefix do routes in routes/api.php get?", "options": ["/v1", "/api", "/json", "none"], "answer": 1, "why": "API routes are registered under /api."},
 {"q": "Which command adds API routes and Sanctum?", "options": ["php artisan make:api", "php artisan install:api", "composer require api", "php artisan api:init"], "answer": 1, "why": "install:api sets up routes/api.php and Sanctum."},
 {"q": "Do API routes use CSRF tokens?", "options": ["Yes", "No, they are stateless and use tokens", "Only for GET", "Only in production"], "answer": 1, "why": "API routes don't use sessions or CSRF."}
]
```

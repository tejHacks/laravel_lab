=== FILE: what-is-an-api.md ===
---
title: What is an API?
summary: How apps talk to servers, and why your mobile app needs one.
minutes: 6
---
An **API** (Application Programming Interface) is a set of URLs that **programs** call to get or change data. A website returns HTML for humans. An API returns **JSON** for code.

:::analogy
An API is a restaurant waiter. Your app (the customer) never walks into the kitchen (the database). It gives an order to the waiter (the API), who brings back exactly what was asked for.
:::

## Where APIs are used

- A **Flutter** or React Native app loading products from your server
- A **React/Vue** single-page app
- Other companies integrating with you (payments, shipping, webhooks)
- Your own backend services talking to each other

## A request and a response

```http
GET /api/v1/books/1 HTTP/1.1
Host: myapp.test
Accept: application/json
Authorization: Bearer 1|Xyz...
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": {
    "id": 1,
    "title": "Things Fall Apart",
    "author": "Chinua Achebe",
    "published_year": 1958
  }
}
```

## Why Laravel for APIs?

Routing, validation, authentication (**Sanctum**), JSON transformation (**API Resources**), pagination, rate limiting and testing are all built in. One Laravel backend can serve your website, your iPhone app and your Android app at the same time.

```quiz
[
 {"q": "What format do most web APIs return?", "options": ["HTML", "JSON", "PDF", "CSV only"], "answer": 1, "why": "JSON is the standard data format for web APIs."},
 {"q": "Who is the main consumer of an API?", "options": ["Humans reading pages", "Other programs and apps", "Search engines only", "Printers"], "answer": 1, "why": "APIs are designed for code: mobile apps, front ends and other services."}
]
```

=== FILE: http-and-json.md ===
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

=== FILE: first-api-routes.md ===
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

=== FILE: json-responses.md ===
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

=== FILE: rest-design.md ===
---
title: Designing a REST API
summary: URLs, nouns, nesting and conventions that make APIs easy to use.
minutes: 8
---
**REST** is a style of API design built on resources (nouns) and HTTP verbs.

## Good URL design

```text
GET    /api/v1/books              list books
POST   /api/v1/books              create a book
GET    /api/v1/books/12           one book
PATCH  /api/v1/books/12           update a book
DELETE /api/v1/books/12           delete a book
GET    /api/v1/authors/3/books    books by author 3 (nested)
```

## Rules of thumb

- Use **plural nouns**: `/books`, not `/getBooks` or `/book`.
- Let the **HTTP verb** say what happens. Never `/books/delete/12`.
- Use **snake_case** JSON keys consistently (Laravel's default): `published_year`.
- Return the **created resource** with **201** after POST.
- **Paginate** every list; never return 100,000 rows at once.
- **Version** your API (`/v1/`) so you can change things later without breaking old apps.
- Use **ISO 8601** dates: `2026-11-19T10:00:00Z`.

## Filtering, sorting and searching with query strings

```text
GET /api/v1/books?search=achebe&genre=fiction&sort=-published_year&page=2&per_page=20
```

## Actions that aren't CRUD

Sometimes an action doesn't fit. Use a sub-resource:

```text
POST /api/v1/orders/42/cancel
POST /api/v1/books/12/favorite
DELETE /api/v1/books/12/favorite
```

:::note
Mobile apps can't be force-updated instantly; people keep old versions for months. That's why **never break existing endpoints** matters so much. Add new fields freely, but don't remove or rename them without a new version.
:::

```quiz
[
 {"q": "Which URL follows REST conventions to delete book 5?", "options": ["POST /deleteBook?id=5", "GET /books/5/delete", "DELETE /books/5", "DELETE /book-delete/5"], "answer": 2, "why": "Use the resource URL plus the DELETE verb."},
 {"q": "Why version an API (/v1)?", "options": ["SEO", "To change it later without breaking old clients", "It's faster", "Laravel requires it"], "answer": 1, "why": "Old app versions keep working while new ones use v2."}
]
```

=== FILE: api-controllers.md ===
---
title: API Resource Controllers & Validation
summary: Build full CRUD endpoints with apiResource and form requests.
minutes: 11
---
```bash
php artisan make:model Book -mf
php artisan make:controller Api/V1/BookController --api --model=Book
php artisan make:request StoreBookRequest
```

```php
// routes/api.php
use App\Http\Controllers\Api\V1\BookController;

Route::prefix('v1')->group(function () {
    Route::apiResource('books', BookController::class);
});
```

`apiResource` registers `index`, `store`, `show`, `update` and `destroy` (no `create` or `edit` form pages).

```php
namespace App\Http\Controllers\Api\V1;

class BookController extends Controller
{
    public function index()
    {
        return BookResource::collection(Book::latest()->paginate(15));
    }

    public function store(StoreBookRequest $request)
    {
        $book = Book::create($request->validated());

        return (new BookResource($book))->response()->setStatusCode(201);
    }

    public function show(Book $book)
    {
        return new BookResource($book);
    }

    public function update(UpdateBookRequest $request, Book $book)
    {
        $book->update($request->validated());

        return new BookResource($book);
    }

    public function destroy(Book $book)
    {
        $book->delete();

        return response()->noContent();
    }
}
```

```php
class StoreBookRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:200'],
            'author' => ['required', 'string', 'max:120'],
            'published_year' => ['nullable', 'integer', 'between:1000,' . date('Y')],
            'genre' => ['nullable', Rule::in(['fiction', 'non-fiction', 'poetry', 'tech'])],
        ];
    }
}

class UpdateBookRequest extends StoreBookRequest
{
    public function rules(): array
    {
        // 'sometimes': validate only the fields that were sent (for PATCH)
        return collect(parent::rules())
            ->map(fn ($rules) => ['sometimes', ...$rules])
            ->all();
    }
}
```

:::tip
For an API request, a failed validation automatically returns **422** with JSON errors. You don't write any error-handling code.
:::

```quiz
[
 {"q": "Which routes does apiResource NOT create?", "options": ["index & show", "create & edit", "store & update", "destroy"], "answer": 1, "why": "APIs don't need HTML form pages."},
 {"q": "What does the 'sometimes' rule do?", "options": ["Validates randomly", "Validates the field only if it's present", "Makes it required", "Skips validation"], "answer": 1, "why": "Ideal for PATCH, where clients send only changed fields."},
 {"q": "What should destroy() return?", "options": ["200 with the deleted model", "204 No Content", "302 redirect", "500"], "answer": 1, "why": "204 is the conventional success response for DELETE."}
]
```

=== FILE: api-resources.md ===
---
title: API Resources (Transformers)
summary: Control exactly what JSON your API returns.
minutes: 10
---
Returning models directly leaks your database structure (and maybe secret columns) to clients. An **API Resource** is a transformer that decides exactly what goes out.

```bash
php artisan make:resource BookResource
```

```php
class BookResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'author' => $this->author,
            'published_year' => $this->published_year,
            'is_classic' => $this->published_year && $this->published_year < 1980,
            'reviews_count' => $this->whenCounted('reviews'),
            'reviews' => ReviewResource::collection($this->whenLoaded('reviews')),
            'created_at' => $this->created_at?->toIso8601String(),
            'links' => ['self' => route('books.show', $this->resource)],
        ];
    }
}
```

```php
return new BookResource($book);                      // {"data": {...}}
return BookResource::collection($books);             // {"data": [...]}
return BookResource::collection(Book::paginate());   // adds "links" and "meta"
return $book->toResource();                          // finds BookResource by convention
```

## Conditional attributes

```php
'email' => $this->when($request->user()?->is_admin, $this->email),
'secret' => $this->when(false, 'never shown'),
$this->mergeWhen($this->is_published, ['published_at' => $this->published_at]),
'author' => new AuthorResource($this->whenLoaded('author')),   // only if eager-loaded
```

`whenLoaded` avoids N+1 queries: the relation appears only if you eager-loaded it with `->with('author')`.

## Paginated collection output

```json
{
  "data": [ { "id": 1, "title": "..." } ],
  "links": { "first": "...?page=1", "last": "...?page=4", "prev": null, "next": "...?page=2" },
  "meta": { "current_page": 1, "per_page": 15, "total": 52, "last_page": 4 }
}
```

```quiz
[
 {"q": "Why use API Resources instead of returning models?", "options": ["Speed only", "Control and stabilise the JSON shape and hide internals", "They're required", "To validate input"], "answer": 1, "why": "Resources decouple your API contract from database columns."},
 {"q": "What does $this->whenLoaded('reviews') do?", "options": ["Always loads reviews", "Includes reviews only if they were eager-loaded", "Counts reviews", "Deletes reviews"], "answer": 1, "why": "It prevents surprise N+1 queries."},
 {"q": "What key wraps a single resource by default?", "options": ["result", "item", "data", "payload"], "answer": 2, "why": "JsonResource wraps output in a data key."}
]
```

=== FILE: pagination-filtering.md ===
---
title: Pagination, Filtering & Sorting
summary: Let clients ask for exactly the data they need.
minutes: 9
---
```php
public function index(Request $request)
{
    $request->validate([
        'search' => ['nullable', 'string', 'max:100'],
        'genre' => ['nullable', 'string'],
        'sort' => ['nullable', Rule::in(['title', '-title', 'published_year', '-published_year'])],
        'per_page' => ['nullable', 'integer', 'between:1,100'],
    ]);

    $sort = $request->input('sort', '-published_year');
    $direction = str_starts_with($sort, '-') ? 'desc' : 'asc';

    $books = Book::query()
        ->when($request->search, fn ($q, $s) => $q->where(fn ($q) => $q
            ->where('title', 'like', "%{$s}%")
            ->orWhere('author', 'like', "%{$s}%")))
        ->when($request->genre, fn ($q, $g) => $q->where('genre', $g))
        ->orderBy(ltrim($sort, '-'), $direction)
        ->paginate($request->integer('per_page', 15))
        ->withQueryString();   // keep filters in the next/prev links

    return BookResource::collection($books);
}
```

```text
GET /api/v1/books?search=adichie&sort=-published_year&per_page=5&page=2
```

:::warning
**Always whitelist** sortable columns (as with `Rule::in` above). Passing user input straight into `orderBy()` lets clients sort by any column, including private ones.
:::

## Cursor pagination for infinite scroll

```php
return BookResource::collection(Book::orderBy('id')->cursorPaginate(20));
// meta.next_cursor: pass ?cursor=... to get the next page
```

Cursor pagination stays fast on huge tables and never skips or repeats items when new rows are added, which makes it perfect for mobile feeds.

```quiz
[
 {"q": "Why validate the sort parameter with Rule::in?", "options": ["Style", "To prevent sorting by arbitrary or private columns", "Speed", "Laravel requires it"], "answer": 1, "why": "Whitelisting stops clients from abusing orderBy."},
 {"q": "What does ->withQueryString() do?", "options": ["Adds SQL", "Keeps current query parameters in pagination links", "Caches the query", "Removes filters"], "answer": 1, "why": "Next/prev links keep ?search=... and other filters."},
 {"q": "Which pagination suits infinite scrolling feeds best?", "options": ["paginate", "cursorPaginate", "get()", "chunk"], "answer": 1, "why": "Cursor pagination is fast and stable for feeds."}
]
```

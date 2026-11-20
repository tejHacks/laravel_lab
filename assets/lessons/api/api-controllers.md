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

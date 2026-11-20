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

---
title: Caching & Performance
summary: Make your API fast under load.
minutes: 9
---
## Avoid N+1 queries

```php
// ❌ 1 + N queries
return BookResource::collection(Book::paginate());   // resource reads $book->author

// ✅ 2 queries
return BookResource::collection(Book::with('author')->withCount('reviews')->paginate());
```

## Cache expensive results

```php
use Illuminate\Support\Facades\Cache;

$stats = Cache::remember('dashboard-stats', now()->addMinutes(10), fn () => [
    'books' => Book::count(),
    'top_genres' => Book::selectRaw('genre, count(*) as total')->groupBy('genre')->orderByDesc('total')->limit(5)->get(),
]);

Cache::forget('dashboard-stats');   // clear it when the data changes
```

Laravel's cache drivers include `database` (the default), `file`, `redis` and `memcached`. Use **Redis** in production for speed.

## Select only what you need

```php
Book::select(['id', 'title', 'author'])->paginate();
```

## Index your database

```php
$table->index('genre');
$table->index(['author_id', 'published_year']);
```

Columns you filter or sort by often should be indexed.

## HTTP caching

```php
return BookResource::collection($books)
    ->response()
    ->setEtag(md5($books->toJson()))
    ->setPublic()
    ->setMaxAge(60);
```

## Measure first

Use **Laravel Telescope** or **Debugbar** locally to see every query, and **Pulse** or **Nightwatch** in production to spot slow endpoints.

```quiz
[
 {"q": "What does Cache::remember do?", "options": ["Always recomputes", "Returns the cached value or computes and stores it", "Deletes cache", "Locks the database"], "answer": 1, "why": "It caches the closure's result for the given time."},
 {"q": "Best fix for N+1 queries in resources?", "options": ["More servers", "Eager load with with()", "Disable resources", "Use raw SQL everywhere"], "answer": 1, "why": "Eager loading fetches relations in bulk."}
]
```

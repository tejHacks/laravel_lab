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

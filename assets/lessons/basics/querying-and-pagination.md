---
title: Querying, Scopes & Pagination
summary: Filter, sort, reuse queries with scopes, and paginate results.
minutes: 9
---
## Building queries

```php
$tasks = Task::query()
    ->where('done', false)
    ->whereDate('due_on', '<=', today())
    ->whereIn('priority', [1, 2])
    ->when($request->search, fn ($q, $term) => $q->where('title', 'like', "%{$term}%"))
    ->orderByDesc('priority')
    ->get();
```

`when()` only adds the condition if the first argument is truthy, which is perfect for optional filters.

## Local scopes with `#[Scope]`

Reuse common conditions:

```php
use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;

class Task extends Model
{
    #[Scope]
    protected function pending(Builder $query): void
    {
        $query->where('done', false);
    }

    #[Scope]
    protected function dueBefore(Builder $query, $date): void
    {
        $query->whereDate('due_on', '<', $date);
    }
}

Task::pending()->dueBefore(now())->get();
```

## Pagination

```php
$tasks = Task::latest()->paginate(10);         // ?page=2
$tasks = Task::latest()->simplePaginate(10);   // only next/previous
$tasks = Task::latest()->cursorPaginate(10);   // fastest for huge tables
```

```blade
@foreach ($tasks as $task) ... @endforeach

{{ $tasks->links() }}                  {{-- page links --}}
{{ $tasks->withQueryString()->links() }} {{-- keep ?search=... --}}
```

## Aggregates

```php
Task::count();
Task::where('done', true)->count();
Order::sum('total');
Order::avg('total');
Task::max('priority');
```

## Collections

`get()` returns a **Collection** with dozens of helpers:

```php
$titles = $tasks->pluck('title');
$byCat  = $tasks->groupBy('category.name');
$late   = $tasks->filter(fn ($t) => $t->is_overdue);
$sum    = $orders->sum('total');
```

```quiz
[
 {"q": "What does ->when($term, fn ...) do?", "options": ["Always adds the condition", "Adds the condition only if $term is truthy", "Delays the query", "Caches the query"], "answer": 1, "why": "when() applies the callback conditionally, ideal for optional filters."},
 {"q": "How do you call a scope declared as `#[Scope] protected function pending()`?", "options": ["Task::scopePending()", "Task::pending()", "Task::scope('pending')", "Task::wherePending()"], "answer": 1, "why": "Scopes are called by their method name."},
 {"q": "Which paginator is best for very large tables?", "options": ["paginate", "simplePaginate", "cursorPaginate", "chunk"], "answer": 2, "why": "Cursor pagination avoids slow OFFSET queries."}
]
```

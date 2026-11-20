---
title: Collections in Depth
summary: Laravel's most-used power tool for working with data.
minutes: 9
---
Eloquent queries return **Collections**, and you can wrap any array with `collect()`.

```php
$orders = collect([
    ['customer' => 'Ada', 'total' => 120, 'status' => 'paid'],
    ['customer' => 'Tunde', 'total' => 80, 'status' => 'pending'],
    ['customer' => 'Ada', 'total' => 45, 'status' => 'paid'],
]);

$orders->where('status', 'paid')->sum('total');            // 165
$orders->groupBy('customer')->map->sum('total');           // ['Ada' => 165, 'Tunde' => 80]
$orders->sortByDesc('total')->first()['customer'];         // 'Ada'
$orders->pluck('customer')->unique()->values();            // ['Ada', 'Tunde']
$orders->partition(fn ($o) => $o['status'] === 'paid');    // [paid, others]
$orders->keyBy('customer');
$orders->chunk(2);
$orders->avg('total');                                     // 81.66...
```

## Higher-order messages

```php
$users->each->notify(new Welcome);
$tasks->filter->is_overdue;
$orders->sum->total;
```

## Lazy collections for huge datasets

```php
// Streams rows one by one instead of loading 1 million into memory
User::lazy()->each(function (User $user) {
    // ...
});
```

:::tip
Learn `map`, `filter`, `reduce`, `groupBy`, `pluck`, `sortBy`, `firstWhere` and `sum` first. They cover 90% of day-to-day needs.
:::

```quiz
[
 {"q": "What does groupBy('customer')->map->sum('total') return?", "options": ["Total of all orders", "Each customer's total", "Number of customers", "The first order"], "answer": 1, "why": "Group per customer, then sum each group."},
 {"q": "Why use lazy() on huge tables?", "options": ["It's prettier", "It streams rows to keep memory low", "It caches", "It sorts faster"], "answer": 1, "why": "Lazy collections avoid loading everything at once."}
]
```

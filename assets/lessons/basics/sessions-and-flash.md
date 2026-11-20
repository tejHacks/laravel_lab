---
title: Sessions & Flash Messages
summary: Remember data between requests and show one-time messages.
minutes: 6
---
HTTP is **stateless**: every request is independent. A **session** lets you remember things between requests (who is logged in, a shopping cart, preferences).

```php
// Store
session(['theme' => 'dark']);
$request->session()->put('cart', $items);
$request->session()->push('cart', $newItem);

// Read
$theme = session('theme', 'light');     // default 'light'
$cart = $request->session()->get('cart', []);

// Remove
$request->session()->forget('cart');
```

## Flash data: available for the next request only

Perfect for "Saved!" messages after a redirect:

```php
return redirect()->route('tasks.index')->with('status', 'Task saved!');
```

```blade
@session('status')
    <div class="alert success">{{ $value }}</div>
@endsession
```

## Where are sessions stored?

`SESSION_DRIVER` in `.env`: `database` (the default in new apps), `file`, `cookie`, `redis` and others.

:::analogy
A session is like a coat-check ticket. The browser keeps a small cookie (the ticket) and the server keeps the coat (the data).
:::

```quiz
[
 {"q": "How long does flashed data last?", "options": ["Forever", "Until logout", "Only the next request", "One hour"], "answer": 2, "why": "Flash data is removed after the next request."},
 {"q": "Which directive shows a flashed 'status' message?", "options": ["@flash('status')", "@session('status')", "@status", "@message"], "answer": 1, "why": "@session('key') ... @endsession exposes $value."}
]
```

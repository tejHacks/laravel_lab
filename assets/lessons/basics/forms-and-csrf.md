---
title: Forms & CSRF Protection
summary: Send data from HTML forms safely and keep old input after errors.
minutes: 8
---
```blade
<form method="POST" action="{{ route('tasks.store') }}">
    @csrf

    <label for="title">Title</label>
    <input id="title" name="title" value="{{ old('title') }}">
    @error('title')
        <p class="error">{{ $message }}</p>
    @enderror

    <button type="submit">Save</button>
</form>
```

## What is `@csrf`?

**CSRF** (Cross-Site Request Forgery) is an attack where another website tricks your browser into submitting a form to your app. `@csrf` adds a hidden secret token. Laravel rejects POST, PUT, PATCH and DELETE requests without a valid token, returning **419 Page Expired**.

:::warning
Forgot `@csrf`? You'll see **419 Page Expired**. Add the directive inside every form.
:::

## PUT, PATCH and DELETE from HTML

HTML forms only support GET and POST, so Laravel "spoofs" the method:

```blade
<form method="POST" action="{{ route('tasks.destroy', $task) }}">
    @csrf
    @method('DELETE')
    <button>Delete</button>
</form>
```

## Reading the input in a controller

```php
public function store(Request $request)
{
    $title = $request->input('title');
    $all   = $request->all();
    $only  = $request->only(['title', 'due_date']);
    $done  = $request->boolean('done');    // "on", "1" and "true" all become true
    $has   = $request->filled('notes');    // present and not empty

    // ...
}
```

## Keeping old input

When validation fails, Laravel redirects back and flashes the input. `old('title')` refills the field so users don't retype everything.

```quiz
[
 {"q": "What error do you get when @csrf is missing?", "options": ["404", "403", "419 Page Expired", "500"], "answer": 2, "why": "Laravel returns 419 when the CSRF token is missing or invalid."},
 {"q": "How do you send a DELETE request from an HTML form?", "options": ["method=\"DELETE\"", "POST + @method('DELETE')", "GET + ?delete=1", "You can't"], "answer": 1, "why": "Use method POST and the @method('DELETE') directive."},
 {"q": "What does old('title') return?", "options": ["The database value", "The previously submitted input after a failed validation", "The route name", "null always"], "answer": 1, "why": "old() reads flashed input from the previous request."}
]
```

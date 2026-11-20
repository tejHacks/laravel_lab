---
title: Validation
summary: Never trust user input. Validate it.
minutes: 10
---
Every piece of user input must be checked before you save it. Laravel makes this one line.

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title'   => ['required', 'string', 'max:120'],
        'email'   => ['required', 'email', 'unique:users,email'],
        'age'     => ['nullable', 'integer', 'between:13,120'],
        'due_on'  => ['nullable', 'date', 'after_or_equal:today'],
        'tags'    => ['array', 'max:5'],
        'tags.*'  => ['string', 'distinct'],
        'avatar'  => ['nullable', 'image', 'max:2048'],   // KB
    ]);

    Task::create($validated);   // only validated fields
}
```

## What happens when validation fails?

- **Web request**: Laravel redirects **back** with the errors and the old input. Show them with `@error` and `old()`.
- **JSON / API request**: Laravel returns **422 Unprocessable Content** with the errors as JSON.

```blade
@if ($errors->any())
    <ul class="errors">
        @foreach ($errors->all() as $error) <li>{{ $error }}</li> @endforeach
    </ul>
@endif

<input name="title" value="{{ old('title') }}" @class(['invalid' => $errors->has('title')])>
@error('title') <small>{{ $message }}</small> @enderror
```

## Useful rules

`required`, `nullable`, `string`, `integer`, `numeric`, `boolean`, `email`, `url`, `min`, `max`, `between`, `in:a,b,c`, `confirmed` (needs `password_confirmation`), `same`, `different`, `date`, `before`, `after`, `exists:table,column`, `unique:table,column`, `regex`, `file`, `image`, `mimes:pdf,docx`.

## Rule objects

```php
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Password;

'status'   => ['required', Rule::in(['draft', 'published'])],
'email'    => ['required', 'email', Rule::unique('users')->ignore($user->id)],
'password' => ['required', 'confirmed', Password::min(8)->letters()->numbers()],
```

## Custom messages

```php
$request->validate(
    ['title' => 'required'],
    ['title.required' => 'Please give your task a title.']
);
```

:::warning
Use `$validated` (the return value) or `$request->validated()`, never `$request->all()`, when saving. That way only checked fields reach the database.
:::

```quiz
[
 {"q": "What does a failed validation return for an API (JSON) request?", "options": ["A redirect", "422 with JSON errors", "500", "200 with errors"], "answer": 1, "why": "JSON requests get a 422 response listing the errors."},
 {"q": "Which rule requires a matching password_confirmation field?", "options": ["same", "confirmed", "match", "equals"], "answer": 1, "why": "'confirmed' expects {field}_confirmation."},
 {"q": "How do you ignore the current user in a unique email rule when editing?", "options": ["unique:users,email,skip", "Rule::unique('users')->ignore($user->id)", "unique:except", "You can't"], "answer": 1, "why": "Rule::unique(...)->ignore($id) excludes that row."}
]
```

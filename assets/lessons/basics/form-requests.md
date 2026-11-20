---
title: Form Requests
summary: Move validation and authorization into dedicated classes.
minutes: 8
---
When validation grows, move it out of the controller into a **Form Request**.

```bash
php artisan make:request StoreTaskRequest
```

```php
namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\StopOnFirstFailure;
use Illuminate\Foundation\Http\FormRequest;

#[StopOnFirstFailure]   // Laravel 13 attribute: stop after the first failing rule
class StoreTaskRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;   // or: $this->user()->can('create', Task::class)
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:120'],
            'category_id' => ['nullable', 'exists:categories,id'],
            'due_on' => ['nullable', 'date'],
        ];
    }

    public function messages(): array
    {
        return ['title.required' => 'Every task needs a title.'];
    }

    protected function prepareForValidation(): void
    {
        $this->merge(['title' => trim((string) $this->title)]);
    }
}
```

Type-hint it in the controller. It is validated **before** your method runs:

```php
public function store(StoreTaskRequest $request)
{
    Task::create($request->validated());

    return to_route('tasks.index')->with('status', 'Task created!');
}
```

:::tip
Other Laravel 13 form-request attributes include `#[ErrorBag('login')]` (a named error bag) and `#[RedirectTo('/somewhere')]` (where to go when validation fails).
:::

```quiz
[
 {"q": "When does a Form Request validate?", "options": ["After the controller method", "Before the controller method runs", "Only on save()", "Never automatically"], "answer": 1, "why": "Laravel resolves and validates it before calling your method."},
 {"q": "What should authorize() return to allow the request?", "options": ["null", "true", "'yes'", "200"], "answer": 1, "why": "Returning false gives a 403 Forbidden response."}
]
```

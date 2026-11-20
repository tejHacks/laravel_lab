---
title: Authorization: Gates & Policies
summary: Decide what a logged-in user is allowed to do.
minutes: 9
---
**Authentication** = who are you? **Authorization** = what are you allowed to do?

## Gates (simple checks)

```php
// app/Providers/AppServiceProvider.php
use Illuminate\Support\Facades\Gate;

public function boot(): void
{
    Gate::define('view-reports', fn (User $user) => $user->is_admin);
}
```

```php
Gate::authorize('view-reports');          // throws 403 if denied
if ($request->user()->can('view-reports')) { ... }
```

## Policies (rules for one model)

```bash
php artisan make:policy TaskPolicy --model=Task
```

```php
class TaskPolicy
{
    public function update(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }

    public function delete(User $user, Task $task): bool
    {
        return $user->id === $task->user_id || $user->is_admin;
    }
}
```

Laravel finds `TaskPolicy` for `Task` automatically through naming conventions.

```php
public function update(UpdateTaskRequest $request, Task $task)
{
    Gate::authorize('update', $task);   // 403 if not the owner
    $task->update($request->validated());
    // ...
}
```

```php
Route::put('/tasks/{task}', ...)->can('update', 'task');
```

```blade
@can('delete', $task)
    <button>Delete</button>
@endcan
```

:::tip
Hiding a button with `@can` is only cosmetic. **Always** check in the controller too, because users can send requests without your UI.
:::

```quiz
[
 {"q": "What's the difference between authentication and authorization?", "options": ["They're the same", "Who you are vs what you may do", "Login vs logout", "Passwords vs tokens"], "answer": 1, "why": "Authentication identifies the user; authorization checks permissions."},
 {"q": "What does Gate::authorize('update', $task) do when denied?", "options": ["Returns false", "Throws, giving a 403 response", "Logs out", "Redirects to login"], "answer": 1, "why": "authorize throws an AuthorizationException, rendered as 403."},
 {"q": "Is @can in Blade enough to secure an action?", "options": ["Yes", "No, also check on the server", "Only for admins", "Only in production"], "answer": 1, "why": "UI checks are cosmetic; enforce permissions server-side."}
]
```

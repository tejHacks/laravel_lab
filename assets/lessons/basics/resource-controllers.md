---
title: Resource Controllers
summary: The 7 standard CRUD routes with one line.
minutes: 7
---
Most features need the same actions: list, show, create, store, edit, update and delete. A **resource controller** gives you all seven.

```bash
php artisan make:controller TaskController --resource --model=Task
```

```php
Route::resource('tasks', TaskController::class);
```

| Verb | URL | Method | Route name |
|---|---|---|---|
| GET | /tasks | index | tasks.index |
| GET | /tasks/create | create | tasks.create |
| POST | /tasks | store | tasks.store |
| GET | /tasks/{task} | show | tasks.show |
| GET | /tasks/{task}/edit | edit | tasks.edit |
| PUT/PATCH | /tasks/{task} | update | tasks.update |
| DELETE | /tasks/{task} | destroy | tasks.destroy |

```php
class TaskController extends Controller
{
    public function index()
    {
        return view('tasks.index', ['tasks' => Task::latest()->paginate(10)]);
    }

    public function store(Request $request)
    {
        $data = $request->validate(['title' => ['required', 'max:120']]);
        Task::create($data);

        return redirect()->route('tasks.index')->with('status', 'Task added!');
    }

    public function destroy(Task $task)
    {
        $task->delete();

        return back()->with('status', 'Task deleted.');
    }

    // show, create, edit, update...
}
```

## Only some routes

```php
Route::resource('photos', PhotoController::class)->only(['index', 'show']);
Route::resource('photos', PhotoController::class)->except(['destroy']);
Route::apiResource('posts', PostController::class); // no create/edit (for APIs)
```

:::tip
This app's **Tasks demo** is a real resource controller. Open it from the Demos menu, then read `app/Http/Controllers/Demo/TaskController.php`.
:::

```quiz
[
 {"q": "How many routes does Route::resource create?", "options": ["4", "5", "7", "10"], "answer": 2, "why": "index, create, store, show, edit, update, destroy."},
 {"q": "Which method handles POST /tasks?", "options": ["create", "store", "update", "index"], "answer": 1, "why": "store saves a new resource; create only shows the form."},
 {"q": "What does apiResource leave out?", "options": ["index and show", "create and edit", "store and update", "destroy"], "answer": 1, "why": "APIs don't need HTML form pages, so create and edit are skipped."}
]
```

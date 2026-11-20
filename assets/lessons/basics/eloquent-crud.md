---
title: CRUD with Eloquent
summary: Create, read, update and delete records.
minutes: 9
---
## Create

```php
$task = Task::create(['title' => 'Learn Eloquent', 'done' => false]);

$task = new Task;
$task->title = 'Write tests';
$task->save();
```

## Read

```php
Task::all();                                // every row (careful on big tables!)
Task::find(1);                              // by id, or null
Task::findOrFail(1);                        // by id, or a 404 error
Task::where('done', false)->get();          // a collection
Task::where('done', false)->first();        // one model or null
Task::where('title', 'like', '%report%')->count();
Task::latest()->take(5)->get();             // newest 5
Task::orderBy('due_on')->pluck('title');    // just one column
```

## Update

```php
$task = Task::findOrFail(1);
$task->update(['done' => true]);

// or
$task->done = true;
$task->save();

// many rows at once
Task::where('due_on', '<', now())->update(['overdue' => true]);
```

## Delete

```php
$task->delete();
Task::destroy([1, 2, 3]);
Task::where('done', true)->delete();
```

## Soft deletes

Keep deleted rows in the table but hide them:

```php
use Illuminate\Database\Eloquent\SoftDeletes;

class Task extends Model
{
    use SoftDeletes;   // add $table->softDeletes() in the migration
}

$task->delete();            // sets deleted_at
Task::withTrashed()->get(); // include deleted rows
$task->restore();
```

## Handy helpers

```php
Task::firstOrCreate(['title' => 'Inbox zero']);
Task::updateOrCreate(['title' => 'Gym'], ['done' => true]);
$task->wasRecentlyCreated;
$task->isDirty('title');  // changed but not saved yet?
```

:::tip
Use `findOrFail()` in controllers: a missing record becomes a clean 404 page instead of a crash.
:::

```quiz
[
 {"q": "What does findOrFail(99) do if row 99 doesn't exist?", "options": ["Returns null", "Throws, which becomes a 404", "Creates it", "Returns an empty model"], "answer": 1, "why": "It throws ModelNotFoundException, rendered as a 404."},
 {"q": "Which call returns a collection of models?", "options": ["Task::where(...)->first()", "Task::where(...)->get()", "Task::find(1)", "Task::count()"], "answer": 1, "why": "get() executes the query and returns a Collection."},
 {"q": "What does SoftDeletes do on delete()?", "options": ["Removes the row", "Sets deleted_at and hides the row", "Archives to a file", "Nothing"], "answer": 1, "why": "Soft-deleted rows stay in the table with a deleted_at timestamp."}
]
```

---
title: Eloquent Relationships
summary: hasMany, belongsTo, belongsToMany and eager loading.
minutes: 11
---
Real data is connected: a category **has many** tasks, a task **belongs to** a category, a post **has many** tags and a tag has many posts.

## One to many

```php
class Category extends Model
{
    public function tasks(): HasMany
    {
        return $this->hasMany(Task::class);   // uses tasks.category_id
    }
}

class Task extends Model
{
    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }
}
```

```php
$category->tasks;                         // collection of tasks
$category->tasks()->where('done', false)->get();
$task->category->name;                    // the parent
$category->tasks()->create(['title' => 'New']);  // sets category_id for you
```

## Many to many

Needs a **pivot table** named after both models in alphabetical order, for example `post_tag`:

```php
Schema::create('post_tag', function (Blueprint $table) {
    $table->foreignId('post_id')->constrained()->cascadeOnDelete();
    $table->foreignId('tag_id')->constrained()->cascadeOnDelete();
    $table->primary(['post_id', 'tag_id']);
});

class Post extends Model
{
    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class);
    }
}

$post->tags()->attach($tagId);
$post->tags()->detach($tagId);
$post->tags()->sync([1, 2, 3]);    // exactly these
```

## Other relationships

- `hasOne` / `belongsTo`: a user has one profile.
- `hasManyThrough`: country → users → posts.
- `morphMany` / `morphTo`: comments on posts **and** videos.

## Eager loading and the N+1 problem

```php
// ❌ 1 query for tasks + 1 query PER task for its category (N+1)
foreach (Task::all() as $task) {
    echo $task->category->name;
}

// ✅ 2 queries total
foreach (Task::with('category')->get() as $task) {
    echo $task->category->name;
}

Category::withCount('tasks')->get();   // $category->tasks_count
```

:::tip
Add `Model::preventLazyLoading(! app()->isProduction());` to `AppServiceProvider::boot()`. Laravel then throws an error whenever you accidentally cause an N+1 query during development.
:::

```quiz
[
 {"q": "A Task belongs to a Category. Which relationship goes on Task?", "options": ["hasMany", "belongsTo", "hasOne", "belongsToMany"], "answer": 1, "why": "The model holding the foreign key (category_id) uses belongsTo."},
 {"q": "What does Task::with('category') solve?", "options": ["Security", "The N+1 query problem", "Validation", "Pagination"], "answer": 1, "why": "Eager loading fetches related models in one extra query."},
 {"q": "What does sync([1,2]) do on a many-to-many relation?", "options": ["Adds 1 and 2", "Makes the related IDs exactly [1, 2]", "Deletes the tags", "Counts tags"], "answer": 1, "why": "sync attaches the missing IDs and detaches the rest."}
]
```

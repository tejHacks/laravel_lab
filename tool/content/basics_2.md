=== FILE: blade-basics.md ===
---
title: Blade Templates
summary: Laravel's templating engine: echoing data, conditionals and loops.
minutes: 9
---
**Blade** templates are HTML files with extra syntax. They live in `resources/views` and end with `.blade.php`.

```php
// Controller
return view('greeting', ['name' => 'Ada', 'tasks' => $tasks]);
```

```blade
{{-- resources/views/greeting.blade.php --}}
<h1>Hello, {{ $name }}!</h1>
```

## Echoing data safely

```blade
{{ $name }}            {{-- escaped: safe from XSS attacks --}}
{!! $trustedHtml !!}   {{-- NOT escaped: only for HTML you fully trust --}}
{{ $name ?? 'Guest' }} {{-- default value --}}
```

:::warning
Always use `{{ }}` for user input. `{!! !!}` prints raw HTML and can let attackers inject scripts.
:::

## Conditionals

```blade
@if ($tasks->isEmpty())
    <p>No tasks yet.</p>
@elseif ($tasks->count() === 1)
    <p>One task.</p>
@else
    <p>{{ $tasks->count() }} tasks.</p>
@endif

@auth   <a href="/logout">Log out</a>   @endauth
@guest  <a href="/login">Log in</a>     @endguest
@env('local') <div class="debug">Local mode</div> @endenv
```

## Loops

```blade
<ul>
@forelse ($tasks as $task)
    <li class="{{ $loop->first ? 'first' : '' }}">
        {{ $loop->iteration }}. {{ $task->title }}
    </li>
@empty
    <li>Nothing to do 🎉</li>
@endforelse
</ul>
```

`$loop` gives you `index`, `iteration`, `first`, `last`, `count` and more.

## Handy directives

```blade
<input type="checkbox" @checked($task->done)>
<option @selected($country === 'NG')>Nigeria</option>
<button @disabled($locked)>Save</button>
<div @class(['task', 'done' => $task->done])></div>
@json($data)   {{-- safely output PHP data as JSON for JavaScript --}}
```

```quiz
[
 {"q": "Which syntax escapes output to prevent XSS?", "options": ["{!! $x !!}", "{{ $x }}", "<?= $x ?>", "@raw($x)"], "answer": 1, "why": "{{ }} runs htmlspecialchars on the value."},
 {"q": "What does @forelse add compared to @foreach?", "options": ["Faster loops", "An @empty block when there are no items", "Pagination", "Sorting"], "answer": 1, "why": "@forelse lets you show something when the collection is empty."},
 {"q": "Which directive conditionally adds CSS classes?", "options": ["@style", "@class", "@css", "@if-class"], "answer": 1, "why": "@class(['a', 'b' => $cond]) builds a class list."}
]
```

=== FILE: layouts-and-components.md ===
---
title: Layouts & Components
summary: Reuse HTML with layouts, Blade components, slots and props.
minutes: 10
---
Most pages share the same header, navigation and footer. **Components** let you write that once.

## A layout component

```bash
php artisan make:component Layout --view
```

```blade
{{-- resources/views/components/layout.blade.php --}}
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ $title ?? 'My App' }}</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <nav>...</nav>
    <main>{{ $slot }}</main>
</body>
</html>
```

```blade
{{-- resources/views/home.blade.php --}}
<x-layout title="Home">
    <h1>Welcome!</h1>
</x-layout>
```

`{{ $slot }}` is replaced with whatever you put between the component tags.

## Props

```blade
{{-- resources/views/components/alert.blade.php --}}
@props(['type' => 'info'])

<div {{ $attributes->merge(['class' => "alert alert-$type"]) }}>
    {{ $slot }}
</div>
```

```blade
<x-alert type="success" class="mb-4">Saved!</x-alert>
<x-alert>Just so you know...</x-alert>
```

## Named slots

```blade
{{-- components/card.blade.php --}}
<div class="card">
    <header>{{ $header }}</header>
    {{ $slot }}
    @isset($footer) <footer>{{ $footer }}</footer> @endisset
</div>

<x-card>
    <x-slot:header>Profile</x-slot:header>
    <p>Content here</p>
    <x-slot:footer><a href="#">Edit</a></x-slot:footer>
</x-card>
```

## Passing PHP values

```blade
<x-alert :type="$status ? 'success' : 'error'">...</x-alert>
```

A colon (`:type`) means "this is a PHP expression", not a plain string.

:::note
The classic alternative is `@extends('layouts.app')` with `@section` and `@yield`. Components are the modern, recommended style.
:::

```quiz
[
 {"q": "What does {{ $slot }} output?", "options": ["Nothing", "The content between the component tags", "The layout title", "All props"], "answer": 1, "why": "The default slot holds the content passed inside <x-component>...</x-component>."},
 {"q": "How do you pass a PHP expression to a component prop?", "options": ["type=\"$x\"", ":type=\"$x\"", "@type($x)", "{type: $x}"], "answer": 1, "why": "Prefix the attribute with a colon."},
 {"q": "Where do anonymous component views live?", "options": ["resources/views/components", "app/View", "public/components", "resources/components"], "answer": 0, "why": "<x-alert> maps to resources/views/components/alert.blade.php."}
]
```

=== FILE: forms-and-csrf.md ===
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

=== FILE: databases-and-migrations.md ===
---
title: Databases & Migrations
summary: Version-control your database schema with migrations.
minutes: 10
---
A **migration** is a PHP file that describes a change to your database: create a table, add a column, add an index. Migrations are like Git for your database schema, so every developer and server gets the same structure.

## Configure the database

```dotenv
# SQLite (default, zero setup)
DB_CONNECTION=sqlite

# MySQL / MariaDB / PostgreSQL
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=my_app
DB_USERNAME=root
DB_PASSWORD=secret
```

## Create a migration

```bash
php artisan make:migration create_tasks_table
```

```php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tasks', function (Blueprint $table) {
            $table->id();                                   // big integer primary key
            $table->string('title', 120);
            $table->text('notes')->nullable();
            $table->boolean('done')->default(false);
            $table->date('due_on')->nullable();
            $table->foreignId('category_id')->nullable()->constrained()->nullOnDelete();
            $table->timestamps();                           // created_at, updated_at
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tasks');
    }
};
```

## Run and undo

```bash
php artisan migrate             # run new migrations
php artisan migrate:status      # see what has run
php artisan migrate:rollback    # undo the last batch
php artisan migrate:fresh --seed  # drop everything, re-run, seed (development only!)
```

## Change an existing table

```bash
php artisan make:migration add_priority_to_tasks_table
```

```php
Schema::table('tasks', function (Blueprint $table) {
    $table->unsignedTinyInteger('priority')->default(2)->after('title');
});
```

:::warning
Never edit a migration that has already run on a shared or production database. Create a **new** migration instead.
:::

## Common column types

`string`, `text`, `integer`, `bigInteger`, `decimal('price', 10, 2)`, `boolean`, `date`, `dateTime`, `json`, `uuid`, `foreignId`, `enum`, `softDeletes()`.

```quiz
[
 {"q": "What is the purpose of the down() method?", "options": ["Speed up queries", "Undo what up() did", "Seed data", "Delete the database"], "answer": 1, "why": "down() reverses the migration so it can be rolled back."},
 {"q": "Which command drops all tables and re-runs every migration?", "options": ["migrate:refresh", "migrate:fresh", "migrate:reset", "db:wipe"], "answer": 1, "why": "migrate:fresh drops every table and migrates from scratch."},
 {"q": "A migration already ran in production and you need a new column. What should you do?", "options": ["Edit the old migration", "Create a new migration", "Edit the database by hand", "Delete the table"], "answer": 1, "why": "Always add a new migration so every environment can apply the change."}
]
```

=== FILE: eloquent-models.md ===
---
title: Eloquent Models
summary: Represent database tables as PHP classes, the Laravel 13 way.
minutes: 10
---
**Eloquent** is Laravel's ORM (Object-Relational Mapper). Each table has a **model** class, and each row becomes an object.

```bash
php artisan make:model Task -mf   # model + migration + factory
```

```php
namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['title', 'notes', 'done', 'due_on', 'category_id'])]
class Task extends Model
{
    use HasFactory;

    protected function casts(): array
    {
        return [
            'done' => 'boolean',
            'due_on' => 'date',
        ];
    }
}
```

## Conventions

- Model `Task` uses the table `tasks` (plural, snake_case).
- The primary key is `id`.
- `created_at` and `updated_at` are managed automatically.

## Laravel 13 model attributes

Laravel 13 lets you configure models with **PHP attributes** instead of properties:

```php
use Illuminate\Database\Eloquent\Attributes\{Fillable, Hidden, Table, Appends};

#[Table('todo_items')]                  // custom table name
#[Fillable(['title', 'done'])]          // mass-assignable columns
#[Hidden(['secret_token'])]             // hidden from JSON
#[Appends(['is_overdue'])]              // add accessors to JSON
class Task extends Model { /* ... */ }
```

:::note
The older style `protected $fillable = ['title', 'done'];` still works. You'll see both in tutorials, so it's good to recognise each.
:::

## Mass assignment

`#[Fillable]` lists the columns allowed in `create()` and `update()`. This stops attackers from setting columns such as `is_admin` by adding extra form fields.

## Casts

Casts convert database values into useful PHP types:

```php
protected function casts(): array
{
    return [
        'done' => 'boolean',
        'due_on' => 'date',            // Carbon date object
        'settings' => 'array',         // JSON <-> PHP array
        'price' => 'decimal:2',
        'status' => TaskStatus::class, // PHP enum
        'password' => 'hashed',
    ];
}
```

## Accessors

```php
use Illuminate\Database\Eloquent\Casts\Attribute;

protected function isOverdue(): Attribute
{
    return Attribute::get(fn () => ! $this->done && $this->due_on?->isPast());
}

// $task->is_overdue
```

```quiz
[
 {"q": "Which table does the model Category use by default?", "options": ["category", "Category", "categories", "category_table"], "answer": 2, "why": "Eloquent uses the plural, snake_case class name."},
 {"q": "What does #[Fillable([...])] protect against?", "options": ["SQL injection", "Mass-assignment of unexpected columns", "XSS", "CSRF"], "answer": 1, "why": "Only listed columns can be set via create() and update()."},
 {"q": "Which cast turns a JSON column into a PHP array?", "options": ["'json' or 'array'", "'string'", "'object' only", "'collection' only"], "answer": 0, "why": "'array' (or 'json') decodes and encodes automatically."}
]
```

=== FILE: eloquent-crud.md ===
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

=== FILE: relationships.md ===
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

=== FILE: factories-and-seeders.md ===
---
title: Factories & Seeders
summary: Generate realistic fake data for development and tests.
minutes: 7
---
## Factories

A **factory** describes how to make a fake model:

```php
// database/factories/TaskFactory.php
class TaskFactory extends Factory
{
    public function definition(): array
    {
        return [
            'title' => fake()->sentence(4),
            'notes' => fake()->optional()->paragraph(),
            'done' => fake()->boolean(30),
            'due_on' => fake()->dateTimeBetween('-1 week', '+2 weeks'),
        ];
    }

    public function done(): static
    {
        return $this->state(['done' => true]);
    }
}
```

```php
Task::factory()->create();                     // 1 saved task
Task::factory()->count(20)->create();
Task::factory()->done()->make();               // not saved
Category::factory()->has(Task::factory()->count(5))->create();
```

## Seeders

```php
// database/seeders/DatabaseSeeder.php
public function run(): void
{
    User::factory()->create(['name' => 'Test User', 'email' => 'test@example.com']);

    Category::factory()
        ->count(4)
        ->has(Task::factory()->count(6))
        ->create();
}
```

```bash
php artisan db:seed
php artisan migrate:fresh --seed   # rebuild + seed (development)
php artisan make:seeder CategorySeeder
```

:::tip
`fake()` is powered by FakerPHP: names, emails, addresses, prices, dates, paragraphs, UUIDs and much more.
:::

```quiz
[
 {"q": "What does factory()->make() do?", "options": ["Creates and saves", "Builds a model without saving it", "Deletes", "Seeds the database"], "answer": 1, "why": "make() builds in memory; create() also saves."},
 {"q": "Which command rebuilds the schema and runs seeders?", "options": ["db:seed --fresh", "migrate:fresh --seed", "seed:all", "migrate --refresh"], "answer": 1, "why": "migrate:fresh --seed drops, migrates and seeds."}
]
```

=== FILE: querying-and-pagination.md ===
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

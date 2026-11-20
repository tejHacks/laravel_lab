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

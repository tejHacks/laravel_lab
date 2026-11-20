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

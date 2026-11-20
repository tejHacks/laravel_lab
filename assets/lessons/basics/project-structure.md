---
title: Project Structure
summary: A guided tour of every important folder in a Laravel app.
minutes: 8
---
A new Laravel 13 app looks like this:

```text
app/
  Http/Controllers/   # your controllers
  Models/             # Eloquent models (User.php ships by default)
  Providers/          # service providers (app setup code)
bootstrap/app.php     # configures routing, middleware and exceptions
config/               # configuration files (app, database, mail...)
database/
  migrations/         # database table blueprints
  factories/          # fake data generators for tests
  seeders/            # code that fills tables with data
  database.sqlite     # the SQLite database file
public/index.php      # the single entry point for every request
resources/
  views/              # Blade templates (*.blade.php)
  css/ js/            # front-end source (built with Vite)
routes/
  web.php             # browser routes (sessions, CSRF protection)
  console.php         # Artisan commands and schedules
storage/              # logs, cache, uploaded files
tests/                # Feature and Unit tests
vendor/               # installed packages (never edit)
artisan               # the command-line tool
composer.json         # PHP dependencies
.env                  # environment settings
```

## Where does my code go?

| You want to... | Put it in |
|---|---|
| Add a page or URL | `routes/web.php` |
| Handle a request | `app/Http/Controllers` |
| Work with a table | `app/Models` + `database/migrations` |
| Write HTML | `resources/views` |
| Add an API | `routes/api.php` (created by `php artisan install:api`) |

## bootstrap/app.php

Since Laravel 11, application setup lives in one small file:

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware): void {
        // register or customise middleware here
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        // customise error handling here
    })->create();
```

:::tip
The `/up` route is a built-in **health check**. Hosting platforms call it to confirm your app is alive.
:::

```quiz
[
 {"q": "Where do Blade templates live?", "options": ["app/Views", "resources/views", "public/views", "routes/views"], "answer": 1, "why": "Views are in resources/views and end with .blade.php."},
 {"q": "Which file is the entry point for every web request?", "options": ["artisan", "routes/web.php", "public/index.php", "bootstrap/app.php"], "answer": 2, "why": "The web server sends every request to public/index.php."},
 {"q": "Should you edit files inside vendor/?", "options": ["Yes, often", "No, Composer manages them", "Only on Fridays", "Only config files"], "answer": 1, "why": "vendor/ is overwritten by Composer; never edit it."}
]
```

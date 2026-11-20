=== FILE: what-is-laravel.md ===
---
title: What is Laravel?
summary: The PHP framework for web apps and APIs, and why developers love it.
minutes: 6
---
**Laravel** is a free, open-source **PHP framework** for building web applications and APIs. A framework gives you a ready-made structure plus tools for the things almost every app needs: routing URLs, talking to a database, logging users in, sending email, validating forms, running background jobs and much more.

:::analogy
Building a web app from scratch is like building a house by first making your own bricks. Laravel hands you quality bricks, plumbing and wiring, so you can focus on designing the house.
:::

## What can you build?

- Websites and web apps (dashboards, shops, blogs, SaaS products)
- **REST APIs** for mobile apps (Flutter, React Native, iOS, Android)
- Admin panels, internal tools, background workers and scheduled tasks

## How a Laravel app works

1. A browser or mobile app sends an **HTTP request** (for example `GET /products`).
2. Laravel's **router** matches the URL to a **route**.
3. The route calls a **controller** method (or a closure).
4. The controller uses **models** to read or write the **database**.
5. It returns a **response**: an HTML page (a **Blade view**) or **JSON**.

This pattern is called **MVC**: **M**odel (data), **V**iew (what the user sees), **C**ontroller (the logic in between).

```php
// routes/web.php
Route::get('/hello', function () {
    return 'Hello from Laravel!';
});
```

## Why Laravel?

- **Elegant syntax**: code that reads almost like English.
- **Batteries included**: auth, queues, mail, caching, testing and file storage are built in.
- **Eloquent ORM**: work with database rows as PHP objects.
- **Artisan CLI**: generate code and run tasks from the terminal.
- **Huge ecosystem**: starter kits, Livewire, Inertia, Forge, Vapor, Cloud, Herd.

:::note
This course targets **Laravel 13**, which needs **PHP 8.3 or newer**. Laravel ships a new major version roughly once a year, and upgrades between versions are usually small.
:::

```quiz
[
 {"q": "Which language is Laravel written in?", "options": ["JavaScript", "Python", "PHP", "Dart"], "answer": 2, "why": "Laravel is a PHP framework."},
 {"q": "In MVC, what does the Controller do?", "options": ["Stores data", "Handles the logic between request, data and response", "Styles the page", "Runs the database"], "answer": 1, "why": "Controllers receive requests, use models and return responses."},
 {"q": "What minimum PHP version does Laravel 13 require?", "options": ["7.4", "8.0", "8.3", "9.0"], "answer": 2, "why": "Laravel 13 requires PHP ^8.3."}
]
```

=== FILE: installing-laravel.md ===
---
title: Installing Laravel
summary: PHP, Composer, the Laravel installer, Herd, and running your first app.
minutes: 9
---
To build with Laravel you need **PHP**, **Composer** (PHP's package manager) and optionally **Node.js** for front-end assets.

## Option A: Laravel Herd (easiest on macOS and Windows)

**Herd** is a free desktop app from the Laravel team that installs PHP, Composer, the Laravel installer and a local web server in one click. Any folder inside Herd's `~/Herd` directory is served at `http://folder-name.test` automatically.

## Option B: install the tools yourself

```bash
# macOS (Homebrew)
brew install php composer

# Check versions
php -v          # needs 8.3+
composer -V

# The Laravel installer
composer global require laravel/installer
```

## Create a project

```bash
laravel new my-app
# The installer asks which starter kit (none, React, Vue, Livewire),
# which testing framework (Pest or PHPUnit) and which database.

cd my-app
composer run dev    # starts the server, queue worker, logs and Vite together
```

Or without the installer:

```bash
composer create-project laravel/laravel my-app
cd my-app
php artisan serve   # http://127.0.0.1:8000
```

:::tip
New projects use **SQLite** by default: the whole database is one file at `database/database.sqlite`. No database server is needed while you learn.
:::

## The `.env` file

Settings that change per machine (database, mail, secret keys) live in `.env`:

```dotenv
APP_NAME="My App"
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=sqlite
```

:::warning
Never commit `.env` to Git. It contains secrets such as `APP_KEY`. Commit `.env.example` instead.
:::

```quiz
[
 {"q": "What is Composer?", "options": ["A code editor", "PHP's package manager", "A database", "A web server"], "answer": 1, "why": "Composer installs and manages PHP packages (dependencies)."},
 {"q": "Which command starts Laravel's built-in development server?", "options": ["php artisan run", "php artisan serve", "composer start", "laravel up"], "answer": 1, "why": "php artisan serve runs the app at http://127.0.0.1:8000."},
 {"q": "Where should secrets like database passwords go?", "options": ["routes/web.php", "The .env file", "public/index.php", "composer.json"], "answer": 1, "why": ".env holds per-environment configuration and secrets."}
]
```

=== FILE: project-structure.md ===
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

=== FILE: artisan-and-lifecycle.md ===
---
title: Artisan & the Request Lifecycle
summary: The command-line tool you will use every day, and what happens on each request.
minutes: 7
---
**Artisan** is Laravel's command-line tool. It generates files, runs migrations, clears caches and much more.

```bash
php artisan list                 # every available command
php artisan make:controller PostController
php artisan make:model Post -mfs # model + migration + factory + seeder
php artisan migrate              # run database migrations
php artisan route:list           # show all routes
php artisan tinker               # interactive PHP shell for your app
php artisan about                # environment overview
php artisan optimize:clear       # clear all caches
```

:::tip
Add `--help` to any command, for example `php artisan make:model --help`, to see its options.
:::

## Tinker: play with your app

```bash
php artisan tinker
> User::count()
= 3
> User::first()->name
= "Ada"
```

## The request lifecycle

1. The web server sends the request to `public/index.php`.
2. Laravel boots: it loads config and **service providers**.
3. The request passes through **global middleware** (trimming strings, maintenance mode and so on).
4. The **router** finds the matching route and runs its middleware (for example `auth`).
5. The **controller** runs and returns a response.
6. The response travels back out through the middleware to the browser.

:::analogy
Middleware are like security checkpoints at an airport. Every passenger (request) passes through them on the way to the gate (controller), and they can stop anyone who isn't allowed through.
:::

```quiz
[
 {"q": "Which command lists every route?", "options": ["php artisan routes", "php artisan route:list", "php artisan list:routes", "composer routes"], "answer": 1, "why": "route:list prints every registered route."},
 {"q": "What does `make:model Post -m` also create?", "options": ["A controller", "A migration", "A view", "A test"], "answer": 1, "why": "-m creates a migration (-f factory, -s seeder, -c controller)."},
 {"q": "What runs before the controller and can block a request?", "options": ["Views", "Migrations", "Middleware", "Seeders"], "answer": 2, "why": "Middleware inspect requests before they reach controllers."}
]
```

=== FILE: routing-basics.md ===
---
title: Routing Basics
summary: Map URLs and HTTP methods to code.
minutes: 8
---
A **route** connects a URL and an HTTP method to the code that handles it. Browser routes go in `routes/web.php`.

```php
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/about', fn () => 'About us');

// Return an array and Laravel converts it to JSON automatically
Route::get('/status', fn () => ['ok' => true, 'time' => now()]);
```

## HTTP methods

```php
Route::get('/posts', ...);          // read
Route::post('/posts', ...);         // create
Route::put('/posts/{id}', ...);     // replace
Route::patch('/posts/{id}', ...);   // update part
Route::delete('/posts/{id}', ...);  // delete
Route::match(['get', 'post'], '/contact', ...);
Route::any('/anything', ...);
```

## Shortcuts

```php
Route::view('/terms', 'pages.terms');            // just show a view
Route::redirect('/home', '/', 301);              // permanent redirect
Route::fallback(fn () => response('Not found', 404));
```

## Groups and prefixes

```php
Route::prefix('admin')->name('admin.')->group(function () {
    Route::get('/dashboard', ...)->name('dashboard'); // URL /admin/dashboard, name admin.dashboard
    Route::get('/users', ...)->name('users');
});
```

:::tip
Run `php artisan route:list` whenever a URL doesn't work. It shows exactly what Laravel registered.
:::

```quiz
[
 {"q": "Which file holds browser routes?", "options": ["routes/api.php", "routes/web.php", "app/routes.php", "config/routes.php"], "answer": 1, "why": "Web routes (with sessions and CSRF) live in routes/web.php."},
 {"q": "What happens when a route returns a PHP array?", "options": ["Error", "It is converted to JSON", "It is printed with print_r", "Nothing is returned"], "answer": 1, "why": "Laravel automatically turns arrays and models into JSON responses."},
 {"q": "Which method is used to create a resource?", "options": ["GET", "POST", "DELETE", "HEAD"], "answer": 1, "why": "POST creates new resources."}
]
```

=== FILE: route-parameters.md ===
---
title: Route Parameters & Named Routes
summary: Dynamic URLs, optional parameters, constraints and URL helpers.
minutes: 8
---
## Required parameters

```php
Route::get('/users/{id}', function (string $id) {
    return "User #$id";
});

Route::get('/posts/{post}/comments/{comment}', function (string $post, string $comment) {
    return "Comment $comment on post $post";
});
```

## Optional parameters

```php
Route::get('/hello/{name?}', function (?string $name = 'stranger') {
    return "Hello, $name!";
});
```

## Constraints

```php
Route::get('/users/{id}', ...)->whereNumber('id');
Route::get('/tags/{slug}', ...)->where('slug', '[a-z0-9-]+');
Route::get('/lang/{code}', ...)->whereIn('code', ['en', 'fr', 'yo']);
```

## Named routes

Give routes names, then generate URLs from the name. If the URL changes later, the links keep working.

```php
Route::get('/user/profile', ProfileController::class)->name('profile');

$url = route('profile');                        // http://app.test/user/profile
return redirect()->route('profile');

Route::get('/posts/{post}', ...)->name('posts.show');
route('posts.show', ['post' => 42]);            // /posts/42
```

## Route model binding

Type-hint a model and Laravel fetches the row for you, returning a 404 if it doesn't exist:

```php
use App\Models\Post;

Route::get('/posts/{post}', function (Post $post) {
    return $post->title;          // $post is already loaded from the database
});

// Bind by a different column
Route::get('/posts/{post:slug}', fn (Post $post) => $post);
```

:::tip
Route model binding removes a lot of repetitive "find or fail" code. It is one of Laravel's best features.
:::

```quiz
[
 {"q": "How do you make a route parameter optional?", "options": ["{name!}", "{name?} with a default value", "{optional:name}", "[name]"], "answer": 1, "why": "Add ? to the parameter and give the function argument a default."},
 {"q": "What does route('posts.show', ['post' => 5]) return?", "options": ["A view", "The URL for that named route", "A redirect", "A Post model"], "answer": 1, "why": "route() generates a URL from a route name."},
 {"q": "With route model binding, what happens if the record doesn't exist?", "options": ["$post is null", "A 404 Not Found response", "A 500 error", "An empty model"], "answer": 1, "why": "Implicit binding returns 404 automatically."}
]
```

=== FILE: controllers.md ===
---
title: Controllers
summary: Organise request-handling logic into classes.
minutes: 8
---
Closures in route files are fine for tiny apps, but real apps put logic in **controllers**.

```bash
php artisan make:controller PageController
```

```php
// app/Http/Controllers/PageController.php
namespace App\Http\Controllers;

class PageController extends Controller
{
    public function home()
    {
        return view('home', ['title' => 'Welcome']);
    }

    public function about()
    {
        return view('about');
    }
}
```

```php
// routes/web.php
use App\Http\Controllers\PageController;

Route::get('/', [PageController::class, 'home'])->name('home');
Route::get('/about', [PageController::class, 'about'])->name('about');
```

## Single-action controllers

```bash
php artisan make:controller ShowDashboard --invokable
```

```php
class ShowDashboard extends Controller
{
    public function __invoke()
    {
        return view('dashboard');
    }
}

Route::get('/dashboard', ShowDashboard::class);
```

## Dependency injection

Type-hint what you need and Laravel's **service container** provides it:

```php
use Illuminate\Http\Request;

public function search(Request $request)
{
    $term = $request->query('q', '');           // ?q=...
    return view('search', compact('term'));
}
```

## Controller middleware with attributes (Laravel 13)

```php
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class SettingsController extends Controller
{
    #[Middleware('throttle:5,1', only: ['update'])]
    public function update() { /* ... */ }
}
```

```quiz
[
 {"q": "How do you point a route to a controller method?", "options": ["'PageController@home'", "[PageController::class, 'home']", "PageController->home()", "new PageController('home')"], "answer": 1, "why": "Use an array of the class name and method name."},
 {"q": "What method does an invokable controller use?", "options": ["handle()", "index()", "__invoke()", "run()"], "answer": 2, "why": "Single-action controllers implement __invoke()."},
 {"q": "How do you read ?q=shoes from the URL?", "options": ["$request->query('q')", "$_GET->q", "request('q')->url", "$request->param('q')"], "answer": 0, "why": "$request->query('q') reads query-string values (request('q') also works)."}
]
```

=== FILE: resource-controllers.md ===
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

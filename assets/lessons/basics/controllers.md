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

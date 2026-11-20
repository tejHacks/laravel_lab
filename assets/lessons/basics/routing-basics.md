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

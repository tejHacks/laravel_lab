---
title: Middleware
summary: Filter and modify requests before they reach your controllers.
minutes: 8
---
**Middleware** wraps your routes. Each one can inspect the request, stop it, or change the response.

## Built-in middleware you'll use

| Alias | What it does |
|---|---|
| `auth` | Requires a logged-in user |
| `guest` | Only for logged-out users |
| `verified` | Requires a verified email |
| `throttle:60,1` | Rate limit: 60 requests per minute |
| `signed` | Requires a valid signed URL |
| `can:update,post` | Authorization check |

## Write your own

```bash
php artisan make:middleware EnsureUserIsAdmin
```

```php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsAdmin
{
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->is_admin) {
            abort(403, 'Admins only.');
        }

        return $next($request);   // continue to the next layer
    }
}
```

## Register it (bootstrap/app.php)

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias(['admin' => EnsureUserIsAdmin::class]);

    // or add to every web request:
    // $middleware->web(append: [TrackLastSeen::class]);
})
```

```php
Route::middleware(['auth', 'admin'])->prefix('admin')->group(function () {
    Route::get('/', AdminDashboard::class);
});
```

## After middleware

```php
public function handle(Request $request, Closure $next): Response
{
    $response = $next($request);                         // run the app first
    $response->headers->set('X-Frame-Options', 'DENY');  // then modify the response
    return $response;
}
```

```quiz
[
 {"q": "What does `return $next($request);` do?", "options": ["Stops the request", "Passes the request to the next layer", "Redirects home", "Logs the user in"], "answer": 1, "why": "$next continues down the middleware pipeline."},
 {"q": "Where do you register a middleware alias in Laravel 13?", "options": ["app/Http/Kernel.php", "bootstrap/app.php", "config/app.php", "routes/web.php"], "answer": 1, "why": "Since Laravel 11, middleware is configured in bootstrap/app.php."},
 {"q": "What does throttle:60,1 mean?", "options": ["60 users max", "60 requests per 1 minute", "Wait 60 seconds", "1 request per 60 minutes"], "answer": 1, "why": "maxAttempts,decayMinutes."}
]
```

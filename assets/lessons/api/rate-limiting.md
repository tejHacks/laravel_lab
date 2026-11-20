---
title: Rate Limiting
summary: Protect your API from abuse and runaway clients.
minutes: 7
---
Rate limiting caps how many requests a client can make in a period. Over the limit, Laravel returns **429 Too Many Requests** with a `Retry-After` header.

## Quick limits with throttle

```php
Route::middleware('throttle:60,1')->group(...);   // 60 per minute
Route::post('/login', ...)->middleware('throttle:5,1');
```

## Named limiters (AppServiceProvider::boot)

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('api', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(120)->by($request->user()->id)   // per user
        : Limit::perMinute(30)->by($request->ip());          // per IP for guests
});

RateLimiter::for('uploads', fn (Request $request) => [
    Limit::perMinute(10)->by($request->user()->id),
    Limit::perDay(200)->by($request->user()->id),
]);
```

```php
Route::middleware(['auth:sanctum', 'throttle:uploads'])->post('/photos', ...);
```

Responses include headers so clients can slow down politely:

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 12
Retry-After: 34
```

```quiz
[
 {"q": "What status code means you hit a rate limit?", "options": ["403", "409", "429", "503"], "answer": 2, "why": "429 Too Many Requests."},
 {"q": "What does ->by($request->user()->id) do?", "options": ["Limits all users together", "Keeps a separate counter per user", "Blocks the user", "Logs the user"], "answer": 1, "why": "The key decides whose counter is incremented."}
]
```

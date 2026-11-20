---
title: Service Providers & Facades
summary: Where apps are configured, and how static-looking calls work.
minutes: 7
---
## Service providers

Providers are where your app is set up: bindings, event listeners, macros, rate limiters, gates.

```php
class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // bind things into the container (don't use other services here)
    }

    public function boot(): void
    {
        // everything is registered: configure, listen, define gates...
        Model::preventLazyLoading(! app()->isProduction());
        Gate::define('admin', fn (User $u) => $u->is_admin);
    }
}
```

Providers are listed in `bootstrap/providers.php`.

## Facades

`Cache::get()`, `Route::get()` and `Mail::to()` look static, but they're **facades**: short proxies to objects living in the container.

```php
Cache::put('key', 'value', 60);
// is the same as
app('cache')->put('key', 'value', 60);
```

Facades can be **faked** in tests (`Mail::fake()`), which is a big reason they're popular.

## Helpers vs facades vs injection

```php
cache('key');                          // helper
Cache::get('key');                     // facade
public function __construct(private CacheRepository $cache) {} // injection
```

All three reach the same service. Pick one style and stay consistent.

```quiz
[
 {"q": "Where should you put Gate::define calls?", "options": ["routes/web.php", "A service provider's boot()", "A controller", "A migration"], "answer": 1, "why": "boot() runs after all services are registered."},
 {"q": "What is a facade?", "options": ["A static class with no state", "A static-style proxy to a service in the container", "A view helper", "A database table"], "answer": 1, "why": "Facades forward calls to container services."}
]
```

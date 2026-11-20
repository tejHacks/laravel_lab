=== FILE: service-container.md ===
---
title: The Service Container
summary: How Laravel builds objects for you, and how to customise it.
minutes: 10
---
The **service container** is the engine at Laravel's core. Whenever you type-hint a class (in a controller, job, command or listener), the container builds it and everything it depends on.

```php
class ReportController extends Controller
{
    // Laravel builds ReportService and anything ReportService needs
    public function __construct(private ReportService $reports) {}
}
```

This is **dependency injection**: classes receive their dependencies instead of creating them, which makes them easy to test and swap.

## Binding interfaces to implementations

```php
// app/Providers/AppServiceProvider.php
public function register(): void
{
    $this->app->bind(PaymentGateway::class, PaystackGateway::class);

    // one shared instance for the whole request
    $this->app->singleton(CurrencyConverter::class, fn () => new CurrencyConverter(config('services.fx.key')));
}
```

Now anything asking for `PaymentGateway` receives a `PaystackGateway`. Switching to Stripe later is a one-line change.

## Contextual attributes (Laravel 11+)

```php
use Illuminate\Container\Attributes\Config;
use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Container\Attributes\Storage;

class InvoiceService
{
    public function __construct(
        #[Config('app.name')] private string $appName,
        #[Storage('s3')] private Filesystem $files,
        #[CurrentUser] private ?User $user,
    ) {}
}
```

## Resolving manually

```php
$converter = app(CurrencyConverter::class);
$converter = resolve(CurrencyConverter::class);
```

:::analogy
The container is a smart kitchen. Order a "burger" (a class) and it fetches the bun, patty and sauce (its dependencies) and assembles them, every time, without you lifting a finger.
:::

```quiz
[
 {"q": "What does $this->app->singleton() do?", "options": ["Creates a new object every time", "Shares one instance", "Deletes a binding", "Registers a route"], "answer": 1, "why": "Singletons are built once and reused."},
 {"q": "Why bind an interface to a class?", "options": ["Speed", "To swap implementations easily and test with fakes", "Required for routes", "To hide the class"], "answer": 1, "why": "Code depends on the interface, not on one concrete class."}
]
```

=== FILE: providers-and-facades.md ===
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

=== FILE: collections.md ===
---
title: Collections in Depth
summary: Laravel's most-used power tool for working with data.
minutes: 9
---
Eloquent queries return **Collections**, and you can wrap any array with `collect()`.

```php
$orders = collect([
    ['customer' => 'Ada', 'total' => 120, 'status' => 'paid'],
    ['customer' => 'Tunde', 'total' => 80, 'status' => 'pending'],
    ['customer' => 'Ada', 'total' => 45, 'status' => 'paid'],
]);

$orders->where('status', 'paid')->sum('total');            // 165
$orders->groupBy('customer')->map->sum('total');           // ['Ada' => 165, 'Tunde' => 80]
$orders->sortByDesc('total')->first()['customer'];         // 'Ada'
$orders->pluck('customer')->unique()->values();            // ['Ada', 'Tunde']
$orders->partition(fn ($o) => $o['status'] === 'paid');    // [paid, others]
$orders->keyBy('customer');
$orders->chunk(2);
$orders->avg('total');                                     // 81.66...
```

## Higher-order messages

```php
$users->each->notify(new Welcome);
$tasks->filter->is_overdue;
$orders->sum->total;
```

## Lazy collections for huge datasets

```php
// Streams rows one by one instead of loading 1 million into memory
User::lazy()->each(function (User $user) {
    // ...
});
```

:::tip
Learn `map`, `filter`, `reduce`, `groupBy`, `pluck`, `sortBy`, `firstWhere` and `sum` first. They cover 90% of day-to-day needs.
:::

```quiz
[
 {"q": "What does groupBy('customer')->map->sum('total') return?", "options": ["Total of all orders", "Each customer's total", "Number of customers", "The first order"], "answer": 1, "why": "Group per customer, then sum each group."},
 {"q": "Why use lazy() on huge tables?", "options": ["It's prettier", "It streams rows to keep memory low", "It caches", "It sorts faster"], "answer": 1, "why": "Lazy collections avoid loading everything at once."}
]
```

=== FILE: frontends.md ===
---
title: Front-ends: Blade, Livewire & Inertia
summary: Choose how to build the UI of a Laravel app.
minutes: 8
---
Laravel supports several ways to build the front end. The official **starter kits** (chosen during `laravel new`) set each one up with authentication included.

## Blade only

Server-rendered HTML. Simple, fast, great SEO. Add **Alpine.js** for small interactions.

## Livewire

Write dynamic, reactive components **in PHP**. No separate JavaScript app.

```php
class Counter extends Component
{
    public int $count = 0;

    public function increment(): void
    {
        $this->count++;
    }

    public function render()
    {
        return view('livewire.counter');
    }
}
```

```blade
<div>
    <h1>{{ $count }}</h1>
    <button wire:click="increment">+</button>
</div>
```

## Inertia (React, Vue or Svelte)

Build pages as React or Vue components, but keep Laravel routing and controllers. No separate API needed.

```php
return Inertia::render('Tasks/Index', ['tasks' => TaskResource::collection(Task::all())]);
```

## Separate SPA or mobile app + API

A Next.js or Nuxt front end, or a **Flutter** app, talking to a Laravel **API** with Sanctum. Choose this when several clients share one backend.

| Choose | When |
|---|---|
| Blade + Alpine | Content sites, admin panels, simple apps |
| Livewire | You love PHP and want interactivity |
| Inertia | Your team knows React or Vue |
| API + Flutter | Mobile apps (and maybe a web app too) |

```quiz
[
 {"q": "Which option lets you build reactive UIs mostly in PHP?", "options": ["Inertia", "Livewire", "Vue", "jQuery"], "answer": 1, "why": "Livewire components are PHP classes with Blade views."},
 {"q": "What should a Flutter app talk to?", "options": ["Blade views", "A Laravel API (JSON + Sanctum)", "Livewire", "Inertia pages"], "answer": 1, "why": "Mobile apps consume JSON APIs."}
]
```

=== FILE: broadcasting.md ===
---
title: Real-time with Broadcasting & Reverb
summary: Push live updates to browsers and apps over WebSockets.
minutes: 8
---
Normally the client asks and the server answers. With **broadcasting**, the server **pushes** events the moment something happens: chat messages, live order status, notifications or dashboards.

```bash
php artisan install:broadcasting   # sets up Laravel Reverb (a first-party WebSocket server)
php artisan reverb:start
```

```php
class OrderStatusUpdated implements ShouldBroadcast
{
    public function __construct(public Order $order) {}

    public function broadcastOn(): array
    {
        return [new PrivateChannel("orders.{$this->order->id}")];
    }
}

OrderStatusUpdated::dispatch($order);
```

```php
// routes/channels.php: who may listen?
Broadcast::channel('orders.{order}', fn (User $user, Order $order) => $order->user_id === $user->id);
```

```js
// Front end (Laravel Echo)
Echo.private(`orders.${orderId}`)
    .listen('OrderStatusUpdated', (e) => console.log(e.order.status));
```

Flutter apps can connect with a Pusher-protocol client package, because Reverb speaks the Pusher protocol.

```quiz
[
 {"q": "What does ShouldBroadcast do?", "options": ["Sends an email", "Pushes the event to listening clients over WebSockets", "Queues a job", "Logs the event"], "answer": 1, "why": "Broadcast events are sent to channels in real time."},
 {"q": "What is Laravel Reverb?", "options": ["A queue driver", "A first-party WebSocket server", "A template engine", "A test runner"], "answer": 1, "why": "Reverb is Laravel's own WebSocket server."}
]
```

=== FILE: architecture.md ===
---
title: Structuring Bigger Apps
summary: Actions, services, DTOs and keeping controllers thin.
minutes: 9
---
As apps grow, fat controllers become hard to test and reuse. Move business logic into dedicated classes.

## Thin controllers

```php
public function store(PlaceOrderRequest $request, PlaceOrder $placeOrder)
{
    $order = $placeOrder->handle($request->user(), $request->validated());

    return new OrderResource($order);
}
```

## Action classes (one job each)

```php
class PlaceOrder
{
    public function __construct(private PaymentGateway $payments) {}

    public function handle(User $user, array $data): Order
    {
        return DB::transaction(function () use ($user, $data) {
            $order = $user->orders()->create(['total' => 0]);

            foreach ($data['items'] as $item) {
                $product = Product::lockForUpdate()->findOrFail($item['product_id']);
                if ($product->stock < $item['qty']) {
                    throw new InsufficientStockException($product);
                }
                $product->decrement('stock', $item['qty']);
                $order->items()->create([...]);
            }

            $order->update(['total' => $order->items->sum('total')]);
            OrderPlaced::dispatch($order);

            return $order;
        });
    }
}
```

The same action can now be called from a controller, an Artisan command, a job or a test.

## Database transactions

`DB::transaction()` makes several writes **all succeed or all fail**. You'll never have an order without its items.

## Folder ideas

```text
app/
  Actions/        PlaceOrder.php, RefundOrder.php
  Services/       PaystackGateway.php
  Enums/          OrderStatus.php
  Data/           DTOs (simple typed data classes)
```

:::tip
Don't over-engineer small apps. Start simple. Extract an action when the same logic appears twice, or when a controller method becomes hard to read.
:::

```quiz
[
 {"q": "Why wrap order creation in DB::transaction?", "options": ["Speed", "All writes succeed or none do", "Caching", "Validation"], "answer": 1, "why": "Transactions keep data consistent."},
 {"q": "What's a key benefit of action classes?", "options": ["Fewer files", "Logic is reusable from controllers, jobs, commands and tests", "Required by Laravel", "Faster routing"], "answer": 1, "why": "Actions isolate business logic from HTTP concerns."}
]
```

=== FILE: security-checklist.md ===
---
title: Security Checklist
summary: The habits that keep Laravel apps safe.
minutes: 8
---
Laravel protects you from many attacks by default. Keep these habits:

1. **Validate all input** with `$request->validate()` or form requests, and save `validated()` data only.
2. **Escape output** with `{{ }}`. Use `{!! !!}` only for HTML you created yourself.
3. **Use Eloquent or the query builder** (they use prepared statements). With raw SQL, always pass bindings: `DB::select('... where id = ?', [$id])`.
4. **Keep `@csrf`** in every web form.
5. **Authorize every action** with policies or gates, never just by hiding buttons.
6. **Use `#[Fillable]`** to prevent mass-assignment of fields like `is_admin`.
7. **Hash passwords** (the `hashed` cast) and use `Password::defaults()` rules.
8. **Rate-limit** login, registration, OTP and password-reset routes.
9. **`APP_DEBUG=false`** in production, and keep `.env` out of Git.
10. **HTTPS everywhere**; add `secure` cookies and HSTS headers.
11. **Store files privately** unless they must be public, and validate types and sizes.
12. **Keep dependencies updated**: run `composer audit` and upgrade regularly.

```bash
composer audit   # lists packages with known vulnerabilities
```

:::warning
The most common real-world Laravel breach is a leaked `.env` file or `APP_DEBUG=true` in production. Double-check both on every deploy.
:::

```quiz
[
 {"q": "How do you safely use raw SQL with user input?", "options": ["String concatenation", "Parameter bindings (?)", "addslashes()", "Base64 encoding"], "answer": 1, "why": "Bindings prevent SQL injection."},
 {"q": "Which command checks Composer packages for known vulnerabilities?", "options": ["composer check", "composer audit", "php artisan security", "composer secure"], "answer": 1, "why": "composer audit reports advisories."}
]
```

=== FILE: ecosystem.md ===
---
title: The Laravel Ecosystem
summary: Official tools and packages worth knowing next.
minutes: 6
---
| Tool | What it's for |
|---|---|
| **Herd** | Local PHP development environment (macOS/Windows) |
| **Sail** | Docker-based local environment |
| **Sanctum** | API tokens and SPA authentication |
| **Passport** | Full OAuth2 server |
| **Socialite** | "Log in with Google/GitHub/Apple" |
| **Cashier** | Stripe and Paddle subscriptions |
| **Scout** | Full-text search (Meilisearch, Typesense, Algolia) |
| **Horizon** | Dashboard for Redis queues |
| **Telescope** | Local debug assistant (requests, queries, jobs) |
| **Pulse** | Production performance dashboard |
| **Reverb** | WebSocket server for real-time features |
| **Octane** | Supercharge performance with FrankenPHP, Swoole or RoadRunner |
| **Pint** | Code style fixer (`./vendor/bin/pint`) |
| **Pest** | Expressive testing framework |
| **Livewire / Inertia** | Front-end approaches |
| **Filament** (community) | Admin panels built with Livewire |
| **Forge / Cloud / Vapor** | Deployment and hosting |

## Keep learning

- **laravel.com/docs**: the official documentation (excellent)
- **Laracasts**: video courses
- **Laravel News**: weekly news and tutorials
- **Build things!** A blog, an inventory system, or an API for a Flutter app.

```quiz
[
 {"q": "Which package adds 'Log in with Google'?", "options": ["Sanctum", "Socialite", "Passport", "Scout"], "answer": 1, "why": "Socialite handles OAuth logins with social providers."},
 {"q": "What does Laravel Pint do?", "options": ["Runs queues", "Fixes code style", "Deploys apps", "Sends mail"], "answer": 1, "why": "Pint formats your PHP code."}
]
```

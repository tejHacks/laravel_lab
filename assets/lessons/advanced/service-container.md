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

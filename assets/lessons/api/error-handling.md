---
title: Error Handling for APIs
summary: Consistent, helpful JSON errors.
minutes: 8
---
Laravel already turns exceptions into JSON for API requests:

| Exception | Status |
|---|---|
| `ValidationException` | 422 |
| `AuthenticationException` | 401 |
| `AuthorizationException` | 403 |
| `ModelNotFoundException` / `NotFoundHttpException` | 404 |
| `ThrottleRequestsException` | 429 |
| Anything else | 500 |

## Customise the output (bootstrap/app.php)

```php
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (NotFoundHttpException $e, Request $request) {
        if ($request->is('api/*')) {
            return response()->json(['message' => 'Resource not found.'], 404);
        }
    });
})
```

## Custom exceptions

```php
class InsufficientStockException extends Exception
{
    public function __construct(public Product $product) {
        parent::__construct("Only {$product->stock} {$product->name} left.");
    }

    public function render(Request $request)
    {
        return response()->json([
            'message' => $this->getMessage(),
            'code' => 'insufficient_stock',
            'available' => $this->product->stock,
        ], 409);
    }
}

throw new InsufficientStockException($product);
```

:::tip
Add a machine-readable `code` (like `insufficient_stock`) next to the human `message`. Apps can then react in code without parsing English text.
:::

:::warning
With `APP_DEBUG=true`, 500 errors include stack traces. Production must have `APP_DEBUG=false` so internals never leak to clients.
:::

```quiz
[
 {"q": "Which status does a ModelNotFoundException become?", "options": ["400", "404", "422", "500"], "answer": 1, "why": "Missing models render as 404 Not Found."},
 {"q": "Why include a machine-readable error code?", "options": ["Decoration", "So clients can react without parsing messages", "Required by HTTP", "For SEO"], "answer": 1, "why": "Codes are stable even if message wording changes."}
]
```

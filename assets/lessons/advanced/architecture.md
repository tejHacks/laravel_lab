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

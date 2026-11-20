---
title: Events & Listeners
summary: Decouple your code by reacting to things that happened.
minutes: 7
---
An **event** says "something happened" (an order was placed). **Listeners** react to it (email a receipt, update stock, notify the warehouse). The code that places the order doesn't need to know about any of them.

```bash
php artisan make:event OrderPlaced
php artisan make:listener SendOrderReceipt --event=OrderPlaced
```

```php
class OrderPlaced
{
    use Dispatchable, SerializesModels;

    public function __construct(public Order $order) {}
}

class SendOrderReceipt implements ShouldQueue   // runs on the queue
{
    public function handle(OrderPlaced $event): void
    {
        Mail::to($event->order->customer)->send(new OrderReceipt($event->order));
    }
}
```

```php
OrderPlaced::dispatch($order);
```

Laravel discovers listeners automatically by scanning `app/Listeners` and reading the type-hint in `handle()`.

## Model events

```php
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy(TaskObserver::class)]
class Task extends Model {}

class TaskObserver
{
    public function created(Task $task): void { /* ... */ }
    public function deleting(Task $task): void { /* ... */ }
}
```

```quiz
[
 {"q": "What is the main benefit of events?", "options": ["Speed", "Decoupling code that reacts from code that triggers", "Smaller database", "Fewer routes"], "answer": 1, "why": "Many listeners can react without the dispatcher knowing about them."},
 {"q": "How do you make a listener run in the background?", "options": ["Implement ShouldQueue", "Add sleep()", "Use a cron job", "Name it Async"], "answer": 0, "why": "Listeners implementing ShouldQueue are queued."}
]
```

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

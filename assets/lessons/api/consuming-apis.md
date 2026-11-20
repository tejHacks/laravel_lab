---
title: Calling Other APIs (HTTP Client)
summary: Use Laravel's HTTP client to talk to payment, weather or any third-party API.
minutes: 8
---
Your API often needs to call **other** APIs: payments (Paystack, Stripe), SMS, maps, AI services. Laravel's `Http` facade makes this pleasant.

```php
use Illuminate\Support\Facades\Http;

$response = Http::acceptJson()
    ->withToken(config('services.paystack.secret'))
    ->timeout(10)
    ->retry(3, 200)                       // retry 3 times, 200 ms apart
    ->get('https://api.paystack.co/transaction/verify/' . $reference);

if ($response->successful()) {
    $status = $response->json('data.status');   // dot notation into the JSON
}

$response->status();      // 200
$response->failed();      // true for 4xx/5xx
$response->throw();       // throw an exception for 4xx/5xx
```

## POST JSON

```php
Http::withToken($token)->post('https://api.example.com/orders', [
    'items' => $items,
    'total' => $total,
]);
```

## Concurrent requests

```php
use Illuminate\Http\Client\Pool;

[$weather, $fx] = Http::pool(fn (Pool $pool) => [
    $pool->get('https://api.open-meteo.com/v1/forecast?latitude=6.5&longitude=3.4&current_weather=true'),
    $pool->get('https://open.er-api.com/v6/latest/USD'),
]);
```

:::warning
Keep secret keys in `.env` and read them through `config/services.php`, never hard-coded in your code.
:::

```quiz
[
 {"q": "How do you read a nested JSON value from a response?", "options": ["$res['data']['status']", "$res->json('data.status')", "$res->get('status')", "json_decode only"], "answer": 1, "why": "json('a.b') reads nested keys with dot notation."},
 {"q": "Where should API secret keys live?", "options": ["In the controller", ".env, read through config", "In routes", "In Git"], "answer": 1, "why": "Secrets belong in environment config."}
]
```

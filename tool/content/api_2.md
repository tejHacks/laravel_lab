=== FILE: sanctum-tokens.md ===
---
title: Token Authentication with Sanctum
summary: Register, log in and protect endpoints for mobile apps.
minutes: 12
---
Mobile apps can't use cookies the way browsers do. Instead they log in once, receive a **token**, and send it with every request:

```http
Authorization: Bearer 3|kE9aP2xQ...
```

**Laravel Sanctum** (installed by `php artisan install:api`) issues and checks these tokens.

## 1. Add the trait to User

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

:::warning
`install:api` does **not** add `HasApiTokens` for you. Without it you'll get "Call to undefined method createToken()".
:::

## 2. Register and login endpoints

```php
// routes/api.php
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

Route::middleware('auth:sanctum')->group(function () {
    Route::get('/me', fn (Request $request) => $request->user());
    Route::post('/logout', [AuthController::class, 'logout']);
});
```

```php
class AuthController extends Controller
{
    public function register(Request $request)
    {
        $data = $request->validate([
            'name' => ['required', 'string', 'max:100'],
            'email' => ['required', 'email', 'unique:users'],
            'password' => ['required', 'min:8'],
            'device_name' => ['required', 'string'],
        ]);

        $user = User::create($data);

        return response()->json([
            'user' => $user,
            'token' => $user->createToken($data['device_name'])->plainTextToken,
        ], 201);
    }

    public function login(Request $request)
    {
        $data = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
            'device_name' => ['required', 'string'],
        ]);

        $user = User::where('email', $data['email'])->first();

        if (! $user || ! Hash::check($data['password'], $user->password)) {
            throw ValidationException::withMessages(['email' => ['The provided credentials are incorrect.']]);
        }

        return ['user' => $user, 'token' => $user->createToken($data['device_name'])->plainTextToken];
    }

    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();   // revoke this device's token

        return response()->noContent();
    }
}
```

## 3. Use the token from Flutter

```dart
final res = await http.get(
  Uri.parse('https://myapp.com/api/me'),
  headers: {
    'Accept': 'application/json',
    'Authorization': 'Bearer $token',
  },
);
```

:::tip
Store the token in **flutter_secure_storage** on the device, never in plain SharedPreferences.
:::

## Token housekeeping

```php
$user->tokens()->delete();                          // log out every device
$user->createToken('ios', ['*'], now()->addDays(30)); // expiring token
```

```quiz
[
 {"q": "How does a mobile app send its Sanctum token?", "options": ["As a cookie", "Authorization: Bearer <token> header", "In the URL", "In the body of GET requests"], "answer": 1, "why": "Bearer tokens go in the Authorization header."},
 {"q": "Which middleware protects routes with Sanctum tokens?", "options": ["auth", "auth:sanctum", "token", "sanctum:api"], "answer": 1, "why": "Use the sanctum guard: auth:sanctum."},
 {"q": "How do you log out only the current device?", "options": ["$user->tokens()->delete()", "$request->user()->currentAccessToken()->delete()", "Auth::logout()", "Session::flush()"], "answer": 1, "why": "Delete only the token used for this request."}
]
```

=== FILE: abilities-and-policies.md ===
---
title: Token Abilities & Policies
summary: Limit what each token and each user can do.
minutes: 9
---
## Token abilities (scopes)

Give tokens only the permissions they need:

```php
$token = $user->createToken('reporting-tool', ['books:read'])->plainTextToken;
$admin = $user->createToken('admin-panel', ['books:read', 'books:write'])->plainTextToken;
```

Register Sanctum's ability middleware in `bootstrap/app.php`:

```php
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'abilities' => CheckAbilities::class,      // needs ALL listed
        'ability' => CheckForAnyAbility::class,    // needs ANY listed
    ]);
})
```

```php
Route::middleware(['auth:sanctum', 'abilities:books:write'])->group(function () {
    Route::post('/books', [BookController::class, 'store']);
});

// or check in code
if ($request->user()->tokenCan('books:write')) { ... }
```

## Policies: who owns what?

Abilities limit the **token**. Policies limit the **user**, for example "only the author may edit their review".

```php
class ReviewPolicy
{
    public function update(User $user, Review $review): bool
    {
        return $review->user_id === $user->id;
    }
}

public function update(UpdateReviewRequest $request, Review $review)
{
    Gate::authorize('update', $review);   // 403 JSON if not the owner
    $review->update($request->validated());
    return new ReviewResource($review);
}
```

## 401 vs 403

- **401 Unauthenticated**: no token, or an invalid token. The app should send the user to the login screen.
- **403 Forbidden**: valid token, but not allowed. Show "You don't have permission".

```quiz
[
 {"q": "A request has a valid token but tries to edit someone else's review. Which status?", "options": ["401", "403", "404", "422"], "answer": 1, "why": "Authenticated but not authorized: 403."},
 {"q": "Which method checks a token ability in code?", "options": ["tokenCan()", "can()", "hasAbility()", "allows()"], "answer": 0, "why": "$user->tokenCan('ability') checks the current token."}
]
```

=== FILE: spa-authentication.md ===
---
title: SPA Authentication (Cookies)
summary: Authenticate a React or Vue front end on your own domain.
minutes: 7
---
If your JavaScript front end lives on the **same top-level domain** as your API (for example `app.myshop.com` and `api.myshop.com`), Sanctum can use secure **session cookies** instead of tokens. That's safer for browsers, because no token is stored in JavaScript.

## Setup

```dotenv
SANCTUM_STATEFUL_DOMAINS=app.myshop.com,localhost:5173
SESSION_DOMAIN=.myshop.com
```

```php
// bootstrap/app.php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

## The flow

```js
// 1. Get a CSRF cookie
await axios.get('/sanctum/csrf-cookie', { withCredentials: true });

// 2. Log in (uses a normal session login route)
await axios.post('/login', { email, password }, { withCredentials: true });

// 3. Call the API; the session cookie authenticates you
const me = await axios.get('/api/user', { withCredentials: true });
```

## Which should I use?

| Client | Use |
|---|---|
| Flutter / iOS / Android app | **API tokens** |
| SPA on your own domain | **Cookie (stateful) auth** |
| Third-party integrations | **Tokens with abilities** (or Laravel Passport for full OAuth2) |

```quiz
[
 {"q": "What should a Flutter app use with Sanctum?", "options": ["Session cookies", "API tokens", "Basic auth", "No auth"], "answer": 1, "why": "Mobile apps use bearer tokens."},
 {"q": "What does GET /sanctum/csrf-cookie do?", "options": ["Logs in", "Sets the CSRF cookie needed before cookie-based login", "Returns a token", "Logs out"], "answer": 1, "why": "SPAs must fetch the CSRF cookie before POSTing."}
]
```

=== FILE: error-handling.md ===
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

=== FILE: rate-limiting.md ===
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

=== FILE: versioning.md ===
---
title: Versioning Your API
summary: Evolve your API without breaking existing apps.
minutes: 7
---
## URL versioning (simple and popular)

```php
// routes/api.php
Route::prefix('v1')->name('v1.')->group(base_path('routes/api_v1.php'));
Route::prefix('v2')->name('v2.')->group(base_path('routes/api_v2.php'));
```

```text
app/Http/Controllers/Api/V1/BookController.php
app/Http/Controllers/Api/V2/BookController.php
app/Http/Resources/V1/BookResource.php
app/Http/Resources/V2/BookResource.php
```

## What counts as a breaking change?

| Safe (no new version needed) | Breaking (needs a new version) |
|---|---|
| Adding a new endpoint | Removing an endpoint |
| Adding a new optional field | Renaming or removing a field |
| Adding an optional query parameter | Changing a field's type |
| | Making an optional input required |

## Deprecating old versions

1. Announce the date when v1 will be switched off.
2. Add a header so clients notice: `Deprecation: true` and `Sunset: Sat, 01 Aug 2027 00:00:00 GMT`.
3. Watch your logs until v1 traffic drops, then remove it.

:::tip
Mobile apps can check a `/api/app-config` endpoint on start-up that returns `minimum_supported_version`, then ask users to update if they're too old.
:::

```quiz
[
 {"q": "Which change requires a new API version?", "options": ["Adding an optional field", "Renaming an existing field", "Adding a new endpoint", "Adding an optional filter"], "answer": 1, "why": "Renaming breaks clients that read the old name."}
]
```

=== FILE: caching-performance.md ===
---
title: Caching & Performance
summary: Make your API fast under load.
minutes: 9
---
## Avoid N+1 queries

```php
// ❌ 1 + N queries
return BookResource::collection(Book::paginate());   // resource reads $book->author

// ✅ 2 queries
return BookResource::collection(Book::with('author')->withCount('reviews')->paginate());
```

## Cache expensive results

```php
use Illuminate\Support\Facades\Cache;

$stats = Cache::remember('dashboard-stats', now()->addMinutes(10), fn () => [
    'books' => Book::count(),
    'top_genres' => Book::selectRaw('genre, count(*) as total')->groupBy('genre')->orderByDesc('total')->limit(5)->get(),
]);

Cache::forget('dashboard-stats');   // clear it when the data changes
```

Laravel's cache drivers include `database` (the default), `file`, `redis` and `memcached`. Use **Redis** in production for speed.

## Select only what you need

```php
Book::select(['id', 'title', 'author'])->paginate();
```

## Index your database

```php
$table->index('genre');
$table->index(['author_id', 'published_year']);
```

Columns you filter or sort by often should be indexed.

## HTTP caching

```php
return BookResource::collection($books)
    ->response()
    ->setEtag(md5($books->toJson()))
    ->setPublic()
    ->setMaxAge(60);
```

## Measure first

Use **Laravel Telescope** or **Debugbar** locally to see every query, and **Pulse** or **Nightwatch** in production to spot slow endpoints.

```quiz
[
 {"q": "What does Cache::remember do?", "options": ["Always recomputes", "Returns the cached value or computes and stores it", "Deletes cache", "Locks the database"], "answer": 1, "why": "It caches the closure's result for the given time."},
 {"q": "Best fix for N+1 queries in resources?", "options": ["More servers", "Eager load with with()", "Disable resources", "Use raw SQL everywhere"], "answer": 1, "why": "Eager loading fetches relations in bulk."}
]
```

=== FILE: api-testing.md ===
---
title: Testing APIs
summary: Write fast, reliable tests for every endpoint.
minutes: 10
---
```php
use Laravel\Sanctum\Sanctum;

class BookApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_it_lists_books(): void
    {
        Book::factory()->count(3)->create();

        $this->getJson('/api/v1/books')
            ->assertOk()
            ->assertJsonCount(3, 'data')
            ->assertJsonStructure(['data' => [['id', 'title', 'author']], 'links', 'meta']);
    }

    public function test_guests_cannot_create_books(): void
    {
        $this->postJson('/api/v1/books', ['title' => 'X'])->assertUnauthorized();   // 401
    }

    public function test_it_creates_a_book(): void
    {
        Sanctum::actingAs(User::factory()->create(), ['books:write']);

        $this->postJson('/api/v1/books', ['title' => 'Half of a Yellow Sun', 'author' => 'Adichie'])
            ->assertCreated()                                  // 201
            ->assertJsonPath('data.title', 'Half of a Yellow Sun');

        $this->assertDatabaseHas('books', ['title' => 'Half of a Yellow Sun']);
    }

    public function test_it_validates_input(): void
    {
        Sanctum::actingAs(User::factory()->create(), ['books:write']);

        $this->postJson('/api/v1/books', [])
            ->assertUnprocessable()                            // 422
            ->assertJsonValidationErrors(['title', 'author']);
    }
}
```

:::tip
Use `getJson`/`postJson`, not `get`/`post`. They send `Accept: application/json`, so errors come back as JSON exactly like in a real app.
:::

## Faking external APIs

```php
Http::fake([
    'api.paystack.co/*' => Http::response(['status' => true], 200),
]);
```

```quiz
[
 {"q": "How do you authenticate as a user with abilities in an API test?", "options": ["$this->actingAs($u)", "Sanctum::actingAs($u, ['books:write'])", "Auth::login($u)", "Add a header by hand only"], "answer": 1, "why": "Sanctum::actingAs sets the user and token abilities."},
 {"q": "Which assertion checks for a 422 response?", "options": ["assertOk", "assertCreated", "assertUnprocessable", "assertForbidden"], "answer": 2, "why": "assertUnprocessable checks 422."}
]
```

=== FILE: consuming-apis.md ===
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

=== FILE: api-documentation.md ===
---
title: Documenting Your API
summary: Make your API easy for app developers (and future you) to use.
minutes: 6
---
An undocumented API is a broken API. Developers need to know every endpoint, what to send and what comes back.

## What good docs include

- Base URL and versioning
- How to authenticate (getting and sending tokens)
- Every endpoint: method, URL, parameters, an example request and response
- Error format and error codes
- Rate limits

## Generate docs automatically

Popular packages read your routes, form requests and resources:

- **Scramble** (`dedoc/scramble`): generates an OpenAPI spec and a docs UI with zero annotations
- **Scribe** (`knuckleswtf/scribe`): docs plus Postman and OpenAPI exports

```bash
composer require dedoc/scramble
# visit /docs/api
```

## OpenAPI

OpenAPI (formerly Swagger) is the standard format for describing APIs. Tools turn it into interactive docs, client SDKs (including Dart for Flutter) and tests.

:::tip
Give app developers a **Postman/Bruno collection** or an **OpenAPI file**. They can then try every endpoint in minutes.
:::

```quiz
[
 {"q": "What is OpenAPI?", "options": ["A PHP framework", "A standard format for describing HTTP APIs", "A database", "A hosting company"], "answer": 1, "why": "OpenAPI specs describe endpoints, inputs and outputs."}
]
```

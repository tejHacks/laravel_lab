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

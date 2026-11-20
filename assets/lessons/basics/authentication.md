---
title: Authentication
summary: Register, log in and log out users, by hand and with starter kits.
minutes: 12
---
**Authentication** answers "who are you?". The fastest route is a **starter kit** (`laravel new app` → choose React, Vue or Livewire), which generates login, registration, password reset and email verification screens. It helps to understand what they do underneath, so here is auth built by hand.

## Register

```php
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rules\Password;

public function register(Request $request)
{
    $data = $request->validate([
        'name' => ['required', 'string', 'max:100'],
        'email' => ['required', 'email', 'unique:users'],
        'password' => ['required', 'confirmed', Password::defaults()],
    ]);

    $user = User::create($data);   // the 'hashed' cast hashes the password
    Auth::login($user);

    return redirect()->intended('/dashboard');
}
```

## Log in

```php
public function login(Request $request)
{
    $credentials = $request->validate([
        'email' => ['required', 'email'],
        'password' => ['required'],
    ]);

    if (Auth::attempt($credentials, $request->boolean('remember'))) {
        $request->session()->regenerate();   // prevents session fixation attacks
        return redirect()->intended('/dashboard');
    }

    return back()->withErrors(['email' => 'These credentials do not match our records.'])
                 ->onlyInput('email');
}
```

## Log out

```php
public function logout(Request $request)
{
    Auth::logout();
    $request->session()->invalidate();
    $request->session()->regenerateToken();

    return redirect('/');
}
```

## Protect routes

```php
Route::middleware('auth')->group(function () {
    Route::get('/dashboard', DashboardController::class);
});

Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
});
```

## Who is logged in?

```php
Auth::user();         // the User model, or null
Auth::id();
Auth::check();        // true or false
$request->user();
```

```blade
@auth Hello, {{ auth()->user()->name }} @endauth
```

:::warning
Never store plain-text passwords. The `'password' => 'hashed'` cast on the User model hashes them automatically with bcrypt or argon.
:::

```quiz
[
 {"q": "Why call $request->session()->regenerate() after login?", "options": ["To speed up the app", "To prevent session fixation attacks", "To log out other devices", "It's optional decoration"], "answer": 1, "why": "Regenerating the session ID protects against fixation."},
 {"q": "Which middleware only lets logged-in users through?", "options": ["guest", "auth", "verified", "csrf"], "answer": 1, "why": "auth redirects guests to the login route."},
 {"q": "What does redirect()->intended('/dashboard') do?", "options": ["Always goes to /dashboard", "Goes to the page the user originally wanted, or /dashboard", "Logs the user out", "Shows a 404"], "answer": 1, "why": "intended() remembers the URL that triggered the login redirect."}
]
```

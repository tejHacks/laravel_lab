=== FILE: validation.md ===
---
title: Validation
summary: Never trust user input. Validate it.
minutes: 10
---
Every piece of user input must be checked before you save it. Laravel makes this one line.

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title'   => ['required', 'string', 'max:120'],
        'email'   => ['required', 'email', 'unique:users,email'],
        'age'     => ['nullable', 'integer', 'between:13,120'],
        'due_on'  => ['nullable', 'date', 'after_or_equal:today'],
        'tags'    => ['array', 'max:5'],
        'tags.*'  => ['string', 'distinct'],
        'avatar'  => ['nullable', 'image', 'max:2048'],   // KB
    ]);

    Task::create($validated);   // only validated fields
}
```

## What happens when validation fails?

- **Web request**: Laravel redirects **back** with the errors and the old input. Show them with `@error` and `old()`.
- **JSON / API request**: Laravel returns **422 Unprocessable Content** with the errors as JSON.

```blade
@if ($errors->any())
    <ul class="errors">
        @foreach ($errors->all() as $error) <li>{{ $error }}</li> @endforeach
    </ul>
@endif

<input name="title" value="{{ old('title') }}" @class(['invalid' => $errors->has('title')])>
@error('title') <small>{{ $message }}</small> @enderror
```

## Useful rules

`required`, `nullable`, `string`, `integer`, `numeric`, `boolean`, `email`, `url`, `min`, `max`, `between`, `in:a,b,c`, `confirmed` (needs `password_confirmation`), `same`, `different`, `date`, `before`, `after`, `exists:table,column`, `unique:table,column`, `regex`, `file`, `image`, `mimes:pdf,docx`.

## Rule objects

```php
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Password;

'status'   => ['required', Rule::in(['draft', 'published'])],
'email'    => ['required', 'email', Rule::unique('users')->ignore($user->id)],
'password' => ['required', 'confirmed', Password::min(8)->letters()->numbers()],
```

## Custom messages

```php
$request->validate(
    ['title' => 'required'],
    ['title.required' => 'Please give your task a title.']
);
```

:::warning
Use `$validated` (the return value) or `$request->validated()`, never `$request->all()`, when saving. That way only checked fields reach the database.
:::

```quiz
[
 {"q": "What does a failed validation return for an API (JSON) request?", "options": ["A redirect", "422 with JSON errors", "500", "200 with errors"], "answer": 1, "why": "JSON requests get a 422 response listing the errors."},
 {"q": "Which rule requires a matching password_confirmation field?", "options": ["same", "confirmed", "match", "equals"], "answer": 1, "why": "'confirmed' expects {field}_confirmation."},
 {"q": "How do you ignore the current user in a unique email rule when editing?", "options": ["unique:users,email,skip", "Rule::unique('users')->ignore($user->id)", "unique:except", "You can't"], "answer": 1, "why": "Rule::unique(...)->ignore($id) excludes that row."}
]
```

=== FILE: form-requests.md ===
---
title: Form Requests
summary: Move validation and authorization into dedicated classes.
minutes: 8
---
When validation grows, move it out of the controller into a **Form Request**.

```bash
php artisan make:request StoreTaskRequest
```

```php
namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\StopOnFirstFailure;
use Illuminate\Foundation\Http\FormRequest;

#[StopOnFirstFailure]   // Laravel 13 attribute: stop after the first failing rule
class StoreTaskRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;   // or: $this->user()->can('create', Task::class)
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:120'],
            'category_id' => ['nullable', 'exists:categories,id'],
            'due_on' => ['nullable', 'date'],
        ];
    }

    public function messages(): array
    {
        return ['title.required' => 'Every task needs a title.'];
    }

    protected function prepareForValidation(): void
    {
        $this->merge(['title' => trim((string) $this->title)]);
    }
}
```

Type-hint it in the controller. It is validated **before** your method runs:

```php
public function store(StoreTaskRequest $request)
{
    Task::create($request->validated());

    return to_route('tasks.index')->with('status', 'Task created!');
}
```

:::tip
Other Laravel 13 form-request attributes include `#[ErrorBag('login')]` (a named error bag) and `#[RedirectTo('/somewhere')]` (where to go when validation fails).
:::

```quiz
[
 {"q": "When does a Form Request validate?", "options": ["After the controller method", "Before the controller method runs", "Only on save()", "Never automatically"], "answer": 1, "why": "Laravel resolves and validates it before calling your method."},
 {"q": "What should authorize() return to allow the request?", "options": ["null", "true", "'yes'", "200"], "answer": 1, "why": "Returning false gives a 403 Forbidden response."}
]
```

=== FILE: sessions-and-flash.md ===
---
title: Sessions & Flash Messages
summary: Remember data between requests and show one-time messages.
minutes: 6
---
HTTP is **stateless**: every request is independent. A **session** lets you remember things between requests (who is logged in, a shopping cart, preferences).

```php
// Store
session(['theme' => 'dark']);
$request->session()->put('cart', $items);
$request->session()->push('cart', $newItem);

// Read
$theme = session('theme', 'light');     // default 'light'
$cart = $request->session()->get('cart', []);

// Remove
$request->session()->forget('cart');
```

## Flash data: available for the next request only

Perfect for "Saved!" messages after a redirect:

```php
return redirect()->route('tasks.index')->with('status', 'Task saved!');
```

```blade
@session('status')
    <div class="alert success">{{ $value }}</div>
@endsession
```

## Where are sessions stored?

`SESSION_DRIVER` in `.env`: `database` (the default in new apps), `file`, `cookie`, `redis` and others.

:::analogy
A session is like a coat-check ticket. The browser keeps a small cookie (the ticket) and the server keeps the coat (the data).
:::

```quiz
[
 {"q": "How long does flashed data last?", "options": ["Forever", "Until logout", "Only the next request", "One hour"], "answer": 2, "why": "Flash data is removed after the next request."},
 {"q": "Which directive shows a flashed 'status' message?", "options": ["@flash('status')", "@session('status')", "@status", "@message"], "answer": 1, "why": "@session('key') ... @endsession exposes $value."}
]
```

=== FILE: authentication.md ===
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

=== FILE: middleware.md ===
---
title: Middleware
summary: Filter and modify requests before they reach your controllers.
minutes: 8
---
**Middleware** wraps your routes. Each one can inspect the request, stop it, or change the response.

## Built-in middleware you'll use

| Alias | What it does |
|---|---|
| `auth` | Requires a logged-in user |
| `guest` | Only for logged-out users |
| `verified` | Requires a verified email |
| `throttle:60,1` | Rate limit: 60 requests per minute |
| `signed` | Requires a valid signed URL |
| `can:update,post` | Authorization check |

## Write your own

```bash
php artisan make:middleware EnsureUserIsAdmin
```

```php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsAdmin
{
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->is_admin) {
            abort(403, 'Admins only.');
        }

        return $next($request);   // continue to the next layer
    }
}
```

## Register it (bootstrap/app.php)

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias(['admin' => EnsureUserIsAdmin::class]);

    // or add to every web request:
    // $middleware->web(append: [TrackLastSeen::class]);
})
```

```php
Route::middleware(['auth', 'admin'])->prefix('admin')->group(function () {
    Route::get('/', AdminDashboard::class);
});
```

## After middleware

```php
public function handle(Request $request, Closure $next): Response
{
    $response = $next($request);                         // run the app first
    $response->headers->set('X-Frame-Options', 'DENY');  // then modify the response
    return $response;
}
```

```quiz
[
 {"q": "What does `return $next($request);` do?", "options": ["Stops the request", "Passes the request to the next layer", "Redirects home", "Logs the user in"], "answer": 1, "why": "$next continues down the middleware pipeline."},
 {"q": "Where do you register a middleware alias in Laravel 13?", "options": ["app/Http/Kernel.php", "bootstrap/app.php", "config/app.php", "routes/web.php"], "answer": 1, "why": "Since Laravel 11, middleware is configured in bootstrap/app.php."},
 {"q": "What does throttle:60,1 mean?", "options": ["60 users max", "60 requests per 1 minute", "Wait 60 seconds", "1 request per 60 minutes"], "answer": 1, "why": "maxAttempts,decayMinutes."}
]
```

=== FILE: authorization.md ===
---
title: Authorization: Gates & Policies
summary: Decide what a logged-in user is allowed to do.
minutes: 9
---
**Authentication** = who are you? **Authorization** = what are you allowed to do?

## Gates (simple checks)

```php
// app/Providers/AppServiceProvider.php
use Illuminate\Support\Facades\Gate;

public function boot(): void
{
    Gate::define('view-reports', fn (User $user) => $user->is_admin);
}
```

```php
Gate::authorize('view-reports');          // throws 403 if denied
if ($request->user()->can('view-reports')) { ... }
```

## Policies (rules for one model)

```bash
php artisan make:policy TaskPolicy --model=Task
```

```php
class TaskPolicy
{
    public function update(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }

    public function delete(User $user, Task $task): bool
    {
        return $user->id === $task->user_id || $user->is_admin;
    }
}
```

Laravel finds `TaskPolicy` for `Task` automatically through naming conventions.

```php
public function update(UpdateTaskRequest $request, Task $task)
{
    Gate::authorize('update', $task);   // 403 if not the owner
    $task->update($request->validated());
    // ...
}
```

```php
Route::put('/tasks/{task}', ...)->can('update', 'task');
```

```blade
@can('delete', $task)
    <button>Delete</button>
@endcan
```

:::tip
Hiding a button with `@can` is only cosmetic. **Always** check in the controller too, because users can send requests without your UI.
:::

```quiz
[
 {"q": "What's the difference between authentication and authorization?", "options": ["They're the same", "Who you are vs what you may do", "Login vs logout", "Passwords vs tokens"], "answer": 1, "why": "Authentication identifies the user; authorization checks permissions."},
 {"q": "What does Gate::authorize('update', $task) do when denied?", "options": ["Returns false", "Throws, giving a 403 response", "Logs out", "Redirects to login"], "answer": 1, "why": "authorize throws an AuthorizationException, rendered as 403."},
 {"q": "Is @can in Blade enough to secure an action?", "options": ["Yes", "No, also check on the server", "Only for admins", "Only in production"], "answer": 1, "why": "UI checks are cosmetic; enforce permissions server-side."}
]
```

=== FILE: file-uploads.md ===
---
title: File Uploads & Storage
summary: Accept uploads, store them on disks, and serve them.
minutes: 8
---
```blade
<form method="POST" action="/avatar" enctype="multipart/form-data">
    @csrf
    <input type="file" name="avatar" accept="image/*">
    <button>Upload</button>
</form>
```

:::warning
Without `enctype="multipart/form-data"` the file is never sent.
:::

```php
public function update(Request $request)
{
    $request->validate(['avatar' => ['required', 'image', 'max:2048']]);   // 2 MB

    $path = $request->file('avatar')->store('avatars', 'public');
    // e.g. "avatars/Xk3j9...png" (a random, safe file name)

    $request->user()->update(['avatar_path' => $path]);

    return back()->with('status', 'Avatar updated!');
}
```

## Disks

`config/filesystems.php` defines **disks**: `local` (private), `public` (web-accessible), `s3` (cloud). Code stays the same, so you can switch to S3 later by changing config.

```bash
php artisan storage:link   # makes storage/app/public available at /storage
```

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('public')->url($path);        // /storage/avatars/...
Storage::disk('public')->delete($oldPath);
Storage::put('reports/today.txt', 'Hello'); // write a file
Storage::download('reports/today.txt');      // force a download
```

```blade
<img src="{{ Storage::url($user->avatar_path) }}" alt="Avatar">
```

```quiz
[
 {"q": "Which form attribute is required for uploads?", "options": ["method=\"FILE\"", "enctype=\"multipart/form-data\"", "upload=\"true\"", "accept=\"*\""], "answer": 1, "why": "Browsers only send files with multipart/form-data encoding."},
 {"q": "What does php artisan storage:link do?", "options": ["Uploads to S3", "Links public/storage to storage/app/public", "Deletes old files", "Compresses images"], "answer": 1, "why": "It creates a symlink so public files can be served."}
]
```

=== FILE: mail-and-notifications.md ===
---
title: Mail & Notifications
summary: Send emails and multi-channel notifications.
minutes: 9
---
## Mailables

```bash
php artisan make:mail WelcomeMail --markdown=mail.welcome
```

```php
class WelcomeMail extends Mailable
{
    use Queueable, SerializesModels;

    public function __construct(public User $user) {}

    public function envelope(): Envelope
    {
        return new Envelope(subject: "Welcome, {$this->user->name}!");
    }

    public function content(): Content
    {
        return new Content(markdown: 'mail.welcome');
    }
}
```

```blade
{{-- resources/views/mail/welcome.blade.php --}}
<x-mail::message>
# Welcome aboard, {{ $user->name }}!

<x-mail::button :url="route('dashboard')">Open your dashboard</x-mail::button>

Thanks,<br>{{ config('app.name') }}
</x-mail::message>
```

```php
Mail::to($user)->send(new WelcomeMail($user));
Mail::to($user)->queue(new WelcomeMail($user));   // send in the background
```

:::tip
In development set `MAIL_MAILER=log`. Emails are written to `storage/logs/laravel.log` instead of being sent. Tools like Mailpit or Herd's mail viewer show them in a browser.
:::

## Notifications (email, database, SMS, Slack...)

```bash
php artisan make:notification OrderShipped
```

```php
class OrderShipped extends Notification
{
    public function __construct(public Order $order) {}

    public function via(object $notifiable): array
    {
        return ['mail', 'database'];
    }

    public function toMail(object $notifiable): MailMessage
    {
        return (new MailMessage)
            ->subject('Your order has shipped')
            ->line("Order #{$this->order->id} is on its way.")
            ->action('Track order', url("/orders/{$this->order->id}"));
    }

    public function toArray(object $notifiable): array
    {
        return ['order_id' => $this->order->id];
    }
}

$user->notify(new OrderShipped($order));
$user->unreadNotifications;   // stored by the 'database' channel
```

```quiz
[
 {"q": "Which mailer writes emails to the log file?", "options": ["smtp", "log", "array", "ses"], "answer": 1, "why": "MAIL_MAILER=log is ideal during development."},
 {"q": "What does via() return in a notification?", "options": ["The recipient", "The channels to send through", "The subject", "A view"], "answer": 1, "why": "via() lists channels such as mail, database or broadcast."}
]
```

=== FILE: queues-and-jobs.md ===
---
title: Queues & Jobs
summary: Run slow work in the background so pages stay fast.
minutes: 9
---
Some work is slow: sending email, resizing images, calling other APIs, generating PDFs. Don't make the user wait. Push it onto a **queue** and let a **worker** process it in the background.

```bash
php artisan make:job ProcessPodcast
```

```php
use Illuminate\Queue\Attributes\Timeout;
use Illuminate\Queue\Attributes\Tries;

#[Tries(3)]        // Laravel 13 attributes
#[Timeout(120)]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    public function __construct(public Podcast $podcast) {}

    public function handle(AudioProcessor $processor): void
    {
        $processor->process($this->podcast);
    }

    public function failed(?Throwable $e): void
    {
        // notify someone, clean up...
    }
}
```

```php
ProcessPodcast::dispatch($podcast);                          // as soon as possible
ProcessPodcast::dispatch($podcast)->delay(now()->addMinutes(5));
ProcessPodcast::dispatch($podcast)->onQueue('audio');
```

## Run a worker

```bash
php artisan queue:work        # keep running and process jobs
php artisan queue:failed      # list failed jobs
php artisan queue:retry all
```

New apps use `QUEUE_CONNECTION=database`, so jobs are stored in the `jobs` table with no extra services. Redis or SQS are faster in production.

:::tip
`composer run dev` starts a queue worker alongside the web server, so jobs run automatically while you develop.
:::

:::warning
In production, keep `queue:work` running with a process manager such as **Supervisor**, and restart workers after each deploy with `php artisan queue:restart`.
:::

```quiz
[
 {"q": "Why use queues?", "options": ["To store data", "To run slow work in the background", "To speed up the database", "For routing"], "answer": 1, "why": "Queues keep responses fast by deferring slow tasks."},
 {"q": "Which command processes queued jobs?", "options": ["php artisan queue:work", "php artisan jobs:run", "php artisan serve --queue", "composer queue"], "answer": 0, "why": "queue:work starts a worker."},
 {"q": "What does #[Tries(3)] on a job mean?", "options": ["Runs 3 times always", "Retries up to 3 attempts if it fails", "3 workers", "Waits 3 seconds"], "answer": 1, "why": "The job may be attempted up to 3 times."}
]
```

=== FILE: events-and-listeners.md ===
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

=== FILE: artisan-commands.md ===
---
title: Custom Commands & Scheduling
summary: Write your own Artisan commands and run them on a schedule.
minutes: 8
---
```bash
php artisan make:command SendDailyReport
```

```php
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;

#[Signature('reports:daily {--email= : Send to this address}')]
#[Description('Email yesterday\'s sales report')]
class SendDailyReport extends Command
{
    public function handle(): int
    {
        $total = Order::whereDate('created_at', today()->subDay())->sum('total');
        $this->info("Yesterday's sales: {$total}");

        if ($email = $this->option('email')) {
            // Mail::to($email)->send(...)
            $this->line("Sent to {$email}");
        }

        return self::SUCCESS;
    }
}
```

```bash
php artisan reports:daily --email=boss@example.com
```

Commands can also `ask()`, `confirm()`, `choice()`, show `table()`s and progress bars.

## Scheduling (routes/console.php)

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('reports:daily')->dailyAt('08:00');
Schedule::command('queue:prune-failed')->weekly();
Schedule::call(fn () => Cart::abandoned()->delete())->hourly();
```

Then add **one** cron entry on the server:

```bash
* * * * * cd /path/to/app && php artisan schedule:run >> /dev/null 2>&1
```

```bash
php artisan schedule:list     # see what's scheduled
php artisan schedule:work     # run the scheduler locally
```

```quiz
[
 {"q": "Where are scheduled tasks defined in Laravel 13?", "options": ["app/Console/Kernel.php", "routes/console.php", "config/schedule.php", "crontab only"], "answer": 1, "why": "Schedules live in routes/console.php."},
 {"q": "How many cron entries does the scheduler need?", "options": ["One per task", "Exactly one (schedule:run every minute)", "None", "Two"], "answer": 1, "why": "A single cron calls schedule:run every minute."}
]
```

=== FILE: testing.md ===
---
title: Testing
summary: Feature and unit tests with PHPUnit or Pest.
minutes: 10
---
Tests prove your app works and let you change code without fear. Laravel supports **PHPUnit** and **Pest**, and you choose when creating the project.

```bash
php artisan make:test TaskTest          # feature test
php artisan make:test PriceTest --unit  # unit test
php artisan test                        # run everything
php artisan test --filter=TaskTest
```

## Feature test (PHPUnit)

```php
namespace Tests\Feature;

use App\Models\Task;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class TaskTest extends TestCase
{
    use RefreshDatabase;   // fresh database for every test

    public function test_guests_are_redirected_to_login(): void
    {
        $this->get('/tasks')->assertRedirect('/login');
    }

    public function test_user_can_create_a_task(): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)
            ->post('/tasks', ['title' => 'Write tests'])
            ->assertRedirect('/tasks')
            ->assertSessionHas('status');

        $this->assertDatabaseHas('tasks', ['title' => 'Write tests']);
    }

    public function test_title_is_required(): void
    {
        $this->actingAs(User::factory()->create())
            ->post('/tasks', ['title' => ''])
            ->assertSessionHasErrors('title');
    }
}
```

## The same test in Pest

```php
it('creates a task', function () {
    $user = User::factory()->create();

    $this->actingAs($user)->post('/tasks', ['title' => 'Write tests'])
        ->assertRedirect('/tasks');

    expect(Task::count())->toBe(1);
});
```

## Faking things

```php
Mail::fake();
Queue::fake();
Storage::fake('public');
Http::fake(['api.example.com/*' => Http::response(['ok' => true])]);

// ...run code...

Mail::assertSent(WelcomeMail::class);
Queue::assertPushed(ProcessPodcast::class);
```

:::tip
Tests run against an in-memory SQLite database (see `phpunit.xml`), so they're fast and never touch your real data.
:::

```quiz
[
 {"q": "What does RefreshDatabase do?", "options": ["Deletes production data", "Gives each test a clean database", "Speeds up queries", "Seeds fake users"], "answer": 1, "why": "It migrates and rolls back so tests don't affect each other."},
 {"q": "How do you act as a logged-in user in a test?", "options": ["$this->login($user)", "$this->actingAs($user)", "Auth::fake()", "$this->user = $user"], "answer": 1, "why": "actingAs() authenticates the user for the request."},
 {"q": "What does Mail::fake() do?", "options": ["Sends real email", "Captures mail so you can assert on it", "Disables mail forever", "Logs mail"], "answer": 1, "why": "Fakes record what would have been sent."}
]
```

=== FILE: deployment.md ===
---
title: Deployment
summary: Put your Laravel app on the internet safely.
minutes: 9
---
## Hosting options

- **Laravel Cloud**: fully managed by the Laravel team. Connect GitHub and deploy.
- **Laravel Forge**: provisions and manages your own servers (DigitalOcean, AWS, Hetzner...).
- **A VPS by hand**: Nginx + PHP-FPM + MySQL/PostgreSQL + Supervisor.
- **Shared hosting**: possible, but you lose queues and SSH conveniences.

## Production checklist

```dotenv
APP_ENV=production
APP_DEBUG=false            # NEVER true in production: it leaks secrets!
APP_URL=https://myapp.com
LOG_LEVEL=error
```

```bash
composer install --no-dev --optimize-autoloader
php artisan migrate --force
php artisan optimize            # caches config, routes, views and events
php artisan storage:link
php artisan queue:restart       # reload workers with the new code
```

## Keep things running

- **Queue workers** with Supervisor: `php artisan queue:work --tries=3`
- **Scheduler** cron: `* * * * * php artisan schedule:run`
- **HTTPS**: free certificates from Let's Encrypt
- **Backups**: database dumps stored off-server
- **Monitoring**: Laravel Pulse, Nightwatch, Sentry or Flare

## Zero-downtime deploys

Forge, Cloud and tools such as Envoyer build the new release in a separate folder and switch a symlink, so visitors never see a half-deployed site.

:::warning
`APP_DEBUG=true` in production shows full error pages including environment variables, which exposes your database password and keys to anyone.
:::

```quiz
[
 {"q": "What must APP_DEBUG be in production?", "options": ["true", "false", "verbose", "It doesn't matter"], "answer": 1, "why": "Debug pages leak secrets; always false in production."},
 {"q": "Which flag do you need to migrate in production?", "options": ["--prod", "--force", "--yes", "--safe"], "answer": 1, "why": "migrate asks for confirmation in production; --force skips it."},
 {"q": "What does php artisan optimize do?", "options": ["Compresses images", "Caches config, routes, views and events", "Upgrades Laravel", "Cleans the database"], "answer": 1, "why": "It builds the framework caches for faster boot."}
]
```

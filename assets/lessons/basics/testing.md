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

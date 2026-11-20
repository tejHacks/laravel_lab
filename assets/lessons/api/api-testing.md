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

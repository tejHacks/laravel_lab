---
title: Factories & Seeders
summary: Generate realistic fake data for development and tests.
minutes: 7
---
## Factories

A **factory** describes how to make a fake model:

```php
// database/factories/TaskFactory.php
class TaskFactory extends Factory
{
    public function definition(): array
    {
        return [
            'title' => fake()->sentence(4),
            'notes' => fake()->optional()->paragraph(),
            'done' => fake()->boolean(30),
            'due_on' => fake()->dateTimeBetween('-1 week', '+2 weeks'),
        ];
    }

    public function done(): static
    {
        return $this->state(['done' => true]);
    }
}
```

```php
Task::factory()->create();                     // 1 saved task
Task::factory()->count(20)->create();
Task::factory()->done()->make();               // not saved
Category::factory()->has(Task::factory()->count(5))->create();
```

## Seeders

```php
// database/seeders/DatabaseSeeder.php
public function run(): void
{
    User::factory()->create(['name' => 'Test User', 'email' => 'test@example.com']);

    Category::factory()
        ->count(4)
        ->has(Task::factory()->count(6))
        ->create();
}
```

```bash
php artisan db:seed
php artisan migrate:fresh --seed   # rebuild + seed (development)
php artisan make:seeder CategorySeeder
```

:::tip
`fake()` is powered by FakerPHP: names, emails, addresses, prices, dates, paragraphs, UUIDs and much more.
:::

```quiz
[
 {"q": "What does factory()->make() do?", "options": ["Creates and saves", "Builds a model without saving it", "Deletes", "Seeds the database"], "answer": 1, "why": "make() builds in memory; create() also saves."},
 {"q": "Which command rebuilds the schema and runs seeders?", "options": ["db:seed --fresh", "migrate:fresh --seed", "seed:all", "migrate --refresh"], "answer": 1, "why": "migrate:fresh --seed drops, migrates and seeds."}
]
```

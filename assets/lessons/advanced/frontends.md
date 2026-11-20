---
title: Front-ends: Blade, Livewire & Inertia
summary: Choose how to build the UI of a Laravel app.
minutes: 8
---
Laravel supports several ways to build the front end. The official **starter kits** (chosen during `laravel new`) set each one up with authentication included.

## Blade only

Server-rendered HTML. Simple, fast, great SEO. Add **Alpine.js** for small interactions.

## Livewire

Write dynamic, reactive components **in PHP**. No separate JavaScript app.

```php
class Counter extends Component
{
    public int $count = 0;

    public function increment(): void
    {
        $this->count++;
    }

    public function render()
    {
        return view('livewire.counter');
    }
}
```

```blade
<div>
    <h1>{{ $count }}</h1>
    <button wire:click="increment">+</button>
</div>
```

## Inertia (React, Vue or Svelte)

Build pages as React or Vue components, but keep Laravel routing and controllers. No separate API needed.

```php
return Inertia::render('Tasks/Index', ['tasks' => TaskResource::collection(Task::all())]);
```

## Separate SPA or mobile app + API

A Next.js or Nuxt front end, or a **Flutter** app, talking to a Laravel **API** with Sanctum. Choose this when several clients share one backend.

| Choose | When |
|---|---|
| Blade + Alpine | Content sites, admin panels, simple apps |
| Livewire | You love PHP and want interactivity |
| Inertia | Your team knows React or Vue |
| API + Flutter | Mobile apps (and maybe a web app too) |

```quiz
[
 {"q": "Which option lets you build reactive UIs mostly in PHP?", "options": ["Inertia", "Livewire", "Vue", "jQuery"], "answer": 1, "why": "Livewire components are PHP classes with Blade views."},
 {"q": "What should a Flutter app talk to?", "options": ["Blade views", "A Laravel API (JSON + Sanctum)", "Livewire", "Inertia pages"], "answer": 1, "why": "Mobile apps consume JSON APIs."}
]
```

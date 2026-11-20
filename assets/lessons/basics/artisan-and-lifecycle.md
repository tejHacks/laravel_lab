---
title: Artisan & the Request Lifecycle
summary: The command-line tool you will use every day, and what happens on each request.
minutes: 7
---
**Artisan** is Laravel's command-line tool. It generates files, runs migrations, clears caches and much more.

```bash
php artisan list                 # every available command
php artisan make:controller PostController
php artisan make:model Post -mfs # model + migration + factory + seeder
php artisan migrate              # run database migrations
php artisan route:list           # show all routes
php artisan tinker               # interactive PHP shell for your app
php artisan about                # environment overview
php artisan optimize:clear       # clear all caches
```

:::tip
Add `--help` to any command, for example `php artisan make:model --help`, to see its options.
:::

## Tinker: play with your app

```bash
php artisan tinker
> User::count()
= 3
> User::first()->name
= "Ada"
```

## The request lifecycle

1. The web server sends the request to `public/index.php`.
2. Laravel boots: it loads config and **service providers**.
3. The request passes through **global middleware** (trimming strings, maintenance mode and so on).
4. The **router** finds the matching route and runs its middleware (for example `auth`).
5. The **controller** runs and returns a response.
6. The response travels back out through the middleware to the browser.

:::analogy
Middleware are like security checkpoints at an airport. Every passenger (request) passes through them on the way to the gate (controller), and they can stop anyone who isn't allowed through.
:::

```quiz
[
 {"q": "Which command lists every route?", "options": ["php artisan routes", "php artisan route:list", "php artisan list:routes", "composer routes"], "answer": 1, "why": "route:list prints every registered route."},
 {"q": "What does `make:model Post -m` also create?", "options": ["A controller", "A migration", "A view", "A test"], "answer": 1, "why": "-m creates a migration (-f factory, -s seeder, -c controller)."},
 {"q": "What runs before the controller and can block a request?", "options": ["Views", "Migrations", "Middleware", "Seeders"], "answer": 2, "why": "Middleware inspect requests before they reach controllers."}
]
```

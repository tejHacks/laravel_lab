---
title: What is Laravel?
summary: The PHP framework for web apps and APIs, and why developers love it.
minutes: 6
---
**Laravel** is a free, open-source **PHP framework** for building web applications and APIs. A framework gives you a ready-made structure plus tools for the things almost every app needs: routing URLs, talking to a database, logging users in, sending email, validating forms, running background jobs and much more.

:::analogy
Building a web app from scratch is like building a house by first making your own bricks. Laravel hands you quality bricks, plumbing and wiring, so you can focus on designing the house.
:::

## What can you build?

- Websites and web apps (dashboards, shops, blogs, SaaS products)
- **REST APIs** for mobile apps (Flutter, React Native, iOS, Android)
- Admin panels, internal tools, background workers and scheduled tasks

## How a Laravel app works

1. A browser or mobile app sends an **HTTP request** (for example `GET /products`).
2. Laravel's **router** matches the URL to a **route**.
3. The route calls a **controller** method (or a closure).
4. The controller uses **models** to read or write the **database**.
5. It returns a **response**: an HTML page (a **Blade view**) or **JSON**.

This pattern is called **MVC**: **M**odel (data), **V**iew (what the user sees), **C**ontroller (the logic in between).

```php
// routes/web.php
Route::get('/hello', function () {
    return 'Hello from Laravel!';
});
```

## Why Laravel?

- **Elegant syntax**: code that reads almost like English.
- **Batteries included**: auth, queues, mail, caching, testing and file storage are built in.
- **Eloquent ORM**: work with database rows as PHP objects.
- **Artisan CLI**: generate code and run tasks from the terminal.
- **Huge ecosystem**: starter kits, Livewire, Inertia, Forge, Vapor, Cloud, Herd.

:::note
This course targets **Laravel 13**, which needs **PHP 8.3 or newer**. Laravel ships a new major version roughly once a year, and upgrades between versions are usually small.
:::

```quiz
[
 {"q": "Which language is Laravel written in?", "options": ["JavaScript", "Python", "PHP", "Dart"], "answer": 2, "why": "Laravel is a PHP framework."},
 {"q": "In MVC, what does the Controller do?", "options": ["Stores data", "Handles the logic between request, data and response", "Styles the page", "Runs the database"], "answer": 1, "why": "Controllers receive requests, use models and return responses."},
 {"q": "What minimum PHP version does Laravel 13 require?", "options": ["7.4", "8.0", "8.3", "9.0"], "answer": 2, "why": "Laravel 13 requires PHP ^8.3."}
]
```

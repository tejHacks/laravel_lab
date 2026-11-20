---
title: Route Parameters & Named Routes
summary: Dynamic URLs, optional parameters, constraints and URL helpers.
minutes: 8
---
## Required parameters

```php
Route::get('/users/{id}', function (string $id) {
    return "User #$id";
});

Route::get('/posts/{post}/comments/{comment}', function (string $post, string $comment) {
    return "Comment $comment on post $post";
});
```

## Optional parameters

```php
Route::get('/hello/{name?}', function (?string $name = 'stranger') {
    return "Hello, $name!";
});
```

## Constraints

```php
Route::get('/users/{id}', ...)->whereNumber('id');
Route::get('/tags/{slug}', ...)->where('slug', '[a-z0-9-]+');
Route::get('/lang/{code}', ...)->whereIn('code', ['en', 'fr', 'yo']);
```

## Named routes

Give routes names, then generate URLs from the name. If the URL changes later, the links keep working.

```php
Route::get('/user/profile', ProfileController::class)->name('profile');

$url = route('profile');                        // http://app.test/user/profile
return redirect()->route('profile');

Route::get('/posts/{post}', ...)->name('posts.show');
route('posts.show', ['post' => 42]);            // /posts/42
```

## Route model binding

Type-hint a model and Laravel fetches the row for you, returning a 404 if it doesn't exist:

```php
use App\Models\Post;

Route::get('/posts/{post}', function (Post $post) {
    return $post->title;          // $post is already loaded from the database
});

// Bind by a different column
Route::get('/posts/{post:slug}', fn (Post $post) => $post);
```

:::tip
Route model binding removes a lot of repetitive "find or fail" code. It is one of Laravel's best features.
:::

```quiz
[
 {"q": "How do you make a route parameter optional?", "options": ["{name!}", "{name?} with a default value", "{optional:name}", "[name]"], "answer": 1, "why": "Add ? to the parameter and give the function argument a default."},
 {"q": "What does route('posts.show', ['post' => 5]) return?", "options": ["A view", "The URL for that named route", "A redirect", "A Post model"], "answer": 1, "why": "route() generates a URL from a route name."},
 {"q": "With route model binding, what happens if the record doesn't exist?", "options": ["$post is null", "A 404 Not Found response", "A 500 error", "An empty model"], "answer": 1, "why": "Implicit binding returns 404 automatically."}
]
```
